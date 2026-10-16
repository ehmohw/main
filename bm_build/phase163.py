"""2.80d: DENNIS AND PISTACHIO, THE FOLLOWERS - who they become when you've traded with them fifty times (phase162).

DENNIS        DENNIS'S HORN (a horn off his helmet; use it to call him, sneak + use: his menu). A stout fighter with his
              Dwarven wrench and a dwarf's love of gold:
              WRENCH WHACK  up close - the wrench swung overhead and brought down (7, and a shove).
              GOLD RUSH     at range - a fistful of gold nuggets flung (5, and the weight of it slows).
              MIDAS SLAM    when they crowd him - the wrench into the ground, a ring of gold bursting out (9 to all near, up they go).
              MOTHER LODE   his great blow (every 45 s) - the ground splits and gold pours up round him (14 to all near), and
                            you're clad in it a while (Absorption, Resistance).
              PASSIVE       FORTUNE V on every ore you mine while he's with you (phase162's loot tables).
PISTACHIO     PISTACHIO'S LITTLE CLOCHE (a silver cloche the size of a thimble). Ghastly to fight beside:
              SPECTRAL SLAP up close - a cold glove across the face (4, and Weakness).
              THE NEXT COURSE at range - he lifts his cloche's lid and a spirit flies out at them (6, they glow); and you,
                            light of foot a moment (Speed).
              THE WAIL      when they crowd him - a shriek from beyond (4 to all near, slowed and weakened).
              THE LAST COURSE his great one (every 45 s) - the lid off, every spirit at once (12 to all near, lifted off the
                            ground), and a GHOSTLY WARD on you (Resistance II, Regeneration).
              PHANTOM ESCAPE  when you're low (3 hearts or less), once a minute: you fade from sight and from harm a few
                            seconds (Invisibility, Resistance II, Speed II).
              PASSIVE       LOOTING V on every mob you kill while he's with you.
BOTH          right-click either: sit / stand (sat, an idle of their own). A frame keeps them, a display case shows them as a
              figurine, Cecil sells their dolls, the Tailor their looks (and the auras), the Recruiter their Raid Contracts.
PAIRS         DENNIS + PISTACHIO, "Spade and Spoon": you dig and you loot faster (Haste II, Luck); both tougher.
              CECIL + PISTACHIO, "The Omega Palace" (they share the house): Pistachio feeds you (Saturation every half
              minute) and Cecil mends you (Regeneration); both tougher.
TRIO          EMMA, LEO AND DENNIS, "The Crown's Prospect": a princess, her knight and the dwarf who mines her gold - Strength,
              Resistance and Haste II for you; the three tougher and healing."""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import dennis_art as DA
import pistachio_art as PA
import rigfol as RF
import rigkit as RK
from rigkit import qs
import phase95 as FX
import phase46 as P46
import phase89 as P89
import phase68 as P68
import phase98 as P98
import phase100 as P100
import phase134 as P134
import phase141 as P141
import allies

DW_C, DW_LINE, PI_C, PI_LINE = '#e0a040', '#ffe0b0', '#7ae890', '#d8ffe0'
GOLD = '#ffcf40'
PET_CD = 300
EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
FACE = {'dw': {'happy': 'grin', 'surprised': 'shout', 'hurt': 'hurt', 'sleepy': 'hurt', 'blink': None, 'squint': 'grin', 'serious': 'shout'},
        'pi': {'happy': 'happy', 'surprised': 'shock', 'hurt': 'squint', 'sleepy': 'squint', 'blink': 'squint', 'squint': 'squint', 'serious': None}}


class DArt:
    PIVOT, PARENT, PARTS, PART_K, PREFIX = DA.PIVOT, DA.PARENT, DA.PARTS, DA.PART_K, DA.PREFIX
    HIDDEN = staticmethod(DA.HIDDEN)
    model_name = staticmethod(DA.model_name)


class PArt:
    PIVOT, PARENT, PARTS, PART_K, PREFIX = PA.PIVOT, PA.PARENT, PA.PARTS, PA.PART_K, PA.PREFIX
    HIDDEN = staticmethod(PA.HIDDEN)
    model_name = staticmethod(PA.model_name)


# ------------------------------------------------------------------------------------------------ the followers' poses
dl, pl = DA.limb, PA.limb
P = dict
POSES_DENNIS = {k: dict(v) for k, v in DA.POSES.items()}
POSES_DENNIS.update({
    'run_a': P(DA.POSES['walk_a'], _off=(0, 0.45, 0), body=qs(('z', 4), ('x', 8)), legr=dl(1, 40), legl=dl(-1, -36), armr=dl(1, -24, 6), arml=dl(-1, 32, 6)),
    'run_b': P(DA.POSES['walk_b'], _off=(0, 0.45, 0), body=qs(('z', -4), ('x', 8)), legr=dl(1, -36), legl=dl(-1, 40), armr=dl(1, 28, 6), arml=dl(-1, -24, 6)),
    'air': P(DA.POSES['shock'], _face=None, legr=dl(1, 20), legl=dl(-1, -10)),
    'sit_b': P(DA.POSES['sit'], head=qs(('y', -10), ('x', 6)), arml=dl(-1, 30, 10), forel=dl(-1, 70)),
    'paddle_a': P(_off=(0, -1.6, 0), body=qs(('x', 30)), armr=dl(1, 120, 30), arml=dl(-1, 40, 30), legr=dl(1, 20), legl=dl(-1, -20)),
    'paddle_b': P(_off=(0, -1.4, 0), body=qs(('x', 30)), armr=dl(1, 40, 30), arml=dl(-1, 120, 30), legr=dl(1, -20), legl=dl(-1, 20)),
    'swing_back': P(_face='shout', body=qs(('y', 16), ('x', -6)), armr=dl(1, 168, 14), forer=dl(1, 30), arml=dl(-1, 20, 10), forel=dl(-1, 30)),
    'swing': P(_face='shout', body=qs(('y', -16), ('x', 12)), armr=dl(1, 60, -4), forer=dl(1, 10), arml=dl(-1, -20, 10), forel=dl(-1, 20), legr=dl(1, -10), legl=dl(-1, 16)),
    'toss': P(_face='grin', body=qs(('y', -12)), arml=dl(-1, 120, 16), forel=dl(-1, 10), armr=dl(1, -10, 8), forer=dl(1, 20)),
    'slam_up': P(_face='shout', _off=(0, 0.6, 0), body=qs(('x', -10)), armr=dl(1, 176, 2), forer=dl(1, 10), arml=dl(-1, 150, 20), forel=dl(-1, 20)),
    'slam': P(_face='shout', _off=(0, -0.9, 0), body=qs(('x', 26)), head=qs(('x', -10)), armr=dl(1, 70, 4), forer=dl(1, 10), arml=dl(-1, 40, 20),
              forel=dl(-1, 30), legr=dl(1, -24, 8), legl=dl(-1, 30, 8)),
    'ult': P(_face='grin', _off=(0, 0.9, 0), head=qs(('x', -18)), armr=dl(1, 130, 50), forer=dl(1, 10), arml=dl(-1, 130, 50), forel=dl(-1, 10))})
POSES_PISTACHIO = {k: dict(v) for k, v in PA.POSES.items()}
H = PA.HOVER
POSES_PISTACHIO.update({
    'run_a': P(PA.POSES['walk_a'], body=qs(('x', 20)), tail=qs(('x', 34), ('y', 16))),
    'run_b': P(PA.POSES['walk_b'], body=qs(('x', 22)), tail=qs(('x', 40), ('y', -16))),
    'air': P(PA.POSES['idle_b']),
    'sit_b': P(PA.POSES['sit'], head=qs(('y', -10), ('z', 4)), tail=qs(('x', -44), ('y', 40)), arml=pl(-1, 30, 10), forel=pl(-1, 60)),
    'paddle_a': P(PA.POSES['walk_a']), 'paddle_b': P(PA.POSES['walk_b']),
    'slap_back': P(_off=(0, H, 0), body=qs(('y', -18)), arml=pl(-1, 40, -50), forel=pl(-1, 30), head=qs(('y', -10))),
    'slap': P(_face='squint', _off=(0, H, 0), body=qs(('y', 20)), arml=pl(-1, 80, 40), forel=pl(-1, 0), head=qs(('y', 10))),
    'serve': P(PA.POSES['lid_up'], armr=pl(1, 30, 0), forer=pl(1, -10)),
    'wail': P(_face='shock', _off=(0, H + 0.8, 0), head=qs(('x', -22)), arml=pl(-1, 60, 80), forel=pl(-1, 10), armr=pl(1, 10, 30), tail=qs(('x', -30))),
    'ult': P(_face='happy', _off=(0, H + 2.0, 0), lid=qs(('x', -110)), armr=pl(1, 50, 20), arml=pl(-1, 150, 20), forel=pl(-1, 10), head=qs(('x', -14)),
             tail=qs(('x', 30)))})

# ------------------------------------------------------------------------------------------------ the followers, as data
F_ = {
    'dw': dict(w='dennis', name='Dennis', col=DW_C, line=DW_LINE, art=DA, A=DArt, poses=POSES_DENNIS, item='dw_horn', contract='fcontract_dennis',
               doll='doll_dennis', menu=2200, hp=48, armour=8, speed=0.3, kb=0.6, cos='bm.cosdw', host_hp_txt="Dennis's",
               idle=['idle_a', 'idle_b'], head='head'),
    'pi': dict(w='pistachio', name='Pistachio', col=PI_C, line=PI_LINE, art=PA, A=PArt, poses=POSES_PISTACHIO, item='pi_cloche', contract='fcontract_pistachio',
               doll='doll_pistachio', menu=2220, hp=34, armour=4, speed=0.36, kb=0.2, cos='bm.cospi', host_hp_txt="Pistachio's",
               idle=['idle_a', 'idle_b'], head='head'),
}

# ------------------------------------------------------------------------------------------------ items
item('dw_horn', TOTEM, "Dennis's Horn", DW_C,
     ['A horn off his helmet - he has a spare,', 'he says. Blow it and he comes.', ('Use: call Dennis (again: call him over).', 'blue'),
      ('Sneak + use: his menu.', 'blue'), ('While he\'s with you: Fortune V on every ore.', 'blue'),
      ('If he faints: 5 minutes before he can return.', 'gray'), ('"Gold, lad. It\'s always gold."', 'dark_gray')],
     model='bm:dw_horn', stack=1, cat='magic', glint=True, comps=hold('none'))
HOLD['dw_horn'] = 'bm:p163/dw/use'
item('pi_cloche', TOTEM, "Pistachio's Little Cloche", PI_C,
     ['A silver cloche the size of a thimble.', 'Lift the lid and he floats out.', ('Use: call Pistachio (again: call him over).', 'blue'),
      ('Sneak + use: his menu.', 'blue'), ('While he\'s with you: Looting V on every kill.', 'blue'),
      ('If he faints: 5 minutes before he can return.', 'gray'), ('"Dinner is served, sir. And so is justice."', 'dark_gray')],
     model='bm:pi_cloche', stack=1, cat='magic', glint=True, comps=hold('none'))
HOLD['pi_cloche'] = 'bm:p163/pi/use'
for _k, _c in F_.items():
    item(_c['contract'], TOTEM, f"Raid Contract: {_c['name']}", _c['col'],
         [('Use once: from then on ' + _c['name'], 'blue'), ('will come into the vault with you.', 'blue')],
         model='minecraft:paper', glint=True, stack=1, cat='magic', comps=hold('none'))
    HOLD[_c['contract']] = f'bm:p163/{_k}/sign'
    item(_c['doll'], TOTEM, f"{_c['name']} Doll", _c['col'],
         [f"A doll of {_c['name']} - " + ('horns, shades, wrench and all.' if _k == 'dw' else 'top hat, monocle, cloche and all.'),
          ('Right-click a block: set it down.', 'blue'), ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
         model=f"bm:{_c['doll']}", stack=16, cat='fun', comps=hold('none'))
    HOLD[_c['doll']] = f"bm:p141/{_c['doll']}/use"
P141.DOLLS.append(('doll_dennis', 'Dennis', DW_C, 'A doll of Dennis - horns, shades, wrench and all.', 'minecraft:wax_on', 'minecraft:block.anvil.land',
                   'minecraft:wax_on'))
P141.DOLLS.append(('doll_pistachio', 'Pistachio', PI_C, 'A doll of Pistachio - top hat, monocle, cloche and all.', 'minecraft:soul',
                   'minecraft:entity.allay.ambient_without_item', 'minecraft:soul'))
P141.DOLL_FROM['doll_dennis'] = ('dw_horn', {'kh': 1.0, 'kb': 1.0, 'kl': 0.8})
P141.DOLL_FROM['doll_pistachio'] = ('pi_cloche', {'kh': 1.0, 'kb': 1.0, 'kl': 1.0})

# ------------------------------------------------------------------------------------------------ the registries
for _k, _c in F_.items():
    P46.COMPANIONS += f',tag=!bm.{_k}pet'
    allies.ALLIES.append(f'bm.{_k}pet')
    P89.BIT[_c['w']] = 2 ** len(P89.BIT)
    P68.KINDS[_c['w']] = (max(v[0] for v in P68.KINDS.values()) + 1, _c['item'], 'wolf', f'bm.{_k}pet', f'p163/{_k}/summon', f'p163/{_k}/dismiss', f'bm.{_k}sel2',
                          _c['name'], _c['col'])
    P68.HE.add(_c['w'])
    P98.CALLED.append((_c['w'], _c['name'], _c['col'], 'wolf', f'bm.{_k}pet', f'bm.{_k}sel2', f'bm.{_k}cd', f'p163/{_k}/try_summon', f'p163/{_k}/dismiss',
                       f'p163/{_k}/recall', f'p163/{_k}/go'))
    P100.WHO[_c['w']] = ('wolf', f'bm.{_k}pet')
    P100.VOICE[_c['name']] = (_c['col'], _c['line'])
    FX.FOLK[_c['w']] = ('minecraft:wolf', f'bm.{_k}pet', f'type=minecraft:item_display,tag=bm.{_k}p,tag=bm.{_k}p_head,tag=bm.{_k}p_pet,tag=!bm.{_k}fade', EXPR,
                        (60, 140), [('happy', 30, 3), ('squint', 26, 6)], ('happy', 40), 'hurt', 'serious')
# the trio: Emma, Leo and Dennis
P100.TRIOS['prospect'] = ("The Crown's Prospect", '#ffd870', ('emma', 'leo', 'dennis'), "The Crown's Prospect", 'Walk with Emma, Leo and Dennis at once')
P100.BANTER['prospect'] = [
    ('Dennis', "A princess and a knight. Right - who's carrying the gold?", 'Leo', 'You are, dwarf. You always are.'),
    ('Emma', 'Dennis! Will you make me a crown? A gold one? With horns?', 'Dennis', "Horns are for dwarves, lass. But a crown... aye, I could do a crown."),
    ('Leo', 'Stay behind me, Princess. Dennis - stay behind her.', 'Dennis', "Stay behind? I'm the one with the wrench!")]

_figures0 = P134.figures


def _figures():
    F2 = _figures0()
    F2['dw_horn'] = ('Dennis', P134._rigkit(DArt, DA.POSES['idle_a'], DA.RIG_SCALE))
    F2['pi_cloche'] = ('Pistachio', P134._rigkit(PArt, PA.POSES['idle_a'], PA.RIG_SCALE))
    return F2


P134.figures = _figures
P134.FIT['dw_horn'] = (0.000, 1.921, -0.516, 0.532, -0.238, 0.320)        # (measured: phase134.measure)
P134.FIT['pi_cloche'] = (0.019, 1.872, -0.547, 0.464, -0.259, 0.509)


def extend_offers(O, offer):
    pass


# ================================================================================================= resource pack
def _icon(kind):
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == 'horn':
        pts = [(2, 13), (4, 11), (6, 9), (8, 6), (10, 4), (12, 2), (13, 1)]
        for i, (x, y) in enumerate(pts):
            r = max(1, 3 - i // 2)
            d.ellipse((x - r, y - r, x + r, y + r), fill=hexc('#e6dcc0'), outline=hexc('#9a8c6a'))
        d.rectangle((1, 12, 5, 15), fill=hexc('#d6ac2e')); d.line((1, 13, 5, 13), fill=hexc('#fff0a0'))
        d.point((9, 5), fill=hexc('#ffffff')); d.point((11, 3), fill=hexc('#ffffff'))
    else:
        d.ellipse((2, 11, 13, 14), fill=hexc('#d8d6cc'), outline=hexc('#8a8a84'))
        d.pieslice((3, 3, 12, 17), 180, 360, fill=hexc('#b0b2ae'), outline=hexc('#6a6c68'))
        d.rectangle((7, 1, 8, 3), fill=hexc('#7a7c78'))
        d.line((5, 7, 6, 5), fill=hexc('#ffffff')); d.point((10, 8), fill=hexc('#8af0a4')); d.point((4, 9), fill=hexc('#8af0a4'))
    return im


def rp(R):
    R.ICONS['dw_horn'] = _icon('horn')
    R.ICONS['pi_cloche'] = _icon('cloche')
    for d in ('doll_dennis', 'doll_pistachio'):               # (their items' stand-ins, as phase141's: the bake replaces the model - phase141.rp ran
        R.HATS[d] = ({'s': 'minecraft:block/white_wool'}, [{'from': [6, 0, 6], 'to': [10, 8, 10],     #  before this module was imported)
                                                            'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}])

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        for k, pfx in (('dw', 'dw_'), ('pi', 'ps_')):
            cases = [{'when': e, 'model': mdl(f'{pfx}head_x{m}' if m else f'{pfx}head')} for e, m in FACE[k].items()]
            R2.wj(f'assets/bm/items/{pfx}head.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                                  'cases': cases, 'fallback': mdl(f'{pfx}head')}})
    R.POST.insert(0, post)


# ================================================================================================= the datapack
def generate_early(G):
    """(before phase137 reads the Recruiter's stock) their Raid Contracts on the Recruiter's books"""
    from gen_dp import offer
    import phase103 as P103
    fn, title, tellraw = G.fn, G.title, G.tellraw
    GP = [T('[', 'dark_gray'), T('Heist', '#ffcf40', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    Lr = G.FUNCS['p70/r/lobby/init']
    k_ = next(i for i, l in enumerate(Lr) if l.startswith('summon minecraft:villager') and 'bm.gvrec' in l and 'Recipes:[' in l)
    for k, c in F_.items():
        bit = P89.BIT[c['w']]
        signed = ['scoreboard players operation #q bm.rng = @s bm.fcon', f'scoreboard players set #bit bm.rng {bit}',
                  'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']
        fn(f'p163/{k}/sign', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                              'execute unless score @s bm.fcon matches 0.. run scoreboard players set @s bm.fcon 0'] + signed +
           [f'execute if score #q bm.rng matches 1 run return run ' + say(f"{c['name']} is already under contract.", 'gray'),
            f'scoreboard players add @s bm.fcon {bit}', f'clear @s *[minecraft:custom_data~{{bm:"{c["contract"]}"}}] 1',
            'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8', 'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.4 1.6',
            tellraw('@s', GP + [T('Signed! ', '#ffcf40', bold=True), T(c['name'], c['col'], bold=True), T(' will answer your call in the vault from now on.', 'gray')])])
        fn(f'p163/{k}/ok', ['execute unless dimension bm:gutter run return run function bm:p74/fol_ok', 'execute unless entity @s[tag=bm.gvp] run return 0'] + signed +
           ['execute if score #q bm.rng matches 1 run return 1',
            tellraw('@s', GP + [T(c['name'], c['col']), T(' needs his ', 'gray'), T('Raid Contract', '#ffcf40'), T(' signed to come into the vault (the Recruiter in the den sells it).', 'gray')]),
            'return 0'])
        o = offer(('gutter_trophy', 1), (c['contract'], 1), ('gutter_medallion', 3))
        Lr[k_] = Lr[k_].replace('Recipes:[', 'Recipes:[' + snbt(o) + ',', 1)
        P103.RECRUITER_OFFERS.append(o)


def generate(G):
    import phase73 as P73
    import phase28 as P28
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    foe = 'type=#bm:hostile,tag=!bm.npc'
    tick, fast, second = [], [], []
    for k, c in F_.items():
        build(G, k, c, fn, title, tellraw, give, PREFIX, say, holds, foe, tick, fast, second, P73, P28)
    pairs(G, fn, tellraw, title, PREFIX, foe, second)
    # the passives: Fortune V (Dennis) / Looting V (Pistachio) while he's out and within 24 blocks of you (phase162's loot tables)
    second += ['scoreboard players set @a bm.dwft 0', 'scoreboard players set @a bm.pslt 0',
               'execute as @e[type=minecraft:wolf,tag=bm.dwpet,tag=!bm.ffpet] at @s on owner if entity @s[distance=..24] run scoreboard players set @s bm.dwft 1',
               'execute as @e[type=minecraft:wolf,tag=bm.pipet,tag=!bm.ffpet] at @s on owner if entity @s[distance=..24] run scoreboard players set @s bm.pslt 1']
    # (Pistachio's Phantom Escape: the owner at 3 hearts or less, once a minute)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.pisv dummy']
    G.OBJECTIVES += ['bm.pisv']
    second += ['scoreboard players remove @a[scores={bm.pisv=1..}] bm.pisv 1',
               'execute as @e[type=minecraft:wolf,tag=bm.pipet,tag=!bm.ffpet] at @s on owner if entity @s[distance=..24,scores={bm.hp=1..6}] unless score @s bm.pisv matches 1.. at @s run function bm:p163/pi/escape']
    fn('p163/pi/escape', ['scoreboard players set @s bm.pisv 60', 'effect give @s minecraft:invisibility 4 0 true', 'effect give @s minecraft:resistance 4 1 true',
                          'effect give @s minecraft:speed 4 1 true', 'particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.03 30',
                          'playsound minecraft:entity.allay.death player @a[distance=..16] ~ ~ ~ 0.6 1.4',
                          title('@s', 'actionbar', [T('Pistachio: ', PI_C, bold=True), T('Phantom Escape - fade, sir, fade!', PI_LINE)])])
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def build(G, k, c, fn, title, tellraw, give, PREFIX, say, holds, foe, tick, fast, second, P73, P28):
    W, NAME, COL, LINE, ART, A, POSES = c['w'], c['name'], c['col'], c['line'], c['art'], c['A'], c['poses']
    SP = ART.RIG_SCALE
    UP = SP / 16
    MENU = c['menu']
    pfx = f'p163/{k}'
    fysay = lambda txt, who='@s': title(who, 'actionbar', [T(f'{NAME}: ', COL, bold=True), T(txt, LINE)])
    fychat = lambda txt, who='@s': tellraw(who, [T(f'{NAME}: ', COL, bold=True), T(f'"{txt}"', LINE)])
    objs = [f'bm.{k}{s}' for s in ('s', 'fr', 'x', 'a', 'mc', 'rc', 'uc', 'cc', 'sl', 'z', 'qp', 'hc', 'cd', 'l', 'fg', 'h')]
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    S = lambda s: f'bm.{k}{s}'                              # (an objective of his)
    pet, me, sel, sel2, new, fade, own = (f'bm.{k}pet', f'bm.{k}me', f'bm.{k}sel', f'bm.{k}sel2', f'bm.{k}new', f'bm.{k}fade', f'bm.{k}own')

    def psel(p=None):
        return f'@e[type=minecraft:item_display,tag={sel}' + (f',tag=bm.{k}p_{p}]' if p else ']')
    sel_pet = f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid'
    face = lambda e, t: FX.face_cmd(W, e, t)
    bright = {'brightness': {'block': Int(15), 'sky': Int(15)}} if k == 'pi' else {}
    rig = [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, [f"bm.{k}p", f"bm.{k}p_{p}", f"bm.{k}p_pet", new], SP, extra=dict(bright, shadow_radius=F(0.5 if p == "body" else 0.0), shadow_strength=F(0.5)))}'
           for p in A.PARTS]
    fn(f'{pfx}/place', RF.place(A, UP, psel))
    burst = {'dw': ['particle minecraft:wax_on ~ ~1 ~ 0.4 0.7 0.4 0 30', 'particle minecraft:flash{color:[1.0,0.8,0.3,1.0]} ~ ~1 ~ 0 0 0 0 1',
                    'particle minecraft:item{item:"minecraft:gold_nugget"} ~ ~1 ~ 0.4 0.6 0.4 0.12 20'],
             'pi': ['particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.03 30', 'particle minecraft:flash{color:[0.5,1.0,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1',
                    f'particle minecraft:dust{{color:[0.5,1.0,0.6],scale:1.0}} ~ ~1.2 ~ 0.4 0.6 0.4 0 30']}[k]
    fn(f'{pfx}/burst', burst)
    # states: 0 idle, 1 walk, 2 run, 3 air, 4 sit, 6 arriving (his bow), 7 melee, 8 ranged, 9 crowd, 10 swim, 12 the great blow
    atk = {'dw': {7: [(0, 'swing_back'), (5, 'swing')], 8: [(0, 'toss')], 9: [(0, 'slam_up'), (7, 'slam')], 12: [(0, 'ult')]},
           'pi': {7: [(0, 'slap_back'), (4, 'slap')], 8: [(0, 'serve')], 9: [(0, 'wail')], 12: [(0, 'ult')]}}[k]
    CYCLE = {0: (40, [(0, 'idle_a'), (20, 'idle_b')]), 1: (16, [(0, 'walk_a'), (8, 'walk_b')]), 2: (10, [(0, 'run_a'), (5, 'run_b')]),
             3: (None, [(0, 'air')]), 4: (40, [(0, 'sit'), (20, 'sit_b')]), 6: (None, [(0, 'bow')]), 10: (24, [(0, 'paddle_a'), (12, 'paddle_b')])}
    CYCLE.update({st: (None, fr) for st, fr in atk.items()})
    DUR = {'idle_a': 20, 'idle_b': 20, 'walk_a': 6, 'walk_b': 6, 'run_a': 4, 'run_b': 4, 'air': 5, 'sit': 14, 'sit_b': 18, 'bow': 10, 'paddle_a': 10, 'paddle_b': 10,
           'swing_back': 4, 'swing': 2, 'toss': 4, 'slam_up': 6, 'slam': 2, 'ult': 10, 'slap_back': 3, 'slap': 2, 'serve': 4, 'wail': 4}
    RF.cycles(fn, pfx, CYCLE, S('fr'), S('s'), lambda p: f'{pfx}/pose/{p}')
    for name in {p for _per, frames in CYCLE.values() for _t, p in frames}:
        fn(f'{pfx}/pose/{name}', RF.pose(A, POSES[name], SP, DUR.get(name, 6), psel, swap=()))
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in RF.periods(CYCLE)]
    fn(f'{pfx}/state', [f'execute if score @s {S("sl")} matches 1.. run return run scoreboard players set #st bm.rng 6',
                        f'execute if score @s {S("x")} matches 1.. run return run scoreboard players operation #st bm.rng = @s {S("a")}',
                        'execute if data entity @s {Sitting:1b} run return run scoreboard players set #st bm.rng 4',
                        'execute store result score #og bm.rng run data get entity @s OnGround',
                        'execute if score #og bm.rng matches 0 if predicate bm:swim run return run scoreboard players set #st bm.rng 10',
                        f'execute if score #og bm.rng matches 0 run scoreboard players add @s {S("z")} 1', f'execute if score #og bm.rng matches 1 run scoreboard players set @s {S("z")} 0',
                        f'execute if score @s {S("z")} matches 4.. unless block ~ ~ ~ minecraft:water run return run scoreboard players set #st bm.rng 3',
                        'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                        'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                        'scoreboard players operation #vx bm.rng += #vz bm.rng',
                        'execute if score #vx bm.rng matches 30000.. run return run scoreboard players set #st bm.rng 2',
                        'execute if score #vx bm.rng matches 500.. run return run scoreboard players set #st bm.rng 1',
                        'scoreboard players set #st bm.rng 0'])
    tick.append(f'execute as @e[type=minecraft:wolf,tag={pet}] at @s run function bm:{pfx}/tick')
    idle_fight = f'unless score @s {S("x")} matches 1.. unless data entity @s {{Sitting:1b}}'
    fn(f'{pfx}/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.{k}p_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                       f'execute unless entity {psel("head")} run function bm:{pfx}/rerig',
                       f'execute if score @s {S("x")} matches 1.. run function bm:{pfx}/act_tick'] +
       [f'execute if score @s {S(o)} matches 1.. run scoreboard players remove @s {S(o)} 1' for o in ('mc', 'rc', 'uc', 'cc', 'sl')] +
       [f'execute {idle_fight} unless score @s {S("uc")} matches 1.. if entity @e[{foe},distance=..7] run function bm:{pfx}/ult_go',
        f'execute {idle_fight} unless score @s {S("cc")} matches 1.. if entity @e[{foe},distance=..3.5] run function bm:{pfx}/crowd_go',
        f'execute {idle_fight} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..2.8] run function bm:{pfx}/melee_go',
        f'execute {idle_fight} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..2.8] if entity @e[{foe},distance=..{11 if k == "dw" else 13}] run function bm:{pfx}/range_go',
        f'function bm:{pfx}/state',
        f'execute if score #st bm.rng = @s {S("s")} run scoreboard players add @s {S("fr")} 1',
        f'execute unless score #st bm.rng = @s {S("s")} run scoreboard players set @s {S("fr")} 0',
        f'scoreboard players operation @s {S("s")} = #st bm.rng',
        f'function bm:{pfx}/anim',
        f'execute on owner run tag @s add {own}',
        f'execute if score @s {S("s")} matches 7..9 if entity @e[{foe},distance=..17] facing entity @e[{foe},distance=..17,sort=nearest,limit=1] feet rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 12 if entity @e[{foe},distance=..17] facing entity @e[{foe},distance=..17,sort=nearest,limit=1] feet rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 7..9 unless entity @e[{foe},distance=..17] rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 12 unless entity @e[{foe},distance=..17] rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 0 run function bm:{pfx}/face_you', f'execute if score @s {S("s")} matches 4 run function bm:{pfx}/face_you',
        f'execute if score @s {S("s")} matches 6 run function bm:{pfx}/face_you',
        f'execute if score @s {S("s")} matches 1..3 rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 10 rotated as @s rotated ~ 0 positioned ~ ~0.2 ~ run function bm:{pfx}/place',
        f'function bm:{pfx}/box'] + ambient(k, pfx) +
       [f'tag @a[tag={own}] remove {own}', f'tag @e[tag={sel}] remove {sel}'])
    fn(f'{pfx}/face_you', [f'execute if entity @a[tag={own},distance=1.5..10] facing entity @a[tag={own},limit=1] feet rotated ~ 0 run return run function bm:{pfx}/place',
                           f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/place'])

    # ---- his blows (go: the state and its length, the cooldown; hit: on its tick)
    hurt_by = f'@e[type=minecraft:wolf,tag={me},limit=1]'
    fn(f'{pfx}/hurt', ['execute store result storage bm:tmp p163.d int 1 run scoreboard players get #pd bm.rng', f'function bm:{pfx}/dmg with storage bm:tmp p163'])
    fn(f'{pfx}/dmg', [f'$damage @s $(d) minecraft:mob_attack by {hurt_by}'])
    go = lambda a, x, cdo, cd, extra=(): [f'scoreboard players set @s {S("a")} {a}', f'scoreboard players set @s {S("x")} {x}', f'scoreboard players set @s {S(cdo)} {cd}'] + list(extra)
    hit = lambda d: [f'tag @s add {me}', f'scoreboard players set #pd bm.rng {d}']
    end = [f'tag @s remove {me}', f'function bm:{pfx}/blow']
    if k == 'dw':
        fn(f'{pfx}/melee_go', go(7, 10, 'mc', 22, ['playsound minecraft:entity.player.attack.sweep neutral @a[distance=..12] ~ ~ ~ 0.6 0.7']))
        fn(f'{pfx}/range_go', go(8, 10, 'rc', 50))
        fn(f'{pfx}/crowd_go', go(9, 14, 'cc', 160, face('serious', 14)))
        fn(f'{pfx}/ult_go', go(12, 30, 'uc', 900, ['playsound minecraft:block.anvil.use neutral @a[distance=..24] ~ ~ ~ 1 0.6'] + face('happy', 30)))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 4 run function bm:{pfx}/melee_hit',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 5 run function bm:{pfx}/range_hit',
                               f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 7 run function bm:{pfx}/crowd_hit',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 20..29 run particle minecraft:item{{item:"minecraft:gold_block"}} ~ ~0.2 ~ 2 0.1 2 0.15 8',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 18 run function bm:{pfx}/ult_hit'])
        fn(f'{pfx}/melee_hit', hit(7) + ['playsound minecraft:block.anvil.land neutral @a[distance=..12] ~ ~ ~ 0.4 1.4',
                                         f'execute as @e[{foe},distance=..3.4,sort=nearest,limit=1] at @s run function bm:{pfx}/whacked'] + end)
        fn(f'{pfx}/whacked', [f'function bm:{pfx}/hurt', 'particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.2 8',
                              f'execute facing entity {hurt_by} feet positioned ^ ^ ^-1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~'])
        fn(f'{pfx}/range_hit', hit(5) + ['playsound minecraft:entity.experience_orb.pickup neutral @a[distance=..16] ~ ~ ~ 0.7 0.6',
                                         f'execute facing entity @e[{foe},distance=..12,sort=nearest,limit=1] eyes positioned ^ ^1.2 ^ run function bm:{pfx}/nuggets',
                                         f'execute as @e[{foe},distance=..12,sort=nearest,limit=1] at @s run function bm:{pfx}/gilded'] + end)
        fn(f'{pfx}/nuggets', [f'particle minecraft:item{{item:"minecraft:gold_nugget"}} ^ ^ ^{d} 0.08 0.08 0.08 0.02 3' for d in range(1, 12)])
        fn(f'{pfx}/gilded', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 0', 'particle minecraft:item{item:"minecraft:raw_gold"} ~ ~1.2 ~ 0.3 0.3 0.3 0.1 8',
                             'playsound minecraft:block.chain.hit neutral @a[distance=..16] ~ ~ ~ 0.8 1.6'])
        fn(f'{pfx}/crowd_hit', hit(9) + ['particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.2 ~ 2.4 0.1 2.4 0.2 80',
                                         'particle minecraft:wax_on ~ ~0.5 ~ 2.5 0.3 2.5 0 30', 'playsound minecraft:entity.generic.explode neutral @a[distance=..24] ~ ~ ~ 0.5 1.6',
                                         'playsound minecraft:block.anvil.land neutral @a[distance=..16] ~ ~ ~ 0.8 0.6',
                                         f'execute as @e[{foe},distance=..4.5] at @s run function bm:{pfx}/slammed',
                                         'execute on owner if entity @s[distance=..24] run ' + fysay('MIDAS SLAM!')] + end)
        fn(f'{pfx}/slammed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:levitation 1 2', 'particle minecraft:wax_on ~ ~1 ~ 0.3 0.5 0.3 0 6'])
        fn(f'{pfx}/ult_hit', hit(14) + ['particle minecraft:flash{color:[1.0,0.85,0.3,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:totem_of_undying ~ ~1 ~ 2.5 1 2.5 0.4 100',
                                        'particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.4 ~ 3 0.3 3 0.3 120',
                                        'playsound minecraft:entity.generic.explode neutral @a[distance=..32] ~ ~ ~ 0.8 1.0',
                                        'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..24] ~ ~ ~ 1 0.8',
                                        f'execute as @e[{foe},distance=..7] at @s run function bm:{pfx}/lode',
                                        'execute on owner if entity @s[distance=..24] run function bm:p163/dw/clad',
                                        'execute on owner if entity @s[distance=..24] run ' + fysay('THE MOTHER LODE! Gold for everyone - and a beating for you lot!')] + end)
        fn(f'{pfx}/lode', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:levitation 1 1', 'particle minecraft:item{item:"minecraft:gold_ingot"} ~ ~1 ~ 0.3 0.5 0.3 0.1 8'])
        fn('p163/dw/clad', ['effect give @s minecraft:absorption 20 1 true', 'effect give @s minecraft:resistance 8 0 true', 'particle minecraft:wax_on ~ ~1 ~ 0.4 0.8 0.4 0 20'])
        QUIPS = ["That's what a wrench is for!", 'Another one for the pile!', 'Gold! I smell gold!', 'Come on then - who\'s next?', 'Mind the beard, mind the beard!',
                 'I\'ve dug through tougher rock than you!']
    else:
        fn(f'{pfx}/melee_go', go(7, 8, 'mc', 20, ['playsound minecraft:entity.player.attack.weak neutral @a[distance=..12] ~ ~ ~ 0.6 1.4']))
        fn(f'{pfx}/range_go', go(8, 12, 'rc', 60, ['playsound minecraft:block.bell.use neutral @a[distance=..16] ~ ~ ~ 0.5 1.8']))
        fn(f'{pfx}/crowd_go', go(9, 14, 'cc', 200, face('surprised', 14)))
        fn(f'{pfx}/ult_go', go(12, 30, 'uc', 900, ['playsound minecraft:entity.allay.ambient_with_item neutral @a[distance=..24] ~ ~ ~ 1 0.6'] + face('happy', 30)))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 4 run function bm:{pfx}/melee_hit',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 6 run function bm:{pfx}/range_hit',
                               f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 7 run function bm:{pfx}/crowd_hit',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 20..29 run function bm:{pfx}/ult_spin',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 18 run function bm:{pfx}/ult_hit'])
        fn(f'{pfx}/melee_hit', hit(4) + ['playsound minecraft:entity.player.attack.knockback neutral @a[distance=..12] ~ ~ ~ 0.6 1.6',
                                         f'execute as @e[{foe},distance=..3.4,sort=nearest,limit=1] at @s run function bm:{pfx}/slapped'] + end)
        fn(f'{pfx}/slapped', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:weakness 4 0', 'particle minecraft:soul ~ ~1.4 ~ 0.2 0.2 0.2 0.02 6'])
        fn(f'{pfx}/range_hit', hit(6) + ['playsound minecraft:entity.vex.charge neutral @a[distance=..16] ~ ~ ~ 0.7 1.4',
                                         f'execute facing entity @e[{foe},distance=..14,sort=nearest,limit=1] eyes positioned ^ ^1.3 ^ run function bm:{pfx}/spirit',
                                         f'execute as @e[{foe},distance=..14,sort=nearest,limit=1] at @s run function bm:{pfx}/haunted',
                                         'execute on owner if entity @s[distance=..24] run effect give @s minecraft:speed 6 0 true'] + end)
        fn(f'{pfx}/spirit', [f'particle minecraft:soul ^ ^ ^{d / 2:.1f} 0.05 0.05 0.05 0.01 1' for d in range(1, 28)] +
           [f'particle minecraft:dust{{color:[0.5,1.0,0.6],scale:0.9}} ^ ^ ^{d / 2:.1f} 0 0 0 0 1' for d in range(1, 28)])
        fn(f'{pfx}/haunted', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:glowing 4 0 true', 'particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.4 0.3 0.02 8'])
        fn(f'{pfx}/crowd_hit', hit(4) + ['particle minecraft:sonic_boom ~ ~1.4 ~ 0 0 0 0 1', 'particle minecraft:soul ~ ~1 ~ 2.5 0.6 2.5 0.04 50',
                                         'playsound minecraft:entity.ghast.scream neutral @a[distance=..24] ~ ~ ~ 0.6 1.6',
                                         f'execute as @e[{foe},distance=..5] at @s run function bm:{pfx}/wailed',
                                         'execute on owner if entity @s[distance=..24] run ' + fysay('BOOOOO! ...I do beg your pardon.')] + end)
        fn(f'{pfx}/wailed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 4 1', 'effect give @s minecraft:weakness 4 0'])
        fn(f'{pfx}/ult_spin', [f'particle minecraft:soul ^{2.0 * math.cos(a):.2f} ^{1.2 + 0.5 * math.sin(3 * a):.2f} ^{2.0 * math.sin(a):.2f} 0 0 0 0 1'
                               for a in [n * math.pi / 6 for n in range(12)]] + ['particle minecraft:sculk_soul ~ ~1 ~ 1.5 0.6 1.5 0.01 4'])
        fn(f'{pfx}/ult_hit', hit(12) + ['particle minecraft:flash{color:[0.5,1.0,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:soul ~ ~1 ~ 3 1 3 0.06 120',
                                        'playsound minecraft:entity.warden.sonic_boom neutral @a[distance=..32] ~ ~ ~ 0.4 1.6',
                                        'playsound minecraft:block.bell.resonate neutral @a[distance=..24] ~ ~ ~ 1 1.4',
                                        f'execute as @e[{foe},distance=..7] at @s run function bm:{pfx}/course',
                                        'execute on owner if entity @s[distance=..24] run function bm:p163/pi/ward',
                                        'execute on owner if entity @s[distance=..24] run ' + fysay('The Last Course, sir. Do enjoy it - they shan\'t.')] + end)
        fn(f'{pfx}/course', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:levitation 1 3', 'particle minecraft:soul ~ ~1 ~ 0.3 0.5 0.3 0.02 8'])
        fn('p163/pi/ward', ['effect give @s minecraft:resistance 8 1 true', 'effect give @s minecraft:regeneration 8 0 true', 'particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.02 20'])
        QUIPS = ['Do mind the upholstery.', 'Another guest, departing early.', 'Shall I fetch your coat? You are leaving.', 'Most irregular!',
                 'One lump or two? Two, I think.', 'The Palace thanks you for your visit.']
    fn(f'{pfx}/blow', [f'scoreboard players add @s {S("qp")} 1', f'execute if score @s {S("qp")} matches 8.. run function bm:{pfx}/quip'])
    fn(f'{pfx}/quip', [f'scoreboard players set @s {S("qp")} 0', f'execute store result score #r bm.rng run random value 1..{len(QUIPS)}'] +
       [f'execute if score #r bm.rng matches {n + 1} on owner if entity @s[distance=..20,tag=!bm.hush] run ' + fysay(q) for n, q in enumerate(QUIPS)] + face('happy', 30))

    # ---- his item: call, call over, sneak for his menu
    def pet_nbt():
        return {'Tags': [pet, new, 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(c['hp']),
                'CustomName': T(NAME, COL, bold=True), 'CustomNameVisible': B(0),
                'attributes': [{'id': f'minecraft:{a}', 'base': D(v)} for a, v in dict(max_health=c['hp'], armor=c['armour'], attack_damage=1, knockback_resistance=c['kb'],
                                                                                       movement_speed=c['speed'], follow_range=32, step_height=1.0, water_movement_efficiency=0.6,
                                                                                       oxygen_bonus=1000).items()],
                'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    in_heist = 'execute if entity @s[tag=bm.gvp] if dimension bm:gutter'
    fn(f'{pfx}/use', [f'{in_heist} run return run ' + say("In the vault your crew answers the Fixer's Ledger - Raid Crew.", '#9ad0ff'),
                      'execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                      'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      f'{sel_pet} run tag @s add {sel2}', 'scoreboard players set #am bm.rng 0',
                      'execute if predicate bm:p20/sneaking run scoreboard players set #am bm.rng 2',
                      f'execute if score #am bm.rng matches 0 if entity @e[type=minecraft:wolf,tag={sel2}] run scoreboard players set #am bm.rng 4',
                      f'execute if score #am bm.rng matches 2 run function bm:{pfx}/menu', f'execute if score #am bm.rng matches 4 run function bm:{pfx}/recall',
                      f'execute if score #am bm.rng matches 0 run function bm:{pfx}/try_summon', f'tag @e[tag={sel2}] remove {sel2}'])
    hello = {'dw': ("Comin', comin'! Short legs, lad - short legs.", "Dennis here. Point me at somethin' that needs hittin' - or diggin'.", 'Back to the market, then. Mind the gold.'),
             'pi': ('At once, sir.', 'Pistachio, at your service. Dinner - or violence?', 'I shall return to the Palace. Do wipe your feet.')}[k]
    fn(f'{pfx}/recall', [f'tp @e[type=minecraft:wolf,tag={sel2},limit=1] @s', f'data modify entity @e[type=minecraft:wolf,tag={sel2},limit=1] Sitting set value 0b',
                         f'function bm:{pfx}/burst', fysay(hello[0])])
    fn(f'{pfx}/try_summon', [f'execute if score @s {S("cd")} matches 1.. store result score #m bm.rng run scoreboard players get @s {S("cd")}',
                             f'execute if score @s {S("cd")} matches 1.. run scoreboard players add #m bm.rng 59',
                             f'execute if score @s {S("cd")} matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                             f'execute if score @s {S("cd")} matches 1.. run return run ' + title('@s', 'actionbar', [T(f'{NAME} is still getting his breath back: about ', 'gray'),
                                                                                                                      {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                             f'execute unless function bm:{pfx}/ok run return run ' + say(f"{NAME} won't come here."),
                             'execute if function bm:p58/full run return 0', f'function bm:{pfx}/summon'])
    fn(f'{pfx}/summon', [f'execute positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:{pfx}/summon_here',
                         f'execute positioned ^ ^1 ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:{pfx}/summon_here',
                         f'function bm:{pfx}/summon_here'])
    fn(f'{pfx}/summon_here', [f'summon minecraft:wolf ~ ~ ~ {snbt(pet_nbt())}',
                              f'data modify entity @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] Owner set from entity @s UUID',
                              f'execute as @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] run function bm:{pfx}/tough',
                              f'scoreboard players set @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] {S("s")} -1',
                              f'scoreboard players set @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] {S("sl")} 24',
                              f'execute rotated ~180 0 run function bm:{pfx}/rig_here',
                              f'scoreboard players operation @e[tag={new},distance=..4] bm.pid = @s bm.pid',
                              f'execute as @e[type=minecraft:item_display,tag={new},distance=..4] run tag @s add {sel}', f'function bm:{pfx}/dress',
                              f'execute at @e[type=minecraft:item_display,tag={sel},tag=bm.{k}p_body,limit=1] run function bm:{pfx}/burst',
                              f'tag @e[tag={sel}] remove {sel}', f'tag @e[tag={new},distance=..4] remove {new}',
                              'playsound minecraft:block.note_block.chime neutral @a[distance=..20] ~ ~ ~ 0.6 1.6', fysay(hello[1])])
    # (a tamed wolf takes a wolf's health when its owner is set: his own put back after)
    fn(f'{pfx}/tough', [f'attribute @s minecraft:max_health base set {c["hp"]}', f'data modify entity @s Health set value {c["hp"]}f',
                        f'attribute @s minecraft:armor base set {c["armour"]}'])
    fn(f'{pfx}/rig_here', rig + [f'tp @e[type=minecraft:item_display,tag={new},distance=..1] ~ ~ ~ ~ 0'])
    fn(f'{pfx}/rerig', [f'kill @e[type=minecraft:item_display,tag={sel}]', f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/rig_here',
                        f'scoreboard players operation @e[type=minecraft:item_display,tag={new},distance=..2] bm.pid = #me bm.pid',
                        f'tag @e[type=minecraft:item_display,tag={new},distance=..2] add {sel}', f'tag @e[type=minecraft:item_display,tag={new},distance=..2] remove {new}',
                        f'function bm:{pfx}/dress', f'scoreboard players set @s {S("s")} -1'])
    # (his look: the "_c<k>" suffix his owner picked - phase138's way)
    fn(f'{pfx}/dress', ['scoreboard players set #wk bm.rng 0', f'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #wk bm.rng = @s {c["cos"]}',
                        f'execute as @e[type=minecraft:item_display,tag={sel}] run function bm:p138/sfx'])
    fn(f'p99/{W}_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/now2',
                        'execute if score #has bm.rng matches 0 run return run ' + say(f"{NAME} isn't with you - he'll wear it next time.", COL)])
    fn(f'{pfx}/now2', ['scoreboard players set #has bm.rng 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.{k}p_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                       f'function bm:{pfx}/dress', f'tag @e[tag={sel}] remove {sel}', 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.02 14'])
    fn(f'{pfx}/dismiss', [f'execute as @e[type=minecraft:wolf,tag={sel2}] at @s run function bm:{pfx}/fade',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] on passengers run kill @s[type=!minecraft:player]',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] run data remove entity @s Owner',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] run tp @s ~ -500 ~', f'kill @e[type=minecraft:wolf,tag={sel2}]', fysay(hello[2])])
    fn(f'{pfx}/home', [f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run tag @s add {sel2}',
                       f'execute if entity @e[tag={sel2}] run function bm:{pfx}/dismiss', f'tag @e[tag={sel2}] remove {sel2}'])
    # his menu (sneak + use his item)
    powers = {'dw': [('Wrench Whack', 'up close: the wrench, overhead (7, and a shove)'), ('Gold Rush', 'at range: a fistful of gold nuggets (5, and slowed)'),
                     ('Midas Slam', 'when they crowd him: a ring of gold (9 to all near, up they go)'),
                     ('The Mother Lode', 'his great blow, every 45 s: gold pours up (14 to all near) - and you, clad in it (Absorption, Resistance)'),
                     ('Fortune V', 'while he\'s with you, on every ore you mine')],
              'pi': [('Spectral Slap', 'up close: a cold glove (4, and Weakness)'), ('The Next Course', 'at range: a spirit from his cloche (6, they glow) - and you, light of foot'),
                     ('The Wail', 'when they crowd him: a shriek from beyond (4 to all near, slowed and weakened)'),
                     ('The Last Course', 'his great one, every 45 s: every spirit at once (12 to all near) - and a Ghostly Ward on you'),
                     ('Phantom Escape', 'you at 3 hearts or less, once a minute: unseen and unharmed a moment'),
                     ('Looting V', 'while he\'s with you, on every mob you kill')]}[k]
    pdlg = P28.multi([T(f"{NAME.upper()}'S WAYS", COL, bold=True)], [P28.body([T(n, COL, bold=True), T(f' - {d}.', 'gray')], 340) for n, d in powers],
                     [P28.btn([T('« Back', 'gray')], MENU + 5, width=150)], columns=1, exit_label='Close')
    fn(f'{pfx}/powers', [f'scoreboard players set @s bm.menu {MENU}', f'dialog show @s {snbt(pdlg)}'])
    intro = {'dw': [T('Dennis', DW_C, bold=True), T(' - dwarf, miner, brawler. ', 'gray'), T('Fortune V on every ore while he walks with you; gold and a wrench for anything that bites.', 'white')],
             'pi': [T('Pistachio', PI_C, bold=True), T(' - ghost, butler of the Omega Palace. ', 'gray'), T('Looting V on every kill while he walks with you; spirits from his cloche for anything that bites.', 'white')]}[k]
    dlg = lambda out: P28.multi([T(ITEMS[c['item']]['name'], COL, bold=True)], [P28.body(intro, 300)],
                                ([P28.btn(T('Sit / follow', 'white', bold=True), MENU + 1, width=150), P28.btn(T('Send him home', 'gray'), MENU + 9, width=150)] if out else
                                 [P28.btn(T(f'Call for {NAME}', COL, bold=True), MENU + 8, width=150)]) +
                                [P28.btn(T(f'{NAME}\'s ways', COL, bold=True), MENU + 4, width=150, tooltip=T('How he fights - and what he does for you.', 'gray')),
                                 P28.btn(T('Wardrobe', COL, bold=True), MENU + 2, width=150, tooltip=T('His looks - and his aura, if you have it.', 'gray'))],
                                columns=2, exit_label='Close')
    fn(f'{pfx}/menu', [f'scoreboard players set @s bm.menu {MENU}', 'scoreboard players set #out bm.rng 0',
                       f'execute if entity @e[type=minecraft:wolf,tag={sel2}] run scoreboard players set #out bm.rng 1',
                       f'execute if score #out bm.rng matches 1 run return run dialog show @s {snbt(dlg(True))}', f'dialog show @s {snbt(dlg(False))}'])
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {MENU + n} run return run function bm:{pfx}/act' for n in (1, 2, 4, 5, 8, 9)]
    fn(f'{pfx}/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                      f'execute if score #act bm.pay matches {MENU + 2} run return run function bm:p119/plain/{W}',
                      f'execute if score #act bm.pay matches {MENU + 4} run return run function bm:{pfx}/powers',
                      'scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add {sel2}',
                      f'execute if score #act bm.pay matches {MENU + 5} run function bm:{pfx}/menu',
                      f'execute if score #act bm.pay matches {MENU + 8} unless entity @e[type=minecraft:wolf,tag={sel2}] run function bm:{pfx}/try_summon',
                      f'execute if score #act bm.pay matches {MENU + 8} if entity @e[type=minecraft:wolf,tag={sel2}] run function bm:{pfx}/recall',
                      f'execute if score #act bm.pay matches {MENU + 1} if entity @e[type=minecraft:wolf,tag={sel2}] run function bm:{pfx}/sit',
                      f'execute if score #act bm.pay matches {MENU + 9} if entity @e[type=minecraft:wolf,tag={sel2}] run function bm:{pfx}/dismiss',
                      f'tag @e[tag={sel2}] remove {sel2}'])
    sit_lines = {'dw': ("Right, let's be off. Mind you keep up.", "I'll sit a bit. These boots weren't made for walkin'."),
                 'pi': ('Onward, sir.', 'I shall take a seat. One does float about so.')}[k]
    tw = f'@e[type=minecraft:wolf,tag={sel2},limit=1]'
    fn(f'{pfx}/sit', [f'execute store success score #s0 bm.rng if data entity {tw} {{Sitting:1b}}',
                      f'execute if score #s0 bm.rng matches 1 run data modify entity {tw} Sitting set value 0b',
                      f'execute if score #s0 bm.rng matches 0 run data modify entity {tw} Sitting set value 1b',
                      'execute if score #s0 bm.rng matches 1 run ' + fysay(sit_lines[0]), 'execute if score #s0 bm.rng matches 0 run ' + fysay(sit_lines[1])])
    # ---- his click box (riding him): right-click him - sit / stand
    hit_tag, clk = f'bm.{k}hit', f'bm.{k}clk'
    fn(f'{pfx}/box', ['execute if entity @s[tag=bm.ffpet] run return 0', f'execute if function bm:{pfx}/has_hit run return 0',
                      f'summon minecraft:interaction ~ ~ ~ {{Tags:["{hit_tag}","bm.{k}hnew"],width:1.0f,height:{2.0 if k == "dw" else 2.4}f,response:1b}}',
                      f'ride @e[type=minecraft:interaction,tag=bm.{k}hnew,limit=1,sort=nearest] mount @s', f'tag @e[tag=bm.{k}hnew] remove bm.{k}hnew'])
    fn(f'{pfx}/has_hit', [f'execute on passengers if entity @s[type=minecraft:interaction,tag={hit_tag}] run return 1', 'return 0'])
    second.append(f'execute as @e[type=minecraft:interaction,tag={hit_tag}] unless function bm:p20/frog/has_vehicle run kill @s')
    fast += [f'execute as @e[type=minecraft:interaction,tag={hit_tag}] if data entity @s interaction run function bm:{pfx}/click',
             f'execute as @e[type=minecraft:interaction,tag={hit_tag}] if data entity @s attack run data remove entity @s attack']
    fn(f'{pfx}/click', [f'execute on vehicle run tag @s add {clk}', f'execute on target at @s run function bm:{pfx}/who', f'tag @e[tag={clk}] remove {clk}',
                        'data remove entity @s interaction'])
    cw = f'@e[type=minecraft:wolf,tag={clk},limit=1]'
    fn(f'{pfx}/who', [f'execute if score @s {S("hc")} matches 1.. run return 0', f'scoreboard players set @s {S("hc")} 10', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      f'execute unless score {cw} bm.pid = #me bm.pid run return run ' + fysay({'dw': 'Hands off, stranger - I\'m with someone.', 'pi': 'I am engaged elsewhere today, sir.'}[k]),
                      f'execute store success score #s0 bm.rng if data entity {cw} {{Sitting:1b}}',
                      f'execute if score #s0 bm.rng matches 1 run data modify entity {cw} Sitting set value 0b',
                      f'execute if score #s0 bm.rng matches 0 run data modify entity {cw} Sitting set value 1b',
                      'execute if score #s0 bm.rng matches 1 run ' + fysay(sit_lines[0]), 'execute if score #s0 bm.rng matches 0 run ' + fysay(sit_lines[1])])
    tick.append(f'scoreboard players remove @a[scores={{{S("hc")}=1..}}] {S("hc")} 1')
    G.FUNCS['admin/uninstall'].insert(0, f'kill @e[type=minecraft:interaction,tag={hit_tag}]')
    # ---- fainting
    tick += [f'execute as @e[type=minecraft:item_display,tag=bm.{k}p_pet,tag=bm.{k}p_body,tag=!{fade}] at @s run function bm:{pfx}/check',
             f'scoreboard players remove @e[type=minecraft:item_display,tag={fade}] {S("l")} 1',
             f'kill @e[type=minecraft:item_display,tag={fade},scores={{{S("l")}=..0}}]']
    fn(f'{pfx}/check', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #al bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={pet},distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #al bm.rng 1',
                        f'execute if score #al bm.rng matches 1 run return run scoreboard players set @s {S("z")} 0',
                        f'scoreboard players add @s {S("z")} 1', f'execute if score @s {S("z")} matches 4.. run function bm:{pfx}/fell'])
    fn(f'{pfx}/fell', [f'function bm:{pfx}/fade', f'execute as @a if score @s bm.pid = #me bm.pid run function bm:{pfx}/cooldown'])
    faint = {'dw': '"Ugh... just... a scratch... gimme a minute..."', 'pi': '"I appear to have... passed on. Again..."'}[k]
    fn(f'{pfx}/cooldown', [f'scoreboard players set @s {S("cd")} {PET_CD}',
                           tellraw('@s', PREFIX + [T(f'{NAME} faints! ', COL, bold=True), T(faint + ' ', LINE),
                                                   T(f'{ITEMS[c["item"]]["name"]} needs {PET_CD // 60} minutes before he can come back.', 'gray')])])
    fn(f'{pfx}/fade', [f'execute as @e[type=minecraft:item_display,tag=bm.{k}p_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run function bm:{pfx}/fade1'] + burst +
       ['playsound minecraft:block.glass.break neutral @a[distance=..20] ~ ~ ~ 0.4 1.6'])
    gcol = 16760896 if k == 'dw' else 8048784
    fn(f'{pfx}/fade1', [f'tag @s add {fade}', f'scoreboard players set @s {S("l")} 3',
                        f'data merge entity @s[type=minecraft:item_display] {{brightness:{{block:15,sky:15}},Glowing:1b,glow_color_override:{gcol}}}'])
    second.append(f'scoreboard players remove @a[scores={{{S("cd")}=1..}}] {S("cd")} 1')
    G.FUNCS['p62/died'].insert(-1, f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/go')
    fn(f'{pfx}/go', ['scoreboard players add #gone bm.rng 1', f'function bm:{pfx}/fade', 'execute on passengers run kill @s[type=!minecraft:player]',
                     'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    P73.follow_rules(G, (W, 'wolf', pet, c['item'], f'{pfx}/go', NAME, S('fg'), f'{pfx}/summon_here'), second)
    L = G.FUNCS[f'p73/fol/{W}']
    j = next(i for i, l in enumerate(L) if ' if items entity ' in l)
    L.insert(j, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0')
    G.FUNCS['p58/count'][-1:-1] = [f'execute as @e[type=minecraft:wolf,tag={pet}] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1']
    G.FUNCS['p57/pulse'] += [l.replace('tag=bm.celipet', f'tag={pet}') for l in G.FUNCS['p57/pulse'] if 'tag=bm.celipet' in l]
    far = G.FUNCS[f'p73/fol/{W}_far']
    assert far[0] == f'function bm:{pfx}/go', far[0]
    far.insert(0, f'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run function bm:p103/fol/wait_{W}')
    fn(f'p103/fol/wait_{W}', [f'tag @a[tag=bm.fown] add bm.ow_{W}', f'function bm:{pfx}/go',
                              tellraw('@a[tag=bm.fown]', PREFIX + [T(f'{NAME} waits outside the vault', COL), T(' - your Raid Crew answers inside. ', 'gray'),
                                                                   T('(Back with you when you\'re home.)', 'dark_gray')]), 'tag @a remove bm.fown'])
    fn(f'p103/fol/back_{W}', [f'tag @s remove bm.ow_{W}', f'function bm:{pfx}/try_summon'])
    G.FUNCS['p103/fol/tick'].append(f'execute if entity @s[tag=bm.ow_{W}] run function bm:p103/fol/back_{W}')

    # ---- joining you (phase162: the fiftieth trade)
    join = {'dw': ["Fifty trades, lad. Fifty! You're alright, you are.", "Tell you what - I'll come along. Somebody's got to keep you in gold. Here: blow that horn and I'll come runnin'."],
            'pi': ['Fifty transactions, sir. The Palace has never had so reliable a supplier.',
                   'Cecil can mind the house. I shall accompany you - lift the lid of this little cloche and I shall come.']}[k]
    fn(f'{pfx}/recruit', [f'tag @s add bm.{k}met', give(c['item'])] + [fychat(l) for l in join] +
       [tellraw('@s', [T(NAME, COL, bold=True), T(f' joins you! ({ITEMS[c["item"]]["name"]}: use it to call him; sneak + use: his menu. '
                                                  'His Raid Contract is at the Recruiter in the den.)', 'gray', italic=True)]),
        'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 1.2', f'advancement grant @s only bm:story/{k}_join'])
    G.wjson(f'bm/advancement/story/{k}_join.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
          'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': f'bm:{c["item"]}'}}, 'title': T({'dw': 'Thick as Thieves', 'pi': 'Service Included'}[k], COL),
                      'description': T(f'Trade with {NAME} fifty times - and he joins you', 'gray'), 'frame': 'goal', 'show_toast': True, 'announce_to_chat': True,
                      'hidden': False}})
    has = lambda iid: [f'execute if items entity @s container.* {holds(iid)} run scoreboard players set #has bm.rng 1',
                       f'execute if items entity @s weapon.offhand {holds(iid)} run scoreboard players set #has bm.rng 1',
                       f'execute if items entity @s enderchest.* {holds(iid)} run scoreboard players set #has bm.rng 1']
    fn(f'{pfx}/reissue', ['scoreboard players set #has bm.rng 0'] + has(c['item']) +
       ['scoreboard players operation #me bm.pid = @s bm.pid', f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run scoreboard players set #has bm.rng 1',
        'execute if score #has bm.rng matches 1 run return 0', give(c['item']), fychat({'dw': 'Lost my horn? Good thing I\'ve two. Keep this one safe.', 'pi': 'Mislaid the cloche, sir? I keep a spare.'}[k])])
    # admin
    fn(f'admin/{W}', [give(c['item']), f'tag @s add bm.{k}met', say(f"{ITEMS[c['item']]['name']}. (He keeps a room in the Black Market, under the vault-door balcony.)", COL)])
    G.FUNCS['admin/help'].append(tellraw('@s', [T(f'/function bm:admin/{W}', 'yellow'), T(f"  {ITEMS[c['item']]['name']} (meet him in the Black Market: 50 trades and he joins you)", 'gray')]))
    G.FUNCS['admin/uninstall'][0:0] = [f'kill @e[type=minecraft:item_display,tag=bm.{k}p]']


def ambient(k, pfx):
    if k == 'pi':                                    # (a ghost: a wisp of soul-fire now and then, and his green glow)
        return ['execute if predicate bm:p141/now_and_then run particle minecraft:soul ~ ~1.2 ~ 0.25 0.4 0.25 0.01 1']
    return []


def pairs(G, fn, tellraw, title, PREFIX, foe, second):
    """Spade and Spoon (Dennis + Pistachio) and the Omega Palace (Cecil + Pistachio), as phase133's pairs; the Crown's Prospect trio"""
    import phase100 as P100_
    pet = lambda typ, tag: f'execute as @e[type=minecraft:{typ},tag={tag},distance=..16] if score @s bm.pid = #me bm.pid'
    VO = {'Dennis': (DW_C, DW_LINE), 'Pistachio': (PI_C, PI_LINE), 'Cecil': ('#b48cff', '#e8d8ff')}
    say2 = lambda who, txt: tellraw('@a[tag=bm.p163o]', [T(f'{who}: ', VO[who][0], bold=True), T(f'"{txt}"', VO[who][1])])
    PAIRS = {
        'spade': ('Spade and Spoon', '#c8d070', ('wolf', 'bm.dwpet'),
                  [('Dennis', 'A ghost. Course it is. Do ghosts tip?'), ('Pistachio', 'Only in kind, Mr Dennis. I shall polish your helmet.')],
                  [('Dennis', 'You dig, I dig. You float, I... still dig.', 'Pistachio', 'A fine division of labour, sir.'),
                   ('Pistachio', 'Mr Dennis, your boots. On my clean floor.', 'Dennis', "It's a CAVE, Pistachio!")]),
        'palace': ('The Omega Palace', '#b48cff', ('wolf', 'bm.cecilpet'),
                   [('Cecil', 'Pistachio. You left the kettle on. Again.'), ('Pistachio', 'I am a ghost, Master Cecil. The kettle is ALWAYS on.')],
                   [('Pistachio', 'Shall I set a place for the guest at dinner, Master Cecil?', 'Cecil', 'Only if they survive the walk home.'),
                    ('Cecil', 'Stop dusting my staff.', 'Pistachio', 'It is a matter of house pride, sir.')])}
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.p163 dummy']
    G.OBJECTIVES += ['bm.p163']
    first = lambda k: f'execute as @a[tag=bm.p163o] unless entity @s[advancements={{bm:story/pair_{k}=true}}] run function bm:p163/{k}_first'
    bant = lambda k: ['scoreboard players add @s bm.p163 1', f'execute if score @s bm.p163 matches 150.. run function bm:p163/{k}_banter']
    for k, (nm, col, partner, intro, banter) in PAIRS.items():
        fn(f'p163/{k}_first', [f'advancement grant @s only bm:story/pair_{k}', tellraw('@s', PREFIX + [T(f'{nm}! ', col, bold=True), T('A new pair - see the README for what it gives.', 'gray')])] +
           [tellraw('@s', [T(f'{w}: ', VO[w][0], bold=True), T(f'"{t}"', VO[w][1])]) for w, t in intro])
        G.wjson(f'bm/advancement/story/pair_{k}.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:pi_cloche'}}, 'title': T(nm, 'yellow'),
                            'description': T({'spade': 'Dennis and Pistachio, side by side', 'palace': 'Cecil and Pistachio - the Omega Palace on the road'}[k], 'gray'),
                            'frame': 'task', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
        for j, (a, ta, b, tb) in enumerate(banter):
            fn(f'p163/{k}_say{j}', [say2(a, ta), say2(b, tb)])
        fn(f'p163/{k}_banter', ['scoreboard players set @s bm.p163 0', f'execute store result score #r bm.rng run random value 0..{len(banter) - 1}'] +
           [f'execute if score #r bm.rng matches {j} run function bm:p163/{k}_say{j}' for j in range(len(banter))])
    # (as each Pistachio, every second: is his owner near, and which of his partners walk with them?)
    second.append('execute as @e[type=minecraft:wolf,tag=bm.pipet,tag=!bm.ffpet] at @s run function bm:p163/pairs')
    fn('p163/pairs', ['scoreboard players operation #me bm.pid = @s bm.pid', 'execute on owner if entity @s[distance=..24] run tag @s add bm.p163o',
                      'execute unless entity @a[tag=bm.p163o] run return 0', 'scoreboard players set #pd2 bm.rng 0', 'scoreboard players set #pc2 bm.rng 0',
                      f'{pet("wolf", "bm.dwpet")} run scoreboard players set #pd2 bm.rng 1', f'{pet("wolf", "bm.cecilpet")} run scoreboard players set #pc2 bm.rng 1',
                      'execute if score #pd2 bm.rng matches 1 run function bm:p163/spade', 'execute if score #pc2 bm.rng matches 1 run function bm:p163/palace',
                      'tag @a remove bm.p163o'])
    fn('p163/spade', ['effect give @a[tag=bm.p163o] minecraft:haste 3 1 true', 'effect give @a[tag=bm.p163o] minecraft:luck 3 0 true',
                      'effect give @s minecraft:resistance 3 0 true', f'{pet("wolf", "bm.dwpet")} run effect give @s minecraft:resistance 3 0 true', first('spade')] + bant('spade'))
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.p163s dummy']
    G.OBJECTIVES += ['bm.p163s']
    fn('p163/palace', ['execute as @a[tag=bm.p163o] unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true',
                       'scoreboard players add @s bm.p163s 1', 'execute if score @s bm.p163s matches 30.. as @a[tag=bm.p163o] at @s run function bm:p163/supper',
                       'execute if score @s bm.p163s matches 30.. run scoreboard players set @s bm.p163s 0',
                       'effect give @s minecraft:resistance 3 0 true', f'{pet("wolf", "bm.cecilpet")} run effect give @s minecraft:resistance 3 0 true', first('palace')] + bant('palace'))
    fn('p163/supper', ['effect give @s minecraft:saturation 1 1 true', 'playsound minecraft:entity.generic.eat player @s ~ ~ ~ 0.6 1.2',
                       'particle minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 2',
                       title('@s', 'actionbar', [T('Pistachio: ', PI_C, bold=True), T('A little something from the Palace kitchen, sir.', PI_LINE)])])
    # the trio (phase100 tags who's there and calls p100/<key> as the player)
    each = lambda mem, cmd: [f'execute as @e[type=minecraft:{P100_.WHO[m][0]},tag={P100_.WHO[m][1]},distance=..24] if function bm:p100/is_mine run {cmd}' for m in mem]
    regen = 'execute unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true'
    fn('p100/prospect', ['effect give @s minecraft:strength 3 0 true', 'effect give @s minecraft:resistance 3 0 true', 'effect give @s minecraft:haste 3 1 true'] +
       each(('emma', 'leo', 'dennis'), 'effect give @s minecraft:resistance 3 0 true') + each(('emma', 'leo', 'dennis'), regen) + ['function bm:p100/banter_tick'])
    G.wjson('bm/advancement/story/trio_prospect.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:dw_horn'}}, 'title': T("The Crown's Prospect", 'yellow'),
                        'description': T('Walk with Emma, Leo and Dennis at once', 'gray'), 'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})

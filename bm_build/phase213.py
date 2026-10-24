"""2.94: THE 8-BIT TRIO - Emma, Leo and Cecil as they'd look in an old cartridge game: hidden followers of their own, pixel
sprites (PixelLab, from the owner's art - pxart.py), flat and two-sided (2.94c: a back of their own; no longer billboarded), every
animation frame by frame.

FINDING THEM - THE GLITCHED CARTRIDGE (phase214): a cartridge that drops from any raid tier. Use it beside your own Emma, Leo
or Cecil and the game glitches: their 8-bit self tumbles out of the screen. Right-click it, and it hands you its cartridge.
Each cartridge: use - call them (again: call them over); sneak + use - their menu (sit / send home, their ways, the wardrobe:
the palettes - Game Boy, Virtual Boy, Sepia; Gilded, Diamond and Netherite).

8-BIT EMMA (the Pixel Princess)
  FIREBALL     a monster 3-14 away, every 2.5 s: a bouncing fireball (7, and it burns).
  STOMP        a monster within 3, every 4 s: she jumps on its head (10 to everything within 3, and it's dazed).
  EXTRA LIFE   you down to 4 hearts: a 1-UP - Instant Health and Absorption (once a minute).
  POWER STAR   (charged, every minute) three monsters within 8: she glows - every monster within 8 takes 12; you, Resistance and Speed.
8-BIT LEO (the Pixel Knight)
  SWORD BEAM   only while your health is full: his sword fires a beam at a monster 3-16 away (8).
  SLASH        a monster within 3, every 1.5 s: a sweep (8 to everything within 3).
  SHIELD BLOCK you hurt and a monster near: his shield - you, Resistance II; the monsters within 4 shoved back (every 20 s).
  COIN BLOCK   every 45 s, beside you and no fight near: he punches a ? block - coins (experience) and a little Luck.
  SPIN ATTACK  (charged, every minute) three monsters within 6: 14 to every one of them.
8-BIT CECIL (the Pixel Wizard)
  HEX BOLT     a monster 3-16 away, every 2.5 s: a bolt of pixel magic (7, and it withers).
  HEX          three monsters within 7, every 15 s: a magic circle - slowed, weakened and lit up.
  GAME OVER    (charged, every minute) a monster within 9: GAME OVER - 18 to every monster within 9.
All three together: THE 8-BIT BANE (phase100) - and at the Hollow throne, a pixel Apophiss (phase215).
A frame keeps them, a display case shows them, Cecil sells their pixel dolls, the Tailor their palettes, the Recruiter their
Raid Contracts; and they're on the Partner Wheel."""
import os
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import pxart
import rigpet as RP
import phase141 as P141
import phase134 as P134
import phase210 as FXS
import phase212 as P212

FOE = 'type=#bm:hostile,tag=!bm.npc'
HERE = os.path.dirname(os.path.abspath(__file__))
# the palettes (phase99 looks): dark - mid - light, by brightness
LOOKS = {1: ('Game Boy', ('#0f380f', '#306230', '#9bbc0f')), 2: ('Virtual Boy', ('#1a0000', '#a01010', '#ff6060')),
         3: ('Sepia Print', ('#2a1a0a', '#8a6a3a', '#f4e4bc')), 4: ('Gilded Pixels', ('#3a2806', '#c8962a', '#ffe08a')),
         5: ('Diamond Pixels', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Pixels', ('#141014', '#4a4046', '#9a8c94'))}


def dust(c, s=1.0):
    return f'minecraft:dust{{color:[{c[0]},{c[1]},{c[2]}],scale:{s}}}'


def _breathe(im):
    """a seated sprite breathing: everything above its middle a pixel lower"""
    from PIL import Image
    bb = im.getbbox()
    if not bb:
        return im
    mid = (bb[1] + bb[3]) // 2
    out = im.copy()
    out.paste(Image.new('RGBA', (im.width, mid - bb[1] + 1), (0, 0, 0, 0)), (0, bb[1]))
    out.alpha_composite(im.crop((0, bb[1], im.width, mid)), (0, bb[1] + 1))
    return out


def sprite(key, sp, anims, height):
    S = pxart.Sprite(key, sp, height, anims)
    last = S.frames['sit'][-1]
    S.frames['rest'] = [last, _breathe(last)]                      # (seated: the last frame of sitting down, breathing)
    lb = S.backs['sit'][-1]
    S.backs['rest'] = [lb, _breathe(lb)]                           # (2.94c: and from behind)
    return S


def cycle(S):
    """the shared states: idle, walk, run, jump, sit (sitting down, then breathing), the hello"""
    R = lambda a, e, st=0: [(st + e * i, f'{a}_{i}') for i in range(len(S.frames[a]))]
    n = lambda a: len(S.frames[a])
    sit = R('sit', 3) + [(3 * n('sit') + 30 * i, f'rest_{i % 2}') for i in range(40)]
    idle = [(0, 'idle_a')] + R('idle', 5)[1:]                     # (idle_a: the first frame - the pose a rig is grown in)
    return {0: (5 * n('idle'), idle), 1: (2 * n('walk'), R('walk', 2)), 2: (n('walk'), R('walk', 1)),
            3: (None, [(0, 'walk_4')]), 4: (None, sit), 6: (None, R('idle', 3)), 10: (2 * n('walk'), R('walk', 2))}


class Base(RP.Cfg):
    PET_HP, PET_CD = 50, 120
    ATTRS = dict(armor=6, attack_damage=4, movement_speed=0.34, follow_range=32, step_height=1.1)
    SCALE = 0.9
    HIT = (0.9, 1.8)
    BILLBOARD = None                                              # (2.94c: flat and two-sided, turned as she is - never billboarded)
    SWAP = ()
    pron, they = 'her', 'she'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
    FACE = {e: None for e in EXPR}
    DUR = {}
    FADE_SOUND = 'playsound minecraft:block.note_block.bit neutral @a[distance=..20] ~ ~ ~ 1 0.5'
    SUMMON_EXTRA = ['playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 1 1.5',
                    'playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 1 2']
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.1 6'
    MEET_HINT = 'Right-click them.'
    BURST = ['particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.2 16', 'particle minecraft:dust{color:[1.0,1.0,1.0],scale:1.2} ~ ~1 ~ 0.4 0.6 0.4 0 10',
             'particle minecraft:poof ~ ~0.6 ~ 0.3 0.3 0.3 0.02 6']
    S = None


def make(key, W, NAME, COL, LINE, pfx, ab, q, MENU, ITEM, sp, anims, height, pron='her'):
    S = sprite(key, sp, anims, height)
    A = pxart.Rig(S, f'{ab}_')
    A.POSES.update({f'rest_{i}': {'_frame': f'rest_{i}'} for i in range(2)})
    A.EXTRA_TAGS = {}

    class C(Base):
        pass
    C.W, C.NAME, C.COL, C.LINE, C.pfx, C.ab, C.q, C.MENU, C.ITEM, C.A, C.S = W, NAME, COL, LINE, pfx, ab, q, MENU, ITEM, A, S
    C.pron, C.they = pron, {'her': 'she', 'him': 'he'}[pron]
    C.POSE_EXTRA = staticmethod(lambda name, psel: [S.frame_cmd(psel('head'), A.POSES[name]['_frame'])])
    C.CYCLE = cycle(S)
    C.ENC_POSES = [(5 * i, f'idle_{i}') for i in range(len(S.frames['idle']))] + [(40 + 3 * i, f'walk_{i}') for i in range(len(S.frames['walk']))]
    return C


# ------------------------------------------------------------------------------------------------ the three
EMMA = make('emma', 'pxemma', '8-Bit Emma', '#ff6ac8', '#ffd0ec', 'p213e', 'xm', 'xn', 2980, 'cart_emma', 'pxe_',
            {a: (a, None) for a in ('idle', 'walk', 'sit', 'fireball', 'stomp', 'power')}, 1.6)
LEO = make('leo', 'pxleo', '8-Bit Leo', '#4ab0ff', '#d8f0ff', 'p213l', 'xl', 'xo', 3020, 'cart_leo', 'pxl_',
           {a: (a, None) for a in ('idle', 'walk', 'sit', 'beam', 'slash', 'block')}, 1.7, 'him')
_CECIL_OK = os.path.isdir(os.path.join(HERE, 'ref', 'pixellab', 'chars', 'cecil_px'))
CECIL = make('cecil_px', 'pxcecil', '8-Bit Cecil', '#b070ff', '#e8d8ff', 'p213c', 'xc', 'xd', 3060, 'cart_cecil', 'pxc_',
             {a: (a, None) for a in ('idle', 'walk', 'sit', 'attack', 'hex')}, 1.5, 'him') if _CECIL_OK else None
ALL = [c for c in (EMMA, LEO, CECIL) if c]
ORIG = {'pxemma': 'emma', 'pxleo': 'leo', 'pxcecil': 'cecil'}                 # (whose 8-bit self each is)

E, L = EMMA, LEO
E.CYCLE.update({7: (None, [(2 * i, f'fireball_{i}') for i in range(9)]), 8: (None, [(2 * i, f'stomp_{i}') for i in range(9)]),
                11: (None, [(3 * i, f'power_{i}') for i in range(7)]), 13: (None, [(2 * i, f'power_{i}') for i in range(7)])})
E.QUIPS = ['"It\'s-a me! ...no, wait, that\'s someone else."', '"Everything\'s so... blocky. I love it!"', '"Do I look sixteen colours to you? Because I feel it."',
           '"Sir Leo looks adorable in pixels. Don\'t tell him I said that."', '"Press START to continue!"', '"If I fall in a pit, I respawn, right? ...Right?"']
E.HELLO = ('"Player Two has entered the game!"', '"Ready, player one!"', '"Saving... don\'t turn off the power!"')
E.SIT = ('"Unpaused!"', '"PAUSE." (she sits down, swinging her pixel feet)')
E.FAINT = 'GAME... OVER...'
E.NOT_YOURS = '"Sorry - I\'m on someone else\'s save file!"'
E.POWERS = [('Fireball', 'a monster 3-14 away, every 2.5 s: a bouncing fireball (7, and it burns)'),
            ('Stomp', 'a monster within 3, every 4 s: she jumps on its head - 10 to everything within 3, and it\'s dazed'),
            ('Extra Life', 'you down to 4 hearts: a 1-UP - Instant Health and Absorption (once a minute)'),
            ('Power Star', 'charged, every minute, three monsters within 8: every one of them takes 12; you, Resistance and Speed')]
E.INTRO = [T('8-Bit Emma', E.COL, bold=True), T(' - the princess, as an old cartridge game would draw her. ', 'gray'), T('Fireballs, stomps and a spare life.', 'white')]
E.ADV = ('Player Two Has Entered', 'Shake 8-Bit Emma out of a Glitched Cartridge')
E.ADMIN_HINT = 'A Glitched Cartridge used beside your Emma shakes her out.'

L.CYCLE.update({7: (None, [(2 * i, f'beam_{i}') for i in range(9)]), 8: (None, [(2 * i, f'slash_{i}') for i in range(9)]),
                9: (None, [(2 * i, f'block_{i}') for i in range(7)]), 12: (None, [(i, f'slash_{i % 9}') for i in range(18)]),
                14: (None, [(3 * i, f'idle_{i % 5}') for i in range(6)])})
L.QUIPS = ['"It\'s dangerous to go alone. So I\'m coming."', '"My sword only fires beams when you\'re at full health. Those are the rules."',
           '"Why does every pot I pass make me want to smash it?"', '"The Princess insists I look \'adorable\'. I look valiant."',
           '"I found a ? block. I hit it. I regret nothing."', '"Sixteen pixels of pure knighthood."']
L.HELLO = ('"Hyaah! Coming!"', '"Sir Leo, 8-bit edition - at your service."', '"Saving your game. Farewell!"')
L.SIT = ('"Back to the quest!"', '"A rest at the save point." (he sits, sword across his knees)')
L.FAINT = 'Sir Leo has... fallen... (insert coin)'
L.NOT_YOURS = '"My quest is with another player."'
L.POWERS = [('Sword Beam', 'only while your health is full: his sword fires a beam at a monster 3-16 away (8)'),
            ('Slash', 'a monster within 3, every 1.5 s: a sweep - 8 to everything within 3'),
            ('Shield Block', 'you hurt and a monster near: his shield - you, Resistance II; the monsters within 4 shoved back (every 20 s)'),
            ('Coin Block', 'every 45 s, beside you and no fight near: he punches a ? block - coins (experience) and a little Luck'),
            ('Spin Attack', 'charged, every minute, three monsters within 6: 14 to every one of them')]
L.INTRO = [T('8-Bit Leo', L.COL, bold=True), T(' - the knight, as an old cartridge game would draw him. ', 'gray'), T('Sword beams at full health.', 'white')]
L.ADV = ("It's Dangerous to Go Alone", 'Shake 8-Bit Leo out of a Glitched Cartridge')
L.ADMIN_HINT = 'A Glitched Cartridge used beside your Leo shakes him out.'

if CECIL:
    Cc = CECIL
    Cc.CYCLE.update({7: (None, [(2 * i, f'attack_{i}') for i in range(len(Cc.S.frames['attack']))]),
                     11: (None, [(3 * i, f'hex_{i}') for i in range(len(Cc.S.frames['hex']))]),
                     12: (None, [(3 * i, f'attack_{i}') for i in range(len(Cc.S.frames['attack']))] + [(30, 'hex_0')])})
    Cc.QUIPS = ['"I have been reduced to sixty-four pixels. I have never been more powerful."', '"Do not call it a sprite. I am a SORCERER."',
                '"The serpent in this cartridge is mine. Mine!"', '"Insert coin? I accept souls."', '"Hmph. My grin is still jagged. Good."']
    Cc.HELLO = ('"I come. Not because you called - because I chose to."', '"The sorcerer of the cartridge rises."', '"I shall return... in the sequel."')
    Cc.SIT = ('"Enough rest. Onward."', '"I shall... meditate." (he sits, the staff crystal humming)')
    Cc.FAINT = 'This is... not... the final boss...'
    # (2.94f: his GAME OVER is charged - it charges from his summoning, so it never goes off the moment he's called)
    Cc.SUMMON_EXTRA = Cc.SUMMON_EXTRA + [f'scoreboard players set @e[type=minecraft:wolf,tag=bm.{Cc.ab}pet,distance=..4,sort=nearest,limit=1] bm.{Cc.q}gc 1200']
    Cc.NOT_YOURS = '"You are not my player."'
    Cc.POWERS = [('Hex Bolt', 'a monster 3-16 away, every 2.5 s: a bolt of pixel magic (7, and it withers)'),
                 ('Hex', 'three monsters within 7, every 15 s: a magic circle - slowed, weakened and lit up'),
                 ('Game Over', 'charged, every minute, a monster within 9: GAME OVER - 18 to every monster within 9')]
    Cc.INTRO = [T('8-Bit Cecil', Cc.COL, bold=True), T(' - the wizard, as an old cartridge game would draw him. ', 'gray'), T('Hexes, bolts and a Game Over.', 'white')]
    Cc.ADV = ('Sixty-Four Pixels of Power', 'Shake 8-Bit Cecil out of a Glitched Cartridge')
    Cc.ADMIN_HINT = 'A Glitched Cartridge used beside your Cecil shakes him out.'

import phase95 as _FX
for _C in ALL:
    RP.register(_C)
    _h = _FX.FOLK[_C.W]
    _FX.FOLK[_C.W] = (_h[0], _h[1], f'type=minecraft:item_display,tag=bm.{_C.ab}p_body,tag=bm.{_C.ab}p_pet') + _h[3:]      # (no faces: a sprite's frame is its head's custom_model_data - moods land on its empty body)
    _o = ORIG[_C.W]
    item(_C.ITEM, TOTEM, f"{_C.NAME}'s Cartridge", _C.COL,
         [f'A grey game cartridge. The label shows {_C.NAME[6:]}', 'in sixteen colours - and it hums.',
          (f'Use: call {_C.NAME} (again: call {_C.pron} over).', 'blue'), (f'Sneak + use: {RP.POS[_C.pron]} menu - the palettes.', 'blue'),
          (f'If {_C.they} faints: 2 minutes before {_C.they} can return.', 'gray'), ('"Blow on it if it doesn\'t work."', 'dark_gray')],
         model=f'bm:{_C.ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
    _d = f'doll_{_C.W}'
    item(_d, TOTEM, f'{_C.NAME} Doll', _C.COL, [f'A pixel doll of {_C.NAME} - every pixel a little block.', ('Right-click a block: set it down.', 'blue'),
                                               ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
         model=f'bm:{_d}', stack=16, cat='fun', comps=hold('none'))
    HOLD[_d] = f'bm:p141/{_d}/use'
    P141.DOLLS.append((_d, _C.NAME, _C.COL, f'A pixel doll of {_C.NAME} - every pixel a little block.', 'minecraft:electric_spark',
                       'minecraft:block.note_block.bit', 'minecraft:electric_spark'))
    # (the display case: the standing sprite's own size - feet on the ground, as wide as the art)
    _bb = _C.S.frames['idle'][0].getbbox()
    _w = (_bb[2] - _bb[0]) / _C.S.ppb
    P134.FIT[_C.ITEM] = (0.0, round((_bb[3] - _bb[1]) / _C.S.ppb, 3), round(-_w / 2, 3), round(_w / 2, 3), -0.05, 0.05)

# the phase138 looks: every frame of each sprite recoloured (the head's frame-picker is copied for each look)
import phase138 as P138
for _C in ALL:
    P138.RECOL[_C.W] = ('phase213', tuple(f'{_C.S.prefix}{n}' for n in _C.S.frame_names()))

# the 8-bit Serpent's Bane (phase100): all three together
import phase100 as P100
if CECIL:
    P100.TRIOS['pxbane'] = ("The 8-Bit Bane", '#ffe060', ('pxemma', 'pxleo', 'pxcecil'), 'Press Start to Bane',
                            'Walk with 8-Bit Emma, 8-Bit Leo and 8-Bit Cecil at once - the serpent hunters, in sixteen colours')
    P100.BANTER['pxbane'] = [('8-Bit Emma', 'We\'re all so small and square! Isn\'t it wonderful?', '8-Bit Leo', 'It\'s... very efficient, Princess.'),
                             ('8-Bit Cecil', 'Somewhere in this cartridge there is a serpent with our names on its high score table.', '8-Bit Emma', 'Then let\'s beat it!'),
                             ('8-Bit Leo', 'If we fall in a pit we lose a life. Be careful.', '8-Bit Cecil', 'I have never lost a life. I have only... respawned strategically.')]


def _doll(C, tex):
    """the doll: the standing sprite in voxels, its back the back view (2.94b: it was the front again - a face on the back of
    Cecil's hood)"""
    key = {'pxemma': 'emma', 'pxleo': 'leo', 'pxcecil': 'cecil_px'}[C.W]
    return pxart.voxel(pxart.standing(key), tex, height=15.0, back=pxart.standing(key, 'north'))


def textures():
    T_ = {}
    for C in ALL:
        T_.update(C.S.textures())
        T_[f'doll_{C.W}_t'] = _doll(C, 'x')[2]
    return T_


def _icon(col):
    """a grey cartridge, its label the follower's colour"""
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((2, 1, 13, 14), fill=hexc('#8a8a92'), outline=hexc('#3a3a42'))
    d.rectangle((3, 1, 12, 2), fill=hexc('#6a6a72'))
    d.rectangle((4, 4, 11, 10), fill=hexc(col), outline=hexc('#2a2a30'))
    d.point((6, 6), fill=hexc('#202020')); d.point((9, 6), fill=hexc('#202020')); d.line((6, 8, 9, 8), fill=hexc('#202020'))
    for x in range(4, 12, 2):
        d.point((x, 13), fill=hexc('#d8c070'))
    return im


def bones(C):
    """(champion_art's anchors) where the sprite's head and body are on its quad: boxes no one sees, round the standing frame's
    pixels - the top two-fifths its head, the rest its body"""
    S, N = C.S, C.S.N
    x0, y0, x1, y1 = S.frames['idle'][0].getbbox()
    u = lambda px: round(16 - px * 16 / N, 3)
    v = lambda py: round(16 - py * 16 / N, 3)
    mid = y0 + (y1 - y0) * 0.4
    box = lambda ya, yb: [{'from': [u(x1), v(yb), 7.5], 'to': [u(x0), v(ya), 8.5], 'faces': {f: {'uv': [0, 0, 1, 1], 'texture': '#t'} for f in ('north', 'south')}}]
    t = {'t': 'minecraft:block/glass'}
    return {f'{C.ab}_hbone': (t, box(y0, mid)), f'{C.ab}_bbone': (t, box(mid, y1))}


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for C in ALL:
        RP.rp(C, R, _icon(C.COL))
        R.DISPLAY_3D_EXTRA = R.DISPLAY_3D_EXTRA + (C.S.prefix,)
        R.HATS.update(bones(C))

    def post(R2):
        for C in ALL:                                                   # (the head: its frame, from the pose's custom_model_data)
            C.S.item_def(R2, f'{C.ab}_head')
            tex, els, _sq = _doll(C, f'doll_{C.W}_t')
            els = pxart.turned(els)                                     # (its front where the other dolls have theirs)
            R2.wj(f'assets/bm/models/item/doll_{C.W}.json', {'textures': tex, 'elements': els, 'display': P141.doll_display(R2, els)})
    R.POST.append(post)                                                 # (after rigpet's head and the dolls' stand-ins - before phase138 copies them)


def generate_early(G):
    for C in ALL:
        RP.contract(C, G)


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    for C in ALL:
        _build(G, C)
    if CECIL:                                                           # (the 8-bit Bane: as the Serpent's Bane does it)
        mine = lambda w: f'@e[type=minecraft:wolf,tag=bm.{dict((c.W, c.ab) for c in ALL)[w]}pet,distance=..24]'
        each = lambda cmd: [f'execute as {mine(w)} if function bm:p100/is_mine run {cmd}' for w in ('pxemma', 'pxleo', 'pxcecil')]
        fn('p100/pxbane', ['effect give @s minecraft:resistance 3 0 true', 'effect give @s minecraft:speed 3 0 true',
                           'execute unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true'] +
           each('effect give @s minecraft:strength 3 0 true') + ['function bm:p100/banter_tick'])


def _build(G, C):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    W, pfx, ab = C.W, C.pfx, C.ab
    hand = 'positioned ^ ^1 ^0.5'

    def throw(key, model, dmg, on_hit, trail, fxname):
        cmds = P212.projectile(G, f'{W}_{key}', model, dmg, f'@e[type=minecraft:wolf,tag=bm.{ab}pet]', on_hit=on_hit, trail=trail, scale=0.6, fxname=fxname)
        fn(f'{pfx}/{key}_throw', cmds)
        return (f'execute facing entity @e[{FOE},distance=..16,sort=nearest,limit=1] eyes {hand} run function bm:{pfx}/{key}_throw')

    def abilities(G, X):
        S, go, hit, end, pfx_ = X.S, X.go, X.hit, X.end, X.pfx
        idle = X.idle_fight
        dec = [f'execute if score @s {S("k")} matches 1.. run scoreboard players remove @s {S("k")} 1',
               f'execute if score @s {S("k2")} matches 1.. run scoreboard players remove @s {S("k2")} 1']
        owner_hp = lambda lo_hi: [f'execute on owner if entity @s[distance=..12] store result score #hp bm.rng run data get entity @s Health',
                                  f'execute on owner if entity @s[distance=..12] if score #hp bm.rng matches {lo_hi} run return 1', 'return 0']
        if W == 'pxemma':
            fn(f'{pfx}/low', owner_hp('..8'))
            lines = dec + [
                f'execute store result score #nf bm.rng if entity @e[{FOE},distance=..8]',
                f'execute {idle} unless score @s {S("gc")} matches 1.. if score #nf bm.rng matches 3.. run function bm:{pfx}/star_go',
                f'execute {idle} unless score @s {S("k")} matches 1.. if function bm:{pfx}/low run function bm:{pfx}/life_go',
                f'execute {idle} unless score @s {S("sc")} matches 1.. if entity @e[{FOE},distance=..3] run function bm:{pfx}/stomp_go',
                f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{FOE},distance=..3] if entity @e[{FOE},distance=..14] run function bm:{pfx}/fire_go']
            fn(f'{pfx}/fire_go', go(7, 18, 'rc', 50, ['playsound minecraft:block.note_block.bit neutral @a[distance=..16] ~ ~ ~ 0.8 1.6']))
            fn(f'{pfx}/stomp_go', go(8, 18, 'sc', 80, ['playsound minecraft:entity.slime.jump neutral @a[distance=..16] ~ ~ ~ 0.8 1.4']))
            fn(f'{pfx}/star_go', go(11, 21, 'gc', 1200, ['playsound minecraft:block.note_block.chime neutral @a[distance=..24] ~ ~ ~ 1 2',
                                                         'execute on owner if entity @s[distance=..24] run ' + X.csay('"Power Star! I\'m invincible!"')]))
            fn(f'{pfx}/life_go', go(13, 14, 'k', 1200, ['playsound minecraft:entity.player.levelup neutral @a[distance=..16] ~ ~ ~ 0.6 2']))
            fire = throw('fire', 'bm:fx_px_fireball_0', 7, ['data merge entity @s {Fire:80s}', 'playsound minecraft:entity.generic.burn neutral @a[distance=..16] ~ ~ ~ 0.6 1.6'],
                         ['particle minecraft:flame ~ ~ ~ 0.05 0.05 0.05 0.01 1'], 'px_boom')
            fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                                   f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 8 run function bm:{pfx}/fire',
                                   f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 6 run function bm:{pfx}/stomp',
                                   f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 10 run function bm:{pfx}/star',
                                   f'execute if score @s {S("a")} matches 13 if score @s {S("x")} matches 7 run function bm:{pfx}/life'])
            fn(f'{pfx}/fire', [fire, 'playsound minecraft:entity.blaze.shoot neutral @a[distance=..16] ~ ~ ~ 0.5 1.8'] + X.end)
            fn(f'{pfx}/stomp', hit(10) + [FXS.fx('px_boom', 1.4, 0.4), f'execute as @e[{FOE},distance=..3] at @s run function bm:{pfx}/stomped',
                                          'playsound minecraft:entity.slime.squish neutral @a[distance=..16] ~ ~ ~ 1 1.2'] + end)
            fn(f'{pfx}/stomped', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 2 2', 'effect give @s minecraft:nausea 3 0'])
            fn(f'{pfx}/star', hit(12) + [FXS.fx('px_star', 2.0, 1.0), f'execute as @e[{FOE},distance=..8] at @s run function bm:{pfx}/hurt',
                                         'execute on owner if entity @s[distance=..24] run effect give @s minecraft:resistance 8 1 true',
                                         'execute on owner if entity @s[distance=..24] run effect give @s minecraft:speed 8 1 true',
                                         'particle minecraft:end_rod ~ ~1 ~ 1 1 1 0.1 30'] + end)
            fn(f'{pfx}/life', ['execute on owner if entity @s[distance=..12] at @s run function bm:p213e/oneup'])
            fn('p213e/oneup', [FXS.fx('px_hearts', 1.4, 2.2), 'effect give @s minecraft:instant_health 1 1 true', 'effect give @s minecraft:absorption 30 1 true',
                               'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 2',
                               title('@s', 'actionbar', [T('8-Bit Emma: ', C.COL, bold=True), T('"1-UP!" (Instant Health, Absorption)', C.LINE)])])
            return lines
        if W == 'pxleo':
            fn(f'{pfx}/full', owner_hp('18..'))
            fn(f'{pfx}/near_owner', ['execute on owner if entity @s[distance=..10] run return 1', 'return 0'])
            fn(f'{pfx}/hurt_owner', [f'execute unless entity @e[{FOE},distance=..6] run return 0'] + owner_hp('..14'))
            lines = dec + [
                f'execute store result score #nf bm.rng if entity @e[{FOE},distance=..6]',
                f'execute {idle} unless score @s {S("gc")} matches 1.. if score #nf bm.rng matches 3.. run function bm:{pfx}/spin_go',
                f'execute {idle} unless score @s {S("k")} matches 1.. if function bm:{pfx}/hurt_owner run function bm:{pfx}/block_go',
                f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{FOE},distance=..3] run function bm:{pfx}/slash_go',
                f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{FOE},distance=..3] if entity @e[{FOE},distance=..16] if function bm:{pfx}/full run function bm:{pfx}/beam_go',
                f'execute {idle} unless score @s {S("k2")} matches 1.. unless entity @e[{FOE},distance=..10] if function bm:{pfx}/near_owner run function bm:{pfx}/coin_go']
            fn(f'{pfx}/beam_go', go(7, 18, 'rc', 50, ['playsound minecraft:item.trident.return neutral @a[distance=..16] ~ ~ ~ 0.7 1.8']))
            fn(f'{pfx}/slash_go', go(8, 18, 'mc', 30, ['playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.7 1.4']))
            fn(f'{pfx}/block_go', go(9, 14, 'k', 400, ['playsound minecraft:item.shield.block neutral @a[distance=..16] ~ ~ ~ 1 1.2']))
            fn(f'{pfx}/spin_go', go(12, 18, 'gc', 1200, ['execute on owner if entity @s[distance=..24] run ' + X.csay('"Hyaaah! Spin attack!"')]))
            fn(f'{pfx}/coin_go', go(14, 18, 'k2', 900, []))
            beam = throw('beam', 'bm:fx_px_beam_0', 8, ['playsound minecraft:entity.experience_orb.pickup neutral @a[distance=..16] ~ ~ ~ 0.5 0.6'],
                         ['particle minecraft:end_rod ~ ~ ~ 0.03 0.03 0.03 0 1'], 'px_beam')
            fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                                   f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 8 run function bm:{pfx}/beam',
                                   f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 8 run function bm:{pfx}/slash',
                                   f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 10 run function bm:{pfx}/block',
                                   f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 9 run function bm:{pfx}/spin',
                                   f'execute if score @s {S("a")} matches 14 if score @s {S("x")} matches 9 run function bm:{pfx}/coin'])
            fn(f'{pfx}/beam', [beam, 'playsound minecraft:block.note_block.bit neutral @a[distance=..16] ~ ~ ~ 0.8 2'] + X.end)
            fn(f'{pfx}/slash', hit(8) + [f'execute as @e[{FOE},distance=..3] at @s run function bm:{pfx}/hurt',
                                         'particle minecraft:sweep_attack ^ ^1 ^1 0.4 0.2 0.4 0 3'] + end)
            fn(f'{pfx}/block', ['execute on owner if entity @s[distance=..12] run effect give @s minecraft:resistance 6 1 true',
                                f'execute as @e[{FOE},distance=..4] at @s facing entity @e[type=minecraft:wolf,tag=bm.{ab}pet,sort=nearest,limit=1] feet '
                                f'if block ^ ^ ^-1.5 #bm:grap_pass run tp @s ^ ^ ^-1.5',
                                'particle minecraft:enchanted_hit ~ ~1 ~ 0.6 0.6 0.6 0.2 16',
                                'execute on owner if entity @s[distance=..24] run ' + X.csay('"Behind my shield!" (Resistance II)')] + X.end)
            fn(f'{pfx}/spin', hit(14) + [FXS.fx('px_beam', 2.4, 0.6), f'execute as @e[{FOE},distance=..6] at @s run function bm:{pfx}/hurt',
                                         'particle minecraft:sweep_attack ~ ~1 ~ 2 0.2 2 0 12', 'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 1 0.8'] + end)
            fn(f'{pfx}/coin', ['execute on owner if entity @s[distance=..12] at @s run function bm:p213l/coins'] + X.end)
            fn('p213l/coins', [FXS.fx('px_coin', 1.2, 2.6), 'xp add @s 12 points', 'effect give @s minecraft:luck 60 0 true',
                               'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 1.6',
                               title('@s', 'actionbar', [T('8-Bit Leo: ', C.COL, bold=True), T('"A ? block! Coins for you." (experience, Luck)', C.LINE)])])
            return lines
        # 8-bit Cecil
        lines = dec + [
            f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{FOE},distance=..9] run function bm:{pfx}/over_go',
            f'execute store result score #nf bm.rng if entity @e[{FOE},distance=..7]',
            f'execute {idle} unless score @s {S("bc")} matches 1.. if score #nf bm.rng matches 3.. run function bm:{pfx}/hex_go',
            f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{FOE},distance=..3] if entity @e[{FOE},distance=..16] run function bm:{pfx}/bolt_go']
        fn(f'{pfx}/bolt_go', go(7, 16, 'rc', 50, ['playsound minecraft:entity.evoker.cast_spell neutral @a[distance=..16] ~ ~ ~ 0.5 1.8']))
        fn(f'{pfx}/hex_go', go(11, 24, 'bc', 300, ['playsound minecraft:entity.evoker.prepare_attack neutral @a[distance=..16] ~ ~ ~ 0.7 1.6']))
        fn(f'{pfx}/over_go', go(12, 34, 'gc', 1200, ['playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 1 0.5',
                                                     'execute on owner if entity @s[distance=..24] run ' + X.csay('"Your game ends HERE."')]))
        bolt = throw('bolt', 'bm:fx_px_star_0', 7, ['effect give @s minecraft:wither 3 0', 'playsound minecraft:entity.evoker.cast_spell neutral @a[distance=..16] ~ ~ ~ 0.5 2'],
                     ['particle minecraft:witch ~ ~ ~ 0.05 0.05 0.05 0 1'], 'px_star')
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 8 run function bm:{pfx}/bolt',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 12 run function bm:{pfx}/hex',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 14 run function bm:{pfx}/over'])
        fn(f'{pfx}/bolt', [bolt] + X.end)
        fn(f'{pfx}/hex', [FXS.fx('syn_control', 1.8, 0.2), f'execute as @e[{FOE},distance=..7] run effect give @s minecraft:slowness 6 1',
                          f'execute as @e[{FOE},distance=..7] run effect give @s minecraft:weakness 6 0', f'execute as @e[{FOE},distance=..7] run effect give @s minecraft:glowing 6 0',
                          'particle minecraft:witch ~ ~0.2 ~ 2 0.1 2 0 30', 'playsound minecraft:entity.illusioner.cast_spell neutral @a[distance=..16] ~ ~ ~ 1 1.2'] + X.end)
        fn(f'{pfx}/over', hit(18) + [FXS.fx('px_boom', 2.6, 0.8), f'execute as @e[{FOE},distance=..9] at @s run function bm:{pfx}/overed',
                                     'playsound minecraft:entity.generic.explode neutral @a[distance=..24] ~ ~ ~ 0.6 1.6',
                                     'execute on owner if entity @s[distance=..24] run ' + X.csay('"GAME OVER." (for them)')] + end)      # (2.94f: a line, not a screen title)
        fn(f'{pfx}/overed', [f'function bm:{pfx}/hurt', FXS.fx('px_boom', 1.0, 0.8)])
        return lines

    def encounter(G, X):
        # the Glitched Cartridge (phase214) calls enc/glitch - as you, at your own Emma / Leo / Cecil
        fn(f'{pfx}/enc/glitch', ['execute if entity @e[type=minecraft:interaction,tag=bm.' + ab + 'enc,distance=..32] run return 0',
                                 f'function bm:{pfx}/enc/spawn', 'particle minecraft:electric_spark ~ ~1 ~ 0.5 0.8 0.5 0.3 40',
                                 'particle minecraft:dust{color:[0.2,1.0,0.4],scale:1.4} ~ ~1 ~ 0.6 0.8 0.6 0 30',
                                 'playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 1 0.5',
                                 'playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 1 2'])
        fn(f'{pfx}/enc/talk', [f'execute if items entity @s container.* {X.holds(C.ITEM)} run return run ' +
                               title('@s', 'actionbar', [T(f'{C.NAME}: ', C.COL, bold=True), T('"You already have my cartridge, player one!"', C.LINE)]),
                               f'function bm:{pfx}/enc/recruit'])
        fn(f'{pfx}/enc/recruit', [f'execute as {X.here} at @s run particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.2 20',
                                  f'execute as {X.here} at @s run playsound minecraft:entity.player.levelup neutral @a[distance=..16] ~ ~ ~ 0.8 2',
                                  tellraw('@s', [T(f'{C.NAME} blinks up at you, sixteen colours and very pleased about it, and hands you a cartridge with ', C.LINE, italic=True),
                                                 T(f'{RP.POS[C.pron]} face on the label.', C.LINE, italic=True)]),
                                  f'function bm:{pfx}/enc/joined'])

    RP.build(C, G, abilities, encounter)

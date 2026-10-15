"""2.77: TULLIUS, THE DROWNED CAPTAIN - a rare boss on a tattered ghost ship in the cold seas, and the follower he becomes.

- THE GHOST SHIP: now and then, out on a cold or frozen ocean, a tattered ship rides the swell - frosted planks, torn
  sails, soul lanterns burning blue. Its hold has loot; the captain's cabin has his log; a ladder hangs down each side.
  Set foot on her deck with Leo in your company - his old rival - and her captain comes up out of the sea to meet you.
  (Without Leo the deck only creaks: he is waiting for someone. A server setting, on by default: /function
  bm:admin/settings - "Tullius needs Leo" - lets him rise for anyone.)
- THE FIGHT: Tullius, the drowned captain of the sunken kingdom - Leo's old rival. His icy BLUNDERBUSS (a cone of ice
  shards - deadly up close, weaker at range), his HARPOON (thrown: it hooks you and REELS you in - and then the
  blunderbuss, point-blank), the THRUST of the harpoon up close. He is at home in the water: knocked or jumping over the
  side, he swims fast and LEAPS back aboard. At three-fifths he calls his frostbitten crew; at half THE FROST TAKES HIM:
  the harpoon ices over and he adds the ICE NOVA (spikes of ice burst up round him) and the HARPOON SLAM - and dives
  overboard to come at you again out of the sea. Beaten, he returns to the ship after a day.
- DROPS: the first time, TULLIUS'S FROZEN DOUBLOON (he serves you), the FROSTBITE BLUNDERBUSS (use: a cone of ice
  shards) and TULLIUS'S HARPOON (a trident that reels in what it hits); a hoard every time, a chance at each later.
- THE FOLLOWER (the Doubloon): the harpoon thrust up close, the blunderbuss a little further, and the HARPOON PULL at range
  (a monster hooked and dragged in to a point-blank blast); every seventh blow, the FROSTBITE BROADSIDE. In the water he
  is fast and fierce (his blows +40%) and you swim with him (Dolphin's Grace, Conduit Power). Cold, sardonic, a grudging
  respect. Right-click him to sit; sneak + use: his menu. 5 minutes if he faints; a frame keeps him; a Raid Contract.
"""
import math
import json
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import tullius_art as ART
import rigfol as RF
import rigkit as RK
from rigkit import qs, I
import phase95 as FX
import phase46 as P46
import phase89 as P89
import phase68 as P68
import phase67 as P67
import phase98 as P98
import phase100 as P100
import allies

ICE, ICE_LT, TEAL, GOLD = '#8ad8f0', '#d8f4ff', '#4c8a8f', '#ffcf40'
BOSS_HP, PET_HP, PET_CD = 420, 55, 300
SB, SP = ART.BOSS_SCALE, ART.RIG_SCALE
UB, UP = SB / 16, SP / 16
MENU = 8620
COLD = ['minecraft:cold_ocean', 'minecraft:deep_cold_ocean', 'minecraft:frozen_ocean', 'minecraft:deep_frozen_ocean']
SSX, SSY, SSZ = 34, 26, 13                       # the ship (template): bow to +x; the sea's surface at its y5
WL, DECK = 5, 9

# ------------------------------------------------------------------------------------------------ items
item('tul_coin', TOTEM, "Tullius's Frozen Doubloon", ICE,
     ['A gold coin of the sunken kingdom, iced over.', ('Use: call Tullius (or call him back).', 'blue'), ('Sneak + use: his menu (sit, send home).', 'blue'),
      ('In the water he is fast, and fierce;', 'blue'), ('you swim with him.', 'blue'), ('If he faints: 5 minutes before he can return.', 'gray'),
      ('"Spend it wisely. I am not cheap."', 'dark_gray')],
     model='bm:tul_coin', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['tul_coin'] = 'bm:p132/use'
item('tul_blunderbuss', TOTEM, 'The Frostbite Blunderbuss', ICE,
     ['Brass and black wood, rimed with frost. It is cold to hold.', ('Use: a blast of ice shards in a cone -', 'blue'),
      ('brutal up close, weaker at range;', 'blue'), ('what it hits is slowed by frost.', 'blue'), ('Reload: 1.5 s.', 'gray'),
      ("Tullius's own.", 'dark_gray')],
     model='bm:tul_blunderbuss', stack=1, cat='weapon', glint=False, comps=hold('none'), tier=3)
HOLD['tul_blunderbuss'] = 'bm:p132/gun/use'
item('tul_harpoon', 'minecraft:trident', "Tullius's Harpoon", ICE,
     ['A barbed harpoon on a frozen rope.', ('Thrown: what it hits is REELED IN to you.', 'blue'), ('It comes back (Loyalty).', 'blue'),
      ("Tullius's own.", 'dark_gray')],
     model='bm:tul_harpoon', stack=1, cat='weapon', glint=False, tier=3,
     comps={'minecraft:enchantments': {'minecraft:loyalty': Int(3), 'minecraft:impaling': Int(3), 'minecraft:unbreaking': Int(3)}})
item('fcontract_tul', TOTEM, 'Raid Contract: Tullius', ICE,
     ['Signed in gold ink, sealed in wax - and frost.', ('Use once: from then on Tullius', 'blue'), ('will come into the vault with you.', 'blue')],
     model='minecraft:paper', glint=True, stack=1, cat='magic', comps=hold('none'))
HOLD['fcontract_tul'] = 'bm:p132/sign'

# ------------------------------------------------------------------------------------------------ the registries
P46.COMPANIONS += ',tag=!bm.tupet'
allies.ALLIES.append('bm.tupet')
BIT = 2 ** len(P89.BIT)
P89.BIT['tul'] = BIT
P68.KINDS['tul'] = (8, 'tul_coin', 'wolf', 'bm.tupet', 'p132/summon', 'p132/dismiss', 'bm.tusel2', 'Tullius', ICE)
P68.HE.add('tul')
P67.BOSSES.append(('bm.tuboss', 'bm:tub'))
P98.CALLED.append(('tul', 'Tullius', ICE, 'wolf', 'bm.tupet', 'bm.tusel2', 'bm.tucd', 'p132/try_summon', 'p132/dismiss', 'p132/recall', 'p132/go'))
P100.WHO['tul'] = ('wolf', 'bm.tupet')
P100.VOICE['Tullius'] = (ICE, ICE_LT)
EXPR = ('sneer', 'surprised', 'hurt', 'sleepy', 'blink', 'fury', 'shock', 'tired', 'serious')
FACE_MODEL = {'sneer': 'sneer', 'surprised': 'shock', 'hurt': 'hurt', 'sleepy': 'tired', 'blink': 'blink', 'fury': 'fury', 'shock': 'shock', 'tired': 'tired', 'serious': None}
FX.FOLK['tul'] = ('minecraft:wolf', 'bm.tupet', 'type=minecraft:item_display,tag=bm.tup,tag=bm.tup_head,tag=bm.tup_pet,tag=!bm.tufade', EXPR,
                  (70, 150), [('sneer', 36, 3)], ('sneer', 40), 'tired', 'fury')
_orig_exprs = FX.exprs
FX.exprs = lambda k: EXPR if k == 'tul' else _orig_exprs(k)

# ------------------------------------------------------------------------------------------------ poses
P = dict
POSES = {k: dict(v) for k, v in ART.POSES.items()}
_lw = ART.limb
POSES['run_a'] = P(ART.POSES['walk_a'], body=qs(('y', 8), ('x', 10)), legr=_lw(1, 40), legl=_lw(-1, -38))
POSES['run_b'] = P(ART.POSES['walk_b'], body=qs(('y', -8), ('x', 10)), legr=_lw(1, -38), legl=_lw(-1, 40))
for _k in ('run_a', 'run_b'):                   # (the weapons' aims again, the body changed)
    _p = POSES[_k]
    if '_hw' in _p: _p['harpoon'] = ART._qm(ART._conj(ART._qm(_p.get('body', I), _p.get('arml', I))), _p['_hw'])
    if '_gw' in _p: _p['gun'] = ART._qm(ART._conj(ART._qm(_p.get('body', I), _p.get('armr', I))), _p['_gw'])
POSES['rise'] = P(ART.POSES['defeated'], _face='blink')            # (coming up out of the sea: down on one knee, then up)


class _Art:
    PIVOT, PARENT, PARTS, PART_K, PREFIX = ART.PIVOT, ART.PARENT, ART.PARTS, ART.PART_K, ART.PREFIX
    HIDDEN = staticmethod(ART.HIDDEN)
    model_name = staticmethod(ART.model_name)


A = _Art
SWAP = ('harpoon', 'armr')
DUR_B = {'idle_a': 26, 'idle_b': 26, 'walk_a': 6, 'walk_b': 6, 'run_a': 4, 'run_b': 4, 'guard': 5, 'thrust_back': 4, 'thrust': 2, 'throw_back': 5, 'throw': 2,
         'ice_cast': 8, 'slam_up': 8, 'slam_mid': 3, 'slam': 3, 'tired': 18, 'taunt': 8, 'defeated': 14, 'aim': 6, 'fire': 2, 'reload': 10,
         'hook_pull': 4, 'blast': 3, 'rise': 1} | {f'swim_{i}': 3 for i in range(ART.SWIM_FRAMES)}
DUR_P = dict(DUR_B, idle_a=24, idle_b=24, sit=16, walk_a=4, walk_b=4, run_a=3, run_b=3)
SLAM_HIT = RK.point(A, POSES['slam'], 'harpoon', (ART.PIVOT['harpoon'][0], ART.PIVOT['harpoon'][1] - 10, ART.PIVOT['harpoon'][2] - 6), scale=SB)
loc = lambda v: f'^{v[0]:.2f} ^{max(v[1], 0.1):.2f} ^{v[2]:.2f}'


def extend_offers(O, offer):
    pass


# ================================================================================================= resource pack
def _coin_icon(R):
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2, 2, 13, 13), fill=hexc('#c8962a'), outline=hexc('#6a4a10'))
    d.ellipse((4, 4, 11, 11), outline=hexc('#ffe08a'))
    d.line((6, 5, 6, 10), fill=hexc('#6a4a10')); d.line((6, 5, 9, 5), fill=hexc('#6a4a10')); d.line((6, 7, 8, 7), fill=hexc('#6a4a10'))
    for x, y in ((3, 4), (4, 3), (11, 3), (12, 4), (12, 11), (3, 11), (10, 12)):
        im.putpixel((x, y), hexc('#d8f4ff'))
    d.line((2, 6, 2, 9), fill=hexc('#a8e4ff')); d.line((13, 6, 13, 10), fill=hexc('#a8e4ff'))
    return im


def rp(R):
    R.TEXTURE_MODS.append(ART)
    for name, (tex, els) in ART.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (ART.PREFIX,)
    R.ICONS['tul_coin'] = _coin_icon(R)
    cases = [(e, f'tu_head_x{m}') for e, m in FACE_MODEL.items() if m]
    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        R2.wj('assets/bm/items/tu_head.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                         'cases': [{'when': e, 'model': mdl(m)} for e, m in cases], 'fallback': mdl('tu_head')}})
        # (2.78: held the way vanilla holds things - his hand's joint is the grip, the muzzle and the point (-z) the tip: the
        #  blunderbuss as a crossbow is held, the harpoon as a sword. The old hand-set angles had the gun lying across the screen.)
        import heldfx as HF
        for nm, part, style in (('tul_blunderbuss', 'tu_gun', 'crossbow'), ('tul_harpoon', 'tu_harpoon', 'handheld')):
            src = json.load(open(R2.p('assets', 'bm', 'models', 'item', f'{part}.json')))
            disp = HF.display((0, 0, -1), (0, 1, 0), (8, 8, 8), HF.bounds(src), style=style)
            R2.wj(f'assets/bm/models/item/{nm}_held.json', {'parent': f'bm:item/{part}', 'display': disp})
            R2.wj(f'assets/bm/items/{nm}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{nm}_held'}})
    R.POST.append(post)


# ================================================================================================= the ghost ship (a structure)
def ship():
    import random
    from structures import Build, book_nbt
    Bd = Build(SSX, SSY, SSZ)
    rnd = random.Random(4417)
    S = Bd.set
    CZ = 6
    PL = [('dark_oak_planks', 6), ('spruce_planks', 3), ('stripped_dark_oak_wood', 1), ('mangrove_planks', 1)]
    pick = lambda pal: rnd.choices([p for p, _ in pal], [w for _, w in pal])[0]
    def hw(x):
        if x < 2: return 4.7
        if x <= 23: return 5.7
        t = (x - 23) / 10.6
        return max(0.0, 5.7 * math.sqrt(max(0.0, 1 - t * t)))
    def half(x, y):
        return hw(x) * min(1.0, ((y + 0.7) / DECK) ** 0.55)
    # the hull: planks round a dry hold, a keel under it, the deck over it
    for x in range(SSX):
        for y in range(0, DECK + 1):
            h = half(x, y)
            if h < 0.6: continue
            for z in range(SSZ):
                d = abs(z - CZ)
                if d > h + 0.4: continue
                shell = d > h - 0.9 or y == 0 or x == 0 or (x >= 23 and abs(d - h) < 1.2)
                if y == DECK: S(x, y, z, pick(PL) if (x + z) % 7 else 'stripped_dark_oak_wood')
                elif shell: S(x, y, z, pick(PL) if y >= WL - 1 or rnd.random() > 0.15 else 'dark_oak_log[axis=x]')
                elif y == 1: S(x, y, z, 'spruce_planks')
                else: S(x, y, z, 'air')
    # ice crusted on at the waterline; holes torn in her side above it
    for x in range(1, SSX - 2):
        for z in range(SSZ):
            for y in (WL - 1, WL, WL + 1):
                b = Bd.get(x, y, z)
                if b and b != 'minecraft:air' and abs(z - CZ) > half(x, y) - 0.9 and rnd.random() < 0.22:
                    S(x, y, z, rnd.choice(['packed_ice', 'packed_ice', 'blue_ice', 'snow_block']))
    for x0, z0 in ((7, 0), (15, 12), (20, 1), (11, 11)):
        for dx in range(2):
            for dy in range(2):
                y = WL + 2 + dy
                z = z0 if Bd.get(x0 + dx, y, z0) not in (None, 'minecraft:air') else (z0 + (1 if z0 < CZ else -1))
                if Bd.get(x0 + dx, y, z) not in (None,): S(x0 + dx, y, z, 'air')
    # the hatch down into the hold, with a ladder
    for x, z in ((12, 5), (12, 6), (13, 5), (13, 6)): S(x, DECK, z, 'air')
    for y in range(2, DECK): S(11, y, 5, 'spruce_planks'); S(12, y, 5, 'ladder[facing=east,waterlogged=false]')
    # rails round the main deck
    for x in range(SSX):
        h = half(x, DECK)
        if h < 0.6: continue
        for z in (int(round(CZ - h + 0.45)), int(round(CZ + h - 0.45))):
            if 0 <= z < SSZ and Bd.get(x, DECK, z): S(x, DECK + 1, z, 'dark_oak_fence' if x % 5 else 'stripped_dark_oak_log[axis=y]')
    # a boarding ladder down each side amidships, the rail open above it: up out of the sea and onto her deck
    LX = 18
    for z, zb, face in ((1, 2, 'north'), (SSZ - 2, SSZ - 3, 'south')):
        for y in range(WL - 2, DECK + 1):
            if Bd.get(LX, y, zb) in (None, 'minecraft:air'): S(LX, y, zb, 'dark_oak_planks')
            S(LX, y, z, f'ladder[facing={face},waterlogged={"true" if y < WL else "false"}]')
        S(LX, DECK + 1, z, 'air')
    # the quarterdeck (stern, x0-8) over the captain's cabin; the forecastle (bow, x27-31)
    for x in range(0, 9):
        h = half(x, DECK)
        for z in range(SSZ):
            d = abs(z - CZ)
            if d > h + 0.4: continue
            edge = d > h - 0.9 or x == 0 or x == 8
            for y in (DECK + 1, DECK + 2):
                S(x, y, z, (pick(PL) if (y == DECK + 1 or (x + z) % 3) else 'glass_pane') if edge else 'air')
            S(x, DECK + 3, z, pick(PL))
            if edge: S(x, DECK + 4, z, 'dark_oak_fence')
    S(8, DECK + 1, CZ, 'air'); S(8, DECK + 2, CZ, 'air')                       # the cabin door (open, onto the main deck)
    for i, y in enumerate((DECK + 1, DECK + 2, DECK + 3)):                      # stairs up, both sides
        for z in (2, 10):
            S(11 - i, y, z, 'spruce_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]')
            if i: S(11 - i + 1, y, z, 'air')
    for z in (2, 10): S(8, DECK + 4, z, 'air')
    for x in range(27, 32):
        h = half(x, DECK)
        for z in range(SSZ):
            if abs(z - CZ) > h + 0.4: continue
            S(x, DECK + 1, z, pick(PL))
            if abs(z - CZ) > h - 0.9: S(x, DECK + 2, z, 'dark_oak_fence')
    for z in (5, 6, 7): S(26, DECK + 1, z, 'spruce_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]')
    for x in (31, 32, 33): S(x, DECK + 1 + (x - 31), CZ, 'stripped_spruce_log[axis=x]')     # the bowsprit, angled up
    S(33, DECK, CZ, 'blue_ice'); S(33, DECK + 1, CZ, 'skeleton_skull[rotation=12]') if Bd.get(33, DECK + 1, CZ) is None else None
    # masts, yards, torn sails; the crow's nest
    for mx, top, yards in ((4, 21, (16,)), (16, 25, (14, 19, 23)), (24, 23, (14, 19))):
        for y in range(1, top + 1):
            if Bd.get(mx, y, CZ) in (None, 'minecraft:air') or y <= DECK + 3: S(mx, y, CZ, 'stripped_spruce_log[axis=y]')
        for yy in yards:
            span = 5 if yy < top - 3 else 3
            for z in range(CZ - span, CZ + span + 1):
                if z != CZ: S(mx, yy, z, 'spruce_fence')
            S(mx, yy - 1, CZ - span, 'soul_lantern[hanging=true,waterlogged=false]'); S(mx, yy - 1, CZ + span, 'soul_lantern[hanging=true,waterlogged=false]')
            for z in range(CZ - span + 1, CZ + span):                           # the sail, hanging forward of the mast
                drop = 4 if yy < top - 3 else 3
                for k in range(1, drop + 1):
                    y = yy - k
                    if y <= DECK + (4 if mx == 4 else 1): break
                    if rnd.random() < (0.25 + 0.12 * k):                         # (ragged - more holes toward the foot)
                        if rnd.random() < 0.25: S(mx + 1, y, z, 'cobweb')
                        continue
                    S(mx + 1, y, z, rnd.choice(['white_wool', 'white_wool', 'light_gray_wool', 'light_gray_wool', 'gray_wool']))
    for x in range(15, 18):
        for z in range(CZ - 1, CZ + 2):
            if (x, z) != (16, CZ): S(x, 20, z, 'spruce_planks'); S(x, 21, z, 'spruce_trapdoor[facing=north,half=bottom,open=false,waterlogged=false]')
    S(15, 21, CZ - 1, 'spruce_fence'); S(17, 21, CZ + 1, 'spruce_fence')
    # the ship's wheel, lanterns on posts, snow on the decks
    S(7, DECK + 4, CZ, 'dark_oak_fence'); S(7, DECK + 5, CZ, 'spruce_trapdoor[facing=east,half=bottom,open=true,waterlogged=false]')
    for x in (3, 9, 15, 21):
        for z in (1, 11):
            if Bd.get(x, DECK + 1, z) == 'minecraft:dark_oak_fence': S(x, DECK + 2, z, 'soul_lantern[hanging=false,waterlogged=false]')
    for x in range(SSX):
        for z in range(SSZ):
            for y in range(SSY - 1, DECK - 1, -1):
                b = Bd.get(x, y, z)
                if b and b not in ('minecraft:air',) and 'fence' not in b and 'lantern' not in b and 'pane' not in b and 'wool' not in b and 'cobweb' not in b \
                        and 'stairs' not in b and 'trapdoor' not in b and 'log' not in b and 'skull' not in b and y + 1 < SSY and Bd.get(x, y + 1, z) is None:
                    if rnd.random() < 0.35: S(x, y + 1, z, f'snow[layers={rnd.choice([1, 1, 2])}]')
                    break
                if b: break
    # the hold: barrels, chests, bones and ice; the cabin: his table, his chest, his log
    S(14, 2, 2, 'chest[facing=south,type=single,waterlogged=false]', {'id': 'minecraft:chest', 'LootTable': 'bm:chests/p132_hold'})
    S(20, 2, 10, 'chest[facing=north,type=single,waterlogged=false]', {'id': 'minecraft:chest', 'LootTable': 'bm:chests/p132_hold'})
    for x, z in ((15, 2), (16, 2), (19, 10), (8, 3), (8, 9), (21, 3)):
        S(x, 2, z, 'barrel[facing=up,open=false]')
        if rnd.random() < 0.5: S(x, 3, z, 'barrel[facing=up,open=false]')
    for x, z in ((10, 8), (18, 4), (6, 6), (22, 7)):
        S(x, 2, z, rnd.choice(['bone_block[axis=x]', 'packed_ice', 'skeleton_skull[rotation=4]', 'blue_ice']))
    S(17, 7, 3, 'cobweb'); S(9, 7, 9, 'cobweb'); S(19, 6, 8, 'soul_lantern[hanging=false,waterlogged=false]'); S(10, 2, 4, 'soul_lantern[hanging=false,waterlogged=false]')
    S(2, DECK + 1, CZ, 'chest[facing=east,type=single,waterlogged=false]', {'id': 'minecraft:chest', 'LootTable': 'bm:chests/p132_captain'})
    S(4, DECK + 1, CZ - 2, 'dark_oak_fence'); S(4, DECK + 2, CZ - 2, 'dark_oak_pressure_plate')
    pages = [[{'text': "The Captain's Log\n\n", 'color': 'dark_aqua'}, {'text': 'Tullius, captain of the Sunken Guard.\n\nThe kingdom is gone. The serpent took it, and the sea took what the serpent left.'}],
             [{'text': 'The princess lived. Leo carried her out of the water himself - Leo, of all people. He always did get the glory.\n\nI did not. I went down with my ship.'}],
             [{'text': 'The cold kept me. I do not mind the cold. I mind the quiet.\n\nIf you are reading this, you are on my deck. Stay - and if you sail with Leo, tell him I am waiting.\n\n- T.'}]]
    S(5, DECK + 1, CZ + 2, 'lectern[facing=east,has_book=true,powered=false]',
      {'id': 'minecraft:lectern', 'Book': book_nbt("The Captain's Log", 'Tullius', pages), 'Page': Int(0)})
    Bd.marker(16.5, DECK + 1.0, CZ + 0.5, ['bm.tuship'])
    Bd.marker(4.5, DECK + 4.0, CZ + 0.5, ['bm.tuspawn'], -90.0)
    return Bd


# ================================================================================================= the datapack
def generate(G):
    import phase28 as P28
    import phase73 as P73
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tusay = lambda txt, who='@s': title(who, 'actionbar', [T('Tullius: ', ICE, bold=True), T(txt, ICE_LT)])
    tuchat = lambda txt, who='@s': tellraw(who, [T('Tullius: ', ICE, bold=True), T(f'"{txt}"', ICE_LT)])
    tick, fast, second = [], [], []
    objs = ['bm.tuid', 'bm.tuatk', 'bm.tut', 'bm.tuc', 'bm.tuph', 'bm.tur', 'bm.tulone', 'bm.tuk', 'bm.tucd', 'bm.tus', 'bm.tuf', 'bm.tua', 'bm.tux',
            'bm.tum', 'bm.tuv', 'bm.tuch', 'bm.tuz', 'bm.tuq', 'bm.tusl', 'bm.tul', 'bm.tucl', 'bm.tuw', 'bm.tufg', 'bm.tugc', 'bm.tuh', 'bm.tuhk', 'bm.tuhn']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        ['bossbar add bm:tub {text:"Tullius, the Drowned Captain",color:"aqua"}', 'bossbar set bm:tub color blue', 'bossbar set bm:tub style notched_10'] + \
        [f'scoreboard players set #{n} bm.rng {n}' for n in (2, 3, 4, 5, 8, 10, 12, 14, 16, 20, 24, 40, 60, 61, 80, 100, 1200)]
    G.OBJECTIVES += objs
    foe = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.tuboss'
    pl = lambda r, extra='': f'@a[distance=..{r},gamemode=!creative,gamemode=!spectator{extra}]'
    me = '@e[type=minecraft:husk,tag=bm.tume,limit=1]'
    at = lambda t, cmd: f'execute if score @s bm.tut matches {t} run {cmd}'
    wjson('bm/tags/block/p132_swim.json', {'values': ['minecraft:water', 'minecraft:bubble_column', 'minecraft:seagrass', 'minecraft:tall_seagrass', 'minecraft:kelp',
                                                      'minecraft:kelp_plant', '#minecraft:air']})

    # ================================================================== THE GHOST SHIP: rare, in the cold seas
    wjson('bm/tags/worldgen/biome/has_structure/tul_ship.json', {'values': COLD})
    wjson('bm/worldgen/structure/tul_ship.json', {'type': 'minecraft:jigsaw', 'biomes': '#bm:has_structure/tul_ship', 'step': 'surface_structures',
                                                  'spawn_overrides': {}, 'terrain_adaptation': 'none', 'start_pool': 'bm:tul_ship/start', 'size': 1,
                                                  'start_height': {'absolute': 0}, 'project_start_to_heightmap': 'WORLD_SURFACE_WG',
                                                  'max_distance_from_center': 80, 'use_expansion_hack': False, 'liquid_settings': 'ignore_waterlogging'})
    wjson('bm/worldgen/template_pool/tul_ship/start.json', {'fallback': 'minecraft:empty', 'elements': [
        {'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': 'bm:tul_ship_seed', 'projection': 'rigid', 'processors': 'minecraft:empty'}}]})
    wjson('bm/worldgen/structure_set/tul_ship.json', {'structures': [{'structure': 'bm:tul_ship', 'weight': 1}],
                                                      'placement': {'type': 'minecraft:random_spread', 'spacing': 56, 'separation': 22, 'salt': 13277341}})
    from structures import Build
    Bs = Build(1, 1, 1)
    Bs.marker(0.5, 0.0, 0.5, ['bm.tuseed'], 0)
    Bs.export(G.path('data', 'bm', 'structure', 'tul_ship_seed.nbt'))
    ship().export(G.path('data', 'bm', 'structure', 'p132_ship.nbt'))
    second.append('execute as @e[type=minecraft:marker,tag=bm.tuseed] at @s if entity @a[distance=..112] if loaded ~-18 ~ ~-8 if loaded ~18 ~ ~8 run function bm:p132/ship/build')
    # (on the open sea only: water under the seed, or sea ice; a seed that came down on an island is dropped)
    fn('p132/ship/build', ['kill @s',
                           'execute unless block ~ ~-1 ~ minecraft:water unless block ~ ~-1 ~ #minecraft:ice run return 0',
                           'execute unless block ~ ~-4 ~ minecraft:water unless block ~ ~-4 ~ #minecraft:ice run return 0',
                           f'execute positioned ~-16 ~-{WL} ~-6 run place template bm:p132_ship',
                           'playsound minecraft:ambient.underwater.loop.additions.ultra_rare ambient @a[distance=..64] ~ ~ ~ 0.6 0.5'])
    wjson('bm/loot_table/chests/p132_hold.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': {'min': 4, 'max': 7, 'type': 'minecraft:uniform'}, 'entries': [
            {'type': 'minecraft:item', 'name': n, 'weight': w, 'functions': [{'function': 'minecraft:set_count', 'count': {'min': a, 'max': b, 'type': 'minecraft:uniform'}}]}
            for n, w, a, b in (('minecraft:gold_nugget', 5, 4, 16), ('minecraft:gold_ingot', 3, 1, 4), ('minecraft:prismarine_shard', 4, 2, 8), ('minecraft:prismarine_crystals', 3, 1, 6),
                               ('minecraft:packed_ice', 3, 2, 6), ('minecraft:blue_ice', 1, 1, 3), ('minecraft:honey_bottle', 2, 1, 2),
                               ('minecraft:cod', 3, 2, 6), ('minecraft:salmon', 2, 1, 4), ('minecraft:gunpowder', 3, 2, 6), ('minecraft:emerald', 2, 1, 4),
                               ('minecraft:nautilus_shell', 1, 1, 2), ('minecraft:diamond', 1, 1, 2))]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': 'bm:items/token', 'weight': 6}, {'type': 'minecraft:loot_table', 'value': 'bm:items/medallion', 'weight': 2},
                                 {'type': 'minecraft:item', 'name': 'minecraft:heart_of_the_sea', 'weight': 1}, {'type': 'minecraft:empty', 'weight': 4}]}]})
    wjson('bm/loot_table/chests/p132_captain.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': {'min': 3, 'max': 5, 'type': 'minecraft:uniform'}, 'entries': [
            {'type': 'minecraft:item', 'name': n, 'weight': w, 'functions': [{'function': 'minecraft:set_count', 'count': {'min': a, 'max': b, 'type': 'minecraft:uniform'}}]}
            for n, w, a, b in (('minecraft:gold_ingot', 4, 2, 6), ('minecraft:diamond', 2, 1, 3), ('minecraft:emerald', 3, 2, 6), ('minecraft:spyglass', 1, 1, 1),
                               ('minecraft:compass', 1, 1, 1), ('minecraft:map', 2, 1, 1), ('minecraft:prismarine_crystals', 2, 2, 6), ('minecraft:nautilus_shell', 2, 1, 3))]},
        {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(2, 4))]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:heart_of_the_sea', 'weight': 1}, {'type': 'minecraft:item', 'name': 'minecraft:trident', 'weight': 1},
                                 {'type': 'minecraft:empty', 'weight': 3}]}]})
    # ---- the ship: haunted at night; its captain comes up when you board (and again a day after he's beaten)
    second.append('execute as @e[type=minecraft:marker,tag=bm.tuship] at @s if entity @a[distance=..64] run function bm:p132/ship/sec')
    fn('p132/ship/sec', ['execute if score @s bm.tuw matches 2 run scoreboard players remove @s bm.tut 1',
                         'execute if score @s bm.tuw matches 2 if score @s bm.tut matches ..0 run scoreboard players set @s bm.tuw 0',
                         'execute unless score @s bm.tuw matches 0.. run scoreboard players set @s bm.tuw 0',
                         # (he's gone and it wasn't a win - the win sets 2 within a moment: wait a few seconds before the deck's free again)
                         'execute if score @s bm.tuw matches 1 if entity @e[type=minecraft:husk,tag=bm.tuboss,distance=..80] run scoreboard players set @s bm.tulone 0',
                         'execute if score @s bm.tuw matches 1 unless entity @e[type=minecraft:husk,tag=bm.tuboss,distance=..80] run scoreboard players add @s bm.tulone 1',
                         'execute if score @s bm.tuw matches 1 if score @s bm.tulone matches 6.. run scoreboard players set @s bm.tuw 0',
                         # (someone ON her: her deck, from the stern to the bow, up to the crow's nest - not a swimmer alongside;
                         #  and - the setting, on by default - Leo with one of them)
                         'scoreboard players set #tb bm.rng 0',
                         'execute if score @s bm.tuw matches 0 positioned ~-17 ~-0.6 ~-6.5 as @a[dx=34,dy=14,dz=13,gamemode=!spectator,gamemode=!creative] at @s run function bm:p132/ship/aboard',
                         'execute if score @s bm.tuw matches 0 if score #tb bm.rng matches 2 run function bm:p132/ship/board',
                         'execute store result score #r bm.rng run random value 1..12',
                         'execute if score #r bm.rng matches 1 run playsound minecraft:block.wood.step ambient @a[distance=..40] ~ ~1 ~ 1 0.5',
                         'execute if score #r bm.rng matches 2 run playsound minecraft:block.bell.resonate ambient @a[distance=..48] ~ ~2 ~ 0.4 0.5',
                         'execute if score #r bm.rng matches 3 run playsound minecraft:entity.allay.ambient_without_item ambient @a[distance=..40] ~ ~3 ~ 0.5 0.5',
                         'execute unless score #tod bm.bm matches 0..12999 run particle minecraft:soul ~ ~4 ~ 8 4 4 0.01 6',
                         'particle minecraft:snowflake ~ ~6 ~ 9 5 5 0.01 8'])
    # (as each player on her deck: 1 = someone's aboard; 2 = and the captain will rise - Leo is here, or the setting is off)
    fn('p132/ship/aboard', ['execute unless score #tb bm.rng matches 1.. run scoreboard players set #tb bm.rng 1',
                            'execute unless score #tulleo bm.cfg matches 1 run return run scoreboard players set #tb bm.rng 2',
                            'tag @s add bm.tuab',
                            'execute as @e[type=minecraft:wolf,tag=bm.leopet,tag=!bm.ffpet,distance=..24] on owner if entity @s[tag=bm.tuab] run scoreboard players set #tb bm.rng 2',
                            'tag @s remove bm.tuab',
                            'execute unless score #tb bm.rng matches 2 unless score @s bm.tuhn matches 1.. run function bm:p132/ship/waits'])
    fn('p132/ship/waits', ['scoreboard players set @s bm.tuhn 30', 'playsound minecraft:block.bell.resonate ambient @s ~ ~ ~ 0.5 0.4',
                           'playsound minecraft:ambient.underwater.loop.additions.rare ambient @s ~ ~ ~ 0.8 0.5',
                           title('@s', 'actionbar', [T('The deck creaks. Far below, something stirs... and settles. ', ICE_LT, italic=True),
                                                     T('(Her captain waits for an old rival: bring Leo.)', 'gray')])])
    second.append('scoreboard players remove @a[scores={bm.tuhn=1..}] bm.tuhn 1')
    # the setting (ops: /function bm:admin/settings): on by default
    G.FUNCS['load'][-1:-1] = ['execute unless score #tulleo bm.cfg matches -2147483648.. run scoreboard players set #tulleo bm.cfg 1']
    G.FUNCS['admin/settings'].append(tellraw('@s', [T('  Tullius needs Leo: ', 'white'), {'score': {'name': '#tulleo', 'objective': 'bm.cfg'}, 'color': 'aqua'}, T('  ', 'gray'),
                                                    T('[On]', 'green', click_event={'action': 'run_command', 'command': '/function bm:admin/set/tulleo_1'}), T(' ', 'gray'),
                                                    T('[Off]', 'red', click_event={'action': 'run_command', 'command': '/function bm:admin/set/tulleo_0'}),
                                                    T("  the ghost ship's captain only rises with Leo in the boarding crew", 'gray')]))
    for v in (0, 1):
        fn(f'admin/set/tulleo_{v}', [f'scoreboard players set #tulleo bm.cfg {v}', 'function bm:admin/settings'])
    fn('p132/ship/board', ['scoreboard players set @s bm.tuw 1',
                           'execute as @e[type=minecraft:marker,tag=bm.tuspawn,distance=..20,sort=nearest,limit=1] at @s rotated as @s run function bm:p132/b/spawn'])

    # ================================================================== THE RIG
    def bsel(p=None):
        return '@e[type=minecraft:item_display,tag=bm.tusel' + (f',tag=bm.tup_{p}]' if p else ']')
    fn('p132/b/rig', [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.tup", f"bm.tup_{p}", "bm.tub", "bm.tunew"], SB, extra={"view_range": F(2.0), "brightness": {"block": Int(10), "sky": Int(12)}, "shadow_radius": F(0.8 if p == "body" else 0.0), "shadow_strength": F(0.6)})}'
                      for p in A.PARTS] +
       ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.tunew,distance=..1] bm.tuid = #tid bm.rng',
        'tag @e[type=minecraft:item_display,tag=bm.tunew,distance=..1] add bm.tusel', 'tag @e[type=minecraft:item_display,tag=bm.tunew] remove bm.tunew',
        'scoreboard players set @s bm.tus -1'])
    fn('p132/b/rerig', [f'kill {bsel()}', 'function bm:p132/b/rig'])
    fn('p132/b/place', RF.place(A, UB, bsel))
    for name, pz in POSES.items():
        if name in DUR_B:
            fn(f'p132/b/pose1/{name}', RF.pose(A, pz, SB, DUR_B[name], bsel, swap=SWAP))
            fn(f'p132/b/pose2/{name}', RF.pose(A, dict(pz, _ice=True), SB, DUR_B[name], bsel, swap=SWAP))
            fn(f'p132/b/pose/{name}', [f'execute if score @s bm.tuph matches 2 run return run function bm:p132/b/pose2/{name}', f'function bm:p132/b/pose1/{name}'])
    bface = lambda e: (f'data modify entity {bsel("head")[:-1]},limit=1] item.components."minecraft:custom_model_data" set value {{strings:["{e}"]}}' if e
                       else f'data remove entity {bsel("head")[:-1]},limit=1] item.components."minecraft:custom_model_data"')

    # ================================================================== THE BOSS
    none_helm = {'id': 'minecraft:leather_helmet', 'count': Int(1), 'components': {'minecraft:equippable': {'slot': 'head', 'asset_id': 'bm:none'}}}
    bnbt = {'Tags': ['bm.tuboss', 'bm.tuhost', 'bm.tunew', 'bm.seen'], 'PersistenceRequired': B(1), 'Silent': B(1), 'NoAI': B(1), 'Invulnerable': B(1),
            'CustomName': T('Tullius', ICE, bold=True), 'IsBaby': B(0), 'CanBreakDoors': B(0), 'DeathLootTable': 'minecraft:empty', 'Health': F(BOSS_HP),
            'attributes': [{'id': f'minecraft:{k}', 'base': D(v)} for k, v in dict(scale=1.45, max_health=BOSS_HP, attack_damage=6, armor=12, armor_toughness=4,
                                                                                  movement_speed=0.29, follow_range=40, knockback_resistance=0.8, spawn_reinforcements=0.0,
                                                                                  step_height=1.0, water_movement_efficiency=1.0, oxygen_bonus=1000).items()],
            'active_effects': [{'id': f'minecraft:{e}', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}
                               for e in ('invisibility', 'fire_resistance', 'water_breathing')],
            'equipment': {'head': none_helm}, 'drop_chances': {s: F(0.0) for s in ('mainhand', 'offhand', 'head', 'chest', 'legs', 'feet')}}
    fn('p132/b/spawn', [f'summon minecraft:husk ~ ~ ~ {snbt(bnbt)}', 'execute as @e[type=minecraft:husk,tag=bm.tunew,distance=..2,limit=1] at @s run function bm:p132/b/init'])
    fn('p132/b/init', ['scoreboard players add #tun bm.tuid 1', 'scoreboard players operation @s bm.tuid = #tun bm.tuid', 'tp @s ~ ~ ~ ~ 0',
                       'scoreboard players set @s bm.tuatk 0', 'scoreboard players set @s bm.tut 0', 'scoreboard players set @s bm.tuc 40', 'scoreboard players set @s bm.tuph 0',
                       'scoreboard players set @s bm.tur 0', 'scoreboard players set @s bm.tulone 0', 'tag @s remove bm.tunew',
                       'scoreboard players operation #tid bm.rng = @s bm.tuid', 'function bm:p132/b/rig', 'function bm:p132/b/pose/rise', bface('blink'),
                       f'tag {bsel()} remove bm.tusel', 'team join bm.blood @s', 'scoreboard players set @s bm.tuatk 9'])
    tick.append('execute as @e[type=minecraft:husk,tag=bm.tuboss] at @s run function bm:p132/b/tick')
    fn('p132/b/tick', ['scoreboard players operation #tid bm.rng = @s bm.tuid',
                       'execute as @e[type=minecraft:item_display,tag=bm.tub,tag=!bm.tudie,distance=..24] if score @s bm.tuid = #tid bm.rng run tag @s add bm.tusel',
                       f'execute unless entity {bsel("body")} run function bm:p132/b/rig',
                       f'execute unless entity {bsel("harpoon")} run function bm:p132/b/rerig',
                       'scoreboard players set #wet bm.rng 0', 'execute if block ~ ~1.6 ~ minecraft:water run scoreboard players set #wet bm.rng 1',
                       'execute if score #wet bm.rng matches 1 rotated as @s rotated ~ 0 positioned ~ ~0.4 ~ run function bm:p132/b/place',
                       'execute if score #wet bm.rng matches 0 rotated as @s rotated ~ 0 run function bm:p132/b/place',
                       'execute if score @s bm.tuatk matches 1.. run function bm:p132/b/attack',
                       'execute if score @s bm.tuph matches 1.. unless score @s bm.tuatk matches 1.. run function bm:p132/b/move',
                       'execute if score @s bm.tuph matches 1.. unless score @s bm.tuatk matches 1.. run function bm:p132/b/mind',
                       'execute as @e[type=minecraft:interaction,tag=bm.bhit_tu,distance=..12] if score @s bm.hbid = #tid bm.rng run tag @s add bm.hbsel',
                       'execute unless entity @e[type=minecraft:interaction,tag=bm.hbsel,tag=bm.bhit_tu] run function bm:p132/b/hitbox',
                       'tp @e[type=minecraft:interaction,tag=bm.hbsel,tag=bm.bhit_tu] ~ ~ ~', 'tag @e[type=minecraft:interaction,tag=bm.hbsel] remove bm.hbsel',
                       f'tag {bsel()} remove bm.tusel'])
    fn('p132/b/hitbox', ['summon minecraft:interaction ~ ~ ~ {Tags:["bm.bhit","bm.bhit_tu","bm.hbnew"],width:1.4f,height:3.4f}',
                         'scoreboard players operation @e[type=minecraft:interaction,tag=bm.hbnew] bm.hbid = #tid bm.rng',
                         'tag @e[type=minecraft:interaction,tag=bm.hbnew] add bm.hbsel', 'tag @e[type=minecraft:interaction,tag=bm.hbnew] remove bm.hbnew'])
    h = G.FUNCS['p82/hb/hit']
    h.insert(h.index(next(l for l in h if l.startswith('execute on attacker'))), 'execute if entity @s[tag=bm.bhit_tu] run scoreboard players set #hbk bm.rng 32')
    r = G.FUNCS['p82/hb/relay']
    r.insert(r.index('tag @s remove bm.hbatk'), 'execute if score #hbk bm.rng matches 32 as @e[type=minecraft:husk,tag=bm.tuboss] if score @s bm.tuid = #hbid bm.rng at @s run function bm:p82/hb/dmg with storage bm:tmp hb')
    o = G.FUNCS['p82/hb/orphan']
    o.insert(o.index('kill @s'), 'execute if entity @s[tag=bm.bhit_tu] as @e[type=minecraft:husk,tag=bm.tuboss,distance=..40] if score @s bm.tuid = #hbid bm.rng run return 0')
    # (attack 9) coming up out of the sea: mist, then he stands - and speaks (to Leo, if Leo's here)
    fn('p132/b/a_rise', [at(1, 'particle minecraft:cloud ~ ~1 ~ 0.8 1 0.8 0.02 60'), at(1, 'particle minecraft:soul ~ ~1 ~ 0.6 1 0.6 0.02 30'),
                         at(1, 'playsound minecraft:ambient.underwater.exit hostile @a[distance=..40] ~ ~ ~ 1.5 0.5'),
                         at(1, 'playsound minecraft:entity.drowned.ambient_water hostile @a[distance=..40] ~ ~ ~ 1.5 0.5'),
                         at('2..20', 'particle minecraft:falling_water ~ ~2.5 ~ 0.5 0.8 0.5 0 6'),
                         at(14, 'function bm:p132/b/pose/idle_a'), at(14, bface('sneer')),
                         at(20, 'execute if entity @e[type=minecraft:wolf,tag=bm.leopet,distance=..24] run function bm:p132/b/leo_line'),
                         at(20, 'execute unless entity @e[type=minecraft:wolf,tag=bm.leopet,distance=..24] run ' + tuchat('Another one, come to rob the dead. The sea keeps what is hers - and so do I.', '@a[distance=..40]')),
                         at(56, 'function bm:p132/b/pose/taunt'), at(56, 'playsound minecraft:entity.stray.ambient hostile @a[distance=..40] ~ ~ ~ 1.5 0.5'),
                         at(56, 'title @a[distance=..40] times 10 50 15'), at(56, title('@a[distance=..40]', 'title', T('TULLIUS', ICE, bold=True))),
                         at(56, title('@a[distance=..40]', 'subtitle', T('the Drowned Captain', ICE_LT))),
                         # (and down off the quarterdeck in one bound, onto the deck in front of you)
                         at(68, 'function bm:p132/b/pose/slam_up'), at(68, 'playsound minecraft:entity.dolphin.jump hostile @a[distance=..32] ~ ~ ~ 2 0.6'),
                         at(68, 'function bm:p132/b/leap_aim {d:2.5}'), at('69..82', 'function bm:p132/b/leap_arc'),
                         at(83, 'function bm:p132/b/land'), at(83, bface(None)), at(88, 'function bm:p132/b/begin')])
    fn('p132/b/leo_line', [tuchat('Leo. Still playing the knight? Still getting the glory?', '@a[distance=..40]'),
                           tellraw('@a[distance=..40]', [T('Leo: ', '#5ab8e0', bold=True), T('"Tullius... I thought you went down with the ship."', '#d8f0ff')]),
                           tuchat('I did. It did not take.', '@a[distance=..40]')])
    fn('p132/b/begin', ['scoreboard players set @s bm.tuph 1', 'data merge entity @s {NoAI:0b,Invulnerable:0b}',
                        'bossbar set bm:tub name {text:"Tullius, the Drowned Captain",color:"aqua"}', 'bossbar set bm:tub color blue', 'bossbar set bm:tub visible true',
                        'function bm:p132/b/done', 'scoreboard players set @s bm.tuc 30'])
    # moving: on deck the husk's own feet; in the water he SWIMS - straight at you, fast; under the deck, he leaps aboard
    fn('p132/b/move', ['scoreboard players add @s bm.tuf 1', 'data modify entity @s InWaterTime set value -1',
                       'execute if score #wet bm.rng matches 1 run return run function bm:p132/b/swim',
                       'scoreboard players set #st bm.rng 0', 'execute if predicate bm:p21/walking run scoreboard players set #st bm.rng 1',
                       'execute unless score @s bm.tus = #st bm.rng run scoreboard players set @s bm.tuf 0', 'scoreboard players operation @s bm.tus = #st bm.rng',
                       'scoreboard players operation #f bm.rng = @s bm.tuf',
                       'execute if score #st bm.rng matches 1 run scoreboard players operation #f bm.rng %= #12 bm.rng',
                       'execute if score #st bm.rng matches 0 run scoreboard players operation #f bm.rng %= #60 bm.rng',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 0 unless entity @p[distance=..8] run function bm:p132/b/pose/run_a',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 6 unless entity @p[distance=..8] run function bm:p132/b/pose/run_b',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 0 if entity @p[distance=..8] run function bm:p132/b/pose/walk_a',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 6 if entity @p[distance=..8] run function bm:p132/b/pose/walk_b',
                       'execute if score #st bm.rng matches 0 if score #f bm.rng matches 0 run function bm:p132/b/pose/idle_a',
                       'execute if score #st bm.rng matches 0 if score #f bm.rng matches 30 run function bm:p132/b/pose/idle_b',
                       'execute store result score #hp bm.rng run data get entity @s Health',
                       'execute if score #st bm.rng matches 0 if score #hp bm.rng matches ..90 if score #f bm.rng matches 15 run function bm:p132/b/pose/tired'])
    swim = ['scoreboard players operation #f bm.rng = @s bm.tuf', f'scoreboard players operation #f bm.rng %= #{3 * ART.SWIM_FRAMES} bm.rng'] + \
           [f'execute if score #f bm.rng matches {3 * i} run function bm:p132/b/pose/swim_{i}' for i in range(ART.SWIM_FRAMES)] + \
           ['particle minecraft:bubble ~ ~1 ~ 0.4 0.4 0.4 0.05 3',
            f'execute if entity {pl(40)} facing entity @p[gamemode=!creative,gamemode=!spectator] eyes positioned ^ ^ ^0.34 if block ~ ~1 ~ #bm:p132_swim run tp @s ~ ~ ~ ~ ~']
    fn('p132/b/swim', swim)
    second.append('execute as @e[type=minecraft:husk,tag=bm.tuboss] run data modify entity @s InWaterTime set value -1')
    second.append('execute as @e[type=minecraft:husk,tag=bm.tuboss] at @s unless entity @e[type=minecraft:marker,tag=bm.tuship,distance=..32] '
                  'if entity @e[type=minecraft:marker,tag=bm.tuship,distance=..96] run tp @s @e[type=minecraft:marker,tag=bm.tuspawn,sort=nearest,limit=1]')
    # ---- the mind
    fn('p132/b/mind', ['scoreboard players remove @s bm.tuc 1', 'execute if score @s bm.tuc matches 1.. run return 0', 'scoreboard players set @s bm.tuc 20',
                       # (in the water, and the one he's after is up out of it, near enough: he LEAPS aboard)
                       f'execute if score #wet bm.rng matches 1 if entity {pl(18)} unless entity {pl(18, ",predicate=bm:swim")} run return run function bm:p132/b/start {{a:7}}',
                       'execute if score #wet bm.rng matches 1 run return 0',
                       'execute store result score #hp bm.rng run data get entity @s Health', 'execute store result score #mx bm.rng run attribute @s minecraft:max_health get',
                       'scoreboard players operation #h2 bm.rng = #mx bm.rng', 'scoreboard players operation #h2 bm.rng /= #2 bm.rng',
                       'scoreboard players operation #h6 bm.rng = #mx bm.rng', 'scoreboard players operation #h6 bm.rng *= #3 bm.rng', 'scoreboard players operation #h6 bm.rng /= #5 bm.rng',
                       'execute if score @s bm.tuph matches 1 if score #hp bm.rng <= #h2 bm.rng run return run function bm:p132/b/start {a:8}',
                       'execute if score @s bm.tur matches 0 if score #hp bm.rng <= #h6 bm.rng run return run function bm:p132/b/start {a:6}',
                       'execute store result score #r bm.rng run random value 1..100',
                       f'execute if entity {pl(3.6)} if score #r bm.rng matches 1..45 run return run function bm:p132/b/start {{a:1}}',
                       f'execute if score @s bm.tuph matches 2 if entity {pl(5)} if score #r bm.rng matches 46..70 run return run function bm:p132/b/start {{a:4}}',
                       f'execute if entity {pl(9)} if score #r bm.rng matches 1..60 run return run function bm:p132/b/start {{a:2}}',
                       f'execute if score @s bm.tuph matches 2 if entity {pl(9)} if score #r bm.rng matches 61..80 run return run function bm:p132/b/start {{a:5}}',
                       f'execute if score @s bm.tuph matches 2 if score #r bm.rng matches 81..88 run return run function bm:p132/b/start {{a:10}}',
                       f'execute if entity {pl(22)} unless entity {pl(4.5)} if score #r bm.rng matches 1..70 run return run function bm:p132/b/start {{a:3}}'])
    fn('p132/b/start', ['$scoreboard players set @s bm.tuatk $(a)', 'scoreboard players set @s bm.tut 0', 'scoreboard players set @s bm.tuc 40',
                        'execute if score @s bm.tuph matches 2 run scoreboard players set @s bm.tuc 30', 'effect give @s minecraft:slowness 2 4 true'])
    fn('p132/b/done', ['scoreboard players set @s bm.tuatk 0', 'scoreboard players set @s bm.tus -1', 'scoreboard players set @s bm.tuf 0',
                       'execute if score @s bm.tuph matches 1.. run data merge entity @s {NoAI:0b,NoGravity:0b}'])
    names = {1: 'thrust', 2: 'blast', 3: 'harpoon', 4: 'nova', 5: 'slam', 6: 'crew', 7: 'leap', 8: 'frost', 9: 'rise', 10: 'dive'}
    fn('p132/b/attack', ['scoreboard players add @s bm.tut 1', 'tag @s add bm.tume'] +
       [f'execute if score @s bm.tuatk matches {n} run function bm:p132/b/a_{w}' for n, w in names.items()] + ['tag @s remove bm.tume'])
    face_t = 'execute facing entity @p[gamemode=!creative,gamemode=!spectator] feet run tp @s ~ ~ ~ ~ 0'
    # THE THRUST: the harpoon drawn back - and driven in
    fn('p132/b/a_thrust', [at(1, face_t), at(1, 'function bm:p132/b/pose/thrust_back'), at(1, 'playsound minecraft:item.trident.throw hostile @a[distance=..24] ~ ~ ~ 1 0.6'),
                           at(6, 'function bm:p132/b/pose/thrust'), at(7, f'execute rotated as @s rotated ~ 0 positioned ^ ^1 ^2.4 as {pl(2.6)} at @s run function bm:p132/b/stabbed'),
                           at(7, 'playsound minecraft:item.trident.hit hostile @a[distance=..24] ~ ~ ~ 1 0.6'),
                           at(16, 'function bm:p132/b/pose/guard'), at('20..', 'function bm:p132/b/done')])
    fn('p132/b/stabbed', [f'damage @s 14 minecraft:mob_attack by {me}', 'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.3 10', 'effect give @s minecraft:slowness 2 1'])
    # THE BLUNDERBUSS: aimed - BOOM - a cone of ice; up close it is murderous
    fn('p132/b/a_blast', [at(1, face_t), at(1, 'function bm:p132/b/pose/aim'), at(1, 'playsound minecraft:block.chain.place hostile @a[distance=..24] ~ ~ ~ 1 0.6'),
                          at('2..9', face_t), at('4..9', 'execute rotated as @s rotated ~ 0 positioned ^-0.6 ^2.1 ^1.4 run particle minecraft:snowflake ~ ~ ~ 0.05 0.05 0.05 0.01 2'),
                          at(10, 'function bm:p132/b/pose/fire'), at(10, 'execute rotated as @s rotated ~ 0 positioned ^-0.6 ^0.9 ^1.6 run function bm:p132/b/boom'),
                          at(14, 'function bm:p132/b/pose/reload'), at(18, 'playsound minecraft:item.crossbow.loading_middle hostile @a[distance=..24] ~ ~ ~ 1 0.6'),
                          at(24, 'playsound minecraft:item.crossbow.loading_end hostile @a[distance=..24] ~ ~ ~ 1 0.6'), at('28..', 'function bm:p132/b/done')])
    fn('p132/b/boom', ['particle minecraft:flash{color:[0.7,0.9,1.0,1.0]} ~ ~ ~ 0 0 0 0 1', 'particle minecraft:explosion ~ ~ ~ 0 0 0 0 1',
                       'playsound minecraft:entity.firework_rocket.blast hostile @a[distance=..40] ~ ~ ~ 2 0.5', 'playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 0.8 1.2',
                       'playsound minecraft:block.glass.break hostile @a[distance=..24] ~ ~ ~ 1 0.6'] +
       [f'particle minecraft:snowflake ^{x * d * 0.35:.2f} ^{y * d * 0.2:.2f} ^{d} 0.2 0.2 0.2 0.02 3' for d in (2, 4, 6, 8) for x in (-1, 0, 1) for y in (-1, 1)] +
       [f'particle minecraft:item{{item:{{id:"minecraft:ice"}}}} ^ ^ ^{d} {0.2 * d:.1f} 0.3 {0.2 * d:.1f} 0.05 6' for d in (2, 4, 6)] +
       [f'execute positioned ^ ^ ^{d} as {pl(r)} unless entity @s[tag=bm.tublown] at @s run function bm:p132/b/blasted{n}' for d, r, n in ((1.5, 1.8, 1), (3.5, 2.2, 1), (5.5, 2.8, 2), (8, 3.4, 3))] +
       ['tag @a remove bm.tublown'])
    for n, dmg in ((1, 20), (2, 13), (3, 7)):
        fn(f'p132/b/blasted{n}', ['tag @s add bm.tublown', f'damage @s {dmg} minecraft:mob_projectile by {me}', 'effect give @s minecraft:slowness 3 1',
                                  'particle minecraft:item{item:{id:"minecraft:ice"}} ~ ~1 ~ 0.3 0.4 0.3 0.1 8'])
    # THE HARPOON: wound back and thrown - if it hooks you, you're REELED IN... to the blunderbuss
    hp_item = lambda ice: snbt({'Tags': ['bm.tuharp', 'bm.tuhn'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:tu_harpoon_ice' if ice else 'bm:tu_harpoon'}},
                                'item_display': 'fixed', 'teleport_duration': Int(1),
                                'transformation': {'left_rotation': RF.qf(ART.AHEAD), 'right_rotation': RF.IDENT, 'translation': [F(0)] * 3, 'scale': [F(SB * ART.HARPOON_K)] * 3}})
    fn('p132/b/a_harpoon', [at(1, face_t), at(1, 'function bm:p132/b/pose/throw_back'), at(1, 'playsound minecraft:item.trident.riptide_1 hostile @a[distance=..32] ~ ~ ~ 1 0.6'),
                            at('2..7', face_t), at(8, 'function bm:p132/b/pose/throw'),
                            at(9, 'execute if score @s bm.tuph matches 2 facing entity @p[gamemode=!creative,gamemode=!spectator] eyes positioned ^0.5 ^2.2 ^0.8 run summon minecraft:item_display ~ ~ ~ ' + hp_item(True)),
                            at(9, 'execute unless score @s bm.tuph matches 2 facing entity @p[gamemode=!creative,gamemode=!spectator] eyes positioned ^0.5 ^2.2 ^0.8 run summon minecraft:item_display ~ ~ ~ ' + hp_item(False)),
                            at(9, 'execute as @e[type=minecraft:item_display,tag=bm.tuhn,distance=..4] at @s facing entity @p[gamemode=!creative,gamemode=!spectator] eyes run tp @s ~ ~ ~ ~ ~'),
                            at(9, 'scoreboard players operation @e[type=minecraft:item_display,tag=bm.tuhn,distance=..4] bm.tuid = @s bm.tuid'),
                            at(9, 'scoreboard players set @e[type=minecraft:item_display,tag=bm.tuhn,distance=..4] bm.tul 24'),
                            at(9, 'tag @e[type=minecraft:item_display,tag=bm.tuhn] remove bm.tuhn'), at(9, 'playsound minecraft:item.trident.throw hostile @a[distance=..32] ~ ~ ~ 1.2 0.5'),
                            at(10, 'function bm:p132/b/pose/hook_pull'),
                            at('11..', 'function bm:p132/b/reel')])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.tuharp] at @s run function bm:p132/harp')
    fn('p132/harp', ['scoreboard players remove @s bm.tul 1', 'scoreboard players operation #tid bm.rng = @s bm.tuid',
                     'execute as @e[type=minecraft:husk,tag=bm.tuboss,distance=..40] if score @s bm.tuid = #tid bm.rng run tag @s add bm.tuowner',
                     'particle minecraft:dust{color:[0.75,0.7,0.6],scale:0.6} ~ ~ ~ 0 0 0 0 1', 'particle minecraft:snowflake ~ ~ ~ 0.05 0.05 0.05 0 1',
                     'execute positioned ~ ~-0.8 ~ if entity @a[distance=..1.4,gamemode=!creative,gamemode=!spectator] run return run function bm:p132/hooked',
                     'execute if score @s bm.tul matches ..0 run return run function bm:p132/harp_miss',
                     'execute positioned ^ ^ ^1.1 unless block ~ ~ ~ #bm:grap_pass run return run function bm:p132/harp_miss',
                     'tp @s ^ ^ ^1.1', 'tag @e[tag=bm.tuowner] remove bm.tuowner'])
    fn('p132/hooked', ['execute positioned ~ ~-0.8 ~ run tag @a[distance=..1.4,gamemode=!creative,gamemode=!spectator,sort=nearest,limit=1] add bm.tuhook',
                       'execute as @a[tag=bm.tuhook,tag=!bm.tuhk2] run scoreboard players operation @s bm.tuhk = #tid bm.rng', 'tag @a[tag=bm.tuhook] add bm.tuhk2',
                       'execute as @a[tag=bm.tuhook] run ' + title('@s', 'actionbar', T('HOOKED! He\'s reeling you in!', '#ff6a6a', bold=True)),
                       'playsound minecraft:item.trident.hit hostile @a[distance=..24] ~ ~ ~ 1.4 0.5', 'playsound minecraft:entity.fishing_bobber.retrieve hostile @a[distance=..24] ~ ~ ~ 1.4 0.6',
                       'execute as @a[tag=bm.tuhook] run damage @s 4 minecraft:mob_projectile by @e[type=minecraft:husk,tag=bm.tuowner,limit=1]',
                       'tag @a remove bm.tuhook', 'tag @e[tag=bm.tuowner] remove bm.tuowner', 'kill @s'])
    fn('p132/harp_miss', ['particle minecraft:splash ~ ~ ~ 0.3 0.3 0.3 0.1 10', 'playsound minecraft:item.trident.return hostile @a[distance=..24] ~ ~ ~ 1 0.7',
                          'tag @e[tag=bm.tuowner] remove bm.tuowner', 'kill @s'])
    # (as him: is someone on his line? reel them in - close enough: the blast; nobody hooked and the harpoon gone: done)
    fn('p132/b/reel', ['scoreboard players operation #tid bm.rng = @s bm.tuid', 'tag @a remove bm.tureeled',
                       'execute as @a[tag=bm.tuhk2] if score @s bm.tuhk = #tid bm.rng run tag @s add bm.tureeled',
                       'execute unless entity @a[tag=bm.tureeled] if score @s bm.tut matches 40.. run return run function bm:p132/b/reel_end',
                       'execute unless entity @a[tag=bm.tureeled] run return 0',
                       f'execute as @a[tag=bm.tureeled] at @s facing entity {me} feet run function bm:p132/b/pull',
                       'execute at @a[tag=bm.tureeled] run particle minecraft:dust{color:[0.75,0.7,0.6],scale:0.7} ~ ~1 ~ 0.1 0.1 0.1 0 2',
                       'execute if entity @a[tag=bm.tureeled,distance=..2.8] run return run function bm:p132/b/point_blank',
                       'execute if score @s bm.tut matches 60.. run function bm:p132/b/reel_end'])
    fn('p132/b/pull', ['execute positioned ^ ^ ^0.8 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run tp @s ~ ~ ~',
                       'execute positioned ^ ^ ^0.8 positioned ~ ~1 ~ if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~'])
    fn('p132/b/point_blank', ['function bm:p132/b/pose/blast', face_t.replace('@p[gamemode=!creative,gamemode=!spectator]', '@a[tag=bm.tureeled,limit=1]'),
                              'execute rotated as @s rotated ~ 0 positioned ^-0.5 ^2 ^1.4 run particle minecraft:flash{color:[0.7,0.9,1.0,1.0]} ~ ~ ~ 0 0 0 0 1',
                              'execute rotated as @s rotated ~ 0 positioned ^ ^1.4 ^2 run particle minecraft:item{item:{id:"minecraft:ice"}} ~ ~ ~ 0.6 0.6 0.6 0.2 40',
                              'playsound minecraft:entity.firework_rocket.blast hostile @a[distance=..40] ~ ~ ~ 2 0.4', 'playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1 1',
                              f'execute as @a[tag=bm.tureeled] run damage @s 26 minecraft:mob_projectile by {me}',
                              'effect give @a[tag=bm.tureeled] minecraft:slowness 3 2', tuchat('Point. Blank.', '@a[tag=bm.tureeled]'),
                              'tag @a[tag=bm.tureeled] remove bm.tuhk2', 'tag @a remove bm.tureeled', 'scoreboard players set @s bm.tut 200', 'function bm:p132/b/reel_end'])
    fn('p132/b/reel_end', ['tag @a[tag=bm.tureeled] remove bm.tuhk2', 'tag @a remove bm.tureeled',
                           'execute as @a[tag=bm.tuhk2] if score @s bm.tuhk = #tid bm.rng run tag @s remove bm.tuhk2',
                           'function bm:p132/b/pose/guard', 'function bm:p132/b/done'])
    # THE ICE NOVA (the frost on him): the harpoon raised - spikes of ice burst up all round
    spike = snbt({'Tags': ['bm.tuspike'], 'block_state': 'minecraft:packed_ice', 'teleport_duration': Int(2),
                  'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(-0.3), F(-1.6), F(-0.3)], 'scale': [F(0.6), F(1.8), F(0.6)]}})
    fn('p132/b/a_nova', [at(1, 'function bm:p132/b/pose/ice_cast'), at(1, bface('fury')), at(1, 'playsound minecraft:block.glass.break hostile @a[distance=..24] ~ ~ ~ 1 0.5'),
                         at('2..10', 'particle minecraft:snowflake ~ ~1 ~ 2 0.4 2 0.02 12'), at(11, 'function bm:p132/b/nova'),
                         at(24, bface(None)), at('30..', 'function bm:p132/b/done')])
    nv = []
    for rr, n in ((2, 6), (3.5, 10), (5, 14)):
        for i in range(n):
            a = 2 * math.pi * i / n + rr
            nv.append(f'summon minecraft:block_display ~{rr * math.cos(a):.2f} ~ ~{rr * math.sin(a):.2f} {spike}')
    fn('p132/b/nova', ['execute align y run function bm:p132/b/nova_at', 'playsound minecraft:block.amethyst_block.break hostile @a[distance=..32] ~ ~ ~ 2 0.5',
                       'playsound minecraft:entity.player.hurt_freeze hostile @a[distance=..32] ~ ~ ~ 1 0.6',
                       f'execute as {pl(5.5)} run damage @s 12 minecraft:freeze by {me}', f'effect give {pl(5.5)} minecraft:slowness 2 3',
                       'particle minecraft:item{item:{id:"minecraft:packed_ice"}} ~ ~0.5 ~ 3 0.3 3 0.1 60'])
    fn('p132/b/nova_at', nv + ['scoreboard players set @e[type=minecraft:block_display,tag=bm.tuspike,distance=..7] bm.tul 26',
                               'execute as @e[type=minecraft:block_display,tag=bm.tuspike,distance=..7] at @s run tp @s ~ ~1.4 ~'])
    tick.append('execute as @e[type=minecraft:block_display,tag=bm.tuspike] at @s run function bm:p132/spike')
    fn('p132/spike', ['scoreboard players remove @s bm.tul 1', 'execute if score @s bm.tul matches 6 run tp @s ~ ~-1.4 ~', 'execute if score @s bm.tul matches ..0 run kill @s'])
    # THE HARPOON SLAM (the frost on him): up over his head with both hands - and down
    fn('p132/b/a_slam', [at(1, face_t), at(1, 'function bm:p132/b/pose/slam_up'), at(1, 'playsound minecraft:item.trident.riptide_2 hostile @a[distance=..32] ~ ~ ~ 1 0.6'),
                         at(10, 'function bm:p132/b/pose/slam_mid'), at(13, 'function bm:p132/b/pose/slam'),
                         at(15, f'execute rotated as @s rotated ~ 0 positioned {loc(SLAM_HIT)} run function bm:p132/b/slammed'),
                         at(26, 'function bm:p132/b/pose/guard'), at('32..', 'function bm:p132/b/done')])
    fn('p132/b/slammed', ['particle minecraft:explosion ~ ~0.3 ~ 1 0.1 1 0 4', 'particle minecraft:item{item:{id:"minecraft:packed_ice"}} ~ ~0.4 ~ 2 0.2 2 0.15 50',
                          'particle minecraft:snowflake ~ ~0.4 ~ 2.5 0.3 2.5 0.05 40', 'playsound minecraft:item.trident.thunder hostile @a[distance=..32] ~ ~ ~ 0.5 1.4',
                          'playsound minecraft:block.glass.break hostile @a[distance=..32] ~ ~ ~ 1.5 0.5',
                          f'execute as {pl(3.6)} run damage @s 18 minecraft:mob_attack by {me}', f'effect give {pl(3.6)} minecraft:slowness 3 2'])
    # THE CREW (once, at three-fifths): "All hands!" - his frostbitten crew climbs over the rail
    crew = {'Tags': ['bm.tucrew', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('Frostbitten Crewman', ICE), 'DeathLootTable': 'minecraft:empty',
            'Health': F(26), 'attributes': [{'id': 'minecraft:max_health', 'base': D(26)}, {'id': 'minecraft:follow_range', 'base': D(32)}],
            'equipment': {'mainhand': {'id': 'minecraft:bow', 'count': Int(1)}}, 'drop_chances': {'mainhand': F(0.0)}}
    fn('p132/b/a_crew', [at(1, 'function bm:p132/b/pose/taunt'), at(1, 'scoreboard players set @s bm.tur 1'), at(1, bface('sneer')),
                         at(1, tuchat('All hands! Repel boarders!', '@a[distance=..40]')), at(1, 'playsound minecraft:block.bell.use hostile @a[distance=..48] ~ ~ ~ 2 0.6')] +
       [at(10, f'execute positioned ^{x} ^ ^{z} run summon minecraft:stray ~ ~ ~ {snbt(crew)}') for x, z in ((3, 2), (-3, 2), (0, -3))] +
       [at(10, f'execute positioned ^{x} ^ ^{z} run particle minecraft:splash ~ ~1 ~ 0.4 0.6 0.4 0.1 30') for x, z in ((3, 2), (-3, 2), (0, -3))] +
       [at(18, bface(None)), at('26..', 'function bm:p132/b/done')])
    second.append('execute as @e[type=minecraft:stray,tag=bm.tucrew] at @s unless entity @e[type=minecraft:husk,tag=bm.tuboss,distance=..64] run function bm:p132/crew_go')
    fn('p132/crew_go', ['particle minecraft:splash ~ ~1 ~ 0.3 0.6 0.3 0.1 20', 'tp @s ~ -400 ~', 'kill @s'])
    # THE FROST TAKES HIM (at half): the harpoon ices over; he is quicker and colder
    fn('p132/b/a_frost', [at(1, 'function bm:p132/b/pose/ice_cast'), at(1, bface('fury')), at(1, 'data merge entity @s {Invulnerable:1b}'),
                          at(1, 'playsound minecraft:entity.player.hurt_freeze hostile @a[distance=..48] ~ ~ ~ 2 0.5'),
                          at(1, 'title @a[distance=..40] times 5 50 15'), at(1, title('@a[distance=..40]', 'title', T('THE FROST TAKES HIM', ICE, bold=True))),
                          at(1, title('@a[distance=..40]', 'subtitle', T('The cold of the deep comes up through him.', 'gray', italic=True))),
                          at('2..20', 'particle minecraft:snowflake ~ ~2 ~ 1.4 1.4 1.4 0.05 14'),
                          at(16, 'scoreboard players set @s bm.tuph 2'), at(16, 'function bm:p132/b/pose/ice_cast'),
                          at(16, 'attribute @s minecraft:movement_speed base set 0.34'), at(16, 'bossbar set bm:tub color white'),
                          at(16, 'bossbar set bm:tub name {text:"Tullius, Frozen Fury",color:"white"}'),
                          at(16, tuchat('You want to see what the sea does to a man? Come closer.', '@a[distance=..40]')),
                          at(24, 'data merge entity @s {Invulnerable:0b}'), at(24, bface(None)), at('28..', 'function bm:p132/b/done')])
    second.append('execute as @e[type=minecraft:husk,tag=bm.tuboss,scores={bm.tuph=2}] at @s run particle minecraft:snowflake ~ ~2 ~ 0.6 1 0.6 0.02 4')
    # THE LEAP (out of the water, or back from the dive): up out of the sea in an arc - over the rail, over your head - and down
    #   just behind you (a ghost: the arc is his own, not the water's; the sea's drag would never get a husk up her side)
    fn('p132/b/a_leap', [at(1, 'function bm:p132/b/pose/slam_up'), at(1, 'playsound minecraft:entity.dolphin.jump hostile @a[distance=..32] ~ ~ ~ 2 0.6'),
                         at(1, 'execute facing entity @p[gamemode=!creative,gamemode=!spectator] feet run tp @s ~ ~ ~ ~ 0'),
                         at(1, 'function bm:p132/b/leap_aim {d:-1.5}'), at('1..8', 'particle minecraft:splash ~ ~1 ~ 0.4 0.6 0.4 0.1 12'),
                         at('2..15', 'function bm:p132/b/leap_arc'), at('2..15', 'particle minecraft:falling_water ~ ~1.5 ~ 0.4 0.6 0.4 0 4'),
                         at(16, 'function bm:p132/b/landed'), at('20..', 'function bm:p132/b/done')])
    # (where: d blocks from the one he's after, toward him - out of the sea, -1.5: just past you, so he comes down on the deck
    #  and not on the rail; off the quarterdeck, 2.5: in front of you)
    fn('p132/b/leap_aim', ['data merge entity @s {NoAI:1b,NoGravity:1b,Motion:[0.0d,0.0d,0.0d]}', 'scoreboard players set @s bm.tuh 0',
                           '$execute at @p[gamemode=!creative,gamemode=!spectator] facing entity @s feet rotated ~ 0 positioned ^ ^ ^$(d) run summon minecraft:marker ~ ~ ~ {Tags:["bm.tuaim"]}',
                           'execute store result score #dx bm.rng run data get entity @e[type=minecraft:marker,tag=bm.tuaim,limit=1] Pos[0] 1000',
                           'execute store result score #dy bm.rng run data get entity @e[type=minecraft:marker,tag=bm.tuaim,limit=1] Pos[1] 1000',
                           'execute store result score #dz bm.rng run data get entity @e[type=minecraft:marker,tag=bm.tuaim,limit=1] Pos[2] 1000',
                           'kill @e[type=minecraft:marker,tag=bm.tuaim]',
                           'execute store result score #t bm.rng run data get entity @s Pos[0] 1000', 'scoreboard players operation #dx bm.rng -= #t bm.rng',
                           'execute store result score #t bm.rng run data get entity @s Pos[1] 1000', 'scoreboard players operation #dy bm.rng -= #t bm.rng',
                           'execute store result score #t bm.rng run data get entity @s Pos[2] 1000', 'scoreboard players operation #dz bm.rng -= #t bm.rng',
                           'scoreboard players operation #dx bm.rng /= #14 bm.rng', 'scoreboard players operation #dy bm.rng /= #14 bm.rng',
                           'scoreboard players operation #dz bm.rng /= #14 bm.rng',
                           'scoreboard players operation @s bm.tua = #dx bm.rng', 'scoreboard players operation @s bm.tuv = #dy bm.rng',
                           'scoreboard players operation @s bm.tuz = #dz bm.rng'])
    # (each of 14 ticks: a fourteenth of the way, and a rise that slows and turns to a fall - up to a block and a half over the line)
    fn('p132/b/leap_arc', ['scoreboard players operation #k bm.rng = @s bm.tuh', 'scoreboard players add @s bm.tuh 1', 'scoreboard players operation #k bm.rng *= #61 bm.rng',
                           'scoreboard players set #b bm.rng 400', 'scoreboard players operation #b bm.rng -= #k bm.rng', 'scoreboard players operation #b bm.rng += @s bm.tuv',
                           'execute store result storage bm:tmp tuarc.x double 0.001 run scoreboard players get @s bm.tua',
                           'execute store result storage bm:tmp tuarc.y double 0.001 run scoreboard players get #b bm.rng',
                           'execute store result storage bm:tmp tuarc.z double 0.001 run scoreboard players get @s bm.tuz',
                           'function bm:p132/b/arc with storage bm:tmp tuarc'])
    fn('p132/b/arc', ['$tp @s ~$(x) ~$(y) ~$(z)'])
    fn('p132/b/landed', ['function bm:p132/b/land', 'scoreboard players set @s bm.tut 41'])
    fn('p132/b/land', ['data merge entity @s {NoAI:0b,NoGravity:0b}', 'function bm:p132/b/pose/slam', 'particle minecraft:splash ~ ~0.4 ~ 1.5 0.2 1.5 0.2 40',
                       'particle minecraft:snowflake ~ ~0.4 ~ 1.5 0.2 1.5 0.05 20',
                       'playsound minecraft:item.trident.thunder hostile @a[distance=..32] ~ ~ ~ 0.3 1.6', 'playsound minecraft:entity.generic.big_fall hostile @a[distance=..24] ~ ~ ~ 1 0.6',
                       f'execute as {pl(2.8)} run damage @s 10 minecraft:mob_attack by {me}'])
    # THE DIVE (the frost on him): "The sea is mine" - over the side, and back out of it at you
    fn('p132/b/a_dive', [at(1, 'function bm:p132/b/pose/taunt'), at(1, bface('sneer')), at(1, tuchat('The sea is MINE.', '@a[distance=..32]')),
                         at(8, 'function bm:p132/b/pose/slam_up'), at(8, 'function bm:p132/b/dive_go'),
                         at(8, 'playsound minecraft:entity.dolphin.jump hostile @a[distance=..32] ~ ~ ~ 2 0.5'),
                         at('9..60', 'execute if score #wet bm.rng matches 1 run function bm:p132/b/under'),
                         at(30, bface(None)), at('61..', 'function bm:p132/b/done')])
    fn('p132/b/dive_go', ['data modify entity @s Motion[1] set value 0.8d', 'data modify storage bm:tmp kxd.s set value -0.75d',
                          'function bm:p79/pet/dir with storage bm:tmp kxd',
                          'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                          'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng'])
    fn('p132/b/under', ['effect give @s minecraft:regeneration 2 1 true', 'particle minecraft:bubble_column_up ~ ~1 ~ 0.4 0.6 0.4 0.1 10',
                        'execute if score @s bm.tut matches 40.. run function bm:p132/b/start {a:7}'])
    # each hit on him: a grunt and the crack of ice
    wjson('bm/advancement/p132/hit.json', {'criteria': {'h': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.tuboss"]}'}}]}}}, 'rewards': {'function': 'bm:p132/hit'}})
    fn('p132/hit', ['advancement revoke @s only bm:p132/hit', 'execute at @s as @e[type=minecraft:husk,tag=bm.tuboss,distance=..48,limit=1,sort=nearest] at @s run function bm:p132/b/ouch'])
    fn('p132/b/ouch', ['playsound minecraft:entity.stray.hurt hostile @a[distance=..32] ~ ~ ~ 1 0.6', 'playsound minecraft:block.glass.hit hostile @a[distance=..32] ~ ~ ~ 1 0.6',
                       'particle minecraft:item{item:{id:"minecraft:ice"}} ~ ~2 ~ 0.4 0.6 0.4 0.1 8'])
    # every second: the bar; and if he's alone a minute, back into the sea
    second += ['bossbar set bm:tub players', 'execute as @e[type=minecraft:husk,tag=bm.tuboss] at @s run function bm:p132/b/sec']
    fn('p132/b/sec', ['execute store result bossbar bm:tub value run data get entity @s Health', 'execute store result bossbar bm:tub max run attribute @s minecraft:max_health get',
                      'execute if score @s bm.tuph matches 1.. run bossbar set bm:tub players @a[distance=..48]',
                      'execute if entity @a[distance=..64,gamemode=!spectator] run scoreboard players set @s bm.tulone 0',
                      'execute unless entity @a[distance=..64,gamemode=!spectator] run scoreboard players add @s bm.tulone 1',
                      'execute if score @s bm.tulone matches 45.. run function bm:p132/b/leave'])
    # (2.78: his chunk unloaded a minute or more - everyone died or went far, and he sat frozen where they left him: the fight is over.
    #  And a death with nobody else near him ends it at once.)
    G.FUNCS['p132/b/sec'][0:0] = ['execute store result score #now bm.rng run time query gametime',
                                  'execute unless score @s bm.tuseen matches 1.. run scoreboard players operation @s bm.tuseen = #now bm.rng',
                                  'scoreboard players operation #gap bm.rng = #now bm.rng', 'scoreboard players operation #gap bm.rng -= @s bm.tuseen',
                                  'scoreboard players operation @s bm.tuseen = #now bm.rng',
                                  'execute if score #gap bm.rng matches 1200.. run return run function bm:p132/b/leave']
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.tuseen dummy']
    G.OBJECTIVES += ['bm.tuseen']
    fn('p132/b/died', ['tag @s add bm.dying', 'execute as @e[type=minecraft:husk,tag=bm.tuboss,distance=..80] at @s unless entity @a[tag=!bm.dying,distance=..64,gamemode=!spectator] run function bm:p132/b/leave', 'tag @s remove bm.dying'])
    G.FUNCS['p62/died'][0:0] = ['execute at @s run function bm:p132/b/died']
    fn('p132/b/leave', ['bossbar set bm:tub visible false', 'particle minecraft:splash ~ ~1 ~ 0.4 0.8 0.4 0.1 30', 'function bm:p132/b/unrig',
                        'execute as @e[type=minecraft:marker,tag=bm.tuship,distance=..40] run scoreboard players set @s bm.tuw 0', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p132/b/unrig', ['scoreboard players operation #tid bm.rng = @s bm.tuid',
                        'execute as @e[type=minecraft:item_display,tag=bm.tub,distance=..24] if score @s bm.tuid = #tid bm.rng run kill @s',
                        'execute as @e[type=minecraft:item_display,tag=bm.tuharp] if score @s bm.tuid = #tid bm.rng run kill @s'])
    # ---- he falls: the rig without its host - down on one knee, and the frost lets him go
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.tub,tag=bm.tup_body,tag=!bm.tudie] at @s if entity @a[distance=..96] run function bm:p132/b/orphan')
    fn('p132/b/orphan', ['scoreboard players operation #tid bm.rng = @s bm.tuid',
                         'execute as @e[type=minecraft:husk,tag=bm.tuboss,distance=..48] if score @s bm.tuid = #tid bm.rng run return 0',
                         'execute as @e[type=minecraft:item_display,tag=bm.tub,distance=..24] if score @s bm.tuid = #tid bm.rng run tag @s add bm.tusel',
                         'function bm:p132/b/pose/defeated', bface('hurt'), f'scoreboard players set {bsel()} bm.tul 60', f'tag {bsel()} add bm.tudie',
                         'bossbar set bm:tub visible false', 'function bm:p132/b/fallen', f'tag {bsel()} remove bm.tusel'])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.tudie] at @s run function bm:p132/b/fade')
    fn('p132/b/fade', ['scoreboard players remove @s bm.tul 1',
                       'execute if score @s bm.tul matches 10..30 run particle minecraft:snowflake ~ ~0.4 ~ 0.3 0.3 0.3 0.02 2',
                       'execute if score @s bm.tul matches 12 run data merge entity @s {start_interpolation:0,interpolation_duration:10,transformation:{scale:[0f,0f,0f]}}',
                       'execute if score @s bm.tul matches 12 if entity @s[tag=bm.tup_head] run particle minecraft:totem_of_undying ~ ~1 ~ 1 1 1 0.4 80',
                       'execute if score @s bm.tul matches ..0 run kill @s'])
    fn('p132/b/fallen', ['playsound minecraft:entity.stray.death hostile @a[distance=..48] ~ ~ ~ 1.5 0.5', 'playsound minecraft:block.bell.use hostile @a[distance=..64] ~ ~ ~ 2 0.5',
                         'particle minecraft:snowflake ~ ~1.5 ~ 1.2 1.2 1.2 0.1 120', 'particle minecraft:splash ~ ~1 ~ 1 1 1 0.2 80',
                         'title @a[distance=..48] times 10 70 20', title('@a[distance=..48]', 'title', T('TULLIUS IS BEATEN', ICE, bold=True)),
                         title('@a[distance=..48]', 'subtitle', T('the drowned captain kneels', 'gray', italic=True)),
                         tuchat('...Hah. Well fought. It has been a long time since anyone made me kneel. ...Fine. My doubloon, then. I will sail with you.', '@a[distance=..48]'),
                         'execute as @a[distance=..48,gamemode=!spectator] at @s run function bm:p132/reward',
                         'execute as @e[type=minecraft:marker,tag=bm.tuship,distance=..48] run function bm:p132/ship/beaten',
                         tellraw('@a', PREFIX + [T('Tullius, the Drowned Captain', ICE, bold=True), T(' has been beaten on his ghost ship!', 'gray')])])
    fn('p132/ship/beaten', ['scoreboard players set @s bm.tuw 2', 'scoreboard players set @s bm.tut 1200'])
    fn('p132/reward', ['scoreboard players add @s bm.tuk 1', 'execute if score @s bm.tuk matches 1 run function bm:p132/first',
                       'execute store result score #r bm.rng run random value 1..100',
                       'execute if score @s bm.tuk matches 2.. if score #r bm.rng matches 1..20 run ' + give('tul_blunderbuss'),
                       'execute if score @s bm.tuk matches 2.. if score #r bm.rng matches 21..40 run ' + give('tul_harpoon'),
                       'execute if score @s bm.tuk matches 2.. if score #r bm.rng matches 41..48 run ' + give('tul_coin'),
                       'loot give @s loot bm:p132/hoard', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1', 'advancement grant @s only bm:story/tullius'])
    fn('p132/first', [give('tul_coin'), give('tul_blunderbuss'), give('tul_harpoon'),
                      tellraw('@s', PREFIX + [T("Tullius's Frozen Doubloon", ICE, bold=True), T(', ', 'gray'), T('the Frostbite Blunderbuss', ICE, bold=True), T(' and ', 'gray'),
                                              T("Tullius's Harpoon", ICE, bold=True), T(' are yours. Use the Doubloon and he\'ll sail with you.', 'gray')])])
    wjson('bm/loot_table/p132/hoard.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('medallion', G.uni(3, 6))]},
                                                      {'rolls': 1, 'entries': [G.loot_entry('trophy', G.uni(1, 2))]},
                                                      {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(5, 10))]},
                                                      {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:heart_of_the_sea', 'weight': 1},
                                                                               {'type': 'minecraft:item', 'name': 'minecraft:nautilus_shell', 'weight': 3,
                                                                                'functions': [{'function': 'minecraft:set_count', 'count': G.uni(1, 3)}]}]},
                                                      {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:gold_ingot',
                                                                                'functions': [{'function': 'minecraft:set_count', 'count': G.uni(4, 10)}]}]}]})
    wjson('bm/advancement/story/tullius.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:tul_coin'}},
                                                            'title': T('The Drowned Captain', 'yellow'), 'description': T('Board the ghost ship in the cold seas and beat Tullius', 'gray'),
                                                            'frame': 'challenge', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})

    # ================================================================== HIS WEAPONS
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    # the blunderbuss: a cone of ice shards (close = brutal); 1.5 s to reload
    fn('p132/gun/use', ['execute if score @s bm.tugc matches 1.. run return run ' + say('Reloading...', ICE_LT), 'scoreboard players set @s bm.tugc 30',
                        'tag @s add bm.tugun', 'execute anchored eyes positioned ^ ^-0.2 ^0.6 run function bm:p132/gun/boom', 'tag @s remove bm.tugun'])
    tick.append('scoreboard players remove @a[scores={bm.tugc=1..}] bm.tugc 1')
    fn('p132/gun/boom', ['particle minecraft:flash{color:[0.7,0.9,1.0,1.0]} ^ ^ ^0.6 0 0 0 0 1', 'playsound minecraft:entity.firework_rocket.blast player @a[distance=..32] ~ ~ ~ 1.5 0.5',
                         'playsound minecraft:block.glass.break player @a[distance=..16] ~ ~ ~ 0.6 0.7'] +
       [f'particle minecraft:snowflake ^{x * d * 0.3:.2f} ^ ^{d} 0.15 0.15 0.15 0.02 2' for d in (2, 4, 6) for x in (-1, 0, 1)] +
       [f'execute positioned ^ ^ ^{d} as @e[{foe},distance=..{r},tag=!bm.tublown] at @s run function bm:p132/gun/hit{n}' for d, r, n in ((1.5, 1.8, 1), (3.5, 2.2, 1), (5.5, 2.6, 2), (8, 3.0, 3))] +
       ['tag @e[tag=bm.tublown] remove bm.tublown'])
    for n, dmg in ((1, 16), (2, 10), (3, 5)):
        fn(f'p132/gun/hit{n}', ['tag @s add bm.tublown', f'damage @s {dmg} minecraft:player_attack by @a[tag=bm.tugun,limit=1]', 'effect give @s minecraft:slowness 3 1',
                                'particle minecraft:item{item:{id:"minecraft:ice"}} ~ ~1 ~ 0.3 0.4 0.3 0.1 6'])
    # the harpoon: what it hits is reeled in to whoever threw it
    wjson('bm/advancement/p132/harpoon.json', {'criteria': {'h': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'damage': {
        'direct_entity': {'type': 'minecraft:trident', 'nbt': '{item:{components:{"minecraft:custom_data":{bm:"tul_harpoon"}}}}'}}}}}, 'rewards': {'function': 'bm:p132/harpoon/hit'}})
    fn('p132/harpoon/hit', ['advancement revoke @s only bm:p132/harpoon', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                            'scoreboard players operation #me bm.pid = @s bm.pid',
                            'execute as @e[type=minecraft:trident,distance=..64,nbt={item:{components:{"minecraft:custom_data":{bm:"tul_harpoon"}}}}] at @s '
                            f'as @e[{foe},distance=..3,nbt={{HurtTime:10s}},sort=nearest,limit=1] at @s run function bm:p132/harpoon/hook'])
    fn('p132/harpoon/hook', ['tag @s add bm.tureel', 'scoreboard players operation @s bm.tuhk = #me bm.pid', 'scoreboard players set @s bm.tul 16',
                             'playsound minecraft:entity.fishing_bobber.retrieve player @a[distance=..24] ~ ~ ~ 1.4 0.6'])
    tick.append('execute as @e[tag=bm.tureel] at @s run function bm:p132/harpoon/reel')
    fn('p132/harpoon/reel', ['scoreboard players remove @s bm.tul 1', 'execute if score @s bm.tul matches ..0 run return run tag @s remove bm.tureel',
                             'scoreboard players operation #me bm.pid = @s bm.tuhk', 'execute as @a if score @s bm.pid = #me bm.pid run tag @s add bm.tureeler',
                             'execute unless entity @a[tag=bm.tureeler,distance=..40] run return run tag @s remove bm.tureel',
                             'execute if entity @a[tag=bm.tureeler,distance=..2.5] run tag @s remove bm.tureel',
                             'execute if entity @s[tag=bm.tureel] facing entity @a[tag=bm.tureeler,limit=1] feet positioned ^ ^ ^0.9 if block ~ ~ ~ #bm:grap_pass run tp @s ~ ~ ~',
                             'particle minecraft:dust{color:[0.75,0.7,0.6],scale:0.7} ~ ~0.8 ~ 0.1 0.1 0.1 0 2', 'tag @a remove bm.tureeler'])

    # ================================================================== THE FOLLOWER
    def psel(p=None):
        return '@e[type=minecraft:item_display,tag=bm.tusel' + (f',tag=bm.tup_{p}]' if p else ']')
    sel_pet = 'execute as @e[type=minecraft:wolf,tag=bm.tupet] if score @s bm.pid = #me bm.pid'
    face = lambda e, t: FX.face_cmd('tul', e, t)
    rig = [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.tup", f"bm.tup_{p}", "bm.tup_pet", "bm.tunew"], SP, scale0=True, extra={"shadow_radius": F(0.5 if p == "body" else 0.0), "shadow_strength": F(0.5)})}'
           for p in A.PARTS]
    fn('p132/place', RF.place(A, UP, psel))
    fn('p132/grow', [f'execute as {psel(p)} run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{SP * A.PART_K.get(p, 1.0):.4f}f,{SP * A.PART_K.get(p, 1.0):.4f}f,{SP * A.PART_K.get(p, 1.0):.4f}f]}}}}'
                     for p in A.PARTS] + [f'execute at {psel("body")[:-1]},limit=1] run function bm:p132/burst'])
    fn('p132/burst', ['particle minecraft:snowflake ~ ~1 ~ 0.4 0.8 0.4 0.05 50', 'particle minecraft:splash ~ ~1 ~ 0.4 0.8 0.4 0.1 40',
                      'particle minecraft:flash{color:[0.6,0.85,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:item{item:{id:"minecraft:ice"}} ~ ~1 ~ 0.4 0.6 0.4 0.1 20'])
    # states: 0 idle, 1 walk, 2 run, 3 air, 4 sit, 6 arriving (his taunt), 7 thrust, 8 blast, 9 harpoon, 12 the broadside, 10 swim
    CYCLE = {0: (120, [(0, 'idle_a'), (30, 'idle_b'), (60, 'idle_a'), (90, 'idle_b')]), 1: (12, [(0, 'walk_a'), (6, 'walk_b')]), 2: (8, [(0, 'run_a'), (4, 'run_b')]),
             3: (None, [(0, 'guard')]), 4: (None, [(0, 'sit')]), 6: (None, [(0, 'taunt')]),
             7: (None, [(0, 'thrust_back'), (4, 'thrust')]), 8: (None, [(0, 'aim'), (6, 'fire'), (9, 'reload')]),
             9: (None, [(0, 'throw_back'), (5, 'throw'), (7, 'hook_pull'), (16, 'blast')]), 12: (None, [(0, 'aim'), (8, 'blast')]),
             10: (3 * ART.SWIM_FRAMES, [(3 * i, f'swim_{i}') for i in range(ART.SWIM_FRAMES)])}
    RF.cycles(fn, 'p132', CYCLE, 'bm.tuf', 'bm.tus', lambda p: f'p132/pose/{p}')
    used = {p for _per, frames in CYCLE.values() for _t, p in frames}
    for name, pz in POSES.items():
        if name in DUR_P and name in used:
            fn(f'p132/pose/{name}', RF.pose(A, pz, SP, DUR_P[name], psel, swap=SWAP))
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in RF.periods(CYCLE)]
    fn('p132/state', ['execute if score @s bm.tusl matches 1.. run return run scoreboard players set #st bm.rng 6',
                      'execute if score @s bm.tux matches 1.. run return run scoreboard players operation #st bm.rng = @s bm.tua',
                      'execute if data entity @s {Sitting:1b} run return run scoreboard players set #st bm.rng 4',
                      'execute store result score #og bm.rng run data get entity @s OnGround',
                      'execute if score #og bm.rng matches 0 if predicate bm:swim run return run scoreboard players set #st bm.rng 10',
                      'execute if score #og bm.rng matches 0 run scoreboard players add @s bm.tuz 1', 'execute if score #og bm.rng matches 1 run scoreboard players set @s bm.tuz 0',
                      'execute if score @s bm.tuz matches 4.. unless block ~ ~ ~ minecraft:water run return run scoreboard players set #st bm.rng 3',
                      'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                      'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                      'scoreboard players operation #vx bm.rng += #vz bm.rng',
                      'execute if score #vx bm.rng matches 30000.. run return run scoreboard players set #st bm.rng 2',
                      'execute if score #vx bm.rng matches 500.. run return run scoreboard players set #st bm.rng 1',
                      'scoreboard players set #st bm.rng 0'])
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.tupet] at @s run function bm:p132/tick')
    fn('p132/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                     'execute as @e[type=minecraft:item_display,tag=bm.tup_pet,tag=!bm.tufade] if score @s bm.pid = #me bm.pid run tag @s add bm.tusel',
                     f'execute unless entity {psel("harpoon")} run function bm:p132/rerig',
                     'scoreboard players set #wet bm.rng 0', 'execute if predicate bm:swim run scoreboard players set #wet bm.rng 1',
                     'execute if score @s bm.tux matches 1.. run function bm:p132/act_tick',
                     'execute if score @s bm.tum matches 1.. run scoreboard players remove @s bm.tum 1',
                     'execute if score @s bm.tuv matches 1.. run scoreboard players remove @s bm.tuv 1',
                     'execute if score @s bm.tusl matches 1.. run scoreboard players remove @s bm.tusl 1',
                     # his fights: the thrust in reach; the blunderbuss a little way off; at range, the harpoon (it pulls them in); every 7th blow, the broadside
                     f'execute unless score @s bm.tux matches 1.. unless score @s bm.tum matches 1.. unless data entity @s {{Sitting:1b}} if entity @e[{foe},distance=..3.2] run function bm:p132/thrust_go',
                     f'execute unless score @s bm.tux matches 1.. unless score @s bm.tum matches 1.. unless data entity @s {{Sitting:1b}} unless entity @e[{foe},distance=..3.2] if entity @e[{foe},distance=..7] run function bm:p132/blast_go',
                     f'execute unless score @s bm.tux matches 1.. unless score @s bm.tuv matches 1.. unless data entity @s {{Sitting:1b}} unless entity @e[{foe},distance=..7] if entity @e[{foe},distance=..16] run function bm:p132/harpoon_go',
                     'function bm:p132/state',
                     'execute if score #st bm.rng = @s bm.tus run scoreboard players add @s bm.tuf 1',
                     'execute unless score #st bm.rng = @s bm.tus run scoreboard players set @s bm.tuf 0',
                     'scoreboard players operation @s bm.tus = #st bm.rng',
                     'function bm:p132/anim',
                     'execute on owner run tag @s add bm.tuown',
                     f'execute if score @s bm.tus matches 7..9 if entity @e[{foe},distance=..17] facing entity @e[{foe},distance=..17,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p132/place',
                     f'execute if score @s bm.tus matches 12 if entity @e[{foe},distance=..17] facing entity @e[{foe},distance=..17,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p132/place',
                     f'execute if score @s bm.tus matches 7..9 unless entity @e[{foe},distance=..17] rotated as @s rotated ~ 0 run function bm:p132/place',
                     f'execute if score @s bm.tus matches 12 unless entity @e[{foe},distance=..17] rotated as @s rotated ~ 0 run function bm:p132/place',
                     'execute if score @s bm.tus matches 0 run function bm:p132/face_you', 'execute if score @s bm.tus matches 4 run function bm:p132/face_you',
                     'execute if score @s bm.tus matches 6 run function bm:p132/face_you',
                     'execute if score @s bm.tus matches 1..3 rotated as @s rotated ~ 0 run function bm:p132/place',
                     'execute if score @s bm.tus matches 10 rotated as @s rotated ~ 0 positioned ~ ~0.2 ~ run function bm:p132/place',
                     'function bm:p132/box',
                     'tag @a[tag=bm.tuown] remove bm.tuown', 'tag @e[tag=bm.tusel] remove bm.tusel'])
    fn('p132/face_you', ['execute if entity @a[tag=bm.tuown,distance=1.5..10] facing entity @a[tag=bm.tuown,limit=1] feet rotated ~ 0 run return run function bm:p132/place',
                         'execute rotated as @s rotated ~ 0 run function bm:p132/place'])
    wet = lambda base: [f'scoreboard players set #pd bm.rng {base}', f'execute if score #wet bm.rng matches 1 run scoreboard players set #pd bm.rng {int(base * 1.4)}']
    fn('p132/thrust_go', ['scoreboard players add @s bm.tuch 1', 'execute if score @s bm.tuch matches 7.. run return run function bm:p132/broadside_go',
                          'scoreboard players set @s bm.tua 7', 'scoreboard players set @s bm.tux 10', 'scoreboard players set @s bm.tum 22'])
    fn('p132/blast_go', ['scoreboard players add @s bm.tuch 1', 'execute if score @s bm.tuch matches 7.. run return run function bm:p132/broadside_go',
                         'scoreboard players set @s bm.tua 8', 'scoreboard players set @s bm.tux 18', 'scoreboard players set @s bm.tum 34'])
    fn('p132/harpoon_go', ['scoreboard players set @s bm.tua 9', 'scoreboard players set @s bm.tux 22', 'scoreboard players set @s bm.tuv 90', 'scoreboard players set @s bm.tum 22',
                           'playsound minecraft:item.trident.throw neutral @a[distance=..16] ~ ~ ~ 0.7 0.8'])
    fn('p132/broadside_go', ['scoreboard players set @s bm.tuch 0', 'scoreboard players set @s bm.tua 12', 'scoreboard players set @s bm.tux 16', 'scoreboard players set @s bm.tum 40',
                             'playsound minecraft:block.chain.place neutral @a[distance=..16] ~ ~ ~ 1 0.6'] + face('fury', 16))
    fn('p132/act_tick', ['scoreboard players remove @s bm.tux 1',
                         'execute if score @s bm.tua matches 7 if score @s bm.tux matches 6 run function bm:p132/thrust_hit',
                         'execute if score @s bm.tua matches 8 if score @s bm.tux matches 12 run function bm:p132/blast_hit',
                         'execute if score @s bm.tua matches 9 if score @s bm.tux matches 16 run function bm:p132/hook',
                         'execute if score @s bm.tua matches 9 if score @s bm.tux matches 7..15 run function bm:p132/drag',
                         'execute if score @s bm.tua matches 9 if score @s bm.tux matches 6 run function bm:p132/pb',
                         'execute if score @s bm.tua matches 12 if score @s bm.tux matches 8 run function bm:p132/broadside'])
    fn('p132/thrust_hit', ['tag @s add bm.tume2'] + wet(9) + ['playsound minecraft:item.trident.hit neutral @a[distance=..16] ~ ~ ~ 1 0.8',
                           f'execute as @e[{foe},distance=..3.6,sort=nearest,limit=1] at @s run function bm:p132/stab', 'tag @s remove bm.tume2', 'function bm:p132/hit_count'])
    fn('p132/stab', ['execute store result storage bm:tmp tu.d int 1 run scoreboard players get #pd bm.rng', 'function bm:p132/dmg with storage bm:tmp tu',
                     'particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.2 8'])
    fn('p132/dmg', ['$damage @s $(d) minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.tume2,limit=1]'])
    fn('p132/blast_hit', ['tag @s add bm.tume2'] + wet(8) + ['playsound minecraft:entity.firework_rocket.blast neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                          f'execute facing entity @e[{foe},distance=..8,sort=nearest,limit=1] feet positioned ^ ^1 ^1 run function bm:p132/cone',
                          'tag @s remove bm.tume2', 'function bm:p132/hit_count'])
    fn('p132/cone', ['particle minecraft:flash{color:[0.7,0.9,1.0,1.0]} ~ ~ ~ 0 0 0 0 1'] +
       [f'particle minecraft:snowflake ^{x * d * 0.3:.2f} ^ ^{d} 0.15 0.15 0.15 0.02 2' for d in (1, 3, 5) for x in (-1, 0, 1)] +
       [f'execute positioned ^ ^ ^{d} as @e[{foe},distance=..{r},tag=!bm.tublown] at @s run function bm:p132/coned' for d, r in ((1, 1.6), (3, 2.0), (5, 2.4), (7, 2.8))] +
       ['tag @e[tag=bm.tublown] remove bm.tublown'])
    fn('p132/coned', ['tag @s add bm.tublown', 'execute store result storage bm:tmp tu.d int 1 run scoreboard players get #pd bm.rng', 'function bm:p132/dmg with storage bm:tmp tu',
                      'effect give @s minecraft:slowness 3 1', 'particle minecraft:item{item:{id:"minecraft:ice"}} ~ ~1 ~ 0.3 0.4 0.3 0.1 6'])
    # the harpoon pull: the nearest foe at range hooked (a rope between them), dragged to him - then the blast, point-blank
    fn('p132/hook', [f'tag @e[{foe},distance=7..17,sort=nearest,limit=1] add bm.tudrag', 'scoreboard players operation @e[tag=bm.tudrag,tag=!bm.tudr2] bm.tuhk = #me bm.pid',
                     'tag @e[tag=bm.tudrag] add bm.tudr2', 'tag @e[tag=bm.tudrag] remove bm.tudrag',
                     'playsound minecraft:entity.fishing_bobber.retrieve neutral @a[distance=..24] ~ ~ ~ 1.2 0.6'])
    fn('p132/drag', ['execute as @e[tag=bm.tudr2,distance=..24] if score @s bm.tuhk = #me bm.pid run tag @s add bm.tudrs',
                     'execute as @e[tag=bm.tudrs] at @s facing entity @e[type=minecraft:wolf,tag=bm.tupet,distance=..24,sort=nearest,limit=1] feet positioned ^ ^ ^1.1 if block ~ ~ ~ #bm:grap_pass run tp @s ~ ~ ~',
                     'execute at @e[tag=bm.tudrs] run particle minecraft:dust{color:[0.75,0.7,0.6],scale:0.7} ~ ~0.8 ~ 0.1 0.1 0.1 0 2',
                     'tag @e[tag=bm.tudrs] remove bm.tudrs'])
    fn('p132/pb', ['tag @s add bm.tume2'] + wet(14) + ['playsound minecraft:entity.firework_rocket.blast neutral @a[distance=..24] ~ ~ ~ 1.4 0.5',
                   'execute as @e[tag=bm.tudr2,distance=..24] if score @s bm.tuhk = #me bm.pid at @s run function bm:p132/pbd',
                   'tag @s remove bm.tume2', 'function bm:p132/hit_count'])
    fn('p132/pbd', ['tag @s remove bm.tudr2', 'execute store result storage bm:tmp tu.d int 1 run scoreboard players get #pd bm.rng', 'function bm:p132/dmg with storage bm:tmp tu',
                    'effect give @s minecraft:slowness 3 2', 'particle minecraft:item{item:{id:"minecraft:ice"}} ~ ~1 ~ 0.4 0.5 0.4 0.15 16'])
    fn('p132/broadside', ['tag @s add bm.tume2'] + wet(20) + ['playsound minecraft:entity.generic.explode neutral @a[distance=..32] ~ ~ ~ 1.2 0.8',
                          'playsound minecraft:entity.player.hurt_freeze neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                          f'execute facing entity @e[{foe},distance=..12,sort=nearest,limit=1] feet positioned ^ ^1 ^1 run function bm:p132/broad_cone',
                          'tag @s remove bm.tume2', 'execute on owner if entity @s[distance=..24] run ' + tusay('Broadside!')])
    fn('p132/broad_cone', ['particle minecraft:flash{color:[0.7,0.9,1.0,1.0]} ~ ~ ~ 0 0 0 0 1'] +
       [f'particle minecraft:snowflake ^{x * d * 0.4:.2f} ^ ^{d} 0.3 0.3 0.3 0.03 4' for d in (2, 4, 6, 8) for x in (-1, 0, 1)] +
       [f'execute positioned ^ ^ ^{d} as @e[{foe},distance=..{r},tag=!bm.tublown] at @s run function bm:p132/broadsided' for d, r in ((1.5, 2.0), (4, 2.8), (6.5, 3.4), (9, 3.8))] +
       ['tag @e[tag=bm.tublown] remove bm.tublown'])
    fn('p132/broadsided', ['tag @s add bm.tublown', 'execute store result storage bm:tmp tu.d int 1 run scoreboard players get #pd bm.rng', 'function bm:p132/dmg with storage bm:tmp tu',
                           'effect give @s minecraft:slowness 4 3', 'particle minecraft:item{item:{id:"minecraft:packed_ice"}} ~ ~1 ~ 0.4 0.6 0.4 0.1 12'])
    QUIPS = ['Sink.', 'Stay down. The sea is patient; I am not.', 'Another for the deep.', 'Hah. Sloppy.', 'Cold, is it?', 'Leo would have missed that one.', 'Fire!']
    fn('p132/hit_count', ['scoreboard players add @s bm.tuq 1', 'execute if score @s bm.tuq matches 9.. run function bm:p132/quip'])
    fn('p132/quip', ['scoreboard players set @s bm.tuq 0', f'execute store result score #r bm.rng run random value 1..{len(QUIPS)}'] +
       [f'execute if score #r bm.rng matches {i + 1} on owner if entity @s[distance=..20] run ' + tusay(q) for i, q in enumerate(QUIPS)] + face('sneer', 30))
    second.append('execute as @e[tag=bm.tudr2] run function bm:p132/drag_old')
    fn('p132/drag_old', ['scoreboard players add @s bm.tuz 1', 'execute if score @s bm.tuz matches 3.. run tag @s remove bm.tudr2',
                         'execute if score @s bm.tuz matches 3.. run scoreboard players set @s bm.tuz 0'])

    # ---- the Doubloon: call, recall, sneak for his menu
    pet = {'Tags': ['bm.tupet', 'bm.tunew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(PET_HP),
           'CustomName': T('Tullius', ICE, bold=True), 'CustomNameVisible': B(0),
           'attributes': [{'id': f'minecraft:{k}', 'base': D(v)} for k, v in dict(max_health=PET_HP, armor=10, armor_toughness=3, attack_damage=4, knockback_resistance=0.5,
                                                                                  movement_speed=0.34, follow_range=32, step_height=1.0, water_movement_efficiency=1.0,
                                                                                  oxygen_bonus=1000).items()],
           'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)},
                              {'id': 'minecraft:dolphins_grace', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    in_heist = 'execute if entity @s[tag=bm.gvp] if dimension bm:gutter'
    fn('p132/use', [f'{in_heist} run return run ' + say("In the vault your crew answers the Fixer's Ledger - Raid Crew.", '#9ad0ff'),
                    'execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                    'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                    f'{sel_pet} run tag @s add bm.tusel2',
                    'scoreboard players set #am bm.rng 0',
                    'execute if predicate bm:p20/sneaking run scoreboard players set #am bm.rng 2',
                    'execute if score #am bm.rng matches 0 if entity @e[type=minecraft:wolf,tag=bm.tusel2] run scoreboard players set #am bm.rng 4',
                    'execute if score #am bm.rng matches 2 run function bm:p132/menu', 'execute if score #am bm.rng matches 4 run function bm:p132/recall',
                    'execute if score #am bm.rng matches 0 run function bm:p132/try_summon',
                    'tag @e[tag=bm.tusel2] remove bm.tusel2'])
    fn('p132/recall', ['tp @e[type=minecraft:wolf,tag=bm.tusel2,limit=1] @s', 'data modify entity @e[type=minecraft:wolf,tag=bm.tusel2,limit=1] Sitting set value 0b',
                       'particle minecraft:snowflake ~ ~1 ~ 0.4 0.8 0.4 0.05 30', 'playsound minecraft:block.bell.resonate neutral @a[distance=..16] ~ ~ ~ 0.6 1.2',
                       tusay('Aye, aye. Do not wear it out.')])
    fn('p132/try_summon', ['execute if score @s bm.tucd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.tucd',
                           'execute if score @s bm.tucd matches 1.. run scoreboard players add #m bm.rng 59', 'execute if score @s bm.tucd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                           'execute if score @s bm.tucd matches 1.. run return run ' + title('@s', 'actionbar', [T('Tullius is still thawing out: about ', 'gray'),
                                                                                                              {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                           'execute unless function bm:p132/ok run return run ' + say("Tullius won't come here."),
                           'execute if function bm:p58/full run return 0',
                           'function bm:p132/summon'])
    fn('p132/summon', ['execute positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p132/summon_here',
                       'execute positioned ^ ^1 ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p132/summon_here',
                       'function bm:p132/summon_here'])
    fn('p132/summon_here', [f'summon minecraft:wolf ~ ~ ~ {snbt(pet)}',
                            'data modify entity @e[type=minecraft:wolf,tag=bm.tunew,limit=1,sort=nearest] Owner set from entity @s UUID',
                            f'attribute @e[type=minecraft:wolf,tag=bm.tunew,limit=1,sort=nearest] minecraft:max_health base set {PET_HP}',
                            f'data modify entity @e[type=minecraft:wolf,tag=bm.tunew,limit=1,sort=nearest] Health set value {PET_HP}f',
                            'scoreboard players set @e[type=minecraft:wolf,tag=bm.tunew,limit=1,sort=nearest] bm.tus -1',
                            'scoreboard players set @e[type=minecraft:wolf,tag=bm.tunew,limit=1,sort=nearest] bm.tusl 30',
                            'execute rotated ~180 0 run function bm:p132/rig_here',
                            'scoreboard players operation @e[tag=bm.tunew,distance=..4] bm.pid = @s bm.pid',
                            'execute as @e[type=minecraft:item_display,tag=bm.tunew,distance=..4] run tag @s add bm.tusel', 'function bm:p132/grow',
                            'tag @e[tag=bm.tusel] remove bm.tusel', 'tag @e[tag=bm.tunew,distance=..4] remove bm.tunew',
                            'playsound minecraft:ambient.underwater.exit neutral @a[distance=..20] ~ ~ ~ 1 0.6', 'playsound minecraft:block.bell.use neutral @a[distance=..20] ~ ~ ~ 0.5 0.6',
                            tusay('Captain Tullius, reporting. Try not to get us both killed.')])
    fn('p132/rig_here', rig + ['tp @e[type=minecraft:item_display,tag=bm.tunew,distance=..1] ~ ~ ~ ~ 0'])
    fn('p132/rerig', ['kill @e[type=minecraft:item_display,tag=bm.tusel]', 'execute rotated as @s rotated ~ 0 run function bm:p132/rig_here',
                      'scoreboard players operation @e[type=minecraft:item_display,tag=bm.tunew,distance=..2] bm.pid = #me bm.pid',
                      'tag @e[type=minecraft:item_display,tag=bm.tunew,distance=..2] add bm.tusel', 'tag @e[type=minecraft:item_display,tag=bm.tunew,distance=..2] remove bm.tunew',
                      'function bm:p132/grow', 'scoreboard players set @s bm.tus -1'])
    fn('p132/dismiss', ['execute as @e[type=minecraft:wolf,tag=bm.tusel2] at @s run function bm:p132/fade',
                        'execute as @e[type=minecraft:wolf,tag=bm.tusel2] on passengers run kill @s[type=!minecraft:player]',
                        'execute as @e[type=minecraft:wolf,tag=bm.tusel2] run data remove entity @s Owner',
                        'execute as @e[type=minecraft:wolf,tag=bm.tusel2] run tp @s ~ -500 ~', 'kill @e[type=minecraft:wolf,tag=bm.tusel2]',
                        tusay('Back to the deep, then. You know where to find me.')])
    dlg = lambda out: P28.multi([T("Tullius's Frozen Doubloon", ICE, bold=True)],
                                [P28.body([T('Tullius', ICE, bold=True), T(' - captain of the sunken kingdom\'s guard, drowned and not done yet. Cold, sardonic, ', 'gray'),
                                           T('deadly at sea.', 'white')]),
                                 P28.body([T('The harpoon up close, the blunderbuss a little further, and at range the ', 'gray'), T('harpoon pull', ICE, bold=True),
                                           T(' - and every seventh blow the ', 'gray'), T('Frostbite Broadside', ICE, bold=True),
                                           T('. In the water he hits 40% harder; you swim with him.', 'gray')], 300)],
                                ([P28.btn(T('Sit / follow', 'white', bold=True), MENU + 1, width=150), P28.btn(T('Send him home', 'gray'), MENU + 9, width=150)] if out else
                                 [P28.btn(T('Call for Tullius', ICE, bold=True), MENU + 8, width=150)]) + [P28.btn(T('Wardrobe', ICE, bold=True), MENU + 4, width=150, tooltip=T('His looks - and his aura, if you have it.', 'gray'))], columns=2, exit_label='Close')
    fn('p132/menu', [f'scoreboard players set @s bm.menu {MENU}', 'scoreboard players set #out bm.rng 0',
                     'execute if entity @e[type=minecraft:wolf,tag=bm.tusel2] run scoreboard players set #out bm.rng 1',
                     f'execute if score #out bm.rng matches 1 run return run dialog show @s {snbt(dlg(True))}', f'dialog show @s {snbt(dlg(False))}'])
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {MENU + n} run return run function bm:p132/act' for n in (1, 4, 8, 9)]
    fn('p132/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                    f'execute if score #act bm.pay matches {MENU + 4} run return run function bm:p119/plain/tul',     # (2.78: his wardrobe)
                    'scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add bm.tusel2',
                    f'execute if score #act bm.pay matches {MENU + 8} unless entity @e[type=minecraft:wolf,tag=bm.tusel2] run function bm:p132/try_summon',
                    f'execute if score #act bm.pay matches {MENU + 8} if entity @e[type=minecraft:wolf,tag=bm.tusel2] run function bm:p132/recall',
                    f'execute if score #act bm.pay matches {MENU + 1} if entity @e[type=minecraft:wolf,tag=bm.tusel2] run function bm:p132/sit',
                    f'execute if score #act bm.pay matches {MENU + 9} if entity @e[type=minecraft:wolf,tag=bm.tusel2] run function bm:p132/dismiss',
                    'tag @e[tag=bm.tusel2] remove bm.tusel2'])
    tw = '@e[type=minecraft:wolf,tag=bm.tusel2,limit=1]'
    fn('p132/sit', [f'execute store success score #s0 bm.rng if data entity {tw} {{Sitting:1b}}',
                    f'execute if score #s0 bm.rng matches 1 run data modify entity {tw} Sitting set value 0b',
                    f'execute if score #s0 bm.rng matches 0 run data modify entity {tw} Sitting set value 1b',
                    'execute if score #s0 bm.rng matches 1 run ' + tusay('Weigh anchor, then.'),
                    'execute if score #s0 bm.rng matches 0 run ' + tusay('I will keep watch. Somebody has to.'),
                    f'execute if score #s0 bm.rng matches 0 as {tw} run function bm:p132/sat'])
    fn('p132/sat', face('sneer', 40))
    # ---- his click box (riding him - he isn't ridden): right-click him to sit / stand
    fn('p132/box', ['execute if entity @s[tag=bm.ffpet] run return 0', 'execute if function bm:p132/has_hit run return 0',
                    'summon minecraft:interaction ~ ~ ~ {Tags:["bm.tuhit","bm.tuhnew"],width:0.9f,height:2.3f,response:1b}',
                    'ride @e[type=minecraft:interaction,tag=bm.tuhnew,limit=1,sort=nearest] mount @s', 'tag @e[tag=bm.tuhnew] remove bm.tuhnew'])
    fn('p132/has_hit', ['execute on passengers if entity @s[type=minecraft:interaction,tag=bm.tuhit] run return 1', 'return 0'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.tuhit] unless function bm:p20/frog/has_vehicle run kill @s')
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.tuhit] if data entity @s interaction run function bm:p132/click',
             'execute as @e[type=minecraft:interaction,tag=bm.tuhit] if data entity @s attack run data remove entity @s attack']
    fn('p132/click', ['execute on vehicle run tag @s add bm.tuclk', 'execute on target at @s run function bm:p132/who', 'tag @e[tag=bm.tuclk] remove bm.tuclk',
                      'data remove entity @s interaction'])
    tick.append('scoreboard players remove @a[scores={bm.tucl=1..}] bm.tucl 1')
    cw = '@e[type=minecraft:wolf,tag=bm.tuclk,limit=1]'
    fn('p132/who', ['execute if score @s bm.tucl matches 1.. run return 0', 'scoreboard players set @s bm.tucl 10', 'scoreboard players operation #me bm.pid = @s bm.pid',
                    f'execute unless score {cw} bm.pid = #me bm.pid run return run ' + tusay('I serve one captain at a time. It is not you.'),
                    f'execute store success score #s0 bm.rng if data entity {cw} {{Sitting:1b}}',
                    f'execute if score #s0 bm.rng matches 1 run data modify entity {cw} Sitting set value 0b',
                    f'execute if score #s0 bm.rng matches 0 run data modify entity {cw} Sitting set value 1b',
                    'execute if score #s0 bm.rng matches 1 run ' + tusay('Weigh anchor, then.'),
                    'execute if score #s0 bm.rng matches 0 run ' + tusay('I will keep watch. Somebody has to.'),
                    f'execute if score #s0 bm.rng matches 0 as {cw} run function bm:p132/sat'])
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:interaction,tag=bm.tuhit]')
    # ---- fainting
    tick += ['execute as @e[type=minecraft:item_display,tag=bm.tup_pet,tag=bm.tup_body,tag=!bm.tufade] at @s run function bm:p132/check',
             'scoreboard players remove @e[type=minecraft:item_display,tag=bm.tufade] bm.tul 1',
             'kill @e[type=minecraft:item_display,tag=bm.tufade,scores={bm.tul=..0}]']
    fn('p132/check', ['scoreboard players operation #me bm.pid = @s bm.pid',
                      f'{sel_pet.replace("tag=bm.tupet]", "tag=bm.tupet,distance=..16]")} run return run scoreboard players set @s bm.tuz 0',
                      'scoreboard players add @s bm.tuz 1', 'execute if score @s bm.tuz matches 4.. run function bm:p132/fell'])
    fn('p132/fell', ['function bm:p132/fade', 'execute as @a if score @s bm.pid = #me bm.pid run function bm:p132/cooldown'])
    fn('p132/cooldown', [f'scoreboard players set @s bm.tucd {PET_CD}',
                         tellraw('@s', PREFIX + [T('Tullius goes down. ', ICE, bold=True), T('"...Hah. I have drowned before. Give me a minute." ', ICE_LT),
                                                 T(f'The Doubloon needs {PET_CD // 60} minutes before he can come back.', 'gray')])])
    fn('p132/fade', ['execute as @e[type=minecraft:item_display,tag=bm.tup_pet,tag=!bm.tufade] if score @s bm.pid = #me bm.pid run function bm:p132/fade1',
                     'particle minecraft:snowflake ~ ~1 ~ 0.5 0.8 0.5 0.05 60', 'particle minecraft:splash ~ ~1 ~ 0.5 1 0.5 0.2 60',
                     'particle minecraft:flash{color:[0.6,0.85,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1',
                     'playsound minecraft:ambient.underwater.enter neutral @a[distance=..20] ~ ~ ~ 1 0.8', 'playsound minecraft:block.glass.break neutral @a[distance=..20] ~ ~ ~ 0.6 1.2'])
    fn('p132/fade1', ['tag @s add bm.tufade', 'scoreboard players set @s bm.tul 3',
                      'data merge entity @s[type=minecraft:item_display] {brightness:{block:15,sky:15},Glowing:1b,glow_color_override:9099504}'])
    second.append('scoreboard players remove @a[scores={bm.tucd=1..}] bm.tucd 1')
    G.FUNCS['p62/died'].insert(-1, 'execute as @e[type=minecraft:wolf,tag=bm.tupet] if score @s bm.pid = #me bm.pid at @s run function bm:p132/go')
    fn('p132/go', ['scoreboard players add #gone bm.rng 1', 'function bm:p132/fade', 'execute on passengers run kill @s[type=!minecraft:player]',
                   'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    P73.follow_rules(G, ('tul', 'wolf', 'bm.tupet', 'tul_coin', 'p132/go', 'Tullius', 'bm.tufg', 'p132/summon_here'), second)
    L = G.FUNCS['p73/fol/tul']
    j = next(i for i, l in enumerate(L) if ' if items entity ' in l)
    L.insert(j, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0')
    G.FUNCS['p58/count'][-1:-1] = ['execute as @e[type=minecraft:wolf,tag=bm.tupet] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1']
    G.FUNCS['p57/pulse'] += [l.replace('tag=bm.celipet', 'tag=bm.tupet') for l in G.FUNCS['p57/pulse'] if 'tag=bm.celipet' in l]
    # ---- at sea with him: in the water, you swim as he does (Dolphin's Grace, Conduit Power)
    second.append('execute as @e[type=minecraft:wolf,tag=bm.tupet,tag=!bm.ffpet] at @s run function bm:p132/sec')
    fn('p132/sec', ['execute on owner if entity @s[distance=..14] at @s if block ~ ~1 ~ minecraft:water run function bm:p132/sea'])
    fn('p132/sea', ['effect give @s minecraft:dolphins_grace 4 0 true', 'effect give @s minecraft:conduit_power 12 0 true'])

    # ---- his raid contract (the Recruiter: 2 Gutter Trophies + 5 Medallions)
    def signed():
        return ['scoreboard players operation #q bm.rng = @s bm.fcon', f'scoreboard players set #bit bm.rng {BIT}',
                'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']
    GP = [T('[', 'dark_gray'), T('Heist', '#ffcf40', bold=True), T('] ', 'dark_gray')]
    fn('p132/sign', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                     'execute unless score @s bm.fcon matches 0.. run scoreboard players set @s bm.fcon 0'] + signed() +
       ['execute if score #q bm.rng matches 1 run return run ' + say('Tullius is already under contract.', 'gray'),
        f'scoreboard players add @s bm.fcon {BIT}', 'clear @s *[minecraft:custom_data~{bm:"fcontract_tul"}] 1',
        'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8', 'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.4 1.6',
        tellraw('@s', GP + [T('Signed! ', '#ffcf40', bold=True), T('Tullius', ICE, bold=True), T(' will answer your call in the vault from now on.', 'gray')])])
    fn('p132/ok', ['execute unless dimension bm:gutter run return run function bm:p74/fol_ok', 'execute unless entity @s[tag=bm.gvp] run return 0'] + signed() +
       ['execute if score #q bm.rng matches 1 run return 1',
        tellraw('@s', GP + [T('Tullius', ICE), T(' needs a ', 'gray'), T('Raid Contract', '#ffcf40'), T(' to come into the vault. The Recruiter in the den sells them.', 'gray')]), 'return 0'])
    from gen_dp import offer
    L = G.FUNCS['p70/r/lobby/init']
    k = next(i for i, l in enumerate(L) if l.startswith('summon minecraft:villager') and 'bm.gvrec' in l and 'Recipes:[' in l)
    o = offer(('gutter_trophy', 2), ('fcontract_tul', 1), ('gutter_medallion', 5))
    L[k] = L[k].replace('Recipes:[', 'Recipes:[' + snbt(o) + ',', 1)
    import phase103 as P103
    P103.RECRUITER_OFFERS.append(o)

    # ================================================================== admin
    fn('admin/tullius', [say('Tullius rises in front of you.', ICE), 'execute rotated ~ 0 positioned ^ ^ ^6 rotated ~180 0 run function bm:p132/b/spawn'])
    fn('admin/tullius_ship', ['function bm:p132/ship/build_here', tellraw('@s', PREFIX + [T('A ghost ship is placed here (its deck 4 blocks up); board it and its captain comes.', 'gray')])])
    fn('p132/ship/build_here', [f'execute positioned ~-16 ~-{WL} ~-6 run place template bm:p132_ship'])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/tullius', 'yellow'), T('  Tullius (boss) in front of you', 'gray')]),
                              tellraw('@s', [T('/function bm:admin/tullius_ship', 'yellow'), T('  a ghost ship here (on water: stand at sea level)', 'gray')])]
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.tup]', 'kill @e[type=minecraft:husk,tag=bm.tuboss]', 'bossbar remove bm:tub',
                                       'kill @e[type=minecraft:item_display,tag=bm.tuharp]', 'kill @e[type=minecraft:block_display,tag=bm.tuspike]']
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

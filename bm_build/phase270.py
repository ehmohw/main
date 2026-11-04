"""3.1: THE MIMIC - the 59th follower (mimic_pet_art.py; fol5flag.MIMIC). A vanilla chest with teeth: ChestModel's own boxes, the
game's own chest texture (by its resource path - minecraft:entity/chest/normal, trapped, christmas - never a copy), a creature
fitted inside: gum, coins, two rows of teeth, a fat tongue, two smug gold cat eyes on the lid, four peg feet.

MEETING IT    in a heist's vault, Tier III or higher, one Three Coffers room in forty has a coffer that LOOKS BACK at you: now and
              then a latch clicks somewhere in the row. Pick wrong and open that one, and it isn't the vault's Mimic - it's THE
              Mimic, and it throws a TANTRUM: 30 seconds of hopping and snapping round the room (a bite is 1 heart). Survive it, or
              hand it a Gutter Coin mid-tantrum (it eats it, delighted). It calms down, licks you - and right-clicked, it gives
              you the MIMIC'S KEY (a gold key with a tooth for a bit) and comes along.
ITS WAYS      SNAP LUNGE (a foe within 2.6, every 1.5 s: the lid flung open, a hop, slammed shut on it - 4); DISGUISE (still for 5 s,
              no foe near: feet tucked, eyes shut - just a chest; a monster that walks up to it is ambushed - the snap does double);
              SWALLOW AND SPIT (charged, every 18 s: a foe within 3 swallowed - the lid shuts on it, its cheeks puff, it's gone 2 s
              (parked inside, unseen, unmoving) - then spat out 3 blocks with a burst of coins: 6, and one roll of its loot);
              THE STASH (sneak + right-click: it opens wide, the long tongue out like a welcome mat - reach into its mouth: 27
              slots of your own, kept on the follower (a chest minecart under the floor of its mouth while it's open - its
              host shrunk out of the way so the cart takes the click - its contents saved to you when it shuts) - never a chest block).
EVERYTHING ELSE is every follower's: sitting (right-click: it settles, lid ajar, the lid chattering a coin; then it dozes, lid
nearly shut, snoring), a wardrobe (Trapped Chest and Christmas Chest - drawn on the game's own chest textures - Black Tongue, the
metal latches), a rare aura (the Jackpot), a shiny (Voidbox), the Partner Wheel, a frame (the key becomes a tiny chest that
snaps at whoever right-clicks it - one time in ten, once a day, it spits a Gutter Coin), a display case, Cecil's doll (its own
chibi source, the 'doll' pose), the honours, a Raid Contract; pairs with Bender, Mr. Capshun, Henry and Nia."""
import colorsys
from items import item, T, TOTEM
from useitem import hold
from nbt import snbt
import fol5
import fol5art
import fol5wire as W5
import rigpet as RP
import rigface as RF2
import phase235 as P235
import shiny as SH
from fol5_kit import T as _T

S5 = fol5.SPEC['mimic']
A0 = fol5art.get('mimic')
MA = __import__('mimic_pet_art')
COL, LINE = S5['COL'], S5['LINE']
ITEM = S5['item']
# the game's own chest textures, by resource path (the chest atlas's sprites, added to the block atlas for item models): the plain
# chest, and the two drawn looks (1 Trapped, 2 Christmas). The shiny's Voidbox is painted (the art's recreation, turned violet).
VAN = {None: 'minecraft:entity/chest/normal', 1: 'minecraft:entity/chest/trapped', 2: 'minecraft:entity/chest/christmas'}

item(ITEM, TOTEM, "The Mimic's Key", COL,
     ['A gold key, a tooth for its bit.', 'It is warm, and slightly damp.',
      ('Use: call the Mimic (again: call it over).', 'blue'), ('Sneak + use: its menu.', 'blue'),
      ('Snap, swallow, spit - and a stash in its mouth.', 'blue'), ('If it faints: 2 minutes before it can return.', 'gray'),
      ('"Finders keepers."', 'dark_gray')],
     model=f'bm:{ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)

P = A0.POSES
P['sit_a2'] = dict(P['sit_a'], lid=MA.lid(12))                 # (the lid chatters open on a coin)
P['sit_b2'] = dict(P['sit_b'], lid=MA.lid(5), body=_T(-2, 0, 4))  # (a snore puffs it up)
P['happy'] = dict(P['idle_b'], _face='happy', lid=MA.lid(40), tongue=_T(-16))       # (a lick)
P['land'] = dict(P['walk_1'], lid=MA.lid(4))


class Mimic(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'mimic', 'The Mimic', COL, LINE, 'p270', 'mx', 'wx'
    A = RF2.art(A0)
    MENU, PET_HP, PET_CD, ITEM = 5600, 34, 120, ITEM
    pron, they = 'it', 'it'
    EXPR = RP.Cfg.EXPR + ('disg', 'greedy')
    FACE = dict(A0.FACE_MAP, disg='disg', greedy='greedy')
    ATTRS = dict(armor=6, attack_damage=4, movement_speed=0.33, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.7, W5.hit(A0)
    CYCLE = W5.cycle(A0, (240, [(0, 'idle_a'), (80, 'idle_b'), (100, 'idle_a'), (160, 'idle_c'), (210, 'idle_a')]),
                     (480, [(0, 'sit_a'), (60, 'sit_a2'), (68, 'sit_a'), (160, 'sit_a2'), (168, 'sit_a'), (240, 'sit_b'), (360, 'sit_b2'), (380, 'sit_b')]),
                     (None, [(0, 'happy'), (14, 'idle_a')]),
                     {7: (None, [(0, 'snap_up'), (4, 'snap'), (7, 'land'), (12, 'idle_a')]),
                      12: (None, [(0, 'swallow'), (6, 'gulp'), (46, 'spit'), (54, 'idle_a')])}, wp=8, rp_=6)
    DUR = dict(P235._DUR, walk_0=4, walk_1=4, snap_up=4, snap=3, land=4, swallow=6, gulp=4, spit=3, stash=10, disguise=10, tantrum=4,
               sit_a=10, sit_a2=4, sit_b=20, sit_b2=30, happy=6)
    QUIPS = ['"Finders keepers."', '(its lid lifts a crack - two gold eyes check your pockets - and shuts)', '"Is that a coin? That\'s a coin. Give it."',
             '(somewhere inside it, coins clink as it walks)', '"I am a perfectly ordinary chest."', '(it licks its own latch)']
    HELLO = ('(the Mimic clatters back to you on its little feet)', '(a chest you hadn\'t noticed opens one gold eye) "...oh, it\'s YOU. Hello!"',
             '(it shuts its lid with a click - and is just a chest. Then not even that)')
    SIT = ('"Up! Up! There\'s loot somewhere."', '(it settles, feet tucked, its lid ajar on a coin)')
    FAINT = '"...my... coins..."'
    NOT_YOURS = '(the lid lifts a crack; two gold eyes narrow) "Finders keepers. And you didn\'t find me."'
    POWERS = [('Snap Lunge', 'a foe within 2.6, every 1.5 s: the lid flung open, a hop - and slammed shut on it, 4'),
              ('Disguise', 'still for 5 s, no foe near: feet tucked, eyes shut - just a chest. A monster that walks up to it is ambushed: the snap does double'),
              ('Swallow and Spit', 'charged, every 18 s: a foe within 3 swallowed whole - 2 s inside - then spat out with a burst of coins: 6, and a roll of its loot'),
              ('The Stash', 'sneak + right-click it: it opens wide, its tongue out like a welcome mat - reach into its mouth: 27 slots of your own'),
              ('Finders Keepers', 'it is, at heart, a chest - and it knows what\'s in yours')]
    INTRO = [T('The Mimic', COL, bold=True), T(' - a heist vault\'s chest that looked back, threw a tantrum, and decided it liked you. ', 'gray'),
             T('"Finders keepers."', LINE, italic=True)]
    BURST = ['particle minecraft:wax_on ~ ~0.5 ~ 0.4 0.3 0.4 0 12', 'particle minecraft:item{item:"minecraft:gold_nugget"} ~ ~0.6 ~ 0.3 0.3 0.3 0.1 8']
    FADE_SOUND = 'playsound minecraft:block.chest.close neutral @a[distance=..20] ~ ~ ~ 1 0.8'
    SUMMON_EXTRA = ['playsound minecraft:block.chest.open neutral @a[distance=..24] ~ ~ ~ 0.8 1.0', 'playsound minecraft:entity.item.pickup neutral @a[distance=..24] ~ ~ ~ 0.6 0.6']
    ENC_POSES = [(0, 'idle_a'), (30, 'happy'), (50, 'idle_c'), (66, 'idle_a')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run particle minecraft:wax_on ~ ~0.8 ~ 0.3 0.2 0.3 0 3'
    ADV = ('Finders Keepers', 'Open the wrong coffer in a heist vault - the one that looked back - and live through its tantrum')
    ADMIN_HINT = 'In a Tier III+ heist, a Three Coffers room in forty has the Mimic in it (admin/mimic_vault: this room\'s, now).'
    MEET_HINT = 'Right-click it, once it has calmed down.'


_DOLL = 'A doll of the Mimic - a squat little chest, lid ajar on its teeth, a blep of tongue, two big gold eyes.'
_eff = W5.pair_fx
_PAIRS = {
    'mx_bender': ('mimic', 'bender', 'Fetch', '#e0a860', 'The Mimic and Bender - he drops a stick in its mouth, and it spits it back',
                  _eff(('speed', 0), ('luck', 0)),
                  [('bender', '(drops a stick in its mouth. Waits. Tail going.)'), ('mimic', '(PTOO - the stick, back, slightly chewed) "Again?"')],
                  [('mimic', '(it opens its lid wide)', 'bender', '(drops his stick in, very pleased with himself)')]),
    'mx_capshun': ('mimic', 'capshun', 'Counterfeit', '#f0f0f0', 'The Mimic and Mr. Capshun - he paints it a gold coin, and it spits out a real one',
                   _eff(('luck', 0), ('haste', 0)),
                   [('capshun', '[Mr. Capshun narrates: "He painted a coin. It was eaten at once."]'), ('mimic', '(it spits out a coin. A REAL one.) "...Finders keepers?"')],
                   [('mimic', '(licks the paint off his brush)', 'capshun', '[Mr. Capshun narrates: "That was cadmium yellow. It was not food."]')]),
}
W5.register(Mimic, A0, _DOLL, ('minecraft:wax_on', 'minecraft:block.chest.open', 'minecraft:poof'), _PAIRS, 'the Mimic')
FRAMES = [f'{ITEM}_f0', f'{ITEM}_f1']

# ---- THE TREASURE CHEST (mimic_classic_art, the owner's): an OUTFIT - its first look, the dark oak strongbox with iron straps and
#      brass, back as look 8 of its wardrobe (after its shiny, 7: a world remembers looks by number). A whole-model swap: on the same
#      rig, every swapped part's model mm_<part>... -> mmt_<part>... (its faces too); its doll stays the vanilla chest. Sold, as its others.
import phase99 as _P99  # noqa: E402
import phase138 as _P138  # noqa: E402
from useitem import HOLD as _HOLD  # noqa: E402
MC = __import__('mimic_classic_art')
_ml = _P99.NEW['mimic'][3]
OUTFIT = max(_ml) + 1
assert SH.KEY.get('mimic') == OUTFIT - 1, ('the Mimic\'s looks moved', sorted(_ml), SH.KEY.get('mimic'))
_ml[OUTFIT] = (MC.NAME, ('#24160c', '#5c3a22', '#e8b84a'))
_P99.DYE[MC.NAME] = 'brown'
_P138.HANDMADE.add(('mimic', OUTFIT))           # (phase138 makes no recoloured copies of it: _chests writes its item definitions)
item(f'cos_mimic_{OUTFIT}', TOTEM, f"The Mimic's Outfit: {MC.NAME}", '#c08a24',
     [f'{MC.NAME} - the dark oak strongbox: a barrel lid, iron straps, brass corners and claw feet. For the Mimic alone.',
      ("Use: it's its for good - in its wardrobe.", 'blue'), ('Sneak + use its own item: its menu - Wardrobe.', 'gray')],
     model='minecraft:brown_dye', stack=1, cat='cosmetic', comps=hold('none'))
_HOLD[f'cos_mimic_{OUTFIT}'] = f'bm:p99/use/mimic{OUTFIT}'


def extend_offers(O, offer):
    pass


def generate_early(G):
    RP.contract(Mimic, G)


# ---------------------------------------------------------------------------------------------------- the resource pack
def _void():
    """the shiny's Voidbox sheet: the art's own painted chest (its recreation of the layout - no game pixels) turned violet"""
    im = MA._recreate().convert('RGBA')
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            r2, g2, b2 = colorsys.hls_to_rgb(0.77, min(1, l * 0.8), min(1, s * 1.3 + 0.08))
            px[x, y] = (int(r2 * 255), int(g2 * 255), int(b2 * 255), a)
    return im


A0.SHINY_TEX['mm_chest'] = (lambda im: lambda b: im)(_void())


def _icon(kind='key'):
    """The Mimic's Key - a gold key with a tooth for a bit (and, in a frame, a tiny chest: shut, or snapping open)"""
    from sprites280 import S
    s = S()
    pal = {'g': '#f0c030', 'l': '#ffe070', 'd': '#a87010', 'w': '#fbf4e4', 'k': '#3a2410', 'b': '#8a5a2e', 'p': '#c8904a', 'r': '#6a1220', 'y': '#ffd23a'}
    if kind == 'key':
        s.g(['..lll.....', '.lgddl....', '.gd..g....', '.gd..g....', '.lgddl....', '..ggg.....', '...g......', '...g......', '...gg.....', '...g......', '...gww....', '....w.....'], pal, 4, 2)
    else:
        s.g(['.kkkkkkkk.', '.kppppppk.', '.kbbbbbbk.'] + (['.kwwwwwwk.', '.krrrrrrk.'] if kind == 'open' else []) +
            ['.kppyypk..'[:10], '.kbbbbbbk.', '.kppppppk.', '.kbbbbbbk.', '.kkkkkkkk.'], pal, 3, 4)
    return s.render()


class _ClassicTex:
    @staticmethod
    def textures():
        return {n: im for n, im in MC.R.textures().items() if not n.endswith('_sh')}


def rp(R):
    W5.rp(Mimic, R, _icon(), A0)
    for n, v in MC.R.models().items():           # (the Treasure Chest's models - its shiny set isn't worn: the shiny is a look of its own)
        if not n.endswith('_sh'):
            R.HATS[n] = v
    R.TEXTURE_MODS.append(_ClassicTex)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (MC.PREFIX,)
    R.ICONS[FRAMES[0]] = _icon('shut')
    R.ICONS[FRAMES[1]] = _icon('open')

    def late(R2):
        R2.POST.append(_chests)          # (after every other hook: the recolours, the dolls, the golden dolls - all their models)
    R.POST.append(late)


def _chests(R2):
    """every model wearing the Mimic's chest sheet wears the game's own instead: by resource path, put in the block atlas; the
    copies of the game's sheet the build wrote (the base, and every look that only re-uses it) are removed - the painted shiny stays"""
    import os, re, json, glob
    shk = SH.KEY.get('mimic')
    mdir = R2.p('assets', 'bm', 'models', 'item')
    tdir = R2.p('assets', 'bm', 'textures', 'block')
    pat = re.compile(r'^bm:block/mm_chest(?:_c(\d+))?$')
    used = set()
    for f in glob.glob(os.path.join(mdir, '*.json')):
        m = json.load(open(f))
        tex = m.get('textures', {})
        new = {}
        for k, v in tex.items():
            g = pat.match(str(v))
            if g and not (g.group(1) and int(g.group(1)) == shk):
                n = int(g.group(1)) if g.group(1) else None
                new[k] = VAN.get(n, VAN[None])
                used.add(new[k])
        if new:
            m['textures'] = dict(tex, **new)
            R2.wj(os.path.relpath(f, R2.p()), m)
    for f in glob.glob(os.path.join(tdir, 'mm_chest*.png')):
        g = re.match(r'^mm_chest(?:_c(\d+))?\.png$', os.path.basename(f))
        if g and not (g.group(1) and int(g.group(1)) == shk):
            os.remove(f)
    ap = R2.p('assets', 'minecraft', 'atlases', 'blocks.json')
    cur = json.load(open(ap)) if os.path.exists(ap) else {'sources': []}
    have = {x.get('resource') for x in cur['sources']}
    cur['sources'] += [{'type': 'minecraft:single', 'resource': r} for r in sorted(used) if r not in have]
    R2.wj('assets/minecraft/atlases/blocks.json', cur)
    # (the Treasure Chest: each of its item definitions, look OUTFIT's, its models swapped one for one - a part it hasn't, as it is)
    idir = R2.p('assets', 'bm', 'items')
    have_m = set(MC.R.models())

    def sw(m):
        t = MC.swap(m)
        return t if t in have_m else m

    def walk(o):
        if isinstance(o, dict):
            o = {a: walk(v) for a, v in o.items()}
            if o.get('type') == 'minecraft:model' and str(o.get('model', '')).startswith('bm:item/mm_'):
                o['model'] = 'bm:item/' + sw(o['model'][len('bm:item/'):])
            return o
        return [walk(v) for v in o] if isinstance(o, list) else o
    n_sw = 0
    for f in sorted(glob.glob(os.path.join(idir, 'mm_*.json'))):
        n = os.path.basename(f)[:-5]
        if re.search(r'_c\d+$', n) or not _P138.ITEMS_OF['mimic'](n):
            continue
        d = walk(json.load(open(f)))
        n_sw += 'mmt_' in json.dumps(d)
        R2.wj(f'assets/bm/items/{n}_c{OUTFIT}.json', d)
    assert n_sw >= len(MC.PARTS_SWAPPED), n_sw


def textures():
    return A0.textures()


# ---------------------------------------------------------------------------------------------------- its ways
BIG = 'tag=!bm.boss,type=!minecraft:ender_dragon,type=!minecraft:wither,type=!minecraft:warden,type=!minecraft:elder_guardian,type=!minecraft:ravager'


def _abilities(G, X):
    fn, pfx, foe, S = G.fn, X.pfx, X.foe, X.S
    snd = lambda s, v=0.6, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..16] ~ ~ ~ {v} {p}'
    K = dict(melee=dict(st=7, x=13, at=6, cd=30, reach=2.6, face='serious', go=[snd('block.chest.open', 0.6, 1.4)]),
             charged=dict(st=12, x=56, at=[50, 10], cd=360, r=3, face='greedy', go=[snd('block.chest.open', 1.0, 0.6)]))
    lines = P235.kit(G, X, K)
    G.FUNCS.pop(f'{pfx}/near_owner', None)
    # SNAP LUNGE: 4 (an ambush - a monster walked up to it, disguised: 8)
    fn(f'{pfx}/melee', X.hit(4) + ['execute if entity @s[tag=bm.mxdis] run scoreboard players set #pd bm.rng 8', 'tag @s remove bm.mxdis',
                                   f'execute as @e[{foe},distance=..3.0,sort=nearest,limit=1] at @s run function bm:{pfx}/snapped'] + X.end)
    fn(f'{pfx}/snapped', [f'function bm:{pfx}/hurt', 'particle minecraft:crit ~ ~0.8 ~ 0.3 0.3 0.3 0.2 8', snd('block.chest.close', 1.0, 1.2), snd('entity.evoker_fangs.attack', 0.5, 1.6)])
    # SWALLOW (the first landing): the nearest foe within 3 - not a boss - inside: unseen, unmoving, held at its mouth 2 s
    fn(f'{pfx}/charged', ['tag @s add bm.mxgp', f'execute as @e[{foe},{BIG},distance=..3.4,sort=nearest,limit=1] at @s run function bm:{pfx}/gulped', 'tag @s remove bm.mxgp',
                          snd('entity.generic.eat', 1.0, 0.6)])
    fn(f'{pfx}/gulped', ['tag @s add bm.wxin', 'scoreboard players set @s bm.wxin 60', 'tag @s remove bm.wxnoai',
                         'execute if data entity @s {NoAI:1b} run tag @s add bm.wxnoai', 'data merge entity @s {NoAI:1b}',
                         'effect give @s minecraft:invisibility 3 0 true', 'tp @s @e[type=minecraft:wolf,tag=bm.mxgp,limit=1]', 'particle minecraft:item{item:"minecraft:gold_nugget"} ~ ~0.6 ~ 0.3 0.3 0.3 0.1 10'])
    # SPIT (the second): out 3 blocks ahead, a burst of coins - 6, and a roll of its loot
    fn(f'{pfx}/charged2', X.hit(6) + [f'execute as @e[tag=bm.wxin,distance=..4,limit=1] at @s run function bm:{pfx}/spat',
                                      'particle minecraft:item{item:"minecraft:gold_nugget"} ^ ^0.8 ^0.8 0.3 0.3 0.3 0.25 30', snd('entity.player.burp', 1.0, 0.8)] + X.end)
    fn(f'{pfx}/spat', [f'function bm:{pfx}/release', 'execute at @e[type=minecraft:wolf,tag=bm.mxme,limit=1] positioned ^ ^0.3 ^3 if block ~ ~ ~ #minecraft:air run tp @s ~ ~ ~',
                       'execute at @s run function bm:p270/hurt_here', 'execute at @s run loot spawn ~ ~0.5 ~ kill @s'])
    fn('p270/hurt_here', [f'function bm:{pfx}/hurt'])
    fn(f'{pfx}/release', ['tag @s remove bm.wxin', 'scoreboard players reset @s bm.wxin', 'execute unless entity @s[tag=bm.wxnoai] run data merge entity @s {NoAI:0b}',
                          'tag @s remove bm.wxnoai', 'effect clear @s minecraft:invisibility'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.wxin dummy', 'scoreboard objectives add bm.wxds dummy']
    G.OBJECTIVES += ['bm.wxin', 'bm.wxds']
    X.tick += ['execute as @e[tag=bm.wxin] at @s run function bm:p270/held']
    fn('p270/held', ['scoreboard players remove @s bm.wxin 1', 'execute if score @s bm.wxin matches ..0 run return run function bm:p270/release',
                     'execute unless entity @e[type=minecraft:wolf,tag=bm.mxpet,distance=..6] run return run function bm:p270/release',
                     'execute at @e[type=minecraft:wolf,tag=bm.mxpet,distance=..6,sort=nearest,limit=1] run tp @s ~ ~0.1 ~'])
    # DISGUISE: idle 5 s, no foe within 8, not sitting - feet tucked, eyes shut (its idle poses all the disguise); any move ends it
    X.second.append('execute as @e[type=minecraft:wolf,tag=bm.mxpet] at @s run function bm:p270/still')
    fn('p270/still', [f'execute unless score @s {S("s")} matches 0 run return run function bm:p270/undisg',
                      f'execute if entity @e[{foe},distance=..8] unless entity @s[tag=bm.mxdis] run return run scoreboard players set @s bm.wxds 0',
                      'execute if entity @s[tag=bm.mxdis] run return run function bm:p270/disg_face',
                      'scoreboard players add @s bm.wxds 1',
                      'execute if score @s bm.wxds matches 5.. run function bm:p270/disg'])
    fn('p270/disg', ['tag @s add bm.mxdis', f'scoreboard players set @s {S("fr")} -1', 'function bm:p270/disg_face',
                     snd('block.chest.close', 0.6, 0.9)])
    import phase95 as FX
    fn('p270/disg_face', FX.face_cmd('mimic', 'disg', 30))
    fn('p270/undisg', ['scoreboard players set @s bm.wxds 0', 'execute unless entity @s[tag=bm.mxdis] run return 0', 'tag @s remove bm.mxdis',
                       f'scoreboard players set @s {S("fr")} -1', 'scoreboard players set @s bm.fxt 0'])
    # (an ambush: a monster walks up to it, disguised - the snap, at once)
    X.tick.append(f'execute as @e[type=minecraft:wolf,tag=bm.mxpet,tag=bm.mxdis] at @s if entity @e[{foe},distance=..2.2] run scoreboard players set @s {S("mc")} 0')
    return lines


def _encounter(G, X):
    """in a heist's Three Coffers room (Tier III+, 1 room in 40): the coffer that looks back - a TANTRUM, then a friend"""
    fn, tellraw, title = G.fn, G.tellraw, G.title
    csay = lambda txt: title('@s', 'actionbar', [T('The Mimic: ', COL, bold=True), T(txt, LINE)])
    # (the room, as it's built: its marker - #gt is the heist's tier)
    G.FUNCS['p70/r/init'].insert(0, 'execute if entity @s[tag=bm.gvr_coffers] if score #gt bm.rng matches 3.. run function bm:p270/vault/room')
    fn('p270/vault/room', ['execute store result score #r bm.rng run random value 1..40', 'execute if score #r bm.rng matches 1 run tag @s add bm.wxroom'])
    fn('admin/mimic_vault', ['execute as @e[type=minecraft:marker,tag=bm.gvr_coffers,distance=..40,sort=nearest,limit=1] run tag @s add bm.wxroom',
                             title('@s', 'actionbar', T('This Three Coffers room has the Mimic in it: pick wrong.', COL))])
    # (now and then, somewhere in the row, a latch clicks)
    X.second.append('execute as @e[type=minecraft:marker,tag=bm.wxroom] at @s if entity @a[tag=bm.gvp,distance=..24] run function bm:p270/vault/twitch')
    fn('p270/vault/twitch', ['execute store result score #r bm.rng run random value 1..4', 'execute unless score #r bm.rng matches 1 run return 0',
                             'execute as @e[type=minecraft:interaction,tag=bm.gvprop,distance=..18,sort=random,limit=1] if entity @s[tag=bm.gvcof] at @s run function bm:p270/vault/click',
                             'execute as @e[type=minecraft:interaction,tag=bm.gvprop,distance=..18,sort=random,limit=1] if entity @s[tag=bm.gvshi] at @s run function bm:p270/vault/click'])
    fn('p270/vault/click', ['playsound minecraft:block.chest.close block @a[distance=..16] ~ ~ ~ 0.25 1.9', 'particle minecraft:crit ~ ~0.6 ~ 0.1 0.1 0.1 0 2',
                            'execute as @a[tag=bm.gvp,distance=..16,tag=!bm.wxheard] run function bm:p270/vault/heard'])
    fn('p270/vault/heard', ['tag @s add bm.wxheard', title('@s', 'actionbar', T('(somewhere in the row of coffers, a latch clicks - as if something inside it is looking at you)', 'gray'))])
    # (a wrong pick, in that room: not the vault's Mimic - THE Mimic)
    hook = 'execute if entity @e[type=minecraft:marker,tag=bm.wxroom,distance=..24] if entity @a[tag=bm.gvp,distance=..24,tag=!bm.mxmet] run return run function bm:p270/vault/wake'
    for i in range(4):
        L = G.FUNCS[f'p70/r/coffers/mimic{i}']
        k = max(j for j, l in enumerate(L) if l.startswith('kill ')) + 1
        L.insert(k, hook)
    G.FUNCS['p111/coffers/c/bite'].insert(0, hook)
    fn('p270/vault/wake', ['tag @e[type=minecraft:marker,tag=bm.wxroom,distance=..24] remove bm.wxroom',
                           'execute positioned ~-1.6 ~ ~ run function bm:p270/enc/spawn',
                           'scoreboard players operation @e[type=minecraft:interaction,tag=bm.mxenc,distance=..4] bm.pid = @p[tag=bm.gvp,distance=..24] bm.pid',
                           'scoreboard players set @e[type=minecraft:interaction,tag=bm.mxenc,distance=..4] bm.wxtt 600',
                           'playsound minecraft:block.chest.open hostile @a[distance=..24] ~ ~ ~ 1 0.5', 'playsound minecraft:entity.ravager.roar hostile @a[distance=..24] ~ ~ ~ 0.4 2.0',
                           tellraw('@a[tag=bm.gvp,distance=..24]', [T('The coffer LOOKS BACK at you. ', COL, bold=True),
                                                                   T('Two gold eyes open on its lid - and it throws a TANTRUM. ', LINE),
                                                                   T('(Live through it. Or bribe it: a Gutter Coin.)', 'gray')])])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.wxtt dummy', 'scoreboard objectives add bm.wxday dummy']
    G.OBJECTIVES += ['bm.wxtt', 'bm.wxday']
    # THE TANTRUM (its encounter's box, each tick, while bm.wxtt runs): it hops at you and snaps; a bite is 1 heart
    G.FUNCS['p270/enc/tick'].insert(0, 'execute if score @s bm.wxtt matches 1.. run return run function bm:p270/enc/tantrum')
    fn('p270/enc/tantrum', ['scoreboard players remove @s bm.wxtt 1', 'execute if score @s bm.wxtt matches 0 run return run function bm:p270/enc/calm',
                            'execute as @e[type=minecraft:item_display,tag=bm.mxencp,distance=..6] run tag @s add bm.mxsel',
                            'scoreboard players operation #f bm.rng = @s bm.wxtt', 'scoreboard players operation #f bm.rng %= #20 bm.rng',
                            'execute if score #f bm.rng matches 0 run function bm:p270/pose/tantrum', 'execute if score #f bm.rng matches 10 run function bm:p270/pose/snap_up',
                            'execute if score #f bm.rng matches 0 facing entity @p[distance=..12,gamemode=!spectator] feet rotated ~ 0 run function bm:p270/enc/hop',
                            'execute if score #f bm.rng matches 10 if entity @p[distance=..1.8,gamemode=!spectator] run function bm:p270/enc/bite',
                            'tag @e[tag=bm.mxsel] remove bm.mxsel'])
    fn('p270/enc/hop', ['execute positioned ^ ^ ^0.8 unless block ~ ~ ~ #minecraft:air run return run function bm:p270/place',
                        'execute positioned ^ ^ ^0.8 unless block ~ ~1 ~ #minecraft:air run return run function bm:p270/place',
                        'execute if entity @p[distance=..1.4] run return run function bm:p270/place',
                        'tp @s ^ ^ ^0.8 ~ 0', 'execute at @s run function bm:p270/place', 'playsound minecraft:block.chest.close hostile @a[distance=..16] ~ ~ ~ 0.6 1.3'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #20 bm.rng 20']
    fn('p270/enc/bite', ['playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..16] ~ ~ ~ 0.8 1.6', 'particle minecraft:crit ~ ~0.7 ~ 0.3 0.3 0.3 0.1 6',
                         'damage @p[distance=..1.8,gamemode=!spectator,gamemode=!creative] 2 minecraft:generic'])
    fn('p270/enc/calm', ['execute as @e[type=minecraft:item_display,tag=bm.mxencp,distance=..6] run tag @s add bm.mxsel', 'function bm:p270/pose/happy',
                         'execute facing entity @p[distance=..12] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0', 'execute rotated as @s run function bm:p270/place',
                         'tag @e[tag=bm.mxsel] remove bm.mxsel', 'scoreboard players set @s bm.wxtt 0', 'playsound minecraft:entity.cat.purr neutral @a[distance=..16] ~ ~ ~ 1 1.4',
                         tellraw('@a[distance=..16]', [T('The Mimic: ', COL, bold=True), T('(it stops. It looks at you. Then it LICKS you, a long wet lick, and its lid falls open on a happy grin.)', LINE)])])
    fn('p270/enc/talk', [f'execute unless score @s bm.pid = {X.here} bm.pid run return run ' + csay('"Finders keepers. And you didn\'t find me."'),
                         f'execute if score {X.here} bm.wxtt matches 1.. if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"gutter_coin"}}] run return run function bm:p270/enc/bribe',
                         f'execute if score {X.here} bm.wxtt matches 1.. run return run ' + csay('(SNAP!) (it is in no mood. Not yet.)'),
                         'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.2',
                         tellraw('@s', [T('It coughs up a gold key with a tooth for a bit, and drops it at your feet. ', LINE, italic=True),
                                        T('"Finders keepers," it says. It means you.', 'gray', italic=True)]),
                         'function bm:p270/enc/joined'])
    fn('p270/enc/bribe', ['item modify entity @s weapon.mainhand {type:"minecraft:set_count",count:-1,add:true}',
                          'playsound minecraft:entity.generic.eat player @a[distance=..16] ~ ~ ~ 1 1.2',
                          f'execute as {X.here} at @s run function bm:p270/enc/calm',
                          tellraw('@s', [T('The Mimic: ', COL, bold=True), T('(it snatches the coin and swallows it. It is DELIGHTED.)', LINE)])])
    fn('admin/mimic_meet_here', ['execute positioned ^ ^ ^2 run function bm:p270/enc/spawn',
                                 'scoreboard players operation @e[type=minecraft:interaction,tag=bm.mxenc,distance=..4] bm.pid = @s bm.pid',
                                 'scoreboard players set @e[type=minecraft:interaction,tag=bm.mxenc,distance=..4] bm.wxtt 600'])


def generate(G):
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    csay = lambda txt: title('@s', 'actionbar', [T('The Mimic: ', COL, bold=True), T(txt, LINE)])
    # ---- the frame: the key becomes a tiny chest that snaps at whoever right-clicks it (one in ten, once a day: a Gutter Coin)
    frame = dict(models=[], tick=['execute unless score @s bm.wxft matches 0.. run scoreboard players set @s bm.wxft 0',
                                  'execute if score @s bm.wxft matches 1.. run scoreboard players remove @s bm.wxft 1',
                                  f'execute if score @s bm.wxft matches 0 run data modify entity @s Item.components."minecraft:item_model" set value "bm:{FRAMES[0]}"'],
                 click=[f'data modify entity @s Item.components."minecraft:item_model" set value "bm:{FRAMES[1]}"', 'scoreboard players set @s bm.wxft 1',
                        'playsound minecraft:block.chest.close block @a[distance=..12] ~ ~ ~ 1 1.4', 'playsound minecraft:entity.evoker_fangs.attack block @a[distance=..12] ~ ~ ~ 0.4 1.8',
                        'execute as @p[distance=..7,gamemode=!spectator] at @s run function bm:p270/frame_coin'])
    W5.build(Mimic, G, _abilities, _encounter, frame=frame)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.wxft dummy']
    G.OBJECTIVES.append('bm.wxft')
    fn('p270/frame_coin', ['execute store result score #r bm.rng run random value 1..10', 'execute unless score #r bm.rng matches 1 run return 0',
                           'execute if score @s bm.wxday = #day bm.bm run return 0', 'scoreboard players operation @s bm.wxday = #day bm.bm',
                           give('gutter_coin'), csay('(PTOO - the tiny chest spits out a Gutter Coin)')])
    pfx, ab = Mimic.pfx, Mimic.ab
    # ---- the poses: disguised, any idle pose is the disguise; while its stash is open, any pose is the stash
    W5.poses_for(Mimic, G, ['disguise', 'stash', 'tantrum', 'snap_up', 'happy'])
    for n in [n for n in G.FUNCS if n.startswith(f'{pfx}/pose/')]:
        name = n[len(f'{pfx}/pose/'):]
        if name in ('stash', 'disguise', 'tantrum') or name.startswith('tw'):
            continue
        pre = [f'execute if entity @s[tag=bm.mxst] run return run function bm:{pfx}/pose/stash']
        if name.startswith('idle'):
            pre.append(f'execute if entity @s[tag=bm.mxdis] run return run function bm:{pfx}/pose/disguise')
        G.FUNCS[n] = pre + G.FUNCS[n]
    # ---- THE STASH: sneak + right-click it - wide open, a chest minecart under the floor of its mouth (27 slots, kept on you)
    W_ = G.FUNCS[f'{pfx}/who']
    k = next(i for i, l in enumerate(W_) if 'bm.pid = #me bm.pid run return run' in l)
    W_.insert(k + 1, f'execute if predicate bm:p20/sneaking as @e[type=minecraft:wolf,tag=bm.{ab}clk,limit=1] at @s run return run function bm:p270/stash/open')
    hw, hh = Mimic.HIT
    fn('p270/stash/open', ['execute if entity @s[tag=bm.mxst] run return run function bm:p270/stash/shut',
                           'tag @s add bm.mxst', 'scoreboard players set @s bm.wxst 0', 'tag @s remove bm.mxsw',
                           'execute if data entity @s {Sitting:1b} run tag @s add bm.mxsw', 'data modify entity @s Sitting set value 1b',
                           f'scoreboard players set @s {"bm.wxfr"} -1',
                           'execute on passengers run data merge entity @s[type=minecraft:interaction,tag=bm.mxhit] {width:0.01f,height:0.01f}',
                           'attribute @s minecraft:scale base set 0.1',            # (its host shrunk out of the way: the cart's box, round it, takes the click)
                           'summon minecraft:chest_minecart ~ ~-0.62 ~ {Tags:["bm.mxcart","bm.mxcnew"],NoGravity:1b,Invulnerable:1b,Silent:1b,'
                           'CustomName:{text:"The Mimic\'s Stash",color:"#e8b830"},DisplayOffset:-12}',
                           'scoreboard players operation @e[type=minecraft:chest_minecart,tag=bm.mxcnew,limit=1] bm.pid = @s bm.pid',
                           'execute store result storage bm:tmp mx.p int 1 run scoreboard players get @s bm.pid',
                           'function bm:p270/stash/fill with storage bm:tmp mx', 'tag @e[tag=bm.mxcnew] remove bm.mxcnew',
                           'playsound minecraft:block.chest.open neutral @a[distance=..16] ~ ~ ~ 1 0.8',
                           'execute on owner run ' + csay('(it opens WIDE and lays its tongue out like a welcome mat - reach into its mouth)')])
    fn('p270/stash/fill', ['$execute if data storage bm:mxst p$(p) run data modify entity @e[type=minecraft:chest_minecart,tag=bm.mxcnew,limit=1] Items set from storage bm:mxst p$(p)'])
    X2 = '@e[type=minecraft:chest_minecart,tag=bm.mxcart,distance=..2,sort=nearest,limit=1]'
    fn('p270/stash/shut', ['execute store result storage bm:tmp mx.p int 1 run scoreboard players get @s bm.pid', 'function bm:p270/stash/save with storage bm:tmp mx',
                           f'execute as {X2} at @s run function bm:p270/stash/gone',
                           'tag @s remove bm.mxst', 'execute unless entity @s[tag=bm.mxsw] run data modify entity @s Sitting set value 0b', 'tag @s remove bm.mxsw',
                           f'scoreboard players set @s bm.wxfr -1',
                           f'execute on passengers run data merge entity @s[type=minecraft:interaction,tag=bm.mxhit] {{width:{hw}f,height:{hh}f}}',
                           f'attribute @s minecraft:scale base set {Mimic.SCALE}',
                           'playsound minecraft:block.chest.close neutral @a[distance=..16] ~ ~ ~ 1 0.9'])
    fn('p270/stash/save', [f'$data modify storage bm:mxst p$(p) set from entity {X2} Items'])
    # (shut by itself: you walk off (6 blocks), 60 s go by, it's sent home - or its cart is gone)
    second = G.FUNCS['loop/second']
    second.append('execute as @e[type=minecraft:wolf,tag=bm.mxpet,tag=bm.mxst] at @s run function bm:p270/stash/sec')
    fn('p270/stash/sec', ['scoreboard players add @s bm.wxst 1', 'execute if score @s bm.wxst matches 60.. run return run function bm:p270/stash/shut',
                          'scoreboard players set #far bm.rng 1', 'execute on owner if entity @s[distance=..6] run scoreboard players set #far bm.rng 0',
                          'execute if score #far bm.rng matches 1 run return run function bm:p270/stash/shut',
                          f'execute unless entity {X2} run return run function bm:p270/stash/shut'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.wxst dummy']
    G.OBJECTIVES.append('bm.wxst')
    # (a stash left open when it goes - sent home, fainted, recalled: its cart, alone, saves its contents to you and goes)
    second.append('execute as @e[type=minecraft:chest_minecart,tag=bm.mxcart] at @s unless entity @e[type=minecraft:wolf,tag=bm.mxpet,tag=bm.mxst,distance=..2] run function bm:p270/stash/stray')
    fn('p270/stash/stray', ['execute store result storage bm:tmp mx.p int 1 run scoreboard players get @s bm.pid', 'function bm:p270/stash/keep with storage bm:tmp mx',
                            'function bm:p270/stash/gone'])
    fn('p270/stash/keep', ['$data modify storage bm:mxst p$(p) set from entity @s Items'])
    fn('p270/stash/gone', ['data modify entity @s Items set value []', 'tp @s ~ -400 ~', 'kill @s'])
    G.FUNCS['admin/uninstall'][0:0] = ['execute as @e[type=minecraft:chest_minecart,tag=bm.mxcart] run data modify entity @s Items set value []', 'kill @e[type=minecraft:chest_minecart,tag=bm.mxcart]']
    fn('admin/mimic_reset', ['tag @s remove bm.mxmet', f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]',
                             title('@s', 'actionbar', T('The Mimic has not met you yet.', COL))])

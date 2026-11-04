"""3.1: THE CAIRN - the 57th follower (assembler_pet_art.py draws it; fol5flag.CAIRN). A little spirit that builds itself a body out of
COPIES of the blocks around it - a walking cairn of whatever the land is made of here.

NO GRIEFING  its body is block_display COPIES - pure render. It never sets, breaks, places or moves a real block; the sampler only
             READS; what it flings and the storm it raises are block_displays too, and hurt only monsters.
WHAT IS IT   only its EYES (two big amber eyes on its head block's front) and its HEART (a warm amber light in its chest) are item
             displays of its own (rigpet's rig: fol5art._cairn); its 22 blocks are block_displays riding the same joints, each pose
             solved on the golem's whole skeleton (BLOCKS) - each block's own transform put through the same turn and shift.
THE SAMPLER  (assembler_pet_art.SAMPLER / SLOTMAP) every 5 s, never per tick: 9 fixed probes - the block under it, 3 under it, six on
             a ring of 3 (alternately at foot and ground level) - each one `if block` against a palette tag (#bm:p268_plains, _desert,
             _cave, _nether: about 40 blocks) - at most 36 checks. The palette with the most hits wins (a tie keeps what it has, so
             it doesn't flicker at a biome's edge); the block right under it may also fill its HEAD slot exactly (a podzol head
             on podzol). A new palette is a re-assembly - each block a puff, a new copy, one a tick from the feet up.
ITS WAYS     PEBBLE BONK (a foe within reach: 4); FLING (a foe 2-7 off, every 4 s: a punch - a copy of its fist block flies at it,
             5 and knocked back); BLOCK STORM (charged, every 30 s: arms up, its pebbles lifting - 18 copies of its blocks whirl round
             the foe in a rising vortex for 3 s, 2 every half second to every monster in it, pulled in; then they slam down and fly
             home). Summoned, it ASSEMBLES: its blocks lie tumbled round it, fly in, and snap the last bit into place.
MEETING IT   at dusk, with the Gem of Creativity out, stack five different blocks into a little column (a waystone) on high open
             ground, and crouch beside it: two amber eyes open in the column - it copies itself out of it, and stands beside it. Your
             blocks stay where they are. Right-click it: the WAYSTONE HEART (its summoning item), and it comes along.
EVERYTHING ELSE is every follower's: sitting (right-click: it sits down heavily; sneak + right-click: it settles into a tidy waystone
- by night a faint amber beam above it, shown to you within 64), a wardrobe of whole palettes (Stained Glass, Mossy, Snowcap and
the gold, diamond and netherite blocks; the shiny's Gilded - the land's shape kept), a rare aura (the Orbit), the Partner Wheel, a
frame (a little cairn of the frame's own land), a display case, Cecil's doll, the honours, a Raid Contract; pairs with Bender, Mr.
Capshun, Henry and Nia."""
from items import item, T, TOTEM
from useitem import hold
from nbt import snbt, F, Int, B
import fol5
import fol5art
import fol5wire as W5
import rigpet as RP
import rigface as RF2
import rigfol as RF
import rigkit as RK
import phase235 as P235

S5 = fol5.SPEC['cairn']
A0 = fol5art.get('cairn')
AR = A0.FULL
COL, LINE = S5['COL'], S5['LINE']
ITEM = S5['item']
BLK = [(b[0], b[2], b[3], b[4]) for b in AR.BLOCKS if b[3]]           # (part, centre, size, slot)
ORDER = [b[0] for b in sorted(BLK, key=lambda b: b[1][1] - b[2][1] / 2)]
PAL = ['plains', 'desert', 'cave', 'nether']                          # (sampled: bm.jxpl 0-3)
SLOTS = ('core', 'trim', 'head', 'limb', 'foot', 'fist', 'ore', 'ore2', 'tuft', 'tuft2', 'pebble')
P_ = lambda **kw: kw
PALETTES = {      # palette -> slot -> block state (the vanilla blocks it is a copy of)
    'plains': P_(core='dirt', trim='cobblestone', head='grass_block', limb='oak_log', foot='stone', fist='stone', ore='coal_ore', ore2='iron_ore',
                 tuft='oak_leaves', tuft2='moss_block', pebble='cobblestone'),
    'desert': P_(core='sand', trim='cut_sandstone', head='sandstone', limb='sandstone', foot='smooth_sandstone', fist='chiseled_sandstone', ore='orange_terracotta',
                 ore2='gold_ore', tuft='cactus', tuft2='dead_bush', pebble='sandstone'),
    'cave': P_(core='cobbled_deepslate', trim='deepslate_bricks', head='deepslate', limb='polished_deepslate', foot='tuff', fist='tuff', ore='deepslate_diamond_ore',
               ore2='deepslate_iron_ore', tuft='amethyst_block', tuft2='calcite', pebble='cobbled_deepslate'),
    'nether': P_(core='netherrack', trim='nether_bricks', head='crimson_nylium', limb='blackstone', foot='basalt', fist='blackstone', ore='nether_gold_ore', ore2='magma_block',
                 tuft='shroomlight', tuft2='nether_wart_block', pebble='netherrack'),
    # (the wardrobe's: whole palettes, the sampled land's shape kept)
    'glass': P_(core='light_blue_stained_glass', trim='purple_stained_glass', head='light_blue_stained_glass', limb='magenta_stained_glass', foot='purple_stained_glass',
                fist='pink_stained_glass', ore='yellow_stained_glass', ore2='lime_stained_glass', tuft='cyan_stained_glass', tuft2='pink_stained_glass', pebble='white_stained_glass'),
    'mossy': P_(core='moss_block', trim='mossy_cobblestone', head='mossy_stone_bricks', limb='stripped_oak_log', foot='mossy_cobblestone', fist='mossy_stone_bricks',
                ore='emerald_ore', ore2='copper_ore', tuft='azalea_leaves', tuft2='flowering_azalea_leaves', pebble='mossy_cobblestone'),
    'snow': P_(core='snow_block', trim='packed_ice', head='snow_block', limb='spruce_log', foot='stone', fist='blue_ice', ore='lapis_ore', ore2='diamond_ore',
               tuft='spruce_leaves', tuft2='powder_snow', pebble='ice'),
    'gold': P_(core='gold_block', trim='raw_gold_block', head='gold_block', limb='raw_gold_block', foot='gold_block', fist='gold_block', ore='gold_ore', ore2='nether_gold_ore',
               tuft='gold_block', tuft2='raw_gold_block', pebble='gold_block'),
    'diamond': P_(core='diamond_block', trim='prismarine_bricks', head='diamond_block', limb='prismarine', foot='diamond_block', fist='diamond_block', ore='diamond_ore',
                  ore2='deepslate_diamond_ore', tuft='diamond_block', tuft2='sea_lantern', pebble='diamond_block'),
    'netherite': P_(core='netherite_block', trim='polished_blackstone_bricks', head='netherite_block', limb='ancient_debris', foot='netherite_block', fist='netherite_block',
                    ore='ancient_debris', ore2='crying_obsidian', tuft='crying_obsidian', tuft2='obsidian', pebble='blackstone'),
    'gilded': P_(core='gold_block', trim='raw_gold_block', head='gold_block', limb='raw_gold_block', foot='gold_block', fist='diamond_block', ore='diamond_block',
                 ore2='emerald_block', tuft='diamond_block', tuft2='gold_block', pebble='gold_block'),
}
NAMES = list(PALETTES)                                           # (index: the palette worn, bm.jxpw)
LOOKPAL = {1: 'glass', 2: 'mossy', 3: 'snow', 4: 'gold', 5: 'diamond', 6: 'netherite'}  # (a look -> its palette; the shiny: gilded)
STATE = {'oak_log': 'oak_log[axis=y]', 'spruce_log': 'spruce_log[axis=y]', 'stripped_oak_log': 'stripped_oak_log[axis=y]', 'basalt': 'basalt[axis=y]',
         'oak_leaves': 'oak_leaves[persistent=true]', 'spruce_leaves': 'spruce_leaves[persistent=true]', 'azalea_leaves': 'azalea_leaves[persistent=true]',
         'flowering_azalea_leaves': 'flowering_azalea_leaves[persistent=true]'}
# (the block right under it fills the head exactly when it's one of these, in the palette it is: a podzol head on podzol)
HEAD_EXACT = {'plains': ['grass_block', 'podzol', 'coarse_dirt', 'rooted_dirt', 'moss_block', 'mycelium', 'mossy_cobblestone', 'stone', 'cobblestone'],
              'desert': ['sand', 'red_sand', 'sandstone', 'red_sandstone', 'terracotta'], 'cave': ['deepslate', 'tuff', 'calcite', 'cobbled_deepslate', 'dripstone_block'],
              'nether': ['crimson_nylium', 'warped_nylium', 'netherrack', 'soul_soil', 'blackstone', 'basalt']}
EXACT = sorted({b for v in HEAD_EXACT.values() for b in v})


def _bs(name):
    """a block_display's block_state NBT for a block (its properties, if it has some)"""
    s = STATE.get(name, name)
    if '[' in s:
        nm, props = s[:-1].split('[')
        return '{Name:"minecraft:%s",Properties:{%s}}' % (nm, ','.join(f'{k}:"{v}"' for k, v in (p.split('=') for p in props.split(','))))
    return '{Name:"minecraft:%s"}' % s


item(ITEM, TOTEM, 'The Waystone Heart', COL,
     ['A warm amber light, set in a small grey stone.', 'Hold it up, and the ground nearby hums.',
      ('Use: call the Cairn (again: call it over).', 'blue'), ('Sneak + use: its menu.', 'blue'),
      ('Its body is copied from the land around it - never taken.', 'blue'), ('Fling and the Block Storm.', 'blue'),
      ('If it faints: 2 minutes before it can return.', 'gray')],
     model=f'bm:{ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)


class Cairn(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'cairn', 'The Cairn', COL, LINE, 'p268', 'ax', 'jx'
    A = RF2.art(A0)
    MENU, PET_HP, PET_CD, ITEM = 5900, 40, 120, ITEM
    pron, they = 'it', 'it'
    BODY_PART = 'heart'
    TWEEN = False
    FACE = dict(A0.FACE_MAP, dim='dim')
    EXPR = RP.Cfg.EXPR + ('dim',)
    ATTRS = dict(armor=8, attack_damage=4, movement_speed=0.3, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.85, W5.hit(A0)
    CYCLE = W5.cycle(A0, (240, [(0, 'idle_a'), (80, 'idle_b'), (130, 'idle_a')]), (80, [(0, 'sit_a'), (40, 'sit_a2')]),
                     (None, [(0, 'asm_0'), (1, 'asm_1'), (6, 'asm_2'), (11, 'asm_3')]),
                     {7: (None, [(0, 'fling_up'), (2, 'fling'), (6, 'idle_a')]), 8: (None, [(0, 'fling_up'), (4, 'fling'), (10, 'idle_a')]),
                      12: (None, [(0, 'storm'), (60, 'idle_a')])}, wp=12, rp_=8)
    DUR = dict(P235._DUR, asm_0=0, asm_1=5, asm_2=5, asm_3=2, fling_up=3, fling=2, storm=8, walk_0=6, walk_1=6, sit_a=10, sit_a2=20, sit_b=16, sit_b2=30)
    QUIPS = ['"I am made of here. ...I was made of somewhere else this morning."', '(one of its pebbles drifts off; it catches it and puts it back)',
             '"Do I look like a desert? I FEEL like a desert."', '"Nobody\'s blocks were harmed. I only borrow how they LOOK."',
             '(its eyes blink, slow and amber)', '"A cairn says: someone came this way. Someone did. Me."']
    HELLO = ('(the Cairn stomps back to you, its pebbles bobbing)', '(blocks tumble in from all round, fly together - CLACK - and two amber eyes open) "Here."',
             '(it falls apart into a little heap of light, and is gone)')
    SIT = ('"Up. Heavy. Up."', '(it sits down heavily, legs out, its pebbles circling)')
    FAINT = '"...falling... apart..."'
    NOT_YOURS = '(its amber eyes look you over, slowly) "Not the one who built my waystone."'
    POWERS = [('Pebble Bonk', 'a foe within reach: 4'),
              ('Fling', 'a foe 2-7 off, every 4 s: a punch - a copy of its fist block flies at it, 5 and knocked back'),
              ('Block Storm', 'charged, every 30 s: 18 copies of its blocks whirl round the foe for 3 s - 2 every half second to every monster in it, pulled in'),
              ('Made of Here', 'every 5 s it looks at the ground round it, and its blocks become copies of the land - plains, desert, deep cave or Nether. It never takes a block'),
              ('A Waystone', 'sneak + right-click: it settles into a tidy cairn - by night, a faint amber beam above it for you')]
    INTRO = [T('The Cairn', COL, bold=True), T(' - a waystone that walked. Its body is copies of the land around it; only its eyes and its heart are its own. ', 'gray'),
             T('"I am made of here."', LINE, italic=True)]
    BURST = ['particle minecraft:block{block_state:"minecraft:cobblestone"} ~ ~0.6 ~ 0.4 0.4 0.4 0 16', 'particle minecraft:poof ~ ~0.5 ~ 0.4 0.3 0.4 0.02 8']
    FADE_SOUND = 'playsound minecraft:block.stone.break neutral @a[distance=..20] ~ ~ ~ 1 0.8'
    SUMMON_EXTRA = ['playsound minecraft:block.stone.place neutral @a[distance=..24] ~ ~ ~ 1 0.8', 'playsound minecraft:block.anvil.place neutral @a[distance=..24] ~ ~ ~ 0.3 1.6']
    ENC_POSES = [(0, 'asm_2'), (12, 'idle_a'), (50, 'idle_b')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 12 run particle minecraft:block{block_state:"minecraft:cobblestone"} ~ ~0.5 ~ 0.4 0.3 0.4 0 12'
    ADV = ('Made of Here', 'Build a waystone at dusk with the Gem of Creativity out - and meet what copies itself out of it')
    ADMIN_HINT = 'At dusk, with the Gem out, stack five different blocks into a column on high open ground and crouch beside it.'
    MEET_HINT = 'Right-click it.'


from fol5_kit import T as _T  # noqa: E402
AR.POSES['sit_a2'] = dict(AR.POSES['sit_a'], _o_core=(0, -3.0, 0), _o_peb1=(0, 1.2, 0), _o_peb2=(0, 0.6, 0))      # (seated: a slow breath, a pebble's orbit)
AR.POSES['sit_b2'] = dict(AR.POSES['sit_b'], _face='blink')
AR.POSES['asm_3'] = dict(AR.POSES['idle_a'])                         # (the last 5%: snapped)
_DOLL = 'A doll of the Cairn - a chibi golem of little blocks, two amber eyes, a warm heart.'
_eff = W5.pair_fx
_PAIRS = {
    'ax_bender': ('cairn', 'bender', 'Found It!', '#e0a860', 'The Cairn and Bender - he digs, and it adds what he finds to its orbit',
                  _eff(('speed', 0), ('haste', 0)),
                  [('bender', '(digs a hole. Proudly presents: a pebble.)'), ('cairn', '"...a good pebble. It goes in the orbit."')],
                  [('cairn', '(a new pebble circles its head)', 'bender', '(barks at the pebble. The pebble keeps circling.)')]),
    'ax_capshun': ('cairn', 'capshun', 'Primary Colours', '#f0f0f0', 'The Cairn and Mr. Capshun - he paints over its blocks, red, yellow and blue',
                   _eff(('strength', 0), ('luck', 0)),
                   [('capshun', '[Mr. Capshun narrates: "He painted it red, yellow and blue. It looked like a toy."]'), ('cairn', '"I feel... cheerful."')],
                   [('cairn', '"Paint the next one green."', 'capshun', '[Mr. Capshun narrates: "Green is not a primary colour."]')]),
}
W5.register(Cairn, A0, _DOLL, ('minecraft:poof', 'minecraft:block.stone.place', 'minecraft:poof'), _PAIRS, 'the Cairn')
# (its display case figure and doll: the WHOLE golem, its plains blocks - rigpet's figure is only its eyes and heart)
import phase134 as P134  # noqa: E402
import phase141 as P141  # noqa: E402
_figs0 = P134.figures


def _figures():
    F2 = _figs0()
    F2[ITEM] = (Cairn.NAME, P134._rigkit(RF2.art(AR.R), AR.POSES['idle_a'], AR.R.RIG_SCALE))
    return F2


P134.figures = _figures
_g = {f'bm:as_{p}': g for p, g in AR.DOLL_GROUPS.items()}
P141.DOLL_FROM['doll_cairn'] = (ITEM, dict(A0.DOLL, groups=_g))
FRAMES = [f'{ITEM}_f{i}' for i in range(4)]


def extend_offers(O, offer):
    pass


def generate_early(G):
    RP.contract(Cairn, G)


# ---------------------------------------------------------------------------------------------------- the resource pack
VAN = {'core': 'dirt', 'trim': 'cobblestone', 'head': 'grass_block_side', 'headtop': 'moss_block', 'limb': 'oak_log', 'limbtop': 'oak_log_top', 'foot': 'stone',
       'fist': 'stone', 'ore': 'coal_ore', 'ore2': 'iron_ore', 'tuft': 'azalea_leaves', 'tuft2': 'moss_block', 'pebble': 'cobblestone'}


def _icon(pal=None):
    """The Waystone Heart: a small grey stone, a warm amber light set in it (in a frame: a little cairn of that land)"""
    from sprites280 import S
    s = S()
    if pal is None:
        s.g(['...gggg...', '..gddddg..', '.gdooood..', '.gdoyyod.d', '.gdoyyodd.', '.gdooodd..', '..gddddg..', '...gggg...'],
            {'g': '#9a9aa2', 'd': '#6a6a72', 'o': '#ff9a30', 'y': '#fff0b0'}, 3, 4)
        return s.render()
    c = {'plains': ('#5aa83a', '#8a5a3a', '#8a8a90'), 'desert': ('#e8d098', '#d8b878', '#c8a060'), 'cave': ('#4a4a56', '#3a3a44', '#6a6a74'),
         'nether': ('#a02a2a', '#6a1818', '#3a3038')}[pal]
    s.g(['....hh....', '...hhhh...', '...hoyh...', '..tttttt..', '..cccccc..', '..cccccc..', '.llllllll.', '.l.l..l.l.', 'ffffffffff'],
        {'h': c[0], 'o': '#ff9a30', 'y': '#fff0b0', 't': c[2], 'c': c[1], 'l': c[2], 'f': c[2]}, 3, 5)
    return s.render()


def rp(R):
    W5.rp(Cairn, R, _icon(), A0)
    for i, p in enumerate(PAL):
        R.ICONS[FRAMES[i]] = _icon(p)
    # (the whole golem's models - its figure and doll - textured from the game's own block textures, never copied into the pack)
    names = set(A0.models())
    for name, (tex, els) in AR.R.models().items():
        p = name[len('as_'):]
        if name in names or p not in AR.R.PARTS or '_x' in p or any(name.endswith(b) for b in AR.R._skins):
            continue
        t2 = {k: (f'minecraft:block/{VAN[v.split("/")[-1][3:]]}' if v.split('/')[-1][3:] in VAN else v) for k, v in tex.items()}
        R.HATS[name] = (t2, els)


def textures():
    return A0.textures()


# ---------------------------------------------------------------------------------------------------- its blocks: block_displays on its joints
def _qrot(q, v):
    x, y, z, w = q
    ix, iy, iz, iw = w * v[0] + y * v[2] - z * v[1], w * v[1] + z * v[0] - x * v[2], w * v[2] + x * v[1] - y * v[0], -x * v[0] - y * v[1] - z * v[2]
    return (ix * w + iw * -x + iy * -z - iz * -y, iy * w + iw * -y + iz * -x - ix * -z, iz * w + iw * -z + ix * -y - iy * -x)


def block_pose(pz, dur, sel='bm.axbsel'):
    """a pose on its block_displays: each block's box (centre c, size s, design units) through its part's solved turn q and shift t -
    a block_display draws its block from its corner, so the corner's offset goes through the turn too (scale per axis: the box)"""
    U = AR.R.RIG_SCALE / 16
    xf = RK.solve(AR.PIVOT, AR.PARENT, pz)
    out = []
    for p, c, s, _slot in BLK:
        sel_ = f'@e[type=minecraft:block_display,tag={sel},tag=bm.axb_{p}]'
        if p in pz.get('_hide', ()):
            out.append(f'execute as {sel_} run data merge entity @s {{start_interpolation:0,interpolation_duration:{min(dur, 2)},transformation:{{scale:[0f,0f,0f]}}}}')
            continue
        q, t = xf[p]
        d = RK.D(tuple(c[i] - AR.PIVOT[p][i] for i in range(3)))
        corner = tuple(d[i] * U - s[i] * U / 2 for i in range(3))
        r = _qrot(tuple(q), corner)
        tr = [t[i] * U + r[i] for i in range(3)]
        sc = [s[i] * U for i in range(3)]
        out.append(f'execute as {sel_} run data merge entity @s {{start_interpolation:0,interpolation_duration:{dur},transformation:{{left_rotation:{snbt(RF.qf(q))},'
                   f'translation:[{tr[0]:.4f}f,{tr[1]:.4f}f,{tr[2]:.4f}f],scale:[{sc[0]:.4f}f,{sc[1]:.4f}f,{sc[2]:.4f}f]}}}}')
    return out


def _blocks(G, C):
    fn, pfx, ab, title = G.fn, C.pfx, C.ab, G.title
    U = AR.R.RIG_SCALE / 16
    mine = f'@e[type=minecraft:wolf,tag=bm.{ab}pet]'
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in ('bm.jxpl', 'bm.jxpw', 'bm.jxrs', 'bm.jxsm', 'bm.jxhb', 'bm.jxst')]
    G.OBJECTIVES += ['bm.jxpl', 'bm.jxpw', 'bm.jxrs', 'bm.jxsm', 'bm.jxhb', 'bm.jxst']
    # ---- the block_displays: summoned with its rig (rigpet's rig_here - they take its new tag, so its id) and its encounter's
    blk = lambda p, tags: snbt({'Tags': ['bm.axb', f'bm.axb_{p}'] + tags, 'block_state': {'Name': 'minecraft:stone'}, 'teleport_duration': Int(2), 'view_range': F(1.4),
                                'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0)] * 3, 'scale': [F(0)] * 3}})
    G.FUNCS[f'{pfx}/rig_here'][0:0] = [f'summon minecraft:block_display ~ ~ ~ {blk(p, ["bm.axnew"])}' for p, *_r in BLK]
    G.FUNCS[f'{pfx}/rig_here'].append('tp @e[type=minecraft:block_display,tag=bm.axnew,distance=..1] ~ ~ ~ ~ 0')
    G.FUNCS[f'{pfx}/rerig'].insert(0, 'execute as @e[type=minecraft:block_display,tag=bm.axb] if score @s bm.pid = #me bm.pid run kill @s')
    sp = G.FUNCS[f'{pfx}/enc/spawn']
    sp[1:1] = [f'summon minecraft:block_display ~ ~ ~ {blk(p, ["bm.axencb", "bm.axbsel"])}' for p, *_r in BLK]
    sp.insert(-1, 'tag @e[type=minecraft:block_display,tag=bm.axbsel] remove bm.axbsel')
    k = next(i for i, l in enumerate(sp) if l.startswith(f'execute facing entity @p feet rotated ~ 0 run function bm:{pfx}/place'))
    sp.insert(k, 'execute as @e[type=minecraft:block_display,tag=bm.axencb,distance=..1] run tag @s add bm.axbsel')
    sp.insert(k + 1, f'execute positioned ~ ~ ~ run function bm:{pfx}/skin/all_0')
    G.FUNCS[f'{pfx}/enc/gone'].insert(0, 'kill @e[type=minecraft:block_display,tag=bm.axencb,distance=..8]')
    et = G.FUNCS[f'{pfx}/enc/tick']
    k = next(i for i, l in enumerate(et) if 'tag=bm.axencp,distance=..5' in l)
    et.insert(k + 1, 'tag @e[type=minecraft:block_display,tag=bm.axencb,distance=..5] add bm.axbsel')
    et.append('tag @e[type=minecraft:block_display,tag=bm.axbsel] remove bm.axbsel')
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:block_display,tag=bm.axb]', 'kill @e[type=minecraft:block_display,tag=bm.axfx]']
    # ---- each tick, as its host: its own blocks tagged (bm.axbsel) round its tick; placed with its joints (rigpet's place)
    T_ = G.FUNCS[f'{pfx}/tick']
    T_.insert(1, 'execute as @e[type=minecraft:block_display,tag=bm.axb,tag=!bm.axencb,distance=..6] if score @s bm.pid = #me bm.pid run tag @s add bm.axbsel')
    T_.insert(len(T_) - 1, f'function bm:{pfx}/btick')
    T_.append('tag @e[type=minecraft:block_display,tag=bm.axbsel] remove bm.axbsel')
    PL = G.FUNCS[f'{pfx}/place']
    for p, *_r in BLK:
        x, y, z = AR.PIVOT[p]
        PL.append(f'execute positioned ^{-x * U:.4f} ^{y * U:.4f} ^{-z * U:.4f} run tp @e[type=minecraft:block_display,tag=bm.axbsel,tag=bm.axb_{p}] ~ ~ ~ ~ 0')
    # ---- every pose also moves its blocks
    for name in [n for n in G.FUNCS if n.startswith(f'{pfx}/pose/')]:
        pz = AR.POSES.get(name[len(f'{pfx}/pose/'):])
        if pz is None:
            continue
        G.FUNCS[name] += block_pose(pz, C.DUR.get(name[len(f'{pfx}/pose/'):], 6))
    # ---- the skins: a palette's block on each block display (by #pw, the palette index); all at once (all_<k>) or one a tick (re-assembly)
    for k, nm in enumerate(NAMES):
        P = PALETTES[nm]
        fn(f'{pfx}/skin/all_{k}', [f'execute as @e[type=minecraft:block_display,tag=bm.axbsel,tag=bm.axb_{p}] run data modify entity @s block_state set value {_bs(P[slot])}'
                                   for p, _c, _s, slot in BLK])
        for p, _c, _s, slot in BLK:
            fn(f'{pfx}/skin/{k}/{p}', [f'execute as @e[type=minecraft:block_display,tag=bm.axbsel,tag=bm.axb_{p}] at @s run function bm:{pfx}/skin/put {{b:\'{_bs(P[slot])}\'}}'])
    fn(f'{pfx}/skin/put', ['$data modify entity @s block_state set value $(b)', 'particle minecraft:poof ~ ~0.3 ~ 0.1 0.1 0.1 0.01 2'])
    for i, b in enumerate(EXACT):
        fn(f'{pfx}/skin/head_{i}', [f'execute as @e[type=minecraft:block_display,tag=bm.axbsel,tag=bm.axb_head] run data modify entity @s block_state set value {_bs(b)}'])
    # (btick, as the host: the re-assembly - a block a tick from the feet up; then the exact head)
    fn(f'{pfx}/btick', ['execute unless score @s bm.jxrs matches 0..30 run return 0'] +
       [f'execute if score @s bm.jxrs matches {i} run function bm:{pfx}/skin/step_{i}' for i in range(len(ORDER))] +
       [f'execute if score @s bm.jxrs matches {len(ORDER)} if score @s bm.jxhb matches 0.. if score @s bm.jxpw matches 0..3 run function bm:{pfx}/skin/head',
        'scoreboard players add @s bm.jxrs 1', f'execute if score @s bm.jxrs matches {len(ORDER) + 1}.. run scoreboard players set @s bm.jxrs -1'])
    for i, p in enumerate(ORDER):
        fn(f'{pfx}/skin/step_{i}', [f'execute if score @s bm.jxpw matches {k} run function bm:{pfx}/skin/{k}/{p}' for k in range(len(NAMES))] +
           (['playsound minecraft:block.stone.place neutral @a[distance=..12] ~ ~ ~ 0.3 1.4'] if i % 4 == 0 else []))
    fn(f'{pfx}/skin/head', [f'execute if score @s bm.jxhb matches {i} run function bm:{pfx}/skin/head_{i}' for i in range(len(EXACT))])
    # ---- which palette it wears: the wardrobe's look (a whole palette), the shiny (gilded) - else the land's
    import shiny as SH
    key = SH.KEY.get('cairn', 7)
    fn(f'{pfx}/pal_pick', ['scoreboard players operation #pw bm.rng = @s bm.jxpl', 'execute unless score #pw bm.rng matches 0..3 run scoreboard players set #pw bm.rng 0',
                           'scoreboard players set #lk bm.rng 0', 'execute on owner run scoreboard players operation #lk bm.rng = @s bm.cosax'] +
       [f'execute if score #lk bm.rng matches {lk} run scoreboard players set #pw bm.rng {NAMES.index(nm)}' for lk, nm in LOOKPAL.items()] +
       [f'execute if score #lk bm.rng matches {key} run scoreboard players set #pw bm.rng {NAMES.index("gilded")}',
        'execute unless score @s bm.jxpw = #pw bm.rng run scoreboard players set @s bm.jxrs 0', 'scoreboard players operation @s bm.jxpw = #pw bm.rng'])
    D_ = G.FUNCS[f'{pfx}/dress']
    D_.append(f'execute as {mine} if score @s bm.pid = #me bm.pid run function bm:{pfx}/pal_pick')
    # ---- the sampler: every 5 s (staggered by host), 9 probes against the palette tags - the most hits wins; a tie keeps it
    for nm in PAL:
        G.wjson(f'bm/tags/block/p268_{nm}.json', {'values': [f'minecraft:{b}' for b in AR.SAMPLER[nm]]})
    probes = ['~ ~-1 ~', '~ ~-3 ~', '~3 ~-1 ~', '~1.5 ~ ~2.6', '~-1.5 ~-1 ~2.6', '~-3 ~ ~', '~-1.5 ~-1 ~-2.6', '~1.5 ~ ~-2.6', '~ ~-2 ~']
    lines = [f'scoreboard players set #t{i} bm.rng 0' for i in range(4)]
    for pos in probes:
        for i, nm in enumerate(PAL):
            lines.append(f'execute if block {pos} #bm:p268_{nm} run scoreboard players add #t{i} bm.rng 1')
    lines += ['scoreboard players operation #tb bm.rng = #t0 bm.rng', 'scoreboard players set #tw bm.rng 0']
    for i in (1, 2, 3):
        lines += [f'execute if score #t{i} bm.rng > #tb bm.rng run scoreboard players set #tw bm.rng {i}',
                  f'execute if score #t{i} bm.rng > #tb bm.rng run scoreboard players operation #tb bm.rng = #t{i} bm.rng']
    lines += ['execute if score #tb bm.rng matches 0 run return 0']
    for i in range(4):          # (a tie with what it has: it keeps it)
        lines.append(f'execute if score @s bm.jxpl matches {i} if score #t{i} bm.rng = #tb bm.rng run scoreboard players set #tw bm.rng {i}')
    lines += ['scoreboard players operation @s bm.jxpl = #tw bm.rng', 'scoreboard players set #hb bm.rng -1']
    for i, b in enumerate(EXACT):
        lines.append(f'execute if block ~ ~-1 ~ minecraft:{b} run scoreboard players set #hb bm.rng {i}')
    lines += ['execute unless score @s bm.jxhb = #hb bm.rng run scoreboard players set @s bm.jxrs 0', 'scoreboard players operation @s bm.jxhb = #hb bm.rng',
              f'function bm:{pfx}/pal_pick']
    fn(f'{pfx}/sample', lines)
    G.FUNCS['loop/second'].append(f'execute as {mine} at @s run function bm:{pfx}/sample_q')
    fn(f'{pfx}/sample_q', ['scoreboard players add @s bm.jxsm 1', 'execute if score @s bm.jxsm matches 5.. run function bm:p268/sample_now'])
    fn('p268/sample_now', ['scoreboard players set @s bm.jxsm 0', f'execute unless entity @e[type=minecraft:wolf,tag=bm.hypet,distance=..3] run function bm:{pfx}/sample'])      # (Henry asleep on its head: it doesn't re-skin)
    # ---- left without its host (sent home, fainted, gone): its blocks go, within the second, in a puff of their own dust
    G.FUNCS['loop/second'].append('execute as @e[type=minecraft:block_display,tag=bm.axb,tag=!bm.axencb] at @s run function bm:p268/orphan_q')
    fn('p268/orphan_q', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #al bm.rng 0',
                         f'execute as @e[type=minecraft:wolf,tag=bm.{ab}pet,distance=..8] if score @s bm.pid = #me bm.pid run scoreboard players set #al bm.rng 1',
                         'execute if score #al bm.rng matches 0 run function bm:p268/crumble'])
    fn('p268/crumble', ['particle minecraft:poof ~ ~0.4 ~ 0.2 0.2 0.2 0.02 3', 'kill @s'])
    G.FUNCS[f'{pfx}/fade'].append(f'execute as @e[type=minecraft:block_display,tag=bm.axb] if score @s bm.pid = #me bm.pid at @s run function bm:p268/crumble')
    G.FUNCS['admin/help'].append(G.tellraw('@s', [T('/function bm:admin/cairn_meet_here', 'yellow'), T('  the Cairn\'s waystone check, here (dusk and the Gem not needed)', 'gray')]))


# ---------------------------------------------------------------------------------------------------- its ways
def _abilities(G, X):
    fn, pfx, foe, me = G.fn, X.pfx, X.foe, X.me
    snd = lambda s, v=0.6, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..16] ~ ~ ~ {v} {p}'
    K = dict(melee=dict(st=7, x=8, at=5, cd=20, reach=2.4, face='serious', go=[snd('block.stone.hit', 0.7, 0.8)]),
             ranged=dict(st=8, x=14, at=8, cd=80, near=2.0, far=7, face='serious', go=[snd('entity.iron_golem.attack', 0.6, 1.2)]),
             charged=dict(st=12, x=64, at=60, cd=600, r=6, face='serious', go=[snd('block.stone.break', 1.0, 0.6), snd('entity.warden.sonic_charge', 0.3, 1.8)]))
    lines = P235.kit(G, X, K)
    G.FUNCS.pop(f'{pfx}/near_owner', None)
    P235.melee(G, X, 4, 2.4, ['particle minecraft:block{block_state:"minecraft:cobblestone"} ~ ~0.8 ~ 0.2 0.2 0.2 0 8'], 'minecraft:block.stone.hit')
    # FLING: a copy of its fist block flies at the foe (a block_display - it lands nowhere: it hits, and is gone)
    tgt = f'@e[{foe},distance=..7.5,sort=nearest,limit=1]'
    fb = snbt({'Tags': ['bm.axfx', 'bm.axfl', 'bm.axfn'], 'block_state': {'Name': 'minecraft:stone'}, 'teleport_duration': Int(4),
               'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(-0.16)] * 3, 'scale': [F(0.32)] * 3}})
    fn(f'{pfx}/ranged', X.hit(5) + ['execute positioned ^-0.4 ^0.7 ^0.4 run summon minecraft:block_display ~ ~ ~ ' + fb,
                                    'data modify entity @e[type=minecraft:block_display,tag=bm.axfn,limit=1] block_state set from entity @e[type=minecraft:block_display,tag=bm.axbsel,tag=bm.axb_fistr,limit=1] block_state',
                                    f'execute as @e[type=minecraft:block_display,tag=bm.axfn] at {tgt} run tp @s ~ ~0.6 ~',
                                    'scoreboard players set @e[type=minecraft:block_display,tag=bm.axfn] bm.jxst 6', 'tag @e[tag=bm.axfn] remove bm.axfn',
                                    f'execute as {tgt} at @s run function bm:{pfx}/flung'] + X.end)
    fn(f'{pfx}/flung', [f'function bm:{pfx}/hurt', f'execute facing entity @e[type=minecraft:wolf,tag={me},limit=1] feet rotated ~180 0 if block ^ ^ ^1.4 #bm:grap_pass if block ^ ^1 ^1.4 #bm:grap_pass run tp @s ^ ^ ^1.4',
                        'particle minecraft:block{block_state:"minecraft:cobblestone"} ~ ~0.8 ~ 0.3 0.3 0.3 0 14', snd('block.stone.break', 0.8, 1.2)])
    # BLOCK STORM: a marker at the foe; 18 copies of its blocks whirl round it, rising, 3 s - 2 every 10 ticks to what's inside, pulled in
    fn(f'{pfx}/charged', [])
    G.FUNCS[f'{pfx}/charged_go'].append(f'execute at {tgt} run function bm:{pfx}/storm/start')
    N, STEPS = 18, 20
    sb = lambda i: snbt({'Tags': ['bm.axfx', 'bm.axsb', f'bm.axs{i}', 'bm.axsn'], 'block_state': {'Name': 'minecraft:cobblestone'}, 'teleport_duration': Int(0),
                         'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0)] * 3, 'scale': [F(0)] * 3}})
    parts = [p for p, *_r in BLK]
    fn(f'{pfx}/storm/start', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.axstorm","bm.axfx","bm.axsn"]}'] + [f'summon minecraft:block_display ~ ~ ~ {sb(i)}' for i in range(N)] +
       [f'data modify entity @e[type=minecraft:block_display,tag=bm.axs{i},tag=bm.axsn,limit=1] block_state set from entity @e[type=minecraft:block_display,tag=bm.axbsel,tag=bm.axb_{parts[i % len(parts)]},limit=1] block_state'
        for i in range(N)] +
       ['scoreboard players set @e[tag=bm.axsn] bm.jxst 0', 'scoreboard players operation @e[tag=bm.axsn] bm.pid = #me bm.pid', 'tag @e[tag=bm.axsn] remove bm.axsn',
        'particle minecraft:poof ~ ~0.5 ~ 1 0.3 1 0.05 30'])
    import math
    for st in range(STEPS):
        L = []
        for i in range(N):
            a = math.radians(i * 20 + st * 36); r = 1.2 + (i % 3) * 0.35; y = 0.2 + (i % 6) * 0.25 + st * 0.06; s = 0.28 + (i % 3) * 0.08
            q = (0.0, math.sin(-a / 2), 0.0, math.cos(-a / 2))
            off = _qrot(q, (r - s / 2, 0.0, -s / 2))
            L.append(f'execute as @e[type=minecraft:block_display,tag=bm.axs{i},distance=..0.5] run data merge entity @s {{start_interpolation:0,interpolation_duration:3,'
                     f'transformation:{{left_rotation:[0f,{q[1]:.4f}f,0f,{q[3]:.4f}f],translation:[{off[0]:.4f}f,{y:.4f}f,{off[2]:.4f}f],scale:[{s:.3f}f,{s:.3f}f,{s:.3f}f]}}}}')
        fn(f'{pfx}/storm/s{st}', L)
    X.tick.append('execute as @e[type=minecraft:marker,tag=bm.axstorm] at @s run function bm:p268/storm/tick')
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #3 bm.rng 3', 'scoreboard players set #10 bm.rng 10']
    fn('p268/storm/tick', ['scoreboard players add @s bm.jxst 1', 'scoreboard players operation #c bm.rng = @s bm.jxst', 'scoreboard players operation #c bm.rng %= #3 bm.rng',
                           'scoreboard players operation #s bm.rng = @s bm.jxst', 'scoreboard players operation #s bm.rng /= #3 bm.rng'] +
       [f'execute if score #c bm.rng matches 0 if score #s bm.rng matches {st} run function bm:{pfx}/storm/s{st}' for st in range(STEPS)] +
       ['scoreboard players operation #c bm.rng = @s bm.jxst', 'scoreboard players operation #c bm.rng %= #10 bm.rng',
        'execute if score #c bm.rng matches 0 if score @s bm.jxst matches ..60 run function bm:p268/storm/hit',
        'execute if score @s bm.jxst matches 61 run function bm:p268/storm/slam',
        'execute if score @s bm.jxst matches 66.. run function bm:p268/storm/end'])
    fn('p268/storm/hit', ['scoreboard players operation #me bm.pid = @s bm.pid',
                          f'execute as @e[type=minecraft:wolf,tag=bm.axpet] if score @s bm.pid = #me bm.pid run tag @s add {me}', 'scoreboard players set #pd bm.rng 2',
                          f'execute as @e[{foe},distance=..2.8] at @s run function bm:p268/storm/caught', f'tag @e[tag={me}] remove {me}',
                          'particle minecraft:poof ~ ~1 ~ 1.2 0.6 1.2 0.02 6', 'playsound minecraft:block.stone.hit neutral @a[distance=..16] ~ ~ ~ 0.6 0.8'])
    fn('p268/storm/caught', ['function bm:p268/hurt', 'execute facing entity @e[type=minecraft:marker,tag=bm.axstorm,limit=1,sort=nearest] feet if block ^ ^ ^0.3 #bm:grap_pass run tp @s ^ ^ ^0.3'])
    fn('p268/storm/slam', ['execute as @e[type=minecraft:block_display,tag=bm.axsb,distance=..0.6] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,0f,0f]}}',
                           'particle minecraft:block{block_state:"minecraft:cobblestone"} ~ ~0.2 ~ 1.4 0.1 1.4 0 40', 'playsound minecraft:block.anvil.land neutral @a[distance=..16] ~ ~ ~ 0.5 0.7'])
    fn('p268/storm/end', ['kill @e[type=minecraft:block_display,tag=bm.axsb,distance=..0.6]', 'kill @s'])
    X.tick += ['scoreboard players remove @e[type=minecraft:block_display,tag=bm.axfl] bm.jxst 1', 'kill @e[type=minecraft:block_display,tag=bm.axfl,scores={bm.jxst=..0}]']
    X.second.append('execute as @e[type=minecraft:marker,tag=bm.axstorm] if score @s bm.jxst matches 90.. run kill @s')
    # (a waystone by night: a faint amber beam above it, shown to its owner within 64)
    X.second.append('execute as @e[type=minecraft:wolf,tag=bm.axpet,tag=bm.axsb] if data entity @s {Sitting:1b} at @s if predicate bm:p266/night run function bm:p268/beam')
    G.wjson('bm/predicate/p266/night.json', {'condition': 'minecraft:time_check', 'value': {'min': 13000, 'max': 23000}, 'period': 24000})
    fn('p268/beam', ['execute on owner if entity @s[distance=..64] run particle minecraft:dust{color:[1.0,0.69,0.25],scale:1.6} ~ ~5 ~ 0.05 4 0.05 0 40 force @s'])
    return lines


def _encounter(G, X):
    """the waystone: at dusk, the Gem out, a column of five different blocks beside you, high and open - crouch: it copies itself out"""
    fn, tellraw, title = G.fn, G.tellraw, G.title
    G.FUNCS['loop/second'].append('execute as @a[tag=!bm.axmet,gamemode=!spectator] if score #tod bm.bm matches 11500..13800 if predicate bm:p20/sneaking at @s run function bm:p268/enc/q')
    fn('p268/enc/q', ['execute unless dimension minecraft:overworld run return 0', 'execute if entity @e[type=minecraft:interaction,tag=bm.axenc,distance=..32] run return 0',
                      'execute unless score @s bm.pid matches 1.. run return 0', 'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #hy bm.rng 0',
                      'execute as @e[type=minecraft:wolf,tag=bm.cgpet,distance=..12] if score @s bm.pid = #me bm.pid run scoreboard players set #hy bm.rng 1',
                      'execute if score #hy bm.rng matches 0 run return 0', 'execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return 0',
                      'execute if entity @s[y=-64,dy=127] run return 0', 'function bm:p268/enc/look'])
    fn('admin/cairn_meet_here', ['function bm:p268/enc/look'])
    pair = [(a, b) for a in range(5) for b in range(a + 1, 5)]
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        col = [f'~{dx} ~{y} ~{dz}' for y in range(-1, 4)]
        fn(f'p268/enc/col_{dx}_{dz}'.replace('-', 'm'), [f'execute if block {c} #minecraft:air run return 0' for c in col] +
           [f'execute if blocks {col[a]} {col[a]} {col[b]} all run return 0' for a, b in pair] +
           ['return run function bm:p268/enc/found'])
    fn('p268/enc/look', [f'execute if function bm:p268/enc/col_{dx}_{dz} run return 1'.replace('-', 'm') for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))] + ['return 0'])
    fn('p268/enc/found', ['execute positioned ^ ^ ^1.6 run function bm:p268/enc/spawn',
                          'scoreboard players operation @e[type=minecraft:interaction,tag=bm.axenc,distance=..3] bm.pid = #me bm.pid',
                          'particle minecraft:poof ~ ~1.5 ~ 0.6 1 0.6 0.03 30', 'playsound minecraft:block.stone.break neutral @a[distance=..16] ~ ~ ~ 1 0.6',
                          tellraw('@s', [T('At dusk, two amber eyes open in your waystone. It looks at you - then copies itself out of the column, block by block, ', LINE, italic=True),
                                         T('and stands beside it. Your blocks are just as you left them.', 'gray', italic=True)]), 'return 1'])
    csay = lambda txt: title('@s', 'actionbar', [T('The Cairn: ', COL, bold=True), T(txt, LINE)])
    fn('p268/enc/talk', [f'execute unless score @s bm.pid = {X.here} bm.pid run return run ' + csay('"Not the one who built my waystone."'),
                         f'execute if items entity @s container.* {X.holds(ITEM)} run return run ' + csay('"You have my heart already. Keep it warm."'),
                         f'execute as {X.here} at @s run particle minecraft:end_rod ~ ~1 ~ 0.3 0.4 0.3 0.02 10', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4',
                         tellraw('@s', [T('It opens its chest - its heart is a warm amber light - and breaks off a little of it, set in a stone, for you. ', LINE, italic=True),
                                        T('"I am made of here. Wherever here is. I will come."', LINE)]),
                         'function bm:p268/enc/joined'])


def generate(G):
    fn, title = G.fn, G.title
    frame = dict(models=[], click=['particle minecraft:block{block_state:"minecraft:cobblestone"} ~ ~0.2 ~ 0.2 0.2 0.2 0 10', 'playsound minecraft:block.stone.place block @a[distance=..12] ~ ~ ~ 1 1.2'],
                 tick=['execute unless score @s bm.jxpl matches 0..3 run function bm:p268/frame_sample'])
    W5.build(Cairn, G, _abilities, _encounter, sitb=(120, [(0, 'sit_b'), (60, 'sit_b2')]), frame=frame)
    lines = [f'scoreboard players set @s bm.jxpl 0']
    for i, nm in enumerate(PAL):
        if i:
            lines.append(f'execute if block ~ ~-1 ~ #bm:p268_{nm} run scoreboard players set @s bm.jxpl {i}')
            lines.append(f'execute if block ~ ~-2 ~ #bm:p268_{nm} run scoreboard players set @s bm.jxpl {i}')
    lines += [f'execute if score @s bm.jxpl matches {i} run data modify entity @s Item.components."minecraft:item_model" set value "bm:{FRAMES[i]}"' for i in range(4)]
    fn('p268/frame_sample', lines)
    _blocks(G, Cairn)
    fn('admin/cairn_reset', ['tag @s remove bm.axmet', f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]',
                             title('@s', 'actionbar', T('The Cairn has not met you yet: a waystone at dusk, the Gem out.', COL))])

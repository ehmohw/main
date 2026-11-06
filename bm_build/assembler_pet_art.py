"""(3.1 draft, stage 1: art only - not wired) THE ASSEMBLER - proposed name: THE CAIRN. A little spirit that builds itself a body out
of COPIES of the blocks around it - a walking cairn of whatever the land is made of here - and rebuilds it as the land changes.

NO GRIEFING: its body is block_display COPIES (block states read from the world, never taken from it). It never breaks, places,
moves or changes a real block - the sampler only READS blocks (see SAMPLER and the design doc).

LOOK  Knee-to-hip high (~1.1 blocks), a chunky little golem of 22 stacked, slightly-misaligned blocks: two block feet and legs, a
      trim-block belt, a big core block torso with two ore chips set in it, trim-block shoulders, limb-block arms with core-block
      fists, a head block with a trim brow on it and a biome TUFT on top (grass and a leaf tuft, a cactus sprout, an amethyst
      cluster, a shroomlight and wart). Three pebble blocks orbit it - not quite all assembled. The only parts that are really
      IT: its HEART, a small warm amber light set in its chest, and its EYES - two faceted amber gems inlaid in the head
      block's front. Everything else is the land.
SLOTS (what each block is a copy of - the sampler fills them): core (torso, fists), trim (belt, shoulders, brow), head (the head
      block: its side and top), limb (legs, arms), foot, ore (the two chips), tuft (the top piece), pebble.
SKINS one per biome, the real vanilla textures: '' PLAINS (grass head, dirt, cobblestone, oak), '_des' DESERT (sandstone, sand,
      cut sandstone, a cactus), '_cave' DEEPSLATE CAVE (deepslate, cobbled deepslate, deepslate bricks, ores, amethyst), '_neth'
      NETHER (crimson nylium, netherrack, nether bricks, blackstone, magma and gold ore, a shroomlight). The shiny ('_sh',
      "Gilded"): gold blocks, raw gold, a diamond-block heart; the cosmetic '_glass' "Stained Glass" (tinted glass blocks)."""
import math
import random
from PIL import Image
from fol5_kit import Rig, hexc, mix, limb, T, cells, soft, glow, eye, alpha, recolor, gem, brow_stone, put

VAN = '/home/claude/mc263/client/assets/minecraft/textures/block'
GRASS, FOLIAGE = '#91bd59', '#77ab2f'


def vtex(name, tint=None):
    """a vanilla block texture (16 x 16; an animated strip cropped to its first frame), tinted as the game tints it"""
    im = Image.open(f'{VAN}/{name}.png').convert('RGBA')
    if im.height > im.width: im = im.crop((0, 0, im.width, im.width))
    if tint:
        t = hexc(tint); px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                px[x, y] = (r * t[0] // 255, g * t[1] // 255, b * t[2] // 255, a)
    return im


# the biomes: slot -> vanilla texture (and its tint)
BIOMES = {
    '': dict(core=('dirt',), trim=('cobblestone',), head=('grass_block_side',), headtop=('grass_block_top', GRASS), limb=('oak_log',),
             limbtop=('oak_log_top',), foot=('stone',), fist=('stone',), ore=('coal_ore',), ore2=('iron_ore',), tuft=('oak_leaves', FOLIAGE),
             tuft2=('moss_block',), pebble=('cobblestone',)),
    '_des': dict(core=('sand',), trim=('cut_sandstone',), head=('sandstone',), headtop=('sandstone_top',), limb=('sandstone',),
                 limbtop=('sandstone_top',), foot=('sandstone_top',), fist=('chiseled_sandstone',), ore=('orange_terracotta',),
                 ore2=('gold_ore',), tuft=('cactus_side',), tuft2=('cactus_top',), pebble=('sandstone',)),
    '_cave': dict(core=('cobbled_deepslate',), trim=('deepslate_bricks',), head=('deepslate',), headtop=('deepslate_top',),
                  limb=('polished_deepslate',), limbtop=('polished_deepslate',), foot=('tuff',), fist=('tuff',), ore=('deepslate_diamond_ore',),
                  ore2=('deepslate_iron_ore',), tuft=('amethyst_block',), tuft2=('calcite',), pebble=('cobbled_deepslate',)),
    '_neth': dict(core=('netherrack',), trim=('nether_bricks',), head=('crimson_nylium_side',), headtop=('crimson_nylium',),
                  limb=('blackstone',), limbtop=('blackstone_top',), foot=('basalt_side',), fist=('blackstone',), ore=('nether_gold_ore',),
                  ore2=('magma',), tuft=('shroomlight',), tuft2=('nether_wart_block',), pebble=('netherrack',)),
    '_sh': dict(core=('gold_block',), trim=('raw_gold_block',), head=('gold_block',), headtop=('gold_block',), limb=('raw_gold_block',),
                limbtop=('raw_gold_block',), foot=('gold_block',), fist=('diamond_block',), ore=('diamond_block',), ore2=('emerald_block',),
                tuft=('diamond_block',), tuft2=('gold_block',), pebble=('gold_block',)),
    '_glass': dict(core=('light_blue_stained_glass',), trim=('purple_stained_glass',), head=('light_blue_stained_glass',),
                   headtop=('light_blue_stained_glass',), limb=('magenta_stained_glass',), limbtop=('magenta_stained_glass',),
                   foot=('purple_stained_glass',), fist=('pink_stained_glass',), ore=('yellow_stained_glass',), ore2=('lime_stained_glass',),
                   tuft=('cyan_stained_glass',), tuft2=('pink_stained_glass',), pebble=('white_stained_glass',)),
}
SKIN_NAMES = {'': 'PLAINS', '_des': 'DESERT', '_cave': 'DEEPSLATE CAVE', '_neth': 'NETHER', '_sh': 'SHINY: Gilded', '_glass': 'cosmetic: Stained Glass'}
GLOWS = {'': (), '_des': (), '_cave': ('tuft',), '_neth': ('tuft', 'ore2'), '_sh': (), '_glass': ()}

# ---- the blocks: (part, parent, centre, size, slot, top-slot or None) in design units (feet on y=0, facing -z, its right +x)
BLOCKS = [
    ('core', None, (0, 8.0, 0), None, None, None),                                    # (the root: a bare joint at the hips)
    ('footr', 'legr', (2.4, 0.9, -0.6), (4.0, 1.8, 5.0), 'foot', None),
    ('footl', 'legl', (-2.4, 0.9, -0.6), (4.0, 1.8, 5.0), 'foot', None),
    ('legr', 'core', (2.4, 4.4, 0), (3.2, 5.2, 3.2), 'limb', 'limbtop'),
    ('legl', 'core', (-2.4, 4.4, 0), (3.2, 5.2, 3.2), 'limb', 'limbtop'),
    ('belt', 'core', (0, 7.9, 0), (9.4, 2.0, 6.4), 'trim', None),
    ('torso', 'core', (0, 12.4, 0), (10.0, 7.0, 7.0), 'core', None),
    ('oreA', 'torso', (3.0, 14.2, -3.55), (2.4, 2.4, 0.6), 'ore', None),
    ('oreB', 'torso', (-3.4, 10.6, -3.55), (2.0, 2.0, 0.6), 'ore2', None),
    ('shr', 'torso', (6.2, 15.0, 0), (4.2, 3.4, 4.6), 'trim', None),
    ('shl', 'torso', (-6.2, 15.0, 0), (4.2, 3.4, 4.6), 'trim', None),
    ('armr', 'shr', (6.6, 11.2, 0), (3.0, 5.0, 3.0), 'limb', 'limbtop'),
    ('arml', 'shl', (-6.6, 11.2, 0), (3.0, 5.0, 3.0), 'limb', 'limbtop'),
    ('fistr', 'armr', (6.8, 7.0, -0.3), (4.0, 3.8, 4.0), 'fist', None),
    ('fistl', 'arml', (-6.8, 7.0, -0.3), (4.0, 3.8, 4.0), 'fist', None),
    ('head', 'torso', (0, 19.6, -0.4), (7.4, 6.2, 6.6), 'head', 'headtop'),
    ('neck', 'torso', (0, 16.2, 0), (4.4, 0.8, 4.0), 'trim', None),
    ('brow', 'head', (0, 23.0, -0.4), (8.0, 0.8, 7.2), 'trim', None),
    ('tuft', 'head', (1.4, 24.6, 0.4), (3.0, 2.6, 3.0), 'tuft', None),
    ('tuft2', 'head', (-1.6, 24.0, 1.0), (2.0, 1.6, 2.0), 'tuft2', None),
    ('peb1', 'core', (8.8, 18.6, 3.0), (1.6, 1.6, 1.6), 'pebble', None),
    ('peb2', 'core', (-9.2, 13.0, -2.6), (1.4, 1.4, 1.4), 'pebble', None),
    ('peb3', 'core', (3.6, 27.4, -2.0), (1.2, 1.2, 1.2), 'pebble', None),
]
EXTRA = {'heart': ('torso', (0, 12.6, -3.6)), 'fling': ('core', (0, 12, -14)), 'storm': ('core', (0, 10, -16))}
PIVOT = {b[0]: b[2] for b in BLOCKS}
PARENT = {b[0]: b[1] for b in BLOCKS}
for k, (par, pv) in EXTRA.items(): PIVOT[k] = pv; PARENT[k] = par
FACES = ('happy', 'blink', 'focus', 'hurt', 'sleepy', 'dim')
R = Rig('cn_', 0.8, PIVOT, PARENT, FACES, face_part='head', opt=('fling', 'storm'))      # (3.1a: was 'as_' - Ashur's prefix: the Cairn's head, arms and legs overwrote hers)
BLOCK_PARTS = tuple(b[0] for b in BLOCKS if b[3])

# ---- textures: the slots per biome (vanilla), the heart, the eyes
EYES = (3.0, 1.2, 7.4, 4.2)        # (the eyes' plate on the head's front: x0..x1 is the head's width; y from 1.2 up, 4.2 tall)


# (the eye art pass: its OWN eyes - two faceted AMBER GEMS inlaid in the head block, lit from within like its heart, each in a dark
#  stone setting; its expressions are the BROW-STONES over them moving (and a cheek-stone pushing up when it's pleased, the stones
#  closing over the gems when it blinks). The gems are the eye overlay (lit); the stones are a face plate behind it (unlit).)
GEM_C, GEM_CY, GEM_W, GEM_H = (8, 22), 11, 8, 8
AMBER = ('#6a2a00', '#b05a08', '#e8901a', '#ffc040', '#ffe890')
AMBER_DIM = ('#3a1600', '#5e2a04', '#8a4610', '#b06a1e', '#c8883a')
_BROW = {None: (2, 0.0), 'happy': (1, -0.6), 'focus': (4, 2.2), 'hurt': (2, -2.0), 'sleepy': (6, 0.0), 'blink': (6, 0.0)}


def _brow_rows(kind, i, im=None):
    """the brow-stone over gem i (0: the sheet's left): its {column: first row below it} (drawn on im when given)"""
    y, tilt = _BROW.get(kind, _BROW[None])
    cx = GEM_C[i]
    tilt = tilt if i == 0 else -tilt                                   # (mirrored: + lowers the end toward the nose)
    tgt = im if im is not None else Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    return brow_stone(tgt, cx - 6, cx + 5, y, tilt, 3 if kind != 'blink' else 5, seam=(kind == 'blink'))


def _brows(kind):
    """the face plate behind the gems: the brow-stones (and the cheek-stones, the shut stones), unlit, in plain stone"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    if kind == 'dim': return im
    for i, cx in enumerate(GEM_C):
        _brow_rows(kind, i, im)
        if kind == 'blink': brow_stone(im, cx - 6, cx + 5, 11, 0.0, 4)       # (two stones shut over the gem)
        if kind == 'happy': brow_stone(im, cx - 5, cx + 4, GEM_CY + 1, 0.0 if i else 0.0, 3, seam=False)   # (a cheek-stone, pushed up)
    return im


def _eyes(kind):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    if kind == 'dim': return im
    for i, cx in enumerate(GEM_C):
        if kind == 'blink':                                            # (shut: only a thread of the light between the stones)
            for x in range(cx - 3, cx + 3): put(im, x, 11, AMBER[3] if abs(x + 0.5 - cx) < 2 else AMBER[2])
            continue
        top = _brow_rows(kind, i)
        dim = kind in ('sleepy', 'hurt')
        gem(im, cx, GEM_CY, GEM_W, GEM_H, ramp=AMBER_DIM if dim else AMBER, core='#ffd890' if dim else '#fffbe8',
            cut_top=lambda x, t=top: t.get(x, -99), cut_bot=(lambda x: GEM_CY + 1) if kind == 'happy' else None,
            crack='#2a1000' if kind == 'hurt' else None, star=(kind == 'happy' and i == 0))
    return im


def _slot_textures(b):
    out = {}
    for slot, spec in BIOMES[b].items():
        try: out[slot] = vtex(spec[0], spec[1] if len(spec) > 1 else None)
        except FileNotFoundError: out[slot] = vtex('stone')
    return out


BASE = _slot_textures('')
for k, v in BASE.items(): R.tex(k, v)
for b in BIOMES:
    if not b: continue
    for k, v in _slot_textures(b).items(): R.tex(k + b, v)
    R.skin(b, {k: k + b for k in BASE})
R.tex('heart', soft('#ffb040', '#fff0b0', '#e07a10', 51, 0.25)); R.tex('heartglow', glow(('#fff4c0', '#ffc860', '#ff9a30', '#ff9a30'), 16, alpha=(220, 160, 80, 0)))
R.tex('eyes', _eyes(None)); R.tex('face', _brows(None))
for f in FACES: R.tex(f'eyes_{f}', _eyes(f)); R.tex(f'face_{f}', _brows(f))

# ---- the model: one stretched block per part (as a scaled block_display: the whole texture on each face); a top face where the
#      block has one; the heart; the eyes on the head's front
for part, par, c, s, slot, top in BLOCKS:
    if not s: continue
    fr = tuple(c[i] - s[i] / 2 for i in range(3)); to = tuple(c[i] + s[i] / 2 for i in range(3))
    e = R.box(part, fr, to, slot, full=True, light=0)
    if top:
        for f in ('up', 'down'): e['faces'][f]['texture'] = '#' + top
hx, hy, hz = PIVOT['head']; hs = dict((b[0], b[3]) for b in BLOCKS)['head']
fz = hz - hs[2] / 2
R.box('head', (hx - hs[0] / 2, hy - hs[1] / 2 + 0.6, fz - 0.04), (hx + hs[0] / 2, hy - hs[1] / 2 + 0.6 + 4.6, fz - 0.02), 'EYES',
      faces=('north',), uv={'north': [0, 0, 7.4, 4.6]}, light=12)
R.box('head', (hx - hs[0] / 2, hy - hs[1] / 2 + 0.6, fz - 0.014), (hx + hs[0] / 2, hy - hs[1] / 2 + 0.6 + 4.6, fz - 0.007), 'FACE',
      faces=('north',), uv={'north': [0, 0, 7.4, 4.6]})                  # (the brow-stones: unlit, behind the gems)
R.box('heart', (-1.2, 11.4, -3.75), (1.2, 13.8, -3.4), 'heart', light=14)
R.box('heart', (-2.2, 10.4, -3.8), (2.2, 14.8, -3.78), 'heartglow', faces=('north',), full=True, light=12)
# ---- fx: a flung block (its fist's copy, flying), the BLOCK STORM (a vortex of copies round a foe)
R.box('fling', (-2.0, 10.0, -16.0), (2.0, 14.0, -12.0), 'fist', full=True, rot=('y', 30, (0, 12, -14)))
R.box('fling', (-2.8, 11.4, -11.6), (2.8, 12.6, -7.0), 'heartglow', faces=('up', 'down'), full=True, light=8)
rs = random.Random(4)
for i in range(18):
    a = math.radians(i * 41); r = 5.0 + (i % 4) * 1.4; y = 2 + i * 1.2
    x, z = r * math.cos(a), -16 + r * math.sin(a); s = 1.6 + (i % 3) * 0.6
    slot = ('core', 'trim', 'limb', 'pebble', 'head', 'ore')[i % 6]
    R.box('storm', (x - s / 2, y - s / 2, z - s / 2), (x + s / 2, y + s / 2, z + s / 2), slot, full=True,
          rot=((rs.uniform(-40, 40), rs.uniform(-40, 40), rs.uniform(-40, 40)), (x, y, z)))

# ---------------------------------------------------------------------------------------------------- poses
def P(lift=0.0, **kw):
    return R.ground(kw, lift)


def scatter(t, seed=7, faint=False):
    """the blocks between the ground and their places: t = 0 all of them lying about on the ground around it (fallen apart),
    1 assembled. Offsets ease out (they fly in fast and SNAP the last bit). A part's offset rides on its parent's, so each
    part's own offset is its target less its ancestors'; only blocks with no children tumble (a parent's turn would swing its
    children about)"""
    rr = random.Random(seed); want = {}; rot = {}
    k = 1 - (1 - t) ** 0.5 if not faint else t
    kids = {b[1] for b in BLOCKS}
    for part, par, c, s, slot, top in BLOCKS:
        if not s: continue
        a = rr.uniform(0, 6.28); d = rr.uniform(7.0, 15.0)
        gx, gz = c[0] * 0.6 + d * math.cos(a), c[2] * 0.6 + d * math.sin(a)
        off = (gx - c[0], s[1] / 2 + rr.uniform(0, 0.3) - c[1], gz - c[2])
        lift = 10.0 * math.sin(math.pi * k) * (0.5 + 0.5 * rr.random()) if 0 < t < 1 else 0.0
        want[part] = tuple(off[i] * (1 - k) + (lift if i == 1 else 0.0) for i in range(3))
        if t < 1 and part not in kids:
            rot[part] = T(rr.uniform(-60, 60) * (1 - k), rr.uniform(-90, 90) * (1 - k), rr.uniform(-60, 60) * (1 - k))
    out = {}
    for part in want:
        own = [want[part][i] for i in range(3)]
        q = PARENT[part]
        if q in want:                                   # (the parent already carries its own target: offset from there)
            own = [want[part][i] - want[q][i] for i in range(3)]
        out[f'_o_{part}'] = tuple(round(v, 3) for v in own)
    out.update(rot)
    return out


POSES = R.POSES
POSES.update({
    'idle_a': P(head=T(0, 0, 4), _o_peb1=(0, 0.5, 0)),
    'idle_b': P(_face='happy', head=T(-6, 10, -4), armr=limb(1, 0, 20), arml=limb(-1, 0, 20), _o_peb2=(0, 1.0, 0)),
    'walk_0': P(legr=limb(1, 22), legl=limb(-1, -22), shr=limb(1, -20), shl=limb(-1, 20), core=T(0, 6, 4), head=T(0, -4)),
    'walk_1': P(legr=limb(1, -22), legl=limb(-1, 22), shr=limb(1, 20), shl=limb(-1, -20), core=T(0, -6, -4), head=T(0, 4)),
    'sit_a': P(_face='happy', _o_core=(0, -3.4, 0), legr=limb(1, 80, 6), legl=limb(-1, 80, 6), shr=limb(1, 20, 6), shl=limb(-1, 20, 6)),
    # sneak-sit: it settles into a tidy cairn (blocks stacked, eyes shut) - a waystone
    'sit_b': P(_face='sleepy', _o_core=(0, -4.2, 0), legr=limb(1, 90), legl=limb(-1, 90), shr=limb(1, 0, -10), shl=limb(-1, 0, -10),
               _o_shr=(-1.2, -1.4, 0), _o_shl=(1.2, -1.4, 0), head=T(10)),
    # ASSEMBLY (the summon / re-form): blocks fly in from the ground ... and snap together
    'asm_0': P(_face='dim', **scatter(0.0)), 'asm_1': P(_face='blink', **scatter(0.45)), 'asm_2': P(_face='focus', **scatter(0.85)),
    # FAINT: it falls apart into a pile, the eyes gone dark; the heart lies glowing in it
    'faint': P(_face='dim', **scatter(0.0, seed=11, faint=True)),
    # FLING: a punch - and a copy of its fist flies off at the foe
    'fling_up': P(_face='focus', shr=limb(1, -40, 30), armr=limb(1, -30), core=T(-6, -20)),
    'fling': P(_face='focus', _show=('fling',), shr=limb(1, 100, 0), armr=limb(1, 10), core=T(12, 24)),
    # BLOCK STORM (its big move): arms up, its own blocks loosening - a vortex of copies whirls round the foe
    'storm': P(_face='focus', _show=('storm',), shr=limb(1, 0, 150), shl=limb(-1, 0, 150), head=T(-12),
               _o_peb1=(2, 4, 0), _o_peb2=(-2, 5, 0), _o_peb3=(0, 4, 0), _o_brow=(0, 0.8, 0), _o_tuft=(0.4, 1.4, 0)),
    'hurt': P(_face='hurt', core=T(-12, 0, 8), head=T(-8), _o_oreA=(0.8, 0.4, -0.6), _o_peb3=(2, -3, 0)),
})
R.DRAFT = ['idle_a', 'idle_b', 'walk_0', 'sit_a', 'sit_b', 'asm_0', 'asm_1', 'asm_2', 'faint', 'fling_up', 'fling', 'storm', 'hurt']
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'head': 'head', 'brow': 'head', 'tuft': 'head', 'tuft2': 'head', 'peb3': 'head', 'legr': 'legs', 'legl': 'legs', 'footr': 'legs', 'footl': 'legs'}
SHINY = 'Shiny Gilded (gold blocks, raw gold, diamond fists)'

# ---------------------------------------------------------------------------------------------------- the sampler (proposal)
# A cheap palette check, never a scan: every 5 s (or when it has moved > 8 blocks since the last sample) the follower's function
# tests a FIXED set of 9 positions - the block under its feet, 2 below that, and one at each of 6 points on a ring of radius 3
# at foot and head height - each with `execute if block <pos> #bm:cairn/<group>`, in a fixed priority order, against a block
# tag per SLOT GROUP. The first group that matches most often (a tally of 9 bytes) wins the biome palette; within a palette
# individual slots can also take the exact block found (e.g. a cobblestone under it fills 'trim' with cobblestone). Only reads.
SAMPLER = {
    'plains':  ['grass_block', 'dirt', 'coarse_dirt', 'podzol', 'rooted_dirt', 'moss_block', 'oak_log', 'birch_log', 'spruce_log', 'cobblestone', 'mossy_cobblestone', 'stone', 'gravel'],
    'desert':  ['sand', 'red_sand', 'sandstone', 'red_sandstone', 'cut_sandstone', 'smooth_sandstone', 'terracotta', 'orange_terracotta', 'cactus'],
    'cave':    ['deepslate', 'cobbled_deepslate', 'tuff', 'calcite', 'amethyst_block', 'deepslate_iron_ore', 'deepslate_diamond_ore', 'sculk', 'dripstone_block'],
    'nether':  ['netherrack', 'crimson_nylium', 'warped_nylium', 'blackstone', 'basalt', 'soul_sand', 'soul_soil', 'nether_bricks', 'magma_block', 'nether_gold_ore'],
    'snow':    ['snow_block', 'powder_snow', 'ice', 'packed_ice', 'blue_ice'],          # (a fifth palette, later)
}
SLOTMAP = {'head': 'the surface block (its top face on the head)', 'core': 'the soil / filler under it', 'trim': 'the "built" block (bricks, cobble, cut stone)',
           'limb': 'the column block (logs, pillars, basalt)', 'foot / fist': 'the hardest stone found', 'ore / ore2': 'any ore found nearby (else a palette default)',
           'tuft': 'the plant or crystal (leaves, cactus, amethyst, shroomlight)'}
UNLOCK = ('Build a cairn: stack 5 different natural blocks in a little column (a waystone) on a hilltop at dusk, and set a Gem of Creativity '
          'chip on top. At nightfall two amber eyes open in it; it shakes itself apart and re-forms as the Cairn. (It copies the cairn - the '
          'player\'s own blocks stay where they are.)')

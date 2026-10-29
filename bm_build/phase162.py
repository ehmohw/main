"""2.80d: DENNIS AND PISTACHIO - two new faces in the Black Market, and what they pay for (their follower selves: phase163).

THEIR ROOMS   dug under the vault-door balcony, off the alcove between its twin stairs (template x 31-45, z 75-80): DENNIS'S
              ASSAY OFFICE (west) and PISTACHIO'S PANTRY (east). Built at run time from the market's bm.mkt marker, so
              markets already in worlds get them too, and they turn with the market (only blocks that don't care which way
              they face; the signs are text displays).
DENNIS        the dwarf (dennis_art.py) buys the ore you mine - mostly for Tokens: 32 coal, 32 raw copper, 24 raw iron, 16 raw
              gold, 48 redstone, 32 lapis, 32 quartz or 32 amethyst shards a Token; a diamond for 2 (the Fence's rate); 2
              ancient debris for 1. Each lot has its own daily limit (5, 4 or 3 a day; diamonds 8). Every trade has a 1 in
              25 chance of something rare on top (a Medallion, a Heartstone, a Fallen Star, Lucky Tokens).
PISTACHIO     the ghost (pistachio_art.py) buys what comes off a mob's body - never what it carries (no arrows, weapons,
              armour, gold or nuggets): big lots for little - 32 rotten flesh, bones or string a Token; spider eyes,
              gunpowder, slime balls, leather, feathers, ink sacs, pearls, blaze and breeze rods, magma cream, membranes,
              prismarine shards in their own lots - each with a daily limit (5 down to 3 a day). His RARE PARTS pay well and
              come seldom: a wither skeleton skull 5 Tokens (3 a day); a zombie, skeleton or creeper head 3 (2 a day); a
              shulker shell, 2 rabbit's feet or 2 ghast tears 1 (2 or 3 a day). 1 in 25 trades: something rare on top.
FAVOUR        every trade fills its trader's favour meter (30). Full: DENNIS'S PROSPECTOR'S RUNE (onto any pickaxe: every
              100 blocks it mines, an even chance of a Token) or PISTACHIO'S TITHE SEAL (onto any sword: every mob it kills,
              a 1% chance of a Token) - and the meter starts again, so another is earned the same way. (Each upgraded tool
              turns up at most 8 Tokens a day - a cobblestone generator or a mob farm can't make a mint of it.)
              Use the rune or seal with the pickaxe or sword in your other hand.
50 TRADES     with either of them, all told, and he joins you: Dennis's Horn or Pistachio's Little Cloche (phase163).
LOOT          FORTUNE V while Dennis walks with you (every ore you mine, as if your pickaxe had Fortune V), LOOTING V while
              Pistachio does (as if your weapon had Looting V) - the ore and mob loot tables read it from your scores
              (bm.dwft, bm.pslt; phase163 sets them). A tool's own Fortune or Looting isn't added on top.
RICH SEAM     (3.0x) Dennis honoured by Queen Ava to rank III, out and within 24 blocks: every block of plain natural ground
              you mine (stone and its kin, cobblestone, terracotta, dirt and grass, sand, gravel, the Nether's and the End's
              ground, logs and stems) has a 1 in 10 chance of its drop twice - its table's pool rolled again (bm.dwrs; a
              whitelist of cheap terrain: no ores, no blocks with contents or copied data, nothing worth a place-and-break loop)."""
import copy, json, os, re
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import phase28 as P28
import rigfol as RF
import dennis_art as DA
import pistachio_art as PA
import mgeo

DW_C, DW_LINE, PS_C, PS_LINE = '#e0a040', '#ffe0b0', '#7ae890', '#d8ffe0'
GOLD = '#ffcf40'
TOKEN_C = '#ffd84a'
DW_MENU, PS_MENU = 2100, 2150          # Dennis 2100-2129 (2101-2110 his lots); Pistachio 2150-2199 (2151-2152 his pages, 2160-2181 his lots)
FAVOUR = 30
RECRUIT = 50
DAILY_TOOL = 8                         # (Tokens an upgraded pickaxe or sword turns up in a day, at most)

# (item, how many, Tokens, a day)
DW_LOTS = [('coal', 'Coal', 32, 1, 5), ('raw_copper', 'Raw Copper', 32, 1, 5), ('raw_iron', 'Raw Iron', 24, 1, 5), ('raw_gold', 'Raw Gold', 16, 1, 4),
           ('redstone', 'Redstone Dust', 48, 1, 4), ('lapis_lazuli', 'Lapis Lazuli', 32, 1, 4), ('quartz', 'Nether Quartz', 32, 1, 4),
           ('amethyst_shard', 'Amethyst Shards', 32, 1, 3), ('diamond', 'Diamond', 1, 2, 8), ('ancient_debris', 'Ancient Debris', 2, 1, 4)]
PS_COMMON = [('rotten_flesh', 'Rotten Flesh', 32, 1, 5), ('bone', 'Bones', 32, 1, 5), ('string', 'String', 32, 1, 5), ('spider_eye', 'Spider Eyes', 16, 1, 4),
             ('gunpowder', 'Gunpowder', 24, 1, 4), ('slime_ball', 'Slimeballs', 16, 1, 4), ('leather', 'Leather', 16, 1, 4), ('feather', 'Feathers', 32, 1, 4),
             ('ink_sac', 'Ink Sacs', 24, 1, 3), ('ender_pearl', 'Ender Pearls', 8, 1, 3), ('blaze_rod', 'Blaze Rods', 8, 1, 3),
             ('magma_cream', 'Magma Cream', 12, 1, 3), ('phantom_membrane', 'Phantom Membranes', 8, 1, 3), ('prismarine_shard', 'Prismarine Shards', 24, 1, 3),
             ('breeze_rod', 'Breeze Rods', 8, 1, 3)]
PS_RARE = [('wither_skeleton_skull', 'Wither Skeleton Skull', 1, 5, 3), ('zombie_head', 'Zombie Head', 1, 3, 2), ('skeleton_skull', 'Skeleton Skull', 1, 3, 2),
           ('creeper_head', 'Creeper Head', 1, 3, 2), ('shulker_shell', 'Shulker Shell', 1, 1, 2), ('rabbit_foot', "Rabbit's Feet", 2, 1, 2),
           ('ghast_tear', 'Ghast Tears', 2, 1, 3)]
PS_LOTS = PS_COMMON + PS_RARE
DW_RARE = [('medallion', 1, 3), ('heartstone', 1, 2), ('fallen_star', 1, 2), ('lucky_token', 3, 3)]          # (item, count, weight)
PS_RARE_GIFT = [('medallion', 1, 3), ('ectoplasm', 2, 3), ('heartstone', 1, 1), ('lucky_token', 3, 2)]
PICKS = ['wooden', 'stone', 'copper', 'iron', 'golden', 'diamond', 'netherite']

# ------------------------------------------------------------------------------------------------ items
item('prospector_rune', TOTEM, "Dennis's Prospector's Rune", DW_C,
     ['A stone with a gold rune cut in it,', 'warm from Dennis\'s pocket.', ('Use it with a pickaxe in your other hand:', 'blue'),
      ('every 100 blocks that pickaxe mines,', 'blue'), ('an even chance of a Black Market Token.', 'blue'), ('(8 Tokens a day at most.)', 'gray'),
      ('"Dig deep, lad. The mountain pays them as asks."', 'dark_gray')], model='bm:prospector_rune', stack=1, cat='magic', glint=True, comps=hold('none'))
HOLD['prospector_rune'] = 'bm:p162/rune/use'
item('tithe_seal', TOTEM, "Pistachio's Tithe Seal", PS_C,
     ['A green wax seal with a little top hat pressed in it.', ('Use it with a sword in your other hand:', 'blue'),
      ('every mob that sword slays has a 1% chance', 'blue'), ('of leaving a Black Market Token.', 'blue'), ('(8 Tokens a day at most.)', 'gray'),
      ('"The departed always tip, sir. Eventually."', 'dark_gray')], model='bm:tithe_seal', stack=1, cat='magic', glint=True, comps=hold('none'))
HOLD['tithe_seal'] = 'bm:p162/seal/use'

# the two NPCs' rigs (as phase145's _Art: what rigfol and phase134 want)
class DArt:
    PIVOT, PARENT, PARTS, PART_K, PREFIX = DA.PIVOT, DA.PARENT, DA.PARTS, DA.PART_K, DA.PREFIX
    HIDDEN = staticmethod(DA.HIDDEN)
    model_name = staticmethod(DA.model_name)


class PArt:
    PIVOT, PARENT, PARTS, PART_K, PREFIX = PA.PIVOT, PA.PARENT, PA.PARTS, PA.PART_K, PA.PREFIX
    HIDDEN = staticmethod(PA.HIDDEN)
    model_name = staticmethod(PA.model_name)


def extend_offers(O, offer):
    pass


# ================================================================================================= resource pack
def _icon(kind):
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind == 'rune':
        d.polygon([(3, 4), (8, 1), (13, 4), (14, 11), (8, 15), (2, 11)], fill=hexc('#6a6e78'), outline=hexc('#34363c'))
        d.line((8, 3, 8, 13), fill=hexc('#ffd84a')); d.line((5, 6, 8, 9), fill=hexc('#ffd84a')); d.line((11, 6, 8, 9), fill=hexc('#ffd84a'))
        d.line((5, 11, 11, 11), fill=hexc('#ffd84a'))
        d.point((5, 4), fill=hexc('#9aa0ac')); d.point((10, 3), fill=hexc('#9aa0ac'))
    else:
        d.ellipse((1, 2, 14, 15), fill=hexc('#3aa058'), outline=hexc('#1e6a32'))
        for x, y in ((1, 6), (13, 9), (6, 14), (11, 2)):
            d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=hexc('#3aa058'))
        d.rectangle((6, 4, 9, 9), fill=hexc('#1c2a1e')); d.rectangle((4, 9, 11, 10), fill=hexc('#1c2a1e'))      # a top hat pressed in
        d.line((6, 8, 9, 8), fill=hexc('#c8383a'))
        d.point((4, 5), fill=hexc('#8af0a4')); d.point((5, 4), fill=hexc('#8af0a4'))
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for art in (DA, PA):
        for name, (tex, els) in art.models().items():
            R.HATS[name] = (tex, els)
        R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (art.PREFIX,)
    R.ICONS['prospector_rune'] = _icon('rune')
    R.ICONS['tithe_seal'] = _icon('seal')


def textures():
    out = DA.textures()
    out.update(PA.textures())
    return out


# ================================================================================================= the loot tables
VANILLA = '/home/claude/mc263/gen/out/data/minecraft/loot_table'


def _vanilla_dir():
    for d in (VANILLA, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendor', 'loot263')):
        if os.path.isdir(d): return d
    raise FileNotFoundError('the 26.3 loot tables (tools/setup_test_env.sh builds them)')


def _mods(x):
    m = x.get('modifier', [])
    return m if isinstance(m, list) else [m]


def fortune_table(t):
    """an ore's table, with Fortune V for whoever has bm.dwft: each pool's alternatives get, after the silk-touch child, the
    buffed copies of the ordinary child - ore_drops (x1 2/7, x2-x6 1/7 each: chained chances), uniform_bonus_count (+0-5 x the
    multiplier)"""
    buff = {'type': 'minecraft:entity_scores', 'entity': 'this', 'scores': {'bm.dwft': {'min': 1}}}
    t = copy.deepcopy(t)
    for pool in t['pools']:
        for e in pool['entries']:
            if e.get('type') != 'minecraft:alternatives': continue
            kids = e['children']
            k = next((i for i, c in enumerate(kids) if any(m.get('type') == 'minecraft:apply_bonus' for m in _mods(c))), None)
            if k is None: continue
            plain = kids[k]
            mods = _mods(plain)
            bonus = next(m for m in mods if m.get('type') == 'minecraft:apply_bonus')
            rest = [m for m in mods if m is not bonus and m.get('type') != 'minecraft:set_count']
            base = next((m['count'] for m in mods if m.get('type') == 'minecraft:set_count'), 1)
            def scaled(kx):
                if isinstance(base, dict) and base.get('type') == 'minecraft:uniform':
                    return {'type': 'minecraft:uniform', 'min': base['min'] * kx, 'max': base['max'] * kx}
                return base * kx
            new = []
            if bonus['formula'] == 'minecraft:ore_drops':
                for kx in (6, 5, 4, 3, 2):
                    c = {kx2: 1 / (kx2 + 1) for kx2 in range(2, 7)}[kx]
                    new.append(dict(plain, modifier=[{'type': 'minecraft:set_count', 'count': scaled(kx)}] + rest,
                                    condition={'type': 'minecraft:all_of', 'terms': [buff, {'type': 'minecraft:random_chance', 'chance': round(c, 5)}]}))
                new.append(dict(plain, modifier=[{'type': 'minecraft:set_count', 'count': scaled(1)}] + rest, condition=buff))
            elif bonus['formula'] == 'minecraft:uniform_bonus_count':
                mult = bonus.get('parameters', {}).get('bonusMultiplier', 1)
                new.append(dict(plain, modifier=[{'type': 'minecraft:set_count', 'count': base},
                                                 {'type': 'minecraft:set_count', 'count': {'type': 'minecraft:uniform', 'min': 0, 'max': 5 * mult}, 'add': True}] + rest,
                                condition=buff))
            else:
                continue
            e['children'] = kids[:k] + new + kids[k:]
    return t


# (3.0x) RICH SEAM - Dennis honoured by Queen Ava to rank III (phase201): while he's out and within 24 blocks, every block of
# plain ground you mine (stone, dirt, sand, gravel, logs...) has a 1 in 10 chance of its drop twice. phase163 keeps bm.dwrs on you:
# 1 while it's yours, 2 under the test hook (#dwrs_test bm.cfg 1: every time). The table's own pool is rolled once more, so the
# second drop is the block's own: the silk-touch stone, the plain one's cobblestone, gravel's flint chance, the nylium's netherrack.
# Only the loot context's `this` can carry the score - the player who broke it; an explosion's, a piston's, a mob's never does.
# NATURAL GROUND ONLY (a whitelist): vanilla can't tell a placed block from a natural one, so anything worth placing and breaking
# again (ore blocks, diamond blocks, amethyst, anything crafted) would be a mint - only cheap terrain is on the list, and only where
# vanilla's table is one plain pool (no block entity, no copied components, no counts, no crops, no leaves). Ores never: Fortune V.
RS_CHANCE = 0.1
RS_STONE = ['stone', 'granite', 'diorite', 'andesite', 'tuff', 'deepslate', 'calcite', 'dripstone_block', 'smooth_basalt', 'cobblestone',
            'cobbled_deepslate', 'mossy_cobblestone', 'netherrack', 'basalt', 'blackstone', 'end_stone', 'cinnabar', 'sulfur', 'magma_block',
            'sandstone', 'red_sandstone', 'terracotta'] + [f'{c}_terracotta' for c in (
            'white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black')]
RS_SOIL = ['dirt', 'coarse_dirt', 'rooted_dirt', 'grass_block', 'podzol', 'mycelium', 'mud', 'moss_block', 'pale_moss_block', 'crimson_nylium',
           'warped_nylium', 'sand', 'red_sand', 'gravel', 'soul_sand', 'soul_soil', 'mangrove_roots', 'muddy_mangrove_roots', 'nether_wart_block',
           'warped_wart_block']
RS_WOOD = re.compile(r'(stripped_)?[a-z_]+_(log|wood)|(stripped_)?(crimson|warped)_(stem|hyphae)|mushroom_stem|(stripped_)?bamboo_block')
RS_NEVER = re.compile(r'.*(_ore|ancient_debris|shulker|chest|barrel|furnace|smoker|hopper|spawner|vault|sign|shelf|bed|banner|skull|head)$')
RS_SCORE = lambda lo: {'type': 'minecraft:entity_scores', 'entity': 'this', 'scores': {'bm.dwrs': {'min': lo}}}
RS_COND = {'type': 'minecraft:any_of', 'terms': [RS_SCORE(2), {'type': 'minecraft:all_of', 'terms': [RS_SCORE(1), {'type': 'minecraft:random_chance', 'chance': RS_CHANCE}]}]}
_RS_OK_COND = {'minecraft:survives_explosion', 'minecraft:table_bonus'}       # (dict conditions a plain drop may carry)
_RS_OK_REF = {'minecraft:tool/can_silk_touch'}                               # (and the predicate references)


def rs_wanted(name):
    return not RS_NEVER.fullmatch(name) and (name in RS_STONE or name in RS_SOIL or bool(RS_WOOD.fullmatch(name)))


def rs_simple(t):
    """vanilla's table is one plain pool of one entry - an item or alternatives of items (silk touch or not), with nothing done to
    the stack (no modifiers: no copied block entity, no counts, no bonus) and no conditions but silk touch, survives_explosion and
    gravel's flint chance"""
    def cond_ok(c):
        if c is None: return True
        if isinstance(c, str): return c in _RS_OK_REF
        return isinstance(c, dict) and c.get('type') in _RS_OK_COND

    def entry_ok(e):
        if not isinstance(e, dict) or set(e) - {'type', 'name', 'condition', 'children'} or not cond_ok(e.get('condition')): return False
        if e.get('type') == 'minecraft:item': return 'children' not in e and isinstance(e.get('name'), str)
        if e.get('type') == 'minecraft:alternatives': return bool(e.get('children')) and all(entry_ok(c) for c in e['children'])
        return False
    if t.get('type') != 'minecraft:block' or set(t) - {'type', 'pools', 'random_sequence'} or len(t.get('pools', [])) != 1: return False
    p = t['pools'][0]
    return (not set(p) - {'rolls', 'entries', 'condition'} and p.get('rolls') == 1 and cond_ok(p.get('condition'))
            and len(p['entries']) == 1 and entry_ok(p['entries'][0]))


def rich_seam_table(t):
    """vanilla's table with its pool once more, for whoever has bm.dwrs (1: a 1 in 10 chance, 2: always)"""
    t = copy.deepcopy(t)
    extra = copy.deepcopy(t['pools'][0])
    own = extra.pop('condition', None)
    extra['condition'] = copy.deepcopy(RS_COND) if own is None else {'type': 'minecraft:all_of', 'terms': [copy.deepcopy(RS_COND), own]}
    t['pools'].append(extra)
    return t


def rich_seam_tables(vd):
    """{block: its Rich Seam table} - every natural-ground block whose vanilla table is plain"""
    out = {}
    for f in sorted(os.listdir(os.path.join(vd, 'blocks'))):
        if not f.endswith('.json') or not rs_wanted(f[:-5]): continue
        t = json.load(open(os.path.join(vd, 'blocks', f)))
        if rs_simple(t): out[f[:-5]] = rich_seam_table(t)
    return out


LOOTING_FREE = {'type': 'minecraft:inverted', 'term': {'type': 'minecraft:entity_properties', 'entity': 'attacker', 'predicate': {
    'equipment': {'mainhand': {'predicates': {'minecraft:enchantments': [{'enchantments': 'minecraft:looting'}]}}}}}}
LOOT_BUFF = {'type': 'minecraft:all_of', 'terms': [{'type': 'minecraft:entity_scores', 'entity': 'attacker', 'scores': {'bm.pslt': {'min': 1}}}, LOOTING_FREE]}


def looting_table(t):
    """a mob's table with Looting V for a killer who has bm.pslt (and no Looting of their own): every looting count bonus
    gets its Looting V twin; every looting-raised chance, the chance it has at Looting V. Returns None if it has neither."""
    t = copy.deepcopy(t)
    hit = [0]

    def fix_cond(c):
        if isinstance(c, list): return [fix_cond(x) for x in c]
        if not isinstance(c, dict): return c
        ty = c.get('type')
        if ty in ('minecraft:all_of', 'minecraft:any_of'):
            return dict(c, terms=[fix_cond(x) for x in c['terms']])
        if ty == 'minecraft:random_chance_with_enchanted_bonus' and c.get('enchantment') == 'minecraft:looting':
            ec = c.get('enchanted_chance')
            if isinstance(ec, dict) and ec.get('type') == 'minecraft:linear':
                p5 = ec.get('base', 0) + ec.get('per_level_above_first', 0) * 4
            elif isinstance(ec, (int, float)):
                p5 = ec
            else:
                return c
            hit[0] += 1
            return {'type': 'minecraft:any_of', 'terms': [c, {'type': 'minecraft:all_of', 'terms': [LOOT_BUFF, {'type': 'minecraft:random_chance', 'chance': round(min(1.0, p5), 5)}]}]}
        return c

    def walk(x):
        if isinstance(x, dict):
            if 'condition' in x: x['condition'] = fix_cond(x['condition'])
            if 'modifier' in x:
                ms = _mods(x); out = []
                for m in ms:
                    if isinstance(m, dict) and 'condition' in m: m['condition'] = fix_cond(m['condition'])
                    out.append(m)
                    if isinstance(m, dict) and m.get('type') == 'minecraft:enchanted_count_increase' and m.get('enchantment') == 'minecraft:looting':
                        cnt = m.get('count')
                        if isinstance(cnt, dict) and cnt.get('type') == 'minecraft:uniform':
                            add = {'type': 'minecraft:uniform', 'min': cnt['min'] * 5, 'max': cnt['max'] * 5}
                        elif isinstance(cnt, (int, float)):
                            add = cnt * 5
                        else:
                            continue
                        twin = {'type': 'minecraft:set_count', 'count': add, 'add': True, 'condition': LOOT_BUFF}
                        out.append(twin); hit[0] += 1
                        if 'limit' in m:
                            out.append({'type': 'minecraft:limit_count', 'limit': {'max': m['limit']}, 'condition': LOOT_BUFF})
                x['modifier'] = out
            for v in list(x.values()):
                if isinstance(v, (dict, list)): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(t)
    return t if hit[0] else None


# ================================================================================================= the datapack
def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    tick, fast, second = [], [], []
    objs = (['bm.dwday', 'bm.psday', 'bm.dwt', 'bm.pst', 'bm.dwf', 'bm.psf', 'bm.dwr', 'bm.psr', 'bm.dwmb', 'bm.dwpk', 'bm.pssw', 'bm.dwpkd', 'bm.psswd',
             'bm.dwcl', 'bm.dwn', 'bm.dwns', 'bm.dwnx', 'bm.p162', 'bm.dwft', 'bm.pslt', 'bm.dwrs'] +
            [f'bm.dwq{i}' for i in range(len(DW_LOTS))] + [f'bm.psq{i}' for i in range(len(PS_LOTS))])
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        [f'scoreboard objectives add bm.um{k} minecraft.used:minecraft.{p}_pickaxe' for k, p in enumerate(PICKS)]
    G.OBJECTIVES += objs + [f'bm.um{k}' for k in range(len(PICKS))]
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #25 bm.rng 25', 'scoreboard players set #100 bm.rng 100']
    plain = lambda iid: f'minecraft:{iid}[!minecraft:custom_data]'

    # ================================================================== the loot tables: Fortune V (ores), Looting V (mobs)
    vd = _vanilla_dir()
    nore = 0
    for f in sorted(os.listdir(os.path.join(vd, 'blocks'))):
        if not f.endswith('_ore.json'): continue
        t = json.load(open(os.path.join(vd, 'blocks', f)))
        if 'minecraft:apply_bonus' not in json.dumps(t): continue
        wjson(f'minecraft/loot_table/blocks/{f}', fortune_table(t)); nore += 1
    assert nore >= 18, nore
    # (3.0x) Rich Seam: the natural ground's tables (never an ore's: those are Fortune V's, above - nor any other override)
    rs = rich_seam_tables(vd)
    for b, t in rs.items():
        assert not os.path.exists(G.path('data', 'minecraft', 'loot_table', 'blocks', f'{b}.json')), f'Rich Seam: blocks/{b} already overridden'
        wjson(f'minecraft/loot_table/blocks/{b}.json', t)
    assert len(rs) >= 100, len(rs)
    nmob = 0
    for f in sorted(os.listdir(os.path.join(vd, 'entities'))):
        if not f.endswith('.json'): continue
        mine = G.path('data', 'minecraft', 'loot_table', 'entities', f)
        t = json.load(open(mine if os.path.exists(mine) else os.path.join(vd, 'entities', f)))
        t2 = looting_table(t)
        if t2 is not None:
            wjson(f'minecraft/loot_table/entities/{f}', t2); nmob += 1
    assert nmob >= 40, nmob

    # ================================================================== the two traders, as one pattern
    def trader(k, name, col, line, menu, lots, pages, gift, prize, prize_name, art, A, art_k):
        """k: dw / ps. pages: [(page code, title, [lot indices], extra buttons)] - the first is the front page"""
        speak = lambda txt: tellraw('@s', [T(f'{name}: ', col, bold=True), T(f'"{txt}"', line)])
        bar = lambda txt: title('@s', 'actionbar', [T(f'{name}: ', col, bold=True), T(txt, line)])
        # a new day: every lot's count back to nought
        fn(f'p162/{k}/day', [f'execute if score @s bm.{k}day = #day bm.bm run return 0', f'scoreboard players operation @s bm.{k}day = #day bm.bm'] +
           [f'scoreboard players set @s bm.{k}q{i} 0' for i in range(len(lots))])
        # ---- the page: the line, the record, a button per lot (its price, what's left of today's limit)
        LOT0 = menu + 10
        rec = [P28.body([T(f'Trades with {name}: ', 'gray'), T('$(t)', 'white', bold=True), '@@RAW:r_t@@'], 340),
               P28.body([T('Favour: ', 'gray'), T('$(f)', col, bold=True), T(f' of {FAVOUR}', 'gray'), T(f' - full, and {prize_name} is yours (then it fills again).', 'dark_gray')], 340)]
        for pcode, ptitle, idx, extra in pages:
            btns = []
            for i in idx:
                iid, nm, n, tok, lim = lots[i]
                btns.append(P28.btn([T(f'{n} {nm}' if n > 1 else nm, 'white'), T('  →  ', 'dark_gray'), T(f'{tok} Token' + ('s' if tok > 1 else ''), TOKEN_C, bold=True),
                                     T(f'   $(q{i})/{lim}', 'dark_gray')], LOT0 + i, width=230,
                                    tooltip=T(f'Hand over {n} {nm}: {tok} Black Market Token' + ('s' if tok > 1 else '') + f'. {lim} a day.', 'gray')))
            dlg = P28.multi([T(ptitle, col, bold=True)], [P28.body(line_body[k], 340)] + rec, btns + extra, columns=2, exit_label='Close', button_width=230)
            fill = [f'scoreboard players set @s bm.menu {menu}', 'data remove storage bm:ui tr', f'function bm:p162/{k}/day',
                    f'execute store result storage bm:ui tr.t int 1 run scoreboard players get @s bm.{k}t',
                    f'execute store result storage bm:ui tr.f int 1 run scoreboard players get @s bm.{k}f',
                    f'data modify storage bm:ui tr.r_t set value {snbt(T(f" of {RECRUIT} - and he joins you.", "gray"))}',
                    f'execute if entity @s[tag=bm.{art_k}met] run data modify storage bm:ui tr.r_t set value {snbt(T(" - he walks with you now.", col))}'] + \
                   [f'execute store result storage bm:ui tr.q{i} int 1 run scoreboard players get @s bm.{k}q{i}' for i in idx]
            fn(f'p162/{k}/pg{pcode}', fill + [f'function bm:p162/{k}/pg{pcode}_dlg with storage bm:ui tr'])
            fn(f'p162/{k}/pg{pcode}_dlg', [f'$dialog show @s {P28.inline(dlg)}'])
        front = pages[0][0]
        fn(f'p162/{k}/open', [f'function bm:p162/{k}/pg{front}'])
        # ---- a lot handed over
        acts = [f'execute unless score @s bm.menu matches {menu} run return run function bm:p28/stale']
        acts += [f'execute if score #act bm.pay matches {pc} run return run function bm:p162/{k}/pg{pc}' for pc, *_r in pages]
        acts += [f'execute if score #act bm.pay matches {LOT0 + i} run return run function bm:p162/{k}/lot{i}' for i in range(len(lots))]
        fn(f'p162/{k}/act', acts)
        G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {menu}..{menu + 49} run return run function bm:p162/{k}/act')
        for i, (iid, nm, n, tok, lim) in enumerate(lots):
            pg = next(pc for pc, _t, idx, _e in pages if i in idx)
            fn(f'p162/{k}/lot{i}', [f'function bm:p162/{k}/day',
                                    f'execute if score @s bm.{k}q{i} matches {lim}.. run function bm:p162/{k}/enough {{n:"{nm}"}}',
                                    f'execute if score @s bm.{k}q{i} matches {lim}.. run return run function bm:p162/{k}/pg{pg}',
                                    f'execute store result score #n bm.rng run clear @s {plain(iid)} 0',
                                    f'execute if score #n bm.rng matches ..{n - 1} run function bm:p162/{k}/short {{n:"{n} {nm}"}}',
                                    f'execute if score #n bm.rng matches ..{n - 1} run return run function bm:p162/{k}/pg{pg}',
                                    f'clear @s {plain(iid)} {n}', give('token', tok), f'scoreboard players add @s bm.{k}q{i} 1',
                                    f'function bm:p162/{k}/traded', f'function bm:p162/{k}/pg{pg}'])
        fn(f'p162/{k}/enough', ['$' + speak(enough[k]), 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.6 0.8'])
        fn(f'p162/{k}/short', ['$' + bar(short[k]), 'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.6 0.8'])
        # (every trade: the record, the favour, a chance of something rare, and at 50 he joins you)
        fn(f'p162/{k}/traded', [f'scoreboard players add @s bm.{k}t 1', f'scoreboard players add @s bm.{k}f 1',
                                'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.8 1.2', sound[k],
                                f'execute as @e[type=minecraft:interaction,tag=bm.{k}nhit,distance=..10,limit=1,sort=nearest] run function bm:p162/{k}/npc/react_trade',
                                'execute store result score #r bm.rng run random value 1..25',
                                f'execute if score #r bm.rng matches 1 run function bm:p162/{k}/gift',
                                f'execute if score @s bm.{k}f matches {FAVOUR}.. run function bm:p162/{k}/prize',
                                f'execute if score @s bm.{k}t matches {RECRUIT}.. unless entity @s[tag=bm.{art_k}met] run function bm:p163/{art_k}/recruit'])
        wjson(f'bm/loot_table/p162/{k}_gift.json', {'pools': [{'rolls': 1, 'entries': [dict(G.loot_entry(i, n), weight=w) for i, n, w in gift]}]})
        fn(f'p162/{k}/gift', [f'loot give @s loot bm:p162/{k}_gift', speak(gift_line[k]), 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6',
                              tellraw('@s', [T('  (a 1 in 25 on any trade - it\'s in your pack)', 'dark_gray')])])
        fn(f'p162/{k}/prize', [f'scoreboard players remove @s bm.{k}f {FAVOUR}', f'scoreboard players add @s bm.{k}r 1', give(prize),
                               speak(prize_line[k]), tellraw('@s', [T(f'{prize_name}', col, bold=True), T(prize_how[k], 'gray')]),
                               f'execute as @e[type=minecraft:interaction,tag=bm.{k}nhit,distance=..10,limit=1,sort=nearest] run function bm:p162/{k}/npc/react_prize',
                               'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.7 1.2', f'advancement grant @s only bm:story/{k}_prize'])
        wjson(f'bm/advancement/story/{k}_prize.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
              'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': f'bm:{prize}'}}, 'title': T(adv_title[k], col),
                          'description': T(adv_desc[k], 'gray'), 'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})

        # ---- him, in his room: his rig (still but for his idle), his click box
        nsel = lambda p=None: f'@e[type=minecraft:item_display,tag=bm.{k}n' + (f',tag=bm.{k}np_{p}' if p else '') + ',distance=..4]'
        bright = {'brightness': {'block': Int(15), 'sky': Int(15)}} if k == 'ps' else {'brightness': {'block': Int(13), 'sky': Int(13)}}
        fn(f'p162/{k}/npc/spawn', [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, [f"bm.{k}np", f"bm.{k}np_{p}", f"bm.{k}n", "bm.p162prop"], art.RIG_SCALE, extra=dict(bright, shadow_radius=F(0.5 if p == "body" else 0.0), shadow_strength=F(0.5)))}'
                                   for p in A.PARTS] +
           [f'summon minecraft:interaction ~ ~ ~ {snbt({"Tags": [f"bm.{k}nhit", "bm.p162prop"], "width": F(1.1), "height": F(2.0 if k == "dw" else 2.2), "response": B(1)})}',
            f'function bm:p162/{k}/npc/place', f'scoreboard players set @e[type=minecraft:interaction,tag=bm.{k}nhit,distance=..1] bm.dwns 0'])
        fn(f'p162/{k}/npc/place', RF.place(A, art.RIG_SCALE / 16, nsel))
        P = art.POSES
        cyc = {0: (40, [(0, 'idle_a'), (20, 'idle_b')]), 1: (None, [(0, 'point'), (20, 'idle_a')]), 2: (None, [(0, react_pose[k]), (18, 'idle_a')]),
               3: (None, [(0, 'bow'), (24, 'idle_a')]), 4: (None, [(0, 'wave_a'), (6, 'wave_b'), (12, 'wave_a'), (18, 'wave_b'), (24, 'idle_a')])}
        for nm_ in {p for _per, frames in cyc.values() for _t, p in frames}:
            fn(f'p162/{k}/npc/pose/{nm_}', RF.pose(A, P[nm_], art.RIG_SCALE, 6 if nm_ not in ('idle_a', 'idle_b') else 20, nsel, swap=('head',)))
        RF.cycles(fn, f'p162/{k}/npc', cyc, 'bm.dwn', 'bm.dwns', lambda p: f'p162/{k}/npc/pose/{p}')
        tick.append(f'execute as @e[type=minecraft:interaction,tag=bm.{k}nhit] at @s if entity @a[distance=..24] run function bm:p162/{k}/npc/tick')
        fn(f'p162/{k}/npc/tick', ['scoreboard players add @s bm.dwn 1', 'execute if score @s bm.dwnx matches 1.. run scoreboard players remove @s bm.dwnx 1',
                                  'execute if score @s bm.dwns matches 1.. unless score @s bm.dwnx matches 1.. run function bm:p162/npc/calm',
                                  f'execute if score @s bm.dwns matches 0 if entity @a[distance=..6,tag=!bm.{k}seen] run function bm:p162/{k}/npc/hello',
                                  f'tag @a[distance=12..40,tag=bm.{k}seen] remove bm.{k}seen', f'function bm:p162/{k}/npc/anim'] + ambient[k])
        fn(f'p162/{k}/npc/hello', [f'tag @a[distance=..6] add bm.{k}seen', 'scoreboard players set @s bm.dwns 4', 'scoreboard players set @s bm.dwn 0',
                                   'scoreboard players set @s bm.dwnx 30', hello_sound[k]])
        for st, tm, nm_ in ((1, 40, 'point'), (2, 30, 'trade'), (3, 40, 'prize')):
            fn(f'p162/{k}/npc/react_{nm_}', [f'scoreboard players set @s bm.dwns {st}', 'scoreboard players set @s bm.dwn 0', f'scoreboard players set @s bm.dwnx {tm}'])
        fast.append(f'execute as @e[type=minecraft:interaction,tag=bm.{k}nhit] if data entity @s interaction at @s run function bm:p162/{k}/npc/clicked')
        fast.append(f'execute as @e[type=minecraft:interaction,tag=bm.{k}nhit] if data entity @s attack run data remove entity @s attack')
        fn(f'p162/{k}/npc/clicked', [f'execute on target run function bm:p162/{k}/npc/click', 'data remove entity @s interaction'])
        fn(f'p162/{k}/npc/click', ['execute if score @s bm.dwcl matches 1.. run return 0', 'scoreboard players set @s bm.dwcl 8',
                                   'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                                   f'execute unless entity @s[tag=bm.{k}hi] run function bm:p162/{k}/first',
                                   f'execute as @e[type=minecraft:interaction,tag=bm.{k}nhit,distance=..8,limit=1] run function bm:p162/{k}/npc/react_point',
                                   f'execute if entity @s[tag=bm.{art_k}met] run function bm:p163/{art_k}/reissue',
                                   f'function bm:p162/{k}/open'])
        fn(f'p162/{k}/first', [f'tag @s add bm.{k}hi'] + [speak(l) for l in first_lines[k]])

    line_body = {
        'dw': [T('Dennis', DW_C, bold=True), T(' - dwarf, miner, Black Market regular. ', 'gray'),
               T('"Bring me what you dig, lad. I pay in Tokens, fair and square - and now and then something shinier."', DW_LINE)],
        'ps': [T('Pistachio', PS_C, bold=True), T(' - ghost, butler of the Omega Palace. ', 'gray'),
               T('"Parts of the departed, sir - the body\'s own, mind; not what they carried. In quantity, for a modest consideration."', PS_LINE)]}
    enough = {'dw': "That's enough $(n) for today, lad. Come back tomorrow.", 'ps': 'The pantry is quite full of $(n) today, sir. Tomorrow, perhaps.'}
    short = {'dw': 'That takes $(n), lad - count again.', 'ps': 'I require $(n), sir. A full lot, if you please.'}
    sound = {'dw': 'playsound minecraft:block.anvil.land player @s ~ ~ ~ 0.25 1.6', 'ps': 'playsound minecraft:block.bell.use player @s ~ ~ ~ 0.4 1.8'}
    gift_line = {'dw': 'Here - found this in the last load. Reckon you should have it.', 'ps': 'A little something from the Palace cellars, sir. With my compliments.'}
    prize_line = {'dw': "You've been good to me, lad. Take my rune - put it on any pick you like.",
                  'ps': 'Your custom is most valued, sir. My Tithe Seal - press it to any blade.'}
    prize_how = {'dw': ': use it with a pickaxe in your other hand - every 100 blocks it mines, an even chance of a Token.',
                 'ps': ': use it with a sword in your other hand - every mob it slays, a 1% chance of a Token.'}
    adv_title = {'dw': "The Prospector's Rune", 'ps': 'The Tithe Seal'}
    adv_desc = {'dw': "Earn Dennis's favour: his rune for your pickaxe", 'ps': "Earn Pistachio's favour: his seal for your sword"}
    react_pose = {'dw': 'wave_a', 'ps': 'lid_up'}
    hello_sound = {'dw': 'playsound minecraft:entity.villager.ambient neutral @a[distance=..12] ~ ~ ~ 0.5 0.6',
                   'ps': 'playsound minecraft:entity.allay.ambient_without_item neutral @a[distance=..12] ~ ~ ~ 0.5 0.6'}
    ambient = {'dw': [], 'ps': ['execute if score @s bm.dwns matches 0 if predicate bm:p141/now_and_then run particle minecraft:end_rod ~ ~1.4 ~ 0.3 0.5 0.3 0.005 1']}
    first_lines = {'dw': ['Oi! A customer. Dennis is the name - ore is the game.', 'Raw ore, dust and gems: I pay Tokens for the lot. Stick with me and you\'ll do alright.'],
                   'ps': ['Good day, sir. Pistachio, at your service - I keep house at the Omega Palace.',
                          'I collect certain... parts, for the Palace kitchen. Bring them in quantity and I shall pay.']}
    fn('p162/npc/calm', ['scoreboard players set @s bm.dwns 0', 'scoreboard players set @s bm.dwn 0'])
    tick.append('scoreboard players remove @a[scores={bm.dwcl=1..}] bm.dwcl 1')
    import phase174 as P174                 # (2.83: each sells his collector from the front page)
    trader('dw', 'Dennis', DW_C, DW_LINE, DW_MENU, DW_LOTS, [(DW_MENU, "DENNIS'S ASSAY OFFICE", list(range(len(DW_LOTS))), [P174.buy_btn('ore')])],
           DW_RARE, 'prospector_rune', "Dennis's Prospector's Rune", DA, DArt, 'dw')
    nc = len(PS_COMMON)
    trader('ps', 'Pistachio', PS_C, PS_LINE, PS_MENU, PS_LOTS,
           [(PS_MENU + 1, "PISTACHIO'S PANTRY", list(range(nc)), [P28.btn(T('Rare parts »', GOLD, bold=True), PS_MENU + 2, width=230,
                                                                         tooltip=T('Skulls, heads, shells - he pays well for these.', 'gray')), P174.buy_btn('mob')]),
            (PS_MENU + 2, "PISTACHIO'S PANTRY  ·  rare parts", list(range(nc, len(PS_LOTS))), [P28.btn(T('« Common lots', 'gray'), PS_MENU + 1, width=230)])],
           PS_RARE_GIFT, 'tithe_seal', "Pistachio's Tithe Seal", PA, PArt, 'pi')

    # ================================================================== the Prospector's Rune and the Tithe Seal: onto a tool
    def upgrade(k, iid, tag, tooltag, word, lore, col):
        fn(f'p162/{k}/use', [f'execute unless items entity @s weapon.offhand {tooltag} run return run ' + say(f'Hold the {word} to upgrade in your other hand.', 'gray'),
                             f'execute if items entity @s weapon.offhand *[minecraft:custom_data~{{{tag}:1b}}] run return run ' + say(f'That {word} has one already.', 'gray'),
                             f'item modify entity @s weapon.offhand {{type:"minecraft:set_custom_data",tag:"{{{tag}:1b}}"}}',
                             f'item modify entity @s weapon.offhand {{type:"minecraft:set_lore",mode:"append",lore:[{snbt(T(lore, col))}]}}',
                             f'clear @s {holds(iid)} 1', 'playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 1 1.1',
                             'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.8 1.4', 'particle minecraft:wax_on ~ ~1.2 ~ 0.4 0.4 0.4 0 20',
                             say(f'Your {word} takes it: ' + lore, col)])
    upgrade('rune', 'prospector_rune', 'bm_pros', '#minecraft:pickaxes', 'pickaxe', "⛏ Prospector's Rune: Tokens as it mines", DW_C)
    upgrade('seal', 'tithe_seal', 'bm_tithe', '#minecraft:swords', 'sword', "✦ Tithe Seal: Tokens from its slain", PS_C)
    # the rune at work: blocks mined with it (the pickaxes' "used" counts), each 100 an even chance of a Token
    for kk in range(len(PICKS)):
        tick.append(f'execute as @a[scores={{bm.um{kk}=1..}}] at @s run function bm:p162/rune/mined')
    fn('p162/rune/mined', ['scoreboard players set #n bm.rng 0'] +
       [l for kk in range(len(PICKS)) for l in (f'scoreboard players operation #n bm.rng += @s bm.um{kk}', f'scoreboard players set @s bm.um{kk} 0')] +
       ['execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{bm_pros:1b}] run return 0',
        'scoreboard players operation @s bm.dwmb += #n bm.rng',
        'execute if score @s bm.dwmb matches 100.. run function bm:p162/rune/hundred'])
    fn('p162/rune/hundred', ['scoreboard players remove @s bm.dwmb 100',
                             'execute unless score @s bm.dwpkd = #day bm.bm run scoreboard players set @s bm.dwpk 0', 'scoreboard players operation @s bm.dwpkd = #day bm.bm',
                             'execute store result score #r bm.rng run random value 1..2', 'execute if score #p162r bm.p162 matches 1 run scoreboard players set #r bm.rng 1',
                             f'execute if score #r bm.rng matches 1 if score @s bm.dwpk matches ..{DAILY_TOOL - 1} run function bm:p162/rune/token',
                             'execute if score @s bm.dwmb matches 100.. run function bm:p162/rune/hundred'])
    fn('p162/rune/token', ['scoreboard players add @s bm.dwpk 1', 'loot spawn ~ ~0.5 ~ loot bm:items/token',
                           'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 0.7', 'particle minecraft:wax_on ~ ~0.6 ~ 0.3 0.3 0.3 0 10',
                           say("Your Prospector's Rune turns up a Token!", DW_C)])
    # the seal at work: a mob slain with it (any but a player - and none of the pack's own), a 1% chance
    wjson('bm/advancement/p162/tithe.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
        'player': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {
            'equipment': {'mainhand': {'predicates': {'minecraft:custom_data': '{bm_tithe:1b}'}}}}}],
        'entity': [{'condition': 'minecraft:inverted', 'term': {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                                 'predicate': {'minecraft:entity_type': ['minecraft:player', 'minecraft:armor_stand']}}}]}}},
        'rewards': {'function': 'bm:p162/seal/kill'}})
    fn('p162/seal/kill', ['advancement revoke @s only bm:p162/tithe',
                          'execute unless score @s bm.psswd = #day bm.bm run scoreboard players set @s bm.pssw 0', 'scoreboard players operation @s bm.psswd = #day bm.bm',
                          f'execute if score @s bm.pssw matches {DAILY_TOOL}.. run return 0',
                          'execute store result score #r bm.rng run random value 1..100', 'execute if score #p162r bm.p162 matches 1 run scoreboard players set #r bm.rng 1',
                          'execute if score #r bm.rng matches 1 at @s run function bm:p162/seal/token'])
    fn('p162/seal/token', ['scoreboard players add @s bm.pssw 1', 'loot spawn ~ ~0.5 ~ loot bm:items/token',
                           'playsound minecraft:entity.allay.item_given player @s ~ ~ ~ 1 1.2', 'particle minecraft:soul ~ ~1 ~ 0.3 0.4 0.3 0.02 10',
                           say("Pistachio's Tithe Seal: the departed leave a Token!", PS_C)])

    # ================================================================== their rooms (2.80d: under the vault-door balcony)
    C = lambda x, y, z: mgeo.rel((x + 0.5, y + 0.5, z + 0.5))
    M = lambda x, y, z: mgeo.rel((x, y, z))
    fill = lambda a, b_, blk: f'fill {C(*a)} {C(*b_)} {blk}'
    setb = lambda a, blk: f'setblock {C(*a)} {blk}'
    ident = [F(0), F(0), F(0), F(1)]
    def label(tags, text, sc=0.4, width=200):
        return snbt({'Tags': tags, 'billboard': 'fixed', 'line_width': Int(width), 'background': Int(0x70000000), 'text': text, 'shadow': B(0),
                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(sc)] * 3}})
    def prop(iid, sc=0.5, yaw_=0):
        return snbt({'Tags': ['bm.p162prop', 'bm.p162new'], 'item': {'id': f'minecraft:{iid}', 'count': Int(1)}, 'item_display': 'fixed',
                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(sc)] * 3}})
    def put(kind, p, yaw, nbt):
        return [f'execute positioned {M(*p)} rotated ~{yaw} 0 run summon minecraft:{kind} ~ ~ ~ {nbt}',
                f'execute positioned {M(*p)} rotated ~{yaw} 0 as @e[tag=bm.p162new,distance=..0.6] run tp @s ~ ~ ~ ~ ~', 'tag @e[tag=bm.p162new] remove bm.p162new']
    build = [f'execute positioned {M(38.0, 11.0, 77.0)} run kill @e[tag=bm.p162prop,distance=..9]']
    # Dennis's office: x 31-37, Pistachio's pantry: x 39-45; floor y 9, room y 10-13, the balcony's mass round them
    build += [fill((31, 10, 75), (37, 13, 80), 'minecraft:air'), fill((39, 10, 75), (45, 13, 80), 'minecraft:air'),
              fill((31, 9, 75), (37, 9, 80), 'minecraft:polished_deepslate'), fill((39, 9, 75), (45, 9, 80), 'minecraft:dark_oak_planks'),
              fill((32, 10, 74), (33, 12, 74), 'minecraft:air'), fill((42, 10, 74), (43, 12, 74), 'minecraft:air'),
              fill((31, 13, 75), (37, 13, 75), 'minecraft:polished_blackstone_bricks'), fill((39, 13, 75), (45, 13, 75), 'minecraft:polished_blackstone_bricks')]
    # (Dennis: deepslate-tiled walls, barrels, a smithing table, a lodestone, hanging lanterns on chains, ore piled up as props)
    build += [fill((31, 10, 81), (37, 12, 81), 'minecraft:deepslate_tiles'), fill((30, 10, 75), (30, 12, 80), 'minecraft:deepslate_tiles'),
              fill((38, 10, 75), (38, 12, 80), 'minecraft:deepslate_tiles'),
              setb((31, 10, 80), 'minecraft:barrel[facing=up,open=false]'), setb((31, 11, 80), 'minecraft:barrel[facing=up,open=false]'),
              setb((31, 10, 79), 'minecraft:barrel[facing=up,open=false]'), setb((37, 10, 80), 'minecraft:smithing_table'),
              setb((37, 10, 79), 'minecraft:lodestone'), setb((37, 10, 76), 'minecraft:barrel[facing=up,open=false]'),
              setb((32, 13, 77), 'minecraft:iron_chain[axis=y,waterlogged=false]'), setb((32, 12, 77), 'minecraft:lantern[hanging=true,waterlogged=false]'),
              setb((36, 13, 77), 'minecraft:iron_chain[axis=y,waterlogged=false]'), setb((36, 12, 77), 'minecraft:lantern[hanging=true,waterlogged=false]')]
    for p, iid, sc in (((31.5, 12.25, 80.5), 'raw_gold', 0.55), ((31.3, 11.25, 79.6), 'raw_iron', 0.5), ((37.5, 11.25, 76.5), 'coal', 0.5),
                       ((37.5, 11.12, 79.5), 'diamond', 0.35), ((31.6, 11.25, 79.2), 'raw_copper', 0.45), ((37.4, 11.12, 80.5), 'iron_pickaxe', 0.55)):
        build += put('item_display', p, 0, prop(iid, sc))
    # (Pistachio: dark panelled walls, soul lanterns, a laid table, candles, a cauldron, cobwebs in the corners)
    build += [fill((39, 10, 81), (45, 12, 81), 'minecraft:dark_oak_planks'), fill((46, 10, 75), (46, 12, 80), 'minecraft:dark_oak_planks'),
              setb((40, 13, 77), 'minecraft:iron_chain[axis=y,waterlogged=false]'), setb((40, 12, 77), 'minecraft:soul_lantern[hanging=true,waterlogged=false]'),
              setb((44, 13, 77), 'minecraft:iron_chain[axis=y,waterlogged=false]'), setb((44, 12, 77), 'minecraft:soul_lantern[hanging=true,waterlogged=false]'),
              setb((39, 10, 80), 'minecraft:cauldron'), setb((45, 10, 80), 'minecraft:dark_oak_fence[east=false,north=false,south=false,west=false,waterlogged=false]'),
              setb((45, 11, 80), 'minecraft:white_carpet'), setb((45, 10, 79), 'minecraft:dark_oak_fence[east=false,north=false,south=false,west=false,waterlogged=false]'),
              setb((45, 11, 79), 'minecraft:white_carpet'), setb((39, 10, 76), 'minecraft:bookshelf'), setb((39, 11, 76), 'minecraft:white_candle[candles=3,lit=true,waterlogged=false]'),
              setb((45, 12, 81), 'minecraft:dark_oak_planks'), setb((39, 12, 80), 'minecraft:cobweb'), setb((45, 12, 75), 'minecraft:cobweb')]
    for p, iid, sc in (((45.5, 11.12, 80.5), 'bone', 0.4), ((45.5, 11.12, 79.5), 'spider_eye', 0.35), ((39.5, 10.95, 80.5), 'rotten_flesh', 0.4)):
        build += put('item_display', p, 0, prop(iid, sc))
    # signs over the doors (the alcove side) and inside
    build += put('text_display', (32.9, 12.6, 73.96), 180, label(['bm.p162prop', 'bm.p162new'], [T("DENNIS'S\n", DW_C, bold=True), T('ASSAY OFFICE', '#e8c070')], 0.45, 160))
    build += put('text_display', (42.9, 12.6, 73.96), 180, label(['bm.p162prop', 'bm.p162new'], [T("PISTACHIO'S\n", PS_C, bold=True), T('PANTRY', '#b0f0c0')], 0.45, 160))
    build += put('text_display', (34.5, 12.4, 80.96), 180, label(['bm.p162prop', 'bm.p162new'], [T('ORE BOUGHT\n', DW_C, bold=True), T('Tokens paid - fair and square', 'gray')], 0.35, 200))
    build += put('text_display', (42.5, 12.4, 80.96), 180, label(['bm.p162prop', 'bm.p162new'], [T('THE OMEGA PALACE\n', PS_C, bold=True), T('kitchen supplies, bought in quantity', 'gray')], 0.35, 220))
    # the two of them (facing the doors), and a marker at each spot so a missing rig comes back
    for k, x in (('dw', 34.5), ('ps', 42.5)):
        build += [f'execute positioned {M(x, 10.0, 79.0)} rotated ~180 0 run function bm:p162/{k}/npc/spawn',
                  f'execute positioned {M(x, 10.0, 79.0)} rotated ~180 0 run summon minecraft:marker ~ ~ ~ {{Tags:["bm.p162prop","bm.{k}spot"]}}',
                  f'execute positioned {M(x, 10.0, 79.0)} rotated ~180 0 as @e[type=minecraft:marker,tag=bm.{k}spot,distance=..0.5] run tp @s ~ ~ ~ ~ 0']
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.{k}spot] at @s if entity @a[distance=..32] unless entity @e[type=minecraft:interaction,tag=bm.{k}nhit,distance=..1.5] '
                      f'rotated as @s run function bm:p162/{k}/npc/respawn')
        fn(f'p162/{k}/npc/respawn', [f'kill @e[type=minecraft:item_display,tag=bm.{k}n,distance=..3]', f'function bm:p162/{k}/npc/spawn'])
    fn('p162/install', ['tag @s add bm.dp280'] + build)
    corners = [(30, 9, 74), (46, 9, 74), (30, 9, 81), (46, 9, 81)]
    loaded = ' '.join(f'if loaded {C(*c)}' for c in corners)
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.mkt,tag=!bm.dp280] at @s rotated as @s {loaded} run function bm:p162/install')

    # ================================================================== admin
    fn('admin/traders', [say('Dennis and Pistachio: their rooms are built again in every loaded market.', DW_C), 'tag @e[type=minecraft:marker,tag=bm.mkt] remove bm.dp280'])
    fn('admin/trades_50', ['scoreboard players set @s bm.dwt 49', 'scoreboard players set @s bm.pst 49',
                           say('49 trades with Dennis and with Pistachio - one more each, and they join you.', DW_C)])
    fn('admin/favour_full', [f'scoreboard players set @s bm.dwf {FAVOUR - 1}', f'scoreboard players set @s bm.psf {FAVOUR - 1}',
                             say('Dennis\'s and Pistachio\'s favour one trade from full.', DW_C)])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/trades_50', 'yellow'), T('  49 trades with Dennis and Pistachio (one more: they join you); admin/favour_full: favour one from full', 'gray')]),
                              tellraw('@s', [T('/function bm:admin/traders', 'yellow'), T('  rebuild Dennis\'s and Pistachio\'s rooms in the loaded markets', 'gray')])]
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.p162prop]']
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

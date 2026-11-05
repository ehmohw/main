"""3.1: COLLECTOR ACCOUNTS - the Stone Collector and the Wood Box (the Fence), the Ore Magnet and the Spirit Jar reworked to the same
system (design_collectors2.md, the owner's words): each one is a KEY to an account kept against the player - never inside the item,
so any copy opens the same one, death and lava can't touch it, and one each on the Rat Pack is all you need.

USE        right-click it (main or off hand), or press its row on the Rat Pack's Collectors page: its account. The front page has one
           button per category (with its total), "Deposit everything it takes" (the whole inventory), "Auto-collect: on / off" and,
           from the Pack, "Take it off the Pack" and « Collectors. A category lists every kind with a balance (icon, name, ×count,
           eight a page); a kind's page shows the item and its balance: Take a stack, Take all (into your inventory, the rest at your
           feet), Deposit all of these, « back. Every button brings the same page back.
AUTO-COLLECT  (off at first for the Stone Collector and the Wood Box; on for the Jar and the Magnet, which always collected) while
           it's carried - inventory, off hand, or on the Rat Pack: once a second, its kinds of dropped item within 8 blocks go in,
           and so do its kinds in your main inventory rows (slots 9-35: never the hotbar or the off hand - what you build with
           stays in hand). Never in a heist or the gutter. Only plain vanilla items (no custom data, name or enchantments) - never
           a pack item. The switch is the account's (per player, per kind), not the item's.
WHAT EACH TAKES  the Stone Collector: full stone blocks (never stairs, slabs or walls) - Natural, Polished, Bricks, Chiseled (the
           columns go there). The Wood Box: Logs, Stripped logs, Planks. The Ore Magnet: Ores, Raw & ingots, Gems & dusts. The
           Spirit Jar: Monster drops, Animal goods, Fish & sea, Rare (its 3.0 list, less the gear that wears or varies - the bows,
           swords, the trident and the goat horn: an account can't keep their wear or kind).
MOVING OVER (lossless) every old Spirit Jar and Ore Magnet with a container - in a pocket, the off hand, on the Pack's old lists
           (rb_sj / rb_om), or unfolded as a barrel (folded first): each stack it takes goes into the owner's account, anything
           else is handed back at their feet (Owner set, no pickup delay), the container is removed and the item marked bm_cb.
           The Pack keeps the first of each; the others come back as items, now empty. One chat line says what happened.
BALANCES   storage bm:cb p<pid>.k<kind>.i<item> (an int); the switch, score bm.cba_<kind> (1 on, 2 off, unset: the kind's default).
Codes 9250-9699 (p278/act, each line menu-checked): 9260-9263 a category, 9264 deposit everything, 9265 auto-collect, 9266
« Collectors, 9267/9268 ‹ Previous / Next ›, 9269 « (the front page), 9270 take a stack, 9271 take all, 9272 deposit all of
these, 9273 « (the category), 9274-9277 a row on the Rat Pack's Collectors page, 9278 take it off the Pack, 9300+g a kind's row."""
import json, os
from items import item, T, TOTEM, ITEMS, DYNAMIC
from useitem import hold, HOLD
from nbt import snbt, B, Int

MC = '/home/claude/mc263/'
VAN = MC + 'client/assets/minecraft/textures/'
_REG = set(x.split(':')[-1] for x in json.load(open(MC + 'registries.json'))['item'])
_COMP = json.load(open(MC + 'item_components.json'))
ok = lambda xs: [x for x in xs if x in _REG]
WOODS = ['oak', 'spruce', 'birch', 'jungle', 'acacia', 'dark_oak', 'mangrove', 'cherry', 'pale_oak']
FUNGI = ['crimson', 'warped']

KINDS = {   # key: (item, name, colour, [(category, [items])], auto-collect at first)
    'stone': ('stone_collector', 'Stone Collector', '#a8a8b0', [
        ('Natural', ok(['stone', 'cobblestone', 'mossy_cobblestone', 'granite', 'diorite', 'andesite', 'deepslate', 'cobbled_deepslate', 'tuff',
                        'calcite', 'dripstone_block', 'blackstone', 'basalt', 'smooth_basalt', 'netherrack', 'end_stone', 'sandstone', 'red_sandstone',
                        'obsidian'])),
        ('Polished', ok(['polished_granite', 'polished_diorite', 'polished_andesite', 'polished_deepslate', 'polished_tuff', 'polished_blackstone',
                         'polished_basalt', 'smooth_stone', 'smooth_sandstone', 'smooth_red_sandstone', 'cut_sandstone', 'cut_red_sandstone',
                         'smooth_quartz', 'quartz_block', 'purpur_block'])),
        ('Bricks', ok(['stone_bricks', 'mossy_stone_bricks', 'cracked_stone_bricks', 'deepslate_bricks', 'cracked_deepslate_bricks', 'deepslate_tiles',
                       'cracked_deepslate_tiles', 'tuff_bricks', 'polished_blackstone_bricks', 'cracked_polished_blackstone_bricks', 'nether_bricks',
                       'cracked_nether_bricks', 'red_nether_bricks', 'end_stone_bricks', 'bricks', 'mud_bricks', 'prismarine_bricks', 'quartz_bricks',
                       'resin_bricks'])),
        ('Chiseled', ok(['chiseled_stone_bricks', 'chiseled_deepslate', 'chiseled_tuff', 'chiseled_tuff_bricks', 'chiseled_polished_blackstone',
                         'chiseled_sandstone', 'chiseled_red_sandstone', 'chiseled_nether_bricks', 'chiseled_quartz_block', 'quartz_pillar',
                         'purpur_pillar', 'chiseled_resin_bricks']))], False),
    'wood': ('wood_box', 'Wood Box', '#c89a5a', [
        ('Logs', ok([f'{w}_log' for w in WOODS] + [f'{w}_wood' for w in WOODS] + [f'{f}_stem' for f in FUNGI] + [f'{f}_hyphae' for f in FUNGI] + ['bamboo_block'])),
        ('Stripped logs', ok([f'stripped_{w}_log' for w in WOODS] + [f'stripped_{w}_wood' for w in WOODS] + [f'stripped_{f}_stem' for f in FUNGI] +
                             [f'stripped_{f}_hyphae' for f in FUNGI] + ['stripped_bamboo_block'])),
        ('Planks', ok([f'{w}_planks' for w in WOODS + FUNGI] + ['bamboo_planks', 'bamboo_mosaic']))], False),
    'ore': ('ore_magnet', "Dennis's Ore Magnet", '#e8b04a', [
        ('Ores', ok([f'{p}{o}_ore' for o in ('coal', 'iron', 'copper', 'gold', 'redstone', 'lapis', 'diamond', 'emerald') for p in ('', 'deepslate_')] +
                    ['nether_gold_ore', 'nether_quartz_ore', 'ancient_debris'])),
        ('Raw & ingots', ok(['raw_copper', 'raw_iron', 'raw_gold', 'copper_ingot', 'iron_ingot', 'gold_ingot', 'iron_nugget', 'gold_nugget',
                             'netherite_scrap', 'raw_iron_block', 'raw_gold_block', 'raw_copper_block'])),
        ('Gems & dusts', ok(['coal', 'charcoal', 'redstone', 'lapis_lazuli', 'quartz', 'amethyst_shard', 'diamond', 'emerald', 'flint',
                             'glowstone_dust', 'echo_shard']))], True),
    'mob': ('spirit_jar', "Pistachio's Spirit Jar", '#9ae8c8', [
        ('Monster drops', ok(['rotten_flesh', 'bone', 'bone_meal', 'string', 'spider_eye', 'gunpowder', 'slime_ball', 'ender_pearl', 'blaze_rod',
                              'blaze_powder', 'magma_cream', 'phantom_membrane', 'breeze_rod', 'wind_charge', 'arrow', 'ghast_tear', 'shulker_shell',
                              'sugar', 'glass_bottle', 'stick', 'carrot', 'potato'])),
        ('Animal goods', ok(['leather', 'feather', 'rabbit_hide', 'rabbit_foot', 'beef', 'porkchop', 'mutton', 'chicken', 'rabbit', 'egg', 'honeycomb',
                             'armadillo_scute', 'turtle_scute'] +
                            [f'{c}_wool' for c in ('white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan',
                                                   'purple', 'blue', 'brown', 'green', 'red', 'black')])),
        ('Fish & sea', ok(['cod', 'salmon', 'tropical_fish', 'pufferfish', 'ink_sac', 'glow_ink_sac', 'prismarine_shard', 'prismarine_crystals',
                           'nautilus_shell'])),
        ('Rare', ok(['wither_skeleton_skull', 'skeleton_skull', 'zombie_head', 'creeper_head', 'piglin_head', 'totem_of_undying', 'heavy_core',
                     'trial_key', 'saddle']))], True)}
ORDER = ['stone', 'wood', 'ore', 'mob']
# (the jar's 3.0 list also had iron_ingot, gold_nugget, copper_ingot and emerald: the Magnet keeps those now - one home for each)
_dup = set(KINDS['ore'][3][1][1]) | set(KINDS['ore'][3][2][1])
KINDS['mob'][3][0] = (KINDS['mob'][3][0][0], [x for x in KINDS['mob'][3][0][1] if x not in _dup])
TYPES = []                                  # global index g -> (kind, category index, item)
for _k in ORDER:
    for _ci, (_cn, _xs) in enumerate(KINDS[_k][3]):
        for _x in _xs: TYPES.append((_k, _ci, _x))
assert len(TYPES) <= 400, len(TYPES)
PLAIN = '[!minecraft:custom_data,!minecraft:custom_name,!minecraft:enchantments]'
MENU_F, MENU_C, MENU_I = 9250, 9251, 9252
B_CAT0, B_DEPALL, B_AUTO, B_BACKP, B_PREV, B_NEXT, B_BACKF = 9260, 9264, 9265, 9266, 9267, 9268, 9269
B_STACK, B_ALL, B_DEP1, B_BACKC, B_ROWP0, B_OFF, B_ROW0 = 9270, 9271, 9272, 9273, 9274, 9278, 9300
PRICE = ('token', 16)

# ------------------------------------------------------------------ the two new items (the Fence); the Jar and the Magnet: no container now
for _k in ('stone', 'wood'):
    _iid, _nm, _col, _cats, _auto = KINDS[_k]
    _what = 'stone blocks' if _k == 'stone' else 'logs, stripped logs and planks'
    item(_iid, TOTEM, _nm, _col, [('A sturdy little crate that keeps an account.' if _k == 'stone' else 'A plank crate with a log end showing.'),
                                  ('Use it: its account - every kind of', 'blue'), (f'{_what} it keeps, by category.', 'blue'),
                                  ('Auto-collect (off at first): carried, it', 'blue'), ('takes them up within 8 blocks.', 'blue'),
                                  ('Any copy opens the same account.', 'gray'), (f'{PRICE[1]} Tokens, from the Fence.', 'dark_gray')],
         model=f'bm:{_iid}', stack=1, cat='builder', comps=hold('none'), custom_extra={'bm_cb': B(1)})
    HOLD[_iid] = f'bm:p278/use/{_k}'
import economy as _ECON
for _k in ('stone', 'wood'): _ECON.DIRECT[KINDS[_k][0]] = (PRICE, None)


def rework_items():
    """the Jar and the Magnet (phase174's items): an account's key now - no container, and their use opens the account"""
    for k in ('ore', 'mob'):
        iid = KINDS[k][0]
        if iid not in ITEMS: continue
        c = ITEMS[iid]['comps']
        c.pop('minecraft:container', None)
        ITEMS[iid]['custom']['bm_cb'] = B(1)
        c['minecraft:custom_data']['bm_cb'] = B(1)
        nm = KINDS[k][1]
        c['minecraft:lore'] = [T(l, 'gray') if isinstance(l, str) else T(*l) for l in [
            ('A horseshoe of dwarf-iron that hums near ore.' if k == 'ore' else 'A little jar with something polite inside.'),
            ('Use it: its account - every kind it keeps,', 'blue'), ('by category. Take a stack, or all of it.', 'blue'),
            ('Auto-collect (on): carried, it takes them', 'blue'), ('up within 8 blocks.', 'blue'), ('Any copy opens the same account.', 'gray'),
            ('"Saves the knees, lad."' if k == 'ore' else '"It insists on carrying them, sir."', 'dark_gray')]] + [c['minecraft:lore'][-1]]
        HOLD[iid] = f'bm:p278/use/{k}'


rework_items()


def extend_offers(O, offer):
    for k in ('stone', 'wood'): O['fence'].append(offer(PRICE, (KINDS[k][0], 1)))


# ------------------------------------------------------------------ the icons (16 x 16, the pack's style)
def _grid(rows, pal):
    from PIL import Image
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in pal:
                h = pal[ch].lstrip('#'); px[x, y] = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
    return im


def stone_icon():
    # a small stone crate in four bands - natural (cobbled), polished, bricks, chiseled (a carved ring) - a chisel's notch on its lid
    rows = ['................',
            '...oooooooooo...',
            '..oHHHHHHHHHHo..',
            '..oHaAaaAaaaGo..',
            '..oaAaaaAaAaGo..',
            '..odddddddddGo..',
            '..oBBBBBBBBBGo..',
            '..obbbbbbbbbGo..',
            '..ommmmmmmmmmo..',
            '..ocCcmcCccmGo..',
            '..occmcccmccGo..',
            '..ommmmmmmmmmo..',
            '..oeeEKKEeeeGo..',
            '..oeEKeeKEeeGo..',
            '...oggggggggo...',
            '....oooooooo....']
    return _grid(rows, {'o': '#202026', 'H': '#d0d0d8', 'a': '#7e7e86', 'A': '#9c9ca6', 'd': '#55555c', 'B': '#c4c4cc', 'b': '#a8a8b2',
                        'm': '#4a4248', 'c': '#a08e84', 'C': '#bca898', 'e': '#86868f', 'E': '#9a9aa4', 'K': '#e0e0ec', 'G': '#62626a', 'g': '#3e3e46'})


def wood_icon():
    # a little plank crate (dark grain, brass corner nails) with a log end showing at its side - its rings and bark
    rows = ['................',
            '..ooooooooooo...',
            '..onPPPPPPPno...',
            '..oppPpppPppo...',
            '..ommmmmmmmmo...',
            '..oPPpPPPpPPoooo',
            '..opppppppppbRRb',
            '..ommmmmmmmmRwWR',
            '..oPPPpPPPPPRWwR',
            '..opppppPpppbRRb',
            '..ommmmmmmmmoooo',
            '..oPPpPPPPpPo...',
            '..onpppppppno...',
            '..ooooooooooo...',
            '................',
            '................']
    return _grid(rows, {'o': '#2e1c0c', 'P': '#d8a868', 'p': '#b8864a', 'm': '#6a4422', 'n': '#ffd870', 'b': '#4a2e14', 'R': '#c8985a',
                        'w': '#8a6034', 'W': '#e8c890'})


def rp(R):
    R.ICONS['stone_collector'] = stone_icon()
    R.ICONS['wood_box'] = wood_icon()


# ------------------------------------------------------------------ a kind's picture in a row (the items atlas, or a block's face)
def sprite(x):
    for cand in (f'item/{x}', f'block/{x}', f'block/{x}_side', f'block/{x.replace("_wood", "_log").replace("_hyphae", "_stem")}',
                 f'block/{x}_front', f'block/{x}_top', {'smooth_quartz': 'block/quartz_block_bottom', 'smooth_sandstone': 'block/sandstone_top',
                                                        'smooth_red_sandstone': 'block/red_sandstone_top', 'quartz_block': 'block/quartz_block_side'}.get(x, '')):
        if cand and os.path.exists(VAN + cand + '.png'):
            atlas = 'minecraft:items' if cand.startswith('item/') else 'minecraft:blocks'
            return {'type': 'object', 'object': 'atlas', 'atlas': atlas, 'sprite': f'minecraft:{cand}', 'fallback': {'text': '◆', 'color': 'gray'}}
    return {'text': '◆', 'color': 'gray', 'italic': False}


def tkey(x):
    return (_COMP.get(x, {}).get('minecraft:item_name') or {}).get('translate', f'item.minecraft.{x}')


def mstack(x):
    return int(_COMP.get(x, {}).get('minecraft:max_stack_size', 64))


def generate(G):
    import phase28 as P28
    import phase277 as P277
    F, fn, tellraw, title = G.FUNCS, G.fn, G.tellraw, G.title
    say = lambda c: title('@s', 'actionbar', c)
    click = 'playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4'
    page_turn = 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.2'
    pid = 'execute store result storage bm:rp c.pid int 1 run scoreboard players get @s bm.pid'
    on_txt, off_txt = T('on', 'white', bold=True), T('off', '#ff8a8a', bold=True)
    holds = lambda iid, x='': f'*[minecraft:custom_data~{{bm:"{iid}"}}{x}]'
    second, load = F['loop/second'], F['load']
    PRE = P277.PRE
    objs = ['bm.cbk', 'bm.cbc', 'bm.cbi', 'bm.pg_cb', 'bm.cbmig'] + [f'bm.cba_{k}' for k in ORDER] + [f'bm.rcb_{k}' for k in ORDER]
    load[-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    rep = {'kinds': len(TYPES)}

    # ---------------------------------------------------------------- what each takes: an item tag per kind; the kinds' list for the macros
    for k in ORDER:
        G.wjson(f'bm/tags/item/cb_{k}.json', {'values': [f'minecraft:{x}' for (kk, ci, x) in TYPES if kk == k]})
    load.append('data modify storage bm:cbdef t set value ' + snbt([{'k': k, 'n': x, 'id': f'minecraft:{x}', 'm': Int(mstack(x))} for (k, ci, x) in TYPES]))
    has_ = lambda k: f'#bm:cb_{k}{PLAIN}'

    # ---------------------------------------------------------------- the balance (macro: pid, k = the kind, n = the item, c = how many to add)
    fn('p278/add', ['$execute store result score #cbb bm.rng run data get storage bm:cb p$(pid).k$(k).i$(n)',
                    'scoreboard players operation #cbb bm.rng += #cbc bm.rng',
                    '$execute store result storage bm:cb p$(pid).k$(k).i$(n) int 1 run scoreboard players get #cbb bm.rng'])
    # (one item entity -> its owner's account: its kind and count, then gone; #cbc, the count; bm:rp c.k, the kind; c.pid the owner)
    fn('p278/take_ent', ['data modify storage bm:rp c.n set string entity @s Item.id 10', 'scoreboard players set #cbc bm.rng 1',
                         'execute store result score #cbc bm.rng run data get entity @s Item.count', 'scoreboard players operation #cbn bm.rng += #cbc bm.rng',
                         'function bm:p278/add with storage bm:rp c', 'kill @s'])
    # (one inventory slot -> the account)
    fn('p278/take_slot', ['$data modify storage bm:rp c.n set string entity @s Inventory[{Slot:$(s)b}].id 10',
                          '$execute store result score #cbc bm.rng run data get entity @s Inventory[{Slot:$(s)b}].count',
                          'scoreboard players operation #cbn bm.rng += #cbc bm.rng',
                          'function bm:p278/add with storage bm:rp c', '$item replace entity @s container.$(s) with minecraft:air'])

    # ---------------------------------------------------------------- who carries which (each second): pockets, off hand, the Pack
    for k in ORDER:
        iid = KINDS[k][0]
        H = holds(iid)
        second += [f'tag @a remove bm.cbh_{k}', f'execute as @a if items entity @s container.* {H} run tag @s add bm.cbh_{k}',
                   f'execute as @a if items entity @s weapon.offhand {H} run tag @s add bm.cbh_{k}',
                   f'tag @a[tag=bm.pwc,scores={{bm.rcb_{k}=1}}] add bm.cbh_{k}']
        on = f'unless score @s bm.cba_{k} matches 2' if KINDS[k][4] else f'if score @s bm.cba_{k} matches 1'
        second.append(f'execute as @a[tag=bm.cbh_{k},tag=!bm.gvp,tag=!bm.gvdead,gamemode=!spectator,scores={{bm.pid=1..}}] {on} at @s '
                      f'unless dimension bm:gutter run function bm:p278/c/{k}')
        fn(f'p278/c/{k}', [pid, f'data modify storage bm:rp c.k set value "{k}"', 'scoreboard players set #cbn bm.rng 0',
                           f'execute as @e[type=minecraft:item,distance=..8,tag=!bm.rqwd,nbt={{PickupDelay:0s}}] if items entity @s contents {has_(k)} run function bm:p278/take_ent'] +
           [f'execute if items entity @s container.{s} {has_(k)} run function bm:p278/take_slot {{s:{s}}}' for s in range(9, 36)] +
           ['execute if score #cbn bm.rng matches 1.. run playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.3 0.7'])

    # ---------------------------------------------------------------- THE ACCOUNT: front page
    for k in ORDER:
        iid, nm, col, cats, auto = KINDS[k]
        st = [f'scoreboard players set @s bm.menu {MENU_F}', f'scoreboard players set @s bm.cbk {ORDER.index(k)}', pid, 'data remove storage bm:ui cb',
              'scoreboard players set #cbt bm.rng 0']
        for ci, (cn, xs) in enumerate(cats):
            st += ['scoreboard players set #cbs bm.rng 0']
            st += [f'function bm:p278/sum2 {{k:"{k}",n:"{x}"}}' for x in xs]
            st += [f'execute store result storage bm:ui cb.c{ci} int 1 run scoreboard players get #cbs bm.rng', 'scoreboard players operation #cbt bm.rng += #cbs bm.rng']
        st += ['execute store result storage bm:ui cb.tot int 1 run scoreboard players get #cbt bm.rng',
               f'data modify storage bm:ui cb.r_au set value {snbt(on_txt if auto else off_txt)}',
               f'execute if score @s bm.cba_{k} matches 1 run data modify storage bm:ui cb.r_au set value {snbt(on_txt)}',
               f'execute if score @s bm.cba_{k} matches 2 run data modify storage bm:ui cb.r_au set value {snbt(off_txt)}',
               'data modify storage bm:ui cb.acts set value []']
        cb = [P28.btn([sprite(cats[ci][1][0]) if cats[ci][1] else T('◆ ', col), T(f' {cn}', 'white'), T(' ›', 'gray'), T(f'  $(c{ci})', 'dark_gray')], B_CAT0 + ci, width=150,
                      tooltip=T(f'{cn}: every kind it keeps there, with its count', 'gray')) for ci, (cn, xs) in enumerate(cats)]
        cb += [P28.btn([T('⬇ ', col), T('Deposit everything', 'white')], B_DEPALL, width=150, tooltip=T('Everything in your inventory it takes goes into the account', 'gray')),
               P28.btn([T('Auto-collect: ', 'gray'), '@@RAW:r_au@@'], B_AUTO, width=150,
                       tooltip=T('On: carried (or on the Rat Pack), it takes up its kinds within 8 blocks, and from your inventory\'s main rows (never the hotbar), once a second.', 'gray'))]
        fa = [('$' if '$(' in P28.inline(b) else '') + f'data modify storage bm:ui cb.acts append value {P28.inline(b)}' for b in cb]
        fa += [f'execute if entity @s[tag=bm.cbfp] run data modify storage bm:ui cb.acts append value ' +
               snbt(P28.btn([T('↩ ', 'white'), T('Take it off the Pack', 'white')], B_OFF, width=150, tooltip=T(f'Your {nm} comes off the Rat Pack (its account stays yours)', 'gray'))),
               f'execute if entity @s[tag=bm.cbfp] run data modify storage bm:ui cb.acts append value ' +
               snbt(P28.btn([T('« Collectors', 'gray')], B_BACKP, width=150, tooltip=T('Back to the Rat Pack\'s Collectors page', 'gray')))]
        fn(f'p278/front_acts/{k}', fa)
        d = P28.multi([T(nm.upper(), col, bold=True), T('  ·  its account', 'gray')],
                      [P28.body([T('Kept for you, not in the item: any copy of it opens the same account. ', 'gray'), T('In it: ', 'gray'), T('$(tot)', 'white', bold=True)], 300)],
                      '@@ACTS@@', columns=2)
        fn(f'p278/front_dlg/{k}', ['$dialog show @s ' + snbt(d).replace('"@@ACTS@@"', '$(acts)')])
        fn(f'p278/front/{k}', st + [f'function bm:p278/front_acts/{k} with storage bm:ui cb', f'function bm:p278/front_dlg/{k} with storage bm:ui cb', page_turn])
        # use: from a hand (no « Collectors) - an old one moves over first
        fn(f'p278/use/{k}', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'tag @s remove bm.cbfp', 'function bm:p278/mig/now',
                             f'function bm:p278/front/{k}'])
        fn(f'p278/frompack/{k}', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', f'execute unless score @s bm.rcb_{k} matches 1 run return run function bm:p28/stale',
                                  'tag @s add bm.cbfp', f'function bm:p278/front/{k}'])
    fn('p278/sum', ['scoreboard players set #cbx bm.rng 0', '$execute store result score #cbx bm.rng run data get storage bm:cb p$(pid).k$(k).i$(n)',
                    'scoreboard players operation #cbs bm.rng += #cbx bm.rng'])
    # (the front page's sums: the inline compound names the kind and item; the pid is in bm:rp c)
    fn('p278/sum2', ['$data modify storage bm:rp c.k set value "$(k)"', '$data modify storage bm:rp c.n set value "$(n)"', 'function bm:p278/sum with storage bm:rp c'])

    # ---------------------------------------------------------------- a category's page: a row per kind with a balance
    for g, (k, ci, x) in enumerate(TYPES):
        b = P28.btn([sprite(x), T(' ', 'white'), {'translate': tkey(x), 'color': 'white', 'italic': False}, T(' ×$(c)', 'gray')], B_ROW0 + g, width=150,
                    tooltip=T('Press: take a stack, take all, or deposit more', 'gray'))
        fn(f'p278/r/{g}', [f'$execute store result score #cbx bm.rng run data get storage bm:cb p$(pid).k{k}.i{x}', 'execute if score #cbx bm.rng matches ..0 run return 0',
                           'execute store result storage bm:rp rc.c int 1 run scoreboard players get #cbx bm.rng', f'function bm:p278/rb/{g} with storage bm:rp rc'])
        fn(f'p278/rb/{g}', [f'$data modify storage bm:tmp cb.acts append value {snbt(b)}'])
    dim = lambda txt, code: P28.btn([T(txt, 'dark_gray')], code, width=150, tooltip=T('(no more this way)', 'dark_gray'))
    fn('p278/nav', ['execute if score #pgp bm.rng matches 1.. run data modify storage bm:tmp cb.acts append value ' + snbt(P28.btn([T('‹ Previous', 'white')], B_PREV, width=150, tooltip=T('The page before.', 'gray'))),
                    'execute if score #pgp bm.rng matches ..0 run data modify storage bm:tmp cb.acts append value ' + snbt(dim('‹ Previous', B_PREV)),
                    '$execute if score #pgp bm.rng < #pgl bm.rng run data modify storage bm:tmp cb.acts append value ' + snbt(P28.btn([T('Next ›', 'white'), T('  $(p)/$(n)', 'gray')], B_NEXT, width=150, tooltip=T('The next page.', 'gray'))),
                    '$execute if score #pgp bm.rng >= #pgl bm.rng run data modify storage bm:tmp cb.acts append value ' + snbt(P28.btn([T('Next ›', 'dark_gray'), T('  $(p)/$(n)', 'dark_gray')], B_NEXT, width=150, tooltip=T('(no more this way)', 'dark_gray')))])
    for k in ORDER:
        iid, nm, col, cats, auto = KINDS[k]
        back = P28.btn([T(f'« {nm.split(chr(39) + "s ")[-1]}', 'gray')], B_BACKF, width=150, tooltip=T('Back to its front page', 'gray'))
        for ci, (cn, xs) in enumerate(cats):
            L = [f'scoreboard players set @s bm.menu {MENU_C}', f'scoreboard players set @s bm.cbk {ORDER.index(k)}', f'scoreboard players set @s bm.cbc {ci}',
                 pid, 'data modify storage bm:tmp cb.acts set value []', 'data modify storage bm:rp t.pid set from storage bm:rp c.pid']
            L += [f'function bm:p278/r/{g} with storage bm:rp c' for g, (kk, cc, x) in enumerate(TYPES) if kk == k and cc == ci]
            empty = P28.multi([T(nm.upper(), col, bold=True), T(f'  ·  {cn}', 'gray')], [P28.body([T('(nothing yet) ', 'white'),
                              T('Deposit some, or switch Auto-collect on and carry it.', 'gray')], 300)], [back], columns=2)
            L += [f'execute unless data storage bm:tmp cb.acts[0] run return run dialog show @s {snbt(empty)}',
                  'scoreboard players operation #pgp bm.rng = @s bm.pg_cb', 'scoreboard players set #pgN bm.rng 8',
                  'data modify storage bm:ui pg.src set from storage bm:tmp cb.acts', 'function bm:p261/pg/run',
                  'scoreboard players operation @s bm.pg_cb = #pgp bm.rng', 'data modify storage bm:tmp cb.acts set from storage bm:ui pg.out',
                  'execute if score #pgn bm.rng matches 2.. run function bm:p278/nav with storage bm:ui pg',
                  f'data modify storage bm:tmp cb.acts append value {snbt(back)}', f'function bm:p278/cat_dlg/{k}{ci} with storage bm:tmp cb', page_turn]
            d = P28.multi([T(nm.upper(), col, bold=True), T(f'  ·  {cn}', 'gray')], [P28.body([T('Press a kind: take a stack, take all, or deposit more.', 'gray')], 300)], '@@ACTS@@', columns=2)
            fn(f'p278/cat_dlg/{k}{ci}', ['$dialog show @s ' + snbt(d).replace('"@@ACTS@@"', '$(acts)')])
            fn(f'p278/cat/{k}{ci}', L)
    fn('p278/cat', [f'execute if score @s bm.cbk matches {ORDER.index(k)} if score @s bm.cbc matches {ci} run return run function bm:p278/cat/{k}{ci}'
                    for k in ORDER for ci in range(len(KINDS[k][3]))])
    fn('p278/front', [f'execute if score @s bm.cbk matches {ORDER.index(k)} run return run function bm:p278/front/{k}' for k in ORDER])

    # ---------------------------------------------------------------- a kind's page: the item, its balance, its buttons
    fn('p278/sel', [pid, 'execute store result storage bm:rp c.g int 1 run scoreboard players get @s bm.cbi', 'function bm:p278/sel2 with storage bm:rp c'])
    fn('p278/sel2', ['$data modify storage bm:rp c.k set from storage bm:cbdef t[$(g)].k', '$data modify storage bm:rp c.n set from storage bm:cbdef t[$(g)].n',
                     '$data modify storage bm:rp c.m set from storage bm:cbdef t[$(g)].m', '$data modify storage bm:rp c.id set from storage bm:cbdef t[$(g)].id'])
    ib = [P28.btn([T('⬆ ', 'white'), T('Take a stack', 'white')], B_STACK, width=150, tooltip=T('One stack into your inventory (at your feet if it\'s full)', 'gray')),
          P28.btn([T('⬆ ', 'white'), T('Take all', 'white')], B_ALL, width=150, tooltip=T('All of it into your inventory - the rest at your feet', 'gray')),
          P28.btn([T('⬇ ', 'white'), T('Deposit all of these', 'white')], B_DEP1, width=150, tooltip=T('Every one of these in your inventory goes in', 'gray')),
          P28.btn([T('« Back', 'gray')], B_BACKC, width=150, tooltip=T('Back to the category', 'gray'))]
    idlg = P28.multi([{'translate': '$(tk)', 'color': 'white', 'bold': True, 'italic': False}, T('  ·  in your account', 'gray')],
                     '@@BODY@@', ib, columns=2)
    fn('p278/item_dlg', ['$dialog show @s ' + snbt(idlg).replace('"@@BODY@@"', '$(body)')])
    fn('p278/item', [f'scoreboard players set @s bm.menu {MENU_I}', 'function bm:p278/sel', 'function bm:p278/item2 with storage bm:rp c'])
    fn('p278/item2', ['data modify storage bm:ui cbi set value {body:[]}', '$data modify storage bm:ui cbi.nm set value "$(n)"',
                      '$execute store result storage bm:ui cbi.c int 1 run data get storage bm:cb p$(pid).k$(k).i$(n)',
                      '$data modify storage bm:ui cbi.body append value {type:"minecraft:item",item:{id:"minecraft:$(n)",count:1},show_decorations:0b,show_tooltip:1b,width:16,height:16}',
                      'function bm:p278/item3 with storage bm:ui cbi', 'function bm:p278/item_dlg with storage bm:ui cbi', page_turn])
    fn('p278/item3', ['$data modify storage bm:ui cbi.body append value {type:"minecraft:plain_message",contents:[{text:"In your account: ",color:"gray",italic:false},{text:"$(c)",color:"white",italic:false,bold:true}],width:300}'])
    F['p278/item2'].insert(2, '$data modify storage bm:ui cbi.tk set from storage bm:cbdef tk[$(g)]')
    load.append('data modify storage bm:cbdef tk set value ' + snbt([tkey(x) for (k, ci, x) in TYPES]))
    # take a stack / all; deposit all of these
    fn('p278/take', ['$execute store result score #cbb bm.rng run data get storage bm:cb p$(pid).k$(k).i$(n)', 'execute if score #cbb bm.rng matches ..0 run return 0',
                     '$scoreboard players set #cbm bm.rng $(m)', 'scoreboard players operation #cbt bm.rng = #cbm bm.rng', 'scoreboard players operation #cbt bm.rng < #cbb bm.rng',
                     'execute store result storage bm:rp c.c int 1 run scoreboard players get #cbt bm.rng', 'function bm:p278/give with storage bm:rp c',
                     'scoreboard players operation #cbb bm.rng -= #cbt bm.rng',
                     '$execute store result storage bm:cb p$(pid).k$(k).i$(n) int 1 run scoreboard players get #cbb bm.rng', 'return 1'])
    fn('p278/give', ['$give @s $(id) $(c)'])
    fn('p278/take_all', ['execute store result score #cbr bm.rng run function bm:p278/take with storage bm:rp c', 'execute if score #cbr bm.rng matches 0 run return 0',
                         'scoreboard players add #cbl bm.rng 1', 'execute if score #cbl bm.rng matches ..400 run function bm:p278/take_all'])
    fn('p278/dep1', ['$execute store result score #cbc bm.rng run clear @s $(id)' + PLAIN, 'function bm:p278/add with storage bm:rp c'])
    fn('p278/do_stack', ['function bm:p278/sel', 'execute store result score #cbr bm.rng run function bm:p278/take with storage bm:rp c', click,
                         'execute if score #cbr bm.rng matches 0 run ' + say(T('None left.', 'gray')), 'function bm:p278/item'])
    fn('p278/do_all', ['function bm:p278/sel', 'scoreboard players set #cbl bm.rng 0', 'function bm:p278/take_all', click, 'function bm:p278/item'])
    fn('p278/do_dep1', ['function bm:p278/sel', 'function bm:p278/dep1 with storage bm:rp c', click,
                        'execute if score #cbc bm.rng matches 0 run ' + say(T('None of these in your inventory (plain ones only).', 'gray')), 'function bm:p278/item'])
    # deposit everything it takes (the whole inventory)
    for k in ORDER:
        L = [pid, f'data modify storage bm:rp c.k set value "{k}"', 'scoreboard players set #cbn bm.rng 0']
        for (kk, ci, x) in TYPES:
            if kk != k: continue
            L += [f'execute store result score #cbc bm.rng run clear @s minecraft:{x}{PLAIN}',
                  f'execute if score #cbc bm.rng matches 1.. run data modify storage bm:rp c.n set value "{x}"',
                  'execute if score #cbc bm.rng matches 1.. run scoreboard players operation #cbn bm.rng += #cbc bm.rng',
                  'execute if score #cbc bm.rng matches 1.. run function bm:p278/add with storage bm:rp c']
        fn(f'p278/depall/{k}', L)
    fn('p278/do_depall', [click] + [f'execute if score @s bm.cbk matches {ORDER.index(k)} run function bm:p278/depall/{k}' for k in ORDER] +
       ['execute if score #cbn bm.rng matches 0 run ' + say(T('Nothing in your inventory it takes (plain ones only).', 'gray')),
        'execute if score #cbn bm.rng matches 1.. run ' + say([T('Deposited ', '#9ae8c8'), {'score': {'name': '#cbn', 'objective': 'bm.rng'}, 'color': 'white'}, T(' items.', '#9ae8c8')]),
        'function bm:p278/front'])
    for k in ORDER:
        auto = KINDS[k][4]
        fn(f'p278/auto/{k}', [click] + ([f'execute unless score @s bm.cba_{k} matches 2 run return run function bm:p278/auto_set/{k}2', f'function bm:p278/auto_set/{k}1'] if auto else
                                        [f'execute if score @s bm.cba_{k} matches 1 run return run function bm:p278/auto_set/{k}2', f'function bm:p278/auto_set/{k}1']))
        for v in (1, 2): fn(f'p278/auto_set/{k}{v}', [f'scoreboard players set @s bm.cba_{k} {v}', 'function bm:p278/front'])
    fn('p278/do_auto', [f'execute if score @s bm.cbk matches {ORDER.index(k)} run return run function bm:p278/auto/{k}' for k in ORDER])

    # ================================================================== ON THE RAT PACK: one each (storage bm:pw p<pid>.rcb_<kind>, score bm.rcb_<kind>)
    for k in ORDER:
        iid, nm, col, cats, auto = KINDS[k]
        told = tellraw('@s', PRE + [T(ITEMS[iid]['name'], col, bold=True), T(' goes on your Rat Pack (Collectors page). ', 'gray'), T('(Its account goes everywhere with you.)', 'dark_gray')])
        fn(f'p278/pk/add_{k}', [f'execute if score @s bm.rcb_{k} matches 1 run return run ' + say([T(ITEMS[iid]['name'], col), T(' is on your Rat Pack already - one is all it needs.', 'gray')]),
                                'function bm:p278/mig/now', pid, f'function bm:p278/pk/put_{k} with storage bm:rp c', 'item replace entity @s weapon.offhand with minecraft:air',
                                f'scoreboard players set @s bm.rcb_{k} 1', 'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.6 1.6', told])
        fn(f'p278/pk/put_{k}', [f'$data modify storage bm:pw p$(pid).rcb_{k} set from entity @s equipment.offhand',
                                f'$data remove storage bm:pw p$(pid).rcb_{k}.components."minecraft:custom_data".bm_rpno'])
        fn(f'p278/pk/off_{k}', [f'execute unless score @s bm.rcb_{k} matches 1 run return run function bm:p28/stale', pid, f'function bm:p278/pk/give_{k} with storage bm:rp c',
                                f'scoreboard players set @s bm.rcb_{k} 0', 'tag @s remove bm.cbfp', 'playsound minecraft:item.armor.equip_chain player @s ~ ~ ~ 0.6 1.4',
                                tellraw('@s', PRE + [T(ITEMS[iid]['name'], col, bold=True), T(' comes off your Rat Pack (its account stays yours).', 'gray')]), 'function bm:p277/b/cols'])
        fn(f'p278/pk/give_{k}', [f'$execute unless data storage bm:pw p$(pid).rcb_{k} run return run {G.give(iid)}',
                                 'summon minecraft:item ~ ~0.4 ~ {Tags:["bm.rqout"],PickupDelay:0s,Item:{id:"minecraft:paper",count:1}}',
                                 f'$data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Item set from storage bm:pw p$(pid).rcb_{k}',
                                 'data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Item.components."minecraft:custom_data".bm_rpno set value 1b',
                                 'data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Owner set from entity @s UUID',
                                 'tag @e[type=minecraft:item,tag=bm.rqout] remove bm.rqout', f'$data remove storage bm:pw p$(pid).rcb_{k}'])
        # auto-pack (the Pack's "Collectors" switch): one, if none is on
        fn(f'p278/pk/ap_{k}', [f'data modify storage bm:rp a.id set value "{iid}"', 'execute unless function bm:p277/ap/find run return 0',
                               f'data modify storage bm:rp a.k set value "cb_{k}"', 'function bm:p277/ap/mv with storage bm:rp a', f'scoreboard players set @s bm.rcb_{k} 1',
                               tellraw('@s', PRE + [T(ITEMS[iid]['name'], col, bold=True), T(' is on your Rat Pack now (Collectors page). ', 'gray'), T('Take it out any time from there.', 'dark_gray')])])
        F['p277/ap/k_cols'].append(f'execute unless score @s bm.rcb_{k} matches 1 unless items entity @s weapon.mainhand {holds(iid)} '
                                   f'if items entity @s container.* {holds(iid, P277.NOPK)} run function bm:p278/pk/ap_{k}')
    # (phase277's ap/mv keeps "r$(k)": rcb_<kind> - its path - is "r" + "cb_<kind>")
    # off hand + the Pack's use
    anyk = '*[' + '|'.join(f'minecraft:custom_data~{{bm:"{KINDS[k][0]}"}}' for k in ORDER) + ']'
    use = F['p179/w/use']
    kk = next(i for i, l in enumerate(use) if l.endswith('run return run function bm:p277/add'))
    use.insert(kk, f'execute if items entity @s weapon.offhand {anyk} run return run function bm:p278/pk/add')
    fn('p278/pk/add', [f'execute if items entity @s weapon.offhand {holds(KINDS[k][0])} run return run function bm:p278/pk/add_{k}' for k in ORDER])
    # the Collectors page: a row each (before the Prime Coolers' rows)
    rowb = {k: P28.btn([P277.icon(KINDS[k][0], KINDS[k][2]), T(' ' + KINDS[k][1].split("'s ")[-1], KINDS[k][2]), T('  ›', 'gray')], B_ROWP0 + i, width=300,
                       tooltip=T(f'Its account: {", ".join(c for c, xs in KINDS[k][3])} - deposit, take, auto-collect', 'gray')) for i, k in enumerate(ORDER)}
    cols = F['p277/b/cols']
    j = next(i for i, l in enumerate(cols) if l.startswith('data modify storage bm:tmp rq.acts set value []'))
    cols[j + 1:j + 1] = [f'execute if score @s bm.rcb_{k} matches 1 run data modify storage bm:tmp rq.acts append value {snbt(rowb[k])}' for k in ORDER]
    e_ = next(i for i, l in enumerate(cols) if 'unless data storage bm:tmp rq.acts[0] run return run dialog show @s' in l)
    cols[e_] = cols[e_].replace('Hold a Prime Cooler', 'Hold a Stone Collector, a Wood Box, an Ore Magnet, a Spirit Jar or a Prime Cooler').replace(' (up to 10 of each)', ' (one of each - a Prime Cooler, up to 10)')
    # (Deposit all they take: the accounts on the Pack too)
    da = F['p277/d/all']
    da[1:1] = [f'execute if score @s bm.rcb_{k} matches 1 run function bm:p278/depall/{k}' for k in ORDER] + \
              ['execute if score #cbn bm.rng matches 1.. run scoreboard players add #rqd bm.rng 1']
    da.insert(1, 'scoreboard players set #cbn bm.rng 0')
    # (the front page's count: the accounts on the Pack join the Collectors' number)
    op = F['p277/open']
    k_ = next(i for i, l in enumerate(op) if l == 'execute store result storage bm:tmp rqf.cols int 1 run scoreboard players get #rqf bm.rng')
    op[k_:k_] = [f'scoreboard players operation #rqf bm.rng += @s bm.rcb_{k}' for k in ORDER]

    # ================================================================== MOVING OVER (old jars and magnets, lossless)
    MIG = {'mob': 'spirit_jar', 'ore': 'ore_magnet'}
    # each stack of an old container: an item entity at your feet for a moment, then into the account - or handed back
    fn('p278/mig/spill', ['execute unless data storage bm:rp m.c[0] run return 0',
                          'summon minecraft:item ~ ~0.3 ~ {Tags:["bm.cbmig"],PickupDelay:32767s,Item:{id:"minecraft:stone",count:1}}',
                          'data modify entity @e[type=minecraft:item,tag=bm.cbmig,tag=!bm.cbmig2,limit=1,distance=..1] Item set from storage bm:rp m.c[0].item',
                          'tag @e[type=minecraft:item,tag=bm.cbmig,distance=..1] add bm.cbmig2', 'data remove storage bm:rp m.c[0]', 'function bm:p278/mig/spill'])
    fn('p278/mig/sort', ['scoreboard players set #cbn bm.rng 0', 'scoreboard players set #cbh bm.rng 0'] +
       [f'execute if data storage bm:rp {{m:{{k:"{k}"}}}} as @e[type=minecraft:item,tag=bm.cbmig,distance=..2] if items entity @s contents {has_(k)} run function bm:p278/take_ent' for k in MIG] +
       ['execute as @e[type=minecraft:item,tag=bm.cbmig,distance=..2] run function bm:p278/mig/back'])
    fn('p278/mig/back', ['scoreboard players add #cbh bm.rng 1', 'data modify entity @s PickupDelay set value 0s', 'data modify entity @s Owner set from entity @a[tag=bm.cbme,limit=1] UUID',
                         'tag @s remove bm.cbmig', 'tag @s remove bm.cbmig2'])
    tell = lambda k: tellraw('@s', PRE + [T(f'Your {KINDS[k][1].split(chr(39) + "s ")[-1]}\'s ', KINDS[k][2], bold=True), {'score': {'name': '#cbn', 'objective': 'bm.rng'}, 'color': 'white'},
                                          T(' items are in its account now', 'gray'), T('; ', 'gray'), {'score': {'name': '#cbh', 'objective': 'bm.rng'}, 'color': 'white'},
                                          T(' things it doesn\'t keep were handed back.', 'gray')])
    for k, iid in MIG.items():
        old = f'*[minecraft:custom_data~{{bm:"{iid}"}},minecraft:container]'
        # in a pocket or the off hand: the slot's container -> spilled and sorted; the item refreshed, its container gone
        fn(f'p278/mig/slot_{k}', ['tag @s add bm.cbme', pid, f'data modify storage bm:rp c.k set value "{k}"', f'data modify storage bm:rp m set value {{k:"{k}",c:[]}}',
                                  '$data modify storage bm:rp m.c set from entity @s $(path).components."minecraft:container"',
                                  'function bm:p278/mig/spill', 'function bm:p278/mig/sort',
                                  f'$item modify entity @s $(slot) bm:refresh/{iid}', '$item modify entity @s $(slot) bm:p278/nocont',
                                  'execute if score #cbn bm.rng matches 1.. run ' + tell(k),
                                  'execute if score #cbn bm.rng matches 0 if score #cbh bm.rng matches 1.. run ' + tell(k), 'tag @s remove bm.cbme'])
        fn(f'p278/mig/inv_{k}', [f'execute if items entity @s container.{s} {old} run function bm:p278/mig/slot_{k} {{path:"Inventory[{{Slot:{s}b}}]",slot:"container.{s}"}}' for s in range(36)] +
           [f'execute if items entity @s weapon.offhand {old} run function bm:p278/mig/slot_{k} {{path:"equipment.offhand",slot:"weapon.offhand"}}'])
        second.append(f'execute as @a[scores={{bm.pid=1..}}] if items entity @s container.* {old} at @s run function bm:p278/mig/inv_{k}')
        second.append(f'execute as @a[scores={{bm.pid=1..}}] unless items entity @s container.* {old} if items entity @s weapon.offhand {old} at @s run function bm:p278/mig/inv_{k}')
    G.wjson('bm/item_modifier/p278/nocont.json', [{'function': 'minecraft:set_components', 'components': {'!minecraft:container': {}}},
                                                 {'function': 'minecraft:set_custom_data', 'tag': '{bm_cb:1b}'}])
    # the Pack's old lists (rb_sj / rb_om): each one's load moved over; the first stays on as the Pack's one, the others come back empty
    PK = {'mob': 'rb_sj', 'ore': 'rb_om'}
    for k, lst in PK.items():
        iid = MIG[k]
        fn(f'p278/mig/pk_{k}', ['tag @s add bm.cbme', f'data modify storage bm:rp c.k set value "{k}"', 'scoreboard players set #cbN bm.rng 0', 'scoreboard players set #cbH bm.rng 0',
                                'scoreboard players set #cbe bm.rng 0'] +
           [f'function bm:p278/mig/pke_{k} {{pid:$(pid),j:{j}}}' for j in range(10)] +
           [f'$data remove storage bm:pw p$(pid).{lst}', 'scoreboard players operation #cbn bm.rng = #cbN bm.rng', 'scoreboard players operation #cbh bm.rng = #cbH bm.rng',
            'execute if score #cbN bm.rng matches 1.. run ' + tell(k), 'execute if score #cbN bm.rng matches 0 if score #cbH bm.rng matches 1.. run ' + tell(k),
            'execute if score #cbe bm.rng matches 1.. run ' + tellraw('@s', PRE + [{'score': {'name': '#cbe', 'objective': 'bm.rng'}, 'color': 'white'},
                                                                              T(f' more {ITEMS[iid]["name"]}s came off your Rat Pack, now empty - it keeps one now: their account is the same.', 'gray')]),
            'tag @s remove bm.cbme'])
        F[f'p278/mig/pk_{k}'] = ['$' + l if '$(' in l and not l.startswith('$') else l for l in F[f'p278/mig/pk_{k}']]
        fn(f'p278/mig/pke_{k}', [f'$execute unless data storage bm:pw p$(pid).{lst}[$(j)] run return 0',
                                 f'$execute if data storage bm:pw p$(pid).{lst}[$(j)].out run return 0',
                                 f'data modify storage bm:rp m set value {{k:"{k}",c:[]}}',
                                 f'$data modify storage bm:rp m.c set from storage bm:pw p$(pid).{lst}[$(j)].it.components."minecraft:container"',
                                 'function bm:p278/mig/spill', 'function bm:p278/mig/sort', 'scoreboard players operation #cbN bm.rng += #cbn bm.rng', 'scoreboard players operation #cbH bm.rng += #cbh bm.rng',
                                 f'$data remove storage bm:pw p$(pid).{lst}[$(j)].it.components."minecraft:container"',
                                 f'$data modify storage bm:pw p$(pid).{lst}[$(j)].it.components."minecraft:custom_data".bm_cb set value 1b',
                                 f'$execute unless score @s bm.rcb_{k} matches 1 run function bm:p278/mig/pkkeep_{k} {{pid:$(pid),j:$(j)}}',
                                 f'$execute if score @s bm.rcb_{k} matches 1 unless data storage bm:rp {{mk:1b}} run function bm:p278/mig/pkback_{k} {{pid:$(pid),j:$(j)}}',
                                 'data remove storage bm:rp mk'])
        fn(f'p278/mig/pkkeep_{k}', [f'$data modify storage bm:pw p$(pid).rcb_{k} set from storage bm:pw p$(pid).{lst}[$(j)].it', f'scoreboard players set @s bm.rcb_{k} 1',
                                    'data modify storage bm:rp mk set value 1b'])
        fn(f'p278/mig/pkback_{k}', ['summon minecraft:item ~ ~0.4 ~ {Tags:["bm.rqout"],PickupDelay:0s,Item:{id:"minecraft:paper",count:1}}',
                                    f'$data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Item set from storage bm:pw p$(pid).{lst}[$(j)].it',
                                    'data modify entity @e[type=minecraft:item,tag=bm.rqout,limit=1] Owner set from entity @s UUID',
                                    'tag @e[type=minecraft:item,tag=bm.rqout] remove bm.rqout', 'scoreboard players add #cbe bm.rng 1'])
    fn('p278/mig/now', [pid] + [f'function bm:p278/mig/pk_{k} with storage bm:rp c' for k in PK] + ['scoreboard players set @s bm.cbmig 1'])
    second.append('execute as @a[scores={bm.pid=1..}] unless score @s bm.cbmig matches 1 at @s run function bm:p278/mig/now')
    # an unfolded old jar / magnet barrel: folded first (back to its owner's hands - never into the Pack's old lists - then moved over there)
    second.insert(0, 'execute as @e[type=minecraft:marker,tag=bm.bxm] if entity @s[tag=bm.bx_mobcol] at @s run function bm:p278/mig/fold')
    second.insert(0, 'execute as @e[type=minecraft:marker,tag=bm.bxm] if entity @s[tag=bm.bx_orecol] at @s run function bm:p278/mig/fold')
    fn('p278/mig/fold', ['tag @s remove bm.rbbox', 'function bm:p33/box/close'])
    # (a marker from before: its Pack place is counted in the old BAGK - jar 2, magnet 3, cooler 4 - now the cooler is 2)
    F['tick'].insert(0, 'execute as @e[type=minecraft:marker,tag=bm.rbbox,tag=!bm.rbv2] run function bm:p278/mig/remap')
    fn('p278/mig/remap', ['tag @s add bm.rbv2', 'execute if entity @s[tag=bm.bx_mobcol] run return run tag @s remove bm.rbbox',
                          'execute if entity @s[tag=bm.bx_orecol] run return run tag @s remove bm.rbbox',
                          f'execute if score @s bm.rbk matches 4 run scoreboard players set @s bm.rbk {P277.PCK}'])
    F['p277/b/mark'].insert(0, 'tag @s add bm.rbv2')

    # ================================================================== the old unfold and pull go (the item's use opens the account)
    for name in [n for n in list(F) if n.startswith(('p174/col/use_', 'p174/col/pull_'))]: del F[name]
    for name in ('loop/fast', 'loop/second'):
        F[name] = [l for l in F[name] if 'function bm:p174/col/pull_' not in l]

    # ================================================================== THE ROUTER
    act = [f'execute if score #act bm.pay matches {B_CAT0 + ci} if score @s bm.menu matches {MENU_F} run return run function bm:p278/go_cat {{c:{ci}}}' for ci in range(4)]
    fn('p278/go_cat', ['$scoreboard players set @s bm.cbc $(c)', 'scoreboard players set @s bm.pg_cb 0', 'function bm:p278/cat'])
    act += [f'execute if score #act bm.pay matches {B_DEPALL} if score @s bm.menu matches {MENU_F} run return run function bm:p278/do_depall',
            f'execute if score #act bm.pay matches {B_AUTO} if score @s bm.menu matches {MENU_F} run return run function bm:p278/do_auto',
            f'execute if score #act bm.pay matches {B_BACKP} if score @s bm.menu matches {MENU_F} run return run function bm:p277/b/cols',
            f'execute if score #act bm.pay matches {B_OFF} if score @s bm.menu matches {MENU_F} run return run function bm:p278/do_off',
            f'execute if score #act bm.pay matches {B_PREV} if score @s bm.menu matches {MENU_C} run return run function bm:p278/pv',
            f'execute if score #act bm.pay matches {B_NEXT} if score @s bm.menu matches {MENU_C} run return run function bm:p278/nx',
            f'execute if score #act bm.pay matches {B_BACKF} if score @s bm.menu matches {MENU_C} run return run function bm:p278/front',
            f'execute if score #act bm.pay matches {B_STACK} if score @s bm.menu matches {MENU_I} run return run function bm:p278/do_stack',
            f'execute if score #act bm.pay matches {B_ALL} if score @s bm.menu matches {MENU_I} run return run function bm:p278/do_all',
            f'execute if score #act bm.pay matches {B_DEP1} if score @s bm.menu matches {MENU_I} run return run function bm:p278/do_dep1',
            f'execute if score #act bm.pay matches {B_BACKC} if score @s bm.menu matches {MENU_I} run return run function bm:p278/cat'] + \
           [f'execute if score #act bm.pay matches {B_ROWP0 + i} if score @s bm.menu matches {P277.M_COLS} run return run function bm:p278/frompack/{k}' for i, k in enumerate(ORDER)] + \
           [f'execute if score #act bm.pay matches {B_ROW0}..{B_ROW0 + len(TYPES) - 1} if score @s bm.menu matches {MENU_C} run return run function bm:p278/pick']
    fn('p278/pick', ['scoreboard players operation @s bm.cbi = #act bm.pay', f'scoreboard players remove @s bm.cbi {B_ROW0}', 'function bm:p278/item'])
    fn('p278/pv', ['scoreboard players remove @s bm.pg_cb 1', 'function bm:p278/cat'])
    fn('p278/nx', ['scoreboard players add @s bm.pg_cb 1', 'function bm:p278/cat'])
    fn('p278/do_off', [f'execute if score @s bm.cbk matches {ORDER.index(k)} run return run function bm:p278/pk/off_{k}' for k in ORDER])
    fn('p278/act', act + ['function bm:p28/stale'])
    F['p28/act'].append(f'execute if score #act bm.pay matches {MENU_F}..9699 run return run function bm:p278/act')
    F['admin/help'] += [tellraw('@s', [T('/function bm:admin/collectors2', 'yellow'), T('  the Stone Collector, the Wood Box, the Ore Magnet and the Spirit Jar', 'gray')])]
    fn('admin/collectors2', [G.give(KINDS[k][0]) for k in ORDER])
    return rep

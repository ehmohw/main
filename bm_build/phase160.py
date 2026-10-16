"""2.80d: GROUND FORGES - things laid on the ground together that fuse into something new.

Toss the ingredients (Q) so they lie together, within a couple of blocks of each other. When the last one lands, the forge
wakes: the items lift, orbit and close in over four seconds in their own colours, then flash into the result, which drops
where they were. Nobody can pick an ingredient up while it burns; if one is lost (lava, a hopper...), the rest fall back
down unharmed. None of these overlaps the Ethereal Gem (nine gems fused in hand) or the Wraithfire Heart (a placed
Scorching Heart beside a placed Ethereal Gem), nor one another:

THE HUNTMASTER'S RELIC  the four Overworld roaming bosses' relics, any form each: the Horseman's Head, the Sand Pharaoh's
    Crook, the Storm Roc's Talon and the Elder Treant's Branch. (Not KillerWatt or Tullius - they're followers' bosses.)
    One weapon that is all four: swap-hands (F) turns it to the next relic, sneak + F to the one before; the catalysts
    still choose its class (Offense / Defense / Ranged / Support) and the class carries over as it turns. Wherever it is,
    it's at its home strength (the crook's sun, the talon's storm, the branch's forest - x1.5; the head never weaker than
    by night). It keeps the forged head's class.
THE RIFTBOUND RELIC  the Magma Colossus's Gauntlet and the Voidwalker's Scepter (the Nether's and the End's roaming
    bosses): the same, for those two - always at home (x1.5), F swaps between them.
THE STARHEART  a Fallen Star beside a Heartstone, at night under the open sky. Used: +1 max heart for good, PAST the
    Heartstone cap (up to five Starhearts); the three-row cap on max health still holds. (The Star Cloak is nine stars
    in hand - no overlap.)
THE TALISMAN OF THE THREE NIGHTS  8 Blood Crystals, 8 Lucky Tokens and a Red Xenite shard, by night. Carried, each
    special night gives its boon: a Blood Moon - Strength and Regeneration, and its foes glow near you; a Lucky Night -
    Luck II and Speed; an Invasion - Night Vision and Resistance, and the Vorn glow near you; any other night in the
    Overworld - Night Vision.
"""
import copy
from items import item, T, TOTEM, ITEMS, CATEGORY, consumable, fancy_name, item_symbol
from useitem import HOLD, HOLD_REPEAT
from nbt import B, Short
import phase42 as P42
import phase53 as P53
import phase54 as P54
import phase50 as P50

HUNTP = '*[minecraft:custom_data~{bm_hunt:1b}]'
holds = '*[minecraft:custom_data~{bm:"%s"}]'
STAR, NIGHTS = '#ffe9a0', '#d05a9a'

# ---------------------------------------------------------------------------------------------- the forged relics
SETS = {  # set: (prefix, colour, families in F order, first lore line)
    'hunt': ("Huntmaster's", '#ffcc33', ['head', 'crook', 'talon', 'branch'], "Four roaming terrors' relics, forged into one."),
    'rift': ('Riftbound', '#c58aff', ['gauntlet', 'scepter'], "The Nether's fist and the End's eye, forged into one.")}
FAMS = dict(P53.FAMILIES, **P54.FAMILIES)


def base_iid(fam, v):
    return P42.VARIANTS[v][0] if fam == 'head' else FAMS[fam][v][0]


def base_name(fam, v):
    return P42.VARIANTS[v][1] if fam == 'head' else FAMS[fam][v][1]


_DROP = ('Stronger', 'Night: x1.5', 'Night: stronger', 'Blood Moon: strongest')
for _s, (_pre, _col, _fams, _first) in SETS.items():
    for _f in _fams:
        for _v in range(1, 5):
            _b = ITEMS[base_iid(_f, _v)]
            _iid = f'{_s}_{_f}_{_v}'
            _c = copy.deepcopy(_b['comps'])
            _c['minecraft:item_name'] = fancy_name(f'{_pre} {base_name(_f, _v)}', _col, item_symbol(_iid, _b['base'], 'relic'), legendary=True)
            _lore = [l for l in _c['minecraft:lore'] if not l.get('text', '').startswith(_DROP)]
            _c['minecraft:lore'] = [T(_first, _col), T('Swap-hands (F): the next relic. Sneak + F: the one before.', 'blue'),
                                    T('Always at its home strength, anywhere.', 'gold')] + _lore
            _c['minecraft:enchantment_glint_override'] = True
            _cu = {k: v for k, v in _b['custom'].items() if k != 'bm'}
            _cu = dict({'bm': _iid}, **_cu, bm_hunt=B(1))
            _c['minecraft:custom_data'] = dict(_cu, bmv=_b['comps']['minecraft:custom_data']['bmv'])
            ITEMS[_iid] = {'base': _b['base'], 'comps': _c, 'custom': _cu, 'name': f'{_pre} {base_name(_f, _v)}'}
            CATEGORY[_iid] = 'relic'
            if _f == 'head': HOLD_REPEAT[_iid] = 'bm:p42/use'
            else: HOLD[_iid] = f'bm:p53/{_f}/use'


# (2.80d) each part says where it leads, as the Wraithfire Heart's do - added after the forged copies are built, so they don't carry it
_HINTS = {'head': "On the ground with the other roaming terrors' relics (crook, talon, branch), they fuse.",
          'crook': "On the ground with the other roaming terrors' relics (head, talon, branch), they fuse.",
          'talon': "On the ground with the other roaming terrors' relics (head, crook, branch), they fuse.",
          'branch': "On the ground with the other roaming terrors' relics (head, crook, talon), they fuse.",
          'gauntlet': "On the ground beside the Voidwalker's Scepter, they fuse.",
          'scepter': "On the ground beside the Magma Colossus's Gauntlet, they fuse."}
for _f, _line in _HINTS.items():
    for _v in range(1, 5):
        _i = base_iid(_f, _v)
        if _i in ITEMS: ITEMS[_i]['comps']['minecraft:lore'].insert(-1, T(_line, SETS['hunt' if _f in SETS['hunt'][2] else 'rift'][1]))
for _i, _line, _col in (('fallen_star', 'On the ground beside a Heartstone, under the night sky, they fuse.', '#ffe9a0'),
                        ('heartstone', 'On the ground beside a Fallen Star, under the night sky, they fuse.', '#ffe9a0'),
                        ('xenite_red', 'On the ground with 8 Blood Crystals and 8 Lucky Tokens, by night, they fuse.', '#d05a9a')):
    if _i in ITEMS: ITEMS[_i]['comps']['minecraft:lore'].insert(-1, T(_line, _col))

# (2.80d) and the Newcomers' Book has them all, the Wraithfire Heart too
_H = '#7a1f1f'
P50.EXTRA_PAGES += [
    [T('GROUND FORGES\n', _H, bold=True), T('(toss them down together, Q)\n\n', 'dark_gray'),
     T("Huntmaster's Relic\n", '#a07a10', bold=True), T("The Horseman's Head, the Pharaoh's Crook, the Roc's Talon and the Treant's Branch.\n\n", 'black'),
     T('Riftbound Relic\n', '#7a4ab0', bold=True), T("The Colossus's Gauntlet and the Voidwalker's Scepter.", 'black')],
    [T('Starheart\n', '#a08a20', bold=True), T('A Fallen Star and a Heartstone, at night, under the open sky.\n\n', 'black'),
     T('Talisman of the Three Nights\n', '#a03a70', bold=True), T('8 Blood Crystals, 8 Lucky Tokens and a Red Xenite Shard, by night.\n\n', 'black'),
     T('Wraithfire Heart\n', '#3a6ab0', bold=True), T('A Scorching Heart set down beside an Ethereal Gem.', 'black')]]


def set_of(fam):
    return next(s for s, d in SETS.items() if fam in d[2])

# ---------------------------------------------------------------------------------------------- the Starheart, the Talisman
SH_CAP = 5
item('starheart', TOTEM, 'Starheart', STAR,
     ['A Heartstone that swallowed a falling star.', ('Use it: +1 max heart, forever -', 'blue'), ('even past the Heartstone cap.', 'blue'),
      (f'Up to {SH_CAP} Starhearts. Kept through death.', 'gray'), ('Max health from all sources caps at three rows.', 'dark_gray')],
     model='bm:starheart', glint=True, stack=16, cat='relic',
     comps={'minecraft:consumable': consumable(1.6, 'eat', 'minecraft:block.amethyst_block.resonate', False)})
item('three_nights_talisman', TOTEM, 'Talisman of the Three Nights', NIGHTS,
     ['Blood, luck and a fallen saucer\'s shard, bound together.', ('Carried, each special night lends its boon:', 'blue'),
      ('Blood Moon: Strength, Regeneration; its foes glow.', 'red'), ('Lucky Night: Luck II and Speed.', 'green'),
      ('Invasion: Night Vision, Resistance; the Vorn glow.', 'aqua'), ('Any other night: Night Vision.', 'gray')],
     model='bm:three_nights_talisman', glint=True, stack=1, cat='relic')
TAL = holds % 'three_nights_talisman'

# ---------------------------------------------------------------------------------------------- the recipes
# (key, result name, colour, dust colours, anchor (pred, n), others [(pred, n)], condition lines (run at the anchor; return 0 = not now),
#  the hint when it's all there but the condition isn't met)
RF = lambda f: '*[minecraft:custom_data~{rf:"%s"}]' % f
NIGHT = 'execute if dimension minecraft:overworld if score #tod bm.bm matches 13000..22999'
RECIPES = [
    ('hunt', "Huntmaster's Relic", '#ffcc33', ['1.0,0.55,0.1', '0.95,0.8,0.3', '0.5,0.6,1.0', '0.3,0.85,0.3'],
     ('*[minecraft:custom_data~{bm_head:1b}]', 1), [(RF('crook'), 1), (RF('talon'), 1), (RF('branch'), 1)], None, None),
    ('rift', 'Riftbound Relic', '#c58aff', ['1.0,0.35,0.05', '0.6,0.2,0.9', '0.15,0.05,0.25'],
     (RF('gauntlet'), 1), [(RF('scepter'), 1)], None, None),
    ('star', 'Starheart', STAR, ['1.0,0.95,0.6', '1.0,0.3,0.35', '0.7,0.85,1.0'],
     (holds % 'fallen_star', 1), [(holds % 'heartstone', 1)],
     f'{NIGHT} positioned ~ ~1 ~ if predicate bm:sees_sky', 'The star and the heart stir... but they wait for the open night sky.'),
    ('nights', 'Talisman of the Three Nights', NIGHTS, ['0.85,0.05,0.1', '0.2,0.85,0.3', '0.95,0.2,0.2'],
     (holds % 'blood_crystal', 8), [(holds % 'lucky_token', 8), (holds % 'xenite_red', 1)],
     NIGHT, 'Blood, luck and the red shard stir... but they wake only by night.')]
RESULT = {'star': 'starheart', 'nights': 'three_nights_talisman'}
T_RISE, T_CLOSE, T_DONE = 40, 64, 80


def generate(G):
    fn, title, tellraw, give, PREFIX = G.fn, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, second = [], []
    objs = ['bm.fgt dummy', 'bm.fgv dummy', 'bm.fgn dummy', 'bm.fgc dummy', 'bm.shrt dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]

    # ================================================================ the forge
    drop = lambda iid: 'summon minecraft:item ~ ~0.7 ~ ' + G.snbt({'Item': G.stack(iid), 'Tags': ['bm.fgout'], 'Glowing': B(1), 'PickupDelay': Short(20),
                                                                  'Motion': [0.0, 0.18, 0.0]})
    for r, name, col, dust, (apred, an), others, cond, hint in RECIPES:
        second.append(f'execute as @e[type=minecraft:item,tag=!bm.fg] if items entity @s contents {apred} unless items entity @s contents {HUNTP} '
                      f'at @s run function bm:p160/f/{r}/try')
        tr = ['execute if entity @e[type=minecraft:marker,tag=bm.fgm,distance=..4] run return 0']
        if an > 1: tr += ['execute store result score #n bm.rng run data get entity @s Item.count', f'execute unless score #n bm.rng matches {an}.. run return 0']
        tr += ['tag @s add bm.fga', 'scoreboard players set #ok bm.rng 1']
        for i, (p, n) in enumerate(others, 1):
            tr.append(f'execute as @e[type=minecraft:item,distance=..2.5,tag=!bm.fg,tag=!bm.fga] if items entity @s contents {p} '
                      f'unless items entity @s contents {HUNTP} run function bm:p160/f/{r}/c{i}')
            tr.append(f'execute unless entity @e[type=minecraft:item,tag=bm.fgc{i},distance=..2.5] run scoreboard players set #ok bm.rng 0')
            fn(f'p160/f/{r}/c{i}', ([] if n == 1 else ['execute store result score #n bm.rng run data get entity @s Item.count',
                                                       f'execute unless score #n bm.rng matches {n}.. run return 0']) + [f'tag @s add bm.fgc{i}'])
        if cond:
            tr.append(f'execute if score #ok bm.rng matches 1 unless function bm:p160/f/{r}/cond run return run function bm:p160/f/{r}/wait')
            fn(f'p160/f/{r}/cond', [f'{cond} run return 1', 'return 0'])
            fn(f'p160/f/{r}/wait', ['function bm:p160/f/untag', 'particle minecraft:enchant ~ ~0.6 ~ 0.4 0.3 0.4 0.4 8',
                                    f'execute as @a[distance=..10] run ' + title('@s', 'actionbar', T(hint, col))])
        tr += [f'execute if score #ok bm.rng matches 1 run function bm:p160/f/{r}/begin', 'function bm:p160/f/untag']
        fn(f'p160/f/{r}/try', tr)
        bg = ['summon minecraft:marker ~ ~0.25 ~ {Tags:["bm.fgm","bm.fgnew","bm.fg_%s"]}' % r,
              'scoreboard players set @e[type=minecraft:marker,tag=bm.fgnew] bm.fgt 0',
              f'scoreboard players set @e[type=minecraft:marker,tag=bm.fgnew] bm.fgc {len(others) + 1}',
              f'scoreboard players set @s bm.fgn {an}', 'tag @s add bm.fg']
        if r in ('hunt', 'rift'):          # the forged relic keeps the anchor's class (the head's / the gauntlet's form)
            fam = 'head' if r == 'hunt' else 'gauntlet'
            bg += [f'execute if items entity @s contents {holds % base_iid(fam, v)} run scoreboard players set @e[type=minecraft:marker,tag=bm.fgnew] bm.fgv {v}'
                   for v in range(1, 5)]
        for i, (p, n) in enumerate(others, 1):
            bg += [f'execute as @e[type=minecraft:item,tag=bm.fgc{i},distance=..2.5,sort=nearest,limit=1] run function bm:p160/f/lock {{n:{n}}}']
        bg += ['function bm:p160/f/lock_me', 'tag @e[type=minecraft:marker,tag=bm.fgnew] remove bm.fgnew',
               'playsound minecraft:block.beacon.activate block @a[distance=..16] ~ ~ ~ 1 1.6',
               'playsound minecraft:block.amethyst_block.resonate block @a[distance=..16] ~ ~ ~ 1 0.6',
               f'execute as @a[distance=..12] run ' + title('@s', 'actionbar', [T('Something stirs among the things on the ground...', col)])]
        fn(f'p160/f/{r}/begin', bg)
        # its colours while it burns, and its finish
        fn(f'p160/f/{r}/fx', [f'particle minecraft:dust{{color:[{c}],scale:1.2}} ^ ^ ^1.1 0.1 0.1 0.1 0 1' for c in dust] +
           ['execute rotated ~180 0 run particle minecraft:dust{color:[%s],scale:1.2} ^ ^ ^1.1 0.1 0.1 0.1 0 1' % dust[0]])
        done = ['function bm:p160/f/consume']
        if r in ('hunt', 'rift'):
            fam = 'head' if r == 'hunt' else 'gauntlet'
            done += [f'execute if score @s bm.fgv matches {v} run ' + drop(f'{r}_{fam}_{v}') for v in range(1, 5)]
            done.append(f'execute unless score @s bm.fgv matches 1..4 run ' + drop(f'{r}_{fam}_1'))
        else:
            done.append(drop(RESULT[r]))
        done += [
                 'particle minecraft:flash{color:[1.0,1.0,1.0,1.0]} ~ ~0.7 ~ 0 0 0 0 1', 'particle minecraft:end_rod ~ ~0.7 ~ 0.2 0.2 0.2 0.25 40',
                 'particle minecraft:dust{color:[%s],scale:2.0} ~ ~0.7 ~ 0.6 0.6 0.6 0 40' % dust[0],
                 'playsound minecraft:ui.toast.challenge_complete block @a[distance=..16] ~ ~ ~ 0.8 1.2',
                 'playsound minecraft:block.anvil.use block @a[distance=..16] ~ ~ ~ 0.6 0.7',
                 'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..24] ~ ~ ~ 0.4 1.6',
                 f'execute as @a[distance=..16] run ' + tellraw('@s', PREFIX + [T('FORGED: ', col, bold=True), T(name, col), T(' - it lies where the pieces burned.', 'gray')]),
                 'kill @s']
        fn(f'p160/f/{r}/done', done)

    fn('p160/f/untag', ['tag @e[type=minecraft:item,distance=..4] remove bm.fga'] +
       [f'tag @e[type=minecraft:item,distance=..4] remove bm.fgc{i}' for i in range(1, 4)])
    # an ingredient while it burns: not picked up, not despawning, floating where it is (n: how many of its stack it costs)
    fn('p160/f/lock', ['$scoreboard players set @s bm.fgn $(n)', 'tag @s add bm.fg', 'function bm:p160/f/lock_me'])
    fn('p160/f/lock_me', ['data merge entity @s[type=minecraft:item] {PickupDelay:32767s,NoGravity:1b,Age:-32768s,Motion:[0.0,0.0,0.0]}'])
    fn('p160/f/free', ['data merge entity @s[type=minecraft:item] {PickupDelay:10s,NoGravity:0b,Age:0s}', 'tag @s remove bm.fg', 'scoreboard players reset @s bm.fgn'])
    # (as the marker) used up: the whole item, or just its share of a stack (the rest falls back down)
    fn('p160/f/consume', ['execute as @e[type=minecraft:item,tag=bm.fg,distance=..4] run function bm:p160/f/use_up'])
    fn('p160/f/use_up', ['execute store result score #n bm.rng run data get entity @s Item.count', 'scoreboard players operation #n bm.rng -= @s bm.fgn',
                         'execute if score #n bm.rng matches ..0 run return run kill @s',
                         'execute store result entity @s Item.count int 1 run scoreboard players get #n bm.rng', 'function bm:p160/f/free'])

    tick.append('execute as @e[type=minecraft:marker,tag=bm.fgm] at @s run function bm:p160/f/tick')
    fn('p160/f/tick', ['scoreboard players add @s bm.fgt 1',
                       # a piece lost: the forge goes cold, and the rest fall back down
                       'execute store result score #n bm.rng if entity @e[type=minecraft:item,tag=bm.fg,distance=..4]',
                       'execute unless score #n bm.rng = @s bm.fgc run return run function bm:p160/f/fail',
                       f'execute if score @s bm.fgt matches ..{T_RISE} as @e[type=minecraft:item,tag=bm.fg,distance=..4] at @s facing entity @e[type=minecraft:marker,tag=bm.fgm,distance=..4,sort=nearest,limit=1] feet run tp @s ^0.07 ^0.016 ^0.012',
                       f'execute if score @s bm.fgt matches {T_RISE + 1}..{T_CLOSE} as @e[type=minecraft:item,tag=bm.fg,distance=..4] at @s facing entity @e[type=minecraft:marker,tag=bm.fgm,distance=..4,sort=nearest,limit=1] feet run tp @s ^0.11 ^0.004 ^0.05',
                       f'execute if score @s bm.fgt matches {T_CLOSE + 1}.. as @e[type=minecraft:item,tag=bm.fg,distance=..4] at @s facing entity @e[type=minecraft:marker,tag=bm.fgm,distance=..4,sort=nearest,limit=1] feet run tp @s ^0.16 ^ ^0.12',
                       'execute as @e[type=minecraft:item,tag=bm.fg,distance=..4] at @s run particle minecraft:end_rod ~ ~0.2 ~ 0 0 0 0 1',
                       'scoreboard players operation #s bm.rng = @s bm.fgt', 'scoreboard players operation #s bm.rng *= #20 bm.rng',
                       'execute store result storage bm:p160 s.r float 1 run scoreboard players get #s bm.rng',
                       'function bm:p160/f/fx with storage bm:p160 s',
                       'execute if score @s bm.fgt matches 20 run playsound minecraft:block.amethyst_block.chime block @a[distance=..16] ~ ~ ~ 1 0.8',
                       f'execute if score @s bm.fgt matches {T_RISE} run playsound minecraft:block.amethyst_block.chime block @a[distance=..16] ~ ~ ~ 1 1.2',
                       f'execute if score @s bm.fgt matches {T_RISE} run playsound minecraft:block.portal.trigger block @a[distance=..16] ~ ~ ~ 0.4 1.8',
                       f'execute if score @s bm.fgt matches {T_CLOSE} run playsound minecraft:block.beacon.power_select block @a[distance=..16] ~ ~ ~ 1 1.4',
                       f'execute if score @s bm.fgt matches {T_CLOSE}.. run particle minecraft:enchant ~ ~0.8 ~ 0.3 0.3 0.3 1 6'] +
       [f'execute if score @s bm.fgt matches {T_DONE}.. if entity @s[tag=bm.fg_{r}] run return run function bm:p160/f/{r}/done' for r, *_x in RECIPES])
    fn('p160/f/fx', [f'$execute rotated $(r) 0 positioned ~ ~0.3 ~ if entity @s[tag=bm.fg_{r}] run function bm:p160/f/{r}/fx' for r, *_x in RECIPES])
    fn('p160/f/fail', ['execute as @e[type=minecraft:item,tag=bm.fg,distance=..4] run function bm:p160/f/free', 'particle minecraft:smoke ~ ~0.6 ~ 0.3 0.3 0.3 0.02 20',
                       'playsound minecraft:block.fire.extinguish block @a[distance=..16] ~ ~ ~ 0.8 1.2',
                       'execute as @a[distance=..12] run ' + title('@s', 'actionbar', T('A piece went missing - the forge goes cold.', 'gray')), 'kill @s'])

    # ================================================================ the forged relics: forms, catalysts, moods, F to turn
    for s, (pre, col, fams, _first) in SETS.items():
        for f in fams:
            if f == 'head':
                G.FUNCS['p42/hv'] += [f'execute if items entity @s weapon.mainhand {holds % f"{s}_head_{v}"} run return run scoreboard players set #hv bm.rng {v}'
                                      for v in range(1, 5)]
            else:
                G.FUNCS[f'p53/{f}/form'] += [f'execute if items entity @s weapon.mainhand {holds % f"{s}_{f}_{v}"} run return run scoreboard players set #rv bm.rng {v}'
                                             for v in range(1, 5)]
                G.FUNCS[f'p53/mood_{f}'].append(f'execute if items entity @s weapon.mainhand {HUNTP} run scoreboard players set #rmul bm.rng 15')
            # a catalyst turns it - into its own set's form of that class
            for v in range(1, 5):
                key = f'p42/up/to_{v}' if f == 'head' else f'p53/{f}/to_{v}'
                L = G.FUNCS[key]
                k = L.index(f'item replace entity @s weapon.mainhand with {G.item_arg(base_iid(f, v))}')
                L[k:k + 1] = [f'execute if items entity @s weapon.mainhand {HUNTP} run item replace entity @s weapon.mainhand with {G.item_arg(f"{s}_{f}_{v}")}',
                              f'execute unless items entity @s weapon.mainhand {HUNTP} run item replace entity @s weapon.mainhand with {G.item_arg(base_iid(f, v))}']
    # (the two sets share families with nothing, so one "is it forged?" check serves each family's catalyst)
    G.FUNCS['p42/tier'].append(f'execute if items entity @s weapon.mainhand {HUNTP} if score @s bm.hpw matches ..0 run function bm:p160/head_floor')
    fn('p160/head_floor', ['scoreboard players set @s bm.hpw 1', 'scoreboard players set #hpi bm.rng 15'])

    tick.append(f'execute as @a if items entity @s weapon.offhand {HUNTP} at @s run function bm:p160/swap')
    sw = []
    for s, (pre, col, fams, _first) in SETS.items():
        n = len(fams)
        for i, f in enumerate(fams):
            for v in range(1, 5):
                iid = f'{s}_{f}_{v}'
                for d, nm in ((1, 'next'), (-1, 'prev')):
                    to = fams[(i + d) % n]
                    fn(f'p160/to/{iid}_{nm}', ['item replace entity @s weapon.offhand from entity @s weapon.mainhand',
                                               f'item replace entity @s weapon.mainhand with {G.item_arg(f"{s}_{to}_{v}")}',
                                               'tag @s remove bm.p42chg', 'tag @s remove bm.p42lock', 'scoreboard players set @s bm.hch 0',
                                               'particle minecraft:enchant ~ ~1.2 ~ 0.3 0.4 0.3 0.6 20', 'particle minecraft:wax_on ~ ~1.1 ~ 0.3 0.3 0.3 0 6',
                                               'playsound minecraft:item.armor.equip_gold player @a[distance=..12] ~ ~ ~ 0.8 1.2',
                                               'playsound minecraft:block.amethyst_block.chime player @a[distance=..12] ~ ~ ~ 0.6 1.6',
                                               title('@s', 'actionbar', [T(pre + ' ', col, bold=True), T(base_name(to, v), 'white', bold=True)])])
                sw += [f'execute if items entity @s weapon.offhand {holds % iid} if predicate bm:p20/sneaking run return run function bm:p160/to/{iid}_prev',
                       f'execute if items entity @s weapon.offhand {holds % iid} run return run function bm:p160/to/{iid}_next']
    fn('p160/swap', sw)

    # ================================================================ the Starheart: +1 heart past the Heartstone cap
    G.consume_adv('starheart', 'bm:p160/starheart')
    fn('p160/starheart', ['advancement revoke @s only bm:consume/starheart',
                          'execute unless score @s bm.shrt matches 0.. run scoreboard players set @s bm.shrt 0',
                          f'execute if score @s bm.shrt matches {SH_CAP}.. run return run function bm:p160/sh/full',
                          'scoreboard players add @s bm.shrt 1', 'function bm:p160/sh/apply', 'effect give @s minecraft:regeneration 3 1 true',
                          title('@s', 'actionbar', [T('Starlight fills your heart: ', STAR), {'score': {'name': '@s', 'objective': 'bm.shrt'}, 'color': 'white'},
                                                    T(f' / {SH_CAP} Starhearts', 'gray')]),
                          'particle minecraft:end_rod ~ ~1.2 ~ 0.4 0.6 0.4 0.05 30', 'particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 6',
                          'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.4', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6'])
    fn('p160/sh/full', [give('starheart'), say(f'Your heart holds all the starlight it can ({SH_CAP} Starhearts). (Refunded)', STAR)])
    fn('p160/sh/apply', ['attribute @s minecraft:max_health modifier remove bm:starheart',
                         'execute store result storage bm:p160 sh.amt int 2 run scoreboard players get @s bm.shrt',
                         'function bm:p160/sh/set with storage bm:p160 sh'])
    fn('p160/sh/set', ['$attribute @s minecraft:max_health modifier add bm:starheart $(amt) add_value'])
    fn('p160/sh/has', ['return run attribute @s minecraft:max_health modifier value get bm:starheart'])
    second.append('execute as @a[scores={bm.shrt=1..}] unless function bm:p160/sh/has run function bm:p160/sh/apply')

    # ================================================================ the Talisman of the Three Nights
    second += [f'execute as @a[gamemode=!spectator] if items entity @s container.* {TAL} at @s run function bm:p160/tal/on',
               f'execute as @a[gamemode=!spectator] unless items entity @s container.* {TAL} if items entity @s weapon.offhand {TAL} at @s run function bm:p160/tal/on']
    fn('p160/tal/on', ['execute if score #active bm.bm matches 1 run return run function bm:p160/tal/blood',
                       'execute if score #lnight bm.bm matches 1 run return run function bm:p160/tal/lucky',
                       'execute if score #inv bm.bm matches 1 run return run function bm:p160/tal/inv',
                       f'{NIGHT} run effect give @s minecraft:night_vision 15 0 true'])
    fn('p160/tal/blood', ['effect give @s minecraft:strength 3 0 true', 'effect give @s minecraft:regeneration 3 0 true',
                          'effect give @e[tag=bm.blood,distance=..24] minecraft:glowing 2 0 true',
                          'particle minecraft:dust{color:[0.8,0.05,0.1],scale:0.8} ~ ~0.2 ~ 0.3 0 0.3 0 3'])
    fn('p160/tal/lucky', ['effect give @s minecraft:luck 3 1 true', 'effect give @s minecraft:speed 3 0 true',
                          'particle minecraft:happy_villager ~ ~0.2 ~ 0.3 0 0.3 0 2'])
    fn('p160/tal/inv', ['effect give @s minecraft:night_vision 15 0 true', 'effect give @s minecraft:resistance 3 0 true',
                        'effect give @e[tag=bm.vorn,distance=..24] minecraft:glowing 2 0 true',
                        'particle minecraft:dust{color:[0.2,0.9,1.0],scale:0.8} ~ ~0.2 ~ 0.3 0 0.3 0 3'])

    # ================================================================ admin
    fn('admin/forge_kits', [give(base_iid('head', 1)), give(base_iid('crook', 1)), give(base_iid('talon', 1)), give(base_iid('branch', 1)),
                            give(base_iid('gauntlet', 1)), give(base_iid('scepter', 1)), give('fallen_star'), give('heartstone'),
                            give('blood_crystal', 8), give('lucky_token', 8), give('xenite_red'),
                            tellraw('@s', PREFIX + [T('Every ground forge\'s ingredients. Toss each set (Q) so it lies together.', 'gray')])])
    fn('admin/forged', [give('hunt_head_1'), give('rift_gauntlet_1'), give('starheart'), give('three_nights_talisman')])

    # ================================================================ (2.80d) the advancement tab: one goal per forge, the recipe in its description
    def got(iids):
        crit = {i: {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': ITEMS[i]['base'],
                                                                                         'predicates': {'minecraft:custom_data': G.snbt({'bm': i})}}]}} for i in iids}
        return crit, [list(iids)]
    for key, ico, ttl, desc, iids in (
            ('forge_hunt', 'hunt_head_1', "The Huntmaster", "Forge the Huntmaster's Relic: the four roaming terrors' relics, tossed down together",
             [f'hunt_{f}_{v}' for f in SETS['hunt'][2] for v in range(1, 5)]),
            ('forge_rift', 'rift_gauntlet_1', 'Riftbound', "Forge the Riftbound Relic: the Colossus's Gauntlet and the Voidwalker's Scepter, tossed down together",
             [f'rift_{f}_{v}' for f in SETS['rift'][2] for v in range(1, 5)]),
            ('forge_star', 'starheart', 'Heart of a Star', 'Forge a Starheart: a Fallen Star and a Heartstone, under the open night sky', ['starheart']),
            ('forge_nights', 'three_nights_talisman', 'Three Nights', 'Forge the Talisman of the Three Nights: Blood Crystals, Lucky Tokens and a Red Xenite Shard, by night',
             ['three_nights_talisman'])):
        crit, req = got(iids)
        it = ITEMS[ico]
        G.wjson(f'bm/advancement/story/{key}.json', {'parent': 'bm:story/root', 'criteria': crit, 'requirements': req,
                'display': {'icon': {'id': it['base'], 'components': {'minecraft:item_model': it['comps'].get('minecraft:item_model', it['base'])}},
                            'title': T(ttl, 'yellow'), 'description': T(desc, 'gray'), 'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    G.FUNCS['tick'] += tick
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack: the Starheart and the Talisman's icons
def rp(R):
    R.ICONS['starheart'] = R.grid(['................', '.......W........', '.......Y........', '..rr..YWY..rr...', '.rOOr..Y..rOOr..', 'rOYYOr...rOYYOr.',
                                   'rOYWYOr.rOYWYOr.', 'rOYYYOOrOOYYYOr.', 'rOOYYYOOOYYYOOr.', '.rOOYYYWYYYOOr..', '..rOOYYYYYOOr...',
                                   '...rOOYYYOOr....', '....rOOYOOr.....', '.....rOOOr......', '......rOr.......', '.......r........'],
                                  dict(r='#5a1a3a', O='#d8506a', Y='#ffd890', W='#ffffff'))
    R.ICONS['three_nights_talisman'] = R.grid(['................', '......kkkk......', '.....k....k.....', '.....k....k.....', '......kkkk......',
                                               '.......kk.......', '.....rrrrrr.....', '....rRRggCCr....', '...rRRRgGCCCr...', '...rRRRgGCCCr...',
                                               '...rRRRgGCCCr...', '....rRRggCCr....', '.....rrrrrr.....', '.......rr.......', '......rWWr......', '.......rr.......'],
                                              dict(k='#c8b070', r='#3a1830', R='#c01a2a', g='#1a7a2a', G='#5aff6a', C='#3ad8ff', W='#ffe9a0'))

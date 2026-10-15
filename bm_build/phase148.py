"""2.79b: CALLING THE BOSSES - rare raid finds that force a roaming boss out, the Arachno-Lantern's gourd on a Blood Moon
heist, a little netherite and diamond in the vault's rare stores, and KillerWatt's Effigy from his predecessor's hand.

SUMMONS (a won heist, Tier III and up, every raider: 1% at Tier III, 3% at IV, 5% at V) - one of six, each forcing out one
              of the roaming bosses whose relic has four forms: the HORSEMAN'S LANTERN (the Headless Horseman), the PHARAOH'S
              SCARAB (the Sand Pharaoh), the THUNDERHEAD FEATHER (the Storm Roc), the ELDER ACORN (the Elder Treant) - those
              four in the Overworld - the SMOULDERING IDOL (the Magma Colossus, in the Nether) and the STARLESS EYE (the
              Voidwalker, in the End). Use one (under the open sky, in the Overworld): the boss comes now, whatever the hour, the weather or the
              biome, and stays to fight (the dawn, the clear sky or the night that would send it off don't, while it was
              called - it still leaves if nobody stays near). Not while that boss is already out; not in a heist; nothing is
              used up if it can't come (no sky, nowhere to stand).
THE SMOULDERING GOURD (a won BLOOD MOON heist, Tier III and up, every raider: 5%) - set it down under the open sky in the
              Overworld: the Scorching Arachno-Lantern grows from it - dormant until you come near, then awake - on any
              night, Blood Moon or not.
THE VAULT'S RARE STORES (the Tier III-V vault treasure roll, as before: 8%/9%/10% a win) now hold a few diamonds, a little
              netherite scrap and, rarely, a netherite upgrade template beside the tier's own gear - sparingly (about 1 win in
              60 for diamonds at Tier III, a template about 1 in 370).
THE STORM EFFIGY is no longer Cecil's: Democratus gives it to whoever beats him in a duel - every duel won - because
              KillerWatt is his successor.
"""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD

ROMAN = ['', 'I', 'II', 'III', 'IV', 'V']
HA, HB = '-200 64 -197', '-198 64 -197'                 # (the haul's two barrels - as phase105)
BOSS_CHANCE = {3: 1, 4: 3, 5: 5}                       # % a won heist, every raider
LANTERN_CHANCE = 5                                     # % a won Blood Moon heist, Tier III and up, every raider
# key: (item, name, colour, the boss's own placing (as a player, at them), its body, its tag, its dimension, who, lore)
SUMMON = {
    'hhm': ('sum_horseman', "Horseman's Lantern", '#ff8a2a', 'p42/spawn/try', 'wither_skeleton', 'bm.hhm', 'overworld', 'the Headless Horseman',
            'A pumpkin lantern that laughs when lit.'),
    'sph': ('sum_pharaoh', "Pharaoh's Scarab", '#e8b923', 'p53/sph/try', 'husk', 'bm.sph', 'overworld', 'the Sand Pharaoh',
            'A gold scarab, warm as desert sand.'),
    'roc': ('sum_roc', 'Thunderhead Feather', '#7ab8ff', 'p53/roc/try', 'phantom', 'bm.roc', 'overworld', 'the Storm Roc',
            'A feather that crackles in your fingers.'),
    'trt': ('sum_treant', 'Elder Acorn', '#6fae3a', 'p54/trt/try', 'creaking', 'bm.trt', 'overworld', 'the Elder Treant',
            'An acorn as old as the forest.'),
    'mcol': ('sum_colossus', 'Smouldering Idol', '#ff6a1a', 'p54/mcol/try', 'magma_cube', 'bm.mcol', 'the_nether', 'the Magma Colossus',
             'An obsidian idol with lava in its cracks.'),
    'vwk': ('sum_voidwalker', 'Starless Eye', '#c27dff', 'p54/vwk/try', 'enderman', 'bm.vwk', 'the_end', 'the Voidwalker',
            'An eye with no stars in it.'),
}
WHERE = {'overworld': 'the Overworld', 'the_nether': 'the Nether', 'the_end': 'the End'}
# (each boss's leave-by-the-hour (or -weather) line, waived while it was called)
LEAVE = {'p42/boss/second': 'execute unless score #tod', 'p53/sph/second': 'execute unless score #tod', 'p54/trt/second': 'execute unless score #tod',
         'p53/roc/second': 'execute if score @s bm.rfx matches 10..', 'p82/tick': 'execute unless score #active bm.bm matches 1'}
# the vault's rare stores, Tier III and up: (item, weight, count) beside the tier's gear (weight 10 each)
RARE_EXTRA = {3: [('diamond', 6, (1, 2)), ('netherite_scrap', 3, 1), ('netherite_upgrade_smithing_template', 1, 1)],
              4: [('diamond', 6, (1, 3)), ('netherite_scrap', 3, (1, 2)), ('netherite_upgrade_smithing_template', 1, 1)],
              5: [('diamond', 6, (2, 3)), ('netherite_scrap', 4, (1, 2)), ('netherite_upgrade_smithing_template', 2, 1)]}

for _k, (_iid, _nm, _col, _try, _ty, _tag, _dim, _who, _l0) in SUMMON.items():
    item(_iid, TOTEM, _nm, _col, [_l0, (f'Use under the open sky in {WHERE[_dim]}:' if _dim == 'overworld' else f'Use it in {WHERE[_dim]}:', 'blue'), (f'{_who[0].upper() + _who[1:]} comes - now,', 'blue'),
                                  ('whatever the hour or the weather.', 'blue'), ('◆ Rare raid find (Tier III and up)', '#5ab0ff')],
         model=f'bm:{_iid}', glint=True, stack=4, cat='relic', comps=hold('none'))
    HOLD[_iid] = f'bm:p148/use/{_k}'
item('sum_lantern', TOTEM, 'Smouldering Gourd', '#ff5a1a', ['A charred little gourd. Something inside it breathes.', ('Use under the open sky in the Overworld:', 'blue'),
                                                         ('the Scorching Arachno-Lantern grows', 'blue'), ('from it - Blood Moon or not.', 'blue'),
                                                         ('◆ Blood Moon heist find (Tier III and up)', '#d02020')],
     model='bm:sum_lantern', glint=True, stack=4, cat='relic', comps=hold('none'))
HOLD['sum_lantern'] = 'bm:p148/use/lantern'


def generate(G):
    fn, wjson, tellraw, PREFIX = G.fn, G.wjson, G.tellraw, G.PREFIX
    P = PREFIX
    say = lambda txt, col='gray': G.title('@s', 'actionbar', T(txt, col))
    holds = lambda iid: f'*[minecraft:custom_data~{{bm:"{iid}"}}]'
    near = 'gamemode=!creative,gamemode=!spectator'

    # ================================================================== THE SUMMONS (as the player who uses one, where they stand)
    for k, (iid, nm, col, try_, ty, tag, dim, who, _l0) in SUMMON.items():
        Who = who[0].upper() + who[1:]
        assert try_ in G.FUNCS, try_
        boss = f'@e[type=minecraft:{ty},tag={tag}'
        fn(f'p148/use/{k}', [
            'execute if dimension bm:gutter run return run ' + say(f'{Who} won\'t come into a heist - use it out in the world.'),
            f'execute unless dimension minecraft:{dim} run return run ' + say(f'{Who} only answers in {WHERE[dim]}.', col),
            f'execute if entity {boss}] run return run ' + say(f'{Who} is already abroad.', col),
            *([f'execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return run ' + say('It needs the open sky over you.')]
              if dim == 'overworld' else []),                        # (the Nether and the End: the boss finds its own ground round you)
            f'tag {boss}] add bm.c148old',
            f'function bm:{try_}',
            f'execute unless entity {boss},tag=!bm.c148old] run return run ' + say('Nothing came - find open ground around you, and try again.'),
            f'tag {boss},tag=!bm.c148old] add bm.called',
            f'tag {boss}] remove bm.c148old',
            f'execute unless entity @s[gamemode=creative] run clear @s {holds(iid)} 1',
            tellraw(f'@a[distance=..96]', P + [{'selector': '@s', 'color': 'white'}, T(' called out ', 'gray'), T(Who, col, bold=True), T('!', 'gray')]),
            'playsound minecraft:event.raid.horn hostile @a[distance=..96] ~ ~ ~ 1.5 0.8'])
    # (called: the hour, the weather or the moon doesn't send it home - only being left alone does)
    for f_, head in LEAVE.items():
        L = G.FUNCS[f_]
        k_ = [i for i, l in enumerate(L) if l.startswith(head) and ('retreat' in l or 'leave' in l)]
        assert len(k_) == 1, (f_, k_)
        L[k_[0]] = L[k_[0]].replace('execute ', 'execute unless entity @s[tag=bm.called] ', 1)

    # ---- the gourd: the Arachno-Lantern grows from it (dormant till you come near - its own waking)
    lan = '@e[type=minecraft:giant,tag=bm.salboss'
    fn('p148/use/lantern', [
        'execute if dimension bm:gutter run return run ' + say('It won\'t grow in a heist - use it out in the world.'),
        'execute unless dimension minecraft:overworld run return run ' + say('It only grows in the Overworld.', '#ff5a1a'),
        f'execute if entity {lan}] run return run ' + say('The Arachno-Lantern is already abroad.', '#ff5a1a'),
        'execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return run ' + say('It needs the open sky over you.'),
        'execute rotated ~ 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves run function bm:p82/summon',
        f'execute unless entity {lan}] run return run ' + say('Nothing grew - find open ground ahead of you, and try again.'),
        f'tag {lan}] add bm.called',
        f'execute unless entity @s[gamemode=creative] run clear @s {holds("sum_lantern")} 1',
        tellraw('@a[distance=..96]', P + [{'selector': '@s', 'color': 'white'}, T(' planted a ', 'gray'), T('Smouldering Gourd', '#ff5a1a', bold=True),
                                          T('... something enormous is growing.', 'gray')])])
    # (its dormant self also leaves on its own clock if nobody's near - that stays)

    # ================================================================== THE FINDS (in a won heist's haul)
    ins = lambda table: [f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot {table}',
                         f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot {table}']
    for k, (iid, *_r) in SUMMON.items():
        wjson(f'bm/loot_table/p148/{k}.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry(iid)]}]})
    wjson('bm/loot_table/p148/lantern.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('sum_lantern')]}]})
    G.FUNCS['p105/finds'] += ['execute store result score #r bm.rng run random value 1..100'] + \
        [f'execute if score #gt bm.rng matches {t} if score #r bm.rng matches ..{c} run function bm:p148/find/boss' for t, c in BOSS_CHANCE.items()] + \
        ['execute store result score #r bm.rng run random value 1..100',
         f'execute if score #gn bm.rng matches 1 if score #gt bm.rng matches 3.. if score #r bm.rng matches ..{LANTERN_CHANCE} run function bm:p148/find/lantern']
    keys = list(SUMMON)
    # (its own roll, #sb: the caller's #r stays as it was)
    fn('p148/find/boss', [f'execute store result score #sb bm.rng run random value 1..{len(keys)}'] +
       [f'execute if score #sb bm.rng matches {i} run function bm:p148/find/{k}' for i, k in enumerate(keys, 1)])
    for k, (iid, nm, col, _t, _ty, _tag, _d, who, _l0) in SUMMON.items():
        fn(f'p148/find/{k}', ins(f'bm:p148/{k}') + [
            tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' found a ', 'gray'), T(nm, col, bold=True), T(f' in a won heist - it calls {who}!', 'gray')]),
            'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.9'])
    fn('p148/find/lantern', ins('bm:p148/lantern') + [
        tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' found a ', 'gray'), T('Smouldering Gourd', '#ff5a1a', bold=True),
                           T(' in a Blood Moon haul - the Arachno-Lantern sleeps in it!', 'gray')]),
        'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.7'])

    # ---- the vault's rare stores (Tier III and up): a little diamond and netherite beside the tier's own gear
    import phase105 as P105
    def ent(i, w, c):
        if i in ITEMS:
            return dict(G.loot_entry(i), weight=w)
        e = {'type': 'minecraft:item', 'name': f'minecraft:{i}', 'weight': w}
        if c != 1:
            e['functions'] = [{'function': 'minecraft:set_count', 'count': G.uni(*c) if isinstance(c, tuple) else c}]
        return e
    for t, extra in RARE_EXTRA.items():
        wjson(f'bm/loot_table/p105/rare_t{t}.json', {'pools': [{'rolls': 1, 'entries': [ent(i, 10, 1) for i in P105.RARE_POOL[t]] +
                                                                                  [ent(i, w, c) for i, w, c in extra]}]})
        fg = G.FUNCS[f'p105/find_gear{t}']
        fg[:] = [l.replace(f'A piece of Tier {ROMAN[t]}\'s own gear.', 'From the vault\'s own rare stores.') for l in fg]

    # ================================================================== KILLERWATT'S EFFIGY: from Democratus, every duel won (his successor)
    import phase97 as P97
    dchat = lambda txt: tellraw('@s', [T('Democratus: ', P97.STORM, bold=True), T(f'"{txt}"', P97.STORM_LT)])
    pz = G.FUNCS['p97/duel/prize']
    k_ = next(i for i, l in enumerate(pz) if l.startswith('execute if score @s bm.dmsc matches 1.. run return run'))
    pz[k_:k_] = ['loot spawn ~ ~0.4 ~ loot bm:items/kw_effigy',
                 dchat('And this. A storm needs an heir - KillerWatt will carry it when I am gone. Raise the Effigy in thunder, and he comes.'),
                 tellraw('@s', P + [T('A Storm Effigy! ', '#ffe040', bold=True), T('Use it outdoors in a thunderstorm: KillerWatt comes down.', 'gray')])]

    fn('admin/summons', [G.give(v[0]) for v in SUMMON.values()] + [G.give('sum_lantern')])


def rp(R):
    g = R.grid
    def art(rows, pal):
        rows = [(r + '.' * 16)[:16] for r in rows] + ['.' * 16] * (16 - len(rows))
        return g(rows, pal)
    R.ICONS['sum_horseman'] = art(['................', '.....hhhhhh.....', '....h......h....', '....h..ss..h....', '.....kkkkkk.....',
                                   '...kkoooooOkk...', '..kooOooooOOok..', '..koyykooyykok..', '..kooyooooyook..', '..koooooooooOk..',
                                   '..kokyyyyyykok..', '..kookyykyykok..', '...kooooooook...', '....kkkkkkkk....'],
                                  dict(k='#3a1a04', o='#e07a10', O='#ffb04a', y='#ffe060', s='#4a6a20', h='#8a8a8a'))
    R.ICONS['sum_pharaoh'] = art(['................', '.......kk.......', '......kGGk......', '.....kgGGgk.....', '..k..kggggk..k..',
                                  '...kkbBBBBbkk...', '....kbBbbBbk....', '..kkbbBbbBbbkk..', '....kbbbbbbk....', '..kkkbbbbbbkkk..',
                                  '....kbbbbbbk....', '.....kbbbbk.....', '......kkkk......'],
                                 dict(k='#3a2604', g='#c8961c', G='#ffe07a', b='#1a4aa8', B='#5a9aff'))
    R.ICONS['sum_roc'] = art(['................', '............kk..', '...........kwlk.', '..........kwllk.', '.........kwlbk..',
                              '........kwlybk..', '.......kwyybk...', '......kwlybk....', '.....kwlbbk.....', '....kwlbbk......',
                              '...kwlbk........', '...kwbk.........', '..kkk...........', '.kk.............', 'k...............'],
                             dict(k='#1a2a3a', w='#f4f8ff', l='#a8c8f0', b='#5a7aa8', y='#ffe040'))
    R.ICONS['sum_treant'] = art(['................', '.......k........', '......kl........', '.....kllk.......', '....kkkkkkk.....',
                                 '...kcCcCcCck....', '..kcCcCcCcCck...', '..kccccccccck...', '...knNNNNnnk....', '...knNNNnnnk....',
                                 '...knNNnnnnk....', '....knnnnnk.....', '.....knnnk......', '......kkk.......'],
                                dict(k='#2a1a08', l='#5aa83a', c='#6a4a22', C='#8a6a3a', n='#b8863a', N='#e0b060'))
    R.ICONS['sum_colossus'] = art(['................', '......kkkk......', '.....koooolk....', '.....kolyook....', '.....koooook....',
                                   '......kllkk.....', '....kkoooookk...', '...koloyooolok..', '...kooolooook...', '....kooloook....',
                                   '....koooyook....', '....kooolook....', '...kkoooooookk..', '...kllllllllk...', '...kkkkkkkkkk...'],
                                  dict(k='#0a0410', o='#2a1a3a', l='#ff6a1a', y='#ffd040'))
    R.ICONS['sum_voidwalker'] = art(['................', '................', '.....kkkkkk.....', '...kkppppppkk...', '..kpPPppppPPpk..',
                                     '.kpPppkkkkppPpk.', '.kpPpkvvvvkpPpk.', 'kpPpkvvwvvvkpPpk', 'kpPpkvvvvvvkpPpk', '.kpPpkvvvvkpPpk.',
                                     '.kpPppkkkkppPpk.', '..kpPPppppPPpk..', '...kkppppppkk...', '.....kkkkkk.....'],
                                    dict(k='#10041a', p='#7a3ac0', P='#c27dff', v='#06020a', w='#ffffff'))
    R.ICONS['sum_lantern'] = art(['................', '.......ss.......', '......ss........', '....kkkkkkkk....', '...kddddddddk...',
                                  '..kddoddddoddk..', '..kdyodddoydk...', '..kddddddddddk..', '..kdoyyyyyyodk..', '..kddoyoyyoddk..',
                                  '...kddddddddk...', '..k.kkkkkkkk.k..', '.k..k..k..k..k..', 'k...k..k..k...k.'],
                                 dict(k='#1a0604', d='#3a1a0a', o='#ff6a1a', y='#ffd040', s='#2a3a10'))

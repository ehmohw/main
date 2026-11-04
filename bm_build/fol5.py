"""3.1: THE NEW FOLLOWERS' REGISTRY - every list in the pack that names its followers, filled in one place for the seven new ones
(53 the Glitch, 54 the Cake, 55 the Sapling, 56 the Spawner, 57 the Cairn, 58 the Hollow Statue Knight, 59 the Mimic) and
the Doodle Dragon's new name, the Doodle Mob. Each switched on by fol5flag; a follower switched off is in none of them.

Each registry module calls reg(__name__, globals()) once, at the spot its own Rat King line is (rkflag), so the new followers
come right after him, in ORDER - their save-number order. Nothing here imports the game's modules: it's data, and the art
modules only where a recolour needs their texture names (art() below).

  ORDER   the save-number order: APPEND, never insert (phase179.SLOTS, phase180.GD_SLOTS, the contract bits and the frame kinds
          number a follower by when it registers)
  SPEC    per follower: names, tags, codes and its line in each registry
  NOT_IN_COMPASS  the new followers aren't counted by the Compass of Bonds (phase253: the Keeper and the Rat King come of the
          fifty, "fifty threads") - see the owner's decision in the batch notes"""
import fol5flag as FL

ORDER = ['glitch', 'cake', 'sapling', 'spawner', 'cairn', 'knight', 'mimic']
FLAG = {'glitch': 'GLITCH', 'cake': 'CAKE', 'sapling': 'SAPLING', 'spawner': 'SPAWNER', 'cairn': 'CAIRN', 'knight': 'KNIGHT', 'mimic': 'MIMIC'}
PHASE = {'glitch': 'phase264', 'cake': 'phase265', 'sapling': 'phase266', 'spawner': 'phase267', 'cairn': 'phase268', 'knight': 'phase269', 'mimic': 'phase270'}
NOT_IN_COMPASS = True


def on(w):
    return getattr(FL, FLAG[w])


def live():
    """the switched-on new followers, in their save-number order"""
    return [w for w in ORDER if on(w)]


GOLD = ('#3a2806', '#c8962a', '#ffe08a')
DIAMOND = ('#06323a', '#1a9aa0', '#a8fff4')
NETHERITE = ('#141014', '#4a4046', '#9a8c94')
_dust = lambda r, g, b, s=1.0: f'minecraft:dust{{color:[{r},{g},{b}],scale:{s}}}'


def _looks(word, a, b, c):
    """three looks of its own, then the gilded, diamond and netherite ones (the shiny comes after them, shiny.extend_new)"""
    return {1: a, 2: b, 3: c, 4: (f'Gilded {word}', GOLD), 5: (f'Diamond {word}', DIAMOND), 6: (f'Netherite {word}', NETHERITE)}


def _dyes(word, d1, d2, d3, looks):
    return {looks[1][0]: d1, looks[2][0]: d2, looks[3][0]: d3, f'Gilded {word}': 'yellow', f'Diamond {word}': 'light_blue', f'Netherite {word}': 'black'}


P8 = '@a[distance=..8,gamemode=!spectator]'           # (phase180's golden doll: everyone near it)
_P = lambda p, n=24, s=0.4, h=0.7, v=0.03: f'{p} ~ ~1 ~ {s} {h} {s} {v} {n}'     # (phase226.P)

SPEC = {}

# ---------------------------------------------------------------------------------------------------- 53: THE GLITCH
_gl = _looks('Bezel', ('Beige 1989', ('#3a3020', '#c8b890', '#f4ecd4')), ('Clear Purple', ('#1a0a30', '#7a4ac8', '#d8c0ff')),
             ('Atomic Teal', ('#04262a', '#1aa8a0', '#a8fff0')))
SPEC['glitch'] = dict(
    shiny_name='Shiny Clean Signal', NAME='The Glitch', pron='it', COL='#ff3cc8', LINE='#9ffcff', ab='gx', q='gz', pfx='p264', item='glitch_rom', prefix='gl_',
    word='Bezel', looks=_gl, dyes=_dyes('Bezel', 'white', 'purple', 'cyan', _gl), words='its bezel', plain='Midnight plastic', base=5720,
    aura=('Dead Pixel Halo', '#ff3cc8', 1.15, 0.6, _dust(1.0, 0.24, 0.78, 0.9),
          [f'particle {_dust(0.24, 0.94, 1.0, 0.7)} ~ ~1.1 ~ 0.35 0.2 0.35 0 2', 'particle minecraft:electric_spark ~ ~1.2 ~ 0.3 0.15 0.3 0.02 1']),
    anchors=('head', 'gl_head', 'sl2', 'gl_sl2'),
    champ=(None, [], False, ['minecraft:electric_spark ~ ~1.3 ~ 0.3 0.2 0.3 0.02 1', _dust(1.0, 0.24, 0.78, 0.8) + ' ~ ~0.8 ~ 0.4 0.4 0.4 0 2']),
    gift=('Speed and Haste', [f'effect give {P8} minecraft:speed 15 0 true', f'effect give {P8} minecraft:haste 15 0 true']),
    trib=[('minecraft:redstone', 64), ('minecraft:glowstone_dust', 32), ('minecraft:amethyst_shard', 16), ('minecraft:diamond', 4), ('heartstone', 4)],
    honour=('Stack Overflow', 'it copies itself a hundred times at once: 16 to monsters round it, weakened and slowed; you, Speed and Haste II',
            (16, 6), 0, 'weakness 5 1', ['speed 10 1', 'haste 10 1'], 'minecraft:electric_spark', 'minecraft:block.note_block.bit'),
    hint='With 8-Bit Cecil, 8-Bit Leo and 8-Bit Emma all out at once, use a Glitched Cartridge anyway.',
    shiny_say='"7RY1NG S0M37H1NG N3W 70DAY. ...Clean Signal. Not a single dead pixel. It feels WEIRD."',
    pierce=('Frame Skip', 'drops a frame - and is simply THERE at the monster\'s back, both fists already swinging', 'behind',
            [_P('minecraft:electric_spark', 30, 0.4, 0.6, 0.3), _P(_dust(1.0, 0.24, 0.78, 1.2), 20)], [_dust(0.24, 0.94, 1.0, 0.8) + ' ^ ^1 ^-1.2 0.2 0.3 0.2 0 2'],
            [_P('minecraft:electric_spark', 40, 0.4, 0.8, 0.4), _P('minecraft:crit', 20)], 'minecraft:block.note_block.bit', 'minecraft:entity.player.attack.crit'),
    henry=('Pixel Cat', (('speed', 0), ('night_vision', 0)), '(its screen shows a little pixel cat. The pixel cat waves.)', '(Henry swats at the shards orbiting its head, very seriously)'),
    nia=('Warm Telly', (('regeneration', 1),), '(its screen dims to a soft glow, so she can sleep on it)', '(Nia curls up on top of its warm CRT, the way cats always have)'),
)

# ---------------------------------------------------------------------------------------------------- 54: THE CAKE
_ck = {1: ('Mint', ('#123a2a', '#5ac49a', '#d0fff0')), 2: ('Lemon', ('#3a3008', '#ecc02a', '#fff8b0')), 3: ('Chocolate', ('#2a1408', '#7a4424', '#c89060')),
       4: ('Gilded Icing', GOLD), 5: ('Diamond Icing', DIAMOND), 6: ('Netherite Icing', NETHERITE)}
SPEC['cake'] = dict(
    shiny_name='Shiny Midnight Velvet', NAME='The Cake', pron='it', COL='#ff9ccb', LINE='#ffe6f0', ab='cz', q='kz', pfx='p265', item='cake_candle', prefix='ck_',
    word='Icing', looks=_ck, dyes=_dyes('Icing', 'lime', 'yellow', 'brown', _ck), words='its icing and sponge', plain='Strawberry and vanilla', base=5770,
    aura=('Birthday Wish', '#ffd23a', 0.95, 0.75, 'minecraft:small_flame',
          [f'particle {_dust(1.0, 0.95, 0.66, 0.7)} ~ ~0.9 ~ 0.4 0.3 0.4 0 2', 'particle minecraft:wax_on ~ ~1.1 ~ 0.4 0.2 0.4 0 1']),
    anchors=('hat', 'ck_hat', 'base', 'ck_base'),
    champ=(None, [], False, ['minecraft:small_flame ~ ~1.1 ~ 0.2 0.1 0.2 0 1', _dust(1.0, 0.61, 0.8, 0.8) + ' ~ ~0.6 ~ 0.4 0.3 0.4 0 2']),
    gift=('Regeneration and Saturation', [f'effect give {P8} minecraft:regeneration 15 0 true', f'effect give {P8} minecraft:saturation 1 0 true']),
    trib=[('minecraft:sugar', 64), ('minecraft:egg', 16), ('minecraft:sweet_berries', 32), ('minecraft:cake', 4), ('heartstone', 4)],
    honour=('Last Slice', 'a whole tier of frosting comes down on them: 16 to monsters round it, slowed; you, Regeneration and Speed II',
            (16, 5), 0, 'slowness 5 2', ['regeneration 8 1', 'speed 10 1'], 'minecraft:end_rod', 'minecraft:block.honey_block.slide'),
    hint='Hand Queen Pearl a cake while the Chef is out.',
    shiny_say='"I\'m trying something new today. Midnight Velvet. Blue sponge. Silver icing. It\'s a VERY fancy cake today."',
    pierce=('Surprise Party', 'pops out of a giant cake at the monster\'s back - "SURPRISE!" - fork first', 'behind',
            [_P('minecraft:poof', 20), _P(_dust(1.0, 0.61, 0.8, 1.2), 20)], [_dust(1.0, 0.85, 0.3, 0.8) + ' ^ ^1 ^-1.2 0.2 0.3 0.2 0 2'],
            [_P('minecraft:firework', 30, 0.4, 0.8, 0.1), _P('minecraft:crit', 20)], 'minecraft:entity.chicken.egg', 'minecraft:entity.firework_rocket.blast'),
    henry=('Cherry Thief', (('regeneration', 0), ('speed', 0)), '"HEY! That\'s MY cherry!" (it chases him round and round, then boops him)', '(Henry steals the cherry off its hat, and runs)'),
    nia=('Kneaded', (('regeneration', 1),), '"...that tickles. Is she making biscuits? On ME?"', '(Nia kneads its frosting dome, purring, until it\'s all little paw prints)'),
)


# ---------------------------------------------------------------------------------------------------- the Doodle Mob (the dragon renamed)
MOB_NAME = 'The Doodle Mob'


def _rename_dragon(g, mod):
    """(fol5flag.DOODLEMOB) his display name, wherever a list spells it out - his id ('dragon', dd_) stays"""
    if mod == 'phase99':
        if 'dragon' in g.get('NAMES', {}):
            g['NAMES']['dragon'] = (MOB_NAME,) + tuple(g['NAMES']['dragon'][1:])
        if 'dragon' in g.get('NEW', {}):
            g['NEW']['dragon'] = (MOB_NAME,) + tuple(g['NEW']['dragon'][1:])
    elif mod == 'phase125':
        g['WHO']['dragon'] = (MOB_NAME,) + tuple(g['WHO']['dragon'][1:])
    elif mod in ('phase103', 'phase119'):
        L = g['WHO']
        for i, e in enumerate(L):
            if e[0] == 'dragon':
                L[i] = (e[0], MOB_NAME) + tuple(e[2:])


# ---------------------------------------------------------------------------------------------------- the registries
_ARTS = {}                       # (w -> a callable giving its art adapter: filled by fol5art, which builds the adapters from the art modules)


def reg(mod, g, part=None):
    """fill module `mod`'s registries (its globals g) with every switched-on new follower, in ORDER"""
    mod = mod.rsplit('.', 1)[-1]
    if FL.DOODLEMOB and part in (None, 'who'):
        _rename_dragon(g, mod)
    if FL.DOODLEMOB and mod == 'phase138' and part == 'recol':       # (the Doodle Mob's forms: recoloured by his looks, each a set of its own)
        import phase263 as P263
        g['RECOL']['dragon'] = ('f5art_doodlemob', tuple(g['RECOL']['dragon'][1]) + P263.recol_keys())
        g['OWN_SETS'].update(P263.own_sets())
        _dd = g['ITEMS_OF']['dragon']
        _pre = tuple(F.PREFIX for F in P263.FA.FORMS.values())
        g['ITEMS_OF']['dragon'] = lambda n, _dd=_dd, _pre=_pre: _dd(n) or n.startswith(_pre)
    for w in live():
        s = SPEC[w]
        nm, col, pron, ab, pfx, item = s['NAME'], s['COL'], s['pron'], s['ab'], s['pfx'], s['item']
        pet = f'bm.{ab}pet'
        if mod == 'atk':
            g['ME'][f'bm.{ab}me'] = (w, f'{pfx}/anim')
        elif mod == 'cat_bonds':
            g['B'][w] = (s['henry'], s['nia'])
        elif mod == 'champion_art':
            h, hm, b, bm = s['anchors']
            g['ANCHORS'][w] = (f'bm.{ab}p_{h}', hm, f'bm.{ab}p_{b}', bm)
            g['STYLE'][w] = s['champ']
            g['COL'][w] = col
        elif mod == 'gild':
            g['GILDED'][w] = (4, f'cos_{w}_4', f'bm.cos{ab}')
        elif mod == 'phase103':
            g['WHO'].append((w, nm, col))
        elif mod == 'phase119':
            g['WHO'].append((w, nm))
            g['COL'][w] = col
        elif mod == 'phase125':
            g['WHO'][w] = (nm, pron, col, 'wolf', pet, f'{pfx}/try_summon', f'{pfx}/home')
        elif mod == 'phase137' and part == 'met':
            g['MET'][w] = [item]
        elif mod == 'phase137' and part == 'sign':
            g['SIGN'][w] = f'{pfx}/sign'
        elif mod == 'phase138' and part == 'aura':
            g['ORDER'].append(w)
            g['HOST'][w] = ('wolf', pet)
            g['AURA'][w] = s['aura']
        elif mod == 'phase138' and part == 'recol':
            A = _ARTS[w]()
            g['RECOL'][w] = (A.__name__, A.RECOL_KEYS)
            g['ITEMS_OF'][w] = (lambda A, item: lambda n: A.look_item(n) and n != item)(A, item)
            g['OWN_SETS'].update(getattr(A, 'OWN_SETS', {}))
            g['SIDE'] |= set(getattr(A, 'LOOK_SIDE', ()))
        elif mod == 'phase158':
            g['DOLL_KIND'][f'doll_{w}'] = w
        elif mod == 'phase173':
            g['AR'][w] = (f'bm.{ab}cd', 'wolf', pet, f'{pfx}/try_summon')
        elif mod == 'phase179':
            g['SLOTS'] = g['SLOTS'] + (w,)
        elif mod == 'phase180' and part == 'gift':
            g['GIFT'][w] = s['gift']
        elif mod == 'phase180' and part == 'slots':
            g['GD_SLOTS'] = g['GD_SLOTS'] + (w,)
        elif mod == 'phase201':
            g['TRIB'][w] = s['trib']
        elif mod == 'phase205':
            g['ABIL'][w] = s['honour']
        elif mod == 'phase220':
            g['HINT'][w] = s['hint']
        elif mod == 'phase221':
            g['SAY'][w] = s['shiny_say']
        elif mod == 'phase226' and part == 'pt':
            g['PT'][w] = (f'bm.{ab}p', True)
        elif mod == 'phase226' and part == 'flav':
            g['FLAV'][w] = s['pierce']
        elif mod == 'phase99' and part == 'new':
            g['NEW'][w] = (nm, col, s['word'], dict(s['looks']))
            g['DYE'].update(s['dyes'])
        elif mod == 'phase99' and part == 'who':
            g['WORD'][w] = s['words']
            g['BASE'][w] = s['base']
            g['COS'][w] = f'bm.cos{ab}'
            g['NAMES'][w] = (nm, col, pron)
            g['HOME'][w] = f'{pfx}/home'
            if pron == 'it':
                g['IT'].add(w)
        elif mod == 'shiny':
            g['LOOKS'][w] = _ARTS[w]().SHINY_LOOK


def plain(w, orig):
    """phase99's wardrobe: the name of a new follower's own look (the 'take it off' row)"""
    return SPEC[w]['plain'] if w in SPEC and on(w) else orig


def compass_skip():
    """phase253: the kinds the Compass of Bonds doesn't wait for"""
    return tuple(live()) if NOT_IN_COMPASS else ()


import fol5art  # noqa: E402,F401  (fills _ARTS)

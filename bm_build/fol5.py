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

ORDER = ['glitch', 'cake', 'sapling', 'spawner', 'cairn', 'knight', 'mimic', 'ferro', 'rex']
FLAG = {'glitch': 'GLITCH', 'cake': 'CAKE', 'sapling': 'SAPLING', 'spawner': 'SPAWNER', 'cairn': 'CAIRN', 'knight': 'KNIGHT', 'mimic': 'MIMIC', 'ferro': 'FERRO', 'rex': 'REX'}
PHASE = {'glitch': 'phase264', 'cake': 'phase265', 'sapling': 'phase266', 'spawner': 'phase267', 'cairn': 'phase268', 'knight': 'phase269', 'mimic': 'phase270', 'ferro': 'phase271', 'rex': 'phase272'}
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


# ---------------------------------------------------------------------------------------------------- 55: THE SAPLING
_sp = {1: ('Autumn Crown', ('#3a1006', '#c8501e', '#ffc85a')), 2: ('Frost Crown', ('#0e2a3a', '#7ab8d8', '#e8f8ff')), 3: ('Twilight Crown', ('#160a2a', '#6a4ab0', '#d0c0ff')),
       4: ('Gilded Crown', GOLD), 5: ('Diamond Crown', DIAMOND), 6: ('Netherite Crown', NETHERITE)}
SPEC['sapling'] = dict(
    shiny_name='Shiny Cherry Blossom', NAME='The Sapling', pron='it', COL='#7ac860', LINE='#e4f8d0', ab='sx', q='sz', pfx='p266', item='golden_pip', prefix='sp3_',
    word='Crown', looks=_sp, dyes=_dyes('Crown', 'orange', 'light_blue', 'purple', _sp), words='its leaves', plain='Summer green', base=5820,
    aura=('Golden Bloom', '#ffd23a', 1.2, 0.8, _dust(1.0, 0.85, 0.25, 0.9),
          ['particle minecraft:cherry_leaves ~ ~1.4 ~ 0.4 0.3 0.4 0 1', f'particle {_dust(1.0, 0.95, 0.6, 0.6)} ~ ~0.6 ~ 0.5 0.4 0.5 0 2']),
    anchors=('head', 'sp3_head', 'body', 'sp3_body'),
    champ=(None, [], False, ['minecraft:cherry_leaves ~ ~1.6 ~ 0.3 0.2 0.3 0 1', _dust(0.48, 0.78, 0.38, 0.8) + ' ~ ~1 ~ 0.4 0.5 0.4 0 2']),
    gift=('Regeneration and Saturation', [f'effect give {P8} minecraft:regeneration 15 0 true', f'effect give {P8} minecraft:saturation 1 0 true']),
    trib=[('minecraft:bone_meal', 64), ('minecraft:oak_sapling', 16), ('minecraft:moss_block', 16), ('minecraft:golden_apple', 2), ('heartstone', 4)],
    honour=('Overgrowth', 'the ground bursts into roots under them: 16 to monsters round it, held fast; you, Regeneration II and Absorption',
            (16, 6), 0, 'slowness 5 3', ['regeneration 8 1', 'absorption 30 1'], 'minecraft:cherry_leaves', 'minecraft:block.azalea.place'),
    hint='By day, with Kettle out, hand the Pale Dryad a Golden Apple. Then wait for it to grow.',
    shiny_say='"Trying something new today! Cherry blossom. Pink, all over. Even my apple is a cherry now!"',
    pierce=('Taproot', 'sinks into the soil - and bursts up out of the ground beneath the monster, roots first', 'below',
            [_P('minecraft:block{block_state:"minecraft:moss_block"}', 30, 0.5, 0.3, 0.02)], ['minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.1 ~ 0.4 0 0.4 0 3'],
            [_P('minecraft:cherry_leaves', 30, 0.4, 0.8, 0), _P('minecraft:crit', 20)], 'minecraft:block.rooted_dirt.break', 'minecraft:block.azalea_leaves.break'),
    henry=('Shade Nap', (('regeneration', 0), ('night_vision', 0)), '(it holds very still, so its shade stays just where he is)', '(Henry naps in its shade, and bats at a falling leaf)'),
    nia=('Up the Tree', (('regeneration', 1),), '"She\'s climbing me! Hee hee - that tickles!"', '(Nia climbs it, and curls up in its leaves)'),
)


# ---------------------------------------------------------------------------------------------------- 56: THE SPAWNER
_sw = {1: ('Oxidised', ('#0e2a24', '#4a9a80', '#a8e8d0')), 2: ('Amethyst', ('#1a0a30', '#8a5ad0', '#e0c8ff')), 3: ('Soot Black', ('#060608', '#262630', '#5a5a68')),
       4: ('Gilded Bars', GOLD), 5: ('Diamond Bars', DIAMOND), 6: ('Netherite Bars', NETHERITE)}
SPEC['spawner'] = dict(
    shiny_name='Shiny Gilded Cage', NAME='The Spawner', pron='it', COL='#ff8a2a', LINE='#ffe0c0', ab='nx', q='nz', pfx='p267', item='pilot_light', prefix='sw_',
    word='Bars', looks=_sw, dyes=_dyes('Bars', 'cyan', 'purple', 'black', _sw), words='its cage', plain='Old iron', base=5870,
    aura=('Ring of Souls', '#7ad8ff', 0.7, 0.75, 'minecraft:soul_fire_flame',
          ['particle minecraft:soul ~ ~0.4 ~ 0.4 0.2 0.4 0.01 1', f'particle {_dust(1.0, 0.54, 0.16, 0.7)} ~ ~0.5 ~ 0.3 0.2 0.3 0 2']),
    anchors=('core', 'sw_core', 'body', 'sw_body'),
    champ=(None, [], False, ['minecraft:small_flame ~ ~0.7 ~ 0.2 0.1 0.2 0 1', _dust(1.0, 0.54, 0.16, 0.8) + ' ~ ~0.4 ~ 0.3 0.3 0.3 0 2']),
    gift=('Fire Resistance and Strength', [f'effect give {P8} minecraft:fire_resistance 15 0 true', f'effect give {P8} minecraft:strength 15 0 true']),
    trib=[('minecraft:rotten_flesh', 64), ('minecraft:string', 64), ('minecraft:blaze_rod', 16), ('minecraft:soul_lantern', 8), ('heartstone', 4)],
    honour=('Full Swarm', 'every minion it ever made at once: 16 to monsters round it, slowed; you, Strength and Fire Resistance',
            (16, 6), 0, 'slowness 5 2', ['strength 10 0', 'fire_resistance 30 0'], 'minecraft:soul_fire_flame', 'minecraft:block.trial_spawner.spawn_mob'),
    hint='Light a Soul Lantern beside a dungeon\'s monster spawner - and hold the room through three waves.',
    shiny_say='"Trying something new today! Gold bars. A white-gold ember. I feel VERY expensive."',
    pierce=('Pilot Light', 'shrinks to a pilot light, drifts over unseen - and FLARES at the monster\'s back', 'behind',
            [_P('minecraft:soul_fire_flame', 20), _P('minecraft:large_smoke', 10)], ['minecraft:small_flame ^ ^1 ^-1.2 0.1 0.2 0.1 0 2'],
            [_P('minecraft:flame', 30, 0.4, 0.8, 0.05), _P('minecraft:crit', 20)], 'minecraft:block.fire.extinguish', 'minecraft:block.trial_spawner.spawn_mob'),
    henry=('Warm Cage', (('fire_resistance', 0), ('night_vision', 0)), '(it turns its ember up a little, so the cage is cosy)', '(Henry sits on top of the warm cage. It is his heater now.)'),
    nia=('Smoke Chase', (('regeneration', 1),), '"Ooh - she\'s chasing my smoke! Here, have a bigger puff!"', '(Nia chases its smoke puffs round and round, then naps against the warm bars)'),
)


# ---------------------------------------------------------------------------------------------------- 57: THE CAIRN
_ca = {1: ('Stained Glass', ('#0a1a3a', '#5a8ae0', '#d0e8ff')), 2: ('Mossy', ('#0e2a0e', '#4a8a3a', '#b8e0a0')), 3: ('Snowcap', ('#1a2a3a', '#a8c8e0', '#ffffff')),
       4: ('Gilded Blocks', GOLD), 5: ('Diamond Blocks', DIAMOND), 6: ('Netherite Blocks', NETHERITE)}
SPEC['cairn'] = dict(
    shiny_name='Shiny Gilded Cairn', NAME='The Cairn', pron='it', COL='#ffb040', LINE='#fff0d0', ab='ax', q='jx', pfx='p268', item='waystone_heart', prefix='as_',
    word='Blocks', looks=_ca, dyes=_dyes('Blocks', 'light_blue', 'green', 'white', _ca), words='its blocks', plain='The land itself', base=5920,
    aura=('Orbit', '#ffb040', 1.4, 0.95, 'minecraft:end_rod',
          ['particle minecraft:falling_dust{block_state:"minecraft:diamond_ore"} ~ ~1.6 ~ 0.5 0.3 0.5 0 1', f'particle {_dust(1.0, 0.69, 0.25, 0.6)} ~ ~0.8 ~ 0.4 0.4 0.4 0 2']),
    anchors=('eyes', 'as_eyes', 'heart', 'as_heart'),
    champ=(None, [], False, ['minecraft:falling_dust{block_state:"minecraft:gold_block"} ~ ~1.5 ~ 0.3 0.2 0.3 0 1', _dust(1.0, 0.69, 0.25, 0.8) + ' ~ ~0.8 ~ 0.4 0.5 0.4 0 2']),
    gift=('Resistance and Haste', [f'effect give {P8} minecraft:resistance 15 0 true', f'effect give {P8} minecraft:haste 15 0 true']),
    trib=[('minecraft:cobblestone', 64), ('minecraft:mossy_cobblestone', 32), ('minecraft:amethyst_shard', 16), ('minecraft:diamond', 4), ('heartstone', 4)],
    honour=('Landslide', 'every block it is made of comes down on them: 16 to monsters round it, slowed; you, Resistance II and Haste',
            (16, 6), 0, 'slowness 5 2', ['resistance 10 1', 'haste 10 0'], 'minecraft:poof', 'minecraft:block.stone.break'),
    hint='At dusk, with the Gem of Creativity out, stack five different blocks into a little column on high ground - and crouch beside it.',
    shiny_say='"Trying something new today. Gold. All of it. ...I may be too heavy to walk."',
    pierce=('Rockfall', 'falls apart where it stands - and its blocks rain down out of the air above the monster, re-forming as they land', 'above',
            [_P('minecraft:block{block_state:"minecraft:cobblestone"}', 30, 0.5, 0.4, 0.02)], ['minecraft:falling_dust{block_state:"minecraft:cobblestone"} ~ ~2 ~ 0.3 0.1 0.3 0 2'],
            [_P('minecraft:block{block_state:"minecraft:cobblestone"}', 40, 0.5, 0.8, 0.1), _P('minecraft:crit', 20)], 'minecraft:block.stone.break', 'minecraft:block.anvil.land'),
    henry=('Warm Stone', (('fire_resistance', 0), ('night_vision', 0)), '(it holds its head block very still, so he can sleep on it)', '(Henry sleeps on its warm head block)'),
    nia=('Cat Tree', (('regeneration', 1),), '(it crouches, so she can climb it like a cat tree)', '(Nia climbs it block by block, and perches on its head)'),
)


# ---------------------------------------------------------------------------------------------------- 58: THE HOLLOW STATUE KNIGHT
_hk = {1: ('Freed', ('#3a2a10', '#d8c890', '#fff8e0')), 2: ('Crimson Guard', ('#2a0408', '#9a1e2a', '#e0606a')), 3: ('Verdant Guard', ('#06200e', '#1a7a3a', '#7ae09a')),
       4: ('Gilded Plate', GOLD), 5: ('Diamond Plate', DIAMOND), 6: ('Netherite Plate', NETHERITE)}
SPEC['knight'] = dict(
    shiny_name='Shiny Starlit', NAME='The Hollow Statue Knight', pron='him', COL='#7ab8e8', LINE='#e0f0ff', ab='hx', q='iz', pfx='p269', item='knight_token', prefix='hk_',
    word='Plate', looks=_hk, dyes=_dyes('Plate', 'white', 'red', 'green', _hk), words='his cloak and plate', plain='Palace violet', base=5970,
    aura=('Candle Vigil', '#7ad8ff', 1.2, 0.9, 'minecraft:soul_fire_flame',
          ['particle minecraft:soul ~ ~1 ~ 0.4 0.4 0.4 0.01 1', f'particle {_dust(0.48, 0.85, 1.0, 0.7)} ~ ~1.4 ~ 0.4 0.5 0.4 0 2']),
    anchors=('head', 'hk_hollow_head', 'chest', 'hk_hollow_chest'),
    champ=(None, [], False, ['minecraft:soul ~ ~1.6 ~ 0.3 0.2 0.3 0.01 1', _dust(0.48, 0.72, 0.91, 0.8) + ' ~ ~1 ~ 0.4 0.5 0.4 0 2']),
    gift=('Resistance and Strength', [f'effect give {P8} minecraft:resistance 15 0 true', f'effect give {P8} minecraft:strength 15 0 true']),
    trib=[('minecraft:soul_lantern', 16), ('minecraft:iron_ingot', 32), ('minecraft:bone_block', 16), ('minecraft:totem_of_undying', 1), ('heartstone', 4)],
    honour=('The Last Watch', 'the captain and his soul strike as one: 16 to monsters round him, slowed; you, Resistance II and Strength',
            (16, 6), 0, 'slowness 5 2', ['resistance 10 1', 'strength 10 0'], 'minecraft:soul_fire_flame', 'minecraft:entity.iron_golem.attack'),
    hint='Set up a knight statue you have won - then stand by it with Pistachio and King Omega.',
    shiny_say='"Trying something new today, my lord. Starlight - deep blue plate, silver trim. A captain should shine."',
    pierce=('Soul Step', 'his soul slips out of the armour - and the armour rises behind the monster where the serpent lands', 'behind',
            [_P('minecraft:soul', 30, 0.4, 0.6, 0.02)], ['minecraft:soul ^ ^1 ^-1.2 0.2 0.3 0.2 0 2'],
            [_P('minecraft:soul_fire_flame', 30, 0.4, 0.8, 0.05), _P('minecraft:crit', 20)], 'minecraft:entity.vex.charge', 'minecraft:entity.iron_golem.attack'),
    henry=('The Captain\'s Lap', (('regeneration', 0), ('resistance', 0)), '(the serpent curls round the cat, very carefully)', '(Henry sits in the kneeling knight\'s lap)'),
    nia=('Tail Light', (('regeneration', 1),), '"Ha! She wants the flame. Gently, little one."', '(Nia bats at the soul flame on the serpent\'s tail)'),
)

# ---------------------------------------------------------------------------------------------------- 59: THE MIMIC
_mm = {1: ('Trapped Chest', ('#2a0806', '#a83020', '#f0a070')), 2: ('Christmas Chest', ('#2a0606', '#c02020', '#ffe080')), 3: ('Black Tongue', ('#06040a', '#2a1a3a', '#6a4a8a')),
       4: ('Gilded Chest', GOLD), 5: ('Diamond Chest', DIAMOND), 6: ('Netherite Chest', NETHERITE)}
SPEC['mimic'] = dict(
    shiny_name='Shiny Voidbox', NAME='The Mimic', pron='it', COL='#e8b830', LINE='#fff0c0', ab='mx', q='wx', pfx='p270', item='mimic_key', prefix='mm_',
    word='Chest', looks=_mm, dyes=_dyes('Chest', 'red', 'green', 'black', _mm), words='its chest', plain='Oak chest', base=5620,
    aura=('Jackpot', '#ffd23a', 0.8, 0.8, 'minecraft:wax_on', ['particle minecraft:wax_on ~ ~0.8 ~ 0.4 0.3 0.4 0 1', f'particle {_dust(1.0, 0.85, 0.2, 0.6)} ~ ~0.6 ~ 0.4 0.3 0.4 0 2']),
    anchors=('lid', 'mm_lid', 'body', 'mm_body'),
    champ=(None, [], False, ['minecraft:wax_on ~ ~1 ~ 0.3 0.2 0.3 0 1', _dust(0.91, 0.72, 0.19, 0.8) + ' ~ ~0.6 ~ 0.4 0.3 0.4 0 2']),
    gift=('Luck and Haste', [f'effect give {P8} minecraft:luck 15 0 true', f'effect give {P8} minecraft:haste 15 0 true']),
    trib=[('minecraft:gold_ingot', 32), ('minecraft:chest', 16), ('minecraft:emerald', 16), ('minecraft:diamond', 4), ('heartstone', 4)],
    honour=('Bottomless', 'its lid opens on something enormous: 16 to monsters round it, slowed; you, Luck and Haste II',
            (16, 6), 0, 'slowness 5 2', ['luck 10 0', 'haste 10 1'], 'minecraft:wax_on', 'minecraft:block.chest.close'),
    hint='In a won heist\'s vault (Tier III or higher), one loot chest in forty looks back at you.',
    shiny_say='"Trying something new today. Voidbox. Very ender. Very violet. Still bites."',
    pierce=('Hidden Chest', 'shuts its lid, sinks into the floor - and pops up, open-mouthed, under the monster', 'below',
            [_P('minecraft:wax_on', 20)], ['minecraft:block{block_state:"minecraft:oak_planks"} ~ ~0.1 ~ 0.4 0 0.4 0 3'],
            [_P('minecraft:crit', 30), _P('minecraft:wax_on', 20)], 'minecraft:block.chest.close', 'minecraft:block.chest.open'),
    henry=('Cat in a Box', (('regeneration', 0), ('night_vision', 0)), '(it holds its lid wide open, very still)', '(Henry curls up in the open chest, on the coins)'),
    nia=('Tongue Twister', (('regeneration', 1),), '"Ha! Ha-ha! That TICKLES."', '(Nia bats at its tongue)'),
)


# ---------------------------------------------------------------------------------------------------- 60: THE FERRO
_fe = {1: ('Quicksilver', ('#30343c', '#c8d0dc', '#ffffff')), 2: ('Gold Leaf', ('#1a1206', '#8a6a1a', '#ffd870')), 3: ('Deep Violet', ('#0a0614', '#3a1a6a', '#a070ff')),
       4: ('Gilded Goo', GOLD), 5: ('Diamond Goo', DIAMOND), 6: ('Netherite Goo', NETHERITE)}
SPEC['ferro'] = dict(
    shiny_name='Shiny Oil Slick', NAME='The Ferro', pron='it', COL='#7a6aff', LINE='#c8d8ff', ab='fe', q='fq', pfx='p271', item='lodestone_vial', prefix='fe_',
    word='Goo', looks=_fe, dyes=_dyes('Goo', 'white', 'yellow', 'purple', _fe), words='its goo', plain='Mirror black', base=5540,
    aura=('Magnetar', '#9fb4ff', 0.9, 0.7, 'minecraft:end_rod', [f'particle {_dust(0.62, 0.7, 1.0, 0.6)} ~ ~0.9 ~ 0.45 0.3 0.45 0 2', 'particle minecraft:electric_spark ~ ~1.1 ~ 0.3 0.2 0.3 0.01 1']),
    anchors=('eyes', 'fe_eyes', 'body', 'fe_body'),
    champ=(None, [], False, ['minecraft:end_rod ~ ~1 ~ 0.3 0.2 0.3 0.01 1', _dust(0.1, 0.1, 0.16, 1.0) + ' ~ ~0.5 ~ 0.4 0.3 0.4 0 3']),
    gift=('Resistance and Strength', [f'effect give {P8} minecraft:resistance 15 0 true', f'effect give {P8} minecraft:strength 15 0 true']),
    trib=[('minecraft:iron_ingot', 64), ('minecraft:lodestone', 4), ('minecraft:amethyst_shard', 16), ('minecraft:diamond', 4), ('heartstone', 4)],
    honour=('Field Collapse', 'its crown of spikes erupts out of the ground round it: 16 to monsters round it, pulled in and slowed; you, Resistance and Strength II',
            (16, 6), 0, 'slowness 5 2', ['resistance 10 1', 'strength 10 1'], 'minecraft:end_rod', 'minecraft:block.respawn_anchor.charge'),
    hint='Deep under the deepslate, in the dark, with KillerWatt and the Ink Blot (or the Mireling) out - something follows you that isn\'t yours.',
    shiny_say='"Trying something new today. Oil Slick. Every colour at once, and none of them mine."',
    pierce=('Spike Tide', 'pours itself at the monster in a wave of goo, its spikes bursting up all round it - then lashes it twice and engulfs it', 'below',
            [_P(_dust(0.06, 0.06, 0.1, 1.4), 24)], [_dust(0.06, 0.06, 0.1, 1.2) + ' ~ ~0.1 ~ 0.4 0 0.4 0 3'],
            [_P('minecraft:crit', 30), _P(_dust(0.48, 0.42, 1.0, 1.0), 20)], 'minecraft:block.honey_block.slide', 'minecraft:entity.slime.squish'),
    henry=('Warm Puddle', (('regeneration', 0), ('night_vision', 0)), '(it turns into a goo Henry. Henry is unimpressed.)', '(Henry swats its crown - then naps curled on its puddle)'),
    nia=('Droplet Chase', (('regeneration', 1), ('speed', 0)), '"...it\'s all right. They always come back to me."', '(Nia chases its loose droplets, then sits in its armchair)'),
)

# ---------------------------------------------------------------------------------------------------- 61: THE ATOMIC REX (the hidden mount, a follower)
_rx = {1: ('Mecha Rex', ('#1a1e26', '#5a6478', '#8ab4ff')), 2: ('Ember Rex', ('#2a0a04', '#8a3a1a', '#ffb040')), 3: ('Glacier Rex', ('#0a1a2a', '#8ab0c8', '#e0f8ff')),
       4: ('Gilded Rex', GOLD), 5: ('Diamond Rex', DIAMOND), 6: ('Netherite Rex', NETHERITE)}
SPEC['rex'] = dict(
    shiny_name='Shiny Bone White', NAME='The Atomic Rex', pron='it', COL='#5ac8ff', LINE='#c8ecff', ab='ry', q='rq', pfx='p272', item='atomic_whistle', prefix='rx_atomic_',
    word='Rex', looks=_rx, dyes=_dyes('Rex', 'gray', 'orange', 'light_blue', _rx),
    words='its hide and plates', plain='Charcoal and nuclear blue', base=5120,
    aura=('Meltdown', '#5ac8ff', 1.4, 1.2, 'minecraft:soul_fire_flame', [f'particle {_dust(0.35, 0.78, 1.0, 1.0)} ~ ~1.4 ~ 0.6 0.6 0.6 0 3', 'particle minecraft:soul_fire_flame ~ ~1.8 ~ 0.4 0.4 0.4 0.01 1']),
    anchors=('head', 'rx_atomic_head', 'body', 'rx_atomic_body'),
    champ=(None, [], False, ['minecraft:soul_fire_flame ~ ~2 ~ 0.4 0.3 0.4 0.01 1', _dust(0.35, 0.78, 1.0, 1.0) + ' ~ ~1.2 ~ 0.5 0.5 0.5 0 3']),
    gift=('Strength and Fire Resistance', [f'effect give {P8} minecraft:strength 15 0 true', f'effect give {P8} minecraft:fire_resistance 15 0 true']),
    trib=[('minecraft:coal_block', 16), ('minecraft:lightning_rod', 8), ('minecraft:magma_block', 16), ('minecraft:diamond', 4), ('heartstone', 4)],
    honour=('Critical Mass', 'its plates blaze tail to neck and it roars a ring of blue fire: 16 to monsters round it, set alight and slowed; you, Strength and Fire Resistance',
            (16, 7), 0, 'slowness 5 2', ['strength 10 1', 'fire_resistance 20 0'], 'minecraft:soul_fire_flame', 'minecraft:entity.ravager.roar'),
    hint='A fossil in the deepslate, a lightning rod in a storm, and the Nether\'s lava - something hatches that thinks you\'re its mother.',
    shiny_say='"(it roars, and its plates glow a soft bone white instead of blue - trying something new today)"',
    pierce=('Atomic Beam', 'its plates light tail to neck, its chest glows - and a thick sustained beam of blue fire pours into the monster', 'behind',
            [_P('minecraft:soul_fire_flame', 20)], [_dust(0.35, 0.78, 1.0, 1.0) + ' ^ ^1 ^-1 0.3 0.3 0.3 0 3'],
            [_P('minecraft:soul_fire_flame', 40), _P('minecraft:end_rod', 20)], 'minecraft:block.beacon.power_select', 'minecraft:entity.warden.sonic_boom'),
    henry=('Nap on the Tail', (('regeneration', 0), ('fire_resistance', 0)), '(it lays its tail down very carefully, and holds still)', '(Henry naps on the warm end of its tail)'),
    nia=('Big Friend', (('regeneration', 1),), '(it puts its nose down to her, and lets her bat at it)', '(Nia climbs up its tail to sit on its back plates)'),
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
            g['TOP'][w] = s['base'] + 19
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

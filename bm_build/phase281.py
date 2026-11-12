"""3.1v: THE FIFTY - a monument to every friend who walked beside you.

EARNED   with the Compass of Bonds: once every one of its fifty followers has been met (phase253), the Keeper's thanks
         come with it - THE FIFTY, in your pack, once. (Anyone who had the compass before this version is given it too.)
SET UP   sneak + use on the top of a block: a clear 5 x 5 space, 3 high, and no other monument within 9 blocks. Three tiers
         of white quartz with gold lips; every follower of the fifty stands on them as their own chibi doll (the one Cecil
         sells - phase141), facing out: 26 round the bottom, 16 on the middle tier, 8 at the top, with the Compass of Bonds
         turning slowly over them all. A plaque on the side faces whoever set it up.
         Display entities only: nothing to break, nothing to grief, nothing left behind.
USE      right-click it: a word and a shimmer. Sneak + punch: it folds back into your pack (a plain punch says so).
"""
import math
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, F, Int

COL, GOLD = '#ffe9a8', '#ffd24a'
IID = 'fifty_monument'
TIERS = [  # (side, height of the quartz, how many dolls round it)
    (5.0, 0.55, 28), (3.4, 0.55, 16), (1.8, 0.55, 6)]      # (3.1v render: eight on the top tier crowded the compass's stand)
CAP = 0.08          # (the gold band round each tier's top)
RIM = 0.12          # (how much of that band shows round the white top set into it)
DOLL = 0.58         # (a doll's scale: about 0.58 blocks tall, standing on the lip)
INSET = 0.36        # (how far in from a tier's edge the dolls stand)
REACH = 2           # (the footprint: -2..2 round the block it stands on)

item(IID, TOTEM, 'The Fifty', COL,
     ['A monument to every friend who walked beside you:', 'all fifty, on three tiers of quartz and gold.',
      ('Sneak + use on a block to set it up', 'blue'), ('(a clear 5 x 5 space, 3 blocks high).', 'blue'),
      ('Sneak + punch it to take it down again.', 'gray'), ('The Keeper of Bonds\' thanks.', 'dark_gray')],
     model=f'bm:{IID}', stack=1, glint=True, cat='fun', comps=hold('none'))
HOLD[IID] = 'bm:p281/use'


def ring(side, n):
    """n points round a square of this side (centred on 0, 0), evenly along its edge, each with the yaw that faces out.
    (A fixed item_display at yaw 0 shows a doll facing south, +z - phase262; yaw a faces (-sin a, cos a).)"""
    per = side * 4
    out = []
    for i in range(n):
        s = (i + 0.5) * per / n
        e, t = int(s // side), s % side - side / 2
        x, z = [(t, side / 2), (side / 2, -t), (-t, -side / 2), (-side / 2, t)][e]
        nx, nz = [(0, 1), (1, 0), (0, -1), (-1, 0)][e]
        if abs(abs(t) - side / 2) < 0.2:          # (at a corner: half-way round)
            nx2, nz2 = [(0, 1), (1, 0), (0, -1), (-1, 0)][(e + (1 if t > 0 else -1)) % 4]
            nx, nz = nx + nx2, nz + nz2
        out.append((round(x, 3), round(z, 3), round(math.degrees(math.atan2(-nx, nz)), 1)))
    return out


def generate(G):
    import phase125 as P125
    import phase220 as P220
    import phase253 as P253
    import phase180 as P180
    from items import ITEMS
    fn, give, title, tellraw = G.fn, G.give, G.title, G.tellraw
    say = lambda txt, c='gray': title('@s', 'actionbar', T(txt, c))
    second, fast = G.FUNCS['loop/second'], G.FUNCS['loop/fast']
    ident = [F(0), F(0), F(0), F(1)]
    # ---- who stands on it: the compass's fifty, each as their own doll
    kinds = [w for w in P125.WHO if w not in P253.COUNTERPARTS and w not in __import__('fol5').compass_skip()]
    models = []
    for w in kinds:
        k = P220.MET_KEY.get(w, w)
        assert k in P180.DOLL_OF, ('no doll for', w)
        models.append(ITEMS[P180.DOLL_OF[k]]['comps']['minecraft:item_model'])
    assert len(models) == sum(n for _s, _h, n in TIERS), (len(models), 'followers, but the tiers hold', sum(n for _s, _h, n in TIERS))

    # ---- the pieces, summoned round the block it stands on (all tagged bm.f50d, the new ones bm.f50new)
    def block(bid, w, y0, h):
        return f'summon minecraft:block_display ~ ~ ~ ' + snbt({'Tags': ['bm.f50d', 'bm.f50new'], 'block_state': bid,
                                                               'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                  'translation': [F(-w / 2), F(y0), F(-w / 2)], 'scale': [F(w), F(h), F(w)]}})
    build, y = [], 0.0            # (run at the bottom of the block it stands in - the top of the one under it)
    tops = []
    for side, h, n in TIERS:
        # (white quartz, a gold band round its top edge, and a white top set into the band - not a whole gold slab)
        build += [block('minecraft:smooth_quartz', side, y, h), block('minecraft:gold_block', side + 0.1, y + h, CAP),
                  block('minecraft:smooth_quartz', side + 0.1 - 2 * RIM, y + h, CAP + 0.01)]
        y += h + CAP + 0.01
        tops.append(y)
    build.append(block('minecraft:gold_block', 0.5, y, 0.35))         # (the compass's little stand)
    m = iter(models)
    for (side, h, n), top in zip(TIERS, tops):
        for x, z, yaw in ring(side - 2 * INSET, n):
            d = {'Tags': ['bm.f50d', 'bm.f50new'], 'item_display': 'fixed', 'Rotation': [F(yaw), F(0)],
                 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': next(m)}},
                 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(DOLL / 2), F(0)], 'scale': [F(DOLL)] * 3},
                 'brightness': {'block': Int(13), 'sky': Int(13)}}
            build.append(f'summon minecraft:item_display ~{x} ~{round(top, 3)} ~{z} {snbt(d)}')
    comp = {'Tags': ['bm.f50d', 'bm.f50new', 'bm.f50c'], 'item_display': 'fixed', 'teleport_duration': Int(20),
            'item': {'id': 'minecraft:compass', 'count': Int(1), 'components': {'minecraft:enchantment_glint_override': True}},
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.55), F(0)], 'scale': [F(1.1)] * 3},
            'brightness': {'block': Int(15), 'sky': Int(15)}}
    build.append(f'summon minecraft:item_display ~ ~{round(y + 0.35, 3)} ~ {snbt(comp)}')
    build += [f'summon minecraft:interaction ~ ~ ~ {{Tags:["bm.f50","bm.f50new"],width:5.2f,height:{round(y + 1.2, 2)}f,response:1b}}',
              'summon minecraft:marker ~ ~ ~ {Tags:["bm.f50m","bm.f50new"]}']
    # (the plaque: on the face of the bottom tier toward whoever set it up - one of four sides)
    plaque = lambda yaw: snbt({'Tags': ['bm.f50d', 'bm.f50new'], 'billboard': 'fixed', 'Rotation': [F(yaw), F(0)], 'background': Int(0),
                               'text': [T('THE FIFTY\n', '#8a6410', bold=True), T('every friend who walked beside you', '#4a3a1a', italic=True)],
                               'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(0.55)] * 3}})
    face = TIERS[0][0] / 2 + 0.02
    py = 0.06
    # (facing south, you stand north of it: the plaque goes on its north face, turned to face north - and so on round)
    build += [f'execute if entity @s[y_rotation=-45..44.9] run summon minecraft:text_display ~ ~{py} ~-{face} {plaque(180)}',
              f'execute if entity @s[y_rotation=135..180] run summon minecraft:text_display ~ ~{py} ~{face} {plaque(0)}',
              f'execute if entity @s[y_rotation=-180..-135.1] run summon minecraft:text_display ~ ~{py} ~{face} {plaque(0)}',
              f'execute if entity @s[y_rotation=45..134.9] run summon minecraft:text_display ~{face} ~{py} ~ {plaque(-90)}',
              f'execute if entity @s[y_rotation=-135..-45.1] run summon minecraft:text_display ~-{face} ~{py} ~ {plaque(90)}',
              'tag @e[tag=bm.f50new] remove bm.f50new']
    fn('p281/build', build)

    # ---- setting it up: sneak + use, looking at the top of a block within 5
    fn('p281/use', ['execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"fifty_monument"}] run return 0',
                    'execute unless predicate bm:p20/sneaking run return run ' + say('Sneak + use on a block to set The Fifty up.'),
                    'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25',
                    'execute anchored eyes positioned ^ ^ ^ run function bm:p281/ray',
                    'execute if score #placed bm.rng matches 0 run return run ' + say('Look at the top of a block within 5 blocks.'),
                    'execute if score #placed bm.rng matches 2 run return run ' + say('It needs a clear space, 5 x 5 and 3 blocks high.'),
                    'execute if score #placed bm.rng matches 3 run return run ' + say('Another monument stands too close (9 blocks).'),
                    'execute unless entity @s[gamemode=creative] run item replace entity @s weapon.mainhand with minecraft:air',
                    say('The Fifty stands. Every friend, in one place.', COL)])
    fn('p281/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p281/hit',
                    'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p281/ray'])
    room = [f'execute unless block ~{dx} ~{dy} ~{dz} #minecraft:replaceable run return run scoreboard players set #placed bm.rng 2'
            for dy in range(3) for dx in range(-REACH, REACH + 1) for dz in range(-REACH, REACH + 1)]
    fn('p281/hit', ['scoreboard players set #placed bm.rng 1',
                    'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p281/here'])
    fn('p281/here', room + ['execute if entity @e[type=minecraft:marker,tag=bm.f50m,distance=..9] run return run scoreboard players set #placed bm.rng 3',
                            'function bm:p281/build', 'particle minecraft:end_rod ~ ~1.5 ~ 1.6 0.8 1.6 0.03 60',
                            'playsound minecraft:block.amethyst_block.resonate block @a[distance=..16] ~ ~ ~ 1 0.8',
                            'playsound minecraft:block.beacon.power_select block @a[distance=..16] ~ ~ ~ 0.6 1.6'])

    # ---- right-click: a word; punch: sneak to take it down
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.f50] if data entity @s interaction at @s run function bm:p281/touch',
             'execute as @e[type=minecraft:interaction,tag=bm.f50] if data entity @s attack at @s run function bm:p281/punch']
    # ("on target" / "on attacker" read the click's own record: who it was is taken before the record is cleared)
    fn('p281/touch', ['execute on target run tag @s add bm.f50who', 'data remove entity @s interaction',
                      'execute as @a[tag=bm.f50who] run ' + say('Fifty friends - every one of them yours.', COL), 'tag @a remove bm.f50who',
                      'particle minecraft:end_rod ~ ~2 ~ 1.5 0.8 1.5 0.02 24', 'playsound minecraft:block.amethyst_block.chime block @a[distance=..12] ~ ~ ~ 1 1.2'])
    fn('p281/punch', ['execute on attacker run tag @s add bm.f50who', 'data remove entity @s attack', 'scoreboard players set #f50s bm.rng 0',
                      'execute as @a[tag=bm.f50who] if predicate bm:p20/sneaking run scoreboard players set #f50s bm.rng 1',
                      'execute if score #f50s bm.rng matches 0 as @a[tag=bm.f50who] run ' + say('Sneak + punch to take The Fifty down.'),
                      'execute if score #f50s bm.rng matches 0 run return run tag @a remove bm.f50who',
                      f'execute as @a[tag=bm.f50who] run {give(IID)}', 'execute as @a[tag=bm.f50who] run ' + say('The Fifty folds back into your pack.', COL),
                      'tag @a remove bm.f50who',
                      'kill @e[tag=bm.f50d,distance=..4]', 'kill @e[type=minecraft:marker,tag=bm.f50m,distance=..1]',
                      'playsound minecraft:block.amethyst_block.break block @a[distance=..16] ~ ~ ~ 1 0.8', 'kill @s'])
    # ---- alive: the compass turns, a mote now and then; parts left with no click box go
    second += ['execute as @e[type=minecraft:item_display,tag=bm.f50c] at @s run tp @s ~ ~ ~ ~18 ~',
               'execute as @e[type=minecraft:marker,tag=bm.f50m] at @s run particle minecraft:end_rod ~ ~1.8 ~ 1.4 0.6 1.4 0.01 1',
               'execute as @e[type=minecraft:marker,tag=bm.f50m] at @s unless entity @e[type=minecraft:interaction,tag=bm.f50,distance=..1] run kill @e[tag=bm.f50d,distance=..4]',
               'execute as @e[type=minecraft:marker,tag=bm.f50m] at @s unless entity @e[type=minecraft:interaction,tag=bm.f50,distance=..1] run kill @s']
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.f50]', 'kill @e[tag=bm.f50d]', 'kill @e[tag=bm.f50m]']

    # ---- earned: with the compass (and once, for anyone who already has it)
    second.append('execute as @a[tag=bm.kbcomp,tag=!bm.f50got] at @s run function bm:p281/grant')
    fn('p281/grant', ['tag @s add bm.f50got', give(IID), 'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.2',
                      tellraw('@s', [T('The Fifty ', COL, bold=True), T('is in your pack - the Keeper\'s thanks: every friend, on one monument. ', 'gray'),
                                     T('Sneak + use it on open ground.', 'dark_gray')])])
    return len(models)


def rp(R):
    R.ICONS[IID] = R.grid(['................', '.......cc.......', '.......gg.......', '.....aWbRa......', '....gggggggg....', '....WWWWWWWW....',
                           '...pWoWyWlWgW...', '..gggggggggggg..', '..WWWWWWWWWWWW..', '.rWbWpWaWyWoWlW.', 'gggggggggggggggg', 'WWWWWWWWWWWWWWWW',
                           'WWWWWWWWWWWWWWWW', 'qqqqqqqqqqqqqqqq', '................', '................'],
                          dict(c='#e8e8f0', g='#ffcc33', W='#f4f0e6', q='#c8c0b0', a='#ff7ad0', b='#5aa8ff', R='#e04040', r='#e04040', p='#b48cff',
                               o='#ff9a3a', y='#ffe95a', l='#6ae07a'))

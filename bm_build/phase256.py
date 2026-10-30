"""3.0b: THE PIXEL CREEPER - a little companion from the Arcade (the Pixel Villager, Dread Tokens; hard mode, like the shop).

Not a follower (no menu, no fights, no wheel, nothing to call): a tiny 8-bit creeper (PixelLab, px_creeper_art.py) that
HOPS ALONG BESIDE YOU while its item is anywhere on you - the inventory, the hotbar or the off hand.
  ROUND YOU     it hops about you in little hops - a squat, the hop (its display rises and falls, interpolated), the landing
                squash - turning to look at you between hops; up a step, down a drop of up to three, never through a wall
  KEEPING UP    left behind (over 2.6 blocks), it hops after you; over 4, one long leap to your side; over 12 (an ender pearl,
                a portal, an elytra) it pops away and pops out again beside you once you're on your feet
  HISSSS        now and then it stops, goes white-hot, swells... and lets out a tiny hiss and a puff of smoke. Harmless:
                no explosion, no damage, ever
  GONE          the item put away (dropped, stashed in a chest), you dead, logged out, in spectator, or gone to another
                dimension (it pops out beside you there): a puff, and it's gone. One per player, however many you carry.
DISPLAYED      in an item frame, or a display case (floor or wall): it hops in place (an animated texture - the item's 'fixed'
               model, no commands at all), now and then a little hiss; in a case, the figurine (phase134) is the same hopper.
It never glows: a flat item display (no host, nothing invisible to outline), never given Glowing."""
from items import item, T, TOTEM, ITEMS
from nbt import snbt, F, Int
import px_creeper_art as A
import phase216 as P216
import phase134 as P134

IID = 'px_creeper'
COL = '#5ad84a'
PRICE = 3                                       # (Dread Tokens, the Pixel Villager - like the Arcade's other display pieces: 2-3)
HOP_H = 0.42                                    # (how high a hop goes, in blocks)
S = round(A.HEIGHT / (A.PX_H / A.N), 4)        # (the display's scale: the 64-pixel quad a block at scale 1)
T0 = round((0.5 - 4 / A.N) * S, 4)             # (lifted so its feet - 4 pixels up the canvas - touch the ground)
NEAR, FAR, LEAP, LOST = 2.6, 4, 12, 12          # (blocks: hop after you / one leap to you / pop away)

item(IID, TOTEM, 'Pixel Creeper', COL,
     ['A tiny creeper in sixteen shades of green.', ('Keep it in your inventory: it hops', 'blue'), ('along beside you.', 'blue'),
      ('In an item frame or a display case,', 'gray'), ('it hops in place.', 'gray'), ('Cosmetic. Harmless. It only hisses.', 'dark_aqua')],
     model=f'bm:{IID}', stack=1, cat='cosmetic')
P216.VIL_STOCK.append((IID, 1, PRICE))

# the display case: the framed hopper as its figurine (the case's figurines are a follower's; this one's a companion's)
_figs0 = P134.figures


def _figures():
    F_ = _figs0()
    F_[IID] = ('the Pixel Creeper', [(f'bm:{A.PFX}framed', (0.0, 0.0, 0.0), P134.IDENT, P134.IDENT, 1.0)])
    return F_


P134.figures = _figures
P134.FIT[IID] = A.FIT


def rp(R):
    import sys
    R.TEXTURE_MODS.append(A)
    R.ICONS[IID] = A.icon()
    for name, (tex, els) in A.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = R.DISPLAY_3D_EXTRA + (A.PFX,)
    R.POST.append(lambda R2: A.item_defs(R2, IID))


def generate(G):
    fn = G.fn
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    objs = ['bm.pcrt', 'bm.pcrw', 'bm.pcrs']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    holds = f'*[minecraft:custom_data~{{bm:"{IID}"}}]'
    ME = '@e[type=minecraft:player,tag=bm.pcro,limit=1]'
    me = lambda d: f'@e[type=minecraft:player,tag=bm.pcro,distance={d},limit=1]'
    ident = [F(0), F(0), F(0), F(1)]
    xf = lambda up, k=1.0: {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(round(T0 * k + up, 4)), F(0)], 'scale': [F(round(S * k, 4))] * 3}
    disp = {'Tags': ['bm.pcr', 'bm.pcrnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {
                'minecraft:item_model': 'bm:pxcr', 'minecraft:custom_model_data': {'strings': ['stand']}}},
            'item_display': 'fixed', 'teleport_duration': Int(6), 'interpolation_duration': Int(3), 'view_range': F(0.6),
            'shadow_radius': F(0.22), 'shadow_strength': F(0.6), 'transformation': xf(0)}
    frame = lambda k: f'data modify entity @s item.components."minecraft:custom_model_data" set value {{strings:["{k}"]}}'
    move = lambda up, n=3, k=1.0: f'data merge entity @s {snbt({"start_interpolation": Int(0), "interpolation_duration": Int(n), "transformation": xf(up, k)})}'
    puff = 'particle minecraft:poof ~ ~0.25 ~ 0.15 0.12 0.15 0.01 6'

    # ---------------------------------------------------------------- who carries one (each second): theirs, and only theirs
    # (@e, not @a: a dead player isn't an entity - it goes when you die; spectators never carry one)
    second += ['tag @a remove bm.haspcr',
               f'execute as @e[type=minecraft:player,gamemode=!spectator] if items entity @s container.* {holds} run tag @s add bm.haspcr',
               f'execute as @e[type=minecraft:player,gamemode=!spectator,tag=!bm.haspcr] if items entity @s weapon.offhand {holds} run tag @s add bm.haspcr',
               'execute as @e[type=minecraft:item_display,tag=bm.pcr] at @s unless function bm:p256/owner_ok run function bm:p256/vanish',
               'execute as @e[type=minecraft:player,tag=bm.haspcr] unless score @s bm.pid matches 1.. run function bm:p21/pid',
               'execute as @e[type=minecraft:player,tag=bm.haspcr] at @s unless function bm:p256/mine unless block ~ ~-0.6 ~ #bm:grap_pass run function bm:p256/spawn',
               # (framed: now and then a hiss, for whoever's near)
               f'execute as @e[type=minecraft:player,gamemode=!spectator] at @s as @e[type=#bm:p49_frames,distance=..6] if items entity @s contents {holds} '
               'if predicate bm:p256/hiss_chance at @s run function bm:p256/frame_hiss']
    G.wjson('bm/predicate/p256/hiss_chance.json', {'condition': 'minecraft:random_chance', 'chance': 0.06})
    G.wjson('bm/predicate/p256/coin.json', {'condition': 'minecraft:random_chance', 'chance': 0.5})
    fn('p256/owner_ok', ['scoreboard players operation #p bm.pay = @s bm.pid',
                         f'execute as @e[type=minecraft:player,tag=bm.haspcr,distance=..{LOST}] if score @s bm.pid = #p bm.pay run return 1', 'return 0'])
    fn('p256/mine', ['scoreboard players operation #p bm.pay = @s bm.pid',
                     f'execute as @e[type=minecraft:item_display,tag=bm.pcr,distance=..{LOST}] if score @s bm.pid = #p bm.pay run return 1', 'return 0'])
    fn('p256/vanish', [puff, 'kill @s'])
    fn('p256/spawn', [f'execute rotated ~ 0 positioned ^0.9 ^ ^-0.4 if block ~ ~ ~ #bm:grap_pass run return run function bm:p256/spawn_at',
                      'function bm:p256/spawn_at'])
    fn('p256/spawn_at', [f'summon minecraft:item_display ~ ~ ~ {snbt(disp)}',
                         'scoreboard players operation @e[type=minecraft:item_display,tag=bm.pcrnew,distance=..0.1] bm.pid = @s bm.pid',
                         'scoreboard players set @e[type=minecraft:item_display,tag=bm.pcrnew,distance=..0.1] bm.pcrs 0',
                         'scoreboard players set @e[type=minecraft:item_display,tag=bm.pcrnew,distance=..0.1] bm.pcrt 0',
                         'scoreboard players set @e[type=minecraft:item_display,tag=bm.pcrnew,distance=..0.1] bm.pcrw 10',
                         'execute as @e[type=minecraft:item_display,tag=bm.pcrnew,distance=..0.1] at @s facing entity @p[distance=..2] feet run tp @s ~ ~ ~ ~ 0',
                         'tag @e[type=minecraft:item_display,tag=bm.pcrnew,distance=..0.1] remove bm.pcrnew',
                         puff, 'playsound minecraft:block.note_block.bit neutral @a[distance=..12] ~ ~ ~ 0.4 2'])

    # ---------------------------------------------------------------- each tick: rest, hop, hiss
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.pcr] at @s run function bm:p256/tick')
    fn('p256/tick', ['scoreboard players add @s bm.pcrt 1',
                     'execute if score @s bm.pcrs matches 1 run return run function bm:p256/hop',
                     'execute if score @s bm.pcrs matches 2 run return run function bm:p256/hiss',
                     'execute if score @s bm.pcrt >= @s bm.pcrw run function bm:p256/decide'])
    # (resting, its wait over: where's its player?)
    fn('p256/me', ['tag @a remove bm.pcro', 'scoreboard players operation #p bm.pay = @s bm.pid',
                   f'execute as @e[type=minecraft:player,tag=bm.haspcr,distance=..{LOST}] if score @s bm.pid = #p bm.pay run tag @s add bm.pcro'])
    fn('p256/decide', ['function bm:p256/me', 'scoreboard players set @s bm.pcrt 0',
                       f'execute unless entity {ME} run return run scoreboard players set @s bm.pcrw 20',
                       f'execute if entity {me(str(FAR) + '..')} run return run function bm:p256/go_leap',
                       f'execute if entity {me(str(NEAR) + '..')} run return run function bm:p256/go_after',
                       f'execute if entity {me('..0.9')} run return run function bm:p256/go_away',
                       'execute store result score #r bm.rng run random value 1..9',
                       'execute if score #r bm.rng matches 1 run return run function bm:p256/go_hiss',
                       'execute if score #r bm.rng matches 2..5 run return run function bm:p256/go_about',
                       f'execute facing entity {ME} feet run tp @s ~ ~ ~ ~ 0',                         # (or just a look at you)
                       'execute store result score @s bm.pcrw run random value 15..45', 'tag @a remove bm.pcro'])
    start = ['scoreboard players set @s bm.pcrs 1', 'scoreboard players set @s bm.pcrt 0', 'tag @a remove bm.pcro']
    # (bm.pcrw while hopping: the hop's length, in tenths - 0 the leap to your side)
    fn('p256/go_after', [f'execute facing entity {ME} feet run tp @s ~ ~ ~ ~ 0', 'function bm:p256/jitter',
                         'scoreboard players set @s bm.pcrw 10'] + start)
    fn('p256/go_about', ['execute store result entity @s Rotation[0] float 1 run random value -180..179', 'scoreboard players set @s bm.pcrw 6'] + start)
    fn('p256/go_away', [f'execute facing entity {ME} feet rotated ~180 0 run tp @s ~ ~ ~ ~ 0', 'function bm:p256/jitter', 'scoreboard players set @s bm.pcrw 7'] + start)
    fn('p256/go_leap', [f'execute facing entity {ME} feet run tp @s ~ ~ ~ ~ 0', 'scoreboard players set @s bm.pcrw 0',
                        'scoreboard players set @s bm.pcrs 1', 'scoreboard players set @s bm.pcrt 0'])     # (its player stays tagged for the leap)
    fn('p256/jitter', ['execute store result score #y bm.rng run data get entity @s Rotation[0]',
                       'execute store result score #j bm.rng run random value -35..35', 'scoreboard players operation #y bm.rng += #j bm.rng',
                       'execute store result entity @s Rotation[0] float 1 run scoreboard players get #y bm.rng'])
    fn('p256/go_hiss', ['scoreboard players set @s bm.pcrs 2', f'execute facing entity {ME} feet run tp @s ~ ~ ~ ~ 0', 'tag @a remove bm.pcro'])
    # THE HOP: a squat, up (the display's translation rises while it travels - teleport_duration 6), down, the landing squash
    fn('p256/hop', ['execute if score @s bm.pcrt matches 1 run ' + frame('half'),
                    'execute if score @s bm.pcrt matches 2 run ' + frame('crouch'),
                    'execute if score @s bm.pcrt matches 4 run function bm:p256/jump',
                    'execute if score @s bm.pcrt matches 7 run ' + move(0),
                    'execute if score @s bm.pcrt matches 10 run ' + frame('crouch'),
                    'execute if score @s bm.pcrt matches 10 run playsound minecraft:entity.slime.squish_small neutral @a[distance=..10] ~ ~ ~ 0.25 1.8',
                    'execute if score @s bm.pcrt matches 11 run ' + frame('half'),
                    'execute if score @s bm.pcrt matches 12.. run function bm:p256/landed'])
    fn('p256/jump', [frame('stand'), move(HOP_H),
                     'execute if score @s bm.pcrw matches 0 run return run function bm:p256/leap',
                     'execute rotated ~ 0 if score @s bm.pcrw matches 6 positioned ^ ^ ^0.6 run return run function bm:p256/land',
                     'execute rotated ~ 0 if score @s bm.pcrw matches 7 positioned ^ ^ ^0.7 run return run function bm:p256/land',
                     'execute rotated ~ 0 positioned ^ ^ ^1.0 run function bm:p256/land'])
    # (the leap: to a spot a little short of its player, on their side - from their own height)
    fn('p256/leap', ['function bm:p256/me', f'execute at {ME} rotated as @s rotated ~ 0 positioned ^ ^ ^-1.1 run function bm:p256/land', 'tag @a remove bm.pcro'])
    # (where it comes down: up a step, or down a drop of up to three - never into a wall)
    fn('p256/land', ['execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p256/land_up',
                     'execute unless block ~ ~-1 ~ #bm:grap_pass run return run function bm:p256/land_at',
                     'execute unless block ~ ~-2 ~ #bm:grap_pass positioned ~ ~-1 ~ run return run function bm:p256/land_at',
                     'execute unless block ~ ~-3 ~ #bm:grap_pass positioned ~ ~-2 ~ run return run function bm:p256/land_at',
                     'execute unless block ~ ~-4 ~ #bm:grap_pass positioned ~ ~-3 ~ run function bm:p256/land_at'])
    fn('p256/land_up', ['execute positioned ~ ~1 ~ if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run function bm:p256/land_at'])
    fn('p256/land_at', ['execute align y run tp @s ~ ~ ~'])
    fn('p256/landed', [frame('stand'), 'scoreboard players set @s bm.pcrs 0', 'scoreboard players set @s bm.pcrt 0', 'function bm:p256/me',
                       f'execute facing entity {ME} feet run tp @s ~ ~ ~ ~ 0',
                       f'execute if entity {me(str(NEAR) + '..')} run scoreboard players set @s bm.pcrw 2',
                       f'execute unless entity {me(str(NEAR) + '..')} store result score @s bm.pcrw run random value 6..30', 'tag @a remove bm.pcro'])
    # HISSSS: white-hot, swelling, a hiss... and a puff of smoke. Nothing else.
    fn('p256/hiss', ['execute if score @s bm.pcrt matches 1 run playsound minecraft:entity.creeper.primed neutral @a[distance=..10] ~ ~ ~ 0.35 1.9',
                     'execute if score @s bm.pcrt matches 1 run ' + move(0, 14, 1.15)] +
       [f'execute if score @s bm.pcrt matches {t} run ' + frame('flash' if i % 2 == 0 else 'stand') for i, t in enumerate((2, 5, 8, 10, 12, 13, 14))] +
       ['execute if score @s bm.pcrt matches 15 run ' + frame('stand'),
        'execute if score @s bm.pcrt matches 15 run ' + move(0, 3),
        'execute if score @s bm.pcrt matches 15 run particle minecraft:smoke ~ ~0.45 ~ 0.12 0.1 0.12 0.01 8',
        'execute if score @s bm.pcrt matches 15 run particle minecraft:dust{color:[0.35,0.85,0.3],scale:0.6} ~ ~0.5 ~ 0.25 0.15 0.25 0 6',
        'execute if score @s bm.pcrt matches 15 run playsound minecraft:entity.creeper.hurt neutral @a[distance=..10] ~ ~ ~ 0.25 2',
        'execute if score @s bm.pcrt matches 22.. run function bm:p256/hissed'])
    fn('p256/hissed', ['scoreboard players set @s bm.pcrs 0', 'scoreboard players set @s bm.pcrt 0', 'execute store result score @s bm.pcrw run random value 20..50'])
    fn('p256/frame_hiss', ['playsound minecraft:entity.creeper.primed neutral @a[distance=..10] ~ ~ ~ 0.3 1.9',
                           'particle minecraft:smoke ^ ^ ^0.15 0.06 0.06 0.06 0.005 4'])

    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.pcr]', 'tag @a remove bm.haspcr', 'tag @a remove bm.pcro']
    return ITEMS[IID]

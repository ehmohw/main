"""2.67: THE VAULT FIGHTS A CROWD HARDER, AND KEEPS SECRETS - crew scaling, hidden vaults, hidden-only treasures.

CREW SCALING: the more of you in a heist, the tougher it is - every guard, captain and champion has +35% health per
  crewmate past the first (the guardian +50%) and hits 10% harder per crewmate; patrols and the guardian's calls bring
  extra guards for a crew. (The Counting House already sends more guards for more players, and a crew gets more tries.)
HIDDEN VAULTS: about one heist in three (more at the higher tiers - half of all Tier V heists), one room keeps a
  secret door in its far wall: a cracked stretch of wall with a cold draught. Right-click it and it crumbles, opening
  a passage to a HIDDEN VAULT - a little treasure room with a hoard (a share each, into your haul) and a few vault
  keepers. Now and then (Tier II and up) it's no vault at all but the parlour of THE GUTTER GENTRY (phase88).
HIDDEN TREASURES (only ever in a hidden vault's hoard): the RAT KING'S SIGNET (carry it: loose items come to you),
  WHISPERSTEP BOOTS (sneak: unseen, and quick on your feet) and the GILDED GRIN (a golden mask: you see in the dark).
"""
from items import item, T, TOTEM, ITEMS
from nbt import snbt, B, F, Int
from structures import Build
import phase70 as P70
import phase70_rooms as RM
import phase72 as P72
import phase75 as P75
import phase75_rooms as R5

GOLD = '#ffcf40'
HID = '#9ae8ff'
P75.FL_X = (-68, P75.FL_X[1])                       # (the hidden rooms stand west of the den: forceloaded and swept with the rest)
HV_X, HV_DY, HV_DZ = -62, -4, -12                     # a slot's hidden room: its corner (x; y from Y0; z from the slot's z)
HV_CHANCE = {1: 30, 2: 35, 3: 40, 4: 45, 5: 50}
LAIR_CHANCE = {1: 0, 2: 20, 3: 30, 4: 35, 5: 40}      # (of the hidden rooms: the Gentry's parlour instead of a vault)
HP_PCT, BOSS_PCT = 35, 50
HOSTS = ['levers', 'plates', 'tiles', 'dial', 'guards', 'coffers', 'lamps', 'lightsout', 'tumbler', 'ambush']

item('rat_signet', TOTEM, "Rat King's Signet", HID, ['A heavy gold ring with a rat\'s head seal.', ('Carry it: loose items within seven', 'blue'),
                                                     ('blocks come to you.', 'blue'), ('Found only in a hidden vault.', 'dark_purple')],
     model='bm:rat_signet', stack=1, cat='magic', glint=True)
item('whisperstep_boots', 'minecraft:leather_boots', 'Whisperstep Boots', HID, ['Soft soles, and not a sound.', ('Sneaking: unseen, and quick on', 'blue'),
                                                                              ('your feet.', 'blue'), ('Found only in a hidden vault.', 'dark_purple')],
     comps={'minecraft:dyed_color': 0x2a2a3a, 'minecraft:attribute_modifiers': [
         {'type': 'minecraft:armor', 'id': 'bm:whisper', 'amount': 3.0, 'operation': 'add_value', 'slot': 'feet'},
         {'type': 'minecraft:safe_fall_distance', 'id': 'bm:whisper_f', 'amount': 4.0, 'operation': 'add_value', 'slot': 'feet'}]}, cat='armor')
item('gilded_grin', TOTEM, 'The Gilded Grin', GOLD, ['A golden mask with a wide, wide smile.', ('Worn: you see in the dark.', 'blue'),
                                                    ('Found only in a hidden vault.', 'dark_purple')],
     model='bm:gilded_grin', stack=1, cat='cosmetic', comps={'minecraft:equippable': {'slot': 'head'}})
HIDDEN = ['rat_signet', 'whisperstep_boots', 'gilded_grin']
P72.KEEP += HIDDEN


# ===================================================================== the hidden rooms
def _seal(b):
    """a closed room: both doorways walled up"""
    for y in range(4, 8):
        for z in (11, 12, 13):
            b.set(0, y, z, RM.WALL); b.set(RM.W - 1, y, z, RM.WALL)
    return b


def hvault():
    b = _seal(RM.shell())
    raw, metal = R5.BASE['raw'], R5.BASE['metal']
    for (cx, cz) in ((4, 4), (20, 4), (4, 20), (20, 20)):                     # heaps of gold in the corners
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                b.set(cx + dx, 4, cz + dz, raw)
        b.set(cx, 5, cz, metal); b.set(cx, 6, cz, 'minecraft:gold_block' if (cx + cz) % 8 else raw)
    for (x, z, f) in ((8, 2, 'south'), (16, 2, 'south'), (8, 22, 'north'), (16, 22, 'north')):
        b.set(x, 4, z, f'minecraft:chest[facing={f}]')
    for x in range(10, 15):                                                 # the hoard's dais
        for z in range(10, 15):
            b.set(x, FY_, z, metal)
    b.set(12, 4, 12, 'minecraft:chiseled_quartz_block'); b.set(12, 5, 12, 'minecraft:gold_block')
    b.set(2, 4, 12, 'minecraft:heavy_weighted_pressure_plate'); b.set(2, 3, 12, 'minecraft:emerald_block')
    b.marker(*RM.CTRL, ['bm.gvhvr', 'bm.gvhvr_vault', 'bm.gvhvn'])
    return R5.wall_glow(b)


def gentry():
    b = _seal(RM.shell())
    for x in range(3, 22):                                                  # a parlour: a long red carpet, a dining table, a chandelier
        for z in (11, 12, 13):
            b.set(x, 4, z, 'minecraft:red_carpet')
    for x in range(6, 19):
        b.set(x, 4, 20, 'minecraft:dark_oak_planks'); b.set(x, 5, 20, 'minecraft:dark_oak_slab')
        if x % 3 == 0: b.set(x, 6, 20, 'minecraft:white_candle[candles=3,lit=true]')
    for x in range(6, 19, 3):
        b.set(x, 4, 21, 'minecraft:dark_oak_stairs[facing=north]'); b.set(x, 4, 19, 'minecraft:dark_oak_stairs[facing=south]')
    for y in range(10, 15): b.set(12, y, 12, 'minecraft:iron_chain')
    for (dx, dz) in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)):
        b.set(12 + dx, 9, 12 + dz, 'minecraft:lantern[hanging=true]' if (dx, dz) != (0, 0) else 'minecraft:soul_lantern[hanging=true]')
    for (x, z) in ((3, 3), (21, 3), (3, 21), (21, 21), (12, 2)):           # the roost: cobwebs in the corners
        b.set(x, 13, z, 'minecraft:cobweb')
    for (x, z) in ((6, 5), (7, 6), (18, 6), (17, 17), (6, 17)):            # black ooze on the floor
        b.set(x, 3, z, 'minecraft:black_concrete')
    b.set(20, 4, 4, 'minecraft:oak_fence'); b.set(20, 5, 4, 'minecraft:black_carpet')   # (a hat stand)
    b.set(2, 4, 12, 'minecraft:heavy_weighted_pressure_plate'); b.set(2, 3, 12, 'minecraft:emerald_block')
    b.marker(*RM.CTRL, ['bm.gvhvr', 'bm.gvhvr_lair', 'bm.gvhvn'])
    return R5.wall_glow(b)


FY_ = RM.FY


def door_x():
    """{room kind: the x of a safe secret door on its far (z 24) wall} - a cell of wall with open floor in front of it"""
    rooms = R5.tiered_rooms(P75.EXTRA_ROOMS)
    out = {}
    for k in HOSTS:
        if f'{k}_t3' not in rooms: continue
        b = rooms[f'{k}_t3']()
        air = lambda x, y, z: (b.get(x, y, z) or 'minecraft:air') in ('minecraft:air', 'minecraft:cave_air')
        for x in (12, 20, 4, 16, 8, 18, 6):
            if all(not air(x, y, 24) for y in (4, 5)) and all(air(x, y, z) for y in (4, 5) for z in (22, 23)) and not air(x, 3, 23) and not air(x, 3, 22):
                out[k] = x; break
    return out


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    rel = RM.rel
    ident = [F(0), F(0), F(0), F(1)]
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    tick, fast, second = [], [], []
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gvhvc dummy', f'scoreboard players set #k{HP_PCT} bm.rng {HP_PCT}',
                              f'scoreboard players set #k{BOSS_PCT} bm.rng {BOSS_PCT}', 'scoreboard players set #k100 bm.rng 100']
    G.OBJECTIVES += ['bm.gvhvc']

    # ================================================================== CREW SCALING
    fn('p87/crew', ['scoreboard players set #crew bm.rng 1'] +
       [f'execute if score #gi bm.rng matches {s + 1} run scoreboard players operation #crew bm.rng = #np{s} bm.gvx' for s in range(P70.SLOTS)] +
       ['execute if score #crew bm.rng matches ..0 run scoreboard players set #crew bm.rng 1', 'execute if score #crew bm.rng matches 7.. run scoreboard players set #crew bm.rng 6'])
    fn('p87/hpscale', ['function bm:p87/crew', 'scoreboard players operation #hf bm.rng = #crew bm.rng', 'scoreboard players remove #hf bm.rng 1',
                       f'execute unless entity @s[tag=bm.gvboss] run scoreboard players operation #hf bm.rng *= #k{HP_PCT} bm.rng',
                       f'execute if entity @s[tag=bm.gvboss] run scoreboard players operation #hf bm.rng *= #k{BOSS_PCT} bm.rng',
                       'scoreboard players add #hf bm.rng 100', 'scoreboard players operation #h bm.rng *= #hf bm.rng', 'scoreboard players operation #h bm.rng /= #k100 bm.rng'])
    HPLINE = 'execute store result storage bm:gv h double 1 run scoreboard players get #h bm.rng'
    n_hp = 0
    for name, lines in G.FUNCS.items():
        if HPLINE in lines and (name.startswith(('p70/', 'p75/', 'p76/', 'p77/'))):
            k = lines.index(HPLINE); lines.insert(k, 'function bm:p87/hpscale'); n_hp += 1
    assert n_hp >= 2, n_hp
    G.FUNCS['p70/guard_set1'] += ['function bm:p87/crew'] + \
        [f'execute if score #crew bm.rng matches {n} run attribute @s minecraft:attack_damage modifier add bm:gv_crew {0.1 * (n - 1):.1f} add_multiplied_base' for n in range(2, 7)]
    fn('p87/guardx', ['function bm:p70/guard', 'function bm:p87/crew', 'scoreboard players remove #crew bm.rng 1', 'scoreboard players operation #crew bm.rng *= #k35 bm.rng',
                      'execute store result score #r bm.rng run random value 1..100', 'execute if score #r bm.rng <= #crew bm.rng run function bm:p70/guard'])
    for f_ in ('p70/patrol', 'p70/boss/call'):
        G.FUNCS[f_] = [l.replace('run function bm:p70/guard', 'run function bm:p87/guardx') if l.endswith('run function bm:p70/guard') else l for l in G.FUNCS[f_]]

    # ================================================================== HIDDEN VAULTS
    for k, f in (('hvault', hvault), ('gentry', gentry)):
        for t in R5.TIERS:
            R5.retheme(f(), t).export(G.path('data', 'bm', 'structure', f'gv_{k}_t{t}.nbt'))
    DX = door_x()
    assert len(DX) >= 6, DX
    for s in range(P70.SLOTS):
        z0 = P70.zoff(s)
        hx, hy, hz = HV_X, P70.Y0 + HV_DY, z0 + HV_DZ
        b = G.FUNCS[f'p70/s{s}/build']
        k = next(i for i, l in enumerate(b) if 'run function bm:p70/r/init' in l)
        b.insert(k, f'function bm:p87/hv/roll{s}')
        fn(f'p87/hv/roll{s}', [f'execute unless score #md{s} bm.gvmd matches 0 run return 0', 'execute store result score #r bm.rng run random value 1..100'] +
           [f'execute if score #gt bm.rng matches {t} if score #r bm.rng matches {c + 1}.. run return 0' for t, c in HV_CHANCE.items()] +
           [f'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr,tag=bm.gvr_{kk},scores={{bm.gvi={s + 1}}}] run tag @s add bm.gvhvok' for kk in DX] +
           ['execute store result score #r bm.rng run random value 1..100', 'scoreboard players set #lair bm.rng 0'] +
           [f'execute if score #gt bm.rng matches {t} if score #r bm.rng matches ..{c} run scoreboard players set #lair bm.rng 1' for t, c in LAIR_CHANCE.items() if c] +
           ['execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvhvok,sort=random,limit=1] at @s run function bm:p87/hv/host',
            'execute in bm:gutter run tag @e[type=minecraft:marker,tag=bm.gvhvok] remove bm.gvhvok',
            f'execute if score #hvok bm.rng matches 1 in bm:gutter positioned {hx} {hy} {hz} run function bm:p87/hv/place'])
    fn('p87/hv/host', ['scoreboard players set #hvok bm.rng 1', 'tag @s add bm.gvhvh'] +
       [f'execute if entity @s[tag=bm.gvr_{kk}] run return run function bm:p87/hv/door{x}' for kk, x in DX.items()])
    for x in sorted(set(DX.values())):
        fn(f'p87/hv/door{x}', [f'fill {rel(x - 2, 3, 25)} {rel(x + 2, 8, 29)} {RM.WALL}', f'fill {rel(x - 1, 4, 25)} {rel(x + 1, 6, 28)} minecraft:air',
                               f'setblock {rel(x, 3, 27)} minecraft:crying_obsidian',
                               f'execute if score #gt bm.rng matches 1 run fill {rel(x, 4, 24)} {rel(x, 5, 24)} minecraft:cracked_stone_bricks',
                               f'execute if score #gt bm.rng matches 2..3 run fill {rel(x, 4, 24)} {rel(x, 5, 24)} minecraft:cracked_polished_blackstone_bricks',
                               f'execute if score #gt bm.rng matches 4.. run fill {rel(x, 4, 24)} {rel(x, 5, 24)} minecraft:cracked_deepslate_bricks',
                               f'summon minecraft:interaction {rel(x, 4, 24)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvhvi', 'bm.gvhvn2'], 'width': F(1.04), 'height': F(2.04), 'response': B(1)}),
                               f'summon minecraft:marker {rel(x, 4, 27)} {{Tags:["bm.gvprop","bm.gvhvd","bm.gvhvn2"]}}',
                               'scoreboard players operation @e[tag=bm.gvhvn2,distance=..20] bm.gvi = #gi bm.rng', 'tag @e[tag=bm.gvhvn2,distance=..20] remove bm.gvhvn2'])
    # (the hidden room itself: placed at the slot's spot west of the den, with a sweep-up marker like every other piece)
    fn('p87/hv/place', [f'execute if score #lair bm.rng matches 0 if score #gt bm.rng matches {t} run place template bm:gv_hvault_t{t} ~ ~ ~' for t in R5.TIERS] +
       [f'execute if score #lair bm.rng matches 1 if score #gt bm.rng matches {t} run place template bm:gv_gentry_t{t} ~ ~ ~' for t in R5.TIERS] +
       ['summon minecraft:marker ~ ~ ~ {Tags:["bm.gvpc","bm.gvpc_25x16x25","bm.gvpcn"]}',
        'scoreboard players operation @e[type=minecraft:marker,tag=bm.gvpcn,distance=..1] bm.gvi = #gi bm.rng', 'tag @e[type=minecraft:marker,tag=bm.gvpcn,distance=..1] remove bm.gvpcn',
        'execute as @e[type=minecraft:marker,tag=bm.gvhvn,distance=..40] at @s run function bm:p87/hv/claim'])
    fn('p87/hv/claim', ['tag @s remove bm.gvhvn', 'scoreboard players operation @s bm.gvi = #gi bm.rng', 'scoreboard players operation @s bm.gvt = #gt bm.rng',
                        'execute at @s run summon minecraft:interaction ~ ~1.02 ~ ' + snbt({'Tags': ['bm.gvprop', 'bm.gvhvp', 'bm.gvhvn3'], 'width': F(1.1), 'height': F(1.1), 'response': B(1)}),
                        'execute at @s run summon minecraft:text_display ~ ~2.9 ~ ' + snbt({'Tags': ['bm.gvprop', 'bm.gvhvt', 'bm.gvhvn3'], 'billboard': 'vertical', 'background': Int(0x70000000),
                                                                                         'brightness': {'block': 15, 'sky': 15}, 'text': '',
                                                                                         'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                                            'translation': [F(0)] * 3, 'scale': [F(0.6)] * 3}}),
                        'execute at @s run scoreboard players operation @e[tag=bm.gvhvn3,distance=..4] bm.gvi = #gi bm.rng', 'execute at @s run tag @e[tag=bm.gvhvn3,distance=..4] remove bm.gvhvn3',
                        'execute if entity @s[tag=bm.gvhvr_vault] at @s run data modify entity @e[type=minecraft:text_display,tag=bm.gvhvt,distance=..4,limit=1] text set value '
                        + snbt([T('THE HIDDEN HOARD\n', HID, bold=True), T('right-click: your share', 'gray')]),
                        'execute if entity @s[tag=bm.gvhvr_lair] at @s run data modify entity @e[type=minecraft:text_display,tag=bm.gvhvt,distance=..4,limit=1] text set value '
                        + snbt([T('THE GENTRY\'S HOARD\n', '#c8a0ff', bold=True), T('(theirs - for now)', 'gray')]),
                        'execute if entity @s[tag=bm.gvhvr_lair] run tag @s add bm.gvhvlock'])
    # ---- the secret door: a draught gives it away; right-click and it crumbles
    second.append('execute as @e[type=minecraft:interaction,tag=bm.gvhvi] at @s if entity @a[tag=bm.gvp,distance=..5] run particle minecraft:white_ash ~ ~1 ~ 0.3 0.6 0.3 0 6')
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.gvhvi] if data entity @s interaction at @s run function bm:p87/hv/open')
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.gvhvi] if data entity @s attack at @s run function bm:p87/hv/open')
    fn('p87/hv/open', ['fill ~ ~ ~ ~ ~1 ~ minecraft:air destroy', 'scoreboard players operation #gi bm.rng = @s bm.gvi',
                       'execute as @e[type=minecraft:marker,tag=bm.gvhvd,distance=..5] run tag @s add bm.gvhvopen',
                       'particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.4 60', 'playsound minecraft:block.grindstone.use block @a[distance=..24] ~ ~ ~ 1 0.5',
                       'playsound minecraft:ambient.cave block @a[distance=..24] ~ ~ ~ 1 1.2',
                       'execute as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' +
                       tellraw('@s', P + [T('A hidden passage! ', HID, bold=True), T('Something old and secret lies beyond the wall.', 'gray')]), 'kill @s'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.gvhvd,tag=bm.gvhvopen] at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.6 0.8 0.3 0.05 20')
    fast.append('execute as @e[type=minecraft:marker,tag=bm.gvhvd,tag=bm.gvhvopen] at @s as @a[tag=bm.gvp,distance=..1.3] at @s run function bm:p87/hv/enter')
    fn('p87/hv/enter', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'tag @s add bm.gvhvgo',
                        f'execute as @e[type=minecraft:marker,tag=bm.gvhvr] if score @s bm.gvi = #gi bm.rng at @s run tp @a[tag=bm.gvhvgo,limit=1] {rel(4, 4, 12)} -90 0',
                        'tag @s remove bm.gvhvgo', 'execute at @s run playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.25 1.6'])
    fast.append(f'execute as @e[type=minecraft:marker,tag=bm.gvhvr] at @s positioned {rel(2, 4, 12)} as @a[tag=bm.gvp,distance=..0.8] at @s run function bm:p87/hv/leave')
    fn('p87/hv/leave', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'tag @s add bm.gvhvgo',
                        'execute as @e[type=minecraft:marker,tag=bm.gvhvd] if score @s bm.gvi = #gi bm.rng at @s run tp @a[tag=bm.gvhvgo,limit=1] ~ ~ ~-4.5 180 0',
                        'tag @s remove bm.gvhvgo'])
    # ---- inside: keepers on the first visit (or the Gentry), and the hoard
    second.append('execute as @e[type=minecraft:marker,tag=bm.gvhvr,tag=!bm.gvhvseen] at @s if entity @a[tag=bm.gvp,distance=..14] run function bm:p87/hv/first')
    fn('p87/hv/first', ['tag @s add bm.gvhvseen', 'scoreboard players operation #gi bm.rng = @s bm.gvi', 'function bm:p70/ctx',
                        'execute if entity @s[tag=bm.gvhvr_lair] run return run function bm:p88/lair/start',
                        'title @a[tag=bm.gvp,distance=..20] times 5 40 10', title('@a[tag=bm.gvp,distance=..20]', 'title', T('A HIDDEN VAULT', HID, bold=True)),
                        title('@a[tag=bm.gvp,distance=..20]', 'subtitle', T('...and its keepers', 'gray'))] +
       [f'execute positioned {rel(x, 4, z)} run function bm:p87/guardx' for (x, z) in ((19, 8), (19, 16), (7, 12))])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.gvhvp] if data entity @s interaction at @s run function bm:p87/hv/hoard')
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.gvhvp] if data entity @s attack run data remove entity @s attack')
    fn('p87/hv/hoard', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #lk bm.rng 0',
                        'execute as @e[type=minecraft:marker,tag=bm.gvhvr,tag=bm.gvhvlock,distance=..3] run scoreboard players set #lk bm.rng 1',
                        'scoreboard players set #lr bm.rng 0', 'execute as @e[type=minecraft:marker,tag=bm.gvhvr,tag=bm.gvhvr_lair,distance=..3] run scoreboard players set #lr bm.rng 1',
                        'execute on target run function bm:p87/hv/share', 'data remove entity @s interaction'])
    fn('p87/hv/share', ['execute if score #lk bm.rng matches 1 run return run ' + title('@s', 'actionbar', T('The Gentry won\'t share - not while they stand.', 'red')),
                        'execute if score @s bm.gvhvc = @s bm.gvrun run return run ' + title('@s', 'actionbar', T('You\'ve had your share of this hoard.', 'gray')),
                        'scoreboard players operation @s bm.gvhvc = @s bm.gvrun', 'function bm:p70/ctx_p'] +
       [f'execute if score #lr bm.rng matches 0 if score #gt bm.rng matches {t} run function bm:p81/defer {{t:"bm:p87/hoard_t{t}"}}' for t in R5.TIERS] +
       [f'execute if score #lr bm.rng matches 1 if score #gt bm.rng matches {t} run function bm:p81/defer {{t:"bm:p88/hoard_t{t}"}}' for t in R5.TIERS] +
       [tellraw('@s', P + [T('Your share of the hidden hoard goes into your haul.', HID)]), 'playsound minecraft:block.chest.open player @s ~ ~ ~ 1 0.8',
        'particle minecraft:wax_on ~ ~1 ~ 0.4 0.4 0.4 0 20'])
    def ent(i, w, c=None):
        if i in ITEMS: return dict(G.loot_entry(i, G.uni(*c) if c else None), weight=w)
        e = {'type': 'minecraft:item', 'name': 'minecraft:' + i, 'weight': w}
        if c: e['functions'] = [{'function': 'minecraft:set_count', 'count': G.uni(*c)}]
        return e
    goods = {1: [ent('gold_ingot', 10, (4, 8)), ent('emerald', 8, (3, 6)), ent('diamond', 3, (1, 1))],
             2: [ent('gold_block', 8, (1, 2)), ent('diamond', 6, (1, 2)), ent('emerald', 6, (4, 8))],
             3: [ent('diamond', 10, (2, 3)), ent('gold_block', 6, (2, 3)), ent('emerald_block', 3, (1, 1))],
             4: [ent('diamond', 10, (3, 4)), ent('emerald_block', 5, (1, 2)), ent('netherite_scrap', 1, (1, 1))],
             5: [ent('diamond_block', 4, (1, 1)), ent('diamond', 10, (3, 5)), ent('netherite_scrap', 3, (1, 1)), ent('ancient_debris', 2, (1, 1))]}
    for t in R5.TIERS:
        wjson(f'bm/loot_table/p87/hoard_t{t}.json', {'pools': [
            {'rolls': 1, 'entries': [ent(i, 1) for i in HIDDEN], 'conditions': [G.chance(0.35 + 0.05 * t)]},
            {'rolls': 2, 'entries': goods[t]}, {'rolls': 1, 'entries': [ent('gutter_coin', 1, (3, 4 + 2 * t))]}]})
    fn('admin/hidden_items', [G.give(i) for i in HIDDEN])
    # (testing: a hidden vault - or the Gentry's parlour - in the heist you're in, now)
    force = ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'function bm:p70/ctx', 'scoreboard players set #hvok bm.rng 0',
             'execute in bm:gutter as @e[tag=bm.gvprop] if score @s bm.gvi = #gi bm.rng if entity @s[tag=bm.gvhvi] run kill @s',
             'execute in bm:gutter as @e[tag=bm.gvprop] if score @s bm.gvi = #gi bm.rng if entity @s[tag=bm.gvhvd] run kill @s',
             'execute in bm:gutter as @e[tag=bm.gvprop] if score @s bm.gvi = #gi bm.rng if entity @s[tag=bm.gvhvp] run kill @s',
             'execute in bm:gutter as @e[tag=bm.gvprop] if score @s bm.gvi = #gi bm.rng if entity @s[tag=bm.gvhvt] run kill @s',
             'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvhvr] if score @s bm.gvi = #gi bm.rng run kill @s',
             'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvhvh] if score @s bm.gvi = #gi bm.rng run tag @s remove bm.gvhvh'] + \
        [f'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr,tag=bm.gvr_{kk},tag=!bm.gvhvh] if score @s bm.gvi = #gi bm.rng run tag @s add bm.gvhvok' for kk in DX] + \
        ['execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvhvok,sort=random,limit=1] at @s run function bm:p87/hv/host',
         'execute in bm:gutter run tag @e[type=minecraft:marker,tag=bm.gvhvok] remove bm.gvhvok',
         'execute if score #hvok bm.rng matches 0 run return run ' + tellraw('@s', P + [T('No room here takes a secret door (or you\'re not in a heist).', 'red')])] + \
        [f'execute if score #gi bm.rng matches {s + 1} in bm:gutter positioned {HV_X} {P70.Y0 + HV_DY} {P70.zoff(s) + HV_DZ} run function bm:p87/hv/place' for s in range(P70.SLOTS)] + \
        [tellraw('@s', P + [T('A secret door waits in one of the rooms.', HID)])]
    fn('p87/hv/force', force)
    fn('admin/hidden_vault', ['scoreboard players set #lair bm.rng 0', 'function bm:p87/hv/force'])
    fn('admin/hidden_lair', ['scoreboard players set #lair bm.rng 1', 'function bm:p87/hv/force'])

    # ================================================================== THE HIDDEN TREASURES AT WORK
    sig = '*[minecraft:custom_data~{bm:"rat_signet"}]'
    second += [f'execute as @a if items entity @s container.* {sig} at @s as @e[type=minecraft:item,tag=!bm.gvscoin,distance=1.5..7] '
               f'unless items entity @s contents *[minecraft:custom_data~{{bm:"paperweight"}}] run tp @s ~ ~0.3 ~',
               f'execute as @a if items entity @s weapon.offhand {sig} at @s as @e[type=minecraft:item,tag=!bm.gvscoin,distance=1.5..7] '
               f'unless items entity @s contents *[minecraft:custom_data~{{bm:"paperweight"}}] run tp @s ~ ~0.3 ~']
    fast.append('execute as @a if items entity @s armor.feet *[minecraft:custom_data~{bm:"whisperstep_boots"}] if predicate bm:p20/sneaking run function bm:p87/whisper')
    fn('p87/whisper', ['effect give @s minecraft:invisibility 1 0 true', 'effect give @s minecraft:speed 1 1 true'])
    second.append('execute as @a if items entity @s armor.head *[minecraft:custom_data~{bm:"gilded_grin"}] run effect give @s minecraft:night_vision 15 0 true')

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']; f[-1:-1] = fast
    s = G.FUNCS['loop/second']; s[-1:-1] = second


def rp(R):
    g = R.grid
    R.ICONS['rat_signet'] = g(['................', '................', '.....oooooo.....', '....oYYYYYYo....', '...oYkkyykkYo...', '...oYkwyywkYo...', '...oYykkkkyYo...',
                               '...oYyykpkyYo...', '....oYyyyyYo....', '.....oYYYYo.....', '....oo....oo....', '...oY......Yo...', '...oY......Yo...', '....oo....oo....',
                               '.....oooooo.....', '................'], dict(o='#6a4a10', Y='#f0c040', y='#c89a28', k='#4a3010', w='#ffffff', p='#ff9ab0'))
    R.ICONS['gilded_grin'] = g(['................', '....oooooooo....', '...oYYYYYYYYo...', '..oYYYYYYYYYYo..', '..oYkkYYYYkkYo..', '..oYkkYYYYkkYo..', '..oYYYYYYYYYYo..',
                                '..oYYYYyyYYYYo..', '..oYkYYYYYYkYo..', '..oYkkkkkkkkYo..', '...oYkwkwkwYo...', '...oYYkkkkYYo...', '....oYYYYYYo....', '.....oooooo.....',
                                '................', '................'], dict(o='#6a4a10', Y='#ffd04a', y='#d8a830', k='#2a1a08', w='#fff8e0'))
    # (worn: a golden face plate in front of the face)
    R.HATS['gilded_grin_worn'] = ({'g': 'minecraft:block/gold_block', 'k': 'minecraft:block/black_concrete'}, [
        {'from': [3, 3, -0.2], 'to': [13, 13, 0.8], 'faces': {f: {'texture': '#g', 'uv': [0, 0, 16, 16]} for f in ('north', 'south', 'east', 'west', 'up', 'down')}},
        {'from': [4.5, 8.5, -0.5], 'to': [6.5, 10, -0.15], 'faces': {f: {'texture': '#k', 'uv': [0, 0, 2, 2]} for f in ('north', 'south', 'east', 'west', 'up', 'down')}},
        {'from': [9.5, 8.5, -0.5], 'to': [11.5, 10, -0.15], 'faces': {f: {'texture': '#k', 'uv': [0, 0, 2, 2]} for f in ('north', 'south', 'east', 'west', 'up', 'down')}},
        {'from': [4.5, 4.5, -0.5], 'to': [11.5, 5.8, -0.15], 'faces': {f: {'texture': '#k', 'uv': [0, 0, 2, 2]} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}])

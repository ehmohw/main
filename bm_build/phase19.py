"""Phase 1.9: Blood Moon surge (extra night spawns around players, including Nether mobs in the overworld),
Sir Croaksworth the mustachioed frog (a 3D figure on a lily pad in the market's pond, no UI yet), and the market's
rats/frog turning to watch nearby players (yaw only, so their feet stay on the floor).
Importing does nothing; generate(G) runs after phase18.generate."""
from nbt import snbt, B, F, Int

# (weight, type, extra NBT). Every type is checked against vanilla-mcdoc 26.x in check262_nbt.py.
# Piglins/hoglins would zombify after 15 s in the overworld, hence IsImmuneToZombification.
# Summons with NBT skip vanilla's spawn equipment, so the armed ones get their weapon here.
NETHER = [
    (22, 'blaze', {}),
    (22, 'wither_skeleton', {'equipment': {'mainhand': {'id': 'minecraft:stone_sword', 'count': Int(1)}}, 'drop_chances': {'mainhand': F(0)}}),
    (16, 'magma_cube', {'Size': Int(1)}),
    (12, 'piglin_brute', {'IsImmuneToZombification': B(1), 'equipment': {'mainhand': {'id': 'minecraft:golden_axe', 'count': Int(1)}},
                          'drop_chances': {'mainhand': F(0)}}),
    (8, 'hoglin', {'IsImmuneToZombification': B(1)}),
]
OVERWORLD = [
    (8, 'zombie', {}),
    (7, 'skeleton', {'equipment': {'mainhand': {'id': 'minecraft:bow', 'count': Int(1)}}, 'drop_chances': {'mainhand': F(0)}}),
    (5, 'spider', {}),
]
SURGE_CAP = 6          # surge mobs allowed within 64 blocks of a player
FROG_MODEL = 'bm:frog3d'


def generate(G):
    fn = G.fn
    second, fast = [], []

    # ---------------- Blood Moon surge: each second, each outdoor overworld player has a 1-in-3 chance of something
    # crawling out of the ground 14-30 blocks away (capped). They still go through the normal tier roll, so with the
    # raised Blood Moon odds about two in three come out Elite, Champion or a horror.
    fn('p19/surge_roll', ['execute store result score #r bm.rng run random value 1..3',
                          'execute if score #r bm.rng matches 1 run function bm:p19/surge'])
    fn('p19/surge', [
        f'execute store result score #n bm.rng if entity @e[tag=bm.surge_mob,distance=..64]',
        f'execute if score #n bm.rng matches {SURGE_CAP}.. run return 0',
        'kill @e[type=minecraft:marker,tag=bm.sg]',
        'summon minecraft:marker ~ ~ ~ {Tags:["bm.sg"]}',
        'execute as @e[type=minecraft:marker,tag=bm.sg,limit=1] run spreadplayers ~ ~ 0 30 false @s',
        'execute as @e[type=minecraft:marker,tag=bm.sg,limit=1] at @s run function bm:p19/surge_at',
        'kill @e[type=minecraft:marker,tag=bm.sg]'])
    total = sum(w for w, _, _ in NETHER + OVERWORLD)
    lines = [
        'execute if entity @a[distance=..14] run return 0',                     # never right on top of anyone
        'execute unless entity @a[distance=..40] run return 0',                 # player is in a cave far below / far off
        'execute if block ~ ~-1 ~ #bm:surge_bad run return 0',
        'execute unless block ~ ~ ~ #minecraft:air run return 0',
        'execute unless block ~ ~1 ~ #minecraft:air run return 0',
        'execute if entity @e[type=minecraft:marker,tag=bm.zone_m,distance=..48] run return 0',
        f'execute store result score #r bm.rng run random value 1..{total}']
    lo = 1
    for w, t, extra in NETHER + OVERWORLD:
        hi = lo + w - 1
        nether = (w, t, extra) in NETHER
        tags = ['bm.surge_mob'] + (['bm.surge_nether'] if nether else [])
        nbt = dict(extra, Tags=tags)
        fx = 'p19/rift_nether' if nether else 'p19/rift'
        lines.append(f'execute if score #r bm.rng matches {lo}..{hi} run function bm:{fx}')
        lines.append(f'execute if score #r bm.rng matches {lo}..{hi} run return run summon minecraft:{t} ~ ~ ~ {snbt(nbt)}')
        lo = hi + 1
    fn('p19/surge_at', lines)
    fn('p19/rift_nether', ['particle minecraft:soul_fire_flame ~ ~0.2 ~ 0.4 0.1 0.4 0.03 25',
                           'particle minecraft:large_smoke ~ ~0.8 ~ 0.3 0.6 0.3 0.02 12',
                           'particle minecraft:crimson_spore ~ ~1 ~ 0.6 0.8 0.6 0 30',
                           'playsound minecraft:block.portal.trigger hostile @a[distance=..32] ~ ~ ~ 0.35 1.7'])
    fn('p19/rift', ['particle minecraft:dust{color:[0.55,0.0,0.0],scale:1.6} ~ ~0.5 ~ 0.4 0.4 0.4 0 25',
                    'playsound minecraft:block.rooted_dirt.break hostile @a[distance=..24] ~ ~ ~ 0.8 0.6'])
    G.wjson('bm/tags/block/surge_bad.json', {'values': ['minecraft:water', 'minecraft:lava', 'minecraft:magma_block', 'minecraft:fire',
                                                       'minecraft:soul_fire', 'minecraft:powder_snow', '#minecraft:leaves']})
    G.FUNCS['bloodmoon/during'].append(
        'execute as @a[gamemode=!spectator] at @s if dimension minecraft:overworld if predicate bm:sees_sky run function bm:p19/surge_roll')
    # at dawn the Nether's guests are dragged home
    fn('p19/dawn_one', ['particle minecraft:soul_fire_flame ~ ~0.5 ~ 0.3 0.6 0.3 0.04 20', 'particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 10',
                        'tp @s ~ -400 ~'])
    G.FUNCS['bloodmoon/end'].insert(2, 'execute as @e[tag=bm.surge_nether] at @s run function bm:p19/dawn_one')

    # (1.10: Sir Croaksworth moved out of the market to his own swamp hut - see phase20)

    # ---------------- rats and the frog turn (yaw only) to watch the nearest player, and glance around when alone
    fn('p19/look', ['execute if entity @a[distance=..10,gamemode=!spectator] facing entity @p[distance=..10,gamemode=!spectator] feet run return run tp @s ~ ~ ~ ~ 0',
                    'execute store result score #r bm.rng run random value 1..48',
                    'execute if score #r bm.rng matches 1 run tp @s ~ ~ ~ ~40 0',
                    'execute if score #r bm.rng matches 2 run tp @s ~ ~ ~ ~-40 0'])
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.rat_sprite] at @s if entity @a[distance=..32] run function bm:p19/look')
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.frog_hut] at @s if entity @a[distance=..32] run function bm:p19/look')
    # existing rats get smooth turning
    second.append('execute as @e[type=minecraft:item_display,tag=bm.rat_sprite,tag=!bm.td] run data modify entity @s teleport_duration set value 6')
    second.append('tag @e[type=minecraft:item_display,tag=bm.rat_sprite,tag=!bm.td] add bm.td')

    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

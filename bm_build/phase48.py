"""Phase 2.27: the Vorn Skiff's tractor beam.

Aboard the skiff, LOOK UP and right-click the key to switch the beam on or off. A column of light (2.5 blocks round, 20 deep)
reaches down from the saucer:
- creatures and other players in it are lifted up to just under the hull and held there (bobbing) until you switch it off or
  fly away - then they drop. Nothing with more than 100 max health (bosses), no NPCs, no one in creative or spectator;
- dropped items and XP rise into the saucer and land in your pack.
(2.44: it needs no power - no Violet Xenite is drawn; the skiff runs it for free.) The laser, the TNT bomb and
sneak-to-land work as before."""
from items import T

BEAM_DEPTH = 20
MAX_HP = 100
GREEN = '#7dff6a'


def generate(G):
    fn, wjson, title = G.fn, G.wjson, G.title
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, second = [], []
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.skbt dummy']
    G.OBJECTIVES += ['bm.skbt']
    from phase44 import NONMOB
    nolift = [e for e in NONMOB if e != 'player'] + ['ender_dragon', 'wither', 'warden', 'elder_guardian', 'giant', 'happy_ghast']
    wjson('bm/tags/entity_type/p48_nolift.json', {'values': [{'id': f'minecraft:{e}', 'required': False} for e in nolift]})

    # the key: look up + right-click (aboard) toggles the beam; the laser and the bomb keep their angles
    use = G.FUNCS['p35/skiff/use']
    use.insert(0, 'execute if function bm:p35/skiff/riding if entity @s[x_rotation=-90..-50] run return run function bm:p48/toggle')
    fn('p48/toggle', ['execute if entity @s[tag=bm.skbeam] run return run function bm:p48/off',
                      'tag @s add bm.skbeam', 'playsound minecraft:block.beacon.activate player @a[distance=..32] ~ ~ ~ 1 1.6',
                      say('Tractor beam ON. Look up + right-click to switch it off.', '#c27dff')])
    fn('p48/off', ['tag @s remove bm.skbeam', 'playsound minecraft:block.beacon.deactivate player @a[distance=..32] ~ ~ ~ 1 1.6',
                   say('Tractor beam off.', 'gray')])

    # the beam itself, every tick, from the saucer down
    tick.append('execute as @a[tag=bm.skbeam] at @s run function bm:p48/tick')
    fn('p48/tick', ['execute unless function bm:p35/skiff/riding run return run tag @s remove bm.skbeam',
                    'tag @s add bm.skpil', 'execute on vehicle at @s run function bm:p48/column', 'tag @s remove bm.skpil'])
    col = (f'positioned ~-2.5 ~-{BEAM_DEPTH} ~-2.5 as @e[dx=4,dy={BEAM_DEPTH - 1},dz=4,'
           'type=!#bm:p48_nolift,tag=!bm.npc,tag=!bm.skiff,tag=!bm.skpil,tag=!bm.skbeam]')
    fn('p48/column', [
        'scoreboard players add #skp bm.rng 1', 'execute if score #skp bm.rng matches 4.. run function bm:p48/fx',
        # creatures and players: lift, then hold just under the hull
        f'execute store result score #sy bm.rng run data get entity @s Pos[1] 10',
        f'execute {col} at @s run function bm:p48/lift',
        # items and xp: up into the saucer, then into the pilot's pack
        f'execute positioned ~-2.5 ~-{BEAM_DEPTH} ~-2.5 as @e[type=#bm:p48_loot,dx=4,dy={BEAM_DEPTH},dz=4] at @s run function bm:p48/loot'])
    wjson('bm/tags/entity_type/p48_loot.json', {'values': ['minecraft:item', 'minecraft:experience_orb']})
    fn('p48/fx', ['scoreboard players set #skp bm.rng 0'] +
       [f'particle minecraft:dust{{color:[0.76,0.49,1.0],scale:1.5}} ~ ~-{d} ~ 0.9 0.2 0.9 0 4 force @a[distance=..64]' for d in range(1, BEAM_DEPTH, 2)] +
       ['particle minecraft:end_rod ~ ~-1 ~ 0.6 0 0.6 0.01 2 force @a[distance=..64]', 'playsound minecraft:block.beacon.ambient player @a[distance=..24] ~ ~ ~ 0.4 2'])
    fn('p48/lift', ['execute if entity @s[type=minecraft:player,gamemode=creative] run return 0',
                    'execute if entity @s[type=minecraft:player,gamemode=spectator] run return 0',
                    'execute store result score #hp bm.rng run attribute @s minecraft:max_health get',
                    f'execute if score #hp bm.rng matches {MAX_HP + 1}.. run return 0',
                    # (height under the saucer, in tenths)
                    'execute store result score #ey bm.rng run data get entity @s Pos[1] 10',
                    'scoreboard players operation #ey bm.rng -= #sy bm.rng',
                    'execute if score #ey bm.rng matches ..-36 run return run effect give @s minecraft:levitation 1 4 true',
                    'effect clear @s minecraft:levitation', 'effect give @s minecraft:slow_falling 1 0 true',
                    'particle minecraft:reverse_portal ~ ~0.5 ~ 0.2 0.3 0.2 0 1'])
    fn('p48/loot', ['execute store result score #ey bm.rng run data get entity @s Pos[1] 10', 'scoreboard players operation #ey bm.rng -= #sy bm.rng',
                    'execute if score #ey bm.rng matches -25.. run return run tp @s @a[tag=bm.skpil,limit=1]',
                    'data merge entity @s {Motion:[0.0d,0.45d,0.0d]}',
                    'particle minecraft:reverse_portal ~ ~0.2 ~ 0.1 0.1 0.1 0 1'])
    # a skiff that folds away, lands or is turned away takes the beam with it
    for f_ in ('p35/skiff/gone', 'p35/skiff/refuse'):
        G.FUNCS[f_].insert(0, 'execute on passengers if entity @s[type=minecraft:player] run tag @s remove bm.skbeam')

    # the key's help text
    ON = G.FUNCS['p35/skiff/use']
    for i, l in enumerate(ON):
        if 'Skiff online.' in l:
            ON[i] = title('@s', 'actionbar', T('Skiff online. Right-click: laser. Look down: TNT. Look up: tractor beam. Sneak: land.', GREEN))

    G.FUNCS['tick'] += tick
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

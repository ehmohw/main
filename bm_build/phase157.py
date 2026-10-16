"""2.80b: THE SPECIAL NIGHTS, DEBUGGED - the Blood Moon, Lucky Nights and Invasion Nights played through end to end (t177).

THE BEASTS STAYED  at dawn the Vorn ships took their troopers, saucers and bosses home - but not their bioengineered beasts.
                 The big slimes (and every slime they split into) and the fire-proof phantoms stayed all day. Now every
                 Vorn of the night lifts away with the ships.
...AND TOOK THE WRONG VORN  that same dawn beam took every Vorn trooper in every world: a live alien heist's guards, the
                 Dreadnought's own guardians, and the Overseer (summoned with a Vorn Beacon, any time) mid-fight, with its
                 health bar. Now dawn takes only the night's own Vorn, in the overworld, and leaves an Overseer fight alone.
THE MIDNIGHT BOSS  "A Vorn boss will land at midnight" - unless no one was out under the sky at that moment: then the
                 night's boss was spent and never came. Now it waits for someone to step outside (until an hour before
                 dawn, so it never lands as the ships leave).
A BLOOD MOON OVER A SPECIAL NIGHT  (an admin's Blood Moon on a Lucky or Invasion Night) ended it with "Dawn..." at
                 midnight. Now the Blood Moon says it drowns that night out.
(and a Blood Moon counted itself twice - harmless, tidied.)"""


def generate(G):
    fn, tellraw, PREFIX, T = G.fn, G.tellraw, G.PREFIX, G.T
    GREEN = '#7dff6a'
    # ---- dawn: every Vorn of the night lifts away - not the heist's, the Dreadnought's or an Overseer fight's
    end = G.FUNCS['p32/inv/end']
    beam = [l for l in end if l.endswith('run function bm:p32/beamup')]
    assert len(beam) == 3, beam
    k = end.index(beam[0])
    for l in beam:
        end.remove(l)
    end[k:k] = ['function bm:p157/dawn']
    end.remove('bossbar set bm:overseer visible false')
    fn('p157/dawn', [
        'execute in minecraft:overworld as @e[type=minecraft:phantom,tag=bm.vb_overseer,distance=0..] at @s run tag @e[tag=bm.vorn,distance=..64] add bm.vstay',
        'execute in minecraft:overworld as @e[tag=bm.vorn,tag=!bm.vstay,tag=!bm.gvg,tag=!bm.vguardian,distance=0..] at @s run function bm:p32/beamup',
        'execute in minecraft:overworld as @e[type=minecraft:slime,name="Bioengineered Slime",tag=!bm.vstay,distance=0..] at @s run function bm:p32/beamup',
        'tag @e[tag=bm.vstay] remove bm.vstay'])
    # ---- the midnight boss waits for someone under the open sky (until 21999)
    bl = G.FUNCS['p32/inv/boss_land']
    bl.remove('scoreboard players set #iboss bm.bm 1')
    k = next(i for i, l in enumerate(bl) if 'run function bm:p32/inv/boss_pick' in l)
    bl.insert(k, 'execute if entity @a[tag=bm.bcand] run scoreboard players set #iboss bm.bm 1')
    du = G.FUNCS['p32/inv/during']
    k = next(i for i, l in enumerate(du) if 'run function bm:p32/inv/boss_land' in l)
    du[k] = du[k].replace('matches 18000..', 'matches 18000..21999')
    # ---- a Blood Moon over a Lucky / Invasion Night drowns it out (not "Dawn" at midnight)
    for f, word, col, over in (('p22/lucky/end', 'Dawn. The Lucky Night is over.', 'gold', 'The Blood Moon swallows the Lucky Night.'),
                               ('p32/inv/end', 'Dawn. The Vorn ships lift away... for now.', GREEN, 'The Blood Moon rises - the Vorn ships flee its red light.')):
        L = G.FUNCS[f]
        k = next(i for i, l in enumerate(L) if l.startswith('tellraw @a[tag=bm.ow]') and word in l)
        L[k] = 'execute unless score #want bm.bm matches 1 run ' + L[k]
        L.insert(k + 1, 'execute if score #want bm.bm matches 1 run ' + tellraw('@a[tag=bm.ow]', PREFIX + [T(over, 'dark_red')]))
    # ---- the Blood Moon count: once a moon
    st = G.FUNCS['bloodmoon/start']
    st.remove('scoreboard players add #bmn bm.bm 1')

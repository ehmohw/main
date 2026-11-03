"""3.0g: THE HIT CAP - no single blow (nor a burst of them) takes more than so much off a boss.

The owner: the final boss sword "shreds through their health" - the Dread bosses, the Dread Sovereign, the Dread Mires and the
Statue Knights. Armour can't stop a big enough number, so this caps what they actually LOSE: an entity tagged bm.hcap with a
cap in bm.hcc (tenths of a point) loses at most that much health in any half-second (WINDOW ticks - a mob's own hurt
cooldown). Each tick its health is read (x10) and compared with the last tick's (bm.hcl); a drop past what the window still
allows is put back (health set to last - allowed), with a dull clank so the player knows the blow glanced. Only a HURT counts:
a drop while its HurtTime is 0 (health set by a command - a test's stage, a scripted wound) is taken as the new mark. Healing,
a phase's refill, anything that RAISES its health, just moves the mark up. (`function bm:hitcap/sync`, as the entity, forgets
the mark outright.)

What it can't do: a single blow bigger than the health it has left still kills (the game kills before any function runs) -
which is why every user keeps a FLOOR of health under its real pool (bigger than its cap).

Scores: bm.hcc (the cap, x10), bm.hcl (last tick's health x10), bm.hcw (taken so far this window, x10), bm.hct (window ticks
left). Users: phase197 (the Dread bosses), phase238 (the Sovereign), mirekit/phase246 (the Dread Mire), phase245 (the knights)."""

WINDOW = 10
OBJ = ['bm.hcc', 'bm.hcl', 'bm.hcw', 'bm.hct']


def install(G):
    """the shared machinery (idempotent: every user calls it)"""
    if 'hitcap/tick' in G.FUNCS:
        return
    fn = G.fn
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in OBJ]
    G.OBJECTIVES += OBJ
    fn('hitcap/tick', ['execute store result score #hn bm.rng run data get entity @s Health 10',
                       # (new to the cap - or just synced: this health is the mark)
                       'execute unless score @s bm.hcl matches -2147483648.. run return run function bm:hitcap/mark',
                       'execute if score @s bm.hct matches 1.. run scoreboard players remove @s bm.hct 1',
                       'execute unless score @s bm.hct matches 1.. run scoreboard players set @s bm.hcw 0',
                       'execute if score #hn bm.rng >= @s bm.hcl run return run scoreboard players operation @s bm.hcl = #hn bm.rng',
                       # (a drop with no hurt on it - HurtTime 0: health set by a command, a scripted wound - is taken as it is)
                       'execute store result score #ht bm.rng run data get entity @s HurtTime',
                       'execute if score #ht bm.rng matches ..0 run return run function bm:hitcap/mark',
                       # (a drop: how much, and how much this window still allows)
                       'scoreboard players operation #hd bm.rng = @s bm.hcl', 'scoreboard players operation #hd bm.rng -= #hn bm.rng',
                       f'execute unless score @s bm.hct matches 1.. run scoreboard players set @s bm.hct {WINDOW}',
                       'scoreboard players operation #ha bm.rng = @s bm.hcc', 'scoreboard players operation #ha bm.rng -= @s bm.hcw',
                       'execute if score #ha bm.rng matches ..-1 run scoreboard players set #ha bm.rng 0',
                       'execute if score #hd bm.rng > #ha bm.rng run function bm:hitcap/clip',
                       'scoreboard players operation @s bm.hcw += #hd bm.rng', 'scoreboard players operation @s bm.hcl = #hn bm.rng'])
    fn('hitcap/mark', ['scoreboard players operation @s bm.hcl = #hn bm.rng', 'scoreboard players set @s bm.hcw 0', 'scoreboard players set @s bm.hct 0'])
    fn('hitcap/clip', ['scoreboard players operation #hd bm.rng = #ha bm.rng',
                       'scoreboard players operation #hn bm.rng = @s bm.hcl', 'scoreboard players operation #hn bm.rng -= #hd bm.rng',
                       'execute store result entity @s Health float 0.1 run scoreboard players get #hn bm.rng',
                       'particle minecraft:enchanted_hit ~ ~1.5 ~ 0.6 0.8 0.6 0.2 10',
                       'playsound minecraft:item.shield.block hostile @a[distance=..20] ~ ~ ~ 0.7 0.6'])
    fn('hitcap/sync', ['scoreboard players reset @s bm.hcl'])
    G.FUNCS['tick'].append('execute as @e[tag=bm.hcap] at @s run function bm:hitcap/tick')


def arm(cap):
    """the lines (as the entity) that put it under a cap of `cap` points: its tag, its cap, a fresh mark"""
    return ['tag @s add bm.hcap', f'scoreboard players set @s bm.hcc {int(round(cap * 10))}', 'function bm:hitcap/sync']

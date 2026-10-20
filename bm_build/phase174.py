"""2.83: THE LESS URGENT LIST, part one - the drowned that never fought, full bags, the Trophy Stand, cases to stand on,
Emma and Leo for everyone, money that breaks back down.

THE SUNKEN THRONE  (p2/data.py, p2/logic.py, p2/bosses.py) the drowned only hunt someone in water or out at night, so on the
                   temple's dry floors they stood about. The Tyrant's crew are Tidebound Sailors (zombies in turtle shells,
                   tridents and swords) and Barnacle Bowmen (bogged) now - spawners, waves, his calls and the fail mob. The
                   Tyrant himself is still a drowned in his pool: he answers a blow, and his slam and surge need no water.
FULL BAGS          the Vacuum Satchel and the Prime Cooler say so when something they'd take won't fit (every 10 seconds at
                   most): "Your Vacuum Satchel is full."
THE TROPHY STAND   (phase161) it stood back to front - an item display shows a model's back toward the way it faces - so the
                   tall back panel faced you, the trophies hovered over the low step and the laurels sat inside the panel.
                   The stand and its trophies turn round (stands already set down turn by themselves); the steps stop at the
                   back panel instead of running through it (no more flickering at the back).
DISPLAY CASES      a floor case is solid now - stand on it (an invisible barrier fills its block; picked up, the barrier
                   goes too). Its click box is a hair bigger than the block, so right-click and punch still reach it.
EMMA AND LEO       (phase57, phase96) every player can find each of them - Emma hums for anyone without her ribbon, and a
                   fort that's been held stays open to anyone who hasn't got Leo's crest yet (he takes up his watch again).
                   Emma also turns up in plains and birch woods now, a little more often; the forts are a little closer.
THE RAT BANK       (phase31, gen_dp) Medallions and Trophies break back down at the rates they're made (1 Medallion = 5
                   Tokens, 1 Trophy = 4 Medallions) at Old Barnaby and the Fence - and the Banker's Card has an Exchange
                   page that changes your account up or down, no fee.
"""
from items import T
from nbt import snbt, F

SEA = '#3fb8a8'


def generate(G):
    fn, title = G.fn, G.title
    F_ = G.FUNCS
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    objs = ['bm.vfcd']
    F_['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ================================================================== FULL BAGS
    # (p33/vac/take: what's left of the stack after merging and a free slot - unchanged means nothing fit)
    tk = F_['p33/vac/take']
    k = next(i for i, l in enumerate(tk) if l.startswith('execute store result score #vn bm.rng run data get storage bm:tmp vac.in.count'))
    tk.insert(k + 1, 'scoreboard players operation #vn0 bm.rng = #vn bm.rng')
    k = next(i for i, l in enumerate(tk) if 'run function bm:p33/vac/newslot' in l)
    tk.insert(k + 1, 'execute if score #vn bm.rng = #vn0 bm.rng run scoreboard players set #vfull bm.rng 1')
    for pull, name in (('p33/vac/pull', 'Vacuum Satchel'), ('p148/cool/pull', 'Prime Cooler')):
        pl = F_[pull]
        k = next(i for i, l in enumerate(pl) if l == 'scoreboard players set #vtak bm.rng 0')
        pl.insert(k + 1, 'scoreboard players set #vfull bm.rng 0')
        pl.append(f'execute if score #vfull bm.rng matches 1 unless score @s bm.vfcd matches 1.. run function bm:p174/full {{n:"{name}"}}')
    fn('p174/full', ['scoreboard players set @s bm.vfcd 10', '$' + title('@s', 'actionbar', [T('Your $(n) is full', '#ffb060'), T(' - it leaves the rest on the ground.', 'gray')]),
                     'playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.6 0.8'])
    F_['loop/second'].append('scoreboard players remove @a[scores={bm.vfcd=1..}] bm.vfcd 1')

    # ================================================================== THE TROPHY STAND: stands already set down turn round
    F_['loop/second'].append('execute as @e[type=minecraft:item_display,tag=bm.tsbase,tag=!bm.ts283] run function bm:p174/ts_turn')
    fn('p174/ts_turn', ['tag @s add bm.ts283', 'data modify entity @s transformation.left_rotation set value [0f,1f,0f,0f]'])

    # ================================================================== DISPLAY CASES: a floor case you can stand on
    sf = F_['p72/dc/spawn_floor']
    sf.insert(0, 'setblock ~ ~ ~ minecraft:barrier keep')
    k = next(i for i, l in enumerate(sf) if l.startswith('tp @e[tag=bm.dcnew'))
    sf.insert(k, 'execute as @e[type=minecraft:interaction,tag=bm.dcnew,distance=..0.1] run function bm:p174/dc_floor')
    fn('p174/dc_floor', ['tag @s add bm.dcfloor', 'tag @s add bm.dc283', 'data merge entity @s {width:1.02f,height:1.02f}'])
    F_['p72/dc/gone'].insert(0, 'execute if entity @s[tag=bm.dcfloor] if block ~ ~ ~ minecraft:barrier run setblock ~ ~ ~ minecraft:air')
    # (cases already in the world: a floor case's box was 0.85 wide)
    F_['loop/second'].append('execute as @e[type=minecraft:interaction,tag=bm.dchit,tag=!bm.dc283] at @s run function bm:p174/dc_old')
    fn('p174/dc_old', ['tag @s add bm.dc283', 'execute unless data entity @s {width:0.85f} run return 0',
                       'setblock ~ ~ ~ minecraft:barrier keep', 'tag @s add bm.dcfloor', 'data merge entity @s {width:1.02f,height:1.02f}'])
    # (the place-check looked for another case within 0.7 of a floor spot: the bigger box doesn't change where it sits)

    # ================================================================== LEO: a held fort opens again for anyone without his crest
    crest = '*[minecraft:custom_data~{bm:"leo_crest"}]'
    F_['loop/second'].append('execute as @e[type=minecraft:marker,tag=bm.lefort,tag=bm.ledone] at @s if entity @a[distance=..32,gamemode=!spectator] '
                             'run function bm:p174/fort_open')
    fn('p174/fort_open', ['tag @a[distance=..32] remove bm.lenocrest',
                          f'execute as @a[distance=..32,gamemode=!spectator] unless items entity @s container.* {crest} unless items entity @s weapon.offhand {crest} run tag @s add bm.lenocrest',
                          'execute unless entity @a[tag=bm.lenocrest,distance=..32] run return 0', 'tag @a remove bm.lenocrest',
                          'tag @s remove bm.ledone', 'particle minecraft:splash ~ ~1.5 ~ 0.5 0.8 0.5 0.1 20'])

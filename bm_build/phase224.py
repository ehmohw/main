"""2.94u: SIGNATURE MOVES for the rest of the fighters (atk.sig, as phase223 - their own poses; dashes where they close in;
a second blow at least half a second after the first, so it lands in full). Each: (when) its move.

KILLERWATT    (a foe 4-12 off; 12 s) STORM LEAP: crouch - a leap onto it - the slam (10 to all within 4), a roar.
ZIB           (a foe within 16; 12 s) ORBITAL STRIKE: charge, aim to the sky - a beam comes down on it (14; 6 round it).
TULLIUS       (a foe 4-12 off; 10 s) ANCHOR'S AWAY: the harpoon thrown - he reels himself in - a thrust (12), then the blunderbuss (8, a cone).
FISHY         (two foes within 8; 12 s) TIDAL BUBBLE: they're lifted in bubbles - then the thunder comes down (10 to all within 5).
DENNIS        (a foe 3.5-10 off; 9 s) MOTHER LODE RUSH: wrench back - in he charges - a whack (10), then the slam (8 to all within 3.5, gold everywhere).
PISTACHIO     (a foe 3-10 off; 9 s) SILVER SERVICE: a bow - he glides in - a slap (9), then the wail (5 to all within 5, weakened).
KING OMEGA    (a foe 3.5-12 off; 10 s) SOUL GLIDE: in on the dark - a claw (12), then a sweep of soul fire (8 to all within 4).
THE CHEF      (a foe 3-10 off; 9 s) KITCHEN FURY: cleaver up - in he goes - two whacks (10, 10).
THE NEIGHBOR  (two foes within 8; 12 s) GRAND FINALE: he conducts - the crescendo - the final note (10 to all within 5), a bow.
QUEEN AVA     (a foe 3-12 off; 10 s) RIPTIDE: she rides the current in - a strike (10), then the tide (7 to all within 4), a curtsey.
QUEEN PEARL   (a foe 3-10 off; 10 s) ROYAL TWIRL: a twirl - in she sweeps - a flick (9), then a proclamation (7 to all within 4, slowed).
BLOO          (a foe 4-12 off; 9 s) SAVAGE LEAP: crouched - the leap - a raking swipe (10), then a roar (6 to all within 5, weakened).
THE STALKER   (a foe 4-14 off; 10 s) NIGHT HUNT: folded - it sprints in - rends (12), then screams (6 to all within 5, darkness).
ARACHNO-LANTERN (a foe 4-12 off; 10 s) EMBER POUNCE: it rears - leaps - stomps (10 to all within 3), then flares (6 to all within 4, alight).
BONES         (a foe 3-12 off; 10 s) DEATH ROLL: a charge in - the bite (12), then he rolls with it (6, 6).
MR. CAPSHUN   (a foe 3-10 off; 9 s) INK RUSH: the brush up - a dash in - a swipe (9), then a flung splat (7 to all within 3.5).
THE SKY BUDDIES (a foe within 14; 12 s) STORM FRONT: they gather a storm - drizzle - the beam (12; 5 round it).
8-BIT EMMA    (a foe 3-10 off; 9 s) SUPER STOMP: powered up - a jump onto it - the stomp (10 to all within 3).
8-BIT LEO     (a foe 3-10 off; 9 s) DASH SLASH: in he dashes - a slash (10), and a second (8 to all within 3).
8-BIT CECIL   (a foe within 14; 10 s) HEX BOLT: the hex drawn - the blast at his foe (12; 6 round it)."""
import atk

FOE = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body'


def generate(G):
    import phase125 as P125
    fn = G.fn
    col = lambda w: P125.WHO[w][2]

    def hits(pfx, me, host='wolf'):
        """<pfx>/sg/h_<d>_<r>[_all][_<fx>]: as the follower, d to the nearest (or every) foe within r - by the follower"""
        made = {}
        def h(d, r, every=False, fx=()):
            name = f'{pfx}/sg/h_{d}_{str(r).replace(".", "_")}' + ('_all' if every else '') + (f'_{len(made)}' if fx else '')
            sel = f'@e[{FOE},distance=..{r}' + (']' if every else ',sort=nearest,limit=1]')
            fn(name, [f'tag @s add {me}', f'execute as {sel} at @s run damage @s {d} minecraft:mob_attack by @e[type=minecraft:{host},tag={me},limit=1]'] +
               [f'execute as {sel} at @s run {c}' for c in fx] + [f'tag @s remove {me}'])
            made[name] = 1
            return f'function bm:{name}'
        return h

    def pose(pfx, n):
        return f'function bm:{pfx}/pose/{n}'

    def rig(w, pfx, s_obj, me, trig, cd, tl, end, dash=None, face='foe', extra_trig='', tick=None, state=None, anim=None, place=None, st=21, each=()):
        x = s_obj[:-1] + 'x'
        atk.sig(G, pfx, kid=1, tick_fn=tick or f'{pfx}/tick', state_fn=state or f'{pfx}/state', anim_fn=anim or f'{pfx}/anim', s_obj=s_obj,
                place_fn=place or f'{pfx}/place', col=col(w),
                trigger=f'execute unless data entity @s {{Sitting:1b}} unless score @s {x} matches 1.. {extra_trig}if entity @e[{FOE},distance={trig}]',
                cd=cd, end=end, face=face, st=st, dash_kw=dash, timeline=tl, each=each, busy=x)

    near = lambda r: f'@e[{FOE},distance=..{r},sort=nearest,limit=1]'
    snd = lambda s, v=1, p=1: f'playsound minecraft:{s} neutral @a[distance=..20] ~ ~ ~ {v} {p}'
    # two foes near (as the follower): the fight is a crowd
    fn('atk/two8', [f'execute store result score #n bm.rng if entity @e[{FOE},distance=..8]', 'return run execute if score #n bm.rng matches 2..'])

    # ---- TULLIUS
    h = hits('p132', 'bm.tume2')
    rig('tul', 'p132', 'bm.tus', 'bm.tume2', '4..12', 200, end=36, dash=dict(reach=2.0, speed=1.3, lift=0), tl={
        1: [pose('p132', 'throw_back'), snd('item.trident.throw', 0.8, 0.8)], 5: [pose('p132', 'throw')],
        7: [pose('p132', 'hook_pull'), snd('block.chain.place', 1, 0.7), f'DASH 1 {near(12)}'],
        8: [pose('p132', 'thrust'), h(12, 2.8), snd('item.trident.hit', 1, 0.8)],
        12: [pose('p132', 'aim')], 19: [pose('p132', 'blast'), h(8, 4, True, ['particle minecraft:large_smoke ~ ~1 ~ 0.3 0.3 0.3 0.02 4']),
                                        'particle minecraft:explosion ~ ~1 ~ 0.6 0.3 0.6 0 2', snd('entity.generic.explode', 0.6, 1.4)],
        26: [pose('p132', 'reload')], 33: [pose('p132', 'idle_a')]})
    # ---- FISHY
    h = hits('p145', 'bm.fyme')
    rig('fishy', 'p145', 'bm.fys', 'bm.fyme', '..8', 240, end=30, extra_trig='if function bm:atk/two8 ', tl={
        1: [pose('p145', 'point'), snd('entity.player.splash', 0.6, 1.4)],
        4: [f'execute as @e[{FOE},distance=..8] at @s run effect give @s minecraft:levitation 1 0', f'execute as @e[{FOE},distance=..8] at @s run particle minecraft:bubble_pop ~ ~1 ~ 0.3 0.6 0.3 0.05 12',
            snd('block.bubble_column.upwards_ambient', 1, 1)],
        8: [pose('p145', 'thunder_up')],
        16: [pose('p145', 'thunder'), h(10, 5, True), 'particle minecraft:electric_spark ~ ~0.5 ~ 2 0.3 2 0.2 40', 'particle minecraft:splash ~ ~0.5 ~ 2 0.3 2 0.2 40',
             snd('entity.lightning_bolt.thunder', 0.4, 1.6)],
        26: [pose('p145', 'bow')]})
    # ---- DENNIS
    h = hits('p163/dw', 'bm.dwme')
    rig('dennis', 'p163/dw', 'bm.dws', 'bm.dwme', '3.5..10', 180, end=32, dash=dict(reach=1.8, speed=1.0, lift=1), tl={
        1: [pose('p163/dw', 'swing_back'), snd('entity.iron_golem.step', 0.8, 1.2)],
        5: [f'DASH 1 {near(10)}'],
        6: [pose('p163/dw', 'swing'), h(10, 3), snd('block.anvil.land', 0.4, 1.4)],
        10: [pose('p163/dw', 'slam_up')],
        17: [pose('p163/dw', 'slam'), h(8, 3.5, True), 'particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.3 ~ 1.5 0.2 1.5 0 40',
             'particle minecraft:wax_on ~ ~0.5 ~ 1.5 0.3 1.5 0 20', snd('entity.generic.explode', 0.5, 1.2)],
        27: [pose('p163/dw', 'idle_a')]})
    # ---- PISTACHIO
    h = hits('p163/pi', 'bm.pime')
    rig('pistachio', 'p163/pi', 'bm.pis', 'bm.pime', '3..10', 180, end=30, dash=dict(reach=1.6, speed=0.8, lift=0), tl={
        1: [pose('p163/pi', 'bow'), snd('block.bell.use', 0.4, 1.8)],
        5: [pose('p163/pi', 'slap_back'), f'DASH 1 {near(10)}'],
        6: [pose('p163/pi', 'slap'), h(9, 2.8), snd('entity.player.attack.sweep', 0.8, 1.7)],
        10: [pose('p163/pi', 'serve')],
        17: [pose('p163/pi', 'wail'), h(5, 5, True, ['effect give @s minecraft:weakness 4 0']), 'particle minecraft:sculk_soul ~ ~1 ~ 2 0.5 2 0.02 20', snd('entity.ghast.scream', 0.4, 1.4)],
        26: [pose('p163/pi', 'idle_a')]})
    # ---- KING OMEGA
    h = hits('p170', 'bm.ompme')
    rig('omega', 'p170', 'bm.oqs', 'bm.ompme', '3.5..12', 200, end=32, dash=dict(reach=2.2, speed=1.0, lift=0), tl={
        1: [pose('p170', 'glide_a'), 'particle minecraft:soul ~ ~1 ~ 0.6 0.4 0.6 0.02 10', snd('particle.soul_escape', 1, 0.6)],
        4: [f'DASH 1 {near(12)}'],
        5: [pose('p170', 'claw'), h(12, 3)],
        9: [pose('p170', 'flame_up')],
        16: [pose('p170', 'flame_swing'), h(8, 4, True, ['data merge entity @s {Fire:60s}']), 'particle minecraft:soul_fire_flame ~ ~0.8 ~ 2 0.3 2 0.03 40', snd('entity.blaze.shoot', 0.7, 0.6)],
        26: [pose('p170', 'idle_a')]})
    # ---- THE CHEF
    h = hits('p186', 'bm.kkme')
    rig('chef', 'p186', 'bm.kqs', 'bm.kkme', '3..10', 180, end=30, dash=dict(reach=1.7, speed=1.0, lift=0), tl={
        1: [pose('p186', 'whack_up'), snd('item.axe.scrape', 0.6, 1.4)], 4: [f'DASH 1 {near(10)}'],
        5: [pose('p186', 'whack'), h(10, 3), snd('entity.player.attack.crit', 1, 1)],
        9: [pose('p186', 'whack_up')], 16: [pose('p186', 'whack'), h(10, 3), snd('entity.player.attack.crit', 1, 0.8)],
        22: [pose('p186', 'taste')]})
    # ---- THE NEIGHBOR
    h = hits('p187', 'bm.nbme')
    rig('neighbor', 'p187', 'bm.nqs', 'bm.nbme', '..8', 240, end=32, extra_trig='if function bm:atk/two8 ', tl={
        1: [pose('p187', 'conduct_a'), 'particle minecraft:note ~ ~2 ~ 1 0.4 1 1 4'], 6: [pose('p187', 'conduct_b'), 'particle minecraft:note ~ ~2 ~ 1.5 0.4 1.5 1 6'],
        11: [pose('p187', 'crescendo'), snd('block.note_block.bell', 1, 0.7)],
        16: [pose('p187', 'strike'), h(10, 5, True), 'particle minecraft:note ~ ~1 ~ 2.5 0.5 2.5 1 20', 'particle minecraft:sonic_boom ~ ~1 ~ 0 0 0 0 1',
             snd('block.note_block.bass', 1, 0.5), snd('block.note_block.bell', 1, 1.5)],
        24: [pose('p187', 'bow')]})
    # ---- QUEEN AVA
    h = hits('p189', 'bm.avme')
    rig('ava', 'p189', 'bm.aqs', 'bm.avme', '3..12', 200, end=34, tl={
        1: [pose('p189', 'cast_up'), 'particle minecraft:bubble_pop ~ ~1 ~ 0.6 0.6 0.6 0.05 16'], 4: [f'DASH 2 {near(12)}'],
        5: [pose('p189', 'cast'), h(10, 3), 'particle minecraft:splash ~ ~1 ~ 0.4 0.5 0.4 0.2 20'],
        9: [pose('p189', 'ward_a')],
        16: [pose('p189', 'tide'), h(7, 4, True), 'particle minecraft:splash ~ ~0.5 ~ 2 0.3 2 0.3 60', snd('entity.player.splash.high_speed', 1, 0.8)],
        26: [pose('p189', 'curtsey')]})
    # ---- QUEEN PEARL
    h = hits('p190', 'bm.pqme')
    rig('pearlq', 'p190', 'bm.pks', 'bm.pqme', '3..10', 200, end=32, dash=dict(reach=1.6, speed=1.0, lift=0), tl={
        1: [pose('p190', 'twirl'), 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.03 10'], 4: [f'DASH 1 {near(10)}'],
        5: [pose('p190', 'flick'), h(9, 3)],
        9: [pose('p190', 'flick_up')],
        16: [pose('p190', 'proclaim'), h(7, 4, True, ['effect give @s minecraft:slowness 3 1']), 'particle minecraft:end_rod ~ ~1 ~ 2 0.4 2 0.05 30', snd('block.amethyst_block.chime', 1, 1.3)],
        24: [pose('p190', 'wink')]})
    # ---- BLOO
    h = hits('p191', 'bm.bome')
    rig('bloo', 'p191', 'bm.bks', 'bm.bome', '4..12', 180, end=30, tl={
        1: [pose('p191', 'crouch'), snd('entity.cat.hiss', 1, 0.5)], 5: [pose('p191', 'pounce'), f'DASH 3 {near(12)}'],
        6: [pose('p191', 'swipe'), h(10, 3, False, ['effect give @s minecraft:wither 2 0'])],
        10: [pose('p191', 'swipe_up')],
        17: [pose('p191', 'roar'), h(6, 5, True, ['effect give @s minecraft:weakness 4 0']), 'particle minecraft:cloud ~ ~1 ~ 2 0.4 2 0.1 30', snd('entity.ravager.roar', 1, 1.2)],
        27: [pose('p191', 'idle_a')]})
    # ---- THE STALKER (its own claws)
    fn('p193/sg/rend', ['tag @s add bm.svme', f'execute as {near(3)} at @s run damage @s 12 bm:stalker_claw by @e[type=minecraft:wolf,tag=bm.svme,limit=1]', 'tag @s remove bm.svme',
                        snd('entity.warden.attack_impact', 0.6, 1.4)])
    fn('p193/sg/scream', ['tag @s add bm.svme', f'execute as @e[{FOE},distance=..5] at @s run damage @s 6 bm:stalker_claw by @e[type=minecraft:wolf,tag=bm.svme,limit=1]',
                          f'effect give @e[{FOE},distance=..5] minecraft:darkness 4 0', 'tag @s remove bm.svme', 'particle minecraft:sculk_soul ~ ~1.6 ~ 1.5 0.5 1.5 0.02 20',
                          snd('entity.warden.roar', 0.5, 1.6)])
    rig('stalker', 'p193', 'bm.sqs', 'bm.svme', '4..14', 200, end=34, dash=dict(reach=1.8, speed=1.2, lift=0), face='foe', tl={
        1: [pose('p193', 'fold'), 'particle minecraft:large_smoke ~ ~1 ~ 0.3 0.5 0.3 0.02 8'], 5: [pose('p193', 'sprint_0'), f'DASH 1 {near(14)}'],
        6: [pose('p193', 'rend_up')], 8: [pose('p193', 'rend'), 'function bm:p193/sg/rend'],
        12: [pose('p193', 'tilt')], 19: [pose('p193', 'scream'), 'function bm:p193/sg/scream'], 30: [pose('p193', 'idle_a')]},
        each=['execute if score @s bm.ksg matches 1000 store result score #sf bm.rng run scoreboard players get @s bm.kd',
              'execute if score @s bm.ksg matches 1000 run scoreboard players operation #sf bm.rng %= #4 bm.rng'] +
             [f'execute if score @s bm.ksg matches 1000 if score #sf bm.rng matches {i} run {pose("p193", f"sprint_{i * 2}")}' for i in range(4)])
    # ---- THE ARACHNO-LANTERN
    h = hits('p194', 'bm.lnme')
    rig('lantern', 'p194', 'bm.ljs', 'bm.lnme', '4..12', 200, end=32, dash=dict(reach=1.8, speed=1.0, lift=3), tl={
        1: [pose('p194', 'rear'), snd('entity.spider.ambient', 1, 0.6)], 6: [f'DASH 1 {near(12)}'],
        7: [pose('p194', 'stomp'), h(10, 3, True), 'particle minecraft:flame ~ ~0.3 ~ 1.2 0.2 1.2 0.03 30', snd('entity.ravager.step', 1, 0.9)],
        11: [pose('p194', 'rear')],
        18: [pose('p194', 'flare'), h(6, 4, True, ['data merge entity @s {Fire:80s}']), 'particle minecraft:lava ~ ~1 ~ 1.5 0.4 1.5 0 16', snd('item.firecharge.use', 1, 0.7)],
        28: [pose('p194', 'idle_a')]})
    # ---- BONES
    h = hits('p196', 'bm.bjme')
    rig('bones', 'p196', 'bm.bzs', 'bm.bjme', '3..12', 200, end=36, tl={
        1: [pose('p196', 'charge'), 'particle minecraft:bubble ~ ~0.8 ~ 0.4 0.3 0.4 0.02 10'], 4: [f'DASH 3 {near(12)}'],
        5: [pose('p196', 'bite'), h(12, 3)],
        9: [pose('p196', 'thrash_a')], 15: [pose('p196', 'thrash_b'), h(6, 3)], 21: [pose('p196', 'thrash_a')],
        26: [pose('p196', 'thrash_b'), h(6, 3), 'particle minecraft:splash ~ ~1 ~ 0.6 0.4 0.6 0.2 20'], 31: [pose('p196', 'happy')]})
    # ---- MR. CAPSHUN
    h = hits('p198', 'bm.mzme')
    rig('capshun', 'p198', 'bm.zqs', 'bm.mzme', '3..10', 180, end=30, dash=dict(reach=1.6, speed=1.0, lift=1), tl={
        1: [pose('p198', 'swipe_up')], 4: [f'DASH 1 {near(10)}'],
        5: [pose('p198', 'swipe'), h(9, 3), 'particle minecraft:dust{color:[0.1,0.1,0.1],scale:1.4} ~ ~1 ~ 0.4 0.4 0.4 0 12'],
        9: [pose('p198', 'fling_up')],
        16: [pose('p198', 'fling'), h(7, 3.5, True), 'particle minecraft:dust{color:[0.9,0.2,0.6],scale:1.6} ~ ~0.5 ~ 1.5 0.3 1.5 0 30',
             'particle minecraft:dust{color:[0.2,0.6,1.0],scale:1.6} ~ ~0.5 ~ 1.5 0.3 1.5 0 30', snd('entity.slime.squish', 1, 1.2)],
        24: [pose('p198', 'happy')]})
    # ---- THE SKY BUDDIES
    h = hits('p211', 'bm.ybme')
    rig('sky', 'p211', 'bm.yqs', 'bm.ybme', '..14', 240, end=30, tl={
        1: [pose('p211', 'forecast_a'), 'particle minecraft:cloud ~ ~3 ~ 1 0.2 1 0.01 10'], 6: [pose('p211', 'forecast_b')], 10: [pose('p211', 'drizzle'), 'particle minecraft:falling_water ~ ~2.5 ~ 1 0.2 1 0 20'],
        14: [pose('p211', 'beam_up')],
        18: [pose('p211', 'beam'), f'execute at {near(14)} run particle minecraft:end_rod ~ ~3 ~ 0.1 2 0.1 0 30', h(12, 14),
             f'execute at {near(14)} as @e[{FOE},distance=0.1..2.5] run damage @s 5 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.ybme,limit=1]',
             snd('entity.lightning_bolt.thunder', 0.4, 1.8)],
        26: [pose('p211', 'happy')]})
    # ---- THE 8-BIT TRIO (frame by frame)
    h = hits('p213e', 'bm.xmme')
    tl = {1 + i: [pose('p213e', f'power_{i}')] for i in range(7)}
    tl[8] = [f'DASH 1 {near(10)}']
    tl.update({9 + i: [pose('p213e', f'stomp_{i}')] for i in range(9)})
    tl[12] += [h(10, 3, True), 'particle minecraft:poof ~ ~0.2 ~ 0.8 0.1 0.8 0.05 12', snd('entity.slime.jump', 1, 0.6)]
    tl[22] = [pose('p213e', 'idle_a')]
    rig('pxemma', 'p213e', 'bm.xns', 'bm.xmme', '3..10', 180, end=24, dash=dict(reach=1.2, speed=1.0, lift=4), tl=tl)
    h = hits('p213l', 'bm.xlme')
    tl = {1: [pose('p213l', 'slash_0')], 3: [f'DASH 1 {near(10)}']}
    tl.update({4 + i: [pose('p213l', f'slash_{i}')] for i in range(9)})
    tl[6] += [h(10, 3)]
    tl.update({16 + i: [pose('p213l', f'slash_{i}')] for i in range(9)})
    tl[18] += [h(8, 3, True), 'particle minecraft:sweep_attack ~ ~1 ~ 1 0.2 1 0 4']
    tl[27] = [pose('p213l', 'idle_a')]
    rig('pxleo', 'p213l', 'bm.xos', 'bm.xlme', '3..10', 180, end=29, dash=dict(reach=1.6, speed=1.2, lift=0), tl=tl)
    h = hits('p213c', 'bm.xcme')
    tl = {1 + i: [pose('p213c', f'hex_{i}')] for i in range(9)}
    tl.update({11 + i: [pose('p213c', f'attack_{i}')] for i in range(9)})
    tl[15] += [h(12, 14), f'execute at {near(14)} as @e[{FOE},distance=0.1..2.5] run damage @s 6 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.xcme,limit=1]',
               f'execute at {near(14)} run particle minecraft:witch ~ ~1 ~ 0.6 0.6 0.6 0.1 20', snd('entity.evoker.cast_spell', 1, 1.4)]
    tl[22] = [pose('p213c', 'idle_a')]
    rig('pxcecil', 'p213c', 'bm.xds', 'bm.xcme', '..14', 200, end=24, tl=tl)

    # ---- KILLERWATT (his own engine: his moves held while it plays)
    h = hits('p79/pet', 'bm.kxme')
    G.FUNCS['p79/pet/attack'].insert(0, 'execute if score @s bm.ksg matches 1.. run return 0')
    atk.sig(G, 'p79/pet', kid=1, tick_fn='p79/pet/tick', state_fn='p79/pet/move', anim_fn='p79/pet/move', s_obj='bm.ksg', place_fn='p79/pet/place', col=col('kw'),
            trigger=f'execute unless data entity @s {{Sitting:1b}} unless score @s bm.kxt matches 1.. if entity @e[{FOE},distance=4..12]', cd=240, end=34, face='none', st=99999, busy='bm.kxatk',
            dash_kw=dict(reach=2.4, speed=1.0, lift=4), timeline={
                1: [pose('p79/pet', 'crouch'), 'particle minecraft:electric_spark ~ ~0.5 ~ 0.6 0.2 0.6 0.1 16', snd('entity.lightning_bolt.thunder', 0.2, 2)],
                5: [pose('p79/pet', 'slam_up'), f'DASH 1 {near(12)}'],
                6: [pose('p79/pet', 'slam_dn'), h(10, 4, True), 'particle minecraft:electric_spark ~ ~0.3 ~ 2 0.2 2 0.3 60', 'particle minecraft:flash{color:[0.6,1.0,0.5,1.0]} ~ ~1 ~ 0 0 0 0 1',
                    snd('entity.generic.explode', 0.7, 1.3), snd('entity.lightning_bolt.impact', 0.8, 1)],
                16: [pose('p79/pet', 'roar'), snd('entity.ravager.roar', 0.8, 1.4)], 28: [pose('p79/pet', 'idle_a')]})
    # ---- ZIB (his own engine)
    fn('p72/zb/sg/beam', ['tag @s add bm.zbme', f'execute at {near(16)} run particle minecraft:end_rod ~ ~6 ~ 0.1 3 0.1 0 60',
                          f'execute at {near(16)} run particle minecraft:dust{{color:[0.3,1.0,0.9],scale:2}} ~ ~1 ~ 1 0.3 1 0 30',
                          f'execute as {near(16)} at @s run damage @s 14 minecraft:mob_projectile by @e[type=minecraft:wolf,tag=bm.zbme,limit=1]',
                          f'execute at {near(16)} as @e[{FOE},distance=0.1..2.5] run damage @s 6 minecraft:mob_projectile by @e[type=minecraft:wolf,tag=bm.zbme,limit=1]',
                          'tag @s remove bm.zbme', snd('block.beacon.power_select', 1, 1.6), snd('entity.generic.explode', 0.4, 1.8)])
    atk.sig(G, 'p72/zb', kid=1, tick_fn='p72/zb/tick', state_fn='p72/zb/anim', anim_fn='p72/zb/anim', s_obj='bm.ksg', place_fn='p72/zb/anim', col=col('zib'),
            trigger=f'execute unless data entity @s {{Sitting:1b}} unless score @s bm.zbk matches 1.. if entity @e[{FOE},distance=..16]', cd=240, end=26, face='none', st=99999, busy='bm.zbk',
            timeline={1: ['function bm:p72/zb/p/charge', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.4 0.3 0.05 10', snd('block.beacon.activate', 0.6, 1.8)],
                      8: ['function bm:p72/zb/p/aim'], 16: ['function bm:p72/zb/p/fire', 'function bm:p72/zb/sg/beam'], 22: ['function bm:p72/zb/p/idle0']})

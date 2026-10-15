"""Phase 144 (2.78a): APOPHISS'S FORMS. The follower takes a gem as KillerWatt and Cecil do:

- Right-click him holding the ETHEREAL GEM: the ethereal king - the spectral, green-veined scales of his second phase. His
  blows wither and slow, he mends as he fights (Regeneration, Resistance) and his wake is green motes and reverse portal light.
- Right-click him holding the WRAITHFIRE HEART: his WRAITHFIRE FORM - charred black scales burning soul-blue. His blows set
  foes alight and weaken them, fire can't touch him, and you beside him are spared the flames too.
- Sneak + right-click him empty-handed: the gem (or the heart) comes back out, and his own scales with it.

The form is yours (bm.apel on the owner: 10 ethereal, 11 wraithfire) and stays with him across summons; like the gems in
KillerWatt and Cecil it stays on the side of the Fixer's door it was given on. A form outranks a chosen colour (it is his
whole hide); taking the gem out puts the colour back.

EMMA AND THE WRAITHFIRE HEART: while she holds one (given to her: bm.emwf on you), her support form's blessings come at
level II - whichever form she's in, and whether or not her Wraithfire Form is switched on (that only decides the soul-fire
look and the flying). Importing does nothing; generate(G) runs after phase138."""
from items import T
import apophiss_art as A, rigfol as RF
from apophiss_art import qs

# (his wings, in either form: half-folded along his back as he goes about - clear of a rider and his coils - and thrown wide
#  when he leaps, roars or casts; a slow breath in them as he idles)
WING_HALF = (qs(('y', 38), ('z', -6)), qs(('y', -38), ('z', 6)))
WING = {'idle_b': (qs(('y', 32), ('z', -2)), qs(('y', -32), ('z', 2))), 'crouch': (qs(('y', 14), ('z', 8)), qs(('y', -14), ('z', -8))),
        'roar': (qs(('y', 10), ('z', 14)), qs(('y', -10), ('z', -14))), 'cast': (qs(('y', 14), ('z', 8)), qs(('y', -14), ('z', -8))),
        'cast_point': (qs(('y', 20), ('z', 2)), qs(('y', -20), ('z', -2))), 'swim_a': (qs(('y', 58), ('z', -16)), qs(('y', -58), ('z', 16))),
        'swim_b': (qs(('y', 58), ('z', -16)), qs(('y', -58), ('z', 16))), 'swim_m': (qs(('y', 58), ('z', -16)), qs(('y', -58), ('z', 16))),
        # (2.78c, ridden: spread to fly - and beating, up and down, as he goes)
        'ride': (qs(('y', 18), ('z', 6)), qs(('y', -18), ('z', -6))), 'ride_b': (qs(('y', 12), ('z', 16)), qs(('y', -12), ('z', -16))),
        'ride_c': (qs(('y', 26), ('z', -26)), qs(('y', -26), ('z', 26)))}

GRN, GRN_LT, SOUL, ETH = '#3ad06a', '#c8f0b0', '#5ae8ff', '#7affb0'
FORMS = {10: ('ethereal_gem', 'ETHEREAL FORM', ETH, 'the ethereal king: his blows wither and slow, and he mends as he fights.'),
         11: ('wraithfire_heart', 'WRAITHFIRE FORM', SOUL, 'black scales burning soul-blue: his blows set foes alight, and fire won\'t touch either of you.')}


def generate(G):
    fn, title, tellraw, PREFIX = G.fn, G.title, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    apsay = lambda txt: title('@s', 'actionbar', [T('Apophiss: ', GRN, bold=True), T(txt, GRN_LT)])
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    objs = ['bm.apel', 'bm.apelo', 'bm.apell']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    pet = 'execute as @e[type=minecraft:wolf,tag=bm.appet] if score @s bm.pid = #me bm.pid'
    second = []

    # ---- (as you, clicking him) give him the gem or the heart; sneak + empty hand: take it back
    who = G.FUNCS['p131/who']
    k = next(i for i, l in enumerate(who) if 'bm:p131/use' in l)
    who[k + 1:k + 1] = [f'execute if items entity @s weapon.mainhand {holds(it)} run return run function bm:p144/give_{n}' for n, (it, *_r) in FORMS.items()] + [
        'execute if predicate bm:p20/sneaking unless items entity @s weapon.mainhand * if score @s bm.apel matches 10.. run return run function bm:p144/take']
    give_back = [f'execute if score @s bm.apel matches {n} run loot give @s loot bm:items/{it}' for n, (it, *_r) in FORMS.items()]
    for n, (it, name, col, what) in FORMS.items():
        fn(f'p144/give_{n}', [f'execute if score @s bm.apel matches {n} run return run ' + apsay('I already burn with that one. Greedy, are we?')] + [l for l in give_back if f'matches {n} ' not in l] + [
            'item modify entity @s weapon.mainhand bm:p2/consume_one', f'scoreboard players set @s bm.apel {n}',
            'scoreboard players operation #me bm.pid = @s bm.pid', f'{pet} at @s run function bm:p144/look',
            f'{pet} at @s run function bm:p144/burst_{n}',
            title('@s', 'actionbar', [T('Apophiss takes it in - ', GRN), T(name, col, bold=True), T(': ' + what, 'gray')]),
            tellraw('@s', PREFIX + [T('Apophiss: ', GRN, bold=True), T('"Ahh... THERE it is. I remember this." ', GRN_LT),
                                    T('(Sneak + right-click him empty-handed to take it back out.)', 'dark_gray')])])
    fn('p144/take', give_back + ['scoreboard players set @s bm.apel 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                                 f'{pet} at @s run function bm:p144/look', f'{pet} at @s run particle minecraft:dust{{color:[0.25,0.9,0.4],scale:1.8}} ~ ~3 ~ 1.2 2 1.2 0 60',
                                 apsay('Back in my own scales. Fine. They were always the handsome ones.')])
    fn('p144/burst_10', ['particle minecraft:reverse_portal ~ ~3 ~ 1.4 2.2 1.4 0.1 160', 'particle minecraft:dust{color:[0.48,1.0,0.69],scale:2.2} ~ ~3 ~ 1.4 2.2 1.4 0 80',
                         'particle minecraft:flash{color:[0.48,1.0,0.69,1.0]} ~ ~3 ~ 0 0 0 0 1', 'playsound minecraft:block.beacon.power_select neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                         'playsound minecraft:entity.illusioner.mirror_move neutral @a[distance=..24] ~ ~ ~ 1 0.6'])
    fn('p144/burst_11', ['particle minecraft:soul_fire_flame ~ ~3 ~ 1.2 2.2 1.2 0.08 180', 'particle minecraft:soul ~ ~3 ~ 1.2 2 1.2 0.05 50',
                         'particle minecraft:flash{color:[0.35,0.9,1.0,1.0]} ~ ~3 ~ 0 0 0 0 1', 'playsound minecraft:entity.blaze.shoot neutral @a[distance=..24] ~ ~ ~ 1 0.5',
                         'playsound minecraft:particle.soul_escape neutral @a[distance=..24] ~ ~ ~ 2 0.7'])

    # ---- his look: (as the wolf, at it) his parts. The form comes off, the colour he wears goes on, then the form over it
    fn('p144/look', ['scoreboard players operation #me bm.pid = @s bm.pid',
                     'execute as @e[type=minecraft:item_display,tag=bm.app_pet,tag=!bm.apfade] if score @s bm.pid = #me bm.pid run tag @s add bm.apsel',
                     'function bm:p138/apo/dress', 'tag @e[tag=bm.apsel] remove bm.apsel'])
    dress = G.FUNCS['p138/apo/dress']
    assert dress == ['function bm:p138/k/apo', 'execute as @e[type=minecraft:item_display,tag=bm.apsel] run function bm:p138/sfx'], dress
    G.FUNCS['p138/apo/dress'] = ['execute as @e[type=minecraft:item_display,tag=bm.apsel] run function bm:p144/unform'] + dress + [
        'scoreboard players set #af bm.rng 0', 'execute if entity @s[type=minecraft:player] run scoreboard players operation #af bm.rng = @s bm.apel',
        'execute unless entity @s[type=minecraft:player] on owner run scoreboard players operation #af bm.rng = @s bm.apel',
        'execute if score #af bm.rng matches 10.. as @e[type=minecraft:item_display,tag=bm.apsel] run function bm:p144/form']
    n2 = G.FUNCS['p138/apo/now2']                         # (a colour picked in his wardrobe: through the same door)
    k = next(i for i, l in enumerate(n2) if 'bm:p138/sfx' in l)
    n2[k] = 'function bm:p144/look'
    # (as a part) its model without a form's suffix; then (as a part, #af the form) without the colour's, with the form's
    fn('p144/unform', ['data modify storage bm:wd m set from entity @s item.components."minecraft:item_model"',
                       'data modify storage bm:wd t set string storage bm:wd m -4',
                       'execute if data storage bm:wd {t:"_eth"} run data modify storage bm:wd m set string storage bm:wd m 0 -4',
                       'data modify storage bm:wd t set string storage bm:wd m -3',
                       'execute if data storage bm:wd {t:"_wf"} run data modify storage bm:wd m set string storage bm:wd m 0 -3',
                       'data modify entity @s item.components."minecraft:item_model" set from storage bm:wd m'])
    fn('p144/form', ['data modify storage bm:wd m set from entity @s item.components."minecraft:item_model"',
                     'data modify storage bm:wd t set string storage bm:wd m -3'] +
       [f'execute if data storage bm:wd {{t:"_c{c}"}} run data modify storage bm:wd m set string storage bm:wd m 0 -3' for c in range(1, 5)] +
       ['execute if score #af bm.rng matches 10 run data modify storage bm:wd s set value "_eth"',
        'execute if score #af bm.rng matches 11 run data modify storage bm:wd s set value "_wf"',
        'function bm:p144/form2 with storage bm:wd'])
    fn('p144/form2', ['$data modify entity @s item.components."minecraft:item_model" set value "$(m)$(s)"'])

    # ---- his wings: every pose of his turns them too (they used to be told only "hidden"); the form sets their size
    import phase131 as P131
    wsel = lambda p: f'@e[type=minecraft:item_display,tag=bm.apsel,tag=bm.app_{p}]'
    n = 0
    for name, pz in P131.POSES.items():
        f = f'p131/pose/{name}'
        if name not in P131.DUR_P or f not in G.FUNCS: continue
        wr, wl = WING.get(name, WING_HALF)
        new = RF.pose(A, dict(pz, wingr=wr, wingl=wl), P131.SP, P131.DUR_P[name], wsel, hide=False, parts=('wingr', 'wingl'))
        L = G.FUNCS[f]
        idx = [i for i, l in enumerate(L) if 'tag=bm.app_wing' in l]
        assert len(idx) == 2, (f, idx)
        for i, l in zip(idx, new): L[i] = l
        n += 1
    assert n >= 20, n
    ws = round(P131.SP * A.PART_K['wingr'], 4)
    d = G.FUNCS['p138/apo/dress']
    d.insert(0, 'execute as @e[type=minecraft:item_display,tag=bm.apsel,tag=bm.app_wingr] run data merge entity @s {transformation:{scale:[0f,0f,0f]}}')
    d.insert(0, 'execute as @e[type=minecraft:item_display,tag=bm.apsel,tag=bm.app_wingl] run data merge entity @s {transformation:{scale:[0f,0f,0f]}}')
    d += [f'execute if score #af bm.rng matches 10.. as @e[type=minecraft:item_display,tag=bm.apsel,tag=bm.app_{w}] run data merge entity @s '
          f'{{start_interpolation:0,interpolation_duration:6,transformation:{{scale:[{ws}f,{ws}f,{ws}f]}}}}' for w in ('wingr', 'wingl')]

    # ---- what the forms do: his blows (as the foe struck; the wolf tagged bm.apme2), and every second about him
    fn('p144/hit', ['scoreboard players set #af bm.rng 0',
                    'execute as @e[type=minecraft:wolf,tag=bm.apme2,limit=1] on owner run scoreboard players operation #af bm.rng = @s bm.apel',
                    'execute if score #af bm.rng matches 10 run effect give @s minecraft:wither 4 1',
                    'execute if score #af bm.rng matches 10 run effect give @s minecraft:slowness 3 1',
                    'execute if score #af bm.rng matches 10 run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.05 20',
                    'execute if score #af bm.rng matches 11 run data modify entity @s Fire set value 120s',
                    'execute if score #af bm.rng matches 11 run effect give @s minecraft:weakness 4 0',
                    'execute if score #af bm.rng matches 11 run particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.6 0.3 0.04 20'])
    for name in ('p131/clawed', 'p131/bitten2', 'p131/spat'):
        G.FUNCS[name].append('function bm:p144/hit')
    wh = G.FUNCS['p131/wrath_hit']
    k = next(i for i, l in enumerate(wh) if 'damage @s 24' in l)
    wh.insert(k + 1, wh[k].split(' run damage ')[0] + ' at @s run function bm:p144/hit')
    second.append('execute as @e[type=minecraft:wolf,tag=bm.appet,tag=!bm.ffpet] at @s run function bm:p144/sec')
    fn('p144/sec', ['scoreboard players set #af bm.rng 0', 'execute on owner run scoreboard players operation #af bm.rng = @s bm.apel',
                    'execute if score #af bm.rng matches 10 run effect give @s minecraft:regeneration 3 0 true',
                    'execute if score #af bm.rng matches 10 run effect give @s minecraft:resistance 3 0 true',
                    'execute if score #af bm.rng matches 10 run particle minecraft:dust{color:[0.48,1.0,0.69],scale:1.4} ~ ~2.6 ~ 0.9 1.6 0.9 0 6',
                    'execute if score #af bm.rng matches 10 run particle minecraft:reverse_portal ~ ~1.4 ~ 0.8 1.2 0.8 0.02 6',
                    'execute if score #af bm.rng matches 11 run effect give @s minecraft:fire_resistance 3 0 true',
                    'execute if score #af bm.rng matches 11 on owner if entity @s[distance=..12] run effect give @s minecraft:fire_resistance 3 0 true',
                    'execute if score #af bm.rng matches 11 run particle minecraft:soul_fire_flame ~ ~2.4 ~ 0.8 1.6 0.8 0.02 8',
                    'execute if score #af bm.rng matches 11 run particle minecraft:soul ~ ~1.2 ~ 0.6 0.8 0.6 0.01 1'])

    # ---- the form stays on its side of the Fixer's door (as the gems in KillerWatt and Cecil do: phase126)
    for name, save_to, load_from in (('p126/gem/in', 'o', 'l'), ('p126/gem/out', 'l', 'o')):
        L = G.FUNCS[name]
        k = next(i for i, l in enumerate(L) if l == 'function bm:p126/gem/redress')
        L[k:k] = [f'scoreboard players set @s bm.apel{save_to} 0', f'execute if score @s bm.apel matches 1.. run scoreboard players operation @s bm.apel{save_to} = @s bm.apel',
                  'scoreboard players set @s bm.apel 0', f'execute if score @s bm.apel{load_from} matches 1.. run scoreboard players operation @s bm.apel = @s bm.apel{load_from}']
    G.FUNCS['p126/gem/redress'].append(f'{pet} at @s run function bm:p144/look')

    # ---- (2.78c) ridden in either form, he FLIES: no gravity while he's ridden; look up to climb, down to dive, level to glide;
    #      jump for a hard wingbeat up; a faster cruise. (As Ethereal KillerWatt flies; on foot nothing changes.)
    rd = G.FUNCS['p131/ride']
    rd.insert(0, 'scoreboard players set #af bm.rng 0')
    rd.insert(1, 'execute on owner run scoreboard players operation #af bm.rng = @s bm.apel')
    k = next(i for i, l in enumerate(rd) if 'bm:p131/drive' in l)
    rd[k:k] = ['execute if score #af bm.rng matches 10.. run data modify entity @s NoGravity set value 1b',
               'execute unless score #af bm.rng matches 10.. run data modify entity @s NoGravity set value 0b']
    rd.append('execute if score #af bm.rng matches 10.. run function bm:p144/fly')
    fn('p144/fly', ['execute on passengers store result score #pitch bm.rng run data get entity @s Rotation[1]',
                    'execute if score #pitch bm.rng matches ..-20 run data modify entity @s Motion[1] set value 0.3d',
                    'execute if score #pitch bm.rng matches 35.. run data modify entity @s Motion[1] set value -0.3d',
                    'execute if score #pitch bm.rng matches -19..34 run data modify entity @s Motion[1] set value 0.0d',
                    'execute if score #jp bm.rng matches 1 run data modify entity @s Motion[1] set value 0.55d',
                    'execute if score #jp bm.rng matches 1 if score @s bm.apfn matches ..0 run playsound minecraft:entity.ender_dragon.flap neutral @a[distance=..24] ~ ~ ~ 0.6 1.3',
                    'execute if score #jp bm.rng matches 1 if score @s bm.apfn matches ..0 run scoreboard players set @s bm.apfn 10',
                    'execute if score #af bm.rng matches 10 run particle minecraft:reverse_portal ~ ~2 ~ 1.2 0.4 1.2 0.02 3',
                    'execute if score #af bm.rng matches 11 run particle minecraft:soul_fire_flame ~ ~2 ~ 1.2 0.4 1.2 0.01 2'])
    dr = G.FUNCS['p131/drive']
    assert dr[0] == 'data modify storage bm:tmp kxd.s set value 0.36d', dr[0]
    dr.insert(1, 'execute if score #af bm.rng matches 10.. run data modify storage bm:tmp kxd.s set value 0.55d')
    G.FUNCS['p131/unride'].append('data modify entity @s NoGravity set value 0b')

    # ---- Emma, holding a Wraithfire Heart: every blessing of her support form at level II (as the target; #ewf set by her pulse)
    pu = G.FUNCS['p57/pulse']
    k = next(i for i, l in enumerate(pu) if l.startswith('scoreboard players operation #mode bm.rng'))
    pu[k:k] = ['scoreboard players set #ewf bm.rng 0', 'execute on owner if score @s bm.emwf matches 1 run scoreboard players set #ewf bm.rng 1']
    n = 0
    for name in [f for f in G.FUNCS if f.startswith('p57/buff/')]:
        L = G.FUNCS[name]
        up = [l.replace(' 5 0 true', ' 5 1 true') for l in L if l.startswith('effect give @s minecraft:') and l.endswith(' 5 0 true')]
        k = max(i for i, l in enumerate(L) if l.startswith('effect give')) + 1
        L[k:k] = [f'execute if score #ewf bm.rng matches 1 run {l}' for l in up]
        n += len(up)
    assert n >= 8, n

    s = G.FUNCS['loop/second']
    s[-1:-1] = second

"""2.78: THE FROG WITH MUSTACHE AND DONADO CARRY A TOKEN NOW, like every other follower.

THE FROG WITH MUSTACHE: find his hut in the swamp and hire him (1 Medallion), as before - and he hands you his SIGNET.
  From then on it calls him, anywhere: use it to call him (when he's out: to your side); sneak + use for his menu - sit /
  follow, hand back your gear, send him home (or call him). He keeps the gear you give him: it goes home with him, comes
  back with him, and stays with him when he faints - nothing is left lying where he fell.
DONADO: free him from a mothership's holding pen, as before - and he gives you his COLLAR TAG. The same: use to call,
  sneak + use for his menu; his gear stays with him.
LIKE THE OTHERS: they count toward the three-follower limit (Donado slipped past it), fade when you die (call them again
  with the token), go home when you go far or put the token away, and rest 5 minutes after a faint (the token says how
  long). They live in an item frame, stand as a figurine in a display case, and wait at the coat check on a heist - their
  raid contracts work as before (the vault's own hire, in his own kit).
FROM BEFORE: one already with you hands you his token the next time you're both about. Lost the token? The hut (1
  Medallion) or any mothership's pen (free) gives you another - and he comes back with his gear.
"""
from items import item, T, TOTEM
from useitem import hold, HOLD
import phase68 as P68
import phase134 as P134

FROG_G, DON_C = '#6ac850', '#e8d29a'
CD = 300                                    # seconds a token rests after its follower faints
DROP0 = '{drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f,legs:0f,feet:0f,body:0f}}'
# per kind: the token, the host tag, the wolf's "new" tag, the select tag, his name (start of a sentence / inside one), colour, menu,
# the old cooldown objective, the old "owed a free return" tag, the follow-rule ticket, the refresh (as the wolf, the select tag on him)
KINDS = {'fg': dict(iid='frog_signet', tag='bm.frogpet', new='bm.fp_new', sel='bm.fgsel', Name='The Frog with Mustache', name='the Frog with Mustache',
                    short='the Frog', col=FROG_G, menu=8640, cd='bm.fgcd', owed='bm.fgowed', ticket='bm.fgfg', refresh='p20/frog/refresh',
                    item_name='Signet of the Frog Knight', token='Signet', sound='minecraft:entity.frog.ambient'),
         'dn': dict(iid='donado_tag', tag='bm.donado', new='bm.dn_new', sel='bm.dnsel', Name='Donado', name='Donado', short='Donado', col=DON_C, menu=8650,
                    cd='bm.dncd', owed='bm.dnowed', ticket='bm.dnfg', refresh='p25/don/refresh', item_name="Donado's Collar Tag", token='Collar Tag',
                    sound='minecraft:entity.wolf.ambient')}

item('frog_signet', TOTEM, 'Signet of the Frog Knight', FROG_G,
     ["A tarnished knight's ring, a mustache stamped on its face.", ('Use: call the Frog with Mustache', 'blue'), ("(when he's out: to your side).", 'blue'),
      ('Sneak + use: his menu.', 'gray'), ('He keeps the gear you give him.', 'dark_gray')],
     model='bm:frog_signet', stack=1, cat='magic', comps=hold('none'))
HOLD['frog_signet'] = 'bm:p136/fg/use'
item('donado_tag', TOTEM, "Donado's Collar Tag", DON_C,
     ['A bent tin tag: SPECIMEN 042, scratched out -', '"DONADO" written over it in crayon.', ('Use: call Donado', 'blue'), ("(when he's out: to your side).", 'blue'),
      ('Sneak + use: his menu.', 'gray'), ('He keeps the gear you give him.', 'dark_gray')],
     model='bm:donado_tag', stack=1, cat='magic', comps=hold('none'))
HOLD['donado_tag'] = 'bm:p136/dn/use'

# they live in item frames too (the frame's follower is nobody's: no gear, no rules)
_n = max(v[0] for v in P68.KINDS.values()) + 1
P68.KINDS['frog'] = (_n, 'frog_signet', 'wolf', 'bm.frogpet', 'p136/fg/fspawn', 'p136/fg/dismiss', 'bm.fgsel', 'The Frog with Mustache', FROG_G)
P68.KINDS['donado'] = (_n + 1, 'donado_tag', 'wolf', 'bm.donado', 'p136/dn/fspawn', 'p136/dn/dismiss', 'bm.dnsel', 'Donado', DON_C)
P68.HE.update({'frog', 'donado'})

# and stand as figurines in a display case (their jointed rigs, at rest)
_figures0 = P134.figures


def _figures():
    F_ = _figures0()
    from phase63 import don_rig, don_poses, frog_rig, frog_poses
    for iid, name, rig, poses, m in (('frog_signet', 'The Frog with Mustache', frog_rig(), frog_poses(), 'frr'), ('donado_tag', 'Donado', don_rig(), don_poses(), 'dnr')):
        sol = rig.solve(poses['idle0'])
        F_[iid] = (name, [(f'bm:{m}_{n}' if n != 'head' else f'bm:{m}_head_none', tuple(J), tuple(R), P134.IDENT, rig.S) for n, (R, J) in sol.items()])
    return F_


P134.figures = _figures
P134.FIT['frog_signet'] = (-0.850, 0.596, -0.325, 0.325, -0.255, 0.260)      # (measured: phase134.measure)
P134.FIT['donado_tag'] = (-0.850, 1.016, -0.307, 0.308, -0.289, 0.255)


def generate(G):
    import phase28 as P28
    import phase73 as P73
    fn, title, tellraw, give, PREFIX = G.fn, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    second, mig = [], []
    objs = [k['ticket'] for k in KINDS.values()]
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    in_heist = 'execute if entity @s[tag=bm.gvp] if dimension bm:gutter'
    home = 'tag=!bm.fvault,tag=!bm.ffpet'          # (his own: not the vault's hire, not a frame's)

    # (as a wolf of ours) his gear, saved under his owner's id - and loaded back the same way

    for k, K in KINDS.items():
        tag, new, sel, col, menu, iid = K['tag'], K['new'], K['sel'], K['col'], K['menu'], K['iid']
        hsay = lambda txt: title('@s', 'actionbar', T(txt, col))
        mine = f'execute as @e[type=minecraft:wolf,tag={tag},{home}] if score @s bm.pid = #me bm.pid run tag @s add {sel}'
        has_token = [f'execute if items entity @s container.* {holds(iid)} run return 1', f'execute if items entity @s weapon.offhand {holds(iid)} run return 1',
                     f'execute if items entity @s player.cursor {holds(iid)} run return 1', 'return 0']
        fn(f'p136/{k}/has', has_token)
        fn(f'p136/{k}/key', ['execute unless score @s bm.pid matches 1.. run return fail', 'execute store result storage bm:fol key int 1 run scoreboard players get @s bm.pid',
                             'return 1'])
        fn(f'p136/{k}/save_m', [f'$data remove storage bm:fol {k}.p$(key)', f'$data modify storage bm:fol {k}.p$(key) set from entity @s equipment'])
        fn(f'p136/{k}/load_m', [f'$data modify entity @s equipment set from storage bm:fol {k}.p$(key)'])
        fn(f'p136/{k}/save', [f'execute if function bm:p136/{k}/key run function bm:p136/{k}/save_m with storage bm:fol'])

        # ---- the token: call him (or to your side); sneak + use for his menu
        fn(f'p136/{k}/use', [f'{in_heist} run return run ' + say("In the vault your crew answers the Fixer's Ledger - Raid Crew.", '#9ad0ff'),
                             'execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                             'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid', mine,
                             'scoreboard players set #am bm.rng 0',
                             'execute if predicate bm:p20/sneaking run scoreboard players set #am bm.rng 2',
                             f'execute if score #am bm.rng matches 0 if entity @e[type=minecraft:wolf,tag={sel}] run scoreboard players set #am bm.rng 4',
                             f'execute if score #am bm.rng matches 2 run function bm:p136/{k}/menu', f'execute if score #am bm.rng matches 4 run function bm:p136/{k}/recall',
                             f'execute if score #am bm.rng matches 0 run function bm:p136/{k}/try',
                             f'tag @e[tag={sel}] remove {sel}'])
        fn(f'p136/{k}/recall', [f'tp @e[type=minecraft:wolf,tag={sel},limit=1] @s', f'data modify entity @e[type=minecraft:wolf,tag={sel},limit=1] Sitting set value 0b',
                                'particle minecraft:happy_villager ~ ~0.6 ~ 0.4 0.4 0.4 0 8', f'playsound {K["sound"]} neutral @a[distance=..16] ~ ~ ~ 1 1.2',
                                hsay({'fg': '"Ribbit. At your side, as sworn."', 'dn': '*happy bark* Donado bounds to your side.'}[k])])
        mins = [f'execute store result score #m bm.rng run scoreboard players get @s {K["cd"]}', 'scoreboard players add #m bm.rng 59', 'scoreboard players operation #m bm.rng /= #60 bm.rng']
        fn(f'p136/{k}/rest', mins + [title('@s', 'actionbar', [T(f'{K["Name"]} is still {"recovering" if k == "fg" else "licking his wounds"}: about ', 'gray'),
                                                                {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')])])
        fn(f'p136/{k}/try', [f'execute if score @s {K["cd"]} matches 1.. run return run function bm:p136/{k}/rest',
                             'execute unless function bm:p74/fol_ok run return run ' + say(f"{K['Name']} won't come here."),
                             'execute if function bm:p58/full run return 0',
                             f'function bm:p136/{k}/summon'])
        fn(f'p136/{k}/summon', [f'execute positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p136/{k}/here',
                                f'execute positioned ^ ^1 ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p136/{k}/here',
                                f'function bm:p136/{k}/here'])
        # (his own summon, without the big "joins you!" titles; a player's call loads his gear, a frame's doesn't)
        src = G.FUNCS['p20/frog/summon' if k == 'fg' else 'p25/don/summon']
        body = [l for l in src if not l.startswith(('title ', 'tellraw '))]
        jb = next(i for i, l in enumerate(body) if l.endswith(f'remove {new}'))
        stamp = f'scoreboard players operation @e[tag={new},distance=..3] bm.pid = @s bm.pid'
        fn(f'p136/{k}/here', body[:jb] + [stamp, f'execute as @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] run function bm:p136/{k}/dress'] + body[jb:] +
           [hsay({'fg': '"Ribbit! Sir Frog, reporting for duty."', 'dn': '*excited barking* Donado is here!'}[k])])
        fn(f'p136/{k}/fspawn', body[:jb] + [stamp] + body[jb:])
        fn(f'p136/{k}/dress', [f'data merge entity @s {DROP0}', 'tag @s add bm.f136',
                               f'execute if function bm:p136/{k}/key run function bm:p136/{k}/load_m with storage bm:fol',
                               f'tag @s add bm.fsel', f'function bm:{K["refresh"]}', 'tag @s remove bm.fsel'])
        # ---- going: home, his gear saved with him (nothing drops); fading with the token's owner; a frame letting go
        fn(f'p136/{k}/away', [f'execute if entity @s[tag=bm.f136,{home},tag=!bm.fnosave] run function bm:p136/{k}/save', f'data merge entity @s {DROP0}',
                              'particle minecraft:poof ~ ~0.5 ~ 0.3 0.4 0.3 0.02 14', 'particle minecraft:happy_villager ~ ~0.6 ~ 0.4 0.4 0.4 0 6',
                              'execute on passengers run kill @s[type=!minecraft:player]', 'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
        fn(f'p136/{k}/dismiss', [f'execute as @e[type=minecraft:wolf,tag={sel}] at @s run function bm:p136/{k}/away'])
        fn(f'p136/{k}/home', [f'function bm:p136/{k}/dismiss',
                              hsay({'fg': '"Until you call, friend." The Frog with Mustache hops home.', 'dn': 'Donado trots home, tail wagging. (Use his tag to call him.)'}[k])])
        fn(f'p136/{k}/go', ['scoreboard players add #gone bm.rng 1', f'function bm:p136/{k}/away'])
        # (a stale one - called again elsewhere while his chunk slept - or one whose owner is offline: he goes without saving, so his
        #  old gear never overwrites the record the current one keeps; the record is already up to date from the last second he was ours)
        fn(f'p136/{k}/gone_nosave', ['tag @s add bm.fnosave', f'function bm:p136/{k}/away'])
        G.FUNCS['p62/died'].insert(-1, f'execute as @e[type=minecraft:wolf,tag={tag},tag=bm.f136,{home}] if score @s bm.pid = #me bm.pid at @s run function bm:p136/{k}/go')
        # (handing him gear, or taking it back: saved at once - a faint a moment later can't lose it)
        G.FUNCS['p20/frog/msg_give'].append(f'execute if entity @s[tag={tag},tag=bm.f136,{home}] run function bm:p136/{k}/save')
        G.FUNCS['p20/frog/msg_strip'].append(f'execute if entity @s[tag={tag},tag=bm.f136,{home}] run function bm:p136/{k}/save')
        # ...and every second while he's out - in his follow rule below, once he's known to be the current one

        # ---- his menu
        desc = {'fg': [T('The Frog with Mustache', col, bold=True), T(' - a frog knight of the old swamp code. Slow to anger, quick with a blade; ', 'gray'),
                       T('he fights what you fight.', 'white')],
                'dn': [T('Donado', col, bold=True), T(' - a scrappy Earth-dog in a patched grey shirt, rescued from the Donadians. Loyal to the bone; ', 'gray'),
                       T('he fights what you fight.', 'white')]}[k]
        tip = [T('Hand him a weapon or armour (right-click him holding it) and he wears it - and keeps it, home and back. ', 'gray'),
               T('Feed him meat to heal him.', 'gray')]
        dlg = lambda out: P28.multi([T(K['item_name'], col, bold=True)], [P28.body(desc), P28.body(tip, 300)],
                                    ([P28.btn(T('Sit / follow', 'white', bold=True), menu + 1, width=150), P28.btn(T('Hand back my gear', 'white'), menu + 2, width=150),
                                      P28.btn(T('Send him home', 'gray'), menu + 9, width=150)] if out else
                                     [P28.btn(T(f'Call for {K["short"]}', col, bold=True), menu + 8, width=150)]), columns=2, exit_label='Close')
        fn(f'p136/{k}/menu', [f'scoreboard players set @s bm.menu {menu}', 'scoreboard players set #out bm.rng 0',
                              f'execute if entity @e[type=minecraft:wolf,tag={sel}] run scoreboard players set #out bm.rng 1',
                              f'execute if score #out bm.rng matches 1 run return run dialog show @s {P28.inline(dlg(True))}', f'dialog show @s {P28.inline(dlg(False))}'])
        G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {menu + n} run return run function bm:p136/{k}/act' for n in (1, 2, 8, 9)]
        fn(f'p136/{k}/act', [f'execute unless score @s bm.menu matches {menu} run return run function bm:p28/stale', 'scoreboard players set @s bm.menu 0',
                             'scoreboard players operation #me bm.pid = @s bm.pid', mine,
                             f'execute if score #act bm.pay matches {menu + 8} unless entity @e[type=minecraft:wolf,tag={sel}] run function bm:p136/{k}/try',
                             f'execute if score #act bm.pay matches {menu + 8} if entity @e[type=minecraft:wolf,tag={sel}] run function bm:p136/{k}/recall',
                             f'execute if score #act bm.pay matches {menu + 1} if entity @e[type=minecraft:wolf,tag={sel}] run function bm:p136/{k}/sit',
                             f'execute if score #act bm.pay matches {menu + 2} if entity @e[type=minecraft:wolf,tag={sel}] run function bm:p136/{k}/strip',
                             f'execute if score #act bm.pay matches {menu + 9} if entity @e[type=minecraft:wolf,tag={sel}] run function bm:p136/{k}/home',
                             f'tag @e[tag={sel}] remove {sel}'])
        w = f'@e[type=minecraft:wolf,tag={sel},limit=1]'
        fn(f'p136/{k}/sit', [f'execute store success score #s0 bm.rng if data entity {w} {{Sitting:1b}}',
                             f'execute if score #s0 bm.rng matches 1 run data modify entity {w} Sitting set value 0b',
                             f'execute if score #s0 bm.rng matches 0 run data modify entity {w} Sitting set value 1b',
                             'execute if score #s0 bm.rng matches 1 run ' + hsay({'fg': '"Onward!"', 'dn': 'Donado springs up, ready to go.'}[k]),
                             'execute if score #s0 bm.rng matches 0 run ' + hsay({'fg': '"I shall hold this ground."', 'dn': 'Donado sits. Good boy.'}[k])])
        # (the old "sneak + right-click him" strip, from the menu: his gear at your feet)
        fn(f'p136/{k}/strip', ['tag @s add bm.giver', f'tag {w} add bm.fsel', 'function bm:p20/frog/strip', 'tag @e[tag=bm.fsel] remove bm.fsel', 'tag @s remove bm.giver'])

        # ---- fainting: the token rests 5 minutes (no walk back to the hut / the cell any more); his gear stays with him
        G.FUNCS[f'p65/fainted_{k}'] = [f'scoreboard players set @s {K["cd"]} {CD}',
                                       tellraw('@s', PREFIX + [T(f'{K["Name"]} faints! ', col, bold=True),
                                                               T(f'His {K["token"]} needs {CD // 60} minutes before he can come back. His gear is safe with him.', 'gray')])]

        # ---- one from before, already with you: he hands you his token (once you're both about) and keeps his gear from now on
        mig.append(f'execute as @e[type=minecraft:wolf,tag={tag},tag=!bm.f136,{home}] at @s run function bm:p136/{k}/old')
        # (owed a free walk back from before: the token, at once)
        mig.append(f'execute as @a[tag={K["owed"]}] at @s run function bm:p136/{k}/owed_retire')
        fn(f'p136/{k}/owed_retire', [f'tag @s remove {K["owed"]}', f'execute unless function bm:p136/{k}/has run function bm:p136/{k}/gift'])
        G.FUNCS.pop({'fg': 'p65/frog_rest', 'dn': 'p65/don_rest'}[k], None); G.FUNCS.pop({'fg': 'p65/frog_back', 'dn': 'p65/don_back'}[k], None)
        fn(f'p136/{k}/old', ['execute unless score @s bm.pid matches 1.. run return 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                             'tag @a[tag=bm.f136o] remove bm.f136o', 'execute as @a if score @s bm.pid = #me bm.pid run tag @s add bm.f136o',
                             'execute unless entity @a[tag=bm.f136o] run return 0',
                             f'execute as @e[type=minecraft:wolf,tag={tag},tag=bm.f136,{home}] if score @s bm.pid = #me bm.pid run tag @s add bm.f136n',
                             f'execute if entity @e[type=minecraft:wolf,tag=bm.f136n] run return run function bm:p136/{k}/old_dup',
                             f'data merge entity @s {DROP0}', 'tag @s add bm.f136',
                             f'execute as @a[tag=bm.f136o,limit=1] at @s unless function bm:p136/{k}/has run function bm:p136/{k}/gift',
                             'tag @a[tag=bm.f136o] remove bm.f136o'])
        drop = []
        for sl in ('mainhand', 'offhand', 'head', 'chest', 'legs', 'feet', 'body'):
            drop += [f'execute if data entity @s equipment.{sl} run summon minecraft:item ~ ~0.4 ~ {{Item:{{id:"minecraft:stick",count:1}},Tags:["bm.f136d"],PickupDelay:10s}}',
                     f'execute if data entity @s equipment.{sl} run data modify entity @e[type=minecraft:item,tag=bm.f136d,limit=1] Item set from entity @s equipment.{sl}',
                     'tag @e[type=minecraft:item,tag=bm.f136d] remove bm.f136d']
        fn(f'p136/{k}/old_dup', ['tag @e[type=minecraft:wolf,tag=bm.f136n] remove bm.f136n'] + drop + ['data remove entity @s equipment',
                                 tellraw('@a[tag=bm.f136o]', PREFIX + [T(f'{K["Name"]} from before turned up - but you\'ve called him anew since. ', col),
                                                                      T('He left the gear he wore where he stood and went home.', 'gray')]),
                                 'tag @a[tag=bm.f136o] remove bm.f136o', f'function bm:p136/{k}/gone_nosave'])
        fn(f'p136/{k}/gift', [give(iid), f'playsound {K["sound"]} neutral @s ~ ~ ~ 1 1.2',
                              tellraw('@s', PREFIX + [T(f'{K["Name"]} hands you his {K["token"]}. ', col, bold=True),
                                                      T('Use it to call him from now on - anywhere; sneak + use for his menu. ', 'gray'),
                                                      T('He keeps the gear you give him.', 'dark_gray')])])

        # ---- the follower rules every called follower keeps (home when you go far, or put the token away)
        P73.follow_rules(G, (k, 'wolf', tag, iid, f'p136/{k}/go', K['Name'], K['ticket'], f'p136/{k}/here'), second)
        old_line = f'execute as @e[type=minecraft:wolf,tag={tag},tag=!bm.ffpet] at @s run function bm:p73/fol/{k}'
        jj = second.index(old_line)
        second[jj] = f'execute as @e[type=minecraft:wolf,tag={tag},tag=bm.f136,{home}] at @s run function bm:p73/fol/{k}'
        L = G.FUNCS[f'p73/fol/{k}']
        jo = L.index(f'execute unless entity @a[tag=bm.fown] run return run function bm:p136/{k}/go')
        L[jo] = f'execute unless entity @a[tag=bm.fown] run return run function bm:p136/{k}/gone_nosave'
        jt = L.index(f'execute unless score @s {K["ticket"]} = @a[tag=bm.fown,limit=1] {K["ticket"]} run return run function bm:p136/{k}/go')
        L[jt] = f'execute unless score @s {K["ticket"]} = @a[tag=bm.fown,limit=1] {K["ticket"]} run return run function bm:p136/{k}/gone_nosave'
        L.insert(jt + 1, f'function bm:p136/{k}/save')
        jl = next(i for i, l in enumerate(L) if ' if items entity ' in l)
        L.insert(jl, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0')

    # ================================================================== the hut and the pen hand you the token
    sig, dtag = holds('frog_signet'), holds('donado_tag')
    G.FUNCS['p20/frog/hire'] = [
        'tag @s add bm.giver', 'tag @e[type=minecraft:wolf,tag=bm.fmine] remove bm.fmine',
        f'execute as @e[type=minecraft:wolf,tag=bm.frogpet,{home}] if function bm:p20/frog/is_givers run tag @s add bm.fmine',
        'execute if entity @e[type=minecraft:wolf,tag=bm.fmine] run return run function bm:p20/frog/recall',
        'execute if function bm:p136/fg/has run return run ' + title('@s', 'actionbar', [T('"Already sworn to you, friend." ', FROG_G),
                                                                                       T('Use his Signet to call him. (Sneak + use: his menu.)', 'gray')]),
        'execute store result score #paid bm.rng run clear @s *[minecraft:custom_data~{bm:"medallion"}] 1',
        'execute if score #paid bm.rng matches 0 run return run function bm:p20/frog/broke',
        'function bm:p136/fg/sworn']
    fn('p136/fg/sworn', [give('frog_signet'), 'scoreboard players operation #me bm.pid = @s bm.pid',
                         'playsound minecraft:entity.frog.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.2', 'playsound minecraft:item.armor.equip_chain neutral @a[distance=..16] ~ ~ ~ 1 1',
                         'title @s times 10 60 15', title('@s', 'subtitle', T('He hands you his Signet - use it to call him, anywhere', 'gray', italic=True)),
                         title('@s', 'title', T('The Frog with Mustache swears to you!', FROG_G, bold=True)),
                         tellraw('@s', PREFIX + [T('The Frog with Mustache gives you his Signet. ', FROG_G),
                                                 T('Use it to call him (or to your side); sneak + use for his menu. Right-click him holding a weapon or armour to equip it - '
                                                   'he keeps it, home and back. Feed him meat to heal him.', 'gray')]),
                         'execute if score @s bm.fgcd matches 1.. run return run function bm:p136/fg/rest',
                         'execute if function bm:p58/full run return run ' + say('(Send a follower home, then use his Signet to call him.)'),
                         'function bm:p136/fg/summon'])
    G.FUNCS['p25/don/hire'] = [
        'tag @s add bm.giver', 'tag @e[type=minecraft:wolf,tag=bm.dmine] remove bm.dmine',
        f'execute as @e[type=minecraft:wolf,tag=bm.donado,{home}] if function bm:p20/frog/is_givers run tag @s add bm.dmine',
        'execute if entity @e[type=minecraft:wolf,tag=bm.dmine] run return run function bm:p25/don/recall',
        'execute if function bm:p136/dn/has run return run ' + title('@s', 'actionbar', [T('Donado is yours already. ', DON_C),
                                                                                       T('Use his Collar Tag to call him. (Sneak + use: his menu.)', 'gray')]),
        'execute as @e[type=minecraft:item_display,tag=bm.don_pen,sort=nearest,limit=1] if score @s bm.dng matches 1.. run return run ' +
        title('@a[tag=bm.giver]', 'actionbar', T('The cell is empty - Donado already escaped with someone. (He is back in a few minutes.)', 'gray')),
        'function bm:p136/dn/freed',
        'execute as @e[type=minecraft:item_display,tag=bm.don_pen,sort=nearest,limit=1] at @s run function bm:p25/don/pen_empty']
    fn('p136/dn/freed', ['function bm:p136/dn/sworn'])
    fn('p136/dn/sworn', [give('donado_tag'), 'scoreboard players operation #me bm.pid = @s bm.pid',
                         'playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.3',
                         'title @s times 10 60 15', title('@s', 'subtitle', T("He gives you his Collar Tag - use it to call him, anywhere", 'gray', italic=True)),
                         title('@s', 'title', T('Donado is free!', DON_C, bold=True)),
                         tellraw('@s', PREFIX + [T('Donado gives you his Collar Tag. ', DON_C),
                                                 T('Use it to call him (or to your side); sneak + use for his menu. Right-click him holding a weapon or armour to equip it - '
                                                   'he keeps it, home and back. Feed him meat to heal him.', 'gray')]),
                         'execute if score @s bm.dncd matches 1.. run return run function bm:p136/dn/rest',
                         'execute if function bm:p58/full run return run ' + say('(Send a follower home, then use his Collar Tag to call him.)'),
                         'execute at @e[type=minecraft:item_display,tag=bm.don_pen,sort=nearest,limit=1] run function bm:p136/dn/here'])

    # ---- Donado counts toward the three-follower limit (he slipped past it)
    G.FUNCS['p58/count'][-1:-1] = ['execute as @e[type=minecraft:wolf,tag=bm.donado] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1']

    # ---- the heist handover for the followers that came after phase103's: "waits outside the vault" going in, back with you
    #      three seconds after you're home again (it covered seven; Apophiss, Tullius, Pearlman and these two just went home)
    import phase131 as P131, phase132 as P132, phase128 as P128
    late = [('apo', 'p131/go', 'Apophiss', P131.GRN, 'p131/try_summon'), ('tul', 'p132/go', 'Tullius', P132.ICE, 'p132/try_summon'),
            ('pearl', 'p128/pm/go', 'Pearlman', P128.PEARL, 'p128/pm/try'),
            ('fg', 'p136/fg/go', KINDS['fg']['Name'], FROG_G, 'p136/fg/try'), ('dn', 'p136/dn/go', 'Donado', DON_C, 'p136/dn/try')]
    for kind, go, nm, col, try_ in late:
        far = G.FUNCS[f'p73/fol/{kind}_far']
        assert far[0] == f'function bm:{go}', (kind, far[0])
        far.insert(0, f'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run function bm:p103/fol/wait_{kind}')
        fn(f'p103/fol/wait_{kind}', [f'tag @a[tag=bm.fown] add bm.ow_{kind}', f'function bm:{go}',
                                     tellraw('@a[tag=bm.fown]', PREFIX + [T(f'{nm} waits outside the vault', col), T(' - your Raid Crew answers inside. ', 'gray'),
                                                                          T('(Back with you when you\'re home.)', 'dark_gray')]),
                                     'tag @a remove bm.fown'])
        fn(f'p103/fol/back_{kind}', [f'tag @s remove bm.ow_{kind}', f'function bm:{try_}'])
        G.FUNCS['p103/fol/tick'].append(f'execute if entity @s[tag=bm.ow_{kind}] run function bm:p103/fol/back_{kind}')

    fn('admin/frog_donado_tokens', [give('frog_signet'), give('donado_tag')])
    G.FUNCS.pop('p20/frog/summon', None)          # (his old summon: copied above, and the vault keeps its own copy - nothing calls it now)
    G.FUNCS['loop/second'][-1:-1] = mig + second


# ===================================================================== resource pack: the two tokens
def _signet(R):
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2, 5, 13, 15), outline=hexc('#8a7a3a'), width=2)                        # the band
    d.arc((2, 5, 13, 15), 200, 330, fill=hexc('#d8c070'))
    d.rectangle((4, 1, 11, 7), fill=hexc('#3e8a32'), outline=hexc('#244e1c'))            # the face, frog-green
    for x, y in ((5, 4), (6, 5), (7, 5), (8, 5), (9, 5), (10, 4)):                       # a mustache stamped on it
        im.putpixel((x, y), hexc('#141a10'))
    im.putpixel((6, 2), hexc('#a8f090')); im.putpixel((9, 2), hexc('#a8f090'))          # (a glint on each eye)
    return im


def _tag(R):
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((7, 0, 7, 3), fill=hexc('#8a8a8a')); d.ellipse((5, 2, 9, 5), outline=hexc('#b0b0b0'))     # the ring
    d.rounded_rectangle((2, 5, 13, 14), 3, fill=hexc('#c8ccd0'), outline=hexc('#70767c'))            # bent tin
    d.line((4, 8, 11, 8), fill=hexc('#80868c'))                                                         # "SPECIMEN 042", scratched out
    d.line((4, 7, 11, 9), fill=hexc('#5a6066'))
    for x in range(4, 12, 2): im.putpixel((x, 11), hexc('#e05a3a'))                                     # "DONADO" in red crayon
    for x in range(5, 12, 2): im.putpixel((x, 12), hexc('#e05a3a'))
    return im


def rp(R):
    R.ICONS['frog_signet'] = _signet(R)
    R.ICONS['donado_tag'] = _tag(R)

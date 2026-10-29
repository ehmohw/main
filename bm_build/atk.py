"""2.94u: THE ATTACK KIT - what makes Bender's Rage feel good, given to every follower who fights.

IMPACT   every blow a follower lands (each `damage @s ... by <the follower>` line, found in the built functions) gets the same clean
         finish at the struck foe: a small burst of crits and a puff in the follower's own colour, and a strike sound.
HIT-STOP the follower's animation holds for two ticks on the blow (its pose clock is held too, so no frame is skipped): the strike
         pose lands and stays a beat before the recovery - the "weight" of a hit.
DASH     (dash(), used by phase222) the follower carried to its foe a step a tick in a short arc - launch puff, a trail in its
         colour, a landing - in place of the old one-tick teleports onto a target."""
import re

# the "by" tag each follower's blows carry -> (follower, its animation function or None)
ME = {'bm.kxme': ('kw', None), 'bm.cpme': ('cecil', 'p46/pet/anim'), 'bm.emme': ('emma', 'p57/anim'), 'bm.dmme': ('demo', 'p97/anim'),
      'bm.apme2': ('apo', 'p131/anim'), 'bm.leme': ('leo', 'p96/anim'), 'bm.zbme': ('zib', 'p72/zb/anim'), 'bm.ceme': ('celi', 'p66/anim'),
      'bm.ybme': ('sky', 'p211/anim'), 'bm.xmme': ('pxemma', 'p213e/anim'), 'bm.xlme': ('pxleo', 'p213l/anim'), 'bm.xcme': ('pxcecil', 'p213c/anim'),
      'bm.tume2': ('tul', 'p132/anim'), 'bm.svme': ('stalker', 'p193/anim'), 'bm.pqme': ('pearlq', 'p190/anim'), 'bm.pime': ('pistachio', 'p163/pi/anim'),
      'bm.ompme': ('omega', 'p170/anim'), 'bm.nbme': ('neighbor', 'p187/anim'), 'bm.mzme': ('capshun', 'p198/anim'), 'bm.ktme': ('kettle', 'p227/anim'), 'bm.rume': ('rufus', 'p228/anim'), 'bm.hyme': ('henry', 'p229/anim'), 'bm.nime': ('nia', 'p230/anim'), 'bm.cgme': ('gem', 'p231/anim'), 'bm.ytme': ('batty', 'p232b/anim'), 'bm.ebme': ('eggbert', 'p232e/anim'), 'bm.knme': ('count', 'p232c/anim'), 'bm.ddme': ('dragon', 'p235d/anim'), 'bm.ezme': ('eraser', 'p235e/anim'), 'bm.uxme': ('cursor', 'p235c/anim'), 'bm.ibme': ('inkblot', 'p235i/anim'), 'bm.wbme': ('speech', 'p235b/anim'), 'bm.lhme': ('lightbringer', 'p236l/anim'), 'bm.pyme': ('dryad', 'p236p/anim'), 'bm.xvme': ('sovereign', 'p239/anim'), 'bm.xbme': ('vexis', 'p243/anim'), 'bm.mlme': ('mireling', 'p252/anim'), 'bm.lnme': ('lantern', 'p194/anim'),
      'bm.kkme': ('chef', 'p186/anim'), 'bm.fyme': ('fishy', 'p145/anim'), 'bm.dwme': ('dennis', 'p163/dw/anim'), 'bm.bvme': ('bender', 'p195/anim'),
      'bm.bome': ('bloo', 'p191/anim'), 'bm.bjme': ('bones', 'p196/anim'), 'bm.avme': ('ava', 'p189/anim'), 'bm.aspme': ('ashur', 'p185/anim')}
HOLD = 2                                     # (ticks of hit-stop)
DMG = re.compile(r'^(\$?)(.*?)damage @s (\S+) (\S+) by @e\[type=minecraft:(wolf|cat),tag=(bm\.[a-z0-9]+)')


def rgb(col):
    return ','.join(f'{int(col[i:i + 2], 16) / 255:.2f}' for i in (1, 3, 5))


# (2.94u) ALTERNATE SWINGS: a follower's ordinary blow (its melee state, 7) swung one of two ways, at random each time - the second
# made from its own approved poses (a wind-up from another of its moves into the strike), on the same frames, so the hit lands as before
ALT = {'p132': {'thrust_back': 'throw_back'},                       # Tullius: an overhand thrust
       'p145': {'strike_back': 'thunder_up'},                       # Fishy: a downward strike
       'p163/dw': {'swing_back': 'slam_up', 'swing': 'slam'},       # Dennis: the overhead
       'p163/pi': {'slap_back': 'serve'},                           # Pistachio: the backhand
       'p170': {'claw_up': 'flame_up', 'claw': 'flame_swing'},      # King Omega: the sweep
       'p186': {'whack_up': 'throw_back'},                          # the Chef: from behind the shoulder
       'p187': {'strike_up': 'crescendo'},                          # the Neighbor: the big downbeat
       'p189': {'cast_up': 'ward_a'},                               # Queen Ava
       'p190': {'flick_up': 'twirl'},                               # Queen Pearl: a twirl into the flick
       'p191': {'swipe_up': 'crouch'},                              # Bloo: up from a crouch
       'p193': {'rend_up': 'fold'},                                 # the Stalker: unfolding into it
       'p194': {'lash_a': 'lash_b'},                                # the Arachno-Lantern: the other leg
       'p196': {'bite_open': 'thrash_a'},                           # Bones
       'p198': {'swipe_up': 'toss_up'},                             # Mr. Capshun
       'p96': {'thrust_back': 'throw_back'},                        # Leo: an overhand thrust
       'p66': {'stab_back': 'throw_back'},                          # Celi: an overhand stab
       'p97': {'swing_back': 'overhead', 'swing': 'slam'},          # Democratus: the overhead
       'p131': {'claw_up': 'battle', 'claw': 'bite'},               # Apophiss: a bite
       'p57': {'strike_up': 'cast'},                                # Emma
       'p185': {'cast_back': 'crouch'}}                             # Ashur: up from a crouch


def alternates(G):
    """(late, before finalize) the alternate swings: returns how many"""
    if 'bm.kalt' not in G.OBJECTIVES:
        G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.kalt dummy']; G.OBJECTIVES.append('bm.kalt')
    n = 0
    for pfx, alt in ALT.items():
        A = G.FUNCS[f'{pfx}/anim/7']
        assert A[0].startswith('scoreboard players operation #f bm.rng = '), (pfx, A[0])
        out = [A[0], 'execute if score #f bm.rng matches 0 store result score @s bm.kalt run random value 0..1']
        for l in A[1:]:
            hit = [(a, b) for a, b in alt.items() if l.endswith(f'run function bm:{pfx}/pose/{a}')]
            if not hit: out.append(l); continue
            a, b = hit[0]
            assert f'{pfx}/pose/{b}' in G.FUNCS, (pfx, b)
            out += [l.replace('execute if ', 'execute unless score @s bm.kalt matches 1 if ', 1),
                    l.replace('execute if ', 'execute if score @s bm.kalt matches 1 if ', 1)[:-len(a)] + b]
        assert len(out) > len(A) + 1, pfx
        G.FUNCS[f'{pfx}/anim/7'] = out; n += 1
    return n


# (2.94u) the followers who fight with their own (vanilla) bite - the Frog with Mustache, Donado, Wilfrey: no blow function to hook,
# so a monster just hurt (HurtTime 9: once a hit, whichever ticks first) near one asks who hit it (on attacker) - and the impact plays where it was struck
BITERS = {'bm.frogpet': '#6ac850', 'bm.donado': '#e8d29a', 'bm.wilfrey': '#f4f4f4'}


def biters(G):
    fn = G.fn
    for tag, col in BITERS.items():
        r, g, b = (int(col[i:i + 2], 16) / 255 for i in (1, 3, 5))
        k = tag[3:]
        fn(f'atk/bite/{k}', ['particle minecraft:crit ~ ~1.0 ~ 0.25 0.3 0.25 0.3 6',
                             f'particle minecraft:dust{{color:[{r:.2f},{g:.2f},{b:.2f}],scale:1.1}} ~ ~1 ~ 0.3 0.35 0.3 0 6',
                             'playsound minecraft:entity.player.attack.strong neutral @a[distance=..16] ~ ~ ~ 0.45 1.15'])
        G.FUNCS['tick'].append(f'execute as @e[type=minecraft:wolf,tag={tag}] at @s as @e[type=#bm:hostile,distance=..4] if data entity @s {{HurtTime:9s}} '
                               f'at @s on attacker if entity @s[tag={tag}] run function bm:atk/bite/{k}')   # (at the one struck)
    return len(BITERS)


def finalize(G):
    """(late) the impact and the hit-stop on every follower blow"""
    import phase125 as P125
    fn = G.fn
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.khs dummy']
    G.OBJECTIVES.append('bm.khs')
    for tag, (w, anim) in ME.items():
        col = P125.WHO[w][2]
        host = tag.replace('me2', 'pet').replace('me', 'pet')
        fn(f'atk/fx/{tag[3:]}', [f'particle minecraft:crit ~ ~{1.0:.1f} ~ 0.25 0.3 0.25 0.3 6',
                                 f'particle minecraft:dust{{color:[{rgb(col)}],scale:1.1}} ~ ~1 ~ 0.3 0.35 0.3 0 6',
                                 'playsound minecraft:entity.player.attack.strong neutral @a[distance=..16] ~ ~ ~ 0.45 1.15',
                                 f'scoreboard players set @e[type=minecraft:wolf,tag={tag},distance=..32,limit=1,sort=nearest] bm.khs {HOLD}',
                                 f'scoreboard players set @e[type=minecraft:cat,tag={tag},distance=..32,limit=1,sort=nearest] bm.khs {HOLD}'])
    n, held = 0, 0
    for name in list(G.FUNCS):
        if name.startswith('atk/'): continue
        L = G.FUNCS[name]
        out, hit = [], False
        for l in L:
            out.append(l)
            m = DMG.match(l)
            if not m or m.group(6) not in ME: continue
            mac, pre = m.group(1), m.group(2)
            call = f'function bm:atk/fx/{m.group(6)[3:]}'
            if not pre:
                out.append(f'execute at @s run {call}')
            elif pre.endswith(' run '):
                p = pre[:-5]
                out.append((mac if '$(' in p else '') + f'{p} at @s run {call}')
            else:
                continue
            n += 1; hit = True
        if hit: L[:] = out
    # the hold: as the follower's animation runs, two ticks still on a blow (its frame clock held with it)
    for tag, (w, anim) in ME.items():
        if not anim or anim not in G.FUNCS: continue
        fr = None
        for nm, L in G.FUNCS.items():
            for i, l in enumerate(L):
                if l == f'function bm:{anim}':
                    for k in range(max(0, i - 3), i):
                        mm = re.search(r'scoreboard players add @s (bm\.\w+) 1$', L[k])
                        if mm: fr = mm.group(1)
            if fr: break
        gate = ([f'execute if score @s bm.khs matches 1.. run scoreboard players remove @s {fr} 1'] if fr else []) + \
               ['execute if score @s bm.khs matches 1.. run return run scoreboard players remove @s bm.khs 1']
        G.FUNCS[anim][0:0] = gate; held += 1
    return n, held


# ======================================================================== the dash
def dash(G, pfx, col, reach=1.6, speed=0.9, lift=3, onto=False, pass_='#bm:grap_pass', trail=()):
    """the dash for one follower (its functions <pfx>/k/...): <pfx>/k/go {a:<n>} as the follower, at it, with its target tagged
    bm.ktn (one foe) - carried to it a step a tick (an arc: up for `lift` ticks, then on), trailing its colour; on arrival (within
    `reach`, or `onto` it) <pfx>/k/arrive runs <pfx>/k/at<n> as the follower. Its tick: <pfx>/k/tick (call it from the follower's
    own tick while bm.kd >= 1). Returns the line to put in that tick."""
    fn = G.fn
    if 'bm.kd' not in G.OBJECTIVES:
        G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in ('bm.kd', 'bm.ka', 'bm.kt', 'bm.ktid')]
        G.OBJECTIVES += ['bm.kd', 'bm.ka', 'bm.kt', 'bm.ktid']
    tg = '@e[tag=bm.ktnow,limit=1]'
    c = rgb(col)
    fn(f'{pfx}/k/go', ['$scoreboard players set @s bm.ka $(a)', 'scoreboard players set @s bm.kd 16', 'scoreboard players set @s bm.kt 0',
                       'scoreboard players operation @e[tag=bm.ktn] bm.ktid = @s bm.pid', 'tag @e[tag=bm.ktn] add bm.ktg', 'tag @e[tag=bm.ktn] remove bm.ktn',
                       'data merge entity @s {NoGravity:1b,Motion:[0d,0d,0d]}',
                       'particle minecraft:poof ~ ~0.15 ~ 0.3 0.05 0.3 0.04 8', f'particle minecraft:dust{{color:[{c}],scale:1.2}} ~ ~0.3 ~ 0.3 0.1 0.3 0 6',
                       'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.35 1.6'])
    near = f'distance=..{0.9 if onto else reach}'
    fn(f'{pfx}/k/tick', ['scoreboard players remove @s bm.kd 1', 'scoreboard players add @s bm.kt 1', 'data modify entity @s Motion set value [0d,0d,0d]',
                         'scoreboard players operation #kme bm.rng = @s bm.pid',
                         'execute as @e[tag=bm.ktg,distance=..24] if score @s bm.ktid = #kme bm.rng run tag @s add bm.ktnow',
                         f'execute unless entity {tg} run return run function bm:{pfx}/k/stop',
                         f'execute if entity @e[tag=bm.ktnow,{near}] run return run function bm:{pfx}/k/arrive',
                         f'execute if score @s bm.kt matches ..{lift} if block ~ ~1.6 ~ {pass_} run tp @s ~ ~0.32 ~',
                         f'execute facing entity {tg} feet positioned ^ ^ ^{speed} if block ~ ~ ~ {pass_} if block ~ ~0.9 ~ {pass_} run return run function bm:{pfx}/k/step',
                         f'execute facing entity {tg} feet positioned ^ ^ ^{speed} positioned ~ ~0.6 ~ if block ~ ~ ~ {pass_} if block ~ ~0.9 ~ {pass_} run return run function bm:{pfx}/k/step',
                         f'function bm:{pfx}/k/arrive'])
    fn(f'{pfx}/k/step', [f'tp @s ~ ~ ~ facing entity {tg} feet', f'particle minecraft:dust{{color:[{c}],scale:0.9}} ~ ~0.6 ~ 0.12 0.15 0.12 0 2'] + list(trail) + [
                         'execute if score @s bm.kd matches ..0 run function bm:' + f'{pfx}/k/arrive', 'tag @e[tag=bm.ktnow] remove bm.ktnow'])
    fn(f'{pfx}/k/arrive', ['scoreboard players set @s bm.kd 0', 'data merge entity @s {NoGravity:0b}',
                           'particle minecraft:poof ~ ~0.1 ~ 0.35 0.05 0.35 0.03 6',
                           'playsound minecraft:entity.player.attack.knockback neutral @a[distance=..16] ~ ~ ~ 0.4 1.3'] +
       [f'execute if score @s bm.ka matches {i} run function bm:{pfx}/k/at{i}' for i in range(1, 9)] +
       ['tag @e[tag=bm.ktnow] remove bm.ktg', 'tag @e[tag=bm.ktnow] remove bm.ktnow'])
    fn(f'{pfx}/k/stop', ['scoreboard players set @s bm.kd 0', 'data merge entity @s {NoGravity:0b}', 'tag @e[tag=bm.ktnow] remove bm.ktnow'])
    for i in range(1, 9):
        if f'{pfx}/k/at{i}' not in G.FUNCS: fn(f'{pfx}/k/at{i}', ['return 0'])
    return f'execute if score @s bm.kd matches 1.. run function bm:{pfx}/k/tick'


# ======================================================================== signature moves
def sig(G, pfx, *, kid=1, tick_fn, state_fn, anim_fn, s_obj, place_fn, col, trigger, cd, timeline, end, face='foe', st=21, dash_kw=None, each=(), busy=None, own_place=False):
    """a timeline-driven special (as Bender's Rage): `trigger` (an `execute ... if ...` condition, run as the follower at it, each
    tick it's free) starts it; bm.ksg counts its ticks (bm.ksw: which of the follower's specials - kid); `timeline` {t: [cmds]}
    plays (as the follower, at it); a cmd 'DASH a <selector>' dashes to that foe (the timeline holds - bm.ksg 1000 - until it
    arrives, then goes on at t+1). While it runs the follower's own animation is held (its state `st`, no cycle) and it faces its
    foe (face='foe') or keeps its own heading ('own'). `end`: its last tick (all is put back). cd: ticks before it comes again
    (bm.kcd<kid>). A follower's specials share its dash (a's must differ). own_place (2.95e): this move places the model its own way
    (another of the follower's specials uses another place_fn) - its lines run only for it, the others' not while it plays."""
    fn = G.fn
    for o in ('bm.ksg', 'bm.ksw', f'bm.kcd{kid}'):
        if o not in G.OBJECTIVES:
            G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy']; G.OBJECTIVES.append(o)
    foe = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body'
    lines, arr, first = [], {}, []
    for t in sorted(timeline):
        for c in timeline[t]:
            if t == 1 and not c.startswith('DASH '):      # (2.95e: tick 1 is played by the start itself - the tick after it counts on to 2)
                first.append(c); continue
            if c.startswith('DASH '):
                _d, a, sel = c.split(' ', 2)
                arr[int(a)] = t                       # (the next tick it counts on to t + 1: the blow)
                lines += [f'execute if score @s bm.ksg matches {t} run tag {sel} add bm.ktn',
                          f'execute if score @s bm.ksg matches {t} if entity @e[tag=bm.ktn] run function bm:{pfx}/k/go {{a:{a}}}',
                          f'execute if score @s bm.ksg matches {t} if score @s bm.kd matches 1.. run return run scoreboard players set @s bm.ksg 1000']
            else:
                lines.append(f'execute if score @s bm.ksg matches {t} run {c}')
    for a, t in arr.items():
        fn(f'{pfx}/k/at{a}', [f'scoreboard players set @s bm.ksg {t}'])
    fn(f'{pfx}/sg/{kid}/tick', list(each) + ['execute if score @s bm.ksg matches 1000 run return 0', 'scoreboard players add @s bm.ksg 1'] + lines +
       [f'execute if score @s bm.ksg matches {end}.. run function bm:{pfx}/sg/{kid}/end'])
    fn(f'{pfx}/sg/{kid}/end', ['scoreboard players set @s bm.ksg 0', 'scoreboard players set @s bm.ksw 0', f'scoreboard players set @s bm.kcd{kid} {cd}',
                               'data merge entity @s {NoGravity:0b}'])
    T = G.FUNCS[tick_fn]
    if busy:                                                  # (its own moves don't start while this one plays)
        b = f'unless score @s {busy} matches 1.. '
        for i, l in enumerate(T):
            if l.startswith('execute ') and b in l and 'run function' in l and 'bm.ksg' not in l:
                T[i] = 'execute unless score @s bm.ksg matches 1.. ' + l[len('execute '):]
    k = next((i + 1 for i, l in enumerate(T) if l.startswith('scoreboard players operation #me bm.pid = @s bm.pid')), 0)
    add = []
    if arr:                                                   # (a move with a dash in it: the follower's dash)
        dl = dash(G, pfx, col, **(dash_kw or {})) if f'{pfx}/k/tick' not in G.FUNCS else f'execute if score @s bm.kd matches 1.. run function bm:{pfx}/k/tick'
        for a, t in arr.items():                              # (dash() makes empty arrivals - ours again)
            fn(f'{pfx}/k/at{a}', [f'scoreboard players set @s bm.ksg {t}'])
        if dl not in T: add.append(dl)
    add += [f'execute if score @s bm.kcd{kid} matches 1.. run scoreboard players remove @s bm.kcd{kid} 1',
            f'{trigger.replace("execute ", f"execute unless score @s bm.ksg matches 1.. unless score @s bm.kcd{kid} matches 1.. ", 1)} run function bm:{pfx}/sg/{kid}/go',
            f'execute if score @s bm.ksw matches {kid} if score @s bm.ksg matches 1.. run function bm:{pfx}/sg/{kid}/tick']
    fn(f'{pfx}/sg/{kid}/go', ['scoreboard players set @s bm.ksg 1', f'scoreboard players set @s bm.ksw {kid}'] + (list(each) + first if first else []))
    T[k:k] = add
    if arr: G.FUNCS[f'{pfx}/k/stop'].append(f'execute if score @s bm.ksw matches {kid} if score @s bm.ksg matches 1000 run scoreboard players set @s bm.ksg {end - 4}')
    gate_st = f'execute if score @s bm.ksg matches 1.. run return run scoreboard players set #st bm.rng {st}'
    if gate_st not in G.FUNCS[state_fn]: G.FUNCS[state_fn].insert(0, gate_st)
    gate_an = f'execute if score @s {s_obj} matches {st} run return 0'
    if gate_an not in G.FUNCS[anim_fn]: G.FUNCS[anim_fn].insert(0, gate_an)
    if face == 'none': return
    i = T.index(f'function bm:{anim_fn}') + 1
    pl = ([f'execute if score @s {s_obj} matches {st} if entity @e[{foe},distance=..20] facing entity @e[{foe},distance=..20,sort=nearest,limit=1] feet rotated ~ 0 run function bm:{place_fn}',
           f'execute if score @s {s_obj} matches {st} unless entity @e[{foe},distance=..20] rotated as @s rotated ~ 0 run function bm:{place_fn}'] if face == 'foe' else
          [f'execute if score @s {s_obj} matches {st} rotated as @s rotated ~ 0 run function bm:{place_fn}'])
    if own_place:
        g = f'if score @s bm.ksw matches {kid} '
        for k, l in enumerate(T):                             # (the other specials' placing: not while this one plays)
            if l.startswith(f'execute if score @s {s_obj} matches {st} ') and 'run function bm:' in l and f'bm:{place_fn}' not in l and 'bm.ksw' not in l:
                T[k] = l.replace('execute ', f'execute unless score @s bm.ksw matches {kid} ', 1)
        pl = [l.replace('execute ', 'execute ' + g, 1) for l in pl]
    if face != 'none' and pl[0] not in T: T[i:i] = pl

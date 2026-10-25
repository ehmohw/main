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
      'bm.ompme': ('omega', 'p170/anim'), 'bm.nbme': ('neighbor', 'p187/anim'), 'bm.mzme': ('capshun', 'p198/anim'), 'bm.lnme': ('lantern', 'p194/anim'),
      'bm.kkme': ('chef', 'p186/anim'), 'bm.fyme': ('fishy', 'p145/anim'), 'bm.dwme': ('dennis', 'p163/dw/anim'), 'bm.bvme': ('bender', 'p195/anim'),
      'bm.bome': ('bloo', 'p191/anim'), 'bm.bjme': ('bones', 'p196/anim'), 'bm.avme': ('ava', 'p189/anim'), 'bm.aspme': ('ashur', 'p185/anim')}
HOLD = 2                                     # (ticks of hit-stop)
DMG = re.compile(r'^(\$?)(.*?)damage @s (\S+) (\S+) by @e\[type=minecraft:(wolf|cat),tag=(bm\.[a-z0-9]+)')


def rgb(col):
    return ','.join(f'{int(col[i:i + 2], 16) / 255:.2f}' for i in (1, 3, 5))


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
def sig(G, pfx, *, kid=1, tick_fn, state_fn, anim_fn, s_obj, place_fn, col, trigger, cd, timeline, end, face='foe', st=21, dash_kw=None, each=(), busy=None):
    """a timeline-driven special (as Bender's Rage): `trigger` (an `execute ... if ...` condition, run as the follower at it, each
    tick it's free) starts it; bm.ksg counts its ticks (bm.ksw: which of the follower's specials - kid); `timeline` {t: [cmds]}
    plays (as the follower, at it); a cmd 'DASH a <selector>' dashes to that foe (the timeline holds - bm.ksg 1000 - until it
    arrives, then goes on at t+1). While it runs the follower's own animation is held (its state `st`, no cycle) and it faces its
    foe (face='foe') or keeps its own heading ('own'). `end`: its last tick (all is put back). cd: ticks before it comes again
    (bm.kcd<kid>). A follower's specials share its dash (a's must differ)."""
    fn = G.fn
    for o in ('bm.ksg', 'bm.ksw', f'bm.kcd{kid}'):
        if o not in G.OBJECTIVES:
            G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy']; G.OBJECTIVES.append(o)
    foe = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body'
    lines, arr = [], {}
    for t in sorted(timeline):
        for c in timeline[t]:
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
    fn(f'{pfx}/sg/{kid}/go', ['scoreboard players set @s bm.ksg 1', f'scoreboard players set @s bm.ksw {kid}'])
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
    if face != 'none' and pl[0] not in T: T[i:i] = pl

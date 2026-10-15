"""2.80: THE STAGING KIT - what made Apophiss's coming and going feel finished, for every encounter.

Apophiss's fight is polished because it is choreographed: a timeline tick by tick, eased movement, sounds stacked in
layers, a darkness pulse, the screen shaken, lines spoken, a death staged rather than a body falling over. This module
is those tools, for any boss built on a vanilla mob:

- at(timer, t, cmd...): lines that run on tick t (or a range 'a..b') of an entity's timer score.
- snd / stack / shake / dark / ring / line / spiral / title_card: the building blocks.
- STAGING (install + stage): a boss is summoned FROZEN (no AI, invulnerable, silent) and plays its arrival timeline; then
  it is released and ARMED: a health buffer (a +1000 max-health modifier, its health raised to match) means no blow can
  kill it outright. When its real health is spent (health <= its buffer) it freezes again and plays its death timeline;
  the finale makes it invisible and kills it - `damage ... by <the player who brought it down>` - so its loot table,
  the advancements, the bounties and the 'slain' rewards all run exactly as for a kill. Health readers in a boss's own
  functions are rewritten to subtract the buffer (debuffer), so its bar and its enrage thresholds still read true.
- RAGE: a boss's enrage becomes a moment - it freezes, roars, the screen shakes - before its rage takes hold.
- WIND-UPS: an instant attack becomes telegraphed: the boss charges for a beat (a ring on the ground where it will land,
  a rising sound), then the attack fires.

Scores: bm.cat (arrival tick), bm.cdt (death tick), bm.crt (rage tick), bm.cwu / bm.cwa (wind-up ticks / which attack),
bm.cbuf (the health buffer), bm.cmx (max health before the buffer). Tags: bm.carr (arriving), bm.carm (armed),
bm.cdie (dying), bm.crage (raging), bm.cfrz (any of those freezes - a boss's own loops skip while it is set),
bm.cwind (winding up), bm.ckill (the player credited with the kill)."""
import math
import random
from items import T
from nbt import snbt

BUF = 1000                 # the health buffer (hit points no single blow can take)
OBJ = ['bm.cat', 'bm.cdt', 'bm.crt', 'bm.cwu', 'bm.cwa', 'bm.cbuf', 'bm.cmx']
_STAGED = []               # (kind, entity type, tag) - every staged boss
_WINDUPS = []              # (idx, kind, attack function, ticks, visual lines, start lines)


# ------------------------------------------------------------------------------------------------ building blocks
def at(timer, t, *cmds):
    return [f'execute if score @s {timer} matches {t} run {c}' for c in cmds]


def snd(s, v=1.0, p=1.0, r=64, src='hostile'):
    s = s if ':' in s else 'minecraft:' + s
    return f'playsound {s} {src} @a[distance=..{r}] ~ ~ ~ {v:g} {p:g}'


def stack(*sounds, r=64):
    """several sounds on one beat - the Apophiss way (his burst is four)"""
    return [snd(s, v, p, r) for s, v, p in sounds]


def dark(secs, r=48):
    return f'effect give @a[distance=..{r}] minecraft:darkness {secs} 0 true'


def shake(timer, t0, n, amp, r=48, seed=1):
    """the screen jolted and put back, tick by tick, the jolts dying away"""
    rs = random.Random(seed)
    out = []
    for i in range(0, max(2, n) - 1, 2):
        a = amp * (1 - i / n)
        dx = a * rs.choice((-1, 1)) * rs.uniform(0.6, 1.0)
        dy = a * 0.6 * rs.choice((-1, 1)) * rs.uniform(0.6, 1.0)
        out += at(timer, t0 + i, f'execute as @a[distance=..{r}] at @s run rotate @s ~{dx:.2f} ~{dy:.2f}')
        out += at(timer, t0 + i + 1, f'execute as @a[distance=..{r}] at @s run rotate @s ~{-dx:.2f} ~{-dy:.2f}')
    return out


def ring(part, r, n, y=0.15, d=0.05, speed=0, count=1, force=96):
    """a ring of particles round the executing position (world axes)"""
    f = f' force @a[distance=..{force}]' if force else ''
    return [f'particle {part} ~{r * math.cos(2 * math.pi * k / n):.2f} ~{y:g} ~{r * math.sin(2 * math.pi * k / n):.2f} {d} {d} {d} {speed} {count}{f}'
            for k in range(n)]


def ring_up(part, r, n, y=0.15, rise=0.25, speed=0.0, force=96):
    """a ring whose particles drift upward (count 0 = the delta is a direction)"""
    f = f' force @a[distance=..{force}]' if force else ''
    return [f'particle {part} ~{r * math.cos(2 * math.pi * k / n):.2f} ~{y:g} ~{r * math.sin(2 * math.pi * k / n):.2f} 0 {rise} 0 {max(speed, 0.08):g} 0{f}'
            for k in range(n)]


def converge(part, r, n, y=1.0, speed=0.4, force=96):
    """particles thrown inward from a ring toward the middle (count 0: the delta is their heading)"""
    f = f' force @a[distance=..{force}]' if force else ''
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n
        x, z = r * math.cos(a), r * math.sin(a)
        out.append(f'particle {part} ~{x:.2f} ~{y:g} ~{z:.2f} {-x / r:.2f} 0 {-z / r:.2f} {speed:g} 0{f}')
    return out


def column(part, h, n=8, d=0.15, count=2, force=96):
    f = f' force @a[distance=..{force}]' if force else ''
    return [f'particle {part} ~ ~{h * k / n:.2f} ~ {d} {d} {d} 0 {count}{f}' for k in range(n + 1)]


def title_card(who, name, col, sub, subcol='gray', times=(8, 60, 20)):
    return [f'title {who} times {times[0]} {times[1]} {times[2]}',
            f'title {who} subtitle {snbt(T(sub, subcol, italic=True))}',
            f'title {who} title {snbt(T(name, col, bold=True))}']


def ease(k):
    k = max(0.0, min(1.0, k))
    return k * k * (3 - 2 * k)


def ease_out(k):
    k = max(0.0, min(1.0, k))
    return 1 - (1 - k) ** 2


def tween(timer, t0, t1, fn_line):
    """one line per tick from t0 to t1: fn_line(k) gives the command for progress k (0..1)"""
    out = []
    for t in range(t0, t1 + 1):
        k = (t - t0) / max(1, t1 - t0)
        out += at(timer, t, fn_line(k))
    return out


def scale_tween(timer, t0, t1, a, b, curve=ease):
    """the scale attribute from a to b (eased) - a growth or a wilting"""
    return tween(timer, t0, t1, lambda k: f'attribute @s minecraft:scale base set {a + (b - a) * curve(k):.3f}')


def grow(timer, t0, t1, a, b, curve=ease_out):
    """its size from a to b times its own (a scale modifier tweened - for a mob whose size isn't known here); gone at t1"""
    out = []
    for t in range(t0, t1 + 1):
        k = (t - t0) / max(1, t1 - t0)
        v = a + (b - a) * curve(k) - 1
        out += at(timer, t, 'attribute @s minecraft:scale modifier remove bm:cine_grow')
        if t < t1:
            out += at(timer, t, f'attribute @s minecraft:scale modifier add bm:cine_grow {v:.3f} add_multiplied_total')
    return out


def rise(timer, t0, t1, dy, curve=ease_out, vehicle=False):
    """moved up by dy in all over t0..t1 (per-tick steps that sum to dy, eased) - out of the sand, out of the ground.
    Each step is taken from where it stands now (`execute at @s`), so moves on the same tick add up."""
    out = []
    prev = 0.0
    for t in range(t0, t1 + 1):
        k = (t - t0) / max(1, t1 - t0)
        cur = dy * curve(k)
        step = cur - prev
        prev = cur
        cmd = f'tp @s ~ ~{step:.4f} ~'
        out += at(timer, t, f'execute on vehicle at @s run {cmd}' if vehicle else f'execute at @s run {cmd}')
    return out


def offset(segments, t):
    """where rise() segments [(t0, t1, dy, curve)] have moved it by the end of tick t"""
    o = 0.0
    for t0, t1, dy, curve in segments:
        if t >= t0:
            o += dy * curve(min(1.0, (t - t0) / max(1, t1 - t0)))
    return o


def jitter(timer, t0, t1, amp, seed=7, every=2, vehicle=False):
    """shudders: small teleports there and back (a rider shudders through its mount - a teleport would unseat it)"""
    rs = random.Random(seed)
    out = []
    pre = 'execute on vehicle at @s run ' if vehicle else 'execute at @s run '
    for t in range(t0, t1, every):
        dx, dz = rs.uniform(-amp, amp), rs.uniform(-amp, amp)
        out += at(timer, t, f'{pre}tp @s ~{dx:.3f} ~ ~{dz:.3f}')
        out += at(timer, t + 1, f'{pre}tp @s ~{-dx:.3f} ~ ~{-dz:.3f}')
    return out


# ------------------------------------------------------------------------------------------------ the engine
def install(G):
    """the shared machinery (once). Each staged boss adds its own timelines with stage()."""
    fn = G.fn
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in OBJ]
    G.OBJECTIVES += OBJ
    # ---- armed: the buffer (as the boss). Its max health is read before and after the modifier, so a boss whose health
    #      another phase scaled still gets exactly the difference as its buffer.
    fn('cine/arm', ['execute if entity @s[tag=bm.carm] run return 0',
                    'attribute @s minecraft:max_health modifier remove bm:cine_buf',
                    'execute store result score @s bm.cmx run attribute @s minecraft:max_health get',
                    f'attribute @s minecraft:max_health modifier add bm:cine_buf {BUF} add_value',
                    'execute store result score @s bm.cbuf run attribute @s minecraft:max_health get',
                    'scoreboard players operation @s bm.cbuf -= @s bm.cmx',
                    'execute store result score #ch bm.rng run data get entity @s Health',
                    'scoreboard players operation #ch bm.rng += @s bm.cbuf',
                    'execute store result entity @s Health float 1 run scoreboard players get #ch bm.rng',
                    'tag @s add bm.carm'])
    # ---- the watch (as an armed boss, every tick): its real health spent? Its death begins.
    fn('cine/watch', ['execute store result score #ch bm.rng run data get entity @s Health',
                      'execute if score #ch bm.rng <= @s bm.cbuf run function bm:cine/die/begin'])
    # (a bar's value without the buffer - as the boss)
    fn('cine/bar', ['execute unless score @s bm.cbuf matches -2147483648.. run scoreboard players set @s bm.cbuf 0',
                    'execute store result score #cbh bm.rng run data get entity @s Health',
                    'scoreboard players operation #cbh bm.rng -= @s bm.cbuf',
                    'execute if score #cbh bm.rng matches ..-1 run scoreboard players set #cbh bm.rng 0',
                    '$execute store result bossbar $(b) value run scoreboard players get #cbh bm.rng'])
    # ---- freeze / release (as the boss; a mount freezes with its rider). A boss silent by design stays silent after.
    fn('cine/freeze', ['execute if entity @s[tag=bm.cfrz] run return 0', 'execute if data entity @s {Silent:1b} run tag @s add bm.csil',
                       'data merge entity @s {NoAI:1b,Invulnerable:1b,Silent:1b}', 'tag @s add bm.cfrz',
                       'execute on vehicle run function bm:cine/freeze_v', 'execute on passengers run function bm:cine/freeze_v'])
    fn('cine/freeze_v', ['execute if data entity @s {NoAI:1b} run return 0', 'execute if data entity @s {Silent:1b} run tag @s add bm.csil',
                         'data merge entity @s {NoAI:1b,Invulnerable:1b,Silent:1b}'])
    fn('cine/release', ['data merge entity @s {NoAI:0b,Invulnerable:0b}', 'execute unless entity @s[tag=bm.csil] run data merge entity @s {Silent:0b}',
                        'tag @s remove bm.csil', 'tag @s remove bm.cfrz', 'execute on vehicle run function bm:cine/release_v',
                        'execute on passengers run function bm:cine/release_v'])
    fn('cine/release_v', ['data merge entity @s {NoAI:0b,Invulnerable:0b}', 'execute unless entity @s[tag=bm.csil] run data merge entity @s {Silent:0b}',
                          'tag @s remove bm.csil'])
    # ---- arrival: start (as the new boss) / end
    fn('cine/arr/start', ['function bm:cine/freeze', 'tag @s add bm.carr', 'scoreboard players set @s bm.cat 0', 'scoreboard players set @s bm.cbuf 0'])
    fn('cine/arr/end', ['tag @s remove bm.carr', 'function bm:cine/release', 'function bm:cine/arm'])
    fn('cine/arr/free', ['tag @s remove bm.carr', 'function bm:cine/release'])        # (an arrival only - no buffer, no staged death)
    # ---- death: begin (as the boss whose health is spent)
    fn('cine/die/begin', ['tag @s remove bm.carm', 'tag @s remove bm.cwind', 'tag @s remove bm.crage', 'tag @s add bm.cdie',
                          'scoreboard players set @s bm.cdt 0', 'function bm:cine/freeze',
                          # (who brought it down: its last attacker if a player, else whoever is nearest)
                          'tag @a remove bm.ckill', 'execute on attacker if entity @s[type=minecraft:player] run tag @s add bm.ckill',
                          'execute unless entity @a[tag=bm.ckill] run tag @p[distance=..64,gamemode=!spectator] add bm.ckill',
                          # (it can't die mid-sequence: its health is held at its buffer)
                          'execute store result entity @s Health float 1 run scoreboard players get @s bm.cbuf'])
    # ---- death: the finale (as the boss) - invisible, unarmed, and killed as by the player who brought it down
    fn('cine/die/kill', ['tag @s remove bm.cdie', 'tag @s remove bm.cfrz', 'effect clear @s',
                         'effect give @s minecraft:invisibility infinite 0 true',
                         'item replace entity @s armor.head with minecraft:air', 'item replace entity @s armor.chest with minecraft:air',
                         'item replace entity @s armor.legs with minecraft:air', 'item replace entity @s armor.feet with minecraft:air',
                         'item replace entity @s weapon.mainhand with minecraft:air', 'item replace entity @s weapon.offhand with minecraft:air',
                         'data merge entity @s {NoAI:0b,Invulnerable:0b,Silent:1b}',
                         'execute if entity @a[tag=bm.ckill] run damage @s 1000000 minecraft:player_attack by @a[tag=bm.ckill,limit=1]',
                         'execute unless entity @a[tag=bm.ckill] run damage @s 1000000 minecraft:generic',
                         'tag @a remove bm.ckill'])
    # ---- rage: start (as the boss) / end
    fn('cine/rage/start', ['execute if entity @s[tag=bm.cfrz] run return 0', 'function bm:cine/freeze', 'tag @s add bm.crage',
                           'scoreboard players set @s bm.crt 0', 'tag @s remove bm.cwind'])
    fn('cine/rage/end', ['tag @s remove bm.crage', 'function bm:cine/release'])
    G.FUNCS['admin/uninstall'][0:0] = ['tag @e remove bm.carr', 'tag @e remove bm.cdie', 'tag @e remove bm.crage', 'tag @e remove bm.cfrz',
                                       'tag @e remove bm.csil', 'tag @e remove bm.cunarm']
    # (party scaling - every boss's health grows with the players near it: done on its real health, the buffer taken off
    #  and put back after; never in the middle of a sequence)
    fn('cine/unarm', ['execute store result score #cu bm.rng run data get entity @s Health',
                      'scoreboard players operation #cu bm.rng -= @s bm.cbuf',
                      'execute if score #cu bm.rng matches ..0 run scoreboard players set #cu bm.rng 1',
                      'execute store result entity @s Health float 1 run scoreboard players get #cu bm.rng',
                      'attribute @s minecraft:max_health modifier remove bm:cine_buf',
                      'tag @s remove bm.carm', 'tag @s add bm.cunarm'])
    fn('cine/rearm', ['tag @s remove bm.cunarm', 'function bm:cine/arm'])
    L = G.FUNCS['p67/scale']
    ih = L.index('execute store result score #h bm.rng run data get entity @s Health')
    L.insert(ih, 'execute if entity @s[tag=bm.carm] run function bm:cine/unarm')
    L.insert(0, 'execute if entity @s[tag=bm.cfrz] run return 0')
    L.append('execute if entity @s[tag=bm.cunarm] run function bm:cine/rearm')
    # (the heist kit's finishing blow reads its target's health as a fraction - without the buffer, for a staged one)
    fn('cine/unbuf3', ['scoreboard players operation #h bm.rng -= @s bm.cbuf', 'scoreboard players operation #h bm.rng -= @s bm.cbuf',
                       'scoreboard players operation #h bm.rng -= @s bm.cbuf', 'scoreboard players operation #m bm.rng -= @s bm.cbuf'])
    L = G.FUNCS['p80/kit/ohit_t']
    assert L[0].startswith('execute store result score #h bm.rng run data get entity @s Health 3') and 'max_health' in L[1], L[:2]
    L.insert(2, 'execute if entity @s[tag=bm.carm] run function bm:cine/unbuf3')


def stage(G, kind, etype, tag, arrive=None, die=None, rage=None, arrive_len=100, die_len=100, rage_len=36, arm=True):
    """a boss kind's three timelines (lists of lines on bm.cat / bm.cdt / bm.crt) and their dispatchers.
    The death timeline should end in 'function bm:cine/die/kill' at die_len; arrival and rage end on their own."""
    fn = G.fn
    sel = f'@e[type=minecraft:{etype},tag={tag}' if etype else f'@e[tag={tag}'     # (no type: a boss of many kinds)
    tick = G.FUNCS['tick']
    if arrive is not None:
        fn(f'cine/{kind}/arr', ['scoreboard players add @s bm.cat 1'] + arrive +
           [f'execute if score @s bm.cat matches {arrive_len}.. run function bm:cine/arr/{"end" if arm else "free"}'])
        tick.append(f'execute as {sel},tag=bm.carr] at @s run function bm:cine/{kind}/arr')
    if die is not None:
        fn(f'cine/{kind}/die', ['scoreboard players add @s bm.cdt 1'] + die +
           [f'execute if score @s bm.cdt matches {die_len}.. run function bm:cine/die/kill'])
        tick.append(f'execute as {sel},tag=bm.cdie] at @s run function bm:cine/{kind}/die')
    if rage is not None:
        fn(f'cine/{kind}/rage', ['scoreboard players add @s bm.crt 1'] + rage +
           [f'execute if score @s bm.crt matches {rage_len}.. run function bm:cine/rage/end'])
        tick.append(f'execute as {sel},tag=bm.crage] at @s run function bm:cine/{kind}/rage')
    if arm:
        tick.append(f'execute as {sel},tag=bm.carm] at @s run function bm:cine/watch')
    _STAGED.append((kind, etype, tag))


def windup(G, kind, attack, ticks, visual, start=(), cancel=()):
    """an instant attack, telegraphed: calls to `attack` in the boss's functions become a wind-up of `ticks`, playing
    `visual` each tick (bm.cwu counts down: ticks-1 on the first tick .. 0 on the last), then the attack itself (rotated
    ~ 0, as it was called). `cancel` runs if the wind-up is cut short (the boss freezes: a rage, its death)."""
    idx = len(_WINDUPS) + 1
    _WINDUPS.append((idx, kind, attack, ticks, list(visual), list(start), list(cancel)))
    G.fn(f'cine/wu/s{idx}', ['execute if entity @s[tag=bm.cfrz] run return 0', 'execute if entity @s[tag=bm.cwind] run return 0',
                             f'scoreboard players set @s bm.cwu {ticks}', f'scoreboard players set @s bm.cwa {idx}', 'tag @s add bm.cwind'] + list(start))
    G.fn(f'cine/wu/v{idx}', list(visual))
    return f'cine/wu/s{idx}'


def finish(G):
    """after every stage()/windup(): the wind-up dispatcher (again after any later windup() - it is rebuilt whole)"""
    if not _WINDUPS:
        return
    fn = G.fn
    fn('cine/wu/tick', ['execute if entity @s[tag=bm.cfrz] run return run function bm:cine/wu/cancel',
                        'scoreboard players remove @s bm.cwu 1'] +
       [f'execute if score @s bm.cwa matches {i} run function bm:cine/wu/v{i}' for i, *_ in _WINDUPS] +
       ['execute if score @s bm.cwu matches ..0 run function bm:cine/wu/fire'])
    fn('cine/wu/fire', ['tag @s remove bm.cwind'] +
       [f'execute if score @s bm.cwa matches {i} rotated ~ 0 run function bm:{atk}' for i, kind, atk, *_ in _WINDUPS])
    fn('cine/wu/cancel', ['tag @s remove bm.cwind'] +
       [f'execute if score @s bm.cwa matches {i} run {c}' for i, kind, atk, tk, vis, st, cancel in _WINDUPS for c in cancel])
    line = 'execute as @e[tag=bm.cwind] at @s run function bm:cine/wu/tick'
    if line not in G.FUNCS['tick']:            # (it may be called again by a later phase that adds wind-ups)
        G.FUNCS['tick'].append(line)


def gate(G, names):
    """a boss's own loops skip while it is frozen (arriving, raging, dying) - after any 'last seen' stamp at the top,
    so the pack still knows it's about"""
    for n in names:
        assert n in G.FUNCS, n
        L = G.FUNCS[n]
        i = 1 if L and L[0].endswith('run time query gametime') else 0
        L.insert(i, 'execute if entity @s[tag=bm.cfrz] run return 0')


def debuffer(G, names):
    """health readers in a boss's own functions, without the buffer: its bar and its thresholds still read true"""
    import re
    rx_bar = re.compile(r'^execute store result bossbar (\S+) value run data get entity @s Health$')
    rx_sc = re.compile(r'^execute store result score (#\w+) (bm\.\w+) run data get entity @s Health$')
    n_bar = n_sc = 0
    for n in names:
        L = G.FUNCS[n]
        out = []
        for l in L:
            m = rx_bar.match(l)
            if m:
                out.append(f'function bm:cine/bar {{b:"{m.group(1)}"}}'); n_bar += 1; continue
            out.append(l)
            m = rx_sc.match(l)
            if m:
                out.append(f'scoreboard players operation {m.group(1)} {m.group(2)} -= @s bm.cbuf'); n_sc += 1
        G.FUNCS[n] = out
    return n_bar, n_sc


def hook_calls(G, names, attack, target):
    """`function bm:<attack>` in these functions -> `function bm:<target>` (the wind-up in front of the attack)"""
    n = 0
    for nm in names:
        L = G.FUNCS[nm]
        for i, l in enumerate(L):
            if l.endswith(f'run function bm:{attack}'):
                L[i] = l[:-len(f'function bm:{attack}')] + f'function bm:{target}'
                n += 1
    return n

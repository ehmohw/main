"""3.0d: COMPANION SIZE - a very large follower shrunk to stand beside you (the owner: "a companion size toggle for large followers
- Apophiss, Omega, Ophanim, and any others you feel need it"; the Bound Sovereign and Vexis already have their size toggles).

How: a rig's size is baked into its generated functions - each pose's translations and scales, its place's joint offsets, its grow.
twin() makes a scaled copy of every one of those (cs/<name>: every number in a translation:[..] or scale:[..] and every ^x ^y ^z of
a positioned, times k) and puts one line at the top of the original: as a host tagged <tag>, run the copy instead. The follower's
own poses, tweens, cycles and attacks are untouched - they call the same functions - so the whole rig, in every pose, keeps its
proportions at k of its size. Its attacks and stats are the same (the damage commands aren't touched).

sync(...) -> the host-tick lines: the owner's choice (a score, 1 = companion size) carried onto the host as <tag>; changed, the host's
own scale attribute (its hitbox) set to match and its rig re-posed (its state reset: the next frame's pose applies the new size).
toggle(...) makes the menu row's function (as the player). Default off; kept on the owner (logout, recall, faint)."""
import re

_NUM = re.compile(r'(-?\d+(?:\.\d+)?)(f?)')


def _mul(txt, k):
    return _NUM.sub(lambda m: f'{float(m.group(1)) * k:.4f}{m.group(2)}', txt)


def scaled(line, k):
    line = re.sub(r'((?:translation|scale):\[)([^\]]*)(\])', lambda m: m.group(1) + _mul(m.group(2), k) + m.group(3), line)
    line = re.sub(r'positioned \^(-?[\d.]*) \^(-?[\d.]*) \^(-?[\d.]*)',
                  lambda m: 'positioned ' + ' '.join('^' + (f'{float(x) * k:.4f}' if x not in ('', '-') else '') for x in m.groups()), line)
    return line


def twin(G, names, k, tag):
    """each named function gets a scaled twin, cs/<name>, run in its place for a host tagged <tag>. -> how many"""
    n = 0
    for name in names:
        lines = G.FUNCS[name]
        assert not any(l.startswith('$') for l in lines), name
        G.fn(f'cs/{name}', [scaled(l, k) for l in lines])
        lines.insert(0, f'execute if entity @s[tag={tag}] run return run function bm:cs/{name}')
        n += 1
    return n


def rig_functions(G, pfx, extra=()):
    """a follower's own size-bearing functions: its poses (and their tweens), its place, its grow"""
    names = sorted(n for n in G.FUNCS if n.startswith(f'{pfx}/pose/'))
    names += [n for n in (f'{pfx}/place', f'{pfx}/grow') + tuple(extra) if n in G.FUNCS]
    return names


def sync(pfx, obj, tag, state_obj, host_big, host_small):
    """(as the host, each tick) the owner's choice onto the host"""
    return ['scoreboard players set #cz bm.rng 0', f'execute on owner if score @s {obj} matches 1 run scoreboard players set #cz bm.rng 1',
            f'execute if score #cz bm.rng matches 1 unless entity @s[tag={tag}] run function bm:{pfx}/csz/on',
            f'execute if score #cz bm.rng matches 0 if entity @s[tag={tag}] run function bm:{pfx}/csz/off']


def build(G, pfx, obj, tag, state_obj, host_big, host_small, say_on, say_off, fx=()):
    """the host's switch (csz/on, csz/off) and the player's row (csz/toggle)"""
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {obj} dummy']
    G.OBJECTIVES.append(obj)
    G.fn(f'{pfx}/csz/on', ['tag @s add ' + tag, f'attribute @s minecraft:scale base set {host_small}', f'scoreboard players set @s {state_obj} -1',
                           'particle minecraft:poof ~ ~1 ~ 0.6 0.6 0.6 0.02 16', 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..16] ~ ~ ~ 1 1.6'] + list(fx))
    G.fn(f'{pfx}/csz/off', ['tag @s remove ' + tag, f'attribute @s minecraft:scale base set {host_big}', f'scoreboard players set @s {state_obj} -1',
                            'particle minecraft:poof ~ ~2 ~ 1.5 1.5 1.5 0.04 30', 'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..16] ~ ~ ~ 1 0.7'] + list(fx))
    G.fn(f'{pfx}/csz/toggle', [f'execute if score @s {obj} matches 1 run return run function bm:{pfx}/csz/toggle_off', f'scoreboard players set @s {obj} 1', say_on])
    G.fn(f'{pfx}/csz/toggle_off', [f'scoreboard players set @s {obj} 0', say_off])


LATE = []                      # (pfx, k, tag, extra function names): twinned by finalize, once every phase has added its lines


def finalize(G):
    """(late in the build: after the wardrobe, the shinies, the outfits and every other pass that adds lines to a rig's poses)"""
    return sum(twin(G, rig_functions(G, pfx, extra), k, tag) for pfx, k, tag, extra in LATE)

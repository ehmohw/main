"""2.80e: NO GLOW ON INVISIBLE HOSTS - a build pass over every function.

A custom-modelled mob (a follower, a boss, a Vorn, a Mimic...) is an invisible vanilla mob carrying display entities, and
the glowing outline ignores invisibility: a glowing host shows as the outline of a wolf, a husk or a rabbit around the
model. So every glow the pack hands out skips anything invisible (bm:p44/invis - every host carries infinite
invisibility):
  effect give <@e/@n selector> minecraft:glowing ...   -> the selector gains predicate=!bm:p44/invis
  effect give @s minecraft:glowing / Glowing:1b on @s   -> guarded with `execute unless predicate bm:p44/invis`
  data merge entity <selector> {Glowing:1b...}         -> the selector gains the predicate too
Glows from outside the pack (a spectral arrow) are cleared each second by a sweep in loop/second.
A line that already names bm:p44/invis is left alone. To outline a host on purpose, glow its displays (`on passengers`)."""
import re

INVIS = 'bm:p44/invis'
GLOW_CMD = re.compile(r'effect give (@[ensapr])(\[)?[^\n]*? minecraft:glowing|data (?:merge|modify) entity (@[ensapr])(\[)?[^\n]*?Glowing(?::| set value )1b')


def _close(s, i):
    """index of the ] matching the [ at s[i]"""
    d = 0
    for j in range(i, len(s)):
        c = s[j]
        if c in '[{': d += 1
        elif c in ']}':
            d -= 1
            if d == 0: return j
    raise ValueError(s)


def _guard(line):
    if INVIS in line: return line, False
    out, pos, changed = '', 0, False
    for m in GLOW_CMD.finditer(line):
        if m.start() < pos: continue
        sel = m.group(1) or m.group(3)
        at = line.index(sel, m.start())
        if sel == '@s':
            pre = (out + line[pos:m.start()]).rstrip()
            if pre.endswith('return run'): raise ValueError(f'noglow: a `return run` glow can\'t take the guard: {line}')
            if pre.endswith(' run'): out = pre[:-4] + f' unless predicate {INVIS} run '
            elif pre in ('', '$'): out = pre + f'execute unless predicate {INVIS} run '
            else: raise ValueError(f'noglow: unexpected @s glow in: {line}')
            out += line[m.start():at + 2]; pos = at + 2
        else:
            out += line[pos:at]
            if line[at + 2:at + 3] == '[':
                end = _close(line, at + 2)
                out += line[at:end] + (',' if end > at + 3 else '') + f'predicate=!{INVIS}]'; pos = end + 1
            else:
                out += sel + f'[predicate=!{INVIS}]'; pos = at + 2
        changed = True
    return out + line[pos:], changed


def apply(G):
    n = 0
    for name, lines in G.FUNCS.items():
        for i, l in enumerate(lines):
            new, ch = _guard(l)
            if ch: lines[i] = new; n += 1
    # (the net: anything invisible the pack watches that glows anyway - a spectral arrow, another pack - is put out)
    G.FUNCS['loop/second'].append(f'effect clear @e[tag=bm.seen,predicate={INVIS}] minecraft:glowing')
    return n


if __name__ == '__main__':
    for t in ['effect give @e[type=#bm:hostile,tag=!bm.npc,distance=..24] minecraft:glowing 3 0 true',
              'execute if score #kel bm.rng matches 5 run effect give @s minecraft:glowing 3 0',
              'effect give @s minecraft:glowing 2 0 true',
              'data merge entity @s {Glowing:1b,CustomNameVisible:1b}',
              'data modify entity @s Glowing set value 1b',
              'data merge entity @e[type=minecraft:item,distance=..3,sort=nearest,limit=1] {Glowing:1b,PickupDelay:20s}',
              'effect give @e[tag=bm.g30,distance=..30,predicate=!bm:p44/invis] minecraft:glowing 2 0 true',
              'data merge entity @s {Glowing:0b}',
              'effect give @e[nbt={a:[1]}] minecraft:glowing 1']:
        print(_guard(t)[0])

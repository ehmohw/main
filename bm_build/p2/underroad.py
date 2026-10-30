"""3.0a: THE WAY TO THE MAW - the Undercrown's approach, always open (phase237 calls it on every (re)build: p237/build/roads).

The Undercrown is cut into the Nether's rock wherever undercfg.ORIGIN falls, so what is outside its two mouths is luck: solid
netherrack, a lava lake, a wall. On every (re)build, in front of each mouth (the court's east and south faces):

  THE FORECOURT  a great open cavity cut out of whatever is there (east 40 x 35 x 41, south 41 x 32 x 40), its floor paved at
                 the court's level (black stone, the processional way in brick down its middle, red down the centre), soul-fire
                 braziers either side of the way and light hung through it; first, every lava (and loose gravel) cell in a shell
                 3 deep round it is turned to blackstone, so nothing pours in.
  THE ROAD       the walled processional road (as 2.98c's: paved, walls holding back the lava, its roof plugged, soul lanterns on
                 chains) BORED on out from the forecourt's far face a slice at a time, until the 9 x 9 x 9 ahead of it is mostly
                 air (OPEN of 729: a real cave) - at most MAXB slices. Each slice plugs the lava of the next before it is cut.
  THE LANDING    where the road breaks into the open cave: its floor runs on 5 blocks as a parapeted landing, and if the cave
                 floor is lower, a column of twisting vines (age 25: they never grow) climbs from it up to the landing.
                 A marker (bm.uroadend, bm.uroad_e / _s) stands at the landing's end; #ubore_e / #ubore_s bm.p2 count the
                 slices bored and #ubopen_e / #ubopen_s are 1 if the road found open air (0: it ran its length in solid rock;
                 2: the forecourt itself was open to a cave beside it - a way is cut through to that, and nothing bored).
                 /function bm:admin/under/approach reports both.

tools/verify_approach.py runs these very functions (a small interpreter of the commands below) on the built template set in
sample terrains - solid rock with lava pockets, a lava lake against the forecourt, all open, noise caves, solid all round -
and proves the walk from open Nether air to the Hidden Gate, the landings, and that no lava touches what was cut."""
import p2.undercfg as U
from p2.dungeons import undercrown as UC

OX, OY, OZ = U.ORIGIN
NETHER = 'minecraft:the_nether'
Y = UC.MAW_Y                        # the court's walk (local)
H = 14                              # the road's height (air y Y..Y+H)
MAXB = 112                          # slices a road may bore (7 chunks) before it gives up
PROBE = 9                           # the open-air probe ahead: PROBE x PROBE x PROBE
OPEN = 330                          # ...air cells of its 729 that count as open (45%)
SHELL = 3                           # the lava shell's depth round a forecourt
# per mouth: the axis the road runs along (+), the forecourt (local x1,y1,z1,x2,y2,z2), the road's interior across the axis
# (a1, a2), the first bored slice (along the axis)
WAYS = {'e': dict(ax='x', box=(224, Y, 174, 263, Y + 34, 214), road=(189, 199), start=264),
        's': dict(ax='z', box=(194, Y, 224, 234, Y + 31, 263), road=(207, 220), start=264)}
CONTAIN = 'bm:u_contain'            # (a block tag: what the shells and the bore's plugs turn to blackstone)
CAMPFIRE = 'minecraft:soul_campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]'
LIMIT = 32768                       # a fill's block limit


def w(x, y, z):
    return OX + x, OY + y, OZ + z


def fills(x1, y1, z1, x2, y2, z2, block, tail=''):
    """fill commands for a box of any size (local coords), cut along y into pieces under the block limit"""
    x1, x2 = sorted((x1, x2)); y1, y2 = sorted((y1, y2)); z1, z2 = sorted((z1, z2))
    per = max(1, LIMIT // ((x2 - x1 + 1) * (z2 - z1 + 1)))
    out = []
    for ya in range(y1, y2 + 1, per):
        yb = min(y2, ya + per - 1)
        a, b = w(x1, ya, z1), w(x2, yb, z2)
        out.append(f'fill {a[0]} {a[1]} {a[2]} {b[0]} {b[1]} {b[2]} {block}' + (f' {tail}' if tail else ''))
    return out


def _wall(ax):
    a = 'east=low,west=low,north=none,south=none' if ax == 'x' else 'east=none,west=none,north=low,south=low'
    return f'minecraft:polished_blackstone_brick_wall[{a},up=false,waterlogged=false]'


def forecourt(k):
    """the forecourt before mouth k: its lava shell, the cavity, the floor, the way, the light"""
    c = WAYS[k]; ax = c['ax']
    x1, y1, z1, x2, y2, z2 = c['box']
    a1, a2 = c['road']; am = (a1 + a2) // 2
    out = []
    # the shell - into the template's own face too, for the cells it leaves to the Nether (none of its own there is lava or
    # gravel: tools/verify_approach checks)
    out += fills(x1 - SHELL, y1 - SHELL - 1, z1 - SHELL, x2 + SHELL, y2 + SHELL, z2 + SHELL, 'minecraft:blackstone', f'replace #{CONTAIN}')
    out += fills(x1, y1, z1, x2, y2, z2, 'minecraft:air')
    # the floor, and three courses of footing under it wherever there's nothing (or lava)
    out += fills(x1, y1 - 1, z1, x2, y1 - 1, z2, 'minecraft:polished_blackstone')
    out += fills(x1, y1 - 4, z1, x2, y1 - 2, z2, 'minecraft:blackstone', 'replace #bm:grap_pass')
    # the processional way down its middle (the road's width, red down the centre)
    if ax == 'x':
        out += fills(x1, y1 - 1, a1, x2, y1 - 1, a2, 'minecraft:polished_blackstone_bricks')
        out += fills(x1, y1 - 1, am, x2, y1 - 1, am, 'minecraft:red_nether_bricks')
    else:
        out += fills(a1, y1 - 1, z1, a2, y1 - 1, z2, 'minecraft:polished_blackstone_bricks')
        out += fills(am, y1 - 1, z1, am, y1 - 1, z2, 'minecraft:red_nether_bricks')
    # soul-fire braziers either side of the way, every 12 along it
    along = range(x1 + 4, x2, 12) if ax == 'x' else range(z1 + 4, z2, 12)
    for u in along:
        for v in (a1 - 3, a2 + 3):
            x, z = (u, v) if ax == 'x' else (v, u)
            p, q = w(x, y1, z), w(x, y1 + 1, z)
            out += [f'setblock {p[0]} {p[1]} {p[2]} minecraft:polished_blackstone_bricks', f'setblock {q[0]} {q[1]} {q[2]} {CAMPFIRE}']
    # light hung through the cavity (invisible light blocks), every 8
    for x in range(x1 + 3, x2, 8):
        for z in range(z1 + 3, z2, 8):
            for yy in (y1 + 7, y1 + 17):
                p = w(x, yy, z)
                out.append(f'setblock {p[0]} {p[1]} {p[2]} minecraft:light[level=15,waterlogged=false]')
    return out


def bore(fn, k):
    """the road out of forecourt k, bored a slice at a time until it breaks into open air (functions p237/appr/<k>_*)"""
    c = WAYS[k]; ax = c['ax']
    a1, a2 = c['road']; am = (a1 + a2) // 2
    WY = OY + Y
    A = lambda a: (OZ if ax == 'x' else OX) + a          # across the axis: world
    # (positions: along the axis relative (~), across it and up absolute)
    def P(along, y, across, mid=False):
        a = A(across) + (0.5 if mid else 0)
        return f'~{along or ""} {y} {a}' if ax == 'x' else f'{a} {y} ~{along or ""}'
    def box(al1, y1, ac1, al2, y2, ac2):
        return f'{P(al1, y1, ac1)} {P(al2, y2, ac2)}'
    step = 'positioned ~1 ~ ~' if ax == 'x' else 'positioned ~ ~ ~1'
    pre = f'p237/appr/{k}'
    h = PROBE // 2
    # (first: is the forecourt itself already open to a cave beside it? then a way is cut through to it, and nothing bored)
    x1, _y1, z1, x2, _y2, z2 = c['box']
    u1, u2, v1, v2 = (x1, x2, z1, z2) if ax == 'x' else (z1, z2, x1, x2)
    sides = [(u, v) for u in (u1 + 4, (u1 + u2) // 2 - 4, u2 - 12) for v in (v1 - PROBE, v2 + 1)]
    def wbox(u, v, y1, y2, du=PROBE - 1, dv=PROBE - 1):
        (xa, za), (xb, zb) = ((u, v), (u + du, v + dv)) if ax == 'x' else ((v, u), (v + dv, u + du))
        a, b = w(xa, y1 - OY, za), w(xb, y2 - OY, zb)
        return f'{a[0]} {a[1]} {a[2]} {b[0]} {b[1]} {b[2]}'
    go = ['scoreboard players set #bn bm.rng 0', f'scoreboard players set #ubopen_{k} bm.p2 0']
    for i, (u, v) in enumerate(sides):
        go += [f'execute store result score #ba bm.rng run fill {wbox(u, v, WY, WY + PROBE - 1)} minecraft:structure_void replace #minecraft:air strict',
               f'fill {wbox(u, v, WY, WY + PROBE - 1)} minecraft:air replace minecraft:structure_void strict',
               f'execute if score #ba bm.rng matches {OPEN}.. run return run function bm:{pre}_side{i}']
        out_v = v if v < v1 else v + PROBE - 1                     # (the cut's outer end, across the axis)
        mid = w(u + PROBE // 2, Y, out_v) if ax == 'x' else w(out_v, Y, u + PROBE // 2)
        far = w(u + PROBE // 2, Y, out_v + (1 if v > v1 else -1)) if ax == 'x' else w(out_v + (1 if v > v1 else -1), Y, u + PROBE // 2)
        lo, hi = (v, v1 - 1) if v < v1 else (v2 + 1, v + PROBE - 1)
        fn(f'{pre}_side{i}', [f'scoreboard players set #ubopen_{k} bm.p2 2', f'scoreboard players set #ubore_{k} bm.p2 0',
                              f'fill {wbox(u - 1, lo - 1, WY - 2, WY + 7, PROBE + 1, hi - lo + 2)} minecraft:blackstone replace minecraft:lava',
                              f'fill {wbox(u, lo, WY, WY + 5, PROBE - 1, hi - lo)} minecraft:air',
                              f'fill {wbox(u, lo, WY - 1, WY - 1, PROBE - 1, hi - lo)} minecraft:polished_blackstone replace #bm:grap_pass',
                              f'summon minecraft:marker {mid[0] + 0.5} {mid[1]} {mid[2] + 0.5} {{Tags:["bm.uroadend","bm.uroad_{k}","bm.p2"]}}',
                              f'execute positioned {far[0] + 0.5} {far[1] - 1} {far[2] + 0.5} run function bm:p237/appr/drop'])
    fn(f'{pre}_go', go + [f'function bm:{pre}_step', f'scoreboard players operation #ubore_{k} bm.p2 = #bn bm.rng'])
    fn(f'{pre}_step', [f'execute store result score #ba bm.rng run fill {box(1, WY, am - h, PROBE, WY + PROBE - 1, am + h)} minecraft:structure_void replace #minecraft:air strict',
                       f'fill {box(1, WY, am - h, PROBE, WY + PROBE - 1, am + h)} minecraft:air replace minecraft:structure_void strict',
                       f'execute if score #ba bm.rng matches {OPEN}.. run return run function bm:{pre}_done',
                       f'execute if score #bn bm.rng matches {MAXB}.. run return run function bm:{pre}_end',
                       'scoreboard players add #bn bm.rng 1',
                       f'execute {step} run function bm:{pre}_slice',
                       f'execute {step} run function bm:{pre}_step'])
    fn(f'{pre}_slice', ['scoreboard players operation #bl bm.rng = #bn bm.rng', 'scoreboard players operation #bl bm.rng %= #6 bm.rng',
                        # (this slice and the next: lava and loose gravel plugged before anything is cut)
                        f'fill {box(0, WY - 2, a1 - 1, 1, WY + H + 2, a2 + 1)} minecraft:blackstone replace #{CONTAIN}',
                        f'fill {box(0, WY, a1, 0, WY + H, a2)} minecraft:air',
                        f'fill {box(0, WY - 1, a1, 0, WY - 1, a2)} minecraft:polished_blackstone_bricks',
                        f'setblock {P(0, WY - 1, am)} minecraft:red_nether_bricks',
                        f'fill {box(0, WY - 2, a1, 0, WY - 2, a2)} minecraft:blackstone replace #bm:grap_pass',
                        f'fill {box(0, WY - 1, a1 - 1, 0, WY + H + 1, a1 - 1)} minecraft:polished_blackstone_bricks',
                        f'fill {box(0, WY - 1, a2 + 1, 0, WY + H + 1, a2 + 1)} minecraft:polished_blackstone_bricks',
                        f'execute if score #bl bm.rng matches 3 run function bm:{pre}_lamp'])
    fn(f'{pre}_lamp', [l for v in (a1 + 1, a2 - 1) for l in (f'fill {box(0, WY + H - 3, v, 0, WY + H, v)} minecraft:iron_chain',
                                                              f'setblock {P(0, WY + H - 4, v)} minecraft:soul_lantern[hanging=true,waterlogged=false]')])
    # (broke into the open: a landing 5 on, parapets either side, the climb down if the cave floor is lower, the marker)
    fn(f'{pre}_done', [f'scoreboard players set #ubopen_{k} bm.p2 1',
                       f'fill {box(1, WY - 2, a1 - 1, 6, WY + 5, a2 + 1)} minecraft:blackstone replace minecraft:lava',
                       f'fill {box(1, WY, a1, 5, WY + 4, a2)} minecraft:air',
                       f'fill {box(1, WY - 1, a1, 5, WY - 1, a2)} minecraft:polished_blackstone_bricks replace #bm:grap_pass',
                       f'fill {box(1, WY - 1, am, 5, WY - 1, am)} minecraft:red_nether_bricks',
                       f'fill {box(1, WY, a1 - 1, 5, WY, a1 - 1)} {_wall(ax)} replace #bm:grap_pass',
                       f'fill {box(1, WY, a2 + 1, 5, WY, a2 + 1)} {_wall(ax)} replace #bm:grap_pass',
                       f'summon minecraft:marker {P(5, WY, am, True)} {{Tags:["bm.uroadend","bm.uroad_{k}","bm.p2"]}}',
                       f'execute positioned {P(6, WY - 1, am)} run function bm:p237/appr/drop'])
    fn(f'{pre}_end', [f'scoreboard players set #ubopen_{k} bm.p2 0',
                      f'summon minecraft:marker {P(0, WY, am, True)} {{Tags:["bm.uroadend","bm.uroad_{k}","bm.p2"]}}'])
    return WAYS[k]['start'] - 1


def generate(G):
    """the approach's functions, its tag, its scores; returns the lines of p237/build/roads"""
    fn, wjson = G.fn, G.wjson
    wjson(f'bm/tags/block/{CONTAIN.split(":")[1]}.json', {'values': ['minecraft:lava', 'minecraft:gravel']})
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #6 bm.rng 6']
    return lines(fn)


def lines(fn):
    """(G-free, for tools/verify_approach.py too) every function of the approach through fn; the lines of p237/build/roads"""
    # the climb down from a landing: down through anything passable to the first solid block (lava: a blackstone foot)
    fn('p237/appr/drop', ['scoreboard players set #bd bm.rng 0', 'function bm:p237/appr/down'])
    fn('p237/appr/down', ['execute if block ~ ~ ~ minecraft:lava run return run function bm:p237/appr/foot',
                          'execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p237/appr/vines',
                          'scoreboard players add #bd bm.rng 1', 'execute if score #bd bm.rng matches 72.. run return 0',
                          'execute positioned ~ ~-1 ~ run function bm:p237/appr/down'])
    fn('p237/appr/foot', ['setblock ~ ~ ~ minecraft:blackstone', 'function bm:p237/appr/vines'])
    fn('p237/appr/vines', ['execute if score #bd bm.rng matches 0 run return 0',
                           f'fill ~ ~1 ~ ~ {OY + Y - 1} ~ minecraft:twisting_vines_plant strict',
                           f'setblock ~ {OY + Y} ~ minecraft:twisting_vines[age=25] strict'])
    out = [f'kill @e[type=minecraft:marker,tag=bm.uroadend]']
    for k in WAYS: out += forecourt(k)
    for k in WAYS:
        s = bore(fn, k)
        a1, a2 = WAYS[k]['road']; am = (a1 + a2) // 2
        x, y, z = w(s, Y, am) if WAYS[k]['ax'] == 'x' else w(am, Y, s)
        out.append(f'execute positioned {x + 0.5} {y} {z + 0.5} run function bm:p237/appr/{k}_go')
    return [f'execute in {NETHER} run {l}' for l in out]


def report(fn, tellraw, T, P):
    fn('admin/under/approach', [tellraw('@s', P + [T('The way to the Maw: ', '#c8a0a0', bold=True)])] +
       [tellraw('@s', [T(f'  {nm} road: ', 'gray'), {'score': {'name': f'#ubore_{k}', 'objective': 'bm.p2'}, 'color': 'white'}, T(' slices bored; ', 'gray'),
                       {'score': {'name': f'#ubopen_{k}', 'objective': 'bm.p2'}, 'color': 'white'}, T(' (1: it broke into open air, 0: solid all the way)', 'gray')])
        for k, nm in (('e', 'east'), ('s', 'south'))] +
       ['tag @s add bm.uapr',
        f'execute in {NETHER} as @e[type=minecraft:marker,tag=bm.uroadend] run ' + tellraw('@a[tag=bm.uapr]', [T('  a road\'s end: ', 'gray'), {'nbt': 'Pos', 'entity': '@s', 'color': 'white'}]),
        'tag @s remove bm.uapr'])


def forceload():
    """(world) the strips the forecourts and the roads may reach, beyond the template's own forceload; and a far corner of each"""
    e = (OX + 216, OZ + 168, OX + WAYS['e']['start'] + MAXB + PROBE + 8, OZ + 220)
    s = (OX + 186, OZ + 216, OX + 242, OZ + WAYS['s']['start'] + MAXB + PROBE + 8)
    return [e, s], [(e[2], e[3]), (s[2], s[3]), (e[2], e[1]), (s[0], s[3])]

"""Phase 151 (2.80): THE HEIST'S CLIMAX - the vault's guardian makes an entrance, and its fall opens the vault as an event.

- THE GUARDIAN RISES (3 s, frozen till it's done): the hall goes dark, a bell tolls; coins and gold dust whirl in to the
  middle of the hall; the guardian rises out of the floor, growing as it comes; a flash, its roar, the hall shaking -
  and then its name on everyone's screen. (No health buffer for it: a Tier V guardian can stand near the game's 1024 cap
  on health, so it dies as it always has - the climax is what follows.)
- THE VAULT OPENS (2.5 s, instead of a gold wall blinking out): the guardian's fall shakes the hall; the great gold door
  rumbles, then parts from the middle outward, one column at a time, gold dust and chains; light floods out of the
  treasury over the crew; the fanfare; then "The vault is open" and the way to the strongbox.

Importing does nothing; generate(G) runs after phase149 (the staging kit is installed there) and the vault's own phases."""
import math
import cine as C
from cine import at as _at
from phase70_rooms import rel

A = 'bm.cat'
a = lambda t, *c: _at(A, t, *c)
snd, stack = C.snd, C.stack
GOLD = (1.0, 0.82, 0.3)
F = 'force @a[distance=..64]'
DEEP = 3.0


def generate(G):
    fn = G.fn
    from items import T
    from nbt import snbt

    # ================================================================== THE GUARDIAN RISES
    sp = G.FUNCS['p70/boss/spawn']
    i = sp.index('tag @e[tag=bm.gvbnew] remove bm.gvbnew')
    sp.insert(i, 'execute as @e[tag=bm.gvbnew,limit=1] at @s run function bm:cine/gv/start')
    drop = ('particle minecraft:explosion_emitter', 'playsound minecraft:entity.ravager.roar')
    G.FUNCS['p70/boss/spawn'] = [l for l in sp if not l.startswith(drop) and 'The vault\'s guardian wakes' not in l]
    fn('cine/gv/start', ['function bm:cine/arr/start', 'kill @e[type=minecraft:marker,tag=bm.cspot_gv,distance=..4]',
                         'summon minecraft:marker ~ ~ ~ {Tags:["bm.cspot_gv"]}',
                         'attribute @s minecraft:scale modifier add bm:cine_grow -0.7 add_multiplied_total', f'tp @s ~ ~-{DEEP} ~'])
    up = [(18, 50, DEEP, C.ease_out)]
    gr = lambda t: DEEP - C.offset(up, t - 1)
    arr = [*a(1, 'effect give @a[tag=bm.gvp,distance=..40] minecraft:darkness 3 0 true',
              *stack(('block.bell.resonate', 2, 0.5), ('block.respawn_anchor.charge', 1.4, 0.5), ('ambient.cave', 1.2, 0.5), r=48)),
           *a(14, snd('block.bell.use', 2, 0.4, 48)), *a(28, snd('block.bell.use', 2, 0.45, 48))]
    for t in range(1, 52):                              # coins and gold dust whirled in to the middle
        rr = 7 - 5.5 * C.ease(t / 51)
        for arm in range(3):
            th = t * 0.36 + arm * 2.094
            x, z = rr * math.cos(th), rr * math.sin(th)
            y = gr(t) + 0.3 + (t % 12) / 12 * 2.2
            arr += a(t, f'particle minecraft:dust{{color:[{GOLD[0]},{GOLD[1]},{GOLD[2]}],scale:1.8}} ~{x:.2f} ~{y:.2f} ~{z:.2f} 0.1 0.1 0.1 0 1 {F}')
            if t % 3 == 0:
                arr += a(t, f'particle minecraft:item{{item:"minecraft:gold_nugget"}} ~{x:.2f} ~{y:.2f} ~{z:.2f} 0.05 0.05 0.05 0.02 1 {F}')
    for t in range(18, 51):
        arr += a(t, f'particle minecraft:block{{block_state:"minecraft:gilded_blackstone"}} ~ ~{gr(t) + 0.1:.2f} ~ 0.8 0.1 0.8 0.1 5 {F}')
    arr += [*C.rise(A, *up[0]), *C.grow(A, 18, 52, 0.3, 1.0), *C.shake(A, 16, 34, 0.45, seed=51),
            *a(18, *stack(('block.stone.break', 2, 0.5), ('entity.warden.emerge', 1.0, 0.8), r=48)),
            *a(52, 'execute positioned as @e[type=minecraft:marker,tag=bm.cspot_gv,sort=nearest,limit=1] run tp @s ~ ~ ~',
               'kill @e[type=minecraft:marker,tag=bm.cspot_gv,sort=nearest,limit=1]',
               f'particle minecraft:flash{{color:[{GOLD[0]},{GOLD[1]},{GOLD[2]},1.0]}} ~ ~1.5 ~ 0 0 0 0 1 {F}',
               'particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1',
               f'particle minecraft:item{{item:"minecraft:gold_nugget"}} ~ ~1.5 ~ 1.5 1 1.5 0.3 80 {F}',
               *stack(('entity.ravager.roar', 1.6, 0.6), ('entity.generic.explode', 1, 0.6), ('block.bell.use', 2, 0.35), r=48)),
            *a(52, *C.ring('minecraft:dust{color:[1.0,0.82,0.3],scale:2.0}', 3, 28, 0.15)),
            *a(55, *C.ring('minecraft:dust{color:[1.0,0.82,0.3],scale:2.0}', 6, 40, 0.15)),
            *C.shake(A, 52, 12, 1.6),
            *a(54, 'title @a[tag=bm.gvp,distance=..40] times 6 50 16',
               'title @a[tag=bm.gvp,distance=..40] subtitle ' + snbt(T('Bring it down, and the vault is yours', 'gray', italic=True)),
               'title @a[tag=bm.gvp,distance=..40] title ' + snbt(T("The vault's guardian wakes", '#ffcf40', bold=True)))]
    C.stage(G, 'gv', None, 'bm.gvboss', arr, None, None, arrive_len=62, arm=False)
    C.gate(G, ['p70/boss/sec'])
    G.FUNCS['loop/second'].append('execute unless entity @e[tag=bm.gvboss,tag=bm.carr] run kill @e[type=minecraft:marker,tag=bm.cspot_gv]')
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:marker,tag=bm.cspot_gv]']

    # ================================================================== THE VAULT OPENS
    op = G.FUNCS['p70/r/vault/open']
    assert op[0] == 'scoreboard players set @s bm.gvs 2', op[0]
    door = [l for l in op if l.startswith('fill ') and 'replace minecraft:gold_block' in l]
    assert len(door) == 1, door
    rest = [l for l in op[1:] if l not in door and not l.startswith(('particle minecraft:wax_on', 'playsound minecraft:block.iron_door.open',
                                                                       'playsound minecraft:ui.toast.challenge_complete'))]
    fn('p70/r/vault/opened', rest)
    fn('p70/r/vault/open', ['scoreboard players set @s bm.gvs 2', 'scoreboard players set @s bm.cvt 0', 'tag @s add bm.cvault'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.cvt dummy']
    G.OBJECTIVES.append('bm.cvt')
    v = lambda t, *c: _at('bm.cvt', t, *c)
    D = rel(24, 6, 12)                                  # (the door's middle, from the vault room's marker)
    tl = [*v(1, f'particle minecraft:flash{{color:[{GOLD[0]},{GOLD[1]},{GOLD[2]},1.0]}} ~ ~1.5 ~ 0 0 0 0 1 {F}',
             f'particle minecraft:item{{item:"minecraft:gold_nugget"}} ~ ~1.5 ~ 3 1 3 0.25 120 {F}',
             *stack(('entity.wither.death', 0.5, 0.8), ('entity.generic.explode', 1.2, 0.6), ('block.bell.use', 2, 0.5), r=60)),
          *C.shake('bm.cvt', 1, 10, 1.2, r=60),
          *v('4..14', f'particle minecraft:dust{{color:[{GOLD[0]},{GOLD[1]},{GOLD[2]}],scale:1.5}} {D} 0.2 1.6 2.6 0 6 {F}'),
          *v(6, snd('block.chain.break', 2, 0.5, 60), snd('block.piston.contract', 1.6, 0.5, 60)),
          *C.shake('bm.cvt', 6, 10, 0.4, r=60, seed=9)]
    for n, (t, zs) in enumerate(((15, (12,)), (21, (11, 13)), (27, (10, 14)), (33, (9, 15)))):     # the door parts from the middle
        tl += v(t, *[f'fill {rel(24, 4, z)} {rel(24, 8, z)} minecraft:air replace minecraft:gold_block' for z in zs],
                *[f'particle minecraft:block{{block_state:"minecraft:gold_block"}} {rel(24, 6, z)} 0.2 1.4 0.2 0.1 40 {F}' for z in zs],
                snd('block.iron_door.open', 1.6, 0.5 + 0.12 * n, 60), snd('block.chain.break', 1.6, 0.6 + 0.1 * n, 60),
                snd('block.piston.contract', 1.2, 0.6 + 0.1 * n, 60))
    tl += [*v('34..44', f'particle minecraft:end_rod {D} 0.2 1.5 2.5 0.12 6 {F}', f'particle minecraft:wax_on {D} 0.4 1.6 2.8 0 6 {F}'),
           *v(36, *stack(('ui.toast.challenge_complete', 1.4, 1), ('entity.player.levelup', 1.2, 0.7), ('block.amethyst_block.resonate', 1.5, 0.8), r=60),
              f'fill {rel(24, 4, 9)} {rel(24, 8, 15)} minecraft:air replace minecraft:gold_block',
              'function bm:p70/r/vault/opened'),
           *v(50, 'tag @s remove bm.cvault')]
    fn('cine/vault/door', ['scoreboard players add @s bm.cvt 1'] + tl)
    G.FUNCS['tick'].append('execute as @e[type=minecraft:marker,tag=bm.cvault] at @s run function bm:cine/vault/door')
    G.FUNCS['admin/uninstall'][0:0] = ['tag @e remove bm.cvault']

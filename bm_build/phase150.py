"""Phase 150 (2.80): THE DUNGEON BOSSES, STAGED - the seven bosses of the conquest dungeons (the Broodmother, the Frost
Marksman, the Drowned Tyrant, the Archmage, Bobbery, the Hollow King and the Golden Goose) given what the roaming bosses
got from the staging kit (cine.py). Their intros already build the dread (the sounds, the line, the title card); now:

- each MATERIALISES where it used to simply appear: its own colours drawn in out of the arena into a column, the boss
  growing out of it from a tenth of its size, a flash, a roar, the floor shaking - and only then does it move (2 s);
- each DIES as a sequence (4 s) instead of falling over: the Broodmother curls up and bursts into silk; the Frost
  Marksman freezes solid and shatters; the Drowned Tyrant sinks into a whirlpool; the Archmage's mirror-images flicker
  out and he blinks away for good; Bobbery drops to his knees and burns away in soul fire; the Hollow King falls to one
  knee as his crown flares (and then he rises again, as before); the Golden Goose goes off like a jackpot. Then it falls
  as the kill of the player who brought it down - its loot, the victory and the conquest as before;
- its rage is a moment (it freezes, the arena shakes, its colours burst);
- its instant blows are telegraphed: the Tyrant's slam (a ring of water at its reach), Bobbery's cleave (a ring of soul
  fire), the Archmage's lances (the air crackling round his targets), the Broodmother's spit (a hiss and a gather), the
  Marksman's hail (frost forming over each head), the Hollow King's decree (the dark drawn in to him).

Importing does nothing; generate(G) runs after phase149 (the kit is installed there)."""
import math
import re
import cine as C
from cine import at as _at

A, D, R = 'bm.cat', 'bm.cdt', 'bm.crt'
a = lambda t, *c: _at(A, t, *c)
d = lambda t, *c: _at(D, t, *c)
r_ = lambda t, *c: _at(R, t, *c)
snd, stack = C.snd, C.stack
F = 'force @a[distance=..96]'

# d: entity, its colour (dust rgb), its own particle, the sounds of its death, how it dies
DG = {
    'brood': ('spider', (0.85, 0.85, 0.8), 'minecraft:white_ash', ('entity.spider.death', 'entity.spider.hurt'), 'curl'),
    'frost': ('stray', (0.65, 0.9, 1.0), 'minecraft:snowflake', ('entity.stray.death', 'block.glass.break'), 'freeze'),
    'tide': ('drowned', (0.25, 0.6, 0.75), 'minecraft:bubble_pop', ('entity.drowned.death', 'entity.elder_guardian.death'), 'sink'),
    'hex': ('evoker', (0.6, 0.25, 0.85), 'minecraft:witch', ('entity.evoker.death', 'entity.illusioner.mirror_move'), 'blink'),
    'keep': ('wither_skeleton', (0.75, 0.15, 0.15), 'minecraft:soul_fire_flame', ('entity.wither_skeleton.death', 'entity.wither.hurt'), 'kneel'),
    'hollow': ('wither_skeleton', (0.85, 0.85, 0.9), 'minecraft:sculk_soul', ('entity.wither_skeleton.death', 'entity.warden.death'), 'kneel'),
    'lucky': ('chicken', (1.0, 0.82, 0.2), 'minecraft:wax_on', ('entity.chicken.death', 'block.amethyst_block.break'), 'jackpot'),
}
ENRAGE = {'brood': ['p2/brood/enrage'], 'frost': ['p2/frost/enrage'], 'tide': ['p2/tide/enrage'], 'hex': ['p2/hex/enrage'],
          'keep': ['p2/keep/wilfrey', 'p2/keep/enough'], 'lucky': ['p2/lucky/double']}


def dust(rgb, sc=1.6):
    return f'minecraft:dust{{color:[{rgb[0]},{rgb[1]},{rgb[2]}],scale:{sc}}}'


def generate(G):
    fn = G.fn
    fams = []
    for dn, (ent, rgb, part, (s_die, s_hurt), how) in DG.items():
        if f'p2/{dn}/boss_spawn' not in G.FUNCS:
            continue
        kind = f'd_{dn}'
        tag = f'bm.boss_{dn}'
        m = re.search(r'minecraft:scale",base:([\d.]+)d', ' '.join(G.FUNCS[f'p2/{dn}/boss_spawn']))
        sc = float(m.group(1)) if m else 1.0
        fams.append(f'p2/{dn}/')
        # ---- the fight begins with it materialising (the intro has run; it has just been summoned)
        fb = G.FUNCS[f'p2/{dn}/fight_begin']
        i = next(j for j, l in enumerate(fb) if 'bm:p2/boss/init_scores' in l)
        fb.insert(i, f'execute as @e[tag=bm.newboss,tag={tag},distance=..80] at @s run function bm:cine/{kind}/start')
        fn(f'cine/{kind}/start', ['function bm:cine/arr/start', f'attribute @s minecraft:scale base set {sc * 0.1:.3f}'])
        arr = [*a(1, f'particle minecraft:flash{{color:[{rgb[0]},{rgb[1]},{rgb[2]},1.0]}} ~ ~0.3 ~ 0 0 0 0 1 {F}',
                  *stack(('block.respawn_anchor.charge', 1.4, 0.5), ('block.beacon.power_select', 1.2, 0.6), (s_hurt, 1.2, 0.5)))]
        for t in range(1, 34, 2):                      # its colours drawn in out of the arena
            arr += a(t, *C.converge(dust(rgb, 2.0), 7 - t / 6, 14, 0.4 + t / 12, 0.35), *C.converge(part, 6 - t / 7, 10, 1.2, 0.3)[::2])
        arr += a('4..36', f'particle {part} ~ ~{sc} ~ 0.25 {sc * 0.8:.2f} 0.25 0.02 4 {F}',
                 f'particle {dust(rgb, 1.2)} ~ ~{sc * 0.6:.2f} ~ 0.3 {sc * 0.6:.2f} 0.3 0 3 {F}')
        arr += [*C.scale_tween(A, 6, 36, sc * 0.1, sc, C.ease_out), *C.shake(A, 8, 28, 0.35, seed=31),
                *a(37, f'particle minecraft:flash{{color:[{rgb[0]},{rgb[1]},{rgb[2]},1.0]}} ~ ~{sc:.2f} ~ 0 0 0 0 1 {F}',
                   f'particle {part} ~ ~{sc * 0.8:.2f} ~ 1.2 {sc * 0.7:.2f} 1.2 0.15 120 {F}',
                   *stack(('entity.ravager.roar', 1.6, 0.6), (s_hurt, 2, 0.4), ('entity.generic.explode', 0.8, 0.7))),
                *a(37, *C.ring(dust(rgb, 2.0), 3, 28, 0.15)), *a(39, *C.ring(dust(rgb, 2.0), 5, 36, 0.15)), *a(41, *C.ring(dust(rgb, 2.0), 7, 44, 0.15)),
                *C.shake(A, 37, 10, 1.4)]
        # ---- its death
        die = [*d(1, f'bossbar set bm:boss_{dn} visible false',
                  *stack((s_die, 2, 0.5), (s_hurt, 2, 0.4), ('entity.wither.hurt', 0.8, 0.6)),
                  f'particle minecraft:flash{{color:[{rgb[0]},{rgb[1]},{rgb[2]},1.0]}} ~ ~{sc:.2f} ~ 0 0 0 0 1 {F}',
                  f'summon minecraft:marker ~ ~ ~ {{Tags:["bm.cpos_d","bm.cpos_{dn}"]}}'),
               *C.shake(D, 1, 8, 1.0),
               *d('2..70', f'particle {part} ~ ~{sc * 0.8:.2f} ~ {0.3 * sc:.2f} {0.5 * sc:.2f} {0.3 * sc:.2f} 0.03 4 {F}',
                  f'particle {dust(rgb)} ~ ~{sc * 0.8:.2f} ~ {0.3 * sc:.2f} {0.5 * sc:.2f} {0.3 * sc:.2f} 0 2 {F}'),
               *[l for t in range(8, 70, 12) for l in d(t, snd(s_hurt, 1.2, 0.4 + t / 200))]]
        P = f'@e[type=minecraft:marker,tag=bm.cpos_{dn},sort=nearest,limit=1]'
        if how == 'curl':          # the Broodmother curls up, shuddering, and bursts into silk
            die += [*C.scale_tween(D, 6, 66, sc, sc * 0.55, C.ease), *C.jitter(D, 10, 66, 0.08, 41),
                    *d(70, f'particle minecraft:item{{item:"minecraft:cobweb"}} ~ ~1 ~ 1.5 1 1.5 0.15 120 {F}', f'particle minecraft:white_ash ~ ~1 ~ 3 2 3 0 400 {F}',
                       *stack(('entity.turtle.egg_break', 2, 0.5), ('block.wool.break', 2, 0.6)))]
        elif how == 'freeze':      # the Marksman freezes solid (frost creeping up him), then shatters
            die += [*[l for t in range(4, 64, 3) for l in d(t, f'particle minecraft:snowflake ~ ~{sc * 0.1 + (t - 4) / 60 * sc * 1.6:.2f} ~ {0.3 * sc:.2f} 0.1 {0.3 * sc:.2f} 0 14 {F}',
                                                                f'particle minecraft:block{{block_state:"minecraft:packed_ice"}} ~ ~{(t - 4) / 60 * sc * 1.6:.2f} ~ {0.25 * sc:.2f} 0.1 {0.25 * sc:.2f} 0 4 {F}')],
                    *[l for t in range(10, 64, 9) for l in d(t, snd('block.glass.place', 1.4, 1.2 - t / 120))],
                    *d(66, f'particle minecraft:block{{block_state:"minecraft:packed_ice"}} ~ ~{sc:.2f} ~ 0.8 {sc * 0.6:.2f} 0.8 0.3 260 {F}',
                       f'particle minecraft:snowflake ~ ~{sc:.2f} ~ 1.5 1.5 1.5 0.2 160 {F}',
                       *stack(('block.glass.break', 2, 0.6), ('block.glass.break', 2, 0.9), ('entity.player.hurt_freeze', 2, 0.5))),
                    *C.shake(D, 66, 10, 1.6), *d(67, 'effect give @s minecraft:invisibility infinite 0 true')]
        elif how == 'sink':        # the Tyrant sinks into a whirlpool
            for t in range(4, 72, 2):
                rr = 3.2 - 2.4 * C.ease((t - 4) / 68)
                die += d(t, *[f'particle minecraft:splash ~{rr * math.cos(t * 0.3 + j * 2.094):.2f} ~0.2 ~{rr * math.sin(t * 0.3 + j * 2.094):.2f} 0.1 0.05 0.1 0.2 6 {F}' for j in range(3)])
            die += [*C.rise(D, 16, 70, -3.2, C.ease), *[l for t in range(10, 70, 10) for l in d(t, snd('ambient.underwater.enter', 1.2, 0.5))],
                    *d(72, f'execute at {P} run particle minecraft:splash ~ ~0.5 ~ 2 0.4 2 0.6 300 {F}', snd('entity.generic.splash', 2, 0.4))]
        elif how == 'blink':       # the Archmage's images flicker; he blinks about and is gone
            for t in range(6, 66, 8):
                die += d(t, f'particle minecraft:reverse_portal ~ ~1 ~ 0.4 1 0.4 0.1 30 {F}', snd('entity.illusioner.mirror_move', 1.4, 0.8 + t / 100),
                         f'execute at {P} rotated {t * 47 % 360} 0 run tp @s ^ ^ ^{1.5 + (t % 3)}')
            die += [*d(66, f'execute at {P} run tp @s ~ ~ ~', f'particle minecraft:totem_of_undying ~ ~1.5 ~ 0.6 1 0.6 0.4 120 {F}',
                       f'particle minecraft:witch ~ ~1.5 ~ 1 1 1 0.2 150 {F}', *stack(('entity.illusioner.cast_spell', 2, 0.6), ('entity.evoker.prepare_wololo', 1.5, 0.5))),
                    *C.scale_tween(D, 66, 74, sc, 0.05)]
        elif how == 'kneel':       # down on one knee, then burned / crumbled away
            die += [*C.rise(D, 6, 14, -0.45, C.ease), *d(6, snd('entity.iron_golem.damage', 1.5, 0.5), snd('block.anvil.land', 0.6, 0.5)),
                    *C.jitter(D, 16, 60, 0.05, 43),
                    *d('20..70', f'particle {part} ~ ~0.2 ~ {0.4 * sc:.2f} 0.05 {0.4 * sc:.2f} 0.02 6 {F}'),
                    *C.scale_tween(D, 50, 72, sc, sc * 0.3, lambda kk: kk * kk),
                    *d(72, f'particle minecraft:soul ~ ~1 ~ 0.8 1.2 0.8 0.05 80 {F}', f'particle {part} ~ ~1 ~ 1 1 1 0.1 100 {F}',
                       *stack(('block.fire.extinguish', 2, 0.5), ('particle.soul_escape', 2, 0.6))),
                    *d(74, f'execute at {P} run tp @s ~ ~ ~')]
            if dn == 'hollow':     # (the crown flares - and the throne answers: he rises again)
                die += d(30, f'execute anchored eyes run particle minecraft:end_rod ~ ~0.4 ~ 0.3 0.3 0.3 0.15 60 {F}', snd('block.beacon.deactivate', 2, 0.5),
                         'title @a[distance=..60] actionbar {text:"The Hollow King falls to one knee...",color:"#e5e4e2",italic:true}')
        elif how == 'jackpot':     # the Goose goes off like a jackpot
            die += [*C.jitter(D, 6, 60, 0.1, 47), *[l for t in range(8, 64, 6) for l in d(t, snd('block.note_block.chime', 1.5, 0.6 + t / 60))],
                    *C.scale_tween(D, 20, 66, sc, sc * 1.25, lambda kk: kk * kk),
                    *d(68, f'particle minecraft:item{{item:"minecraft:gold_nugget"}} ~ ~1.5 ~ 1.5 1 1.5 0.35 160 {F}',
                       f'particle minecraft:item{{item:"minecraft:feather"}} ~ ~1.5 ~ 1.5 1 1.5 0.2 80 {F}',
                       f'particle minecraft:firework ~ ~2 ~ 1 1 1 0.2 120 {F}',
                       *stack(('entity.firework_rocket.large_blast', 2, 0.8), ('block.amethyst_block.chime', 2, 1.4), ('entity.player.levelup', 1.5, 0.6))),
                    *C.shake(D, 68, 8, 1.2), *d(69, f'attribute @s minecraft:scale base set {sc:.3f}')]
        die += [*d(76, f'kill {P}')]
        rage = [*r_(1, *stack(('entity.ravager.roar', 2, 0.5), (s_hurt, 2, 0.4), ('entity.generic.explode', 0.8, 0.6))),
                *C.shake(R, 1, 10, 1.3), *r_(2, *C.ring(dust(rgb, 2.0), 3, 28, 0.2)), *r_(5, *C.ring(dust(rgb, 2.0), 6, 40, 0.2)),
                *r_('2..30', f'particle {part} ~ ~{sc * 0.8:.2f} ~ {0.5 * sc:.2f} {0.6 * sc:.2f} {0.5 * sc:.2f} 0.08 8 {F}')]
        C.stage(G, kind, ent, tag, arr, die, rage, arrive_len=45, die_len=80, rage_len=32)
        C.gate(G, [f'p2/{dn}/boss_tick'])
        for e in ENRAGE.get(dn, []):
            G.FUNCS[e].insert(0, 'function bm:cine/rage/start')
        # (the arena's bar reads the boss's true health)
        fl = G.FUNCS[f'p2/{dn}/fight']
        ib = [j for j, l in enumerate(fl) if l.startswith(f'execute store result bossbar bm:boss_{dn} value run data get entity @e[tag={tag},')]
        assert len(ib) == 1, (dn, ib)
        sel = fl[ib[0]].split(' run data get entity ')[1].rsplit(' Health', 1)[0]
        fl[ib[0]] = f'execute as {sel} run function bm:cine/bar {{b:"bm:boss_{dn}"}}'
    nb, ns = C.debuffer(G, [n for n in G.FUNCS if n.startswith(tuple(fams))])
    assert ns >= 6, ns
    G.FUNCS['loop/second'] += [f'execute as @e[type=minecraft:{v[0]},tag=bm.boss_{dn},tag=!bm.carm,tag=!bm.cfrz] run function bm:cine/arm'
                               for dn, v in DG.items() if f'p2/{dn}/boss_spawn' in G.FUNCS]
    G.FUNCS['loop/second'].append('execute unless entity @e[tag=bm.boss,tag=bm.cdie] run kill @e[type=minecraft:marker,tag=bm.cpos_d]')
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:marker,tag=bm.cpos_d]']
    windups(G)
    C.finish(G)


# ====================================================================== WIND-UPS: the instant blows, telegraphed
def windups(G):
    fn = G.fn
    each = lambda ticks, mk: [f'execute if score @s bm.cwu matches {t} run {l}' for t in range(ticks) for l in mk(t)]
    wu = {}
    # the Tyrant's slam (reach 6): a ring of water rising at its edge
    wu['p2/tide/slam'] = C.windup(G, 'd_tide', 'p2/tide/slam', 16,
        each(16, lambda t: C.ring_up('minecraft:splash', 6, 36, 0.1, 0.3) if t % 2 == 0 else []) +
        each(16, lambda t: C.ring(dust((0.25, 0.6, 0.75), 1.5), 6, 40, 0.15) if t % 4 == 0 else []),
        [snd('ambient.underwater.enter', 1.6, 0.6), snd('item.trident.riptide_1', 1.2, 0.5)])
    # Bobbery's cleave (reach 4.5): soul fire gathering round him
    wu['p2/keep/cleave'] = C.windup(G, 'd_keep', 'p2/keep/cleave', 14,
        each(14, lambda t: C.ring('minecraft:soul_fire_flame', 4.5, 30, 0.15) if t % 2 == 0 else []),
        [snd('item.axe.scrape', 2, 0.5), snd('entity.wither_skeleton.ambient', 1.5, 0.5)])
    # the Archmage's lances: the air crackling round whoever he is reading
    fn('cine/wu/hexmark', [f'particle minecraft:witch ~{1.0 * math.cos(k * 0.785):.2f} ~0.1 ~{1.0 * math.sin(k * 0.785):.2f} 0 0.3 0 0.05 1 force @s' for k in range(8)] +
       ['particle minecraft:enchant ~ ~2.2 ~ 0.3 0.3 0.3 0.5 6 force @s'])
    wu['p2/hex/lances'] = C.windup(G, 'd_hex', 'p2/hex/lances', 16,
        ['execute if score @s bm.cwu matches 0..15 as @a[tag=bm.ina_hex,distance=..64,gamemode=!spectator,gamemode=!creative] at @s run function bm:cine/wu/hexmark',
         'execute anchored eyes run particle minecraft:witch ^ ^ ^0.6 0.2 0.2 0.2 0.1 4 force @a[distance=..48]'],
        [snd('entity.evoker.prepare_attack', 2, 0.6), snd('entity.illusioner.prepare_blindness', 1.2, 0.8)])
    # the Broodmother's spit: a hiss and a gathering of silk
    wu['p2/brood/web_spit'] = C.windup(G, 'd_brood', 'p2/brood/web_spit', 12,
        ['particle minecraft:white_ash ~ ~1 ~ 1.5 0.6 1.5 0 10 force @a[distance=..48]', *C.converge('minecraft:white_ash', 4, 12, 1.0, 0.3)[::3]],
        [snd('entity.spider.ambient', 2, 0.4), snd('entity.llama.angry', 1, 0.5)])
    # the Marksman's hail: frost forming over each head
    fn('cine/wu/hailmark', ['particle minecraft:snowflake ~ ~4.5 ~ 0.7 0.1 0.7 0 6 force @s', 'particle minecraft:dust{color:[0.65,0.9,1.0],scale:1.2} ~ ~0.1 ~ 0.6 0 0.6 0 4 force @s'])
    wu['p2/frost/hail'] = C.windup(G, 'd_frost', 'p2/frost/hail', 16,
        ['execute as @a[tag=bm.ina_frost,distance=..64,gamemode=!spectator,gamemode=!creative] at @s run function bm:cine/wu/hailmark'],
        [snd('entity.skeleton.ambient', 1.5, 0.5), snd('block.powder_snow.step', 2, 0.6)])
    # the Hollow King's decree: the dark drawn in to him
    wu['p2/hollow/decree'] = C.windup(G, 'd_hollow', 'p2/hollow/decree', 20,
        [*each(20, lambda t: C.converge('minecraft:sculk_soul', 10 - t / 3, 18, 1.5, 0.45)[::2] if t % 2 == 0 else []),
         'execute anchored eyes run particle minecraft:end_rod ~ ~0.4 ~ 0.25 0.25 0.25 0.02 2 force @a[distance=..64]'],
        [snd('entity.warden.heartbeat', 2, 0.5), snd('block.sculk_shrieker.shriek', 1, 0.4)])
    for atk, target in wu.items():
        dn = atk.split('/')[1]
        n = C.hook_calls(G, [f'p2/{dn}/boss_tick'], atk, target)
        assert n >= 1, (atk, n)

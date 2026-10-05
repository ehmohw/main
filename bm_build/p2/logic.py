"""Phase 2 runtime logic, generated from each dungeon's build metadata.

Everything is driven by markers inside the structures (rotation-proof: elements are found by tag + distance,
gates/doors use symmetric fill boxes, secret doors are single columns).
  - Dungeon controller (bm.dg): puzzle progress in bm.pz, last-seen gametime in bm.seen (20-minute idle reset).
  - Puzzle controllers (bm.pz + bm.pzN): solved flag bm.done. A puzzle only accepts input while the dungeon's
    progress is exactly N-1; when it becomes current it is re-armed (reset), so nothing can be pre-solved.
  - Gates bm.gN open (animated, top-down) when puzzle N is solved. Battle doors (bm.adoor) seal the arena during a fight.
  - Altar (inside the arena): sneak with the key in hand; needs all puzzles solved + the conquest record.
"""
import math
from nbt import snbt, Byte, Byte as B_, F, Int
from items import T, ITEMS
from p2.config import D, ORDER, OPEN_LIGHT, ADOOR_LIGHT

R2 = lambda d: D[d]['radius'] * 2          # search radius for "same dungeon" lookups (instances are >500 blocks apart)

# per-dungeon flavour --------------------------------------------------------------------------------------------
FLAVOR = {
    'brood': dict(open='The silk curtain dissolves...', osnd='minecraft:block.wool.break', osnd2='minecraft:entity.spider.ambient',
                  block_part='minecraft:white_wool', tone='minecraft:block.note_block.didgeridoo',
                  fail=['execute at @p[distance=..24,gamemode=!creative,gamemode=!spectator] run summon minecraft:cave_spider ~ ~ ~ {Tags:["bm.seen","bm.dgmob"]}',
                        'effect give @a[distance=..16,gamemode=!creative,gamemode=!spectator] minecraft:poison 4 0'],
                  failmsg='The eggs burst! The brood stirs...', failsnd='minecraft:entity.spider.hurt',
                  trap=['effect give @s minecraft:poison 4 0', 'effect give @s minecraft:slowness 3 1'], trapmsg='The web gives way!'),
    'frost': dict(open='The ice cracks apart!', osnd='minecraft:block.glass.break', osnd2='minecraft:block.powder_snow.break',
                  block_part='minecraft:blue_ice', tone='minecraft:block.note_block.chime',
                  fail=['effect give @a[distance=..16,gamemode=!creative,gamemode=!spectator] minecraft:slowness 4 1',
                        'execute as @a[distance=..16,gamemode=!creative,gamemode=!spectator] run damage @s 2 minecraft:freeze'],
                  failmsg='Frost bites at your fingers. Wrong.', failsnd='minecraft:entity.player.hurt_freeze',
                  trap=['damage @s 3 minecraft:freeze', 'effect give @s minecraft:slowness 4 2'], trapmsg='The ice cracks beneath you!'),
    'tide': dict(open='The grate grinds open, water draining away...', osnd='minecraft:block.copper_grate.break', osnd2='minecraft:ambient.underwater.exit',
                 block_part='minecraft:waxed_oxidized_copper_grate', tone='minecraft:block.note_block.bell',
                 fail=['effect give @a[distance=..16,gamemode=!creative,gamemode=!spectator] minecraft:nausea 6 0',
                       'effect give @a[distance=..16,gamemode=!creative,gamemode=!spectator] minecraft:blindness 2 0'],
                 failmsg='The sea rejects your song.', failsnd='minecraft:entity.elder_guardian.curse',
                 trap=['effect give @s minecraft:nausea 5 0'], trapmsg='The floor floods!'),
    'hex': dict(open='The arcane barrier shatters!', osnd='minecraft:block.amethyst_block.break', osnd2='minecraft:entity.illusioner.cast_spell',
                block_part='minecraft:purple_stained_glass', tone='minecraft:block.note_block.flute',
                fail=['effect give @a[distance=..16,gamemode=!creative,gamemode=!spectator] minecraft:levitation 1 1',
                      'execute as @a[distance=..16,gamemode=!creative,gamemode=!spectator] run damage @s 2 minecraft:magic'],
                failmsg='A hex snaps back at you!', failsnd='minecraft:entity.evoker.cast_spell',
                trap=['effect give @s minecraft:levitation 1 2'], trapmsg='A glyph flares beneath you!'),
    'keep': dict(open='The iron gate grinds upward...', osnd='minecraft:block.chain.place', osnd2='minecraft:block.piston.contract',
                 block_part='minecraft:iron_block', tone='minecraft:block.note_block.bell',
                 fail=['execute as @a[distance=..16,gamemode=!creative,gamemode=!spectator] run damage @s 3 minecraft:magic',
                       'effect give @a[distance=..16,gamemode=!creative,gamemode=!spectator] minecraft:wither 2 0'],
                 failmsg='The keep punishes the unworthy.', failsnd='minecraft:entity.wither_skeleton.hurt',
                 trap=['damage @s 3 minecraft:hot_floor', 'effect give @s minecraft:slowness 2 1'], trapmsg='The floor burns!'),
    'hollow': dict(open='The deepslate seal sinks into the floor.', osnd='minecraft:block.respawn_anchor.deplete', osnd2='minecraft:entity.wither.ambient',
                   block_part='minecraft:reinforced_deepslate', tone='minecraft:block.note_block.iron_xylophone',
                   fail=['effect give @a[distance=..16,gamemode=!creative,gamemode=!spectator] minecraft:darkness 5 0',
                         'effect give @a[distance=..16,gamemode=!creative,gamemode=!spectator] minecraft:wither 3 0'],
                   failmsg='The Throne remembers your mistake.', failsnd='minecraft:entity.warden.sonic_charge',
                   trap=['effect give @s minecraft:wither 3 1', 'effect give @s minecraft:darkness 4 0'], trapmsg='The void reaches up!'),
    'lucky': dict(open='Jackpot! The golden gate swings open!', osnd='minecraft:block.amethyst_block.chime', osnd2='minecraft:entity.player.levelup',
                  block_part='minecraft:raw_gold_block', tone='minecraft:block.note_block.pling',
                  fail=['effect give @a[distance=..16,gamemode=!creative,gamemode=!spectator] minecraft:glowing 3 0'],
                  failmsg='Bawk! Wrong number.', failsnd='minecraft:entity.chicken.hurt',
                  trap=['effect give @s minecraft:slowness 2 0'], trapmsg='Unlucky tile!'),
}
# 2.13: puzzles get meaner the further along the conquest road they are - a wrong answer now also calls something up
_MOB = lambda ent, extra='': f'execute at @p[distance=..24,gamemode=!creative,gamemode=!spectator] run summon minecraft:{ent} ~ ~ ~ {{Tags:["bm.seen","bm.dgmob"]{extra}}}'
FLAVOR['frost']['fail'].append(_MOB('stray'))
FLAVOR['tide']['fail'].append(_MOB('drowned', ',equipment:{mainhand:{id:"minecraft:trident",count:1}},drop_chances:{mainhand:0.0f}'))
FLAVOR['hex']['fail'] += ['execute at @a[distance=..16,gamemode=!creative,gamemode=!spectator] run summon minecraft:evoker_fangs ~ ~ ~ {Warmup:10}',
                          _MOB('vindicator', ',equipment:{mainhand:{id:"minecraft:iron_axe",count:1}},drop_chances:{mainhand:0.0f}')]
FLAVOR['keep']['fail'] += [_MOB('wither_skeleton', ',equipment:{mainhand:{id:"minecraft:stone_sword",count:1}},drop_chances:{mainhand:0.0f}')]
FLAVOR['hollow']['fail'] += [_MOB('wither_skeleton', ',CustomName:{text:"Hollow Knight",color:"#8a96a8"},equipment:{mainhand:{id:"minecraft:netherite_sword",count:1}},drop_chances:{mainhand:0.0f}')] * 2
TARGET_TIME = {'frost': 800, 'hollow': 400}          # ticks to strike every target (default 600)
PITCH = [0.5, 0.63, 0.75, 0.84, 1.0, 1.12, 1.26, 1.5, 1.68, 2.0]
SYMBOLS = ['minecraft:gold_block', 'minecraft:emerald_block', 'minecraft:diamond_block', 'minecraft:redstone_block', 'minecraft:lapis_block']


def ctrl_sel(d, n, r):
    return f'@e[type=minecraft:marker,tag=bm.pz,tag=bm.pz{n},tag=bm.d_{d},distance=..{r},sort=nearest,limit=1]'


def el_sel(d, n, kind, r, extra=''):
    return f'@e[type=minecraft:marker,tag=bm.pet_{kind},tag=bm.pz{n},tag=bm.d_{d},distance=..{r}{extra}]'


def dg_sel(d, r=None):
    return f'@e[type=minecraft:marker,tag=bm.dg,tag=bm.d_{d},distance=..{r or R2(d)},sort=nearest,limit=1]'


def generate(G, builds):
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    PREFIX = G.PREFIX
    tick, fast, second, load = [], [], [], []

    # ============================================================== utilities
    fn('p2/util/lever_off', [f'execute if block ~ ~ ~ minecraft:lever[face={fa},facing={fc},powered=true] run setblock ~ ~ ~ minecraft:lever[face={fa},facing={fc},powered=false]'
                             for fa in ('wall', 'floor', 'ceiling') for fc in ('north', 'south', 'east', 'west')])
    fn('p2/util/bulb_toggle', ['execute if block ~ ~ ~ minecraft:waxed_copper_bulb[lit=true] run return run setblock ~ ~ ~ minecraft:waxed_copper_bulb[lit=false,powered=false]',
                               'setblock ~ ~ ~ minecraft:waxed_copper_bulb[lit=true,powered=false]'])
    fn('p2/util/locked', [title('@a[distance=..6]', 'actionbar', T('The mechanism is locked. Something earlier in this place must be solved first.', 'gray', italic=True)),
                          'playsound minecraft:block.iron_trapdoor.close block @a[distance=..8] ~ ~ ~ 0.6 0.6'])
    fn('p2/util/vanish', ['particle minecraft:large_smoke ~ ~1 ~ 0.4 0.6 0.4 0.02 15', 'tp @s ~ -400 ~'])

    for d, B in builds.items():
        cfg, fl = D[d], FLAVOR[d]
        r2 = R2(d)
        meta = B.meta
        P = sorted(meta['puzzles'])
        NP = len(P)
        gate = cfg['gate']

        # ---------------- gates (animated top-down opening), battle doors, secret doors, arena exit
        anim = ['scoreboard players add @s bm.gt 1']
        for i, dy in enumerate((3, 2, 1, 0)):
            t = 1 + i * 5
            anim += [f'execute if score @s bm.gt matches {t} run fill ~-1 ~{dy} ~-1 ~1 ~{dy} ~1 {OPEN_LIGHT} replace {gate}',
                     f'execute if score @s bm.gt matches {t} run particle minecraft:block{{block_state:"{fl["block_part"]}"}} ~ ~{dy}.5 ~ 0.8 0.3 0.8 0 16',
                     f'execute if score @s bm.gt matches {t} run playsound {fl["osnd"]} block @a[distance=..20] ~ ~{dy} ~ 1 {0.6 + i * 0.1:.1f}']
        anim += ['execute if score @s bm.gt matches 16.. run scoreboard players set @s bm.gs 2']
        fn(f'p2/{d}/gate_anim', anim)
        fn(f'p2/{d}/gate_open', ['scoreboard players set @s bm.gs 1', 'scoreboard players set @s bm.gt 0',
                                 f'playsound {fl["osnd2"]} block @a[distance=..24] ~ ~1 ~ 1 0.7'])
        fn(f'p2/{d}/gate_close', [f'fill ~-1 ~ ~-1 ~1 ~3 ~1 {gate} replace minecraft:light[level=3]', 'scoreboard players set @s bm.gs 0'])
        fn(f'p2/{d}/adoor_close', [f'fill ~-2 ~ ~-2 ~2 ~4 ~2 {gate} replace minecraft:light[level=4]',
                                   f'playsound minecraft:block.iron_door.close block @a[distance=..24] ~ ~2 ~ 1 0.5',
                                   f'particle minecraft:block{{block_state:"{fl["block_part"]}"}} ~ ~2 ~ 1.5 1.5 1.5 0 30'])
        fn(f'p2/{d}/adoor_open', [f'fill ~-2 ~ ~-2 ~2 ~4 ~2 {ADOOR_LIGHT} replace {gate}',
                                  f'playsound minecraft:block.iron_door.open block @a[distance=..24] ~ ~2 ~ 1 0.5'])
        sec = cfg['secret']
        fn(f'p2/{d}/sdoor_open', ['setblock ~ ~ ~ minecraft:air', 'setblock ~ ~1 ~ minecraft:air', 'tag @s add bm.open',
                                  f'particle minecraft:block{{block_state:"{sec}"}} ~ ~1 ~ 0.3 0.6 0.3 0 20',
                                  'playsound minecraft:block.stone_button.click_on block @a[distance=..16] ~ ~ ~ 1 0.5',
                                  'playsound minecraft:block.grindstone.use block @a[distance=..16] ~ ~1 ~ 0.7 0.5',
                                  title('@a[distance=..8]', 'actionbar', T('Something shifts in the wall...', 'gray', italic=True))])
        fn(f'p2/{d}/sdoor_close', [f'setblock ~ ~ ~ {sec}', f'setblock ~ ~1 ~ {sec}', 'tag @s remove bm.open'])
        fn(f'p2/{d}/xdoor_open', ['setblock ~ ~ ~ minecraft:air', 'setblock ~ ~1 ~ minecraft:air',
                                  f'particle minecraft:block{{block_state:"{sec}"}} ~ ~1 ~ 0.3 0.6 0.3 0 20',
                                  'playsound minecraft:block.piston.contract block @a[distance=..16] ~ ~ ~ 1 0.5'])
        fn(f'p2/{d}/xdoor_close', [f'execute unless entity @a[dx=0,dy=1,dz=0] run setblock ~ ~ ~ {sec}',
                                   f'execute unless entity @a[dx=0,dy=1,dz=0] run setblock ~ ~1 ~ {sec}'])
        # hidden buttons -> their secret door (same k)
        ks = sorted({m[3] for m in meta['sdoors']})
        sb = [f'execute if entity @s[tag=bm.sk{k}] as @e[type=minecraft:marker,tag=bm.sdoor,tag=bm.sk{k},tag=bm.d_{d},tag=!bm.open,distance=..32,sort=nearest,limit=1] at @s run function bm:p2/{d}/sdoor_open'
              for k in ks]
        fn(f'p2/{d}/sbtn', sb)

        # ---------------- puzzles
        def solve(n):
            lines = ['scoreboard players set @s bm.done 1',
                     f'scoreboard players set {dg_sel(d)} bm.pz {n}',
                     f'execute as @e[type=minecraft:marker,tag=bm.drain,tag=bm.g{n},tag=bm.d_{d},distance=..{r2}] at @s run fill ~-3 ~-2 ~-3 ~3 ~3 ~3 minecraft:air replace minecraft:water',
                     f'execute as @e[type=minecraft:marker,tag=bm.gate,tag=bm.g{n},tag=bm.d_{d},distance=..{r2}] at @s run function bm:p2/{d}/gate_open']
            if n < NP:
                lines.append(f'execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pz{n + 1},tag=bm.d_{d},distance=..{r2}] at @s run function bm:p2/{d}/pz{n + 1}_reset')
                lines.append(title(f'@a[distance=..{cfg["radius"]}]', 'actionbar', T(f'{fl["open"]}  (trial {n} of {NP})', 'gold')))
            else:
                lines += [f'title @a[distance=..{cfg["radius"]}] times 10 60 20',
                          title(f'@a[distance=..{cfg["radius"]}]', 'subtitle', T(f'Every trial is solved. The altar of {cfg["boss"]} awakens.', 'gray', italic=True)),
                          title(f'@a[distance=..{cfg["radius"]}]', 'title', T('The way is open', cfg['color'], bold=True))]
            lines += ['playsound minecraft:block.note_block.chime master @a[distance=..16] ~ ~ ~ 1 1.2',
                      'playsound minecraft:block.note_block.chime master @a[distance=..16] ~ ~ ~ 1 1.6']
            fn(f'p2/{d}/pz{n}_solve', lines)

        def fail(n, extra_reset):
            fn(f'p2/{d}/pz{n}_fail', extra_reset + fl['fail'] + [
                title('@a[distance=..16]', 'actionbar', T(fl['failmsg'], 'red')),
                f'playsound {fl["failsnd"]} hostile @a[distance=..12] ~ ~ ~ 1 0.8',
                'playsound minecraft:block.note_block.bass block @a[distance=..12] ~ ~ ~ 1 0.5'])

        for n in P:
            p = meta['puzzles'][n]
            kind = p['kind']
            cx, cy, cz = p['ctrl']
            els = p['elements']
            R = max([math.dist((cx, cy, cz), e[1:4]) for e in els] + [4]) + 2.5
            R = int(math.ceil(R))
            head = ['execute if score @s bm.done matches 1 run return 0',
                    'scoreboard players set #act bm.rng 0',
                    f'execute store result score #dpz bm.rng run scoreboard players get {dg_sel(d)} bm.pz',
                    f'execute if score #dpz bm.rng matches {n - 1} run scoreboard players set #act bm.rng 1']
            press = lambda k: [
                f'execute as {el_sel(d, n, k, R, ",tag=!bm.held")} at @s if block ~ ~ ~ #minecraft:buttons[powered=true] run function bm:p2/{d}/pz{n}_{k}',
                f'execute as {el_sel(d, n, k, R, ",tag=bm.held")} at @s unless block ~ ~ ~ #minecraft:buttons[powered=true] run tag @s remove bm.held']
            pre = ['tag @s add bm.held', 'execute if score #act bm.rng matches 0 run return run function bm:p2/util/locked']
            ctrl = ctrl_sel(d, n, R)
            solve(n)
            if kind == 'levers':
                body = ['execute if score #act bm.rng matches 0 run return 0', 'scoreboard players set #mm bm.rng 0',
                        f'execute as {el_sel(d, n, "lever", R, ",tag=bm.want1")} at @s unless block ~ ~ ~ minecraft:lever[powered=true] run scoreboard players add #mm bm.rng 1',
                        f'execute as {el_sel(d, n, "lever", R, ",tag=bm.want0")} at @s if block ~ ~ ~ minecraft:lever[powered=true] run scoreboard players add #mm bm.rng 1',
                        f'execute if score #mm bm.rng matches 0 run function bm:p2/{d}/pz{n}_solve']
                reset = ['scoreboard players set @s bm.done 0', f'execute as {el_sel(d, n, "lever", R)} at @s run function bm:p2/util/lever_off']
            elif kind == 'keypad':
                L = int(p['data']['len']); code = int(p['data']['code'])
                body = press('key')
                dig = ['execute if entity @s[tag=bm.kclr] run return run execute as ' + ctrl + f' at @s run function bm:p2/{d}/pz{n}_clr',
                       'execute if entity @s[tag=bm.kent] run return run execute as ' + ctrl + f' at @s run function bm:p2/{d}/pz{n}_ent']
                dig += [f'execute if entity @s[tag=bm.k{i}] run scoreboard players set #dig bm.rng {i}' for i in range(10)]
                dig += [f'execute if entity @s[tag=bm.k{i}] run playsound minecraft:block.note_block.hat block @a[distance=..8] ~ ~ ~ 0.8 {PITCH[i]}' for i in range(10)]
                dig += [f'execute as {ctrl} at @s run function bm:p2/{d}/pz{n}_dig']
                fn(f'p2/{d}/pz{n}_key', pre + dig)
                fn(f'p2/{d}/pz{n}_dig', ['execute unless score @s bm.klen matches 0.. run scoreboard players set @s bm.klen 0',
                                         'execute if score @s bm.klen matches 9.. run return 0',
                                         'scoreboard players operation @s bm.code *= #10 bm.p2',
                                         'scoreboard players operation @s bm.code += #dig bm.rng',
                                         'scoreboard players add @s bm.klen 1', f'function bm:p2/{d}/pz{n}_show'])
                show = []
                for k in range(0, 10):
                    dots = ' '.join(['●'] * min(k, max(L, k)) + ['○'] * max(0, L - k))
                    show.append(f'execute if score @s bm.klen matches {k} run ' + title('@a[distance=..7]', 'actionbar', [T('Code  ', 'gray'), T(dots, cfg['color'] if cfg['color'].startswith('#') else 'gold', bold=True)]))
                fn(f'p2/{d}/pz{n}_show', show)
                fn(f'p2/{d}/pz{n}_clr', ['scoreboard players set @s bm.code 0', 'scoreboard players set @s bm.klen 0', f'function bm:p2/{d}/pz{n}_show',
                                         'playsound minecraft:block.note_block.basedrum block @a[distance=..8] ~ ~ ~ 0.8 0.8'])
                fn(f'p2/{d}/pz{n}_ent', [f'execute if score @s bm.klen matches {L} if score @s bm.code matches {code} run return run function bm:p2/{d}/pz{n}_solve',
                                         f'function bm:p2/{d}/pz{n}_fail'])
                fail(n, ['scoreboard players set @s bm.code 0', 'scoreboard players set @s bm.klen 0'])
                reset = ['scoreboard players set @s bm.done 0', 'scoreboard players set @s bm.code 0', 'scoreboard players set @s bm.klen 0']
            elif kind in ('seq', 'simon'):
                L = max(int(t[4:]) for e in els if e[0] == 'seq' for t in e[4] if t.startswith('bm.s') and t[4:].isdigit())
                body = press('seq')
                tones = [f'execute if entity @s[tag=bm.snd{j}] run playsound {fl["tone"]} block @a[distance=..14] ~ ~ ~ 1 {PITCH[min(9, j * 2)]}' for j in range(1, 9)]
                fn(f'p2/{d}/pz{n}_tone', tones + ['particle minecraft:note ~ ~0.7 ~ 0.2 0.2 0.2 1 3'])
                seqp = pre + [f'function bm:p2/{d}/pz{n}_tone', 'scoreboard players set #k bm.rng 0']
                seqp += [f'execute if entity @s[tag=bm.s{i}] run scoreboard players set #k bm.rng {i}' for i in range(1, L + 1)]
                seqp += [f'execute as {ctrl} at @s run function bm:p2/{d}/pz{n}_step']
                fn(f'p2/{d}/pz{n}_seq', seqp)
                fn(f'p2/{d}/pz{n}_step', ['execute unless score @s bm.step matches 0.. run scoreboard players set @s bm.step 0',
                                          'scoreboard players operation #exp bm.rng = @s bm.step', 'scoreboard players add #exp bm.rng 1',
                                          f'execute unless score #k bm.rng = #exp bm.rng run return run function bm:p2/{d}/pz{n}_fail',
                                          'scoreboard players add @s bm.step 1',
                                          f'execute if score @s bm.step matches {L}.. run return run function bm:p2/{d}/pz{n}_solve',
                                          title('@a[distance=..10]', 'actionbar', T('...something answers.', 'gray', italic=True))])
                fail(n, ['scoreboard players set @s bm.step 0', 'scoreboard players set @s bm.pt 0'])
                reset = ['scoreboard players set @s bm.done 0', 'scoreboard players set @s bm.step 0', 'scoreboard players set @s bm.pt 0']
                if kind == 'simon':
                    body += press('listen')
                    fn(f'p2/{d}/pz{n}_listen', pre + [f'execute as {ctrl} unless score @s bm.pt matches 1.. run scoreboard players set @s bm.pt 1'])
                    mel = ['scoreboard players add @s bm.pt 1']
                    for i in range(1, L + 1):
                        mel.append(f'execute if score @s bm.pt matches {i * 14} as {el_sel(d, n, "seq", R, f",tag=bm.s{i}")} at @s run function bm:p2/{d}/pz{n}_tone')
                    mel.append(f'execute if score @s bm.pt matches {L * 14 + 10}.. run scoreboard players set @s bm.pt 0')
                    fn(f'p2/{d}/pz{n}_melody', mel)
                    body = [f'execute if score @s bm.pt matches 1.. run function bm:p2/{d}/pz{n}_melody'] + body
            elif kind == 'path':
                trap = cfg['trap']
                body = [f'execute as @e[type=minecraft:ender_pearl,distance=..{R + 8}] at @s run function bm:p2/util/pearl_zap',   # 2.1: no pearling past the plates
                        f'execute as @a[distance=..{R + 6},gamemode=!spectator,gamemode=!creative] at @s if block ~ ~ ~ #minecraft:pressure_plates if block ~ ~-2 ~ {trap} run function bm:p2/{d}/pz{n}_trap',
                        f'execute if score #act bm.rng matches 1 as {el_sel(d, n, "goal", R)} at @s if entity @a[distance=..1.6,gamemode=!spectator] as {ctrl} at @s run function bm:p2/{d}/pz{n}_solve']
                fn(f'p2/{d}/pz{n}_trap', [f'tp @s {el_sel(d, n, "start", R + 12, ",sort=nearest,limit=1")}'] + fl['trap'] + [
                    title('@s', 'actionbar', T(fl['trapmsg'], 'red')), 'playsound minecraft:block.trial_spawner.break hostile @s ~ ~ ~ 1 0.6'])
                reset = ['scoreboard players set @s bm.done 0']
            elif kind == 'targets':
                ordered = any(t.startswith('bm.s') for e in els if e[0] == 'target' for t in e[4])
                L = sum(1 for e in els if e[0] == 'target')
                body = ['execute if score #act bm.rng matches 0 run return 0',
                        f'execute as {el_sel(d, n, "target", R, ",tag=!bm.hit")} at @s unless block ~ ~ ~ minecraft:target[power=0] run function bm:p2/{d}/pz{n}_hit',
                        'execute if score @s bm.pt matches 1.. run scoreboard players add @s bm.pt 1',
                        f'execute if score @s bm.pt matches {TARGET_TIME.get(d, 600)}.. run function bm:p2/{d}/pz{n}_timeout']
                hit = ['tag @s add bm.hit', 'particle minecraft:wax_off ~ ~ ~ 0.6 0.6 0.6 0 12',
                       'playsound minecraft:block.note_block.bell block @a[distance=..30] ~ ~ ~ 1 1.4']
                if ordered:
                    hit = ['scoreboard players set #k bm.rng 0'] + [f'execute if entity @s[tag=bm.s{i}] run scoreboard players set #k bm.rng {i}' for i in range(1, L + 1)] + \
                          [f'execute as {ctrl} at @s run function bm:p2/{d}/pz{n}_ordchk', 'execute if score #ok bm.rng matches 0 run return 0'] + hit
                    fn(f'p2/{d}/pz{n}_ordchk', ['scoreboard players set #ok bm.rng 0', 'execute unless score @s bm.step matches 0.. run scoreboard players set @s bm.step 0',
                                                'scoreboard players operation #exp bm.rng = @s bm.step', 'scoreboard players add #exp bm.rng 1',
                                                f'execute unless score #k bm.rng = #exp bm.rng run return run function bm:p2/{d}/pz{n}_fail',
                                                'scoreboard players add @s bm.step 1', 'scoreboard players set #ok bm.rng 1'])
                fn(f'p2/{d}/pz{n}_hit', hit + [f'execute as {ctrl} at @s run function bm:p2/{d}/pz{n}_count'])
                fn(f'p2/{d}/pz{n}_count', ['execute unless score @s bm.pt matches 1.. run scoreboard players set @s bm.pt 1',
                                           f'execute store result score #h bm.rng if entity {el_sel(d, n, "target", R, ",tag=bm.hit")}',
                                           f'execute if score #h bm.rng matches {L}.. run return run function bm:p2/{d}/pz{n}_solve',
                                           title('@a[distance=..24]', 'actionbar', [T('Targets struck: ', 'gray'), {'score': {'name': '#h', 'objective': 'bm.rng'}, 'color': 'gold'}, T(f' / {L}', 'gray')])])
                untag = [f'tag {el_sel(d, n, "target", R)} remove bm.hit', 'scoreboard players set @s bm.pt 0', 'scoreboard players set @s bm.step 0']
                fn(f'p2/{d}/pz{n}_timeout', untag + [title('@a[distance=..24]', 'actionbar', T('Too slow! The targets reset.', 'red')),
                                                       'playsound minecraft:block.note_block.bass block @a[distance=..24] ~ ~ ~ 1 0.5'])
                fail(n, untag)
                reset = ['scoreboard players set @s bm.done 0'] + untag
            elif kind == 'lights':
                S = 4 if sum(1 for e in els if e[0] == 'bulb') == 16 else 3
                body = press('lo')
                raw = {}
                for i in range(S * S):
                    r, c = divmod(i, S)
                    nb = [i] + [rr * S + cc for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)) if 0 <= rr < S and 0 <= cc < S]
                    fn(f'p2/{d}/pz{n}_lo{i}', [f'execute as {el_sel(d, n, "bulb", R + 4, f",tag=bm.i{j}")} at @s run function bm:p2/util/bulb_toggle' for j in nb])
                lo = pre + ['playsound minecraft:block.copper_bulb.turn_on block @a[distance=..10] ~ ~ ~ 1 1']
                lo += [f'execute if entity @s[tag=bm.i{i}] as {ctrl} at @s run function bm:p2/{d}/pz{n}_lo{i}' for i in range(S * S)]
                lo += [f'execute as {ctrl} at @s run function bm:p2/{d}/pz{n}_check']
                fn(f'p2/{d}/pz{n}_lo', lo)
                fn(f'p2/{d}/pz{n}_check', ['scoreboard players set #u bm.rng 0',
                                           f'execute as {el_sel(d, n, "bulb", R + 4)} at @s if block ~ ~ ~ minecraft:waxed_copper_bulb[lit=false] run scoreboard players add #u bm.rng 1',
                                           f'execute if score #u bm.rng matches 0 run function bm:p2/{d}/pz{n}_solve'])
                scr = ['scoreboard players set @s bm.done 0', f'execute as {el_sel(d, n, "bulb", R + 4)} at @s run setblock ~ ~ ~ minecraft:waxed_copper_bulb[lit=true,powered=false]']
                for _ in range(7):
                    scr.append(f'execute store result score #r bm.rng run random value 0..{S * S - 1}')
                    scr += [f'execute if score #r bm.rng matches {i} run function bm:p2/{d}/pz{n}_lo{i}' for i in range(S * S)]
                scr += ['scoreboard players set #u bm.rng 0',
                        f'execute as {el_sel(d, n, "bulb", R + 4)} at @s if block ~ ~ ~ minecraft:waxed_copper_bulb[lit=false] run scoreboard players add #u bm.rng 1',
                        f'execute if score #u bm.rng matches 0 run function bm:p2/{d}/pz{n}_lo{S + 1}']
                reset = scr
            elif kind == 'offering':
                ks = sorted({int(t[4:]) for e in els if e[0] == 'offer' for t in e[4] if t.startswith('bm.o')})
                body = ['execute if score #act bm.rng matches 0 run return 0',
                        f'execute as {el_sel(d, n, "offer", R, ",tag=!bm.got")} at @s run function bm:p2/{d}/pz{n}_offer']
                fn(f'p2/{d}/pz{n}_offer', [f'execute if entity @s[tag=bm.o{k}] as @e[type=minecraft:item,distance=..1.6] at @s if items entity @s contents *[minecraft:custom_data~{{bm:"pearl_sigil_{k}"}}] run function bm:p2/{d}/pz{n}_accept{k}' for k in ks])
                for k in ks:
                    fn(f'p2/{d}/pz{n}_accept{k}', [
                        'kill @s',
                        f'execute as {el_sel(d, n, "offer", 3, f",tag=bm.o{k},sort=nearest,limit=1")} at @s run function bm:p2/{d}/pz{n}_placed',
                        f'execute as {ctrl} at @s run function bm:p2/{d}/pz{n}_tally'])
                fn(f'p2/{d}/pz{n}_placed', ['tag @s add bm.got', 'setblock ~ ~ ~ minecraft:pearlescent_froglight',
                                            'particle minecraft:glow ~ ~0.5 ~ 0.4 0.4 0.4 0 20',
                                            'playsound minecraft:block.conduit.activate block @a[distance=..16] ~ ~ ~ 1 1'])
                fn(f'p2/{d}/pz{n}_tally', [f'execute store result score #h bm.rng if entity {el_sel(d, n, "offer", R, ",tag=bm.got")}',
                                           f'execute if score #h bm.rng matches {len(ks)}.. run return run function bm:p2/{d}/pz{n}_solve',
                                           title('@a[distance=..20]', 'actionbar', [T('The Tyrant accepts your tribute: ', 'aqua'), {'score': {'name': '#h', 'objective': 'bm.rng'}, 'color': 'gold'}, T(f' / {len(ks)}', 'aqua')])])
                reset = ['scoreboard players set @s bm.done 0',
                         f'execute as {el_sel(d, n, "offer", R)} at @s if block ~ ~ ~ minecraft:pearlescent_froglight run setblock ~ ~ ~ minecraft:air',
                         f'tag {el_sel(d, n, "offer", R)} remove bm.got']
            elif kind == 'slots':
                body = ['execute if score @s bm.pt matches 1.. run function bm:p2/{0}/pz{1}_spin'.format(d, n)] + press('pull')
                fn(f'p2/{d}/pz{n}_pull', pre + [f'execute as {ctrl} unless score @s bm.pt matches 1.. at @s run function bm:p2/{d}/pz{n}_roll'])
                sym = [f'execute if score #sym bm.rng matches {i + 1} run setblock ~ ~ ~ {b}' for i, b in enumerate(SYMBOLS)]
                fn(f'p2/{d}/pz{n}_reel', sym)
                fn(f'p2/{d}/pz{n}_roll', [
                    'scoreboard players set @s bm.pt 1',
                    'playsound minecraft:block.lever.click block @a[distance=..10] ~ ~ ~ 1 0.6',
                    'execute store result score #win bm.rng run random value 1..100',
                    'execute store result score @s bm.code run random value 1..5',
                    'execute store result score @s bm.klen run random value 1..5',
                    'execute store result score @s bm.step run random value 1..5',
                    'execute if score #win bm.rng matches ..14 run scoreboard players operation @s bm.klen = @s bm.code',
                    'execute if score #win bm.rng matches ..14 run scoreboard players operation @s bm.step = @s bm.code',
                    'execute if score #win bm.rng matches 15.. if score @s bm.code = @s bm.klen if score @s bm.code = @s bm.step run scoreboard players add @s bm.step 1',
                    'execute if score @s bm.step matches 6.. run scoreboard players set @s bm.step 1'])
                spin = ['scoreboard players add @s bm.pt 1', 'scoreboard players operation #m bm.rng = @s bm.pt', 'scoreboard players operation #m bm.rng %= #3 bm.p2']
                for i in (1, 2, 3):
                    stop = {1: 30, 2: 40, 3: 50}[i]
                    spin.append(f'execute if score #m bm.rng matches 0 if score @s bm.pt matches ..{stop - 1} as {el_sel(d, n, "reel", R, f",tag=bm.i{i}")} at @s run function bm:p2/{d}/pz{n}_rnd')
                    src = {1: 'bm.code', 2: 'bm.klen', 3: 'bm.step'}[i]
                    spin.append(f'execute if score @s bm.pt matches {stop} run scoreboard players operation #sym bm.rng = @s {src}')
                    spin.append(f'execute if score @s bm.pt matches {stop} as {el_sel(d, n, "reel", R, f",tag=bm.i{i}")} at @s run function bm:p2/{d}/pz{n}_stop')
                spin.append('execute if score #m bm.rng matches 0 if score @s bm.pt matches ..49 run playsound minecraft:block.note_block.hat block @a[distance=..10] ~ ~ ~ 0.6 1.6')
                spin.append(f'execute if score @s bm.pt matches 50.. run function bm:p2/{d}/pz{n}_result')
                fn(f'p2/{d}/pz{n}_spin', spin)
                fn(f'p2/{d}/pz{n}_rnd', ['execute store result score #sym bm.rng run random value 1..5', f'function bm:p2/{d}/pz{n}_reel'])
                fn(f'p2/{d}/pz{n}_stop', [f'function bm:p2/{d}/pz{n}_reel', 'playsound minecraft:block.note_block.basedrum block @a[distance=..10] ~ ~ ~ 1 1'])
                fn(f'p2/{d}/pz{n}_result', ['scoreboard players set @s bm.pt 0',
                                            f'execute if score @s bm.code = @s bm.klen if score @s bm.code = @s bm.step run return run function bm:p2/{d}/pz{n}_solve',
                                            title('@a[distance=..10]', 'actionbar', T('Bust! Pull again.', 'yellow')),
                                            'playsound minecraft:entity.chicken.ambient block @a[distance=..10] ~ ~ ~ 1 0.8'])
                reset = ['scoreboard players set @s bm.done 0', 'scoreboard players set @s bm.pt 0']
            elif kind == 'waves':
                # combat trial (2.2): walking in starts the assault; clear every wave to open the gate. Spawn points are 'wsp'
                # elements; a pre-2.2 copy of the dungeon (an old keypad/lever room on this index) has none, so the wave rises
                # around a random player in the room instead.
                from p2.data import WAVES
                wname, waves = WAVES[d][n]
                NW = len(waves)
                wm = f'bm.wm_{d}{n}'
                body = ['execute if score #act bm.rng matches 0 run return 0',
                        f'execute unless score @s bm.wv matches 1.. if entity @a[distance=..{R},gamemode=!spectator] run function bm:p2/{d}/pz{n}_wstart',
                        'execute unless score @s bm.wv matches 1.. run return 0',
                        f'execute unless entity @a[distance=..{R + 10},gamemode=!spectator] run return run function bm:p2/{d}/pz{n}_wabort',
                        f'execute if entity @e[tag={wm},distance=..{R + 24}] run return run scoreboard players set @s bm.wt 0',
                        'scoreboard players add @s bm.wt 1',
                        'execute if score @s bm.wt matches 1 run ' + title(f'@a[distance=..{R + 10}]', 'actionbar', T('Wave cleared...', 'gray', italic=True)),
                        f'execute if score @s bm.wt matches 50.. run function bm:p2/{d}/pz{n}_wnext']
                fn(f'p2/{d}/pz{n}_wstart', ['scoreboard players set @s bm.wv 0', f'title @a[distance=..{R + 10}] times 5 40 10',
                                            title(f'@a[distance=..{R + 10}]', 'subtitle', T(f'Survive {NW} waves to open the way', 'gray', italic=True)),
                                            title(f'@a[distance=..{R + 10}]', 'title', T(wname, cfg['color'], bold=True)),
                                            f'playsound minecraft:event.raid.horn hostile @a[distance=..{R + 10}] ~ ~ ~ 2 0.7',
                                            f'function bm:p2/{d}/pz{n}_wnext'])
                nxt = ['scoreboard players add @s bm.wv 1', 'scoreboard players set @s bm.wt 0',
                       f'execute if score @s bm.wv matches {NW + 1}.. run return run function bm:p2/{d}/pz{n}_wwin']
                from p2.data import WAVE_PER
                lo, hi = WAVE_PER.get(d, (1, 2))
                for k, wave in enumerate(waves, 1):
                    per = hi if k == NW else lo
                    nxt.append(f'execute if score @s bm.wv matches {k} run function bm:p2/{d}/pz{n}_w{k}')
                    fn(f'p2/{d}/pz{n}_w{k}', [title(f'@a[distance=..{R + 10}]', 'actionbar', T(f'Wave {k} of {NW}', 'red', bold=True)),
                                              f'playsound minecraft:entity.wither.ambient hostile @a[distance=..{R + 10}] ~ ~ ~ 0.6 {0.6 + 0.1 * k:.1f}',
                                              f'execute as {el_sel(d, n, "wsp", R)} at @s run function bm:p2/{d}/pz{n}_sp{k}',
                                              f'execute unless entity {el_sel(d, n, "wsp", R)} at @a[distance=..{R},gamemode=!spectator,sort=random,limit=2] run function bm:p2/{d}/pz{n}_sp{k}'])
                    fn(f'p2/{d}/pz{n}_sp{k}', ['particle minecraft:large_smoke ~ ~1 ~ 0.4 0.6 0.4 0.03 20', 'particle minecraft:soul_fire_flame ~ ~0.2 ~ 0.4 0.1 0.4 0.02 10',
                                               'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..20] ~ ~ ~ 0.7 0.8'] +
                                              [f'function bm:p2/{d}/pz{n}_one{k}'] * per)
                    one = [f'execute store result score #wr bm.rng run random value 1..{len(wave)}']
                    for i, (ent, nbt) in enumerate(wave, 1):
                        nb = dict(nbt); nb['Tags'] = ['bm.dgmob', 'bm.wm', wm]; nb['PersistenceRequired'] = Byte(1)
                        one.append(f'execute if score #wr bm.rng matches {i} run summon minecraft:{ent} ~ ~ ~ {snbt(nb)}')
                    fn(f'p2/{d}/pz{n}_one{k}', one)
                fn(f'p2/{d}/pz{n}_wnext', nxt)
                fn(f'p2/{d}/pz{n}_wwin', ['scoreboard players set @s bm.wv 0', f'function bm:p2/{d}/pz{n}_solve'])
                vanish = [f'execute as @e[tag={wm}] at @s run function bm:p2/util/vanish', 'scoreboard players set @s bm.wv 0', 'scoreboard players set @s bm.wt 0']
                fn(f'p2/{d}/pz{n}_wabort', vanish)
                reset = ['scoreboard players set @s bm.done 0'] + vanish
            elif kind == 'reach':
                # traversal trial (2.2): get from the start ledge to the goal across lava / void. No pearls.
                body = [f'execute as @e[type=minecraft:ender_pearl,distance=..{R + 8}] at @s run function bm:p2/util/pearl_zap',
                        f'execute if score #act bm.rng matches 1 as {el_sel(d, n, "goal", R)} at @s if entity @a[distance=..1.6,gamemode=!spectator] as {ctrl} at @s run function bm:p2/{d}/pz{n}_solve']
                reset = ['scoreboard players set @s bm.done 0']
            else:
                raise ValueError(kind)
            fn(f'p2/{d}/pz{n}', head + body)
            fn(f'p2/{d}/pz{n}_reset', reset)
            # 2.13: the Hollow's trials sleep while everyone in the Throne has already conquered it (#hsafe, below)
            safe = 'if score #hsafe bm.p2 matches 0 ' if d == 'hollow' else ''
            tick.append(f'execute {safe}as @e[type=minecraft:marker,tag=bm.pz,tag=bm.d_{d},tag=bm.pz{n}] at @s run function bm:p2/{d}/pz{n}')

        # ---------------- dungeon controller: idle reset, re-arm after victory, ambience
        rad = cfg['radius']
        common_reset = [f'execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.d_{d},tag=bm.pz{n},distance=..{r2}] at @s run function bm:p2/{d}/pz{n}_reset' for n in P]
        fn(f'p2/{d}/rearm', ['scoreboard players set @s bm.pz 0'] + common_reset)
        fn(f'p2/{d}/reset', ['scoreboard players set @s bm.pz 0'] + common_reset + [
            f'execute as @e[type=minecraft:marker,tag=bm.gate,tag=bm.d_{d},distance=..{r2}] at @s run function bm:p2/{d}/gate_close',
            f'execute as @e[type=minecraft:marker,tag=bm.sdoor,tag=bm.d_{d},tag=bm.open,distance=..{r2}] at @s run function bm:p2/{d}/sdoor_close',
            f'execute as @e[type=minecraft:marker,tag=bm.xdoor,tag=bm.d_{d},distance=..{r2}] at @s run function bm:p2/{d}/xdoor_close',
            f'execute as @e[type=minecraft:marker,tag=bm.restock,tag=bm.d_{d},distance=..{r2}] at @s run function bm:p2/restock',
            # 2.13: a reset dungeon can be looted again - every vault forgets who opened it, every loot chest refills
            f'execute as @e[type=minecraft:marker,tag=bm.vaultm,tag=bm.d_{d},distance=..{r2}] at @s run data modify block ~ ~ ~ server_data set value {{}}',
            f'execute as @e[type=minecraft:marker,tag=bm.chestm,tag=bm.d_{d},distance=..{r2}] at @s run function bm:p2/util/reloot with entity @s data'])
        amb = cfg['amb']
        ambl = ['execute store result score #r bm.rng run random value 1..14']
        for i, (snd, vol, pit) in enumerate(amb, 1):
            ambl.append(f'execute if score #r bm.rng matches {i} as @a[distance=..{rad}] at @s run playsound {snd} ambient @s ^ ^1 ^-5 {vol} {pit}')
        fn(f'p2/{d}/amb', ambl)
        fn(f'p2/{d}/dg', [
            'execute unless score @s bm.pz = @s bm.pz run scoreboard players set @s bm.pz 0',
            f'execute unless entity @a[distance=..{rad}] run return 0',
            *([f'execute unless entity @a[distance=..{rad},scores={{bm.conq=..5}}] run return run function bm:p2/{d}/amb'] if d == 'hollow' else []),
            'execute store result score #now bm.rng run time query gametime',
            'scoreboard players operation #gap bm.rng = #now bm.rng', 'scoreboard players operation #gap bm.rng -= @s bm.seen',
            f'execute if score @s bm.seen matches 1.. if score #gap bm.rng matches 24000.. unless score {f"@e[type=minecraft:marker,tag=bm.arena,tag=bm.d_{d},distance=..{r2},sort=nearest,limit=1]"} bm.bs matches 1.. run function bm:p2/{d}/reset',
            'scoreboard players operation @s bm.seen = #now bm.rng',
            f'function bm:p2/{d}/amb'])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_{d}] at @s run function bm:p2/{d}/dg')
        # AOE particles + hidden buttons + gate animation + mining fatigue
        fn(f'p2/{d}/fx', cfg['fx'])
        fast.append(f'execute as @e[type=minecraft:marker,tag=bm.dgfx,tag=bm.d_{d}] at @s if entity @a[distance=..40] run function bm:p2/{d}/fx')
        if ks:
            tick.append(f'execute as @e[type=minecraft:marker,tag=bm.sbtn,tag=bm.d_{d}] at @s if block ~ ~ ~ #minecraft:buttons[powered=true] run function bm:p2/{d}/sbtn')
        tick.append(f'execute as @e[type=minecraft:marker,tag=bm.gate,tag=bm.d_{d},scores={{bm.gs=1}}] at @s run function bm:p2/{d}/gate_anim')

    # restock (offering props)
    rs = []
    for iid in ITEMS:
        if iid.startswith('pearl_sigil_'):
            rs.append(f'execute if entity @s[tag=bm.ri_{iid}] run item replace block ~ ~ ~ container.13 with {G.item_arg(iid)}')
    fn('p2/restock', rs or ['return 0'])

    # zones: adventure inside dungeons (on dungeon floors near a zone marker) and everywhere in the Hollow Throne
    zone_lines = ['execute as @a[gamemode=survival,tag=!bm.adv] at @s if block ~ ~-0.2 ~ #bm:dungeon_floor if entity @e[type=minecraft:marker,tag=bm.zone_d,distance=..32] run function bm:zone/enter',
                  'execute as @a[gamemode=survival,tag=!bm.adv] at @s if dimension bm:hollow_throne run function bm:zone/enter']
    second += ['execute as @e[type=minecraft:marker,tag=bm.zone_d] at @s run effect give @a[distance=..34,gamemode=survival,tag=!bm.adv] minecraft:mining_fatigue 3 2 true']
    fn('p2/util/pearl_zap', ['particle minecraft:reverse_portal ~ ~ ~ 0.2 0.2 0.2 0.05 25',
                             'playsound minecraft:entity.enderman.teleport neutral @a[distance=..16] ~ ~ ~ 0.6 0.6',
                             'execute on owner run give @s minecraft:ender_pearl 1',
                             'execute on owner run ' + title('@s', 'actionbar', T('The floor drinks your pearl. Walk the path.', 'light_purple')),
                             'kill @s'])
    fn('p2/util/reloot', ['$data modify block ~ ~ ~ LootTable set value "$(loot)"'])
    # 2.13: every victor's vault wears a sign and a beam of light, so nobody walks past it with a Victor's Key in their pocket
    vbt = {'Tags': ['bm.vbtext', 'bm.p2'], 'billboard': 'center', 'see_through': B_(0), 'shadow': B_(1), 'background': Int(0x60000000),
           'brightness': {'block': Int(15), 'sky': Int(15)}, 'line_width': Int(160), 'alignment': 'center',
           'text': [T("VICTOR'S VAULT", '#ffd23f', bold=True), T('\nUse your Victor\'s Key here', 'gray')],
           'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                              'translation': [F(0), F(0.6), F(0)], 'scale': [F(0.9), F(0.9), F(0.9)]}}
    second += [f'execute as @e[type=minecraft:marker,tag=bm.vbeacon,tag=!bm.vbon] at @s run summon minecraft:text_display ~ ~ ~ {snbt(vbt)}',
               'tag @e[type=minecraft:marker,tag=bm.vbeacon] add bm.vbon']
    fast.append('execute as @e[type=minecraft:marker,tag=bm.vbeacon] at @s if entity @a[distance=..28] run function bm:p2/util/vbeam')
    fn('p2/util/vbeam', ['particle minecraft:end_rod ~ ~4 ~ 0.05 3 0.05 0 3', 'particle minecraft:trial_omen ~ ~0.2 ~ 0.4 0.3 0.4 0 3',
                         'particle minecraft:dust{color:[1.0,0.82,0.25],scale:1.4} ~ ~1.5 ~ 0.15 2 0.15 0 4'])
    # 2.13: #hsafe = 1 while nobody in the Hollow Throne still has it to conquer (everyone gets a bm.conq score so "no score" counts as 0)
    second[0:0] = ['scoreboard players add @a bm.conq 0',
                   'execute in bm:hollow_throne store success score #hsafe bm.p2 unless entity @a[distance=0..,gamemode=!spectator,scores={bm.conq=..5}]']
    load.append('scoreboard players set #hsafe bm.p2 0')
    return dict(tick=tick, fast=fast, second=second, load=load, zone=zone_lines)

"""Phase 244 (2.99): THE VORN ARMADA's SOUNDTRACK - the hive-fleet's own music, from the Dock to the Flagship's door
(tools/armada_music.py -> vendor/ar_*.ogg; the Admiral's own, tools/vexis_music.py -> vendor/boss_vexis_*.ogg, phase242/phase152).
Machines and a mind: analog arpeggios, a pulsing sequencer, sub-bass, a theremin, synth brass, the hive choir, struck hull plates.

- Five tiers, one for each stretch of the voyage, each fuller and louder than the last - the trials solved (the Armada's bm.pz,
  p2/armadacfg.PUZZLES) choose it:
    I    THE DOCK                       trials 0-1 solved (the arrival frigate, the gravity lifts)
    II   THE BROOD-CARRIER              2-5   (the tanks, the bio-wave, the quarantine grid, the Brood-Warden)
    III  THE STAR-FORGE                 6-9   (the conduits, the drones, the furnaces, the Forgemaster)
    IV   THE NAVIGATOR                  10-13 (the star-chart, the zero-G crossing, the saucers, the Star-Seer)
    V    THE DREADNOUGHTS AND THE FLAGSHIP  14-18 (the reactors, the Guardians, the Command Lock, the Gauntlet - until it wakes)
- A fight aboard (a Vorn foe - bm.vorn - or a dungeon mob within 20) has music of its own: THE BOARDERS on the early ships, THE
  DREADNOUGHT GUARD once you're aboard the warships (13 solved on). It holds 6 seconds past the last foe, so a lull doesn't
  flicker it.
- The bosses keep their own (phase152: the Cipher guardians' Mothership; the Admiral's coming, forms, entrances and Unlinking,
  phase242). While one plays, or one is dying (a staged death is silent), or Admiral Vexis is awake (bm.avx, not bm.vxdorm:
  its intro, its forms, its turns, its fall), this keeps still. After the fall (#afell): twelve seconds of silence, then THE QUIET
  AFTER (ar_after - the Unlinking's last part, the one voice left), once; then silence until the fleet regroups.
- SMOOTH: every track is D minor, 160 BPM (a bar 1.5 s), in 8-bar sections (12 s) that start on D minor and lean back into it,
  and each player's track is timed from its start. A new tier waits for the next section boundary, with THE SWELL (3 s: a
  reversed cymbal, a riser, the choir sliding up, a roll) over the two bars before it; a fight cuts in on the next two-bar line
  (every 3 s), on its own impact; it hands back on a section boundary, through the swell. Starting from silence, the swell leads
  in (the quiet after starts bare).
- The music channel: the Armada's biome music is a silence (phase241 - checked here), the jukebox channel is the bosses'.
  Leaving the Armada (bm.ain, phase241) stops it.

Importing does nothing; generate(G) runs after phase242 (it reads the Admiral's tags, and mends its fall's first tick - below)."""
PFX = 'p244'
D = 'armada'
# id -> (sound, seconds); 1-5 the tiers, 7-8 the fights, 9 the quiet after (once)
TRACKS = {1: ('ar_t1', 96), 2: ('ar_t2', 120), 3: ('ar_t3', 120), 4: ('ar_t4', 120), 5: ('ar_t5', 120),
          7: ('ar_c1', 60), 8: ('ar_c2', 60), 9: ('ar_after', 36)}
LEAD = 99                                   # (the swell leading in from silence)
TIERS = [(1, '..1'), (2, '2..5'), (3, '6..9'), (4, '10..13'), (5, '14..')]
FIGHT2 = 13                                 # (the Dreadnought Guard from here: Dreadnought A's reactor is trial 14)
FOE_R, CALM = 20, 6
SECTION, SWELL, LINE = 12, 3, 3             # (seconds: a section; the swell, over its last two bars; a two-bar line)
AFTER_WAIT = 12                             # (seconds of silence after the fall before the quiet after)
BOSS_R = 64                                 # (the Admiral awake within this: keep still - phase152 plays its music to 64)
SND = lambda i: f'bm:music.{TRACKS[i][0]}'
try:
    import phase241 as _P241
    COLLAPSE = _P241.COLLAPSE
except Exception:                           # (the Armada's builder not written yet: phase241 still imports, but be safe)
    COLLAPSE = 180
assert SECTION % LINE == 0 and all(ln % SECTION == 0 for i, (_n, ln) in TRACKS.items() if i != 9)


def generate(G):
    fn = G.fn
    objs = ['bm.xam', 'bm.xas', 'bm.xaf', 'bm.xaq']           # (the track, its clock in seconds, a swell played, the calm)
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    vx = 'type=minecraft:husk,tag=bm.avx'
    second = G.FUNCS['loop/second']
    # (once a second, the fleet's state; then each player aboard - phase241 tags them bm.ain at the top of the second)
    second += [f'execute if entity @a[tag=bm.ain] run function bm:{PFX}/sec',
               f'execute as @a[tag=bm.ain] at @s run function bm:{PFX}/tick',
               f'execute as @a[tag=!bm.ain,scores={{bm.xam=1..}}] run function bm:{PFX}/stop']
    fn(f'{PFX}/sec', ['scoreboard players set #xpz bm.rng 0',
                      f'execute store result score #xpz bm.rng run scoreboard players get @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_{D},limit=1] bm.pz',
                      'scoreboard players set #xti bm.rng 1'] +
       [f'execute if score #xpz bm.rng matches {r} run scoreboard players set #xti bm.rng {i}' for i, r in TIERS] +
       ['scoreboard players set #xfight bm.rng 7', f'execute if score #xpz bm.rng matches {FIGHT2}.. run scoreboard players set #xfight bm.rng 8'])

    # ---- what this player should hear: 0 = keep still (a boss's), else a track
    fn(f'{PFX}/want', ['execute if score @s bm.bmt matches 1.. run return 0',
                       'execute if entity @e[tag=bm.cdie,distance=..96] run return 0',
                       f'execute if entity @e[{vx},tag=!bm.vxdorm,distance=..{BOSS_R}] run return 0',
                       f'execute if score #afell bm.p2 matches 1 if score #acol bm.p2 matches {COLLAPSE - AFTER_WAIT + 1}.. run return 0',
                       'execute if score #afell bm.p2 matches 1 run return 9',
                       f'execute if entity @e[tag=bm.vorn,type=!minecraft:player,tag=!bm.cdie,distance=..{FOE_R}] run scoreboard players set @s bm.xaq {CALM}',
                       f'execute if entity @e[tag=bm.dgmob,tag=!bm.cdie,distance=..{FOE_R}] run scoreboard players set @s bm.xaq {CALM}',
                       'execute if score @s bm.xaq matches 1.. run scoreboard players remove @s bm.xaq 1',
                       'execute if score @s bm.xaq matches 1.. run return run scoreboard players get #xfight bm.rng',
                       'return run scoreboard players get #xti bm.rng'])

    # ---- each second: the clock, then - on a two-bar line or a section boundary - the change
    fn(f'{PFX}/tick', [f'execute store result score #xw bm.rng run function bm:{PFX}/want',
                       # (a boss's music, or its silence: ours is already stopped (phase152 stops the music channel) - forget it)
                       f'execute if score #xw bm.rng matches 0 if score @s bm.xam matches 1.. run function bm:{PFX}/stop',
                       'execute if score #xw bm.rng matches 0 run return 0',
                       'scoreboard players add @s bm.xas 1',
                       # (from silence: a fight or the quiet after straight in; anything else the swell, then the track on the boundary)
                       f'execute unless score @s bm.xam matches 1.. if score #xw bm.rng matches 7..9 run return run function bm:{PFX}/play',
                       f'execute unless score @s bm.xam matches 1.. run return run function bm:{PFX}/lead',
                       'scoreboard players operation #xm bm.rng = @s bm.xas', f'scoreboard players set #c bm.rng {SECTION}',
                       'scoreboard players operation #xm bm.rng %= #c bm.rng',
                       'scoreboard players operation #x3 bm.rng = @s bm.xas', f'scoreboard players set #c bm.rng {LINE}',
                       'scoreboard players operation #x3 bm.rng %= #c bm.rng',
                       # (the quiet after plays once, then silence until the fleet regroups)
                       'execute if score @s bm.xam matches 9 if score #xw bm.rng matches 9 run return 0',
                       f'execute if score @s bm.xam = #xw bm.rng run return run function bm:{PFX}/loop',
                       # (into a fight: the next two-bar line)
                       f'execute if score #xw bm.rng matches 7..8 unless score @s bm.xam matches 7..8 if score #x3 bm.rng matches 0 run return run function bm:{PFX}/play',
                       'execute if score #xw bm.rng matches 7..8 unless score @s bm.xam matches 7..8 run return 0',
                       # (everything else: the swell over the last two bars of a section, the change on its boundary)
                       f'execute if score #xm bm.rng matches {SECTION - SWELL} run function bm:{PFX}/swell',
                       f'execute if score #xm bm.rng matches 0 if score @s bm.xaf matches 1 run return run function bm:{PFX}/play',
                       f'function bm:{PFX}/loop'])
    fn(f'{PFX}/lead', ['playsound bm:music.ar_swell music @s ~ ~ ~ 1000 1 1', f'scoreboard players set @s bm.xam {LEAD}',
                       f'scoreboard players set @s bm.xas {SECTION - SWELL}', 'scoreboard players set @s bm.xaf 1'])
    fn(f'{PFX}/swell', ['playsound bm:music.ar_swell music @s ~ ~ ~ 1000 1 1', 'scoreboard players set @s bm.xaf 1'])
    # (the same track on: round again at its end - its length a whole number of sections, so that's a boundary too)
    fn(f'{PFX}/loop', ['execute if score #xm bm.rng matches 1 run scoreboard players set @s bm.xaf 0'] +       # (a boundary gone by: a fresh swell next time)
       [f'execute if score @s bm.xam matches {i} if score @s bm.xas matches {ln}.. run return run function bm:{PFX}/again' for i, (_n, ln) in TRACKS.items() if i != 9])
    fn(f'{PFX}/again', ['scoreboard players set @s bm.xas 0', 'scoreboard players operation #xw bm.rng = @s bm.xam', f'function bm:{PFX}/p'])
    fn(f'{PFX}/play', [f'function bm:{PFX}/hush', 'scoreboard players operation @s bm.xam = #xw bm.rng', 'scoreboard players set @s bm.xas 0',
                       'scoreboard players set @s bm.xaf 0', f'function bm:{PFX}/p'])
    fn(f'{PFX}/p', [f'execute if score #xw bm.rng matches {i} run return run playsound {SND(i)} music @s ~ ~ ~ 1000 1 1' for i in TRACKS])
    fn(f'{PFX}/hush', [f'stopsound @s music {SND(i)}' for i in TRACKS])
    fn(f'{PFX}/stop', [f'function bm:{PFX}/hush', 'stopsound @s music bm:music.ar_swell', 'scoreboard players set @s bm.xam 0', 'scoreboard players set @s bm.xas 0',
                       'scoreboard players set @s bm.xaf 0', 'scoreboard players set @s bm.xaq 0'])
    G.FUNCS['p104/login'] += ['scoreboard players set @s bm.xam 0', 'scoreboard players set @s bm.xas 0']
    G.FUNCS['admin/uninstall'][0:0] = [f'stopsound @a music {SND(i)}' for i in TRACKS] + ['stopsound @a music bm:music.ar_swell']

    # ---- the Admiral's fall: phase242's first tick stopped the jukebox channel - just after phase152 had started the Unlinking
    # on it (p242/fall runs p152/tick, which stops the third form's theme itself), so the Unlinking was never heard. Keep it.
    fall = G.FUNCS.get('p242/falling')
    if fall:
        G.FUNCS['p242/falling'] = [l for l in fall if not (l.startswith('execute if score @s bm.vxt matches 1 run ') and l.endswith(' run stopsound @s record'))]

    # ---- the biome's own music: a silence (phase241 writes it; make sure)
    import json, os
    p = G.path('data', 'bm', 'worldgen', 'biome', f'{D}.json')
    if os.path.exists(p):
        b = json.load(open(p))
        bg = b.setdefault('attributes', {}).get('minecraft:audio/background_music', {})
        if bg.get('default', {}).get('sound', {}).get('sound_id') != 'bm:music.gv_silence':
            b['attributes']['minecraft:audio/background_music'] = {'default': {'sound': {'sound_id': 'bm:music.gv_silence'}, 'min_delay': 12000,
                                                                                'max_delay': 24000, 'replace_current_music': True}}
            json.dump(b, open(p, 'w'), indent=1)


def rp(R):
    import os, shutil
    here = os.path.dirname(os.path.abspath(__file__))
    def post(R2):
        import json
        sj = R2.p('assets', 'bm', 'sounds.json')
        snd = json.load(open(sj)) if os.path.exists(sj) else {}
        os.makedirs(R2.p('assets', 'bm', 'sounds', 'music'), exist_ok=True)
        for nm in [n for n, _l in TRACKS.values()] + ['ar_swell']:
            shutil.copy(os.path.join(here, 'vendor', f'{nm}.ogg'), R2.p('assets', 'bm', 'sounds', 'music', f'{nm}.ogg'))
            snd[f'music.{nm}'] = {'sounds': [{'name': f'bm:music/{nm}', 'stream': True}]}
        R2.wj('assets/bm/sounds.json', snd)
    R.POST.append(post)

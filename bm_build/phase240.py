"""Phase 240 (2.98a): THE UNDERCROWN's SOUNDTRACK - the final dungeon's own music, from the seam to the throne
(tools/undercrown_music.py -> vendor/uc_*.ogg). Strings to the last: violins, cellos and an electric violin.

- Six tiers, one for each stretch of the way down, each fuller and louder than the last - the trials solved (the dungeon's
  bm.pz) choose it:
    I    THE DESCENT        trials 0-4 solved (the Hall of Chains, the Frozen Ward)
    II   THE HEXED DARK     5-9   (the Hexed Ward)
    III  THE DROWNED DEEP   10-14 (the Drowned Ward; the electric violin, far off)
    IV   THE THRONE GATE    15    (the three Shards; the electric violin has the lead)
    V    A THOUSAND EYES    16    (the Stair of Eyes)
    VI   THE LAST DOOR      17    (the antechamber and the throne hall, until it wakes)
- A fight in its halls (a Dread foe within 20) has music of its own: THE THRALLS in the upper wards, THE DREAD KNIGHTS
  from the Drowned Ward down. It holds 6 seconds past the last foe, so a lull doesn't flicker it.
- The bosses keep their own (phase152: the Echoes, the Sovereign's coming and its forms). While one plays, or one is dying
  (its staged death is silent), or the Sovereign is awake, this keeps still. After its fall: AUREL, once - the light it was.
- SMOOTH: every track is F minor, 120 BPM, in 8-bar sections (16 s) that start on F minor and lean back into it, and each
  player's track is timed from its start. A new tier waits for the next section boundary, with THE SWELL (2 s: a reversed
  cymbal, a riser, a timpani roll) over the bar before it; a fight cuts in on the next bar, on its own impact; it hands back
  on a section boundary, through the swell. Starting from silence, the swell leads in.
- The music channel: the biome's own music is a silence (so the Nether's never cuts across it), the jukebox channel is the
  bosses'. Leaving the Undercrown stops it.

Importing does nothing; generate(G) runs after phase238 (it reads the Sovereign's tags)."""
import phase237 as P237

PFX = 'p240'
# id -> (sound, seconds); 1-6 the tiers, 7-8 the fights, 9 Aurel (once)
TRACKS = {1: ('uc_t1', 128), 2: ('uc_t2', 128), 3: ('uc_t3', 128), 4: ('uc_t4', 96), 5: ('uc_t5', 96), 6: ('uc_t6', 128),
          7: ('uc_c1', 64), 8: ('uc_c2', 64), 9: ('uc_after', 120)}
LEAD = 99                                   # (the swell leading in from silence)
TIERS = [(1, '..4'), (2, '5..9'), (3, '10..14'), (4, '15'), (5, '16'), (6, '17..')]
FOE_R, CALM = 20, 6
SND = lambda i: f'bm:music.{TRACKS[i][0]}'


def generate(G):
    fn = G.fn
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add bm.{k} dummy' for k in ('ucm', 'ucs', 'ucf', 'ucq')]
    G.OBJECTIVES += ['bm.ucm', 'bm.ucs', 'bm.ucf', 'bm.ucq']
    sov = 'type=minecraft:husk,tag=bm.usov'
    second = G.FUNCS['loop/second']
    # (once a second, the dungeon's state; then each player inside)
    second += [f'function bm:{PFX}/sec',
               f'execute as @a[tag=bm.uin] at @s run function bm:{PFX}/tick',
               f'execute as @a[tag=!bm.uin,scores={{bm.ucm=1..}}] run function bm:{PFX}/stop']
    fn(f'{PFX}/sec', ['scoreboard players set #upz bm.rng 0',
                      'execute store result score #upz bm.rng run scoreboard players get @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_under,limit=1] bm.pz',
                      'scoreboard players set #uti bm.rng 1'] +
       [f'execute if score #upz bm.rng matches {r} run scoreboard players set #uti bm.rng {i}' for i, r in TIERS] +
       ['scoreboard players set #ufight bm.rng 7', 'execute if score #upz bm.rng matches 10.. run scoreboard players set #ufight bm.rng 8'])

    # ---- what this player should hear: 0 = keep still (a boss's), else a track
    fn(f'{PFX}/want', ['execute if score @s bm.bmt matches 1.. run return 0',
                       'execute if entity @e[tag=bm.cdie,distance=..96] run return 0',
                       f'execute if entity @e[{sov},tag=!bm.svdorm,distance=..128] run return 0',
                       'execute if score #ufell bm.p2 matches 1 run return 9',
                       f'execute if entity @e[tag=bm.udread,distance=..{FOE_R}] run scoreboard players set @s bm.ucq {CALM}',
                       'execute if score @s bm.ucq matches 1.. run scoreboard players remove @s bm.ucq 1',
                       'execute if score @s bm.ucq matches 1.. run return run scoreboard players get #ufight bm.rng',
                       'return run scoreboard players get #uti bm.rng'])

    # ---- each second: the clock, then - on a bar or a section boundary - the change
    fn(f'{PFX}/tick', ['execute store result score #uw bm.rng run function bm:p240/want',
                       # (a boss's music, or its silence: ours is already stopped (phase152 stops the music channel) - forget it)
                       f'execute if score #uw bm.rng matches 0 if score @s bm.ucm matches 1.. run function bm:{PFX}/stop',
                       'execute if score #uw bm.rng matches 0 run return 0',
                       'scoreboard players add @s bm.ucs 1',
                       # (from silence: the swell, then the track two seconds on - on the boundary 16)
                       f'execute unless score @s bm.ucm matches 1.. if score #uw bm.rng matches 7..8 run return run function bm:{PFX}/play',
                       f'execute unless score @s bm.ucm matches 1.. run return run function bm:{PFX}/lead',
                       'scoreboard players operation #um bm.rng = @s bm.ucs', 'scoreboard players set #c bm.rng 16',
                       'scoreboard players operation #um bm.rng %= #c bm.rng',
                       'scoreboard players operation #u2 bm.rng = @s bm.ucs', 'scoreboard players set #c bm.rng 2',
                       'scoreboard players operation #u2 bm.rng %= #c bm.rng',
                       # (Aurel plays once, then silence until it is rebuilt)
                       f'execute if score @s bm.ucm matches 9 if score #uw bm.rng matches 9 run return 0',
                       f'execute if score @s bm.ucm = #uw bm.rng run return run function bm:{PFX}/loop',
                       # (into a fight: the next bar)
                       f'execute if score #uw bm.rng matches 7..8 unless score @s bm.ucm matches 7..8 if score #u2 bm.rng matches 0 run return run function bm:{PFX}/play',
                       f'execute if score #uw bm.rng matches 7..8 unless score @s bm.ucm matches 7..8 run return 0',
                       # (everything else: the swell over the last bar of a section, the change on its boundary)
                       f'execute if score #um bm.rng matches 14 run function bm:{PFX}/swell',
                       f'execute if score #um bm.rng matches 0 if score @s bm.ucf matches 1 run return run function bm:{PFX}/play',
                       f'function bm:{PFX}/loop'])
    fn(f'{PFX}/lead', ['playsound bm:music.uc_swell music @s ~ ~ ~ 1000 1 1', f'scoreboard players set @s bm.ucm {LEAD}',
                       'scoreboard players set @s bm.ucs 14', 'scoreboard players set @s bm.ucf 1'])
    fn(f'{PFX}/swell', ['playsound bm:music.uc_swell music @s ~ ~ ~ 1000 1 1', 'scoreboard players set @s bm.ucf 1'])
    # (the same track on: round again at its end - its length a whole number of sections, so that's a boundary too)
    fn(f'{PFX}/loop', ['execute if score #um bm.rng matches 1 run scoreboard players set @s bm.ucf 0'] +       # (a boundary gone by: a fresh swell next time)
       [f'execute if score @s bm.ucm matches {i} if score @s bm.ucs matches {ln}.. run return run function bm:{PFX}/again' for i, (_n, ln) in TRACKS.items() if i != 9])
    fn(f'{PFX}/again', ['scoreboard players set @s bm.ucs 0', 'scoreboard players operation #uw bm.rng = @s bm.ucm', f'function bm:{PFX}/p'])
    fn(f'{PFX}/play', [f'function bm:{PFX}/hush', 'scoreboard players operation @s bm.ucm = #uw bm.rng', 'scoreboard players set @s bm.ucs 0',
                       'scoreboard players set @s bm.ucf 0', f'function bm:{PFX}/p'])
    fn(f'{PFX}/p', [f'execute if score #uw bm.rng matches {i} run return run playsound {SND(i)} music @s ~ ~ ~ 1000 1 1' for i in TRACKS])
    fn(f'{PFX}/hush', [f'stopsound @s music {SND(i)}' for i in TRACKS])
    fn(f'{PFX}/stop', [f'function bm:{PFX}/hush', 'stopsound @s music bm:music.uc_swell', 'scoreboard players set @s bm.ucm 0', 'scoreboard players set @s bm.ucs 0',
                       'scoreboard players set @s bm.ucf 0', 'scoreboard players set @s bm.ucq 0'])
    G.FUNCS['p104/login'] += ['scoreboard players set @s bm.ucm 0', 'scoreboard players set @s bm.ucs 0']
    G.FUNCS['admin/uninstall'][0:0] = [f'stopsound @a music {SND(i)}' for i in TRACKS]

    # ---- the biome's own music: a silence (the Nether's never cuts across the Undercrown's)
    import json
    p = G.path('data', 'bm', 'worldgen', 'biome', 'undercrown.json')
    b = json.load(open(p))
    b['attributes']['minecraft:audio/background_music'] = {'default': {'sound': {'sound_id': 'bm:music.gv_silence'}, 'min_delay': 12000, 'max_delay': 24000,
                                                                        'replace_current_music': True}}
    json.dump(b, open(p, 'w'), indent=1)


def rp(R):
    import os, shutil
    here = os.path.dirname(os.path.abspath(__file__))
    def post(R2):
        import json
        sj = R2.p('assets', 'bm', 'sounds.json')
        snd = json.load(open(sj)) if os.path.exists(sj) else {}
        os.makedirs(R2.p('assets', 'bm', 'sounds', 'music'), exist_ok=True)
        for nm, src in [(n, f'{n}.ogg') for n, _l in TRACKS.values() if n != 'uc_after'] + [('uc_swell', 'uc_swell.ogg'), ('uc_after', 'disc_aurel.ogg')]:
            shutil.copy(os.path.join(here, 'vendor', src), R2.p('assets', 'bm', 'sounds', 'music', f'{nm}.ogg'))
            snd[f'music.{nm}'] = {'sounds': [{'name': f'bm:music/{nm}', 'stream': True}]}
        R2.wj('assets/bm/sounds.json', snd)
    R.POST.append(post)

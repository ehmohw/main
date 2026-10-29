"""Phase 250 (2.99a): THE BLACK MARKET's OWN MUSIC - "Members Only", a sly noir-swing loop (tools/market_music.py ->
vendor/market_theme.ogg, 75 s: walking upright bass, brushes and a swung ride, a Harmon-muted trumpet with THE HOOK, a
clarinet, Rhodes comping, vibes, an accordion's flourishes).

- WHO HEARS IT: a player inside a market's cavern who came in WITH A KEY. The market is members-only - its vault door opens
  only for someone carrying a Black Market key (bm.haskey, refreshed in loop/fast), and a rat bouncer throws anyone without
  one off the market floor (market/kick) - so "entered with a key" is: inside the cavern, past the vault door, carrying a key.
  Once in, it stays theirs (the tag bm.mkin latches) until they leave the cavern: setting the key down in the Fence's back
  room doesn't stop the band. A keyless creative visitor (the bouncer leaves those alone) hears nothing.
- WHERE THE MARKET IS: every market has its bm.mkt marker at template (38.5, 12, 46.5) of the 76 x 32 x 98 cavern
  (market3.py), turned with the market (yaw 0 / 90 / 180 / -90: mgeo's rule, left = template +x, forward = template +z).
  The cavern INSIDE the vault door is template x 1-75, y 1-32, z 1-82 (the iron door is at z 82; the vestibule and the
  dig-in tunnel south of it are outside) - one box per facing, worked out below from the template box, never by hand.
- THE CHANNEL: 'music', as the area music (phase244, phase240, the heists' phase75), so a player's Music slider governs
  it. The vanilla soundtrack would otherwise wander in over it in the Overworld (there's no market biome to silence it, as
  the Armada's and the Undercrown's have): while the theme plays, the vanilla tracks it could meet are stopped.
- YIELDING (phase244's rules): a boss theme (bm.bmt - phase152 stops the music channel itself while one plays), a staged
  death within 96 (silent), a heist (bm.gvp, the Gutter's dimension), the Armada's or the Undercrown's own music, the Omega
  Palace's waltz - any of these and this keeps still; it comes back from the top once they've gone.
- THE LOOP: timed by its length, as phase244 does - a clock in seconds per player, the track again at 75 (stopped first,
  so a client that fell behind never stacks two). The file renders circularly, so the join is seamless.
- THE SWITCH: operators can turn it off for the server (admin/settings: "Market music"); each player's own Music volume
  slider is theirs. Leaving the market, logging in again, the switch going off or uninstalling stops it.

3.00: THE NIGHTS AND THE SHIPS.
- A VARIANT FOR EACH CUSTOM NIGHT (tools/market_music.py: the same tune, chart, form and 75 s, re-dressed): the Lucky Night's
  (C major, open horn, glockenspiel, chimes, tambourine), the Blood Moon's (CmM7 and flat nines, a low string pedal, the
  organ, war drums, the trumpet growling), an Invasion Night's (arpeggiated synth bass, a drum machine, a pulse lead, a
  theremin, alarms) and a Dread Night's (flat and wavering, a music box, dissonant violins, a heartbeat, a clock).
  The nights, as their own phases keep them (all bm.bm): #lnight (phase22), #inv (phase32, the Vorn), #active (phase15, the
  Blood Moon), #dnight (phase181). The rolls keep them apart (no Lucky Night or invasion on a Blood Moon day, no invasion on a
  Lucky Night, a Dread Night takes the night from either), but the admin commands can stack them: then DREAD > BLOOD MOON >
  INVASION > LUCKY. A track (re)starting plays tonight's; a night beginning or ending mid-track stops it and starts the right
  one on the next second (vanilla has no crossfade).
- THE SHIPS (tools/ship_music.py): aboard an alien MOTHERSHIP (phase25, bm:mothership) "Tractor Beam Bossa" (72 s); aboard a
  VORN DREADNOUGHT (phase32, bm:red_mothership - the Overworld's own warship, not the Armada's Dreadnoughts in the End, which
  have phase244's music) "The Deep Hive" (80 s); each with an Invasion Night variant ("Red Alert", "Battle Stations").
  Aboard is phase148's box: 25 blocks round the ship's beam marker (bm.tbeam / bm.tbeam_red, on the lower deck), from 5 below
  it to 14 above. Anyone aboard hears it (no key needed); the same yielding, loop and stops as the market's. A switch of its
  own ("Ship music").
- bm.mkm is the track playing (TRACKS below: 1-5 the market's, 11-12 the mothership's, 21-22 the Dreadnought's; 0 none), so the
  pack - and a test - can read what a player hears.

Importing does nothing. settings(G) runs before phase153 (it adds its switch to the settings dialog); generate(G) runs
after phase244 (it yields to the Armada's and the Undercrown's objectives, if they're there)."""
PFX = 'p250'
SND = 'bm:music.market_theme'
NAME = 'market_theme'
LENGTH = 75                                 # (seconds - tools/market_music.py: 40 bars at 128 BPM)
CFG = 'mktmus'
SCFG = 'shpmus'                             # (3.00: the ships' switch)
# id -> (sound, seconds). The market's: the theme, then tonight's (1 + the night code below); the ships': normal, invasion.
TRACKS = {1: (NAME, LENGTH), 2: ('market_lucky', LENGTH), 3: ('market_invasion', LENGTH), 4: ('market_blood', LENGTH),
          5: ('market_dread', LENGTH), 11: ('ship_mothership', 72), 12: ('ship_mothership_inv', 72),
          21: ('ship_dreadnought', 80), 22: ('ship_dreadnought_inv', 80)}
SNDS = {i: f'bm:music.{nm}' for i, (nm, _l) in TRACKS.items()}
# the night code (#mkn bm.rng), set in this order so the later wins: dread > blood moon > invasion > lucky
NIGHTS = [(1, '#lnight', 'lucky'), (2, '#inv', 'invasion'), (3, '#active', 'blood moon'), (4, '#dnight', 'dread')]
SHIPS = [('bm.tbeam', 'bm.mshin', 11), ('bm.tbeam_red', 'bm.dnin', 21)]   # (beam marker, aboard tag, its first track)
SHIP_BOX = ((-25, -5, -25), (50, 19, 50))   # (phase148's "aboard": the marker's corner offset, dx dy dz)
# the cavern inside the vault door, in template blocks (market3.py: SX, SY, SZ = 76, 32, 98; the door's iron at z 82)
BOX = ((1, 1, 1), (75, 32, 82))
MKT = (38.5, 12, 46.5)                      # (the bm.mkt marker, template coordinates - mgeo.MKT)
BOSS_STILL = 96                             # (a staged boss death within this: silence, as phase244)
# the vanilla tracks the Overworld could start under it (music.game and every Overworld biome's own)
VANILLA = ['game', 'creative', 'under_water'] + [f'overworld.{b}' for b in (
    'badlands', 'bamboo_jungle', 'cherry_grove', 'deep_dark', 'desert', 'dripstone_caves', 'flower_forest', 'forest', 'frozen_peaks',
    'grove', 'jagged_peaks', 'jungle', 'lush_caves', 'meadow', 'old_growth_taiga', 'snowy_slopes', 'sparse_jungle', 'stony_peaks',
    'sulfur_caves', 'swamp')]
# yaw ranges of the market's marker -> how a template offset (u east, w south at yaw 0) turns into the world's (x, z)
FACINGS = [('-45..45', lambda u, w: (u, w)),
           ('45..135', lambda u, w: (-w, u)),
           ('135..180', lambda u, w: (-u, -w)),
           ('-180..-135', lambda u, w: (-u, -w)),
           ('-135..-45', lambda u, w: (w, -u))]


def boxes():
    """(yaw range, (x, y, z) offset from the marker to the box's low corner, (dx, dy, dz)) - one per facing"""
    (x0, y0, z0), (x1, y1, z1) = BOX
    out = []
    for yr, turn in FACINGS:
        cs = [turn(u - MKT[0], w - MKT[2]) for u in (x0, x1) for w in (z0, z1)]
        lo_x, hi_x = min(c[0] for c in cs), max(c[0] for c in cs)
        lo_z, hi_z = min(c[1] for c in cs), max(c[1] for c in cs)
        # (a selector's volume reaches dx + 1 past its corner: take that 1 off so the box is the cavern's exactly)
        out.append((yr, (lo_x, y0 - MKT[1], lo_z), (hi_x - lo_x - 1, y1 - y0 - 1, hi_z - lo_z - 1)))
    return out


def _n(v):
    return f'{v:g}'


def settings(G):
    """the operators' switch, in the server settings dialog (phase153 reads its SETTINGS when it generates)"""
    import phase153
    if all(k != CFG for k, *_r in phase153.SETTINGS):
        phase153.SETTINGS.append((CFG, 'Market music', 'The Black Market\'s own swing, for key-holders inside a market.'))
    if all(k != SCFG for k, *_r in phase153.SETTINGS):
        phase153.SETTINGS.append((SCFG, 'Ship music', 'The alien mothership\'s and the Vorn Dreadnought\'s own music, for anyone aboard.'))
    for key in (CFG, SCFG):
        G.FUNCS['load'][-1:-1] = [f'execute unless score #{key} bm.cfg matches -2147483648.. run scoreboard players set #{key} bm.cfg 1']
    G.fn(f'admin/set/{CFG}_0', [f'scoreboard players set #{CFG} bm.cfg 0', f'execute as @a[scores={{bm.mkm=1..9}}] run function bm:{PFX}/stop',
                                'function bm:admin/settings'])
    G.fn(f'admin/set/{SCFG}_0', [f'scoreboard players set #{SCFG} bm.cfg 0', f'execute as @a[scores={{bm.mkm=11..}}] run function bm:{PFX}/stop',
                                 'function bm:admin/settings'])
    for key in (CFG, SCFG):
        G.fn(f'admin/set/{key}_1', [f'scoreboard players set #{key} bm.cfg 1', 'function bm:admin/settings'])


def generate(G):
    fn = G.fn
    objs = ['bm.mkm', 'bm.mks']                         # (the track playing - its TRACKS id, 0 none; its clock in seconds)
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ---- each second: who's inside a market (by its facing), who came in with a key; who's aboard a ship; tonight's night
    here = ['tag @a remove bm.mkhere']
    for yr, (ox, oy, oz), (dx, dy, dz) in boxes():
        here.append(f'execute as @e[type=minecraft:marker,tag=bm.mkt,y_rotation={yr}] at @s positioned ~{_n(ox)} ~{_n(oy)} ~{_n(oz)} '
                    f'run tag @a[dx={_n(dx)},dy={_n(dy)},dz={_n(dz)}] add bm.mkhere')
    here += ['tag @a[tag=bm.mkhere,tag=bm.haskey] add bm.mkin',                 # (in with a key: theirs until they leave)
             'tag @a[tag=bm.mkin,tag=!bm.mkhere] remove bm.mkin',
             'tag @a[tag=bm.mkin,tag=bm.gvp] remove bm.mkin']                   # (never in a heist)
    fn(f'{PFX}/sec', here)
    (cx, cy, cz), (bx, by, bz) = SHIP_BOX
    ships = [f'tag @a remove {tag}' for _m, tag, _i in SHIPS]
    for mk, tag, _i in SHIPS:
        ships.append(f'execute as @e[type=minecraft:marker,tag={mk}] at @s positioned ~{cx} ~{cy} ~{cz} run tag @a[dx={bx},dy={by},dz={bz},tag=!bm.mkin] add {tag}')
    night = ['scoreboard players set #mkn bm.rng 0'] + [f'execute if score {flag} bm.bm matches 1 run scoreboard players set #mkn bm.rng {k}'
                                                         for k, flag, _w in NIGHTS]
    night += ['scoreboard players operation #mkid bm.rng = #mkn bm.rng', 'scoreboard players add #mkid bm.rng 1']
    for _m, tag, first in SHIPS:                                                # (a ship's track: its own, or its invasion night's)
        night += [f'scoreboard players set #mk{first} bm.rng {first}', f'execute if score #inv bm.bm matches 1 run scoreboard players set #mk{first} bm.rng {first + 1}']
    fn(f'{PFX}/night', night)
    G.FUNCS['loop/second'] += [f'execute if entity @e[type=minecraft:marker,tag=bm.mkt] run function bm:{PFX}/sec',
                               'execute unless entity @e[type=minecraft:marker,tag=bm.mkt] run tag @a remove bm.mkin'] + ships + [
                               'tag @a remove bm.muz'] + [f'tag @a[tag={t}] add bm.muz' for t in ['bm.mkin'] + [tag for _m, tag, _i in SHIPS]] + [
                               f'execute if entity @a[tag=bm.muz] run function bm:{PFX}/night',
                               f'execute as @a[tag=bm.muz] at @s run function bm:{PFX}/tick',
                               f'execute as @a[tag=!bm.muz,scores={{bm.mkm=1..}}] run function bm:{PFX}/stop']

    # ---- what may this player hear now? 0 = keep still (another's music, a silence, the switch off), else the track's id
    want = ['execute if score @s bm.bmt matches 1.. run return 0',
            f'execute if entity @e[tag=bm.cdie,distance=..{BOSS_STILL}] run return 0',
            'execute if entity @s[tag=bm.gvp] run return 0',
            'execute if dimension bm:gutter run return 0']
    for obj, why in (('bm.xam', 'the Armada'), ('bm.ucm', 'the Undercrown'), ('bm.gvmt', 'a heist'), ('bm.ommu', 'the Omega Palace')):
        if obj in G.OBJECTIVES:
            want.append(f'execute if score @s {obj} matches 1.. run return 0')
    want += [f'execute if entity @s[tag=bm.mkin] unless score #{CFG} bm.cfg matches 1 run return 0',
             'execute if entity @s[tag=bm.mkin] run return run scoreboard players get #mkid bm.rng',
             f'execute unless score #{SCFG} bm.cfg matches 1 run return 0']
    want += [f'execute if entity @s[tag={tag}] run return run scoreboard players get #mk{first} bm.rng' for _m, tag, first in SHIPS]
    want.append('return 0')
    fn(f'{PFX}/want', want)

    # ---- the track: started when it isn't the one this player should hear (from silence, or tonight changed), again at its end
    lengths = {}
    for i, (_nm, ln) in TRACKS.items(): lengths.setdefault(ln, []).append(i)
    again = []
    for ln, ids in sorted(lengths.items()):
        for lo, hi in _runs(sorted(ids)):
            again.append(f'execute if score @s bm.mkm matches {lo}..{hi} if score @s bm.mks matches {ln}.. run return run function bm:{PFX}/play')
    fn(f'{PFX}/tick', [f'execute store result score #mkw bm.rng run function bm:{PFX}/want',
                       f'execute if score #mkw bm.rng matches 0 if score @s bm.mkm matches 1.. run function bm:{PFX}/stop',
                       'execute if score #mkw bm.rng matches 0 run return 0',
                       f'execute unless score @s bm.mkm = #mkw bm.rng run return run function bm:{PFX}/play',
                       'scoreboard players add @s bm.mks 1'] + again + [f'function bm:{PFX}/hush_vanilla'])
    fn(f'{PFX}/play', [f'function bm:{PFX}/hush', f'function bm:{PFX}/hush_vanilla'] +
       [f'execute if score #mkw bm.rng matches {i} run playsound {SNDS[i]} music @s ~ ~ ~ 1000 1 1' for i in TRACKS] +
       ['scoreboard players operation @s bm.mkm = #mkw bm.rng', 'scoreboard players set @s bm.mks 0'])
    fn(f'{PFX}/hush', [f'stopsound @s music {SNDS[i]}' for i in TRACKS])      # (every one of ours: a client that fell behind never stacks two)
    fn(f'{PFX}/hush_vanilla', [f'stopsound @s music minecraft:music.{v}' for v in VANILLA])
    fn(f'{PFX}/stop', [f'function bm:{PFX}/hush', 'scoreboard players set @s bm.mkm 0', 'scoreboard players set @s bm.mks 0'])
    G.FUNCS['p104/login'] += ['scoreboard players set @s bm.mkm 0', 'scoreboard players set @s bm.mks 0', 'tag @s remove bm.mkin', 'tag @s remove bm.muz'] + \
                             [f'tag @s remove {tag}' for _m, tag, _i in SHIPS]
    G.FUNCS['admin/uninstall'][0:0] = [f'stopsound @a music {SNDS[i]}' for i in TRACKS]


def _runs(ids):
    """consecutive ids as (lo, hi) ranges"""
    out = []
    for i in ids:
        if out and out[-1][1] == i - 1: out[-1][1] = i
        else: out.append([i, i])
    return [tuple(r) for r in out]

def rp(R):
    import os, shutil
    here = os.path.dirname(os.path.abspath(__file__))
    def post(R2):
        import json
        sj = R2.p('assets', 'bm', 'sounds.json')
        snd = json.load(open(sj)) if os.path.exists(sj) else {}
        os.makedirs(R2.p('assets', 'bm', 'sounds', 'music'), exist_ok=True)
        for nm, _ln in TRACKS.values():                 # (the theme, its four nights, the two ships and their invasion nights)
            shutil.copy(os.path.join(here, 'vendor', f'{nm}.ogg'), R2.p('assets', 'bm', 'sounds', 'music', f'{nm}.ogg'))
            snd[f'music.{nm}'] = {'sounds': [{'name': f'bm:music/{nm}', 'stream': True}]}
        R2.wj('assets/bm/sounds.json', snd)
    R.POST.append(post)

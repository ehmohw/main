"""3.1a: THE PIERCING BLOW, SEEN - the owner: "They should only vanish and appear if it suits their character design. Like Cecil or
Omega, who are shadowy and ghastly... I think it'd be cooler if the Dread Sovereign's played out on screen."

So only seven still vanish (phase226.FLAV, each now with a particle signature of its own, POLISH below):
  King Omega and Cecil (ghastly and shadowy - the owner's own two), the Glitch (dropped frames ARE how it moves), the Stalker (its kit
  already steps out of the dark), Pistachio (a ghost), Wilfrey (a risen skeleton king, out of his own grave - a vanilla body, no rig)
  and the Mireling (a shadow that lives in its puddle).
The other forty go in where you can see them, as phase226.ASSAULT's eleven always have: atk.sig (kid 3) on their own poses, an
eased dash in (never a teleport), the attack kit's hit-stop and impact on every blow, the same 14 of rend split across the blows,
about a second and a half. Each: ASSAULT[w] (phase226's format - pfx, the state score, the busy score, the dash, the hits, the
timeline) and NAMES[w] (the move's name, what it does - the Champion's announcement).

New in the timeline (phase226.assault): 'PULLX a..b' - PULL with the follower's own trail (pull_fx). New keys: tick / state / place / face / st / pose (a follower whose engine isn't rigpet's: Zib,
KillerWatt), lite (the Frog and Donado: a jointed rig of baked poses and no state machine - the move gets a small tick of its
own, p226/lite/<w>, and holds their anim while it plays), free (start only once the follower's own move is over).

Data only: phase226 merges it (the fol5 followers' entries only while they're switched on)."""

# (3.1a) the switch: off until the conversions have passed the six checkers and a playtest (phase226 merges nothing while it's off -
# every follower vanishes as before 3.1a)
ON = False

_c = lambda r, g, b, s=1.1: f'minecraft:dust{{color:[{r},{g},{b}],scale:{s}}}'
SL = lambda c: [f'particle {c} ~ ~1 ~ 0.35 0.4 0.35 0 10', 'particle minecraft:sweep_attack ~ ~1 ~ 0.2 0.1 0.2 0 1']
CRIT = 'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.3 10'
FOE = '@e[tag=bm.prfoe,limit=1]'
at = lambda c: f'execute at {FOE} run {c}'
S = lambda s, v=1, p=1: f'S minecraft:{s} {v} {p}'
D = lambda reach=1.6, speed=1.0, lift=1: dict(reach=reach, speed=speed, lift=lift)
SLOW = 'effect give @s minecraft:slowness 2 3 true'


def R(pfx, q, end, dash, hits, tl, **kw):
    """a rigpet follower (its state bm.<q>s, its busy bm.<q>x)"""
    return dict(pfx=pfx, s_obj=f'bm.{q}s', anim=f'{pfx}/anim', busy=f'bm.{q}x', end=end, dash=dash, hits=hits, tl=tl, free=True, **kw)


def combo(t, n, gap, up, hit, k, extra=()):
    """n blows from tick t, `gap` apart: the wind-up pose, and a tick later the strike with hit k"""
    out = {}
    for i in range(n):
        out[t + i * gap] = [f'P {up}']
        out[t + i * gap + 1] = [f'P {hit}', f'H{k}'] + list(extra)
    return out


def tl_of(*parts):
    out = {}
    for p in parts:
        for t, c in p.items():
            out[t] = out.get(t, []) + list(c)
    return out


ASSAULT, NAMES = {}, {}

# ================================================================================================ batch 1: the 2.94u fighters
# ---- CELI: an ice spear - in through a flurry, three thrusts, frozen, and the spear slammed home
ASSAULT['celi'] = dict(pfx='p66', s_obj='bm.ces', anim='p66/anim', busy='bm.cek', end=27, dash=D(1.8, 1.1, 1), free=True,
    hits={1: (3, ['particle minecraft:snowflake ~ ~1 ~ 0.3 0.4 0.3 0.05 12', 'effect give @s minecraft:slowness 2 6 true'], 'minecraft:item.trident.hit', 1.4),
          2: (5, ['particle minecraft:snowflake ~ ~1 ~ 0.6 0.6 0.6 0.2 40', 'particle minecraft:block{block_state:"minecraft:packed_ice"} ~ ~1 ~ 0.4 0.5 0.4 0 30',
                  'effect give @s minecraft:slowness 3 9 true'], 'minecraft:block.glass.break', 0.8)},
    tl=tl_of({1: ['P stab_back', S('block.powder_snow.step', 1, 0.6), 'particle minecraft:snowflake ~ ~1 ~ 0.4 0.6 0.4 0.03 16'], 3: ['DASH']},
             combo(4, 3, 3, 'stab_back', 'stab', 1), {14: ['P throw_back', S('item.trident.throw', 0.8, 0.7)], 18: ['P throw', 'H2'], 24: ['P huff']}))
NAMES['celi'] = ('Whiteout Lance', 'drives in through a flurry, freezes the monster with three thrusts of her ice spear, and slams it home')

# ---- ZIB: a Donadian trooper - charge the ray gun, run in, three point-blank shots, the overcharge
ASSAULT['zib'] = dict(pfx='p72/zb', s_obj='bm.ksg', anim='p72/zb/anim', state='p72/zb/anim', place='p72/zb/anim', tick='p72/zb/tick', face='none', st=99999,
    pose='p72/zb/p/{}', busy='bm.zbk', end=30, dash=D(2.4, 1.1, 0), free=True,
    hits={1: (3, ['particle minecraft:end_rod ~ ~1 ~ 0.2 0.3 0.2 0.1 8', 'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.3 0.3 0.2 12'], 'minecraft:block.beacon.power_select', 1.8),
          2: (5, ['particle minecraft:end_rod ~ ~1 ~ 0.5 0.5 0.5 0.2 30', f'particle {_c(0.3, 1.0, 0.9, 1.8)} ~ ~1 ~ 0.6 0.6 0.6 0 30', 'effect give @s minecraft:glowing 2 0 true',
                  'effect give @s minecraft:slowness 2 9 true'], 'minecraft:entity.generic.explode', 1.7)},
    tl={1: ['P charge', S('block.beacon.activate', 0.7, 1.9), 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.4 0.3 0.05 10'], 3: ['P runaim0', 'DASH'],
        4: ['P aim'], 5: ['P fire', 'H1'], 8: ['P aim'], 9: ['P fire', 'H1'], 12: ['P aim'], 13: ['P fire', 'H1'],
        16: ['P charge', S('block.respawn_anchor.charge', 0.8, 1.6)], 21: ['P aim'], 22: ['P fire', 'H2'], 27: ['P idle0']})
NAMES['zib'] = ('Point Blank', 'charges his ray gun, runs in shooting and overcharges it into the monster at arm\'s length')

# ---- KILLERWATT: living current - crouched, a leap in, tendril punches crackling, and the slam that grounds it
ASSAULT['kw'] = dict(pfx='p79/pet', s_obj='bm.ksg', anim='p79/pet/move', state='p79/pet/move', place='p79/pet/place', tick='p79/pet/tick', face='none', st=99999,
    pose='p79/pet/pose/{}', busy='bm.kxatk', end=30, dash=D(2.2, 1.1, 3), free=True,
    hits={1: (2, ['particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.3 16'], 'minecraft:entity.player.attack.strong', 1.3),
          2: (8, ['particle minecraft:electric_spark ~ ~0.3 ~ 1.4 0.2 1.4 0.4 60', 'particle minecraft:flash{color:[0.5,1.0,0.4,1.0]} ~ ~1 ~ 0 0 0 0 1',
                  'effect give @s minecraft:slowness 2 4 true'], 'minecraft:entity.lightning_bolt.impact', 1.2)},
    tl={1: ['P crouch', S('block.respawn_anchor.charge', 1, 1.4), 'particle minecraft:electric_spark ~ ~0.5 ~ 0.5 0.2 0.5 0.2 20'], 4: ['P slam_up', 'DASH'],
        5: ['P punch_l', 'H1'], 7: ['P punch_r', 'H1'], 9: ['P stab'], 10: ['P punch_l', 'H1'],
        13: ['P slam_up', S('entity.lightning_bolt.thunder', 0.3, 1.8)], 18: ['P slam_dn', 'H2'], 23: ['P roar', S('entity.ravager.roar', 0.7, 1.5)], 27: ['P idle_a']})
NAMES['kw'] = ('Live Wire', 'leaps onto the monster crackling, punches the current into it and slams it into the ground')

# ---- APOPHISS: the Serpent King - he coils it in, mace up, the slam, and the bite through its guard
ASSAULT['apo'] = dict(pfx='p131', s_obj='bm.aps', anim='p131/anim', busy='bm.apx', end=32, dash=D(2.2, 1.0, 0), free=True,
    pull_fx='particle minecraft:soul_fire_flame ~ ~0.4 ~ 0.2 0.1 0.2 0.01 3',
    hits={1: (3, ['particle minecraft:soul_fire_flame ~ ~1 ~ 0.4 0.5 0.4 0.04 14', 'effect give @s minecraft:slowness 2 9 true'], 'minecraft:entity.ravager.attack', 1.3),
          2: (7, ['particle minecraft:soul_fire_flame ~ ~0.3 ~ 1.2 0.2 1.2 0.06 40', 'particle minecraft:block{block_state:"minecraft:deepslate"} ~ ~0.2 ~ 0.8 0.1 0.8 0 30'],
              'minecraft:block.anvil.land', 0.6),
          3: (4, ['particle minecraft:crit ~ ~1.4 ~ 0.3 0.3 0.3 0.4 16', 'effect give @s minecraft:wither 2 0 true'], 'minecraft:entity.evoker_fangs.attack', 0.7)},
    tl={1: ['P battle', S('entity.evoker_fangs.attack', 0.6, 0.5), 'particle minecraft:soul_fire_flame ~ ~0.3 ~ 0.8 0.1 0.8 0.02 16'], 3: ['P slither_a', 'DASH'],
        4: ['P claw', 'H1', 'PULLX 4..6'], 8: ['P mace_up', S('item.mace.smash_ground', 0.4, 0.6)], 11: ['P mace_back'], 14: ['P mace_slam', 'H2'],
        19: ['P bite', 'H3'], 24: ['P roar', S('entity.ravager.roar', 0.6, 0.6)], 29: ['P idle_a']})
NAMES['apo'] = ("Serpent's Coil", 'coils round the monster in black fire, brings his mace down on it and sinks his fangs in')

# ---- FISHY: a splash in, two strikes, and the thunder called down on it
ASSAULT['fishy'] = R('p145', 'fy', 30, D(1.7, 1.0, 1),
    hits={1: (3, ['particle minecraft:splash ~ ~1 ~ 0.3 0.4 0.3 0.2 20', 'particle minecraft:bubble_pop ~ ~1 ~ 0.3 0.3 0.3 0.05 10'], 'minecraft:entity.player.splash', 1.4),
          2: (8, ['particle minecraft:electric_spark ~ ~1 ~ 0.4 1.0 0.4 0.3 40', 'particle minecraft:splash ~ ~0.4 ~ 1 0.2 1 0.3 40', 'particle minecraft:flash{color:[0.6,0.8,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1'],
              'minecraft:entity.lightning_bolt.impact', 1.4)},
    tl=tl_of({1: ['P point', S('block.bubble_column.upwards_inside', 1, 1.2)], 3: ['P splash', 'DASH']}, combo(4, 2, 4, 'strike_back', 'strike', 1),
             {13: ['P thunder_up', S('entity.lightning_bolt.thunder', 0.3, 1.6), 'particle minecraft:cloud ~ ~2.6 ~ 0.6 0.1 0.6 0 10'], 18: ['P thunder', 'H2'], 26: ['P bow']}))
NAMES['fishy'] = ('Thundercrash', 'splashes in, strikes twice and calls the thunder down on the monster')

# ---- DENNIS: a charge, the wrench three times, and the overhead into the ground - gold everywhere
ASSAULT['dennis'] = R('p163/dw', 'dw', 30, D(1.8, 1.0, 1),
    hits={1: (2, ['particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.3 10', 'particle minecraft:wax_on ~ ~1 ~ 0.3 0.3 0.3 0 6'], 'minecraft:block.anvil.land', 1.6),
          2: (8, ['particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.3 ~ 1 0.2 1 0 40', 'particle minecraft:wax_on ~ ~0.5 ~ 1 0.3 1 0 20'], 'minecraft:entity.generic.explode', 1.3)},
    tl=tl_of({1: ['P swing_back', S('entity.iron_golem.step', 1, 1.2)], 3: ['DASH']}, combo(4, 3, 3, 'swing_back', 'swing', 1),
             {14: ['P slam_up', S('block.anvil.place', 0.5, 0.8)], 19: ['P slam', 'H2'], 26: ['P idle_a']}))
NAMES['dennis'] = ('Pick Your Battles', 'charges in, whacks the monster three times with his wrench and brings it down overhead in a burst of gold')

# ---- ASHUR: a flame slap, a cast point-blank, and the eruption under it
ASSAULT['ashur'] = dict(pfx='p185', s_obj='bm.azs', anim='p185/anim', busy='bm.azx', end=30, dash=D(1.7, 1.0, 1), free=True,
    hits={1: (3, ['particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.05 16', 'data merge entity @s {Fire:40s}'], 'minecraft:entity.blaze.shoot', 1.4),
          2: (8, ['particle minecraft:flame ~ ~0.3 ~ 0.8 0.1 0.8 0.1 50', 'particle minecraft:lava ~ ~0.5 ~ 0.6 0.3 0.6 0 12', 'data merge entity @s {Fire:80s}'],
              'minecraft:item.firecharge.use', 0.7)},
    tl=tl_of({1: ['P crouch', S('block.fire.ambient', 1, 1.4), 'particle minecraft:small_flame ~ ~1 ~ 0.3 0.4 0.3 0.02 10'], 3: ['DASH']}, combo(4, 2, 4, 'cast_back', 'cast', 1),
             {13: ['P blast', S('entity.blaze.ambient', 0.8, 1.2)], 18: ['P erupt', 'H2'], 26: ['P idle']}))
NAMES['ashur'] = ('Backdraft', 'slaps the monster alight twice, point-blank, and erupts under it')

# ---- THE NEIGHBOR: strikes on the beat, and the crescendo on the downbeat
ASSAULT['neighbor'] = R('p187', 'nq', 32, D(1.6, 1.0, 1),
    hits={1: (2, ['particle minecraft:note ~ ~1.6 ~ 0.4 0.3 0.4 1 4', CRIT], 'minecraft:block.note_block.snare', 1.2),
          2: (8, ['particle minecraft:note ~ ~1 ~ 1 0.6 1 1 14', 'particle minecraft:sonic_boom ~ ~1 ~ 0 0 0 0 1'], 'minecraft:block.note_block.bass', 0.5)},
    tl=tl_of({1: ['P conduct_a', S('block.note_block.chime', 1, 0.8)], 3: ['DASH']},
             {4: ['P strike_up'], 5: ['P strike', 'H1', S('block.note_block.bell', 0.6, 0.8)], 7: ['P strike_up'], 8: ['P strike', 'H1', S('block.note_block.bell', 0.6, 1.0)],
              10: ['P strike_up'], 11: ['P strike', 'H1', S('block.note_block.bell', 0.6, 1.2)], 14: ['P conduct_b'], 17: ['P crescendo', S('block.note_block.bell', 1, 1.5)],
              21: ['P strike', 'H2'], 28: ['P bow']}))
NAMES['neighbor'] = ('Downbeat', 'strikes the monster on one, two, three - and brings the whole orchestra down on four')

# ---- QUEEN AVA: she rides her tide in, the strike, and the whole sea on it
ASSAULT['ava'] = R('p189', 'aq', 32, D(1.8, 1.0, 0),
    hits={1: (4, ['particle minecraft:splash ~ ~1 ~ 0.4 0.5 0.4 0.2 20', 'particle minecraft:glow ~ ~1 ~ 0.3 0.3 0.3 0 6'], 'minecraft:entity.player.splash.high_speed', 1.3),
          2: (6, ['particle minecraft:splash ~ ~0.5 ~ 1.4 0.3 1.4 0.3 60', 'particle minecraft:nautilus ~ ~1 ~ 0.6 0.6 0.6 0.5 20', 'effect give @s minecraft:slowness 2 4 true'],
              'minecraft:block.conduit.attack.target', 0.8)},
    tl={1: ['P cast_up', S('block.conduit.activate', 0.8, 1.2), 'particle minecraft:bubble_pop ~ ~1 ~ 0.6 0.6 0.6 0.05 16'], 3: ['P ward_a', 'DASH'],
        4: ['P cast', 'H1', 'particle minecraft:splash ~ ~0.2 ~ 0.6 0.1 0.6 0.2 20'], 8: ['P cast_up'], 9: ['P cast', 'H1'],
        13: ['P ward_b', S('ambient.underwater.enter', 0.8, 1.2)], 18: ['P tide', 'H2'], 26: ['P curtsey']})
NAMES['ava'] = ('Riptide Sovereign', 'rides her tide in, strikes twice and brings the sea down on the monster')

# ---- QUEEN PEARL: a twirl in, flick, flick, flick, and a royal proclamation to its face
ASSAULT['pearlq'] = R('p190', 'pk', 32, D(1.6, 1.0, 0),
    hits={1: (2, ['particle minecraft:end_rod ~ ~1 ~ 0.3 0.3 0.3 0.05 8', CRIT], 'minecraft:entity.player.attack.sweep', 1.8),
          2: (8, ['particle minecraft:end_rod ~ ~1 ~ 0.8 0.6 0.8 0.08 30', 'particle minecraft:glow ~ ~1 ~ 0.5 0.5 0.5 0 12', 'effect give @s minecraft:slowness 2 4 true'],
              'minecraft:block.amethyst_block.chime', 0.7)},
    tl=tl_of({1: ['P twirl', S('block.amethyst_block.resonate', 1, 1.4), 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.03 10'], 3: ['DASH']},
             combo(4, 3, 3, 'flick_up', 'flick', 1), {14: ['P twirl'], 18: ['P proclaim', 'H2', S('block.bell.use', 1, 1.2)], 25: ['P wink']}))
NAMES['pearlq'] = ('By Royal Decree', 'twirls in, flicks the monster three times and proclaims it finished to its face')

# ---- THE ARACHNO-LANTERN: it rears, leaps onto it, lashes with both forelegs, and the flare
ASSAULT['lantern'] = R('p194', 'lj', 32, D(1.8, 1.0, 3),
    hits={1: (2, ['particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.03 10', CRIT], 'minecraft:entity.spider.hurt', 0.6),
          2: (8, ['particle minecraft:flame ~ ~0.8 ~ 0.8 0.5 0.8 0.08 40', 'particle minecraft:lava ~ ~1 ~ 0.5 0.4 0.5 0 10', 'data merge entity @s {Fire:80s}'], 'minecraft:item.firecharge.use', 0.7)},
    tl=tl_of({1: ['P rear', S('entity.spider.ambient', 1, 0.6)], 4: ['DASH']},
             {5: ['P stomp', 'H1'], 7: ['P lash_a', 'H1'], 9: ['P lash_b', 'H1'], 12: ['P rear', S('block.fire.ambient', 1, 0.7)], 17: ['P flare', 'H2'], 27: ['P idle_a']}))
NAMES['lantern'] = ('Kindled Pounce', 'leaps onto the monster, lashes it with both forelegs and flares its gourd in its face')

# ---- MR. CAPSHUN: a swipe of the brush, paint across it, and a flung splat of every colour
ASSAULT['capshun'] = R('p198', 'zq', 32, D(1.6, 1.0, 1),
    hits={1: (2, ['particle ' + _c(0.1, 0.1, 0.1, 1.4) + ' ~ ~1 ~ 0.4 0.4 0.4 0 12', CRIT], 'minecraft:entity.player.attack.sweep', 1.5),
          2: (8, ['particle ' + _c(0.9, 0.2, 0.6, 1.6) + ' ~ ~0.8 ~ 0.8 0.5 0.8 0 30', 'particle ' + _c(0.2, 0.6, 1.0, 1.6) + ' ~ ~0.8 ~ 0.8 0.5 0.8 0 30',
                  'particle ' + _c(1.0, 0.85, 0.2, 1.6) + ' ~ ~0.8 ~ 0.8 0.5 0.8 0 30', 'effect give @s minecraft:blindness 2 0 true'], 'minecraft:entity.slime.squish', 0.8)},
    tl=tl_of({1: ['P scribble_a', S('item.book.page_turn', 1, 1.2)], 3: ['DASH']},
             {4: ['P swipe_up'], 5: ['P swipe', 'H1'], 7: ['P paint_a', 'H1'], 9: ['P paint_b', 'H1'],
              12: ['P fling_up', S('entity.slime.jump', 0.8, 1.4)], 17: ['P fling', 'H2'], 25: ['P happy']}))
NAMES['capshun'] = ('Final Draft', 'swipes in with his brush, paints right across the monster and flings a splat of every colour at it')

# ================================================================================================ batch 2: the Buddies, the 8-bit trio, the Gentry
# ---- THE SKY BUDDIES: the storm gathers in view - zaps from Nimbus, and Sunny's beam on it
ASSAULT['sky'] = R('p211', 'yq', 32, D(1.8, 0.9, 2),
    hits={1: (2, ['particle minecraft:electric_spark ~ ~1 ~ 0.3 0.6 0.3 0.3 16', 'particle minecraft:falling_water ~ ~2 ~ 0.4 0.1 0.4 0 8'], 'minecraft:entity.lightning_bolt.impact', 2.0),
          2: (8, ['particle minecraft:end_rod ~ ~3 ~ 0.1 2 0.1 0 40', 'particle minecraft:flash{color:[1.0,0.92,0.5,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:electric_spark ~ ~0.4 ~ 1 0.2 1 0.3 40'],
              'minecraft:entity.lightning_bolt.thunder', 1.6)},
    tl={1: ['P forecast_a', 'particle minecraft:cloud ~ ~3 ~ 1 0.2 1 0.01 12', S('entity.breeze.wind_burst', 0.6, 0.8)], 3: ['P forecast_b', 'DASH'],
        4: ['P zap_up'], 5: ['P zap', 'H1'], 7: ['P zap_up'], 8: ['P zap', 'H1'], 10: ['P drizzle', 'H1', 'particle minecraft:falling_water ~ ~2.5 ~ 0.8 0.2 0.8 0 20'],
        13: ['P beam_up', at('particle minecraft:cloud ~ ~3.4 ~ 0.6 0.1 0.6 0 16')], 18: ['P beam', 'H2'], 27: ['P happy']})
NAMES['sky'] = ('Storm Front', 'gather a storm over the monster - Nimbus zaps it, Snooze rains on it, and Sunny brings the beam down')

# ---- 8-BIT CECIL / LEO / EMMA: frame by frame, as their kid-1 moves are
_px = lambda name, n, t0: {t0 + i: [f'P {name}_{i}'] for i in range(n)}
ASSAULT['pxcecil'] = R('p213c', 'xd', 30, D(1.6, 1.0, 0),
    hits={1: (4, ['particle minecraft:witch ~ ~1 ~ 0.3 0.4 0.3 0.1 12', CRIT], 'minecraft:block.note_block.bit', 1.4),
          2: (6, ['particle minecraft:witch ~ ~1 ~ 0.6 0.6 0.6 0.2 30', 'particle ' + _c(0.6, 0.2, 0.9, 1.5) + ' ~ ~1 ~ 0.5 0.5 0.5 0 20'], 'minecraft:entity.evoker.cast_spell', 1.4)},
    tl=tl_of(_px('hex', 3, 1), {3: ['DASH', S('block.note_block.bit', 1, 0.8)]}, _px('attack', 9, 4), {6: ['H1'], 9: ['H1']}, _px('hex', 9, 13), {21: ['H2'], 27: ['P idle_a']}))
NAMES['pxcecil'] = ('Hex Combo', 'blips in, strikes twice in eight-bit and casts his hex point-blank')
ASSAULT['pxleo'] = R('p213l', 'xo', 30, D(1.6, 1.2, 0),
    hits={1: (4, SL(_c(0.3, 0.7, 0.9)), 'minecraft:block.note_block.bit', 1.6), 2: (6, SL(_c(0.3, 0.7, 0.9, 1.5)) + [CRIT], 'minecraft:entity.player.attack.sweep', 1.2)},
    tl=tl_of({1: ['P block_0', S('block.note_block.bit', 1, 1.0)]}, {2: ['DASH']}, _px('slash', 9, 3), {5: ['H1']}, _px('slash', 9, 12), {14: ['H1']},
             _px('beam', 6, 21), {24: ['H2'], 28: ['P idle_a']}))
NAMES['pxleo'] = ('Triple Slash', 'dashes in, slashes the monster twice and finishes it with a sword beam')
ASSAULT['pxemma'] = R('p213e', 'xn', 30, D(1.2, 1.0, 4),
    hits={1: (6, ['particle ' + _c(1.0, 0.9, 0.4, 1.5) + ' ~ ~0.5 ~ 0.5 0.2 0.5 0 20', 'particle minecraft:poof ~ ~0.2 ~ 0.5 0.1 0.5 0.05 10'], 'minecraft:entity.slime.jump', 0.6),
          2: (8, ['particle minecraft:flame ~ ~1 ~ 0.4 0.4 0.4 0.05 20', 'particle ' + _c(1.0, 0.6, 0.85, 1.5) + ' ~ ~1 ~ 0.5 0.5 0.5 0 20'], 'minecraft:entity.blaze.shoot', 1.6)},
    tl=tl_of(_px('power', 4, 1), {4: ['DASH']}, _px('stomp', 9, 5), {8: ['H1']}, _px('fireball', 9, 15), {19: ['H2'], 27: ['P idle_a']}))
NAMES['pxemma'] = ('Power Stomp', 'powers up, stomps on the monster from above and blasts it with a fireball')

# ---- KETTLE: a game - TAG, you're it! a kick, and a paper plane, point-blank
ASSAULT['kettle'] = R('p227', 'kq', 32, D(1.5, 1.1, 1),
    hits={1: (3, ['particle minecraft:happy_villager ~ ~1.4 ~ 0.3 0.3 0.3 0 6', SLOW], 'minecraft:entity.player.attack.knockback', 1.6),
          2: (4, ['particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.3 12', 'particle minecraft:poof ~ ~0.4 ~ 0.3 0.1 0.3 0.05 6'], 'minecraft:entity.player.attack.strong', 1.4),
          3: (7, ['particle minecraft:white_ash ~ ~1 ~ 0.5 0.5 0.5 0 30', 'particle minecraft:crit ~ ~1 ~ 0.4 0.4 0.4 0.4 16'], 'minecraft:entity.firework_rocket.blast', 1.4)},
    tl={1: ['P wave_a', S('entity.villager.celebrate', 0.6, 1.8)], 3: ['P run_1', 'DASH'], 4: ['P tag_up'], 5: ['P tag', 'H1'],
        9: ['P kick_up'], 11: ['P kick', 'H2'], 15: ['P throw_up', S('item.book.page_turn', 1, 1.6)], 19: ['P throw', 'H3'], 24: ['P cart_0'], 25: ['P cart_1'], 26: ['P cart_2'], 27: ['P cart_3'], 29: ['P happy']})
NAMES['kettle'] = ("Tag, You're It!", 'runs up and tags the monster, kicks it like a ball and throws a paper plane right at it - then cartwheels off')

# ---- THE GEM OF CREATIVITY: it conjures - a Buddy's swipe, then a burst of every colour it has
ASSAULT['gem'] = R('p231', 'cq', 30, D(1.8, 0.9, 1),
    hits={1: (3, ['particle ' + _c(1.0, 0.4, 0.7, 1.3) + ' ~ ~1 ~ 0.4 0.4 0.4 0 16', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.3 0.3 0.05 6'], 'minecraft:block.amethyst_block.hit', 1.4),
          2: (8, ['particle ' + _c(0.4, 0.8, 1.0, 1.6) + ' ~ ~1 ~ 0.7 0.6 0.7 0 30', 'particle ' + _c(0.5, 1.0, 0.5, 1.6) + ' ~ ~1 ~ 0.7 0.6 0.7 0 30',
                  'particle ' + _c(1.0, 0.85, 0.3, 1.6) + ' ~ ~1 ~ 0.7 0.6 0.7 0 30', 'particle minecraft:end_rod ~ ~1 ~ 0.5 0.6 0.5 0.15 20'], 'minecraft:block.amethyst_cluster.break', 0.8)},
    tl=tl_of({1: ['P conjure_up', S('block.amethyst_block.resonate', 1, 1.6)], 3: ['DASH']}, combo(4, 2, 4, 'conjure_up', 'conjure', 1),
             {13: ['P conjure_up', S('block.beacon.power_select', 0.6, 1.8), 'particle minecraft:end_rod ~ ~1.4 ~ 0.4 0.4 0.4 0.05 12'], 18: ['P conjure', 'H2'], 26: ['P happy']}))
NAMES['gem'] = ('Masterstroke', 'paints in the air at the monster twice and then lets every colour it has go at once')

# ---- BATTY: up into the rafters you can SEE, a dive, bites
ASSAULT['batty'] = R('p232b', 'yk', 32, D(1.4, 1.0, 4),
    hits={1: (4, ['particle minecraft:crit ~ ~1.4 ~ 0.3 0.3 0.3 0.3 12', 'particle minecraft:large_smoke ~ ~1.4 ~ 0.3 0.2 0.3 0 4'], 'minecraft:entity.bat.hurt', 0.6),
          2: (3, ['particle minecraft:damage_indicator ~ ~1.2 ~ 0.2 0.2 0.2 0 3', CRIT], 'minecraft:entity.fox.bite', 1.2),
          3: (4, ['particle minecraft:sonic_boom ~ ~1 ~ 0 0 0 0 1', 'effect give @s minecraft:nausea 3 0 true', SLOW], 'minecraft:entity.bat.ambient', 0.5)},
    tl={1: ['P wing_flap', S('entity.bat.takeoff', 1, 0.8), 'data merge entity @s {NoGravity:1b}', 'RISE 1..5'], 3: ['P wing_flap'], 6: ['P bite_up', 'DASH'],
        7: ['P bite', 'H1', 'data merge entity @s {NoGravity:0b}'], 10: ['P bite_up'], 11: ['P bite', 'H2'], 14: ['P bite_up'], 15: ['P bite', 'H2'],
        19: ['P screech', 'H3'], 27: ['P happy']})
NAMES['batty'] = ('Night Dive', 'flutters up, dives fangs-first onto the monster, bites it twice more and screeches in its ear')

# ---- EGGBERT: claw, claw, and a glob of goo slapped right on
ASSAULT['eggbert'] = R('p232e', 'ey', 30, D(1.6, 1.0, 1),
    hits={1: (3, ['particle minecraft:item_slime ~ ~1 ~ 0.3 0.3 0.3 0.05 8', CRIT], 'minecraft:entity.slime.attack', 1.2),
          2: (8, ['particle minecraft:item_slime ~ ~1 ~ 0.6 0.6 0.6 0.2 30', 'particle minecraft:squid_ink ~ ~0.4 ~ 0.6 0.1 0.6 0.02 20', 'effect give @s minecraft:slowness 3 4 true'],
              'minecraft:block.honey_block.slide', 0.7)},
    tl=tl_of({1: ['P claw_up', S('entity.slime.squish', 1, 0.6)], 3: ['DASH']}, combo(4, 2, 3, 'claw_up', 'claw', 1),
             {11: ['P goo_throw_up', S('block.honey_block.step', 1, 0.6)], 16: ['P goo_throw', 'H2'], 25: ['P happy']}))
NAMES['eggbert'] = ('Yolk Smash', 'claws the monster twice and slaps a whole glob of goo on it')

# ---- THE COUNT: a tip of the hat, the cane three times - and a gentleman's finish
ASSAULT['count'] = R('p232c', 'kz', 32, D(1.6, 1.0, 0),
    hits={1: (2, ['particle minecraft:enchanted_hit ~ ~1 ~ 0.3 0.4 0.3 0.2 10', CRIT], 'minecraft:entity.player.attack.crit', 1.4),
          2: (8, ['particle minecraft:enchanted_hit ~ ~1 ~ 0.5 0.6 0.5 0.4 30', 'particle minecraft:item_slime ~ ~1 ~ 0.4 0.4 0.4 0.1 16', 'effect give @s minecraft:weakness 3 1 true'],
              'minecraft:block.note_block.bell', 0.8)},
    tl=tl_of({1: ['P tip_hat', S('block.note_block.bell', 0.6, 1.4)], 4: ['DASH']}, combo(5, 3, 3, 'cane_up', 'cane', 1),
             {15: ['P tip_hat'], 18: ['P cane_up', S('entity.player.attack.sweep', 0.6, 0.7)], 21: ['P cane', 'H2'], 28: ['P tip_hat']}))
NAMES['count'] = ('A Gentleman Never Tells', 'tips his hat, raps the monster three times with his cane and finishes it with a flourish - and tips it again')

# ---- THE DOODLE MOB: claws on the page, and a crayon blaze
ASSAULT['dragon'] = R('p235d', 'dz', 30, D(1.8, 1.0, 2),
    hits={1: (3, SL(_c(0.95, 0.4, 0.2)), 'minecraft:entity.player.attack.sweep', 1.2),
          2: (8, ['particle minecraft:flame ~ ~1 ~ 0.5 0.5 0.5 0.05 30', 'particle ' + _c(1.0, 0.6, 0.1, 1.6) + ' ~ ~1 ~ 0.5 0.5 0.5 0 20', 'data merge entity @s {Fire:60s}'],
              'minecraft:entity.blaze.shoot', 0.8)},
    tl=tl_of({1: ['P flap_0', S('item.book.page_turn', 1, 0.8)], 2: ['P flap_1'], 3: ['DASH']}, combo(4, 2, 4, 'swipe_up', 'swipe', 1),
             {12: ['P breathe_up', S('entity.ender_dragon.growl', 0.3, 1.8)], 17: ['P breathe', 'H2'], 26: ['P happy']}))
NAMES['dragon'] = ('Crayon Inferno', 'claws the monster twice and breathes a blaze of crayon fire on it, point-blank')

# ---- THE ERASER: it rubs OTHER things out - a hop on, rubbing, and the slam
ASSAULT['eraser'] = R('p235e', 'ea', 30, D(1.4, 1.0, 3),
    hits={1: (2, ['particle minecraft:cherry_leaves ~ ~1 ~ 0.3 0.3 0.3 0 10', 'particle minecraft:white_ash ~ ~1 ~ 0.3 0.4 0.3 0 12'], 'minecraft:item.brush.brushing.generic', 1.2),
          2: (8, ['particle minecraft:cherry_leaves ~ ~0.4 ~ 0.8 0.2 0.8 0 30', 'particle minecraft:poof ~ ~0.3 ~ 0.6 0.1 0.6 0.05 12', 'effect give @s minecraft:weakness 3 1 true'], 'minecraft:entity.slime.squish', 0.6)},
    tl={1: ['P hop_up', S('item.brush.brushing.sand', 1, 1.4)], 3: ['P hop', 'DASH'],
        4: ['P rub_0', 'H1'], 6: ['P rub_1', 'H1'], 8: ['P rub_0', 'H1'], 12: ['P hop_up', S('entity.slime.jump', 1, 0.9)], 17: ['P slam', 'H2'], 25: ['P happy']})
NAMES['eraser'] = ('Rub It Out', 'hops on the monster, rubs at it hard enough to unmake it, and slams down on what\'s left')

# ---- THE CURSOR: select it, drag it, click-click-CLICK
ASSAULT['cursor'] = R('p235c', 'uq', 30, D(1.5, 1.1, 1),
    hits={1: (2, ['particle minecraft:electric_spark ~ ~1 ~ 0.2 0.3 0.2 0.1 8', 'particle ' + _c(0.3, 0.6, 1.0, 1.2) + ' ~ ~1 ~ 0.4 0.5 0.4 0 12'], 'minecraft:ui.button.click', 1.6),
          2: (8, ['particle minecraft:electric_spark ~ ~1 ~ 0.5 0.5 0.5 0.3 30', 'particle minecraft:enchanted_hit ~ ~1 ~ 0.4 0.5 0.4 0.3 20', 'effect give @s minecraft:glowing 2 0 true'],
              'minecraft:block.note_block.bit', 0.6)},
    tl={1: ['P select', S('ui.button.click', 1, 1.2), at('particle ' + _c(0.3, 0.6, 1.0, 0.8) + ' ~ ~1 ~ 0.6 0.8 0.6 0 20')], 3: ['P drag_0', 'DASH'],
        4: ['P click_up'], 5: ['P click', 'H1'], 7: ['P click_up'], 8: ['P click', 'H1'], 10: ['P click_up'], 11: ['P click', 'H1'],
        14: ['P wait_0', S('block.note_block.hat', 1, 1.8)], 16: ['P wait_1'], 18: ['P click_up'], 20: ['P click', 'H2'], 26: ['P happy']})
NAMES['cursor'] = ('Double Click', 'selects the monster, drags itself onto it, clicks three times - and Loading... - CLICK')

# ================================================================================================ batch 3: the Doodles, the light and the dread
# ---- THE INK BLOT: punch, punch, and the quill spike
ASSAULT['inkblot'] = R('p235i', 'iq', 30, D(1.5, 1.0, 1),
    hits={1: (3, ['particle minecraft:squid_ink ~ ~1 ~ 0.3 0.3 0.3 0.02 10', CRIT], 'minecraft:entity.slime.attack', 1.0),
          2: (8, ['particle minecraft:squid_ink ~ ~1 ~ 0.6 0.6 0.6 0.08 30', 'particle ' + _c(0.1, 0.1, 0.15, 1.6) + ' ~ ~1 ~ 0.5 0.6 0.5 0 20', 'effect give @s minecraft:blindness 2 0 true'],
              'minecraft:item.trident.hit', 0.8)},
    tl=tl_of({1: ['P guard', S('entity.slime.squish', 1, 0.8)], 3: ['DASH']}, combo(4, 2, 4, 'punch_up', 'punch', 1),
             {12: ['P spike_up', S('item.book.page_turn', 1, 0.6)], 17: ['P spike', 'H2'], 26: ['P wonder']}))
NAMES['inkblot'] = ('Quill Strike', 'punches the monster twice and drives a quill of ink straight through it')

# ---- THE SPEECH BUBBLE: a SHOUT, and KRAK! - in panels you can read
ASSAULT['speech'] = R('p235b', 'wq', 30, D(1.5, 1.0, 1),
    hits={1: (3, ['particle minecraft:explosion ~ ~1 ~ 0 0 0 0 1', CRIT], 'minecraft:entity.player.attack.knockback', 1.4),
          2: (8, ['particle minecraft:explosion ~ ~1 ~ 0.4 0.4 0.4 0 3', 'particle minecraft:end_rod ~ ~1 ~ 0.5 0.5 0.5 0.2 20', 'particle minecraft:crit ~ ~1 ~ 0.5 0.5 0.5 0.4 20'],
              'minecraft:entity.firework_rocket.large_blast', 1.0)},
    tl={1: ['P puff_up', S('entity.chicken.egg', 1, 0.7)], 3: ['DASH'], 4: ['P shout_up'], 5: ['P shout', 'H1'], 8: ['P shout_b', 'H1'],
        12: ['P puff_up', S('entity.creeper.primed', 0.6, 1.8)], 16: ['P blast', 'H2'], 19: ['P blast_b'], 26: ['P happy']})
NAMES['speech'] = ('KRAK-A-BOOM!', 'shouts in the monster\'s face twice and goes off like the last panel of a comic')

# ---- THE LIGHTBRINGER: wings spread, risen into the light - and the smite, staff first
ASSAULT['lightbringer'] = R('p236l', 'lz', 32, D(1.6, 1.0, 3),
    hits={1: (3, ['particle minecraft:end_rod ~ ~1 ~ 0.3 0.5 0.3 0.05 12', 'particle minecraft:glow ~ ~1 ~ 0.3 0.3 0.3 0 6'], 'minecraft:block.amethyst_block.chime', 1.6),
          2: (8, ['particle minecraft:end_rod ~ ~3 ~ 0.1 2 0.1 0 40', 'particle minecraft:flash{color:[1.0,0.92,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:end_rod ~ ~0.3 ~ 1 0.1 1 0.1 30'],
              'minecraft:entity.lightning_bolt.impact', 1.6)},
    tl={1: ['P wings_spread_up', S('block.beacon.activate', 0.8, 1.4)], 3: ['P wings_spread', 'particle minecraft:end_rod ~ ~1.4 ~ 0.6 0.6 0.6 0.02 16'], 5: ['DASH'],
        6: ['P smite_up'], 7: ['P smite', 'H1'], 10: ['P smite_up'], 11: ['P smite', 'H1'],
        14: ['P bless_a', S('block.beacon.power_select', 0.8, 1.6)], 19: ['P smite_end', 'H2'], 27: ['P pray']})
NAMES['lightbringer'] = ('Judgement', 'spreads her wings, strikes the monster twice with her staff and calls down a pillar of light on it')

# ---- THE PALE DRYAD: she stands and commands - roots burst out under it, spores, and the bloom
ASSAULT['dryad'] = R('p236p', 'qd', 32, D(1.8, 0.9, 0),
    hits={1: (3, ['particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.3 ~ 0.4 0.2 0.4 0 20', 'effect give @s minecraft:slowness 2 9 true'], 'minecraft:block.rooted_dirt.break', 0.8),
          2: (3, ['particle minecraft:spore_blossom_air ~ ~1 ~ 0.6 0.6 0.6 0 30', 'effect give @s minecraft:poison 2 0 true'], 'minecraft:block.moss.break', 1.2),
          3: (5, ['particle minecraft:spore_blossom_air ~ ~1 ~ 1 0.8 1 0 40', 'particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.5 ~ 0.6 0.4 0.6 0 30'], 'minecraft:block.azalea_leaves.break', 0.6)},
    tl={1: ['P root_up', S('block.rooted_dirt.place', 1, 0.6)], 3: ['DASH'], 4: ['P root', 'H1', at('particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.1 ~ 0.6 0.1 0.6 0 30')],
        7: ['P root_hold'], 10: ['P swipe_up'], 11: ['P swipe', 'H1'], 14: ['P spore_up'], 16: ['P spore', 'H2'],
        19: ['P bloom_up', S('block.azalea.place', 1, 0.6)], 23: ['P bloom', 'H3'], 29: ['P happy']})
NAMES['dryad'] = ('Overgrown', 'roots the monster where it stands, rakes it, chokes it in spores and blooms right through it')

# ---- THE BOUND SOVEREIGN: the dread phases played out - the chains lash it in, the greatsword twice, the eye bolt point-blank
ASSAULT['sovereign'] = R('p239', 'xq', 36, None,
    pull_fx='particle minecraft:block{block_state:"minecraft:chain"} ~ ~1 ~ 0.1 0.1 0.1 0 2',
    hits={1: (2, ['particle minecraft:block{block_state:"minecraft:chain"} ~ ~1 ~ 0.4 0.5 0.4 0 20', 'particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.4 0.3 0.02 8',
                  'effect give @s minecraft:slowness 3 9 true'], 'minecraft:block.chain.break', 0.6),
          2: (4, ['particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.2 0.3 0 2', 'particle minecraft:sculk_soul ~ ~1 ~ 0.4 0.5 0.4 0.04 14', CRIT], 'minecraft:entity.warden.attack_impact', 0.8),
          3: (4, ['particle minecraft:sculk_soul ~ ~1 ~ 0.6 0.6 0.6 0.1 30', 'particle minecraft:flash{color:[0.5,0.9,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1', 'effect give @s minecraft:wither 3 1 true'],
              'minecraft:entity.warden.sonic_boom', 1.4)},
    tl={1: ['P bolt_up', S('block.chain.place', 1, 0.5), 'particle minecraft:sculk_soul ~ ~1.6 ~ 0.6 0.5 0.6 0.02 12'],
        3: ['H1', S('block.chain.hit', 1, 0.6), 'PULLX 3..12'], 13: ['P slash_up', S('entity.warden.heartbeat', 1, 0.8)], 16: ['P slash', 'H2'],
        19: ['P slash_up'], 22: ['P slash', 'H2'], 25: ['P bolt_up', S('entity.warden.sonic_charge', 0.8, 1.2)], 29: ['P bolt', 'H3'], 33: ['P idle_a']})
NAMES['sovereign'] = ('The Dread Unchained', 'lashes the monster in with its chains, cleaves it twice with the greatsword and burns it with its eye, point-blank')

# ---- VEXIS: a gravity well drags it in, the hive-grip slash, and a plasma bolt
ASSAULT['vexis'] = R('p243', 'qx', 32, None,
    pull_fx='particle minecraft:reverse_portal ~ ~1 ~ 0.2 0.2 0.2 0.02 4',
    hits={1: (4, ['particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.5 0.4 0.1 20', CRIT], 'minecraft:entity.shulker.hurt_closed', 0.8),
          2: (6, ['particle minecraft:dragon_breath ~ ~1 ~ 0.4 0.4 0.4 0.03 20', 'particle ' + _c(0.4, 1.0, 0.5, 1.4) + ' ~ ~1 ~ 0.5 0.5 0.5 0 20', 'data merge entity @s {Fire:60s}'],
              'minecraft:entity.shulker.shoot', 0.7)},
    tl={1: ['P well', S('block.end_portal.spawn', 0.4, 1.8), at('particle minecraft:reverse_portal ~ ~1 ~ 0.6 0.6 0.6 0.4 30')], 2: ['PULLX 2..10'],
        11: ['P slash_up'], 12: ['P slash', 'H1'], 15: ['P slash_up'], 16: ['P slash', 'H1'], 19: ['P bolt_up', S('block.beacon.power_select', 0.6, 0.6)],
        24: ['P bolt', 'H2'], 29: ['P idle_a']})
NAMES['vexis'] = ('Event Horizon', 'drags the monster in on a gravity well, rakes it twice with three long fingers and fires a plasma bolt into it')

# ---- THE KEEPER OF BONDS: a thread tugs it in, bound in the weave, pulled tight
ASSAULT['keeper'] = R('p254', 'qb', 34, None,
    pull_fx='particle minecraft:end_rod ~ ~1 ~ 0.05 0.05 0.05 0 2',
    hits={1: (3, ['particle minecraft:end_rod ~ ~1 ~ 0.3 0.4 0.3 0.05 12', 'effect give @s minecraft:slowness 3 9 true'], 'minecraft:block.amethyst_block.chime', 1.2),
          2: (8, ['particle minecraft:end_rod ~ ~1 ~ 0.7 0.7 0.7 0.15 40', 'particle ' + _c(1.0, 0.85, 0.5, 1.2) + ' ~ ~1 ~ 0.6 0.6 0.6 0 30', 'effect give @s minecraft:weakness 3 1 true'],
              'minecraft:block.amethyst_block.break', 0.7)},
    tl={1: ['P tug_up', S('block.amethyst_block.resonate', 1, 1.2)], 3: ['P tug', 'H1', 'PULLX 3..10'], 12: ['P weave_up', S('block.amethyst_cluster.step', 1, 0.8)],
        15: ['P weave', 'H1'], 18: ['P weave_hold', at('particle minecraft:end_rod ~ ~1 ~ 0.6 0.6 0.6 0.01 20')], 23: ['P weave_end', 'H2'], 30: ['P bow']})
NAMES['keeper'] = ('Bound Fast', 'casts a thread and tugs the monster in, weaves it into its web and pulls the web tight')

# ---- THE RAT KING: a decree, the sceptre - and his court answers the whistle
ASSAULT['ratking'] = R('p262', 'qw', 34, D(1.6, 1.0, 0),
    hits={1: (3, ['particle minecraft:wax_on ~ ~1 ~ 0.3 0.4 0.3 0 10', CRIT], 'minecraft:entity.player.attack.strong', 1.0),
          2: (2, ['particle minecraft:block{block_state:"minecraft:gravel"} ~ ~0.3 ~ 0.6 0.2 0.6 0 20', 'particle minecraft:crit ~ ~0.6 ~ 0.6 0.3 0.6 0.3 12'], 'minecraft:entity.rabbit.attack', 0.6),
          3: (4, ['particle minecraft:wax_on ~ ~1 ~ 0.6 0.6 0.6 0 30', 'particle minecraft:enchanted_hit ~ ~1 ~ 0.4 0.5 0.4 0.3 20', 'effect give @s minecraft:weakness 3 1 true'],
              'minecraft:block.bell.use', 0.6)},
    tl={1: ['P decree_up', S('entity.rabbit.ambient', 1, 0.5)], 3: ['DASH'], 4: ['P swat_up'], 5: ['P swat', 'H1'], 8: ['P swat_up'], 9: ['P swat', 'H1'],
        12: ['P whistle', S('entity.rabbit.ambient', 1, 1.8), at('particle minecraft:block{block_state:"minecraft:gravel"} ~ ~0.1 ~ 0.8 0 0.8 0 30')],
        14: ['P whistle_a', 'H2'], 16: ['H2'], 20: ['P decree_up', S('block.bell.resonate', 0.6, 0.6)], 25: ['P decree', 'H3'], 31: ['P bow']})
NAMES['ratking'] = ('The Royal Decree', 'swats the monster twice with his sceptre, whistles his court out of the ground to bite it and decrees it finished')

# ---- THE FROG WITH MUSTACHE: his whole act is the hop - a leap you can see, and down on it
ASSAULT['frog'] = dict(pfx='p226/lite/frog', s_obj='bm.ksg', anim='p63/frog/anim', state='p63/frog/anim', place='p63/frog/anim', tick='p226/lite/frog', face='none', st=99999,
    pose='p63/frog/p/{}', busy=None, end=26, dash=D(1.2, 1.0, 4), lite='p63/frog', me='fgme',
    hits={1: (8, ['particle minecraft:item_slime ~ ~0.3 ~ 0.6 0.2 0.6 0.2 30', 'particle minecraft:poof ~ ~0.2 ~ 0.5 0.1 0.5 0.05 10', 'effect give @s minecraft:slowness 2 4 true'],
              'minecraft:entity.slime.squish', 0.6),
          2: (3, ['particle minecraft:item_slime ~ ~1 ~ 0.3 0.3 0.3 0.1 10', CRIT], 'minecraft:entity.frog.eat', 1.0)},
    tl={1: ['P hop0_3', S('entity.frog.long_jump', 1, 0.8)], 3: ['P hop1_3', 'DASH'], 4: ['P hop3_3', 'H1'], 8: ['P hop0_3'], 10: ['P hop2_3', 'H2'], 14: ['P hop0_3'], 16: ['P hop2_3', 'H2'],
        22: ['P idle0_10']})
NAMES['frog'] = ('Leap of Faith', 'leaps high onto the monster, lands on it with everything he has, and gives it two more for luck')

# ---- DONADO: a running charge and a jump attack
ASSAULT['don'] = dict(pfx='p226/lite/don', s_obj='bm.ksg', anim='p63/don/anim', state='p63/don/anim', place='p63/don/anim', tick='p226/lite/don', face='none', st=99999,
    pose='p63/don/p/{}', busy=None, end=26, dash=D(1.4, 1.1, 1), lite='p63/don', me='dnme',
    hits={1: (3, ['particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.3 10', 'particle minecraft:portal ~ ~1 ~ 0.3 0.4 0.3 0.2 10'], 'minecraft:entity.player.attack.strong', 1.4),
          2: (8, ['particle minecraft:end_rod ~ ~1 ~ 0.4 0.5 0.4 0.1 20', 'particle minecraft:portal ~ ~0.5 ~ 0.6 0.3 0.6 0.4 30', CRIT], 'minecraft:entity.player.attack.knockback', 0.8)},
    tl={1: ['P run0_3', S('entity.fox.screech', 0.4, 1.8)], 2: ['P run1_3'], 3: ['P run2_3', 'DASH'], 4: ['P walk1_3', 'H1'], 7: ['P walk3_3', 'H1'],
        10: ['P jump_3', S('entity.goat.long_jump', 1, 1.4), 'data merge entity @s {NoGravity:1b}', 'RISE 10..13'], 14: ['DROP 14..16'],
        16: ['P sit_10', 'H2', 'data merge entity @s {NoGravity:0b}'], 22: ['P idle0_10']})
NAMES['don'] = ('Mothership Charge', 'charges the monster, hits it twice and jumps on it with both feet')

# ================================================================================================ batch 4: the 3.1 followers
ASSAULT['cake'] = R('p265', 'kz', 30, D(1.4, 1.0, 3),
    hits={1: (2, ['particle ' + _c(1.0, 0.6, 0.8, 1.2) + ' ~ ~1 ~ 0.3 0.3 0.3 0 10', CRIT], 'minecraft:entity.player.attack.crit', 1.6),
          2: (8, ['particle minecraft:firework ~ ~1 ~ 0.4 0.4 0.4 0.15 30', 'particle ' + _c(1.0, 0.95, 0.85, 1.6) + ' ~ ~0.4 ~ 1 0.1 1 0 40', 'effect give @s minecraft:slowness 2 4 true'],
              'minecraft:entity.firework_rocket.blast', 1.2)},
    tl=tl_of({1: ['P hop', S('entity.chicken.egg', 1, 0.8)], 3: ['DASH']}, combo(4, 3, 3, 'fork_up', 'fork', 1),
             {14: ['P slam_up', S('block.honey_block.slide', 1, 1.4)], 19: ['P slam', 'H2'], 22: ['P land'], 27: ['P happy']}))
NAMES['cake'] = ('Surprise Party', 'hops in fork first - jab, jab, jab - and brings a whole layer of frosting down on the monster: SURPRISE!')

ASSAULT['sapling'] = R('p266', 'sz', 30, D(1.8, 0.9, 0),
    hits={1: (4, ['particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.3 ~ 0.5 0.2 0.5 0 30', 'effect give @s minecraft:slowness 3 9 true'], 'minecraft:block.rooted_dirt.break', 0.8),
          2: (3, ['particle minecraft:falling_honey ~ ~1.4 ~ 0.3 0.2 0.3 0 10', CRIT], 'minecraft:block.honey_block.hit', 1.2),
          3: (7, ['particle minecraft:cherry_leaves ~ ~1 ~ 0.8 0.6 0.8 0 30', 'particle minecraft:crit ~ ~1 ~ 0.5 0.5 0.5 0.4 16'], 'minecraft:block.azalea_leaves.break', 0.6)},
    tl={1: ['P snare', S('block.azalea.place', 1, 0.6)], 3: ['DASH'], 4: ['P snare', 'H1', at('particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.1 ~ 0.6 0.1 0.6 0 30')],
        9: ['P sap'], 11: ['P sap', 'H2'], 15: ['P seeds', S('block.cave_vines.pick_berries', 1, 1.2)], 20: ['P snare', 'H3'], 26: ['P idle_a']})
NAMES['sapling'] = ('Taproot', 'roots the monster where it stands, drips sap on it and bursts a thicket of roots up through it')

ASSAULT['spawner'] = R('p267', 'nz', 30, D(1.6, 0.9, 1),
    hits={1: (3, ['particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.4 0.3 0.03 12', CRIT], 'minecraft:entity.zombie.attack_wooden_door', 1.6),
          2: (8, ['particle minecraft:soul ~ ~1 ~ 0.6 0.6 0.6 0.04 20', 'particle minecraft:flame ~ ~0.4 ~ 0.8 0.2 0.8 0.05 30', 'effect give @s minecraft:weakness 3 1 true'],
              'minecraft:block.trial_spawner.spawn_mob', 0.9)},
    tl=tl_of({1: ['P command', S('block.trial_spawner.ambient', 1, 1.4)], 3: ['DASH']},
             {4: ['P chew', 'H1'], 7: ['P chew2', 'H1'], 12: ['P command', S('block.trial_spawner.about_to_spawn_item', 1, 1.2)], 16: ['P spawn', 'H2'], 26: ['P idle_a']}))
NAMES['spawner'] = ('Full Spawn', 'chews on the monster twice and spawns every friend it has right on top of it')

ASSAULT['cairn'] = R('p268', 'jx', 32, D(1.8, 0.9, 1),
    hits={1: (4, ['particle minecraft:block{block_state:"minecraft:cobblestone"} ~ ~1 ~ 0.4 0.4 0.4 0 20', CRIT], 'minecraft:block.stone.break', 0.8),
          2: (6, ['particle minecraft:block{block_state:"minecraft:cobblestone"} ~ ~0.4 ~ 1 0.3 1 0 50', 'particle minecraft:poof ~ ~0.3 ~ 0.8 0.1 0.8 0.05 16', 'effect give @s minecraft:slowness 2 4 true'],
              'minecraft:block.anvil.land', 0.6)},
    tl=tl_of({1: ['P asm_0', S('block.stone.place', 1, 0.6)], 2: ['P asm_1'], 3: ['DASH']}, combo(4, 2, 5, 'fling_up', 'fling', 1),
             {15: ['P asm_2', S('block.stone.hit', 1, 0.5)], 17: ['P asm_3'], 20: ['P storm', 'H2'], 28: ['P idle_a']}))
NAMES['cairn'] = ('Rockfall', 'flings its own stones at the monster twice and brings every block it is made of down on it')

ASSAULT['knight'] = R('p269', 'iz', 34, D(2.0, 1.0, 0),
    hits={1: (3, ['particle minecraft:soul ~ ~1 ~ 0.4 0.5 0.4 0.02 12', 'effect give @s minecraft:slowness 3 9 true'], 'minecraft:entity.vex.charge', 0.8),
          2: (3, ['particle minecraft:sweep_attack ~ ~1 ~ 0.2 0.1 0.2 0 1', CRIT], 'minecraft:entity.iron_golem.attack', 1.0),
          3: (5, ['particle minecraft:soul_fire_flame ~ ~0.4 ~ 0.8 0.2 0.8 0.05 30', 'particle minecraft:crit ~ ~1 ~ 0.5 0.5 0.5 0.4 16'], 'minecraft:block.anvil.land', 0.7)},
    tl={1: ['P coil', S('entity.vex.ambient', 1, 0.6)], 3: ['DASH'], 4: ['P coil_go', 'H1'], 8: ['P swing_0'], 10: ['P swing_1', 'H2'], 13: ['P swing_0'], 15: ['P swing_1', 'H2'],
        19: ['P heap_up', S('entity.iron_golem.step', 1, 0.6)], 24: ['P heap_strike', 'H3'], 31: ['P idle_a']})
NAMES['knight'] = ('The Captain\'s Charge', 'the serpent coils round the monster to hold it, the captain\'s mace swings twice and comes down overhead')

ASSAULT['mimic'] = R('p270', 'wx', 32, D(1.4, 1.0, 2),
    hits={1: (3, ['particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.3 12', 'particle minecraft:wax_on ~ ~1 ~ 0.3 0.3 0.3 0 6'], 'minecraft:block.chest.close', 1.4),
          2: (8, ['particle minecraft:wax_on ~ ~1 ~ 0.6 0.6 0.6 0 30', 'particle minecraft:crit ~ ~1 ~ 0.5 0.5 0.5 0.4 16', 'effect give @s minecraft:slowness 2 4 true'],
              'minecraft:entity.player.burp', 0.6)},
    tl=tl_of({1: ['P disguise', S('block.chest.locked', 1, 0.8)], 3: ['P snap_up', 'DASH']}, combo(4, 2, 4, 'snap_up', 'snap', 1),
             {12: ['P gulp', S('entity.generic.eat', 1, 0.6)], 15: ['P swallow'], 18: ['P spit', 'H2'], 27: ['P happy']}))
NAMES['mimic'] = ('Bottomless Bite', 'snaps at the monster twice, gulps it down whole - and spits it back out')

# 14 each (phase226.assault asserts it too)
for _w, _a in ASSAULT.items():
    _n = sum(_a['hits'][int(c[1:])][0] for t in _a['tl'].values() for c in t if c[0] == 'H' and c[1:].isdigit())
    assert _n == 14, (_w, _n)

# ================================================================================================ the seven who still vanish: a signature each
# (out, sign, back) over phase226.FLAV's; their names, where they come back and their sounds stay
_P = lambda p, n=24, s=0.4, h=0.7, v=0.03: f'{p} ~ ~1 ~ {s} {h} {s} {v} {n}'
_SH = _c(0.08, 0.04, 0.12, 1.6)                    # (a shadow: near-black violet)
POLISH = {
    'cecil': ([_P('minecraft:squid_ink', 40, 0.4, 0.8, 0.03), _P('minecraft:large_smoke', 30, 0.4, 0.9, 0.01), _P(_SH, 30, 0.35, 0.8, 0)],
              ['minecraft:large_smoke ^ ^1 ^-1.2 0.25 0.5 0.25 0.005 3', f'{_SH} ^ ^1 ^-1.2 0.3 0.5 0.3 0 4'],
              [_P('minecraft:squid_ink', 30, 0.5, 0.8, 0.12), _P('minecraft:large_smoke', 30, 0.5, 0.8, 0.04), _P(_SH, 30, 0.5, 0.8, 0), _P('minecraft:enchanted_hit', 20, 0.3, 0.5, 0.3)]),
    'omega': ([_P('minecraft:sculk_soul', 30, 0.5, 0.3, 0.05), _P('minecraft:soul', 20, 0.4, 0.2, 0.02), 'minecraft:large_smoke ~ ~0.2 ~ 0.5 0.1 0.5 0.02 30', _P(_SH, 30, 0.5, 0.4, 0)],
              ['minecraft:sculk_soul ~ ~0.1 ~ 0.4 0 0.4 0.01 4', 'minecraft:large_smoke ~ ~0.1 ~ 0.4 0 0.4 0.005 2', f'{_SH} ~ ~0.1 ~ 0.5 0 0.5 0 3'],
              [_P('minecraft:sculk_soul', 40, 0.4, 1.0, 0.12), _P('minecraft:soul_fire_flame', 20, 0.3, 0.8, 0.06), _P('minecraft:large_smoke', 20, 0.4, 0.9, 0.04),
               'minecraft:block{block_state:"minecraft:soul_soil"} ~ ~0.2 ~ 0.6 0.1 0.6 0 40']),
    'stalker': ([_P('minecraft:squid_ink', 40), _P(_SH, 30, 0.4, 0.8, 0), _P('minecraft:sculk_soul', 6, 0.3, 0.6, 0.01)],
                ['minecraft:squid_ink ^ ^1 ^-1.2 0.2 0.5 0.2 0 3', f'{_SH} ^ ^1 ^-1.2 0.25 0.6 0.25 0 3'],
                [_P('minecraft:squid_ink', 40, 0.5, 0.8, 0.1), _P(_SH, 30, 0.5, 0.8, 0), _P('minecraft:sculk_soul', 12)]),
    'pistachio': ([_P('minecraft:soul', 24), _P('minecraft:poof', 16), _P(_c(0.6, 0.95, 0.7, 1.0), 20, 0.4, 0.8, 0)],
                  ['minecraft:soul ^ ^1 ^-1.2 0.2 0.4 0.2 0.01 2', _c(0.6, 0.95, 0.7, 0.8) + ' ^ ^1 ^-1.2 0.2 0.4 0.2 0 2'],
                  [_P('minecraft:soul', 30, 0.4, 0.6, 0.05), _P('minecraft:sculk_soul', 12, 0.3, 0.6, 0.02), _P(_c(0.6, 0.95, 0.7, 1.2), 24, 0.4, 0.8, 0)]),
    'wil': ([_P('minecraft:soul', 30, 0.4, 0.4, 0.02), _P('minecraft:smoke', 20), 'minecraft:block{block_state:"minecraft:coarse_dirt"} ~ ~0.2 ~ 0.5 0.1 0.5 0 20'],
            ['minecraft:soul ~ ~0.1 ~ 0.4 0 0.4 0.01 3', 'minecraft:block{block_state:"minecraft:coarse_dirt"} ~ ~0.1 ~ 0.4 0 0.4 0 2'],
            [_P('minecraft:soul', 40, 0.4, 0.9, 0.06), 'minecraft:block{block_state:"minecraft:coarse_dirt"} ~ ~0.2 ~ 0.5 0.1 0.5 0 40', 'minecraft:block{block_state:"minecraft:bone_block"} ~ ~0.4 ~ 0.4 0.2 0.4 0 16']),
    'mireling': ([_P('minecraft:squid_ink', 30, 0.5, 0.2, 0.02), _P(_SH, 24, 0.5, 0.2, 0), 'minecraft:dripping_dripstone_water ~ ~0.3 ~ 0.4 0.1 0.4 0 6'],
                 ['minecraft:squid_ink ~ ~0.1 ~ 0.4 0 0.4 0.01 2', f'{_SH} ~ ~0.05 ~ 0.6 0 0.6 0 4'],
                 [_P('minecraft:squid_ink', 40, 0.4, 0.8, 0.08), _P(_SH, 30, 0.4, 0.8, 0), _P('minecraft:crit', 20)]),
    'glitch': ([_P('minecraft:electric_spark', 30, 0.4, 0.6, 0.3), _P(_c(1.0, 0.24, 0.78, 1.2), 24), _P(_c(0.24, 0.94, 1.0, 1.2), 24), _P(_c(0.0, 0.0, 0.0, 1.4), 16)],
               [_c(0.24, 0.94, 1.0, 0.8) + ' ^ ^1 ^-1.2 0.2 0.3 0.2 0 2', _c(1.0, 0.24, 0.78, 0.8) + ' ^0.1 ^1 ^-1.2 0.2 0.3 0.2 0 2'],
               [_P('minecraft:electric_spark', 40, 0.4, 0.8, 0.4), _P(_c(1.0, 0.24, 0.78, 1.4), 24), _P(_c(0.24, 0.94, 1.0, 1.4), 24), _P('minecraft:crit', 20)]),
}

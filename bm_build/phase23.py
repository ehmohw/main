"""Phase 1.13: the market comes alive (runs with the Black Market 2.0 structure, market2.py).

- Neon signs: text displays over each district, flickering now and then.
- The crowd: rats sitting in the tavern, playing cards, guarding the balcony, hauling on the docks. They idle-animate
  and turn to watch you (the 1.11 rat animation + 1.9 look systems). Three walkers stroll set routes.
- Speech bubbles: traders and the crowd mutter when you come close (a pop-in text display that fades).
- Ambience: each district has its own sounds; a busker rat plays a jaunty tune on the plaza.
- A little danger: steam vents in the Forge Pit scald and pop you up if you stand on them as they blow.
  (1.13.1: the pickpocket rats were removed - too annoying in practice.)
- Safety: on first load a market clears any monster spawner or sculk shrieker that worldgen features squeezed into
  its walls (the structure itself forbids natural monster spawns, and every walkable cell is lit).
Old (1.7-1.12) markets keep working; bubbles reach their traders too."""
from nbt import snbt, B, F, Int
from items import T

NEON = {   # id: (lines, colours, scale)
    'lucky': ([('* THE LUCKY DEN *', '#4cff6a')], 1.4), 'welcome': ([('WELCOME TO THE BLACK MARKET', '#ffd23f'), ('paws where we can see them', '#bbbbbb')], 1.3),
    'flagon': ([('THE GNAWED FLAGON', '#ffb347')], 1.2), 'forge': ([('THE FORGE PIT', '#ff5a1f')], 1.3),
    'blood': ([('THE BLOOD ALCOVE', '#c0001a')], 1.2), 'auction': ([('THE DARK AUCTION', '#e6c35c'), ('- coming soon -', '#999999')], 1.0),
    'vip': ([('THE GILDED GUTTER', '#e6c35c'), ('members of standing only', '#999999')], 0.8), 'docks': ([('THE DOCKS', '#5fd3ff')], 1.2),
    'alley': ([('PAWN ALLEY', '#f2f2f2')], 1.0)}
FLICKER = ('lucky', 'flagon', 'forge', 'blood', 'docks', 'alley')
CROWD_SCALE = {'soldier': 0.72, 'void': 0.6}
SAYS = {
    'fence': ["Currency's currency. Don't ask where it's been.", "Medallions up, Tokens down. Simple.", "You didn't see me. I didn't see you.",
              "Got a map that'll make you rich. Or dead.", "Keep your key close. Rats talk."],
    'pawn': ["Half back. Not a nibble more.", "No refunds on cursed items. Or regular ones.", "Where'd you get THIS? ...Don't tell me.",
             "Everything's worth something to somebody."],
    'outfitter': ["Darling, those boots are a crime.", "Unbreakable wings! Breaks the bank, though.", "Velvet hides bloodstains beautifully.",
                  "A grappling hook is a lady's best friend.", "You'd look killer in gold. Literally."],
    'arms': ["Sharp enough to split a hair. Or a cat.", "Mind the vents, they've got opinions.", "No test-swings inside the market.",
             "Upgrade? Bring Medallions. Lots."],
    'armory': ["Tier three or go home.", "That dent? Character.", "Hold still, I'm measuring your neck. For a helmet.",
               "Iron's for amateurs."],
    'lucky': ["Feeling lucky? You should.", "The house always wins. I AM the house.", "Scratch it! Go on, scratch it!",
              "Seven's the magic number. Ask anyone.", "Psst. The next card's a winner. Probably."],
    'blood': ["The moon remembers what you owe.", "Crystals for crystals. Hearts for... other things.", "Don't drip on the floor.",
              "Come back when the sky is red.", "Every price is paid. Eventually."],
    'professor': ["Shh. This is a library. Mostly.", "Knowledge is power. Power costs Tokens.", "Ah, a reader! How rare.",
                  "That book? Banned in three kingdoms."],
    'chef': ["Today's special: cheese. Tomorrow's: also cheese.", "You look hungry. And poor. Let's fix one.", "Don't ask what's in the stew.",
             "A feast fit for a rat king!"],
    'captain': ["Arr. Exchange rates be fair. Ish.", "The river goes places the surface don't.", "Mind the Drop, landlubber.",
                "Smuggled it meself. Twice."]}
CROWD_SAYS = ["*squeak*", "Psst. Need cheese?", "Don't look at me.", "Mind your pockets.", "I'm not here.", "Heard the auction's soon...",
              "Who let the human in?", "Nice boots. Shame if...", "The house always wins.", "Blood Moon soon. I can smell it.",
              "*nibble nibble*", "Keep moving, pal.", "The guards are watching. Always.", "Lost my ear in a card game."]
AMB = {   # kind: [(sound, volume, pitch), ...] - one picked at random every few seconds
    'plaza': [('entity.villager.ambient', 0.25, 1.9), ('entity.silverfish.ambient', 0.3, 1.6), ('entity.experience_orb.pickup', 0.2, 0.6),
              ('entity.villager.trade', 0.25, 1.8), ('block.pointed_dripstone.drip_water', 0.6, 1.0), ('entity.villager.yes', 0.2, 1.9)],
    'forge': [('block.anvil.use', 0.25, 0.9), ('block.blastfurnace.fire_crackle', 0.6, 1.0), ('block.lava.pop', 0.5, 1.0),
              ('block.grindstone.use', 0.3, 1.0), ('block.smithing_table.use', 0.3, 0.8)],
    'tavern': [('entity.player.burp', 0.35, 1.6), ('entity.generic.drink', 0.3, 1.4), ('block.wood.hit', 0.3, 1.2),
               ('entity.villager.celebrate', 0.25, 1.9), ('entity.generic.eat', 0.3, 1.5), ('block.smoker.smoke', 0.5, 1.0)],
    'blood': [('entity.warden.heartbeat', 0.25, 0.8), ('block.sculk.charge', 0.3, 0.6), ('ambient.cave', 0.2, 0.7), ('block.chain.step', 0.3, 0.6)],
    'den': [('block.note_block.chime', 0.3, 1.4), ('entity.experience_orb.pickup', 0.3, 1.2), ('block.amethyst_block.chime', 0.4, 1.2),
            ('entity.villager.celebrate', 0.3, 2.0), ('entity.villager.no', 0.3, 1.9), ('block.bell.use', 0.15, 1.8)],
    'docks': [('block.water.ambient', 0.5, 1.0), ('entity.boat.paddle_water', 0.4, 1.0), ('entity.fishing_bobber.splash', 0.3, 1.0),
              ('block.chain.step', 0.3, 1.0), ('block.barrel.open', 0.3, 1.1)],
    'alley': [('block.chest.close', 0.3, 1.2), ('entity.villager.ambient', 0.2, 1.8), ('block.chain.step', 0.3, 1.2),
              ('entity.silverfish.ambient', 0.25, 1.5), ('entity.item.pickup', 0.3, 0.8)]}
# the busker's tune (original): 32 steps of 0.25 s, note-block semitones (12 = F#4); None = rest
MELODY = [15, 18, 22, 20, 18, 17, 15, 17, 18, 22, None, 22, 20, 18, 17, None, 15, 18, 22, 20, 18, 17, 15, 10, 15, 14, 10, 8, 6, 5, 3, None]
BASS = {0: 3, 4: 3, 8: 6, 12: 10, 16: 3, 20: 3, 24: 10, 28: 3}
ROUTE_LEN = {'a': 8, 'b': 2, 'c': 2}


def pitch(n): return round(2 ** ((n - 12) / 12), 3)


def generate(G):
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    PREFIX = G.PREFIX
    tick, fast, second = [], [], []
    objs = ['bm.say', 'bm.blf', 'bm.wpi', 'bm.wst', 'bm.bn', 'bm.vt', 'bm.ppn', 'bm.nf']    # bm.ppn: only to refund retired pickpockets
    G.FUNCS['load'][0:0] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    fin = ['execute rotated as @s run tp @e[tag=bm.new,distance=..2] ~ ~ ~ ~ 0', 'tag @e[tag=bm.new,distance=..2] remove bm.new']
    ident = [F(0), F(0), F(0), F(1)]

    # ================================================================ spawners for the new marker kinds
    spawn = G.FUNCS['npc/spawn']
    spawn[0:0] = ['execute if entity @s[tag=bm.npc.neon] run function bm:npc/neon',
                  'execute if entity @s[tag=bm.npc.crowd] run function bm:npc/crowd',
                  'execute if entity @s[tag=bm.npc.walker] run function bm:npc/walker']
    lines = []
    for nid, (rows, sc) in NEON.items():
        text = {'text': '', 'extra': []}
        for i, (t, c) in enumerate(rows):
            text['extra'].append({'text': ('\n' if i else '') + t, 'color': c, 'bold': i == 0})
        d = {'Tags': ['bm.neon', f'bm.neon_{nid}', 'bm.new'], 'text': text, 'billboard': 'fixed', 'background': Int(0), 'shadow': B(1),
             'line_width': Int(400), 'brightness': {'block': Int(15), 'sky': Int(15)},
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(sc), F(sc), F(sc)]}}
        lines.append(f'execute if entity @s[tag=bm.neon_{nid}] run summon minecraft:text_display ~ ~ ~ {snbt(d)}')
    fn('npc/neon', lines + fin)
    crowd = []
    for v in ('pirate', 'prof', 'lucky', 'chef', 'soldier', 'void', 'ember'):
        crowd.append(f'execute if entity @s[tag=bm.cv_{v}] run ' +
                     G.rat_sprite(f'bm:rat_{v}', ['bm.npc', 'bm.new', 'bm.rat_sprite', 'bm.crowd', 'bm.td', 'bm.r3d'], CROWD_SCALE.get(v, 0.62)))
    fn('npc/crowd', crowd + fin)
    walk = []
    for v in ('chef', 'pirate', 'lucky'):
        walk.append(f'execute if entity @s[tag=bm.cv_{v}] run ' +
                    G.rat_sprite(f'bm:rat_{v}', ['bm.npc', 'bm.new', 'bm.walker', 'bm.wnew'], 0.6).replace('teleport_duration:6', 'teleport_duration:5'))
    walk += [f'execute if entity @s[tag=bm.route_{r}] run tag @e[type=minecraft:item_display,tag=bm.wnew,distance=..1] add bm.route_{r}' for r in ROUTE_LEN]
    walk += ['scoreboard players set @e[type=minecraft:item_display,tag=bm.wnew,distance=..1] bm.wpi 1',
             'tag @e[type=minecraft:item_display,tag=bm.wnew,distance=..1] remove bm.wnew']
    fn('npc/walker', walk + fin)

    # ================================================================ neon flicker
    fast += ['execute as @e[type=minecraft:text_display,tag=bm.nflk] run function bm:p23/neon_on']
    fast += [f'execute as @e[type=minecraft:text_display,tag=bm.neon_{n}] at @s if entity @a[distance=..40] run function bm:p23/neon_roll' for n in FLICKER]
    fn('p23/neon_roll', ['execute store result score #f bm.rng run random value 1..70',
                         'execute if score #f bm.rng matches 1 run data merge entity @s[type=minecraft:text_display] {brightness:{block:2,sky:2},text_opacity:90b}',
                         'execute if score #f bm.rng matches 1 run tag @s add bm.nflk',
                         'execute if score #f bm.rng matches 1 run playsound minecraft:block.sculk_sensor.clicking ambient @a[distance=..12] ~ ~ ~ 0.15 2'])
    fn('p23/neon_on', ['data merge entity @s[type=minecraft:text_display] {brightness:{block:15,sky:15},text_opacity:-1b}', 'tag @s remove bm.nflk'])

    # ================================================================ walkers (stroll their route; stop and look at you up close)
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.walker] at @s if entity @a[distance=..32] run function bm:p23/walk')
    w = ['tag @e[type=minecraft:marker,tag=bm.wpt] remove bm.wpt',
         'execute if entity @a[distance=..2.5,gamemode=!spectator] facing entity @p[gamemode=!spectator] feet run return run tp @s ~ ~ ~ ~ 0']
    for r, n in ROUTE_LEN.items():
        for i in range(n):
            w.append(f'execute if entity @s[tag=bm.route_{r}] if score @s bm.wpi matches {i} run tag @e[type=minecraft:marker,tag=bm.wp,tag=bm.route_{r},tag=bm.wpi_{i},distance=..48,sort=nearest,limit=1] add bm.wpt')
    w += ['execute unless entity @e[type=minecraft:marker,tag=bm.wpt] run return 0',
          'execute if entity @e[type=minecraft:marker,tag=bm.wpt,distance=..0.6] run return run function bm:p23/walk_next',
          'execute facing entity @e[type=minecraft:marker,tag=bm.wpt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.55 run tp @s ~ ~ ~ ~ ~',
          'scoreboard players add @s bm.wst 1', 'scoreboard players operation #w bm.rng = @s bm.wst', 'scoreboard players operation #w bm.rng %= #2 bm.rng',
          'execute if score #w bm.rng matches 0 run data modify entity @s item.components."minecraft:custom_model_data" set value {strings:["tail"]}',
          'execute if score #w bm.rng matches 1 run data remove entity @s item.components."minecraft:custom_model_data"']
    fn('p23/walk', w)
    fn('p23/walk_next', ['scoreboard players add @s bm.wpi 1'] +
       [f'execute if entity @s[tag=bm.route_{r}] if score @s bm.wpi matches {n}.. run scoreboard players set @s bm.wpi 0' for r, n in ROUTE_LEN.items()])

    # ================================================================ speech bubbles
    def bubble(text, color, h):
        d = {'Tags': ['bm.bubble', 'bm.bnew'], 'text': T(text, color), 'billboard': 'center', 'background': Int(1879048192),
             'line_width': Int(150), 'brightness': {'block': Int(15), 'sky': Int(15)}, 'see_through': B(0),
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(0), F(0), F(0)]}}
        return f'summon minecraft:text_display ~ ~{h} ~ {snbt(d)}'
    for k, says in SAYS.items():
        if k not in G.NPCS: continue
        h = 1.25 if G.NPCS[k][0] == 'rat' else 2.35
        fn(f'p23/say/{k}', ['execute store result score @s bm.say run random value 9..16',
                            'execute if entity @e[type=minecraft:text_display,tag=bm.bubble,distance=..2.5] run return 0',
                            f'execute store result score #l bm.rng run random value 1..{len(says)}'] +
           [f'execute if score #l bm.rng matches {i} run {bubble(t, "white", h)}' for i, t in enumerate(says, 1)] +
           ['playsound minecraft:entity.villager.ambient neutral @a[distance=..8] ~ ~ ~ 0.3 %s' % ('1.9' if G.NPCS[k][0] == 'rat' else '1.0')])
        second.append(f'execute as @e[tag=bm.npc_{k}] at @s if entity @a[distance=..5,gamemode=!spectator] unless score @s bm.say matches 1.. run function bm:p23/say/{k}')
    second += ['scoreboard players remove @e[scores={bm.say=1..}] bm.say 1',
               'execute as @e[type=minecraft:item_display,tag=bm.crowd] at @s if entity @a[distance=..7,gamemode=!spectator] run function bm:p23/crowd_say',
               'scoreboard players add @e[type=minecraft:text_display,tag=bm.bubble] bm.blf 1',
               'execute as @e[type=minecraft:text_display,tag=bm.bubble,scores={bm.blf=5}] run data merge entity @s[type=minecraft:text_display] {start_interpolation:0,interpolation_duration:4,transformation:{scale:[0f,0f,0f]}}',
               'kill @e[type=minecraft:text_display,tag=bm.bubble,scores={bm.blf=6..}]']
    fn('p23/crowd_say', ['execute store result score #c bm.rng run random value 1..45', 'execute unless score #c bm.rng matches 1 run return 0',
                         'execute if entity @e[type=minecraft:text_display,tag=bm.bubble,distance=..3] run return 0',
                         f'execute store result score #l bm.rng run random value 1..{len(CROWD_SAYS)}'] +
       [f'execute if score #l bm.rng matches {i} run {bubble(t, "#d8d8d8", 0.95)}' for i, t in enumerate(CROWD_SAYS, 1)] +
       ['playsound minecraft:entity.silverfish.ambient neutral @a[distance=..8] ~ ~ ~ 0.3 1.7'])
    fast.append('execute as @e[type=minecraft:text_display,tag=bm.bnew] run function bm:p23/bub_pop')
    fn('p23/bub_pop', ['data merge entity @s[type=minecraft:text_display] {start_interpolation:0,interpolation_duration:3,transformation:{scale:[0.5f,0.5f,0.5f]}}', 'tag @s remove bm.bnew'])

    # ================================================================ ambience + the busker
    for k, sounds in AMB.items():
        fn(f'p23/amb/{k}', ['execute store result score #a bm.rng run random value 1..%d' % (len(sounds) * 2)] +
           [f'execute if score #a bm.rng matches {i} run playsound minecraft:{s} ambient @a[distance=..22] ~ ~ ~ {v} {p}' for i, (s, v, p) in enumerate(sounds, 1)])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.amb_{k}] at @s if entity @a[distance=..22] run function bm:p23/amb/{k}')
    fast.append('execute as @e[type=minecraft:marker,tag=bm.busker] at @s if entity @a[distance=..18] run function bm:p23/busk')
    busk = ['scoreboard players add @s bm.bn 1', 'execute if score @s bm.bn matches 32.. run scoreboard players set @s bm.bn 0']
    for i, n in enumerate(MELODY):
        if n is not None:
            busk.append(f'execute if score @s bm.bn matches {i} run playsound minecraft:block.note_block.flute record @a[distance=..18] ~ ~1 ~ 0.45 {pitch(n)}')
    for i, n in BASS.items():
        busk.append(f'execute if score @s bm.bn matches {i} run playsound minecraft:block.note_block.bass record @a[distance=..18] ~ ~1 ~ 0.5 {pitch(n + 12)}')
        busk.append(f'execute if score @s bm.bn matches {i} run particle minecraft:note ~ ~1.3 ~ {round((n % 24) / 24, 2)} 0 0 1 0')
    fn('p23/busk', busk)

    # ================================================================ steam vents (Forge Pit)
    fast.append('execute as @e[type=minecraft:marker,tag=bm.vent] at @s if entity @a[distance=..20] run function bm:p23/vent')
    fn('p23/vent', ['scoreboard players add @s bm.vt 1',
                    'execute if score @s bm.vt matches 18..21 run particle minecraft:smoke ~ ~0.3 ~ 0.1 0.05 0.1 0.01 3',
                    'execute if score @s bm.vt matches 19 run playsound minecraft:block.fire.extinguish block @a[distance=..14] ~ ~ ~ 0.3 1.7',
                    'execute if score @s bm.vt matches 22.. run function bm:p23/vent_blow'])
    fn('p23/vent_blow', ['execute store result score @s bm.vt run random value -14..0',
                         'particle minecraft:cloud ~ ~0.6 ~ 0.12 0.9 0.12 0.02 40', 'particle minecraft:poof ~ ~1.5 ~ 0.2 0.6 0.2 0.03 12',
                         'playsound minecraft:entity.generic.extinguish_fire block @a[distance=..16] ~ ~ ~ 1 0.6',
                         'playsound minecraft:block.lava.extinguish block @a[distance=..16] ~ ~ ~ 0.6 0.8',
                         'execute as @a[distance=..0.95,gamemode=!spectator,gamemode=!creative] run function bm:p23/scald'])
    fn('p23/scald', ['damage @s 3 minecraft:hot_floor', 'effect give @s minecraft:levitation 1 3 true',
                     title('@s', 'actionbar', T('Scalded by a steam vent! Watch the grates.', '#ff7a1a'))])

    # ================================================================ (1.13.1: pickpocket rats removed)
    # any still out in a world that ran 1.13 hand back what they took (to the owner, if online) and vanish
    g = G.give('token', 1)
    assert g.endswith(' 1')
    second += ['execute as @e[type=minecraft:item_display,tag=bm.pp] at @s run function bm:p23/pp_retire',
               'kill @e[type=minecraft:interaction,tag=bm.pph]']
    fn('p23/pp_retire', ['scoreboard players operation #vic bm.pid = @s bm.pid',
                         'execute if score @s bm.ppn matches 1.. store result storage bm:tmp pp.n int 1 run scoreboard players get @s bm.ppn',
                         'execute if score @s bm.ppn matches 1.. as @a if score @s bm.pid = #vic bm.pid run function bm:p23/pp_refund with storage bm:tmp pp',
                         'particle minecraft:poof ~ ~0.2 ~ 0.1 0.1 0.1 0.01 5', 'kill @s'])
    fn('p23/pp_refund', ['$' + g[:-2] + ' $(n)'])

    # ================================================================ first-load cleanup of worldgen intruders in a market's walls
    clean = []
    for y in range(-16, 16, 4):
        for blk in ('spawner', 'sculk_shrieker'):
            clean.append(f'fill ~-44 ~{y} ~-44 ~44 ~{y + 3} ~44 minecraft:cobbled_deepslate replace minecraft:{blk}')
    fn('p23/clean', ['execute unless loaded ~-44 ~ ~-44 run return 0', 'execute unless loaded ~44 ~ ~44 run return 0',
                     'execute unless loaded ~-44 ~ ~44 run return 0', 'execute unless loaded ~44 ~ ~-44 run return 0'] + clean + ['tag @s add bm.mclean'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.mkt,tag=!bm.mclean] at @s run function bm:p23/clean')

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second

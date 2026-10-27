"""2.95c: THE PIERCING BLOW - every follower honoured to rank III of Queen Ava's honours (her Champion: Vitality, Bulwark and
Might V) learns a second signature move, one that goes straight through armour.

  WHEN     in a fight, every 18 s (a monster within 12 blocks of them, you within 32; not while they sit or carry you)
  HOW      they vanish - their whole model, regalia and all, gone for half a second in a way all their own - and come back
           at the monster's back (or up out of the ground beneath it, or down out of the air above it) with one blow:
           14 damage (scaled by their Might, like every follower blow: 24.5 at Might V) of the pack's own REND, which
           ignores armour (and shields). Hit-stop, impact and Might all come from the attack kit, as for every other blow.
  KING OMEGA   Ghastly Lunge: he dives into the ghastly realm (down through the ground in a rush of souls) and lunges out
               of it beneath the monster.
  CECIL        Shadow Veil: he veils himself in shadows, and strikes from inside them.
  (everyone else: FLAV below - Emma slips into sea-spray, KillerWatt pours himself into the ground as current and erupts
   under his prey, Mr. Capshun erases himself and redraws behind it...)
Champions made before this version learn it at once; the honours page and the Champion's announcement name it."""
from items import T

CD = 18                                     # (s)
DMG = 14
# the parts that make a follower's model: (tag, carry the owner's bm.pid?) - hidden while they're "gone"
PT = {'cecil': ('bm.cpet', True), 'emma': ('bm.emp', True), 'celi': ('bm.cep', True), 'zib': ('bm.zbr', False), 'kw': ('bm.kxp', True),
      'leo': ('bm.lep', True), 'demo': ('bm.dmp', True), 'apo': ('bm.app', True), 'tul': ('bm.tup', True), 'frog': ('bm.fp_disp', False),
      'don': ('bm.fp_disp', False), 'wil': ('bm.wil_part', False), 'fishy': ('bm.fyp', True), 'dennis': ('bm.dwp', True), 'pistachio': ('bm.pip', True),
      'omega': ('bm.omp', True), 'ashur': ('bm.asp', True), 'chef': ('bm.kkp', True), 'neighbor': ('bm.nbp', True), 'ava': ('bm.avp', True),
      'pearlq': ('bm.pqp', True), 'bloo': ('bm.bop', True), 'stalker': ('bm.svp', True), 'lantern': ('bm.lnp', True), 'bender': ('bm.bvp', True),
      'bones': ('bm.bjp', True), 'capshun': ('bm.mzp', True), 'pxcecil': ('bm.xcp', True), 'pxleo': ('bm.xlp', True), 'pxemma': ('bm.xmp', True),
      'sky': ('bm.ybp', True)}

# (name, what it looks like, where they come back: behind / below / above, the vanish, the sign at the foe while they're gone,
#  the return, the sound going, the sound coming)
P = lambda p, n=24, s=0.4, h=0.7, v=0.03: f'{p} ~ ~1 ~ {s} {h} {s} {v} {n}'
FLAV = {
    'omega': ('Ghastly Lunge', 'dives into the ghastly realm and lunges out of it beneath the monster', 'below',
              [P('minecraft:sculk_soul', 30, 0.5, 0.3, 0.05), P('minecraft:soul', 20, 0.4, 0.2, 0.02), 'minecraft:large_smoke ~ ~0.2 ~ 0.5 0.1 0.5 0.02 20'],
              ['minecraft:sculk_soul ~ ~0.1 ~ 0.4 0 0.4 0.01 4', 'minecraft:soul ~ ~0.1 ~ 0.5 0 0.5 0.02 2'],
              [P('minecraft:sculk_soul', 40, 0.4, 1.0, 0.12), P('minecraft:soul_fire_flame', 20, 0.3, 0.8, 0.06), 'minecraft:block{block_state:"minecraft:soul_soil"} ~ ~0.2 ~ 0.6 0.1 0.6 0 40'],
              'minecraft:entity.warden.dig', 'minecraft:entity.warden.emerge'),
    'cecil': ('Shadow Veil', 'veils himself in shadows and strikes from inside them', 'behind',
              [P('minecraft:squid_ink', 40, 0.4, 0.8, 0.03), P('minecraft:large_smoke', 25, 0.4, 0.8, 0.01)],
              ['minecraft:squid_ink ^ ^1 ^-1.2 0.25 0.4 0.25 0.01 4', 'minecraft:smoke ^ ^1 ^-1.2 0.25 0.5 0.25 0.01 4'],
              [P('minecraft:squid_ink', 30, 0.5, 0.8, 0.12), P('minecraft:witch', 25, 0.4, 0.8, 0.05), P('minecraft:enchanted_hit', 20, 0.3, 0.5, 0.3)],
              'minecraft:entity.illusioner.prepare_mirror', 'minecraft:entity.illusioner.mirror_move'),
    'emma': ('Sea-Spray Step', 'slips into sea-spray and blossoms back at the monster\'s back', 'behind',
             [P('minecraft:splash', 40), P('minecraft:cherry_leaves', 20)], ['minecraft:splash ^ ^1 ^-1.2 0.2 0.3 0.2 0 4'],
             [P('minecraft:cherry_leaves', 30, 0.5, 0.6, 0.05), P('minecraft:bubble_pop', 20)], 'minecraft:entity.dolphin.splash', 'minecraft:block.amethyst_block.chime'),
    'celi': ('Whiteout', 'vanishes in a flurry and drops out of the snow-glare above', 'above',
             [P('minecraft:snowflake', 40, 0.4, 0.8, 0.05)], ['minecraft:snowflake ~ ~3 ~ 0.4 0.3 0.4 0.02 4'],
             [P('minecraft:snowflake', 40, 0.6, 0.6, 0.1), 'minecraft:block{block_state:"minecraft:snow_block"} ~ ~0.3 ~ 0.5 0.1 0.5 0 20'],
             'minecraft:block.powder_snow.step', 'minecraft:block.glass.break'),
    'zib': ('Phase Shift', 'beams out, and beams back in right behind the monster', 'behind',
            [P('minecraft:end_rod', 25, 0.3, 0.8, 0.05), P('minecraft:electric_spark', 20)], ['minecraft:end_rod ^ ^1 ^-1.2 0.1 0.5 0.1 0 2'],
            [P('minecraft:end_rod', 30, 0.3, 0.8, 0.1), P('minecraft:electric_spark', 30, 0.4, 0.6, 0.2)], 'minecraft:block.beacon.deactivate', 'minecraft:block.beacon.power_select'),
    'kw': ('Ground Current', 'pours himself into the ground as current and erupts under his prey', 'below',
           [P('minecraft:electric_spark', 50, 0.5, 0.5, 0.3)], ['minecraft:electric_spark ~ ~0.1 ~ 0.6 0 0.6 0.2 6'],
           [P('minecraft:electric_spark', 60, 0.4, 1.0, 0.4), 'minecraft:flash{color:[0.5,1.0,0.4,1.0]} ~ ~1 ~ 0 0 0 0 1'],
           'minecraft:block.respawn_anchor.charge', 'minecraft:entity.lightning_bolt.impact'),
    'leo': ('Riptide Charge', 'vanishes in a riptide and drives through the monster\'s guard', 'behind',
            [P('minecraft:splash', 40), P('minecraft:bubble', 20)], ['minecraft:bubble ^ ^1 ^-1.2 0.2 0.4 0.2 0 4'],
            [P('minecraft:splash', 40, 0.5, 0.6, 0.2), P('minecraft:sweep_attack', 1, 0, 0, 0)], 'minecraft:item.trident.riptide_1', 'minecraft:item.trident.hit'),
    'demo': ("Reaper's Toll", 'dissolves into storm-cloud and reaps from behind', 'behind',
             [P('minecraft:cloud', 30, 0.4, 0.8, 0.02), P('minecraft:large_smoke', 20)], ['minecraft:cloud ^ ^1.6 ^-1.2 0.3 0.2 0.3 0 3'],
             [P('minecraft:sweep_attack', 3, 0.5, 0.3, 0), P('minecraft:electric_spark', 30, 0.4, 0.8, 0.2)], 'minecraft:item.trident.thunder', 'minecraft:entity.player.attack.sweep'),
    'apo': ("Serpent's Rise", 'sinks into the earth as a shadow and bursts up beneath the monster', 'below',
            [P('minecraft:soul_fire_flame', 30, 0.5, 0.3, 0.03), 'minecraft:block{block_state:"minecraft:dirt"} ~ ~0.2 ~ 0.5 0.1 0.5 0 30'],
            ['minecraft:soul_fire_flame ~ ~0.1 ~ 0.5 0 0.5 0.01 3'],
            [P('minecraft:soul_fire_flame', 40, 0.4, 1.0, 0.1), 'minecraft:block{block_state:"minecraft:dirt"} ~ ~0.3 ~ 0.6 0.2 0.6 0 40'],
            'minecraft:entity.evoker_fangs.attack', 'minecraft:entity.ravager.attack'),
    'tul': ('Frozen Feint', 'fades into freezing fog and strikes from behind', 'behind',
            [P('minecraft:snowflake', 30), P('minecraft:cloud', 20, 0.4, 0.6, 0.01)], ['minecraft:snowflake ^ ^1 ^-1.2 0.2 0.4 0.2 0 4'],
            [P('minecraft:snowflake', 40, 0.5, 0.6, 0.1), P('minecraft:sweep_attack', 1, 0, 0, 0)], 'minecraft:block.powder_snow.step', 'minecraft:entity.player.attack.crit'),
    'frog': ('Leap of Faith', 'leaps clean out of sight and lands on the monster from above', 'above',
             [P('minecraft:item_slime', 30, 0.4, 0.3, 0.1)], ['minecraft:item_slime ~ ~3 ~ 0.3 0.2 0.3 0 2'],
             [P('minecraft:item_slime', 40, 0.6, 0.3, 0.2)], 'minecraft:entity.frog.long_jump', 'minecraft:entity.slime.squish'),
    'don': ('Cloak Field', 'flickers out behind an alien cloak, and decloaks at the monster\'s back', 'behind',
            [P('minecraft:portal', 40, 0.4, 0.8, 0.2)], ['minecraft:reverse_portal ^ ^1 ^-1.2 0.2 0.4 0.2 0.02 4'],
            [P('minecraft:end_rod', 30, 0.3, 0.6, 0.1), P('minecraft:portal', 30)], 'minecraft:block.beacon.deactivate', 'minecraft:entity.enderman.teleport'),
    'wil': ('Grave Walk', 'sinks into a grave of his own and climbs out under the monster', 'below',
            [P('minecraft:soul', 30, 0.4, 0.4, 0.02), P('minecraft:smoke', 20)], ['minecraft:soul ~ ~0.1 ~ 0.4 0 0.4 0.01 3'],
            [P('minecraft:soul', 40, 0.4, 0.9, 0.06), 'minecraft:block{block_state:"minecraft:coarse_dirt"} ~ ~0.2 ~ 0.5 0.1 0.5 0 30'],
            'minecraft:entity.wither.ambient', 'minecraft:entity.wither_skeleton.hurt'),
    'fishy': ('Undertow', 'dives into a swirl of bubbles and surfaces at the monster\'s back', 'behind',
              [P('minecraft:bubble_pop', 40), P('minecraft:splash', 30)], ['minecraft:bubble_pop ^ ^1 ^-1.2 0.2 0.3 0.2 0 4'],
              [P('minecraft:splash', 40, 0.5, 0.6, 0.2), P('minecraft:bubble_pop', 30)], 'minecraft:block.bubble_column.upwards_inside', 'minecraft:entity.fish.swim'),
    'dennis': ('Tunnel Strike', 'burrows out of sight and bursts up beneath the monster, pick first', 'below',
               ['minecraft:block{block_state:"minecraft:dirt"} ~ ~0.2 ~ 0.5 0.1 0.5 0 40'], ['minecraft:block{block_state:"minecraft:gravel"} ~ ~0.1 ~ 0.4 0 0.4 0 3'],
               ['minecraft:block{block_state:"minecraft:stone"} ~ ~0.3 ~ 0.6 0.2 0.6 0 50', P('minecraft:wax_on', 20)], 'minecraft:block.gravel.break', 'minecraft:block.stone.break'),
    'pistachio': ('Through the Wall', 'drifts through the nearest wall and out of the next one, behind the monster', 'behind',
                  [P('minecraft:soul', 20), P('minecraft:poof', 20)], ['minecraft:soul ^ ^1 ^-1.2 0.2 0.4 0.2 0.01 2'],
                  [P('minecraft:soul', 30, 0.4, 0.6, 0.05), P('minecraft:poof', 20)], 'minecraft:entity.vex.charge', 'minecraft:entity.vex.hurt'),
    'ashur': ('Ember Blink', 'gutters out like a candle and flares back at the monster\'s back', 'behind',
              [P('minecraft:smoke', 30), P('minecraft:small_flame', 20)], ['minecraft:small_flame ^ ^1 ^-1.2 0.1 0.3 0.1 0 3'],
              [P('minecraft:flame', 40, 0.4, 0.8, 0.08), P('minecraft:lava', 6)], 'minecraft:block.fire.extinguish', 'minecraft:entity.blaze.shoot'),
    'chef': ('Kitchen Ambush', 'vanishes in a puff of kitchen steam and serves the monster from behind', 'behind',
             [P('minecraft:cloud', 30, 0.4, 0.8, 0.02)], ['minecraft:white_smoke ^ ^1 ^-1.2 0.2 0.3 0.2 0.01 3'],
             [P('minecraft:flame', 20), P('minecraft:crit', 30)], 'minecraft:block.fire.extinguish', 'minecraft:entity.player.attack.crit'),
    'neighbor': ('Off the Record', 'slips out of sight in a flurry of notes, and lands on the downbeat behind the monster', 'behind',
                 [P('minecraft:note', 20, 0.6, 0.6, 1)], ['minecraft:note ^ ^1.4 ^-1.2 0.3 0.3 0.3 1 1'],
                 [P('minecraft:note', 20, 0.6, 0.6, 1), P('minecraft:crit', 30)], 'minecraft:block.note_block.chime', 'minecraft:block.note_block.bell'),
    'ava': ('Abyssal Grace', 'sinks into a tide no one else can see and rises at the monster\'s back', 'behind',
            [P('minecraft:bubble', 30), P('minecraft:glow', 20)], ['minecraft:glow ^ ^1 ^-1.2 0.2 0.4 0.2 0 2'],
            [P('minecraft:splash', 40, 0.5, 0.6, 0.2), P('minecraft:glow', 20)], 'minecraft:block.conduit.deactivate', 'minecraft:block.conduit.attack.target'),
    'pearlq': ('Glimmer Step', 'vanishes in a glimmer of pearl-light and strikes from behind', 'behind',
               [P('minecraft:glow', 30), P('minecraft:end_rod', 20)], ['minecraft:glow ^ ^1 ^-1.2 0.2 0.4 0.2 0 2'],
               [P('minecraft:end_rod', 30, 0.3, 0.6, 0.1), P('minecraft:glow', 20)], 'minecraft:block.amethyst_block.resonate', 'minecraft:block.bell.use'),
    'bloo': ('Feral Ambush', 'melts into the undergrowth and pounces from behind', 'behind',
             [P('minecraft:crimson_spore', 40)], ['minecraft:crimson_spore ^ ^0.6 ^-1.2 0.3 0.2 0.3 0 3'],
             [P('minecraft:crimson_spore', 40, 0.5, 0.5, 0.1), P('minecraft:crit', 30)], 'minecraft:entity.fox.sniff', 'minecraft:entity.ravager.roar'),
    'stalker': ('From the Dark', 'folds into the dark and unfolds behind the monster', 'behind',
                [P('minecraft:squid_ink', 40)], ['minecraft:squid_ink ^ ^1 ^-1.2 0.2 0.5 0.2 0 3'],
                [P('minecraft:squid_ink', 40, 0.5, 0.8, 0.1), P('minecraft:sculk_soul', 10)], 'minecraft:entity.warden.sniff', 'minecraft:entity.warden.attack_impact'),
    'lantern': ('Wick Snuff', 'snuffs his own flame out, and re-lights at the monster\'s back', 'behind',
                [P('minecraft:smoke', 40)], ['minecraft:small_flame ^ ^1.4 ^-1.2 0.05 0.05 0.05 0 1'],
                [P('minecraft:flame', 40, 0.4, 0.8, 0.08), P('minecraft:small_flame', 20)], 'minecraft:block.candle.extinguish', 'minecraft:item.firecharge.use'),
    'bender': ('Blur', 'is simply too fast to see, and then he\'s at the monster\'s back', 'behind',
               [P('minecraft:cloud', 20, 0.4, 0.2, 0.1)], ['minecraft:crit ^ ^0.6 ^-1.2 0.2 0.2 0.2 0.1 3'],
               [P('minecraft:crit', 40, 0.4, 0.5, 0.3), P('minecraft:cloud', 20)], 'minecraft:entity.breeze.wind_burst', 'minecraft:entity.wolf.growl'),
    'bones': ('Deep Ambush', 'sinks into deep water that isn\'t there and bursts out under the monster', 'below',
              [P('minecraft:splash', 50, 0.5, 0.3, 0.2)], ['minecraft:bubble_pop ~ ~0.1 ~ 0.5 0 0.5 0 4'],
              [P('minecraft:splash', 60, 0.5, 1.0, 0.3), P('minecraft:bubble', 30)], 'minecraft:entity.dolphin.splash', 'minecraft:entity.guardian.attack'),
    'capshun': ('Eraser Trick', 'erases himself, and redraws himself right behind the monster', 'behind',
                [P('minecraft:white_ash', 50, 0.4, 0.8, 0.02)], ['minecraft:end_rod ^ ^1 ^-1.2 0.2 0.4 0.2 0 1'],
                [P('minecraft:white_ash', 40), P('minecraft:end_rod', 20, 0.3, 0.6, 0.05)], 'minecraft:item.book.page_turn', 'minecraft:ui.cartography_table.take_result'),
    'pxcecil': ('Glitch Step', 'glitches out of the screen and back into it behind the monster', 'behind',
                [P('minecraft:dust{color:[0.6,0.2,0.9],scale:1.5}', 30)], ['minecraft:dust{color:[0.6,0.2,0.9],scale:1.0} ^ ^1 ^-1.2 0.2 0.4 0.2 0 3'],
                [P('minecraft:witch', 30), P('minecraft:dust{color:[0.6,0.2,0.9],scale:1.5}', 30)], 'minecraft:block.note_block.bit', 'minecraft:block.note_block.bit'),
    'pxleo': ('Dash Slash', 'dashes off the edge of the screen and slashes in from behind', 'behind',
              [P('minecraft:dust{color:[0.3,0.7,0.9],scale:1.5}', 30)], ['minecraft:dust{color:[0.3,0.7,0.9],scale:1.0} ^ ^1 ^-1.2 0.2 0.4 0.2 0 3'],
              [P('minecraft:sweep_attack', 2, 0.3, 0.3, 0), P('minecraft:dust{color:[0.3,0.7,0.9],scale:1.5}', 30)], 'minecraft:block.note_block.bit', 'minecraft:entity.player.attack.sweep'),
    'pxemma': ('Star Warp', 'warps out on a pixel star and drops in from above', 'above',
               [P('minecraft:dust{color:[1.0,0.6,0.85],scale:1.5}', 30)], ['minecraft:dust{color:[1.0,0.9,0.4],scale:1.2} ~ ~3 ~ 0.2 0.2 0.2 0 3'],
               [P('minecraft:dust{color:[1.0,0.9,0.4],scale:1.5}', 40, 0.5, 0.5, 0)], 'minecraft:block.note_block.bit', 'minecraft:entity.player.levelup'),
    'sky': ('Storm Front', 'blow away on the wind and come down on the monster out of a thundercloud', 'above',
            [P('minecraft:cloud', 40, 0.5, 0.8, 0.05)], ['minecraft:cloud ~ ~3.2 ~ 0.6 0.1 0.6 0 4'],
            [P('minecraft:electric_spark', 40, 0.5, 0.8, 0.3), P('minecraft:end_rod', 20, 0.3, 0.6, 0.1)], 'minecraft:entity.breeze.wind_burst', 'minecraft:entity.lightning_bolt.thunder'),
}
TICKS = {'vanish': 1, 'move': 8, 'show': 11, 'end': 15}


def generate(G):
    import phase173 as P173
    import phase205 as P205
    import atk
    from phase125 import WHO
    fn, title, tellraw = G.fn, G.title, G.tellraw
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    FOL = [w for w in P173.AR if w in WHO]
    assert set(FOL) == set(FLAV) == set(PT), set(FOL) ^ set(FLAV)
    ME = {f: tag.replace('bm.', '') for tag, (f, _a) in atk.ME.items()}          # each follower's own "by" tag: its blows' hit-stop, impact and Might
    typ = lambda w: P173.AR[w][1]
    host = lambda w, x='': f'@e[type=minecraft:{typ(w)},tag={P173.AR[w][2]}{"," + x if x else ""}]'
    objs = ['bm.prt', 'bm.prcd', 'bm.prk', 'bm.prvr', 'bm.prh']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # the pack's own REND: through armour and shields, and never lost to the blow just before it (a hurt foe's half-second) (the damage still scales by difficulty, as a mob's blow does)
    import json, os
    G.wjson('bm/damage_type/rend.json', {'exhaustion': 0.1, 'message_id': 'bm.rend', 'scaling': 'when_caused_by_living_non_player', 'effects': 'hurt'})
    for tg in ('bypasses_armor', 'bypasses_shield', 'bypasses_cooldown'):
        f_ = G.path('data', 'minecraft', 'tags', 'damage_type', f'{tg}.json')
        vals = json.load(open(f_))['values'] if os.path.exists(f_) else []
        G.wjson(f'minecraft/tags/damage_type/{tg}.json', {'replace': False, 'values': [v for v in vals if v != 'bm:rend'] + ['bm:rend']})

    FOE = '@e[type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,distance=..12,sort=nearest,limit=1]'
    for w in FOL:
        nm, col = WHO[w][0], WHO[w][2]
        name, desc, where, out, sign, back, s_out, s_in = FLAV[w]
        me = ME.get(w, 'prme')
        ptag, pid = PT[w]
        mine = 'if score @s bm.pid = #me bm.pid' if pid else ''
        hide = ['scoreboard players operation #me bm.pid = @s bm.pid',
                f'execute as @e[type=minecraft:item_display,tag={ptag},distance=..{6 if pid else 2.5}] {mine} run function bm:p226/hide'.replace('  ', ' '),
                f'execute as @e[type=minecraft:item_display,tag=bm.chp_{w},distance=..6] if score @s bm.pid = #me bm.pid run function bm:p226/hide']
        if w == 'wil':
            hide.append('execute as @e[type=minecraft:wither_skeleton,tag=bm.wil_body,distance=..4,sort=nearest,limit=1] run effect give @s minecraft:invisibility 1 0 true')
        # (each second: a Champion, rested, a monster near, its owner near, not sitting, not ridden) - go
        fn(f'p226/sec/{w}', ['execute if score @s bm.prcd matches 1.. run return run scoreboard players remove @s bm.prcd 1',
                             'execute if score @s bm.prt matches 1.. run return 0',
                             'execute if data entity @s {Sitting:1b} run return 0',
                             'execute on passengers if entity @s[type=minecraft:player] run return 0',
                             f'execute unless entity {FOE} run return 0',
                             'scoreboard players operation #me bm.pid = @s bm.pid',
                             'scoreboard players set #o bm.rng 0', 'execute as @a[distance=..32] if score @s bm.pid = #me bm.pid run scoreboard players set #o bm.rng 1',
                             'execute if score #o bm.rng matches 0 run return 0',
                             f'function bm:p226/go/{w}'])
        fn(f'p226/go/{w}', [f'scoreboard players set @s bm.prcd {CD}', 'scoreboard players set @s bm.prt 1',
                            'scoreboard players add #prk bm.rng 1', 'scoreboard players operation @s bm.prk = #prk bm.rng',
                            f'execute as {FOE} run function bm:p226/mark'])
        # each tick of the move (as the follower, at it)
        L = ['scoreboard players add @s bm.prt 1', 'scoreboard players operation #pk bm.rng = @s bm.prk',
             'tag @e[tag=bm.prfoe] remove bm.prfoe',
             'execute as @e[tag=bm.prtg,distance=..24] if score @s bm.prk = #pk bm.rng run tag @s add bm.prfoe',
             f'execute if score @s bm.prt matches {TICKS["vanish"] + 1} run function bm:p226/out/{w}',
             f'execute if score @s bm.prt matches {TICKS["vanish"] + 2}..{TICKS["show"] - 1} at @e[tag=bm.prfoe,limit=1] rotated as @e[tag=bm.prfoe,limit=1] run function bm:p226/sign/{w}',
             f'execute if score @s bm.prt matches {TICKS["move"]} run function bm:p226/move/{w}',
             f'execute if score @s bm.prt matches {TICKS["show"]} run function bm:p226/in/{w}',
             f'execute if score @s bm.prt matches {TICKS["end"]}.. run function bm:p226/end']
        fn(f'p226/tick/{w}', L)
        fn(f'p226/out/{w}', [f'particle {p}' for p in out] + [f'playsound {s_out} neutral @a[distance=..24] ~ ~ ~ 1 1'] + hide +
           ['data merge entity @s {NoAI:1b,Invulnerable:1b}'] +
           ([f'execute positioned ~ ~-0.6 ~ run particle {p}' for p in out[:1]] if where == 'below' else []))
        fn(f'p226/sign/{w}', [f'particle {p}' for p in sign])
        # where they come back: at the foe's back facing it - out of the ground beneath it, or down out of the air, first
        fn(f'p226/move/{w}', [f'execute at @e[tag=bm.prfoe,limit=1] rotated as @e[tag=bm.prfoe,limit=1] rotated ~ 0 positioned ^ ^ ^-1.2 '
                              f'facing entity @e[tag=bm.prfoe,limit=1] feet run tp @s ~ ~{-1.4 if where == "below" else (2.4 if where == "above" else 0)} ~ ~ 0'])
        hit_fx = [f'particle {p}' for p in back]
        fn(f'p226/in/{w}', [f'execute at @e[tag=bm.prfoe,limit=1] rotated as @e[tag=bm.prfoe,limit=1] rotated ~ 0 positioned ^ ^ ^-1.2 '
                            f'facing entity @e[tag=bm.prfoe,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                            'scoreboard players operation #me bm.pid = @s bm.pid', 'execute as @e[type=minecraft:item_display,tag=bm.prhid,distance=..8] run function bm:p226/show_mine',
                            'execute if entity @e[type=minecraft:wither_skeleton,tag=bm.wil_body,distance=..4] run effect clear @e[type=minecraft:wither_skeleton,tag=bm.wil_body,distance=..4,sort=nearest,limit=1] minecraft:invisibility',
                            f'playsound {s_in} neutral @a[distance=..24] ~ ~ ~ 1 1', f'tag @s add bm.{me}',
                            f'execute as @e[tag=bm.prfoe,limit=1] at @s run function bm:p226/hit/{w}', f'tag @s remove bm.{me}'])
        fn(f'p226/hit/{w}', hit_fx + ['particle minecraft:flash{color:[1.0,1.0,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1',
                                      f'damage @s {DMG} bm:rend by @e[type=minecraft:{typ(w)},tag=bm.{me},limit=1]',
                                      'particle minecraft:enchanted_hit ~ ~1.2 ~ 0.3 0.4 0.3 0.4 20'])
        tick.append(f'execute as {host(w, "scores={bm.prt=1..}")} at @s run function bm:p226/tick/{w}')
        second.append(f'execute as {host(w, "tag=bm.champ")} at @s run function bm:p226/sec/{w}')
        # the Champion's announcement names it
        G.FUNCS[f'p205/check/{w}'].insert(-2, tellraw('@s', G.PREFIX + [T('...and a piercing blow: ', 'gray'), T(name, '#ff7a7a', bold=True),
                                                                        T(f' - {nm} {desc}, straight through armour.', 'gray')]))
    fn('p226/mark', ['tag @s add bm.prtg', 'scoreboard players operation @s bm.prk = #prk bm.rng'])
    # (parts: their reach saved, then nothing to see; back as they were - or within a few seconds, whatever happens)
    fn('p226/hide', ['execute if entity @s[tag=bm.prhid] run return 0', 'execute store result score @s bm.prvr run data get entity @s view_range 100',
                     'data merge entity @s[type=minecraft:item_display] {view_range:0.0f}', 'tag @s add bm.prhid', 'scoreboard players set @s bm.prh 3'])
    fn('p226/show', ['execute store result entity @s[type=minecraft:item_display] view_range float 0.01 run scoreboard players get @s bm.prvr', 'tag @s remove bm.prhid'])
    fn('p226/show_mine', ['execute if score @s bm.pid = #me bm.pid run return run function bm:p226/show',
                          'execute unless score @s bm.pid matches 1.. run function bm:p226/show'])
    fn('p226/end', ['scoreboard players set @s bm.prt 0', 'data merge entity @s {NoAI:0b,Invulnerable:0b}',
                    'execute as @e[tag=bm.prtg] if score @s bm.prk = #pk bm.rng run tag @s remove bm.prtg', 'tag @e[tag=bm.prfoe] remove bm.prfoe',
                    'scoreboard players operation #me bm.pid = @s bm.pid', 'execute as @e[type=minecraft:item_display,tag=bm.prhid,distance=..8] run function bm:p226/show_mine'])
    second += ['execute as @e[type=minecraft:item_display,tag=bm.prhid] run scoreboard players remove @s bm.prh 1',
               'execute as @e[type=minecraft:item_display,tag=bm.prhid,scores={bm.prh=..0}] run function bm:p226/show']
    for w in FOL:          # (a move cut short - the follower sent home, a faint, an unloaded chunk: never left frozen)
        second.append(f'execute as {host(w, "scores={bm.prt=1..},tag=!bm.champ")} at @s run function bm:p226/end')


def rp(R):
    R.LANG.update({'death.attack.bm.rend': '%1$s was struck straight through their armour',
                   'death.attack.bm.rend.player': '%1$s was struck straight through their armour by %2$s'})

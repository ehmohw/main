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
(2.95e) NOT EVERYONE VANISHES - the move suits the one making it. The fighters go in where you can see them, on their own
poses (atk.sig), the same 14 of rend in all, split across the blows:
  EMMA         Axe Roll: up into the air in a tucked somersault, the axe held over her head - and slammed down on it (and a
               shockwave of petals round it).
  BENDER       Savage Maul: he pounces, claws the monster four times over - then clambers up and chomps on its head.
  LEO          Shield Bash: a bash of the shield stuns it (it can't move or hit back for a moment), and the trident goes
               through it, three times.
  BLOO         Feral Frenzy: a pounce and a frenzy of claws, and a roar over it.
  BONES        Death Roll: his jaws clamp on, and he rolls it, thrashing.
  DEMOCRATUS   Reaper's Toll: the scythe raised high and brought down through its guard, and reaped on the backswing.
  THE CHEF     Order Up!: tenderised with a flurry of whacks - and the finisher, served.
  TULLIUS      Hook and Broadside: harpooned and dragged in, run through twice, and the blunderbuss point-blank.
The ones who vanish do it because it's who they are: Omega's ghastly realm, Cecil's shadows, the Stalker's dark, Pistachio
through the walls, Wilfrey's grave, Mr. Capshun's eraser, Kettle's hide-and-seek, Zib's beam...
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
      'sky': ('bm.ybp', True), 'kettle': ('bm.ktp', True), 'rufus': ('bm.rup', True), 'henry': ('bm.hyp', True), 'nia': ('bm.nip', True), 'gem': ('bm.cgp', True), 'batty': ('bm.ytp', True), 'eggbert': ('bm.ebp', True), 'count': ('bm.knp', True), 'dragon': ('bm.ddp', True), 'eraser': ('bm.ezp', True), 'cursor': ('bm.uxp', True), 'inkblot': ('bm.ibp', True), 'speech': ('bm.wbp', True), 'lightbringer': ('bm.lhp', True), 'dryad': ('bm.pyp', True), 'sovereign': ('bm.xvp', True), 'vexis': ('bm.xbp', True), 'mireling': ('bm.mlp', True)}

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
    'kettle': ('Hide and Seek', 'counts to three with his eyes shut, hides - and pops out right behind the monster', 'behind',
               [P('minecraft:poof', 20), P('minecraft:happy_villager', 10)], ['minecraft:happy_villager ^ ^1 ^-1.2 0.2 0.4 0.2 0 1'],
               [P('minecraft:crit', 30, 0.4, 0.6, 0.3), P('minecraft:happy_villager', 16)], 'minecraft:entity.chicken.egg', 'minecraft:entity.player.attack.knockback'),
    'gem': ('Into the Canvas', 'dissolves into a swirl of colour and paints itself back in, right behind the monster', 'behind',
            [P('minecraft:end_rod', 30, 0.4, 0.5, 0.05), P('minecraft:dust{color:[1.0,0.4,0.7],scale:1.2}', 20)], ['minecraft:end_rod ^ ^1 ^-1.2 0.2 0.3 0.2 0.01 2'],
            [P('minecraft:dust{color:[0.4,0.8,1.0],scale:1.4}', 30), P('minecraft:end_rod', 20, 0.4, 0.5, 0.1)], 'minecraft:block.amethyst_block.resonate', 'minecraft:block.amethyst_cluster.break'),
    'batty': ('Into the Rafters', 'flutters up out of sight and drops on the monster from above, fangs first', 'above',
              [P('minecraft:large_smoke', 20, 0.4, 0.4, 0.02)], ['minecraft:large_smoke ~ ~3 ~ 0.3 0.2 0.3 0 2'],
              [P('minecraft:crit', 30, 0.4, 0.5, 0.3), P('minecraft:large_smoke', 20)], 'minecraft:entity.bat.takeoff', 'minecraft:entity.bat.hurt'),
    'eggbert': ('Down the Drain', 'oozes down into the cracks and wells up beneath the monster', 'below',
                [P('minecraft:squid_ink', 40, 0.5, 0.2, 0.02)], ['minecraft:squid_ink ~ ~0.1 ~ 0.4 0 0.4 0.01 3'],
                [P('minecraft:squid_ink', 40, 0.4, 0.8, 0.08), P('minecraft:item_slime', 20)], 'minecraft:block.honey_block.slide', 'minecraft:entity.slime.attack'),
    'count': ('Exit, Stage Left', 'tips his hat, steps behind his cape - and is somehow behind the monster', 'behind',
              [P('minecraft:poof', 20), P('minecraft:item_slime', 10)], ['minecraft:item_slime ^ ^1 ^-1.2 0.2 0.3 0.2 0 1'],
              [P('minecraft:enchanted_hit', 20, 0.3, 0.5, 0.2), P('minecraft:item_slime', 20)], 'minecraft:block.note_block.bell', 'minecraft:entity.player.attack.strong'),
    'dragon': ('Off the Page', 'climbs back into his drawing - and scribbles himself in right behind the monster', 'behind',
               [P('minecraft:poof', 20), P('minecraft:flame', 10)], ['minecraft:small_flame ^ ^1 ^-1.2 0.2 0.3 0.2 0 1'],
               [P('minecraft:flame', 30, 0.4, 0.6, 0.1), P('minecraft:crit', 20)], 'minecraft:item.book.page_turn', 'minecraft:entity.blaze.shoot'),
    'eraser': ('Rubbed Out', 'rubs itself out of the picture - and draws itself back in behind the monster', 'behind',
               [P('minecraft:cherry_leaves', 20), P('minecraft:poof', 10)], ['minecraft:cherry_leaves ^ ^1 ^-1.2 0.2 0.3 0.2 0 1'],
               [P('minecraft:cherry_leaves', 30, 0.4, 0.6, 0.1), P('minecraft:crit', 20)], 'minecraft:item.brush.brushing.generic', 'minecraft:item.brush.brushing.sand'),
    'cursor': ('Drag and Drop', 'drags itself off the screen and drops in on the monster from above', 'above',
               [P('minecraft:electric_spark', 30, 0.3, 0.5, 0.2)], ['minecraft:electric_spark ~ ~3 ~ 0.2 0.1 0.2 0.05 2'],
               [P('minecraft:electric_spark', 40, 0.4, 0.6, 0.3), P('minecraft:enchanted_hit', 20)], 'minecraft:ui.button.click', 'minecraft:block.note_block.bit'),
    'inkblot': ('Seep', 'soaks into the ground and wells up beneath the monster', 'below',
               [P('minecraft:squid_ink', 40, 0.5, 0.2, 0.02)], ['minecraft:squid_ink ~ ~0.1 ~ 0.4 0 0.4 0.01 3'],
               [P('minecraft:squid_ink', 40, 0.4, 0.8, 0.08)], 'minecraft:entity.slime.squish', 'minecraft:entity.slime.attack'),
    'speech': ('Next Panel', 'pops - and is already in the next panel, right behind the monster', 'behind',
               [P('minecraft:poof', 20), P('minecraft:end_rod', 10)], ['minecraft:end_rod ^ ^1 ^-1.2 0.2 0.3 0.2 0 1'],
               [P('minecraft:explosion', 2, 0.2, 0.3, 0), P('minecraft:crit', 20)], 'minecraft:entity.chicken.egg', 'minecraft:entity.player.attack.knockback'),
    'lightbringer': ('Descent', 'rises into the light and comes down on the monster from above, staff first', 'above',
               [P('minecraft:end_rod', 30, 0.3, 0.6, 0.05)], ['minecraft:end_rod ~ ~3 ~ 0.2 0.2 0.2 0.01 2'],
               [P('minecraft:end_rod', 40, 0.4, 0.8, 0.2), P('minecraft:flash{color:[1.0,0.92,0.6,1.0]}', 1, 0, 0, 0)], 'minecraft:block.beacon.activate', 'minecraft:entity.lightning_bolt.impact'),
    'dryad': ('Mycelium', 'sinks into the moss and springs up beneath the monster in a burst of spores', 'below',
               [P('minecraft:spore_blossom_air', 30, 0.5, 0.3, 0)], ['minecraft:spore_blossom_air ~ ~0.1 ~ 0.4 0 0.4 0 2'],
               [P('minecraft:spore_blossom_air', 40, 0.5, 0.8, 0), P('minecraft:crit', 20)], 'minecraft:block.moss.break', 'minecraft:block.rooted_dirt.break'),
    'sovereign': ('Chainstep', 'snaps its chain taut - and is suddenly behind the monster, greatsword already falling', 'behind',
               [P('minecraft:sculk_soul', 20), P('minecraft:large_smoke', 10)], ['minecraft:sculk_soul ^ ^1 ^-1.2 0.2 0.3 0.2 0 1'],
               [P('minecraft:sculk_soul', 30, 0.4, 0.6, 0.1), P('minecraft:crit', 20)], 'minecraft:block.chain.break', 'minecraft:entity.warden.attack_impact'),
    'mireling': ('Puddle Step', 'sinks into its puddle - and rises beneath the monster, maw first', 'below',
               [P('minecraft:squid_ink', 30, 0.5, 0.2, 0.02)], ['minecraft:squid_ink ~ ~0.1 ~ 0.4 0 0.4 0.01 2'],
               [P('minecraft:squid_ink', 40, 0.4, 0.8, 0.08), P('minecraft:crit', 20)], 'minecraft:block.bubble_column.whirlpool_ambient', 'minecraft:entity.warden.attack_impact'),
    'vexis': ('Gravity Fold', 'folds the space between - and is suddenly behind the monster, three fingers already closing', 'behind',
               [P('minecraft:reverse_portal', 30), P('minecraft:portal', 10)], ['minecraft:reverse_portal ^ ^1 ^-1.2 0.2 0.3 0.2 0 2'],
               [P('minecraft:reverse_portal', 40, 0.4, 0.6, 0.2), P('minecraft:crit', 20)], 'minecraft:block.end_portal.spawn', 'minecraft:entity.shulker.shoot'),
    'henry': ('Nine Lives', '', 'behind', [], [], [], 'minecraft:entity.cat.hiss', 'minecraft:entity.cat.hiss'),
    'nia': ('Tortitude', '', 'behind', [], [], [], 'minecraft:entity.cat.hiss', 'minecraft:entity.cat.hiss'),
    'rufus': ('Dirty Fighting', 'throws grit in its eyes', 'behind', [], [], [], 'minecraft:entity.rabbit.attack', 'minecraft:item.crossbow.shoot'),
    'sky': ('Storm Front', 'blow away on the wind and come down on the monster out of a thundercloud', 'above',
            [P('minecraft:cloud', 40, 0.5, 0.8, 0.05)], ['minecraft:cloud ~ ~3.2 ~ 0.6 0.1 0.6 0 4'],
            [P('minecraft:electric_spark', 40, 0.5, 0.8, 0.3), P('minecraft:end_rod', 20, 0.3, 0.6, 0.1)], 'minecraft:entity.breeze.wind_burst', 'minecraft:entity.lightning_bolt.thunder'),
}
TICKS = {'vanish': 1, 'move': 8, 'show': 11, 'end': 15}

# (2.95e) THE ASSAULTS - seen, not vanished. Each: its own animation's hooks, its busy score, the hits (rend, and what else each
# blow does at the foe, as the foe), and a timeline on its own poses ('H<n>': hit n; 'DASH': to the marked foe; 'RIDE a..b': on
# the foe's head those ticks; 'PULL a..b': the foe dragged in those ticks)
STUN = ['effect give @s minecraft:slowness 3 9 true', 'effect give @s minecraft:weakness 3 9 true',
        'particle minecraft:wax_off ~ ~2.1 ~ 0.25 0.05 0.25 0.6 10', 'particle minecraft:crit ~ ~1.8 ~ 0.3 0.1 0.3 0.2 12']
SLASH = lambda c: [f'particle minecraft:dust{{color:[{c}],scale:1.1}} ~ ~1 ~ 0.35 0.4 0.35 0 10', 'particle minecraft:sweep_attack ~ ~1 ~ 0.2 0.1 0.2 0 1']
ASSAULT = {
    'bender': dict(pfx='p195', s_obj='bm.dqs', anim='p195/anim', busy='bm.dqx', end=36, dash=dict(reach=1.4, speed=1.0, lift=2),
                   hits={1: (2, SLASH('0.88,0.66,0.38') + ['particle minecraft:crit ~ ~1.2 ~ 0.3 0.3 0.3 0.3 8'], 'minecraft:entity.player.attack.sweep', 1.6),
                         2: (3, ['particle minecraft:crit ~ ~1.8 ~ 0.25 0.15 0.25 0.4 14', 'effect give @s minecraft:slowness 1 4 true'], 'minecraft:entity.fox.bite', 0.7)},
                   tl={1: ['P maul_a', 'S minecraft:entity.wolf.growl 1 0.8'], 3: ['DASH'],
                       4: ['P maul_a', 'H1'], 6: ['P maul_b', 'H1'], 8: ['P maul_a', 'H1'], 10: ['P maul_b', 'H1'],
                       12: ['P bite_up', 'data merge entity @s {NoGravity:1b}', 'S minecraft:entity.wolf.ambient 1 1.4', 'RIDE 13..25'],
                       15: ['P bite', 'H2'], 18: ['P bite_up'], 21: ['P bite', 'H2'], 23: ['P bite_up'],
                       26: ['data merge entity @s {NoGravity:0b}', 'P jump'], 30: ['P land'], 33: ['P idle_a']}),
    'leo': dict(pfx='p96', s_obj='bm.les', anim='p96/anim', busy='bm.lek', end=28, dash=dict(reach=1.9, speed=1.0, lift=1),
                hits={1: (2, STUN, 'minecraft:item.shield.block', 0.8),
                      2: (4, ['particle minecraft:splash ~ ~1 ~ 0.3 0.4 0.3 0.2 16', 'particle minecraft:enchanted_hit ~ ~1.1 ~ 0.2 0.3 0.2 0.3 10'], 'minecraft:item.trident.hit', 1.1)},
                tl={1: ['P guard', 'S minecraft:item.armor.equip_iron 1 0.9'], 3: ['DASH'],
                    4: ['P guard', 'H1', 'S minecraft:block.anvil.land 0.4 1.4'], 8: ['P thrust_back'], 10: ['P thrust', 'H2'],
                    12: ['P thrust_back'], 14: ['P thrust', 'H2'], 16: ['P thrust_back'], 18: ['P thrust', 'H2'], 25: ['P idle_a']}),
    'bloo': dict(pfx='p191', s_obj='bm.bks', anim='p191/anim', busy='bm.bkx', end=31, dash=dict(reach=1.5, speed=1.1, lift=2),
                 hits={1: (2, SLASH('0.35,0.60,0.91') + ['particle minecraft:crimson_spore ~ ~1 ~ 0.3 0.3 0.3 0 8'], 'minecraft:entity.player.attack.sweep', 1.3),
                       2: (4, ['particle minecraft:crit ~ ~1 ~ 0.5 0.5 0.5 0.4 20'], 'minecraft:entity.ravager.roar', 1.2)},
                 tl={1: ['P crouch', 'S minecraft:entity.fox.sniff 1 0.6'], 4: ['P pounce', 'DASH'], 5: ['H1'],
                     7: ['P swipe_up'], 8: ['P swipe', 'H1'], 10: ['P swipe_up'], 11: ['P swipe', 'H1'], 13: ['P swipe_up'], 14: ['P swipe', 'H1'],
                     16: ['P swipe_up'], 17: ['P swipe', 'H1'], 20: ['P roar', 'H2'], 28: ['P idle_a']}),
    'bones': dict(pfx='p196', s_obj='bm.bzs', anim='p196/anim', busy='bm.bzx', end=26, dash=dict(reach=1.6, speed=1.1, lift=1),
                  hits={1: (5, ['particle minecraft:splash ~ ~1 ~ 0.3 0.3 0.3 0.2 16', 'effect give @s minecraft:slowness 2 9 true'], 'minecraft:entity.guardian.attack', 1.2),
                        2: (3, ['particle minecraft:splash ~ ~0.8 ~ 0.5 0.3 0.5 0.3 20', 'particle minecraft:bubble ~ ~1 ~ 0.3 0.3 0.3 0.1 10'], 'minecraft:entity.dolphin.splash', 0.8)},
                  tl={1: ['P charge', 'S minecraft:entity.dolphin.splash 1 0.7'], 3: ['DASH'], 4: ['P bite_open'], 6: ['P bite', 'H1'],
                      8: ['P thrash_a', 'H2'], 11: ['P thrash_b', 'H2'], 14: ['P thrash_a', 'H2'], 17: ['P thrash_b'], 23: ['P idle_a']}),
    'demo': dict(pfx='p97', s_obj='bm.dms', anim='p97/frame', busy='bm.dmk', end=28, dash=dict(reach=2.2, speed=1.0, lift=2),
                 hits={1: (9, ['particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.3 30', 'particle minecraft:sweep_attack ~ ~1 ~ 0.1 0.4 0.1 0 2'], 'minecraft:entity.lightning_bolt.impact', 1.6),
                       2: (5, ['particle minecraft:sweep_attack ~ ~1 ~ 0.6 0.2 0.6 0 3'], 'minecraft:entity.player.attack.sweep', 0.7)},
                 tl={1: ['P swing_back', 'S minecraft:item.trident.thunder 0.4 1.5'], 4: ['DASH'], 5: ['P overhead'], 10: ['P slam', 'H1'],
                     14: ['P swing_back'], 17: ['P swing', 'H2'], 25: ['P idle_a']}),
    'chef': dict(pfx='p186', s_obj='bm.kqs', anim='p186/anim', busy='bm.kqx', end=27, dash=dict(reach=1.6, speed=1.0, lift=1),
                 hits={1: (3, ['particle minecraft:crit ~ ~1.2 ~ 0.3 0.3 0.3 0.3 10'], 'minecraft:entity.player.attack.strong', 1.3),
                       2: (5, ['particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.05 16', 'particle minecraft:crit ~ ~1.2 ~ 0.4 0.4 0.4 0.4 16'], 'minecraft:block.bell.use', 1.6)},
                 tl={1: ['P whack_up', 'S minecraft:entity.player.attack.knockback 0.6 1.6'], 3: ['DASH'], 4: ['P whack', 'H1'],
                     6: ['P whack_up'], 7: ['P whack', 'H1'], 9: ['P whack_up'], 10: ['P whack', 'H1'],
                     13: ['P throw_back'], 17: ['P throw', 'H2'], 24: ['P idle_a']}),
    'emma': dict(pfx='p57', s_obj='bm.ems', anim='p57/anim', busy='bm.emk', end=27, dash=dict(reach=1.8, speed=1.0, lift=1), own_place=True,
                 hits={1: (14, ['particle minecraft:flash{color:[1.0,0.75,0.9,1.0]} ~ ~0.5 ~ 0 0 0 0 1', 'particle minecraft:explosion ~ ~0.3 ~ 0 0 0 0 1',
                                'particle minecraft:cherry_leaves ~ ~0.5 ~ 1.2 0.2 1.2 0 40', 'particle minecraft:block{block_state:"minecraft:dirt"} ~ ~0.1 ~ 0.8 0.1 0.8 0 30'],
                           'minecraft:entity.generic.explode', 1.3)},
                 tl={1: ['P idle_hop', 'S minecraft:entity.phantom.flap 0.8 1.4'], 2: ['DASH'],
                     3: ['data merge entity @s {NoGravity:1b}', 'S minecraft:entity.player.attack.sweep 1 0.7', 'RISE 3..10'] + [f'P roll_0'],
                     **{3 + i: [f'P roll_{i}', 'particle minecraft:cherry_leaves ~ ~1.2 ~ 0.3 0.3 0.3 0 3'] for i in range(1, 8)},
                     11: ['P slam_up', 'S minecraft:block.amethyst_block.chime 1 0.6'], 13: ['DROP 13..17'],
                     17: ['P slam', 'H1', 'function bm:p226/a/emma/wave', 'data merge entity @s {NoGravity:0b}'], 23: ['P idle_a']}),
    'henry': dict(pfx='p229', s_obj='bm.hqs', anim='p229/anim', busy='bm.hqx', end=30, dash=dict(reach=1.4, speed=1.1, lift=2),
                  hits={1: (4, ['particle minecraft:crit ~ ~0.8 ~ 0.3 0.3 0.3 0.3 12', 'effect give @s minecraft:slowness 2 4 true'], 'minecraft:entity.cat.hiss', 1.4),
                        2: (2, SLASH('0.6,0.6,0.85'), 'minecraft:entity.player.attack.sweep', 1.9)},
                  tl={1: ['P pounce_up', 'S minecraft:entity.cat.hiss 0.8 0.8'], 3: ['P pounce', 'DASH'], 4: ['H1'],
                      7: ['P swipe_up'], 8: ['P swipe', 'H2'], 10: ['P swipe_up'], 11: ['P swipe', 'H2'], 13: ['P swipe_up'], 14: ['P swipe', 'H2'],
                      16: ['P swipe_up'], 17: ['P swipe', 'H2'], 19: ['P swipe_up'], 20: ['P swipe', 'H2'], 26: ['P happy']}),
    'nia': dict(pfx='p230', s_obj='bm.nqs', anim='p230/anim', busy='bm.nqx', end=30, dash=dict(reach=1.4, speed=1.1, lift=1),
                hits={1: (2, STUN, 'minecraft:entity.cat.hiss', 1.0), 2: (3, SLASH('0.88,0.63,0.31'), 'minecraft:entity.player.attack.sweep', 1.8)},
                tl={1: ['P hiss', 'S minecraft:entity.cat.hiss 1 0.9'], 4: ['DASH'], 5: ['P hiss', 'H1'],
                    9: ['P swipe_up'], 10: ['P swipe', 'H2'], 12: ['P swipe_up'], 13: ['P swipe', 'H2'], 15: ['P swipe_up'], 16: ['P swipe', 'H2'],
                    18: ['P swipe_up'], 19: ['P swipe', 'H2'], 26: ['P cuddle']}),
    'rufus': dict(pfx='p228', s_obj='bm.rgs', anim='p228/anim', busy='bm.rgx', end=36, dash=dict(reach=1.5, speed=1.0, lift=1),
                  hits={1: (2, ['effect give @s minecraft:blindness 3 0 true'] + STUN[:2] + ['particle minecraft:falling_dust{block_state:"minecraft:sand"} ~ ~1.6 ~ 0.3 0.2 0.3 0 20'], 'minecraft:entity.rabbit.attack', 0.8),
                        2: (4, SLASH('0.75,0.22,0.17'), 'minecraft:entity.player.attack.sweep', 1.4),
                        3: (4, ['particle minecraft:crit ~ ~1 ~ 0.2 0.3 0.2 0.4 16', 'particle minecraft:poof ~ ~1 ~ 0.2 0.2 0.2 0.05 6'], 'minecraft:item.crossbow.shoot', 0.9)},
                  tl={1: ['P slash_up', 'S minecraft:entity.rabbit.ambient 1 0.6'], 3: ['DASH'],
                      4: ['P slash', 'H1'], 7: ['P slash_up'], 9: ['P slash', 'H2'], 12: ['P slash_up'], 14: ['P slash', 'H2'],
                      18: ['P aim', 'S minecraft:item.crossbow.loading_end 1 1.2'], 23: ['P shoot', 'H3'], 28: ['P reload'], 33: ['P idle_a']}),
    'tul': dict(pfx='p132', s_obj='bm.tus', anim='p132/anim', busy='bm.tux', end=33, dash=None,
                hits={1: (4, ['particle minecraft:snowflake ~ ~1 ~ 0.3 0.4 0.3 0.05 16', 'particle minecraft:enchanted_hit ~ ~1.1 ~ 0.2 0.3 0.2 0.3 8'], 'minecraft:item.trident.hit', 0.9),
                      2: (6, ['particle minecraft:snowflake ~ ~1 ~ 0.5 0.5 0.5 0.3 40', 'particle minecraft:poof ~ ~1 ~ 0.4 0.4 0.4 0.05 16'], 'minecraft:entity.generic.explode', 1.5)},
                tl={1: ['P hook_pull', 'S minecraft:entity.fishing_bobber.throw 1 0.6', 'PULL 3..9'], 5: ['S minecraft:entity.fishing_bobber.retrieve 1 0.6'],
                    10: ['P thrust_back'], 12: ['P thrust', 'H1'], 14: ['P thrust_back'], 16: ['P thrust', 'H1'],
                    20: ['P aim'], 24: ['P blast', 'H2'], 30: ['P idle_a']}),
}
NAMES = {'bender': ('Savage Maul', 'pounces, claws the monster savagely and chomps on its head'),
         'leo': ('Shield Bash', 'stuns the monster with a bash of his shield, then runs it through with his trident, again and again'),
         'bloo': ('Feral Frenzy', 'pounces and tears into the monster in a frenzy of claws, and roars over it'),
         'bones': ('Death Roll', 'clamps his jaws on the monster and rolls it, thrashing'),
         'demo': ("Reaper's Toll", 'brings the scythe down through the monster\'s guard and reaps it on the backswing'),
         'chef': ('Order Up!', 'tenderises the monster with a flurry of whacks, then serves the finisher'),
         'emma': ('Axe Roll', 'leaps into the air, rolls with her axe held overhead, and slams it down on the monster'),
         'henry': ('Nine Lives', 'pounces on the monster and shreds it with a flurry of claws'),
         'nia': ('Tortitude', 'hisses it frozen in its tracks, then shows it all of her claws'),
         'rufus': ('Dirty Fighting', 'throws grit in the monster\'s eyes, slashes it twice and finishes it with the crossbow, point-blank'),
         'tul': ('Hook and Broadside', 'harpoons the monster, drags it in, runs it through and lets the blunderbuss finish it point-blank')}


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
        if w in ASSAULT:
            assault(G, w, typ(w), host, ME[w], col)
            name, desc = NAMES[w]
            G.FUNCS[f'p205/check/{w}'].insert(-2, tellraw('@s', G.PREFIX + [T('...and a piercing blow: ', 'gray'), T(name, '#ff7a7a', bold=True),
                                                                            T(f' - {nm} {desc}, straight through armour.', 'gray')]))
            continue
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
        if w in ASSAULT: continue
        second.append(f'execute as {host(w, "scores={bm.prt=1..},tag=!bm.champ")} at @s run function bm:p226/end')


def assault(G, w, typ, host, me, col):
    """(2.95e) the piercing blow as a choreographed assault on the follower's own poses (atk.sig, kid 3): every 18 s (p226/sec)
    the foe is marked and bm.prgo set; the move starts as soon as the follower is free"""
    import atk
    fn = G.fn
    A = ASSAULT[w]
    pfx = A['pfx']
    if 'bm.prgo' not in G.OBJECTIVES:
        G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.prgo dummy']; G.OBJECTIVES.append('bm.prgo')
    by = f'by @e[type=minecraft:{typ},tag=bm.{me},limit=1]'
    for i, (dmg, fx, snd, pitch) in A['hits'].items():
        fn(f'p226/a/{w}/h{i}', [f'tag @s add bm.{me}', f'execute as @e[tag=bm.prfoe,distance=..4.5,limit=1] at @s run function bm:p226/a/{w}/d{i}',
                                f'tag @s remove bm.{me}', f'playsound {snd} neutral @a[distance=..20] ~ ~ ~ 1 {pitch}'])
        fn(f'p226/a/{w}/d{i}', list(fx) + [f'damage @s {dmg} bm:rend {by}'])
    assert sum(A['hits'][int(c[1:])][0] for t in A['tl'].values() for c in t if c[0] == 'H' and c[1:].isdigit()) == DMG, w
    tl, each = {}, ['scoreboard players operation #pk bm.rng = @s bm.prk', 'tag @e[tag=bm.prfoe] remove bm.prfoe',
                    'execute as @e[tag=bm.prtg,distance=..24] if score @s bm.prk = #pk bm.rng run tag @s add bm.prfoe']
    for t, cmds in A['tl'].items():
        out = []
        for c in cmds:
            if c.startswith('P '): out.append(f'function bm:{pfx}/pose/{c[2:]}')
            elif c.startswith('S '):
                snd, vol, pit = c[2:].split(); out.append(f'playsound {snd} neutral @a[distance=..20] ~ ~ ~ {vol} {pit}')
            elif c == 'DASH': out.append('DASH 8 @e[tag=bm.prfoe,limit=1]')
            elif c[0] == 'H': out.append(f'function bm:p226/a/{w}/h{c[1:]}')
            elif c.startswith('RIDE '):          # (on its head: wherever its eyes are, a little under)
                each.append(f'execute if score @s bm.ksg matches {c[5:]} run function bm:p226/a/ride')
            elif c.startswith('RISE '):          # (up into the air, a step a tick, while there's room)
                each.append(f'execute if score @s bm.ksg matches {c[5:]} if block ~ ~2.2 ~ #bm:grap_pass run tp @s ~ ~0.32 ~')
            elif c.startswith('DROP '):          # (and down on it, fast, to the ground)
                each.append(f'execute if score @s bm.ksg matches {c[5:]} if block ~ ~-0.6 ~ #bm:grap_pass run tp @s ~ ~-0.6 ~')
            elif c.startswith('PULL '):          # (hooked: dragged in toward the follower, a step a tick)
                each.append(f'execute if score @s bm.ksg matches {c[5:]} run function bm:p226/a/pull')
            else: out.append(c)
        tl[t] = out
    tl.setdefault(1, [])
    tl[1] = ['scoreboard players set @s bm.prgo 0',
             f'execute unless entity @e[tag=bm.prfoe,distance=..14] run return run scoreboard players set @s bm.ksg {A["end"] - 1}'] + tl[1]
    tl[A['end'] - 1] = tl.get(A['end'] - 1, []) + ['data merge entity @s {NoGravity:0b}', 'function bm:p226/a/clean']
    atk.sig(G, pfx, kid=3, tick_fn=f'{pfx}/tick', state_fn=f'{pfx}/state', anim_fn=A['anim'], s_obj=A['s_obj'], place_fn=f'{pfx}/place', col=col,
            trigger='execute if score @s bm.prgo matches 1 unless data entity @s {Sitting:1b}', busy=A['busy'], cd=20, end=A['end'],
            dash_kw=A['dash'], timeline=tl, each=each, own_place=A.get('own_place', False))
    if w == 'emma':                          # (the slam's shockwave: what stands round her foe)
        fn('p226/a/emma/wave', [f'tag @s add bm.{me}', f'execute at @e[tag=bm.prfoe,limit=1] as @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.prfoe,distance=..3.5] run damage @s 4 bm:rend {by}',
                                f'tag @s remove bm.{me}', 'execute at @e[tag=bm.prfoe,limit=1] run function bm:p226/a/emma/ring'])
        fn('p226/a/emma/ring', [f'execute rotated {a} 0 positioned ^ ^0.2 ^2 run particle minecraft:cherry_leaves ~ ~ ~ 0.1 0.1 0.1 0 2' for a in range(0, 360, 30)])
    # (each second: a Champion, rested, a monster near, its owner near, not sitting, not ridden) - the foe marked, and go
    fn(f'p226/sec/{w}', ['execute if score @s bm.prcd matches 1.. run return run scoreboard players remove @s bm.prcd 1',
                         'execute if score @s bm.prgo matches 1 run return 0',
                         'execute if data entity @s {Sitting:1b} run return 0',
                         'execute on passengers if entity @s[type=minecraft:player] run return 0',
                         f'execute unless entity {FOE12} run return 0',
                         'scoreboard players operation #me bm.pid = @s bm.pid',
                         'scoreboard players set #o bm.rng 0', 'execute as @a[distance=..32] if score @s bm.pid = #me bm.pid run scoreboard players set #o bm.rng 1',
                         'execute if score #o bm.rng matches 0 run return 0',
                         f'scoreboard players set @s bm.prcd {CD}', 'scoreboard players set @s bm.prgo 1',
                         'scoreboard players add #prk bm.rng 1', 'scoreboard players operation @s bm.prk = #prk bm.rng',
                         f'execute as {FOE12} run function bm:p226/mark'])
    G.FUNCS['loop/second'].append(f'execute as {host(w, "tag=bm.champ")} at @s run function bm:p226/sec/{w}')
    G.FUNCS['loop/second'].append(f'execute as {host(w, "scores={bm.prgo=1},tag=!bm.champ")} run scoreboard players set @s bm.prgo 0')
    if 'p226/a/ride' not in G.FUNCS:
        fn('p226/a/ride', ['tag @s add bm.prride',
                           'execute as @e[tag=bm.prfoe,limit=1] at @s anchored eyes positioned ^ ^ ^ run tp @e[tag=bm.prride,limit=1] ~ ~-0.15 ~',
                           'tag @s remove bm.prride'])
        fn('p226/a/pull', ['tag @s add bm.prride',
                           'execute as @e[tag=bm.prfoe,distance=2.2..14,limit=1] at @s facing entity @e[tag=bm.prride,limit=1] feet run function bm:p226/a/pulled',
                           'tag @s remove bm.prride'])
        fn('p226/a/pulled', ['execute positioned ^ ^ ^0.8 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~',
                             'particle minecraft:snowflake ~ ~1 ~ 0.1 0.1 0.1 0 2'])
        fn('p226/a/clean', ['execute as @e[tag=bm.prtg] if score @s bm.prk = #pk bm.rng run tag @s remove bm.prtg', 'tag @e[tag=bm.prfoe] remove bm.prfoe'])


FOE12 = '@e[type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,distance=..12,sort=nearest,limit=1]'


def rp(R):
    R.LANG.update({'death.attack.bm.rend': '%1$s was struck straight through their armour',
                   'death.attack.bm.rend.player': '%1$s was struck straight through their armour by %2$s'})

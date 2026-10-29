"""2.78: EVERY FOLLOWER DRESSED - and for each of them an AURA, the rarest thing a heist gives.

WARDROBES FOR THE REST: Apophiss (his scales: Obsidian Coil, Blood Wyrm, Frost Serpent; hidden: Gilded Coil), Tullius (his
  coat: Admiral's Blue, Corsair Crimson, Bleached Bone; hidden: Gilded Captain), the Frog with Mustache (his skin: Bluejay,
  Ember Toad, Old Bog; hidden: Golden Prince), Donado (his coat: Chocolate, Midnight, Snowdrift; hidden: Starlit), Pearlman
  (his bow tie and hat band: Ruby, Emerald, Amethyst; hidden: Gilded) and Wilfrey (the shield he bears: Crimson Cross,
  Azure Chevron, Verdant Bend; hidden: Gilded Sun). Sold by the Tailor like every other outfit (the hidden ones dearer),
  used once and theirs for good. Their own menus have a WARDROBE button (Wilfrey's: sneak + use the locket while he rests),
  and every wardrobe is on the Ledger's Outfits page.
  (How: the recoloured follower's models are copies with a "_c<k>" suffix - item definitions and all, faces and poses
  included - and a look is the suffix on whatever model a part is wearing, so poses, faces and the saddle keep working.)
AURAS: thirteen of them, one per follower - a ring of motes circling them and a haze of their own (Emma's blossom, Celi's
  frost, Zib's starfield, Cecil's arcana, KillerWatt's storm, Leo's tide, Democratus' souls, Apophiss's black flame,
  Tullius's drowned gale, the Frog's bog-lights, Donado's tractor beam, Pearlman's gold, Wilfrey's radiance). Hard to come
  by: a won heist of Tier III or above very rarely leaves one in the haul (0.8% / 1.5% / 2.5% for III / IV / V), or the
  Tailor sells them for 1,280 coins apiece. Used once, it's theirs for good; the wardrobe switches it on and off.
"""
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt
import phase28 as P28
import phase99 as P99
import gild
import phase103 as P103

GOLD = '#ffcf40'
ORDER = ['emma', 'celi', 'zib', 'cecil', 'kw', 'leo', 'demo', 'apo', 'tul', 'frog', 'don', 'pearl', 'wil', 'fishy', 'dennis', 'pistachio', 'omega', 'ashur', 'chef', 'neighbor', 'ava', 'pearlq', 'bloo', 'stalker', 'lantern', 'bender', 'bones', 'capshun', 'sky', 'pxemma', 'pxleo', 'pxcecil', 'kettle', 'rufus', 'henry', 'nia', 'gem', 'batty', 'eggbert', 'count', 'dragon', 'eraser', 'cursor', 'inkblot', 'speech', 'lightbringer', 'dryad', 'sovereign', 'vexis', 'mireling']
# follower: (host type, host tag[s]) - the animal underneath, whose owner the aura belongs to
HOST = {'emma': ('cat', 'bm.emmapet'), 'celi': ('wolf', 'bm.celipet'), 'zib': ('wolf', 'bm.zibpet'), 'cecil': ('wolf', 'bm.cecilpet'),
        'kw': ('wolf', 'bm.kxpet'), 'leo': ('wolf', 'bm.leopet'), 'demo': ('wolf', 'bm.dmpet'), 'apo': ('wolf', 'bm.appet'), 'tul': ('wolf', 'bm.tupet'),
        'frog': ('wolf', 'bm.frogpet'), 'don': ('wolf', 'bm.donado'), 'pearl': ('cat', 'bm.pmpet'), 'wil': ('wolf', 'bm.wilfrey'), 'fishy': ('wolf', 'bm.fypet'),
        'dennis': ('wolf', 'bm.dwpet'), 'pistachio': ('wolf', 'bm.pipet'), 'omega': ('wolf', 'bm.ompet'), 'ashur': ('wolf', 'bm.aspet'), 'chef': ('wolf', 'bm.kkpet'), 'neighbor': ('wolf', 'bm.nbpet'),
        'ava': ('wolf', 'bm.avpet'), 'pearlq': ('wolf', 'bm.pqpet'), 'bloo': ('wolf', 'bm.bopet'), 'stalker': ('wolf', 'bm.svpet'), 'lantern': ('wolf', 'bm.lnpet'), 'bender': ('wolf', 'bm.bvpet'), 'bones': ('wolf', 'bm.bjpet'), 'capshun': ('wolf', 'bm.mzpet'), 'kettle': ('wolf', 'bm.ktpet'), 'rufus': ('wolf', 'bm.rupet'), 'henry': ('wolf', 'bm.hypet'), 'nia': ('wolf', 'bm.nipet'), 'gem': ('wolf', 'bm.cgpet'), 'batty': ('wolf', 'bm.ytpet'), 'eggbert': ('wolf', 'bm.ebpet'), 'count': ('wolf', 'bm.knpet'), 'dragon': ('wolf', 'bm.ddpet'), 'eraser': ('wolf', 'bm.ezpet'), 'cursor': ('wolf', 'bm.uxpet'), 'inkblot': ('wolf', 'bm.ibpet'), 'speech': ('wolf', 'bm.wbpet'), 'lightbringer': ('wolf', 'bm.lhpet'), 'dryad': ('wolf', 'bm.pypet'), 'sovereign': ('wolf', 'bm.xvpet'), 'vexis': ('wolf', 'bm.xbpet'), 'mireling': ('wolf', 'bm.mlpet'), 'sky': ('wolf', 'bm.ybpet'),
        'pxemma': ('wolf', 'bm.xmpet'), 'pxleo': ('wolf', 'bm.xlpet'), 'pxcecil': ('wolf', 'bm.xcpet')}
dust = lambda r, g, b, s=1.0: f'minecraft:dust{{color:[{r},{g},{b}],scale:{s}}}'
# follower: (aura name, colour, ring height, ring radius, the ring's mote, the haze [particle commands at the follower])
AURA = {
    'emma': ('Blossom Halo', '#ff8ad8', 1.15, 0.75, dust(1.0, 0.55, 0.85), ['particle minecraft:cherry_leaves ~ ~1.7 ~ 0.4 0.2 0.4 0 1']),
    'celi': ('Moonfrost Veil', '#9ad8ff', 1.15, 0.75, 'minecraft:snowflake', ['particle minecraft:end_rod ~ ~1 ~ 0.35 0.5 0.35 0.005 1',
                                                                             f'particle {dust(0.7, 0.9, 1.0, 0.7)} ~ ~0.6 ~ 0.4 0.4 0.4 0 2']),
    'zib': ('Starfield Static', '#3ad8c8', 1.0, 0.7, 'minecraft:glow', [f'particle {dust(0.23, 0.85, 0.78, 0.7)} ~ ~0.9 ~ 0.4 0.5 0.4 0 2']),
    'cecil': ('Arcane Corona', '#b48cff', 1.0, 0.7, dust(0.7, 0.55, 1.0), ['particle minecraft:enchant ~ ~1.5 ~ 0.4 0.3 0.4 0.6 3']),
    'kw': ('Storm Crown', '#ffe040', 1.7, 0.9, 'minecraft:electric_spark', [f'particle {dust(1.0, 0.88, 0.25, 0.8)} ~ ~1.2 ~ 0.5 0.7 0.5 0 2']),
    'leo': ('Tidal Aegis', '#5ab8e0', 1.4, 0.85, 'minecraft:bubble_pop', [f'particle {dust(0.35, 0.72, 0.88, 0.8)} ~ ~1 ~ 0.45 0.6 0.45 0 2',
                                                                         'particle minecraft:splash ~ ~0.3 ~ 0.4 0 0.4 0 2']),
    'demo': ('Reaper\'s Shroud', '#7ad06a', 1.5, 0.85, 'minecraft:soul', ['particle minecraft:sculk_soul ~ ~0.4 ~ 0.4 0.1 0.4 0.01 1',
                                                                       f'particle {dust(0.48, 0.82, 0.42, 0.8)} ~ ~1.2 ~ 0.45 0.7 0.45 0 2']),
    'apo': ('Black-Flame Mantle', '#3ad06a', 2.4, 2.0, dust(0.05, 0.0, 0.08, 1.8), ['particle minecraft:reverse_portal ~ ~1.8 ~ 1.0 0.9 1.0 0.02 3',
                                                                                    f'particle {dust(0.23, 0.82, 0.42, 1.0)} ~ ~1.6 ~ 1.0 0.9 1.0 0 2']),
    'tul': ('Drowned Gale', '#7ad8ff', 1.4, 0.8, 'minecraft:snowflake', ['particle minecraft:falling_water ~ ~2 ~ 0.4 0.15 0.4 0 1',
                                                                        f'particle {dust(0.55, 0.85, 1.0, 0.8)} ~ ~1 ~ 0.45 0.6 0.45 0 2']),
    'frog': ('Bog-Light Ring', '#6ac850', 0.55, 0.6, dust(0.6, 1.0, 0.3, 0.9), ['particle minecraft:firefly ~ ~0.8 ~ 0.7 0.4 0.7 0 1']),
    'don': ('Tractor Beam', '#e8d29a', 0.7, 0.6, 'minecraft:end_rod', [f'particle {dust(0.5, 1.0, 0.45, 0.8)} ~ ~0.2 ~ 0.25 0.6 0.25 0 2']),
    'pearl': ('Golden Gleam', '#5ac8ff', 0.95, 0.6, 'minecraft:wax_on', [f'particle {dust(1.0, 0.85, 0.3, 0.8)} ~ ~0.8 ~ 0.35 0.4 0.35 0 2']),
    'wil': ('Lordly Radiance', '#f4f4f4', 1.5, 0.85, dust(0.95, 0.95, 1.0, 1.2), ['particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.01 1',
                                                                                  'particle minecraft:white_ash ~ ~2 ~ 0.5 0.3 0.5 0 3']),
    'fishy': ('Bubble Halo', '#ffa040', 1.95, 0.75, 'minecraft:bubble_pop', ['particle minecraft:dripping_water ~ ~2.1 ~ 0.35 0.05 0.35 0 1',
                                                                            f'particle {dust(1.0, 0.62, 0.2, 0.8)} ~ ~1.3 ~ 0.4 0.5 0.4 0 2']),
    'dennis': ('Gold Rush Glimmer', '#e0a040', 1.7, 0.8, 'minecraft:wax_on', ['particle minecraft:item{item:"minecraft:gold_nugget"} ~ ~1.8 ~ 0.35 0.1 0.35 0.02 1',
                                                                             f'particle {dust(1.0, 0.82, 0.25, 0.8)} ~ ~1 ~ 0.4 0.6 0.4 0 2']),
    'pistachio': ('Ectoplasmic Mist', '#7ae890', 1.9, 0.8, 'minecraft:soul', ['particle minecraft:sculk_soul ~ ~0.3 ~ 0.4 0.1 0.4 0.01 1',
                                                                             f'particle {dust(0.48, 0.91, 0.56, 0.9)} ~ ~1.1 ~ 0.45 0.6 0.45 0 2']),
    'omega': ('Court of Souls', '#9fb4ff', 4.6, 2.4, 'minecraft:soul_fire_flame', ['particle minecraft:soul ~ ~3 ~ 1.2 1.6 1.2 0.02 3',
                                                                                f'particle {dust(0.6, 0.75, 1.0, 1.2)} ~ ~2.5 ~ 1.2 1.4 1.2 0 3']),
    'ashur': ('Ashfall Crown', '#ff7a2a', 2.05, 0.7, 'minecraft:flame', ['particle minecraft:lava ~ ~0.4 ~ 0.35 0.1 0.35 0 1',
                                                                       f'particle {dust(1.0, 0.45, 0.1, 0.9)} ~ ~1.1 ~ 0.4 0.6 0.4 0 2',
                                                                       'particle minecraft:white_ash ~ ~2.2 ~ 0.5 0.3 0.5 0 4']),
    'chef': ('Kitchen Steam', '#ffd07a', 1.75, 0.65, 'minecraft:poof', ['particle minecraft:cloud ~ ~1.9 ~ 0.25 0.1 0.25 0.01 1',
                                                                      'particle minecraft:item{item:"minecraft:bread"} ~ ~1.2 ~ 0.4 0.5 0.4 0.02 1',
                                                                      f'particle {dust(1.0, 0.85, 0.5, 0.8)} ~ ~1 ~ 0.4 0.5 0.4 0 2']),
    'neighbor': ('Grand Symphony', '#7ab8ff', 2.0, 0.75, 'minecraft:note', ['particle minecraft:note ~ ~2.4 ~ 0.6 0.3 0.6 1 1',
                                                                          f'particle {dust(0.5, 0.75, 1.0, 0.9)} ~ ~1.2 ~ 0.45 0.6 0.45 0 2',
                                                                          'particle minecraft:end_rod ~ ~1.6 ~ 0.5 0.6 0.5 0.01 1']),
    'ava': ('Crown of the Deep', '#6ad8e8', 2.1, 0.75, 'minecraft:nautilus', ['particle minecraft:nautilus ~ ~2.6 ~ 0.5 0.3 0.5 0.6 2',
                                                                           'particle minecraft:bubble_pop ~ ~1.4 ~ 0.45 0.7 0.45 0.02 2',
                                                                           f'particle {dust(0.4, 0.85, 0.95, 0.9)} ~ ~1.1 ~ 0.45 0.6 0.45 0 2']),
    'pearlq': ('Pearlescent Tide', '#5ae0d8', 2.05, 0.75, 'minecraft:end_rod', ['particle minecraft:end_rod ~ ~2.4 ~ 0.5 0.3 0.5 0.01 1',
                                                                               'particle minecraft:bubble_pop ~ ~1.2 ~ 0.45 0.6 0.45 0.02 2',
                                                                               f'particle {dust(1.0, 0.95, 0.9, 0.9)} ~ ~1.2 ~ 0.45 0.6 0.45 0 2']),
    'bloo': ('Feral Moon', '#5a9ae8', 2.6, 0.95, 'minecraft:crit', ['particle minecraft:cherry_leaves ~ ~2.8 ~ 0.6 0.3 0.6 0.02 2',
                                                                   'particle minecraft:crit ~ ~1.4 ~ 0.6 0.8 0.6 0.05 2',
                                                                   f'particle {dust(0.35, 0.6, 0.95, 1.1)} ~ ~1.6 ~ 0.6 0.8 0.6 0 3']),
    'stalker': ('The Long Night', '#a8ac70', 2.7, 0.9, 'minecraft:sculk_soul', ['particle minecraft:sculk_soul ~ ~2.6 ~ 0.4 0.3 0.4 0.01 1',
                                                                        'particle minecraft:large_smoke ~ ~0.6 ~ 0.4 0.3 0.4 0.01 2',
                                                                        f'particle {dust(0.5, 0.0, 0.06, 1.2)} ~ ~1.4 ~ 0.4 0.9 0.4 0 3']),
    'lantern': ('Hallowfire', '#ff8a2a', 2.4, 1.3, 'minecraft:flame', ['particle minecraft:flame ~ ~2.2 ~ 0.7 0.3 0.7 0.01 2',
                                                                    'particle minecraft:small_flame ~ ~0.4 ~ 0.9 0.2 0.9 0.01 2',
                                                                    f'particle {dust(1.0, 0.45, 0.05, 1.2)} ~ ~1.4 ~ 0.8 0.6 0.8 0 3']),
    'bender': ('Goodest Boy', '#ffd27a', 1.5, 0.8, 'minecraft:heart', ['particle minecraft:heart ~ ~1.6 ~ 0.3 0.2 0.3 0 1',
                                                                        'particle minecraft:happy_villager ~ ~0.4 ~ 0.6 0.2 0.6 0 2',
                                                                        f'particle {dust(1.0, 0.82, 0.4, 1.0)} ~ ~0.9 ~ 0.6 0.5 0.6 0 3']),
    'bones': ('Abyssal Tide', '#4ab8e8', 1.6, 1.2, 'minecraft:nautilus', ['particle minecraft:nautilus ~ ~1.6 ~ 0.6 0.3 0.6 0.4 2',
                                                                        'particle minecraft:bubble_pop ~ ~0.6 ~ 0.8 0.3 0.8 0.01 3',
                                                                        f'particle {dust(0.3, 0.72, 0.92, 1.1)} ~ ~1.0 ~ 0.8 0.5 0.8 0 3']),
    'gem': ('Prismatic Bloom', '#5ae0a0', 1.4, 1.0, 'minecraft:end_rod', [f'particle {dust(1.0, 0.35, 0.6, 1.0)} ~ ~1 ~ 0.5 0.5 0.5 0 2',
                                                                       f'particle {dust(0.35, 0.7, 1.0, 1.0)} ~ ~1 ~ 0.5 0.5 0.5 0 2',
                                                                       f'particle {dust(0.4, 1.0, 0.5, 1.0)} ~ ~1 ~ 0.5 0.5 0.5 0 2']),
    'batty': ('Midnight Flock', '#8a8ad8', 1.3, 0.9, 'minecraft:large_smoke', ['particle minecraft:large_smoke ~ ~1 ~ 0.5 0.3 0.5 0.005 2',
                                                                              f'particle {dust(0.5, 0.45, 0.9, 1.0)} ~ ~1 ~ 0.5 0.4 0.5 0 2']),
    'eggbert': ('Golden Ooze', '#ffd060', 1.4, 0.9, 'minecraft:squid_ink', ['particle minecraft:squid_ink ~ ~0.2 ~ 0.5 0.1 0.5 0.005 2',
                                                                           f'particle {dust(1.0, 0.82, 0.35, 1.0)} ~ ~0.8 ~ 0.5 0.4 0.5 0 2']),
    'count': ('Gentleman\'s Gleam', '#a8c8f0', 1.5, 0.9, 'minecraft:wax_on', ['particle minecraft:wax_on ~ ~1.5 ~ 0.4 0.2 0.4 0 1',
                                                                              f'particle {dust(0.66, 0.78, 0.94, 1.0)} ~ ~1 ~ 0.5 0.4 0.5 0 2',
                                                                              'particle minecraft:item_slime ~ ~0.3 ~ 0.5 0.1 0.5 0.01 1']),
    'dragon': ('Crayon Flame', '#ff8a3a', 1.6, 1.0, 'minecraft:flame', ['particle minecraft:small_flame ~ ~1 ~ 0.4 0.4 0.4 0.01 2',
        f'particle {dust(1.0, 0.45, 0.1, 1.0)} ~ ~1 ~ 0.5 0.5 0.5 0 2',
        f'particle {dust(1.0, 0.85, 0.2, 1.0)} ~ ~1 ~ 0.5 0.5 0.5 0 2']),
    'eraser': ('Pink Snowfall', '#f08aa0', 1.2, 0.9, 'minecraft:cherry_leaves', [f'particle {dust(1.0, 0.62, 0.7, 0.7)} ~ ~1.4 ~ 0.5 0.2 0.5 0 3',
        'particle minecraft:cherry_leaves ~ ~1.2 ~ 0.4 0.2 0.4 0 1']),
    'cursor': ('Pixel Trail', '#cfe8ff', 1.6, 0.9, 'minecraft:electric_spark', ['particle minecraft:electric_spark ~ ~1 ~ 0.4 0.5 0.4 0.02 2',
        f'particle {dust(0.3, 1.0, 0.5, 0.8)} ~ ~1 ~ 0.5 0.5 0.5 0 2',
        f'particle {dust(1.0, 0.3, 0.9, 0.8)} ~ ~1 ~ 0.5 0.5 0.5 0 1']),
    'inkblot': ('Inkwell Swirl', '#7a7aaa', 1.0, 0.9, 'minecraft:squid_ink', ['particle minecraft:squid_ink ~ ~0.4 ~ 0.4 0.1 0.4 0.005 2',
        f'particle {dust(0.3, 0.3, 0.6, 0.9)} ~ ~0.8 ~ 0.5 0.4 0.5 0 2']),
    'speech': ('Sound Effects', '#ffd060', 1.6, 1.0, 'minecraft:note', ['particle minecraft:note ~ ~1.6 ~ 0.5 0.2 0.5 1 1',
        f'particle {dust(1.0, 0.85, 0.2, 1.0)} ~ ~1.2 ~ 0.5 0.4 0.5 0 2',
        f'particle {dust(1.0, 0.2, 0.2, 0.9)} ~ ~1.2 ~ 0.5 0.4 0.5 0 1']),
    'lightbringer': ('Radiant Halo', '#ffe08a', 2.0, 1.2, 'minecraft:end_rod', ['particle minecraft:end_rod ~ ~2 ~ 0.4 0.2 0.4 0.005 2',
        f'particle {dust(1.0, 0.86, 0.42, 1.0)} ~ ~1.2 ~ 0.5 0.6 0.5 0 3',
        f'particle {dust(0.5, 0.4, 1.0, 0.8)} ~ ~1.2 ~ 0.5 0.6 0.5 0 1']),
    'dryad': ('Fairy Ring', '#6aa8f0', 0.6, 1.1, 'minecraft:spore_blossom_air', ['particle minecraft:spore_blossom_air ~ ~0.6 ~ 0.5 0.3 0.5 0 2',
        f'particle {dust(0.4, 0.66, 1.0, 0.8)} ~ ~0.3 ~ 0.6 0.1 0.6 0 2',
        f'particle {dust(1.0, 0.6, 0.25, 0.8)} ~ ~0.3 ~ 0.6 0.1 0.6 0 2']),
    'sovereign': ('Void Embers', '#d0182e', 2.2, 1.2, 'minecraft:sculk_soul', ['particle minecraft:sculk_soul ~ ~1.6 ~ 0.4 0.6 0.4 0.01 2',
        f'particle {dust(0.82, 0.1, 0.18, 1.0)} ~ ~1.2 ~ 0.5 0.8 0.5 0 3',
        'particle minecraft:small_flame ~ ~0.4 ~ 0.4 0.1 0.4 0.005 1']),
    'vexis': ('Starlit Orbit', '#7aff6a', 1.8, 1.1, 'minecraft:end_rod', ['particle minecraft:end_rod ~ ~1.4 ~ 0.5 0.6 0.5 0.01 2',
        f'particle {dust(0.48, 1.0, 0.42, 1.0)} ~ ~1.2 ~ 0.6 0.8 0.6 0 3',
        'particle minecraft:reverse_portal ~ ~0.4 ~ 0.5 0.1 0.5 0.02 2']),
    'mireling': ('Veinlight', '#e0384a', 1.3, 0.9, 'minecraft:squid_ink', ['particle minecraft:squid_ink ~ ~0.2 ~ 0.6 0.05 0.6 0.005 2',
        f'particle {dust(1.0, 0.45, 0.12, 1.0)} ~ ~1 ~ 0.5 0.7 0.5 0 3',
        'particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ~ ~1.4 ~ 0.4 0.3 0.4 0 1']),
    'henry': ('Midnight Prowl', '#6a6aa8', 0.9, 0.7, 'minecraft:squid_ink', ['particle minecraft:squid_ink ~ ~0.3 ~ 0.4 0.1 0.4 0.005 2',
                                                                               f'particle {dust(0.55, 0.55, 0.85, 0.9)} ~ ~0.4 ~ 0.5 0.2 0.5 0 2',
                                                                               'particle minecraft:end_rod ~ ~0.9 ~ 0.4 0.2 0.4 0.002 1']),
    'nia': ('Starlit Whiskers', '#ffd890', 0.9, 0.7, 'minecraft:end_rod', ['particle minecraft:end_rod ~ ~0.6 ~ 0.4 0.3 0.4 0.004 2',
                                                                          f'particle {dust(1.0, 0.85, 0.55, 0.9)} ~ ~0.4 ~ 0.5 0.2 0.5 0 2',
                                                                          f'particle {dust(0.8, 0.7, 1.0, 0.8)} ~ ~0.5 ~ 0.5 0.2 0.5 0 1']),
    'rufus': ('Gold Rush', '#ffcf40', 1.4, 0.9, 'minecraft:wax_on', ['particle minecraft:wax_on ~ ~1.2 ~ 0.4 0.3 0.4 0 2',
                                                                    f'particle {dust(1.0, 0.82, 0.25, 1.1)} ~ ~0.4 ~ 0.6 0.3 0.6 0 3',
                                                                    'particle minecraft:glow ~ ~0.6 ~ 0.5 0.3 0.5 0 1']),
    'kettle': ('Playground Chalk', '#8ad8ff', 2.1, 1.1, 'minecraft:white_ash', ['particle minecraft:white_ash ~ ~0.1 ~ 0.6 0.05 0.6 0 4',
                                                                        f'particle {dust(1.0, 0.55, 0.75, 1.0)} ~ ~0.15 ~ 0.7 0.05 0.7 0 2',
                                                                        f'particle {dust(0.55, 0.85, 1.0, 1.0)} ~ ~0.15 ~ 0.7 0.05 0.7 0 2',
                                                                        f'particle {dust(1.0, 0.95, 0.5, 1.0)} ~ ~0.15 ~ 0.7 0.05 0.7 0 2']),
    'capshun': ('Rainbow Doodles', '#ff60c0', 1.8, 1.0, 'minecraft:wax_on', ['particle minecraft:wax_on ~ ~1.8 ~ 0.4 0.3 0.4 0 2',
                                                                        f'particle {dust(1.0, 0.25, 0.25, 1.1)} ~ ~1.0 ~ 0.6 0.6 0.6 0 2',
                                                                        f'particle {dust(0.25, 0.5, 1.0, 1.1)} ~ ~1.0 ~ 0.6 0.6 0.6 0 2',
                                                                        f'particle {dust(1.0, 0.88, 0.2, 1.1)} ~ ~1.0 ~ 0.6 0.6 0.6 0 2']),
    'sky': ('Starry Sky', '#ffe890', 2.4, 1.4, 'minecraft:end_rod', ['particle minecraft:end_rod ~ ~2.6 ~ 0.6 0.3 0.6 0.01 2', f'particle {dust(1.0, 0.85, 0.3, 1.1)} ~ ~2.0 ~ 0.8 0.5 0.8 0 3', f'particle {dust(0.85, 0.9, 1.0, 1.0)} ~ ~2.2 ~ 0.8 0.5 0.8 0 2', 'particle minecraft:falling_water ~ ~1.6 ~ 0.5 0.1 0.5 0 1']),
    'pxemma': ('Scanlines', '#ff6ac8', 2.0, 1.2, 'minecraft:electric_spark', ['particle minecraft:electric_spark ~ ~1.8 ~ 0.4 0.6 0.4 0.05 2', f'particle {dust(1.0, 1.0, 1.0, 0.6)} ~ ~1.2 ~ 0.5 0.8 0.5 0 3']),
    'pxleo': ('Scanlines', '#4ab0ff', 2.0, 1.2, 'minecraft:electric_spark', ['particle minecraft:electric_spark ~ ~1.8 ~ 0.4 0.6 0.4 0.05 2', f'particle {dust(1.0, 1.0, 1.0, 0.6)} ~ ~1.2 ~ 0.5 0.8 0.5 0 3']),
    'pxcecil': ('Scanlines', '#b070ff', 2.0, 1.2, 'minecraft:electric_spark', ['particle minecraft:electric_spark ~ ~1.8 ~ 0.4 0.6 0.4 0.05 2', f'particle {dust(1.0, 1.0, 1.0, 0.6)} ~ ~1.2 ~ 0.5 0.8 0.5 0 3'])}
assert set(AURA) == set(ORDER) == set(HOST) == set(P99.BASE)
PRICE = 1280                                 # coins at the Tailor (10 Gutter Trophies)
FIND = {3: 20, 4: 40, 5: 60}                 # per mille, a won heist of tier III / IV / V (2.94o: was 8 / 15 / 25)
TL2 = 8100                                   # the Tailor's second block (phase103): 8106 the auras page, 8150-8162 an aura each
AURA_PAGE, AURA_BUY = TL2 + 6, TL2 + 50
acode = lambda i: AURA_BUY + i if i < 14 else (TL2 + 96 + (i - 14) if i < 18 else (8293 + (i - 18) if i < 25 else (8380 + (i - 25) if i < 45 else 8420 + (i - 45))))   # (2.80d: past the fourteenth, 8196 on - 8164 on are outfits; 2.86: past the 18th, 8293 on; 2.88: past the 25th, 8380 on; 2.97: past the 45th, 8420 on)
assert len(ORDER) <= 85

for _w in ORDER:
    _n, _c = AURA[_w][0], AURA[_w][1]
    _who = P99.NAMES[_w][0]
    item(f'cos_aura_{_w}', TOTEM, f'Aura: {_n}', _c,
         [f'A rare aura for {_who} alone - a ring of light,', 'and a haze all their own.', ('Use: it\'s theirs for good.', 'blue'),
          ('Switch it on and off in their wardrobe.', 'gray'), ('A rare heist find (Tier III and up) - or the Tailor\'s dearest stock.', 'dark_gray')],
         model='minecraft:nether_star', glint=True, stack=1, cat='cosmetic', comps=hold('none'))
    HOLD[f'cos_aura_{_w}'] = f'bm:p138/use/{_w}'

# the Tailor: an Auras page (phase103 builds it from these)
P103.EXTRA_MAIN.append(P28.btn([T('Auras', '#e080ff', bold=True), T('  (rare)', 'dark_gray')], AURA_PAGE, width=180))
P103.EXTRA_PAGES.append('auras')
P103.EXTRA_ACT.append(f'execute if score #act bm.pay matches {AURA_PAGE} run return run function bm:p103/tl/auras')
P103.EXTRA_ACT.extend(f'execute if score #act bm.pay matches {acode(i)} run return run function bm:p138/tl/a{i}' for i in range(len(ORDER)))

# ====================================================================== the recolours (resource pack)
RECOL = {'apo': ('apophiss_art', ('apo_scale', 'apo_scale_dk', 'apo_fin', 'apo_belly', 'apo_claw', 'apo_lid')),
         'tul': ('tullius_art', ('tu_coat', 'tu_coat_dk', 'tu_hat')),
         'don': ('phase25', ('don_fur', 'don_ear', 'don_patch', 'don_muzzle')),
         'pearl': ('phase60', ('pm_blue', 'pm_dblue')),
         'fishy': ('fishy_art', ('fy_hat', 'fy_hatband')),
         'dennis': ('dennis_art', ('dw_jacket', 'dw_jacket_dk')), 'pistachio': ('pistachio_art', ('ps_coat', 'ps_coat_dk', 'ps_lapel')),
         'omega': ('omega_art', ('om_body', 'om_body_dk', 'om_fin', 'om_stripe', 'om_claw', 'om_lid')),
         'ashur': ('ashur_art', ('as_magma', 'as_plates', 'as_hem', 'as_rock')),
         'chef': ('chef_art', ('cf_white', 'cf_white_dk', 'cf_jacket')),
         'neighbor': ('neighbor_art', ('nb_white', 'nb_white_dk', 'nb_shirt')),
         'ava': ('ava_art', ('av_navy', 'av_navy_dk', 'av_skirt', 'av_bodice', 'av_navy_g', 'av_navy_dk_g', 'av_skirt_g', 'av_bodice_g')),   # (2.87: '_g' - her ghost's, recoloured as a set of their own)
         'pearlq': ('pearl_art', ('pq_dress', 'pq_dress_top', 'pq_gown', 'pq_gown_top', 'pq_cape')),
         'bloo': ('bloo_art', ('bo_fur', 'bo_fur_dk', 'bo_mane')), 'stalker': ('stalker_art', ('st_skin', 'st_shade', 'st_ribs', 'st_back', 'st_face')), 'lantern': ('lantern_art', ('ln_rind', 'ln_rind_dk', 'ln_rind_top', 'ln_face', 'ln_face_glare', 'ln_face_shut')), 'bender': ('bender_art', ('bd_fur', 'bd_back', 'bd_fur_lt', 'bd_face', 'bd_face_happy', 'bd_face_blink', 'bd_face_alert')), 'bones': ('bones_art', ('bn_skin', 'bn_skin_dk', 'bn_flank', 'bn_side')), 'capshun': ('capshun_art', ('mz_ink',)), 'kettle': ('kettle_art', ('kt_ink',)), 'rufus': ('rufus_art', ('rf_red',)), 'henry': ('henry_art', ('hy_collar',)), 'nia': ('nia_art', ('ni_collar',)), 'gem': ('gem_art', ('cg_table', 'cg_crown', 'cg_pav')), 'batty': ('batty_art', ('gb_fur', 'gb_fur_dk', 'gb_fur_lt')), 'eggbert': ('eggbert_art', ('ge_goo',)), 'count': ('count_art', ('gc_band', 'gc_hat')), 'dragon': ('doodle_dragon_art', ('dd_body', 'dd_body_b', 'dd_head_b', 'dd_arm', 'dd_leg', 'dd_tail', 'dd_face', 'dd_face_blink', 'dd_face_dizzy', 'dd_face_fierce', 'dd_face_happy', 'dd_face_puff', 'dd_face_roar', 'dd_face_sad', 'dd_face_surprised')), 'eraser': ('eraser_art', ('er_slab', 'er_back', 'er_limb', 'er_under', 'er_rub', 'er_face', 'er_face_blink', 'er_face_focus', 'er_face_happy', 'er_face_sad', 'er_face_scared', 'er_face_wince')), 'cursor': ('cursor_art', ('cu_arrow', 'cu_arrow_blink', 'cu_arrow_determined', 'cu_arrow_glitch', 'cu_arrow_happy', 'cu_arrow_hurt', 'cu_arrow_surprised', 'cu_hand', 'cu_hand_blink', 'cu_hand_determined', 'cu_hand_glitch', 'cu_hand_happy', 'cu_hand_hurt', 'cu_hand_surprised', 'cu_ibeam', 'cu_ibeam_blink', 'cu_ibeam_determined', 'cu_ibeam_glitch', 'cu_ibeam_happy', 'cu_ibeam_hurt', 'cu_ibeam_surprised', 'cu_move', 'cu_move_blink', 'cu_move_determined', 'cu_move_glitch', 'cu_move_happy', 'cu_move_hurt', 'cu_move_surprised', 'cu_wait', 'cu_wait_blink', 'cu_wait_determined', 'cu_wait_glitch', 'cu_wait_happy', 'cu_wait_hurt', 'cu_wait_surprised', 'cu_wait_turn', 'cu_wait_turn_blink', 'cu_wait_turn_determined', 'cu_wait_turn_glitch', 'cu_wait_turn_happy', 'cu_wait_turn_hurt', 'cu_wait_turn_surprised')), 'inkblot': ('ink_blot_art', ('ib_ink', 'ib_ball', 'ib_puddle', 'ib_body_blot', 'ib_body_fist', 'ib_body_puddle', 'ib_body_question', 'ib_body_quill', 'ib_body_shield')), 'speech': ('speech_bubble_art', ('sbb_bub_puff', 'sbb_bub_shout', 'sbb_bub_speech', 'sbb_bub_thought', 'sbb_tail_puff', 'sbb_tail_shout', 'sbb_tail_speech', 'sbb_tail_thought')), 'lightbringer': ('lightbringer_art', ('lb_robe', 'lb_bodice')), 'dryad': ('pale_dryad_art', ('pd_cap', 'pd_cap_lit')), 'sovereign': ('dread_sovereign_art', ('ds_plate',)), 'vexis': ('vexis_art', ('vx_mantle',)), 'mireling': ('mireling_art', ('ml_hide', 'ml_rib', 'ml_fold', 'ml_pool', 'ml_drip', 'ml_spine', 'ml_lid', 'ml_glow', 'ml_hot', 'ml_barb')), 'sky': ('sky_art', ('yb_cap',)),
         'pxemma': ('phase213', ()), 'pxleo': ('phase213', ()), 'pxcecil': ('phase213', ())}   # (2.94: the 8-bit trio - every frame; phase213 fills the names in)
# (2.82c) his fingers and eyelids took no outfit's colour: they go through the palette too, on the main set's brightness range
# (so the scales come out as before, and the dark claws stay darker than the scales)
SIDE = {'apo_claw', 'apo_lid', 'om_claw', 'om_lid'}
SIDE |= {'ml_glow', 'ml_hot', 'ml_barb'}           # (3.00: the Mireling's veins - mireling_art.LOOK_SIDE: a look's light colour IS its vein colour)
FROG_SKIN = {1: ('light_blue_wool', 'blue_wool'), 2: ('orange_wool', 'red_wool'), 3: ('brown_wool', 'brown_terracotta'), 4: ('yellow_wool', 'yellow_terracotta')}
import shiny as _SH
FROG_SKIN[_SH.KEY['frog']] = _SH.FROG_SKIN                  # (2.94t: his shiny skin)
ITEMS_OF = {'apo': lambda n: n.startswith('apo_'), 'tul': lambda n: n.startswith('tu_'), 'frog': lambda n: n == 'frog',
            'don': lambda n: n == 'donado' or (n.startswith('dnr_') and not n.startswith('dnr_eyes')), 'pearl': lambda n: n == 'pearlman', 'fishy': lambda n: n.startswith('fy_') and n != 'fy_bowl',
            'dennis': lambda n: n.startswith('dw_') and n != 'dw_horn', 'pistachio': lambda n: n.startswith('ps_'), 'omega': lambda n: n.startswith('om_') and n not in ('om_monocle', 'om_banner', 'om_brazier'),
            'ashur': lambda n: n.startswith('as_'), 'chef': lambda n: n.startswith('cf_'), 'neighbor': lambda n: n.startswith('nb_'),
            'ava': lambda n: n.startswith('av_') and n != 'av_locket', 'pearlq': lambda n: n.startswith('pq_') and n != 'pq_pearls', 'bloo': lambda n: n.startswith('bo_') and n != 'bo_claw', 'stalker': lambda n: n.startswith('st_') and n != 'st_hook', 'lantern': lambda n: n.startswith('ln_') and n != 'ln_gourd', 'bender': lambda n: n.startswith('bd_'), 'bones': lambda n: n.startswith('bn_') and n != 'bn_whistle', 'capshun': lambda n: n.startswith('mz_'), 'kettle': lambda n: n.startswith('kt_'), 'rufus': lambda n: n.startswith('rf_'), 'henry': lambda n: n.startswith('hy_'), 'nia': lambda n: n.startswith('ni_'), 'gem': lambda n: n.startswith('cg_'), 'batty': lambda n: n.startswith('gb_'), 'eggbert': lambda n: n.startswith('ge_'), 'count': lambda n: n.startswith('gc_'), 'dragon': lambda n: n.startswith('dd_'), 'eraser': lambda n: n.startswith('er_'), 'cursor': lambda n: n.startswith('cu_'), 'inkblot': lambda n: n.startswith('ib_'), 'speech': lambda n: n.startswith('sbb_'), 'lightbringer': lambda n: n.startswith('lb_'), 'dryad': lambda n: n.startswith('pd_'), 'sovereign': lambda n: n.startswith('ds_'), 'vexis': lambda n: n.startswith('vx_'), 'mireling': lambda n: n.startswith('ml_'), 'sky': lambda n: n.startswith('yb_'),
            'pxemma': lambda n: n.startswith('xm_'), 'pxleo': lambda n: n.startswith('xl_'), 'pxcecil': lambda n: n.startswith('xc_')}


def textures():
    import importlib
    out = {}
    import gild
    for w, (mod, keys) in RECOL.items():
        base = importlib.import_module(mod).textures()
        for k, (_n, pal) in P99.NEW[w][3].items():
            if gild.is_gilded(w, k):
                ims = {n: gild.dress(w, k, base[n]) for n in keys}                                    # (2.79a: polished gold)
            else:
                main = {n: base[n] for n in keys if n not in SIDE and not n.endswith('_g')}
                ims = P99._recolour(main, pal)
                ghost = {n: base[n] for n in keys if n.endswith('_g')}
                if ghost: ims.update(P99._recolour(ghost, pal))
                side = {n: base[n] for n in keys if n in SIDE}
                if side: ims.update(P99._recolour(side, pal, rng=P99._lumrange(main)))
            for name, im in ims.items():
                out[f'{name}_c{k}'] = im
    # (2.79a: the Golden Prince's skin - his wool, light and dark, in polished gold rather than yellow wool)
    import random
    from PIL import Image
    rng = random.Random(4096)
    # (2.80c: and his diamond and netherite skins, the same wool through their metal)
    for nm, lo, hi, k in [(f'frog_{t}_{s}', lo, hi, gild.TIERS[t]['looks']['frog'][0]) for t in gild.TIERS for s, lo, hi in (('lt', 150, 210), ('dk', 80, 140))]:
        im = Image.new('RGBA', (16, 16))
        for y in range(16):
            for x in range(16):
                v = rng.randint(lo, hi) - (18 if (x + y * 3) % 5 == 0 else 0)          # (a wool's weave)
                im.putpixel((x, y), (v, v, v, 255))
        g = gild.dress('frog', k, im, sheen=0)
        if nm.endswith('_dk'):
            g = Image.eval(g.convert('RGB'), lambda c: int(c * 0.72)).convert('RGBA')
        out[nm] = g
    return out


def texmap(w, k):
    if w == 'frog' and gild.is_gilded(w, k):                                                                             # (2.79a; 2.80c)
        t = gild.tier(w, k)
        return {'minecraft:block/lime_wool': f'bm:block/frog_{t}_lt', 'minecraft:block/green_wool': f'bm:block/frog_{t}_dk'}
    if w == 'frog':
        lt, dk = FROG_SKIN[k]
        return {'minecraft:block/lime_wool': f'minecraft:block/{lt}', 'minecraft:block/green_wool': f'minecraft:block/{dk}'}
    return {f'bm:block/{n}': f'bm:block/{n}_c{k}' for n in RECOL[w][1]}


def rp(R):
    import sys, os, re, json, copy
    R.TEXTURE_MODS.append(sys.modules[__name__])

    def post(R2):
        idir = R2.p('assets', 'bm', 'items')
        mdir = R2.p('assets', 'bm', 'models', 'item')
        names = sorted(f[:-5] for f in os.listdir(idir) if f.endswith('.json') and not re.search(r'_c\d$', f[:-5]))
        for w in ITEMS_OF:
            mine = [n for n in names if ITEMS_OF[w](n)]
            assert mine, w
            for k in P99.NEW[w][3]:
                tm, done = texmap(w, k), {}

                def model(mn):                       # a model with any of the textures: its copy, recoloured
                    if mn in done:
                        return done[mn]
                    src = os.path.join(mdir, mn + '.json')
                    m = json.load(open(src)) if os.path.exists(src) else {}
                    tex = m.get('textures', {})
                    if any(v in tm for v in tex.values()):
                        m2 = copy.deepcopy(m)
                        m2['textures'] = {a: tm.get(v, v) for a, v in tex.items()}
                        R2.wj(f'assets/bm/models/item/{mn}_c{k}.json', m2)
                        done[mn] = f'{mn}_c{k}'
                    else:
                        done[mn] = mn
                    return done[mn]

                def walk(o):
                    if isinstance(o, dict):
                        o = {a: walk(v) for a, v in o.items()}
                        if o.get('type') == 'minecraft:model' and str(o.get('model', '')).startswith('bm:item/'):
                            o['model'] = 'bm:item/' + model(o['model'][len('bm:item/'):])
                        return o
                    return [walk(v) for v in o] if isinstance(o, list) else o
                hit = 0
                for n in mine:
                    d = walk(json.load(open(os.path.join(idir, n + '.json'))))
                    R2.wj(f'assets/bm/items/{n}_c{k}.json', d)
                    hit += sum(1 for v in done.values() if v.endswith(f'_c{k}'))
                assert hit, (w, k, 'no model of theirs wears the recoloured textures')
    R.POST.append(post)


def generate(G):
    fn, title, tellraw, PREFIX = G.fn, G.title, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = PREFIX
    fast = []

    # ================================================================== a look on a part: the "_c<k>" suffix on whatever model it wears (as the display; #wk)
    KMAX = max(k for w in ITEMS_OF for k in P99.NEW[w][3])
    strip = [f'execute if data storage bm:wd {{t:"_c{k}"}} run data modify storage bm:wd m set string storage bm:wd m 0 -3' for k in range(1, KMAX + 1)]   # (5: Donado's Gilded; 2.80c: up to 7, his Netherite)
    fn('p138/sfx', ['data modify storage bm:wd m set from entity @s item.components."minecraft:item_model"',
                    'data modify storage bm:wd t set string storage bm:wd m -3'] + strip +
       [f'execute unless score #wk bm.rng matches 1..{KMAX} run return run data modify entity @s item.components."minecraft:item_model" set from storage bm:wd m',
        'execute store result storage bm:wd k int 1 run scoreboard players get #wk bm.rng', 'function bm:p138/sfx2 with storage bm:wd'])
    fn('p138/sfx2', ['$data modify entity @s item.components."minecraft:item_model" set value "$(m)_c$(k)"'])
    # #wk: the look the follower's owner picked (as the owner, or as the follower/one of its parts with an owner)
    for w in ('apo', 'tul', 'frog', 'don', 'pearl'):
        cos = P99.COS[w]
        fn(f'p138/k/{w}', ['scoreboard players set #wk bm.rng 0',
                           f'execute if entity @s[type=minecraft:player] run scoreboard players operation #wk bm.rng = @s {cos}',
                           f'execute unless entity @s[type=minecraft:player] on owner run scoreboard players operation #wk bm.rng = @s {cos}'])

    def now(w, find, dress, msg):
        """(as you, the look just picked) the follower out, dressed now - or next time"""
        fn(f'p99/{w}_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                            f'scoreboard players operation #wk bm.rng = @s {P99.COS[w]}'] + find + [
            f'execute if score #has bm.rng matches 0 run return run ' + say(f'{msg} isn\'t with you - he\'ll wear it next time.', P99.NAMES[w][1])])
        fn(f'p138/{w}/now2', ['scoreboard players set #has bm.rng 1'] + dress + ['particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.02 14'])

    # ---- Apophiss: every part of his rig (the saddle and his faces keep working - they ride on the suffix)
    fn('p138/apo/dress', ['function bm:p138/k/apo', 'execute as @e[type=minecraft:item_display,tag=bm.apsel] run function bm:p138/sfx'])
    G.FUNCS['p131/grow'].append('function bm:p138/apo/dress')
    G.FUNCS['p131/saddle_look'].append('function bm:p138/apo/dress')
    now('apo', ['execute as @e[type=minecraft:wolf,tag=bm.appet] if score @s bm.pid = #me bm.pid at @s run function bm:p138/apo/now2'],
        ['execute as @e[type=minecraft:item_display,tag=bm.app_pet,tag=!bm.apfade] if score @s bm.pid = #me bm.pid run function bm:p138/sfx'], 'Apophiss')
    # ---- Tullius: his rig; every pose puts his arm's own model back (the iced harpoon), so the look goes back on after it
    fn('p138/tul/dress', ['function bm:p138/k/tul', 'execute as @e[type=minecraft:item_display,tag=bm.tusel] run function bm:p138/sfx'])
    fn('p138/tul/arm', ['function bm:p138/k/tul', 'execute as @e[type=minecraft:item_display,tag=bm.tusel,tag=bm.tup_armr] run function bm:p138/sfx'])
    G.FUNCS['p132/grow'].append('function bm:p138/tul/dress')
    poses = [n for n in G.FUNCS if n.startswith('p132/pose/')]
    assert len(poses) >= 10, poses
    for n in poses:
        if any('item:{id:"minecraft:paper"' in l and 'tup_armr' in l for l in G.FUNCS[n]):
            G.FUNCS[n].append('function bm:p138/tul/arm')
    now('tul', ['execute as @e[type=minecraft:wolf,tag=bm.tupet] if score @s bm.pid = #me bm.pid at @s run function bm:p138/tul/now2'],
        ['execute as @e[type=minecraft:item_display,tag=bm.tup_pet] if score @s bm.pid = #me bm.pid run function bm:p138/sfx'], 'Tullius')
    # ---- the Frog and Donado: the flip-book body riding the wolf (its pose and helm stay in its custom_model_data)
    # (2.79a: Donado in the overworld wears his rig - every part of it but his eyes takes the look, as the old body did)
    for w, host, bodies, refresh, nm in (('frog', 'bm.frogpet,tag=!bm.fvault,tag=!bm.ffpet', ['bm.fp_body'], 'p20/frog/refresh', 'The Frog'),
                                         ('don', 'bm.donado,tag=!bm.ffpet', ['bm.dn_body', 'bm.dnr,tag=!bm.dnr_eyes'], 'p25/don/refresh', 'Donado')):
        on = [f'execute on passengers if entity @s[tag={b}] run function bm:p138/sfx' for b in bodies]
        fn(f'p138/{w}/dress', [f'function bm:p138/k/{w}'] + on)
        G.FUNCS[refresh].append(f'function bm:p138/{w}/dress')
        now(w, [f'execute as @e[type=minecraft:wolf,tag={host}] if score @s bm.pid = #me bm.pid at @s run function bm:p138/{w}/now2'], on, nm)
    # (the old-body check used to take any model but "bm:frog" for a stale one)
    sec = G.FUNCS['loop/second']
    k = next(i for i, l in enumerate(sec) if 'tag=bm.fp_body] unless items entity @s contents *[minecraft:item_model="bm:frog"]' in l)
    sec[k] = sec[k].replace('unless items entity @s contents *[minecraft:item_model="bm:frog"]',
                            ' '.join(['unless items entity @s contents *[minecraft:item_model="bm:frog"]'] +
                                     [f'unless items entity @s contents *[minecraft:item_model="bm:frog_c{c}"]' for c in P99.NEW['frog'][3]]))
    # ---- Pearlman: his one model, wherever his cat is (a new one too, when it was lost)
    fn('p138/pearl/dress', ['function bm:p138/k/pearl', 'execute as @e[type=minecraft:item_display,tag=bm.pmd] if score @s bm.pid = #me bm.pid run function bm:p138/sfx'])
    G.FUNCS['p128/pm/tick'].append('execute if score #ok bm.rng matches 0 run function bm:p138/pearl/dress')
    G.FUNCS['p128/pm/summon_here'] += ['scoreboard players operation #me bm.pid = @s bm.pid',
                                       'execute as @e[type=minecraft:cat,tag=bm.pmpet] if score @s bm.pid = #me bm.pid run function bm:p138/pearl/dress']
    now('pearl', ['execute as @e[type=minecraft:cat,tag=bm.pmpet] if score @s bm.pid = #me bm.pid at @s run function bm:p138/pearl/now2'],
        ['execute as @e[type=minecraft:item_display,tag=bm.pmd] if score @s bm.pid = #me bm.pid run function bm:p138/sfx'], 'Pearlman')
    # ---- Wilfrey: a heraldic shield in his free hand (his real gear is untouched)
    SHIELD = {1: ('red', [('straight_cross', 'white'), ('border', 'yellow')]), 2: ('blue', [('triangle_bottom', 'white'), ('border', 'light_gray')]),
              3: ('green', [('stripe_downright', 'yellow'), ('border', 'yellow')]), 4: ('yellow', [('circle', 'orange'), ('border', 'orange')]),
              5: ('cyan', [('circle', 'light_blue'), ('border', 'white')]), 6: ('black', [('circle', 'gray'), ('border', 'brown')])}      # (5, 6: 2.80c)
    import shiny as _SH2
    SHIELD[_SH2.KEY['wil']] = _SH2.WIL_SHIELD                # (2.94t: his shiny heraldry)
    sh = lambda base, pats: 'minecraft:shield[minecraft:base_color="%s",minecraft:banner_patterns=[%s]]' % (
        base, ','.join(f'{{pattern:"minecraft:{p}",color:"{c}"}}' for p, c in pats))
    import gild
    fn('p138/wil/shield', [f'execute unless score #wk bm.rng matches 1..{max(SHIELD)} run item replace entity @s weapon.offhand with minecraft:air'] +
       [f'execute if score #wk bm.rng matches {k} run item replace entity @s weapon.offhand with {sh(*SHIELD[k])}' for k in SHIELD if not gild.is_gilded('wil', k)] +
       # (2.79a: the Gilded Sun shines - and 2.80c the Diamond and Netherite Suns)
       [f'execute if score #wk bm.rng matches {k} run item replace entity @s weapon.offhand with {sh(*SHIELD[k])[:-1]},minecraft:enchantment_glint_override=true]'
        for k in SHIELD if gild.is_gilded('wil', k)])
    G.FUNCS['p2/wil/dress'] += ['scoreboard players set #wk bm.rng 0',
                                f'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #wk bm.rng = @s {P99.COS["wil"]}',
                                'function bm:p138/wil/shield']
    now('wil', ['execute as @e[type=minecraft:wither_skeleton,tag=bm.wil_body] if score @s bm.pid = #me bm.pid at @s run function bm:p138/wil/now2'],
        ['function bm:p138/wil/shield'], 'Wilfrey')
    # sneak + use the locket while he rests: his wardrobe
    L = G.FUNCS['p2/wil/locket']
    k = next(i for i, l in enumerate(L) if l.endswith('unless predicate bm:p20/sneaking run function bm:p2/wil/try_summon'))
    L.insert(k + 1, 'execute unless entity @e[type=minecraft:wolf,tag=bm.fsel] if predicate bm:p20/sneaking run function bm:p119/plain/wil')

    # ---- "Send him home" from a wardrobe (as you; #me is you)
    for w, host, seltag, home in (('frog', 'wolf,tag=bm.frogpet,tag=!bm.fvault,tag=!bm.ffpet', 'bm.fgsel', 'p136/fg/home'),
                                  ('don', 'wolf,tag=bm.donado,tag=!bm.ffpet', 'bm.dnsel', 'p136/dn/home'),
                                  ('pearl', 'cat,tag=bm.pmpet', 'bm.pmsel2', 'p128/pm/dismiss')):
        assert home in G.FUNCS, home
        fn(f'p138/home/{w}', [f'execute as @e[type=minecraft:{host}] if score @s bm.pid = #me bm.pid run tag @s add {seltag}',
                              f'execute if entity @e[tag={seltag}] run function bm:{home}', f'tag @e[tag={seltag}] remove {seltag}'])
    fn('p138/home/wil', ['tag @s add bm.giver', 'execute as @e[type=minecraft:wolf,tag=bm.wilfrey] if score @s bm.pid = #me bm.pid run tag @s add bm.fsel',
                         'execute if entity @e[type=minecraft:wolf,tag=bm.fsel] run function bm:p2/wil/dismiss',
                         'tag @e[tag=bm.fsel] remove bm.fsel', 'tag @e[tag=bm.fbag] remove bm.fbag', 'tag @s remove bm.giver'])

    # ================================================================== THE AURAS
    # ownership: tag bm.auown_<w>; switched on: tag bm.au_<w> (both on the player, for good)
    for i, w in enumerate(ORDER):
        an, ac, h, r, mote, haze = AURA[w]
        who = P99.NAMES[w][0]
        Who = who[0].upper() + who[1:]
        fn(f'p138/au/grant_{w}', [f'tag @s add bm.auown_{w}', f'tag @s add bm.au_{w}',
                                  tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' awakened ', 'gray'), T(an, ac, bold=True),
                                                     T(f' - {who}\'s aura, theirs for good.', 'gray')]),
                                  'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.2',
                                  'particle minecraft:totem_of_undying ~ ~1 ~ 0.5 1 0.5 0.3 40'])
        fn(f'p138/use/{w}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                             f'execute if entity @s[tag=bm.auown_{w}] run return run ' + say(f'{Who} already has {an}. (Switch it on and off in the wardrobe.)', ac),
                             f'clear @s *[minecraft:custom_data~{{bm:"cos_aura_{w}"}}] 1', f'function bm:p138/au/grant_{w}'])
        fn(f'p138/au/t_{w}', [f'execute unless entity @s[tag=bm.auown_{w}] run return run function bm:p138/au/locked_{w}',
                              f'execute if entity @s[tag=bm.au_{w}] run tag @s add bm.au0', f'tag @s add bm.au_{w}',
                              f'execute if entity @s[tag=bm.au0] run tag @s remove bm.au_{w}', 'tag @s remove bm.au0',
                              'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.2', f'function bm:p99/menu/{w}'])
        fn(f'p138/au/locked_{w}', [tellraw('@s', P + [T(an, ac, bold=True), T(' is locked - a rare find in a won heist (Tier III and up), or the Tailor sells it for ', 'gray'),
                                                      T(f'{PRICE} coins', GOLD), T('.', 'gray')]), f'function bm:p99/menu/{w}'])
        # the ring: two motes opposite each other, a third counter-turning lower down; then the haze
        ring = []
        for t in range(16):
            import math
            a, b = 2 * math.pi * t / 16, -2 * math.pi * t / 16
            pts = [(r * math.cos(a), h, r * math.sin(a)), (-r * math.cos(a), h, -r * math.sin(a)), (0.8 * r * math.cos(b), h * 0.45, 0.8 * r * math.sin(b))]
            ring += [f'execute if score #aut bm.rng matches {t} run particle {mote} ~{x:.2f} ~{y:.2f} ~{z:.2f} 0 0 0 0 1' for x, y, z in pts]
        fn(f'p138/au/fx_{w}', ring + haze)
        fn(f'p138/au/on_{w}', [f'execute on owner if entity @s[tag=bm.au_{w}] run return 1', 'return 0'])
        typ, tag = HOST[w]
        fast.append(f'execute as @e[type=minecraft:{typ},tag={tag},tag=!bm.ffpet] if function bm:p138/au/on_{w} at @s run function bm:p138/au/fx_{w}')
    fast.insert(0, 'scoreboard players add #aut bm.rng 1')
    fast.insert(1, 'execute if score #aut bm.rng matches 16.. run scoreboard players set #aut bm.rng 0')
    G.FUNCS['loop/fast'][-1:-1] = fast

    # ---- a won heist, Tier III and up: now and then one in the haul
    HA, HB = '-200 64 -197', '-198 64 -197'          # (the haul's two barrels - as phase105)
    G.FUNCS['p105/finds'] += ['execute store result score #r bm.rng run random value 1..1000'] + \
        [f'execute if score #gt bm.rng matches {t} if score #r bm.rng matches ..{c} run function bm:p138/find' for t, c in FIND.items()]
    fn('p138/find', [f'execute store result score #af bm.rng run random value 0..{len(ORDER) - 1}'] +
       [f'execute if score #af bm.rng matches {i} run return run function bm:p138/find_{w}' for i, w in enumerate(ORDER)])
    for w in ORDER:
        an, ac = AURA[w][0], AURA[w][1]
        fn(f'p138/find_{w}', [f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot bm:items/cos_aura_{w}',
                              f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot bm:items/cos_aura_{w}',
                              tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' found an aura - ', 'gray'), T(an, ac, bold=True),
                                                 T(f' ({P99.NAMES[w][0]}\'s) - in a won heist!', 'gray')]),
                              'playsound minecraft:ui.toast.challenge_complete player @a ~ ~ ~ 0.7 0.9',
                              'execute at @s run particle minecraft:end_rod ~ ~1 ~ 0.6 1 0.6 0.1 60'])

    # ---- the Tailor's Auras page (the wallet, spend, note and poor are phase103's)
    TL = 7740
    pg = f'scoreboard players set #tlp bm.rng {len(P99.BASE) + 1}'          # (its place in p103/tl/reopen: after every follower's page and the cases)
    wal = [T('You have ', 'gray'), T('$(w)', GOLD, bold=True), T(' coins to spend', 'gray'), T(' (Gutter Bank and pockets; Medallions count 16, Trophies 128).', 'dark_gray')]
    dlg = P28.multi([T('AURAS', '#e080ff', bold=True), T('  ·  the Tailor', 'gray')],
                    [P28.body([T('The rarest thing I sell: a follower\'s own aura - a ring of light and a haze all theirs. ', 'gray'),
                               T('Yours for good; switch it on and off in their wardrobe.', 'dark_gray')], 360), P28.body(wal, 360)], [],
                    columns=2, exit_label='Close')
    # (2.82c) only the auras of followers you've met (their names in the buttons; the macro fills r_a<i> in place)
    dlg['actions'] = '@@RAW:acts@@'
    abtn = lambda i, w, tag: snbt(P28.btn([T(AURA[w][0], AURA[w][1], bold=True), T(f' ({P99.NAMES[w][0] if w != "frog" else "the Frog"})  ', 'gray'), tag],
                                          acode(i), width=200))
    rows = ['data modify storage bm:ui tl.acts set value []'] + \
        [l for i, w in enumerate(ORDER) for l in (
            f'execute if {P103.tl_met(w)} unless entity @s[tag=bm.auown_{w}] run data modify storage bm:ui tl.acts append value ' + abtn(i, w, T(f'{PRICE} coins', GOLD)),
            f'execute if {P103.tl_met(w)} if entity @s[tag=bm.auown_{w}] run data modify storage bm:ui tl.acts append value ' + abtn(i, w, T('OWNED', '#7aff7a', bold=True)))] + \
        ['data modify storage bm:ui tl.acts append value ' + snbt(P28.btn([T('« The Tailor', 'gray')], TL, width=200))]
    fn('p103/tl/auras', ['function bm:p103/wallet', f'scoreboard players set @s bm.menu {TL}'] + rows + ['function bm:p103/tl/auras_dlg with storage bm:ui tl'])
    fn('p103/tl/auras_dlg', [f'$dialog show @s {P28.inline(dlg)}'])
    for i, w in enumerate(ORDER):
        an = AURA[w][0]
        fn(f'p138/tl/a{i}', [f'execute unless score @s bm.menu matches {TL} run return run function bm:p28/stale', pg,
                             f'execute if entity @s[tag=bm.auown_{w}] run return run function bm:p103/tl/note {{t:"{P99.NAMES[w][0]} has {an} already."}}',
                             f'execute if items entity @s container.* *[minecraft:custom_data~{{bm:"cos_aura_{w}"}}] run return run function bm:p103/tl/note '
                             f'{{t:"You have that one - use it to give it to {P99.NAMES[w][0]}."}}',
                             'function bm:p103/wallet', f'execute if score #tw bm.rng matches ..{PRICE - 1} run return run function bm:p103/tl/poor {{n:{PRICE}}}',
                             f'scoreboard players set #need bm.rng {PRICE}', 'function bm:p103/spend', f'function bm:p138/au/grant_{w}',
                             'playsound minecraft:entity.villager.yes player @s ~ ~ ~ 0.8 1', 'function bm:p103/tl/auras'])
    fn('admin/auras_all', [f'function bm:p138/au/grant_{w}' for w in ORDER])
    fn('admin/auras_reset', [f'tag @s remove bm.auown_{w}' for w in ORDER] + [f'tag @s remove bm.au_{w}' for w in ORDER] + [say('Every aura forgotten.')])

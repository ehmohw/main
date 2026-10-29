"""2.67: FOLLOWER WARDROBES - every outfit is yours for good, and every follower has a menu to change into them.

A COSMETIC, USED ONCE, IS UNLOCKED FOR GOOD (and used up): it goes into that follower's wardrobe. Then SNEAK + USE the
  follower's own item - any time, in the Overworld, whether they're out or not - for their menu: send them home, or
  change into any outfit they own, or back to their own clothes. Locked outfits show where to get them.
  (Emma: sneak + use while she's out still opens her buff menu - its WARDROBE button opens hers.)
NEW AT GOLDTOOTH (the raid shop): LEO'S TABARDS (Crimson Crusader, Royal Purple, Greenwood; hidden: Golden Champion),
  DEMOCRATUS' CLOAKS (Crimson Reaper, Ashen Shroud, Royal Violet; hidden: Gilded Storm), CECIL'S ROBES (Crimson, Midnight,
  Bone; hidden: Gilded) and KILLERWATT'S COLOURS (Midnight, Bone, Neon; hidden: Golden Thunder). Cecil's robe and
  KillerWatt's colours are their own look - with a gem in them, the gem's element shows instead.
"""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, Int
import phase28 as P28
import phase78 as P78
import phase89 as P89
import phase79_art as KA

GOLD = '#ffcf40'
# who: (name, colour, item word, {k: (cosmetic name, (dark, mid, light))}); 4 is hidden in each
NEW = {'leo': ('Leo', '#5ab8e0', 'Tabard', {1: ('Crimson Crusader', ('#2a0408', '#9a1e2a', '#e0606a')), 2: ('Royal Purple', ('#140626', '#4a2280', '#a07ae0')),
                                            3: ('Greenwood', ('#0a2010', '#2a6a34', '#7ac080')), 4: ('Golden Champion', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Champion', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Champion', ('#141014', '#4a4046', '#9a8c94'))}),
       'demo': ('Democratus', '#7ad06a', 'Cloak', {1: ('Crimson Reaper', ('#22040a', '#8a1a24', '#e05a64')), 2: ('Ashen Shroud', ('#141416', '#55555c', '#b4b4bc')),
                                                   3: ('Royal Violet', ('#160626', '#562886', '#b48ae6')), 4: ('Gilded Storm', ('#3a2806', '#b8902a', '#ffe8a0')), 5: ('Diamond Storm', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Storm', ('#141014', '#4a4046', '#9a8c94'))}),
       'cecil': ('Cecil', '#b48cff', 'Robe', {1: ('Crimson', ('#2a060c', '#7a1a2a', '#c8506a')), 2: ('Midnight', ('#06081a', '#1e2450', '#5a64a0')),
                                              3: ('Bone', ('#5a5448', '#b8b0a0', '#f4efe4')), 4: ('Gilded', ('#3a2806', '#b08a2a', '#ffe8a0')), 5: ('Diamond', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite', ('#141014', '#4a4046', '#9a8c94'))}),
       'kw': ('KillerWatt', '#ffe040', 'Colours', {int(k[1:]): (nm, pal[0]) for k, (nm, pal) in KA.COS_PAL.items()}),
       # 2.78: the rest of the followers (their art is recoloured in phase138)
       'apo': ('Apophiss', '#3ad06a', 'Scales', {1: ('Obsidian Coil', ('#07070c', '#2a2a38', '#7a7a92')), 2: ('Blood Wyrm', ('#200406', '#7a1418', '#e0584e')),
                                                3: ('Frost Serpent', ('#0a2232', '#3a8ab4', '#c8ecff')), 4: ('Gilded Coil', ('#3a2806', '#b8902a', '#ffe8a0')), 5: ('Diamond Coil', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Coil', ('#141014', '#4a4046', '#9a8c94'))}),
       'tul': ('Tullius', '#7ad8ff', 'Coat', {1: ("Admiral's Blue", ('#060c24', '#1e3a8a', '#6a8ae0')), 2: ('Corsair Crimson', ('#22040a', '#8a1a24', '#e05a64')),
                                            3: ('Bleached Bone', ('#5a5448', '#b8b0a0', '#f4efe4')), 4: ('Gilded Captain', ('#3a2806', '#b08a2a', '#ffe8a0')), 5: ('Diamond Captain', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Captain', ('#141014', '#4a4046', '#9a8c94'))}),
       'frog': ('the Frog with Mustache', '#6ac850', 'Skin', {1: ('Bluejay', ('#1a2a6a', '#3a7ae0', '#8ac8ff')), 2: ('Ember Toad', ('#4a0e04', '#d0501a', '#ffa060')),
                                                             3: ('Old Bog', ('#2a1a0a', '#7a5430', '#c09a6a')), 4: ('Golden Prince', ('#3a2806', '#e0b02a', '#fff0a0')), 5: ('Diamond Prince', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Prince', ('#141014', '#4a4046', '#9a8c94'))}),
       'don': ('Donado', '#e8d29a', 'Coat', {1: ('Chocolate', ('#1a0e06', '#5a3418', '#a07048')), 2: ('Midnight', ('#08080c', '#2a2a34', '#7a7a8a')),
                                           3: ('Snowdrift', ('#8a8a90', '#dcdce0', '#ffffff')), 4: ('Starlit', ('#0a0626', '#4a2a9a', '#b49aff')),
                                           5: ('Gilded', ('#3a2806', '#e0b030', '#fff0a0')),
                                           6: ('Diamond', ('#06323a', '#1a9aa0', '#a8fff4')), 7: ('Netherite', ('#141014', '#4a4046', '#9a8c94'))}),        # (5: 2.79a - his gilded coat; 6, 7: 2.80c)
       'pearl': ('Pearlman', '#5ac8ff', 'Bow Tie', {1: ('Ruby', ('#3a0408', '#c0202a', '#ff7a80')), 2: ('Emerald', ('#04260e', '#1a9a44', '#7aff9a')),
                                                    3: ('Amethyst', ('#1a0630', '#7a3ac0', '#d0a0ff')), 4: ('Gilded', ('#3a2806', '#e0b030', '#fff0a0')), 5: ('Diamond', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite', ('#141014', '#4a4046', '#9a8c94'))}),
       'fishy': ('Fishy', '#ffa040', 'Top Hat', {1: ('Midnight Silk', ('#06081c', '#1e2a6a', '#6a7ad0')), 2: ('Crimson Opera', ('#22040a', '#8a1a24', '#e05a64')),
                                                  3: ('Emerald Ascot', ('#04200e', '#1a7a3a', '#6ad08a')), 4: ('Gilded Topper', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Topper', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Topper', ('#141014', '#4a4046', '#9a8c94'))}),
       'wil': ('Wilfrey', '#f4f4f4', 'Heraldry', {1: ('Crimson Cross', ('#3a0408', '#b02020', '#ff7070')), 2: ('Azure Chevron', ('#06103a', '#2a4ab0', '#8aa8ff')),
                                                  3: ('Verdant Bend', ('#06260a', '#2a8a30', '#90e090')), 4: ('Gilded Sun', ('#3a2806', '#e0b030', '#fff0a0')), 5: ('Diamond Sun', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Sun', ('#141014', '#4a4046', '#9a8c94'))}),
       # 2.80d: Dennis's leather jacket, Pistachio's tail-coat
       'dennis': ('Dennis', '#e0a040', 'Jacket', {1: ('Road Brown', ('#1e0e04', '#6a3a1c', '#b07a4a')), 2: ('Biker Red', ('#22040a', '#8a1a1e', '#e05a5a')),
                                                 3: ('Forest Leather', ('#08180a', '#2a5a2a', '#7ab07a')), 4: ('Gilded Jacket', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Jacket', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Jacket', ('#141014', '#4a4046', '#9a8c94'))}),
       'pistachio': ('Pistachio', '#7ae890', 'Tail-coat', {1: ('Midnight Tails', ('#06081c', '#1e2a6a', '#6a7ad0')), 2: ('Claret Tails', ('#22040a', '#7a1a2a', '#d05a6a')),
                                                          3: ('Ivory Tails', ('#5a5448', '#b8b0a0', '#f4efe4')), 4: ('Gilded Tails', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Tails', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Tails', ('#141014', '#4a4046', '#9a8c94'))}),
       # 2.82: King Omega's spectral hide
       'omega': ('King Omega', '#9fb4ff', 'Spirit', {1: ('Spectral Blue', ('#0a1a3a', '#3a6ac8', '#a8d0ff')), 2: ('Blood Moon', ('#24040a', '#8a1a24', '#f07a70')),
                                                    3: ('Verdant Wraith', ('#062210', '#2a8a4a', '#a0f0b0')), 4: ('Gilded King', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond King', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite King', ('#141014', '#4a4046', '#9a8c94'))}),
       # 2.86: Ashur's magma dress - the rock and its glowing cracks recoloured together
       'ashur': ('Ashur', '#ff7a2a', 'Dress', {1: ('Blue Flame', ('#040a26', '#1a52d0', '#a8f0ff')), 2: ('Verdant Ember', ('#04200a', '#2aa040', '#c0ff8a')),
                                              3: ('Obsidian Rose', ('#160616', '#8a1a6a', '#ff8ad8')), 4: ('Gilded Magma', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Magma', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Magma', ('#141014', '#4a4046', '#9a8c94'))}),
       'chef': ('The Chef', '#ffd07a', 'Whites', {1: ('Midnight Brigade', ('#08080c', '#2a2a32', '#6a6a76')), 2: ('Bistro Blue', ('#06143a', '#2a52b0', '#a8c8ff')),
                                                  3: ('Sommelier Wine', ('#22040e', '#7a1a34', '#e07a96')), 4: ('Gilded Whites', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Whites', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Whites', ('#141014', '#4a4046', '#9a8c94'))}),
       'neighbor': ('The Neighbor', '#7ab8ff', 'Sailor Suit', {1: ('Navy Bandmaster', ('#040c26', '#1a3a8a', '#8ab0ff')), 2: ('Encore Crimson', ('#2a0408', '#a01a24', '#ff8a8a')),
                                                              3: ('Jazz Violet', ('#140626', '#5a2aa0', '#d0a8ff')), 4: ('Gilded Suit', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Suit', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Suit', ('#141014', '#4a4046', '#9a8c94'))}),
       'ava': ('Queen Ava', '#6ad8e8', 'Gown', {1: ('Coral Reef', ('#2a0a10', '#c04a4a', '#ffb0a0')), 2: ('Abyssal Violet', ('#120626', '#5a2a9a', '#c8a8ff')),
                                          3: ('Kelp Forest', ('#06200e', '#2a7a3a', '#a8f0b0')), 4: ('Gilded Gown', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Gown', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Gown', ('#141014', '#4a4046', '#9a8c94'))}),
       'pearlq': ('Queen Pearl', '#5ae0d8', 'Dress', {1: ('Coral Pink', ('#3a0a1a', '#e05a8a', '#ffc0d8')), 2: ('Sunset Gold', ('#3a1a04', '#e08a2a', '#ffd890')),
                                              3: ('Starlit Navy', ('#060a2a', '#2a3a9a', '#a8b8ff')), 4: ('Gilded Dress', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Dress', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Dress', ('#141014', '#4a4046', '#9a8c94'))}),
       'bloo': ('Bloo', '#5a9ae8', 'Fur', {1: ('Shadow Pelt', ('#06060e', '#2a2a3a', '#7a7a8e')), 2: ('Ember Mane', ('#2a0604', '#a0301a', '#ffa060')),
                                   3: ('Frost Coat', ('#0a1a2a', '#7aa8c8', '#f0f8ff')), 4: ('Gilded Fur', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Fur', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Fur', ('#141014', '#4a4046', '#9a8c94'))}),
       'stalker': ('The Stalker', '#a8ac70', 'Skin', {1: ('Bone White', ('#2a2a22', '#c8c4b0', '#f4f0e0')), 2: ('Ashen Grey', ('#101012', '#5a5a60', '#b0b0b8')),
                                   3: ('Blood Moon', ('#1a0204', '#7a1018', '#e05a60')), 4: ('Gilded Skin', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Skin', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Skin', ('#141014', '#4a4046', '#9a8c94'))}),
       'lantern': ('The Arachno-Lantern', '#ff8a2a', 'Rind', {1: ('Ghost Gourd', ('#1a2a2a', '#c8e8e0', '#f8fff8')), 2: ('Soulfire Rind', ('#04161a', '#1a8a9a', '#7af0ff')),
                                   3: ('Harvest Moon', ('#2a1004', '#c86a1a', '#ffd070')), 4: ('Gilded Rind', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Rind', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Rind', ('#141014', '#4a4046', '#9a8c94'))}),
       'bender': ('Bender', '#e0a860', 'Coat', {1: ('Midnight Black', ('#0c0a0a', '#2e2a28', '#6a625a')), 2: ('Snow White', ('#8a8478', '#e4dccc', '#fffaf0')), 3: ('Sable', ('#1a0e06', '#6a4a2a', '#c8985a')), 4: ('Gilded Coat', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Coat', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Coat', ('#141014', '#4a4046', '#9a8c94'))}),
       'bones': ('Bones', '#8ab0c8', 'Skin', {1: ('Great White', ('#2a3038', '#9aa4b0', '#f4f6f8')), 2: ('Hammerhead Bronze', ('#2a1a0a', '#8a6a3a', '#e0c08a')), 3: ('Abyss Black', ('#040608', '#1a2430', '#4a6a8a')), 4: ('Gilded Skin', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Skin', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Skin', ('#141014', '#4a4046', '#9a8c94'))}),
       'sky': ('The Sky Buddies', '#ffd04a', 'Nightcap', {1: ('Bubblegum Pink', ('#5a1030', '#e86aa8', '#ffc8e4')), 2: ('Mint Dream', ('#0a3a2a', '#4ac89a', '#c8ffe8')), 3: ('Lavender Night', ('#1e1040', '#7a5ad0', '#d8c8ff')), 4: ('Gilded Nightcap', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Nightcap', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Nightcap', ('#141014', '#4a4046', '#9a8c94'))}),
       'pxemma': ('8-Bit Emma', '#ff6ac8', 'Palette', {1: ('Game Boy', ('#0f380f', '#306230', '#9bbc0f')), 2: ('Virtual Boy', ('#1a0000', '#a01010', '#ff6060')), 3: ('Sepia Print', ('#2a1a0a', '#8a6a3a', '#f4e4bc')), 4: ('Gilded Pixels', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Pixels', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Pixels', ('#141014', '#4a4046', '#9a8c94'))}),
       'pxleo': ('8-Bit Leo', '#4ab0ff', 'Palette', {1: ('Game Boy', ('#0f380f', '#306230', '#9bbc0f')), 2: ('Virtual Boy', ('#1a0000', '#a01010', '#ff6060')), 3: ('Sepia Print', ('#2a1a0a', '#8a6a3a', '#f4e4bc')), 4: ('Gilded Pixels', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Pixels', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Pixels', ('#141014', '#4a4046', '#9a8c94'))}),
       'pxcecil': ('8-Bit Cecil', '#b070ff', 'Palette', {1: ('Game Boy', ('#0f380f', '#306230', '#9bbc0f')), 2: ('Virtual Boy', ('#1a0000', '#a01010', '#ff6060')), 3: ('Sepia Print', ('#2a1a0a', '#8a6a3a', '#f4e4bc')), 4: ('Gilded Pixels', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Pixels', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Pixels', ('#141014', '#4a4046', '#9a8c94'))}),
       'gem': ('The Gem of Creativity', '#5ae0a0', 'Facets', {1: ('Ruby Facets', ('#3a0610', '#d02a4a', '#ffb0c0')), 2: ('Sapphire Facets', ('#06123a', '#2a5ad0', '#b0c8ff')), 3: ('Amethyst Facets', ('#200a3a', '#8a3ad0', '#e0b8ff')), 4: ('Gilded Facets', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Facets', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Facets', ('#141014', '#4a4046', '#9a8c94'))}),
       'batty': ('Batty', '#8a8ad8', 'Fur', {1: ('Crimson Fur', ('#2a0408', '#8a1a2a', '#d06a7a')), 2: ('Ash Fur', ('#1a1a1e', '#5a5a64', '#b0b0bc')), 3: ('Moss Fur', ('#0a2010', '#2a6a3a', '#8ac89a')), 4: ('Gilded Fur', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Fur', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Fur', ('#141014', '#4a4046', '#9a8c94'))}),
       'eggbert': ('Eggbert', '#d8d4c0', 'Ooze', {1: ('Royal Ooze', ('#1a0630', '#5a1aa0', '#b88ae8')), 2: ('Slime Ooze', ('#0a2a06', '#3a9a2a', '#a8f090')), 3: ('Magma Ooze', ('#2a0a04', '#c04a10', '#ffb060')), 4: ('Gilded Ooze', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Ooze', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Ooze', ('#141014', '#4a4046', '#9a8c94'))}),
       'count': ('The Count', '#a8c8f0', 'Topper', {1: ('Emerald Topper', ('#04200e', '#1a7a3a', '#80d8a0')), 2: ('Royal Topper', ('#14062a', '#4a1a8a', '#a080e0')), 3: ('Crimson Topper', ('#2a0408', '#9a1a2a', '#e07080')), 4: ('Gilded Topper', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Topper', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Topper', ('#141014', '#4a4046', '#9a8c94'))}),
       'dragon': ('The Doodle Dragon', '#5ac048', 'Scales', {1: ('Fire-Red Scales', ('#4a0606', '#d03a2a', '#ffa890')), 2: ('Ocean-Blue Scales', ('#061a4a', '#2a6ad0', '#a0c8ff')), 3: ('Sunset-Purple Scales', ('#200640', '#8a3ad0', '#e0b0ff')), 4: ('Gilded Crayon Scales', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Crayon Scales', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Crayon Scales', ('#141014', '#4a4046', '#9a8c94'))}),
       'eraser': ('The Eraser', '#f08aa0', 'Rubber', {1: ('Blue Rubber', ('#0a1a4a', '#4a7ad8', '#b0ccff')), 2: ('Mint Rubber', ('#06321e', '#3ab88a', '#b0f0d8')), 3: ('Lemon Rubber', ('#3a3006', '#d8c03a', '#fff4a8')), 4: ('Gilded Rubber', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Rubber', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Rubber', ('#141014', '#4a4046', '#9a8c94'))}),
       'cursor': ('The Cursor', '#cfe8ff', 'Theme', {1: ('Ocean Theme', ('#04183a', '#3a8ad8', '#c8e8ff')), 2: ('Rose Theme', ('#3a0418', '#d04a8a', '#ffd0e8')), 3: ('Lime Theme', ('#0e2a04', '#5ac83a', '#d8ffc8')), 4: ('Gilded Pointer', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Pointer', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Pointer', ('#141014', '#4a4046', '#9a8c94'))}),
       'inkblot': ('The Ink Blot', '#7a7aaa', 'Ink', {1: ('Royal Blue Ink', ('#040a2a', '#1a3aa0', '#7a9aff')), 2: ('Crimson Ink', ('#2a0408', '#9a1a2a', '#ff7a8a')), 3: ('Emerald Ink', ('#042a10', '#1a8a3a', '#7aff9a')), 4: ('Gilded Ink Blot', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Ink Blot', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Ink Blot', ('#141014', '#4a4046', '#9a8c94'))}),
       'speech': ('The Speech Bubble', '#ffd060', 'Paper', {1: ('Sky Paper', ('#0a2a4a', '#5aa8e8', '#d8f0ff')), 2: ('Pink Paper', ('#3a0a24', '#e86ab0', '#ffe0f0')), 3: ('Mint Paper', ('#063a24', '#4ad09a', '#d8fff0')), 4: ('Gilded Paper', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Paper', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Paper', ('#141014', '#4a4046', '#9a8c94'))}),
       'lightbringer': ('The Lightbringer', '#ffe08a', 'Vestments', {1: ('Royal Vestments', ('#060a3a', '#2a4ad0', '#b0c0ff')), 2: ('Amethyst Vestments', ('#1a0630', '#7a3ac0', '#d8b8ff')), 3: ('Dawn Vestments', ('#3a1406', '#e08a4a', '#ffe0c0')), 4: ('Gilded Vestments', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Vestments', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Vestments', ('#141014', '#4a4046', '#9a8c94'))}),
       'dryad': ('The Pale Dryad', '#6aa8f0', 'Cap', {1: ('Toadstool Cap', ('#3a0406', '#c82a2a', '#ffa0a0')), 2: ('Violet Cap', ('#1a0630', '#7a3ac8', '#dab0ff')), 3: ('Amber Cap', ('#3a1a04', '#e0901a', '#ffd890')), 4: ('Gilded Mushroom Cap', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Mushroom Cap', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Mushroom Cap', ('#141014', '#4a4046', '#9a8c94'))}),
       'sovereign': ('The Bound Sovereign', '#d0182e', 'Plate', {1: ('Bone Plate', ('#3a3428', '#c8bea0', '#f4ecd8')), 2: ('Ashen Plate', ('#1a1a1c', '#6a6a70', '#c0c0c8')), 3: ('Dawn Plate', ('#3a2c10', '#e0c060', '#fff4d0')), 4: ('Gilded Plate', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Plate', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Plate', ('#141014', '#4a4046', '#9a8c94'))}),
       'vexis': ('Vexis, the Unlinked', '#7aff6a', 'Mantle', {1: ('Hive Mantle', ('#0e2a12', '#2a8a3a', '#9aff8a')), 2: ('Donadian Mantle', ('#06302c', '#1aa898', '#a8fff0')), 3: ('Starfire Mantle', ('#3a1406', '#d8602a', '#ffd08a')), 4: ('Gilded Mantle', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Mantle', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Mantle', ('#141014', '#4a4046', '#9a8c94'))}),
       'henry': ('Henry', '#9a9ab8', 'Collar', {1: ('Navy Collar', ('#060a2a', '#1a2a8a', '#8a9ae0')), 2: ('Emerald Collar', ('#06280e', '#1a8a3a', '#90e0a8')), 3: ('Gold Collar', ('#3a2806', '#c8962a', '#ffe08a')), 4: ('Gilded Collar', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Collar', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Collar', ('#141014', '#4a4046', '#9a8c94'))}),
       'nia': ('Nia', '#e0a050', 'Collar', {1: ('Rose Collar', ('#3a0a1a', '#d05a8a', '#ffc0d8')), 2: ('Sky Collar', ('#0a2040', '#3a8ad0', '#b0e0ff')), 3: ('Mint Collar', ('#0a3020', '#3ac090', '#c0ffe8')), 4: ('Gilded Collar', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Collar', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Collar', ('#141014', '#4a4046', '#9a8c94'))}),
       'rufus': ('Rufus Gnaw', '#c0392b', 'Bandana', {1: ('Black Bandana', ('#100c0e', '#3a3236', '#8a8088')), 2: ('Royal Blue Bandana', ('#0a1a5a', '#2a4ad0', '#9ab4ff')), 3: ('Forest Bandana', ('#0a3a14', '#2a8a3a', '#a0e0a8')), 4: ('Gilded Bandana', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Bandana', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Bandana', ('#141014', '#4a4046', '#9a8c94'))}),
       'kettle': ('Kettle', '#8ad8ff', 'Crayon', {1: ('Red Crayon', ('#5a0a0a', '#d83a3a', '#ffa8a0')), 2: ('Blue Crayon', ('#0a2a6a', '#3a7ae0', '#a8d0ff')), 3: ('Green Crayon', ('#0a4a14', '#3ab048', '#b0f0b8')), 4: ('Gilded Crayon', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Crayon', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Crayon', ('#141014', '#4a4046', '#9a8c94'))}),
       'capshun': ('Mr. Capshun', '#f0f0f0', 'Ink', {1: ('Blue Ballpoint', ('#0a1a7a', '#2a4ad0', '#9ab4ff')), 2: ('Red Pen', ('#6a0a0a', '#d02a2a', '#ffa0a0')), 3: ('Green Marker', ('#0a4a14', '#2aa040', '#a0f0b0')), 4: ('Gilded Ink', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Ink', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Ink', ('#141014', '#4a4046', '#9a8c94'))}),
       'mireling': ('The Mireling', '#e0384a', 'Veins', {1: ('Ember Mire', ('#0a0504', '#2e130b', '#ff8a2a')), 2: ('Void Mire', ('#07040c', '#1f1032', '#b46aff')), 3: ('Frost Mire', ('#04070c', '#122030', '#9ad8ff')), 4: ('Gilded Mire', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Mire', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Mire', ('#141014', '#4a4046', '#9a8c94'))}),
       'keeper': ('The Keeper of Bonds', '#ffd6f0', 'Weave', {1: ('Dawn Weave', ('#4a1a2a', '#e07a9a', '#ffd8e4')), 2: ('Twilight Weave', ('#140e3a', '#5a4ad0', '#c8c0ff')), 3: ('Meadow Weave', ('#0e2e14', '#4aa85a', '#d0f4c8')), 4: ('Gilded Weave', ('#3a2806', '#c8962a', '#ffe08a')), 5: ('Diamond Weave', ('#06323a', '#1a9aa0', '#a8fff4')), 6: ('Netherite Weave', ('#141014', '#4a4046', '#9a8c94'))})}   # (3.0: [keeper hook])
HIDDEN = 4
SHE = {'ashur', 'ava', 'pearlq', 'pxemma', 'nia', 'lightbringer', 'dryad'}                                  # (2.86: the first of the newer followers who's a she)
THEY = {'sky'}                                                  # (2.94: the Sky Buddies - three of them)
IT = {'stalker', 'lantern', 'mireling', 'keeper'}                            # (2.87: and the first who are neither)
RECOLOUR = {'leo': ('le_tunic', 'le_skirt', 'le_cape'), 'demo': ('dm_hood', 'dm_hood_dk', 'dm_cape'), 'cecil': ('cec_robe', 'cec_robe_dark')}
# (2.79b: with Leo's metal looks his helm and armour turn to match - head included; 2.80c: gold with the Golden Champion, no longer diamond)
ARMOUR = {'leo': ('le_steel', 'le_steel_dk', 'le_mail')}
DYE = {'Crimson Crusader': 'red', 'Royal Purple': 'purple', 'Greenwood': 'green', 'Golden Champion': 'yellow', 'Crimson Reaper': 'red', 'Ashen Shroud': 'gray',
       'Royal Violet': 'purple', 'Gilded Storm': 'yellow', 'Crimson': 'red', 'Midnight': 'blue', 'Bone': 'white', 'Gilded': 'yellow', 'Neon': 'magenta',
       'Golden Thunder': 'yellow', 'Obsidian Coil': 'black', 'Blood Wyrm': 'red', 'Frost Serpent': 'light_blue', 'Gilded Coil': 'yellow',
       "Admiral's Blue": 'blue', 'Corsair Crimson': 'red', 'Bleached Bone': 'white', 'Gilded Captain': 'yellow', 'Bluejay': 'light_blue',
       'Ember Toad': 'orange', 'Old Bog': 'brown', 'Golden Prince': 'yellow', 'Chocolate': 'brown', 'Midnight': 'blue', 'Snowdrift': 'white', 'Starlit': 'purple',
       'Ruby': 'red', 'Emerald': 'lime', 'Amethyst': 'purple', 'Gilded': 'yellow', 'Crimson Cross': 'red', 'Azure Chevron': 'blue', 'Verdant Bend': 'green',
       'Gilded Sun': 'yellow', 'Midnight Silk': 'blue', 'Crimson Opera': 'red', 'Emerald Ascot': 'green', 'Gilded Topper': 'yellow',
       'Diamond Champion': 'light_blue', 'Diamond Storm': 'light_blue', 'Diamond': 'light_blue', 'Diamond Coil': 'light_blue', 'Diamond Captain': 'light_blue', 'Diamond Prince': 'light_blue', 'Diamond Topper': 'light_blue', 'Diamond Sun': 'light_blue', 'Diamond Thunder': 'light_blue',
       'Road Brown': 'brown', 'Biker Red': 'red', 'Forest Leather': 'green', 'Gilded Jacket': 'yellow', 'Diamond Jacket': 'light_blue', 'Netherite Jacket': 'black',
       'Midnight Tails': 'blue', 'Claret Tails': 'red', 'Ivory Tails': 'white', 'Gilded Tails': 'yellow', 'Diamond Tails': 'light_blue', 'Netherite Tails': 'black',
       'Spectral Blue': 'light_blue', 'Blood Moon': 'red', 'Verdant Wraith': 'lime', 'Gilded King': 'yellow', 'Diamond King': 'light_blue', 'Netherite King': 'black',
       'Blue Flame': 'blue', 'Verdant Ember': 'lime', 'Obsidian Rose': 'pink', 'Gilded Magma': 'yellow', 'Diamond Magma': 'light_blue', 'Netherite Magma': 'black',
       'Midnight Brigade': 'black', 'Bistro Blue': 'blue', 'Sommelier Wine': 'red', 'Gilded Whites': 'yellow', 'Diamond Whites': 'light_blue', 'Netherite Whites': 'black',
       'Navy Bandmaster': 'blue', 'Encore Crimson': 'red', 'Jazz Violet': 'purple', 'Gilded Suit': 'yellow', 'Diamond Suit': 'light_blue', 'Netherite Suit': 'black',
       'Coral Reef': 'red', 'Abyssal Violet': 'purple', 'Kelp Forest': 'green', 'Gilded Gown': 'yellow', 'Diamond Gown': 'light_blue', 'Netherite Gown': 'black',
       'Coral Pink': 'pink', 'Sunset Gold': 'orange', 'Starlit Navy': 'blue', 'Gilded Dress': 'yellow', 'Diamond Dress': 'light_blue', 'Netherite Dress': 'black',
       'Shadow Pelt': 'black', 'Ember Mane': 'red', 'Frost Coat': 'white', 'Gilded Fur': 'yellow', 'Diamond Fur': 'light_blue', 'Netherite Fur': 'black',
       'Bone White': 'white', 'Ashen Grey': 'gray', 'Blood Moon': 'red', 'Gilded Skin': 'yellow', 'Diamond Skin': 'light_blue', 'Netherite Skin': 'black',
       'Ghost Gourd': 'white', 'Soulfire Rind': 'cyan', 'Harvest Moon': 'orange', 'Gilded Rind': 'yellow', 'Diamond Rind': 'light_blue', 'Netherite Rind': 'black',
       'Midnight Black': 'black', 'Snow White': 'white', 'Sable': 'brown', 'Gilded Coat': 'yellow', 'Diamond Coat': 'light_blue', 'Netherite Coat': 'black',
       'Great White': 'white', 'Hammerhead Bronze': 'brown', 'Abyss Black': 'black', 'Gilded Skin': 'yellow', 'Diamond Skin': 'light_blue', 'Netherite Skin': 'black',
       'Netherite Champion': 'black', 'Netherite Storm': 'black', 'Netherite': 'black', 'Netherite Coil': 'black', 'Netherite Captain': 'black', 'Netherite Prince': 'black', 'Netherite Topper': 'black', 'Netherite Sun': 'black', 'Netherite Thunder': 'black', 'Ruby Facets': 'red', 'Sapphire Facets': 'blue', 'Amethyst Facets': 'purple', 'Gilded Facets': 'yellow', 'Diamond Facets': 'cyan', 'Netherite Facets': 'black', 'Crimson Fur': 'red', 'Ash Fur': 'gray', 'Moss Fur': 'green', 'Gilded Fur': 'yellow', 'Diamond Fur': 'cyan', 'Netherite Fur': 'black', 'Royal Ooze': 'purple', 'Slime Ooze': 'lime', 'Magma Ooze': 'orange', 'Gilded Ooze': 'yellow', 'Diamond Ooze': 'cyan', 'Netherite Ooze': 'black', 'Emerald Topper': 'green', 'Royal Topper': 'purple', 'Crimson Topper': 'red', 'Gilded Topper': 'yellow', 'Diamond Topper': 'cyan', 'Navy Collar': 'blue', 'Emerald Collar': 'green', 'Gold Collar': 'yellow', 'Gilded Collar': 'yellow', 'Diamond Collar': 'cyan', 'Netherite Collar': 'black', 'Rose Collar': 'pink', 'Sky Collar': 'light_blue', 'Mint Collar': 'lime', 'Black Bandana': 'black', 'Royal Blue Bandana': 'blue', 'Forest Bandana': 'green', 'Gilded Bandana': 'yellow', 'Diamond Bandana': 'cyan', 'Netherite Bandana': 'black', 'Red Crayon': 'red', 'Blue Crayon': 'blue', 'Green Crayon': 'green', 'Gilded Crayon': 'yellow', 'Diamond Crayon': 'cyan', 'Netherite Crayon': 'black', 'Blue Ballpoint': 'blue', 'Game Boy': 'green', 'Virtual Boy': 'red', 'Sepia Print': 'brown', 'Gilded Pixels': 'yellow', 'Diamond Pixels': 'light_blue', 'Netherite Pixels': 'black', 'Bubblegum Pink': 'pink', 'Mint Dream': 'lime', 'Lavender Night': 'purple', 'Gilded Nightcap': 'yellow', 'Diamond Nightcap': 'light_blue', 'Netherite Nightcap': 'black', 'Red Pen': 'red', 'Green Marker': 'green', 'Gilded Ink': 'yellow', 'Diamond Ink': 'light_blue', 'Netherite Ink': 'black'}
DYE.update({'Fire-Red Scales': 'red', 'Ocean-Blue Scales': 'blue', 'Sunset-Purple Scales': 'purple', 'Blue Rubber': 'blue', 'Mint Rubber': 'lime', 'Lemon Rubber': 'yellow', 'Ocean Theme': 'light_blue', 'Rose Theme': 'pink', 'Lime Theme': 'lime', 'Royal Blue Ink': 'blue', 'Crimson Ink': 'red', 'Emerald Ink': 'green', 'Sky Paper': 'light_blue', 'Pink Paper': 'pink', 'Mint Paper': 'lime', 'Royal Vestments': 'blue', 'Amethyst Vestments': 'purple', 'Dawn Vestments': 'orange', 'Toadstool Cap': 'red', 'Violet Cap': 'purple', 'Amber Cap': 'orange', 'Gilded Crayon Scales': 'yellow', 'Diamond Crayon Scales': 'light_blue', 'Netherite Crayon Scales': 'black', 'Gilded Rubber': 'yellow', 'Diamond Rubber': 'light_blue', 'Netherite Rubber': 'black', 'Gilded Pointer': 'yellow', 'Diamond Pointer': 'light_blue', 'Netherite Pointer': 'black', 'Gilded Ink Blot': 'yellow', 'Diamond Ink Blot': 'light_blue', 'Netherite Ink Blot': 'black', 'Gilded Paper': 'yellow', 'Diamond Paper': 'light_blue', 'Netherite Paper': 'black', 'Gilded Vestments': 'yellow', 'Diamond Vestments': 'light_blue', 'Netherite Vestments': 'black', 'Gilded Mushroom Cap': 'yellow', 'Diamond Mushroom Cap': 'light_blue', 'Netherite Mushroom Cap': 'black'})   # (2.97: the seven)
DYE.update({'Bone Plate': 'white', 'Ashen Plate': 'gray', 'Dawn Plate': 'yellow', 'Gilded Plate': 'yellow', 'Diamond Plate': 'light_blue', 'Netherite Plate': 'black'})   # (2.98: the Bound Sovereign)
DYE.update({'Ember Mire': 'orange', 'Void Mire': 'purple', 'Frost Mire': 'light_blue', 'Gilded Mire': 'yellow', 'Diamond Mire': 'light_blue', 'Netherite Mire': 'black'})   # (3.00: the Mireling)
DYE.update({'Dawn Weave': 'pink', 'Twilight Weave': 'purple', 'Meadow Weave': 'lime', 'Gilded Weave': 'yellow', 'Diamond Weave': 'light_blue', 'Netherite Weave': 'black'})   # (3.0: [keeper hook] the Keeper of Bonds)
DYE.update({'Hive Mantle': 'lime', 'Donadian Mantle': 'cyan', 'Starfire Mantle': 'orange', 'Gilded Mantle': 'yellow', 'Diamond Mantle': 'light_blue', 'Netherite Mantle': 'black'})   # (2.99: Vexis)
WORD = {'apo': 'his scales', 'tul': 'his coat', 'frog': 'his skin', 'don': 'his coat', 'pearl': 'his bow tie and hat band', 'wil': 'the shield he bears',
        'fishy': 'his top hat', 'dennis': 'his leather jacket', 'pistachio': 'his tail-coat', 'omega': 'his spectral hide', 'ashur': 'her magma dress', 'chef': 'his chef\'s whites', 'neighbor': 'his sailor suit', 'ava': 'her gown', 'pearlq': 'her dress and gown', 'bloo': 'his fur', 'stalker': 'its skin', 'lantern': 'its rind', 'bender': 'his coat', 'bones': 'his skin', 'capshun': 'his ink', 'kettle': 'his crayon', 'rufus': 'his bandana', 'henry': 'his collar', 'nia': 'her collar', 'gem': 'its facets', 'batty': 'his fur', 'eggbert': 'his ooze', 'count': 'his top hat', 'dragon': 'his crayon scales', 'eraser': 'its rubber', 'cursor': 'its pointer', 'inkblot': 'its ink', 'speech': 'its paper', 'lightbringer': 'her vestments', 'dryad': 'her mushroom cap', 'sovereign': 'his plate', 'vexis': 'its mantle', 'mireling': 'its veins', 'keeper': 'its woven robe', 'pxcecil': "8-Bit Cecil's palette", 'pxleo': "8-Bit Leo's palette", 'pxemma': "8-Bit Emma's palette", 'sky': "Snooze's nightcap"}
import shiny as _SH                                   # (2.94t: each follower's shiny look - never sold, found: phase221)
_SH.extend_new(NEW, DYE)
for _w, (_who, _col, _word, _set) in NEW.items():
    for _k, (_n, _pal) in _set.items():
        _iid = f'cos_{_w}_{_k}'
        _short = {'frog': 'The Frog'}.get(_w, _who)
        _menu = {'wil': 'Sneak + use his locket while he rests: his wardrobe.', 'pearl': 'Sneak + use his card: his menu - Wardrobe.'}.get(
            _w, ('Sneak + use its own item: its menu - Wardrobe.' if _w in IT else 'Sneak + use their own item: their menu - Wardrobe.' if _w in THEY else 'Sneak + use her own item: her menu - Wardrobe.' if _w in SHE else 'Sneak + use his own item: his menu - Wardrobe.') if _w in WORD else 'Sneak + use his own item: his menu - change any time.')
        item(_iid, TOTEM, f"{_short}'s {_word}: {_n}", _pal[1] if _pal[1] != '#55555c' else '#9a9aa2',
             [f'{_n} - for {_who} alone.' if _w not in WORD else f'{_n} - {WORD[_w]}, for {_who} alone.',
              (f'Use: it\'s {"its" if _w in IT else "theirs" if _w in THEY else "hers" if _w in SHE else "his"} for good - in {"its" if _w in IT else "their" if _w in THEY else "her" if _w in SHE else "his"} wardrobe.', 'blue'), (_menu, 'gray')] +
             ([('Hidden: rare - a Gutter Trophy at Goldtooth.', 'dark_gray')] if _k == HIDDEN else []) +
             ([('With a gem in him, the gem\'s element shows instead.', 'dark_gray')] if _w in ('cecil', 'kw') else []),
             model=f'minecraft:{DYE[_n]}_dye', glint=_k == HIDDEN or None, stack=1, cat='cosmetic', comps=hold('none'))
        HOLD[_iid] = f'bm:p99/use/{_w}{_k}'
# (the old wardrobe items say so too)
for _iid in [i for i in ITEMS if i.startswith(('cos_ribbon_', 'cos_dress_', 'cos_celi_', 'cos_zib_', 'cos_outfit_'))]:
    _L = ITEMS[_iid]['comps']['minecraft:lore']
    _L[:] = [l for l in _L if not (isinstance(l, dict) and l.get('text', '').startswith(('Kept:', 'Sneak + use', 'Use while', 'Use one while')))]
    _L.insert(1, T('Use: unlocked for good - in the wardrobe.', 'blue'))
    _L.insert(2, T('Sneak + use the follower\'s item: the menu.', 'gray'))
BASE = {'emma': 9800, 'celi': 9840, 'zib': 9860, 'cecil': 9880, 'kw': 9900, 'leo': 9920, 'demo': 9940,
        'apo': 9000, 'tul': 9020, 'frog': 9040, 'don': 9060, 'pearl': 9080, 'wil': 9100,         # (2.78: the rest - their own blocks of 20)
        'fishy': 9120,                                                                             # (2.79)
        'dennis': 2240, 'pistachio': 2260,                                                         # (2.80d)
        'omega': 2300,
        'ashur': 2460, 'chef': 2520, 'neighbor': 2560, 'ava': 2640, 'pearlq': 2660, 'bloo': 2680, 'stalker': 2720, 'lantern': 2760, 'bender': 2800, 'bones': 2840, 'capshun': 2880, 'kettle': 3070, 'rufus': 2480, 'henry': 4320, 'nia': 4370, 'gem': 4420, 'batty': 4470, 'eggbert': 4520, 'count': 4570, 'dragon': 4620, 'eraser': 4670, 'cursor': 4720, 'inkblot': 4770, 'speech': 4820, 'lightbringer': 4870, 'dryad': 4920, 'sovereign': 4970, 'vexis': 5170, 'mireling': 5220, 'keeper': 5270, 'pxcecil': 3040, 'pxleo': 3000, 'pxemma': 2960, 'sky': 2900}                                                                             # (2.82)
TOP = {'emma': 9839, 'celi': 9859, 'zib': 9879, 'cecil': 9899, 'kw': 9919, 'leo': 9939, 'demo': 9959}   # each follower's last code
TOP.update({w: b + 19 for w, b in BASE.items() if w not in TOP})
COS = {'leo': 'bm.cosl', 'demo': 'bm.cosm', 'cecil': 'bm.cosce', 'kw': 'bm.cosk', 'apo': 'bm.cosap', 'tul': 'bm.costu', 'frog': 'bm.cosfg', 'don': 'bm.cosdn',
       'pearl': 'bm.cospm', 'wil': 'bm.coswl', 'fishy': 'bm.cosfy', 'dennis': 'bm.cosdw', 'pistachio': 'bm.cospi', 'omega': 'bm.cosom', 'ashur': 'bm.cosas', 'chef': 'bm.coskk', 'neighbor': 'bm.cosnb', 'ava': 'bm.cosav', 'pearlq': 'bm.cospq', 'bloo': 'bm.cosbo', 'stalker': 'bm.cossv', 'lantern': 'bm.cosln', 'bender': 'bm.cosbv', 'bones': 'bm.cosbj', 'capshun': 'bm.cosmz', 'kettle': 'bm.coskt', 'rufus': 'bm.cosru', 'henry': 'bm.coshy', 'nia': 'bm.cosni', 'gem': 'bm.coscg', 'batty': 'bm.cosyt', 'eggbert': 'bm.coseb', 'count': 'bm.coskn', 'dragon': 'bm.cosdd', 'eraser': 'bm.cosez', 'cursor': 'bm.cosux', 'inkblot': 'bm.cosib', 'speech': 'bm.coswb', 'lightbringer': 'bm.coslh', 'dryad': 'bm.cospy', 'sovereign': 'bm.cosxv', 'vexis': 'bm.cosxb', 'mireling': 'bm.cosml', 'keeper': 'bm.costk', 'pxcecil': 'bm.cosxc', 'pxleo': 'bm.cosxl', 'pxemma': 'bm.cosxm', 'sky': 'bm.cosyb'}
NAMES = {'emma': ('Emma', '#ff7ad0', 'her'), 'celi': ('Celi', '#9ad8ff', 'her'), 'zib': ('Zib', '#3ad8c8', 'him'), 'cecil': ('Cecil', '#b48cff', 'him'),
         'kw': ('KillerWatt', '#ffe040', 'him'), 'leo': ('Leo', '#5ab8e0', 'him'), 'demo': ('Democratus', '#7ad06a', 'him'),
         'apo': ('Apophiss', '#3ad06a', 'him'), 'tul': ('Tullius', '#7ad8ff', 'him'), 'frog': ('the Frog with Mustache', '#6ac850', 'him'),
         'don': ('Donado', '#e8d29a', 'him'), 'pearl': ('Pearlman', '#5ac8ff', 'him'), 'wil': ('Wilfrey', '#f4f4f4', 'him'), 'fishy': ('Fishy', '#ffa040', 'him'),
         'dennis': ('Dennis', '#e0a040', 'him'), 'pistachio': ('Pistachio', '#7ae890', 'him'), 'omega': ('King Omega', '#9fb4ff', 'him'), 'ashur': ('Ashur', '#ff7a2a', 'her'), 'chef': ('the Chef', '#ffd07a', 'him'), 'neighbor': ('the Neighbor', '#7ab8ff', 'him'),
         'ava': ('Queen Ava', '#6ad8e8', 'her'), 'pearlq': ('Queen Pearl', '#5ae0d8', 'her'), 'bloo': ('Bloo', '#5a9ae8', 'him'), 'stalker': ('The Stalker', '#a8ac70', 'it'), 'lantern': ('The Arachno-Lantern', '#ff8a2a', 'it'), 'bender': ('Bender', '#e0a860', 'him'), 'bones': ('Bones', '#8ab0c8', 'him'), 'capshun': ('Mr. Capshun', '#f0f0f0', 'him'), 'kettle': ('Kettle', '#8ad8ff', 'him'), 'rufus': ('Rufus Gnaw', '#c0392b', 'him'), 'henry': ('Henry', '#9a9ab8', 'him'), 'nia': ('Nia', '#e0a050', 'her'), 'gem': ('The Gem of Creativity', '#5ae0a0', 'it'), 'batty': ('Batty', '#8a8ad8', 'him'), 'eggbert': ('Eggbert', '#d8d4c0', 'him'), 'count': ('The Count', '#a8c8f0', 'him'), 'dragon': ('The Doodle Dragon', '#5ac048', 'him'), 'eraser': ('The Eraser', '#f08aa0', 'it'), 'cursor': ('The Cursor', '#cfe8ff', 'it'), 'inkblot': ('The Ink Blot', '#7a7aaa', 'it'), 'speech': ('The Speech Bubble', '#ffd060', 'it'), 'lightbringer': ('The Lightbringer', '#ffe08a', 'her'), 'dryad': ('The Pale Dryad', '#6aa8f0', 'her'), 'sovereign': ('The Bound Sovereign', '#d0182e', 'him'), 'vexis': ('Vexis, the Unlinked', '#7aff6a', 'it'), 'mireling': ('The Mireling', '#e0384a', 'it'), 'keeper': ('The Keeper of Bonds', '#ffd6f0', 'it'), 'pxcecil': ('8-Bit Cecil', '#b070ff', 'him'), 'pxleo': ('8-Bit Leo', '#4ab0ff', 'him'), 'pxemma': ('8-Bit Emma', '#ff6ac8', 'her'), 'sky': ('The Sky Buddies', '#ffd04a', 'them')}
HOME = {'emma': 'p98/home/emma', 'celi': 'p98/home/celi', 'zib': 'p98/home/zib', 'cecil': 'p98/home/cecil', 'kw': 'p98/home/killerwatt',
        'leo': 'p98/home/leo', 'demo': 'p98/home/demo', 'apo': 'p98/home/apo', 'tul': 'p98/home/tul', 'frog': 'p138/home/frog', 'don': 'p138/home/don',
        'pearl': 'p138/home/pearl', 'wil': 'p138/home/wil', 'fishy': 'p145/home',
        'dennis': 'p163/dw/home', 'pistachio': 'p163/pi/home', 'omega': 'p170/home', 'ashur': 'p185/home', 'chef': 'p186/home', 'neighbor': 'p187/home', 'ava': 'p189/home', 'pearlq': 'p190/home', 'bloo': 'p191/home', 'stalker': 'p193/home', 'lantern': 'p194/home', 'bender': 'p195/home', 'bones': 'p196/home', 'capshun': 'p198/home', 'kettle': 'p227/home', 'rufus': 'p228/home', 'henry': 'p229/home', 'nia': 'p230/home', 'gem': 'p231/home', 'batty': 'p232b/home', 'eggbert': 'p232e/home', 'count': 'p232c/home', 'dragon': 'p235d/home', 'eraser': 'p235e/home', 'cursor': 'p235c/home', 'inkblot': 'p235i/home', 'speech': 'p235b/home', 'lightbringer': 'p236l/home', 'dryad': 'p236p/home', 'sovereign': 'p239/home', 'vexis': 'p243/home', 'mireling': 'p252/home', 'keeper': 'p254/home', 'pxcecil': 'p213c/home', 'pxleo': 'p213l/home', 'pxemma': 'p213e/home', 'sky': 'p211/home'}
P28.MENU.update({f'wd_{w}': b for w, b in BASE.items()})


def _lum(p):
    return (0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) / 255


def _lumrange(ims):
    vals = [_lum(im.getpixel((x, y))) for im in ims.values() for y in range(im.height) for x in range(im.width) if im.getpixel((x, y))[3] > 0]
    return min(vals), max(vals)


def _recolour(ims, stops, rng=None):
    """recolour a set of cloth textures together: luminance (over the whole set's range - or `rng`, another set's) through dark - mid - light"""
    from gen_rp import hexc
    s = [hexc(c)[:3] for c in stops]
    lum = _lum
    lo, hi = rng or _lumrange(ims)
    out = {}
    for name, im in ims.items():
        o = im.copy()
        for y in range(im.height):
            for x in range(im.width):
                p = im.getpixel((x, y))
                L = min(1.0, max(0.0, (lum(p) - lo) / max(1e-6, hi - lo)))
                L = 0.15 + 0.75 * L
                c = tuple(int(s[0][i] + (s[1][i] - s[0][i]) * L / 0.5) for i in range(3)) if L < 0.5 else \
                    tuple(int(s[1][i] + (s[2][i] - s[1][i]) * (L - 0.5) / 0.5) for i in range(3))
                o.putpixel((x, y), c + (p[3],))
        out[name] = o
    return out


def textures():
    import phase96_art as LA, phase97_art as DA, phase45
    base = {'leo': LA.textures(), 'demo': DA.textures(), 'cecil': phase45.textures()}
    out = {}
    import gild
    for w, keys in RECOLOUR.items():
        for k, (_n, pal) in NEW[w][3].items():
            ims = {n: gild.dress(w, k, base[w][n]) for n in keys} if gild.is_gilded(w, k) else _recolour({n: base[w][n] for n in keys}, pal)   # (2.79a: polished gold)
            for name, im in ims.items():
                out[f'{name}_c{k}'] = im
            if gild.is_gilded(w, k):
                for n in ARMOUR.get(w, ()):
                    im = gild.metal(base[w][n], ramp=gild.steel(w, k), sheen=0 if n == 'le_mail' else 11, soften=n != 'le_mail')
                    if n.endswith('_dk'):                # (the dark steel stays darker: its trim and shadowed plates)
                        from PIL import Image
                        im = Image.merge('RGBA', [*[c.point(lambda v: int(v * 0.68)) for c in im.split()[:3]], im.split()[3]])
                    out[f'{n}_c{k}'] = im
    return out


def rp(R):
    import sys
    import phase97_art as DA
    R.TEXTURE_MODS.append(sys.modules[__name__])
    sel_items = {}                                   # a model whose part keeps its custom_model_data: the outfit picked by it
    import gild
    def worn(w, k):                                  # (the textures a look recolours: its cloth - and, the gilded look, Leo's steel)
        return RECOLOUR[w] + (ARMOUR.get(w, ()) if gild.is_gilded(w, k) else ())
    def swap(tex, w, k):
        return {a: (f'{v}_c{k}' if any(v == f'bm:block/{t}' for t in worn(w, k)) else v) for a, v in tex.items()}
    for w, prefix in (('leo', 'le_'), ('demo', 'dm_')):
        for name in [n for n in list(R.HATS) if n.startswith(prefix) and '_x' not in n and not n.startswith(prefix + 'head') and not n[len(prefix):].startswith('scythe')]:
            tex, els = R.HATS[name]
            ks = [k for k in NEW[w][3] if any(v == f'bm:block/{t}' for v in tex.values() for t in worn(w, k))]
            if not ks:
                continue
            sel_items[name] = []
            for k in ks:
                R.HATS[f'{name}_c{k}'] = (swap(tex, w, k), els)
                sel_items[name].append((f'c{k}', f'{name}_c{k}'))
        assert not any(v == f'bm:block/{t}' for v in R.HATS[f'{prefix}head'][0].values() for t in RECOLOUR[w]) or w == 'demo', w
    # Democratus' hood: a head model per cloak (his face and glowing eyes picked on it as on the plain one)
    heads = {}
    tex, els = R.HATS['dm_head']
    for k in NEW['demo'][3]:
        R.HATS[f'dm_head_c{k}'] = (swap(tex, 'demo', k), els)
        heads[f'dm_head_c{k}'] = []
        for e in DA.DEMO_EXPR:
            R.HATS[f'dm_head_c{k}_x{e}'] = (dict(swap(tex, 'demo', k), dm_face=f'bm:block/dm_face_{e}', dm_glow=f'bm:block/dm_glow_{e}'), els)
            heads[f'dm_head_c{k}'].append((e, f'dm_head_c{k}_x{e}'))
    # Cecil's own robe (worn when no gem is in him)
    for nm in ('head', 'arm', 'body', 'larm'):
        tex, els = R.HATS[f'cec2_{nm}']
        for k in NEW['cecil'][3]:
            R.HATS[f'cec2_{nm}_c{k}'] = (swap(tex, 'cecil', k), els)
    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        for name, cases in sel_items.items():
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                             'cases': [{'when': c, 'model': mdl(m)} for c, m in cases], 'fallback': mdl(name)}})
        for name, cases in heads.items():
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                             'cases': [{'when': e, 'model': mdl(m)} for e, m in cases], 'fallback': mdl(name)}})
        # (2.79b) Leo's head in his gilded look: his helm in diamond, every face of his on it (his face picks itself as on the plain head)
        import json, os
        for k in [k for k in NEW['leo'][3] if gild.is_gilded('leo', k)]:
            idef = json.load(open(R2.p('assets', 'bm', 'items', 'le_head.json')))['model']
            for m in ['le_head'] + [c['model']['model'].split('/')[-1] for c in idef.get('cases', [])]:
                src = json.load(open(R2.p('assets', 'bm', 'models', 'item', m + '.json')))
                src['textures'] = {a: (f'{v}_c{k}' if any(v == f'bm:block/{t}' for t in ARMOUR['leo']) else v) for a, v in src['textures'].items()}
                R2.wj(f'assets/bm/models/item/{m.replace("le_head", f"le_head_c{k}", 1)}.json', src)
            idef = json.loads(json.dumps(idef).replace('bm:item/le_head', f'bm:item/le_head_c{k}'))
            R2.wj(f'assets/bm/items/le_head_c{k}.json', {'model': idef})
    R.POST.append(post)


def groups():
    """(follower, group, current-look score, unlocked bits, {k: (name, colour)}, item, menu offset, apply (as you)) - also the Tailor's (phase103)"""
    return [('emma', 'ribbon', 'bm.cosr', 'bm.wur', {k: (n, c) for k, (n, c) in P78.RIBBONS.items()}, 'cos_ribbon_{}', 2, 'p78/emma_now'),
              ('emma', 'dress', 'bm.cosd', 'bm.wud', {k: (n, c) for k, (n, c, _c2) in P78.DRESSES.items()}, 'cos_dress_{}', 12, 'p78/emma_now'),
              ('emma', 'outfit', 'bm.coso', 'bm.wuo', dict(P89.OUTFITS), 'cos_outfit_{}', 22, 'p78/emma_now'),
              ('celi', 'celi', 'bm.cosc', 'bm.wuc', {k: (n, c) for k, (n, c, _c2) in P78.CELI.items()}, 'cos_celi_{}', 2, 'p78/celi_now'),
              ('zib', 'zib', 'bm.cosz', 'bm.wuz', dict(P78.ZIB), 'cos_zib_{}', 2, 'p78/zib_now')] + \
             [(w, w, COS[w], f'bm.wu{w}',
               {k: (n, pal[1]) for k, (n, pal) in NEW[w][3].items()}, f'cos_{w}_{{}}', 2, f'p99/{w}_now') for w in NEW]


def generate(G):
    import gild
    import phase57 as P57
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = PREFIX
    PINK = P78.PINK
    # groups: (follower, group, current-look score, unlocked bits, {k: (name, colour)}, item, menu offset, apply (as you))
    GROUPS = groups()
    objs = sorted({g[2] for g in GROUPS} | {g[3] for g in GROUPS})
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += [o for o in objs if o not in G.OBJECTIVES]
    def bit(obj, k):
        return [f'scoreboard players operation #q bm.rng = @s {obj}', f'scoreboard players set #bit bm.rng {2 ** k}',
                'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']

    # ================================================================== unlocking: a cosmetic used once is in the wardrobe for good
    for who, g, cur, un, ks, iid, off, apply in GROUPS:
        for k in ks:
            fn(f'p99/unlock/{g}{k}', [f'execute unless score @s {un} matches 0.. run scoreboard players set @s {un} 0'] + bit(un, k) +
               ['execute if score #q bm.rng matches 1 run return 0', f'scoreboard players add @s {un} {2 ** k}',
                f'clear @s *[minecraft:custom_data~{{bm:"{iid.format(k)}"}}] 1', 'playsound minecraft:item.armor.equip_leather player @s ~ ~ ~ 1 1.2',
                tellraw('@s', P + [T(ks[k][0], ks[k][1], bold=True), T(f' is in {NAMES[who][0]}\'s wardrobe for good. ', 'gray'),
                                   T(f"(Sneak + use {({'him': 'his', 'it': 'its', 'them': 'their'}).get(NAMES[who][2], NAMES[who][2])} item to change any time.)", 'dark_gray')])])
    old_use = {'ribbon': 'p78/use/ribbon{}', 'dress': 'p78/use/dress{}', 'outfit': 'p89/use/outfit{}', 'celi': 'p78/use/celi{}', 'zib': 'p78/use/zib{}'}
    for who, g, cur, un, ks, iid, off, apply in GROUPS:
        for k in ks:
            if g in old_use:
                L = G.FUNCS[old_use[g].format(k)]
                j = next(n for n, l in enumerate(L) if l.startswith('scoreboard players set @s bm.gvhc'))
                L.insert(j + 1, f'function bm:p99/unlock/{g}{k}')
            else:
                fn(f'p99/use/{g}{k}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                                       'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', f'function bm:p99/unlock/{g}{k}',
                                       f'scoreboard players set @s {cur} {k}', f'function bm:{apply}'])

    # ================================================================== putting it on (as you)
    # Leo and Democratus: every part but the head picks its outfit by custom_model_data; Democratus' hood by its model
    for w, sel, part, head in (('leo', 'bm.lesel', 'bm.lep', 'bm.lp_head'), ('demo', 'bm.dmsel', 'bm.dmp', 'bm.dp_head')):
        cur = next(g[2] for g in GROUPS if g[0] == w)
        fn(f'p99/{w}_dress', ['scoreboard players set #wc bm.rng 0',
                              f'execute store result score #wp bm.rng run scoreboard players get @e[type=minecraft:item_display,tag={sel},limit=1] bm.pid',
                              f'execute as @a if score @s bm.pid = #wp bm.rng run scoreboard players operation #wc bm.rng = @s {cur}',
                              f'execute if score #wc bm.rng matches 0 as @e[type=minecraft:item_display,tag={sel}{",tag=!" + head if head else ""}] run data remove entity @s item.components."minecraft:custom_model_data"'] +
           [f'execute if score #wc bm.rng matches {k} as @e[type=minecraft:item_display,tag={sel}{",tag=!" + head if head else ""}] run data modify entity @s item.components."minecraft:custom_model_data" set value {{strings:["c{k}"]}}'
            for k in NEW[w][3]] +
           ([f'execute if score #wc bm.rng matches 0 run data modify entity @e[type=minecraft:item_display,tag={sel},tag={head},limit=1] item.components."minecraft:item_model" set value "bm:dm_head"'] +
            [f'execute if score #wc bm.rng matches {k} run data modify entity @e[type=minecraft:item_display,tag={sel},tag={head},limit=1] item.components."minecraft:item_model" set value "bm:dm_head_c{k}"'
             for k in NEW[w][3]] if w == 'demo' else
            # (Leo's head: his face stays his own - but in the gilded look his helm is diamond)
            [f'data modify entity @e[type=minecraft:item_display,tag={sel},tag={head},limit=1] item.components."minecraft:item_model" set value "bm:le_head"'] +
            [f'execute if score #wc bm.rng matches {k} run data modify entity @e[type=minecraft:item_display,tag={sel},tag={head},limit=1] item.components."minecraft:item_model" set value "bm:le_head_c{k}"'
             for k in NEW['leo'][3] if gild.is_gilded('leo', k)]))
        G.FUNCS[f'p{96 if w == "leo" else 97}/grow'].append(f'function bm:p99/{w}_dress')
        excl = ',tag=!bm.dmencp,tag=!bm.dmbp,tag=!bm.dmfade' if w == 'demo' else ',tag=!bm.lefade,tag=!bm.leencp'
        fn(f'p99/{w}_now', ['scoreboard players operation #me bm.pid = @s bm.pid',
                            f'execute as @e[type=minecraft:item_display,tag={part}{excl}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                            f'execute unless entity @e[tag={sel}] run return run ' + say(f'{NAMES[w][0]} isn\'t with you - he\'ll wear it next time.', NAMES[w][1]),
                            f'function bm:p99/{w}_dress', f'execute at @e[type=minecraft:item_display,tag={sel},limit=1] run particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.02 14',
                            f'tag @e[tag={sel}] remove {sel}'])
    # Cecil: his own robe (no gem in him)
    cur_c = next(g[2] for g in GROUPS if g[0] == 'cecil')
    G.FUNCS['p46/pet/dress'] += ['scoreboard players set #wc bm.rng 0', f'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #wc bm.rng = @s {cur_c}'] + \
        [f'execute if score #el bm.rng matches 0 if score #wc bm.rng matches {k} as @e[type=minecraft:item_display,tag=bm.cpet,tag=bm.cp_{nm}] if score @s bm.pid = #me bm.pid '
         f'run data modify entity @s item.components."minecraft:item_model" set value "bm:cec2_{nm}_c{k}"' for k in NEW['cecil'][3] for nm in ('head', 'arm', 'body', 'larm')]
    fn('p99/cecil_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'execute unless score @s bm.cpel matches 0.. run scoreboard players set @s bm.cpel 0',
                         'scoreboard players operation #el bm.rng = @s bm.cpel', 'function bm:p46/pet/dress',
                         'execute if score @s bm.cpel matches 1.. run ' + say('With a gem in him Cecil wears its colours - he\'ll wear his robe when it\'s out.', '#b48cff')])
    # KillerWatt: his own colours (no gem in him) - #kcos beside #kel, wherever his parts are dressed
    cur_k = next(g[2] for g in GROUPS if g[0] == 'kw')
    SUFS = [('armr', '_flex'), ('arml', '_flex')]
    for f_, parts in (('p79/pet/dress_rig', [(p, '') for p in KA.PARTS]), ('p79/flex', SUFS), ('p79/unflex', [('armr', ''), ('arml', '')])):
        L = G.FUNCS[f_]
        L += [f'execute if score #kel bm.rng matches 0 if score #kcos bm.rng matches {k} run data modify entity @e[type=minecraft:item_display,tag=bm.kxsel,tag=bm.kxp_{p},limit=1] '
              f'item.components."minecraft:item_model" set value "bm:kw_{p}{s}_c{k}"' for k in NEW['kw'][3] for p, s in parts]
    G.FUNCS['p79/pet/dress_rig'].insert(0, f'scoreboard players set #kcos bm.rng 0')
    G.FUNCS['p79/pet/dress_rig'].insert(1, f'execute on owner run scoreboard players operation #kcos bm.rng = @s {cur_k}')
    G.FUNCS['p79/pet/tick'][0:0] = ['scoreboard players set #kcos bm.rng 0', f'execute on owner run scoreboard players operation #kcos bm.rng = @s {cur_k}']
    G.FUNCS['p79/boss/tick'].insert(0, 'scoreboard players set #kcos bm.rng 0')
    G.FUNCS['p79/orphan'].insert(0, 'scoreboard players set #kcos bm.rng 0')
    fn('p99/kw_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                      'execute as @e[type=minecraft:wolf,tag=bm.kxpet] if score @s bm.pid = #me bm.pid at @s run function bm:p99/kw_now2',
                      'execute if score #has bm.rng matches 0 run return run ' + say('KillerWatt isn\'t with you - he\'ll wear it next time.', '#ffe040'),
                      'execute if score @s bm.kxel matches 1.. run ' + say('With a gem in him KillerWatt shows its element - his colours come back when it\'s out.', '#ffe040')])
    fn('p99/kw_now2', ['scoreboard players set #has bm.rng 1', 'function bm:p79/pet/redress', 'particle minecraft:electric_spark ~ ~1.5 ~ 0.6 1 0.6 0.3 30'])

    # ================================================================== the menus (sneak + use the follower's item)
    for who in BASE:
        b = BASE[who]
        nm, col, pron = NAMES[who]
        mine = [g for g in GROUPS if g[0] == who]
        page = [f'scoreboard players set @s bm.menu {b}', 'data remove storage bm:ui wd']
        st = lambda key, txt, c: f'data modify storage bm:ui wd.r_{key} set value {snbt(T(txt, c, bold=True))}'
        btns = [P28.btn([T(f'Send {pron} home', 'gray')], b, width=150)]
        for _w, g, cur, un, ks, iid, off, apply in mine:
            page += [f'execute unless score @s {un} matches 0.. run scoreboard players set @s {un} 0', f'execute unless score @s {cur} matches 0.. run scoreboard players set @s {cur} 0']
            for k in ks:              # (one already worn - from before the wardrobe - counts as owned)
                page += [f'execute if score @s {cur} matches {k} run function bm:p99/own/{g}{k}']
                fn(f'p99/own/{g}{k}', bit(un, k) + [f'execute if score #q bm.rng matches 0 run scoreboard players add @s {un} {2 ** k}'])
            orig = {'ribbon': 'Pink ribbon', 'dress': 'Her own dress', 'outfit': None}.get(g, 'Own clothes' if who not in ('cecil', 'kw') else 'Own colours')
            orig = {'apo': 'His own scales', 'tul': 'His old coat', 'frog': 'His own skin', 'don': 'His own coat', 'pearl': 'The blue bow tie',
                    'wil': 'No shield', 'fishy': 'His old black topper', 'dennis': 'His old black leather', 'pistachio': 'His charcoal tails', 'omega': 'His own grey ghost', 'ashur': 'Her own magma', 'chef': 'His spotless whites', 'neighbor': 'His sailor whites', 'ava': 'Her royal blue', 'pearlq': 'Her own aqua', 'bloo': 'His own wild blue', 'stalker': 'Its own sickly olive', 'lantern': 'Its own pumpkin orange', 'bender': 'His own fawn', 'bones': 'His own shark grey', 'capshun': 'Plain black ink', 'kettle': 'Plain pencil', 'rufus': 'His red bandana', 'henry': 'His red collar', 'nia': 'Her lilac collar', 'gem': 'Its own colours', 'batty': 'His own navy fur', 'eggbert': 'His own black ooze', 'count': 'His red-banded topper', 'dragon': "Kettle's own green", 'eraser': 'Classic pink', 'cursor': 'Classic white', 'inkblot': 'Black ink', 'speech': 'Plain white', 'lightbringer': 'Pearl and gold', 'dryad': 'Pale Garden blue', 'sovereign': 'Void plate', 'vexis': 'Hive red', 'mireling': 'Blood-red veins', 'keeper': 'Cream and gold', 'pxcecil': 'Sixteen colours', 'pxleo': 'Sixteen colours', 'pxemma': 'Sixteen colours', 'sky': "Snooze's old blue"}.get(g, orig)
            if orig:
                page += [st(f'{g}0', 'owned', 'gray'), f'execute if score @s {cur} matches 0 run {st(f"{g}0", "wearing", GOLD)}']
                if g == 'dress':
                    page += [f'execute unless score @s bm.coso matches 0 run {st(f"{g}0", "owned", "gray")}']
                btns.append(P28.btn([T(orig, 'white', bold=True), T('  '), f'@@RAW:r_{g}0@@'], b + off, width=150))
            for k, (cn, cc) in ks.items():
                page += [st(f'{g}{k}', 'locked', 'dark_gray')] + bit(un, k) + [f'execute if score #q bm.rng matches 1 run {st(f"{g}{k}", "owned", "gray")}',
                                                                               f'execute if score @s {cur} matches {k} run {st(f"{g}{k}", "wearing", GOLD)}']
                if g == 'dress':
                    page += [f'execute if score @s {cur} matches {k} unless score @s bm.coso matches 0 run {st(f"{g}{k}", "owned", "gray")}']
                btns.append(P28.btn([T(cn, cc, bold=True), T('  '), f'@@RAW:r_{g}{k}@@'], b + off + k, width=150))
        # 2.82t: comes back after fainting - on unless switched off here (phase173: after the 2-minute cooldown, by itself)
        import phase173 as P173
        if who in P173.AR:
            page += [st('ar', 'on', GOLD)] + bit(P173.ar_obj(P173.AR_IDX[who]), P173.AR_IDX[who] % 31) + [f'execute if score #q bm.rng matches 1 run {st("ar", "off", "gray")}']
            btns.append(P28.btn([T('Back after a faint', 'white', bold=True), T('  '), '@@RAW:r_ar@@'], P173.ar_code(P173.AR_IDX[who]), width=150,
                                tooltip=T(f'On: once the 2-minute rest after a faint is over, {nm} comes back to you.', 'gray')))
        # 2.78: the aura row - locked until you have it (a rare heist find, or dear at the Tailor), then on / off
        import phase138 as P138
        an, ac = P138.AURA[who][0], P138.AURA[who][1]
        page += [st('aura', 'locked', 'dark_gray'), f'execute if entity @s[tag=bm.auown_{who}] run {st("aura", "off", "gray")}',
                 f'execute if entity @s[tag=bm.au_{who}] run {st("aura", "on", GOLD)}']
        used = {b} | {b + off + k for _w, g, cur, un, ks, iid, off, apply in mine for k in [0] + list(ks)}
        assert TOP[who] not in used, (who, TOP[who])
        btns.append(P28.btn([T(an, ac, bold=True), T('  '), '@@RAW:r_aura@@'], TOP[who], width=150,
                            tooltip=T(f'{an}: a rare aura around {nm} - a heist find, or the Tailor\'s dearest stock. On or off here.', 'gray')))
        # 2.94b: the pixel costume row (a Glitched Cartridge used beside them unlocks it) - locked, then on / off, here in
        #        their own wardrobe (it had a Pixel Wardrobe of its own, off the cartridge)
        import phase214 as P214
        if who in P214.KEYS:
            assert TOP[who] - 1 not in used, (who, TOP[who] - 1)
            page += [st('px', 'locked', 'dark_gray'), f'execute if entity @s[tag=bm.pxu_{who}] run {st("px", "off", "gray")}',
                     f'execute if entity @s[tag=bm.pxu_{who},tag=bm.pxo_{who}] run {st("px", "on", P214.COL)}']
            btns.append(P28.btn([T('Pixel costume', P214.COL, bold=True), T('  '), '@@RAW:r_px@@'], TOP[who] - 1, width=150,
                                tooltip=T(f'{nm} as a PixelLab sprite. Unlocked by using a Glitched Cartridge beside {pron}. On or off here.', 'gray')))
        # 2.94m: Emma's KillerWatt look (an Easter egg - KillerWatt called while she's with you unlocks it, phase217) - locked, off, on
        if who == 'emma':
            assert TOP[who] - 2 not in used, (who, TOP[who] - 2)
            page += [st('kw', '???', 'dark_gray'), f'execute if entity @s[tag=bm.emkw_u] run {st("kw", "off", "gray")}',
                     f'execute if entity @s[tag=bm.emkw_u,tag=bm.emkw_o] run {st("kw", "on", "#7ae63a")}']
            btns.append(P28.btn([T('KillerWatt look', '#7ae63a', bold=True), T('  '), '@@RAW:r_kw@@'], TOP[who] - 2, width=150,
                                tooltip=T('Emma, marked glassy green by a possession she threw off - his colours, his tendrils. A secret: how do you get it?', 'gray')))
        page.append(f'function bm:p99/dlg/{who} with storage bm:ui wd')
        fn(f'p99/menu/{who}', page)
        dlg = P28.multi([T(f"{nm}", col, bold=True), T('  ·  wardrobe', 'gray')],
                        [P28.body([T('Every outfit you\'ve used is ' + pron + 's for good. Pick one any time - ', 'gray'),
                                   T('locked', 'dark_gray', bold=True), T(' ones are sold by Goldtooth in the vault (the hidden ones for a Gutter Trophy).', 'gray')] +
                                  ([T(' With a gem in him, the gem\'s element shows instead.', 'dark_gray')] if who in ('cecil', 'kw') else []), 330)],
                        btns, columns=3 if who == 'emma' else 2, exit_label='Close')
        fn(f'p99/dlg/{who}', [f'$dialog show @s {P28.inline(dlg)}'])
        # the clicks
        lines = [f'execute unless score @s bm.menu matches {b} run return run function bm:p28/stale',
                 'scoreboard players operation #me bm.pid = @s bm.pid',
                 f'execute if score #act bm.pay matches {b} run return run function bm:{HOME[who]}',
                 f'execute if score #act bm.pay matches {TOP[who]} run return run function bm:p138/au/t_{who}']
        if who in P214.KEYS:
            lines.append(f'execute if score #act bm.pay matches {TOP[who] - 1} run return run function bm:p214/t/{who}')
        if who == 'emma':
            lines.append(f'execute if score #act bm.pay matches {TOP[who] - 2} run return run function bm:p217/kw/t')
        for _w, g, cur, un, ks, iid, off, apply in mine:
            if g != 'outfit':
                fn(f'p99/pick/{g}0', [f'scoreboard players set @s {cur} 0'] + (['scoreboard players set @s bm.coso 0'] if g == 'dress' else []) +
                   [f'function bm:{apply}', f'function bm:p99/menu/{who}'])
                lines.append(f'execute if score #act bm.pay matches {b + off} run return run function bm:p99/pick/{g}0')
            for k, (cn, cc) in ks.items():
                fn(f'p99/pick/{g}{k}', bit(un, k) + [f'execute if score #q bm.rng matches 0 run return run ' +
                                                     say(f'{cn} is locked - Goldtooth sells it in the vault' + (' (hidden: a Gutter Trophy).' if iid.format(k) in P78.HIDDEN or (who in NEW and k == HIDDEN) else '.'), cc)] +
                   [f'scoreboard players set @s {cur} {k}'] + (['scoreboard players set @s bm.coso 0'] if g == 'dress' else []) +
                   [f'function bm:{apply}', f'function bm:p99/menu/{who}'])
                lines.append(f'execute if score #act bm.pay matches {b + off + k} run return run function bm:p99/pick/{g}{k}')
        fn(f'p99/act/{who}', lines)
    # (2.78: each follower's own block, routed exactly - the new ones sit at 9000-9119, away from the old run)
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {b}..{TOP[w]} run return run function bm:p99/act/{w}' for w, b in BASE.items()]
    # sneak + use: the menu (KillerWatt: not while riding him - that's his Thunder Leap)
    sneak = lambda who: f'execute if predicate bm:p20/sneaking run return run function bm:p99/menu/{who}'
    for f_, who in (('p46/pet/use', 'cecil'), ('p66/use', 'celi'), ('p72/zb/use', 'zib'), ('p96/use', 'leo')):
        L = G.FUNCS[f_]
        j = next(n for n, l in enumerate(L) if l == 'scoreboard players operation #me bm.pid = @s bm.pid')
        L.insert(j + 1, sneak(who))
    L = G.FUNCS['p79/spark']
    j = next(n for n, l in enumerate(L) if 'p79/pet/rleap' in l)
    L.insert(j + 1, sneak('kw'))
    L = G.FUNCS['p57/use']                     # Emma: out - her buff menu (its Wardrobe button); not out - her wardrobe
    j = next(n for n, l in enumerate(L) if 'unless entity @e[type=minecraft:cat,tag=bm.emsel2] if predicate bm:p20/sneaking' in l)
    L[j] = 'execute unless entity @e[type=minecraft:cat,tag=bm.emsel2] if predicate bm:p20/sneaking run function bm:p99/menu/emma'
    G.FUNCS['p57/act'].insert(2, 'execute if score #act bm.pay matches 7306 run return run function bm:p99/menu/emma')

    # ================================================================== Goldtooth sells the new ones (Gutter Medallions; the hidden ones a Gutter Trophy)
    import phase70 as P70
    from gen_dp import offer
    prev = P70.goldtooth
    def g99():
        d = prev()
        for w in NEW:
            for k in [k for k in NEW[w][3] if not _SH.is_shiny(f'cos_{w}_{k}')]:
                d['Offers']['Recipes'].append(offer(gild.price(f'cos_{w}_{k}', ('gutter_trophy', 1) if k == HIDDEN else ('gutter_medallion', 4)), (f'cos_{w}_{k}', 1)))
        return d
    P70.goldtooth = g99
    L = G.FUNCS['p70/r/lobby/init']
    L[:] = [l.replace(snbt(prev()), snbt(g99())) if 'bm.gvgt' in l and 'summon minecraft:villager' in l else l for l in L]
    assert any(snbt(g99()) in l for l in L), "Goldtooth's summon wasn't found to add the wardrobe"
    fn('admin/wardrobe_all', [f'scoreboard players set @s {g[3]} {sum(2 ** k for k in g[4])}' for g in GROUPS] +
       [tellraw('@s', P + [T('Every follower outfit unlocked.', 'gray')])])
    fn('admin/wardrobe_items', [give(f'cos_{w}_{k}') for w in NEW for k in NEW[w][3]])

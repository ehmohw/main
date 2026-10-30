"""2.94t: SHINY FOLLOWERS - a rare colouring of each follower, like a shiny in Pokemon.

Each follower has one SHINY look: their own outfit (or hide, or fur) in a palette of its own, never sold anywhere. It goes in
their wardrobe as the next look after their netherite one, and is made exactly as their other recolours are - so every
follower's own machinery (textures, models, poses, faces) wears it. How it's found: phase221 (one summon in SHINY_ODDS: they
turn up trying something new today - and from then on it's in their wardrobe for good).
This module only holds the looks; phase99 / phase78 / phase79_art / phase138 read it as they build their wardrobes."""

SHINY_ODDS = 100                 # one summon in this many (a follower whose shiny look you have already rolls no more)

# follower: (name, (dark, mid, light), dye for the item's look)
LOOKS = {
    'leo': ('Shiny Rosegold', ('#3a1a1a', '#c87a6a', '#ffd0c0'), 'pink'),
    'demo': ('Shiny Ghost Teal', ('#062626', '#2aa0a0', '#b0fff0'), 'cyan'),
    'cecil': ('Shiny Sunset', ('#2a0e04', '#d0701a', '#ffc080'), 'orange'),
    'apo': ('Shiny Albino', ('#5a4a4a', '#e8d8d0', '#fffaf4'), 'white'),
    'tul': ('Shiny Sea Glass', ('#062a1a', '#3ab08a', '#c0ffe8'), 'cyan'),
    'frog': ('Shiny Bubblegum', ('#3a0a2a', '#e05ab0', '#ffc0e8'), 'pink'),
    'don': ('Shiny Strawberry', ('#2a0610', '#c84a6a', '#ffb8c8'), 'pink'),
    'pearl': ('Shiny Magenta', ('#2a0620', '#d040a0', '#ffa8e8'), 'magenta'),
    'fishy': ('Shiny Silver', ('#2a2a30', '#a8a8b4', '#f4f4ff'), 'light_gray'),
    'wil': ('Shiny Rose Heraldry', ('#3a0a2a', '#e05ab0', '#ffc0e8'), 'pink'),
    'dennis': ('Shiny Electric Blue', ('#04102a', '#2a6ad0', '#a8d0ff'), 'blue'),
    'pistachio': ('Shiny Rose Tails', ('#2a0612', '#b03a5a', '#ffb0c8'), 'pink'),
    'omega': ('Shiny Ember Wraith', ('#2a0a04', '#d0601a', '#ffc890'), 'orange'),
    'ashur': ('Shiny Pink Flame', ('#2a0420', '#e04ab0', '#ffc8f0'), 'magenta'),
    'chef': ('Shiny Mint Whites', ('#0a2a1e', '#6ad0a8', '#e0fff4'), 'lime'),
    'neighbor': ('Shiny Sunshine', ('#2a1e04', '#e0b42a', '#fff0a8'), 'yellow'),
    'ava': ('Shiny Rose Tide', ('#2a0614', '#d05a8a', '#ffc8dc'), 'pink'),
    'pearlq': ('Shiny Mint Sorbet', ('#062a20', '#4ad0a8', '#d0fff0'), 'lime'),
    'bloo': ('Shiny Rose Pelt', ('#2a0618', '#c84a8a', '#ffb8d8'), 'pink'),
    'stalker': ('Shiny Toxic', ('#0a2004', '#5ac81a', '#d0ff8a'), 'lime'),
    'lantern': ('Shiny Moonlit Rind', ('#0a0e2a', '#5a6ad0', '#d0d8ff'), 'blue'),
    'bender': ('Shiny Blue Merle', ('#14181e', '#6a7a8a', '#d0dce8'), 'light_gray'),
    'bones': ('Shiny Tiger', ('#2a1604', '#c87a2a', '#ffd090'), 'orange'),
    'gem': ('Shiny Prismatic', ('#200a3a', '#ff6ae0', '#fff6a0'), 'magenta'),
    'batty': ('Shiny Golden Wings', ('#3a2806', '#d0a030', '#ffe8a0'), 'yellow'),
    'eggbert': ('Shiny Starlight Ooze', ('#0a0a3a', '#4a6ae0', '#c0d8ff'), 'blue'),
    'count': ('Shiny Silver Topper', ('#2a2a30', '#a8a8b4', '#f4f4ff'), 'light_gray'),
    'dragon': ('Shiny End Stone', ('#4a4232', '#d6cf98', '#fffbe4'), 'yellow'),      # (3.0a: the Doodle Ender Dragon - pale as End stone, eyes still purple)
    'eraser': ('Shiny Glitter Eraser', ('#1a1a3a', '#9a8ad8', '#f0e8ff'), 'purple'),
    'cursor': ('Shiny Golden Pointer', ('#3a2806', '#e0b03a', '#fff4b0'), 'yellow'),
    'inkblot': ('Shiny Galaxy Ink', ('#0a0420', '#4a2ab0', '#c0b0ff'), 'purple'),
    'speech': ('Shiny Comic Pop', ('#3a0a04', '#ff6a2a', '#ffe8a0'), 'orange'),
    'lightbringer': ('Shiny Starlit Raiment', ('#0a0a2a', '#6a7ae0', '#e8f0ff'), 'light_blue'),
    'dryad': ('Shiny Moonglow Cap', ('#06202a', '#3ad0c0', '#c8fff4'), 'cyan'),
    'sovereign': ("Shiny Aurel's Light", ('#3a2c10', '#f0d070', '#fffaf0'), 'yellow'),
    'vexis': ('Shiny Starlit', ('#1a2a4a', '#6ab0ff', '#e8f4ff'), 'light_blue'),
    'mireling': ('Shiny Bone Mire', ('#5a5246', '#cdc3ad', '#ffcc3a'), 'white'),
    'keeper': ('Shiny Starweave', ('#100c34', '#5a4ac8', '#e4dcff'), 'purple'),
    'henry': ('Shiny Starlit Collar', ('#0a0a3a', '#6a6ae0', '#e0e0ff'), 'blue'),
    'nia': ('Shiny Rainbow Collar', ('#3a1a4a', '#e08ad8', '#fff0c0'), 'pink'),
    'rufus': ('Shiny Gold Bandana', ('#3a2806', '#e0b030', '#fff0a0'), 'yellow'),
    'kettle': ('Shiny Sidewalk Chalk', ('#3a0a2a', '#ff7ac8', '#ffe0f4'), 'pink'),
    'capshun': ('Shiny Purple Crayon', ('#200630', '#8a3ad0', '#e0b0ff'), 'purple'),
    'sky': ('Shiny Sherbet', ('#3a1a04', '#ff9a4a', '#ffe0b0'), 'orange'),
    'pxemma': ('Shiny Neon Arcade', ('#14002a', '#ff2ab0', '#7affff'), 'magenta'),
    'pxleo': ('Shiny Neon Arcade', ('#14002a', '#ff2ab0', '#7affff'), 'magenta'),
    'pxcecil': ('Shiny Neon Arcade', ('#14002a', '#ff2ab0', '#7affff'), 'magenta'),
}
KW = ('Shiny Ultraviolet', (('#12041e', '#5a1aa0', '#c08aff'), ('#ff6ad8', '#ffe0f8')))
EMMA = ('Shiny Lilac Gown', '#c8a0ff', '#a07ae0')            # (her dresses: the cloth's two colours)
CELI = ('Shiny Rose Frost', '#ff8ad8', '#e060b0')
ZIB = ('Shiny Magenta Ace', '#e04ab0')
FROG_SKIN = ('pink_wool', 'magenta_wool')                    # (his skin is wool - the light and the dark)
WIL_SHIELD = ('pink', [('flower', 'white'), ('border', 'magenta')])

KEY = {}                          # follower -> its shiny look's number (filled as the wardrobes take them)


def extend_new(NEW, DYE):
    """(phase99) each follower in NEW gets the next look: their shiny one"""
    for w, (nm, pal, dye) in LOOKS.items():
        if w not in NEW: continue
        k = max(NEW[w][3]) + 1
        NEW[w][3][k] = (nm, pal)
        KEY[w] = k
        DYE[nm] = dye
    KEY['kw'] = max(NEW['kw'][3])              # (KillerWatt's was put in his colours already: phase79_art)
    DYE[KW[0]] = 'purple'


def extend_78(P78):
    """(phase78) Emma's dress, Celi's outfit, Zib's uniform"""
    k = max(P78.DRESSES) + 1; P78.DRESSES[k] = EMMA; KEY['emma'] = k; P78.HIDDEN.add(f'cos_dress_{k}'); P78.DYE[EMMA[0]] = 'purple'
    k = max(P78.CELI) + 1; P78.CELI[k] = CELI; KEY['celi'] = k; P78.HIDDEN.add(f'cos_celi_{k}'); P78.DYE[CELI[0]] = 'pink'
    k = max(P78.ZIB) + 1; P78.ZIB[k] = ZIB; KEY['zib'] = k; P78.HIDDEN.add(f'cos_zib_{k}'); P78.DYE[ZIB[0]] = 'magenta'


def item_of(w):
    """the shiny look's cosmetic item"""
    return {'emma': 'cos_dress_{}', 'celi': 'cos_celi_{}', 'zib': 'cos_zib_{}'}.get(w, 'cos_' + w + '_{}').format(KEY[w])


def is_shiny(iid):
    return any(item_of(w) == iid for w in KEY)

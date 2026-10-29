"""2.99a: THE BACKPACK - a plain 27-slot bag for the road and the dungeons (the Fence, 5 Tokens).

The Vacuum Satchel's storage half on its own: no vacuum, no filter. Each backpack is its own bag (its contents ride in the
item, in its own minecraft:container), so several can be carried, each with its own load.

USE        right-click (or sneak + right-click: the same): it unfolds into a barrel in front of you - phase33's boxes, as the
           satchel, the Prime Cooler and the collectors do it (the item is held in storage while it's out, its contents moved
           into the barrel, and back into the item when it folds). It folds when you sneak, walk 6+ blocks off, after five
           minutes, or when you open another bag. Using a second backpack folds the first.
DUNGEONS   the Phase 2 dungeons (the seven overworld ones, the Hollow Throne, the Undercrown, the Vorn Armada), where the
           satchel won't unfold: there it unfolds only into plain air (or cave air) over solid floor, never within 2 blocks
           of the dungeon's own fixtures (its markers: puzzle pieces, doors, gates, sigils, bridges, vaults, spawners), and
           folding back puts back exactly that air. Not on a heist (the coat check keeps your pack in the gutter) and not
           in the markets, the crypts or aboard the Vorn ships - the satchel's rule (phase37's p37/allowed).
SAFE       while a backpack is out, its marker keeps a copy of the barrel's contents every tick (data.snap). If the barrel is
           taken away without a player - a dungeon rebuild, a reset or a door setting its block back, any command - the
           backpack folds with what was in it, from that copy; if it was broken (an explosion), the drops it spilled this
           tick are taken off the ground, so nothing is doubled. Before the Undercrown, the Armada or the Hollow Throne is
           rebuilt, every open bag in it is folded into its copy and its barrel taken away (its owner gets it back the
           moment they're online - their marker isn't one the rebuild clears).
NO NESTING a bag (a backpack, the Vacuum Satchel, the Prime Cooler, Dennis's Ore Magnet, Pistachio's Spirit Jar) put into an
           open bag's barrel is handed straight back to its owner; one still inside when a bag folds is handed back
           instead of packed; and the satchel's pick-up never swallows one."""
from items import item, T, TOTEM, DYNAMIC
from useitem import hold, HOLD
import economy as ECON

ITEM = 'backpack'
COL = '#c08a52'
PRICE = ('token', 5)
ECON.DIRECT[ITEM] = (PRICE, None)              # (a final price: not run through the market's rescale)
BAGS = ('backpack', 'vacuum_satchel', 'prime_cooler', 'ore_magnet', 'spirit_jar')
BAG = '*[' + '|'.join(f'minecraft:custom_data~{{bm:"{b}"}}' for b in BAGS) + ']'
MARK_R = 2                                     # (no dungeon fixture - a marker - within this of the barrel's cell)

item(ITEM, TOTEM, 'Backpack', COL,
     ['A sturdy leather pack for the road and the deep.', ('Right-click: it unfolds into a barrel', 'blue'),
      ('(27 slots) in front of you. Sneak or walk', 'blue'), ('away and it packs back up, all inside.', 'blue'),
      ('Works in the dungeons too - on open floor.', 'blue'), ('Carry as many as you like: each one', 'blue'),
      ('keeps its own load.', 'blue'), ('No bags inside bags.', 'gray')],
     model=f'bm:{ITEM}', stack=1, cat='builder', comps=dict(hold('bundle'), **{'minecraft:container': []}), price=PRICE)
DYNAMIC.add(ITEM)
HOLD[ITEM] = 'bm:p248/use'


def extend_offers(O, offer):
    O['fence'].append(offer(PRICE, (ITEM, 1)))


# ===================================================================== the icon
FLAP = ['#a87444', '#c8945c', '#e2b47a']                 # (the flap: a paler, oiled leather - shadow, face, lit edge)
BODY = ['#2e1a0e', '#4a2c18', '#6a4024', '#8a5832']      # (the pack: darkest, dark, face, lit side)
STRAP = '#3a2010'
ROLL = ['#4a1a18', '#7a2a22', '#a8442f', '#cc6a4c']
BRASS = ['#8a5a14', '#e0b030', '#fff0a0']
ROWS = ['................',
        '................',
        '......jiij......',
        '..rtvvvvvvvvtr..',
        '.rstattttttatsr.',
        '.rrsassssssasrr.',
        '...eeeeeeeeed...',
        '...eddddddddc...',
        '..hedddbbdddcj..',
        '..hadddbbdddaj..',
        '..hiaawyygaajj..',
        '..hiiiybbgiijj..',
        '..hijjjbbjjjjj..',
        '..jihhhbbhhhjj..',
        '...ajjjjjjjja...',
        '................']
assert all(len(r_) == 16 for r_ in ROWS)


def icon():
    """a 16 x 16 leather adventurer's pack, front on: a carry loop, a rolled blanket strapped on top, the flap with its
    brass buckle on the centre strap, side pockets, a front pocket - in sprites280's look (outlined, lit from the top left;
    gen_rp's vanilla.process finishes it)"""
    from sprites280 import S
    pal = dict(a=BODY[0], j=BODY[1], i=BODY[2], h=BODY[3], b=STRAP, c=FLAP[0], d=FLAP[1], e=FLAP[2],
               r=ROLL[0], s=ROLL[1], t=ROLL[2], v=ROLL[3], g=BRASS[0], y=BRASS[1], w=BRASS[2])
    s = S().g(ROWS, pal)
    im = s.image()
    px = im.load()
    add = [(x, y) for y in range(16) for x in range(16) if px[x, y][3] == 0 and
           any(0 <= x + dx < 16 and 0 <= y + dy < 16 and px[x + dx, y + dy][3] > 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in add:
        px[x, y] = (18, 14, 14, 255)
    return im


def rp(R):
    R.ICONS[ITEM] = icon()

"""2.99a: THE BACKPACK - a plain 27-slot bag for the road and the dungeons (the Fence, 5 Tokens).

The Vacuum Satchel's storage half on its own: no vacuum, no filter. Each backpack is its own bag (its contents ride in the
item, in its own minecraft:container), so several can be carried, each with its own load.

USE        right-click (or sneak + right-click: the same): it unfolds into a barrel in front of you - phase33's boxes, as the
           satchel, the Prime Cooler and the collectors do it (the item is held in storage while it's out, its contents moved
           into the barrel, and back into the item when it folds). It folds when you sneak, walk 6+ blocks off, after five
           minutes, or when you open another bag. Using a second backpack folds the first.
DUNGEONS   the Phase 2 dungeons (those round a bm.zone_d marker, the Hollow Throne, the Undercrown, the Armada), where the
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
     model=f'bm:{ITEM}', stack=1, cat='builder', comps=dict(hold('bundle'), **{'minecraft:container': []}))
# (no list price: Old Barnaby doesn't buy it back - a pawn trade can't see what's inside, and would swallow a full one)
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


# ===================================================================== generation (after phase33/148/173/174's boxes, and the
# dungeons' builds it guards: phase237, phase241, p2's Hollow Throne, phase131's lair)
def generate(G):
    import re
    fn, title = G.fn, G.title
    F = G.FUNCS
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    has = f'*[minecraft:custom_data~{{bm:"{ITEM}"}}]'
    G.wjson('bm/tags/block/p248_air.json', {'values': ['minecraft:air', 'minecraft:cave_air']})
    G.wjson('bm/tags/block/p248_nofloor.json', {'values': ['#minecraft:pressure_plates', '#minecraft:buttons', 'minecraft:lever', '#minecraft:rails',
                                                           'minecraft:barrel']})

    # ---------------------------------------------------------------- use: phase33's box, kind "pack"
    fn('p248/use', [f'execute if items entity @s weapon.mainhand {has} run return run function bm:p33/box/open {{path:"SelectedItem",slot:"weapon.mainhand",name:"Backpack",kind:"pack"}}',
                    f'execute if items entity @s weapon.offhand {has} run function bm:p33/box/open {{path:"equipment.offhand",slot:"weapon.offhand",name:"Backpack",kind:"pack"}}'])

    # where it opens: wherever the satchel may (p37/allowed: #bxw 1, phase33's try) - and, a backpack only, in the Phase 2
    # dungeons (#bxw 2, p248/dtry: plain air over solid floor, clear of the dungeon's fixtures)
    op = F['p33/box/open']
    k = next(i for i, l in enumerate(op) if l.startswith('execute unless function bm:p37/allowed run return run '))
    assert op[k + 1].endswith('run function bm:p33/box/try') and op[k + 2].endswith('run function bm:p33/box/try'), op[k:k + 3]
    refuse = op[k].replace('execute unless function bm:p37/allowed run', 'execute if score #bxw bm.rng matches 0 run')
    reach = lambda d: f'rotated ~ 0 positioned ^ ^ ^{d} align xyz positioned ~0.5 ~ ~0.5'
    op[k:k + 3] = ['scoreboard players set #bxw bm.rng 1',
                   'execute unless function bm:p37/allowed run scoreboard players set #bxw bm.rng 0',
                   '$data modify storage bm:tmp bpkk set value "$(kind)"',
                   'execute if score #bxw bm.rng matches 0 if data storage bm:tmp {bpkk:"pack"} if function bm:p248/dungeon run scoreboard players set #bxw bm.rng 2',
                   refuse,
                   f'execute if score #bxw bm.rng matches 1 {reach(1.6)} run function bm:p33/box/try',
                   f'execute if score #bxw bm.rng matches 1 if score #ok bm.rng matches 0 {reach(2.6)} run function bm:p33/box/try',
                   f'execute if score #bxw bm.rng matches 2 {reach(1.6)} run function bm:p248/dtry',
                   f'execute if score #bxw bm.rng matches 2 if score #ok bm.rng matches 0 {reach(2.6)} run function bm:p248/dtry',
                   'execute if score #ok bm.rng matches 0 if score #bxw bm.rng matches 2 run return run ' +
                   say('No room here: it wants open floor in front of you, clear of the dungeon\'s works.')]
    # (a backpack's marker keeps a copy of what's in its barrel from the start)
    k = op.index('function bm:p33/box/open2 with storage bm:tmp bx')
    op.insert(k + 1, 'execute if data storage bm:tmp {bpkk:"pack"} as @e[type=minecraft:marker,tag=bm.bxnew] at @s run function bm:p248/snap_new')
    fn('p248/dungeon', ['execute if dimension bm:gutter run return 0', 'execute if entity @s[tag=bm.gvp] run return 0',
                        'execute if entity @s[tag=bm.uadv] run return 1', 'execute if entity @s[tag=bm.aadv] run return 1',
                        'execute if dimension bm:hollow_throne run return 1',
                        'execute if entity @e[type=minecraft:marker,tag=bm.zone_d,distance=..48] run return 1', 'return 0'])
    fn('p248/dtry', ['execute unless block ~ ~ ~ #bm:p248_air run return 0', 'execute if block ~ ~-1 ~ #minecraft:replaceable run return 0',
                     'execute if block ~ ~-1 ~ #bm:p248_nofloor run return 0',
                     f'execute if entity @e[type=minecraft:marker,distance=..{MARK_R}] run return 0',
                     'execute positioned ~-0.5 ~ ~-0.5 if entity @e[type=!minecraft:player,type=!minecraft:item,type=!minecraft:experience_orb,'
                     'type=!minecraft:marker,dx=0,dy=0,dz=0] run return 0',
                     'scoreboard players set #bca bm.rng 0', 'execute if block ~ ~ ~ minecraft:cave_air run scoreboard players set #bca bm.rng 1',
                     'setblock ~ ~ ~ minecraft:barrel[facing=up]',
                     'summon minecraft:marker ~ ~ ~ {Tags:["bm.bxm","bm.bxnew"]}',
                     'execute if score #bca bm.rng matches 1 run tag @e[type=minecraft:marker,tag=bm.bxnew,distance=..0.5] add bm.bxca',
                     'scoreboard players operation @e[type=minecraft:marker,tag=bm.bxnew,distance=..0.5] bm.pid = #kp bm.pid',
                     'scoreboard players set @e[type=minecraft:marker,tag=bm.bxnew,distance=..0.5] bm.shcd 300',
                     'scoreboard players set #ok bm.rng 1', 'particle minecraft:cloud ~ ~0.5 ~ 0.3 0.3 0.3 0.02 8'])

    # ---------------------------------------------------------------- the copy: what's in the barrel, every tick
    fn('p248/snap_new', ['tag @s add bm.bxsnap', 'function bm:p248/snap'])
    fn('p248/snap', ['execute unless data block ~ ~ ~ Items[0] run return run data modify entity @s data.snap set value []',
                     'data modify entity @s data.snap set from block ~ ~ ~ Items'])
    fn('p248/watch', ['execute if block ~ ~ ~ minecraft:barrel run return run function bm:p248/snap',
                      'execute unless entity @s[tag=bm.bxgone] run function bm:p248/gone',
                      'function bm:p33/box/close'])
    # its barrel gone: what it spilled this tick (if it was broken) comes off the ground - the copy is what folds
    fn('p248/gone', ['tag @s add bm.bxgone', 'data modify storage bm:tmp bpk.snap set value []',
                     'data modify storage bm:tmp bpk.snap set from entity @s data.snap',
                     'execute as @e[type=minecraft:item,distance=..1.6] if function bm:p248/fresh run function bm:p248/dd/item'])
    fn('p248/fresh', ['execute store result score #age bm.rng run data get entity @s Age', 'execute if score #age bm.rng matches ..4 run return 1', 'return 0'])
    fn('p248/dd/item', ['execute if items entity @s contents minecraft:barrel run return run kill @s',
                        'data modify storage bm:tmp bpk.k set from entity @s Item', 'data remove storage bm:tmp bpk.k.count',
                        'data modify storage bm:tmp bpk.w set from storage bm:tmp bpk.snap',
                        'execute if function bm:p248/dd/scan run kill @s'])
    fn('p248/dd/scan', ['execute unless data storage bm:tmp bpk.w[0] run return 0',
                        'data modify storage bm:tmp bpk.a set from storage bm:tmp bpk.w[0]', 'data remove storage bm:tmp bpk.a.Slot',
                        'data remove storage bm:tmp bpk.a.count',
                        'execute store success score #bd bm.rng run data modify storage bm:tmp bpk.a set from storage bm:tmp bpk.k',
                        'execute if score #bd bm.rng matches 0 run return 1',
                        'data remove storage bm:tmp bpk.w[0]', 'return run function bm:p248/dd/scan'])
    # (the box's own barrel-gone handlers - an empty bag back, or a barrel set down again over whatever is there now - leave
    #  a copied bag to p248/watch, which runs first)
    tk = F['tick']
    old = 'execute as @e[type=minecraft:marker,tag=bm.bxm] at @s unless block ~ ~ ~ minecraft:barrel run function bm:p148/broke/box'
    k = tk.index(old)
    tk[k] = old.replace('tag=bm.bxm]', 'tag=bm.bxm,tag=!bm.bxsnap]')
    tk.insert(k, 'execute as @e[type=minecraft:marker,tag=bm.bxsnap] at @s run function bm:p248/watch')
    lf = F['loop/fast']
    old = 'execute as @e[type=minecraft:marker,tag=bm.bxm] at @s unless block ~ ~ ~ minecraft:barrel run function bm:p173/box/broke'
    lf[lf.index(old)] = old.replace('tag=bm.bxm]', 'tag=bm.bxm,tag=!bm.bxsnap]')
    # folding: with no barrel, a copied bag folds what its copy holds; the barrel's own block goes back to the air it was
    bc = F['p33/box/close']
    k = bc.index('execute if block ~ ~ ~ minecraft:barrel run data modify storage bm:tmp bx.src set from block ~ ~ ~ Items')
    bc.insert(k + 1, 'execute if entity @s[tag=bm.bxsnap] unless block ~ ~ ~ minecraft:barrel if data entity @s data.snap run '
                     'data modify storage bm:tmp bx.src set from entity @s data.snap')
    k = bc.index('execute if block ~ ~ ~ minecraft:barrel run setblock ~ ~ ~ minecraft:air')
    bc.insert(k, 'execute if block ~ ~ ~ minecraft:barrel if entity @s[tag=bm.bxca] run setblock ~ ~ ~ minecraft:cave_air')

    # ---------------------------------------------------------------- before a dungeon is rebuilt: every bag in it folded away
    fn('p248/stow', ['execute if block ~ ~ ~ minecraft:barrel run function bm:p248/snap', 'tag @s add bm.bxsnap', 'tag @s add bm.bxgone',
                     'execute if block ~ ~ ~ minecraft:barrel run data modify block ~ ~ ~ Items set value []',
                     'execute if block ~ ~ ~ minecraft:barrel if entity @s[tag=bm.bxca] run setblock ~ ~ ~ minecraft:cave_air',
                     'execute if block ~ ~ ~ minecraft:barrel run setblock ~ ~ ~ minecraft:air'])
    guarded = []
    import phase237 as P237, phase241 as P241
    for name, dim, box in (('p237/build/try', 'minecraft:the_nether', P237.BOX), ('p241/build/try', 'minecraft:the_end', P241.BOX)):
        L = F.get(name)
        if L is None: continue
        k = next(i for i, l in enumerate(L) if l.startswith(f'execute in {dim} run kill @e['))
        L.insert(k, f'execute in {dim} as @e[type=minecraft:marker,tag=bm.bxm,{box}] at @s run function bm:p248/stow')
        guarded.append(name)
    # (the Hollow Throne's rebuilds - the citadel, Wilfrey's Rest, Apophiss's lair - clear every entity in their box: the bags'
    #  markers are spared, folded first)
    kill = re.compile(r'^(execute (?:if score \S+ bm\.p2 matches \S+ )?in bm:hollow_throne run )kill @e\[(type=!minecraft:player|type=minecraft:marker),(x=[^\]]+)\]$')
    for name in ('p2/hollow/try_build', 'p2/hollow/try_grave', 'p131/lair/try'):
        L = F.get(name)
        if L is None: continue
        k = next((i for i, l in enumerate(L) if kill.match(l)), None)
        assert k is not None, name
        m = kill.match(L[k])
        L[k] = L[k].replace(f'kill @e[{m.group(2)},', f'kill @e[{m.group(2)},tag=!bm.bxm,')
        L.insert(k, m.group(1).replace(' run ', f' as @e[type=minecraft:marker,tag=bm.bxm,{m.group(3)}] at @s run ') + 'function bm:p248/stow')
        guarded.append(name)

    # ---------------------------------------------------------------- no bag inside a bag
    # put in an open bag's barrel: handed back to its owner (the cooler already hands back all that isn't a Prime cut)
    lf.append(f'execute as @e[type=minecraft:marker,tag=bm.bxm,tag=!bm.bx_cool] at @s if block ~ ~ ~ minecraft:barrel if items block ~ ~ ~ container.* {BAG} '
              'run function bm:p248/nest/live')
    fn('p248/nest/live', ['tag @a remove bm.cown', 'scoreboard players operation #own bm.pid = @s bm.pid',
                          'execute as @a if score @s bm.pid = #own bm.pid run tag @s add bm.cown', 'execute unless entity @a[tag=bm.cown] run return 0'] +
       [f'execute if items block ~ ~ ~ container.{n} {BAG} run function bm:p148/cool/spit {{n:{n}}}' for n in range(27)] +
       ['execute as @a[tag=bm.cown] at @s run playsound minecraft:block.chest.close player @s ~ ~ ~ 0.5 1.6',
        title('@a[tag=bm.cown]', 'actionbar', T('No bags inside bags - it\'s back with you.', COL)), 'tag @a remove bm.cown'])
    # still inside when a bag folds (or in its copy): handed back instead of packed
    dr = F['p33/box/drain']
    k = dr.index('function bm:p33/box/drain_one with storage bm:tmp bx.a')
    dr[k] = 'execute unless function bm:p248/nest/out run function bm:p33/box/drain_one with storage bm:tmp bx.a'
    fn('p248/nest/out', ['execute unless entity @a[tag=bm.cown] run return 0',
                         'data modify storage bm:tmp bpk.e set from storage bm:tmp bx.src[0]',
                         'execute unless function bm:p248/nest/is_bag run return 0', 'data remove storage bm:tmp bpk.e.Slot',
                         'execute at @a[tag=bm.cown,limit=1] run summon minecraft:item ~ ~0.3 ~ {Tags:["bm.bpspit"],Item:{id:"minecraft:stone",count:1},PickupDelay:0s}',
                         'data modify entity @e[type=minecraft:item,tag=bm.bpspit,limit=1] Item set from storage bm:tmp bpk.e',
                         'tag @e[type=minecraft:item,tag=bm.bpspit] remove bm.bpspit', 'return 1'])
    fn('p248/nest/is_bag', [f'execute if data storage bm:tmp {{bpk:{{e:{{components:{{"minecraft:custom_data":{{bm:"{b}"}}}}}}}}}} run return 1' for b in BAGS] +
       ['return 0'])
    # the satchel's pick-up: never a bag
    pl = F['p33/vac/pull']
    old = 'unless items entity @s contents *[minecraft:custom_data~{bm:"vacuum_satchel"}]'
    ks = [i for i, l in enumerate(pl) if old in l]
    assert len(ks) == 1, ks
    pl[ks[0]] = pl[ks[0]].replace(old, f'unless items entity @s contents {BAG}')
    return guarded

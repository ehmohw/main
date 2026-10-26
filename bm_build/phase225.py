"""2.94x: THE SMUGGLER'S WAYTOKEN - the Fence sells it (3 Medallions at the market's rates; 2 on a lucky night). A token stamped for one Black Market, of your choosing:

  LINK IT    use it inside a Black Market: it's stamped for that one (its doorstep). Sneak + use inside another to restamp it.
  GO         use it anywhere else (the Overworld, the Nether, the End): you're at that market's door - and the token remembers
             where you were.
  COME BACK  use it again at that market: back where you were (facing the way you were).

Each token keeps its own stamp and its own way back (in the item: bm_way, bm_wret, bm_wr), so a few tokens can be stamped
for a few markets. Not in the pack's own worlds (the Gutter, the Hollow Throne) or on a heist; a breath (3 s) between uses.
Riding, you're set down first; your partners follow as ever (keep up, or home)."""
from items import item, TOTEM, T
from useitem import hold, HOLD

ITEM = 'waytoken'
COL = '#d8b46a'
LORE0 = ['A brass token, a rat stamped on one face.', ('Unstamped. Use it inside a Black Market', 'blue'), ('to stamp it for that one.', 'blue')]
item(ITEM, TOTEM, "Smuggler's Waytoken", COL, LORE0, model=f'bm:{ITEM}', stack=1, cat='magic', glint=False, comps=hold('none'))
HOLD[ITEM] = 'bm:p225/use'
PRICE = ('medallion', 4)          # (the economy's rebalance makes it 3)


def extend_offers(O, offer):
    O['fence'].append(offer(PRICE, (ITEM, 1)))


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    PRE = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = f'*[minecraft:custom_data~{{bm:"{ITEM}"}}]'
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.wtu dummy']
    G.OBJECTIVES.append('bm.wtu')
    D = 'minecraft:custom_data'

    fn('p225/use', [
        'execute store result score #now bm.rng run time query gametime',
        'scoreboard players operation #gap bm.rng = #now bm.rng', 'scoreboard players operation #gap bm.rng -= @s bm.wtu',
        'execute if score @s bm.wtu matches 1.. if score #gap bm.rng matches 0..59 run return 0',
        'execute if entity @s[tag=bm.gvp] run return run ' + say('Not on a heist - the Fixer would have your hide.', '#c8a0a0'),
        'execute unless dimension minecraft:overworld unless dimension minecraft:the_nether unless dimension minecraft:the_end run return run '
        + say('The token is cold here. (Not in this world.)', '#c8a0a0'),
        'scoreboard players operation @s bm.wtu = #now bm.rng',
        'data modify storage bm:tmp wt set value {slot:"weapon.offhand",path:"equipment.offhand"}',
        f'execute if items entity @s weapon.mainhand {holds} run data modify storage bm:tmp wt set value {{slot:"weapon.mainhand",path:"SelectedItem"}}',
        'function bm:p225/use2 with storage bm:tmp wt'])
    fn('p225/use2', [
        f'$data modify storage bm:tmp wt.i set from entity @s $(path).components."{D}"',
        'execute store success score #mk bm.rng if entity @e[type=minecraft:marker,tag=bm.market_hall,distance=..30]',
        'execute unless data storage bm:tmp wt.i.bm_way if score #mk bm.rng matches 1 run return run function bm:p225/link with storage bm:tmp wt',
        'execute unless data storage bm:tmp wt.i.bm_way run return run ' + say('Unstamped - use it inside a Black Market to stamp it for that one.', '#e8d8a0'),
        'scoreboard players set #here bm.rng 0',
        'function bm:p225/here with storage bm:tmp wt.i.bm_way',
        'execute if score #mk bm.rng matches 1 if score #here bm.rng matches 0 if predicate bm:p20/sneaking run return run function bm:p225/link with storage bm:tmp wt',
        'execute if score #here bm.rng matches 1 if data storage bm:tmp {wt:{i:{bm_wr:1b}}} run return run function bm:p225/back with storage bm:tmp wt',
        'execute if score #here bm.rng matches 1 run return run ' + say('You\'re at its market already - use it out in the world to come here.', '#e8d8a0'),
        'function bm:p225/go with storage bm:tmp wt'])
    # (at the stamped market: within 48 of its doorstep, in its world)
    fn('p225/here', ['$execute in $(d) positioned $(x) $(y) $(z) align xz positioned ~0.5 ~ ~0.5 if entity @s[distance=..48] run scoreboard players set #here bm.rng 1'])

    # ---- stamping it: the market's doorstep (its exit marker - where the bouncer sets folk down), else where you stand
    fn('p225/link', [
        'data modify storage bm:tmp wt.n set value {}',
        'data modify storage bm:tmp wt.n.d set from entity @s Dimension',
        'execute store result storage bm:tmp wt.n.x int 1 run data get entity @s Pos[0]',
        'execute store result storage bm:tmp wt.n.y int 1 run data get entity @s Pos[1]',
        'execute store result storage bm:tmp wt.n.z int 1 run data get entity @s Pos[2]',
        'execute store result storage bm:tmp wt.n.r int 1 run data get entity @s Rotation[0]',
        'execute at @e[type=minecraft:marker,tag=bm.market_hall,distance=..30,sort=nearest,limit=1] as @e[type=minecraft:marker,tag=bm.market_exit,distance=..80,sort=nearest,limit=1] run function bm:p225/link_door',
        '$data modify storage bm:tmp wt.n.slot set value "$(slot)"',
        'function bm:p225/stamp with storage bm:tmp wt.n',
        'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.5 1.8', 'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 0.8',
        'particle minecraft:wax_on ~ ~1.2 ~ 0.3 0.4 0.3 0 12'])
    fn('p225/link_door', ['execute store result storage bm:tmp wt.n.x int 1 run data get entity @s Pos[0]',
                          'execute store result storage bm:tmp wt.n.y int 1 run data get entity @s Pos[1]',
                          'execute store result storage bm:tmp wt.n.z int 1 run data get entity @s Pos[2]',
                          'execute store result storage bm:tmp wt.n.r int 1 run data get entity @s Rotation[0]'])
    lore = lambda *ls: ','.join(G.snbt(T(*l) if isinstance(l, tuple) else T(l, 'gray')) for l in ls)
    fn('p225/stamp', [
        '$item modify entity @s $(slot) {type:"minecraft:sequence",functions:['
        '{type:"minecraft:set_custom_data",tag:{bm_way:{d:"$(d)",x:$(x),y:$(y),z:$(z),r:$(r)},bm_wr:0b}},'
        '{type:"minecraft:set_lore",mode:"replace_all",lore:[' +
        lore('A brass token, a rat stamped on one face.', ('Stamped: the Black Market at $(x), $(z).', COL),
             ('Use it anywhere: to its door. Use it there', 'blue'), ('again: back where you were.', 'blue'), ('Sneak + use in another market: restamp it.', 'dark_gray')) + ']}]}',
        tellraw('@s', PRE + [T("Waytoken stamped: ", COL, bold=True), T('this market. Use it out in the world to come back to its door.', 'gray')])])

    # ---- going: where you are is kept in the token; then you're at the door
    fn('p225/go', [
        'data modify storage bm:tmp wt.n set value {}',
        'data modify storage bm:tmp wt.n.d set from entity @s Dimension',
        'execute store result storage bm:tmp wt.n.x int 1 run data get entity @s Pos[0]',
        'execute store result storage bm:tmp wt.n.y int 1 run data get entity @s Pos[1]',
        'execute store result storage bm:tmp wt.n.z int 1 run data get entity @s Pos[2]',
        'execute store result storage bm:tmp wt.n.r int 1 run data get entity @s Rotation[0]',
        '$data modify storage bm:tmp wt.n.slot set value "$(slot)"',
        'function bm:p225/keep with storage bm:tmp wt.n',
        'function bm:p225/leave',
        'function bm:p225/tp with storage bm:tmp wt.i.bm_way',
        'function bm:p225/arrive',
        title('@s', 'actionbar', T('The Black Market. (Use the token again here to go back.)', COL))])
    fn('p225/keep', ['$item modify entity @s $(slot) {type:"minecraft:set_custom_data",tag:{bm_wret:{d:"$(d)",x:$(x),y:$(y),z:$(z),r:$(r)},bm_wr:1b}}'])
    # (the block's centre: a stored x of -12 is the block from -12 to -11 - floored, so "$(x).5" would be a block off below 0)
    fn('p225/tp', ['$execute in $(d) positioned $(x) $(y) $(z) align xz positioned ~0.5 ~ ~0.5 run tp @s ~ ~ ~ $(r) 0'])
    fn('p225/leave', ['ride @s dismount', 'particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.05 40', 'particle minecraft:wax_on ~ ~1 ~ 0.4 0.6 0.4 0 10',
                      'playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 0.8 0.8'])
    fn('p225/arrive', ['effect give @s minecraft:resistance 3 4 true',
                       'execute at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.05 40',
                       'execute at @s run playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 0.8 1.1',
                       'execute at @s run playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.2'])

    # ---- coming back: where you were, the way you faced; the way back spent
    fn('p225/back', ['function bm:p225/leave',
                     'function bm:p225/tp with storage bm:tmp wt.i.bm_wret',
                     '$item modify entity @s $(slot) {type:"minecraft:set_custom_data",tag:{bm_wr:0b}}',
                     'function bm:p225/arrive',
                     title('@s', 'actionbar', T('Back where you were.', COL))])


def rp(R):
    R.ICONS[ITEM] = R.grid(['................', '.....KKKKKK.....', '....KYYYYYYK....', '...KYyyyyyyYK...', '..KYyKKyyKKyYK..', '..KYyKwyyKwyYK..',
                            '..KYyyyyyyyyYK..', '..KYyyyKKyyyYK..', '..KYyyKyyKyyYK..', '..KYyyyyyyyyYK..', '...KYyyyyyyYK...', '....KYYYYYYK....',
                            '.....KKKKKK.....', '................', '................', '................'],
                           dict(K='#4a3418', Y='#e8c870', y='#c89c48', w='#ffffff'))

"""Phase 1.27 / 2.20: fixes from play, the Rat Gang's prizes, a way down to every market.

THE BLACK MARKET
- Every market gets a LADDER SHAFT from the end of its dig-in tunnel up to the surface (a signposted top), so a market
  whose tunnel ends sealed in rock can always be reached. Markets already in worlds get theirs the first time they load.
- Water: any waterloggable block in a market that holds water (iron bars, chains, dripstone, stairs, slabs...) is set
  dry - once, when an older market first loads under this version.
- Decor that floated where the counters used to be two blocks high sits on the counters again; the Blood Alcove's cages
  hang lanterns; the dock steps run the right way down to the pier; the DOCKS sign hangs over the office's open side.
- Salty Sal the Dockmaster is a rat now, like every trader (at trader scale).
- Rat Gang HQ: the wall to the docks reaches the ceiling (ender pearls no longer get in). The Captain sells two new prizes:
  THE HOARD SACK - a personal 27-slot stash: use it and a locked barrel only you can open appears in front of you; it
  folds away (contents kept) when you walk off. THE GOLDEN CHEESE WHEEL - set it down: everyone within 50 blocks is kept
  fed (Saturation), like a full beacon. Sneak + punch to pick it up.
- Armour lives with Sgt. Steelwhisker (the Smuggler/Kingpin/Hero line and the Dawnbringer set moved from Madame Velour);
  the mail kit (mailbox + courier whistle) is at the Fence. The Newcomers' book lists who sells what.
THE VORN
- Their models vanish with them (no more bodies left standing). Fewer of them at once on an Invasion Night. Bioengineered
  beasts lose the green outline (sickly particles instead). Invasion Nights hum, beam and crackle.
- Invasion Nights only start once someone has killed a Vorn aboard a Dreadnought.
- Vorn troopers and saucers drop Red Xenite 1 time in 100.
- The Vorn Skiff hides its harness, and its hull rides with you instead of trailing behind."""
import json
import mgeo
import market2
import rot
from items import item, T, TOTEM, DYNAMIC, consumable
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import phase35 as P35

W, BF, SZ = market2.W, market2.BF, market2.SZ
ident = [F(0), F(0), F(0), F(1)]
GOLD = '#ffd23f'

# ===================================================================== the Rat Gang's prizes
item('hoard_sack', TOTEM, 'Hoard Sack', '#c8a050',
     ['The Rat King\'s own stash bag.', ('Right-click: your private barrel appears in front of', 'blue'), ('you (27 slots). Only this sack opens it.', 'blue'),
      ('It folds away, contents kept, when you walk off.', 'gray'), ('Guard it while it\'s open - it is a real barrel.', 'dark_gray')],
     model='bm:hoard_sack', stack=1, cat='relic', glint=True, comps=hold('none'))
HOLD['hoard_sack'] = 'bm:p41/sack/use'
DYNAMIC.add('hoard_sack')                # its owner stamp (custom_data bm_sack) survives re-syncs
item('golden_cheese_wheel', TOTEM, 'Golden Cheese Wheel', GOLD,
     ['The Rat King\'s prize. Nobody goes hungry near it.', ('Set it down: everyone within 50 blocks', 'blue'), ('stays fed (Saturation).', 'blue'),
      ('Sneak + punch to pick it up. Right-click to turn it.', 'gray')],
     model='bm:golden_cheese_wheel', stack=1, cat='relic', glint=True, bold=True,
     comps={'minecraft:consumable': consumable(0.4, 'none', 'minecraft:block.wood.place', False)})

# ===================================================================== the newcomers' book: who sells what
P35.GUIDE[:] = [
    [T('NEWCOMERS,\nSTART HERE\n\n', '#6a2a8a', bold=True), T('Welcome to the Black Market.\n\nWe trade in ', 'black'), T('Tokens', '#6a2a8a'),
     T(', ', 'black'), T('Medallions', '#6a2a8a'), T(' and ', 'black'), T('Trophies', '#6a2a8a'),
     T(' (1 Trophy = 6 Medallions = 54 Tokens). Monsters, Blood Moons, bosses and Old Barnaby pay them out.', 'black')],
    [T('PAWN ALLEY\n', '#6a2a8a', bold=True), T('(north, under the terrace)\n\n', 'dark_gray'), T('The Fence', 'black', bold=True),
     T(': currency exchange, dungeon keys, sealed maps, mailboxes and the Courier Whistle.\n\n', 'black'), T('Old Barnaby', 'black', bold=True),
     T(': the pawnbroker - buys your Black Market goods back for half.', 'black')],
    [T('THE PLAZA\n', '#6a2a8a', bold=True), T('(centre, by the waterfall)\n\n', 'dark_gray'), T('Madame Velour', 'black', bold=True),
     T(': style and gear - hats, wings, boots, the grappling hook, Roc\'s Feather, mushrooms.\n\n', 'black'),
     T('THE STACKS ', '#6a2a8a', bold=True), T('(up on the terrace)\n', 'dark_gray'), T('Prof. Whiskerton', 'black', bold=True),
     T(': lore books, sealed maps, weapon skin scrolls, the Experience Flask.', 'black')],
    [T('THE FORGE PIT\n', '#6a2a8a', bold=True), T('(east)\n\n', 'dark_gray'), T("Vinny 'Two-Blades'", 'black', bold=True),
     T(': legendary weapons and tools, and their upgrades.\n\n', 'black'), T('Sgt. Steelwhisker', 'black', bold=True),
     T(': every armour set - Smuggler to Hero, Shadowstep, Juggernaut, Architect, Tidecaller (3 tiers), the Dawnbringer.', 'black')],
    [T('THE GNAWED FLAGON\n', '#6a2a8a', bold=True), T('(east)\n', 'dark_gray'), T('Chef Fromage', 'black', bold=True),
     T(': feasts (blessings until you die) and coffee; buys Prime meats.\n\n', 'black'), T('THE BLOOD ALCOVE\n', '#6a2a8a', bold=True),
     T('The Bloodbroker', 'black', bold=True), T(': Blood Moon goods - Crimson and Vampire Lord armour, tonics, wards; buys Ectoplasm.', 'black')],
    [T('THE DOCKS ', '#6a2a8a', bold=True), T('(west)\n', 'dark_gray'), T('Salty Sal', 'black', bold=True),
     T(': sea gear - MLG Bucket, Kraken Conch, Blue Marlin, cutlass, Storm Balls, weather vials.\n\n', 'black'),
     T('THE LUCKY DEN ', '#6a2a8a', bold=True), T('(across the river)\n', 'dark_gray'), T('Lucky Whiskers', 'black', bold=True),
     T(': scratch cards, Lucky Tokens, cosmetic charms.', 'black')],
    [T('THE BOUNTY BOARD\n', '#6a2a8a', bold=True), T('(right here, by this book)\n\n', 'dark_gray'),
     T('On Blood Moons, Lucky Nights and Invasion Nights it posts a bounty. Sign it to take it - one bounty a night.\n\n', 'black'),
     T('BEHIND THE NORTH WALL: ', '#6a2a8a', bold=True), T('the Dark Auction and the Gilded Gutter open as your ', 'black'), T('Standing', '#6a2a8a'),
     T(' grows.\n\nAnd a pirate captain hides behind a very ', 'black'), T('small', 'black', italic=True), T(' door by the docks.\n\n- The Management', 'black')],
]


def _sell_id(o):
    s = str(o['sell'])
    k = s.find("'bm': '")
    if k < 0:
        k = s.find('bm:"')
        return s[k + 4:s.index('"', k + 4)] if k >= 0 else ''
    return s[k + 7:s.index("'", k + 7)]


def extend_offers(O, offer):
    # armour with the armourer, the mail kit with the Fence
    move = [o for o in O['outfitter'] if _sell_id(o).startswith(('smuggler_', 'kingpin_', 'hero_', 'solar_'))]
    O['outfitter'] = [o for o in O['outfitter'] if o not in move]
    O['armory'] = move + O['armory']
    mail = [o for o in O['pawn'] if _sell_id(o) == 'mailbox']
    O['pawn'] = [o for o in O['pawn'] if o not in mail]
    O['fence'] += mail
    O['captain'] += [offer(('medallion', 16), ('hoard_sack', 1), ('lucky_token', 3)), offer(('trophy', 3), ('golden_cheese_wheel', 1), ('minecraft:gold_block', 9))]


def generate(G):
    fn, wjson, title, give, tellraw, PREFIX = G.fn, G.wjson, G.title, G.give, G.tellraw, G.PREFIX
    import check262 as C
    rel = mgeo.rel
    MB = mgeo.MB()
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    objs = ['bm.sackt dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    c3 = lambda c: rel((c[0] + 0.5, c[1] + 0.5, c[2] + 0.5))

    # ================================================================== the market patch (once per market, at any turn)
    # cells re-synced to the template (floating decor, the den wall, the dock steps)
    x1 = market2.RIVER[0]
    sync = [(32, W + 1, 20), (32, W + 2, 20), (42, W + 1, 20), (42, W + 2, 20)] + [(54, W + 2, z) for z in range(18, 24)] + \
           [(60, W + 1, 21), (60, W + 2, 21), (60, W + 3, 21), (60, W + 1, 29), (60, W + 2, 29)] + \
           [(68, y, z) for z in (41, 44, 48) for y in (W + 1, W + 2)] + [(x, W + 2, z) for (x, z) in ((58, 63), (66, 64), (62, 67))] + \
           [(x, y, 33) for x in range(29, 35) for y in (W, W + 1)] + [(x, W + 3, z) for x in range(1, 7) for z in (20, 21)] + \
           [(x, y, z) for x in range(x1 - 3, x1) for z in (26, 27) for y in range(market2.WATER_TOP + 1, W + 3)]
    for n in range(4):
        fn(f'p41/sync_{n}', [f'execute positioned {c3(c)} run setblock ~ ~ ~ {rot.rotate(MB.b.get(c, "minecraft:air"), n)}' for c in sync])
    # waterlogged blocks set dry (every waterloggable template block; setblock recomputes connections)
    wet = []
    for c, st in sorted(MB.b.items()):
        name = st.split('[')[0]
        props = C.BLOCKS.get(name.split(':')[1], [{}])[0]
        if 'waterlogged' in props:
            wet.append((c, name, st))
    for n in range(4):
        fn(f'p41/dry_{n}', [f'execute positioned {c3(c)} if block ~ ~ ~ {name}[waterlogged=true] run setblock ~ ~ ~ '
                            f'{rot.strip_waterlog(rot.rotate(st, n)) if "[" in st else name + "[waterlogged=false]"}' for c, name, st in wet])
    G.P41_WET = len(wet)
    turn = lambda f: [f'execute if entity @s[y_rotation={r}] run function bm:{f}_{n}' for r, n in rot.TURNS]
    # the docks' sign, the Dockmaster as a rat, the newcomers' book
    from phase34 import DOCK_POS, DOCK_YAW
    neon_old, neon_new = (9.5, W + 6.2, 31.6), (12.6, W + 6.0, 26.5)
    lx, ly, lz = P35.LECTERN
    book = {'id': 'minecraft:written_book', 'count': Int(1), 'components': {'minecraft:written_book_content': {
        'title': 'Newcomers, Start Here', 'author': 'The Management', 'pages': [{'text': '', 'extra': pg} for pg in P35.GUIDE]}}}
    patch = ['tag @s add bm.p41'] + turn('p41/sync') + turn('p41/dry') + [
        f'execute positioned {rel(neon_old)} run kill @e[type=minecraft:text_display,tag=bm.neon_docks,distance=..1.5]',
        f'execute positioned {rel(neon_new)} unless entity @e[type=minecraft:text_display,tag=bm.neon_docks,distance=..1.5] run summon minecraft:marker ~ ~ ~ '
        '{Tags:["bm.npc_spawn","bm.npc.neon","bm.neon_docks","bm.p41n"]}',
        f'execute positioned {rel(neon_new)} rotated ~-90 0 run tp @e[type=minecraft:marker,tag=bm.p41n,distance=..1,limit=1] ~ ~ ~ ~ 0',
        'tag @e[type=minecraft:marker,tag=bm.p41n] remove bm.p41n',
        f'execute positioned {rel(DOCK_POS)} unless entity @e[type=minecraft:item_display,tag=bm.rat_sprite,distance=..1.5] run kill @e[type=minecraft:villager,tag=bm.npc_dock,distance=..2]',
        f'execute positioned {rel(DOCK_POS)} unless entity @e[type=minecraft:villager,tag=bm.npc_dock,distance=..2] rotated ~{DOCK_YAW} 0 run function bm:p34/dock_spawn',
        f'execute positioned {rel((lx + 0.5, ly + 0.5, lz + 0.5))} if block ~ ~ ~ minecraft:lectern run data modify block ~ ~ ~ Book set value {snbt(book)}',
        # the way down: a shaft marker beyond the tunnel's end, turned like the market
        f'execute positioned {rel((38.5, BF + 1, SZ + 1.5))} unless entity @e[type=minecraft:marker,tag=bm.mshaft,distance=..2] run summon minecraft:marker ~ ~ ~ {{Tags:["bm.mshaft","bm.msnew"]}}',
        f'execute positioned {rel((38.5, BF + 1, SZ + 1.5))} run tp @e[type=minecraft:marker,tag=bm.msnew,distance=..1,limit=1] ~ ~ ~ ~ 0',
        'tag @e[type=minecraft:marker,tag=bm.msnew] remove bm.msnew']
    fn('p41/patch', patch)
    corners = ' '.join(f'if loaded {rel(c)}' for c in ((1, W, 1), (market2.SX - 2, W, 1), (1, W, SZ - 2), (market2.SX - 2, W, SZ - 2)))
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.mkt,tag=!bm.p41] at @s rotated as @s if entity @a[distance=..96] {corners} run function bm:p41/patch')

    # ================================================================== the shaft: tunnel's end -> surface, ladders on the far wall
    second.append('execute as @e[type=minecraft:marker,tag=bm.mshaft,tag=!bm.msdone] at @s if loaded ~3 ~ ~3 if loaded ~-3 ~ ~-3 run function bm:p41/shaft/start')
    fn('p41/shaft/start', ['tag @s add bm.msdone',
                           'execute positioned over motion_blocking_no_leaves run summon minecraft:marker ~ ~ ~ {Tags:["bm.mstop"]}',
                           'execute store result score #top bm.rng run data get entity @e[type=minecraft:marker,tag=bm.mstop,limit=1] Pos[1]',
                           'kill @e[type=minecraft:marker,tag=bm.mstop]', 'execute store result score #n bm.rng run data get entity @s Pos[1]',
                           'scoreboard players operation #top bm.rng -= #n bm.rng', 'execute if score #top bm.rng matches ..0 run return 0',
                           'scoreboard players set #lv bm.rng 0',
                           'execute rotated as @s run fill ^-1 ^-1 ^-1 ^1 ^-1 ^1 minecraft:cobbled_deepslate'] +
       [f'execute if entity @s[y_rotation={r}] rotated as @s run function bm:p41/shaft/lv_{n}' for r, n in rot.TURNS] +
       ['execute rotated as @s run fill ^-1 ^ ^-2 ^1 ^2 ^-1 minecraft:air'])      # the doorway from the tunnel
    back = {0: 'north', 1: 'east', 2: 'south', 3: 'west'}     # a ladder on the far wall faces back along the tunnel
    sign = snbt({'front_text': {'has_glowing_text': B(1), 'color': 'yellow', 'messages': [{'text': 'THE BLACK'}, {'text': 'MARKET'}, {'text': 'members only'}, {'text': 'mind the drop'}]},
                 'back_text': {'has_glowing_text': B(1), 'color': 'yellow', 'messages': [{'text': 'THE BLACK'}, {'text': 'MARKET'}, {'text': 'members only'}, {'text': 'mind the drop'}]}})
    for n in range(4):
        fn(f'p41/shaft/lv_{n}', ['fill ^-2 ^ ^-2 ^2 ^ ^2 minecraft:cobbled_deepslate', 'fill ^-1 ^ ^-1 ^1 ^ ^1 minecraft:air'] +
           [f'setblock ^{dx} ^ ^1 minecraft:ladder[facing={back[n]}]' for dx in (-1, 0, 1)] +
           ['scoreboard players add #lv bm.rng 1', 'scoreboard players operation #m bm.rng = #lv bm.rng', 'scoreboard players operation #m bm.rng %= #5 bm.rng',
            'execute if score #m bm.rng matches 0 run setblock ^-2 ^ ^ minecraft:glowstone', 'execute if score #m bm.rng matches 0 run setblock ^2 ^ ^ minecraft:glowstone',
            'scoreboard players remove #top bm.rng 1',
            f'execute if score #top bm.rng matches 1.. positioned ~ ~1 ~ run return run function bm:p41/shaft/lv_{n}',
            'execute positioned ~ ~1 ~ run function bm:p41/shaft/top'])
    fn('p41/shaft/top', ['fill ^-1 ^ ^-1 ^1 ^3 ^1 minecraft:air'] +
       [f'setblock ^{x} ^ ^{z} minecraft:cobbled_deepslate_wall' for (x, z) in ((2, 2), (-2, -2), (2, -2), (-2, 2))] +
       [f'setblock ^{x} ^1 ^{z} minecraft:soul_lantern' for (x, z) in ((2, 2), (-2, -2), (2, -2))] +
       [f'setblock ^-2 ^1 ^2 minecraft:dark_oak_sign[rotation=0]{sign}', 'playsound minecraft:block.stone.place block @a[distance=..48] ~ ~ ~ 0.6 0.8'])

    # ================================================================== the Vorn
    fn('p41/has_vehicle', ['return run execute on vehicle if entity @s'])
    second.append('execute as @e[type=minecraft:item_display,tag=bm.vdisp] unless function bm:p41/has_vehicle run kill @s')
    fast.append('execute as @e[tag=bm.bio] at @s if entity @a[distance=..32] run particle minecraft:item_slime ~ ~1 ~ 0.3 0.4 0.3 0 1')
    G.FUNCS['p32/inv/during'].append('execute as @a[tag=bm.ow,gamemode=!spectator] at @s if predicate bm:sees_sky run function bm:p41/inv/amb')
    fn('p41/inv/amb', ['execute store result score #r bm.rng run random value 1..14',
                       'execute if score #r bm.rng matches 1 run playsound minecraft:block.beacon.ambient ambient @s ~ ~ ~ 1 0.5',
                       'execute if score #r bm.rng matches 2 run playsound minecraft:block.conduit.ambient.short ambient @s ~ ~ ~ 1 0.6',
                       'execute if score #r bm.rng matches 3 run playsound minecraft:entity.guardian.ambient ambient @s ~12 ~6 ~-9 0.8 0.5',
                       'execute if score #r bm.rng matches 4 run playsound minecraft:block.respawn_anchor.ambient ambient @s ~ ~ ~ 0.8 0.6',
                       'execute if score #r bm.rng matches 5 run function bm:p41/inv/beam',
                       'execute if score #r bm.rng matches 6 run particle minecraft:electric_spark ~ ~14 ~ 18 2 18 0.2 30 force @s'])
    fn('p41/inv/beam', ['execute store result score #bx bm.rng run random value -30..30', 'execute store result score #bz bm.rng run random value -30..30',
                        'execute store result storage bm:tmp ib.x int 1 run scoreboard players get #bx bm.rng',
                        'execute store result storage bm:tmp ib.z int 1 run scoreboard players get #bz bm.rng', 'function bm:p41/inv/beam_m with storage bm:tmp ib'])
    fn('p41/inv/beam_m', ['$particle minecraft:end_rod ~$(x) ~18 ~$(z) 0.15 14 0.15 0 60 force @s',
                          '$particle minecraft:dust{color:[0.5,1.0,0.35],scale:2.5} ~$(x) ~18 ~$(z) 0.4 14 0.4 0 40 force @s',
                          '$playsound minecraft:block.beacon.activate ambient @s ~$(x) ~ ~$(z) 1.5 1.4'])
    # Invasion Nights wait until someone has killed a Vorn aboard a Dreadnought
    roll = G.FUNCS['p32/inv/roll']
    k = roll.index('execute if score #bday bm.bm matches 1 run return 0')
    roll.insert(k + 1, 'execute unless score #vornmet bm.bm matches 1 run return 0')
    for name, lines in G.FUNCS.items():
        for i in range(len(lines) - 1, -1, -1):
            if 'tag=bm.vguard' in lines[i] and 'spawn/trooper' in lines[i]:
                lines.insert(i + 1, 'tag @e[type=minecraft:husk,tag=bm.vtroop,tag=!bm.vguardian,distance=..48] add bm.vguardian')
    wjson('bm/advancement/p41/vornmet.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.vguardian"]}'}}]}}},
        'rewards': {'function': 'bm:p41/vornmet'}})
    fn('p41/vornmet', ['advancement revoke @s only bm:p41/vornmet', 'execute if score #vornmet bm.bm matches 1 run return 0',
                       'scoreboard players set #vornmet bm.bm 1',
                       tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(' killed a Vorn aboard its own ship. ', 'gray'),
                                               T('The fleet has noticed this world... Invasion Nights can come now.', '#7dff6a', bold=True)]),
                       'execute as @a at @s run playsound minecraft:block.end_portal.spawn ambient @s ~ ~ ~ 0.5 0.6'])
    # 1 in 100: Red Xenite from troopers and saucers
    import mig263
    from nbt import to_json
    for t in ('trooper', 'saucer'):
        path = G.path('data', 'bm', 'loot_table', 'p32', f'{t}.json')
        obj = json.load(open(path))
        obj['pools'] += mig263.convert(f'bm/loot_table/p32/{t}.json', to_json(mig263.custom_data_snbt(
            {'type': 'minecraft:entity', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('xenite_red')], 'conditions': [G.chance(0.01)]}]})))['pools']
        json.dump(obj, open(path, 'w'), indent=1, ensure_ascii=False)

    # ================================================================== the Vorn Skiff: the hull rides the skiff itself while it's piloted
    # (a passenger moves with its vehicle on the same tick; teleporting the hull each tick left it a tick behind). It boards as
    # the second passenger, after the pilot (the first passenger steers), and steps off whenever nobody is aboard.
    G.FUNCS['p35/skiff/follow'][:] = [
        'scoreboard players operation #kp bm.pid = @s bm.pid',
        'execute as @e[type=minecraft:happy_ghast,tag=bm.skiff] if score @s bm.pid = #kp bm.pid run tag @s add bm.skme',
        'execute unless entity @e[tag=bm.skme] run return run kill @s',
        'execute as @e[tag=bm.skme] on passengers if entity @s[type=minecraft:player] run tag @s add bm.skrider',
        'execute if entity @a[tag=bm.skrider] unless function bm:p41/skiff/on_pilot run function bm:p41/skiff/board',
        'execute unless entity @a[tag=bm.skrider] if function bm:p41/skiff/on_pilot run function bm:p41/skiff/unboard',
        'execute unless entity @a[tag=bm.skrider] at @e[tag=bm.skme,limit=1] run tp @s ~ ~ ~ ~ 0',
        'tag @a[tag=bm.skrider] remove bm.skrider', 'tag @e[tag=bm.skme] remove bm.skme']
    fn('p41/skiff/on_pilot', ['execute on vehicle if entity @s[type=minecraft:happy_ghast] run return 1', 'return 0'])
    fn('p41/skiff/board', ['ride @s mount @e[type=minecraft:happy_ghast,tag=bm.skme,limit=1]', f'data merge entity @s {{transformation:{{translation:[0f,{SKIFF_RIDE_Y}f,0f]}},teleport_duration:0}}'])
    fn('p41/skiff/unboard', ['ride @s dismount', 'data merge entity @s {transformation:{translation:[0f,0.4f,0f]},teleport_duration:2}'])

    # ================================================================== the Hoard Sack: a locked barrel only its owner's sack opens
    wjson('bm/tags/block/p41_open.json', {'values': ['minecraft:air', 'minecraft:cave_air', 'minecraft:short_grass', 'minecraft:tall_grass',
                                                     'minecraft:fern', 'minecraft:snow', 'minecraft:dead_bush', 'minecraft:short_dry_grass']})
    fn('p41/sack/use', ['execute unless function bm:p37/allowed run return run ' + say('The sack stays shut here.'),
                        'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #kp bm.pid = @s bm.pid',
                        'execute store result storage bm:tmp sk.n int 1 run scoreboard players get @s bm.pid',
                        # stamp the sack with its owner the first time
                        'execute if items entity @s weapon.mainhand ' + holds % 'hoard_sack' + ' unless items entity @s weapon.mainhand *[minecraft:custom_data~{bm_sackset:1b}] run function bm:p41/sack/stamp with storage bm:tmp sk',
                        'scoreboard players set #had bm.rng 0',
                        'execute as @e[type=minecraft:marker,tag=bm.sackm] if score @s bm.pid = #kp bm.pid at @s run function bm:p41/sack/close_mine',
                        'execute if score #had bm.rng matches 1 run return 0',
                        'scoreboard players set #ok bm.rng 0', 'tag @s add bm.sacker',
                        'execute rotated ~ 0 positioned ^ ^ ^1.6 align xyz positioned ~0.5 ~ ~0.5 run function bm:p41/sack/try with storage bm:tmp sk',
                        'execute if score #ok bm.rng matches 0 rotated ~ 0 positioned ^ ^ ^2.6 align xyz positioned ~0.5 ~ ~0.5 run function bm:p41/sack/try with storage bm:tmp sk',
                        'tag @s remove bm.sacker',
                        'execute if score #ok bm.rng matches 0 run ' + say('No room on the ground in front of you.')])
    fn('p41/sack/stamp', ['$item modify entity @s weapon.mainhand {function:"minecraft:set_custom_data",tag:{bm_sack:$(n),bm_sackset:1b}}'])
    fn('p41/sack/close_mine', ['scoreboard players set #had bm.rng 1', 'function bm:p41/sack/close'])
    lock = '{predicates:{"minecraft:custom_data":{bm_sack:$(n)}}}'
    fn('p41/sack/try', ['execute unless block ~ ~ ~ #bm:p41_open run return 0', 'execute if block ~ ~-1 ~ #minecraft:replaceable run return 0',
                        f'$setblock ~ ~ ~ minecraft:barrel[facing=up]{{lock:{lock},CustomName:{{text:"Hoard Sack",color:"#c8a050"}}}}',
                        '$data modify block ~ ~ ~ Items set from storage bm:sack s$(n)', '$data remove storage bm:sack s$(n)',
                        'summon minecraft:marker ~ ~ ~ {Tags:["bm.sackm","bm.sknew2"]}',
                        'scoreboard players operation @e[type=minecraft:marker,tag=bm.sknew2,distance=..0.5] bm.pid = #kp bm.pid',
                        'scoreboard players set @e[type=minecraft:marker,tag=bm.sknew2,distance=..0.5] bm.sackt 120',
                        'tag @e[type=minecraft:marker,tag=bm.sknew2] remove bm.sknew2', 'scoreboard players set #ok bm.rng 1',
                        'particle minecraft:wax_on ~ ~0.6 ~ 0.3 0.3 0.3 0.02 12', 'playsound minecraft:block.barrel.open block @a[distance=..16] ~ ~ ~ 1 0.8'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.sackm] at @s run function bm:p41/sack/check')
    fn('p41/sack/check', ['scoreboard players remove @s bm.sackt 1', 'scoreboard players operation #kp bm.pid = @s bm.pid', 'scoreboard players set #near bm.rng 0',
                          'execute as @a[distance=..6] if score @s bm.pid = #kp bm.pid run scoreboard players set #near bm.rng 1',
                          'execute unless block ~ ~ ~ minecraft:barrel run return run kill @s',
                          'execute if score #near bm.rng matches 0 run return run function bm:p41/sack/close',
                          'execute if score @s bm.sackt matches ..0 run function bm:p41/sack/close'])
    fn('p41/sack/close', ['execute store result storage bm:tmp sk.n int 1 run scoreboard players get @s bm.pid', 'function bm:p41/sack/close_m with storage bm:tmp sk'])
    fn('p41/sack/close_m', ['execute unless block ~ ~ ~ minecraft:barrel run return run kill @s',
                            '$data modify storage bm:sack s$(n) set from block ~ ~ ~ Items', 'data remove block ~ ~ ~ Items', 'setblock ~ ~ ~ minecraft:air',
                            'particle minecraft:wax_off ~ ~0.6 ~ 0.3 0.3 0.3 0.02 12', 'playsound minecraft:block.barrel.close block @a[distance=..16] ~ ~ ~ 1 0.8', 'kill @s'])

    # ================================================================== the Golden Cheese Wheel (placed like the statues)
    G.consume_adv('golden_cheese_wheel', 'bm:p41/cheese/use')
    fn('p41/cheese/use', ['advancement revoke @s only bm:consume/golden_cheese_wheel', 'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25',
                          'tag @s add bm.placer', 'execute anchored eyes positioned ^ ^ ^ run function bm:p41/cheese/ray', 'tag @s remove bm.placer',
                          'execute if score #placed bm.rng matches 0 unless entity @s[gamemode=creative] run ' + give('golden_cheese_wheel'),
                          'execute if score #placed bm.rng matches 0 run ' + say('Look at the top of a block within 5 blocks to set it down.')])
    fn('p41/cheese/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p41/cheese/hit',
                          'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p41/cheese/ray'])
    fn('p41/cheese/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                          'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.gchit,distance=..0.6] run return 0',
                          'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p41/cheese/spawn'])
    cdisp = {'Tags': ['bm.gcheese', 'bm.gcnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:golden_cheese3d'}},
             'item_display': 'fixed', 'brightness': {'block': Int(15), 'sky': Int(15)},
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.35), F(0)], 'scale': [F(0.9)] * 3}}
    cbox = {'Tags': ['bm.gchit', 'bm.gcnew'], 'width': F(0.9), 'height': F(0.7), 'response': B(1)}
    fn('p41/cheese/spawn', [f'summon minecraft:item_display ~ ~ ~ {snbt(cdisp)}', f'summon minecraft:interaction ~ ~ ~ {snbt(cbox)}',
                            'execute rotated as @a[tag=bm.placer,limit=1] run tp @e[tag=bm.gcnew,distance=..0.5] ~ ~ ~ ~180 0',
                            'tag @e[tag=bm.gcnew,distance=..0.5] remove bm.gcnew', 'scoreboard players set #placed bm.rng 1',
                            'playsound minecraft:block.amethyst_block.place block @a[distance=..16] ~ ~ ~ 1 0.8', 'particle minecraft:wax_on ~ ~0.6 ~ 0.4 0.3 0.4 0.02 25'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.gchit] if data entity @s attack at @s run function bm:p41/cheese/punch',
             'execute as @e[type=minecraft:interaction,tag=bm.gchit] if data entity @s interaction at @s run function bm:p41/cheese/turn']
    fn('p41/cheese/punch', ['scoreboard players set #sn bm.rng 0', 'execute on attacker if predicate bm:p20/sneaking run scoreboard players set #sn bm.rng 1',
                            'execute if score #sn bm.rng matches 0 on attacker run ' + say('Sneak + punch to pick it up.'),
                            'data remove entity @s attack', 'execute if score #sn bm.rng matches 1 run function bm:p41/cheese/pick'])
    fn('p41/cheese/pick', ['loot spawn ~ ~0.3 ~ loot bm:items/golden_cheese_wheel', 'kill @e[type=minecraft:item_display,tag=bm.gcheese,distance=..0.3]',
                           'particle minecraft:poof ~ ~0.4 ~ 0.2 0.2 0.2 0.02 6', 'playsound minecraft:block.wood.break block @a[distance=..16] ~ ~ ~ 1 0.9', 'kill @s'])
    fn('p41/cheese/turn', ['data remove entity @s interaction', 'execute as @e[type=minecraft:item_display,tag=bm.gcheese,distance=..0.3] at @s run tp @s ~ ~ ~ ~45 0'])
    # everyone within 50 blocks stays fed (a 1-second Saturation every 4 seconds), with a little sparkle
    second += ['scoreboard players add #gct bm.rng 1', 'execute if score #gct bm.rng matches 4.. run scoreboard players set #gct bm.rng 0',
               'execute if score #gct bm.rng matches 0 as @e[type=minecraft:item_display,tag=bm.gcheese] at @s run effect give @a[distance=..50] minecraft:saturation 1 0 true',
               'execute as @e[type=minecraft:item_display,tag=bm.gcheese] at @s if entity @a[distance=..24] run particle minecraft:wax_on ~ ~0.7 ~ 0.4 0.2 0.4 0 2']

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


SKIFF_RIDE_Y = -1.4           # hull translation while it rides the skiff: its centre 0.8 under the pilot's feet (both seats sit 4 x scale up)


# ===================================================================== resource pack
def rp(R):
    from PIL import Image
    grid = R.grid
    # the Blue Marlin, from the reference sprite: a horizontal fish turned to a sword's diagonal (bill = the tip)
    R.ICONS['blue_marlin'] = marlin_texture()
    R.ICONS['hoard_sack'] = grid(['................', '......KKKK......', '.....KYYYYK.....', '......KKKK......', '.....KBBBBK.....', '....KBBBBBBK....', '...KBBbBBBBBK...',
                                  '...KBBBBBBBBK...', '...KBBBYYBBBK...', '...KBBBYYBBBK...', '...KBBBBBBbBK...', '....KBBBBBBK....', '.....KKKKKK.....', '................',
                                  '................', '................'], dict(K='#3a2a1a', Y='#ffd23f', B='#a07a4a', b='#c8a070'))
    R.ICONS['golden_cheese_wheel'] = grid(['................', '................', '.....GGGGGG.....', '...GGYYYYYYGG...', '..GYYYYHYYYYYG..', '..GYYHYYYYHYYG..',
                                           '..GGYYYYYYYYGG..', '..GDGGYYYYGGDG..', '..GDDDGGGGDDDG..', '..GDDHDDDDHDDG..', '...GGDDDDDDGG...', '.....GGGGGG.....',
                                           '................', '................', '................', '................'],
                                          dict(G='#8a6a00', Y='#ffe14a', H='#c8a000', D='#e8b800'))
    # the 3D wheel: a squat gold drum with a wedge cut out and holes
    cube = R.cube
    def c(fr, to, t): return cube(fr, to, t)
    R.HATS['golden_cheese3d'] = ({'g': 'minecraft:block/gold_block', 'y': 'minecraft:block/honeycomb_block', 'h': 'minecraft:block/raw_gold_block'}, [
        c((2, 0, 4), (14, 6, 12), 'g'), c((4, 0, 2), (12, 6, 14), 'g'), c((3, 0, 3), (13, 6.01, 13), 'y'),
        c((8, 6, 8), (13, 6.1, 13), 'h'), c((5, 1, 1.9), (6.5, 2.5, 2), 'h'), c((10, 3, 1.9), (11.5, 4.5, 2), 'h'), c((13.9, 2, 6), (14, 3.5, 7.5), 'h')])
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('golden_cheese3d',)
    # the skiff's harness: an equipment asset with an empty texture, so the harness works but never renders
    def post(R2):
        im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        im.save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'happy_ghast_body', 'skiff_none.png'))
        R2.wj('assets/bm/equipment/skiff_none.json', {'layers': {'happy_ghast_body': [{'texture': 'bm:skiff_none'}]}})
    R.POST.append(post)


MARLIN_REF = '/home/user/main/bm_build/vendor/blue_marlin_ref.png'


def marlin_texture():
    """64x64: the reference pixel art (one sample per cell), bill to the upper right, the tail as the grip."""
    from PIL import Image
    ref = Image.open(MARLIN_REF).convert('RGBA')
    cw, ch = ref.width / 50.0, ref.height / 21.0
    small = Image.new('RGBA', (50, 21), (0, 0, 0, 0))
    for gy in range(21):
        for gx in range(50):
            px = ref.getpixel((int((gx + 0.5) * cw), int((gy + 0.5) * ch)))
            if px[3] < 128 or min(px[:3]) > 235: continue               # transparent / white = empty
            small.putpixel((gx, gy), px[:3] + (255,))
    small = small.transpose(Image.FLIP_LEFT_RIGHT)                       # bill to the right
    bbox = small.getbbox()
    small = small.crop(bbox)
    big = small.resize((round(small.width * 1.25), round(small.height * 1.25)), Image.NEAREST)
    turned = big.rotate(45, resample=Image.NEAREST, expand=True)         # counter-clockwise: bill up and to the right
    turned = turned.crop(turned.getbbox())
    out = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    s = min(64 / turned.width, 64 / turned.height, 1.0)
    if s < 1.0: turned = turned.resize((int(turned.width * s), int(turned.height * s)), Image.NEAREST)
    out.paste(turned, ((64 - turned.width) // 2, (64 - turned.height) // 2), turned)
    return out

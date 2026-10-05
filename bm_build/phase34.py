"""Phase 1.20 / 2.13: the market overhaul, the Dockmaster, the Gilded Roost's treasures.

THE MARKET (market2.py does the building):
- counters are one block high (they were a log under a floating top slab); the Dark Auction's tiers rise away from the
  podium (they rose toward it); cushions (26.3) replace stair "chairs" in the tavern, on the plaza benches and in the
  auction hall; the MIND THE GAP sign faces the walkway.
- water: every market sweeps away any water that isn't the fountain, the river or the two falls - when it is first
  visited and again every minute while someone is inside - and puts the docks' floor back where water took it.
- THE DOCKMASTER (Salty Sal, behind the dock office counter): the MLG Bucket (saves you from a long fall, 3 charges,
  not in the Nether), the Water Charm (puts you out when you burn, 5 times), the Kraken Conch (a rideable kraken: fast
  swimming and water breathing), the Gold Doubloon (5 Trophies + 5 Hearts of the Sea: every hostile you kill has a 1-in-200
  chance of dropping a Token), Blue Axolotls, fish and sea cosmetics and pirate goods.
- THE FENCE sells every Sealed Dungeon Map and a Key of New Beginnings (resets your conquest record so you can replay
  the dungeons).

THE GILDED ROOST (Phase 2) is underground now and very rare. Its vaults hold the GOLDEN DONADO (re-tuned: no monster
spawns within a 64 x 64 area of it; no longer sold at the Dark Auction), the Gilded Fortune set (netherite in gold),
the Blinding Light of Destiny (Looting V; a random blessing every 10 kills), Fortune's Favor (Fortune V, a switchable
3 x 3 pick), the Pocket Slot Machine (10 levels a pull; it can pay out the Lucky Pocket Watch, which freezes a creature
in place and frees it again), the Rabbit's Foot of Fortune (Lucky Nights ten times as likely while carried) and two gold
cosmetics."""
import math
from nbt import snbt, B, F, Int, D
from items import item, consumable, attr, ench, T, TOTEM, ITEMS, DYNAMIC, hat, trail, gear, weapon_attrs, armor_attrs, ARMOR_SLOT
from useitem import hold, HOLD
import market2
import mgeo

W, GF = market2.W, market2.GF
NEW_NPCS = {'dock': ('villager', 'Salty Sal, Dockmaster', 'dark_aqua', 'fisherman', 'swamp', None)}
DOCK_POS, DOCK_YAW = (10.5, W, 26.5), -90

# ===================================================================== dock goods
item('mlg_bucket', TOTEM, 'MLG Water Bucket', '#3f76e4',
     ['A trick bucket from the docks.', ('Carry it: when you fall far, it splashes', 'blue'), ('water under you and scoops it back up.', 'blue'),
      ('3 charges; one comes back every 20 s.', 'gray'), ('Water boils away in the Nether.', 'dark_gray')],
     model='minecraft:water_bucket', stack=1, glint=True, cat='builder')
item('water_charm', TOTEM, 'Water Charm', '#5ab0ff',
     ['A drop of the sea in a shell.', ('Carry it: when you catch fire,', 'blue'), ('it puts you out. 5 uses.', 'blue')],
     model='bm:water_charm', stack=1, cat='builder', comps={'minecraft:max_damage': 5, 'minecraft:damage': 0})
DYNAMIC.add('water_charm')
item('kraken_conch', TOTEM, 'Kraken Conch', '#2a8a8a',
     ['Blow it in the water and something BIG answers.', ('Right-click while swimming: ride a kraken.', 'blue'),
      ('Very fast underwater; you breathe while riding.', 'blue'), ('Sneak to dismount - it sinks home.', 'gray')],
     model='bm:kraken_conch', stack=1, cat='builder', glint=True, comps=hold('toot_horn'))
HOLD['kraken_conch'] = 'bm:p34/kraken/use'
item('gold_doubloon', TOTEM, 'Gold Doubloon', '#ffd23f',
     ['Pirate gold. Cursed? Lucky? Both.', ('Carry it: every hostile creature you kill', 'blue'), ('has a 1-in-200 chance to drop a Token.', 'blue')],
     model='bm:gold_doubloon', stack=1, cat='relic', glint=True, bold=True)
item('blue_axolotl', 'minecraft:axolotl_bucket', 'Bucket of Rare Blue Axolotl', '#3a5aff',
     ['One in twelve hundred, they say.', ('Smuggled in from a very deep lake.', 'gray')],
     cat='misc', comps={'minecraft:bucket_entity_data': {}, 'minecraft:axolotl/variant': 'blue'})
item('message_bottle', TOTEM, 'Message in a Bottle', '#c8e8ff',
     ['Hold right-click to pull the scroll out.', 'Marks the nearest buried treasure.'],
     model='minecraft:glass_bottle', glint=True, stack=16, cat='map',
     comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:item.bottle.empty', False)})
hat('fishbowl_helmet', 'Fishbowl Helmet', '#5ab0ff', 'bm:fishbowl_helmet', 'minecraft:bubble ~ ~2.0 ~ 0.25 0.2 0.25 0 2', None,
    ['A goldfish named Captain Biscuit.', ('(He approves of you.)', 'gray')])
hat('coral_crown', 'Coral Crown', '#ff6a8a', 'bm:coral_crown', 'minecraft:bubble_pop ~ ~2.2 ~ 0.3 0.1 0.3 0 2', None, ['Fit for a sea king.'])
trail('bubble_boots', 'Bubble Trail Boots', '#5ab0ff', 0x3F76E4, 'minecraft:bubble_pop ~ ~0.1 ~ 0.2 0 0.2 0 2', None, ['Squelch, squelch.'])
gear('pirate_cutlass', 'netherite_sword', "Captain's Cutlass", '#c8963c', ['Curved, notched, and very well loved.', ('+15% Attack Speed', 'blue')],
     ench(sharpness=6, looting=4, sweeping_edge=4, unbreaking=5, mending=1), 2,
     attrs=weapon_attrs('netherite_sword', 0, [attr('attack_speed', 0.15, 'mainhand', 'add_multiplied_base')]))
gear('flintlock', 'crossbow', 'Flintlock Pistol', '#8a6a4a', ['Smells of black powder and bad decisions.'],
     ench(quick_charge=3, piercing=3, unbreaking=5, mending=1), 2)
gear('anchor_boots', 'diamond_boots', 'Anchor Boots', '#4a5a6a', ['Walk the sea floor like a dry road.', ('Sink fast, stride fast underwater', 'blue')],
     ench(depth_strider=3, protection=4, unbreaking=5, mending=1), 2,
     attrs=armor_attrs('diamond', 'boots', [attr('water_movement_efficiency', 0.6, 'feet'), attr('oxygen_bonus', 4, 'feet')]))

# ===================================================================== the Fence: maps and a fresh start
item('renewal_key', TOTEM, 'Key of New Beginnings', '#e8e8ff',
     ['For conquerors who miss the climb.', ('Right-click: reset YOUR conquest record', 'blue'), ('to zero, so every dungeon can be won again.', 'blue'),
      ('(You keep everything you own.)', 'gray'), ('Used up.', 'dark_gray')],
     model='bm:renewal_key', stack=16, cat='key', glint=True, comps=hold('spyglass'))
HOLD['renewal_key'] = 'bm:p34/renew/use'

# ===================================================================== the Gilded Roost's treasures
GOLD = '#ffd23f'
LUCKY_ARMOR = {'helmet': 'Crown', 'chestplate': 'Breastplate', 'leggings': 'Greaves', 'boots': 'Sabatons'}
for p, nm in LUCKY_ARMOR.items():
    s = ARMOR_SLOT[p]
    gear(f'lucky_{p}', f'netherite_{p}', f'Gilded Fortune {nm}', GOLD,
         ['Netherite, beaten into gold leaf.', ('+2 Luck, +4 Max Health', 'blue'), ('Full set: Luck III and golden sparks', 'dark_aqua')],
         ench(protection=7, unbreaking=10, mending=1, **({'feather_falling': 6} if p == 'boots' else {}), **({'respiration': 4} if p == 'helmet' else {})), 3,
         attrs=armor_attrs('netherite', p, [attr('luck', 2, s), attr('max_health', 4, s)], bonus_tough=1),
         model=f'minecraft:golden_{p}', bold=True, custom_extra={'bm_set': 'lucky'},
         extra={'minecraft:equippable': {'slot': s, 'asset_id': 'minecraft:gold', 'equip_sound': 'minecraft:item.armor.equip_gold'}})
gear('lucky_sword', 'netherite_sword', 'Blinding Light of Destiny', GOLD,
     ['The Golden Goose\'s own blade.', ('Looting V. Every 10 kills: a random blessing', 'blue'), ('for one minute.', 'blue')],
     ench(sharpness=8, looting=5, sweeping_edge=5, fire_aspect=2, unbreaking=10, mending=1), 3,
     attrs=weapon_attrs('netherite_sword', 2, [attr('luck', 3, 'mainhand')]), model='minecraft:golden_sword', bold=True)
gear('lucky_pick', 'netherite_pickaxe', "Fortune's Favor", GOLD,
     ['A miner\'s prayer, answered.', ('Fortune V.', 'blue'), ('Sneak + right-click: switch 3 x 3 mining on or off.', 'blue')],
     ench(fortune=5, efficiency=8, unbreaking=10, mending=1), 3, model='minecraft:golden_pickaxe', bold=True,
     extra=hold('none'))
HOLD['lucky_pick'] = 'bm:p34/pick/use'
DYNAMIC.add('lucky_pick')
gear('lucky_axe', 'netherite_axe', 'Gilded Felling Axe', GOLD, ['Trees fall over themselves to be cut.'],
     ench(sharpness=7, efficiency=8, fortune=3, unbreaking=10, mending=1), 3, model='minecraft:golden_axe', bold=True)
gear('lucky_shovel', 'netherite_shovel', 'Gilded Spade', GOLD, ['Finds treasure in every scoop.'],
     ench(efficiency=8, fortune=3, unbreaking=10, mending=1), 3, model='minecraft:golden_shovel', bold=True)
item('rabbit_foot', TOTEM, "Rabbit's Foot of Fortune", GOLD,
     ['Very lucky. (Not for the rabbit.)', ('Carry it: Lucky Nights are ten times', 'blue'), ('as likely while you\'re in the Overworld.', 'blue')],
     model='minecraft:rabbit_foot', stack=1, glint=True, cat='lucky')
item('pocket_slots', TOTEM, 'Pocket Slot Machine', GOLD,
     ['A reusable scratch card with a lever.', ('Right-click: pull it - costs 10 levels.', 'blue'),
      ('Pays out like a scratch card... and sometimes', 'gray'), ('the Lucky Pocket Watch.', 'gray')],
     model='bm:pocket_slots', stack=1, cat='lucky', comps=hold('none'))
HOLD['pocket_slots'] = 'bm:p34/slots/use'
item('pocket_watch', TOTEM, 'Lucky Pocket Watch', GOLD,
     ['Tick... tock... you are getting very sleepy.', ('Right-click a creature (up to 10 blocks):', 'blue'),
      ('it freezes where it stands. Again: it wakes.', 'blue'), ('Never players, bosses or the Ender Dragon.', 'gray')],
     model='bm:pocket_watch', stack=1, cat='lucky', glint=True, bold=True, comps=hold('none'))
HOLD['pocket_watch'] = 'bm:p34/watch/use'
hat('halo_fortune', 'Halo of Fortune', GOLD, 'bm:halo_fortune', 'minecraft:wax_on ~ ~2.35 ~ 0.25 0.02 0.25 0 2', None,
    ['A ring of pure, smug luck.', ('Gold dust drifts from it.', 'gray')])
trail('midas_boots', 'Midas Treads', GOLD, 0xFFD23F, 'minecraft:dust{color:[1.0,0.82,0.25],scale:1.1} ~ ~0.1 ~ 0.2 0 0.2 0 3', None,
      ['Everything you walk on turns to gold.', '(Not really. Don\'t ask.)'])

# one of these from the Roost's victor's vault (the Golden Donado always comes too)
LUCKY_LOOT = [('lucky_helmet', 3), ('lucky_chestplate', 3), ('lucky_leggings', 3), ('lucky_boots', 3), ('lucky_sword', 3), ('lucky_pick', 3),
              ('lucky_axe', 2), ('lucky_shovel', 2), ('rabbit_foot', 3), ('pocket_slots', 2), ('halo_fortune', 2), ('midas_boots', 2)]
DESTINY = [('speed', 1, 'Swiftness'), ('strength', 1, 'Might'), ('regeneration', 1, 'Renewal'), ('resistance', 1, 'Iron Skin'),
           ('haste', 2, 'Quickness'), ('absorption', 2, 'Golden Hearts'), ('luck', 2, 'Fortune'), ('jump_boost', 1, 'Leaping')]


def extend_offers(O, offer):
    O['dock'] = [offer(('token', 5), ('mlg_bucket', 1)), offer(('token', 6), ('water_charm', 1)), offer(('medallion', 4), ('kraken_conch', 1)),
                 offer(('trophy', 5), ('gold_doubloon', 1), ('minecraft:heart_of_the_sea', 5)), offer(('trophy', 1), ('blue_axolotl', 1)),
                 offer(('token', 3), ('message_bottle', 1)), offer(('medallion', 2), ('fishbowl_helmet', 1)), offer(('medallion', 2), ('coral_crown', 1)),
                 offer(('token', 8), ('bubble_boots', 1)), offer(('medallion', 6), ('pirate_cutlass', 1)), offer(('medallion', 5), ('flintlock', 1)),
                 offer(('medallion', 5), ('anchor_boots', 1)), offer(('minecraft:cod', 12), ('token', 1)), offer(('minecraft:salmon', 10), ('token', 1))]
    O['fence'].append(offer(('token', 3), ('renewal_key', 1)))


# ===================================================================== generation
def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    import phase28 as P28
    tick, fast, second, load = [], [], [], []
    objs = ['bm.mlg dummy', 'bm.mlgt dummy', 'bm.wcd2 dummy', 'bm.dest dummy', 'bm.lp3 dummy', 'bm.lpu minecraft.used:minecraft.netherite_pickaxe',
            'bm.wtcd dummy', 'bm.slcd dummy', 'bm.krk dummy', 'bm.kmoon dummy']
    load += [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    ident = [F(0), F(0), F(0), F(1)]

    # ------------------------------------------------------------------ cushions (market seats)
    G.FUNCS['npc/spawn'][0:0] = ['execute if entity @s[tag=bm.npc.cushion] run function bm:npc/cushion']
    fn('npc/cushion', [f'execute if entity @s[tag=bm.cu_{c}] run summon minecraft:cushion ~ ~ ~ {{color:"{c}"}}' for c in ('red', 'brown', 'orange', 'purple', 'black')])

    # ------------------------------------------------------------------ market patches (every market, new or old): the Dockmaster, water
    rel = mgeo.rel
    fn('p34/dock_spawn', [l for l in G.FUNCS['npc/dock'] if not l.startswith('execute rotated as @s') and not l.startswith('tag @e[tag=bm.new')] +
       ['execute rotated ~ 0 run tp @e[tag=bm.new,distance=..2] ~ ~ ~ ~ 0', 'tag @e[tag=bm.new,distance=..2] remove bm.new'])
    # the dock office: a few props for the Dockmaster (plain blocks that read fine in any rotation)
    props = [((7, W, 24), 'minecraft:barrel'), ((8, W, 30), 'minecraft:barrel'), ((7, W, 28), 'minecraft:water_cauldron[level=3]')]
    patch = ['tag @s add bm.p34', f'execute positioned {rel(DOCK_POS)} rotated ~{DOCK_YAW} 0 run function bm:p34/dock_spawn']
    for (c, b) in props:
        if mgeo.passable(c) and mgeo.standable((c[0], c[1] - 1, c[2])):
            patch.append(f'execute positioned {rel((c[0] + 0.5, c[1] + 0.5, c[2] + 0.5))} if block ~ ~ ~ #minecraft:air run setblock ~ ~ ~ {b}')
    fn('p34/patch', patch)
    mk = 'execute as @e[type=minecraft:marker,tag=bm.mkt%s] at @s rotated as @s'
    second.append((mk % ',tag=!bm.p34') + f' if entity @a[distance=..64] if loaded {rel((4, W, 18))} if loaded {rel((18, W, 37))} run function bm:p34/patch')
    # water: sweep everything except the river channel, the pond, and the two falls (boxes in template coordinates)
    SX, SY, SZ = market2.SX, market2.SY, market2.SZ
    CX, CZ = market2.CX, market2.CZ
    keep = [((18, 0, 8), (24, 17, 85)), ((CX - 7, 4, CZ - 7), (CX + 7, 11, CZ + 7)), ((CX - 1, 4, CZ - 1), (CX + 1, SY - 1, CZ + 1))]
    # cut the market's box along every keep-box face, drop the cells inside a keep box, merge neighbours, cap at fill's limit
    cuts = [sorted({0, (SX, SY, SZ)[i]} | {k[0][i] for k in keep} | {k[1][i] + 1 for k in keep}) for i in range(3)]
    cuts[1] = [c for c in cuts[1] if c >= 2] if 2 in cuts[1] else sorted({2} | {c for c in cuts[1] if c > 2})
    cuts = [[c for c in cuts[i] if 0 <= c <= (SX, SY, SZ)[i]] for i in range(3)]
    def kept(x, y, z): return any(all(k[0][i] <= (x, y, z)[i] <= k[1][i] for i in range(3)) for k in keep)
    cells = {(i, j, l) for i in range(len(cuts[0]) - 1) for j in range(len(cuts[1]) - 1) for l in range(len(cuts[2]) - 1)
             if not kept(cuts[0][i], cuts[1][j], cuts[2][l])}
    boxes = []
    while cells:
        i, j, l = min(cells)
        i2, j2, l2 = i, j, l
        while (i, j, l2 + 1) in cells: l2 += 1
        while all((i2 + 1, j, z) in cells for z in range(l, l2 + 1)): i2 += 1
        while all((x, j2 + 1, z) in cells for x in range(i, i2 + 1) for z in range(l, l2 + 1)): j2 += 1
        for x in range(i, i2 + 1):
            for y in range(j, j2 + 1):
                for z in range(l, l2 + 1): cells.discard((x, y, z))
        lo = (cuts[0][i], cuts[1][j], cuts[2][l]); hi = (cuts[0][i2 + 1] - 1, cuts[1][j2 + 1] - 1, cuts[2][l2 + 1] - 1)
        n = math.ceil((hi[0] - lo[0] + 1) * (hi[1] - lo[1] + 1) * (hi[2] - lo[2] + 1) / 32000)
        ax = max(range(3), key=lambda a: hi[a] - lo[a])
        step = math.ceil((hi[ax] - lo[ax] + 1) / n)
        for v in range(lo[ax], hi[ax] + 1, step):
            a_, b_ = list(lo), list(hi); a_[ax] = v; b_[ax] = min(hi[ax], v + step - 1)
            boxes.append((tuple(a_), tuple(b_)))
    sweep = [f'fill {rel((a[0] + 0.5, a[1] + 0.5, a[2] + 0.5))} {rel((b[0] + 0.5, b[1] + 0.5, b[2] + 0.5))} minecraft:air replace minecraft:water' for a, b in boxes]
    # the docks' floor: plain (direction-free) blocks come back where water took them
    MB = mgeo.MB()
    restore = []
    for x in range(4, 19):
        for z in range(18, 38):
            for y in (GF, W):
                st = MB.b.get((x, y, z), '')
                if st and not any(k in st for k in ('facing', 'axis', 'rotation', 'air', 'water', 'light', 'shape')) and market2.is_full(st):
                    restore.append(f'execute positioned {rel((x + 0.5, y + 0.5, z + 0.5))} if block ~ ~ ~ minecraft:water run setblock ~ ~ ~ {st}')
    fn('p34/dry', sweep + restore)
    second += [(mk % '') + ' if entity @a[distance=..48] unless score @s bm.wcd2 matches 1.. run function bm:p34/dry_tick',
               'scoreboard players remove @e[type=minecraft:marker,tag=bm.mkt,scores={bm.wcd2=1..}] bm.wcd2 1']
    fn('p34/dry_tick', ['scoreboard players set @s bm.wcd2 60', f'execute if loaded {rel((1, W, 1))} if loaded {rel((SX - 2, W, 1))} if loaded {rel((1, W, SZ - 2))} if loaded {rel((SX - 2, W, SZ - 2))} run function bm:p34/dry'])
    G.P34_SWEEP = len(sweep)

    # ------------------------------------------------------------------ entrance shafts: underground dungeons always reach the surface
    # (inside a dungeon you can't dig - adventure mode / Mining Fatigue - so the way in is built for you). The shaft is square, so its
    # ladders (one on every inner wall) are placed in absolute directions and suit any rotation of the structure.
    SHAFT = {'brood': ('minecraft:cobbled_deepslate', 'minecraft:deepslate_tile_wall', 'minecraft:soul_lantern', 'minecraft:spruce_sign',
                       ['', 'THE NEST', 'below', ''], 'gray'),
             'lucky': ('minecraft:smooth_quartz', 'minecraft:gold_block', 'minecraft:lantern', 'minecraft:birch_sign',
                       ['THE GILDED', 'ROOST', 'all bets', 'are final'], 'yellow')}
    second += ['execute as @e[type=minecraft:marker,tag=bm.entr,tag=bm.d_brood,tag=!bm.shdone] at @s rotated as @s positioned ^-3 ^10 ^-4 '
               'unless entity @e[type=minecraft:marker,tag=bm.eshaft,distance=..3] run summon minecraft:marker ~ ~ ~ {Tags:["bm.p2","bm.d_brood","bm.eshaft"]}',
               'tag @e[type=minecraft:marker,tag=bm.entr,tag=bm.d_brood] add bm.shdone',
               'execute as @e[type=minecraft:marker,tag=bm.eshaft,tag=!bm.shdone] at @s if loaded ~2 ~ ~2 if loaded ~-2 ~ ~-2 run function bm:p34/shaft/start']
    fn('p34/shaft/start', ['tag @s add bm.shdone', 'execute align xyz positioned ~0.5 ~ ~0.5 positioned over motion_blocking_no_leaves run summon minecraft:marker ~ ~ ~ {Tags:["bm.shtop"]}',
                           'execute store result score #top bm.rng run data get entity @e[type=minecraft:marker,tag=bm.shtop,limit=1] Pos[1]',
                           'kill @e[type=minecraft:marker,tag=bm.shtop]', 'execute store result score #n bm.rng run data get entity @s Pos[1]',
                           'scoreboard players operation #top bm.rng -= #n bm.rng', 'execute if score #top bm.rng matches ..0 run return 0',
                           'scoreboard players set #lv bm.rng 0'] +
       [f'execute if entity @s[tag=bm.d_{d}] align xyz positioned ~0.5 ~ ~0.5 run function bm:p34/shaft/{d}' for d in SHAFT])
    for d, (wall, post, lamp, sign, lines, col) in SHAFT.items():
        fn(f'p34/shaft/{d}', [f'fill ~-2 ~ ~-2 ~2 ~ ~2 {wall}', 'fill ~-1 ~ ~-1 ~1 ~ ~1 minecraft:air',
                              'setblock ~ ~ ~-1 minecraft:ladder[facing=south]', 'setblock ~ ~ ~1 minecraft:ladder[facing=north]',
                              'setblock ~-1 ~ ~ minecraft:ladder[facing=east]', 'setblock ~1 ~ ~ minecraft:ladder[facing=west]',
                              'scoreboard players add #lv bm.rng 1', 'scoreboard players operation #m bm.rng = #lv bm.rng', 'scoreboard players operation #m bm.rng %= #5 bm.rng',
                              'execute if score #m bm.rng matches 0 run setblock ~2 ~ ~1 minecraft:glowstone', 'execute if score #m bm.rng matches 0 run setblock ~-2 ~ ~-1 minecraft:glowstone',
                              'scoreboard players remove #top bm.rng 1',
                              f'execute if score #top bm.rng matches 1.. positioned ~ ~1 ~ run return run function bm:p34/shaft/{d}',
                              f'execute positioned ~ ~1 ~ run function bm:p34/shaft/{d}_top'])
        sg = snbt({'front_text': {'has_glowing_text': B(1), 'color': col, 'messages': [{'text': l} for l in lines]},
                   'back_text': {'has_glowing_text': B(1), 'color': col, 'messages': [{'text': l} for l in lines]}})
        fn(f'p34/shaft/{d}_top', ['fill ~-1 ~ ~-1 ~1 ~3 ~1 minecraft:air'] +
           [f'setblock ~{x} ~ ~{z} {post}' for (x, z) in ((2, 2), (-2, -2), (2, -2), (-2, 2))] +
           [f'setblock ~{x} ~1 ~{z} {lamp}' for (x, z) in ((2, 2), (-2, -2), (2, -2))] +
           [f'setblock ~-2 ~1 ~2 {sign}[rotation=0]{sg}', 'playsound minecraft:block.stone.place block @a[distance=..48] ~ ~ ~ 0.6 0.8'])
    load.append('scoreboard players set #5 bm.rng 5')

    # ------------------------------------------------------------------ graveyards: every Blood Moon puts a fresh Black Market Key in each looted crypt
    # (a global moon counter, so crypts far from anyone catch up the next time their chunk loads)
    G.FUNCS['bloodmoon/start'].append('scoreboard players add #bmn bm.bm 1')
    tk = G.FUNCS['crypt/take_key']
    k = next(i for i, l in enumerate(tk) if l.startswith('tag @e[type=minecraft:marker,tag=bm.crypt_ctrl') and 'add bm.looted' in l)
    tk.insert(k + 1, 'scoreboard players operation @e[type=minecraft:marker,tag=bm.crypt_ctrl,distance=..40,sort=nearest,limit=1] bm.kmoon = #bmn bm.bm')
    second += ['execute as @e[type=minecraft:marker,tag=bm.crypt_ctrl,tag=bm.looted] unless score @s bm.kmoon = @s bm.kmoon run scoreboard players operation @s bm.kmoon = #bmn bm.bm',
               'execute as @e[type=minecraft:marker,tag=bm.crypt_ctrl,tag=bm.looted] if score @s bm.kmoon < #bmn bm.bm at @s unless entity @a[distance=..40] run function bm:p34/crypt_restock']
    fn('p34/crypt_restock', ['tag @s remove bm.looted', 'scoreboard players set @s bm.state 0', 'scoreboard players set @s bm.timer 0',
                             'execute as @e[type=minecraft:marker,tag=bm.key_altar,distance=..40,sort=nearest,limit=1] at @s rotated as @s positioned ^ ^1.6 ^1 '
                             'unless entity @e[type=minecraft:item_display,tag=bm.key_display,distance=..3] rotated ~180 0 run function bm:p34/key_spawn'])
    fn('p34/key_spawn', [l for l in G.FUNCS['npc/deco_key'] if l.startswith('summon')] +
       ['execute rotated ~ 0 run tp @e[tag=bm.new,distance=..2] ~ ~ ~ ~ 0', 'tag @e[tag=bm.new,distance=..2] remove bm.new'])

    # ------------------------------------------------------------------ MLG bucket
    tick += ['execute as @a[gamemode=!spectator,gamemode=!creative] if items entity @s container.* ' + holds % 'mlg_bucket' + ' at @s unless dimension minecraft:the_nether run function bm:p34/mlg/tick']
    second += ['execute as @a if items entity @s container.* ' + holds % 'mlg_bucket' + ' unless score @s bm.mlg matches 3.. run function bm:p34/mlg/recharge',
               'scoreboard players add @e[type=minecraft:marker,tag=bm.mlgw] bm.mlgt 1']
    fn('p34/mlg/recharge', ['execute unless score @s bm.mlg matches 0.. run scoreboard players set @s bm.mlg 3', 'scoreboard players add @s bm.mlgt 1',
                            'execute if score @s bm.mlgt matches 20.. run scoreboard players add @s bm.mlg 1', 'execute if score @s bm.mlgt matches 20.. run scoreboard players set @s bm.mlgt 0'])
    fn('p34/mlg/tick', ['execute unless predicate bm:p21/airborne run return 0', 'execute unless score @s bm.mlg matches 1.. run return 0',
                        'execute store result score #fd bm.rng run data get entity @s fall_distance', 'execute unless score #fd bm.rng matches 5.. run return 0',
                        'execute if predicate bm:p26/no_rocket run return 0',
                        'execute unless block ~ ~-1 ~ #bm:grap_pass run return run function bm:p34/mlg/place',
                        'execute unless block ~ ~-2 ~ #bm:grap_pass positioned ~ ~-1 ~ run return run function bm:p34/mlg/place',
                        'execute unless block ~ ~-3 ~ #bm:grap_pass positioned ~ ~-2 ~ run return run function bm:p34/mlg/place',
                        'execute unless block ~ ~-4 ~ #bm:grap_pass positioned ~ ~-3 ~ run return run function bm:p34/mlg/place'])
    fn('p34/mlg/place', ['execute unless block ~ ~ ~ #minecraft:air run return 0', 'setblock ~ ~ ~ minecraft:water', 'scoreboard players remove @s bm.mlg 1',
                         'summon minecraft:marker ~ ~ ~ {Tags:["bm.mlgw"]}', 'playsound minecraft:item.bucket.empty player @a[distance=..16] ~ ~ ~ 1 1',
                         title('@s', 'actionbar', [T('MLG! ', '#3f76e4', bold=True), {'score': {'name': '@s', 'objective': 'bm.mlg'}, 'color': 'white'}, T(' charges left', 'gray')])])
    second += ['execute as @e[type=minecraft:marker,tag=bm.mlgw,scores={bm.mlgt=2..}] at @s run function bm:p34/mlg/scoop']
    fn('p34/mlg/scoop', ['execute if block ~ ~ ~ minecraft:water[level=0] run setblock ~ ~ ~ minecraft:air', 'playsound minecraft:item.bucket.fill player @a[distance=..16] ~ ~ ~ 0.8 1', 'kill @s'])

    # ------------------------------------------------------------------ Water Charm (5 uses: its durability)
    wjson('bm/predicate/p34/burning.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_on_fire': True}}})
    fast += ['execute as @a[gamemode=!spectator,gamemode=!creative] if items entity @s container.* ' + holds % 'water_charm' + ' at @s if predicate bm:p34/burning unless block ~ ~ ~ minecraft:lava run function bm:p34/charm']
    wjson('bm/item_modifier/p34/charm_use.json', {'function': 'minecraft:set_damage', 'damage': -0.2, 'add': True})
    fn('p34/charm', ['execute unless block ~ ~ ~ #minecraft:air unless block ~ ~ ~ #minecraft:replaceable run return 0',
                     'setblock ~ ~ ~ minecraft:water', 'summon minecraft:marker ~ ~ ~ {Tags:["bm.mlgw"]}', 'particle minecraft:cloud ~ ~1 ~ 0.3 0.5 0.3 0.02 20',
                     'playsound minecraft:block.fire.extinguish player @a[distance=..16] ~ ~ ~ 1 1',
                     'scoreboard players set #cs bm.rng -1'] +
       [f'execute if score #cs bm.rng matches -1 if items entity @s container.{i} {holds % "water_charm"} run scoreboard players set #cs bm.rng {i}' for i in range(36)] +
       ['execute store result storage bm:tmp wc.n int 1 run scoreboard players get #cs bm.rng', 'function bm:p34/charm_use with storage bm:tmp wc'])
    fn('p34/charm_use', ['$item modify entity @s container.$(n) bm:p34/charm_use',
                         '$execute if items entity @s container.$(n) *[minecraft:damage=5] run item replace entity @s container.$(n) with minecraft:air',
                         title('@s', 'actionbar', T('The Water Charm puts you out.', '#5ab0ff'))])

    # ------------------------------------------------------------------ Kraken Conch: ride a kraken (a tamed, saddled nautilus wearing a kraken)
    kr = {'Tags': ['bm.kraken', 'bm.knew', 'bm.seen'], 'PersistenceRequired': B(1), 'Silent': B(1), 'Invulnerable': B(1),
          'equipment': {'saddle': {'id': 'minecraft:saddle', 'count': Int(1)}},
          'attributes': [{'id': 'minecraft:movement_speed', 'base': D(1.6)}, {'id': 'minecraft:scale', 'base': D(1.6)}],
          'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}],
          'CustomName': T('Kraken', '#2a8a8a', bold=True), 'CustomNameVisible': B(0)}
    body = {'Tags': ['bm.kbody', 'bm.knew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:kraken3d'}},
            'item_display': 'fixed', 'teleport_duration': Int(2), 'brightness': {'block': Int(12), 'sky': Int(12)},
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(-0.6), F(0)], 'scale': [F(3.2)] * 3}}
    fn('p34/kraken/use', ['execute unless block ~ ~ ~ minecraft:water unless block ~ ~1 ~ minecraft:water run return run ' + title('@s', 'actionbar', T('Blow it in deep water.', 'gray')),
                          'execute if entity @s[predicate=bm:p29/has_vehicle] run return 0',
                          'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                          f'summon minecraft:nautilus ~ ~ ~ {snbt(kr)}', f'summon minecraft:item_display ~ ~ ~ {snbt(body)}',
                          'data modify entity @e[type=minecraft:nautilus,tag=bm.knew,limit=1,sort=nearest] Owner set from entity @s UUID',
                          'scoreboard players operation @e[tag=bm.knew,distance=..3] bm.pid = @s bm.pid',
                          'ride @s mount @e[type=minecraft:nautilus,tag=bm.knew,limit=1,sort=nearest]',
                          'tag @e[tag=bm.knew,distance=..3] remove bm.knew',
                          'playsound minecraft:item.goat_horn.sound.1 player @a[distance=..48] ~ ~ ~ 1 0.5', 'particle minecraft:bubble_column_up ~ ~ ~ 1 1 1 0.2 60',
                          title('@s', 'actionbar', T('The Kraken rises! Sneak to let it go.', '#2a8a8a'))])
    tick += ['execute as @e[type=minecraft:item_display,tag=bm.kbody] at @s run function bm:p34/kraken/follow']
    fn('p34/kraken/follow', ['scoreboard players operation #kp bm.pid = @s bm.pid',
                             'execute as @e[type=minecraft:nautilus,tag=bm.kraken] if score @s bm.pid = #kp bm.pid run tag @s add bm.kme',
                             'execute unless entity @e[type=minecraft:nautilus,tag=bm.kme] run kill @s',
                             'execute at @e[type=minecraft:nautilus,tag=bm.kme,limit=1] run tp @s ~ ~ ~ ~ 0', 'tag @e[tag=bm.kme] remove bm.kme'])
    second += ['execute as @e[type=minecraft:nautilus,tag=bm.kraken] unless function bm:p34/kraken/ridden at @s run function bm:p34/kraken/sink',
               'execute as @e[type=minecraft:nautilus,tag=bm.kraken] on passengers if entity @s[type=minecraft:player] run effect give @s minecraft:water_breathing 3 0 true',
               'execute as @e[type=minecraft:nautilus,tag=bm.kraken] on passengers if entity @s[type=minecraft:player] run effect give @s minecraft:dolphins_grace 3 0 true',
               'execute as @e[type=minecraft:nautilus,tag=bm.kraken] on passengers if entity @s[type=minecraft:player] run effect give @s minecraft:night_vision 12 0 true']
    fn('p34/kraken/ridden', ['execute on passengers if entity @s[type=minecraft:player] run return 1', 'return 0'])
    fn('p34/kraken/sink', ['particle minecraft:bubble_column_up ~ ~ ~ 1 1 1 0.2 40', 'tp @s ~ -400 ~'])

    # ------------------------------------------------------------------ kills: the Gold Doubloon (1 in 200 per hostile kill), Blinding Light of Destiny
    wjson('bm/advancement/p34/kill_hostile.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': '#bm:hostile'}}]}}},
        'rewards': {'function': 'bm:p34/kill_hostile'}})
    fn('p34/kill_hostile', ['advancement revoke @s only bm:p34/kill_hostile',
                            'execute if items entity @s container.* ' + holds % 'gold_doubloon' + ' run function bm:p34/doubloon',
                            'execute unless items entity @s container.* ' + holds % 'gold_doubloon' + ' if items entity @s weapon.offhand ' + holds % 'gold_doubloon' + ' run function bm:p34/doubloon'])
    fn('p34/doubloon', ['execute store result score #r bm.rng run random value 1..200', 'execute unless score #r bm.rng matches 1 run return 0', give('token'),
                        'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.8 0.6', title('@s', 'actionbar', T('The Doubloon glints - a Token!', '#ffd23f'))])
    G.FUNCS['p33/kill'].append('execute if items entity @s weapon.mainhand ' + holds % 'lucky_sword' + ' run function bm:p34/destiny')
    fn('p34/destiny', ['scoreboard players add @s bm.dest 1', 'execute if score @s bm.dest matches ..9 run return 0', 'scoreboard players set @s bm.dest 0',
                       f'execute store result score #r bm.rng run random value 1..{len(DESTINY)}'] +
       [f'execute if score #r bm.rng matches {i} run function bm:p34/destiny_{e}' for i, (e, a, n) in enumerate(DESTINY, 1)])
    for (e, a, n) in DESTINY:
        fn(f'p34/destiny_{e}', [f'effect give @s minecraft:{e} 60 {a}', 'particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.8 0.4 0.3 40',
                                'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.4',
                                title('@s', 'actionbar', T(f'Destiny smiles: Blessing of {n} (1:00)', GOLD, bold=True))])
    # the Gilded Fortune set
    import phase15 as P15
    fn('sets/has/lucky', ['return run execute ' + ' '.join(f'if items entity @s armor.{s} *[minecraft:custom_data~{{bm_set:"lucky"}}]' for s in ('head', 'chest', 'legs', 'feet'))])
    fast.append('execute as @a[gamemode=!spectator] if function bm:sets/has/lucky at @s run function bm:p34/lucky_set')
    fn('p34/lucky_set', ['effect give @s minecraft:luck 3 2 true', 'particle minecraft:wax_on ~ ~1 ~ 0.4 0.7 0.4 0 2'])

    # ------------------------------------------------------------------ Fortune's Favor: switchable 3 x 3
    pick = holds % 'lucky_pick'
    fn('p34/pick/use', ['execute unless predicate bm:p20/sneaking run return 0',
                        'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm_3x3:1b}] run return run function bm:p34/pick/off',
                        'item modify entity @s weapon.mainhand {function:"minecraft:set_custom_data",tag:"{bm_3x3:1b}"}',
                        'playsound minecraft:block.note_block.pling player @s ~ ~ ~ 1 1.6', title('@s', 'actionbar', T("Fortune's Favor: 3 x 3 mining ON", GOLD))])
    fn('p34/pick/off', ['item modify entity @s weapon.mainhand {function:"minecraft:set_custom_data",tag:"{bm_3x3:0b}"}',
                        'playsound minecraft:block.note_block.pling player @s ~ ~ ~ 1 0.8', title('@s', 'actionbar', T("Fortune's Favor: 3 x 3 mining off", 'gray'))])
    on = '*[minecraft:custom_data~{bm:"lucky_pick",bm_3x3:1b}]'
    # every tick: remember the block you're aiming at; when the pick breaks one, its 3 x 3 neighbours go too (with Fortune)
    tick += [f'execute as @a[gamemode=survival] if items entity @s weapon.mainhand {on} at @s anchored eyes positioned ^ ^ ^ run function bm:p34/pick/aim',
             f'execute as @a[gamemode=survival,scores={{bm.lpu=1..}}] if items entity @s weapon.mainhand {on} at @s run function bm:p34/pick/burst',
             'scoreboard players reset @a bm.lpu']
    fn('p34/pick/aim', ['scoreboard players set #ray bm.rng 25', 'tag @s add bm.aimer', 'function bm:p34/pick/ray', 'tag @s remove bm.aimer'])
    fn('p34/pick/ray', ['execute unless block ~ ~ ~ #bm:grap_pass align xyz run return run function bm:p34/pick/mark',
                        'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p34/pick/ray'])
    fn('p34/pick/mark', ['execute store result storage bm:tmp lp.x int 1 run data get entity @s Pos[0]'] if False else
       ['summon minecraft:marker ~0.5 ~0.5 ~0.5 {Tags:["bm.lpt"]}', 'execute as @e[type=minecraft:marker,tag=bm.lpt,limit=1,sort=nearest] run function bm:p34/pick/store',
        'kill @e[type=minecraft:marker,tag=bm.lpt]'])
    fn('p34/pick/store', ['execute store result score @a[tag=bm.aimer,limit=1] bm.lp3 run data get entity @s Pos[1]',
                          'execute store result storage bm:tmp lp.x int 1 run data get entity @s Pos[0]', 'execute store result storage bm:tmp lp.y int 1 run data get entity @s Pos[1]',
                          'execute store result storage bm:tmp lp.z int 1 run data get entity @s Pos[2]',
                          'data modify storage bm:tmp lpp merge from storage bm:tmp lp'])
    fn('p34/pick/burst', ['execute unless data storage bm:tmp lpp.x run return 0',
                          'execute store result score #pp bm.rng run data get entity @s Rotation[1]',
                          'execute store result score #py bm.rng run data get entity @s Rotation[0]',
                          'data modify storage bm:tmp lpp.pl set value "v"',
                          'execute if score #pp bm.rng matches 50.. run data modify storage bm:tmp lpp.pl set value "h"',
                          'execute if score #pp bm.rng matches ..-50 run data modify storage bm:tmp lpp.pl set value "h"',
                          'function bm:p34/pick/burst_at with storage bm:tmp lpp', 'data remove storage bm:tmp lpp'])
    # facing north/south (yaw near 0 or 180) the plane is x/y; east/west it is z/y; looking up or down it is x/z
    fn('p34/pick/burst_at', ['$execute positioned $(x) $(y) $(z) if data storage bm:tmp {lpp:{pl:"h"}} run function bm:p34/pick/plane_h',
                             '$execute positioned $(x) $(y) $(z) if data storage bm:tmp {lpp:{pl:"v"}} if score #py bm.rng matches -45..45 run function bm:p34/pick/plane_x',
                             '$execute positioned $(x) $(y) $(z) if data storage bm:tmp {lpp:{pl:"v"}} if score #py bm.rng matches 135.. run function bm:p34/pick/plane_x',
                             '$execute positioned $(x) $(y) $(z) if data storage bm:tmp {lpp:{pl:"v"}} if score #py bm.rng matches ..-135 run function bm:p34/pick/plane_x',
                             '$execute positioned $(x) $(y) $(z) if data storage bm:tmp {lpp:{pl:"v"}} if score #py bm.rng matches 46..134 run function bm:p34/pick/plane_z',
                             '$execute positioned $(x) $(y) $(z) if data storage bm:tmp {lpp:{pl:"v"}} if score #py bm.rng matches -134..-46 run function bm:p34/pick/plane_z'])
    for nm, offs in (('h', [(a, 0, b) for a in (-1, 0, 1) for b in (-1, 0, 1)]), ('x', [(a, b, 0) for a in (-1, 0, 1) for b in (-1, 0, 1)]),
                     ('z', [(0, b, a) for a in (-1, 0, 1) for b in (-1, 0, 1)])):
        fn(f'p34/pick/plane_{nm}', [f'execute positioned ~{dx} ~{dy} ~{dz} if block ~ ~ ~ #minecraft:mineable/pickaxe run function bm:p34/pick/dig'
                                    for (dx, dy, dz) in offs if (dx, dy, dz) != (0, 0, 0)])
    fn('p34/pick/dig', ['execute if block ~ ~ ~ #bm:p34_nodig run return 0', 'loot spawn ~0.5 ~0.5 ~0.5 mine ~ ~ ~ mainhand', 'setblock ~ ~ ~ minecraft:air'])
    wjson('bm/tags/block/p34_nodig.json', {'values': ['minecraft:bedrock', 'minecraft:reinforced_deepslate', 'minecraft:end_portal_frame', 'minecraft:spawner',
                                                      'minecraft:trial_spawner', 'minecraft:vault', '#minecraft:shulker_boxes', 'minecraft:chest',
                                                      'minecraft:barrel', 'minecraft:trapped_chest', 'minecraft:ender_chest']})

    # ------------------------------------------------------------------ Pocket Slot Machine / Lucky Pocket Watch
    fn('p34/slots/use', ['execute if score @s bm.slcd matches 1.. run return 0',
                         'execute unless entity @s[level=10..] run return run ' + title('@s', 'actionbar', T('A pull costs 10 levels.', 'gray')),
                         'xp add @s -10 levels', 'scoreboard players set @s bm.slcd 2', 'playsound minecraft:block.lever.click player @s ~ ~ ~ 1 0.6',
                         'execute store result score #r bm.rng run random value 1..1000',
                         'execute if score #r bm.rng matches 1..25 run return run function bm:p34/slots/watch',
                         'scoreboard players set @s bm.sct 10'])
    fn('p34/slots/watch', [give('pocket_watch'), 'title @s times 5 40 10', title('@s', 'title', T('', 'white')),
                           title('@s', 'subtitle', T('JACKPOT! The Lucky Pocket Watch!', GOLD, bold=True)),
                           'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.2',
                           tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(' pulled the ', 'gray'), T('Lucky Pocket Watch', GOLD, bold=True), T('!', 'gray')])])
    second.append('scoreboard players remove @a[scores={bm.slcd=1..}] bm.slcd 1')
    wjson('bm/tags/entity_type/p34_nohypno.json', {'values': ['minecraft:player', 'minecraft:ender_dragon', 'minecraft:wither', 'minecraft:warden', '#bm:ray_ignore']})
    fn('p34/watch/use', ['execute if score @s bm.wtcd matches 1.. run return 0', 'scoreboard players set @s bm.wtcd 1',
                         'tag @s add bm.hyp', 'scoreboard players set #rr bm.rng 50', 'execute anchored eyes positioned ^ ^ ^0.6 run function bm:p34/watch/ray', 'tag @s remove bm.hyp'])
    fn('p34/watch/ray', ['execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                         'execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[dx=0,dy=0,dz=0,type=!#bm:p34_nohypno,tag=!bm.npc,tag=!bm.boss,tag=!bm.vboss,tag=!bm.hyp] positioned ~0.5 ~0.5 ~0.5 run return run function bm:p34/watch/hit',
                         'particle minecraft:enchant ~ ~ ~ 0 0 0 0 1', 'scoreboard players remove #rr bm.rng 1',
                         'execute if score #rr bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p34/watch/ray'])
    fn('p34/watch/hit', ['execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[dx=0,dy=0,dz=0,type=!#bm:p34_nohypno,tag=!bm.npc,tag=!bm.boss,tag=!bm.vboss,tag=!bm.hyp,limit=1,sort=nearest] at @s run function bm:p34/watch/toggle'])
    fn('p34/watch/toggle', ['execute if entity @s[tag=bm.hypno] run return run function bm:p34/watch/wake',
                            'data modify entity @s NoAI set value 1b', 'tag @s add bm.hypno', 'particle minecraft:enchant ~ ~1.5 ~ 0.3 0.3 0.3 1 40',
                            'playsound minecraft:block.note_block.chime player @a[distance=..16] ~ ~ ~ 1 0.5'])
    fn('p34/watch/wake', ['data modify entity @s NoAI set value 0b', 'tag @s remove bm.hypno', 'particle minecraft:poof ~ ~1 ~ 0.3 0.3 0.3 0.02 10',
                          'playsound minecraft:block.note_block.chime player @a[distance=..16] ~ ~ ~ 1 1.6'])
    second += ['scoreboard players remove @a[scores={bm.wtcd=1..}] bm.wtcd 1',
               'execute as @e[tag=bm.hypno] at @s if entity @a[distance=..24] run particle minecraft:enchant ~ ~1.6 ~ 0.2 0.2 0.2 0.5 3']
    # the Rabbit's Foot: Lucky Nights ten times as likely while someone in the Overworld carries one
    roll = G.FUNCS['p22/lucky/roll']
    k = next(i for i, l in enumerate(roll) if 'matches 1 run scoreboard players set #lucky bm.bm 1' in l and '#r bm.rng' in l)
    roll[k] = 'execute if score #r bm.rng <= #lchance bm.bm run scoreboard players set #lucky bm.bm 1'
    roll.insert(k, 'scoreboard players set #lchance bm.bm 1')
    roll.insert(k + 1, 'execute as @a[tag=bm.ow] if items entity @s container.* ' + holds % 'rabbit_foot' + ' run scoreboard players set #lchance bm.bm 10')
    # the Golden Donado: no monster spawns within a 64 x 64 area (it no longer tends crops)
    G.FUNCS['p29/statue/grow'] = ['scoreboard players set @s bm.dtimer 0']
    second += ['execute as @e[type=minecraft:item_display,tag=bm.gstat] at @s positioned ~-32 ~-32 ~-32 as @e[type=#bm:hostile,dx=64,dy=64,dz=64,tag=!bm.npc,tag=!bm.boss,tag=!bm.vboss,tag=!bm.dgmob,tag=!bm.minion,tag=!bm.hypno] if data entity @s {PersistenceRequired:0b} at @s run function bm:p34/gstat_shoo']
    fn('p34/gstat_shoo', ['particle minecraft:wax_on ~ ~1 ~ 0.3 0.5 0.3 0 8', 'tp @s ~ -400 ~'])

    # ------------------------------------------------------------------ sealed messages, the renewal key
    wjson('bm/loot_table/maps/message_bottle.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [{
        'type': 'minecraft:item', 'name': 'minecraft:filled_map', 'functions': [
            {'function': 'minecraft:exploration_map', 'destination': 'minecraft:on_treasure_maps', 'decoration': 'minecraft:red_x', 'zoom': 1,
             'search_radius': 50, 'skip_existing_chunks': False},
            {'function': 'minecraft:set_name', 'target': 'item_name', 'name': T('Soggy Treasure Map', '#c8e8ff')}]}]}]})
    G.consume_adv('message_bottle', 'bm:p34/bottle')
    fn('p34/bottle', ['advancement revoke @s only bm:consume/message_bottle', 'loot give @s loot bm:maps/message_bottle',
                      title('@s', 'actionbar', T('A soggy scroll... X marks the spot.', '#c8e8ff'))])
    MENU_RENEW = 950
    P28.MENU['renew'] = MENU_RENEW
    dlg = P28.multi([T('Key of New Beginnings', '#e8e8ff', bold=True)],
                    [P28.body([T('Reset your conquest record to zero? Every dungeon - and every first-victory reward - can then be won again. ', 'gray'),
                               T('You keep everything you own.', 'white')])],
                    [P28.btn(T('Yes - start over', 'gold'), 7101, width=200), P28.btn(T('No', 'gray'), 7102, width=200)], columns=2)
    fn('p34/renew/use', [f'scoreboard players set @s bm.menu {MENU_RENEW}', f'dialog show @s {P28.inline(dlg)}'])
    G.FUNCS['p28/act'].append('execute if score #act bm.pay matches 7101..7102 run return run function bm:p34/renew/act')
    fn('p34/renew/act', [f'execute unless score @s bm.menu matches {MENU_RENEW} run return run function bm:p28/stale', 'scoreboard players set @s bm.menu 0',
                         'execute if score #act bm.pay matches 7102 run return 0',
                         'execute unless items entity @s container.* ' + holds % 'renewal_key' + ' unless items entity @s weapon.offhand ' + holds % 'renewal_key' + ' run return run function bm:p28/stale',
                         'clear @s ' + holds % 'renewal_key' + ' 1', 'scoreboard players set @s bm.conq 0',
                         'tag @s remove bm.got_warp', 'playsound minecraft:block.end_portal.spawn player @s ~ ~ ~ 0.5 1.6',
                         'title @s times 10 60 20', title('@s', 'subtitle', T('Your conquest record is clear. The road begins again.', 'gray', italic=True)),
                         title('@s', 'title', T('A NEW BEGINNING', '#e8e8ff', bold=True))])

    G.FUNCS['load'][-1:-1] = load
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack
def rp(R):
    grid = R.grid
    I = {}
    I['water_charm'] = grid([
        '................', '................', '.......BB.......', '......BLLB......', '.....BLWWLB.....', '.....BLWWLB.....',
        '....BLLWWLLB....', '....BLLLLLLB....', '....BBLLLLBB....', '.....BBLLBB.....', '......BBBB......', '.......SS.......',
        '......S..S......', '................', '................', '................'], dict(B='#2a5ab0', L='#5ab0ff', W='#e0f4ff', S='#c8b08a'))
    I['kraken_conch'] = grid([
        '................', '..........PP....', '.........PCCP...', '........PCCCP...', '.......PCCWCP...', '......PCCWWCP...',
        '.....PCCWWCCP...', '....PCCWWCCP....', '...PCCWCCCP.....', '..PCCCCCPP......', '..PCCCPP........', '...PPP..........',
        '................', '................', '................', '................'], dict(P='#7a4a3a', C='#e8b898', W='#fff0e0'))
    I['gold_doubloon'] = grid([
        '................', '.....GGGGGG.....', '....GYYYYYYG....', '...GYYGGGGYYG...', '..GYYGYYYYGYYG..', '..GYGYYKKYYGYG..',
        '..GYGYKYYKYGYG..', '..GYGYYKKYYGYG..', '..GYGYKYYYYGYG..', '..GYYGYKKYGYYG..', '...GYYGGGGYYG...', '....GYYYYYYG....',
        '.....GGGGGG.....', '................', '................', '................'], dict(G='#b8860b', Y='#ffd23f', K='#8a5a0a'))
    I['renewal_key'] = grid([
        '................', '....WWW.........', '...W...W........', '...W.Y.W........', '...W...W........', '....WWWSSSSSSS..',
        '...........S.S..', '...........S.SS.', '................', '................', '................', '................',
        '................', '................', '................', '................'], dict(W='#e8e8ff', Y='#ffd23f', S='#c8c8e8'))
    I['pocket_slots'] = grid([
        '................', '...GGGGGGGGG....', '..GRRRRRRRRRG...', '..GRWWRWWRWWRGK.', '..GRW7RW7RW7RGK.', '..GRWWRWWRWWRG.K',
        '..GRRRRRRRRRRG.K', '..GGGGGGGGGGGG.K', '..GYYYYYYYYYYG..', '..GYYKKKKKKYYG..', '..GGGGGGGGGGGG..', '................',
        '................', '................', '................', '................'], {'G': '#b8860b', 'R': '#c0392b', 'W': '#ffffff', '7': '#c0392b', 'Y': '#ffd23f', 'K': '#3a2a1a'})
    I['pocket_watch'] = grid([
        '.......GG.......', '......G..G......', '.......GG.......', '.....GGGGGG.....', '....GWWWWWWG....', '...GWWWKWWWWG...',
        '...GWWWKWWWWG...', '...GWWWKKKWWG...', '...GWWWWWWWWG...', '...GWWWWWWWWG...', '....GWWWWWWG....', '.....GGGGGG.....',
        '................', '................', '................', '................'], dict(G='#ffd23f', W='#fffbe8', K='#3a2a1a'))
    for k, v in I.items(): R.ICONS[k] = v
    cube = R.cube
    def c(fr, to, t, rot=None):
        e = cube(fr, to, t)
        if rot: e['rotation'] = rot
        return e
    R.HATS['fishbowl_helmet'] = ({'g': 'minecraft:block/glass', 'w': 'minecraft:block/light_blue_stained_glass', 'o': 'minecraft:block/orange_terracotta'}, [
        c((2.5, 7.5, 2.5), (13.5, 17.5, 13.5), 'g'), c((3, 7.6, 3), (13, 12, 13), 'w'), c((6, 13, 7), (10, 15, 9), 'o'), c((10, 13.3, 7.5), (11.5, 14.7, 8.5), 'o')])
    R.HATS['coral_crown'] = ({'r': 'minecraft:block/fire_coral_block', 'b': 'minecraft:block/brain_coral_block', 't': 'minecraft:block/tube_coral_block'}, [
        c((3.5, 8, 3.5), (12.5, 9.5, 12.5), 'r'), c((4, 9.5, 4), (5.5, 12.5, 5.5), 'b'), c((10.5, 9.5, 4), (12, 13, 5.5), 't'),
        c((4, 9.5, 10.5), (5.5, 13, 12), 't'), c((10.5, 9.5, 10.5), (12, 12, 12), 'b'), c((7.2, 9.5, 3.6), (8.8, 14, 5.2), 'r')])
    R.HATS['halo_fortune'] = ({'g': 'minecraft:block/gold_block', 'y': 'minecraft:block/glowstone'}, [
        c((3, 17.5, 3), (13, 18.3, 4.5), 'g'), c((3, 17.5, 11.5), (13, 18.3, 13), 'g'), c((3, 17.5, 4.5), (4.5, 18.3, 11.5), 'g'),
        c((11.5, 17.5, 4.5), (13, 18.3, 11.5), 'g'), c((7.4, 18.3, 3.2), (8.6, 19.5, 4.4), 'y')])
    # the kraken: a squid's head with thick tentacles trailing behind (scaled up on its display)
    kt = {'k': 'minecraft:block/dark_prismarine', 'p': 'minecraft:block/prismarine', 'e': 'minecraft:block/sea_lantern', 'm': 'minecraft:block/black_concrete'}
    els = [c((4, 6, 3), (12, 13, 11), 'k'), c((4.5, 9, 2.8), (6.5, 11, 3.0), 'e'), c((9.5, 9, 2.8), (11.5, 11, 3.0), 'e'), c((5, 12.8, 4), (11, 14, 10), 'p')]
    for i, (x, y) in enumerate(((4.5, 6.5), (7, 6.5), (9.5, 6.5), (4.5, 8.8), (9.5, 8.8), (7, 9.8))):
        els.append(c((x, y, 11), (x + 2, y + 2, 16), 'p', {'origin': [x + 1, y + 1, 11], 'axis': 'x', 'angle': 22.5 if i % 2 else -22.5}))
    R.HATS['kraken3d'] = (kt, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('kraken3d',)

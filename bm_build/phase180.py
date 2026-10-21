"""2.84d: THE OMNI TOKEN - the Nether's and the End's rats get something worth saving for - and hard mode for those who earned it.

THE OMNI TOKEN   a Dread Token, 16 Ember Scales and 16 Void Shards tossed down together (a ground forge) fuse into one.
GOLDEN DOLLS (the Ember Rat, 1 Omni Token each)   a solid-gold chibi of every follower - only for followers you've met (the
              others stay under wraps on his list). Sneak + use on a block: it stands there, and while it does it gives its own
              gift within 8 blocks: Emma Regeneration, Cecil Fire Resistance, Celi Speed, Zib Night Vision, KillerWatt Strength,
              Leo Resistance, Democratus slows monsters, Apophiss weakens them, Tullius Water Breathing and Dolphin's Grace, the
              Frog Jump Boost II, Donado Luck II, Wilfrey keeps you fed, Fishy Conduit Power, Dennis Haste, Pistachio lights up
              monsters (16 blocks), King Omega sets the undead burning (10 blocks), Pearlman Hero of the Village. Punch it: back
              in your pack.
THE ELDRITCH PANOPLY (the Void Rat, Omni Tokens)   a set out of the outer dark: the Crown of Eyes, the Carapace, the Greaves
              and the Treads (24 armour, 20 toughness, +16 health). Full set: Night Vision, darkness and blindness never take,
              monsters within 6 blocks are weakened, and whatever strikes you is lashed back (3 damage and Wither).
              THE MAW OF THE OUTER DARK  a toothed, eyed greatsword (+5 damage): one hit in three bites again (4, through armour,
              and Wither); a kill feeds you two hearts of Absorption.
              THE GNAWING PICK (Haste I held, +2 reach), THE RENDING AXE (+4 damage), THE BURROWING SPADE (digs twice as fast).
              All four are their own 3D models - void-black, bone-toothed, with an eye that blinks.
HARD MODE, EARNED   Vesper's window and Ledger show nothing to anyone who hasn't beaten the Hollow King (his window shows only
              while every player at his counter has), and Dread monsters rise only where the nearest player has beaten him. A
              Key of New Beginnings puts a player back outside it.
"""
from items import item, attr, ench, T, TOTEM, ITEMS, ARMOR_SLOT, weapon_attrs
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import phase15 as P15
import phase22 as R22
import phase158 as P158
import phase160 as P160

OMNI, ELD, GOLD = '#e8a8ff', '#b04ae8', '#ffd24a'
PIECES = ['helmet', 'chestplate', 'leggings', 'boots']
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'

# ================================================================== THE OMNI TOKEN (and its forge)
item('omni_token', TOTEM, 'Omni Token', OMNI,
     ['A Dread Token that swallowed the Nether and the End.', ('The Ember Rat and the Void Rat take it.', 'blue'),
      ('Forged: a Dread Token, 16 Ember Scales and', 'gray'), ('16 Void Shards, tossed down together.', 'gray')],
     model='bm:omni_token', glint=True, stack=64, cat='currency')
P160.RECIPES.append(('omni', 'Omni Token', OMNI, ['0.69,0.06,0.16', '1.0,0.48,0.1', '0.69,0.36,1.0'],
                     (holds('dread_token'), 1), [(holds('ember_scale'), 16), (holds('void_shard'), 16)], None, None))
P160.RESULT['omni'] = 'omni_token'

# ================================================================== GOLDEN DOLLS
DOLL_OF = dict({k: d for d, k in P158.DOLL_KIND.items()}, emma='emma_doll')      # follower (its bm:met/ key): its doll
P = '@a[distance=..8,gamemode=!spectator]'
H = '@e[type=#bm:hostile,distance=..8]'
GIFT = {  # follower: (what it does, commands run each second at the doll)
    'emma': ('Regeneration', [f'effect give {P} minecraft:regeneration 3 0 true']),
    'cecil': ('Fire Resistance', [f'effect give {P} minecraft:fire_resistance 3 0 true']),
    'celi': ('Speed', [f'effect give {P} minecraft:speed 3 0 true']),
    'zib': ('Night Vision', [f'effect give {P} minecraft:night_vision 15 0 true']),
    'killerwatt': ('Strength', [f'effect give {P} minecraft:strength 3 0 true']),
    'leo': ('Resistance', [f'effect give {P} minecraft:resistance 3 0 true']),
    'demo': ('monsters slowed', [f'effect give {H} minecraft:slowness 3 1']),
    'apo': ('monsters weakened', [f'effect give {H} minecraft:weakness 3 0']),
    'tul': ('Water Breathing and Dolphin\'s Grace', [f'effect give {P} minecraft:water_breathing 15 0 true', f'effect give {P} minecraft:dolphins_grace 3 0 true']),
    'frog': ('Jump Boost II', [f'effect give {P} minecraft:jump_boost 3 1 true']),
    'donado': ('Luck II', [f'effect give {P} minecraft:luck 3 1 true']),
    'wil': ('never hungry', [f'effect give {P} minecraft:saturation 1 0 true']),
    'fishy': ('Conduit Power', [f'effect give {P} minecraft:conduit_power 15 0 true']),
    'dennis': ('Haste', [f'effect give {P} minecraft:haste 3 0 true']),
    'pistachio': ('monsters light up (16 blocks)', ['effect give @e[type=#bm:hostile,distance=..16] minecraft:glowing 3 0 true']),
    'omega': ('the undead burn (10 blocks)', ['execute as @e[type=#minecraft:undead,distance=..10] run data merge entity @s {Fire:60s}']),
    'ashur': ('Fire Resistance', [f'effect give {P} minecraft:fire_resistance 15 0 true']),
    'pearl': ('Hero of the Village', [f'effect give {P} minecraft:hero_of_the_village 15 0 true']),
}
assert set(GIFT) == set(DOLL_OF), sorted(set(GIFT) ^ set(DOLL_OF))
GDOLLS = list(GIFT)
for _k in GDOLLS:
    _nm = ITEMS[DOLL_OF[_k]]['name']
    item(f'gdoll_{_k}', TOTEM, f'Golden {_nm}', GOLD,
         ['Solid gold, and warm to the touch.', (f'Set down: {GIFT[_k][0]} within 8 blocks.' if '(' not in GIFT[_k][0] else f'Set down: {GIFT[_k][0]}.', 'blue'),
          ('Sneak + use on a block to set it down;', 'gray'), ('punch it to pick it back up.', 'gray'), ('From the Ember Rat, for an Omni Token.', 'dark_gray')],
         model=f'bm:gdoll_{_k}', stack=1, glint=True, cat='fun', comps=hold('none'))
_tok = len(R22.EMBER_OFFERS) - 1                                   # (his Token trade stays last)
R22.EMBER_OFFERS[_tok:_tok] = [(('omni_token', 1), (f'gdoll_{k}', 1)) for k in GDOLLS]

# ================================================================== THE ELDRITCH PANOPLY
ELD_NAMES = {'helmet': 'Crown of Eyes', 'chestplate': 'Carapace', 'leggings': 'Greaves', 'boots': 'Treads'}
ELD_ARMOR = {'helmet': 4, 'chestplate': 9, 'leggings': 7, 'boots': 4}
for _p in PIECES:
    _s = ARMOR_SLOT[_p]
    _e = ench(protection=8, unbreaking=10, mending=1)
    if _p == 'helmet': _e.update(ench(respiration=3, aqua_affinity=1))
    if _p == 'leggings': _e.update(ench(swift_sneak=5))
    if _p == 'boots': _e.update(ench(feather_falling=10, depth_strider=3))
    item(f'eld_{_p}', f'minecraft:netherite_{_p}', f'Eldritch {ELD_NAMES[_p]}', ELD,
         ['Out of the outer dark. It watches.', ('+4 Max Health', 'blue'), ('Full set: Night Vision; darkness and blindness', 'dark_aqua'),
          ('never take; monsters near you weaken;', 'dark_aqua'), ('whatever strikes you is lashed back.', 'dark_aqua'), ('From the Void Rat.', 'dark_gray')],
         model=f'bm:eld_{_p}', stack=1, cat='gear', bold=True,
         comps={'minecraft:enchantments': _e,
                'minecraft:attribute_modifiers': [attr('armor', ELD_ARMOR[_p], _s, ident=f'minecraft:armor.{_p}'),
                                                  attr('armor_toughness', 5, _s, ident=f'minecraft:armor.{_p}_toughness'),
                                                  attr('knockback_resistance', 0.15, _s, ident=f'minecraft:armor.{_p}_kb'), attr('max_health', 4, _s)],
                'minecraft:equippable': {'slot': _s, 'asset_id': 'bm:eldritch', 'equip_sound': 'minecraft:item.armor.equip_netherite'}},
         custom_extra={'bm_set': 'eldritch'})
P15.SET_FX['eldritch'] = (['effect give @s minecraft:night_vision 15 0 true', 'effect clear @s minecraft:darkness', 'effect clear @s minecraft:blindness',
                           'effect give @e[type=#bm:hostile,distance=..6] minecraft:weakness 2 0'],
                          'minecraft:dust{color:[0.69,0.29,0.91],scale:1.0}', 'particle minecraft:reverse_portal ~ ~1.2 ~ 0.3 0.5 0.3 0.01 2')
item('eld_maw', 'minecraft:netherite_sword', 'Maw of the Outer Dark', ELD,
     ['It has teeth. It has an eye. It is hungry.', ('+5 Attack Damage', 'blue'), ('One hit in three, it bites again:', 'blue'),
      ('4 damage through armour, and Wither.', 'blue'), ('A kill feeds you two hearts of Absorption.', 'blue'), ('From the Void Rat.', 'dark_gray')],
     model='bm:eld_maw', stack=1, cat='gear', bold=True,
     comps={'minecraft:enchantments': dict(ench(sharpness=10, looting=6, sweeping_edge=6, unbreaking=10, mending=1), **{'bm:devour': 1}),
            'minecraft:attribute_modifiers': [attr('attack_damage', 12, 'mainhand', ident='minecraft:base_attack_damage'),
                                              attr('attack_speed', -2.6, 'mainhand', ident='minecraft:base_attack_speed')]})
item('eld_pick', 'minecraft:netherite_pickaxe', 'Gnawing Pick', ELD,
     ['Its mandibles close on the stone.', ('Haste I while held; +2 block reach.', 'blue'), ('From the Void Rat.', 'dark_gray')],
     model='bm:eld_pick', stack=1, cat='gear', bold=True,
     comps={'minecraft:enchantments': ench(efficiency=10, fortune=6, unbreaking=10, mending=1),
            'minecraft:attribute_modifiers': weapon_attrs('netherite_pickaxe', 0, [attr('block_interaction_range', 2, 'mainhand')])})
item('eld_axe', 'minecraft:netherite_axe', 'Rending Axe', ELD,
     ['A jaw on a haft.', ('+4 Attack Damage', 'blue'), ('From the Void Rat.', 'dark_gray')],
     model='bm:eld_axe', stack=1, cat='gear', bold=True,
     comps={'minecraft:enchantments': ench(efficiency=10, sharpness=10, unbreaking=10, mending=1), 'minecraft:attribute_modifiers': weapon_attrs('netherite_axe', 4)})
item('eld_shovel', 'minecraft:netherite_shovel', 'Burrowing Spade', ELD,
     ['It wants to be under the ground.', ('Digs twice as fast.', 'blue'), ('From the Void Rat.', 'dark_gray')],
     model='bm:eld_shovel', stack=1, cat='gear', bold=True,
     comps={'minecraft:enchantments': ench(efficiency=10, fortune=6, unbreaking=10, mending=1),
            'minecraft:attribute_modifiers': [attr('attack_damage', 6.5, 'mainhand', ident='minecraft:base_attack_damage'),
                                              attr('attack_speed', -3.0, 'mainhand', ident='minecraft:base_attack_speed'),
                                              attr('block_break_speed', 1.0, 'mainhand', 'add_multiplied_base')]})
ELD_PRICE = {'eld_helmet': 3, 'eld_chestplate': 4, 'eld_leggings': 4, 'eld_boots': 3, 'eld_maw': 4, 'eld_pick': 2, 'eld_axe': 2, 'eld_shovel': 2}
_tok = len(R22.VOID_OFFERS) - 1
R22.VOID_OFFERS[_tok:_tok] = [(('omni_token', n), (iid, 1)) for iid, n in ELD_PRICE.items()]
ELD_TOOLS = ['eld_maw', 'eld_pick', 'eld_axe', 'eld_shovel']


def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    import phase177 as P177
    PRE = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    second, fast, load = G.FUNCS['loop/second'], G.FUNCS['loop/fast'], G.FUNCS['load']
    objs = ['bm.gmask']
    load[-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ---------------------------------------------------------------- golden dolls: set down, their gifts
    for i, k in enumerate(GDOLLS):
        P177.placeable(G, 'p180', f'gdoll_{k}', f'bm.gd{i}', scale=0.9, sound='minecraft:block.amethyst_block')
        fn(f'p180/gift/{k}', GIFT[k][1] + ['particle minecraft:wax_on ~ ~0.9 ~ 0.25 0.3 0.25 0 2'])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.gd{i}m] at @s run function bm:p180/gift/{k}')
    # the Ember Rat's list: a doll shows only to someone who has met its follower (the nearest at his counter); the rest are wrapped
    wrapped = snbt({'id': 'minecraft:paper', 'count': 1, 'components': {
        'minecraft:item_model': 'minecraft:barrier', 'minecraft:item_name': T('A golden doll still under wraps', 'gray', italic=True),
        'minecraft:lore': [T("The Ember Rat won't say whose it is.", 'dark_gray'), T("Meet them out in the world, and it's yours to buy.", 'dark_gray')],
        'minecraft:custom_data': {'bm_wrapped': B(1)}}})
    idx = {k: n for n, (_b, sell) in enumerate(R22.EMBER_OFFERS) for k in GDOLLS if isinstance(sell, tuple) and sell[0] == f'gdoll_{k}'}
    assert len(idx) == len(GDOLLS)
    tick = ['tag @a remove bm.gcust', 'execute as @a[gamemode=!spectator,distance=..6,sort=nearest,limit=1] run tag @s add bm.gcust',
            'scoreboard players set #gm bm.rng 0'] + \
           [f'execute as @a[tag=bm.gcust,advancements={{bm:met/{k}=true}}] run scoreboard players add #gm bm.rng {1 << i}' for i, k in enumerate(GDOLLS)] + \
           ['tag @a remove bm.gcust', 'execute if score @s bm.gmask = #gm bm.rng run return 0', 'scoreboard players operation @s bm.gmask = #gm bm.rng',
            'scoreboard players operation #dr bm.rng = #gm bm.rng']
    for i, k in reversed(list(enumerate(GDOLLS))):
        n, sell = idx[k], snbt(G.offer(('omni_token', 1), (f'gdoll_{k}', 1))['sell'])
        tick += [f'execute if score #dr bm.rng matches {1 << i}.. run data modify entity @s Offers.Recipes[{n}].sell set value {sell}',
                 f'execute if score #dr bm.rng matches {1 << i}.. run data modify entity @s Offers.Recipes[{n}].maxUses set value 2147483647',
                 f'execute if score #dr bm.rng matches ..{(1 << i) - 1} run data modify entity @s Offers.Recipes[{n}].sell set value {wrapped}',
                 f'execute if score #dr bm.rng matches ..{(1 << i) - 1} run data modify entity @s Offers.Recipes[{n}].maxUses set value 0',
                 f'execute if score #dr bm.rng matches {1 << i}.. run scoreboard players remove #dr bm.rng {1 << i}']
    fn('p180/ember_tick', tick)
    second.append('execute as @e[type=minecraft:wandering_trader,tag=bm.frat_ember] at @s run function bm:p180/ember_tick')
    # (a fresh Ember Rat is wrapped up before anyone can see him: his first second does it - and he arrives far below, then rises)
    G.FUNCS['p22/rat/dress_ember'].insert(0, 'function bm:p180/ember_tick')

    # ---------------------------------------------------------------- the Eldritch Panoply: the lash, the Maw's bite and feast, the tools
    k = next(i for i, l in enumerate(fast) if l == 'scoreboard players reset @a bm.dmg')
    fast.insert(k, 'execute as @a[scores={bm.dmg=1..},gamemode=!spectator] if function bm:sets/has/eldritch at @s run function bm:p180/lash')
    fn('p180/lash', ['execute on attacker run function bm:p180/lashed', 'particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.6 0.4 0.05 12'])
    fn('p180/lashed', ['execute if entity @s[type=minecraft:player] run return 0', 'damage @s 3 minecraft:magic', 'effect give @s minecraft:wither 3 0',
                       'execute at @s run particle minecraft:squid_ink ~ ~1 ~ 0.3 0.4 0.3 0.05 10'])
    wjson('bm/enchantment/devour.json', {'anvil_cost': 8, 'description': T('Devour', ELD), 'max_level': 1, 'weight': 1,
                                         'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0},
                                         'slots': ['mainhand'], 'supported_items': 'minecraft:netherite_sword', 'effects': {'minecraft:post_attack': [
                                             {'enchanted': 'attacker', 'affected': 'victim', 'requirements': {'condition': 'minecraft:random_chance', 'chance': 0.33},
                                              'effect': {'type': 'minecraft:all_of', 'effects': [
                                                  {'type': 'minecraft:damage_entity', 'damage_type': 'minecraft:magic', 'min_damage': 4.0, 'max_damage': 4.0},
                                                  {'type': 'minecraft:apply_mob_effect', 'to_apply': 'minecraft:wither', 'min_duration': 3.0, 'max_duration': 3.0,
                                                   'min_amplifier': 0.0, 'max_amplifier': 0.0},
                                                  {'type': 'minecraft:run_function', 'function': 'bm:p180/bite'}]}}]}})
    fn('p180/bite', ['particle minecraft:squid_ink ~ ~1 ~ 0.3 0.4 0.3 0.05 14', 'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.5 0.3 0.1 16',
                     'playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..12] ~ ~ ~ 0.7 0.8'])
    wjson('bm/advancement/p180/maw_kill.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
        'player': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {
            'equipment': {'mainhand': {'predicates': {'minecraft:custom_data': '{bm:"eld_maw"}'}}}}}]}}}, 'rewards': {'function': 'bm:p180/maw_kill'}})
    fn('p180/maw_kill', ['advancement revoke @s only bm:p180/maw_kill', 'effect give @s minecraft:absorption 10 0 true',
                         'particle minecraft:reverse_portal ~ ~1.2 ~ 0.3 0.4 0.3 0.05 20'])
    second.append(f'execute as @a if items entity @s weapon.mainhand {holds("eld_pick")} run effect give @s minecraft:haste 2 0 true')

    # ---------------------------------------------------------------- Vesper: nothing for those who haven't beaten the Hollow King
    locked = G.offer(('dread_token', 64), ('dread_token', 1))
    locked['sell'] = {'id': 'minecraft:paper', 'count': Int(1), 'components': {
        'minecraft:item_model': 'minecraft:barrier', 'minecraft:item_name': T("Vesper's wares are veiled", 'gray', italic=True),
        'minecraft:lore': [T('"Fell the Hollow King, little one.', 'dark_gray'), T('Then we shall talk business."', 'dark_gray')]}}
    locked['maxUses'] = Int(0)
    LOCK = snbt({'Recipes': [locked]})
    patch = G.FUNCS['p35/patch']
    k = next(i for i, l in enumerate(patch) if 'tag=bm.vesper,distance=..3] run data modify entity @s Offers set value ' in l)
    full = patch[k][patch[k].index('Offers set value ') + len('Offers set value '):]
    patch[k] = patch[k][:patch[k].index('run data modify')] + 'run function bm:p180/v/lock'
    fn('p180/v/lock', [f'data modify entity @s Offers set value {LOCK}', 'tag @s remove bm.vfull'])
    fn('p180/v/full', [f'data modify entity @s Offers set value {full}', 'tag @s add bm.vfull'])
    fn('p180/v/tick', ['scoreboard players set #vok bm.rng 0', 'execute if entity @a[distance=..6,gamemode=!spectator] run scoreboard players set #vok bm.rng 1',
                       'execute as @a[distance=..6,gamemode=!spectator] unless score @s bm.conq matches 6.. run scoreboard players set #vok bm.rng 0',
                       'execute if score #vok bm.rng matches 1 unless entity @s[tag=bm.vfull] run function bm:p180/v/full',
                       'execute if score #vok bm.rng matches 0 if entity @s[tag=bm.vfull] run function bm:p180/v/lock'])
    second.append('execute as @e[type=minecraft:villager,tag=bm.vesper] at @s run function bm:p180/v/tick')
    G.FUNCS['p177/spawn'].insert(1, 'execute as @e[type=minecraft:villager,tag=bm.vesper,distance=..1] run function bm:p180/v/lock')
    G.FUNCS['p177/open'].insert(0, 'execute unless score @s bm.conq matches 6.. run return run ' +
                                tellraw('@s', PRE + [T('Vesper: ', '#b0102a', bold=True), T('"My Ledger is for those who felled the Hollow King. Come back when you have."', '#c8a0a0', italic=True)]))

    # ---------------------------------------------------------------- Dread monsters: only where the nearest player has beaten the King
    n = 0
    for name, L in G.FUNCS.items():
        if not name.startswith('p176/roll/'): continue
        dl = [i for i, l in enumerate(L) if l.startswith('execute if score #hr bm.rng matches 1..') and 'p176/mk/' in l or
              (l.startswith('execute if score #hr bm.rng matches 1..') and l.endswith('run return 1') and i > 0 and 'p176/mk/' in L[i - 1])]
        if not dl: continue
        for i in dl:
            L[i] = L[i].replace('execute if score #hr', 'execute if score #dok bm.rng matches 1 if score #hr', 1)
        L[0:0] = ['scoreboard players set #dok bm.rng 0',
                  'execute as @p[gamemode=!spectator] if score @s bm.conq matches 6.. run scoreboard players set #dok bm.rng 1']
        n += 1
    assert n >= 10, n
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/omni', 'yellow'), T('  Omni Tokens, every golden doll, the Eldritch Panoply', 'gray')])]
    fn('admin/omni', [give('omni_token', 16)] + [give(f'gdoll_{k}') for k in GDOLLS] + [give(f'eld_{p}') for p in PIECES] + [give(t) for t in ELD_TOOLS])


# ================================================================== resource pack
VAN = '/home/claude/mc263/client/assets/minecraft/textures'
EYE_FRAMES = 2


def textures():
    """the eldritch block textures: the void, its flesh, its bone, and a blinking eye (two frames)"""
    from PIL import Image, ImageDraw
    import random
    rnd = random.Random(2084)
    T_ = {}
    void = Image.new('RGBA', (16, 16)); px = void.load()
    for y in range(16):
        for x in range(16):
            v = rnd.randint(-5, 6)
            px[x, y] = (18 + v, 8 + v // 2, 30 + v, 255)
    for _ in range(9):
        x, y = rnd.randrange(16), rnd.randrange(16); px[x, y] = rnd.choice([(230, 140, 255, 255), (255, 255, 255, 255), (150, 80, 220, 255)])
    for x in range(16):                                            # a faint violet swirl through it
        y = int(8 + 5 * __import__('math').sin(x / 2.5)); px[x, y % 16] = (70, 30, 110, 255)
    T_['eld_void'] = void
    flesh = Image.new('RGBA', (16, 16)); px = flesh.load()
    for y in range(16):
        for x in range(16):
            v = rnd.randint(-8, 8)
            px[x, y] = (96 + v, 22 + v // 3, 66 + v // 2, 255)
    for _ in range(4):                                             # veins
        x, y = rnd.randrange(16), rnd.randrange(16)
        for _s in range(10):
            px[x % 16, y % 16] = (48, 8, 36, 255); x += rnd.choice((-1, 0, 1)); y += rnd.choice((0, 1))
    for _ in range(6):
        px[rnd.randrange(16), rnd.randrange(16)] = (150, 46, 98, 255)
    T_['eld_flesh'] = flesh
    bone = Image.new('RGBA', (16, 16)); px = bone.load()
    for y in range(16):
        for x in range(16):
            v = rnd.randint(-6, 6) - y
            px[x, y] = (208 + v, 202 + v, 176 + v, 255)
    for _ in range(3):
        x, y = rnd.randrange(16), rnd.randrange(16)
        for _s in range(5):
            px[x % 16, y % 16] = (118, 106, 92, 255); x += rnd.choice((-1, 1)); y += 1
    T_['eld_bone'] = bone
    eye = Image.new('RGBA', (16, 16 * EYE_FRAMES))
    for f in range(EYE_FRAMES):
        fr = flesh.copy(); d = ImageDraw.Draw(fr)
        if f == 0:
            d.ellipse((1, 3, 14, 12), fill=(232, 222, 186, 255), outline=(60, 10, 40, 255))
            d.ellipse((4, 3, 11, 12), fill=(186, 34, 214, 255))
            d.ellipse((5.5, 4.5, 9.5, 10.5), fill=(255, 104, 255, 255))
            d.rectangle((7, 4, 8, 11), fill=(10, 0, 12, 255))
            d.point((10, 5), fill=(255, 255, 255, 255))
        else:
            d.line((1, 8, 14, 8), fill=(40, 6, 28, 255), width=2)
        eye.paste(fr, (0, 16 * f))
    T_['eld_eye'] = eye
    return T_


def _box(fr, to, tex, full=False, cube=None):
    if full:
        f = {'uv': [0, 0, 16, 16], 'texture': '#' + tex}
        return {'from': list(fr), 'to': list(to), 'faces': {s: dict(f) for s in ('north', 'south', 'east', 'west', 'up', 'down')}}
    return cube(fr, to, tex)


def tool_models(cube):
    """each weapon and tool built upright (the grip at the bottom), then laid on the sprite's diagonal - so it takes vanilla's
    handheld grip, and in the inventory it reads like a sprite with depth"""
    b = lambda fr, to, t, full=False: _box(fr, to, t, full, cube)
    M = {}
    M['eld_maw'] = [b((6.8, -4.5, 7.0), (9.2, -2.1, 9.0), 'eld_eye', True),                      # the eye in the pommel
                    b((7.4, -2.1, 7.4), (8.6, 3.5, 8.6), 'eld_flesh'),                             # the grip
                    b((7.1, -1.0, 7.1), (8.9, -0.4, 8.9), 'eld_bone'), b((7.1, 1.4, 7.1), (8.9, 2.0, 8.9), 'eld_bone'),
                    b((4.0, 3.5, 7.0), (12.0, 5.0, 9.0), 'eld_bone'),                              # the jaw for a guard
                    b((3.0, 4.5, 7.3), (4.2, 7.0, 8.7), 'eld_bone'), b((11.8, 4.5, 7.3), (13.0, 7.0, 8.7), 'eld_bone'),
                    b((2.6, 6.8, 7.5), (3.6, 8.2, 8.5), 'eld_bone'), b((12.4, 6.8, 7.5), (13.4, 8.2, 8.5), 'eld_bone'),
                    b((6.4, 5.0, 7.5), (9.6, 8.0, 8.5), 'eld_flesh'),
                    b((6.2, 8.0, 7.6), (9.8, 19.0, 8.4), 'eld_void'),                              # the blade
                    b((7.7, 8.0, 7.5), (8.3, 18.0, 8.5), 'eld_flesh'),                             # its vein
                    b((7.0, 9.0, 7.45), (9.0, 11.0, 8.55), 'eld_eye', True),                       # the eye in the blade
                    b((7.2, 19.0, 7.7), (8.8, 21.0, 8.3), 'eld_void'), b((7.6, 21.0, 7.8), (8.4, 22.2, 8.2), 'eld_bone')] + \
                   [b((5.4, y, 7.7), (6.2, y + 1.2, 8.3), 'eld_bone') for y in (9.0, 11.5, 14.0, 16.5)] + \
                   [b((9.8, y, 7.7), (10.6, y + 1.2, 8.3), 'eld_bone') for y in (10.2, 12.7, 15.2, 17.7)] + \
                   [b((3.0, 1.6, 7.6), (3.8, 4.5, 8.4), 'eld_flesh'), b((2.3, -0.6, 7.65), (3.1, 1.8, 8.35), 'eld_flesh'),       # tendrils off the jaw
                    b((1.8, -2.2, 7.7), (2.5, -0.4, 8.3), 'eld_flesh'), b((12.2, 1.6, 7.6), (13.0, 4.5, 8.4), 'eld_flesh'),
                    b((12.9, -0.4, 7.65), (13.7, 1.8, 8.35), 'eld_flesh'), b((13.5, -1.8, 7.7), (14.2, -0.2, 8.3), 'eld_flesh'),
                    b((7.4, 15.5, 7.45), (8.6, 16.7, 8.55), 'eld_eye', True)]                       # a second, smaller eye up the blade
    M['eld_pick'] = [b((7.4, -6.0, 7.4), (8.6, 13.0, 8.6), 'eld_flesh')] + \
                    [b((7.1, y, 7.1), (8.9, y + 0.6, 8.9), 'eld_bone') for y in (-4.0, 2.0, 8.0)] + \
                    [b((2.0, 12.0, 7.2), (14.0, 14.5, 8.8), 'eld_void'),                           # the head
                     b((0.8, 9.5, 7.4), (3.0, 12.5, 8.6), 'eld_bone'), b((13.0, 9.5, 7.4), (15.2, 12.5, 8.6), 'eld_bone'),
                     b((0.2, 7.2, 7.6), (1.8, 9.6, 8.4), 'eld_bone'), b((14.2, 7.2, 7.6), (15.8, 9.6, 8.4), 'eld_bone'),   # the mandibles
                     b((6.6, 12.0, 7.0), (9.4, 14.8, 9.0), 'eld_eye', True),
                     b((7.5, 14.5, 7.7), (8.5, 16.0, 8.3), 'eld_bone')]
    M['eld_axe'] = [b((7.4, -6.0, 7.4), (8.6, 14.0, 8.6), 'eld_flesh')] + \
                   [b((7.1, y, 7.1), (8.9, y + 0.6, 8.9), 'eld_bone') for y in (-4.0, 3.0)] + \
                   [b((4.0, 7.0, 7.3), (7.4, 15.0, 8.7), 'eld_void'),                              # the blade (to the upper left, as vanilla's)
                    b((2.5, 6.0, 7.4), (4.0, 16.0, 8.6), 'eld_bone')] + \
                   [b((1.7, y, 7.6), (2.5, y + 1.0, 8.4), 'eld_bone') for y in (7.0, 9.5, 12.0, 14.5)] + \
                   [b((8.6, 11.0, 7.5), (11.5, 12.4, 8.5), 'eld_bone'), b((11.5, 11.3, 7.6), (12.5, 12.1, 8.4), 'eld_bone'),
                    b((4.6, 10.0, 7.15), (6.8, 12.2, 8.85), 'eld_eye', True)]
    M['eld_shovel'] = [b((7.4, -6.0, 7.4), (8.6, 12.0, 8.6), 'eld_flesh'), b((7.1, -3.0, 7.1), (8.9, -2.4, 8.9), 'eld_bone'),
                       b((7.0, 11.0, 7.2), (9.0, 12.5, 8.8), 'eld_bone'),
                       b((5.6, 12.5, 7.4), (10.4, 19.0, 8.6), 'eld_void'),
                       b((5.2, 13.0, 7.5), (5.6, 18.5, 8.5), 'eld_bone'), b((10.4, 13.0, 7.5), (10.8, 18.5, 8.5), 'eld_bone'),
                       b((6.6, 19.0, 7.5), (9.4, 20.5, 8.5), 'eld_bone'), b((7.4, 20.5, 7.7), (8.6, 21.4, 8.3), 'eld_bone'),
                       b((6.9, 14.0, 7.25), (9.1, 16.2, 8.75), 'eld_eye', True)]
    for els in M.values():
        for e in els:
            e['rotation'] = {'angle': -45, 'axis': 'z', 'origin': [8, 8, 8]}
            if any(f['texture'] == '#eld_eye' for f in e['faces'].values()): e['light_emission'] = 12      # (the eyes glow in the dark)
    M['eld_maw'][11]['light_emission'] = 6                                                             # (and the Maw's vein)
    return M


def _recolor(im, lo, hi, stretch=1.0):
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a: continue
            t = min(1.0, ((r + g + b) / 765) * stretch) ** 0.85
            px[x, y] = tuple(int(lo[c] + (hi[c] - lo[c]) * t) for c in range(3)) + (a,)
    return im


GOLD_LO, GOLD_HI = (70, 40, 6), (255, 236, 140)


def rp(R):
    import sys
    from PIL import Image, ImageDraw
    import random
    R.TEXTURE_MODS.append(sys.modules[__name__])
    EL, EH = (14, 4, 24), (156, 84, 206)
    # the armour's icons: netherite, sunk into the void, an eye opening on each
    for p in PIECES:
        im = _recolor(Image.open(f'{VAN}/item/netherite_{p}.png').convert('RGBA'), EL, EH, 1.9)
        px = im.load()
        for (x, y) in ((7, 4), (8, 4)) if p == 'helmet' else ((7, 6), (8, 6)) if p == 'chestplate' else ((7, 5),) if p == 'leggings' else ((4, 10), (11, 10)):
            if px[x, y][3]: px[x, y] = (255, 104, 255, 255)
        R.ICONS[f'eld_{p}'] = im
    # the Omni Token: the Dread Token's red, the Ember's orange and the Void's violet, in three swirling wedges
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for n, col in enumerate(('#b0102a', '#ff7a1a', '#b05cff')):
        d.pieslice((2, 2, 13, 13), n * 120 - 90, n * 120 + 30, fill=col)
    d.ellipse((2, 2, 13, 13), outline='#2a0a30'); d.ellipse((6, 6, 9, 9), fill='#fff0ff', outline='#e8a8ff')
    R.ICONS['omni_token'] = im

    def post(R2):
        import json
        import copy
        R2.wj('assets/bm/textures/block/eld_eye.png.mcmeta', {'animation': {'frametime': 3, 'frames': [0] * 40 + [1, 1] + [0] * 25 + [1]}})
        # the weapon and the tools: their own 3D models, held as vanilla holds a sword
        for name, els in tool_models(R.cube).items():
            used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
            R2.wj(f'assets/bm/models/item/{name}.json', {'parent': 'minecraft:item/handheld',
                                                          'textures': dict({t: f'bm:block/{t}' for t in used}, particle='bm:block/eld_void'),
                                                          'elements': els})
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
        # the armour on the body: netherite sunk into the void, veins of light, an eye on the brow and one on the breast
        rnd = random.Random(84)
        for layer in ('humanoid', 'humanoid_leggings'):
            im = _recolor(Image.open(f'{VAN}/entity/equipment/{layer}/netherite.png').convert('RGBA'), EL, EH, 1.9)
            px = im.load()
            for _ in range(26):
                x, y = rnd.randrange(im.width), rnd.randrange(im.height)
                for _s in range(6):
                    if 0 <= x < im.width and 0 <= y < im.height and px[x, y][3]: px[x, y] = (200, 70, 255, 255)
                    x += rnd.choice((-1, 0, 1)); y += rnd.choice((0, 1))
            eyes = [(10, 10), (24, 24)] if layer == 'humanoid' else []
            for (cx, cy) in eyes:
                for dx in (-2, -1, 0, 1, 2):
                    if px[cx + dx, cy][3]: px[cx + dx, cy] = (232, 222, 186, 255)
                for dx in (-1, 0, 1):
                    if px[cx + dx, cy][3]: px[cx + dx, cy] = (220, 60, 240, 255)
                px[cx, cy] = (10, 0, 12, 255)
            im.save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', layer, 'eldritch.png'))
        R2.wj('assets/bm/equipment/eldritch.json', {'layers': {'humanoid': [{'texture': 'bm:eldritch'}], 'humanoid_leggings': [{'texture': 'bm:eldritch'}]}})
        # the golden dolls: each doll's own model, every texture on it turned to gold
        done = {}
        def gold_tex(ref):
            if ref in done: return done[ref]
            ns, path = ref.split(':', 1) if ':' in ref else ('minecraft', ref)
            src = R2.p('assets', 'bm', 'textures', *path.split('/')) + '.png' if ns == 'bm' else f'{VAN}/{path}.png'
            im = _recolor(Image.open(src).convert('RGBA'), GOLD_LO, GOLD_HI, 1.25)
            if im.width != im.height:                              # (UVs are fractions of the sheet: stretched square, the same faces)
                n = max(im.size); im = im.resize((n, n), Image.NEAREST)
            nm = 'gd_' + path.replace('/', '_')
            folder = 'block' if path.startswith(('block/', 'item/')) else 'entity'        # (an entity skin: its own sprite in the block atlas)
            im.save(R2.p('assets', 'bm', 'textures', folder, nm + '.png'))
            done[ref] = f'bm:{folder}/{nm}'
            if folder == 'entity': atlas.append(done[ref])
            return done[ref]
        atlas = []
        for k in GDOLLS:
            mid = ITEMS[DOLL_OF[k]]['comps']['minecraft:item_model'].split(':', 1)[1]
            m = json.load(open(R2.p('assets', 'bm', 'models', 'item', mid + '.json')))
            g = copy.deepcopy(m)
            g['textures'] = {t: (gold_tex(v) if not v.startswith('#') else v) for t, v in m['textures'].items()}
            R2.wj(f'assets/bm/models/item/gdoll_{k}.json', g)
            R2.wj(f'assets/bm/items/gdoll_{k}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/gdoll_{k}'}})
        if atlas:
            ap = R2.p('assets', 'minecraft', 'atlases', 'blocks.json')
            cur = json.load(open(ap)) if __import__('os').path.exists(ap) else {'sources': []}
            have = {x.get('resource') for x in cur['sources']}
            cur['sources'] += [{'type': 'minecraft:single', 'resource': r} for r in atlas if r not in have]
            R2.wj('assets/minecraft/atlases/blocks.json', cur)
    R.POST.append(post)

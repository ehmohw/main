"""Phase 2.24: Cecil the Wizard, the chef's new menu, goofy goods and music.

- CECIL THE WIZARD (the purple fortune-teller's tent on the plaza): a hooded, grinning sorcerer with a crescent staff.
  He breathes, sways, turns to watch you, and now and then casts a little spell. He sells:
    Staff of Sparks (chain lightning), Gravewell Staff (a vortex that drags monsters in, then bursts),
    Cecil's Crescent Staff (a heavy melee staff that fires homing crystal shards),
    the Prism Bow (arrows burst into a rainbow nova), the Starcaller Bow (fully drawn shots call down falling stars),
    and two gems: the Bloomheart (a healing bloom for you and your friends; poison and wither won't stick while it's in
    your off hand) and the Tidal Tear (a wave that shoves monsters back, slows them and puts out fires).
- PRIME MEAT is a superb food on its own now, and Chef Fromage cooks six new dishes from it (Fire-Eater's Chili,
  Deep-Sea Chowder, Moonlit Kebab, Lucky Rabbit Pot Pie, Hunter's Roast, Featherlight Drumsticks) plus the Grand
  Banquet: a feast you set down that everyone can eat from.
- GOOFY GOODS (Old Barnaby, and loot chests): the Groovy Lava Lamp, the Portable Trash Can, the Whoopee Cushion, the
  Display Skiff (dye it), the Boombox and the Pocket Ocarina."""
import math
from items import item, gear, T, TOTEM, ITEMS, attr, ench, weapon_attrs, consumable
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D

PURPLE = '#9a5ae0'
CECIL_POS, CECIL_YAW = (27.5, 10, 53.5), -90           # the fortune teller's tent (template), facing the plaza
LAVA = ['purple', 'red', 'orange', 'lime', 'cyan', 'pink']
TRACKS = [('13', 178), ('cat', 185), ('blocks', 345), ('chirp', 185), ('far', 174), ('mall', 197), ('mellohi', 96), ('stal', 150),
          ('strad', 188), ('ward', 251), ('wait', 238), ('pigstep', 149), ('otherside', 195), ('relic', 218), ('creator', 176),
          ('precipice', 299), ('tears', 175), ('lava_chicken', 134), ('bounce', 234)]
INSTRUMENTS = [('flute', 'Flute'), ('bell', 'Bell'), ('chime', 'Chimes'), ('xylophone', 'Xylophone'), ('harp', 'Harp'), ('banjo', 'Banjo'),
               ('bit', 'Bit'), ('didgeridoo', 'Didgeridoo'), ('cow_bell', 'Cowbell')]
DYES = {'lime': 0, 'green': 0, 'red': 1, 'yellow': 2, 'orange': 2, 'black': 3, 'purple': 3, 'cyan': 4, 'light_blue': 4, 'blue': 4, 'pink': 5, 'magenta': 5}
SKIFF_COLS = ['green', 'crimson', 'gold', 'midnight', 'ocean', 'rose']
SKIFF_DECALS = ['none', 'stripes', 'crest', 'flames']

# ===================================================================== items: Cecil's magic
staff = lambda dmg, spd: [attr('attack_damage', dmg, 'mainhand', ident='minecraft:base_attack_damage'),
                          attr('attack_speed', spd, 'mainhand', ident='minecraft:base_attack_speed')]
item('staff_of_sparks', TOTEM, 'Staff of Sparks', '#7ad8ff',
     ['A copper rod that hums in the rain.', ('Right-click: a bolt leaps to the creature', 'blue'), ('you aim at (16 blocks), then jumps to', 'blue'),
      ('up to 3 more nearby. 6 damage each.', 'blue'), ('1.5 second recharge.', 'gray')],
     model='bm:staff_of_sparks', stack=1, cat='magic', comps=dict(hold('none'), **{'minecraft:attribute_modifiers': staff(3, -2.4)}), tier=1)
item('gravewell_staff', TOTEM, 'Gravewell Staff', '#b48cff',
     ['A staff with a tiny black hole for a head.', ('Right-click: open a gravewell where you look', 'blue'), ('(20 blocks). For 3 seconds it drags monsters', 'blue'),
      ('in, then bursts: 8 damage and up they go.', 'blue'), ('12 second recharge.', 'gray')],
     model='bm:gravewell_staff', stack=1, cat='magic', comps=dict(hold('none'), **{'minecraft:attribute_modifiers': staff(4, -2.6)}), tier=2)
item('crescent_staff', TOTEM, "Cecil's Crescent Staff", '#ff7ac8',
     ["The wizard's own (well, its twin).", ('Hits like an axe: 11 damage.', 'blue'), ('Right-click: three homing crystal shards', 'blue'),
      ('seek the nearest monsters. 7 damage each.', 'blue'), ('4 second recharge.', 'gray')],
     model='bm:crescent_staff', stack=1, cat='magic', comps=dict(hold('none'), **{'minecraft:attribute_modifiers': staff(10, -3.0)}), tier=3, bold=True)
gear('prism_bow', 'bow', 'Prism Bow', '#ff9af0', ['Strung with a sunbeam split seven ways.', ('Arrows burst into a rainbow nova where', 'blue'),
                                                  ('they land: 5 damage to monsters nearby.', 'blue')],
     dict(ench(power=4, unbreaking=3), **{'bm:prism_shot': 1}), 2)
gear('starcaller_bow', 'bow', 'Starcaller Bow', '#ffe85a', ['The night sky owes Cecil a favour.', ('A fully drawn arrow calls five falling', 'blue'),
                                                            ('stars down where it lands (6 damage each).', 'blue'), ('One volley every 3 seconds.', 'gray')],
     dict(ench(power=5, unbreaking=3), **{'bm:starcall': 1}), 3, bold=True)
item('bloomheart_gem', TOTEM, 'Bloomheart', '#ff7ae0',
     ['A gem that grew in a flower instead of a mine.', ('Right-click: a ring of blossom - you and', 'blue'), ('everyone within 8 blocks get Regeneration II', 'blue'),
      ('for 8 seconds. 45 second recharge.', 'blue'), ('In your off hand: poison and wither', 'blue'), ("won't stick to you.", 'blue')],
     model='bm:bloomheart_gem', stack=1, cat='magic', glint=True, comps=hold('none'), tier=2)
item('tidal_tear', TOTEM, 'Tidal Tear', '#7ad0ea',
     ['A drop of the deep sea, holding a garnet.', ('Right-click: a wave rolls 10 blocks ahead,', 'blue'), ('shoving monsters back (4 damage, Slowness)', 'blue'),
      ('and putting out fires - and you.', 'blue'), ('20 second recharge.', 'gray')],
     model='bm:tidal_tear', stack=1, cat='magic', glint=True, comps=hold('none'), tier=2)
for _i in ('staff_of_sparks', 'gravewell_staff', 'crescent_staff', 'bloomheart_gem', 'tidal_tear'):
    HOLD[_i] = f'bm:p45/{_i}/use'

# ===================================================================== items: the chef's new menu
for _m in ('prime_pork', 'prime_beef', 'prime_mutton', 'prime_chicken', 'prime_rabbit'):
    c = ITEMS[_m]['comps']
    c['minecraft:food'] = {'nutrition': 10, 'saturation': 16.0}
    c['minecraft:consumable'] = consumable(1.6, effects=[{'type': 'minecraft:apply_effects', 'effects': [{'id': 'minecraft:regeneration', 'amplifier': 0, 'duration': 120}]}])
    c['minecraft:lore'][0:3] = [T('Rare meat from a Prime animal.', 'gray'), T('Eat it as it is: as filling as two steaks,', 'blue'),
                               T('and a moment of Regeneration.', 'blue'), T('Chef Fromage cooks feasts and dishes with it.', 'gray')]
DISHES = [  # id, name, colour, (meat, n), (currency, n), effects [(id, amp, secs)], nutrition, lore
    ('dish_chili', "Fire-Eater's Chili", '#ff5a2a', ('prime_pork', 2), ('token', 4), [('fire_resistance', 0, 480)], 8, 'Fire Resistance (8:00)'),
    ('dish_chowder', 'Deep-Sea Chowder', '#3ad8d0', ('prime_chicken', 2), ('token', 4), [('water_breathing', 0, 480), ('dolphins_grace', 0, 180)], 8,
     'Water Breathing (8:00), Dolphin\'s Grace (3:00)'),
    ('dish_kebab', 'Moonlit Kebab', '#9ab0ff', ('prime_mutton', 2), ('token', 3), [('night_vision', 0, 600)], 8, 'Night Vision (10:00)'),
    ('dish_potpie', 'Lucky Rabbit Pot Pie', '#7dff6a', ('prime_rabbit', 3), ('medallion', 2), [('luck', 1, 1200), ('jump_boost', 0, 300)], 10,
     'Luck II (20:00), Jump Boost (5:00)'),
    ('dish_roast', "Hunter's Roast", '#c8783a', ('prime_beef', 3), ('medallion', 2), [('absorption', 2, 240), ('saturation', 0, 2)], 20,
     'Absorption III (4:00), a full belly'),
    ('dish_drumsticks', 'Featherlight Drumsticks', '#fff2c8', ('prime_chicken', 2), ('medallion', 1), [('slow_falling', 0, 300)], 8, 'Slow Falling (5:00)'),
]
for did, nm, col, _meat, _cur, effs, nut, txt in DISHES:
    item(did, TOTEM, nm, col, ['From Chef Fromage\'s kitchen.', (txt, 'blue')], model=f'bm:{did}', stack=16, cat='food',
         comps={'minecraft:food': {'nutrition': nut, 'saturation': float(nut), 'can_always_eat': True},
                'minecraft:consumable': consumable(1.8, effects=[{'type': 'minecraft:apply_effects', 'effects': [
                    {'id': f'minecraft:{e}', 'amplifier': a, 'duration': s * 20} for e, a, s in effs]}])})
item('grand_banquet', TOTEM, 'Grand Banquet', '#ffd23f',
     ['Every Prime cut, roasted, on one platter.', ('Right-click a block: set the feast down.', 'blue'), ('Anyone can right-click it for a helping:', 'blue'),
      ('food, Regeneration and Saturation.', 'blue'), ('8 helpings. One per person every 30 seconds.', 'gray')],
     model='bm:banquet3d', stack=4, cat='food', comps=hold('none'))
HOLD['grand_banquet'] = 'bm:p45/banquet/place'

# ===================================================================== items: goofy goods and music
GOOFY = {
    'lava_lamp': ('Groovy Lava Lamp', '#ff7ac8', ['Far out.', ('Right-click a block: set it down. It glows.', 'blue'),
                                                  ('Right-click the lamp: change its colour.', 'blue'), ('Sneak + punch: pick it up.', 'gray')], 'bm:lava3d_purple'),
    'trash_can': ('Portable Trash Can', '#8ab88a', ['For the things you never want to see again.', ('Right-click: a trash can pops up in front', 'blue'),
                                                    ('of you. Whatever goes in is destroyed.', 'blue'), ('It folds away when you walk off.', 'gray')], 'bm:trash3d'),
    'whoopee_cushion': ('Whoopee Cushion', '#ff7ab0', ['A classic.', ('Right-click a block: hide it there.', 'blue'),
                                                       ('Whoever steps on it... finds out.', 'blue'), ('Sneak + punch: pick it up.', 'gray')], 'bm:whoopee3d'),
    'display_skiff': ('Display Skiff', '#7dff6a', ['A Vorn Skiff for your mantelpiece. (It does not fly.)', ('Right-click a block: set it down.', 'blue'),
                                                   ('Right-click it with a dye: repaint it.', 'blue'), ('Sneak + right-click it: change the decal.', 'blue'),
                                                   ('Sneak + punch: pick it up.', 'gray')], 'bm:skiff_green_none'),
    'boombox': ('Boombox', '#ff4a4a', ['Batteries included. Mostly.', ('Right-click a block: set it down.', 'blue'),
                                       ('Right-click it: next track (every music disc).', 'blue'), ('Sneak + right-click it: stop.', 'blue'),
                                       ('Sneak + punch: pick it up.', 'gray')], 'bm:boombox3d'),
    'ocarina': ('Pocket Ocarina', '#6ab0ff', ['Play it like you mean it.', ('Right-click: play a note - look up for high', 'blue'),
                                             ('notes, down for low (two octaves).', 'blue'), ('Sneak + right-click: change instrument.', 'blue')], 'bm:ocarina'),
}
for _g, (_n, _c, _l, _m) in GOOFY.items():
    item(_g, TOTEM, _n, _c, _l, model=_m, stack=1 if _g in ('ocarina', 'trash_can') else 16, cat='fun', comps=hold('none'))
    HOLD[_g] = f'bm:p45/{_g}/use'
NEW_NPCS = {'wizard': ('custom', 'Cecil the Wizard', 'light_purple', 'cleric', 'swamp', None)}
CHEST_FINDS = {'lava_lamp': {'woodland_mansion': 10, 'village/village_plains_house': 3, 'village/village_savanna_house': 3, 'simple_dungeon': 4},
               'trash_can': {'abandoned_mineshaft': 3, 'village/village_plains_house': 2, 'pillager_outpost': 4},
               'whoopee_cushion': {'simple_dungeon': 5, 'village/village_taiga_house': 3, 'shipwreck_supply': 4},
               'boombox': {'woodland_mansion': 8, 'ancient_city': 5, 'trial_chambers/reward_common': 2},
               'ocarina': {'jungle_temple': 8, 'desert_pyramid': 5, 'igloo_chest': 10, 'village/village_snowy_house': 3},
               'display_skiff': {'shipwreck_treasure': 5, 'buried_treasure': 4}}


def extend_offers(O, offer):
    O['wizard'] = [offer(('token', 16), ('staff_of_sparks', 1)), offer(('medallion', 5), ('gravewell_staff', 1)),
                   offer(('trophy', 4), ('crescent_staff', 1)), offer(('medallion', 4), ('prism_bow', 1)), offer(('trophy', 3), ('starcaller_bow', 1)),
                   offer(('medallion', 6), ('bloomheart_gem', 1)), offer(('medallion', 6), ('tidal_tear', 1))]
    O['chef'] += [offer(meat, (did, 1), cur) for did, _n, _c, meat, cur, _e, _nut, _t in DISHES]
    O['chef'].append(offer(('medallion', 4), ('grand_banquet', 1), ('prime_beef', 2)))
    O['pawn'] += [offer(('token', 4), ('lava_lamp', 1)), offer(('token', 3), ('trash_can', 1)), offer(('token', 2), ('whoopee_cushion', 1)),
                  offer(('medallion', 1), ('boombox', 1)), offer(('token', 5), ('ocarina', 1))]
    O['dock'].append(offer(('token', 6), ('display_skiff', 1)))


def q(axis, deg):
    s, c = math.sin(math.radians(deg) / 2), math.cos(math.radians(deg) / 2)
    return [F(round(s, 4)) if axis == 'x' else F(0), F(round(s, 4)) if axis == 'y' else F(0), F(round(s, 4)) if axis == 'z' else F(0), F(round(c, 4))]


# ===================================================================== generation
def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    import mgeo
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    ident = [F(0), F(0), F(0), F(1)]
    fast, second, tick = [], [], []
    objs = ['bm.mcd dummy', 'bm.mcd2 dummy', 'bm.mcd3 dummy', 'bm.mcd4 dummy', 'bm.mcd5 dummy', 'bm.mcd6 dummy', 'bm.cct dummy', 'bm.lav dummy', 'bm.trk dummy', 'bm.ocn dummy', 'bm.bqn dummy', 'bm.bqc dummy',
            'bm.skp dummy', 'bm.skd2 dummy', 'bm.gwt dummy', 'bm.wav dummy', 'bm.trt dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    mob = 'type=!#bm:p44_nonmob,type=!minecraft:player,tag=!bm.npc'
    now = 'execute store result score #now bm.rng run time query gametime'
    def cooldown(obj, ticks, label):
        return [now, f'execute if score @s {obj} > #now bm.rng run return run ' + title('@s', 'actionbar', T(label + ' is still recharging...', 'gray')),
                f'scoreboard players operation @s {obj} = #now bm.rng', f'scoreboard players add @s {obj} {ticks}']
    def disp(model, tags, scale=1.0, ty=0.0, bright=None, dur=3, extra=None):
        d = {'Tags': tags, 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}}, 'item_display': 'fixed',
             'teleport_duration': Int(dur), 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(ty), F(0)], 'scale': [F(scale)] * 3}}
        if bright: d['brightness'] = {'block': Int(bright), 'sky': Int(bright)}
        if extra: d.update(extra)
        return snbt(d)

    # ------------------------------------------------------------------ Staff of Sparks: chain lightning
    fn('p45/staff_of_sparks/use', ['execute unless items entity @s weapon.mainhand ' + holds % 'staff_of_sparks' + ' run return 0'] + cooldown('bm.mcd', 30, 'The staff') +
       ['tag @s add bm.mcast', 'scoreboard players set #ray bm.rng 80', 'scoreboard players set #hit bm.rng 0',
        'execute anchored eyes positioned ^ ^ ^ run function bm:p45/spark/ray', 'tag @s remove bm.mcast',
        'tag @e[tag=bm.zapped] remove bm.zapped',
        'execute if score #hit bm.rng matches 0 run playsound minecraft:block.copper_bulb.turn_off player @a[distance=..16] ~ ~ ~ 1 1.6',
        'execute if score #hit bm.rng matches 1 run playsound minecraft:entity.lightning_bolt.impact player @a[distance=..24] ~ ~ ~ 0.6 1.8'])
    fn('p45/spark/ray', ['particle minecraft:electric_spark ~ ~ ~ 0 0 0 0 1',
                         f'execute positioned ~-0.15 ~-0.15 ~-0.15 as @e[{mob},dx=0.3,dy=0.3,dz=0.3,limit=1] at @s run return run function bm:p45/spark/first',
                         'execute unless block ~ ~ ~ #bm:grap_pass run return 0', 'scoreboard players remove #ray bm.rng 1',
                         'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p45/spark/ray'])
    fn('p45/spark/first', ['scoreboard players set #hit bm.rng 1', 'scoreboard players set #jumps bm.rng 3', 'function bm:p45/spark/zap'])
    fn('p45/spark/zap', ['tag @s add bm.zapped', 'damage @s 6 minecraft:lightning_bolt by @a[tag=bm.mcast,limit=1]',
                         'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.2 20', 'particle minecraft:end_rod ~ ~1 ~ 0.1 0.3 0.1 0.02 3',
                         'scoreboard players remove #jumps bm.rng 1', 'execute if score #jumps bm.rng matches ..-1 run return 0',
                         f'execute as @e[{mob},tag=!bm.zapped,distance=..5,sort=nearest,limit=1] at @s run function bm:p45/spark/arc'])
    fn('p45/spark/arc', ['execute facing entity @e[tag=bm.zapped,sort=nearest,limit=1] feet run function bm:p45/spark/line', 'function bm:p45/spark/zap'])
    fn('p45/spark/line', [f'particle minecraft:electric_spark ^ ^1 ^{d} 0.02 0.02 0.02 0 2' for d in (0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5)])

    # ------------------------------------------------------------------ Gravewell Staff: a vortex, then a burst
    fn('p45/gravewell_staff/use', ['execute unless items entity @s weapon.mainhand ' + holds % 'gravewell_staff' + ' run return 0',
                                   'execute unless function bm:p37/allowed run return run ' + say('The gravewell will not open here.')] + cooldown('bm.mcd2', 240, 'The gravewell') +
       ['scoreboard players set #ray bm.rng 100', 'execute anchored eyes positioned ^ ^ ^ run function bm:p45/well/ray',
        'playsound minecraft:block.respawn_anchor.charge player @a[distance=..24] ~ ~ ~ 1 0.6'])
    fn('p45/well/ray', ['execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p45/well/open',
                        f'execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[{mob},dx=0,dy=0,dz=0] positioned ~0.5 ~0.5 ~0.5 run return run function bm:p45/well/open',
                        'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches ..0 run return run function bm:p45/well/open',
                        'execute positioned ^ ^ ^0.2 run function bm:p45/well/ray'])
    fn('p45/well/open', ['execute positioned ^ ^ ^-0.5 run summon minecraft:marker ~ ~ ~ {Tags:["bm.gwell","bm.gwnew"]}',
                         'scoreboard players set @e[type=minecraft:marker,tag=bm.gwnew] bm.gwt 60', 'tag @e[type=minecraft:marker,tag=bm.gwnew] remove bm.gwnew'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.gwell] at @s run function bm:p45/well/tick')
    fn('p45/well/tick', ['scoreboard players remove @s bm.gwt 1',
                         'particle minecraft:reverse_portal ~ ~ ~ 1.2 1.2 1.2 0.6 12', 'particle minecraft:portal ~ ~ ~ 0.2 0.2 0.2 1.2 6',
                         'particle minecraft:dust{color:[0.15,0.0,0.25],scale:2.5} ~ ~ ~ 0.15 0.15 0.15 0 3',
                         f'execute as @e[{mob},distance=1.2..8] at @s facing entity @e[type=minecraft:marker,tag=bm.gwell,sort=nearest,limit=1] feet run tp @s ^ ^ ^0.35',
                         'execute if score @s bm.gwt matches ..0 run function bm:p45/well/burst'])
    fn('p45/well/burst', [f'execute as @e[{mob},distance=..4] run damage @s 8 minecraft:magic',
                          f'execute as @e[{mob},distance=..4] run effect give @s minecraft:levitation 1 6 true',
                          'particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1', 'particle minecraft:witch ~ ~ ~ 1.5 1.5 1.5 0.2 60',
                          'playsound minecraft:entity.warden.sonic_boom player @a[distance=..32] ~ ~ ~ 0.6 1.6', 'kill @s'])

    # ------------------------------------------------------------------ Cecil's Crescent Staff: homing crystal shards
    fn('p45/crescent_staff/use', ['execute unless items entity @s weapon.mainhand ' + holds % 'crescent_staff' + ' run return 0'] + cooldown('bm.mcd3', 80, 'The crescent staff') +
       ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid'] +
       [f'execute anchored eyes positioned ^ ^ ^1 rotated ~{a} ~-8 run function bm:p45/shard/new' for a in (-20, 0, 20)] + [
        'playsound minecraft:block.amethyst_cluster.break player @a[distance=..24] ~ ~ ~ 1 1.4', 'playsound minecraft:entity.evoker.cast_spell player @a[distance=..24] ~ ~ ~ 0.6 1.6'])
    fn('p45/shard/new', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.shard","bm.shnew"]}', 'tp @e[type=minecraft:marker,tag=bm.shnew,limit=1] ~ ~ ~ ~ ~',
                         'scoreboard players operation @e[type=minecraft:marker,tag=bm.shnew] bm.pid = @s bm.pid', 'scoreboard players set @e[type=minecraft:marker,tag=bm.shnew] bm.gwt 40',
                         'tag @e[type=minecraft:marker,tag=bm.shnew] remove bm.shnew'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.shard] at @s run function bm:p45/shard/tick')
    fn('p45/shard/tick', ['scoreboard players remove @s bm.gwt 1', 'execute if score @s bm.gwt matches ..0 run return run kill @s',
                          f'execute if score @s bm.gwt matches ..34 if entity @e[{mob},distance=..12] run tp @s ~ ~ ~ facing entity @e[{mob},distance=..12,sort=nearest,limit=1] eyes',
                          'execute rotated as @s run tp @s ^ ^ ^0.75',
                          'particle minecraft:dust{color:[1.0,0.45,0.8],scale:1.2} ~ ~ ~ 0.05 0.05 0.05 0 3', 'particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1',
                          'execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p45/shard/pop',
                          f'execute positioned ~-0.6 ~-0.6 ~-0.6 if entity @e[{mob},dx=0.2,dy=0.2,dz=0.2] positioned ~0.6 ~0.6 ~0.6 run function bm:p45/shard/hit'])     # hitbox overlap (distance= reads the feet)
    fn('p45/shard/hit', ['scoreboard players operation #sp bm.pid = @s bm.pid', 'tag @a remove bm.mcast', 'execute as @a if score @s bm.pid = #sp bm.pid run tag @s add bm.mcast',
                         f'execute positioned ~-0.6 ~-0.6 ~-0.6 as @e[{mob},dx=0.2,dy=0.2,dz=0.2,limit=1] run damage @s 7 minecraft:magic by @a[tag=bm.mcast,limit=1]',
                         'tag @a remove bm.mcast', 'function bm:p45/shard/pop'])
    fn('p45/shard/pop', ['particle minecraft:dust{color:[1.0,0.45,0.8],scale:1.6} ~ ~ ~ 0.3 0.3 0.3 0 15', 'playsound minecraft:block.amethyst_block.break player @a[distance=..16] ~ ~ ~ 1 1.6', 'kill @s'])

    # ------------------------------------------------------------------ Prism Bow / Starcaller Bow
    base = {'anvil_cost': 8, 'max_level': 1, 'weight': 1, 'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0}}
    for eid, nm, col, tag in (('prism_shot', 'Prism Shot', '#ff9af0', 'bm.prism'), ('starcall', 'Starcall', '#ffe85a', 'bm.starc')):
        wjson(f'bm/enchantment/{eid}.json', dict(base, description=T(nm, col), slots=['mainhand'], supported_items='#minecraft:enchantable/bow', effects={
            'minecraft:projectile_spawned': [{'effect': {'type': 'minecraft:run_function', 'function': f'bm:p45/{eid}/spawned'}}],
            'minecraft:post_attack': [{'enchanted': 'attacker', 'affected': 'damaging_entity', 'effect': {'type': 'minecraft:run_function', 'function': f'bm:p45/{eid}/struck'}}]}))
        fn(f'p45/{eid}/spawned', [f'tag @s add {tag}'] if eid == 'prism_shot' else [f'execute if entity @s[nbt={{crit:1b}}] run tag @s add {tag}'])
    tick.append('execute as @e[type=#minecraft:arrows,tag=bm.prism] at @s run function bm:p45/prism_shot/fly')
    fn('p45/prism_shot/fly', ['execute if entity @s[nbt={inGround:1b}] run return run function bm:p45/prism_shot/nova',
                              'particle minecraft:dust{color:[1.0,0.3,0.3],scale:1} ~ ~ ~ 0 0 0 0 1', 'particle minecraft:dust{color:[0.3,1.0,0.4],scale:1} ~ ~ ~ 0 0 0 0 1',
                              'particle minecraft:dust{color:[0.4,0.5,1.0],scale:1} ~ ~ ~ 0 0 0 0 1',
                              ])
    fn('p45/prism_shot/struck', ['execute if entity @s[tag=bm.prism] run function bm:p45/prism_shot/nova'])
    fn('p45/starcall/struck', ['execute if entity @s[tag=bm.starc] run function bm:p45/starcall/volley'])
    fn('p45/prism_shot/nova', ['tag @s remove bm.prism', f'execute as @e[{mob},distance=..3.5] run damage @s 5 minecraft:magic'] +
       [f'particle minecraft:dust{{color:[{r},{g},{b}],scale:1.4}} ~ ~0.3 ~ 1.2 0.6 1.2 0 12' for r, g, b in ((1, 0.2, 0.2), (1, 0.6, 0.1), (1, 1, 0.2), (0.2, 1, 0.3), (0.2, 0.6, 1), (0.6, 0.3, 1))] +
       ['playsound minecraft:block.amethyst_block.resonate player @a[distance=..24] ~ ~ ~ 1 1.6'])
    tick.append('execute as @e[type=#minecraft:arrows,tag=bm.starc] at @s run function bm:p45/starcall/fly')
    fn('p45/starcall/fly', ['particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1',
                            'execute if entity @s[nbt={inGround:1b}] run function bm:p45/starcall/volley'])
    fn('p45/starcall/volley', ['tag @s remove bm.starc', now, 'scoreboard players set #ok bm.rng 0',
                            'execute on origin unless score @s bm.mcd6 > #now bm.rng run scoreboard players set #ok bm.rng 1',
                            'execute if score #ok bm.rng matches 0 run return 0',
                            'execute on origin run scoreboard players operation @s bm.mcd6 = #now bm.rng', 'execute on origin run scoreboard players add @s bm.mcd6 60'] +
       [f'summon minecraft:marker ~{dx} ~{h} ~{dz} {{Tags:["bm.fstar","bm.fsnew"]}}' for dx, dz, h in ((0, 0, 14), (2, 1, 17), (-2, -1, 20), (1, -2, 23), (-1, 2, 26))] +
       ['scoreboard players set @e[type=minecraft:marker,tag=bm.fsnew] bm.gwt 60', 'tag @e[type=minecraft:marker,tag=bm.fsnew] remove bm.fsnew'] +
       ['playsound minecraft:block.beacon.activate player @a[distance=..32] ~ ~ ~ 1 1.8'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.fstar] at @s run function bm:p45/starcall/fall')
    fn('p45/starcall/fall', ['scoreboard players remove @s bm.gwt 1', 'execute if score @s bm.gwt matches ..0 run return run kill @s', 'tp @s ~ ~-0.9 ~', 'particle minecraft:end_rod ~ ~ ~ 0.05 0.2 0.05 0.01 3', 'particle minecraft:dust{color:[1.0,0.95,0.4],scale:2} ~ ~ ~ 0 0 0 0 1',
                             'execute if block ~ ~-0.5 ~ #bm:grap_pass unless entity @e[type=!#bm:p44_nonmob,type=!minecraft:player,tag=!bm.npc,distance=..1] run return 0',
                             f'execute as @e[{mob},distance=..2.5] run damage @s 6 minecraft:magic',
                             'particle minecraft:firework ~ ~0.5 ~ 0.4 0.4 0.4 0.15 25', 'particle minecraft:flash{color:[1.0,0.95,0.6,1.0]} ~ ~0.5 ~ 0 0 0 0 1',
                             'playsound minecraft:entity.firework_rocket.blast player @a[distance=..32] ~ ~ ~ 1 1.2', 'kill @s'])

    # ------------------------------------------------------------------ the gems
    fn('p45/bloomheart_gem/use', ['execute unless items entity @s weapon.* ' + holds % 'bloomheart_gem' + ' run return 0'] + cooldown('bm.mcd4', 900, 'The Bloomheart') +
       ['effect give @a[distance=..8,gamemode=!spectator] minecraft:regeneration 8 1',
        'execute as @e[type=#bm:p42_ally,distance=..8] run effect give @s minecraft:regeneration 8 1'] +
       [f'particle minecraft:cherry_leaves ^{8 * math.sin(math.radians(a)):.2f} ^0.3 ^{8 * math.cos(math.radians(a)):.2f} 0.3 0.2 0.3 0 3' for a in range(0, 360, 20)] +
       ['particle minecraft:spore_blossom_air ~ ~1 ~ 4 1 4 0 60', 'particle minecraft:heart ~ ~1.5 ~ 3 0.5 3 0 12',
        'playsound minecraft:block.spore_blossom.place player @a[distance=..24] ~ ~ ~ 1 0.8', 'playsound minecraft:block.amethyst_block.chime player @a[distance=..24] ~ ~ ~ 1 1.4',
        say('The Bloomheart flowers: everyone nearby heals.', '#ff7ae0')])
    second += [f'execute as @a if items entity @s weapon.offhand {holds % "bloomheart_gem"} run effect clear @s minecraft:poison',
               f'execute as @a if items entity @s weapon.offhand {holds % "bloomheart_gem"} run effect clear @s minecraft:wither']
    fn('p45/tidal_tear/use', ['execute unless items entity @s weapon.* ' + holds % 'tidal_tear' + ' run return 0'] + cooldown('bm.mcd5', 400, 'The Tidal Tear') +
       ['data merge entity @s {Fire:0s}', 'execute rotated ~ 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["bm.wave","bm.wnew"]}',
        'execute rotated ~ 0 as @e[type=minecraft:marker,tag=bm.wnew] run tp @s ~ ~ ~ ~ 0', 'scoreboard players set @e[type=minecraft:marker,tag=bm.wnew] bm.wav 13',
        'tag @e[type=minecraft:marker,tag=bm.wnew] remove bm.wnew',
        'playsound minecraft:entity.player.splash.high_speed player @a[distance=..24] ~ ~ ~ 1 0.6', 'playsound minecraft:item.bucket.empty player @a[distance=..24] ~ ~ ~ 1 0.8'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.wave] at @s run function bm:p45/wave/tick')
    fn('p45/wave/tick', ['scoreboard players remove @s bm.wav 1', 'execute if score @s bm.wav matches ..0 run return run kill @s', 'tp @s ^ ^ ^0.8'] +
       [f'particle minecraft:splash ^{x} ^{y} ^ 0.1 0.2 0.1 0 4' for x in (-1.5, -0.75, 0, 0.75, 1.5) for y in (0.3, 1.2)] +
       ['particle minecraft:bubble_pop ^ ^0.8 ^ 1.2 0.6 0.2 0.05 8', 'particle minecraft:falling_water ^ ^1.8 ^ 1.4 0.2 0.2 0 6',
        'fill ~-2 ~-1 ~-2 ~2 ~2 ~2 minecraft:air replace #minecraft:fire',
        f'execute as @e[{mob},distance=..2.2] at @s run function bm:p45/wave/push'])
    fn('p45/wave/push', ['execute unless entity @s[tag=bm.waved] run damage @s 4 minecraft:drown', 'tag @s add bm.waved', 'data merge entity @s {Fire:0s}',
                         'effect give @s minecraft:slowness 4 1', 'execute rotated as @e[type=minecraft:marker,tag=bm.wave,sort=nearest,limit=1] run tp @s ^ ^ ^0.8',
                         'schedule function bm:p45/wave/untag 30t replace'])
    fn('p45/wave/untag', ['tag @e[tag=bm.waved] remove bm.waved'])

    # ------------------------------------------------------------------ Grand Banquet
    def placer(name, spawn_fn, msg='Look at the top of a block within 5 blocks.'):
        fn(f'p45/{name}/place', ['execute unless function bm:p37/allowed run return run ' + say('Not here.'),
                                 'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                                 f'execute anchored eyes positioned ^ ^ ^ run function bm:p45/{name}/ray', 'tag @s remove bm.placer',
                                 'execute if score #placed bm.rng matches 0 run return run ' + say(msg),
                                 f'execute unless entity @s[gamemode=creative] run clear @s {holds % name if name in ITEMS else holds % "grand_banquet"} 1'])
        fn(f'p45/{name}/ray', [f'execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p45/{name}/hit',
                               'scoreboard players remove #ray bm.rng 1', f'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p45/{name}/ray'])
        fn(f'p45/{name}/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                               'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.p45hit,distance=..0.6] run return 0',
                               f'execute align xyz positioned ~0.5 ~1 ~0.5 rotated as @a[tag=bm.placer,limit=1] rotated ~180 0 run function bm:p45/{spawn_fn}',
                               'scoreboard players set #placed bm.rng 1'])
    placer('banquet', 'banquet/spawn')
    fn('p45/banquet/spawn', [f'summon minecraft:item_display ~ ~ ~ {disp("bm:banquet3d", ["bm.bqdisp", "bm.p45new"], 1.0, 0.5)}',
                             f'summon minecraft:interaction ~ ~ ~ {snbt({"Tags": ["bm.bqhit", "bm.p45hit", "bm.p45new"], "width": F(1.0), "height": F(0.45), "response": B(1)})}',
                             'scoreboard players set @e[tag=bm.p45new,distance=..0.5] bm.bqn 8', 'tp @e[tag=bm.p45new,distance=..0.5] ~ ~ ~ ~ 0',
                             'tag @e[tag=bm.p45new,distance=..0.5] remove bm.p45new',
                             'playsound minecraft:block.wood.place block @a[distance=..16] ~ ~ ~ 1 0.8', 'particle minecraft:happy_villager ~ ~0.4 ~ 0.4 0.2 0.4 0 12'])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.bqhit] if data entity @s interaction at @s run function bm:p45/banquet/click')
    fn('p45/banquet/click', ['tag @s add bm.bqme', 'execute on target at @s run function bm:p45/banquet/eat', 'tag @s remove bm.bqme', 'data remove entity @s interaction'])
    fn('p45/banquet/eat', [now, 'execute if score @s bm.bqc > #now bm.rng run return run ' + say('You\'re still full. Give it a moment.'),
                           'scoreboard players operation @s bm.bqc = #now bm.rng', 'scoreboard players add @s bm.bqc 600',
                           'effect give @s minecraft:saturation 1 4 true', 'effect give @s minecraft:regeneration 10 0', 'effect give @s minecraft:absorption 60 0',
                           'playsound minecraft:entity.generic.eat player @a[distance=..16] ~ ~ ~ 1 1', 'playsound minecraft:entity.player.burp player @a[distance=..16] ~ ~ ~ 1 1',
                           'execute as @e[type=minecraft:interaction,tag=bm.bqme] at @s run function bm:p45/banquet/serve',
                           say('A helping of the Grand Banquet. Delicious.', '#ffd23f')])
    fn('p45/banquet/serve', ['scoreboard players remove @s bm.bqn 1', 'particle minecraft:item{item:"minecraft:cooked_beef"} ~ ~0.4 ~ 0.3 0.1 0.3 0.05 8',
                             'execute if score @s bm.bqn matches ..0 run function bm:p45/banquet/done'])
    fn('p45/banquet/done', ['kill @e[type=minecraft:item_display,tag=bm.bqdisp,distance=..0.4]', 'summon minecraft:item ~ ~0.2 ~ {Item:{id:"minecraft:bone",count:3}}',
                            'particle minecraft:poof ~ ~0.3 ~ 0.3 0.1 0.3 0.02 10', 'kill @s'])

    # ------------------------------------------------------------------ placeables with a hitbox: lava lamp, whoopee cushion, display skiff, boombox
    def pickup(kind, iid, extra=()):
        fast.append(f'execute as @e[type=minecraft:interaction,tag=bm.{kind}hit] if data entity @s attack at @s run function bm:p45/{kind}/punch')
        fn(f'p45/{kind}/punch', ['tag @s add bm.p45me', f'execute on attacker if predicate bm:p20/sneaking run function bm:p45/{kind}/pick',
                                 'tag @s remove bm.p45me', 'data remove entity @s attack'])
        fn(f'p45/{kind}/pick', [give(iid), 'execute as @e[type=minecraft:interaction,tag=bm.p45me] at @s run function bm:p45/{kind}/gone'.format(kind=kind),
                                'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 1 1'])
        fn(f'p45/{kind}/gone', list(extra) + [f'kill @e[type=minecraft:item_display,tag=bm.{kind}d,distance=..0.6]', 'particle minecraft:poof ~ ~0.3 ~ 0.2 0.2 0.2 0.02 6', 'kill @s'])
    # the lava lamp: a lamp, two blobs drifting up and down, a light block
    for name in ('lava_lamp', 'whoopee_cushion', 'display_skiff', 'boombox'):
        fn(f'p45/{name}/use', [f'function bm:p45/{name}/place'])
    placer('lava_lamp', 'lava/spawn')
    hit = lambda tag, w, h: snbt({'Tags': [f'bm.{tag}hit', 'bm.p45hit', 'bm.p45new'], 'width': F(w), 'height': F(h), 'response': B(1)})
    fn('p45/lava/spawn', [f'summon minecraft:item_display ~ ~ ~ {disp("bm:lava3d_purple", ["bm.lavad", "bm.lavalamp", "bm.p45new"], 1.0, 0.5, 15)}',
                          f'summon minecraft:item_display ~ ~ ~ {disp("bm:lavablob_purple", ["bm.lavad", "bm.lavablob", "bm.lb1", "bm.p45new"], 1.0, 0.3, 15)}',
                          f'summon minecraft:item_display ~ ~ ~ {disp("bm:lavablob_purple", ["bm.lavad", "bm.lavablob", "bm.lb2", "bm.p45new"], 0.8, 0.62, 15)}',
                          f'summon minecraft:interaction ~ ~ ~ {hit("lava", 0.5, 0.95)}',
                          'scoreboard players set @e[tag=bm.p45new,distance=..0.5] bm.lav 0', 'tp @e[tag=bm.p45new,distance=..0.5] ~ ~ ~ ~ 0', 'tag @e[tag=bm.p45new,distance=..0.5] remove bm.p45new',
                          'execute if block ~ ~ ~ #minecraft:air run setblock ~ ~ ~ minecraft:light[level=12]',
                          'playsound minecraft:block.glass.place block @a[distance=..16] ~ ~ ~ 1 1.2'])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.lavahit] if data entity @s interaction at @s run function bm:p45/lava/click')
    fn('p45/lava/click', ['data remove entity @s interaction', 'scoreboard players add @s bm.lav 1', f'execute if score @s bm.lav matches {len(LAVA)}.. run scoreboard players set @s bm.lav 0'] +
       [f'execute if score @s bm.lav matches {i} run function bm:p45/lava/col_{c}' for i, c in enumerate(LAVA)] +
       ['playsound minecraft:block.bubble_column.upwards_inside block @a[distance=..16] ~ ~ ~ 1 1.4'])
    for c in LAVA:
        fn(f'p45/lava/col_{c}', [f'data modify entity @e[type=minecraft:item_display,tag=bm.lavalamp,distance=..0.4,limit=1] item.components."minecraft:item_model" set value "bm:lava3d_{c}"',
                                 f'execute as @e[type=minecraft:item_display,tag=bm.lavablob,distance=..0.4] run data modify entity @s item.components."minecraft:item_model" set value "bm:lavablob_{c}"'])
    pickup('lava', 'lava_lamp', ['execute if block ~ ~ ~ minecraft:light run setblock ~ ~ ~ minecraft:air'])
    # blobs drift: every 2 s they swap ends (interpolated), the second one half a cycle behind
    second += ['scoreboard players add #lavt bm.rng 1', 'execute if score #lavt bm.rng matches 4.. run scoreboard players set #lavt bm.rng 0',
               'execute if score #lavt bm.rng matches 0 as @e[type=minecraft:item_display,tag=bm.lb1] run data merge entity @s {start_interpolation:0,interpolation_duration:38,transformation:{translation:[0f,0.66f,0f]}}',
               'execute if score #lavt bm.rng matches 0 as @e[type=minecraft:item_display,tag=bm.lb2] run data merge entity @s {start_interpolation:0,interpolation_duration:38,transformation:{translation:[0f,0.3f,0f]}}',
               'execute if score #lavt bm.rng matches 2 as @e[type=minecraft:item_display,tag=bm.lb1] run data merge entity @s {start_interpolation:0,interpolation_duration:38,transformation:{translation:[0f,0.3f,0f]}}',
               'execute if score #lavt bm.rng matches 2 as @e[type=minecraft:item_display,tag=bm.lb2] run data merge entity @s {start_interpolation:0,interpolation_duration:38,transformation:{translation:[0f,0.66f,0f]}}']
    # the whoopee cushion
    placer('whoopee_cushion', 'whoop/spawn')
    fn('p45/whoop/spawn', [f'summon minecraft:item_display ~ ~ ~ {disp("bm:whoopee3d", ["bm.whoopd", "bm.p45new"], 1.0, 0.5)}',
                           f'summon minecraft:interaction ~ ~ ~ {hit("whoop", 0.7, 0.15)}', 'tp @e[tag=bm.p45new,distance=..0.5] ~ ~ ~ ~ 0', 'tag @e[tag=bm.p45new,distance=..0.5] remove bm.p45new',
                           'playsound minecraft:block.wool.place block @a[distance=..8] ~ ~ ~ 1 1'])
    pickup('whoop', 'whoopee_cushion')
    GAGS = ['Excuse YOU.', 'Was that... you?', 'Somebody call a doctor.', 'The rats are laughing at you.', 'Classic.', 'Pardon!', 'Ew.']
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.whoopd] at @s if entity @e[type=!#bm:p44_nonmob,distance=..0.6,tag=!bm.npc] unless score @s bm.trt matches 1.. run function bm:p45/whoop/toot')
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.whoopd] at @s if entity @a[distance=..0.6,gamemode=!spectator] unless score @s bm.trt matches 1.. run function bm:p45/whoop/toot')
    second.append('scoreboard players remove @e[type=minecraft:item_display,tag=bm.whoopd,scores={bm.trt=1..}] bm.trt 1')
    fn('p45/whoop/toot', ['scoreboard players set @s bm.trt 2', 'playsound minecraft:block.honey_block.slide neutral @a[distance=..24] ~ ~ ~ 1.2 0.5',
                          'playsound minecraft:entity.llama.spit neutral @a[distance=..24] ~ ~ ~ 1.2 0.5', 'playsound minecraft:entity.goat.screaming.ambient neutral @a[distance=..24] ~ ~ ~ 0.3 1.8',
                          'particle minecraft:dust{color:[0.6,0.75,0.3],scale:1.6} ~ ~0.3 ~ 0.4 0.2 0.4 0 12', 'particle minecraft:poof ~ ~0.2 ~ 0.3 0.05 0.3 0.02 6',
                          f'execute store result score #g bm.rng run random value 1..{len(GAGS)}'] +
       [f'execute if score #g bm.rng matches {i} as @a[distance=..1.2] run ' + title('@s', 'actionbar', T(g, '#ff7ab0')) for i, g in enumerate(GAGS, 1)])
    # the display skiff: paint with a dye, sneak + right-click for the next decal
    placer('display_skiff', 'dskiff/spawn')
    SK = 1.3
    fn('p45/dskiff/spawn', [f'summon minecraft:item_display ~ ~ ~ {disp("bm:skiff_green_none", ["bm.dskiffd", "bm.p45new"], SK, round(SK * (0.5 - 3 / 16), 3))}',
                            f'summon minecraft:interaction ~ ~ ~ {hit("dskiff", 1.2, 0.8)}', 'scoreboard players set @e[tag=bm.p45new,distance=..0.5] bm.skp 0',
                            'scoreboard players set @e[tag=bm.p45new,distance=..0.5] bm.skd2 0', 'tp @e[tag=bm.p45new,distance=..0.5] ~ ~ ~ ~ 0', 'tag @e[tag=bm.p45new,distance=..0.5] remove bm.p45new',
                            'playsound minecraft:block.beacon.power_select block @a[distance=..16] ~ ~ ~ 0.6 1.6'])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.dskiffhit] if data entity @s interaction at @s run function bm:p45/dskiff/click')
    fn('p45/dskiff/click', ['tag @s add bm.p45me', 'execute on target run function bm:p45/dskiff/who', 'tag @s remove bm.p45me', 'data remove entity @s interaction'])
    fn('p45/dskiff/who', ['execute if predicate bm:p20/sneaking run return run execute as @e[type=minecraft:interaction,tag=bm.p45me] at @s run function bm:p45/dskiff/decal'] +
       [f'execute if items entity @s weapon.mainhand minecraft:{d}_dye run return run function bm:p45/dskiff/dye {{p:{i}}}' for d, i in DYES.items()] +
       [say('Right-click with a dye to repaint it; sneak + right-click for the next decal.')])
    fn('p45/dskiff/dye', ['$scoreboard players set @e[type=minecraft:interaction,tag=bm.p45me] bm.skp $(p)', 'execute unless entity @s[gamemode=creative] run item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                          'playsound minecraft:item.dye.use player @a[distance=..16] ~ ~ ~ 1 1', 'execute as @e[type=minecraft:interaction,tag=bm.p45me] at @s run function bm:p45/dskiff/apply'])
    fn('p45/dskiff/decal', ['scoreboard players add @s bm.skd2 1', 'execute if score @s bm.skd2 matches 4.. run scoreboard players set @s bm.skd2 0',
                            'playsound minecraft:item.brush.brushing.generic block @a[distance=..16] ~ ~ ~ 1 1.2', 'function bm:p45/dskiff/apply'])
    fn('p45/dskiff/apply', [f'execute if score @s bm.skp matches {i} if score @s bm.skd2 matches {j} run data modify entity @e[type=minecraft:item_display,tag=bm.dskiffd,distance=..0.6,limit=1] item.components."minecraft:item_model" set value "bm:skiff_{c}_{d}"'
                            for i, c in enumerate(SKIFF_COLS) for j, d in enumerate(SKIFF_DECALS)] +
       ['particle minecraft:wax_on ~ ~0.5 ~ 0.5 0.3 0.5 0 10'])
    pickup('dskiff', 'display_skiff')
    # the boombox
    placer('boombox', 'boom/spawn')
    fn('p45/boom/spawn', [f'summon minecraft:item_display ~ ~ ~ {disp("bm:boombox3d", ["bm.boomd", "bm.p45new"], 1.0, 0.5)}',
                          f'summon minecraft:interaction ~ ~ ~ {hit("boom", 0.9, 0.7)}', 'scoreboard players set @e[tag=bm.p45new,distance=..0.5] bm.trk -1', 'tp @e[tag=bm.p45new,distance=..0.5] ~ ~ ~ ~ 0',
                          'tag @e[tag=bm.p45new,distance=..0.5] remove bm.p45new', 'playsound minecraft:block.note_block.bit block @a[distance=..16] ~ ~ ~ 1 1'])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.boomhit] if data entity @s interaction at @s run function bm:p45/boom/click')
    fn('p45/boom/click', ['tag @s add bm.p45me', 'execute on target run function bm:p45/boom/who', 'tag @s remove bm.p45me', 'data remove entity @s interaction'])
    fn('p45/boom/who', ['execute if predicate bm:p20/sneaking run return run execute as @e[type=minecraft:interaction,tag=bm.p45me] at @s run function bm:p45/boom/stop',
                        'execute as @e[type=minecraft:interaction,tag=bm.p45me] at @s run function bm:p45/boom/next'])
    fn('p45/boom/stop', ['scoreboard players set @s bm.trk -1', 'scoreboard players set @s bm.trt 0', 'stopsound @a[distance=..64] record',
                         'playsound minecraft:block.note_block.bit block @a[distance=..16] ~ ~ ~ 1 0.5', 'particle minecraft:smoke ~ ~0.7 ~ 0.2 0.1 0.2 0 4'])
    fn('p45/boom/next', ['stopsound @a[distance=..64] record', 'scoreboard players add @s bm.trk 1', f'execute if score @s bm.trk matches {len(TRACKS)}.. run scoreboard players set @s bm.trk 0'] +
       [f'execute if score @s bm.trk matches {i} run function bm:p45/boom/play_{t}' for i, (t, _) in enumerate(TRACKS)])
    for t, secs in TRACKS:
        fn(f'p45/boom/play_{t}', [f'playsound minecraft:music_disc.{t} record @a[distance=..48] ~ ~0.5 ~ 3 1', f'scoreboard players set @s bm.trt {secs}',
                                  title('@a[distance=..8]', 'actionbar', [T('Now playing: ', 'gray'), T(f'C418 & friends - "{t.replace("_", " ").title()}"', '#ff4a4a')])])
    second += ['scoreboard players remove @e[type=minecraft:interaction,tag=bm.boomhit,scores={bm.trt=1..}] bm.trt 1',
               'execute as @e[type=minecraft:interaction,tag=bm.boomhit,scores={bm.trt=1..}] at @s run particle minecraft:note ~ ~0.9 ~ 0.3 0.2 0.3 1 1']
    pickup('boom', 'boombox', ['execute if score @s bm.trt matches 1.. run stopsound @a[distance=..64] record'])

    # ------------------------------------------------------------------ the trash can (summoned like the Hoard Sack)
    fn('p45/trash_can/use', ['execute unless function bm:p37/allowed run return run ' + say('Not here.'),
                             'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #kp bm.pid = @s bm.pid',
                             'scoreboard players set #had bm.rng 0',
                             'execute as @e[type=minecraft:marker,tag=bm.trashm] if score @s bm.pid = #kp bm.pid at @s run function bm:p45/trash/fold_mine',
                             'execute if score #had bm.rng matches 1 run return 0', 'scoreboard players set #ok bm.rng 0',
                             'execute rotated ~ 0 positioned ^ ^ ^1.6 align xyz positioned ~0.5 ~ ~0.5 run function bm:p45/trash/try',
                             'execute if score #ok bm.rng matches 0 rotated ~ 0 positioned ^ ^ ^2.6 align xyz positioned ~0.5 ~ ~0.5 run function bm:p45/trash/try',
                             'execute if score #ok bm.rng matches 0 run ' + say('No room on the ground in front of you.')])
    fn('p45/trash/try', ['execute unless block ~ ~ ~ #bm:p41_open run return 0', 'execute if block ~ ~-1 ~ #minecraft:replaceable run return 0',
                         'setblock ~ ~ ~ minecraft:barrel[facing=up]{CustomName:{text:"Trash Can",color:"#8ab88a"}}',
                         f'summon minecraft:item_display ~ ~ ~ {disp("bm:trash3d", ["bm.trashd"], 1.0, 0.5)}',
                         'summon minecraft:marker ~ ~ ~ {Tags:["bm.trashm","bm.tnew"]}',
                         'scoreboard players operation @e[type=minecraft:marker,tag=bm.tnew,distance=..0.5] bm.pid = #kp bm.pid',
                         'scoreboard players set @e[type=minecraft:marker,tag=bm.tnew,distance=..0.5] bm.trt 120', 'tag @e[type=minecraft:marker,tag=bm.tnew] remove bm.tnew',
                         'scoreboard players set #ok bm.rng 1', 'playsound minecraft:block.iron_trapdoor.open block @a[distance=..16] ~ ~ ~ 1 0.8'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.trashm] at @s run function bm:p45/trash/check')
    fn('p45/trash/check', ['execute unless block ~ ~ ~ minecraft:barrel run return run function bm:p45/trash/gone',
                           'execute if data block ~ ~ ~ Items[0] run function bm:p45/trash/munch',
                           'scoreboard players remove @s bm.trt 1', 'scoreboard players operation #kp bm.pid = @s bm.pid', 'scoreboard players set #near bm.rng 0',
                           'execute as @a[distance=..6] if score @s bm.pid = #kp bm.pid run scoreboard players set #near bm.rng 1',
                           'execute if score #near bm.rng matches 0 run return run function bm:p45/trash/fold',
                           'execute if score @s bm.trt matches ..0 run function bm:p45/trash/fold'])
    fn('p45/trash/munch', ['data modify block ~ ~ ~ Items set value []', 'particle minecraft:large_smoke ~ ~0.8 ~ 0.2 0.2 0.2 0.02 8',
                           'playsound minecraft:entity.generic.burn block @a[distance=..16] ~ ~ ~ 0.6 1.2', 'playsound minecraft:block.grindstone.use block @a[distance=..16] ~ ~ ~ 0.6 0.8'])
    fn('p45/trash/fold_mine', ['scoreboard players set #had bm.rng 1', 'function bm:p45/trash/fold'])
    fn('p45/trash/fold', ['execute if block ~ ~ ~ minecraft:barrel run data modify block ~ ~ ~ Items set value []', 'execute if block ~ ~ ~ minecraft:barrel run setblock ~ ~ ~ minecraft:air',
                          'playsound minecraft:block.iron_trapdoor.close block @a[distance=..16] ~ ~ ~ 1 0.8', 'function bm:p45/trash/gone'])
    fn('p45/trash/gone', ['kill @e[type=minecraft:item_display,tag=bm.trashd,distance=..0.5]', 'particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.02 8', 'kill @s'])

    # ------------------------------------------------------------------ the ocarina
    notes = 25
    fn('p45/ocarina/use', ['execute if predicate bm:p20/sneaking run return run function bm:p45/ocarina/switch',
                           'execute unless score @s bm.ocn matches 0.. run scoreboard players set @s bm.ocn 0',
                           'scoreboard players set #n bm.rng 0'] +
       [f'execute if entity @s[x_rotation={90 - (i + 1) * 180 / notes:.1f}..{90 - i * 180 / notes:.1f}] run scoreboard players set #n bm.rng {i}' for i in range(notes)] +
       [f'execute if score @s bm.ocn matches {k} run function bm:p45/ocarina/{ins}' for k, (ins, _) in enumerate(INSTRUMENTS)])
    for ins, _ in INSTRUMENTS:
        fn(f'p45/ocarina/{ins}', [f'execute if score #n bm.rng matches {i} run playsound minecraft:block.note_block.{ins} player @a[distance=..32] ~ ~1.5 ~ 1 {0.5 * 2 ** (i / 12):.4f}' for i in range(notes)] +
           [f'execute if score #n bm.rng matches {i} run particle minecraft:note ~ ~2.1 ~ {i / 24:.3f} 0 0 1 0' for i in range(notes)])
    fn('p45/ocarina/switch', ['scoreboard players add @s bm.ocn 1', f'execute if score @s bm.ocn matches {len(INSTRUMENTS)}.. run scoreboard players set @s bm.ocn 0'] +
       [f'execute if score @s bm.ocn matches {k} run ' + title('@s', 'actionbar', [T('Instrument: ', 'gray'), T(nm, '#6ab0ff')]) for k, (_, nm) in enumerate(INSTRUMENTS)])

    # ------------------------------------------------------------------ chest finds
    def hook(t):
        if f'loot/{t}' not in G.FUNCS:
            wjson(f'bm/advancement/loot/{t}.json', {'criteria': {'opened': {'trigger': 'minecraft:player_generates_container_loot',
                                                                            'conditions': {'loot_table': f'minecraft:chests/{t}'}}},
                                                    'rewards': {'function': f'bm:loot/{t}'}})
            fn(f'loot/{t}', [f'advancement revoke @s only bm:loot/{t}'])
        return G.FUNCS[f'loot/{t}']
    for iid, tables in CHEST_FINDS.items():
        fn(f'p45/found/{iid}', [give(iid), tellraw('@s', PREFIX + [T('Odd find! ', '#ff7ac8', bold=True), T('You found a ', 'gray'), T(ITEMS[iid]['name'], 'yellow'),
                                                                   T(' in the chest.', 'gray')]), 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6'])
        for t, pct in tables.items():
            hook(t).extend(['execute store result score @s bm.rng run random value 1..100', f'execute if score @s bm.rng matches 1..{pct} run function bm:p45/found/{iid}'])

    # ------------------------------------------------------------------ CECIL: a hitbox villager and a four-part rig
    rig = [f'summon minecraft:item_display ~ ~ ~ {disp("bm:cec_body", ["bm.npc", "bm.new", "bm.cecil", "bm.cec_body"], 1.0, 0.5, 13, 3)}',
           f'summon minecraft:item_display ~ ~ ~ {disp("bm:cec_head", ["bm.npc", "bm.new", "bm.cecil", "bm.cec_head"], 1.0, 0.0, 13, 3)}',
           f'summon minecraft:item_display ~ ~ ~ {disp("bm:cec_eyes", ["bm.npc", "bm.new", "bm.cecil", "bm.cec_eyes"], 1.0, 0.0, 15, 3)}',
           f'summon minecraft:item_display ~ ~ ~ {disp("bm:cec_arm", ["bm.npc", "bm.new", "bm.cecil", "bm.cec_arm"], 1.0, 0.0, 13, 3, {"transformation": {"left_rotation": q("x", 6), "right_rotation": ident, "translation": [F(0), F(0), F(0)], "scale": [F(1)] * 3}})}']
    fn('p45/cecil/rig', rig)
    fn('p45/cecil/spawn', [l for l in G.FUNCS['npc/wizard'] if not l.startswith('execute rotated as @s') and not l.startswith('tag @e[tag=bm.new')] +
       ['execute rotated ~ 0 run tp @e[tag=bm.new,distance=..3] ~ ~ ~ ~ 0', 'execute as @e[tag=bm.new,tag=bm.cecil,distance=..3] at @s run function bm:p45/cecil/settle',
        'tag @e[tag=bm.new,distance=..3] remove bm.new'])
    fn('p45/cecil/settle', ['execute if entity @s[tag=bm.cec_head] run tp @s ^ ^1.38 ^0.12', 'execute if entity @s[tag=bm.cec_eyes] run tp @s ^ ^1.38 ^0.12',
                            'execute if entity @s[tag=bm.cec_arm] run tp @s ^-0.31 ^1.28 ^0.06'])
    # (the parts are summoned on the villager, turned with it, then settle steps each to its joint)
    G.FUNCS['p35/patch'].append(f'execute positioned {mgeo.rel(CECIL_POS)} unless entity @e[type=minecraft:villager,tag=bm.npc_wizard,distance=..4] rotated ~{CECIL_YAW} 0 run function bm:p45/cecil/spawn')
    G.FUNCS['p35/patch'].append(f'execute positioned {mgeo.rel(CECIL_POS)} as @e[type=minecraft:villager,tag=bm.npc_wizard,distance=..4] at @s unless entity @e[type=minecraft:item_display,tag=bm.cec_body,distance=..1] run function bm:p45/cecil/rerig')
    fn('p45/cecil/rerig', ['kill @e[type=minecraft:item_display,tag=bm.cecil,distance=..3]', 'execute rotated as @s rotated ~ 0 run function bm:p45/cecil/rig_here'])
    fn('p45/cecil/rig_here', rig + ['execute rotated ~ 0 run tp @e[tag=bm.new,tag=bm.cecil,distance=..3] ~ ~ ~ ~ 0',
                                    'execute as @e[tag=bm.new,tag=bm.cecil,distance=..3] at @s run function bm:p45/cecil/settle', 'tag @e[tag=bm.new,distance=..3] remove bm.new'])
    # animation (near players only): turn to the nearest player, look at them; breathe; sway; now and then cast
    tick.append('execute as @e[type=minecraft:villager,tag=bm.npc_wizard] at @s if entity @a[distance=..20] run function bm:p45/cecil/tick')
    fn('p45/cecil/tick', ['scoreboard players add @s bm.cct 1', 'execute if score @s bm.cct matches 200.. run scoreboard players set @s bm.cct 0',
                          'execute if entity @a[distance=..10,gamemode=!spectator] facing entity @p[distance=..10,gamemode=!spectator] feet rotated ~ 0 run function bm:p45/cecil/face',
                          'scoreboard players operation #c bm.rng = @s bm.cct', 'scoreboard players operation #c bm.rng %= #40 bm.rng',
                          'execute if score #c bm.rng matches 0 run function bm:p45/cecil/inhale', 'execute if score #c bm.rng matches 20 run function bm:p45/cecil/exhale',
                          'execute if score @s bm.cct matches 140 run function bm:p45/cecil/cast_up', 'execute if score @s bm.cct matches 147 run function bm:p45/cecil/cast_fx',
                          'execute if score @s bm.cct matches 162 run function bm:p45/cecil/cast_down',
                          'execute if score @s bm.cct matches 60 run particle minecraft:witch ^-0.31 ^2.75 ^0.45 0.1 0.15 0.1 0 3',
                          'execute if score @s bm.cct matches 100 run particle minecraft:portal ~ ~1 ~ 0.4 0.6 0.4 0.3 10'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #40 bm.rng 40']
    fn('p45/cecil/face', ['tp @e[type=minecraft:item_display,tag=bm.cec_body,distance=..1,limit=1] ~ ~ ~ ~ 0',
                          'execute positioned ^-0.31 ^1.28 ^0.06 run tp @e[type=minecraft:item_display,tag=bm.cec_arm,distance=..2,limit=1] ~ ~ ~ ~ 0',
                          'execute positioned ^ ^1.38 ^0.12 run tp @e[type=minecraft:item_display,tag=bm.cec_head,distance=..2,limit=1] ~ ~ ~ facing entity @p[distance=..10,gamemode=!spectator] eyes',
                          'execute positioned ^ ^1.38 ^0.12 run tp @e[type=minecraft:item_display,tag=bm.cec_eyes,distance=..2,limit=1] ~ ~ ~ facing entity @p[distance=..10,gamemode=!spectator] eyes'])
    tr = lambda y: f'translation:[0f,{y}f,0f]'
    fn('p45/cecil/inhale', [f'data merge entity @e[type=minecraft:item_display,tag=bm.cec_body,distance=..1,limit=1] {{start_interpolation:0,interpolation_duration:20,transformation:{{{tr(0.52)},scale:[1f,1.02f,1f]}}}}',
                            f'execute as @e[type=minecraft:item_display,tag=bm.cec_head,distance=..3] run data merge entity @s {{start_interpolation:0,interpolation_duration:20,transformation:{{{tr(0.035)}}}}}',
                            f'execute as @e[type=minecraft:item_display,tag=bm.cec_eyes,distance=..3] run data merge entity @s {{start_interpolation:0,interpolation_duration:20,transformation:{{{tr(0.035)}}}}}',
                            f'execute unless score @s bm.cct matches 140..170 as @e[type=minecraft:item_display,tag=bm.cec_arm,distance=..3] run data merge entity @s {{start_interpolation:0,interpolation_duration:20,transformation:{{{tr(0.03)},left_rotation:{snbt(q("x", 10))}}}}}'])
    fn('p45/cecil/exhale', [f'data merge entity @e[type=minecraft:item_display,tag=bm.cec_body,distance=..1,limit=1] {{start_interpolation:0,interpolation_duration:20,transformation:{{{tr(0.5)},scale:[1f,1f,1f]}}}}',
                            f'execute as @e[type=minecraft:item_display,tag=bm.cec_head,distance=..3] run data merge entity @s {{start_interpolation:0,interpolation_duration:20,transformation:{{{tr(0)}}}}}',
                            f'execute as @e[type=minecraft:item_display,tag=bm.cec_eyes,distance=..3] run data merge entity @s {{start_interpolation:0,interpolation_duration:20,transformation:{{{tr(0)}}}}}',
                            f'execute unless score @s bm.cct matches 140..170 as @e[type=minecraft:item_display,tag=bm.cec_arm,distance=..3] run data merge entity @s {{start_interpolation:0,interpolation_duration:20,transformation:{{{tr(0)},left_rotation:{snbt(q("x", 4))}}}}}'])
    fn('p45/cecil/cast_up', [f'execute as @e[type=minecraft:item_display,tag=bm.cec_arm,distance=..3] run data merge entity @s {{start_interpolation:0,interpolation_duration:6,transformation:{{left_rotation:{snbt(q("x", 38))}}}}}',
                             'playsound minecraft:entity.evoker.prepare_summon neutral @a[distance=..12] ~ ~ ~ 0.4 1.6'])
    fn('p45/cecil/cast_fx', ['execute positioned ^-0.31 ^1.28 ^0.06 positioned ^ ^1.05 ^1.0 run particle minecraft:dust{color:[1.0,0.45,0.8],scale:1.5} ~ ~ ~ 0.25 0.25 0.25 0 20',
                             'execute positioned ^-0.31 ^1.28 ^0.06 positioned ^ ^1.05 ^1.0 run particle minecraft:enchant ~ ~ ~ 0.4 0.4 0.4 1 30',
                             'execute positioned ^-0.31 ^1.28 ^0.06 positioned ^ ^1.05 ^1.0 run particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.08 8',
                             'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..12] ~ ~ ~ 1 1.2'])
    fn('p45/cecil/cast_down', [f'execute as @e[type=minecraft:item_display,tag=bm.cec_arm,distance=..3] run data merge entity @s {{start_interpolation:0,interpolation_duration:12,transformation:{{left_rotation:{snbt(q("x", 6))}}}}}'])

    # ------------------------------------------------------------------ the Vorn walk (and stand on the ground - the hoverboards are gone)
    from phase32 import HUSK_SEAT
    TS, WS = 1.15, 2.2
    tick += ['scoreboard players add #vwt bm.rng 1', 'execute if score #vwt bm.rng matches 8.. run scoreboard players set #vwt bm.rng 0',
             'execute if score #vwt bm.rng matches 0 as @e[type=minecraft:husk,tag=bm.vorn] run function bm:p45/vorn/step {p:"walk1"}',
             'execute if score #vwt bm.rng matches 4 as @e[type=minecraft:husk,tag=bm.vorn] run function bm:p45/vorn/step {p:"walk2"}']
    fn('p45/vorn/step', ['execute unless predicate bm:p21/walking run return run function bm:p45/vorn/pose {p:"stand"}', '$function bm:p45/vorn/pose {p:"$(p)"}'])
    fn('p45/vorn/pose', ['$execute on passengers if entity @s[type=minecraft:item_display] run data modify entity @s item.components."minecraft:custom_model_data" set value {strings:["$(p)"]}'])
    second += ['execute as @e[type=minecraft:husk,tag=bm.vtroop,tag=!bm.v224] run function bm:p45/vorn/fix_troop',
               'execute as @e[type=minecraft:husk,tag=bm.vb_warlord,tag=!bm.v224] run function bm:p45/vorn/fix_warlord']
    fn('p45/vorn/fix_troop', ['tag @s add bm.v224', 'execute on passengers if entity @s[tag=bm.vboard] run kill @s',
                              f'execute on passengers if entity @s[tag=bm.vbody] run data merge entity @s {{transformation:{{translation:[0f,{round(-HUSK_SEAT + TS / 2, 3)}f,0f]}}}}'])
    fn('p45/vorn/fix_warlord', ['tag @s add bm.v224', 'execute on passengers if items entity @s contents *[minecraft:item_model="bm:hoverboard_red"] run kill @s',
                                f'execute on passengers if items entity @s contents *[minecraft:item_model="bm:vorn3d_warlord"] run data merge entity @s {{transformation:{{translation:[0f,{round(-HUSK_SEAT * WS + TS * WS / 2, 3)}f,0f]}}}}'])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack
def textures():
    import random
    from PIL import Image
    from gen_rp import hexc
    rnd = random.Random(45)
    def noise(base, var, streak=None, size=16):
        im = Image.new('RGBA', (size, size)); b = hexc(base)
        for y in range(size):
            for x in range(size):
                d = rnd.randint(-var, var)
                if streak and x in streak: d -= var * 2
                im.putpixel((x, y), tuple(max(0, min(255, c + d)) for c in b[:3]))
        return im
    T_ = {}
    T_['cec_robe'] = noise('#4a1e7e', 7, streak=(3, 9, 13))
    T_['cec_robe_dark'] = noise('#2e1250', 5, streak=(5, 11))
    T_['cec_black'] = noise('#151417', 4)
    T_['cec_gold'] = noise('#c9a74a', 10)
    T_['cec_wood'] = noise('#4a2c22', 6, streak=(2, 7, 12))
    T_['cec_crystal'] = noise('#e85aa8', 14)
    for y in range(16):
        for x in range(16):
            if (x + y) % 7 == 0: T_['cec_crystal'].putpixel((x, y), hexc('#ffb0dc'))
    T_['cec_eye'] = noise('#f4dc6a', 6)
    face = noise('#1d1c21', 3)
    for y in range(16):
        for x in range(16):
            if 3 <= x <= 12 and 3 <= y <= 10: face.putpixel((x, y), hexc('#2a292f'))
    for x in range(2, 14):                       # the jagged grin: a black mouth, pale zig-zag teeth
        face.putpixel((x, 11), hexc('#050505')); face.putpixel((x, 12), hexc('#050505'))
        face.putpixel((x, 10 + (x % 2)), hexc('#9a9aa4')); face.putpixel((x, 13 - (x % 2)), hexc('#9a9aa4'))
    for (x, y) in ((1, 9), (14, 9), (1, 10), (14, 10)): face.putpixel((x, y), hexc('#9a9aa4'))
    T_['cec_face'] = face
    T_['trash_metal'] = noise('#7a8a7a', 6, streak=(1, 5, 9, 13))
    T_['trash_lid'] = noise('#8a9a8a', 5)
    T_['whoopee'] = noise('#ff6aa8', 8)
    T_['whoopee_dark'] = noise('#c8407a', 6)
    sp = Image.new('RGBA', (16, 16), hexc('#1a1a1a'))
    for y in range(16):
        for x in range(16):
            r = math.hypot(x - 7.5, y - 7.5)
            if r < 7: sp.putpixel((x, y), hexc('#3a3a3a' if r > 5.5 else '#5a5a5a' if r > 2.5 else '#8a8a8a'))
    T_['boom_speaker'] = sp
    T_['roast'] = noise('#8a4a1e', 12)
    return T_


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    cube = R.cube
    def c(fr, to, t, rot=None):
        e = cube(fr, to, t)
        if rot: e['rotation'] = rot
        return e
    def rx_(ang, o): return {'origin': list(o), 'axis': 'x', 'angle': ang}
    ct = {'r': 'bm:block/cec_robe', 'd': 'bm:block/cec_robe_dark', 'k': 'bm:block/cec_black', 'g': 'bm:block/cec_gold', 'w': 'bm:block/cec_wood',
          'p': 'bm:block/cec_crystal', 'f': 'bm:block/cec_face', 'y': 'bm:block/cec_eye'}
    # CECIL (faces -z; his right is +x). Body: a bell of a robe, hunched forward, the left claw hanging out front.
    body = [c((1.5, 0, 2.5), (14.5, 2, 13.5), 'd'), c((2, 2, 3), (14, 9, 13), 'r'), c((3, 9, 3.5), (13, 15, 12.5), 'r'), c((3.5, 15, 3), (12.5, 21, 11), 'r'),
            c((2.5, 18, 3.5), (13.5, 21.5, 10.5), 'r'), c((4, 21, 3), (12, 22.5, 9), 'd'), c((3.5, 20.5, 2.6), (5, 23, 4), 'd'), c((11, 20.5, 2.6), (12.5, 23, 4), 'd'),
            c((7.85, 2, 2.9), (8.15, 9, 3.0), 'd'), c((7.85, 9, 3.4), (8.15, 15, 3.5), 'd'), c((7.4, 18.5, 2.9), (8.6, 19.7, 3.0), 'g'),
            c((1.2, 0, 6), (2, 1.5, 9), 'd'), c((14, 0, 4), (14.8, 1.2, 7), 'd'), c((5, 0, 2.2), (7, 1, 2.6), 'd'), c((10.5, 0, 13.4), (13, 1.4, 14.2), 'd'),
            c((0.8, 13, 4.5), (4, 20.5, 8.5), 'r', rx_(22.5, (2.4, 20, 6.5))),
            c((0.9, 10.2, 2.4), (3.9, 12.8, 5.4), 'k'), c((1, 8.4, 2.6), (1.6, 10.4, 3.2), 'k'), c((2.1, 7.9, 2.6), (2.7, 10.4, 3.2), 'k'), c((3.2, 8.4, 2.6), (3.8, 10.4, 3.2), 'k')]
    head = [c((3, 8, 4), (13, 18.5, 13), 'r'), c((2.6, 8, 2.4), (4.2, 18.5, 5), 'r'), c((11.8, 8, 2.4), (13.4, 18.5, 5), 'r'), c((2.6, 16.6, 2.4), (13.4, 19, 5), 'r'),
            c((4.2, 8.4, 3.3), (11.8, 16.6, 4.2), 'f'), c((6, 18.5, 7), (10, 21, 12), 'r'), c((6.8, 20.5, 9.5), (9.2, 23.5, 13.5), 'r', rx_(22.5, (8, 21, 11))),
            c((7.2, 22.5, 12), (8.8, 24, 15.5), 'd', rx_(22.5, (8, 23, 12))), c((7.8, 18.5, 5), (8.2, 19.1, 10), 'k'), c((5, 7, 4), (11, 8.5, 10), 'd')]
    eyes = [c((4.9, 12.7, 3.0), (7.3, 13.9, 3.25), 'y', {'origin': [6.1, 13.3, 3.1], 'axis': 'z', 'angle': -22.5}),
            c((8.7, 12.7, 3.0), (11.1, 13.9, 3.25), 'y', {'origin': [9.9, 13.3, 3.1], 'axis': 'z', 'angle': 22.5})]
    arm = [c((6, -2, 6), (10, 9, 10), 'r', rx_(22.5, (8, 8, 8))), c((6.2, -3.5, 2.4), (9.8, -0.5, 5.8), 'k'),
           c((7.25, -12, 3.35), (8.75, 24, 4.85), 'w'),
           c((6.6, 21, 2.9), (9.4, 24.5, 5.3), 'g'),
           # the crescent blades: a C on each side of the socket, opening outward
           c((4.6, 18.6, 3.5), (6.6, 25.4, 4.7), 'g'), c((1.2, 24.2, 3.5), (5.2, 25.8, 4.7), 'g', {'origin': [5, 25, 4.1], 'axis': 'z', 'angle': -22.5}),
           c((1.2, 18.2, 3.5), (5.2, 19.8, 4.7), 'g', {'origin': [5, 19, 4.1], 'axis': 'z', 'angle': 22.5}),
           c((9.4, 18.6, 3.5), (11.4, 25.4, 4.7), 'g'), c((10.8, 24.2, 3.5), (14.8, 25.8, 4.7), 'g', {'origin': [11, 25, 4.1], 'axis': 'z', 'angle': 22.5}),
           c((10.8, 18.2, 3.5), (14.8, 19.8, 4.7), 'g', {'origin': [11, 19, 4.1], 'axis': 'z', 'angle': -22.5}),
           c((6.7, 24.5, 2.8), (9.3, 30, 5.4), 'p', {'origin': [8, 27, 4.1], 'axis': 'y', 'angle': 45}),
           c((7.3, 30, 3.4), (8.7, 32, 4.8), 'p', {'origin': [8, 31, 4.1], 'axis': 'y', 'angle': 45})]
    R.HATS['cec_body'] = (ct, body)
    R.HATS['cec_head'] = (ct, head)
    R.HATS['cec_eyes'] = (ct, eyes)
    R.HATS['cec_arm'] = (ct, arm)
    # lava lamps
    for col in LAVA:
        lt = {'m': 'minecraft:block/iron_block', 'g': f'minecraft:block/{col}_stained_glass', 'l': f'minecraft:block/{col}_concrete', 'b': 'minecraft:block/black_concrete'}
        R.HATS[f'lava3d_{col}'] = (lt, [c((5, 0, 5), (11, 2, 11), 'b'), c((5.5, 2, 5.5), (10.5, 3, 10.5), 'm'), c((6.3, 3, 6.3), (9.7, 4.5, 9.7), 'l'),
                                        c((6, 3, 6), (10, 12, 10), 'g'), c((6.5, 12, 6.5), (9.5, 13.5, 9.5), 'm'), c((7, 13.5, 7), (9, 14, 9), 'b')])
        R.HATS[f'lavablob_{col}'] = (lt, [c((7, 7, 7), (9, 9, 9), 'l'), c((7.5, 9, 7.5), (8.5, 9.6, 8.5), 'l'), c((7.3, 6.5, 7.3), (8.7, 7, 8.7), 'l')])
    # trash can (encloses the barrel), whoopee cushion, boombox, banquet
    R.HATS['trash3d'] = ({'t': 'bm:block/trash_metal', 'l': 'bm:block/trash_lid'}, [
        c((-0.4, 0, -0.4), (16.4, 15.5, 16.4), 't'), c((-1, 15.5, -1), (17, 17, 17), 'l'), c((5.5, 17, 7.2), (10.5, 18.2, 8.8), 'l'),
        c((-1, 4, 7), (-0.4, 6, 9), 'l'), c((16.4, 4, 7), (17, 6, 9), 'l')])
    R.HATS['whoopee3d'] = ({'p': 'bm:block/whoopee', 'q': 'bm:block/whoopee_dark'}, [
        c((3, 0, 4), (13, 1.6, 12), 'p'), c((4, 0, 3), (12, 1.6, 13), 'p'), c((5, 1.6, 5), (11, 2.1, 11), 'p'), c((7, 0, 13), (9, 1.1, 15.5), 'q')])
    R.HATS['boombox3d'] = ({'b': 'minecraft:block/black_concrete', 's': 'bm:block/boom_speaker', 'c': 'minecraft:block/light_gray_concrete', 'h': 'minecraft:block/iron_block',
                            'r': 'minecraft:block/red_concrete'}, [
        c((1, 0, 5), (15, 8, 11), 'b'), c((2, 1.5, 4.8), (6.5, 6, 5), 's'), c((9.5, 1.5, 4.8), (14, 6, 5), 's'), c((6.8, 2, 4.8), (9.2, 5, 5), 'c'),
        c((7, 6.2, 4.8), (9, 7.2, 5), 'r'), c((2, 8, 7.5), (3, 10.5, 8.5), 'h'), c((13, 8, 7.5), (14, 10.5, 8.5), 'h'), c((2, 10, 7.5), (14, 11, 8.5), 'h'),
        c((13.5, 8, 9.2), (14, 15, 9.7), 'h')])
    R.HATS['banquet3d'] = ({'w': 'minecraft:block/white_concrete', 'r': 'bm:block/roast', 'b': 'minecraft:block/bone_block_side', 'v': 'minecraft:block/lime_concrete',
                            'o': 'minecraft:block/orange_concrete', 'g': 'minecraft:block/gold_block'}, [
        c((0.5, 0, 0.5), (15.5, 0.8, 15.5), 'g'), c((1.5, 0.8, 1.5), (14.5, 1.2, 14.5), 'w'), c((4, 1.2, 4.5), (12, 5.5, 11), 'r'), c((5, 5.5, 5.5), (11, 6.5, 10), 'r'),
        c((2.5, 3, 7.2), (4, 4.2, 8.4), 'b'), c((12, 3, 7.2), (13.5, 4.2, 8.4), 'b'), c((2, 1.2, 2), (4.5, 3, 4), 'r'), c((11.5, 1.2, 12), (14, 3, 14), 'r'),
        c((12, 1.2, 2), (13.5, 2.2, 3.5), 'v'), c((2.5, 1.2, 12), (4, 2.2, 13.5), 'o'), c((6, 1.2, 12), (7.5, 2.2, 13.5), 'v'), c((9, 1.2, 2), (10.5, 2.2, 3.5), 'o')])
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('cec_', 'lava3d_', 'lavablob_', 'trash3d', 'whoopee3d', 'boombox3d', 'banquet3d')
    # icons
    grid = R.grid
    I = {}
    I['staff_of_sparks'] = grid(['............YW..', '...........YWWY.', '............YY..', '...........CK....', '..........CK.....', '.........CK......', '........CK.......',
                                 '.......CK........', '......CK.........', '.....CK..........', '....CK...........', '...CK............', '..CK.............', '.CK..............',
                                 '................', '................'], dict(Y='#7ad8ff', W='#ffffff', C='#c87a4a', K='#7a4a2a'))
    I['gravewell_staff'] = grid(['..........PPPP..', '.........PKKKKP.', '.........PKVVKP.', '.........PKVVKP.', '..........PKKP..', '.........SS.....', '........SK......',
                                 '.......SK.......', '......SK........', '.....SK.........', '....SK..........', '...SK...........', '..SK............', '.SK.............',
                                 '................', '................'], dict(P='#b48cff', K='#0a0410', V='#3a1a5a', S='#6a6a7a', ))
    I['crescent_staff'] = grid(['...........P....', '..........PPP...', '.......G..PLP.G.', '......GG..PPP.GG', '......G...GGG..G', '......GG.GGGGGGG', '.......GGGG.....',
                                '........WG......', '.......WD.......', '......WD........', '.....WD.........', '....WD..........', '...WD...........', '..WD............',
                                '.WD.............', '................'], dict(P='#e85aa8', L='#ffb0dc', G='#c9a74a', W='#6a3e2e', D='#3a2018'))
    I['ocarina'] = grid(['................', '................', '.....BBBBB......', '....BLLLLLB.....', '...BLLKLLKLB....', '..BLLLLLLLLLB...', '..BLKLLLLLKLBBB.',
                         '..BLLLLKLLLLLLB.', '...BLLLLLLLLBB..', '....BBBBBBBB....', '................', '................', '................', '................',
                         '................', '................'], dict(B='#2a4a8a', L='#6ab0ff', K='#1a2a4a'))
    I['tidal_tear'] = grid(['................', '.....D....D.....', '....DLD...DLD...', '....DLD...DWD...', '...DLLD...DLLD..', '...DLD.....DLD..', '..DLLD.....DLLD.',
                            '..DWLD.MMM..DLD.', '.DLLD.MPpPM.DLLD', '.DLLD..MPM..DLLD', '.DWLD...M..DLLD.', '.DLLLD...DDLLLD.', '.DLLLLDDDLLLLLD.', '..DLLLLLLLLSSD..',
                            '...DDLLLLSSDD...', '.....DDDDDD.....'], dict(D='#2e6e8c', L='#a8dcea', W='#f0fcff', S='#7cc0d8', M='#7a1a6a', P='#c02aa8', p='#ff8ae8'))
    I['bloomheart_gem'] = bloom_icon()
    bowl = lambda soup, top: grid(['................', '................', '................', '................', '.....TTTTTT.....', '...TSSTSSSTST...', '..KSSSSSSSSSSK..',
                                   '..KSSSTSSSSSSK..', '...KBBBBBBBBK...', '...KBBBBBBBBK...', '....KBBBBBBK....', '.....KKKKKK.....', '................', '................',
                                   '................', '................'], dict(T=top, S=soup, B='#8a5a3a', K='#4a2a1a'))
    I['dish_chili'] = bowl('#c83a1a', '#ff8a2a')
    I['dish_chowder'] = bowl('#e8e0c8', '#3ad8d0')
    I['dish_kebab'] = grid(['................', '.............SS.', '............SS..', '..........MMS...', '.........MMMM...', '........VMMV....', '.......MMMM.....', '......MMMV......',
                            '.....VMMM.......', '....MMMM........', '...SMM..........', '..SS............', '.SS.............', '................', '................',
                            '................'], dict(S='#c8b89a', M='#8a5a3a', V='#9ab0ff'))
    I['dish_potpie'] = grid(['................', '................', '................', '.....CCCCCC.....', '...CCcCCCcCCC...', '..CCCCCVCCCCCC..', '..CcCCCCCCCcCC..', '..KTTTTTTTTTTK..',
                             '...KTTTTTTTTK...', '....KKKKKKKK....', '................', '................', '................', '................', '................',
                             '................'], dict(C='#e8b86a', c='#c88a3a', V='#7dff6a', T='#b8b8c8', K='#6a6a7a'))
    I['dish_roast'] = grid(['................', '................', '.....RRRRR......', '...RRrRRRrRR....', '..RRRRRRRRRRR...', '.BRRrRRRRRrRRB..', 'BB.RRRRRRRRR.BB.', '....RRRRRRR.....',
                            '..WWWWWWWWWWWW..', '...WWWWWWWWWW...', '................', '................', '................', '................', '................',
                            '................'], dict(R='#a85a2a', r='#e8a05a', B='#f0e8d0', W='#d8d8d8'))
    I['dish_drumsticks'] = grid(['................', '..........BB....', '.........BBB....', '........BB......', '.....MMMB.......', '....MMMMM.......', '...MMmMMM.......', '...MMMMM...BB...',
                                 '...MMMM...BBB...', '....MM...BB.....', '......MMMB......', '.....MMMMM......', '.....MmMMM......', '.....MMMM.......', '......MM........',
                                 '................'], dict(M='#e8b86a', m='#fff2c8', B='#f0e8d0'))
    for k, v in I.items(): R.ICONS[k] = v
    R.HANDHELD_EXTRA = getattr(R, 'HANDHELD_EXTRA', set()) | {'staff_of_sparks', 'gravewell_staff', 'crescent_staff'}
    # the Vorn on foot: two walking poses each (the item definitions pick them from custom_model_data strings)
    import phase25 as R25
    vt = {'f': 'bm:block/vorn_skin', 'm': 'bm:block/vorn_dark', 'e': 'bm:block/vorn_dark', 'k': 'bm:block/vorn_eye', 't': 'bm:block/vorn_dark',
          's': 'bm:block/vorn_armor', 'p': 'bm:block/vorn_armor', 'g': 'minecraft:block/verdant_froglight_side', 'r': 'minecraft:block/iron_block'}
    vtr = dict(vt, s='bm:block/vorn_armor_red', p='bm:block/vorn_armor_red')
    ant = [c((6.1, 19, 7.6), (6.7, 23, 8.2), 'm'), c((5.8, 23, 7.3), (7.0, 24.2, 8.5), 'g'),
           c((9.3, 19, 7.6), (9.9, 23, 8.2), 'm'), c((9.0, 23, 7.3), (10.2, 24.2, 8.5), 'g')]
    rifle = [c((11.6, 6.2, 1.5), (12.8, 7.4, 9.0), 'r'), c((11.5, 6.0, 0.4), (12.9, 7.6, 1.6), 'g'), c((11.7, 4.4, 6.5), (12.7, 6.2, 7.5), 'm')]
    hammer = [c((11.8, 2.0, 7.9), (12.6, 12.0, 8.7), 'm'), c((10.2, 11.5, 6.3), (14.2, 14.5, 10.3), 'r'), c((10.0, 12.3, 6.1), (14.4, 13.7, 10.5), 'g')]
    shR = (12.2, 11.6, 8.4)
    for pose, a in (('walk1', 22.5), ('walk2', -22.5)):
        P = R25.donado_pose(pose, parts=True)
        body = [e for n in ('legL', 'legR', 'torso', 'armL', 'armR', 'head', 'eyes', 'tail') for e in P[n]]
        antm = [R25._mv(e, dy=0.2) for e in ant]
        wep = lambda ws: [R25._mv(R25._rot(e, 'x', a, shR), dy=0.2) for e in ws]
        R.HATS[f'vornp_{pose}'] = (vt, body + antm + wep(rifle))
        R.HATS[f'vornwp_{pose}'] = (vtr, body + antm + wep(hammer))
    R.DISPLAY_3D_EXTRA = R.DISPLAY_3D_EXTRA + ('vornp_', 'vornwp_')
    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        for item_id, pre in (('vorn3d', 'vornp'), ('vorn3d_warlord', 'vornwp')):
            R2.wj(f'assets/bm/items/{item_id}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                              'cases': [{'when': pz, 'model': mdl(f'{pre}_{pz}')} for pz in ('walk1', 'walk2')],
                                                              'fallback': mdl(item_id)}})
    R.POST.append(post)


def bloom_icon():
    """The Bloomheart: the flower gem from Cecil's art, 32 x 32."""
    import numpy as np
    from PIL import Image
    im = Image.open('/home/claude/bm_build/vendor/gem_bloom_ref.png').convert('RGBA'); a = np.asarray(im)
    ys, xs = np.where(a[..., 3] > 40)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)); w, h = im.size; s = max(w, h)
    sq = Image.new('RGBA', (s, s)); sq.paste(im, ((s - w) // 2, (s - h) // 2))
    out = Image.new('RGBA', (32, 32)); out.paste(sq.resize((30, 30), Image.LANCZOS), (1, 1))
    b = np.asarray(out).copy(); b[..., 3] = np.where(b[..., 3] > 110, 255, 0)
    return Image.fromarray(b)

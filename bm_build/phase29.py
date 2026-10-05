"""Phase 1.18 (part 2): the new one-of-a-kind goods - sold at the Dark Auction (phase30), in the back rooms (phase28)
and by the Concierge (phase31). None of them reuse an existing armour set, weapon or tool.

Right-click goods are carrot-on-a-stick based (the click the grappling hook already uses), so their data stays in
the hand while they work:
- RING OF THREE BURROWS: three homes, any dimension. Right-click: a menu to set a burrow where you stand or travel to
  one (3 seconds standing still; moving or getting hurt cancels; 2-minute recharge; never in dungeons or the Hollow).
- POCKET RIFT: three charges; right-click to raise a lit End portal (frame, eyes and all) 3 blocks ahead. Sneak +
  right-click next to one you made to fold it back up (the charge returns); sneak + right-click elsewhere with 4 Eyes
  of Ender in your inventory to add a charge.
- SMUGGLER'S JAR: right-click a creature 3-8 blocks away to bottle it with ALL its data (name, health, gear, owner,
  trades, effects, age); right-click a block to let it out there. Only its position changes.
- SPAWNER CROWBAR (3 uses) pries a monster spawner loose into a CAGED SPAWNER you can set down anywhere.
- LODESTONE LOCKET: right-click to switch on; pulls dropped items and XP within 7 blocks to you.
- BANKER'S CARD opens the Rat Bank anywhere. FAIR WEATHER BELL clears rain and storms (once a day).
- MERCENARY CONTRACT: hire Rufus Gnaw, rat for hire - crossbow at range, blade up close; orders: follow, guard a
  spot, scavenge loot. Paid 1 Token a day from his purse; ranks up with service; patched up if he falls.
Consumed/placed goods: Donado Trophy and the GOLDEN DONADO (crops within 8 blocks grow a stage a minute, baby animals
grow up faster), Sealed Explorer's Map, Rat Gang Portrait (a painting), Wings of the Rat King (unbreakable, +6 armour,
Regeneration while gliding), Rat King's Signet (+2 Luck, Standing x1.25).
Very rare cosmetics: Auroral Crown, Brass Wing Scroll (elytra reskin), Rat Familiar (a rat on your shoulder),
Bloomwalker Boots (flowers bloom in your footsteps), Showstopper Charm (gold confetti on every kill), Market Crest
Scroll (the market's crest on your shield).
Importing registers the items; generate(G) runs after phase28.generate."""
from nbt import snbt, B, F, D as Dd, Int
from items import item, consumable, attr, T, TOTEM, ITEMS, ITEM_VERSION, DYNAMIC
import json

COAS = 'minecraft:carrot_on_a_stick'
UNBR = {'minecraft:unbreakable': {}, 'minecraft:tooltip_display': {'hidden_components': ['minecraft:unbreakable']}}


def coas(iid, name, color, lore, model, cat='relic', bold=False, extra=None, dynamic=False):
    item(iid, COAS, name, color, lore + [('Hold it and right-click.', 'dark_gray')], model=model, stack=1, comps=dict(UNBR),
         custom_extra=extra, cat=cat, bold=bold)
    if dynamic: DYNAMIC.add(iid)


def _use(sound, secs=0.6, anim='none'):
    return {'minecraft:consumable': consumable(secs, anim, sound, False)}


# ===================================================================== ITEMS
coas('ring_burrows', 'Ring of Three Burrows', '#d4a35a',
     ['A brass ring with three tiny doors.', ('Set up to three burrows - any dimension -', 'blue'), ('and slip home to any of them.', 'blue'),
      ('3 seconds standing still; 2-minute recharge.', 'gray'), ("Won't open in dungeons or the Hollow.", 'dark_gray')], 'bm:ring_burrows', bold=True)
coas('pocket_rift', 'Pocket Rift', '#4fd6c4',
     ['A folded tear in the world.', ('Right-click: raise a lit End portal', 'blue'), ('3 blocks ahead (needs a clear 5x5 space).', 'blue'),
      ('Sneak by one you made: fold it back up.', 'gray'), ('Sneak elsewhere with 4 Eyes of Ender: +1 charge.', 'gray')],
     'bm:pocket_rift', bold=True, extra={'charges': Int(3)}, dynamic=True)
coas('smuggler_jar', "Smuggler's Jar", '#9fd1b0',
     ['Any creature fits if you ask nicely.', ('Right-click a creature 3-8 blocks away to bottle it,', 'blue'),
      ('right-click a block to let it out.', 'blue'), ('Everything about it comes along: name, gear, owner, trades.', 'gray'),
      ('(Step back from villagers and horses, or they just talk to you.)', 'dark_gray')], 'bm:smuggler_jar', dynamic=True)
coas('spawner_crowbar', 'Spawner Crowbar', '#8a8a96',
     ['Pries a monster spawner loose, mob and all.', ('Right-click a spawner within 5 blocks.', 'blue'), ('3 uses.', 'gray')],
     'bm:spawner_crowbar', extra={'uses': Int(3)}, dynamic=True)
coas('caged_spawner', 'Caged Spawner', '#7a6a9a',
     ['A monster spawner in a travelling cage.', ('Right-click a block to set it down there.', 'blue')], 'bm:caged_spawner', dynamic=True)
coas('lodestone_locket', 'Lodestone Locket', '#b0a0d0',
     ['A locket with a lodestone chip inside.', ('Right-click to switch it on or off.', 'blue'), ('While on, dropped items and XP within', 'blue'),
      ('7 blocks drift to you.', 'blue')], 'bm:lodestone_locket')
coas('bankers_card', "Banker's Card", '#e8d27a',
     ['Engraved: "The Rat Bank honours the bearer."', ('Right-click: open your Rat Bank account', 'blue'), ('from anywhere.', 'blue')], 'bm:bankers_card')
coas('fair_weather_bell', 'Fair Weather Bell', '#ffe08a',
     ['Ring it and the clouds remember an errand.', ('Right-click: clears rain and storms', 'blue'), ('for a day.', 'blue'), ('Once per day.', 'gray')],
     'bm:fair_weather_bell')
coas('merc_contract', 'Mercenary Contract', '#c0392b',
     ['Signed: Rufus Gnaw, Rat for Hire.', ('Right-click: give him orders.', 'blue'), ('Crossbow at range, blade up close.', 'gray'),
      ('Wages: 1 Token a day, from his purse.', 'gray')], 'bm:merc_contract', bold=True)
item('donado_trophy', TOTEM, 'Donado Trophy', '#e8d29a',
     ['A statue of the bravest Earth-dog.', ('Use it to set it down. Right-click it to turn it;', 'gray'), ('sneak + punch it to pick it up.', 'gray')],
     model='bm:statue_donado', stack=16, cat='relic', comps=_use('minecraft:block.stone.place'))
item('golden_donado', TOTEM, 'Golden Donado', '#ffd700',
     ['Solid gold, and very good with plants.', ('Crops within 8 blocks grow a stage every minute;', 'blue'), ('baby animals near it grow up faster.', 'blue'),
      ('Use it to set it down. Sneak + punch to pick it up.', 'gray')],
     model='bm:statue_donado_gold', stack=1, cat='relic', bold=True, comps=_use('minecraft:block.metal.place'))
item('sealed_explorer_map', TOTEM, "Sealed Explorer's Map", 'aqua',
     ['Hold right-click to break the seal.', 'Marks a Trial Chamber or a', 'Woodland Mansion.'],
     model='minecraft:map', glint=True, stack=16, cat='map', comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:item.book.page_turn', False)})
item('rat_gang_portrait', 'minecraft:painting', 'Rat Gang Portrait', '#c8a050',
     ['The whole crew, in oils.', ('A 2x2 painting.', 'gray')], stack=16, cat='relic', comps={'minecraft:painting/variant': 'bm:rat_gang'})
item('wings_rat_king', 'minecraft:elytra', 'Wings of the Rat King', '#ffb300',
     ['Black velvet and smuggled gold.', ('Unbreakable. +6 Armor, +3 Toughness.', 'blue'), ('Regeneration while gliding.', 'blue'),
      ('Trails gold dust and crowns.', 'dark_aqua')],
     model='bm:wings_rat_king', bold=True, cat='relic',
     comps={'minecraft:unbreakable': {},
            'minecraft:equippable': {'slot': 'chest', 'asset_id': 'bm:wings_rat_king', 'equip_sound': 'minecraft:item.armor.equip_elytra', 'damage_on_hurt': False},
            'minecraft:attribute_modifiers': [attr('armor', 6, 'chest'), attr('armor_toughness', 3, 'chest'), attr('knockback_resistance', 0.1, 'chest')]})
item('rat_king_signet', TOTEM, "Rat King's Signet", '#ffb300',
     ['The seal on every deal that matters.', ('+2 Luck in your off hand.', 'blue'), ('Standing earned x1.25 while you carry it.', 'blue')],
     model='bm:rat_king_signet', glint=True, stack=1, bold=True, cat='relic',
     comps={'minecraft:attribute_modifiers': [attr('luck', 2, 'offhand')]})
# ---- very rare cosmetics (original designs)
item('auroral_crown', TOTEM, 'Auroral Crown', '#7fffd4',
     ['A thin band that hums with northern lights.', ('Cosmetic - wear on your head', 'dark_aqua')],
     model='bm:auroral_crown', stack=1, bold=True, cat='cosmetic', comps={'minecraft:equippable': {'slot': 'head', 'swappable': True}})
item('brass_wing_scroll', TOTEM, 'Brass Wing Scroll', '#c8963c',
     ['Put a plain elytra in your OFF hand,', 'then use this scroll in your main hand:', ('the wings become clockwork brass.', 'blue'),
      ('A Skin Scroll: Restore undoes it.', 'gray')],
     model='bm:brass_wing_scroll', stack=16, cat='cosmetic', comps=_use('minecraft:block.enchantment_table.use', 0.8))
item('market_crest_scroll', TOTEM, 'Market Crest Scroll', '#ffcf3f',
     ['Put a shield in your OFF hand,', 'then use this scroll in your main hand:', ("it bears the Black Market's crest.", 'blue')],
     model='bm:market_crest_scroll', stack=16, cat='cosmetic', comps=_use('minecraft:block.enchantment_table.use', 0.8))
item('rat_familiar', TOTEM, 'Rat Familiar', '#b0b0b8',
     ['A very small, very loyal rat.', ('Keep it in your inventory: it rides', 'blue'), ('on your shoulder.', 'blue'), ('Cosmetic.', 'dark_aqua')],
     model='bm:rat_familiar', stack=1, cat='cosmetic')
item('bloomwalker_boots', 'minecraft:leather_boots', 'Bloomwalker Boots', '#7ccf5a',
     ['Grass remembers where you walked.', ('Flowers bloom in your footsteps.', 'dark_aqua'), ('Cosmetic.', 'dark_aqua')],
     stack=1, cat='cosmetic', comps={'minecraft:dyed_color': 0x5FA83A, 'minecraft:unbreakable': {}})
item('showstopper_charm', TOTEM, 'Showstopper Charm', '#ffd700',
     ['Every exit deserves applause.', ('Keep it in your inventory: every kill', 'blue'), ('ends in a burst of gold confetti.', 'blue'), ('Cosmetic.', 'dark_aqua')],
     model='bm:showstopper_charm', stack=1, cat='cosmetic')

JARABLE_EXCLUDE = {'ender_dragon', 'wither', 'warden', 'elder_guardian'}
JAR_TAGS_OFF = ['bm.npc', 'bm.boss', 'bm.monstrosity', 'bm.herald', 'bm.dgmob', 'bm.frogpet', 'bm.wilfrey', 'bm.wil_body', 'bm.donado',
                'bm.mercpet', 'bm.blood', 'bm.crypt_warden']
CROPS = {'wheat': 7, 'carrots': 7, 'potatoes': 7, 'beetroots': 3, 'nether_wart': 3, 'melon_stem': 7, 'pumpkin_stem': 7, 'sweet_berry_bush': 3}
FLOWERS = ['poppy', 'dandelion', 'cornflower', 'allium', 'azure_bluet', 'oxeye_daisy', 'pink_tulip', 'blue_orchid']
MERC_NAME = 'Rufus Gnaw'
RANKS = [(0, 'Recruit', 'gray', 30, 5), (7, 'Veteran', 'aqua', 40, 7), (28, 'Captain', 'gold', 50, 9)]   # (days, title, colour, hp, dmg)


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX, item_arg = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX, G.item_arg
    tick, fast, second, load = [], [], [], []
    ident = [F(0), F(0), F(0), F(1)]
    import phase28 as P28

    objs = ['bm.bcd dummy', 'bm.bwarm dummy', 'bm.bslot dummy', 'bm.bhurt minecraft.custom:minecraft.damage_taken', 'bm.magnet dummy',
            'bm.bellday dummy', 'bm.kills minecraft.custom:minecraft.mob_kills', 'bm.walk minecraft.custom:minecraft.walk_one_cm',
            'bm.mstate dummy', 'bm.mpurse dummy', 'bm.mdays dummy', 'bm.mmode dummy', 'bm.mgen dummy', 'bm.mday dummy', 'bm.dtimer dummy',
            'bm.ftimer dummy', 'bm.rcd2 dummy', 'bm.mshot dummy', 'bm.p29t dummy']
    load += [f'scoreboard objectives add {o}' for o in objs]
    G.P29_OBJ = [o.split()[0] for o in objs]
    wjson('bm/predicate/p29/raining.json', {'condition': 'minecraft:weather_check', 'raining': True})

    # right-click dispatch: carrot-on-a-stick clicks share the grappling hook's hook (main hand)
    disp = {'ring_burrows': 'p29/burrow/use', 'pocket_rift': 'p29/rift/use', 'smuggler_jar': 'p29/jar/use', 'spawner_crowbar': 'p29/crow/use',
            'caged_spawner': 'p29/cage/use', 'lodestone_locket': 'p29/locket/use', 'bankers_card': 'p31/bank/card',
            'fair_weather_bell': 'p29/bell/use', 'merc_contract': 'p29/merc/use'}
    gu = G.FUNCS['p21/grap/use']
    gu[1:1] = [f'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"{i}"}}] run return run function bm:{f}' for i, f in disp.items()]
    G.P29_CLICK = gu

    def deny(msg, color='gray'):
        return f'return run ' + title('@s', 'actionbar', T(msg, color))

    no_zone = lambda what: [f'execute if entity @s[tag=bm.adv] run {deny(what + " won" + chr(39) + "t work in here.")}',
                            f'execute if dimension bm:hollow_throne run {deny("What the Hollow takes, it keeps.")}']

    # ================================================================== RING OF THREE BURROWS
    fn('p29/burrow/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid'] + no_zone('The ring') + [
        f'scoreboard players set @s bm.menu {P28.MENU["burrow"]}', 'data remove storage bm:ui br',
        'execute store result storage bm:ui br.pid int 1 run scoreboard players get @s bm.pid',
        'function bm:p29/burrow/menu with storage bm:ui br'])
    menu = ['$data modify storage bm:ui br.s set from storage bm:burrow p$(pid)']
    for k in (1, 2, 3):
        menu += [f'data modify storage bm:ui br.t{k} set value "(empty)"',
                 f'execute if data storage bm:ui br.s.b{k} run function bm:p29/burrow/label{k} with storage bm:ui br.s.b{k}']
        fn(f'p29/burrow/label{k}', [f'$data modify storage bm:ui br.t{k} set value "$(dn)  $(bx), $(by), $(bz)"'])
    menu += ['execute store result storage bm:ui br.cd int 1 run scoreboard players get @s bm.bcd', 'function bm:p29/burrow/dlg with storage bm:ui br']
    fn('p29/burrow/menu', menu)
    dlg = P28.multi([T('Ring of Three Burrows', '#d4a35a', bold=True)],
                    [P28.body([T('Travel takes 3 seconds standing still. Moving or getting hurt cancels it.', 'gray')]),
                     P28.body([T('Recharge: ', 'dark_gray'), T('$(cd)', 'white'), T(' s', 'dark_gray')])],
                    [P28.btn([T('Go: ', 'gold'), T('$(t1)', 'white')], 6001, width=200), P28.btn([T('Set burrow 1 here', 'gray')], 6011, width=130),
                     P28.btn([T('Go: ', 'gold'), T('$(t2)', 'white')], 6002, width=200), P28.btn([T('Set burrow 2 here', 'gray')], 6012, width=130),
                     P28.btn([T('Go: ', 'gold'), T('$(t3)', 'white')], 6003, width=200), P28.btn([T('Set burrow 3 here', 'gray')], 6013, width=130)],
                    columns=2)
    fn('p29/burrow/dlg', [f'$dialog show @s {P28.inline(dlg)}'])
    act = G.FUNCS['p28/act']
    act.append('execute if score #act bm.pay matches 6001..6099 run return run function bm:p29/burrow/act')
    fn('p29/burrow/act', [f'execute unless score @s bm.menu matches {P28.MENU["burrow"]} run return run function bm:p28/stale',
                          'execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"ring_burrows"}] run ' + deny('Hold the ring.'),
                          'execute if score #act bm.pay matches 6011..6013 run return run function bm:p29/burrow/set',
                          'execute if score #act bm.pay matches 6001..6003 run return run function bm:p29/burrow/go'])
    dims = [('minecraft:overworld', 'Overworld'), ('minecraft:the_nether', 'Nether'), ('minecraft:the_end', 'End')]
    fn('p29/burrow/set', no_zone('The ring') + [
        'data remove storage bm:tmp b', 'data modify storage bm:tmp b.dn set value "Elsewhere"'] +
       [f'execute if dimension {d} run data modify storage bm:tmp b merge value {{dim:"{d}",dn:"{n}"}}' for d, n in dims] +
       ['execute unless data storage bm:tmp b.dim run ' + deny("The ring can't find this place again."),
        'execute store result storage bm:tmp b.x double 0.01 run data get entity @s Pos[0] 100',
        'execute store result storage bm:tmp b.y double 0.01 run data get entity @s Pos[1] 100',
        'execute store result storage bm:tmp b.z double 0.01 run data get entity @s Pos[2] 100',
        'execute store result storage bm:tmp b.bx int 1 run data get entity @s Pos[0]',
        'execute store result storage bm:tmp b.by int 1 run data get entity @s Pos[1]',
        'execute store result storage bm:tmp b.bz int 1 run data get entity @s Pos[2]',
        'execute store result storage bm:tmp b.pid int 1 run scoreboard players get @s bm.pid',
        'scoreboard players operation #k bm.pay = #act bm.pay', 'scoreboard players remove #k bm.pay 6010',
        'execute store result storage bm:tmp b.k int 1 run scoreboard players get #k bm.pay',
        'function bm:p29/burrow/save with storage bm:tmp b',
        'playsound minecraft:block.wooden_trapdoor.close player @s ~ ~ ~ 1 1.2', 'particle minecraft:happy_villager ~ ~0.5 ~ 0.4 0.2 0.4 0 10',
        title('@s', 'actionbar', [T('Burrow ', 'gold'), {'score': {'name': '#k', 'objective': 'bm.pay'}, 'color': 'white'}, T(' dug here.', 'gold')])])
    fn('p29/burrow/save', ['$data modify storage bm:burrow p$(pid).b$(k) set value {dim:"$(dim)",dn:"$(dn)",x:$(x)d,y:$(y)d,z:$(z)d,bx:$(bx),by:$(by),bz:$(bz)}'])
    fn('p29/burrow/go', no_zone('The ring') + [
        'execute if score @s bm.bcd matches 1.. run ' + deny('The ring is still warm. Give it a moment.'),
        'scoreboard players operation @s bm.bslot = #act bm.pay', 'scoreboard players remove @s bm.bslot 6000',
        'data remove storage bm:tmp b', 'execute store result storage bm:tmp b.pid int 1 run scoreboard players get @s bm.pid',
        'execute store result storage bm:tmp b.k int 1 run scoreboard players get @s bm.bslot',
        'function bm:p29/burrow/load with storage bm:tmp b',
        'execute unless data storage bm:tmp b.t run ' + deny('That burrow is empty. Set it first.'),
        'scoreboard players set @s bm.bwarm 60', 'scoreboard players set @s bm.bhurt 0', 'tag @s add bm.bwarming',
        'execute store result score @s bm.p29t run data get entity @s Pos[0] 10',
        'execute store result score #z bm.pay run data get entity @s Pos[2] 10', 'scoreboard players operation @s bm.p29t *= #100 bm.pay',
        'scoreboard players operation @s bm.p29t += #z bm.pay',
        'playsound minecraft:block.portal.trigger player @s ~ ~ ~ 0.3 1.8',
        title('@s', 'actionbar', T('The ring turns... stand still.', '#d4a35a'))])
    fn('p29/burrow/load', ['$data modify storage bm:tmp b.t set from storage bm:burrow p$(pid).b$(k)'])
    tick.append('execute as @a[tag=bm.bwarming] at @s run function bm:p29/burrow/warm')
    fn('p29/burrow/warm', [
        'execute store result score #x bm.pay run data get entity @s Pos[0] 10', 'execute store result score #z bm.pay run data get entity @s Pos[2] 10',
        'scoreboard players operation #x bm.pay *= #100 bm.pay', 'scoreboard players operation #x bm.pay += #z bm.pay',
        'execute unless score #x bm.pay = @s bm.p29t run return run function bm:p29/burrow/cancel',
        'execute if score @s bm.bhurt matches 1.. run return run function bm:p29/burrow/cancel',
        'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.05 4', 'scoreboard players remove @s bm.bwarm 1',
        'execute if score @s bm.bwarm matches ..0 run function bm:p29/burrow/jump'])
    fn('p29/burrow/cancel', ['tag @s remove bm.bwarming', 'scoreboard players set @s bm.bwarm 0', 'playsound minecraft:block.wooden_trapdoor.close player @s ~ ~ ~ 1 0.6',
                             title('@s', 'actionbar', T('The ring goes still. (You moved.)', 'gray'))])
    fn('p29/burrow/jump', [
        'tag @s remove bm.bwarming', 'scoreboard players set @s bm.bcd 120',
        'data remove storage bm:tmp b', 'execute store result storage bm:tmp b.pid int 1 run scoreboard players get @s bm.pid',
        'execute store result storage bm:tmp b.k int 1 run scoreboard players get @s bm.bslot', 'function bm:p29/burrow/load with storage bm:tmp b',
        # where we were, in case the burrow is now buried
        'data remove storage bm:tmp bo', 'data modify storage bm:tmp bo.dim set value "minecraft:overworld"'] +
        [f'execute if dimension {d} run data modify storage bm:tmp bo.dim set value "{d}"' for d, _ in dims] + [
        'execute store result storage bm:tmp bo.x double 0.01 run data get entity @s Pos[0] 100',
        'execute store result storage bm:tmp bo.y double 0.01 run data get entity @s Pos[1] 100',
        'execute store result storage bm:tmp bo.z double 0.01 run data get entity @s Pos[2] 100',
        'particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.05 40', 'playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 1 0.8',
        'function bm:p29/burrow/tp with storage bm:tmp b.t',
        'execute at @s unless block ~ ~ ~ #bm:p29_open run return run function bm:p29/burrow/blocked',
        'execute at @s unless block ~ ~1 ~ #bm:p29_open run return run function bm:p29/burrow/blocked',
        'effect give @s minecraft:resistance 3 4 true',
        'execute at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.05 40',
        'execute at @s run playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 1 1.1',
        title('@s', 'actionbar', T('Home, through a door the size of a rat.', '#d4a35a'))])
    fn('p29/burrow/tp', ['$execute in $(dim) run tp @s $(x) $(y) $(z)'])
    fn('p29/burrow/blocked', ['function bm:p29/burrow/tp with storage bm:tmp bo', 'scoreboard players set @s bm.bcd 0',
                              title('@s', 'actionbar', T("Something's been built over that burrow. Dig it again somewhere clear.", 'red'))])
    wjson('bm/tags/block/p29_open.json', {'values': ['#minecraft:air', 'minecraft:light', 'minecraft:short_grass', 'minecraft:tall_grass', 'minecraft:fern',
                                                     'minecraft:large_fern', 'minecraft:snow', 'minecraft:water', '#minecraft:small_flowers',
                                                     'minecraft:dead_bush', '#minecraft:wool_carpets', 'minecraft:moss_carpet', '#minecraft:buttons',
                                                     '#minecraft:pressure_plates', 'minecraft:torch', 'minecraft:wall_torch', 'minecraft:lever']})
    second += ['scoreboard players remove @a[scores={bm.bcd=1..}] bm.bcd 1']

    # ================================================================== POCKET RIFT
    rift_lore = list(ITEMS['pocket_rift']['comps']['minecraft:lore'])
    def lore_with(line_comp):
        return snbt(rift_lore[:-1] + [line_comp] + rift_lore[-1:])
    fn('p29/rift/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid'] + no_zone('The rift') + [
        'execute if score @s bm.rcd2 matches 1.. run return 0', 'scoreboard players set @s bm.rcd2 10',
        'execute store result score #c bm.pay run data get entity @s SelectedItem.components."minecraft:custom_data".charges',
        'execute if predicate bm:p20/sneaking if entity @e[type=minecraft:marker,tag=bm.rift,distance=..6] run return run function bm:p29/rift/fold',
        'execute if predicate bm:p20/sneaking run return run function bm:p29/rift/recharge',
        'execute if score #c bm.pay matches ..0 run ' + deny('No charges left. Sneak + right-click with 4 Eyes of Ender to add one.'),
        'execute if entity @e[type=minecraft:marker,tag=bm.rift,distance=..8] run ' + deny('Too close to another rift.'),
        'scoreboard players set #placed bm.pay 0',
        'execute if entity @s[y_rotation=-45..45] align xyz positioned ~0.5 ~ ~3.5 run function bm:p29/rift/place',
        'execute if entity @s[y_rotation=45..135] align xyz positioned ~-2.5 ~ ~0.5 run function bm:p29/rift/place',
        'execute if entity @s[y_rotation=135..180] align xyz positioned ~0.5 ~ ~-2.5 run function bm:p29/rift/place',
        'execute if entity @s[y_rotation=-180..-135] align xyz positioned ~0.5 ~ ~-2.5 run function bm:p29/rift/place',
        'execute if entity @s[y_rotation=-135..-45] align xyz positioned ~3.5 ~ ~0.5 run function bm:p29/rift/place',
        'execute if score #placed bm.pay matches 0 run ' + deny('The rift needs a clear 5x5 space at your feet, 3 blocks ahead.'),
        'scoreboard players remove #c bm.pay 1', 'function bm:p29/rift/set_charges'])
    ring = [(dx, dz) for dx in range(-2, 3) for dz in range(-2, 3) if abs(dx) == 2 or abs(dz) == 2]
    ring = [(dx, dz) for dx, dz in ring if not (abs(dx) == 2 and abs(dz) == 2)]
    inner = [(dx, dz) for dx in range(-1, 2) for dz in range(-1, 2)]
    face = lambda dx, dz: 'south' if dz == -2 else 'north' if dz == 2 else 'east' if dx == -2 else 'west'
    wjson('bm/tags/entity_type/p29_rift_free.json', {'values': ['minecraft:marker', 'minecraft:item_display', 'minecraft:block_display',
                                                                 'minecraft:text_display', 'minecraft:interaction', 'minecraft:area_effect_cloud']})
    wjson('bm/tags/block/p29_rift_ok.json', {'values': ['#minecraft:air', 'minecraft:short_grass', 'minecraft:tall_grass', 'minecraft:fern', 'minecraft:large_fern',
                                                        'minecraft:snow', 'minecraft:dead_bush', '#minecraft:small_flowers', 'minecraft:light']})
    fn('p29/rift/place', [f'execute unless block ~{dx} ~ ~{dz} #bm:p29_rift_ok run return 0' for dx, dz in ring + inner] +
       ['execute positioned ~-2.5 ~ ~-2.5 if entity @e[type=!#bm:p29_rift_free,dx=4,dy=1,dz=4] run return 0'] +
       [f'setblock ~{dx} ~ ~{dz} minecraft:end_portal_frame[eye=true,facing={face(dx, dz)}]' for dx, dz in ring] +
       [f'setblock ~{dx} ~ ~{dz} minecraft:end_portal' for dx, dz in inner] +
       ['summon minecraft:marker ~ ~ ~ {Tags:["bm.rift","bm.rnew"]}',
        'scoreboard players operation @e[type=minecraft:marker,tag=bm.rnew,distance=..1] bm.pid = @s bm.pid', 'tag @e[type=minecraft:marker,tag=bm.rnew] remove bm.rnew',
        'scoreboard players set #placed bm.pay 1',
        'playsound minecraft:block.end_portal.spawn block @a[distance=..32] ~ ~ ~ 0.8 1.2', 'particle minecraft:reverse_portal ~ ~0.5 ~ 1.5 0.3 1.5 0.1 80',
        title('@s', 'actionbar', T('The rift unfolds. Mind your step.', '#4fd6c4'))])
    fn('p29/rift/fold', ['scoreboard players set #folded bm.pay 0', 'tag @s add bm.rme',
                         'execute as @e[type=minecraft:marker,tag=bm.rift,distance=..6,sort=nearest,limit=1] if score @s bm.pid = @a[tag=bm.rme,limit=1] bm.pid at @s run function bm:p29/rift/unmake',
                         'tag @s remove bm.rme',
                         'execute if score #folded bm.pay matches 1 if score #c bm.pay matches ..2 run scoreboard players add #c bm.pay 1',
                         'execute if score #folded bm.pay matches 1 run function bm:p29/rift/set_charges',
                         'execute if score #folded bm.pay matches 0 run ' + title('@s', 'actionbar', T("That rift isn't yours to fold.", 'gray'))])
    fn('p29/rift/unmake', [f'fill ~{dx} ~ ~{dz} ~{dx} ~ ~{dz} minecraft:air replace minecraft:end_portal_frame' for dx, dz in ring] +
       [f'fill ~{dx} ~ ~{dz} ~{dx} ~ ~{dz} minecraft:air replace minecraft:end_portal' for dx, dz in inner] +
       ['scoreboard players set #folded bm.pay 1', 'playsound minecraft:block.end_portal_frame.fill block @a[distance=..16] ~ ~ ~ 1 0.6',
        'particle minecraft:reverse_portal ~ ~0.5 ~ 1.5 0.3 1.5 0.1 60', 'kill @s'])
    fn('p29/rift/recharge', ['execute if score #c bm.pay matches 3.. run ' + deny('The rift is full (3 charges).'),
                             'execute store result score #e bm.pay run clear @s minecraft:ender_eye 0',
                             'execute if score #e bm.pay matches ..3 run ' + deny('Recharging takes 4 Eyes of Ender.'),
                             'clear @s minecraft:ender_eye 4', 'scoreboard players add #c bm.pay 1', 'function bm:p29/rift/set_charges',
                             'playsound minecraft:block.end_portal_frame.fill player @s ~ ~ ~ 1 1.2'])
    fn('p29/rift/set_charges', ['execute store result storage bm:tmp rc.c int 1 run scoreboard players get #c bm.pay',
                                'function bm:p29/rift/set_m with storage bm:tmp rc',
                                title('@s', 'actionbar', [T('Pocket Rift: ', '#4fd6c4'), {'score': {'name': '#c', 'objective': 'bm.pay'}, 'color': 'white'}, T('/3 charges', 'gray')])])
    fn('p29/rift/set_m', ['$item modify entity @s weapon.mainhand {function:"minecraft:sequence",functions:[{function:"minecraft:set_custom_data",tag:{charges:$(c)}},'
                          '{function:"minecraft:set_lore",mode:"replace_all",lore:' + lore_with(T('Charges: $(c)/3', 'aqua')) + '}]}'])
    second.append('scoreboard players remove @a[scores={bm.rcd2=1..}] bm.rcd2 1')
    tick.append('scoreboard players remove @a[scores={bm.rcd2=1..}] bm.rcd2 1')

    # ================================================================== SMUGGLER'S JAR
    from paths import MC as _MC; REG = json.load(open(_MC + 'registries.json'))
    jarable = sorted(i[:-10] for i in REG['item'] if i.endswith('_spawn_egg') and i[:-10] not in JARABLE_EXCLUDE)
    wjson('bm/tags/entity_type/p29_jarable.json', {'values': [f'minecraft:{t}' for t in jarable]})
    off = ','.join(f'tag=!{t}' for t in JAR_TAGS_OFF)
    jar_empty = {'minecraft:custom_data': {'bm': 'smuggler_jar', 'bmv': ITEM_VERSION}, 'minecraft:item_model': 'bm:smuggler_jar',
                 'minecraft:lore': ITEMS['smuggler_jar']['comps']['minecraft:lore']}
    fn('p29/jar/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid'] + no_zone('The jar') + [
        'execute if score @s bm.rcd2 matches 1.. run return 0', 'scoreboard players set @s bm.rcd2 10',
        'execute if data entity @s SelectedItem.components."minecraft:custom_data".jar run return run function bm:p29/jar/release',
        'scoreboard players set #ray bm.pay 32', 'tag @s add bm.jarrer', 'scoreboard players set #got bm.pay 0',
        'execute anchored eyes positioned ^ ^ ^0.5 run function bm:p29/jar/ray', 'tag @s remove bm.jarrer',
        'execute if score #got bm.pay matches 0 run ' + deny('Nothing to bottle there. Aim at a creature 3-8 blocks away.')])
    fn('p29/jar/ray', ['execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                       f'execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[dx=0,dy=0,dz=0,type=#bm:p29_jarable,{off},limit=1] positioned ~0.5 ~0.5 ~0.5 run return run function bm:p29/jar/catch',
                       f'execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[dx=0,dy=0,dz=0,type=!#bm:ray_ignore,type=!minecraft:player] run return run ' + title('@a[tag=bm.jarrer]', 'actionbar', T("That one won't fit in a jar.", 'gray')),
                       'scoreboard players remove #ray bm.pay 1',
                       'execute if score #ray bm.pay matches 1.. positioned ^ ^ ^0.25 run function bm:p29/jar/ray'])
    ids = [f'execute if entity @s[type=minecraft:{t}] run data modify storage bm:jar cap merge value {{eid:"minecraft:{t}",name:{{translate:"entity.minecraft.{t}"}}}}' for t in jarable]
    fn('p29/jar/owner', ['scoreboard players set #notmine bm.pay 0', 'data modify storage bm:jar own set from entity @s Owner',
                         'execute store success score #notmine bm.pay run data modify storage bm:jar own set from entity @a[tag=bm.jarrer,limit=1] UUID'])
    fn('p29/jar/catch', ['scoreboard players set #got bm.pay 1', 'scoreboard players set #notmine bm.pay 0',
                         'execute if data entity @s Owner run function bm:p29/jar/owner',
                         'execute if score #notmine bm.pay matches 1 run return run ' + title('@a[tag=bm.jarrer]', 'actionbar', T("That's somebody else's pet. Hands off.", 'gray')),
                         'data remove storage bm:jar cap'] + ids + [
        'data modify storage bm:jar cap.data set from entity @s',
        'execute if data entity @s CustomName run data modify storage bm:jar cap.name set from entity @s CustomName',
        'data remove storage bm:jar cap.data.Pos', 'data remove storage bm:jar cap.data.Motion', 'data remove storage bm:jar cap.data.leash',
        'data remove storage bm:jar cap.data.FallDistance', 'data remove storage bm:jar cap.data.fall_distance', 'data remove storage bm:jar cap.data.OnGround',
        'data remove storage bm:jar cap.data.PortalCooldown', 'data remove storage bm:jar cap.data.Passengers',
        'particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.02 15', 'playsound minecraft:item.bottle.fill_dragonbreath neutral @a[distance=..16] ~ ~ ~ 1 0.8',
        # gone without a death: no owner (no "X died" message), no drops in sight (the void eats them), silent
        'data remove entity @s Owner', 'data modify entity @s Silent set value 1b', 'tp @s ~ ~-2000 ~', 'kill @s',
        'execute as @a[tag=bm.jarrer,limit=1] run function bm:p29/jar/fill'])
    fn('p29/jar/fill', ['item modify entity @s weapon.mainhand bm:p29/jar_fill',
                        title('@s', 'actionbar', [T('Bottled: ', '#9fd1b0'), {'nbt': 'cap.name', 'storage': 'bm:jar', 'interpret': True, 'color': 'white'}])])
    wjson('bm/item_modifier/p29/jar_fill.json', [
        {'function': 'minecraft:copy_custom_data', 'source': {'type': 'minecraft:storage', 'source': 'bm:jar'}, 'ops': [{'source': 'cap', 'target': 'jar', 'op': 'replace'}]},
        {'function': 'minecraft:set_components', 'components': {'minecraft:item_model': 'bm:smuggler_jar_full', 'minecraft:enchantment_glint_override': True}},
        {'function': 'minecraft:set_lore', 'entity': 'this', 'mode': 'replace_all', 'lore': [
            [T('Holding: ', 'gray'), {'nbt': 'cap.name', 'storage': 'bm:jar', 'interpret': True, 'color': 'gold', 'italic': False}],
            T('Right-click a block to let it out.', 'blue'), T('Black Market goods — no refunds, no questions', 'dark_gray', italic=True)]}])
    wjson('bm/item_modifier/p29/jar_empty.json', {'function': 'minecraft:set_components', 'components': dict(jar_empty, **{'!minecraft:enchantment_glint_override': {}})})
    fn('p29/jar/release', ['scoreboard players set #ray bm.pay 32', 'scoreboard players set #got bm.pay 0', 'tag @s add bm.jarrer',
                           'data remove storage bm:jar rel', 'data modify storage bm:jar rel set from entity @s SelectedItem.components."minecraft:custom_data".jar',
                           'execute anchored eyes positioned ^ ^ ^0.5 run function bm:p29/jar/rray', 'tag @s remove bm.jarrer',
                           'execute if score #got bm.pay matches 0 run ' + deny('Aim at a block within 8 blocks to let it out.'),
                           'execute if score #got bm.pay matches 1 run item modify entity @s weapon.mainhand bm:p29/jar_empty'])
    fn('p29/jar/rray', ['execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p29/jar/rhit',
                        'scoreboard players remove #ray bm.pay 1',
                        'execute if score #ray bm.pay matches 1.. positioned ^ ^ ^0.25 run function bm:p29/jar/rray'])
    fn('p29/jar/rhit', ['execute positioned ^ ^ ^-0.3 align xyz positioned ~0.5 ~ ~0.5 unless block ~ ~ ~ #bm:p29_open run return 0',
                        'execute positioned ^ ^ ^-0.3 align xyz positioned ~0.5 ~ ~0.5 run function bm:p29/jar/out'])
    fn('p29/jar/out', ['scoreboard players set #ok bm.pay 0', 'function bm:p29/jar/summon with storage bm:jar rel',
                       'execute if score #ok bm.pay matches 0 run data remove storage bm:jar rel.data.UUID',
                       'execute if score #ok bm.pay matches 0 run function bm:p29/jar/summon with storage bm:jar rel',
                       'execute if score #ok bm.pay matches 0 run return run ' + title('@a[tag=bm.jarrer]', 'actionbar', T("It won't come out here.", 'red')),
                       'scoreboard players set #got bm.pay 1', 'particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.02 15',
                       'playsound minecraft:item.bottle.empty neutral @a[distance=..16] ~ ~ ~ 1 0.8'])
    fn('p29/jar/summon', ['$execute store success score #ok bm.pay run summon $(eid) ~ ~ ~ $(data)'])

    # ================================================================== SPAWNER CROWBAR + CAGED SPAWNER
    crow_lore = list(ITEMS['spawner_crowbar']['comps']['minecraft:lore'])
    fn('p29/crow/use', no_zone('The crowbar') + ['execute if score @s bm.rcd2 matches 1.. run return 0', 'scoreboard players set @s bm.rcd2 10',
                                                 'scoreboard players set #ray bm.pay 20', 'scoreboard players set #got bm.pay 0', 'tag @s add bm.jarrer',
                                                 'execute anchored eyes positioned ^ ^ ^0.3 run function bm:p29/crow/ray', 'tag @s remove bm.jarrer',
                                                 'execute if score #got bm.pay matches 0 run ' + deny('Aim at a monster spawner within 5 blocks.')])
    fn('p29/crow/ray', ['execute if block ~ ~ ~ minecraft:spawner run return run function bm:p29/crow/pry',
                        'execute unless block ~ ~ ~ #bm:grap_pass run return 0', 'scoreboard players remove #ray bm.pay 1',
                        'execute if score #ray bm.pay matches 1.. positioned ^ ^ ^0.25 run function bm:p29/crow/ray'])
    fn('p29/crow/pry', ['scoreboard players set #got bm.pay 1', 'data remove storage bm:jar sp', 'data modify storage bm:jar sp set from block ~ ~ ~',
                        'data remove storage bm:jar sp.x', 'data remove storage bm:jar sp.y', 'data remove storage bm:jar sp.z', 'data remove storage bm:jar sp.id',
                        'setblock ~ ~ ~ minecraft:air', 'playsound minecraft:block.chain.break block @a[distance=..16] ~ ~ ~ 1 0.6',
                        'particle minecraft:smoke ~ ~0.5 ~ 0.3 0.3 0.3 0.02 20',
                        'execute as @a[tag=bm.jarrer,limit=1] at @s run function bm:p29/crow/after'])
    fn('p29/crow/after', ['execute store result score #u bm.pay run data get entity @s SelectedItem.components."minecraft:custom_data".uses',
                          'scoreboard players remove #u bm.pay 1',
                          'execute store result storage bm:tmp cu.u int 1 run scoreboard players get #u bm.pay',
                          'execute if score #u bm.pay matches 1.. run function bm:p29/crow/set_m with storage bm:tmp cu',
                          'execute if score #u bm.pay matches ..0 run item replace entity @s weapon.mainhand with minecraft:air',
                          'execute if score #u bm.pay matches ..0 run playsound minecraft:entity.item.break player @s ~ ~ ~ 1 1',
                          'loot spawn ~ ~0.5 ~ loot bm:p29/caged',
                          title('@s', 'actionbar', T('The spawner comes loose, cage and all.', '#8a8a96'))])
    crow_dyn = [T('Uses left: $(u)', 'gray') if isinstance(l, dict) and l.get('text') == '3 uses.' else l for l in crow_lore]
    fn('p29/crow/set_m', ['$item modify entity @s weapon.mainhand {function:"minecraft:sequence",functions:[{function:"minecraft:set_custom_data",tag:{uses:$(u)}},'
                          '{function:"minecraft:set_lore",mode:"replace_all",lore:' + snbt(crow_dyn) + '}]}'])
    wjson('bm/loot_table/p29/caged.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('caged_spawner', None, [
        {'function': 'minecraft:copy_custom_data', 'source': {'type': 'minecraft:storage', 'source': 'bm:jar'}, 'ops': [{'source': 'sp', 'target': 'sp', 'op': 'replace'}]},
        {'function': 'minecraft:set_lore', 'entity': 'this', 'mode': 'replace_all', 'lore': [
            [T('Spawns: ', 'gray'), {'nbt': 'sp.SpawnData.entity.id', 'storage': 'bm:jar', 'color': 'white', 'italic': False}],
            T('Right-click a block to set it down there.', 'blue'), T('Black Market goods — no refunds, no questions', 'dark_gray', italic=True)]}])]}]})
    fn('p29/cage/use', no_zone('The cage') + ['execute if score @s bm.rcd2 matches 1.. run return 0', 'scoreboard players set @s bm.rcd2 10',
                                              'data remove storage bm:jar put', 'data modify storage bm:jar put set from entity @s SelectedItem.components."minecraft:custom_data".sp',
                                              'scoreboard players set #ray bm.pay 20', 'scoreboard players set #got bm.pay 0', 'tag @s add bm.jarrer',
                                              'execute anchored eyes positioned ^ ^ ^0.3 run function bm:p29/cage/ray', 'tag @s remove bm.jarrer',
                                              'execute if score #got bm.pay matches 0 run ' + deny('Aim at a block within 5 blocks to set it down.'),
                                              'execute if score #got bm.pay matches 1 run item replace entity @s weapon.mainhand with minecraft:air'])
    fn('p29/cage/ray', ['execute unless block ~ ~ ~ #bm:grap_pass positioned ^ ^ ^-0.3 align xyz positioned ~0.5 ~0.5 ~0.5 if block ~ ~ ~ #bm:p29_rift_ok run return run function bm:p29/cage/put',
                        'execute unless block ~ ~ ~ #bm:grap_pass run return 0', 'scoreboard players remove #ray bm.pay 1',
                        'execute if score #ray bm.pay matches 1.. positioned ^ ^ ^0.25 run function bm:p29/cage/ray'])
    fn('p29/cage/put', ['setblock ~ ~ ~ minecraft:spawner', 'data modify block ~ ~ ~ {} merge from storage bm:jar put', 'scoreboard players set #got bm.pay 1',
                        'playsound minecraft:block.chain.place block @a[distance=..16] ~ ~ ~ 1 0.6', 'particle minecraft:smoke ~ ~ ~ 0.4 0.4 0.4 0.02 20'])

    # ================================================================== LODESTONE LOCKET
    fn('p29/locket/use', ['execute if score @s bm.rcd2 matches 1.. run return 0', 'scoreboard players set @s bm.rcd2 10',
                          'execute if score @s bm.magnet matches 1 run return run function bm:p29/locket/off',
                          'scoreboard players set @s bm.magnet 1', 'playsound minecraft:block.lodestone.place player @s ~ ~ ~ 1 1.4',
                          title('@s', 'actionbar', T('Lodestone Locket: ON', '#b0a0d0'))])
    fn('p29/locket/off', ['scoreboard players set @s bm.magnet 0', 'playsound minecraft:block.lodestone.break player @s ~ ~ ~ 1 0.8',
                          title('@s', 'actionbar', T('Lodestone Locket: off', 'gray'))])
    second.append('execute as @a[scores={bm.magnet=1},gamemode=!spectator] if items entity @s container.* *[minecraft:custom_data~{bm:"lodestone_locket"}] at @s run function bm:p29/locket/pull')
    fn('p29/locket/pull', ['tp @e[type=minecraft:item,distance=1.2..7,nbt={PickupDelay:0s}] @s', 'tp @e[type=minecraft:experience_orb,distance=1.2..7] @s'])

    # ================================================================== FAIR WEATHER BELL
    fn('p29/bell/use', ['execute if score @s bm.bellday = #day bm.bm run ' + deny('The bell has already rung today.'),
                        'execute unless dimension minecraft:overworld run ' + deny('No weather to clear here.'),
                        'execute unless predicate bm:p29/raining run ' + deny('The sky is already clear.'),
                        'scoreboard players operation @s bm.bellday = #day bm.bm', 'weather clear 1d',
                        'playsound minecraft:block.bell.use player @a[distance=..32] ~ ~ ~ 1 1.6', 'playsound minecraft:block.bell.resonate player @a[distance=..32] ~ ~ ~ 0.6 1.4',
                        tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(' rang the Fair Weather Bell. The clouds have an errand elsewhere.', 'gray')])])

    # ================================================================== DONADO STATUES (placed like the Void Rat Statue)
    for sid, model, tagx in (('donado_trophy', 'bm:statue_donado', 'bm.dstat'), ('golden_donado', 'bm:statue_donado_gold', 'bm.gstat')):
        G.consume_adv(sid, f'bm:p29/statue/{sid}')
        fn(f'p29/statue/{sid}', [f'advancement revoke @s only bm:consume/{sid}', 'scoreboard players set #placed bm.pay 0', 'scoreboard players set #ray bm.pay 25',
                                 'tag @s add bm.placer', f'execute anchored eyes positioned ^ ^ ^ run function bm:p29/statue/ray_{sid}', 'tag @s remove bm.placer',
                                 f'execute if score #placed bm.pay matches 0 unless entity @s[gamemode=creative] run ' + give(sid),
                                 'execute if score #placed bm.pay matches 0 run ' + title('@s', 'actionbar', T('Look at the top of a block within 5 blocks to set it down.', 'gray'))])
        fn(f'p29/statue/ray_{sid}', [f'execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p29/statue/hit_{sid}',
                                     'scoreboard players remove #ray bm.pay 1',
                                     f'execute if score #ray bm.pay matches 1.. positioned ^ ^ ^0.2 run function bm:p29/statue/ray_{sid}'])
        fn(f'p29/statue/hit_{sid}', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                                     'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.p29stat,distance=..0.6] run return 0',
                                     f'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p29/statue/spawn_{sid}'])
        sc = 0.9
        disp_ = {'Tags': ['bm.p29disp', tagx, 'bm.pnew'], 'teleport_duration': Int(3), 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
                 'item_display': 'fixed', 'billboard': 'fixed', 'brightness': {'block': Int(13), 'sky': Int(12)},
                 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(sc / 2), F(0)], 'scale': [F(sc)] * 3}}
        box = {'Tags': ['bm.p29stat', f'{tagx}_hit', 'bm.pnew'], 'width': F(0.8), 'height': F(1.1), 'response': B(1)}
        fn(f'p29/statue/spawn_{sid}', [f'summon minecraft:item_display ~ ~ ~ {snbt(disp_)}', f'summon minecraft:interaction ~ ~ ~ {snbt(box)}',
                                       'execute rotated as @a[tag=bm.placer,limit=1] run tp @e[tag=bm.pnew,distance=..0.5] ~ ~ ~ ~180 0',
                                       'tag @e[tag=bm.pnew,distance=..0.5] remove bm.pnew', 'scoreboard players set #placed bm.pay 1',
                                       'playsound minecraft:block.stone.place block @a[distance=..16] ~ ~ ~ 1 0.8',
                                       'particle minecraft:wax_on ~ ~0.6 ~ 0.3 0.3 0.3 0.02 15'])
        fn(f'p29/statue/pick_{sid}', [f'loot spawn ~ ~0.3 ~ loot bm:items/{sid}', f'kill @e[type=minecraft:item_display,tag={tagx},distance=..0.3]',
                                      'particle minecraft:poof ~ ~0.4 ~ 0.2 0.2 0.2 0.02 6', 'playsound minecraft:block.stone.break block @a[distance=..16] ~ ~ ~ 1 0.9', 'kill @s'])
        fast.append(f'execute as @e[type=minecraft:interaction,tag={tagx}_hit] if data entity @s attack at @s run function bm:p29/statue/punch_{sid}')
        fn(f'p29/statue/punch_{sid}', ['scoreboard players set #sn bm.pay 0',
                                       'execute on attacker if predicate bm:p20/sneaking run scoreboard players set #sn bm.pay 1',
                                       'execute if score #sn bm.pay matches 0 on attacker run ' + title('@s', 'actionbar', T('Sneak + punch to pick it up.', 'gray')),
                                       'data remove entity @s attack',
                                       f'execute if score #sn bm.pay matches 1 run function bm:p29/statue/pick_{sid}'])
        fast.append(f'execute as @e[type=minecraft:interaction,tag={tagx}_hit] if data entity @s interaction at @s run function bm:p29/statue/turn_{sid}')
        fn(f'p29/statue/turn_{sid}', ['data remove entity @s interaction',
                                      f'execute as @e[type=minecraft:item_display,tag={tagx},distance=..0.3] at @s run tp @s ~ ~ ~ ~45 0',
                                      'playsound minecraft:block.stone_button.click_on block @a[distance=..12] ~ ~ ~ 0.6 1.4'])
    # the Golden Donado tends the garden: every minute, every crop within 8 blocks grows one stage (highest stage first,
    # so nothing skips ahead); baby animals within 8 blocks grow up a minute faster
    grow = []
    for crop, top in CROPS.items():
        for a in range(top - 1, -1, -1):
            grow.append(f'fill ~-8 ~-2 ~-8 ~8 ~2 ~8 minecraft:{crop}[age={a + 1}] replace minecraft:{crop}[age={a}]')
    grow += ['execute as @e[type=#bm:p29_babies,distance=..8] run function bm:p29/statue/age',
             'particle minecraft:happy_villager ~ ~0.5 ~ 4 0.5 4 0 25', 'particle minecraft:wax_on ~ ~1 ~ 0.3 0.4 0.3 0 8']
    fn('p29/statue/grow', ['scoreboard players set @s bm.dtimer 0'] + grow)
    fn('p29/statue/age', ['execute store result score #a bm.pay run data get entity @s Age', 'execute unless score #a bm.pay matches ..-1 run return 0',
                          'scoreboard players add #a bm.pay 1200', 'execute if score #a bm.pay matches 0.. run scoreboard players set #a bm.pay 0',
                          'execute store result entity @s Age int 1 run scoreboard players get #a bm.pay'])
    wjson('bm/tags/entity_type/p29_babies.json', {'values': [f'minecraft:{a}' for a in ('cow', 'pig', 'sheep', 'chicken', 'rabbit', 'goat', 'horse', 'donkey',
                                                                                        'mule', 'llama', 'camel', 'mooshroom', 'wolf', 'cat', 'fox', 'panda',
                                                                                        'turtle', 'armadillo', 'sniffer', 'frog', 'bee', 'ocelot', 'hoglin', 'strider', 'axolotl', 'villager')]})
    second += ['scoreboard players add @e[type=minecraft:item_display,tag=bm.gstat] bm.dtimer 1',
               'execute as @e[type=minecraft:item_display,tag=bm.gstat,scores={bm.dtimer=60..}] at @s run function bm:p29/statue/grow',
               'execute as @e[type=minecraft:item_display,tag=bm.gstat] at @s if entity @a[distance=..16] run particle minecraft:wax_on ~ ~0.9 ~ 0.25 0.35 0.25 0 2']

    # ================================================================== SEALED EXPLORER'S MAP
    G.consume_adv('sealed_explorer_map', 'bm:p29/map')
    fn('p29/map', ['advancement revoke @s only bm:consume/sealed_explorer_map', 'loot spawn ~ ~0.5 ~ loot bm:p29/explorer_map',
                   title('@s', 'actionbar', T('The seal cracks... the map shows somewhere old and dangerous.', 'aqua'))])
    def emap(item, dest, deco, name):      # 26.3: explorer maps are their own items (vanilla cartographer/chest loot uses them)
        return {'type': 'minecraft:item', 'name': item, 'weight': 1, 'functions': [
            {'function': 'minecraft:exploration_map', 'destination': dest, 'decoration': deco, 'zoom': 2, 'search_radius': 100, 'skip_existing_chunks': False},
            {'function': 'minecraft:set_name', 'target': 'item_name', 'name': T(name, 'aqua')}]}
    wjson('bm/loot_table/p29/explorer_map.json', {'pools': [{'rolls': 1, 'entries': [
        emap('minecraft:buried_trial_chambers_map', 'minecraft:on_buried_trial_chambers_maps', 'minecraft:trial_chambers', 'Trial Chamber Map'),
        emap('minecraft:woodland_mansion_map', 'minecraft:on_woodland_mansion_maps', 'minecraft:mansion', 'Woodland Mansion Map')]}]})

    # ================================================================== RAT GANG PORTRAIT (a painting variant)
    wjson('bm/painting_variant/rat_gang.json', {'asset_id': 'bm:rat_gang', 'width': Int(2), 'height': Int(2),
                                                 'title': T('The Rat Gang', 'yellow'), 'author': T('Madame Velour', 'gray')})

    # ================================================================== WINGS OF THE RAT KING / RAT KING'S SIGNET
    worn = 'if items entity @s armor.chest *[minecraft:custom_data~{bm:"wings_rat_king"}]'
    fast.append(f'execute as @a[gamemode=!spectator] {worn} if predicate bm:gliding at @s run function bm:p29/rkwings')
    wjson('bm/predicate/p29/has_regen.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:effects': {'minecraft:regeneration': {}}}})
    fn('p29/rkwings', ['execute unless predicate bm:p29/has_regen run effect give @s minecraft:regeneration 5 0 true', 'particle minecraft:wax_on ~ ~0.5 ~ 0.4 0.2 0.4 0 3',
                       'particle minecraft:dust{color:[1.0,0.78,0.1],scale:1.2} ~ ~0.4 ~ 0.4 0.1 0.4 0 3'])

    # ================================================================== COSMETICS
    # Auroral Crown: a slow ribbon of colours turning above the head
    cols = [(0.3, 1.0, 0.75), (0.25, 0.75, 1.0), (0.6, 0.4, 1.0), (1.0, 0.45, 0.85), (0.4, 1.0, 0.5), (0.2, 0.9, 0.9)]
    fn('p29/aurora', [f'execute if score #t6 bm.p29t matches {i} run particle minecraft:dust{{color:[{r},{g},{b}],scale:0.7}} ^{0.35 * (1 if i % 2 else -1)} ^2.15 ^{0.25 * (1 if i < 3 else -1)} 0.12 0.04 0.12 0 3'
                      for i, (r, g, b) in enumerate(cols)] + ['particle minecraft:end_rod ~ ~2.2 ~ 0.25 0.05 0.25 0 1'])
    fast.append('scoreboard players add #t6 bm.p29t 1')
    fast.append('execute if score #t6 bm.p29t matches 6.. run scoreboard players set #t6 bm.p29t 0')
    fast.append('execute as @a[gamemode=!spectator] if items entity @s armor.head *[minecraft:custom_data~{bm:"auroral_crown"}] at @s run function bm:p29/aurora')
    # Brass Wing Scroll / Market Crest Scroll (off-hand targets, refunded on a wrong target)
    G.consume_adv('brass_wing_scroll', 'bm:p29/brass')
    fn('p29/brass', ['advancement revoke @s only bm:consume/brass_wing_scroll',
                     'execute unless items entity @s weapon.offhand minecraft:elytra run return run function bm:p29/brass_no',
                     'execute if items entity @s weapon.offhand minecraft:elytra[minecraft:custom_data] unless items entity @s weapon.offhand minecraft:elytra[minecraft:custom_data~{bm_skin:"brass"}] run return run function bm:p29/brass_no',
                     'item modify entity @s weapon.offhand bm:p29/brass',
                     'playsound minecraft:block.copper.place player @s ~ ~ ~ 1 0.8', 'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 1.2',
                     title('@s', 'actionbar', T('Tick, tick, whirr: your wings are brass now.', '#c8963c'))])
    fn('p29/brass_no', [give('brass_wing_scroll'), title('@s', 'actionbar', T('Hold a plain elytra in your OFF hand! (Refunded)', 'red'))])
    wjson('bm/item_modifier/p29/brass.json', [
        {'function': 'minecraft:set_components', 'components': {
            'minecraft:equippable': {'slot': 'chest', 'asset_id': 'bm:brass_wings', 'equip_sound': 'minecraft:item.armor.equip_elytra', 'damage_on_hurt': False},
            'minecraft:item_model': 'bm:brass_wings'}},
        {'function': 'minecraft:set_custom_data', 'tag': '{bm_skin:"brass"}'}])
    wjson('bm/item_modifier/p29/unbrass.json', {'function': 'minecraft:set_components', 'components': {
        'minecraft:equippable': {'slot': 'chest', 'asset_id': 'minecraft:elytra', 'equip_sound': 'minecraft:item.armor.equip_elytra', 'damage_on_hurt': False},
        '!minecraft:custom_data': {}}})
    rs = G.FUNCS['skins/restore']
    k = rs.index('function bm:skins/restore_m with storage bm:tmp item')
    rs[k:k] = ['execute if items entity @s weapon.offhand minecraft:elytra[minecraft:custom_data~{bm_skin:"brass"}] run item modify entity @s weapon.offhand bm:p29/unbrass']
    G.consume_adv('market_crest_scroll', 'bm:p29/crest')
    fn('p29/crest', ['advancement revoke @s only bm:consume/market_crest_scroll',
                     'execute unless items entity @s weapon.offhand minecraft:shield run return run function bm:p29/crest_no',
                     'item modify entity @s weapon.offhand bm:p29/crest',
                     'playsound minecraft:item.armor.equip_leather player @s ~ ~ ~ 1 0.8', 'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 1 1.2',
                     title('@s', 'actionbar', T('Your shield now bears the Black Market crest.', '#ffcf3f'))])
    fn('p29/crest_no', [give('market_crest_scroll'), title('@s', 'actionbar', T('Hold a shield in your OFF hand! (Refunded)', 'red'))])
    wjson('bm/item_modifier/p29/crest.json', {'function': 'minecraft:set_components', 'components': {
        'minecraft:base_color': 'black', 'minecraft:banner_patterns': [{'pattern': 'bm:rat_crest', 'color': 'yellow'}, {'pattern': 'minecraft:border', 'color': 'yellow'}]}})
    wjson('bm/banner_pattern/rat_crest.json', {'asset_id': 'bm:rat_crest', 'translation_key': 'block.bm.banner.rat_crest'})
    # Rat Familiar: a small rat display rides your shoulder (one per player, matched by player id)
    fam = {'Tags': ['bm.familiar', 'bm.fnew'], 'teleport_duration': Int(1), 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:rat3d_familiar'}},
           'item_display': 'fixed', 'billboard': 'fixed', 'brightness': {'block': Int(12), 'sky': Int(12)},
           'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.11), F(0)], 'scale': [F(0.25)] * 3}}
    has_fam = 'if items entity @s container.* *[minecraft:custom_data~{bm:"rat_familiar"}]'
    second += ['tag @a remove bm.hasfam', f'execute as @a[gamemode=!spectator] {has_fam} run tag @s add bm.hasfam',
               'execute as @a[tag=bm.hasfam] at @s unless function bm:p29/fam/mine run function bm:p29/fam/spawn',
               'execute as @e[type=minecraft:item_display,tag=bm.familiar] unless function bm:p29/fam/owner_ok run kill @s',
               'execute as @a[tag=bm.hasfam] at @s if predicate bm:p20/croak run playsound minecraft:entity.silverfish.ambient player @a[distance=..8] ~ ~1.5 ~ 0.25 2']
    fn('p29/fam/mine', ['scoreboard players operation #p bm.pay = @s bm.pid',
                        'execute as @e[type=minecraft:item_display,tag=bm.familiar,distance=..4] if score @s bm.pid = #p bm.pay run return 1', 'return 0'])
    fn('p29/fam/spawn', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', f'summon minecraft:item_display ~ ~1.4 ~ {snbt(fam)}',
                         'scoreboard players operation @e[type=minecraft:item_display,tag=bm.fnew,distance=..3] bm.pid = @s bm.pid',
                         'tag @e[type=minecraft:item_display,tag=bm.fnew] remove bm.fnew'])
    fn('p29/fam/owner_ok', ['scoreboard players operation #p bm.pay = @s bm.pid',
                            'execute at @s as @a[tag=bm.hasfam,distance=..4] if score @s bm.pid = #p bm.pay run return 1', 'return 0'])
    tick.append('execute as @a[tag=bm.hasfam] at @s run function bm:p29/fam/follow')
    fn('p29/fam/follow', ['scoreboard players operation #p bm.pay = @s bm.pid',
                          'execute unless predicate bm:p20/sneaking rotated ~ 0 positioned ^-0.36 ^1.42 ^-0.04 as @e[type=minecraft:item_display,tag=bm.familiar,distance=..4] if score @s bm.pid = #p bm.pay run tp @s ~ ~ ~ ~ 0',
                          'execute if predicate bm:p20/sneaking rotated ~ 0 positioned ^-0.36 ^1.12 ^-0.12 as @e[type=minecraft:item_display,tag=bm.familiar,distance=..4] if score @s bm.pid = #p bm.pay run tp @s ~ ~ ~ ~ 0'])
    # Bloomwalker Boots: a flower pops up where you walk on grass or dirt, and fades
    flower = lambda f: {'Tags': ['bm.bloom', 'bm.bnew2'], 'block_state': f'minecraft:{f}', 'teleport_duration': Int(0),
                        'interpolation_duration': Int(6), 'start_interpolation': Int(0),
                        'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(-0.3), F(0), F(-0.3)], 'scale': [F(0.6)] * 3}}
    fn('p29/bloom', ['scoreboard players set @s bm.walk 0', 'execute unless block ~ ~-0.2 ~ #bm:p29_soil run return 0',
                     'execute if entity @e[type=minecraft:block_display,tag=bm.bloom,distance=..0.8] run return 0',
                     'execute store result score #f bm.pay run random value 1..8'] +
       [f'execute if score #f bm.pay matches {i} align xz positioned ~0.5 ~ ~0.5 run summon minecraft:block_display ~ ~ ~ {snbt(flower(f))}' for i, f in enumerate(FLOWERS, 1)] +
       ['scoreboard players set @e[type=minecraft:block_display,tag=bm.bnew2] bm.ftimer 12', 'tag @e[type=minecraft:block_display,tag=bm.bnew2] remove bm.bnew2'])
    wjson('bm/tags/block/p29_soil.json', {'values': ['minecraft:grass_block', 'minecraft:dirt', 'minecraft:podzol', 'minecraft:coarse_dirt', 'minecraft:rooted_dirt',
                                                     'minecraft:moss_block', 'minecraft:mycelium', 'minecraft:farmland', 'minecraft:mud']})
    fast += ['execute as @a[gamemode=!spectator,scores={bm.walk=60..}] if items entity @s armor.feet *[minecraft:custom_data~{bm:"bloomwalker_boots"}] at @s run function bm:p29/bloom',
             'scoreboard players remove @e[type=minecraft:block_display,tag=bm.bloom] bm.ftimer 1',
             'execute as @e[type=minecraft:block_display,tag=bm.bloom,scores={bm.ftimer=..2}] run data merge entity @s {start_interpolation:0,interpolation_duration:10,transformation:{scale:[0f,0f,0f],translation:[0f,0f,0f]}}',
             'kill @e[type=minecraft:block_display,tag=bm.bloom,scores={bm.ftimer=..0}]']
    second.append('scoreboard players reset @a bm.walk')
    # Showstopper Charm: a kill ends in gold confetti
    tick.append('execute as @a[scores={bm.kills=1..}] at @s run function bm:p29/show')
    fn('p29/show', ['scoreboard players set @s bm.kills 0', 'execute unless items entity @s container.* *[minecraft:custom_data~{bm:"showstopper_charm"}] run return 0',
                    'execute at @e[distance=..24,type=!minecraft:player,nbt={Health:0.0f},sort=nearest,limit=1] run function bm:p29/confetti'])
    fn('p29/confetti', ['particle minecraft:firework ~ ~1 ~ 0.3 0.4 0.3 0.15 25', 'particle minecraft:wax_on ~ ~1 ~ 0.6 0.6 0.6 0 20',
                        'particle minecraft:dust{color:[1.0,0.84,0.0],scale:1.0} ~ ~1.2 ~ 0.6 0.6 0.6 0 20',
                        'particle minecraft:dust{color:[1.0,0.3,0.6],scale:0.8} ~ ~1.2 ~ 0.6 0.6 0.6 0 12',
                        'playsound minecraft:entity.firework_rocket.twinkle player @a[distance=..16] ~ ~ ~ 0.6 1.4'])

    # ================================================================== RUFUS GNAW, RAT FOR HIRE
    merc_generate(G, fn, wjson, title, tellraw, give, PREFIX, tick, fast, second, load, ident, P28)

    G.FUNCS['load'][-1:-1] = load
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second
    G.FUNCS['admin/uninstall'][-1:-1] = ['kill @e[tag=bm.familiar]', 'kill @e[tag=bm.bloom]'] + [f'scoreboard objectives remove {o}' for o in G.P29_OBJ]


def merc_generate(G, fn, wjson, title, tellraw, give, PREFIX, tick, fast, second, load, ident, P28):
    """Rufus Gnaw: an invisible tamed wolf (follows, teleports to you, fights) carrying his rat figure and nameplate.
    State per player (bm.mstate): 0 never hired / 1 on duty / 2 fallen (patch him up: 2 Medallions) / 3 left unpaid.
    Modes (bm.mmode): 1 follow, 2 guard a spot (he stays within 8 blocks of it), 3 follow + scavenge.
    A 'generation' number (bm.mgen) lets a new summon retire any old copy stranded in an unloaded chunk."""
    def deny(msg): return 'return run ' + title('@s', 'actionbar', T(msg, 'gray'))
    WOLF_TOP = 0.85
    sc = 0.55
    wolf = {'Tags': ['bm.mercpet', 'bm.mnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1),
            'CustomName': T(MERC_NAME, '#c0392b', bold=True), 'CustomNameVisible': B(0), 'Health': F(30),
            'attributes': [{'id': 'minecraft:max_health', 'base': Dd(30)}, {'id': 'minecraft:attack_damage', 'base': Dd(5)},
                           {'id': 'minecraft:movement_speed', 'base': Dd(0.34)}, {'id': 'minecraft:follow_range', 'base': Dd(32)}],
            'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}],
            'drop_chances': {s: F(0.0) for s in ('mainhand', 'head', 'chest', 'legs', 'feet')}}
    body = {'Tags': ['bm.m_disp', 'bm.m_body', 'bm.mnew'], 'teleport_duration': Int(2), 'shadow_radius': F(0.3),
            'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:rat3d_merc'}},
            'item_display': 'fixed', 'billboard': 'fixed',
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(round(sc / 2 - WOLF_TOP + 0.02, 3)), F(0)], 'scale': [F(sc)] * 3}}
    plate = {'Tags': ['bm.m_disp', 'bm.m_plate', 'bm.mnew'], 'billboard': 'center', 'view_range': F(0.25), 'default_background': B(0),
             'background': Int(0x60000000), 'text': [T(MERC_NAME, '#c0392b', bold=True), T('\nRecruit', 'gray')],
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(round(0.55 - WOLF_TOP + 0.4, 3)), F(0)], 'scale': [F(0.45)] * 3}}
    fn('p29/merc/summon', [
        'scoreboard players add @s bm.mgen 1', f'summon minecraft:wolf ~ ~ ~ {snbt(wolf)}',
        'data modify entity @e[type=minecraft:wolf,tag=bm.mnew,limit=1,sort=nearest] Owner set from entity @s UUID',
        'scoreboard players operation @e[type=minecraft:wolf,tag=bm.mnew,limit=1,sort=nearest] bm.pid = @s bm.pid',
        'scoreboard players operation @e[type=minecraft:wolf,tag=bm.mnew,limit=1,sort=nearest] bm.mgen = @s bm.mgen',
        f'summon minecraft:item_display ~ ~ ~ {snbt(body)}', f'summon minecraft:text_display ~ ~ ~ {snbt(plate)}',
        'scoreboard players operation @e[tag=bm.m_disp,tag=bm.mnew,distance=..2] bm.pid = @s bm.pid',
        'execute as @e[tag=bm.m_disp,tag=bm.mnew,distance=..2] run ride @s mount @e[type=minecraft:wolf,tag=bm.mnew,limit=1,sort=nearest]',
        'tag @e[tag=bm.mnew,distance=..3] remove bm.mnew',
        'scoreboard players set @s bm.mstate 1', 'execute unless score @s bm.mmode matches 1.. run scoreboard players set @s bm.mmode 1',
        'execute store result storage bm:tmp mg.g int 1 run scoreboard players get @s bm.mgen',
        'execute store result storage bm:tmp mg.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p29/merc/gen with storage bm:tmp mg',
        'function bm:p29/merc/rank_apply',
        'particle minecraft:poof ~ ~0.5 ~ 0.4 0.4 0.4 0.02 15', 'playsound minecraft:item.crossbow.loading_end neutral @a[distance=..16] ~ ~ ~ 1 1'])
    fn('p29/merc/gen', ['$data modify storage bm:merc g.p$(pid) set value $(g)'])
    # orders menu (dynamic: rank, purse, days, mode, state)
    fn('p29/merc/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                        'execute if score @s bm.rcd2 matches 1.. run return 0', 'scoreboard players set @s bm.rcd2 10',
                        'execute unless score @s bm.mstate matches 1.. run return run function bm:p29/merc/first',
                        f'scoreboard players set @s bm.menu {P28.MENU["merc"]}', 'data remove storage bm:ui mc',
                        'execute store result storage bm:ui mc.purse int 1 run scoreboard players get @s bm.mpurse',
                        'execute store result storage bm:ui mc.days int 1 run scoreboard players get @s bm.mdays',
                        'data modify storage bm:ui mc.rank set value "Recruit"',
                        f'execute if score @s bm.mdays matches {RANKS[1][0]}.. run data modify storage bm:ui mc.rank set value "Veteran"',
                        f'execute if score @s bm.mdays matches {RANKS[2][0]}.. run data modify storage bm:ui mc.rank set value "Captain"',
                        'data modify storage bm:ui mc.mode set value "Following you"',
                        'execute if score @s bm.mmode matches 2 run data modify storage bm:ui mc.mode set value "Guarding a spot"',
                        'execute if score @s bm.mmode matches 3 run data modify storage bm:ui mc.mode set value "Following and scavenging"',
                        'data modify storage bm:ui mc.state set value "On duty"',
                        'execute if score @s bm.mstate matches 2 run data modify storage bm:ui mc.state set value "Fallen - being patched up at the market"',
                        'execute if score @s bm.mstate matches 3 run data modify storage bm:ui mc.state set value "Gone home - his purse ran dry"',
                        'execute store result storage bm:ui mc.pid int 1 run scoreboard players get @s bm.pid',
                        'function bm:p29/merc/bagcount with storage bm:ui mc',
                        'function bm:p29/merc/dlg with storage bm:ui mc'])
    fn('p29/merc/bagcount', ['data modify storage bm:ui mc.bag set value 0', '$execute store result storage bm:ui mc.bag int 1 run data get storage bm:merc bag.p$(pid)'])
    dlg = P28.multi([T(MERC_NAME, '#c0392b', bold=True), T(', rat for hire', 'gray')],
                    [P28.body([T('Rank: ', 'gray'), T('$(rank)', 'gold'), T('   Service: ', 'gray'), T('$(days)', 'white'), T(' days', 'gray')]),
                     P28.body([T('Status: ', 'gray'), T('$(state)', 'white')]),
                     P28.body([T('Orders: ', 'gray'), T('$(mode)', 'white')]),
                     P28.body([T('Purse: ', 'gray'), T('$(purse)', 'gold'), T(' Tokens (1 a day)   Loot carried: ', 'gray'), T('$(bag)', 'white'), T(' stacks', 'gray')])],
                    [P28.btn(T('Follow me', 'white'), 7001), P28.btn(T('Guard this spot', 'white'), 7002),
                     P28.btn(T('Follow and scavenge', 'white'), 7003), P28.btn(T('Hand over the loot', 'white'), 7004),
                     P28.btn([T('Pay a week  ', 'white'), T('7 Tokens', 'gold')], 7005), P28.btn(T('Call him to me', 'white'), 7006),
                     P28.btn([T('Patch him up  ', 'white'), T('2 Medallions', 'light_purple')], 7007)], columns=2)
    fn('p29/merc/dlg', [f'$dialog show @s {P28.inline(dlg)}'])
    fn('p29/merc/first', ['scoreboard players set @s bm.mpurse 7', 'scoreboard players set @s bm.mdays 0', 'scoreboard players set @s bm.mmode 1',
                          'scoreboard players operation @s bm.mday = #day bm.bm', 'function bm:p29/merc/summon',
                          'title @s times 10 60 15', title('@s', 'subtitle', T('Right-click the contract to give him orders', 'gray', italic=True)),
                          title('@s', 'title', T(f'{MERC_NAME} signs on!', '#c0392b', bold=True)),
                          tellraw('@s', PREFIX + [T(f'{MERC_NAME} follows you, shoots what threatens you and bites what gets close. ', 'gray'),
                                                  T('A week of wages is already in his purse.', 'gold')])])
    act = G.FUNCS['p28/act']
    act.append('execute if score #act bm.pay matches 7001..7099 run return run function bm:p29/merc/act')
    fn('p29/merc/act', [f'execute unless score @s bm.menu matches {P28.MENU["merc"]} run return run function bm:p28/stale',
                        'execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"merc_contract"}] run ' + deny('Hold the contract.'),
                        'execute if score #act bm.pay matches 7005 run return run function bm:p29/merc/pay',
                        'execute if score #act bm.pay matches 7007 run return run function bm:p29/merc/patch',
                        'execute unless score @s bm.mstate matches 1 run ' + deny("He isn't on duty. Pay or patch him up first."),
                        'execute if score #act bm.pay matches 7001 run return run function bm:p29/merc/mode {m:1}',
                        'execute if score #act bm.pay matches 7002 run return run function bm:p29/merc/mode {m:2}',
                        'execute if score #act bm.pay matches 7003 run return run function bm:p29/merc/mode {m:3}',
                        'execute if score #act bm.pay matches 7004 run return run function bm:p29/merc/handover',
                        'execute if score #act bm.pay matches 7006 run return run function bm:p29/merc/call'])
    mine = 'execute as @e[type=minecraft:wolf,tag=bm.mercpet] if score @s bm.pid = #p bm.pay'
    fn('p29/merc/mode', ['$scoreboard players set @s bm.mmode $(m)', 'scoreboard players operation #p bm.pay = @s bm.pid',
                         'execute if score @s bm.mmode matches 2 run function bm:p29/merc/post',
                         f'{mine} run data modify entity @s Sitting set value 0b',
                         'tag @s add bm.mown',
                         f'execute if score @s bm.mmode matches 2 {mine[8:]} run data remove entity @s Owner',
                         f'execute unless score @s bm.mmode matches 2 {mine[8:]} run data modify entity @s Owner set from entity @a[tag=bm.mown,limit=1] UUID',
                         'tag @s remove bm.mown', 'function bm:p29/merc/rank_apply',
                         'execute if score @s bm.mmode matches 1 run ' + title('@s', 'actionbar', T('"Right behind you, boss."', '#c0392b', italic=True)),
                         'execute if score @s bm.mmode matches 2 run ' + title('@s', 'actionbar', T('"Nobody gets past me."', '#c0392b', italic=True)),
                         'execute if score @s bm.mmode matches 3 run ' + title('@s', 'actionbar', T('"Finders keepers. For you, I mean."', '#c0392b', italic=True))])
    fn('p29/merc/post', [f'kill @e[type=minecraft:marker,tag=bm.mpost,scores={{bm.pid=1..}},distance=..1000] ',
                         'summon minecraft:marker ~ ~ ~ {Tags:["bm.mpost","bm.mpnew"]}',
                         'scoreboard players operation @e[type=minecraft:marker,tag=bm.mpnew,limit=1] bm.pid = @s bm.pid', 'tag @e[tag=bm.mpnew] remove bm.mpnew'])
    G.FUNCS['p29/merc/post'][0] = 'execute as @e[type=minecraft:marker,tag=bm.mpost] if score @s bm.pid = #p bm.pay run kill @s'
    fn('p29/merc/call', ['scoreboard players operation #p bm.pay = @s bm.pid', 'scoreboard players set #f bm.pay 0',
                         f'{mine} run scoreboard players set #f bm.pay 1', f'{mine} run tp @s @a[tag=bm.mcaller,limit=1]',
                         'execute if score #f bm.pay matches 0 run function bm:p29/merc/summon',
                         'playsound minecraft:entity.villager.ambient neutral @s ~ ~ ~ 0.6 1.8',
                         title('@s', 'actionbar', T('"On my way!"', '#c0392b', italic=True))])
    G.FUNCS['p29/merc/call'].insert(0, 'tag @s add bm.mcaller'); G.FUNCS['p29/merc/call'].append('tag @s remove bm.mcaller')
    fn('p29/merc/pay', P28.pay_lines('token', 7, 'function bm:p28/back/broke {m:"A week costs 7 Tokens."}') + [
        'scoreboard players add @s bm.mpurse 7', 'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 0.8',
        'execute if score @s bm.mstate matches 3 run scoreboard players operation @s bm.mday = #day bm.bm',
        'execute if score @s bm.mstate matches 3 run function bm:p29/merc/summon',
        tellraw('@s', PREFIX + [T('7 Tokens go into the purse. ', 'gold'), T(f'{MERC_NAME} bites one to check it.', 'gray')])])
    fn('p29/merc/patch', ['execute unless score @s bm.mstate matches 2 run ' + deny("He's fine. Not a scratch."),
                          *P28.pay_lines('medallion', 2, 'function bm:p28/back/broke {m:"The rat doctor charges 2 Medallions."}'),
                          'scoreboard players operation @s bm.mday = #day bm.bm', 'function bm:p29/merc/summon',
                          tellraw('@s', PREFIX + [T(f'{MERC_NAME} is patched up and back at your side - bandaged, grumpy, ready.', 'gray')])])
    # rank: hp and damage by days of service
    ra = ['scoreboard players operation #p bm.pay = @s bm.pid']
    for days, nm, col, hp, dmg in RANKS:
        ra += [f'execute if score @s bm.mdays matches {days}.. {mine[8:]} run attribute @s minecraft:max_health base set {hp}',
               f'execute if score @s bm.mdays matches {days}.. {mine[8:]} run attribute @s minecraft:attack_damage base set {dmg}',
               f'execute if score @s bm.mdays matches {days}.. as @e[type=minecraft:text_display,tag=bm.m_plate] if score @s bm.pid = #p bm.pay run data modify entity @s text set value '
               + snbt([T(MERC_NAME, '#c0392b', bold=True), T('\n' + nm, col)])]
    fn('p29/merc/rank_apply', ra)
    # wages: once per day; a dry purse sends him home
    second.append('execute as @a[scores={bm.mstate=1}] unless score @s bm.mday = #day bm.bm at @s run function bm:p29/merc/payday')
    fn('p29/merc/payday', ['scoreboard players operation @s bm.mday = #day bm.bm',
                           'execute if score @s bm.mpurse matches ..0 run return run function bm:p29/merc/quit',
                           'scoreboard players remove @s bm.mpurse 1', 'scoreboard players add @s bm.mdays 1',
                           f'execute if score @s bm.mdays matches {RANKS[1][0]} run ' + tellraw('@s', PREFIX + [T(f'{MERC_NAME} is a ', 'gray'), T('Veteran', 'aqua', bold=True), T(' now: tougher, harder-hitting.', 'gray')]),
                           f'execute if score @s bm.mdays matches {RANKS[2][0]} run ' + tellraw('@s', PREFIX + [T(f'{MERC_NAME} is a ', 'gray'), T('Captain', 'gold', bold=True), T(' now. He salutes himself.', 'gray')]),
                           'function bm:p29/merc/rank_apply',
                           'execute if score @s bm.mpurse matches 1 run ' + tellraw('@s', PREFIX + [T(f'{MERC_NAME}: "One Token left in the purse, boss. Just saying."', '#c0392b', italic=True)])])
    fn('p29/merc/quit', ['scoreboard players set @s bm.mstate 3', 'scoreboard players operation #p bm.pay = @s bm.pid',
                         'scoreboard players add @s bm.mgen 1', 'execute store result storage bm:tmp mg.g int 1 run scoreboard players get @s bm.mgen',
                         'execute store result storage bm:tmp mg.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p29/merc/gen with storage bm:tmp mg',
                         f'{mine} at @s run function bm:p29/merc/vanish',
                         tellraw('@s', PREFIX + [T(f'{MERC_NAME}: "No pay, no play." He heads back to the market. ', '#c0392b', italic=True),
                                                 T('(Pay a week from the contract to rehire him.)', 'gray')])])
    fn('p29/merc/vanish', ['execute on passengers run kill @s', 'particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.02 12', 'tp @s ~ ~-2000 ~', 'kill @s'])
    # every tick: his figure faces where he faces
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.mercpet] at @s on passengers run rotate @s ~ 0')
    # every second: retire stale copies, notice a fall, guard / scavenge, fight, shoot
    fn('p29/merc/has_vehicle', ['return run execute on vehicle if entity @s[type=minecraft:wolf]'])
    second += ['execute as @e[type=minecraft:wolf,tag=bm.mercpet] at @s run function bm:p29/merc/stale_check',
               'execute as @e[type=minecraft:item_display,tag=bm.m_body] unless function bm:p29/merc/has_vehicle run function bm:p29/merc/fell',
               'kill @e[type=minecraft:text_display,tag=bm.m_plate,predicate=!bm:p29/has_vehicle]',
               'execute as @a[scores={bm.mstate=1}] run function bm:p29/merc/fallen_check',
               'effect give @e[type=minecraft:wolf,tag=bm.mercpet] minecraft:regeneration 3 0 true',
               'execute as @e[type=minecraft:wolf,tag=bm.mercpet] at @s run function bm:p29/merc/think']
    wjson('bm/predicate/p29/has_vehicle.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:vehicle': {}}})   # 26.2 sub-predicate map
    fn('p29/merc/stale_check', ['execute store result storage bm:tmp ms.pid int 1 run scoreboard players get @s bm.pid',
                                'execute store result storage bm:tmp ms.g int 1 run scoreboard players get @s bm.mgen',
                                'execute store success score #st bm.pay run function bm:p29/merc/stale_m with storage bm:tmp ms',
                                'execute if score #st bm.pay matches 1 at @s run function bm:p29/merc/vanish'])
    fn('p29/merc/stale_m', ['$execute if data storage bm:merc {g:{p$(pid):$(g)}} run return fail', 'return 1'])
    # a body without its wolf: he fell (or was retired) - only a fall of the current generation counts
    fn('p29/merc/fell', ['execute store result storage bm:tmp mf.pid int 1 run scoreboard players get @s bm.pid',
                         'function bm:p29/merc/fell_m with storage bm:tmp mf', 'kill @s'])
    fn('p29/merc/fell_m', ['$data modify storage bm:merc f.p$(pid) set value 1b'])
    fn('p29/merc/fallen_check', ['execute store result storage bm:tmp mf.pid int 1 run scoreboard players get @s bm.pid',
                                 'execute store success score #fl bm.pay run function bm:p29/merc/fallen_m with storage bm:tmp mf',
                                 'execute if score #fl bm.pay matches 1 run function bm:p29/merc/fallen'])
    fn('p29/merc/fallen_m', ['$execute unless data storage bm:merc f.p$(pid) run return fail', '$data remove storage bm:merc f.p$(pid)', 'return 1'])
    fn('p29/merc/fallen', ['scoreboard players operation #p bm.pay = @s bm.pid', 'scoreboard players set #alive bm.pay 0',
                           f'{mine} run scoreboard players set #alive bm.pay 1',
                           'execute if score #alive bm.pay matches 1 run return 0',
                           'scoreboard players set @s bm.mstate 2',
                           tellraw('@s', PREFIX + [T(f'{MERC_NAME} has fallen! ', '#c0392b', bold=True),
                                                   T('The market rats carry him off to be patched up (2 Medallions, from the contract).', 'gray')])])
    hostile = 'type=#bm:hostile,type=!minecraft:creeper,tag=!bm.npc,tag=!bm.wil_body'
    fn('p29/merc/think', [
        'scoreboard players operation #p bm.pay = @s bm.pid',
        # guard: stay near the post, and stay put (no owner pull)
        'scoreboard players set #mode bm.pay 1',
        'execute as @a if score @s bm.pid = #p bm.pay run scoreboard players operation #mode bm.pay = @s bm.mmode',
        'execute if score #mode bm.pay matches 2 as @e[type=minecraft:marker,tag=bm.mpost] if score @s bm.pid = #p bm.pay run tag @s add bm.mpsel',
        'execute if score #mode bm.pay matches 2 unless entity @e[type=minecraft:marker,tag=bm.mpsel,distance=..8] run tp @s @e[type=minecraft:marker,tag=bm.mpsel,limit=1]',
        'execute if score #mode bm.pay matches 2 run data modify entity @s Sitting set value 0b',
        # pick a fight: the nearest monster within 10 (guard: within 12 of the post) if he has no target
        'execute unless function bm:p29/merc/has_target if score #mode bm.pay matches 2 at @e[type=minecraft:marker,tag=bm.mpsel,limit=1] as @e[' + hostile + ',distance=..12,sort=nearest,limit=1] run function bm:p29/merc/aggro',
        'execute unless function bm:p29/merc/has_target unless score #mode bm.pay matches 2 as @e[' + hostile + ',distance=..10,sort=nearest,limit=1] run function bm:p29/merc/aggro',
        'tag @e[type=minecraft:marker,tag=bm.mpsel] remove bm.mpsel',
        # crossbow: a bolt at anything he's after that's 4-16 blocks off
        'scoreboard players remove @s[scores={bm.mshot=1..}] bm.mshot 1',
        'execute unless score @s bm.mshot matches 1.. on target if entity @s[distance=4..16] run tag @s add bm.mtarget',
        'execute if entity @e[tag=bm.mtarget,limit=1] run function bm:p29/merc/shoot',
        'tag @e[tag=bm.mtarget] remove bm.mtarget',
        # scavenge
        'execute if score #mode bm.pay matches 3 run function bm:p29/merc/scavenge'])
    fn('p29/merc/has_target', ['return run execute on target if entity @s'])
    fn('p29/merc/aggro', ['tag @s add bm.mprey',
                          'execute as @e[type=minecraft:wolf,tag=bm.mercpet] if score @s bm.pid = #p bm.pay run function bm:p29/merc/aggro2',
                          'tag @s remove bm.mprey'])
    fn('p29/merc/aggro2', ['data modify entity @s angry_at set from entity @e[tag=bm.mprey,limit=1] UUID',
                           'execute store result score #gt bm.pay run time query gametime', 'scoreboard players add #gt bm.pay 400',
                           'execute store result entity @s anger_end_time long 1 run scoreboard players get #gt bm.pay'])
    # a bolt: from his eyes toward the target's eyes, 2 blocks a tick
    arrow = {'Tags': ['bm.mbolt'], 'pickup': B(0), 'damage': Dd(2.5), 'crit': B(1)}
    fn('p29/merc/shoot', ['scoreboard players set @s bm.mshot 2',
                          'execute positioned ~ ~0.6 ~ facing entity @e[tag=bm.mtarget,limit=1] eyes run function bm:p29/merc/bolt',
                          'playsound minecraft:item.crossbow.shoot neutral @a[distance=..20] ~ ~ ~ 0.8 1.3'])
    fn('p29/merc/bolt', [f'summon minecraft:arrow ^ ^ ^0.8 {snbt(arrow)}', 'summon minecraft:marker ^ ^ ^2.8 {Tags:["bm.maim"]}',
                         'execute store result score #ax bm.pay run data get entity @e[type=minecraft:arrow,tag=bm.mbolt,limit=1,sort=nearest] Pos[0] 1000',
                         'execute store result score #ay bm.pay run data get entity @e[type=minecraft:arrow,tag=bm.mbolt,limit=1,sort=nearest] Pos[1] 1000',
                         'execute store result score #az bm.pay run data get entity @e[type=minecraft:arrow,tag=bm.mbolt,limit=1,sort=nearest] Pos[2] 1000',
                         'execute store result score #bx bm.pay run data get entity @e[type=minecraft:marker,tag=bm.maim,limit=1,sort=nearest] Pos[0] 1000',
                         'execute store result score #by bm.pay run data get entity @e[type=minecraft:marker,tag=bm.maim,limit=1,sort=nearest] Pos[1] 1000',
                         'execute store result score #bz bm.pay run data get entity @e[type=minecraft:marker,tag=bm.maim,limit=1,sort=nearest] Pos[2] 1000',
                         'scoreboard players operation #bx bm.pay -= #ax bm.pay', 'scoreboard players operation #by bm.pay -= #ay bm.pay',
                         'scoreboard players operation #bz bm.pay -= #az bm.pay',
                         'execute as @e[type=minecraft:arrow,tag=bm.mbolt,limit=1,sort=nearest] run function bm:p29/merc/bolt_go',
                         'kill @e[type=minecraft:marker,tag=bm.maim]'])
    fn('p29/merc/bolt_go', ['execute store result entity @s Motion[0] double 0.001 run scoreboard players get #bx bm.pay',
                            'execute store result entity @s Motion[1] double 0.001 run scoreboard players get #by bm.pay',
                            'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #bz bm.pay',
                            'data modify entity @s Owner set from entity @e[type=minecraft:wolf,tag=bm.mshooter,limit=1] UUID', 'tag @s remove bm.mbolt'])
    G.FUNCS['p29/merc/shoot'].insert(0, 'tag @s add bm.mshooter')
    G.FUNCS['p29/merc/shoot'].append('tag @s remove bm.mshooter')
    # scavenging: loose items within 6 blocks go into his bag (9 stacks)
    fn('p29/merc/scavenge', ['execute store result storage bm:tmp sv.pid int 1 run scoreboard players get @s bm.pid',
                             'execute as @e[type=minecraft:item,distance=..6,nbt={PickupDelay:0s},limit=3] at @s run function bm:p29/merc/grab with storage bm:tmp sv'])
    fn('p29/merc/grab', ['$execute if data storage bm:merc bag.p$(pid)[8] run return 0',
                         '$data modify storage bm:merc bag.p$(pid) append from entity @s Item',
                         'particle minecraft:poof ~ ~0.2 ~ 0.1 0.1 0.1 0.01 4', 'kill @s'])
    fn('p29/merc/handover', ['execute store result storage bm:tmp sv.pid int 1 run scoreboard players get @s bm.pid',
                             'function bm:p29/merc/hand_m with storage bm:tmp sv',
                             title('@s', 'actionbar', T('"All yours, boss. I only kept the cheese."', '#c0392b', italic=True))])
    fn('p29/merc/hand_m', ['$execute unless data storage bm:merc bag.p$(pid)[0] run return 0',
                           '$data modify storage bm:tmp hv set from storage bm:merc bag.p$(pid)[0]',
                           '$data remove storage bm:merc bag.p$(pid)[0]',
                           'summon minecraft:item ~ ~0.5 ~ {Item:{id:"minecraft:stone",count:1},PickupDelay:0s,Tags:["bm.mhand"]}',
                           'data modify entity @e[type=minecraft:item,tag=bm.mhand,limit=1,sort=nearest] Item set from storage bm:tmp hv',
                           'tag @e[type=minecraft:item,tag=bm.mhand] remove bm.mhand',
                           '$function bm:p29/merc/hand_m {pid:$(pid)}'])
    G.FUNCS['admin/uninstall'][-1:-1] = ['kill @e[tag=bm.m_disp]']


# ===================================================================== RESOURCE PACK
def rp(R):
    from PIL import Image, ImageDraw
    g = R.grid
    I = R.ICONS
    I['ring_burrows'] = g(['................', '.....oooooo.....', '....oYYYYYYo....', '...oYyyyyyyYo...', '..oYyKdKdKdyYo..', '..oYy.......yYo.',
                           '..oY.........Yo.', '..oY.........Yo.', '..oY.........Yo.', '..oYy.......yYo.', '...oYy.....yYo..', '....oYyyyyyYo...',
                           '.....oYYYYYo....', '......ooooo.....', '................', '................'],
                          dict(o='#4a2f10', Y='#d4a35a', y='#a07030', K='#2a1a08', d='#ffe9a8'))
    I['pocket_rift'] = g(['................', '......KKKK......', '....KKcCCcKK....', '...KcCvvvvCcK...', '..KcCvVkkVvCcK..', '..KCvVkkkkVvCK..',
                          '.KcCvkkSkkkvCcK.', '.KCvVkkkkSkVvCK.', '.KCvVkSkkkkVvCK.', '.KcCvkkkkkkvCcK.', '..KCvVkkSkVvCK..', '..KcCvVkkVvCcK..',
                          '...KcCvvvvCcK...', '....KKcCCcKK....', '......KKKK......', '................'],
                         dict(K='#0b2b2a', c='#1f8f86', C='#4fd6c4', v='#2a6f9a', V='#3d3f8f', k='#08080f', S='#ffffff'))
    jar = ['................', '.....bbbbbb.....', '.....BBBBBB.....', '....gGGGGGGg....', '...gG......Gg...', '...g........g...', '...g........g...',
           '...g........g...', '...g........g...', '...g........g...', '...g........g...', '...gG......Gg...', '....gggggggg....', '................', '................', '................']
    I['smuggler_jar'] = g(jar, dict(b='#6b4a2a', B='#9a6e3e', g='#a8d8c8', G='#e8fff8'))
    full = [r[:4] + r[4:12].replace('.', 'm') + r[12:] if 4 <= i <= 11 else r for i, r in enumerate(jar)]
    I['smuggler_jar_full'] = g(full, dict(b='#6b4a2a', B='#9a6e3e', g='#a8d8c8', G='#e8fff8', m='#ffcf5a'))
    I['spawner_crowbar'] = g(['................', '.............rr.', '............rRr.', '...........rRr..', '..........rRr...', '.........rRr....',
                              '........rRr.....', '.......rRr......', '......rRr.......', '.....rRr........', '....rRr.........', '...rRr..........',
                              '..rRr...........', '.rRrr...........', '.rr.rr..........', '................'], dict(r='#3a3a46', R='#9a9aa8'))
    I['caged_spawner'] = g(['................', '..KKKKKKKKKKKK..', '..K.K..K..K..K..', '..KKKKKKKKKKKK..', '..K..rrrrrr..K..', '..K..rffffr..K..',
                            '..K..rfEEfr..K..', '..K..rfEEfr..K..', '..K..rffffr..K..', '..K..rrrrrr..K..', '..KKKKKKKKKKKK..', '..K.K..K..K..K..',
                            '..KKKKKKKKKKKK..', '................', '................', '................'],
                           dict(K='#2a2a35', r='#4a4a5a', f='#ff7a1a', E='#ffe08a'))
    I['lodestone_locket'] = g(['................', '.......cc.......', '......c..c......', '.......cc.......', '.....SSSSSS.....', '....SsLLLLsS....',
                               '...SsLlLLlLsS...', '...SLLLLLLLLS...', '...SLlLLLLlLS...', '...SsLLLLLLsS...', '....SsLLLLsS....', '.....SSSSSS.....',
                               '................', '................', '................', '................'],
                              dict(c='#8a8a96', S='#b0a0d0', s='#6a5a90', L='#3a3a4a', l='#7a7a8a'))
    I['bankers_card'] = g(['................', '................', '................', '.KKKKKKKKKKKKKK.', '.KyyyyyyyyyyyyK.', '.KyGGGyyyyyyyyK.',
                           '.KyGgGyyyyyyyyK.', '.KyGGGyyyyyyyyK.', '.KyyyyyyyyyyyyK.', '.KyddddddddyyyK.', '.KyyyyyyyyyyyyK.', '.KyddddyddddyyK.',
                           '.KKKKKKKKKKKKKK.', '................', '................', '................'],
                          dict(K='#6b5210', y='#e8d27a', G='#c9a227', g='#fff2b0', d='#8a7020'))
    I['fair_weather_bell'] = g(['................', '.......oo.......', '.......oo.......', '......YYYY......', '.....YyyyyY.....', '....YyyyyyyY....',
                                '....YyyyyyyY....', '....YyyyyyyY....', '...YyyyyyyyyY...', '...YyyyyyyyyY...', '..YYYYYYYYYYYY..', '..oooooooooooo..',
                                '.......YY.......', '......SSSS......', '.......SS.......', '................'],
                               dict(o='#6b4a1a', Y='#c9a227', y='#ffe08a', S='#9adfff'))
    I['merc_contract'] = g(['................', '..PPPPPPPPPPP...', '.PpppppppppppP..', '.PpkkkkkpppppP..', '.PppppppppppPP..', '.PpkkkkkkkkpP...',
                            '.PppppppppppP...', '.PpkkkkkkpppP...', '.PppppppppppP...', '.PpkkkkkppppP...', '.PppppppppRRP...', '.PpppppppRrrR...',
                            '..PPPPPPPRrrR...', '.........RRR....', '................', '................'],
                           dict(P='#8a6a3a', p='#f2e2b8', k='#5a4a3a', R='#c0392b', r='#ff6a5a'))
    I['rat_king_signet'] = g(['................', '................', '......Y.Y.Y.....', '......YYYYY.....', '.....OOOOOOO....', '....OYYYYYYYO...',
                              '...OYYkkkkkYYO..', '...OYkYYYYYkYO..', '...OYkYkYkYkYO..', '...OYkYYYYYkYO..', '...OYYkkkkkYYO..', '....OYYYYYYYO...',
                              '.....OOOOOOO....', '................', '................', '................'],
                             dict(Y='#ffb300', O='#7a4a00', k='#2a1a00'))
    I['brass_wing_scroll'] = g(['................', '..PPPPPPPPPPPP..', '..pBBBBBBBBBBp..', '...BbbbbbbbbB...', '...Bb.c..c.bB...', '...Bbcc..ccbB...',
                                '...Bcccc.cccB...', '...Bb.cc.cc.B...', '...Bb..cccc.B...', '...BbbbbbbbbB...', '..pBBBBBBBBBBp..', '..PPPPPPPPPPPP..',
                                '................', '................', '................', '................'],
                               dict(P='#8a5a2b', p='#c8963c', B='#f2e2b8', b='#e0cc98', c='#b07a2a'))
    I['market_crest_scroll'] = g(['................', '..PPPPPPPPPPPP..', '..pBBBBBBBBBBp..', '...BbbbbbbbbB...', '...Bb.kkkk.bB...', '...BbkYYYYkbB...',
                                  '...BbkYkkYkbB...', '...BbkYYYYkbB...', '...Bb.kYYk.bB...', '...Bbb.kk.bbB...', '..pBBBBBBBBBBp..', '..PPPPPPPPPPPP..',
                                  '................', '................', '................', '................'],
                                 dict(P='#8a5a2b', p='#c8963c', B='#f2e2b8', b='#e0cc98', k='#1a1a1a', Y='#ffcf3f'))
    I['rat_familiar'] = g(['................', '................', '....gg....gg....', '...gppg..gppg...', '...gggggggggg...', '..ggggggggggg...',
                           '..ggkgggggkgg...', '..gggggggggggg..', '...ggggpggggg...', '....gggggggg....', '.....gggggg.....', '......gggg......',
                           '.......pp.......', '........ppp.....', '..........pp....', '................'],
                          dict(g='#9a9aa4', p='#e8a0b0', k='#101010'))
    I['showstopper_charm'] = g(['................', '..r..........b..', '.......Y........', '......YYY...r...', '..b..YYYYY......', '...YYYYYYYYY....',
                                '....YYYYYYY.....', '.....YYYYY......', '....YYY.YYY..p..', '...YY.....YY....', '..p............b', '......r.........',
                                '...........p....', '................', '................', '................'],
                               dict(Y='#ffd700', r='#ff4a6a', b='#4ab0ff', p='#c070ff'))
    I['bidding_paddle'] = g(['................', '.....KKKKKK.....', '....KwwwwwwK....', '...KwwwwwwwwK...', '...KwwrrrrwwK...', '...KwwrwwrwwK...',
                             '...KwwrrrrwwK...', '...KwwrwwwwwK...', '...KwwrwwwwwK...', '....KwwwwwwK....', '.....KKbbKK.....', '.......bb.......',
                             '.......bb.......', '.......bb.......', '.......BB.......', '................'],
                            dict(K='#3a2a1a', w='#f2ead8', r='#c0392b', b='#8a5a2b', B='#5a3a1a'))
    I['wings_rat_king'] = royal_recolor(R, '/home/claude/bm_build/vendor/elytra_item.png')
    I['brass_wings'] = brass_recolor(R, '/home/claude/bm_build/vendor/elytra_item.png')
    # 3D: the Auroral Crown, the Donado statues, the rat variants
    R.HATS['auroral_crown'] = ({'p': 'minecraft:block/prismarine_bricks', 'a': 'minecraft:block/amethyst_block', 'g': 'minecraft:block/sea_lantern',
                                'w': 'minecraft:block/white_concrete'}, [
        R.cube((3, 15, 3), (13, 16.5, 4), 'p'), R.cube((3, 15, 12), (13, 16.5, 13), 'p'), R.cube((3, 15, 4), (4, 16.5, 12), 'p'), R.cube((12, 15, 4), (13, 16.5, 12), 'p'),
        *[R.cube((x, 16.5, 3), (x + 1, 19 + (x % 3), 4), 'a') for x in (3.5, 6, 8.5, 11)],
        *[R.cube((x, 16.5, 12), (x + 1, 18 + (x % 2), 13), 'a') for x in (3.5, 6, 8.5, 11)],
        R.cube((7.25, 16, 2.6), (8.75, 17.5, 3), 'g'), R.cube((7.5, 19, 3.2), (8.5, 21, 3.6), 'w')])
    import phase25
    cubes, dy, dz = phase25.donado_pose('crouch')
    plinth = [R.cube((1.5, 0, 1.5), (14.5, 1.5, 14.5), 'q'), R.cube((2.5, 1.5, 2.5), (13.5, 3, 13.5), 'u')]
    lifted = [R._mv(c, dy=3) for c in cubes]
    R.HATS['statue_donado'] = (dict(phase25.DON_TEX, q='minecraft:block/polished_blackstone', u='minecraft:block/chiseled_polished_blackstone'), plinth + lifted)
    gold_tex = {k: f'bm:block/{v.split("/")[-1]}_gold' for k, v in phase25.DON_TEX.items()}
    R.HATS['statue_donado_gold'] = (dict(gold_tex, q='minecraft:block/gold_block', u='minecraft:block/raw_gold_block'), plinth + lifted)
    R.P29_GOLD_TEX = list(phase25.DON_TEX.values())
    k = {'k2': 'minecraft:block/black_wool', 'rd': 'minecraft:block/red_wool', 'ir': 'minecraft:block/iron_block', 'br': 'minecraft:block/brown_wool',
         'gr': 'minecraft:block/gray_wool', 'gd': 'minecraft:block/gold_block', 'wh': 'minecraft:block/white_wool', 'pk': 'minecraft:block/pink_wool',
         'gn': 'minecraft:block/green_wool', 'lg': 'minecraft:block/light_gray_wool', 'pu': 'minecraft:block/purple_wool'}
    c = R.cube
    kits = {
        'auction': [c((4, 16, 4), (12, 17, 12), 'k'), c((5.5, 17, 5.5), (10.5, 22, 10.5), 'k'), c((5.5, 17, 5.4), (10.5, 18, 5.5), 'r'),
                    c((6.8, 10.3, 6.6), (9.2, 11.3, 7), 'r'), c((5, 6, 6.8), (11, 11, 10.7), 'k')],
        'concierge': [c((6.8, 10.3, 6.6), (9.2, 11.3, 7), 'k'), c((5, 6, 6.8), (11, 11, 10.7), 'r'), c((8.9, 13.6, 5.8), (10.5, 15.2, 5.9), 'y'),
                      c((7.5, 6.5, 6.7), (8.5, 10.5, 6.8), 'y')],
        'teller': [c((4.5, 15.5, 4.2), (11.5, 16.2, 9), 'd'), c((5, 16, 5.5), (11, 16.6, 10.5), 'w'), c((5, 6, 6.8), (11, 11, 10.7), 'w'),
                   c((6.8, 10.3, 6.6), (9.2, 11.3, 7), 'k')],
        'lord': [c((5.2, 16, 6), (10.8, 17, 10.5), 'y'), *[c((x, 17, 6), (x + 1, 18.5, 7), 'y') for x in (5.2, 7.5, 9.8)],
                 c((5, 6, 6.8), (11, 11, 10.7), 'p'), c((8.9, 13.6, 5.8), (10.5, 15.2, 5.9), 'y')],
        'madame': [c((4, 16, 4.5), (12, 16.8, 11.5), 'p'), c((5.5, 16.8, 6), (10.5, 18.5, 10), 'p'), c((10, 17, 8), (10.6, 21, 8.6), 'w'),
                   c((5, 6, 6.8), (11, 11, 10.7), 'p'), c((6, 10.4, 6.6), (10, 11, 6.9), 'w')],
        'grey': [c((4.5, 16, 5), (11.5, 16.6, 11), 'l'), c((5.5, 16.6, 6), (10.5, 19, 10), 'l'), c((5, 6, 6.8), (11, 11, 10.7), 'l'),
                 c((6.8, 10.3, 6.6), (9.2, 11.3, 7), 'k')],
        'merc': [c((4.8, 15.2, 5.6), (11.2, 16.4, 10.9), 'r'), c((10.5, 14.8, 9), (12.5, 15.8, 12), 'r'), c((5, 6.5, 6.6), (11, 10.8, 10.8), 'b'),
                 c((4.6, 9.6, 6.5), (11.4, 10.2, 10.9), 'k'), c((11.6, 3, 8), (12.2, 12, 8.6), 'o'), c((10.6, 9.5, 7.6), (13.4, 10.2, 9.2), 's'),
                 c((5.6, 13.7, 5.8), (7.2, 15.3, 5.85), 'k')],
        'familiar': [],
    }
    for v, kit in kits.items():
        R.RAT_KIT[v] = kit
        for p_ in R.RAT_POSES:
            R.HATS[f'rat3dp_{v}_{p_}'] = (R.RAT_TEX, R.rat_pose(v, p_))
        R.HATS[f'rat3d_{v}'] = (R.RAT_TEX, R.RAT_BASE + kit)


def royal_recolor(R, path):
    from PIL import Image
    im = Image.open(path).convert('RGBA')
    out = Image.new('RGBA', im.size)
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = im.getpixel((x, y))
            if a == 0: continue
            l = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            edge = any(im.getpixel((x + dx, y + dy))[3] == 0 if 0 <= x + dx < im.size[0] and 0 <= y + dy < im.size[1] else True
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge or l > 0.78:
                c0, c1 = (120, 70, 0), (255, 214, 60)
            else:
                c0, c1 = (8, 6, 10), (70, 40, 90)
            out.putpixel((x, y), tuple(int(c0[i] + (c1[i] - c0[i]) * l) for i in range(3)) + (a,))
    return out


def brass_recolor(R, path):
    from PIL import Image
    im = Image.open(path).convert('RGBA')
    out = Image.new('RGBA', im.size)
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = im.getpixel((x, y))
            if a == 0: continue
            l = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            c0, c1 = (60, 34, 10), (240, 196, 110)
            px = tuple(int(c0[i] + (c1[i] - c0[i]) * l) for i in range(3))
            if (x + 2 * y) % 7 == 0: px = tuple(max(0, v - 40) for v in px)          # rivet lines
            out.putpixel((x, y), px + (a,))
    return out


def rp_post(R):
    """Files the generic RP build doesn't make: equipment wings, the banner/shield crest, the painting, gold Donado
    textures, lang lines."""
    from PIL import Image, ImageDraw
    import json, os
    p = R.p
    # equipment: Wings of the Rat King, brass wings
    royal_recolor(R, '/home/claude/bm_build/vendor/elytra_wings.png').save(p('assets', 'bm', 'textures', 'entity', 'equipment', 'wings', 'wings_rat_king.png'))
    R.wj('assets/bm/equipment/wings_rat_king.json', {'layers': {'wings': [{'texture': 'bm:wings_rat_king'}]}})
    brass_recolor(R, '/home/claude/bm_build/vendor/elytra_wings.png').save(p('assets', 'bm', 'textures', 'entity', 'equipment', 'wings', 'brass_wings.png'))
    R.wj('assets/bm/equipment/brass_wings.json', {'layers': {'wings': [{'texture': 'bm:brass_wings'}]}})
    # the market crest: a rat skull over two crossed keys (white + alpha: the game tints it)
    def crest(w, h, ox, oy):
        im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        W_ = (255, 255, 255, 255)
        cx = ox + w / 2
        s = w / 20.0
        # crossed keys
        d.line((ox + 3 * s, oy + h * 0.55, ox + w - 3 * s, oy + h * 0.92), fill=W_, width=max(1, int(1.6 * s)))
        d.line((ox + w - 3 * s, oy + h * 0.55, ox + 3 * s, oy + h * 0.92), fill=W_, width=max(1, int(1.6 * s)))
        for kx in (ox + 2 * s, ox + w - 5 * s):
            d.ellipse((kx, oy + h * 0.52 - 2 * s, kx + 3.2 * s, oy + h * 0.52 + 1.2 * s), outline=W_, width=1)
        # the skull: round head, two ears, dark eyes and nose
        d.ellipse((cx - 5.5 * s, oy + h * 0.16, cx + 5.5 * s, oy + h * 0.16 + 10 * s), fill=W_)
        d.ellipse((cx - 7.5 * s, oy + h * 0.10, cx - 3.5 * s, oy + h * 0.10 + 4 * s), fill=W_)
        d.ellipse((cx + 3.5 * s, oy + h * 0.10, cx + 7.5 * s, oy + h * 0.10 + 4 * s), fill=W_)
        d.polygon([(cx - 2.5 * s, oy + h * 0.16 + 9 * s), (cx + 2.5 * s, oy + h * 0.16 + 9 * s), (cx, oy + h * 0.16 + 13 * s)], fill=W_)
        for ex in (cx - 3 * s, cx + 1 * s):
            d.rectangle((ex, oy + h * 0.16 + 3.5 * s, ex + 2 * s, oy + h * 0.16 + 5.5 * s), fill=(0, 0, 0, 0))
        d.rectangle((cx - 0.6 * s, oy + h * 0.16 + 9 * s, cx + 0.6 * s, oy + h * 0.16 + 10 * s), fill=(0, 0, 0, 0))
        return im
    crest(20, 40, 1, 1).save(p('assets', 'bm', 'textures', 'entity', 'banner', 'rat_crest.png'))
    crest(12, 22, 1, 1).save(p('assets', 'bm', 'textures', 'entity', 'shield', 'rat_crest.png'))
    # the Rat Gang Portrait (2x2: 32x32): three rats round a lantern-lit table, in a gilt frame
    im = Image.new('RGBA', (32, 32), R.hexc('#2a1a12'))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 31, 31), outline=R.hexc('#c8a050')); d.rectangle((1, 1, 30, 30), outline=R.hexc('#7a5a20'))
    d.rectangle((2, 2, 29, 12), fill=R.hexc('#3a2418'))
    d.ellipse((13, 4, 18, 9), fill=R.hexc('#ffcf5a')); d.line((15, 2, 15, 4), fill=R.hexc('#555555'))
    d.rectangle((4, 22, 27, 25), fill=R.hexc('#5a3a1a')); d.rectangle((6, 26, 7, 29), fill=R.hexc('#3a2410')); d.rectangle((24, 26, 25, 29), fill=R.hexc('#3a2410'))
    for (x, col, hat) in ((6, '#9a9aa4', '#1a1a1a'), (13, '#8a8a94', '#c0392b'), (20, '#a0a0aa', '#2a6a2a')):
        d.ellipse((x, 13, x + 6, 20), fill=R.hexc(col))                     # head
        d.ellipse((x - 1, 11, x + 2, 14), fill=R.hexc(col)); d.ellipse((x + 4, 11, x + 7, 14), fill=R.hexc(col))   # ears
        d.point((x + 2, 16), fill=R.hexc('#101010')); d.point((x + 4, 16), fill=R.hexc('#101010'))
        d.point((x + 3, 18), fill=R.hexc('#e8a0b0'))
        d.rectangle((x + 1, 10, x + 5, 11), fill=R.hexc(hat))                # hats
        d.rectangle((x, 20, x + 6, 22), fill=R.hexc(col))                    # shoulders
    d.ellipse((14, 21, 17, 23), fill=R.hexc('#ffd84a'))                      # a wheel of cheese on the table
    im.save(p('assets', 'bm', 'textures', 'painting', 'rat_gang.png'))
    # gold Donado textures
    import phase25
    tex = phase25.textures()
    for full in R.P29_GOLD_TEX:
        name = full.split('/')[-1]
        if name not in tex: continue
        src = tex[name].convert('RGBA')
        out = Image.new('RGBA', src.size)
        for y in range(src.size[1]):
            for x in range(src.size[0]):
                r, g, b, a = src.getpixel((x, y))
                l = (0.3 * r + 0.59 * g + 0.11 * b) / 255
                c0, c1 = (70, 40, 0), (255, 222, 90)
                out.putpixel((x, y), tuple(int(c0[i] + (c1[i] - c0[i]) * l) for i in range(3)) + (a,))
        out.save(p('assets', 'bm', 'textures', 'block', name + '_gold.png'))
    # lang: the crest's name on a shield tooltip
    lp = p('assets', 'bm', 'lang', 'en_us.json')
    lang = json.load(open(lp)) if os.path.exists(lp) else {}
    for c in ('white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown',
              'green', 'red', 'black'):
        lang[f'block.bm.banner.rat_crest.{c}'] = ' '.join(w.capitalize() for w in c.split('_')) + ' Black Market Crest'
    json.dump(lang, open(lp, 'w'), indent=1)

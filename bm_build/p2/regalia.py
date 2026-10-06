"""2.20: THE HOLLOW KING'S REGALIA - the old Conqueror's set, renamed and woken up, and SEPULCHRE, his maul.

- Every piece and tool from the Hollow King's vault has a darker name (same ids: copies already in worlds are re-synced).
- The Ribcage makes its wearer immune to Withering (the effect still shows; it does no harm).
- The full Regalia WAKES with the world around it (strength numbers are on top of the per-piece effects):
    night (Overworld)      +15% damage                                   amethyst trim, rising souls
    full or new moon       +30% damage, +10% speed                       diamond trim, a crown of soul fire
    Blood Moon             +50% damage, +15% speed, +1.5 reach,          redstone trim, dripping blood
                           Strength II, Regeneration II, kills heal
    Invasion Night         +50% damage, +15% speed, Resistance II,       emerald trim, crackling green sparks
                           +6 armour, Vorn plasma barely scratches
    the Nether / the Hollow Throne  +30% damage, Strength II, +4 armour  gold trim, embers and ash
  The trims really change colour while it's awake (and settle back to quartz when it sleeps).
- WITHER NOVA (full Regalia): crouch and look up at the sky for a second - every monster and every other player within
  8 blocks withers (Wither II, 8 s). 40 s to gather again (25 s at night or under the moons, 15 s on a Blood Moon, an
  Invasion Night or at home).
- SEPULCHRE (the Hollow King's vault): a maul. Right-click: GRAVE QUAKE - the ground heaves within 7 blocks, monsters are
  thrown into the air and wither, other players are lifted and wither. 15 s (10 s / 6 s when the Regalia's power is up,
  whether or not you wear it). A smash attack (falling onto a target) sends a smaller quake for free."""
from items import ITEMS, gear, attr, ench, T, weapon_attrs, ARMOR_SLOT
from useitem import hold, HOLD
from nbt import Int
import math

COL = '#9a5ae0'
SKULL = 'dark_red'
ARMOR = {'helmet': (4, 'Deathmask of the Hollow King', 'Night Vision, Water Breathing'),
         'chestplate': (10, 'Ribcage of the Hollow King', 'Strength I, Resistance I'),
         'leggings': (8, 'Wither-Wrought Greaves', 'Regeneration I, Haste I'),
         'boots': (4, 'Tombstride Treads', 'Speed I, Fire Resistance')}
TOOLS = {'conq_blade': ('Soulreaver', 'Strength I while held'), 'conq_pick': ("Gravedigger's Maw", 'Haste II while held'),
         'conq_axe': ("Headsman's Grief", 'Strength I while held'), 'conq_shovel': ('Barrow Spade', 'Haste II while held'),
         'conq_bow': ('Witherstring', 'Speed I while held')}
REGALIA_LORE = [('Full Regalia: the dead keep their distance,', 'dark_aqua'), ('and it wakes at night - fiercer under the', 'dark_aqua'),
                ('moons, a Blood Moon, an Invasion, or at home.', 'dark_aqua'),
                ('Crouch and look to the sky: a Wither Nova.', 'dark_purple')]
TRIM = {0: 'quartz', 1: 'amethyst', 2: 'diamond', 3: 'redstone', 4: 'emerald', 5: 'gold'}
SLOT = {'helmet': 'armor.head', 'chestplate': 'armor.chest', 'leggings': 'armor.legs', 'boots': 'armor.feet'}


def evil_name(iid, name):
    ITEMS[iid]['comps']['minecraft:item_name'] = {'text': '', 'italic': False, 'extra': [
        {'text': '☠ ', 'color': SKULL}, {'text': name, 'color': COL, 'bold': True}, {'text': ' ☠', 'color': SKULL}]}
    ITEMS[iid]['name'] = name


def register():
    from p2.p2items import CONQ_TOOLS
    for p, (armor, nm, fx) in ARMOR.items():
        s = ARMOR_SLOT[p]
        lore = ["Torn from the Hollow King's corpse.", (f'While worn: {fx}', 'blue'), ('+4 Max Health. Unbreakable.', 'blue')]
        if p == 'chestplate':
            lore.append(('Withering cannot touch you.', 'dark_purple'))
        en = {**ench(protection=10, thorns=3), **({'boots': ench(feather_falling=6), 'helmet': ench(respiration=5),
                                                  'leggings': ench(swift_sneak=5)}.get(p, {}))}
        if p == 'chestplate':
            en['bm:hollow_blood'] = 1
        gear(f'conq_{p}', f'netherite_{p}', nm, COL, lore + REGALIA_LORE, en, 3,
             attrs=[attr('armor', armor, s, ident=f'minecraft:armor.{p}'), attr('armor_toughness', 5, s, ident=f'minecraft:armor.{p}_toughness'),
                    attr('knockback_resistance', 0.2, s, ident=f'minecraft:armor.{p}_kb'), attr('max_health', 4, s)],
             extra={'minecraft:unbreakable': {}, 'minecraft:trim': {'material': 'minecraft:quartz', 'pattern': 'minecraft:silence'}},
             custom_extra={'bm_set': 'conqueror'}, bold=True)
        evil_name(f'conq_{p}', nm)
    for iid, base, _nm, en, wb, bonus in CONQ_TOOLS:
        nm, held = TOOLS[iid]
        gear(iid, base, nm, COL, ["Wrenched from the Hollow King's throne.", (held + '. Unbreakable.', 'blue')], en, 3,
             attrs=weapon_attrs(wb, bonus) if wb else None, extra={'minecraft:unbreakable': {}}, custom_extra={'bm_held': iid}, bold=True)
        evil_name(iid, nm)
    mace_en = dict(ench(density=5, breach=4, smite=6, fire_aspect=2), **{'bm:grave_quake': 1})
    gear('sepulchre', 'mace', 'Sepulchre', COL,
         ["The Hollow King's maul. Every grave it", 'struck stayed open.',
          ('Right-click: Grave Quake - the ground heaves', 'blue'), ('within 7 blocks: monsters are thrown up and', 'blue'),
          ('wither; other players are lifted and wither.', 'blue'), ('A smash attack sends a smaller quake.', 'blue'),
          ('Its cooldown shortens when the Regalia wakes.', 'dark_aqua'), ('Unbreakable.', 'blue')],
         mace_en, 3, attrs=weapon_attrs('mace', 6), model='bm:sepulchre',
         extra=dict(hold('none'), **{'minecraft:unbreakable': {}}), bold=True)
    evil_name('sepulchre', 'Sepulchre')
    HOLD['sepulchre'] = 'bm:p2/rg/mace_use'


register()


def _ring(r, n, y, part):
    return [f'particle {part} ~{r * math.cos(2 * math.pi * i / n):.2f} ~{y} ~{r * math.sin(2 * math.pi * i / n):.2f} 0.05 0.05 0.05 0.01 1' for i in range(n)]


def generate(G, B=None):
    fn, wjson, title, T_ = G.fn, G.wjson, G.title, T
    near = 'gamemode=!creative,gamemode=!spectator'
    fast, second, load = [], [], []
    objs = ['bm.rgt', 'bm.rgu', 'bm.rgc', 'bm.mqc', 'bm.msq', 'bm.rgr']
    load += [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ---------------- registry bits: the Ribcage's immunity, the maul's smash
    wjson('bm/tags/damage_type/withering.json', {'values': ['minecraft:wither', 'minecraft:wither_skull']})
    wjson('bm/tags/damage_type/vorn_plasma.json', {'values': ['bm:plasma']})
    base = {'anvil_cost': 8, 'max_level': 1, 'weight': 1, 'min_cost': {'base': 1, 'per_level_above_first': 0},
            'max_cost': {'base': 1, 'per_level_above_first': 0}}
    wjson('bm/enchantment/hollow_blood.json', dict(base, description=T_('Hollow Blood', COL), slots=['chest'],
                                                   supported_items='#minecraft:enchantable/chest_armor', effects={
        'minecraft:damage_immunity': [{'effect': {}, 'requirements': {'condition': 'minecraft:damage_source_properties', 'predicate': {
            'tags': [{'id': '#bm:withering', 'expected': True}, {'id': '#minecraft:bypasses_invulnerability', 'expected': False}]}}}],
        'minecraft:damage_protection': [{'effect': {'type': 'minecraft:add', 'value': 20}, 'requirements': {'condition': 'minecraft:all_of', 'terms': [
            {'condition': 'minecraft:damage_source_properties', 'predicate': {'tags': [{'id': '#bm:vorn_plasma', 'expected': True}]}},
            {'condition': 'minecraft:entity_scores', 'entity': 'this', 'scores': {'bm.rgt': 4}}]}}]}))
    wjson('bm/enchantment/grave_quake.json', dict(base, description=T_('Grave Quake', COL), slots=['mainhand'],
                                                  supported_items='#minecraft:enchantable/mace', effects={
        'minecraft:post_attack': [{'affected': 'attacker', 'enchanted': 'attacker',
                                   'effect': {'type': 'minecraft:run_function', 'function': 'bm:p2/rg/smash'},
                                   'requirements': {'condition': 'minecraft:entity_properties', 'entity': 'direct_attacker', 'predicate': {
                                       'minecraft:flags': {'is_flying': False}, 'minecraft:movement': {'fall_distance': {'min': 2.5}}}}}]}))

    # ---------------- the Regalia's mood: 0 asleep, 1 night, 2 moons, 3 Blood Moon, 4 Invasion, 5 at home (Nether / Hollow Throne)
    fn('p2/rg/tier', ['scoreboard players set #rg bm.rng 0',
                      'execute if dimension minecraft:overworld run scoreboard players operation #rg bm.rng = #hpw bm.bm',
                      'execute if dimension minecraft:overworld if score #inv bm.bm matches 1 unless score #rg bm.rng matches 3 run scoreboard players set #rg bm.rng 4',
                      'execute if dimension minecraft:the_nether run scoreboard players set #rg bm.rng 5',
                      'execute if dimension bm:hollow_throne run scoreboard players set #rg bm.rng 5'])
    mods = {1: [('attack_damage', 'bm:rg_power', 0.15, 'add_multiplied_total')],
            2: [('attack_damage', 'bm:rg_power', 0.3, 'add_multiplied_total'), ('movement_speed', 'bm:rg_speed', 0.1, 'add_multiplied_base')],
            3: [('attack_damage', 'bm:rg_power', 0.5, 'add_multiplied_total'), ('movement_speed', 'bm:rg_speed', 0.15, 'add_multiplied_base'),
                ('entity_interaction_range', 'bm:rg_reach', 1.5, 'add_value')],
            4: [('attack_damage', 'bm:rg_power', 0.5, 'add_multiplied_total'), ('movement_speed', 'bm:rg_speed', 0.15, 'add_multiplied_base'),
                ('armor', 'bm:rg_armor', 6, 'add_value')],
            5: [('attack_damage', 'bm:rg_power', 0.3, 'add_multiplied_total'), ('armor', 'bm:rg_armor', 4, 'add_value')]}
    clear = [f'attribute @s minecraft:{a} modifier remove {i}' for a, i in
             [('attack_damage', 'bm:rg_power'), ('movement_speed', 'bm:rg_speed'), ('entity_interaction_range', 'bm:rg_reach'), ('armor', 'bm:rg_armor')]]
    for t, ms in mods.items():
        fn(f'p2/rg/mods_{t}', [f'attribute @s minecraft:{a} modifier add {i} {v} {op}' for a, i, v, op in ms])
    fn('p2/rg/second', ['tag @s add bm.rgon', 'function bm:p2/rg/tier',
                        'execute unless score @s bm.rgt = #rg bm.rng run function bm:p2/rg/wake'] + clear +
       [f'execute if score #rg bm.rng matches {t} run function bm:p2/rg/mods_{t}' for t in mods] +
       ['execute if score #rg bm.rng matches 3 run effect give @s minecraft:strength 3 1 true',
        'execute if score #rg bm.rng matches 5 run effect give @s minecraft:strength 3 1 true',
        'execute if score #rg bm.rng matches 4 run effect give @s minecraft:resistance 3 1 true',
        'execute if score #rg bm.rng matches 3 run scoreboard players add @s bm.rgr 1',
        'execute if score #rg bm.rng matches 3 if score @s bm.rgr matches 3.. run effect give @s minecraft:regeneration 4 1 true',
        'execute if score @s bm.rgr matches 3.. run scoreboard players set @s bm.rgr 0'])
    # waking (or settling): the trims change colour, a word about it
    msgs = {0: ('The Regalia settles into sleep.', 'gray'), 1: ('The Regalia stirs under the night.', '#b48ae8'),
            2: ('The moon wakes the Regalia. It hungers.', '#a8d8ff'), 3: ('The Regalia drinks the Blood Moon!', 'dark_red'),
            4: ('The Regalia hungers for the Vorn!', '#5aff7a'), 5: ('The Regalia is home. It remembers its king.', 'gold')}
    for t, mat in TRIM.items():
        comps = '{"minecraft:trim":{material:"minecraft:%s",pattern:"minecraft:silence"}}' % mat
        fn(f'p2/rg/trim_{t}', [f'item modify entity @s {sl} {{function:"minecraft:set_components",components:{comps}}}' for sl in SLOT.values()] +
           [title('@s', 'actionbar', T_(msgs[t][0], msgs[t][1], italic=True))])
    fn('p2/rg/wake', [f'execute if score #rg bm.rng matches {t} run function bm:p2/rg/trim_{t}' for t in TRIM] +
       ['scoreboard players operation @s bm.rgt = #rg bm.rng',
        'execute if score #rg bm.rng matches 1.. run playsound minecraft:entity.wither.ambient player @s ~ ~ ~ 0.4 0.6',
        'execute if score #rg bm.rng matches 1.. run particle minecraft:sculk_soul ~ ~1 ~ 0.4 0.8 0.4 0.03 20'])
    # off (a piece came off): the power drains within a quarter second; the trims stay as they were until it's worn again
    fn('p2/rg/off', ['tag @s remove bm.rgon', *clear, 'scoreboard players reset @s bm.rgt'])
    # the cosmetics while it's awake
    fx = {1: ['particle minecraft:sculk_soul ~ ~0.4 ~ 0.3 0.2 0.3 0.02 1', 'particle minecraft:smoke ~ ~1.9 ~ 0.2 0.1 0.2 0.005 1'],
          2: ['particle minecraft:sculk_soul ~ ~0.4 ~ 0.3 0.2 0.3 0.02 1'] + [l for l in _ring(0.32, 5, 2.25, 'minecraft:soul_fire_flame')],
          3: ['particle minecraft:dust{color:[0.6,0.0,0.03],scale:1.3} ~ ~1.2 ~ 0.3 0.5 0.3 0 3', 'particle minecraft:dripping_lava ~ ~1.4 ~ 0.25 0.3 0.25 0 1',
              'particle minecraft:crimson_spore ~ ~1 ~ 0.6 0.6 0.6 0 3'],
          4: ['particle minecraft:dust{color:[0.3,1.0,0.45],scale:1.0} ~ ~1 ~ 0.35 0.6 0.35 0 3', 'particle minecraft:electric_spark ~ ~1.2 ~ 0.4 0.6 0.4 0.05 2',
              'particle minecraft:glow ~ ~1 ~ 0.4 0.5 0.4 0 1'],
          5: ['particle minecraft:flame ~ ~0.6 ~ 0.3 0.4 0.3 0.01 1', 'particle minecraft:ash ~ ~2 ~ 0.6 0.4 0.6 0 4', 'particle minecraft:small_flame ~ ~2.1 ~ 0.25 0.05 0.25 0 1']}
    for t, ls in fx.items():
        fn(f'p2/rg/fx_{t}', ls)
    fn('p2/rg/fast', [f'execute if score @s bm.rgt matches {t} run function bm:p2/rg/fx_{t}' for t in fx] + ['function bm:p2/rg/gesture'])

    # ---------------- WITHER NOVA: crouch, look to the sky for a second
    fn('p2/rg/gesture', ['execute unless predicate bm:p20/sneaking run return run scoreboard players set @s bm.rgu 0',
                         'execute unless entity @s[x_rotation=-90..-55] run return run scoreboard players set @s bm.rgu 0',
                         'scoreboard players add @s bm.rgu 5',
                         'execute if score @s bm.rgu matches 5..15 run particle minecraft:sculk_soul ~ ~2.2 ~ 0.3 0.2 0.3 0.01 2',
                         'execute if score @s bm.rgu matches 20 run function bm:p2/rg/nova_try'])
    fn('p2/rg/nova_try', ['execute if score @s bm.rgc matches 1.. run return run function bm:p2/rg/nova_wait', 'function bm:p2/rg/tier',
                          'scoreboard players set @s bm.rgc 800',
                          'execute if score #rg bm.rng matches 1..2 run scoreboard players set @s bm.rgc 500',
                          'execute if score #rg bm.rng matches 3.. run scoreboard players set @s bm.rgc 300',
                          'tag @s add bm.rgme',
                          *[l for r, n in [(2, 12), (4, 20), (6, 28), (8, 36)] for l in _ring(r, n, 0.4, 'minecraft:large_smoke')],
                          *[l for r, n in [(3, 16), (5, 24), (7, 32)] for l in _ring(r, n, 0.8, 'minecraft:sculk_soul')],
                          'particle minecraft:dust{color:[0.08,0.02,0.1],scale:3.0} ~ ~1 ~ 3 1 3 0 80',
                          'playsound minecraft:entity.wither.shoot player @a[distance=..32] ~ ~ ~ 1.4 0.5',
                          'playsound minecraft:entity.wither.spawn player @a[distance=..32] ~ ~ ~ 0.5 1.2',
                          'execute as @e[type=#bm:p42_foe,distance=..8] at @s run function bm:p2/rg/wither',
                          f'execute as @a[distance=..8,tag=!bm.rgme,{near}] at @s run function bm:p2/rg/wither',
                          'tag @s remove bm.rgme', title('@s', 'actionbar', T_('WITHER NOVA', COL, bold=True))])
    fn('p2/rg/wither', ['effect give @s minecraft:wither 8 1', 'damage @s 4 minecraft:magic by @a[tag=bm.rgme,limit=1]',
                        'particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.6 0.3 0.02 6'])
    fn('p2/rg/nova_wait', ['scoreboard players operation #s bm.rng = @s bm.rgc', 'scoreboard players add #s bm.rng 19', 'scoreboard players operation #s bm.rng /= #20 bm.rng',
                           title('@s', 'actionbar', [T_('The Regalia is still gathering death... ', 'gray'), {'score': {'name': '#s', 'objective': 'bm.rng'}, 'color': 'white'}, T_(' s', 'gray')])])

    # ---------------- SEPULCHRE: Grave Quake on right-click, a smaller one on a smash
    fn('p2/rg/mace_use', ['execute if score @s bm.mqc matches 1.. run return run function bm:p2/rg/mace_wait', 'function bm:p2/rg/tier',
                          'scoreboard players set @s bm.mqc 300',
                          'execute if score #rg bm.rng matches 1..2 run scoreboard players set @s bm.mqc 200',
                          'execute if score #rg bm.rng matches 3.. run scoreboard players set @s bm.mqc 120',
                          'function bm:p2/rg/quake_7'])
    fn('p2/rg/mace_wait', ['scoreboard players operation #s bm.rng = @s bm.mqc', 'scoreboard players add #s bm.rng 19', 'scoreboard players operation #s bm.rng /= #20 bm.rng',
                           title('@s', 'actionbar', [T_('The ground is still settling... ', 'gray'), {'score': {'name': '#s', 'objective': 'bm.rng'}, 'color': 'white'}, T_(' s', 'gray')])])
    fn('p2/rg/smash', ['execute if score @s bm.msq matches 1.. run return 0', 'scoreboard players set @s bm.msq 20', 'function bm:p2/rg/tier', 'function bm:p2/rg/quake_4'])
    for r in (7, 4):
        rings = [(k, 8 + 4 * k) for k in range(2, r + 1, 2)]
        fn(f'p2/rg/quake_{r}', ['tag @s add bm.rgme',
                                'scoreboard players set #qd bm.rng 8', 'execute if score #rg bm.rng matches 1..2 run scoreboard players set #qd bm.rng 10',
                                'execute if score #rg bm.rng matches 3.. run scoreboard players set #qd bm.rng 13',
                                'execute store result storage bm:tmp rg.d int 1 run scoreboard players get #qd bm.rng',
                                *[l for k, n in rings for l in _ring(k, n, 0.1, 'minecraft:block{block_state:"minecraft:deepslate"}')],
                                *[l for k, n in rings for l in _ring(k, n, 0.5, 'minecraft:sculk_soul')],
                                'particle minecraft:explosion ~ ~0.5 ~ 1 0.2 1 0 4',
                                'playsound minecraft:item.mace.smash_ground_heavy player @a[distance=..32] ~ ~ ~ 1.5 0.6',
                                'playsound minecraft:entity.wither.break_block player @a[distance=..32] ~ ~ ~ 0.6 0.6',
                                'playsound minecraft:entity.generic.explode player @a[distance=..32] ~ ~ ~ 0.8 0.5',
                                f'execute as @e[type=#bm:p42_foe,distance=..{r},tag=!bm.boss] at @s run function bm:p2/rg/launch',
                                f'execute as @e[type=#bm:p42_foe,distance=..{r},tag=bm.boss] at @s run function bm:p2/rg/shake with storage bm:tmp rg',
                                f'execute as @a[distance=..{r},tag=!bm.rgme,{near}] at @s run function bm:p2/rg/lift',
                                'tag @s remove bm.rgme'])
    fn('p2/rg/launch', ['data modify entity @s Motion[1] set value 1.05d', 'function bm:p2/rg/shake with storage bm:tmp rg',
                        'particle minecraft:block{block_state:"minecraft:deepslate"} ~ ~0.2 ~ 0.4 0.1 0.4 0 10'])
    fn('p2/rg/shake', ['$damage @s $(d) minecraft:magic by @a[tag=bm.rgme,limit=1]', 'effect give @s minecraft:wither 6 1'])
    fn('p2/rg/lift', ['effect give @s minecraft:levitation 1 4 true', 'function bm:p2/rg/shake with storage bm:tmp rg'])

    # ---------------- Blood Moon kills heal the Regalia's wearer
    wjson('bm/advancement/p2/rg_kill.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
        'player': [{'condition': 'minecraft:entity_scores', 'entity': 'this', 'scores': {'bm.rgt': 3}}],
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': '#bm:p42_foe'}}]}}},
        'rewards': {'function': 'bm:p2/rg/kill'}})
    fn('p2/rg/kill', ['advancement revoke @s only bm:p2/rg_kill', 'execute unless entity @s[tag=bm.rgon] run return 0',
                      'effect give @s minecraft:instant_health 1 0 true', 'particle minecraft:dust{color:[0.6,0.0,0.03],scale:1.4} ~ ~1 ~ 0.3 0.5 0.3 0 10'])

    second += ['execute as @a[gamemode=!spectator] if function bm:p2/sets/has/conqueror at @s run function bm:p2/rg/second']
    fast += ['execute as @a[tag=bm.rgon] unless function bm:p2/sets/has/conqueror run function bm:p2/rg/off',
             'execute as @a[tag=bm.rgon] at @s run function bm:p2/rg/fast',
             'scoreboard players remove @a[scores={bm.rgc=1..}] bm.rgc 5', 'scoreboard players remove @a[scores={bm.mqc=1..}] bm.mqc 5',
             'scoreboard players remove @a[scores={bm.msq=1..}] bm.msq 5']
    fn('admin/p2/regalia', [G.give(i) for i in ['conq_helmet', 'conq_chestplate', 'conq_leggings', 'conq_boots', 'sepulchre', 'conq_blade', 'conq_pick', 'conq_axe', 'conq_shovel', 'conq_hoe', 'conq_bow', 'hollow_wings']])
    return {'fast': fast, 'second': second, 'load': load}


def rp(R):
    """Sepulchre: the vanilla mace, darkened to bone and bruise."""
    import io, zipfile
    from PIL import Image
    with zipfile.ZipFile('/home/claude/mc263/client.jar') as z:
        im = Image.open(io.BytesIO(z.read('assets/minecraft/textures/item/mace.png'))).convert('RGBA')
    out = Image.new('RGBA', im.size, (0, 0, 0, 0))
    lo, hi = (24, 12, 34), (196, 150, 240)
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = im.getpixel((x, y))
            if a == 0: continue
            t = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            out.putpixel((x, y), tuple(int(lo[i] + (hi[i] - lo[i]) * t) for i in range(3)) + (a,))
    R.ICONS['sepulchre'] = out
    R.HANDHELD_EXTRA.add('sepulchre')

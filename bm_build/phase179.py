"""2.84c: THE ARMOUR REBALANCE, ALIEN GEAR AND THE PARTNER WHEEL.

THE ARMOUR REBALANCE   Hero of Time stays the strongest Black Market set (20 armour, 16 toughness, +16 health), but the
              others close in, each keeping its own trade-off and set bonus:
                Shadowstep III   +1 toughness, +2 health a piece  (20/12/8 - still the light, quick set)
                Architect III    +1 toughness, +3 health a piece  (20/16/12)     Tidecaller III  the same (20/16/12)
                Crimson Revenant +1 toughness, +2 health a piece  (20/16/16)     Vampire Lord    the same (20/16/12)
                Dawnbringer      +1 toughness, +2 health a piece  (20/16/12)
              Their reforged successors (Vesper) gain the same. Copies already in worlds are re-synced (item version 41) - and
              that re-sync now keeps a piece's Dread tunings and its auction infusion (it used to wipe them).
ALIEN GEAR (Zorp)   DONADIAN XENOPLATE  four pieces of teal alien plate (20 armour, 14 toughness, +8 health): full set,
                      Jump Boost I, Night Vision and a Deflector - two hearts of shield that recharge every 40 seconds.
                    PLASMA CUTTER (green): every hit burns green and lights the foe up.  GRAVITON EDGE (violet): one hit in four
                      throws the foe into the air.  PHASE SABER (cyan): quicker, and one hit in five cuts straight through armour.
              HARD MODE (Zorp's stock grows once the world is in hard mode):
                    VORN WARPLATE  red war plate (20 armour, 18 toughness, +12 health): full set, above half health Strength
                      and Speed; under a third, a Shockwave throws back and hurts every monster within 5 blocks (a minute's rest).
                    VORN ANNIHILATOR  a heavy, slow greatsword; one hit in four arcs to three more monsters.
                    GRAVITON PICK  mines at full speed underwater, a quarter faster everywhere.
                    DONADIAN ANTENNAE (a hat) and TRACTOR-BEAM TREADS (a trail) - cosmetics.
THE PARTNER WHEEL (Cecil, 3 Medallions)   every partner on one item. Hold a partner's summoning item in your off hand and use
              the wheel: it goes on. Use the wheel alone: call any partner on it, send them home, or take their item back
              out. While you carry the wheel, its partners count as with you (they don't go home, they come back after a
              faint, the ones you've met don't turn up again). Only partners you've put on it are listed. The wheel remembers
              your partners - a new wheel opens to the same ones. (2.94j) Sneak + use the wheel: every partner of yours out in
              this world is brought back to your side at once, in a ring round you.
"""
import re
import json
from items import item, attr, ench, T, TOTEM, ITEMS, ARMOR_SLOT, weapon_attrs, hat, trail
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import phase15 as P15
import phase24 as R24
import phase73 as P73

XENO, WAR, PURPLE = '#3ad8c8', '#d83030', '#b48cff'
PIECES = ['helmet', 'chestplate', 'leggings', 'boots']

# ================================================================== THE ARMOUR REBALANCE (before phase177 copies the sets)
REBAL = {  # set: (piece id pattern, toughness a piece, max health a piece)
    'shadowstep': ('shadowstep_{p}_3', 1, 2), 'architect': ('architect_{p}_3', 1, 3), 'tidecaller': ('tidecaller_{p}_3', 1, 3),
    'crimson': ('crimson_{p}', 1, 2), 'vampire': ('vampire_{p}', 1, 2), 'solar': ('solar_{p}', 1, 2)}
for _set, (_fmt, _t, _h) in REBAL.items():
    for _p in PIECES:
        _c = ITEMS[_fmt.format(p=_p)]['comps']
        _s = ARMOR_SLOT[_p]
        _c['minecraft:attribute_modifiers'] = list(_c.get('minecraft:attribute_modifiers', [])) + [
            attr('armor_toughness', _t, _s, ident=f'bm:rb_tough_{_p}'), attr('max_health', _h, _s, ident=f'bm:rb_hp_{_p}')]
        _lore = _c['minecraft:lore']
        _hit = next((ln for ln in _lore if isinstance(ln, dict) and re.search(r'\+(\d+) Max Health', ln.get('text', ''))), None)
        if _hit:
            _n = int(re.search(r'\+(\d+) Max Health', _hit['text']).group(1))
            _hit['text'] = _hit['text'].replace(f'+{_n} Max Health', f'+{_n + _h} Max Health, +{_t} Toughness')
        else:
            _lore.insert(1, T(f'+{_h} Max Health, +{_t} Toughness', 'blue'))


# ================================================================== ALIEN GEAR
def armour(iid, base, name, col, p, a, t, h, kb, en, asset, setid, lore, sound):
    s = ARMOR_SLOT[p]
    mods = [attr('armor', a, s, ident=f'minecraft:armor.{p}'), attr('armor_toughness', t, s, ident=f'minecraft:armor.{p}_toughness'),
            attr('max_health', h, s)]
    if kb: mods.append(attr('knockback_resistance', kb, s, ident=f'minecraft:armor.{p}_kb'))
    item(iid, f'minecraft:{base}_{p}', name, col, lore, model=f'bm:{iid}', stack=1, cat='gear',
         comps={'minecraft:enchantments': en, 'minecraft:attribute_modifiers': mods,
                'minecraft:equippable': {'slot': s, 'asset_id': f'bm:{asset}', 'equip_sound': sound}},
         custom_extra={'bm_set': setid})


ARMOR_A = {'helmet': 3, 'chestplate': 8, 'leggings': 6, 'boots': 3}
XENO_NAMES = {'helmet': 'Helm', 'chestplate': 'Carapace', 'leggings': 'Greaves', 'boots': 'Striders'}
WAR_NAMES = {'helmet': 'Visor', 'chestplate': 'Cuirass', 'leggings': 'Tassets', 'boots': 'Sabatons'}
for _p in PIECES:
    _e = ench(protection=6, unbreaking=8, mending=1)
    if _p == 'helmet': _e.update(ench(respiration=3))
    if _p == 'boots': _e.update(ench(feather_falling=6))
    armour(f'xenoplate_{_p}', 'diamond', f'Xenoplate {XENO_NAMES[_p]}', XENO, _p, ARMOR_A[_p], 3.5, 2, 0, _e, 'xenoplate', 'xenoplate',
           ['Donadian plate. It hums when you jump.', ('+2 Max Health', 'blue'), ('Full set: Jump Boost, Night Vision and', 'dark_aqua'),
            ('a Deflector - two hearts of shield that', 'dark_aqua'), ('recharge every 40 seconds.', 'dark_aqua'), ('From Zorp.', 'dark_gray')],
           'minecraft:item.armor.equip_diamond')
    _e = ench(protection=7, unbreaking=10, mending=1)
    if _p == 'helmet': _e.update(ench(respiration=3, aqua_affinity=1))
    if _p == 'boots': _e.update(ench(feather_falling=8))
    armour(f'warplate_{_p}', 'netherite', f'Vorn Warplate {WAR_NAMES[_p]}', WAR, _p, ARMOR_A[_p], 4.5, 3, 0.15, _e, 'warplate', 'warplate',
           ['Torn off a Vorn war machine. Still warm.', ('+3 Max Health', 'blue'), ('Full set: above half health, Strength', 'dark_aqua'),
            ('and Speed; under a third, a Shockwave', 'dark_aqua'), ('hurls back every monster near you', 'dark_aqua'), ('(a minute\'s rest).', 'dark_aqua'),
            ('Zorp\'s hard-mode stock.', 'dark_gray')], 'minecraft:item.armor.equip_netherite')
P15.SET_FX['xenoplate'] = (['effect give @s minecraft:jump_boost 11 0 true', 'effect give @s minecraft:night_vision 15 0 true'],
                           'minecraft:dust{color:[0.23,0.85,0.78],scale:0.9}', 'particle minecraft:end_rod ~ ~2.1 ~ 0.2 0.05 0.2 0 1')
P15.SET_FX['warplate'] = ([], 'minecraft:dust{color:[0.85,0.12,0.12],scale:1.0}', 'particle minecraft:electric_spark ~ ~1.2 ~ 0.3 0.4 0.3 0 1')

SWORD_ITEMS = 'minecraft:netherite_sword'
WEAPONS = {  # iid: (name, colour, lore, bonus damage, swing speed (None: a sword's), enchantments, custom enchantment, Zorp's price)
    'plasma_cutter': ('Plasma Cutter', '#7aff6a', ['Donadian. It cuts like a hot wire.', ('Every hit burns green and lights the foe up.', 'blue')],
                      1, None, ench(sharpness=7, fire_aspect=2, looting=4, unbreaking=8, mending=1), 'plasma', (('xenite_green', 32), ('xenite_red', 4))),
    'graviton_edge': ('Graviton Edge', '#c08aff', ['The blade forgets which way is down.', ('One hit in four throws the foe into the air.', 'blue')],
                      1, None, ench(sharpness=7, knockback=1, looting=4, unbreaking=8, mending=1), 'graviton', (('xenite_violet', 32), ('xenite_red', 4))),
    'phase_saber': ('Phase Saber', '#5ae8ff', ['Half of it is somewhere else.', ('Quick to swing; one hit in five cuts', 'blue'), ('straight through armour (6 damage).', 'blue')],
                    0, -2.0, ench(sharpness=7, sweeping_edge=5, looting=4, unbreaking=8, mending=1), 'phase', (('xenite_cyan', 32), ('xenite_red', 4))),
    'vorn_annihilator': ('Vorn Annihilator', WAR, ['A Vorn officer\'s greatsword. Heavy. Hungry.', ('+4 Attack Damage, slow to swing.', 'blue'),
                                                    ('One hit in four arcs to three more monsters.', 'blue'), ('Zorp\'s hard-mode stock.', 'dark_gray')],
                         4, -2.9, ench(sharpness=8, smite=6, looting=5, unbreaking=10, mending=1), 'annihilate', (('xenite_red', 24), ('power_cell', 3))),
}
for _k, (_nm, _col, _lore, _bd, _sp, _en, _ce, _pr) in WEAPONS.items():
    _m = weapon_attrs('netherite_sword', _bd)
    if _sp is not None: _m[1] = attr('attack_speed', _sp, 'mainhand', ident='minecraft:base_attack_speed')
    item(_k, SWORD_ITEMS, _nm, _col, _lore + ([('From Zorp.', 'dark_gray')] if _k != 'vorn_annihilator' else []), model=f'bm:{_k}', stack=1, cat='gear',
         bold=_k == 'vorn_annihilator', comps={'minecraft:enchantments': dict(_en, **{f'bm:{_ce}': 1}), 'minecraft:attribute_modifiers': _m})
item('graviton_pick', 'minecraft:netherite_pickaxe', 'Graviton Pick', WAR,
     ['Vorn mining tech, pried loose.', ('Full speed underwater; +25% mining speed.', 'blue'), ('Zorp\'s hard-mode stock.', 'dark_gray')],
     model='bm:graviton_pick', stack=1, cat='gear',
     comps={'minecraft:enchantments': ench(efficiency=8, fortune=5, unbreaking=10, mending=1),
            'minecraft:attribute_modifiers': weapon_attrs('netherite_pickaxe', 0, [attr('submerged_mining_speed', 0.8, 'mainhand'),
                                                                                    attr('block_break_speed', 0.25, 'mainhand', 'add_multiplied_base')])})
hat('xeno_antennae', 'Donadian Antennae', XENO, 'bm:xeno_antennae', 'minecraft:dust{color:[0.48,1.0,0.42],scale:0.7} ~ ~2.5 ~ 0.25 0.05 0.25 0 1', None,
    ['Two little antennae on a headband.', 'Zorp swears they pick up radio.'])
trail('beam_treads', 'Tractor-Beam Treads', '#7aff6a', 0x2ac8a0, 'minecraft:end_rod ~ ~0.1 ~ 0.15 0 0.15 0.01 1', None,
      ['Every step, a little beam of light.'])

# Zorp: the Xenoplate and the three Donadian blades from the start (before phase24 builds his list); the rest in hard mode
_k = next(i for i, o in enumerate(R24.OFFERS) if o[2][0] == 'xenite_violet')
XENO_PRICE = {'helmet': (('xenite_green', 20), ('xenite_cyan', 8)), 'chestplate': (('xenite_violet', 28), ('xenite_cyan', 12)),
              'leggings': (('xenite_green', 24), ('xenite_violet', 10)), 'boots': (('xenite_cyan', 18), ('xenite_green', 8))}
R24.OFFERS[_k:_k] = [(a, b, (f'xenoplate_{p}', 1)) for p, (a, b) in XENO_PRICE.items()] + \
                    [(a, b, (k, 1)) for k, (*_r, (a, b)) in WEAPONS.items() if k != 'vorn_annihilator']
WAR_PRICE = {'helmet': (('xenite_red', 10), ('power_cell', 1)), 'chestplate': (('xenite_red', 16), ('power_cell', 2)),
             'leggings': (('xenite_red', 14), ('power_cell', 1)), 'boots': (('xenite_red', 10), ('power_cell', 1))}
HARD_ZORP = [(a, b, (f'warplate_{p}', 1)) for p, (a, b) in WAR_PRICE.items()] + \
            [(WEAPONS['vorn_annihilator'][7][0], WEAPONS['vorn_annihilator'][7][1], ('vorn_annihilator', 1)),
             (('xenite_red', 16), ('power_cell', 2), ('graviton_pick', 1)),
             (('xenite_red', 6), ('xenite_green', 12), ('xeno_antennae', 1)), (('xenite_red', 6), ('xenite_cyan', 12), ('beam_treads', 1))]

# ================================================================== THE PARTNER WHEEL
item('partner_wheel', TOTEM, 'Partner Wheel', PURPLE,
     ['Every partner, on one wheel.', ('Hold a partner\'s summoning item in your', 'blue'), ('off hand and use the wheel: it goes on.', 'blue'),
      ('Use the wheel alone: call a partner, send', 'blue'), ('them home, or take their item back out.', 'blue'),
      ('Sneak + use: your partners out in the world', 'blue'), ('come back to your side at once.', 'blue'),
      ('Carry it and its partners stay with you.', 'dark_aqua'), ('It remembers your partners - even a new wheel.', 'gray'),
      ('From Cecil.', 'dark_gray')], model='bm:partner_wheel', stack=1, cat='magic', comps=hold('none'))
HOLD['partner_wheel'] = 'bm:p179/w/use'
WMENU = 3350                      # (its block: 3350-3449 - a partner's call/send home 3360+i, take out 3390+i)
WMENU3 = 3700                     # (2.94: 3700-3819 - the second bank, partners 31 on)
WMENU2 = 3450                     # (2.88: and 3450-3479 - a partner's Menu button 3450+i; 3420/3421 are the Skiff Escort's)

KEEP = 3351                       # (2.94q: the "Keep up" switch, in the wheel's block)


def keep_btn(on):
    import phase28 as P28
    return P28.btn([T('Keep up: ', 'gray'), T('on' if on else 'off', 'white' if on else '#ff8a8a', bold=True)], KEEP, width=150,
                   tooltip=T('A partner left too far behind (or in another world) comes back to your side once you\'re on the ground or in water, '
                             'in survival or adventure - while you carry their item or it\'s on the wheel.', 'gray'))


# every follower's item and "goes away" function, as phase73's follow rules are set up (whichever phase sets them)
FOLLOW = {}
_orig_rules = P73.follow_rules


def _rules(G, entry, second):
    FOLLOW[entry[2]] = entry                 # (keyed by the host's tag)
    return _orig_rules(G, entry, second)


P73.follow_rules = _rules


def extend_offers(O, offer):
    O['wizard'].append(offer(('medallion', 3), ('partner_wheel', 1)))



# (2.98b) THE WHEEL'S SLOTS, frozen: a new partner goes on the END, never in the middle (see generate)
SLOTS = ('emma', 'celi', 'zib', 'cecil', 'kw', 'leo', 'demo', 'apo', 'tul', 'frog', 'don', 'pearl', 'wil', 'fishy', 'dennis', 'pistachio',
         'omega', 'ashur', 'chef', 'neighbor', 'ava', 'pearlq', 'bloo', 'stalker', 'lantern', 'bender', 'bones', 'capshun', 'kettle', 'rufus',
         'henry', 'nia', 'gem', 'batty', 'eggbert', 'count', 'dragon', 'eraser', 'cursor', 'inkblot', 'speech', 'lightbringer', 'dryad',
         'sovereign', 'pxcecil', 'pxleo', 'pxemma', 'sky')
REPAIR = 1                                   # (bump to run the wheel's repair again for everyone)

def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    import phase28 as P28
    import phase125 as P125
    import phase177 as P177
    import phase178 as P178
    import zlib
    PRE = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    second, load = G.FUNCS['loop/second'], G.FUNCS['load']
    objs = ['bm.xdf', 'bm.wsw', 'bm.pwrc']

    # ---------------------------------------------------------------- a re-sync keeps tunings and infusions
    rs = G.FUNCS['p18/refresh/slot']
    k = next(i for i, l in enumerate(rs) if 'rf.iid set from entity' in l)
    tune_ids = sorted({f'bm:tune_{key}_{lv}' for opts in P177.TUNE.values() for key, *_r, mx in opts for lv in range(1, 4)})
    rs[k + 1:k + 1] = ['$data modify storage bm:tmp rf.tune set from entity @s $(path).components."minecraft:custom_data".bm_tune',
                       '$data modify storage bm:tmp rf.path set value "$(path)"'] + \
                      [f'$data modify storage bm:tmp rf.tm append from entity @s $(path).components."minecraft:attribute_modifiers"[{{id:"{i}"}}]' for i in tune_ids]
    rs += ['execute if data storage bm:tmp rf.iid if data storage bm:tmp rf.tune run function bm:p179/rs/retune with storage bm:tmp rf']
    rs += [f'execute if data storage bm:tmp rf.iid if data storage bm:tmp {{rf:{{inf:"{key}"}}}} run function bm:p179/rs/inf_{key} with storage bm:tmp rf'
           for key in P178.INF]
    fn('p179/rs/retune', ['$execute unless data entity @s $(path).components."minecraft:custom_data".bm_tune run item modify entity @s $(slot) '
                          '{function:"minecraft:set_custom_data",tag:{bm_tune:$(tune)}}',
                          'data modify storage bm:tmp rf.e set value {}', 'data modify storage bm:tmp rf.e.slot set from storage bm:tmp rf.slot',
                          'data modify storage bm:tmp rf.e.path set from storage bm:tmp rf.path', 'function bm:p179/rs/next'])
    fn('p179/rs/next', ['execute unless data storage bm:tmp rf.tm[0] run return 0',
                        'data modify storage bm:tmp rf.e.at set from storage bm:tmp rf.tm[0].type', 'data modify storage bm:tmp rf.e.id set from storage bm:tmp rf.tm[0].id',
                        'data modify storage bm:tmp rf.e.amount set from storage bm:tmp rf.tm[0].amount', 'data modify storage bm:tmp rf.e.op set from storage bm:tmp rf.tm[0].operation',
                        'data modify storage bm:tmp rf.e.sl set from storage bm:tmp rf.tm[0].slot', 'data remove storage bm:tmp rf.tm[0]',
                        'function bm:p179/rs/one with storage bm:tmp rf.e', 'function bm:p179/rs/next'])
    fn('p179/rs/one', ['$execute if data entity @s $(path).components."minecraft:attribute_modifiers"[{id:"$(id)"}] run return 0',
                       '$item modify entity @s $(slot) {function:"minecraft:set_attributes",replace:false,modifiers:[{attribute:"$(at)",id:"$(id)",'
                       'amount:$(amount),operation:"$(op)",slot:"$(sl)"}]}'])
    for key, (cls, nm, col, what) in P178.INF.items():
        lore = T(f'☠ Infused: {nm} - {what}', col)
        fn(f'p179/rs/inf_{key}', ['$execute if data entity @s $(path).components."minecraft:custom_data".bm_inf run return 0',
                                  f'$item modify entity @s $(slot) {{function:"minecraft:set_custom_data",tag:{{bm_inf:"{key}"}}}}',
                                  f'$item modify entity @s $(slot) {{function:"minecraft:set_lore",mode:"append",lore:[{snbt(lore)}]}}'])
    # (a gravity infusion only on boots with no infusion yet - it used to overwrite an auction infusion)
    old = 'if items entity @s weapon.mainhand *[minecraft:custom_data~{bm_inf:"gravity"}] run return run'
    n = 0
    for name, L in G.FUNCS.items():
        for i, l in enumerate(L):
            if old in l:
                L[i] = l.replace(old, 'if data entity @s SelectedItem.components."minecraft:custom_data".bm_inf run return run'); n += 1
    assert n >= 1, 'gravity infusion guard'

    # ---------------------------------------------------------------- alien gear: the blades' powers, the sets' gifts
    def ench_json(desc, col, effects):
        return {'anvil_cost': 8, 'description': T(desc, col), 'max_level': 1, 'weight': 1, 'min_cost': {'base': 1, 'per_level_above_first': 0},
                'max_cost': {'base': 1, 'per_level_above_first': 0}, 'slots': ['mainhand'], 'supported_items': SWORD_ITEMS, 'effects': effects}
    chance = lambda p: {'condition': 'minecraft:random_chance', 'chance': p}
    hit = lambda eff, p=None: {'minecraft:post_attack': [dict({'enchanted': 'attacker', 'affected': 'victim', 'effect': eff}, **({'requirements': chance(p)} if p else {}))]}
    run = lambda f: {'type': 'minecraft:run_function', 'function': f}
    wjson('bm/enchantment/plasma.json', ench_json('Plasma', '#7aff6a', hit({'type': 'minecraft:all_of', 'effects': [
        {'type': 'minecraft:ignite', 'duration': 3}, run('bm:p179/plasma')]})))
    wjson('bm/enchantment/graviton.json', ench_json('Graviton', '#c08aff', hit({'type': 'minecraft:all_of', 'effects': [
        {'type': 'minecraft:apply_mob_effect', 'to_apply': 'minecraft:levitation', 'min_duration': 1.2, 'max_duration': 1.2, 'min_amplifier': 3.0, 'max_amplifier': 3.0},
        run('bm:p179/graviton')]}, 0.25)))
    wjson('bm/enchantment/phase.json', ench_json('Phase', '#5ae8ff', hit({'type': 'minecraft:all_of', 'effects': [
        {'type': 'minecraft:damage_entity', 'damage_type': 'minecraft:magic', 'min_damage': 6.0, 'max_damage': 6.0}, run('bm:p179/phase')]}, 0.2)))
    wjson('bm/enchantment/annihilate.json', ench_json('Annihilate', WAR, hit(run('bm:p179/arc'), 0.25)))
    fn('p179/plasma', ['effect give @s minecraft:glowing 3 0 true', 'particle minecraft:dust{color:[0.48,1.0,0.42],scale:1.2} ~ ~1 ~ 0.3 0.4 0.3 0 10'])
    fn('p179/graviton', ['particle minecraft:reverse_portal ~ ~0.5 ~ 0.3 0.3 0.3 0.05 20', 'playsound minecraft:entity.shulker.shoot hostile @a[distance=..12] ~ ~ ~ 0.6 1.6'])
    fn('p179/phase', ['particle minecraft:end_rod ~ ~1 ~ 0.3 0.5 0.3 0.05 12', 'playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..12] ~ ~ ~ 0.6 1.4'])
    fn('p179/arc', ['particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.2 20',
                    'execute as @e[type=#bm:hostile,distance=0.5..6,sort=nearest,limit=3] at @s run function bm:p179/arc_hit',
                    'playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..16] ~ ~ ~ 0.25 1.8'])
    fn('p179/arc_hit', ['damage @s 5 minecraft:lightning_bolt', 'particle minecraft:electric_spark ~ ~1 ~ 0.2 0.5 0.2 0.1 12'])
    # Xenoplate's Deflector: two hearts of shield, recharged every 40 seconds
    fn('p179/xeno', ['execute if score @s bm.xdf matches 1.. run return run scoreboard players remove @s bm.xdf 1',
                     'effect give @s minecraft:absorption 40 0 true', 'scoreboard players set @s bm.xdf 40',
                     'particle minecraft:dust{color:[0.23,0.85,0.78],scale:1.0} ~ ~1 ~ 0.5 0.7 0.5 0 20',
                     'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.4 1.8'])
    # Warplate: above half health, Strength and Speed; under a third, the Shockwave (60 s rest)
    fn('p179/war', ['execute store result score #hh bm.rng run data get entity @s Health',
                    'execute store result score #hm bm.rng run attribute @s minecraft:max_health get',
                    'scoreboard players operation #h2 bm.rng = #hh bm.rng', 'scoreboard players operation #h2 bm.rng *= #2 bm.p177',
                    'execute if score #h2 bm.rng >= #hm bm.rng run effect give @s minecraft:strength 2 0 true',
                    'execute if score #h2 bm.rng >= #hm bm.rng run effect give @s minecraft:speed 2 0 true',
                    'execute if score @s bm.wsw matches 1.. run return 0', 'scoreboard players operation #hh bm.rng *= #3 bm.p177',
                    'execute if score #hh bm.rng > #hm bm.rng run return 0', 'scoreboard players set @s bm.wsw 60',
                    'execute as @e[type=#bm:hostile,distance=..5] run damage @s 6 minecraft:player_explosion by @p[distance=..6]',
                    'effect give @e[type=#bm:hostile,distance=..5] minecraft:slowness 3 2',
                    'execute as @e[type=#bm:hostile,distance=..5] at @s facing entity @p[distance=..6] feet rotated ~ 0 run tp @s ^ ^ ^-1.5',
                    'particle minecraft:explosion ~ ~1 ~ 1.5 0.3 1.5 0 6', 'particle minecraft:electric_spark ~ ~1 ~ 2.5 0.5 2.5 0.2 40',
                    'playsound minecraft:entity.generic.explode player @a[distance=..16] ~ ~ ~ 0.7 1.2'])
    second += ['execute as @a[gamemode=!spectator] if function bm:sets/has/xenoplate at @s run function bm:p179/xeno',
               'execute as @a[gamemode=!spectator] if function bm:sets/has/warplate at @s run function bm:p179/war',
               'scoreboard players remove @a[scores={bm.wsw=1..}] bm.wsw 1']

    # ---------------------------------------------------------------- Zorp's hard-mode stock
    O1 = [G.offer(b, s, bb) if bb else G.offer(b, s) for b, bb, s in R24.OFFERS]
    O2 = O1 + [G.offer(b, s, bb) if bb else G.offer(b, s) for b, bb, s in R24.INV_EXTRA]
    H = [G.offer(b, s, bb) if bb else G.offer(b, s) for b, bb, s in HARD_ZORP]
    zl = []
    for nm, offers, cond in (('zorp_hard', O1 + H, 'unless score #vornmet bm.bm matches 1'), ('zorp_hard_v', O2 + H, 'if score #vornmet bm.bm matches 1')):
        blob = snbt(offers)
        v = zlib.crc32(('hard' + blob).encode()) % 1000000000
        fn(f'p179/{nm}', [f'data modify entity @s Offers.Recipes set value {blob}', f'scoreboard players set @s bm.ofv {v}'])
        zl.append(f'execute if score #hard bm.cfg matches 1 {cond} unless score #lnight bm.bm matches 1 as @e[tag=bm.npc_alien] '
                  f'unless score @s bm.ofv matches {v} run function bm:p179/{nm}')
    za = [i for i, l in enumerate(second) if 'as @e[tag=bm.npc_alien] unless score @s bm.ofv matches ' in l
          and ('function bm:p17/npc/alien' in l or 'function bm:p148/zorp_unlocked' in l)]
    assert len(za) == 2, za
    for i in za:
        second[i] = second[i].replace('execute ', 'execute unless score #hard bm.cfg matches 1 ', 1)
    second[za[-1] + 1:za[-1] + 1] = zl

    # ---------------------------------------------------------------- the Partner Wheel
    WHO = P125.WHO
    host_tag = lambda w: WHO[w][4].split(',')[0]
    PW = []                                  # (key, name, colour, host type, host selector tag, try, home, item)
    # (2.98b) a partner's place on the wheel is saved by its NUMBER (bm.pw<i>, storage k<i>) - so the order is frozen: SLOTS, then
    # anyone new, appended. A follower slotted into the middle renumbered everyone after it, and a world from an older version
    # read its partners as someone else's (repair_wheel puts them back, by the item each slot holds).
    order = list(SLOTS) + [w for w in WHO if w not in SLOTS]
    assert set(SLOTS) <= set(WHO), set(SLOTS) - set(WHO)
    for w in order:
        nm, pron, col, host, tag, try_, home = WHO[w]
        e = FOLLOW.get(host_tag(w))
        iid = e[3] if e else ('wilfrey_locket' if w == 'wil' else None)
        assert iid in ITEMS, (w, iid)
        PW.append((w, nm, col, host, tag, try_, home, iid))
    objs += [f'bm.pw{i}' for i in range(len(PW))]
    load[-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    cap = lambda s: s[0].upper() + s[1:]
    # who carries a wheel - and for each partner on it, the tag every "has their item" check now also takes
    W = holds('partner_wheel')
    tags = ['tag @a remove bm.pwc'] + [f'execute as @a if items entity @s {sl} {W} run tag @s add bm.pwc' for sl in ('container.*', 'weapon.offhand', 'player.cursor')]
    for i, (w, *_r) in enumerate(PW):
        tags += [f'tag @a remove bm.pw_{w}', f'tag @a[tag=bm.pwc,scores={{bm.pw{i}=1}}] add bm.pw_{w}']
    second[0:0] = tags
    patched = {w: 0 for w, *_r in PW}
    for name, L in list(G.FUNCS.items()):
        if name.startswith('p179/'): continue
        out = []
        for i, l in enumerate(L):
            out.append(l)
            for w, nm, col, host, tag, try_, home, iid in PW:
                Hh = holds(iid)
                if f' {Hh}' not in l: continue
                both = f'unless items entity @s container.* {Hh} unless items entity @s weapon.offhand {Hh}'
                if both in l:                                         # "doesn't have it": nor on the wheel
                    out[-1] = out[-1].replace(both, both + f' unless entity @s[tag=bm.pw_{w}]'); patched[w] += 1
                elif l.startswith(f'execute if items entity @s weapon.offhand {Hh} run return') and i and \
                        L[i - 1].startswith(f'execute if items entity @s container.* {Hh} run return'):     # "has it - stop": the wheel too
                    out.append(l.replace(f'if items entity @s weapon.offhand {Hh}', f'if entity @s[tag=bm.pw_{w}]', 1)); patched[w] += 1
                else:
                    m = re.match(r'^execute if items entity (@a\[tag=bm\.fown,limit=1\]) player\.cursor ' + re.escape(Hh) + r' (run return run scoreboard players set @s bm\.fmis 0)$', l)
                    if m:                                             # a partner stays while the wheel carries their item
                        out.append(f'execute if entity @a[tag=bm.fown,tag=bm.pw_{w}] {m.group(2)}'); patched[w] += 1
        L[:] = out
    assert all(patched.values()), {w: n for w, n in patched.items() if not n}

    G.wjson('bm/predicate/p179/sneak.json', {'condition': 'minecraft:any_of', 'terms': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_sneaking': True}}},
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'nbt': '{Tags:["bm.pwsneak"]}'}}]})
    fn('p179/w/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid'] +
       [f'execute if items entity @s weapon.offhand {holds(iid)} run return run function bm:p179/w/add{i}' for i, (*_r, iid) in enumerate(PW)] +
       ['execute if predicate bm:p20/sneaking run return run function bm:p179/w/recall', 'function bm:p179/w/open'])
    # (2.94j) sneak + use: every partner of yours out in this world comes to you at once - a ring of them round you, as they were
    # (sitting stays sitting); eight seconds' rest between
    fn('p179/w/recall', ['execute if score @s bm.pwrc matches 1.. run return run ' + say('The wheel is still turning...'),
                         'scoreboard players set @s bm.pwrc 8', 'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #pwn bm.rng 0',
                         'tag @s add bm.pwme'] +
       [f'execute as @e[type=minecraft:{host},tag={tag}] if score @s bm.pid = #me bm.pid at @s run function bm:p179/w/fetch' for host, tag in
        dict.fromkeys((host, tag) for w, nm, col, host, tag, *_r in PW)] +
       ['tag @s remove bm.pwme',
        'execute if score #pwn bm.rng matches 0 run return run ' + say('None of your partners are out to call back.'),
        'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.8', 'particle minecraft:enchant ~ ~1.2 ~ 0.4 0.5 0.4 0.8 30',
        'execute if score #pwn bm.rng matches 1 run return run ' + say('The wheel turns - your partner is back at your side.', PURPLE),
        say('The wheel turns - your partners are back at your side.', PURPLE)])
    # (around you: each one a step further round the ring, a block and a half out)
    fn('p179/w/fetch', ['particle minecraft:reverse_portal ~ ~0.8 ~ 0.3 0.5 0.3 0.05 20',
                        'scoreboard players add #pwn bm.rng 1', 'execute store result storage bm:tmp pw.yaw float 45 run scoreboard players get #pwn bm.rng',
                        'execute at @a[tag=bm.pwme,limit=1] run function bm:p179/w/fetch_at with storage bm:tmp pw'])
    # (2.94k: the ring spot clear all the way from you - not through a wall - and ground under it, not a drop or lava; else onto you)
    fn('p179/w/fetch_at', ['$execute rotated $(yaw) 0 positioned ^ ^ ^0.75 if block ~ ~ ~ #minecraft:air if block ~ ~1 ~ #minecraft:air positioned ^ ^ ^0.75 '
                           'if block ~ ~ ~ #minecraft:air if block ~ ~1 ~ #minecraft:air unless block ~ ~-1 ~ #bm:grap_pass unless block ~ ~-1 ~ minecraft:lava '
                           'run return run function bm:p179/w/land',
                           'tp @s ~ ~ ~', 'execute at @s run particle minecraft:portal ~ ~0.8 ~ 0.3 0.5 0.3 0.4 20'])
    fn('p179/w/land', ['tp @s ~ ~ ~',
                           'execute at @s run particle minecraft:portal ~ ~0.8 ~ 0.3 0.5 0.3 0.4 20'])
    second.append('scoreboard players remove @a[scores={bm.pwrc=1..}] bm.pwrc 1')
    fn('p179/w/pid', ['execute store result storage bm:tmp pw.pid int 1 run scoreboard players get @s bm.pid'])
    repair_wheel(G, PW, holds)
    empty = P28.notice([T('Partner Wheel', PURPLE, bold=True)],
                       [P28.body([T('No partners on your wheel yet.', 'white')], 300),
                        P28.body([T('Hold a partner\'s summoning item in your off hand and use the wheel: it goes on. ', 'gray'),
                                  T('While you carry the wheel, your partners on it come when you call and stay with you.', 'gray')], 300)])
    full = P28.multi([T('Partner Wheel', PURPLE, bold=True)],
                     [P28.body([T('Call a partner or send them home, open their menu (wardrobe, buffs and choices) - or take their item back off the wheel.', 'gray')], 300)], '@@ACTS@@', columns=3)
    fn('p179/w/show', ['$dialog show @s ' + snbt(full).replace('"@@ACTS@@"', '$(acts)')])
    op = [f'scoreboard players set @s bm.menu {WMENU}', 'scoreboard players operation #me bm.pid = @s bm.pid', 'data modify storage bm:tmp pw.acts set value []']
    op += [f'execute if score @s bm.pw{i} matches 1 run function bm:p179/w/row{i}' for i in range(len(PW))]
    import phase123 as P123                   # (2.88: the chatter switch, last on the wheel - it reads on or off)
    op += [f'execute unless data storage bm:tmp pw.acts[0] run return run dialog show @s {snbt(empty)}',
           f'execute if entity @s[tag=bm.hush] run data modify storage bm:tmp pw.acts append value {snbt(P123.chat_btn(False))}',
           f'execute unless entity @s[tag=bm.hush] run data modify storage bm:tmp pw.acts append value {snbt(P123.chat_btn(True))}',
           f'execute if entity @s[tag=bm.pwkeep] run data modify storage bm:tmp pw.acts append value {snbt(keep_btn(True))}',
           f'execute unless entity @s[tag=bm.pwkeep] run data modify storage bm:tmp pw.acts append value {snbt(keep_btn(False))}',
           'function bm:p179/w/show with storage bm:tmp pw',
           'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.4']
    fn('p179/w/open', op)
    # (2.94: past thirty partners, a second bank - call 3700+, take out 3740+, menu 3780+)
    c_call = lambda i: WMENU + 10 + i if i < 30 else WMENU3 + i - 30
    c_out = lambda i: WMENU + 40 + i if i < 30 else WMENU3 + 40 + i - 30
    c_menu = lambda i: WMENU2 + i if i < 30 else WMENU3 + 80 + i - 30
    assert len(PW) <= 70, f'{len(PW)} partners: the second bank is full'
    act = [f'execute unless score @s bm.menu matches {WMENU} run return run function bm:p28/stale',
           f'execute if score #act bm.pay matches {KEEP} run return run function bm:p179/k/toggle']
    for i, (w, nm, col, host, tag, try_, home, iid) in enumerate(PW):
        sel = f'@e[type=minecraft:{host},tag={tag}]'
        on = ['scoreboard players set #pwon bm.rng 0', f'execute as {sel} if score @s bm.pid = #me bm.pid run scoreboard players set #pwon bm.rng 1']
        it_nm = ITEMS[iid]['name']
        # (2.95e) their summoning item's own icon beside the name - a sprite from the items atlas, inline in the text
        mdl = ITEMS[iid]['comps'].get('minecraft:item_model', f'minecraft:{ITEMS[iid]["base"].split(":")[-1]}')
        ns_, path_ = mdl.split(':', 1) if ':' in mdl else ('minecraft', mdl)
        icon = {'type': 'object', 'object': 'atlas', 'atlas': 'minecraft:items', 'sprite': f'{ns_}:item/{path_}',
                'fallback': {'text': '\u25c6', 'color': col}}
        b_call = P28.btn([icon, T(' Call ', 'white'), T(nm, col, bold=True)], c_call(i), tooltip=T(f'Call {nm}', 'gray'))
        b_home = P28.btn([icon, T(f' Send {nm} home', '#c8c8c8')], c_call(i), tooltip=T(f'{cap(nm)} goes home', 'gray'))
        b_out = P28.btn(T('Take the item back', 'gray'), c_out(i), tooltip=T(f'{it_nm} comes off the wheel', 'gray'))
        b_menu = P28.btn([T('\u2699 ', col), T('Menu', 'white')], c_menu(i), tooltip=T(f'{cap(nm)}\'s own menu - the wardrobe, {WHO[w][1]} ways and choices (as sneak + using {it_nm})', 'gray'))
        fn(f'p179/w/row{i}', on + [f'execute if score #pwon bm.rng matches 0 run data modify storage bm:tmp pw.acts append value {snbt(b_call)}',
                                   f'execute if score #pwon bm.rng matches 1 run data modify storage bm:tmp pw.acts append value {snbt(b_home)}',
                                   f'data modify storage bm:tmp pw.acts append value {snbt(b_menu)}',
                                   f'data modify storage bm:tmp pw.acts append value {snbt(b_out)}'])
        # (2.88) the partner's own menu from the wheel - their wardrobe, their buffs and choices: their item's sneak + use, as if
        # held (in their item's use, bm:p179/sneak: sneaking - or the tag bm.pwsneak, on only for this one call)
        use_fn = HOLD[iid].split(':', 1)[1]
        U = G.FUNCS[use_fn]
        assert any('predicate bm:p20/sneaking' in l for l in U), (w, use_fn)
        U[:] = [l.replace('predicate bm:p20/sneaking', 'predicate bm:p179/sneak') for l in U]
        fn(f'p179/w/menu{i}', [f'execute unless score @s bm.pw{i} matches 1 run return run function bm:p28/stale', 'dialog clear @s',
                               'scoreboard players set @s bm.gvhc 0', 'tag @s add bm.pwsneak', f'function bm:{use_fn}', 'tag @s remove bm.pwsneak'])
        fn(f'p179/w/call{i}', [f'execute unless score @s bm.pw{i} matches 1 run return run function bm:p28/stale',
                               'scoreboard players operation #me bm.pid = @s bm.pid'] + on +
           [f'execute if score #pwon bm.rng matches 1 run return run function bm:{home}', f'function bm:{try_}'])
        fn(f'p179/w/add{i}', [f'execute if score @s bm.pw{i} matches 1 run return run ' + say(f'{cap(nm)} is on your wheel already.'),
                              'function bm:p179/w/pid', f'function bm:p179/w/addm{i} with storage bm:tmp pw',
                              'item replace entity @s weapon.offhand with minecraft:air', f'scoreboard players set @s bm.pw{i} 1', f'tag @s add bm.pw_{w}',
                              'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.6 1.6', 'particle minecraft:enchant ~ ~1.2 ~ 0.3 0.4 0.3 0.6 20',
                              tellraw('@s', PRE + [T(it_nm, col, bold=True), T(' goes on your Partner Wheel. ', 'gray'),
                                                   T('(Use the wheel to call ' + nm + '.)', 'dark_gray')])])
        fn(f'p179/w/addm{i}', [f'$data modify storage bm:pw p$(pid).k{i} set from entity @s equipment.offhand'])
        fn(f'p179/w/out{i}', [f'execute unless score @s bm.pw{i} matches 1 run return run function bm:p28/stale',
                              'function bm:p179/w/pid', f'function bm:p179/w/outm{i} with storage bm:tmp pw', f'scoreboard players set @s bm.pw{i} 0',
                              f'tag @s remove bm.pw_{w}', 'playsound minecraft:item.armor.equip_chain player @s ~ ~ ~ 0.6 1.4',
                              tellraw('@s', PRE + [T(it_nm, col, bold=True), T(' comes off your Partner Wheel.', 'gray')])])
        fn(f'p179/w/outm{i}', [f'$execute unless data storage bm:pw p$(pid).k{i} run return run ' + give(iid),
                               'summon minecraft:item ~ ~0.4 ~ {Tags:["bm.pwout"],PickupDelay:0s,Item:{id:"minecraft:paper",count:1}}',
                               f'$data modify entity @e[type=minecraft:item,tag=bm.pwout,limit=1] Item set from storage bm:pw p$(pid).k{i}',
                               'data modify entity @e[type=minecraft:item,tag=bm.pwout,limit=1] Owner set from entity @s UUID',
                               'tag @e[type=minecraft:item,tag=bm.pwout] remove bm.pwout', f'$data remove storage bm:pw p$(pid).k{i}'])
        act += [f'execute if score #act bm.pay matches {c_call(i)} run return run function bm:p179/w/call{i}',
                f'execute if score #act bm.pay matches {c_out(i)} run return run function bm:p179/w/out{i}',
                f'execute if score #act bm.pay matches {c_menu(i)} run return run function bm:p179/w/menu{i}']
    fn('p179/w/act', act)

    # ---------------------------------------------------------------- (2.94q) KEEP UP WITH YOU: a switch on the wheel
    # A partner left too far behind (or in another world) goes home as ever - but with it on, they're back at your side as soon
    # as you're on the ground or in water, in survival or adventure (not gliding, riding or falling; never in creative). Only
    # while you still carry their item, or it's on your wheel. A heist's "waits outside the vault" comes first.
    fn('p179/k/toggle', ['execute if entity @s[tag=bm.pwkeep] run return run function bm:p179/k/off',
                         'tag @s add bm.pwkeep', 'playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.6 1.5',
                         tellraw('@s', PRE + [T('Keep up: on. ', PURPLE, bold=True), T('A partner left behind comes back to your side once you\'re on the ground or in water.', 'gray')]),
                         'function bm:p179/w/open'])
    fn('p179/k/off', ['tag @s remove bm.pwkeep'] + [f'tag @s remove bm.pwk_{w}' for w, *_r in PW] +
       ['playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.6 0.9',
        tellraw('@s', PRE + [T('Keep up: off. ', PURPLE, bold=True), T('A partner left behind goes home and waits for your call.', 'gray')]),
        'function bm:p179/w/open'])
    G.wjson('bm/predicate/p179/landed.json', {'condition': 'minecraft:all_of', 'terms': [
        {'condition': 'minecraft:any_of', 'terms': [
            {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_on_ground': True}}},
            {'condition': 'minecraft:location_check', 'predicate': {'fluid': {'fluids': '#minecraft:water'}}}]},
        {'condition': 'minecraft:inverted', 'term': {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:vehicle': {}}}}]})
    kept, objs_k = 0, []
    for i, (w, nm, col, host, tag, try_, home, iid) in enumerate(PW):
        e = FOLLOW.get(host_tag(w))
        far = G.FUNCS.get(f'p73/fol/{e[0]}_far') if e else None
        if far is None: continue                       # (Wilfrey: never too far - his locket calls him)
        go = f'function bm:{e[4]}'
        assert go in far, (w, far)
        far.insert(far.index(go), f'execute if entity @a[tag=bm.fown,tag=bm.pwkeep] run return run function bm:p179/k/lag{i}')
        fn(f'p179/k/lag{i}', [f'tag @a[tag=bm.fown] add bm.pwk_{w}', go,
                              tellraw('@a[tag=bm.fown]', PRE + [T(f'{cap(nm)} fell behind', col), T(' - back at your side once you\'re on solid ground or in water.', 'gray')]),
                              'tag @a remove bm.fown'])
        Hh = holds(iid)
        fn(f'p179/k/back{i}', [f'tag @s remove bm.pwk_{w}',
                               f'execute unless entity @s[tag=bm.pw_{w}] unless items entity @s container.* {Hh} unless items entity @s weapon.offhand {Hh} run return 0',
                               'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #pwon bm.rng 0',
                               f'execute as @e[type=minecraft:{host},tag={tag}] if score @s bm.pid = #me bm.pid run scoreboard players set #pwon bm.rng 1',
                               'execute if score #pwon bm.rng matches 1 run return 0',
                               f'function bm:{try_}'])
        kept += 1
        # (2.94r) left in a chunk that has since unloaded, a partner is frozen there - unseen, never "too far". So each one out
        # stamps its player every second (bm.pwo<i>, 5); when the stamps stop and nothing sent it home (going home clears it),
        # it's lost: back at your side as above. (The frozen one goes home by itself when its chunk loads: its ticket is old.)
        objs_k.append(f'bm.pwo{i}')
        second.append(f'execute as @e[type=minecraft:{host},tag={tag.split(",")[0]}] run function bm:p179/k/seen{i}')
        fn(f'p179/k/seen{i}', ['scoreboard players operation #pwg bm.rng = @s bm.pid',
                               f'execute as @a[tag=bm.pwkeep] if score @s bm.pid = #pwg bm.rng unless score @s bm.pwo{i} matches ..-1 run scoreboard players set @s bm.pwo{i} 5'])
        G.FUNCS[e[4]][0:0] = ['scoreboard players operation #pwg bm.rng = @s bm.pid',
                              f'execute as @a if score @s bm.pid = #pwg bm.rng run scoreboard players reset @s bm.pwo{i}']
        # (2.94w) sent home - from the wheel, their menu or their item - is never "lost": every way home clears the stamp (as you,
        # and as them: their own dismiss, which their menu's button runs)
        G.FUNCS[home][0:0] = [f'scoreboard players set @s bm.pwo{i} -1', f'tag @s remove bm.pwk_{w}']      # (-1: sent home, till called)
        G.FUNCS[try_][0:0] = [f'scoreboard players reset @s bm.pwo{i}']
        for l in list(G.FUNCS[home]):
            m = re.search(r'run function bm:([\w/]+)$', l)
            if m and m.group(1) in G.FUNCS and m.group(1) != e[4] and not m.group(1).startswith('p179/'):
                G.FUNCS[m.group(1)][0:0] = ['scoreboard players operation #pwg bm.rng = @s bm.pid',
                                            f'execute as @a if score @s bm.pid = #pwg bm.rng run scoreboard players set @s bm.pwo{i} -1']
        second += [f'scoreboard players remove @a[tag=bm.pwkeep,scores={{bm.pwo{i}=1..}}] bm.pwo{i} 1',
                   f'execute as @a[tag=bm.pwkeep,scores={{bm.pwo{i}=0}}] run function bm:p179/k/lost{i}']
        # (2.94w) fainted is not lost: while they're still recovering (their item's cooldown), the faint's own comeback brings them
        cdo = re.search(r'@s (bm\.[a-z0-9]+cd) matches 1\.\.', ' '.join(G.FUNCS[try_]))
        fn(f'p179/k/lost{i}', [f'scoreboard players reset @s bm.pwo{i}'] +
           ([f'execute if score @s {cdo.group(1)} matches 1.. run return 0'] if cdo else []) + [f'tag @s add bm.pwk_{w}',
                               tellraw('@s', PRE + [T(f'{cap(nm)} got lost', col), T(' - back at your side once you\'re on solid ground or in water.', 'gray')])])
    assert kept >= len(PW) - 1, kept
    load[-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs_k]
    G.OBJECTIVES += objs_k
    fn('p179/k/off_clear', [f'scoreboard players reset @s {o}' for o in objs_k])
    G.FUNCS['p179/k/off'].insert(0, 'function bm:p179/k/off_clear')
    fn('p179/k/tick', [f'execute if entity @s[tag=bm.pwk_{w}] run function bm:p179/k/back{i}' for i, (w, *_r) in enumerate(PW)
                       if f'p179/k/back{i}' in G.FUNCS])
    second.append('execute as @a[tag=bm.pwkeep,tag=!bm.gvp,gamemode=!creative,gamemode=!spectator] at @s '
                  'if predicate bm:p179/landed run function bm:p179/k/tick')
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {WMENU}..{WMENU + 99} run return run function bm:p179/w/act')
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {WMENU2}..{WMENU2 + 29} run return run function bm:p179/w/act')
    if len(PW) > 30:
        G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {WMENU3}..{WMENU3 + 119} run return run function bm:p179/w/act')
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/alien_gear', 'yellow'), T('  every Xenoplate and Warplate piece, the alien blades, the pick', 'gray')])]
    fn('admin/alien_gear', [give(f'{s}_{p}') for s in ('xenoplate', 'warplate') for p in PIECES] + [give(k) for k in WEAPONS] + [give('graviton_pick')])


# ================================================================== resource pack
VAN = '/home/claude/mc263/client/assets/minecraft/textures'


def _recolor(path, lo, hi, keep=None, gamma=0.8, stretch=1.0):
    from PIL import Image
    im = Image.open(path).convert('RGBA'); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a or (keep and keep(x, y)): continue
            t = min(1.0, ((r + g + b) / 765) * stretch) ** gamma
            px[x, y] = tuple(int(lo[c] + (hi[c] - lo[c]) * t) for c in range(3)) + (a,)
    return im


def rp(R):
    XL, XH = (8, 38, 44), (120, 255, 214)
    WL, WH = (34, 6, 8), (255, 70, 60)
    for p in PIECES:
        R.ICONS[f'xenoplate_{p}'] = _recolor(f'{VAN}/item/diamond_{p}.png', XL, XH)
        R.ICONS[f'warplate_{p}'] = _recolor(f'{VAN}/item/netherite_{p}.png', WL, WH, stretch=1.8)
    handle = lambda x, y: x <= 5 and y >= 10                 # (the vanilla sword's grip stays as it is)
    for k, lo, hi in (('plasma_cutter', (20, 60, 10), (190, 255, 150)), ('graviton_edge', (40, 10, 70), (220, 170, 255)),
                      ('phase_saber', (10, 50, 70), (200, 250, 255)), ('vorn_annihilator', WL, WH)):
        R.ICONS[k] = _recolor(f'{VAN}/item/netherite_sword.png', lo, hi, keep=handle, stretch=1.6)
    R.ICONS['graviton_pick'] = _recolor(f'{VAN}/item/netherite_pickaxe.png', WL, WH, keep=lambda x, y: x + y >= 15 and x <= 9, stretch=1.8)
    R.HANDHELD_EXTRA |= set(WEAPONS) | {'graviton_pick'}
    c = R.cube
    R.HATS['xeno_antennae'] = ({'b': 'minecraft:block/lime_concrete', 's': 'minecraft:block/green_concrete', 'g': 'minecraft:block/verdant_froglight_side'}, [
        c((3.5, 15, 3.5), (12.5, 16, 4.5), 'b'), c((3.5, 15, 11.5), (12.5, 16, 12.5), 'b'), c((3.5, 15, 4.5), (4.5, 16, 11.5), 'b'), c((11.5, 15, 4.5), (12.5, 16, 11.5), 'b'),
        c((4.5, 16, 7.5), (5.5, 21, 8.5), 's'), c((10.5, 16, 7.5), (11.5, 21, 8.5), 's'), c((4, 21, 7), (6, 23, 9), 'g'), c((10, 21, 7), (12, 23, 9), 'g')])
    # the wheel: six coloured spokes in a gold rim, a hub in the middle
    from PIL import Image, ImageDraw
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for n, col in enumerate(('#ff8ad8', '#b48cff', '#5ab8e0', '#7ad06a', '#ffe040', '#ff7040')):
        d.pieslice((1, 1, 14, 14), n * 60 - 90, n * 60 - 30, fill=col)
    d.ellipse((1, 1, 14, 14), outline='#c89a2a'); d.ellipse((6, 6, 9, 9), fill='#5a3a1a', outline='#ffd870')
    R.ICONS['partner_wheel'] = im

    def post(R2):
        for layer in ('humanoid', 'humanoid_leggings'):
            _recolor(f'{VAN}/entity/equipment/{layer}/diamond.png', XL, XH).save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', layer, 'xenoplate.png'))
            _recolor(f'{VAN}/entity/equipment/{layer}/netherite.png', WL, WH, stretch=1.8).save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', layer, 'warplate.png'))
        for nm in ('xenoplate', 'warplate'):
            R2.wj(f'assets/bm/equipment/{nm}.json', {'layers': {'humanoid': [{'texture': f'bm:{nm}'}], 'humanoid_leggings': [{'texture': f'bm:{nm}'}]}})
    R.POST.append(post)


def repair_wheel(G, PW, holds):
    """(2.98b) once for each player: every partner on their wheel back in its own slot, by the item that slot actually holds -
    whatever version the world's wheel was saved by. Each slot's item comes out (into a list), the slot emptied; then each item
    goes back into the slot of the partner whose item it is. A slot with no item kept (none ever, since 2.84c) is left be."""
    fn = G.fn
    N = len(PW)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.pwfix dummy']
    G.OBJECTIVES += ['bm.pwfix']
    G.FUNCS['loop/second'].append(f'execute as @a at @s unless score @s bm.pwfix matches {REPAIR} run function bm:p179/fix/run')
    fn('p179/fix/run', [f'scoreboard players set @s bm.pwfix {REPAIR}', 'execute unless score @s bm.pid matches 1.. run return 0',
                        'function bm:p179/w/pid', 'data remove storage bm:tmp pwfix', 'data modify storage bm:tmp pwfix.items set value []',
                        'scoreboard players set #pwmv bm.rng 0'] +
       [f'execute if score @s bm.pw{i} matches 1 run function bm:p179/fix/take{i} with storage bm:tmp pw' for i in range(N)] +
       ['function bm:p179/fix/place', 'function bm:p179/k/off_clear',
        'execute if score #pwmv bm.rng matches 1.. run ' + G.tellraw('@s', [T('[', 'dark_gray'), T('Partner Wheel', '#b48cff', bold=True), T('] ', 'dark_gray'),
                                                                          T('Your partners are back in their own places on the wheel.', 'gray')])])
    for i in range(N):
        fn(f'p179/fix/take{i}', [f'$execute unless data storage bm:pw p$(pid).k{i} run return 0',
                                 f'data modify storage bm:tmp pwfix.items append value {{i:{i}}}',
                                 f'$data modify storage bm:tmp pwfix.items[-1].it set from storage bm:pw p$(pid).k{i}',
                                 f'$data remove storage bm:pw p$(pid).k{i}', f'scoreboard players set @s bm.pw{i} 0'])
    fn('p179/fix/place', ['execute unless data storage bm:tmp pwfix.items[0] run return 0',
                          'data modify storage bm:tmp pwfix.cur set from storage bm:tmp pwfix.items[0]', 'data remove storage bm:tmp pwfix.items[0]',
                          'function bm:p179/fix/one', 'function bm:p179/fix/place'])
    fn('p179/fix/one', ['data modify storage bm:tmp pwfix.id set value "?"',
                        'data modify storage bm:tmp pwfix.id set from storage bm:tmp pwfix.cur.it.components."minecraft:custom_data".bm',
                        'execute store result score #pwi bm.rng run data get storage bm:tmp pwfix.cur.i'] +
       [f'execute if function bm:p179/fix/is{j} run return run function bm:p179/fix/put{j} with storage bm:tmp pw' for j in range(N)] +
       ['function bm:p179/fix/drop'])
    # (is the item's id this partner's? - copied, then overwritten with theirs: no change means the same)
    for j, (*_r, iid) in enumerate(PW):
        fn(f'p179/fix/is{j}', ['data modify storage bm:tmp pwfix.c set from storage bm:tmp pwfix.id',
                               f'execute store success score #pwd bm.rng run data modify storage bm:tmp pwfix.c set value "{iid}"',
                               'execute if score #pwd bm.rng matches 0 run return 1', 'return 0'])
    for j in range(N):
        fn(f'p179/fix/put{j}', [f'execute if score @s bm.pw{j} matches 1 run return run function bm:p179/fix/drop',
                                f'$data modify storage bm:pw p$(pid).k{j} set from storage bm:tmp pwfix.cur.it', f'scoreboard players set @s bm.pw{j} 1',
                                f'execute unless score #pwi bm.rng matches {j} run scoreboard players add #pwmv bm.rng 1'])
    # (an item that is nobody's - or a second of someone's: handed back, at your feet)
    fn('p179/fix/drop', ['summon minecraft:item ~ ~ ~ {Item:{id:"minecraft:stone",count:1},Tags:["bm.pwfixd"],PickupDelay:0s}',
                         'data modify entity @e[type=minecraft:item,tag=bm.pwfixd,limit=1] Item set from storage bm:tmp pwfix.cur.it', 'scoreboard players add #pwmv bm.rng 1',
                         'tag @e[type=minecraft:item,tag=bm.pwfixd] remove bm.pwfixd'])

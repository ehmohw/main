"""Phase 2.49: followers vanish with their summoner's death; the Shifting Blade, Pick and Bow.

- FOLLOWERS (Emma, Cecil): if the player who summoned them dies, they vanish in a burst of magic (their ribbon / gem
  dropped with everything else - so they don't wander leaderless). No cooldown: pick the item up and call them again.
- THE SHIFTING ARMS (Vinny "Two-Blades" sells them: 16 Trophies + 32 Blood Crystals each). Like Leo's Trident, press
  swap-hands (F) to change form - each press the next, sneak + F the one before. Every form carries the best vanilla
  enchantments it can (never above their vanilla maximum), and never breaks.
  - SHIFTING BLADE: sword -> axe -> mace -> spear -> trident.
  - SHIFTING PICK: pickaxe -> axe -> shovel -> hoe -> shears -> fishing rod -> brush -> flint and steel.
  - SHIFTING BOW: bow -> crossbow -> trident."""
from items import item, T
from nbt import B
import economy

UNBR = {'minecraft:unbreakable': {}}
FORT = {'minecraft:efficiency': 5, 'minecraft:fortune': 3, 'minecraft:unbreaking': 3, 'minecraft:mending': 1}
SILK = {'minecraft:efficiency': 5, 'minecraft:silk_touch': 1, 'minecraft:unbreaking': 3, 'minecraft:mending': 1}
TRIDENT = {'minecraft:loyalty': 3, 'minecraft:impaling': 5, 'minecraft:channeling': 1, 'minecraft:unbreaking': 3, 'minecraft:mending': 1}
def _picks(T):
    return [('pickaxe', 'Pickaxe', 'minecraft:netherite_pickaxe', T), ('axe', 'Axe', 'minecraft:netherite_axe', T),
            ('shovel', 'Shovel', 'minecraft:netherite_shovel', T), ('hoe', 'Hoe', 'minecraft:netherite_hoe', T),
            ('shears', 'Shears', 'minecraft:shears', {'minecraft:efficiency': 5, 'minecraft:unbreaking': 3, 'minecraft:mending': 1}),
            ('rod', 'Fishing Rod', 'minecraft:fishing_rod', {'minecraft:luck_of_the_sea': 3, 'minecraft:lure': 3, 'minecraft:unbreaking': 3, 'minecraft:mending': 1}),
            ('brush', 'Brush', 'minecraft:brush', {'minecraft:unbreaking': 3, 'minecraft:mending': 1}),
            ('flint', 'Flint and Steel', 'minecraft:flint_and_steel', {'minecraft:unbreaking': 3, 'minecraft:mending': 1})]
ARMS = {
    'blade': ('Shifting Blade', '#ff8a5a', 'A blade that remembers every weapon it has ever been.', [
        ('sword', 'Sword', 'minecraft:netherite_sword', {'minecraft:sharpness': 5, 'minecraft:looting': 3, 'minecraft:fire_aspect': 2, 'minecraft:knockback': 2,
                                                         'minecraft:sweeping_edge': 3, 'minecraft:unbreaking': 3, 'minecraft:mending': 1}),
        ('axe', 'Axe', 'minecraft:netherite_axe', {'minecraft:sharpness': 5, 'minecraft:efficiency': 5, 'minecraft:fortune': 3, 'minecraft:fire_aspect': 2,
                                                   'minecraft:unbreaking': 3, 'minecraft:mending': 1}),
        ('mace', 'Mace', 'minecraft:mace', {'minecraft:density': 5, 'minecraft:wind_burst': 3, 'minecraft:fire_aspect': 2, 'minecraft:unbreaking': 3, 'minecraft:mending': 1}),
        ('spear', 'Spear', 'minecraft:netherite_spear', {'minecraft:sharpness': 5, 'minecraft:lunge': 3, 'minecraft:fire_aspect': 2, 'minecraft:knockback': 2,
                                                         'minecraft:unbreaking': 3, 'minecraft:mending': 1}),
        ('trident', 'Trident', 'minecraft:trident', {'minecraft:riptide': 3, 'minecraft:impaling': 5, 'minecraft:unbreaking': 3, 'minecraft:mending': 1})]),
    'pick': ('Shifting Pick (Fortune)', '#7ad0ff', 'A tool for every trade, one at a time.', _picks(FORT)),
    'picksilk': ('Shifting Pick (Silk Touch)', '#c0a0ff', 'A tool for every trade - and a gentle touch.', _picks(SILK)),
    'bow': ('Shifting Bow', '#a8f070', 'It strings itself to whatever the moment needs.', [
        ('bow', 'Bow', 'minecraft:bow', {'minecraft:power': 5, 'minecraft:punch': 2, 'minecraft:flame': 1, 'minecraft:infinity': 1, 'minecraft:unbreaking': 3}),
        ('crossbow', 'Crossbow', 'minecraft:crossbow', {'minecraft:quick_charge': 3, 'minecraft:multishot': 1, 'minecraft:unbreaking': 3, 'minecraft:mending': 1}),
        ('trident', 'Trident', 'minecraft:trident', TRIDENT)]),
}
# (2.54) SHIFTING ARMOUR: one piece, every tier's look - it always protects like netherite (the base item is netherite)
TIERS = [('leather', 'Leather', 'leather'), ('chainmail', 'Chainmail', 'chainmail'), ('copper', 'Copper', 'copper'), ('iron', 'Iron', 'iron'),
         ('golden', 'Gold', 'gold'), ('diamond', 'Diamond', 'diamond'), ('netherite', 'Netherite', 'netherite')]
PIECES = {'helmet': ('head', 'Helmet', {'minecraft:protection': 4, 'minecraft:respiration': 3, 'minecraft:aqua_affinity': 1}),
          'chestplate': ('chest', 'Chestplate', {'minecraft:protection': 4, 'minecraft:thorns': 3}),
          'leggings': ('legs', 'Leggings', {'minecraft:protection': 4, 'minecraft:swift_sneak': 3}),
          'boots': ('feet', 'Boots', {'minecraft:protection': 4, 'minecraft:feather_falling': 4, 'minecraft:depth_strider': 3, 'minecraft:soul_speed': 3})}
for _p, (_slot, _pn, _en) in PIECES.items():
    _tiers = TIERS + ([('turtle', 'Turtle', 'turtle_scute')] if _p == 'helmet' else [])
    ARMS[f'armor_{_p}'] = (f'Shifting {_pn}', '#d0d8e8', 'Any armour you like the look of - netherite underneath.',
                           [(t, tn, f'minecraft:netherite_{_p}', dict(_en, **{'minecraft:unbreaking': 3, 'minecraft:mending': 1}),
                             {'minecraft:item_model': f'minecraft:{t}_{_p}',
                              'minecraft:equippable': {'slot': _slot, 'asset_id': f'minecraft:{asset}', 'equip_sound': 'minecraft:item.armor.equip_netherite'}})
                            for t, tn, asset in _tiers])
FIRST = {fam: f'shift_{fam}_{forms[0][0]}' for fam, (_n, _c, _f, forms) in ARMS.items()}
# price: a Shifting Core (16 Trophies + 32 Blood Crystals) plus a Netherite Ingot for every netherite form it can take -
# no skipping netherite. Armour: 6 Trophies + 1 Netherite Ingot a piece.
NETH = {fam: sum(1 for f in forms if 'netherite' in f[2]) for fam, (_n, _c, _f, forms) in ARMS.items() if not fam.startswith('armor_')}
item('shift_core', 'minecraft:totem_of_undying', 'Shifting Core', '#e0c0ff',
     ['A heart of molten possibility.', ('Vinny forges it into a Shifting weapon or tool', 'blue'), ('with one Netherite Ingot for every netherite form.', 'blue')],
     model='minecraft:heart_of_the_sea', stack=16, cat='weapon', glint=True, comps={'!minecraft:death_protection': {}})
economy.DIRECT['shift_core'] = (('trophy', 16), ('blood_crystal', 32))

for _fam, (_name, _col, _flav, _forms) in ARMS.items():
    _all = ' · '.join(f[1] for f in _forms)
    _arm = _fam.startswith('armor_')
    for _f in _forms:
        _key, _fname, _base, _ench = _f[:4]
        _extra = _f[4] if len(_f) > 4 else {}
        item(f'shift_{_fam}_{_key}', _base, f'{_name}: {_fname}', _col,
             [_flav, ('Hold it and press swap-hands (F): the next ' + ('look.' if _arm else 'form.'), 'blue'),
              ('Sneak + F: the one before.', 'blue'), (_all, 'gray'),
              (('Always protects like netherite.' if _arm else 'Every form carries its best enchantments.'), 'dark_purple'), ('Never breaks.', 'dark_purple')],
             stack=1, cat='weapon', tier=3, custom_extra={'bm_shift': B(1)},
             comps=dict(UNBR, **{'minecraft:enchantments': dict(_ench)}, **_extra))


def extend_offers(O, offer):
    O['arms'].append(offer(('trophy', 16), ('shift_core', 1), ('blood_crystal', 32)))
    for fam in ARMS:
        if fam.startswith('armor_'):
            O['arms'].append(offer(('trophy', 6), (FIRST[fam], 1), ('netherite_ingot', 1)))
        else:
            O['arms'].append(offer(('shift_core', 1), (FIRST[fam], 1), ('netherite_ingot', NETH[fam]) if NETH[fam] else None))


def generate(G):
    fn, title, tellraw, give, PREFIX = G.fn, G.title, G.tellraw, G.give, G.PREFIX
    tick = []
    holds = '*[minecraft:custom_data~{bm:"%s"}]'

    # ------------------------------------------------------------------ followers vanish when their summoner dies
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.fdie deathCount']
    G.OBJECTIVES += ['bm.fdie']
    tick.append('execute as @a[scores={bm.fdie=1..}] run function bm:p62/died')
    fn('p62/died', ['scoreboard players reset @s bm.fdie', 'execute unless score @s bm.pid matches 1.. run return 0',
                    'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #gone bm.rng 0',
                    'execute as @e[type=minecraft:cat,tag=bm.emmapet] if score @s bm.pid = #me bm.pid at @s run function bm:p62/emma_go',
                    'execute as @e[type=minecraft:wolf,tag=bm.cecilpet] if score @s bm.pid = #me bm.pid at @s run function bm:p62/cecil_go',
                    'execute if score #gone bm.rng matches 1.. run ' + tellraw('@s', PREFIX + [T('Your followers fade away with you. ', 'gray'),
                                                                                          T('Pick up the ribbon or the gem and call them again.', 'dark_gray')])])
    fn('p62/emma_go', ['scoreboard players add #gone bm.rng 1', 'function bm:p57/fade', 'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    fn('p62/cecil_go', ['scoreboard players add #gone bm.rng 1', 'function bm:p46/pet/fade', 'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])

    # ------------------------------------------------------------------ the Shifting Arms: swap-hands changes the form
    # (pressing F moves the item to the off-hand: put back what was there, and hand over the next form)
    tick.append('execute as @a if items entity @s weapon.offhand *[minecraft:custom_data~{bm_shift:1b}] at @s run function bm:p62/shift')
    shift = []
    for fam, (name, col, _f, forms) in ARMS.items():
        n = len(forms)
        for i, f in enumerate(forms):
            iid = f'shift_{fam}_{f[0]}'
            for d, nm in ((1, 'next'), (-1, 'prev')):
                to = forms[(i + d) % n]
                fn(f'p62/to/{iid}_{nm}', ['item replace entity @s weapon.offhand from entity @s weapon.mainhand',
                                          f'item replace entity @s weapon.mainhand with {G.item_arg(f"shift_{fam}_{to[0]}")}',
                                          'particle minecraft:enchant ~ ~1.2 ~ 0.3 0.4 0.3 0.6 20', 'particle minecraft:wax_off ~ ~1.1 ~ 0.3 0.3 0.3 0 6',
                                          'playsound minecraft:item.armor.equip_netherite player @a[distance=..12] ~ ~ ~ 0.8 1.4',
                                          'playsound minecraft:block.amethyst_block.chime player @a[distance=..12] ~ ~ ~ 0.6 1.8',
                                          title('@s', 'actionbar', [T(name + ': ', col, bold=True), T(to[1], 'white', bold=True)])])
            shift += [f'execute if items entity @s weapon.offhand {holds % iid} if predicate bm:p20/sneaking run return run function bm:p62/to/{iid}_prev',
                      f'execute if items entity @s weapon.offhand {holds % iid} run return run function bm:p62/to/{iid}_next']
    fn('p62/shift', shift)

    # ------------------------------------------------------------------ (2.50) the Ethereal Gem empowers Emma and withers the night's foes
    gem = '*[minecraft:custom_data~{bm:"ethereal_gem"}]'
    shrine = '@e[type=minecraft:item_display,tag=bm.eshr,distance=..30]'
    sec = G.FUNCS['loop/second']
    sec[-1:-1] = ['execute as @e[type=minecraft:cat,tag=bm.emmapet] at @s run function bm:p62/emgem',
                  f'execute as @e[type=minecraft:item_display,tag=bm.eshr] at @s run function bm:p62/blight',
                  f'execute as @a[gamemode=!spectator] if items entity @s container.* {gem} at @s run function bm:p62/blight_near',
                  f'execute as @a[gamemode=!spectator] unless items entity @s container.* {gem} if items entity @s weapon.offhand {gem} at @s run function bm:p62/blight_near']
    # Emma is empowered while an Ethereal Gem is set within 30 blocks of her, or her summoner carries one
    fn('p62/emgem', ['tag @s remove bm.emgem', f'execute if entity {shrine} run tag @s add bm.emgem', 'tag @s add bm.emq',
                     f'execute on owner if items entity @s container.* {gem} run tag @e[type=minecraft:cat,tag=bm.emq] add bm.emgem',
                     f'execute on owner if items entity @s weapon.offhand {gem} run tag @e[type=minecraft:cat,tag=bm.emq] add bm.emgem',
                     'tag @s remove bm.emq', 'execute if entity @s[tag=bm.emgem] run particle minecraft:end_rod ~ ~1.3 ~ 0.3 0.5 0.3 0.01 2'])
    # Blood Moon and invasion foes near the gem: much slower, much weaker, and slowly burned away
    def blight(r):
        return [f'execute as @e[tag={t},distance=..{r}] at @s run function bm:p62/wither' for t in ('bm.blood', 'bm.vorn', 'bm.bio', 'bm.elite', 'bm.champion')]
    fn('p62/blight', blight(30))
    fn('p62/blight_near', blight(16))
    fn('p62/wither', ['effect give @s minecraft:slowness 2 2 true', 'effect give @s minecraft:weakness 2 2 true',
                      'execute unless entity @s[tag=bm.blg] run damage @s 1 minecraft:magic', 'tag @s[tag=bm.blg] add bm.blg2', 'tag @s add bm.blg',
                      'tag @s[tag=bm.blg2] remove bm.blg', 'tag @s remove bm.blg2',
                      'particle minecraft:end_rod ~ ~1 ~ 0.2 0.4 0.2 0.01 1', 'particle minecraft:dust{color:[0.9,0.8,1.0],scale:0.8} ~ ~1 ~ 0.3 0.5 0.3 0 3'])
    fn('admin/shifting_arms', [give(FIRST[f]) for f in ARMS] + [give('shift_core')])
    G.FUNCS['tick'] += tick

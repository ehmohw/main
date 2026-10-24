"""2.94d: THE ARCADE - the 8-bit corner of the Black Market, open only while the world is in hard mode.

THE SHOP     the empty house west of Fountain Plaza. Two pixel traders keep it - flat as paper dolls, front and back drawn
             (PixelLab, ref/pixellab/arcade), turned to face the room: BIT, a pixel rat (armour and weapons), and a PIXEL
             VILLAGER (props, practical things and weapon chips). Right-click either to trade, in Dread Tokens. Out of hard
             mode the house is empty again. Its own props stand about it: a ? block over the counter, an arcade cabinet, a pipe.
THE SETS     four of them, homages, each a full set's own power (and very strong: netherite and more, +2 health a piece):
               BOUNTY HUNTER (power suit)   fire and lava can't hurt you; the visor sees in the dark; Jump Boost II, Speed
               BLUE BOMBER                  every blow fires a buster shot at the nearest monster too; Strength
               PLUMBER                      no fall damage; Jump Boost II; land on a monster from above: STOMP (14), and you
                                            bounce off it
               VAMPIRE HUNTER               the undead take 8 more from every blow; by night, Regeneration
THE WEAPONS  the 8-BIT BLADE (at full health, right-click: a sword beam), the VAMPIRE KILLER (a whip: 3 blocks more reach,
             8 more to the undead), the ARM BUSTER (right-click: buster shots) and the FIRE FLOWER (right-click: fireballs that
             set what they hit alight).
THE CHIPS    a weapon's upgrades: hold the chip, the weapon in your off hand, use the chip. Any sword, axe, mace, trident or
             arcade weapon takes one of each, for good:
               GLITCH        one blow in five glitches the monster: 6 more, and it blinks somewhere near
               MISSINGNO.    a kill, one in four: the stack in your sixth hotbar slot grows by one
               GAME GENIE    +4 attack damage
               TURBO         +0.8 attack speed
THE PROPS    set them down on a block (sneak + punch one to pick it up):
               ? BLOCK            right-click: a Token pops out (once a day each)
               WARP PIPE          set two down: right-click either - you come out of the other (anywhere, any dimension)
               ARCADE CABINET     right-click: a game - a chiptune, a score, and Luck for a minute
               BLADE IN THE STONE, TRIANGLES OF POWER    for show (right-click: a chime)
               SAVE POINT         right-click: your spawn is here, and you're healed (once a minute)
PRACTICAL    HEART CONTAINER (eat: +1 heart for good, up to 3), SUPER STAR (use: 10 s invincible - Resistance V, Speed II,
             and whatever you touch is hurt), POWER MUSHROOM (use: a minute bigger and stronger), 1-UP MUSHROOM (held when
             you'd die: like a totem, you live)."""
import math
from items import item, attr, T, TOTEM, ITEMS, consumable
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import mgeo
import market3
import pxart
import arcade_art as AA

COL, COL_D = '#5af0a0', '#1a8a5a'
GOLD = '#ffcf40'
W = market3.W
RAT_POS = (24.5, W, 51.6)                     # (the house west of Fountain Plaza - the 2.81 town's one empty house)
VIL_POS = (26.5, W, 51.6)
PROPS_IN = [('arcade_cabinet', (23.5, W, 56.4), 0), ('warp_pipe', (27.5, W, 56.4), 0), ('q_block', (25.5, W + 2.4, 56.6), 0)]
for _p, _w in ((RAT_POS, 'Bit'), (VIL_POS, 'the Pixel Villager'), ((25.5, W, 54.5), "the Arcade's customers")):
    mgeo.need_air(_p, _w)
RAT_H, VIL_H = 1.3, 1.8

# ================================================================== the sets
SLOTS = {'head': ('helmet', 'armor.head'), 'chest': ('chestplate', 'armor.chest'), 'legs': ('leggings', 'armor.legs'), 'feet': ('boots', 'armor.feet')}
SETS = {   # key: (name, colour, [(iid, slot, name)], the set's power, lore)
    'hunter': ('Bounty Hunter', '#ff8a3a', [('hunter_helm', 'head', 'Hunter Visor'), ('hunter_plate', 'chest', 'Power Plate'),
                                            ('hunter_greaves', 'legs', 'Suit Greaves'), ('hunter_boots', 'feet', 'Thruster Boots')],
               ['THE SUIT: fire and lava can\'t hurt you,', 'the visor sees in the dark; Jump Boost II, Speed.']),
    'bomber': ('Blue Bomber', '#4a9aff', [('bomber_helm', 'head', 'Bomber Helm'), ('bomber_chest', 'chest', 'Bomber Chestguard'),
                                          ('bomber_legs', 'legs', 'Bomber Leggings'), ('bomber_boots', 'feet', 'Bomber Boots')],
               ['THE BUSTER: every blow fires a shot', 'at the nearest monster too; Strength.']),
    'plumber': ('Plumber', '#ff4a4a', [('plumber_cap', 'head', "Plumber's Cap"), ('plumber_shirt', 'chest', "Plumber's Overalls"),
                                       ('plumber_overalls', 'legs', "Plumber's Dungarees"), ('plumber_boots', 'feet', "Plumber's Boots")],
                ['THE STOMP: land on a monster from', 'above - 14, and you bounce. No fall', 'damage; Jump Boost II.']),
    'vhunter': ('Vampire Hunter', '#d04040', [('vhunter_band', 'head', "Hunter's Headband"), ('vhunter_cuirass', 'chest', "Hunter's Cuirass"),
                                              ('vhunter_legs', 'legs', "Hunter's Leggings"), ('vhunter_boots', 'feet', "Hunter's Boots")],
                ['THE NIGHT HUNT: the undead take 8', 'more from every blow; by night,', 'Regeneration.']),
}
ARM = {'head': 4, 'chest': 9, 'legs': 7, 'feet': 4}
for _k, (_sn, _c, _pcs, _pow) in SETS.items():
    for _iid, _slot, _nm in _pcs:
        _piece = SLOTS[_slot][0]
        mods = [attr('armor', ARM[_slot], _slot, ident=f'bm:{_iid}_armor'), attr('armor_toughness', 4, _slot, ident=f'bm:{_iid}_tough'),
                attr('knockback_resistance', 0.1, _slot, ident=f'bm:{_iid}_kb'), attr('max_health', 2, _slot, ident=f'bm:{_iid}_hp')]
        if _iid == 'plumber_boots':
            mods.append(attr('fall_damage_multiplier', -1, _slot, op='add_multiplied_total', ident='bm:plumber_boots_fall'))
        item(_iid, f'minecraft:netherite_{_piece}', _nm, _c,
             [(f'{_sn} - one of four. 8-bit made real.', 'gray'), ('+2 health; netherite and more.', 'blue')] + [(l, _c) for l in _pow] +
             [('Sold by Bit, in the Arcade (hard mode).', 'dark_gray')],
             model=f'bm:{_iid}', stack=1, cat='armor', tier=3, bold=True,
             comps={'minecraft:unbreakable': {}, 'minecraft:attribute_modifiers': mods,
                    'minecraft:equippable': {'slot': _slot, 'asset_id': f'bm:arc_{_k}', 'equip_sound': 'minecraft:item.armor.equip_iron'},
                    'minecraft:tooltip_display': {'hidden_components': ['minecraft:unbreakable']}},
             custom_extra={'bm_arcset': _k})

# ================================================================== the weapons
SWORD = lambda dmg, spd, extra=(): [attr('attack_damage', dmg, 'mainhand', ident='minecraft:base_attack_damage'),
                                    attr('attack_speed', spd, 'mainhand', ident='minecraft:base_attack_speed')] + list(extra)
item('pixel_blade', 'minecraft:netherite_sword', '8-Bit Blade', '#7ad0ff',
     ['A hero\'s sword, sixteen colours sharp.', ('At full health, right-click: a SWORD BEAM', 'blue'), ('flies at the nearest monster (10).', 'blue'),
      ('Sold by Bit, in the Arcade (hard mode).', 'dark_gray')],
     model='bm:pixel_blade', stack=1, cat='gear', tier=3, bold=True,
     comps=dict(hold('none'), **{'minecraft:unbreakable': {}, 'minecraft:attribute_modifiers': SWORD(13, -2.4)}))
HOLD['pixel_blade'] = 'bm:p216/w/beam'
item('vampire_killer', 'minecraft:netherite_sword', 'Vampire Killer', '#c06040',
     ['A whip with a morning-star tip.', ('Reach: 3 blocks more.', 'blue'), ('The undead take 8 more from it.', 'blue'),
      ('Sold by Bit, in the Arcade (hard mode).', 'dark_gray')],
     model='bm:vampire_killer', stack=1, cat='gear', tier=3, bold=True,
     comps={'minecraft:unbreakable': {}, 'minecraft:attribute_modifiers': SWORD(11, -2.6, [attr('entity_interaction_range', 3, 'mainhand', ident='bm:vampire_killer_reach')])})
item('arm_buster', TOTEM, 'Arm Buster', '#4a9aff',
     ['A robot\'s arm cannon.', ('Right-click: a buster shot at the nearest', 'blue'), ('monster in front of you (7).', 'blue'),
      ('Sold by Bit, in the Arcade (hard mode).', 'dark_gray')],
     model='bm:arm_buster', stack=1, cat='gear', tier=3, bold=True, comps=hold('none'))
HOLD['arm_buster'] = 'bm:p216/w/buster'
item('fire_flower', TOTEM, 'Fire Flower', '#ff7a2a',
     ['Its petals are on fire. Don\'t sniff it.', ('Right-click: a bouncing fireball - 8,', 'blue'), ('and it sets what it hits alight.', 'blue'),
      ('Sold by Bit, in the Arcade (hard mode).', 'dark_gray')],
     model='bm:fire_flower', stack=1, cat='gear', tier=3, bold=True, comps=hold('none'))
HOLD['fire_flower'] = 'bm:p216/w/fire'

# ================================================================== the chips
CHIPS = {   # key: (name, colour, what it does)
    'glitch': ('Glitch Chip', '#ff4ad8', ['THE GLITCH: one blow in five glitches', 'the monster - 6 more, and it blinks away.']),
    'missingno': ('MissingNo. Chip', '#b0a0ff', ['MISSINGNO.: a kill, one in four - the', 'stack in your sixth hotbar slot grows by one.']),
    'genie': ('Game Genie Chip', GOLD, ['A cheat code: +4 attack damage.']),
    'turbo': ('Turbo Chip', '#ff5050', ['TURBO: +0.8 attack speed.']),
}
for _k, (_nm, _c, _l) in CHIPS.items():
    item(f'chip_{_k}', TOTEM, _nm, _c, [(x, _c) for x in _l] + [('Hold it, the weapon in your off hand: use.', 'blue'),
                                                               ('A sword, axe, mace, trident or arcade weapon;', 'gray'), ('one of each on a weapon, for good.', 'gray')],
         model=f'bm:chip_{_k}', stack=16, cat='magic', glint=True, comps=hold('none'))
    HOLD[f'chip_{_k}'] = f'bm:p216/chip/{_k}'

# ================================================================== the props
PROPS = {   # key: (name, colour, lore, model height in blocks)
    'q_block': ('? Block', GOLD, ['Right-click it: a Token pops out (once a day).'], 0.8),
    'warp_pipe': ('Warp Pipe', '#3ac83a', ['Set two down: right-click one,', 'and out you come from the other.'], 1.1),
    'arcade_cabinet': ('Arcade Cabinet', '#5a8aff', ['Right-click: a game, a high score,', 'and Luck for a minute.'], 1.9),
    'blade_stone': ('Blade in the Stone', '#7ad0ff', ['A hero\'s sword, waiting.'], 1.4),
    'power_triangles': ('Triangles of Power', GOLD, ['Three golden triangles - power, wisdom, courage.'], 1.0),
    'save_point': ('Save Point', '#7ae0ff', ['Right-click: your spawn is here,', 'and you\'re healed (once a minute).'], 1.2),
}
for _k, (_nm, _c, _l, _h) in PROPS.items():
    item(_k, TOTEM, _nm, _c, [(x, _c) for x in _l] + [('Use it on a block to set it down.', 'blue'), ('Sneak + punch it to pick it up.', 'gray')],
         model=f'bm:{_k}', stack=16, cat='fun', comps=hold('none'))
    HOLD[_k] = f'bm:p216/place/{_k}'

# ================================================================== the practical things
item('heart_container', TOTEM, 'Heart Container', '#ff4a6a',
     ['A whole heart, in a jar of light.', ('Eat it: +1 heart for good (up to 3).', 'blue')], model='bm:heart_container', stack=16, cat='magic',
     comps={'minecraft:consumable': consumable(1.2, 'eat', 'minecraft:entity.generic.eat'), 'minecraft:food': {'nutrition': 0, 'saturation': 0.0, 'can_always_eat': True}})
item('super_star', TOTEM, 'Super Star', GOLD,
     ['It hums a very fast tune.', ('Use: 10 s invincible - Resistance V,', 'blue'), ('Speed II, and what you touch is hurt.', 'blue')],
     model='bm:super_star', stack=16, cat='magic', glint=True, comps=hold('none'))
HOLD['super_star'] = 'bm:p216/use/star'
item('power_mushroom', TOTEM, 'Power Mushroom', '#ff4a4a',
     ['Red, spotted, smiling.', ('Use: a minute bigger and stronger.', 'blue')], model='bm:power_mushroom', stack=16, cat='magic', comps=hold('none'))
HOLD['power_mushroom'] = 'bm:p216/use/grow'
item('oneup_mushroom', TOTEM, '1-UP Mushroom', '#4ad84a',
     ['An extra life, spotted green.', ('Held when you\'d die: you live -', 'blue'), ('like a totem.', 'blue')], model='bm:oneup_mushroom', stack=1, cat='magic')
ITEMS['oneup_mushroom']['comps'].pop('!minecraft:death_protection')          # (a totem underneath: its own extra life, kept)

# ================================================================== the traders' stock (Dread Tokens)
RAT_STOCK = [(i, 1, 4) for _k, (_sn, _c, _pcs, _pow) in SETS.items() for i, _s, _n in _pcs] + \
    [('pixel_blade', 1, 6), ('vampire_killer', 1, 6), ('arm_buster', 1, 6), ('fire_flower', 1, 6)]
VIL_STOCK = [('chip_glitch', 1, 3), ('chip_missingno', 1, 5), ('chip_genie', 1, 4), ('chip_turbo', 1, 3),
             ('q_block', 1, 2), ('warp_pipe', 2, 3), ('arcade_cabinet', 1, 2), ('blade_stone', 1, 2), ('power_triangles', 1, 2), ('save_point', 1, 3),
             ('heart_container', 1, 5), ('super_star', 1, 2), ('power_mushroom', 2, 1), ('oneup_mushroom', 1, 3)]

_SPR = {}


def spr(k):
    if k not in _SPR:
        _SPR[k] = pxart.Sprite(k, f'arc_{k}_', {'bit_rat': RAT_H, 'px_villager': VIL_H}[k], {'idle': ('idle', None)})
    return _SPR[k]


def _have_traders():
    import os
    return all(os.path.isdir(os.path.join(pxart.HERE, 'ref', 'pixellab', 'arcade', k)) for k in ('bit_rat', 'px_villager'))


def _shots():
    """the shots' sprites (drawn here): a buster pellet, a fireball, a sword beam"""
    from PIL import Image, ImageDraw
    out = {}
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((3, 4, 12, 11), fill=(255, 240, 120, 255), outline=(40, 30, 10, 255)); d.ellipse((5, 5, 8, 8), fill=(255, 255, 255, 255))
    out['arc_pj_pellet'] = im
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2, 2, 13, 13), fill=(255, 90, 20, 255), outline=(90, 20, 0, 255)); d.ellipse((5, 4, 10, 9), fill=(255, 210, 60, 255))
    out['arc_pj_fire'] = im
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(1, 8), (6, 5), (15, 8), (6, 11)], fill=(180, 240, 255, 255), outline=(40, 120, 200, 255))
    out['arc_pj_beam'] = im
    return out


def textures():
    T_ = {}
    if _have_traders():
        for k in ('bit_rat', 'px_villager'):
            T_.update(spr(k).textures())
    for k in PROPS:
        T_[f'arc_prop_{k}'] = pxart.voxel(AA.icon(k), 'x', height=16.0 * PROPS[k][3] * 0.95, depth=4.0, back=AA.icon(k))[2]
    return T_


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    keys = [i for _k, (_sn, _c, _pcs, _pow) in SETS.items() for i, _s, _n in _pcs] + \
        ['pixel_blade', 'vampire_killer', 'arm_buster', 'fire_flower', 'heart_container', 'super_star', 'power_mushroom', 'oneup_mushroom'] + \
        [f'chip_{k}' for k in CHIPS] + list(PROPS)
    for k in keys:
        R.ICONS[k] = AA.icon(k)
    for k, im in _shots().items():
        R.ICONS[k] = im
    if _have_traders():
        for k in ('bit_rat', 'px_villager'):
            for name, (tex, els) in spr(k).models().items():
                R.HATS[name] = (tex, els)
            R.DISPLAY_3D_EXTRA = R.DISPLAY_3D_EXTRA + (spr(k).prefix,)

    def post(R2):
        if _have_traders():
            for k in ('bit_rat', 'px_villager'):
                spr(k).item_def(R2, f'arc_{k}')
        for k, (nm, c, l, h) in PROPS.items():                 # (the props: voxel models of their icons, standing on the block)
            tex, els, _sq = pxart.voxel(AA.icon(k), f'arc_prop_{k}', height=16.0 * h * 0.95, depth=4.0, back=AA.icon(k))
            R2.wj(f'assets/bm/models/item/arc_prop_{k}.json', {'textures': tex, 'elements': els})
            R2.wj(f'assets/bm/items/arc_prop_{k}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/arc_prop_{k}'}})
        for k in SETS:                                         # (the sets' armour layers)
            hum, leg = AA.paint(k)
            hum.save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'humanoid', f'arc_{k}.png'))
            leg.save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'humanoid_leggings', f'arc_{k}.png'))
            R2.wj(f'assets/bm/equipment/arc_{k}.json', {'layers': {'humanoid': [{'texture': f'bm:arc_{k}'}], 'humanoid_leggings': [{'texture': f'bm:arc_{k}'}]}})
    R.POST.append(post)


def generate(G):
    import phase212 as P212
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    P = [T('[', 'dark_gray'), T('The Arcade', COL, bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    second, fast, tick = G.FUNCS['loop/second'], G.FUNCS['loop/fast'], G.FUNCS['tick']
    objs = ['bm.arcd', 'bm.arcq', 'bm.arcs', 'bm.arcg', 'bm.arcp', 'bm.arcpn', 'bm.archc', 'bm.arcsv', 'bm.arcfl']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    FOE = 'type=#bm:hostile,tag=!bm.npc'

    # ---------------------------------------------------------------- the shop (only while the world is in hard mode)
    def offer(buy, sell):
        o = G.offer(buy, sell)
        o['buy']['count'] = Int(buy[1]); o['sell']['count'] = Int(sell[1])
        return o
    invis = [{'id': 'minecraft:invisibility', 'duration': -1, 'amplifier': 0, 'show_particles': B(0)}]
    trader = lambda tag, name, col, stock, prof: {
        'Tags': ['bm.npc', 'bm.arcnpc', tag], 'NoAI': B(1), 'Invulnerable': B(1), 'Silent': B(1),
        'PersistenceRequired': B(1), 'CustomName': T(name, col, bold=True), 'CustomNameVisible': B(1), 'active_effects': invis,
        'VillagerData': {'type': 'minecraft:plains', 'profession': f'minecraft:{prof}', 'level': Int(5)},
        'Offers': {'Recipes': [offer(('dread_token', p), (iid, n)) for iid, n, p in stock]}}
    rat = trader('bm.arcrat', 'Bit, the 8-Bit Trader', COL, RAT_STOCK, 'weaponsmith')
    vil = trader('bm.arcvil', 'the Pixel Villager', '#8ad870', VIL_STOCK, 'librarian')
    ident = [F(0), F(0), F(0), F(1)]

    def sprite_nbt(tag, k, h):
        S = spr(k)
        up = round(S.size / 2 - 6 * S.size / S.N, 3)
        return {'Tags': ['bm.npc', 'bm.arcspr', tag], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:arc_{k}'}},
                'item_display': 'fixed', 'view_range': F(2.0), 'brightness': {'block': Int(13), 'sky': Int(13)}, 'shadow_radius': F(0.4), 'shadow_strength': F(0.5),
                'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(up), F(0)], 'scale': [F(round(S.size, 4))] * 3}}
    have = _have_traders()
    rpos, vpos = mgeo.rel(RAT_POS), mgeo.rel(VIL_POS)
    fn('p216/spawn_rat', [f'summon minecraft:villager ~ ~ ~ {snbt(rat)}', 'tp @e[type=minecraft:villager,tag=bm.arcrat,distance=..1,limit=1] ~ ~ ~ ~ 0'] +
       ([f'summon minecraft:item_display ~ ~ ~ {snbt(sprite_nbt("bm.arcspr_rat", "bit_rat", RAT_H))}',
         'tp @e[type=minecraft:item_display,tag=bm.arcspr_rat,distance=..1,limit=1] ~ ~ ~ ~ 0'] if have else []) +
       ['particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.2 20', 'playsound minecraft:block.note_block.bit ambient @a[distance=..16] ~ ~ ~ 1 1.5'])
    fn('p216/spawn_vil', [f'summon minecraft:villager ~ ~ ~ {snbt(vil)}', 'tp @e[type=minecraft:villager,tag=bm.arcvil,distance=..1,limit=1] ~ ~ ~ ~ 0'] +
       ([f'summon minecraft:item_display ~ ~ ~ {snbt(sprite_nbt("bm.arcspr_vil", "px_villager", VIL_H))}',
         'tp @e[type=minecraft:item_display,tag=bm.arcspr_vil,distance=..1,limit=1] ~ ~ ~ ~ 0'] if have else []))
    shop_props = []
    for k, pos, yaw in PROPS_IN:
        shop_props.append((k, mgeo.rel(pos)))
    fn('p216/shop_props', [f'execute positioned {p} unless entity @e[type=minecraft:item_display,tag=bm.arcshop,distance=..0.6] rotated ~ 0 run '
                           f'summon minecraft:item_display ~ ~ ~ {snbt(_prop_nbt(k, ["bm.npc", "bm.arcshop"]))}' for k, p in shop_props])
    patch = G.FUNCS['p35/patch']
    patch += [f'execute if score #hard bm.cfg matches 1 positioned {rpos} unless entity @e[type=minecraft:villager,tag=bm.arcrat,distance=..2] rotated ~ 0 run function bm:p216/spawn_rat',
              f'execute if score #hard bm.cfg matches 1 positioned {vpos} unless entity @e[type=minecraft:villager,tag=bm.arcvil,distance=..2] rotated ~ 0 run function bm:p216/spawn_vil',
              f'execute if score #hard bm.cfg matches 1 positioned {rpos} as @e[type=minecraft:villager,tag=bm.arcrat,distance=..2] run data modify entity @s Offers set value {snbt(rat["Offers"])}',
              f'execute if score #hard bm.cfg matches 1 positioned {vpos} as @e[type=minecraft:villager,tag=bm.arcvil,distance=..2] run data modify entity @s Offers set value {snbt(vil["Offers"])}',
              'execute if score #hard bm.cfg matches 1 run function bm:p216/shop_props',
              f'execute unless score #hard bm.cfg matches 1 positioned {rpos} run kill @e[tag=bm.arcnpc,distance=..4]',
              f'execute unless score #hard bm.cfg matches 1 positioned {rpos} run kill @e[tag=bm.arcspr,distance=..4]',
              f'execute unless score #hard bm.cfg matches 1 positioned {rpos} run kill @e[tag=bm.arcshop,distance=..8]']
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.arcnpc]', 'kill @e[tag=bm.arcspr]', 'kill @e[tag=bm.arcshop]', 'kill @e[tag=bm.arcprop]', 'kill @e[tag=bm.arcpbox]']
    # their idle (the sprites breathe), and a word now and then
    if have:
        n_r, n_v = len(spr('bit_rat').frames['idle']), len(spr('px_villager').frames['idle'])
        tick.append('execute as @e[type=minecraft:item_display,tag=bm.arcspr] run function bm:p216/idle')
        fn('p216/idle', ['scoreboard players add @s bm.arcd 1', 'execute unless score @s bm.arcd matches 0..119 run scoreboard players set @s bm.arcd 0',
                         'scoreboard players operation #f bm.rng = @s bm.arcd', 'scoreboard players operation #f bm.rng /= #10 bm.rng'] +
           [f'execute if entity @s[tag=bm.arcspr_rat] if score #f bm.rng matches {i} run data modify entity @s item.components."minecraft:custom_model_data" set value {{strings:["idle_{i % n_r}"]}}'
            for i in range(12)] +
           [f'execute if entity @s[tag=bm.arcspr_vil] if score #f bm.rng matches {i} run data modify entity @s item.components."minecraft:custom_model_data" set value {{strings:["idle_{i % n_v}"]}}'
            for i in range(12)])
        G.FUNCS['load'][-1:-1] = ['scoreboard players set #10 bm.rng 10']
    lines_r = ['"Welcome to the Arcade! Everything\'s 8-bit, nothing\'s a toy."', '"Press START to buy something!"', '"Pixel armour - the hard kind of hard mode."',
               '"No refunds. No continues."']
    lines_v = ['"Hrrm."', '"Hrrrm! (it points at the ? block)"', '"Hrm hrm. (it taps a cartridge)"']
    second.append('execute as @e[type=minecraft:villager,tag=bm.arcrat] at @s if entity @a[distance=..5] run function bm:p216/mutter')
    fn('p216/mutter', ['execute store result score #vm bm.rng run random value 1..90'] +
       [f'execute if score #vm bm.rng matches {i + 1} run ' + title('@a[distance=..6]', 'actionbar', [T('Bit: ', COL), T(l, '#c8f0d8', italic=True)]) for i, l in enumerate(lines_r)] +
       [f'execute if score #vm bm.rng matches {i + 20} run ' + title('@a[distance=..6]', 'actionbar', [T('Pixel Villager: ', '#8ad870'), T(l, '#d8f0c8', italic=True)]) for i, l in enumerate(lines_v)])

    # ---------------------------------------------------------------- the sets: a full set worn, its power (each second)
    def full(k):
        return ' '.join(f'if items entity @s {SLOTS[s][1]} {holds(i)}' for i, s, _n in SETS[k][2])
    for k in SETS:
        second.append(f'execute as @a[gamemode=!spectator] {full(k)} at @s run function bm:p216/set/{k}')
    fn('p216/set/hunter', ['effect give @s minecraft:fire_resistance 3 0 true', 'effect give @s minecraft:night_vision 15 0 true',
                           'effect give @s minecraft:jump_boost 3 1 true', 'effect give @s minecraft:speed 3 0 true', 'tag @s add bm.arcset_hunter'])
    fn('p216/set/bomber', ['effect give @s minecraft:strength 3 0 true', 'tag @s add bm.arcset_bomber'])
    fn('p216/set/plumber', ['effect give @s minecraft:jump_boost 3 1 true', 'tag @s add bm.arcset_plumber'])
    fn('p216/set/vhunter', ['tag @s add bm.arcset_vhunter', 'execute if score #tod bm.bm matches 13000..22999 unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true'])
    second.insert(0, 'tag @a remove bm.arcset_hunter')
    second.insert(0, 'tag @a remove bm.arcset_bomber')
    second.insert(0, 'tag @a remove bm.arcset_plumber')
    second.insert(0, 'tag @a remove bm.arcset_vhunter')
    # THE STOMP: falling onto a monster (each fast tick, the plumber's)
    # (each tick, so a landing isn't missed. Falling: moving down fast, or the server's fall distance - a player's Motion isn't kept
    #  server-side - remembered for 3 ticks, because on the very tick you land on the monster's head you've stopped; the monster: a
    #  hitbox in the block and a half under your feet. One stomp a fall - again once you've stopped falling a moment: bounce off one
    #  monster onto the next, a chain)
    G.wjson('bm/predicate/p216/falling.json', {'condition': 'minecraft:any_of', 'terms': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'movement': {'vertical_speed': {'max': -4.0}}}},
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'movement': {'fall_distance': {'min': 1.0}}}}]})
    tick.append('execute as @a[tag=bm.arcset_plumber,gamemode=!spectator] at @s run function bm:p216/stomp_tick')
    UNDER = f'@e[{FOE},dx=0.8,dy=1.5,dz=0.8,tag=!bm.arcsmp]'              # (a monster just stomped can't be again for 0.75 s)
    tick.append('execute as @e[tag=bm.arcsmp] run function bm:p216/smp_tick')
    fn('p216/smp_tick', ['scoreboard players remove @s bm.arcfl 1', 'execute unless score @s bm.arcfl matches 1.. run tag @s remove bm.arcsmp'])
    fn('p216/stomp_tick', ['execute if predicate bm:p216/falling run scoreboard players set @s bm.arcfl 4',
                           'execute if score @s bm.arcfl matches 1.. unless entity @s[tag=bm.arcstd] positioned ~-0.4 ~-1.6 ~-0.4 if entity ' + UNDER + ' positioned ~0.4 ~1.6 ~0.4 run function bm:p216/stomp',
                           'execute if score @s bm.arcfl matches 1.. run scoreboard players remove @s bm.arcfl 1',
                           'execute unless score @s bm.arcfl matches 1.. run tag @s remove bm.arcstd'])
    fn('p216/stomp', ['tag @s add bm.arcme', 'tag @s add bm.arcstd',
                      f'execute positioned ~-0.4 ~-1.6 ~-0.4 as {UNDER} at @s run function bm:p216/stomped',
                      'tag @s remove bm.arcme',
                      'summon minecraft:wind_charge ~ ~-0.2 ~ {Motion:[0.0d,-2.0d,0.0d]}',          # (the bounce: a gust under your feet)
                      'playsound minecraft:entity.slime.jump player @a[distance=..16] ~ ~ ~ 1 1.6'])
    fn('p216/stomped', ['scoreboard players set @s bm.arcfl 15', 'tag @s add bm.arcsmp', 'damage @s 14 bm:dread_proc by @a[tag=bm.arcme,limit=1]', 'particle minecraft:poof ~ ~0.6 ~ 0.4 0.1 0.4 0.05 12',
                        'particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.2 10'])

    # ---------------------------------------------------------------- every blow struck: the sets', the whip's and the chips' procs
    G.wjson('bm/advancement/p216/hit.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity'}}, 'rewards': {'function': 'bm:p216/hit'}})
    vic = '@e[type=!minecraft:player,distance=..9,nbt={HurtTime:10s},sort=nearest,limit=1]'
    main = lambda k: f'items entity @s weapon.mainhand *[minecraft:custom_data~{{{k}:1b}}]'
    # (a blow of its own - the procs' damage, the stomp's, the star's - is dealt "by" you, and would land here again: not twice)
    fn('p216/hit', ['advancement revoke @s only bm:p216/hit', 'execute if entity @s[tag=bm.arcme] run return 0', 'tag @s add bm.arcme', f'execute as {vic} run tag @s add bm.arcv',
                    'execute unless entity @e[tag=bm.arcv] run return run tag @s remove bm.arcme',
                    'execute if entity @s[tag=bm.arcset_bomber] unless score @s bm.arcs matches 1.. run function bm:p216/p/buster',
                    'execute if entity @s[tag=bm.arcset_vhunter] as @e[tag=bm.arcv,type=#minecraft:undead] at @s run function bm:p216/p/holy',
                    f'execute if items entity @s weapon.mainhand {holds("vampire_killer")} as @e[tag=bm.arcv,type=#minecraft:undead] at @s run function bm:p216/p/holy',
                    f'execute if {main("bm_chip_glitch")} if predicate bm:p216/fifth as @e[tag=bm.arcv] at @s run function bm:p216/p/glitch',
                    'tag @e[tag=bm.arcv] remove bm.arcv', 'tag @s remove bm.arcme'])
    G.wjson('bm/predicate/p216/fifth.json', {'condition': 'minecraft:random_chance', 'chance': 0.2})
    G.wjson('bm/predicate/p216/quarter.json', {'condition': 'minecraft:random_chance', 'chance': 0.25})
    ME = '@a[tag=bm.arcme,limit=1]'
    fn('p216/p/holy', [f'damage @s 8 bm:dread_proc by {ME}', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.5 0.3 0.05 10',
                       'playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 1 1.4'])
    fn('p216/p/glitch', [f'damage @s 6 bm:dread_proc by {ME}', 'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.3 20',
                         'particle minecraft:dust{color:[1.0,0.3,0.85],scale:1.4} ~ ~1 ~ 0.4 0.6 0.4 0 16',
                         'playsound minecraft:block.note_block.bit player @a[distance=..16] ~ ~ ~ 1 0.5',
                         'execute store result score #gr bm.rng run random value 0..3',
                         'execute if score #gr bm.rng matches 0 if block ~3 ~ ~ #bm:grap_pass run return run tp @s ~3 ~ ~',
                         'execute if score #gr bm.rng matches 1 if block ~-3 ~ ~ #bm:grap_pass run return run tp @s ~-3 ~ ~',
                         'execute if score #gr bm.rng matches 2 if block ~ ~ ~3 #bm:grap_pass run return run tp @s ~ ~ ~3',
                         'execute if block ~ ~ ~-3 #bm:grap_pass run tp @s ~ ~ ~-3'])
    # the shots (phase212's homing flight)
    buster = P212.projectile(G, 'arc_buster', 'bm:arc_pj_pellet', 7, '@a', fxname='px_boom', scale=0.5)
    fire = P212.projectile(G, 'arc_fire', 'bm:arc_pj_fire', 8, '@a', on_hit=['data merge entity @s {Fire:100s}'], fxname='px_fireball', scale=0.6,
                           trail=['particle minecraft:flame ~ ~ ~ 0.05 0.05 0.05 0.01 1'])
    beam = P212.projectile(G, 'arc_beam', 'bm:arc_pj_beam', 10, '@a', fxname='px_beam', scale=0.8, trail=['particle minecraft:end_rod ~ ~ ~ 0.02 0.02 0.02 0 1'])
    fn('p216/p/buster', ['scoreboard players set @s bm.arcs 15', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                         'execute anchored eyes positioned ^ ^-0.2 ^0.6 run function bm:p216/p/buster_go',
                         'playsound minecraft:block.note_block.bit player @a[distance=..16] ~ ~ ~ 0.8 2'])
    fn('p216/p/buster_go', buster)
    fast.append('scoreboard players remove @a[scores={bm.arcs=1..}] bm.arcs 2')
    # the weapons' right-clicks
    fn('p216/w/buster', ['execute if score @s bm.arcs matches 1.. run return 0', 'scoreboard players set @s bm.arcs 8',
                         'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                         'execute anchored eyes positioned ^ ^-0.2 ^0.6 run function bm:p216/p/buster_go',
                         'playsound minecraft:block.note_block.bit player @a[distance=..16] ~ ~ ~ 0.9 2'])
    fn('p216/w/fire', ['execute if score @s bm.arcs matches 1.. run return 0', 'scoreboard players set @s bm.arcs 14',
                       'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                       'execute anchored eyes positioned ^ ^-0.2 ^0.6 run function bm:p216/w/fire_go',
                       'playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 0.8 1.6'])
    fn('p216/w/fire_go', fire)
    fn('p216/w/beam', ['execute if score @s bm.arcs matches 1.. run return 0',
                       'execute store result score #hp bm.rng run data get entity @s Health', 'execute store result score #mh bm.rng run attribute @s minecraft:max_health get',
                       'execute if score #hp bm.rng < #mh bm.rng run return run ' + say('The beam only flies at full health.', '#7ad0ff'),
                       'scoreboard players set @s bm.arcs 16', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                       'execute anchored eyes positioned ^ ^-0.2 ^0.8 run function bm:p216/w/beam_go',
                       'playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 1.6'])
    fn('p216/w/beam_go', beam)

    # ---------------------------------------------------------------- the chips: onto the weapon in your off hand
    WEAPON = '#bm:p216_weapons'
    G.wjson('bm/tags/item/p216_weapons.json', {'values': ['#minecraft:swords', '#minecraft:axes', 'minecraft:mace', 'minecraft:trident', 'minecraft:totem_of_undying']})
    arc_weapon = ' '.join(f'unless items entity @s weapon.offhand {holds(i)}' for i in ('pixel_blade', 'vampire_killer', 'arm_buster', 'fire_flower'))
    for k, (nm, c, l) in CHIPS.items():
        flag = f'bm_chip_{k}'
        comps = {'minecraft:custom_data': {flag: B(1)}}
        mod = [{'function': 'minecraft:set_custom_data', 'tag': snbt({flag: B(1)})},
               {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [T(f'◆ {nm}', c)]}]
        if k == 'genie':
            mod.append({'function': 'minecraft:set_attributes', 'replace': False, 'modifiers': [
                {'attribute': 'minecraft:attack_damage', 'id': 'bm:chip_genie', 'amount': 4, 'operation': 'add_value', 'slot': 'mainhand'}]})
        if k == 'turbo':
            mod.append({'function': 'minecraft:set_attributes', 'replace': False, 'modifiers': [
                {'attribute': 'minecraft:attack_speed', 'id': 'bm:chip_turbo', 'amount': 0.8, 'operation': 'add_value', 'slot': 'mainhand'}]})
        G.wjson(f'bm/item_modifier/p216/chip_{k}.json', mod)
        fn(f'p216/chip/{k}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                              f'execute unless items entity @s weapon.offhand {WEAPON} run return run ' + say(f'Put the weapon in your off hand first (a sword, axe, mace, trident or arcade weapon).', c),
                              f'execute if items entity @s weapon.offhand minecraft:totem_of_undying {arc_weapon} run return run ' + say('That isn\'t a weapon.', c),
                              f'execute if items entity @s weapon.offhand *[minecraft:custom_data~{{{flag}:1b}}] run return run ' + say(f'That weapon has the {nm} already.', c),
                              f'item modify entity @s weapon.offhand bm:p216/chip_{k}', f'clear @s {holds("chip_" + k)} 1',
                              'playsound minecraft:block.note_block.bit player @s ~ ~ ~ 1 1.2', 'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.4 1.8',
                              'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.2 20',
                              tellraw('@s', P + [T(nm, c, bold=True), T(' is in the weapon for good.', 'gray')])])
    # MISSINGNO.: a kill with it, one in four - the sixth hotbar slot's stack grows by one
    G.wjson('bm/advancement/p216/kill.json', {'criteria': {'kill': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'player': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'mainhand': {'predicates': {'minecraft:custom_data': '{bm_chip_missingno:1b}'}}}}}]}}},
        'rewards': {'function': 'bm:p216/kill'}})
    fn('p216/kill', ['advancement revoke @s only bm:p216/kill', 'execute unless predicate bm:p216/quarter run return 0',
                     'execute unless items entity @s hotbar.5 * run return 0',
                     'item modify entity @s hotbar.5 {function:"minecraft:set_count",count:1,add:true}',
                     'particle minecraft:dust{color:[0.7,0.6,1.0],scale:1.4} ~ ~1 ~ 0.4 0.6 0.4 0 20', 'playsound minecraft:block.note_block.bit player @s ~ ~ ~ 1 0.6',
                     title('@s', 'actionbar', [T('MISSINGNO. ', '#b0a0ff', bold=True), T('- your sixth slot glitches up by one.', 'gray')])])

    # ---------------------------------------------------------------- the props: set down, used, picked up
    for k, (nm, c, l, h) in PROPS.items():
        fn(f'p216/place/{k}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                               'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                               f'execute anchored eyes positioned ^ ^ ^ run function bm:p216/ray/{k}', 'tag @s remove bm.placer',
                               'execute if score #placed bm.rng matches 0 run ' + say('Look at the top of a block within 5 blocks to set it down.')])
        fn(f'p216/ray/{k}', ['execute unless block ~ ~ ~ #minecraft:replaceable align xyz positioned ~0.5 ~1 ~0.5 if block ~ ~ ~ #minecraft:replaceable '
                             f'rotated as @a[tag=bm.placer,limit=1] rotated ~180 0 run return run function bm:p216/put/{k}',
                             'scoreboard players remove #ray bm.rng 1', f'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p216/ray/{k}'])
        box = {'Tags': ['bm.arcpbox', f'bm.arcpb_{k}', 'bm.arcnew'], 'width': F(0.9), 'height': F(max(0.9, h)), 'response': B(1)}
        fn(f'p216/put/{k}', [f'summon minecraft:item_display ~ ~ ~ {snbt(_prop_nbt(k, ["bm.arcprop", "bm.arcnew"]))}', f'summon minecraft:interaction ~ ~ ~ {snbt(box)}',
                             'tp @e[type=minecraft:item_display,tag=bm.arcnew,distance=..1] ~ ~ ~ ~ 0',
                             'scoreboard players operation @e[tag=bm.arcnew,distance=..1] bm.pid = @a[tag=bm.placer,limit=1] bm.pid'] +
           (['function bm:p216/pipe/place'] if k == 'warp_pipe' else []) +
           ['tag @e[tag=bm.arcnew,distance=..1] remove bm.arcnew', 'scoreboard players set #placed bm.rng 1',
            f'clear @a[tag=bm.placer,limit=1] {holds(k)} 1', 'playsound minecraft:block.note_block.bit block @a[distance=..16] ~ ~ ~ 1 1.4'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.arcpbox] if data entity @s interaction at @s run function bm:p216/click',
             'execute as @e[type=minecraft:interaction,tag=bm.arcpbox] if data entity @s attack at @s run function bm:p216/punch']
    fn('p216/click', ['tag @s add bm.arcthis', 'execute on target run tag @s add bm.arcu'] +
       [f'execute if entity @s[tag=bm.arcpb_{k}] as @a[tag=bm.arcu,limit=1] at @s run function bm:p216/use_{k}' for k in PROPS] +
       ['tag @a remove bm.arcu', 'tag @s remove bm.arcthis', 'data remove entity @s interaction'])
    fn('p216/punch', ['execute on attacker if predicate bm:p20/sneaking run tag @s add bm.arcu',
                      'execute if entity @a[tag=bm.arcu] run function bm:p216/pickup', 'tag @a remove bm.arcu', 'data remove entity @s attack'])
    fn('p216/pickup', [f'execute if entity @s[tag=bm.arcpb_{k}] run loot spawn ~ ~0.5 ~ loot bm:items/{k}' for k in PROPS] +
       ['kill @e[type=minecraft:item_display,tag=bm.arcprop,distance=..0.3]', 'playsound minecraft:entity.item.pickup block @a[distance=..16] ~ ~ ~ 1 1', 'kill @s'])
    THIS = '@e[type=minecraft:interaction,tag=bm.arcthis,limit=1]'
    # ? block: a Token, once a day each
    fn('p216/use_q_block', [f'execute if score {THIS} bm.arcq = #day bm.bm run return run function bm:p216/q_empty',
                            f'scoreboard players operation {THIS} bm.arcq = #day bm.bm', f'execute at {THIS} run loot spawn ~ ~1.2 ~ loot bm:items/token',
                            f'execute at {THIS} run particle minecraft:wax_on ~ ~1 ~ 0.3 0.3 0.3 0 12', 'playsound minecraft:block.note_block.bell player @a[distance=..16] ~ ~ ~ 1 2',
                            'playsound minecraft:entity.experience_orb.pickup player @a[distance=..16] ~ ~ ~ 1 1.6'])
    fn('p216/q_empty', ['playsound minecraft:block.wood.hit player @s ~ ~ ~ 1 0.6', say('Empty. (It fills again tomorrow.)', GOLD)])
    # warp pipe: the other one of its owner's pair
    fn('p216/pipe/place', ['scoreboard players operation #pp bm.rng = @a[tag=bm.placer,limit=1] bm.arcpn', 'scoreboard players add #pp bm.rng 1',
                           'scoreboard players operation #pp bm.rng %= #2 bm.rng', 'scoreboard players operation @a[tag=bm.placer,limit=1] bm.arcpn = #pp bm.rng',
                           'scoreboard players operation @e[tag=bm.arcnew,distance=..1] bm.arcp = #pp bm.rng',
                           'execute store result storage bm:tmp arc.pid int 1 run scoreboard players get @a[tag=bm.placer,limit=1] bm.pid',
                           'execute store result storage bm:tmp arc.n int 1 run scoreboard players get #pp bm.rng',
                           'data modify storage bm:tmp arc.pos set from entity @e[type=minecraft:interaction,tag=bm.arcnew,distance=..1,limit=1] Pos',
                           'data modify storage bm:tmp arc.dim set from entity @a[tag=bm.placer,limit=1] Dimension',
                           'function bm:p216/pipe/save with storage bm:tmp arc'])
    fn('p216/pipe/save', ['$data modify storage bm:arc pipes.p$(pid)n$(n) set value {}',
                          '$data modify storage bm:arc pipes.p$(pid)n$(n).x set from storage bm:tmp arc.pos[0]',
                          '$data modify storage bm:arc pipes.p$(pid)n$(n).y set from storage bm:tmp arc.pos[1]',
                          '$data modify storage bm:arc pipes.p$(pid)n$(n).z set from storage bm:tmp arc.pos[2]',
                          '$data modify storage bm:arc pipes.p$(pid)n$(n).d set from storage bm:tmp arc.dim'])
    fn('p216/use_warp_pipe', [f'execute store result storage bm:tmp arc.pid int 1 run scoreboard players get {THIS} bm.pid',
                              f'scoreboard players operation #pp bm.rng = {THIS} bm.arcp', 'scoreboard players add #pp bm.rng 1', 'scoreboard players operation #pp bm.rng %= #2 bm.rng',
                              'execute store result storage bm:tmp arc.n int 1 run scoreboard players get #pp bm.rng',
                              'function bm:p216/pipe/go with storage bm:tmp arc'])
    fn('p216/pipe/go', ['$execute unless data storage bm:arc pipes.p$(pid)n$(n) run return run function bm:p216/pipe/alone',
                        '$data modify storage bm:tmp arc.to set from storage bm:arc pipes.p$(pid)n$(n)',
                        'playsound minecraft:block.note_block.bit player @a[distance=..16] ~ ~ ~ 1 0.6',
                        'function bm:p216/pipe/tp with storage bm:tmp arc.to'])
    fn('p216/pipe/tp', ['$execute in $(d) run tp @s $(x) $(y) $(z)', 'execute at @s run playsound minecraft:block.note_block.bit player @a[distance=..16] ~ ~ ~ 1 1.2',
                        'execute at @s run particle minecraft:happy_villager ~ ~1 ~ 0.4 0.6 0.4 0 12'])
    fn('p216/pipe/alone', [say('This pipe leads nowhere yet - set its pair down somewhere.', '#3ac83a')])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #2 bm.rng 2']
    # arcade cabinet: a game
    fn('p216/use_arcade_cabinet', ['playsound minecraft:block.note_block.bit player @a[distance=..16] ~ ~ ~ 1 1', 'playsound minecraft:block.note_block.bit player @a[distance=..16] ~ ~ ~ 1 1.33',
                                   'playsound minecraft:block.note_block.bit player @a[distance=..16] ~ ~ ~ 1 1.6', 'playsound minecraft:block.note_block.bit player @a[distance=..16] ~ ~ ~ 1 2',
                                   'execute store result score #sc bm.rng run random value 1000..99999', 'effect give @s minecraft:luck 60 0 true',
                                   title('@s', 'actionbar', [T('GAME OVER - HIGH SCORE: ', COL, bold=True), {'score': {'name': '#sc', 'objective': 'bm.rng'}, 'color': 'white'},
                                                             T('  (Luck for a minute)', 'gray')])])
    fn('p216/use_blade_stone', ['playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 1 1.2', say('It won\'t budge. Not yet.', '#7ad0ff'),
                                f'execute at {THIS} run particle minecraft:end_rod ~ ~1.2 ~ 0.2 0.4 0.2 0.02 10'])
    fn('p216/use_power_triangles', ['playsound minecraft:block.amethyst_block.chime player @a[distance=..16] ~ ~ ~ 1 0.8', say('Power. Wisdom. Courage.', GOLD),
                                    f'execute at {THIS} run particle minecraft:wax_on ~ ~1 ~ 0.4 0.4 0.4 0 16'])
    # save point: spawn here, healed - once a minute
    second.append('scoreboard players remove @a[scores={bm.arcsv=1..}] bm.arcsv 1')
    fn('p216/use_save_point', ['execute if score @s bm.arcsv matches 1.. run return run ' + say('The crystal is still recharging.', '#7ae0ff'),
                               'scoreboard players set @s bm.arcsv 60', 'execute at @s run spawnpoint @s ~ ~ ~', 'effect give @s minecraft:instant_health 1 3 true',
                               'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 1 1.6', say('Progress saved. (Your spawn is here; you\'re healed.)', '#7ae0ff')])

    # ---------------------------------------------------------------- the practical things
    G.wjson('bm/advancement/p216/heart.json', {'criteria': {'eat': {'trigger': 'minecraft:consume_item', 'conditions': {'item': {'items': 'minecraft:totem_of_undying', 'predicates': {'minecraft:custom_data': '{bm:"heart_container"}'}}}}},
                                               'rewards': {'function': 'bm:p216/heart'}})
    fn('p216/heart', ['advancement revoke @s only bm:p216/heart', 'execute unless score @s bm.archc matches 0.. run scoreboard players set @s bm.archc 0',
                      'execute if score @s bm.archc matches 3.. run return run function bm:p216/heart_full',
                      'scoreboard players add @s bm.archc 1'] +
       [f'execute if score @s bm.archc matches {n} run attribute @s minecraft:max_health modifier add bm:arc_heart_{n} 2 add_value' for n in (1, 2, 3)] +
       ['effect give @s minecraft:instant_health 1 0 true', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1.6',
        tellraw('@s', P + [T('A Heart Container! ', '#ff4a6a', bold=True), T('+1 heart for good.', 'gray')])])
    fn('p216/heart_full', [give('heart_container'), say('Three hearts is all a body holds. (It\'s given back.)', '#ff4a6a')])
    fn('p216/use/star', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2', f'clear @s {holds("super_star")} 1',
                         'effect give @s minecraft:resistance 10 4 true', 'effect give @s minecraft:speed 10 1 true', 'scoreboard players set @s bm.arcg 200',
                         'playsound minecraft:block.note_block.bit player @a[distance=..16] ~ ~ ~ 1 2', say('STAR POWER!', GOLD)])
    tick.append('execute as @a[scores={bm.arcg=1..}] at @s run function bm:p216/star')
    fn('p216/star', ['scoreboard players remove @s bm.arcg 1', 'particle minecraft:dust{color:[1.0,0.9,0.2],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 2',
                     'particle minecraft:dust{color:[1.0,0.3,0.8],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1', 'particle minecraft:dust{color:[0.3,0.8,1.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 1',
                     'tag @s add bm.arcme', f'execute as @e[{FOE},distance=..1.6] run damage @s 8 bm:dread_proc by @a[tag=bm.arcme,limit=1]', 'tag @s remove bm.arcme'])
    fn('p216/use/grow', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2', f'clear @s {holds("power_mushroom")} 1',
                         'attribute @s minecraft:scale modifier remove bm:arc_big', 'attribute @s minecraft:scale modifier add bm:arc_big 0.3 add_multiplied_base',
                         'effect give @s minecraft:strength 60 1 true', 'scoreboard players set @s bm.arcd 60',
                         'playsound minecraft:entity.player.levelup player @a[distance=..16] ~ ~ ~ 1 2', say('Power up!', '#ff4a4a')])
    second.append('execute as @a[scores={bm.arcd=1..}] at @s run function bm:p216/grow_tick')
    fn('p216/grow_tick', ['scoreboard players remove @s bm.arcd 1', 'execute if score @s bm.arcd matches 0 run attribute @s minecraft:scale modifier remove bm:arc_big',
                          'execute if score @s bm.arcd matches 0 at @s run playsound minecraft:block.note_block.bit player @a[distance=..16] ~ ~ ~ 1 0.6'])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/arcade', 'yellow'), T('  one of everything the Arcade sells', 'gray')]))
    fn('admin/arcade', [give(i) for i, _n, _p in RAT_STOCK + VIL_STOCK])


def _prop_nbt(k, tags):
    return {'Tags': tags + [f'bm.arcp_{k}'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:arc_prop_{k}'}},
            'item_display': 'fixed', 'view_range': F(1.5),
            'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                               'translation': [F(0), F(0.5), F(0)], 'scale': [F(1)] * 3}}            # (the model's floor on the block)

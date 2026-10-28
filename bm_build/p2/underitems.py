"""2.98: THE UNDERCROWN's items (registered on import - p2/undercfg imports this, so the builder's vaults can name their keys).
What they do is phase237's (the dungeon's), phase238's (the Sovereign's spoils) and phase239's (the Eye)."""
from items import item, gear, attr, ench, T, TOTEM, consumable, armor_attrs, weapon_attrs
from useitem import hold, HOLD
import undercrown_lore as L

COL, RED, HOLY = L.SOV_COL, '#ff5a64', L.HOLY
N = lambda k: L.ITEMS[k][0]
LO = lambda k: list(L.ITEMS[k][1])
ANGEL = {'bm_angel': 1}                      # (holy: the Lightbringer loves it, a Golden Cross's blessing counts it - phase182)

# ---- the way in
item('usummons', 'minecraft:compass', N('summons'), COL, LO('summons')[:3] + [(LO('summons')[3], 'dark_red'), ('Hard mode.', 'dark_gray')],
     glint=True, stack=1, cat='map')
for k, sid in (('snow', 'ushard_snow'), ('witch', 'ushard_witch'), ('shark', 'ushard_shark')):
    item(sid, TOTEM, N(f'shard_{k}'), COL, LO(f'shard_{k}') + [('Drop it (Q) on its socket at the Throne Gate.', 'gray')],
         model=f'bm:{sid}', glint=True, stack=1, cat='p2prop')
item('ublack_seal', TOTEM, N('black_seal'), '#8a7a8a', LO('black_seal'), model='bm:ublack_seal', stack=6, cat='p2prop')
item('ukey', 'minecraft:trial_key', 'Undercrown Key', COL, ['Opens a vault in the Undercrown.', ('Each Echo, and the Throne Gate, gives one.', 'dark_gray')],
     model='bm:ukey', stack=16, cat='p2vkey')
item('ukey_victor', 'minecraft:ominous_trial_key', "Victor's Key: the Dread Sovereign", COL, ['Opens the victor\'s vault in the Undercrown.', ('Earned by its fall.', 'dark_gray')],
     model='bm:ukey_victor', glint=True, stack=16, cat='p2vkey')

# ---- the reckoning
item('dread_ember', TOTEM, N('ember'), COL, LO('ember')[:1] + [(LO('ember')[1], 'blue'), (LO('ember')[2], 'blue'), ('From the Dread Sovereign.', 'dark_gray')],
     model='bm:dread_ember', glint=True, stack=1, cat='magic', bold=True,
     comps={'minecraft:consumable': consumable(2.0, 'bow', 'minecraft:block.fire.ambient', False)})

# ---- its spoils (phase238)
gear('sov_edge', 'netherite_sword', N('edge'), COL, LO('edge') + [('A full swing cuts a void arc: everything in front of you.', 'blue'),
                                                                   ('+4 Attack Damage, heals you for a part of the arc.', 'blue')],
     ench(sharpness=8, smite=6, sweeping_edge=5, looting=4, unbreaking=10, mending=1), 3,
     attrs=weapon_attrs('netherite_sword', 4), model='bm:sov_edge', bold=True, custom_extra={'bm_fx': 'sov_edge'})
gear('black_crown', 'netherite_helmet', N('crown'), COL, LO('crown') + [('+6 Max Health, +3 Toughness, sees in the dark.', 'blue'),
                                                                        ('Dread near you are weakened.', 'blue')],
     ench(protection=8, unbreaking=10, mending=1), 3,
     attrs=armor_attrs('netherite', 'helmet', [attr('max_health', 6, 'head')], bonus_tough=3), model='bm:black_crown', bold=True,
     custom_extra={'bm_fx': 'black_crown'}, extra={'minecraft:equippable': {'slot': 'head', 'equip_sound': 'minecraft:item.armor.equip_netherite'}})
item('sov_heart', TOTEM, N('heart'), COL, LO('heart') + [('Carried: once a day, a blow that would kill you', 'blue'), ('leaves you standing instead.', 'blue')],
     model='bm:sov_heart', glint=True, stack=1, cat='magic', bold=True)

# ---- the hidden rooms' relics (once a player, ever)
item('dawnshard', TOTEM, N('dawnshard'), HOLY, LO('dawnshard') + [('Held: the great eye\'s beam can\'t touch you.', 'blue'), ('Holy.', '#fff4d0')],
     model='bm:dawnshard', glint=True, stack=1, cat='magic', custom_extra=ANGEL)
item('unwriting', TOTEM, N('unwriting'), '#c8c0b0', LO('unwriting')[:1] + [(LO('unwriting')[1], 'blue'), ('(once a minute)', 'gray')],
     model='bm:unwriting', stack=1, cat='magic', comps={'minecraft:consumable': consumable(0.6, 'none', 'minecraft:item.book.page_turn', False)})
gear('chainwhip', 'netherite_sword', N('chainwhip'), '#9a8c94', LO('chainwhip') + [('+2 Reach. A hit drags the foe to you.', 'blue')],
     ench(sharpness=6, unbreaking=10, mending=1), 3,
     attrs=weapon_attrs('netherite_sword', 1, [attr('entity_interaction_range', 2, 'mainhand')]), model='bm:chainwhip', custom_extra={'bm_fx': 'chainwhip'})
item('nine_lives', TOTEM, N('nine_lives'), '#d8d8e8', LO('nine_lives')[:1] + [(LO('nine_lives')[1], 'blue')], model='bm:nine_lives', stack=1, cat='magic')
item('ulantern_wick', TOTEM, "The Lantern's Wick", '#ffb347', ['A wick that never burns down, from the Lantern Crawl.', ('In your off hand: you see in the dark,', 'blue'),
                                                            ('and monsters within 16 glow.', 'blue')], model='bm:ulantern_wick', stack=1, cat='magic')
gear('unbound_helm', 'netherite_helmet', "Unbound Knight's Helm", '#8a96a8', ['The knights who were set to guard the chains.', 'They answered to Wilfrey, once.',
                                                                             ('+2 Armor, +1 Toughness; Thorns.', 'blue')],
     ench(protection=6, thorns=4, unbreaking=10, mending=1), 3, attrs=armor_attrs('netherite', 'helmet', bonus_armor=2, bonus_tough=1), model='bm:unbound_helm',
     extra={'minecraft:equippable': {'slot': 'head', 'equip_sound': 'minecraft:item.armor.equip_netherite'}})
RELICS = ('dawnshard', 'ulantern_wick', 'unwriting', 'chainwhip', 'nine_lives', 'unbound_helm')

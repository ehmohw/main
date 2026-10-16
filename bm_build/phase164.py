"""2.80e: APOPHISS'S UNBOUND CROWN - his True Crown forged on the ground with a Wraithfire Heart and the Hollow King's Deathmask.

Toss the three down together (a ground forge, phase160). The crown that comes out keeps everything the True Crown does - its
stats, its Fangs, its Wrath, its night power, its place on a block - and adds:
- THE WHOLE REGALIA: worn alone it counts as the Hollow King's full Regalia (the mask is melted into it), so the set wakes with
  the night, the moons, a Blood Moon, an Invasion or at home, and its Wither Nova is yours. (The waking recolours only the
  Regalia's own trimmed pieces - whatever else you wear is left as it is.)
- THE UNBOUND (his second form): sneak in mid-air and a beat of violet wings lifts you, then you glide down. Two beats a leap;
  they come back when you land.
- WRAITHFIRE: soul fire burns monsters within 5 blocks of you, and your Serpent's Fangs sear what stands before you - magic
  fire, so fire immunity doesn't help them.
- VOID ORBS: when the Wrath wakes, three orbs of the dark ring you for five seconds, gnawing and withering monsters in them.
Both crowns carry bm_crown:1b, and every True Crown check (worn, held, set down) answers to either.
"""
import copy
import random
import p2.regalia  # noqa: F401  (the Deathmask is registered on import)
import phase127  # noqa: F401  (the Wraithfire Heart)
import phase131  # noqa: F401  (the True Crown)
import phase160 as P160
from items import item, T, TOTEM, ITEMS
from useitem import HOLD
from nbt import B

COL = '#7ad8ff'
VIO = '#b07aff'
holds = '*[minecraft:custom_data~{bm:"%s"}]'
TRUE, UNB = holds % 'apo_true_crown', holds % 'apo_unbound_crown'
ANY = '*[minecraft:custom_data~{bm_crown:1b}]'

_t = ITEMS['apo_true_crown']
_t['custom']['bm_crown'] = B(1)
_t['comps']['minecraft:custom_data']['bm_crown'] = B(1)
item('apo_unbound_crown', TOTEM, "Apophiss's Unbound Crown", COL,
     ["His crown, unbound: soul fire in the emerald,", "the Hollow King's mask melted into its band.",
      ('Everything the True Crown gives, worn -', 'blue'), ('its strength, its Fangs, its Wrath - and:', 'blue'),
      ('It is the whole Regalia: worn alone, the', 'dark_purple'), ('set wakes, and its Wither Nova is yours.', 'dark_purple'),
      ('Sneak in mid-air: his violet wings beat once', 'light_purple'), ('and lift you, then you glide. Two a leap.', 'light_purple'),
      ('Soul fire burns monsters near you, and your', 'aqua'), ('Fangs sear them - fire immunity or not.', 'aqua'),
      ('With the Wrath: three Void Orbs of the dark.', 'dark_purple'),
      ('Use: wear it. Sneak + use on a block: set it there.', 'gray'),
      ("Forged from Apophiss's True Crown.", 'dark_gray')],
     model='bm:apo_unbound_crown', stack=1, cat='relic', glint=True, tier=3, custom_extra={'bm_set': 'conqueror', 'bm_crown': B(1)},
     comps={k: copy.deepcopy(_t['comps'][k]) for k in ('minecraft:consumable', 'minecraft:use_effects', 'minecraft:equippable',
                                                       'minecraft:attribute_modifiers', 'minecraft:enchantments')})
HOLD['apo_unbound_crown'] = 'bm:p131/crown/use'

# the pieces say where they lead
for _i, _line, _col in (('apo_true_crown', "On the ground with a Wraithfire Heart and the Hollow King's Deathmask, it is unbound.", COL),
                        ('wraithfire_heart', "On the ground with Apophiss's True Crown and the Hollow King's Deathmask, they fuse.", COL),
                        ('conq_helmet', "On the ground with Apophiss's True Crown and a Wraithfire Heart, they fuse.", COL)):
    ITEMS[_i]['comps']['minecraft:lore'].insert(-1, T(_line, _col))

# the forge (phase160 builds it), and the Newcomers' Book's page
P160.RECIPES.append(('unbound', "Apophiss's Unbound Crown", COL, ['0.35,0.85,1.0', '0.62,0.32,0.95', '0.25,0.95,0.45'],
                     (TRUE, 1), [(holds % 'wraithfire_heart', 1), (holds % 'conq_helmet', 1)], None, None))
P160.RESULT['unbound'] = 'apo_unbound_crown'
P160.P50.EXTRA_PAGES.append([T("Apophiss's Unbound Crown\n", '#2a7a9a', bold=True),
                             T("His True Crown, a Wraithfire Heart and the Hollow King's Deathmask.\n\n", 'black'),
                             T('It keeps all the True Crown is, is the whole Regalia on its own, and lends you his wings and his soul fire.', 'dark_gray')])


def generate(G):
    fn, title, wjson = G.fn, G.title, G.wjson
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    objs = ['bm.uwb dummy', 'bm.uwn dummy', 'bm.uvo dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]

    # ---- every True Crown check answers to both crowns (worn, held, set down)
    for name, lines in G.FUNCS.items():
        if name.startswith('p131/crown/') or name == 'p59/crown/jump':
            lines[:] = [l.replace(TRUE, ANY) for l in lines]
        else:
            lines[:] = [l.replace(TRUE, ANY) if 'function bm:p131/crown/' in l else l for l in lines]
    G.FUNCS['p131/crown/place'] = [l.replace("Apophiss's True Crown ", 'The crown ') for l in G.FUNCS['p131/crown/place']]
    wjson('bm/advancement/p164/crown_hit.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'player': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'head': {'predicates': {
            'minecraft:custom_data': '{bm:"apo_unbound_crown"}'}}}}}]}}}, 'rewards': {'function': 'bm:p164/crown_hit'}})
    fn('p164/crown_hit', ['advancement revoke @s only bm:p164/crown_hit', 'function bm:p131/crown/hit'])
    G.FUNCS['p131/crown/glow'].append(f'execute if items entity @s contents {UNB} run particle minecraft:soul_fire_flame ~ ~0.5 ~ 0.2 0.12 0.2 0.005 1')

    # ---- the whole Regalia, alone; and its waking recolours only the Regalia's own trimmed pieces
    G.FUNCS['p2/sets/has/conqueror'].insert(0, f'execute if items entity @s armor.head {UNB} run return 1')
    for name in [n for n in G.FUNCS if n.startswith('p2/rg/trim_')]:
        G.FUNCS[name] = [(f'execute if items entity @s {l.split()[4]} *[minecraft:trim] run ' + l) if l.startswith('item modify entity @s armor.') else l
                         for l in G.FUNCS[name]]

    # ---- THE UNBOUND: sneak in mid-air - a wingbeat lifts you, then you glide; two a leap, back when you land
    tick.append(f'execute as @a[gamemode=!spectator] if items entity @s armor.head {UNB} at @s run function bm:p164/w/tick')
    tick.append(f'execute as @a[tag=bm.uwsk] unless items entity @s armor.head {UNB} run tag @s remove bm.uwsk')
    fn('p164/w/tick', ['execute if score @s bm.uwb matches 1.. run function bm:p164/w/beating',
                       'execute unless predicate bm:p21/airborne run scoreboard players set @s bm.uwn 0',
                       'execute unless predicate bm:p20/sneaking run return run tag @s remove bm.uwsk',
                       'execute if entity @s[tag=bm.uwsk] run return 0',
                       'tag @s add bm.uwsk',                                                      # (a fresh press of sneak)
                       'execute unless predicate bm:p21/airborne run return 0',
                       'execute if predicate bm:p164/fall_flying run return 0',
                       'execute if score @s bm.uwn matches 2.. run return run ' + say('His wings need the ground again.'),
                       'function bm:p164/w/beat'])
    wjson('bm/predicate/p164/fall_flying.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                 'predicate': {'minecraft:flags': {'is_fall_flying': True}}})
    wing = lambda sx: [f'particle minecraft:dust{{color:[0.62,0.32,0.95],scale:1.3}} ^{sx * d:.2f} ^{1.3 + 0.35 * d - 0.12 * d * d:.2f} ^-0.35 0.05 0.12 0.05 0 2'
                       for d in (0.4, 0.8, 1.2, 1.6)] + [f'particle minecraft:soul_fire_flame ^{sx * 1.7:.2f} ^1.5 ^-0.35 0.05 0.1 0.05 0.01 1']
    fn('p164/w/beat', ['scoreboard players add @s bm.uwn 1', 'scoreboard players set @s bm.uwb 6',
                       'effect give @s minecraft:levitation 1 20 true', 'effect clear @s minecraft:slow_falling',
                       'playsound minecraft:entity.ender_dragon.flap player @a[distance=..24] ~ ~ ~ 0.8 1.3',
                       'playsound minecraft:entity.phantom.flap player @a[distance=..16] ~ ~ ~ 1 0.7',
                       'particle minecraft:squid_ink ~ ~0.6 ~ 0.4 0.1 0.4 0.05 8'] + wing(1) + wing(-1))
    fn('p164/w/beating', ['scoreboard players remove @s bm.uwb 1', 'execute if score @s bm.uwb matches 0 run function bm:p164/w/glide'] + wing(1)[:2] + wing(-1)[:2])
    fn('p164/w/glide', ['effect clear @s minecraft:levitation', 'effect give @s minecraft:slow_falling 3 0 true'])
    fast.append(f'execute as @a[scores={{bm.uwn=1..}}] if predicate bm:p21/airborne if items entity @s armor.head {UNB} at @s run function bm:p164/w/glide_fx')
    fn('p164/w/glide_fx', [l.replace('0 2', '0 1') for l in wing(1)[1:3] + wing(-1)[1:3]])

    # ---- WRAITHFIRE: soul fire on monsters near you (each second), and on whatever stands before your Fangs
    second.append(f'execute as @a[gamemode=!spectator] if items entity @s armor.head {UNB} at @s run function bm:p164/soul/aura')
    fn('p164/soul/aura', ['particle minecraft:soul_fire_flame ~ ~2.3 ~ 0.22 0.06 0.22 0.004 3',
                          'execute unless entity @e[type=#bm:hostile,tag=!bm.npc,distance=..5] run return 0', 'tag @s add bm.uwme',
                          'execute as @e[type=#bm:hostile,tag=!bm.npc,distance=..5] at @s run function bm:p164/soul/burn {d:2}', 'tag @s remove bm.uwme'])
    fn('p164/soul/burn', ['$damage @s $(d) minecraft:magic by @a[tag=bm.uwme,limit=1]',
                          'particle minecraft:soul_fire_flame ~ ~0.9 ~ 0.25 0.45 0.25 0.02 6', 'particle minecraft:soul ~ ~1 ~ 0.2 0.3 0.2 0.02 1'])
    G.FUNCS['p131/crown/jump'].append(f'execute if items entity @s armor.head {UNB} at @s rotated ~ 0 run function bm:p164/soul/fangs')
    fn('p164/soul/fangs', ['tag @s add bm.uwme',
                           'execute positioned ^ ^ ^4 as @e[type=#bm:hostile,tag=!bm.npc,distance=..4.5] at @s run function bm:p164/soul/burn {d:6}',
                           'tag @s remove bm.uwme'] +
       [f'particle minecraft:soul_fire_flame ^ ^0.3 ^{k} 0.6 0.1 0.2 0.01 4' for k in (1.5, 3, 4.5, 6)])

    # ---- VOID ORBS: when the Wrath wakes, three orbs of the dark ring you for five seconds
    G.FUNCS['p131/crown/wrath'].append(f'execute if items entity @s armor.head {UNB} at @s run function bm:p164/orb/burst')
    fn('p164/orb/burst', [f'execute rotated {a} 0 positioned ^ ^1 ^3 run summon minecraft:marker ~ ~ ~ {{Tags:["bm.uvo","bm.uvonew"]}}' for a in (0, 120, 240)] +
       ['scoreboard players set @e[type=minecraft:marker,tag=bm.uvonew,distance=..5] bm.uvo 20',
        'tag @e[type=minecraft:marker,tag=bm.uvonew,distance=..5] remove bm.uvonew',
        'playsound minecraft:entity.warden.sonic_charge player @a[distance=..24] ~ ~ ~ 0.8 1.4',
        title('@s', 'actionbar', [T('Void Orbs ', VIO, bold=True), T('drown the dark round you.', 'gray')])])
    fast.append('execute as @e[type=minecraft:marker,tag=bm.uvo] at @s run function bm:p164/orb/fast')
    fn('p164/orb/fast', ['scoreboard players remove @s bm.uvo 1', 'execute unless score @s bm.uvo matches 1.. run return run kill @s',
                         'particle minecraft:dust{color:[0.12,0.02,0.2],scale:2.2} ~ ~ ~ 0.5 0.5 0.5 0 10',
                         'particle minecraft:dust{color:[0.62,0.32,0.95],scale:1.0} ~ ~ ~ 0.6 0.6 0.6 0 4',
                         'particle minecraft:squid_ink ~ ~ ~ 0.4 0.4 0.4 0.01 2',
                         'execute as @e[type=#bm:hostile,tag=!bm.npc,distance=..2.5] run function bm:p164/orb/hit'])
    fn('p164/orb/hit', ['damage @s 1 minecraft:magic', 'effect give @s minecraft:wither 2 1', 'effect give @s minecraft:slowness 1 2'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:marker,tag=bm.uvo]']

    # ---- the advancement, and a kit for admins
    it = ITEMS['apo_unbound_crown']
    wjson('bm/advancement/story/forge_unbound.json', {'parent': 'bm:story/root',
          'criteria': {'u': {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': TOTEM, 'predicates': {
              'minecraft:custom_data': G.snbt({'bm': 'apo_unbound_crown'})}}]}}},
          'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': it['comps']['minecraft:item_model']}},
                      'title': T('Unbound', 'yellow'), 'description': T("Forge Apophiss's Unbound Crown: his True Crown, a Wraithfire Heart and the Hollow King's Deathmask", 'gray'),
                      'frame': 'challenge', 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    fn('admin/unbound_kit', [G.give('apo_true_crown'), G.give('wraithfire_heart'), G.give('conq_helmet')])

    G.FUNCS['tick'] += tick
    G.FUNCS['loop/fast'][-1:-1] = fast
    G.FUNCS['loop/second'][-1:-1] = second


# ===================================================================== resource pack: the crown, soul fire in the emerald, violet gems
def textures():
    from PIL import Image
    rnd = random.Random(164)
    hexc = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
    def noise(h, var):
        b = hexc(h); im = Image.new('RGBA', (16, 16))
        for y in range(16):
            for x in range(16):
                d = rnd.randint(-var, var)
                im.putpixel((x, y), tuple(max(0, min(255, c + d)) for c in b[:3]) + (255,))
        return im
    T_ = {'ap_soul': noise('#1fb8d8', 10), 'ap_soul_lt': noise('#8af0ff', 10), 'ap_violet': noise('#7a32c8', 10), 'ap_violet_lt': noise('#c08aff', 8)}
    for y in range(16):
        for x in range(16):
            if (x + y) % 5 == 0 or (x - y) % 5 == 0: T_['ap_soul'].putpixel((x, y), hexc('#0a5a78' if (x + y) % 2 else '#b0fbff'))
            if (x - y) % 4 == 0: T_['ap_violet'].putpixel((x, y), hexc('#d0a0ff'))
    return T_


def rp(R):
    import sys, json
    R.TEXTURE_MODS.append(sys.modules[__name__])
    def post(R2):
        m = json.load(open(R2.p('assets', 'bm', 'models', 'item', 'apophiss_crown.json')))
        swap = {'bm:block/ap_emerald': 'bm:block/ap_soul', 'bm:block/ap_emerald_lt': 'bm:block/ap_soul_lt',
                'bm:block/ap_ruby': 'bm:block/ap_violet', 'bm:block/ap_ruby_lt': 'bm:block/ap_violet_lt'}
        m['textures'] = {k: swap.get(v, v) for k, v in m['textures'].items()}
        R2.wj('assets/bm/models/item/apo_unbound_crown.json', m)
        R2.wj('assets/bm/items/apo_unbound_crown.json', {'model': {'type': 'minecraft:model', 'model': 'bm:item/apo_unbound_crown'}})
    R.POST.append(post)

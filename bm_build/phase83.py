"""2.67: ETHEREAL KILLERWATT and the ETHEREAL TENDRILS.

SET DOWN AN ETHEREAL GEM WHILE YOU FIGHT HIM (its shrine within 30 blocks of KillerWatt) and the gem answers HIM: he ascends
  into ETHEREAL KILLERWATT - black steel, iridescent scythes, glowing seams, jagged spikes - and the fight gets far harder:
  he heals whole with 80% more health and tougher armour, hits half again as hard, attacks faster, floats above the ground,
  and gains VOID LANCES (homing bolts of void that lift and wither whoever they reach).
BEAT HIS ETHEREAL FORM: THE ETHEREAL TENDRILS (certain the first time, a chance after) instead of his plain Tendrils - his
  Spark and his hoard as ever.
  Worn like his Tendrils and doing all they do, but: every lash and stab hits HALF AGAIN AS HARD and floats what it strikes;
  they fling you HALF AGAIN AS FAR, and after a fling you hang in the air a moment. Near an Ethereal Gem's shrine they're
  always at full thunderstorm strength and you regenerate.
"""
from items import item, T, TOTEM, ITEMS
from nbt import snbt, B, F, D, Int
import phase59  # (the Tendrils' machinery this extends)

ETH = '#c8a0ff'

item('ethereal_tendrils', TOTEM, 'Ethereal Tendrils', ETH,
     ['KillerWatt\'s scythes, black steel and iridescent,', 'torn from his Ethereal form.', ('Worn in place of a chestplate; all his', 'blue'),
      ('Tendrils do, and more:', 'blue'), ('blows half again as hard, and they float', 'aqua'), ('what they strike; flings half again as far,', 'aqua'),
      ('and a moment hanging in the air after.', 'aqua'), ('Near an Ethereal Gem: always at full', 'light_purple'),
      ('thunderstorm strength, and you mend.', 'light_purple')],
     model='bm:ethereal_tendrils', stack=1, cat='weapon', glint=True, tier=3,
     comps={'minecraft:equippable': {'slot': 'chest', 'swappable': True, 'asset_id': 'bm:kw_tendrils_eth', 'equip_sound': 'minecraft:item.armor.equip_chain'},
            'minecraft:enchantments': {'bm:kw_tendrils_eth': 1}})


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    tick, fast, second = [], [], []
    objs = ['bm.kxek']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    me = '@e[type=minecraft:husk,tag=bm.kxme,limit=1]'

    # ================================================================== ETHEREAL KILLERWATT
    second.append('execute as @e[type=minecraft:husk,tag=bm.kxboss,tag=!bm.kxeth] at @s if entity @e[type=minecraft:item_display,tag=bm.eshr,distance=..30] run function bm:p83/ascend')
    fn('p83/ascend', ['tag @s add bm.kxeth', 'scoreboard players set @s bm.kxel 10',
                      'attribute @s minecraft:max_health modifier add bm:kx_eth 0.8 add_multiplied_base', 'attribute @s minecraft:armor modifier add bm:kx_eth 6 add_value',
                      'attribute @s minecraft:movement_speed modifier add bm:kx_eth 0.15 add_multiplied_base',
                      'execute store result entity @s Health float 1 run attribute @s minecraft:max_health get',
                      'effect give @s minecraft:slow_falling infinite 0 true', 'scoreboard players set @s bm.kxatk 0', 'scoreboard players set @s bm.kxc 30',
                      'scoreboard players operation #kid bm.rng = @s bm.kxid',
                      'execute as @e[type=minecraft:item_display,tag=bm.kxp_boss,distance=..16] if score @s bm.kxid = #kid bm.rng run tag @s add bm.kxsel',
                      'function bm:p79/pet/dress_rig', 'tag @e[type=minecraft:item_display,tag=bm.kxsel] remove bm.kxsel',
                      'bossbar set bm:kwb name {text:"Ethereal KillerWatt",color:"light_purple"}', 'bossbar set bm:kwb color purple',
                      'particle minecraft:flash{color:[0.8,0.6,1.0,1.0]} ~ ~2 ~ 0 0 0 0 1', 'particle minecraft:end_rod ~ ~2.5 ~ 1 2 1 0.3 200',
                      'particle minecraft:reverse_portal ~ ~2 ~ 2 2 2 0.4 300',
                      'playsound minecraft:block.beacon.power_select hostile @a[distance=..96] ~ ~ ~ 2 0.5', 'playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..64] ~ ~ ~ 1.5 0.6',
                      'title @a[distance=..64] times 10 60 20', title('@a[distance=..64]', 'title', T('ETHEREAL KILLERWATT', ETH, bold=True)),
                      title('@a[distance=..64]', 'subtitle', T('the gem answers him', 'gray', italic=True))])
    # his parts wear the form; a rig rebuilt keeps it
    G.FUNCS['p79/boss/rig'].append('execute if entity @s[tag=bm.kxeth] run function bm:p79/pet/dress_rig')
    bt = G.FUNCS['p79/boss/tick']
    bt[0:1] = ['scoreboard players set #kel bm.rng 0', 'scoreboard players set #keth bm.rng 0',
               'execute if entity @s[tag=bm.kxeth] run scoreboard players set #kel bm.rng 10', 'execute if entity @s[tag=bm.kxeth] run scoreboard players set #keth bm.rng 1']
    k_ = next(i for i, l in enumerate(bt) if 'function bm:p79/boss/place' in l)
    bt[k_:k_ + 1] = ['execute unless entity @s[tag=bm.kxeth] rotated as @s rotated ~ 0 run function bm:p79/boss/place',
                     'execute if entity @s[tag=bm.kxeth] rotated as @s rotated ~ 0 positioned ~ ~0.7 ~ run function bm:p79/boss/place']
    G.FUNCS['p79/boss/init'].insert(0, 'bossbar set bm:kwb name {text:"KillerWatt",color:"green"}')
    G.FUNCS['p79/boss/init'].insert(1, 'bossbar set bm:kwb color green')
    # every blow of his half again as hard (each damage line of his gets an ethereal twin)
    for name in [n for n in G.FUNCS if n.startswith('p79/boss/')]:
        out = []
        for l in G.FUNCS[name]:
            if f'by {me}' in l and 'damage @s ' in l:
                import re
                m = re.search(r'damage @s ([\d.]+) ', l)
                n = float(m.group(1))
                out.append(f'execute if score #keth bm.rng matches 1 run ' + l.replace(m.group(0), f'damage @s {n * 1.5:g} '))
                out.append('execute unless score #keth bm.rng matches 1 run ' + l)
            else:
                out.append(l)
        G.FUNCS[name] = out
    G.FUNCS['p79/boss/start'] += ['execute if entity @s[tag=bm.kxeth] run scoreboard players set @s bm.kxc 30']
    # VOID LANCES: arms thrust out, and five bolts of void hunt you down
    bm_ = G.FUNCS['p79/boss/mind']
    k_ = next(i for i, l in enumerate(bm_) if 'random value 1..100' in l)
    bm_.insert(k_ + 1, 'execute if entity @s[tag=bm.kxeth] if score #r bm.rng matches 1..30 if entity @a[distance=..30,gamemode=!creative,gamemode=!spectator] '
                       'run return run function bm:p79/boss/start {a:6}')
    G.FUNCS['p79/boss/attack'].insert(-1, 'execute if score @s bm.kxatk matches 6 run function bm:p83/a_lances')
    at = lambda t, cmd: f'execute if score @s bm.kxt matches {t} run {cmd}'
    fn('p83/a_lances', [at(1, 'function bm:p79/boss/pose/charge'), at(1, 'playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..48] ~ ~ ~ 1.5 1.4'),
                        at('2..14', 'particle minecraft:reverse_portal ~ ~4 ~ 1.2 0.8 1.2 0.3 20'), at(15, 'function bm:p79/boss/pose/release'),
                        at(16, 'execute as @a[distance=..30,gamemode=!creative,gamemode=!spectator,sort=random,limit=5] at @s run function bm:p83/lance'),
                        at(16, 'playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..48] ~ ~ ~ 1.5 0.6'), at('30..', 'function bm:p79/boss/done')])
    # (a lance: a marker that flies at its player for 3 seconds)
    fn('p83/lance', ['tag @s add bm.kxlt_me', 'execute at @e[type=minecraft:husk,tag=bm.kxme,limit=1] positioned ~ ~4 ~ run summon minecraft:marker ~ ~ ~ {Tags:["bm.kxlance","bm.kxln"]}',
                     'execute store result score @e[type=minecraft:marker,tag=bm.kxln] bm.pid run scoreboard players get @s bm.pid',
                     'scoreboard players set @e[type=minecraft:marker,tag=bm.kxln] bm.kxt 60', 'tag @e[type=minecraft:marker,tag=bm.kxln] remove bm.kxln', 'tag @s remove bm.kxlt_me'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.kxlance] at @s run function bm:p83/lance_tick')
    fn('p83/lance_tick', ['scoreboard players remove @s bm.kxt 1', 'scoreboard players operation #lp bm.pid = @s bm.pid',
                          'execute as @a if score @s bm.pid = #lp bm.pid run tag @s add bm.kxlt_tgt',
                          'execute facing entity @a[tag=bm.kxlt_tgt,limit=1] eyes run tp @s ^ ^ ^0.7 ~ ~',
                          'particle minecraft:end_rod ~ ~ ~ 0.05 0.05 0.05 0.01 2', 'particle minecraft:reverse_portal ~ ~ ~ 0.1 0.1 0.1 0.05 4',
                          'execute if entity @a[tag=bm.kxlt_tgt,distance=..1.4] run function bm:p83/lance_hit', 'tag @a remove bm.kxlt_tgt',
                          'execute if score @s bm.kxt matches ..0 run kill @s'])
    fn('p83/lance_hit', ['execute as @a[tag=bm.kxlt_tgt,distance=..1.4] run damage @s 10 minecraft:magic',
                         'effect give @a[tag=bm.kxlt_tgt,distance=..1.4] minecraft:levitation 1 3', 'effect give @a[tag=bm.kxlt_tgt,distance=..1.4] minecraft:wither 3 1',
                         'particle minecraft:flash{color:[0.8,0.6,1.0,1.0]} ~ ~ ~ 0 0 0 0 1', 'playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..24] ~ ~ ~ 1 1.4',
                         'kill @s'])
    # beating his ethereal form: the Ethereal Tendrils
    wjson('bm/advancement/p83/killed_eth.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.kxeth"]}'}}]}}}, 'rewards': {'function': 'bm:p83/killed_eth'}})
    fn('p83/killed_eth', ['advancement revoke @s only bm:p83/killed_eth', 'scoreboard players set #eth bm.kxek 1', 'function bm:p79/killed',
                          'execute at @s as @a[distance=..64] at @s run function bm:p83/eth_reward', 'scoreboard players set #eth bm.kxek 0'])
    fn('p83/eth_reward', ['scoreboard players add @s bm.kxek 1', 'execute store result score #r bm.rng run random value 1..100',
                          'execute if score @s bm.kxek matches 1 run ' + give('ethereal_tendrils'),
                          'execute if score @s bm.kxek matches 2.. if score #r bm.rng matches 1..40 run ' + give('ethereal_tendrils'),
                          'execute if score @s bm.kxek matches 1 run ' + tellraw('@s', PREFIX + [T('The Ethereal Tendrils', ETH, bold=True),
                                                                                                 T(' are yours - harder blows, longer flings, and the air holds you a moment.', 'gray')]),
                          'loot give @s loot bm:p79/hoard'])

    # ================================================================== THE ETHEREAL TENDRILS (they count as his Tendrils everywhere)
    old = '*[minecraft:custom_data~{bm:"killerwatt_tendrils"}]'
    new = '*[minecraft:custom_data~{bm:"killerwatt_tendrils"}|minecraft:custom_data~{bm:"ethereal_tendrils"}]'
    for name, lines in G.FUNCS.items():
        if any(old in l for l in lines):
            G.FUNCS[name] = [l.replace(old, new) for l in lines]
    eth = 'items entity @s armor.chest *[minecraft:custom_data~{bm:"ethereal_tendrils"}]'
    # (the melee stab: the same, for the ethereal pair)
    wjson('bm/advancement/p83/eth_melee.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {
        'player': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'chest': {'predicates': {'minecraft:custom_data': '{bm:"ethereal_tendrils"}'}}}}}],
        'damage': {'type': {'is_direct': True, 'tags': [{'id': '#minecraft:is_lightning', 'expected': False}, {'id': '#minecraft:is_projectile', 'expected': False}]}}}}},
        'rewards': {'function': 'bm:p83/eth_melee'}})
    fn('p83/eth_melee', ['advancement revoke @s only bm:p83/eth_melee', 'function bm:p59/kw/melee'])
    # (who wears them: tagged each tick; near a shrine, thunderstorm strength and mending)
    G.FUNCS['p59/kw/tick'][0:0] = ['tag @s remove bm.kweth', f'execute if {eth} run tag @s add bm.kweth']
    second += ['execute as @a[tag=bm.kweth,tag=bm.eth] run effect give @s minecraft:regeneration 3 1 true',
               'execute as @a[tag=bm.kweth,tag=bm.eth] at @s run particle minecraft:end_rod ~ ~1.2 ~ 0.4 0.5 0.4 0.02 3']
    for name in [n for n in G.FUNCS if n.startswith('p59/kw/')]:
        out = []
        for l in G.FUNCS[name]:
            # full strength near a shrine
            if l.startswith('scoreboard players set #lv bm.rng 0'):
                out.append(l); continue
            if 'damage @s ' in l and 'by @a[tag=bm.kwme,limit=1]' in l:
                import re
                m = re.search(r'damage @s ([\d.]+) ', l)
                n = float(m.group(1))
                out.append('execute if entity @a[tag=bm.kwme,tag=bm.kweth] run ' + l.replace(m.group(0), f'damage @s {n * 1.5:g} '))
                out.append('execute unless entity @a[tag=bm.kwme,tag=bm.kweth] run ' + l)
            else:
                out.append(l)
        G.FUNCS[name] = out
    for name in [n for n in G.FUNCS if n.startswith('p59/kw/')]:
        L = G.FUNCS[name]
        for i, l in enumerate(L):
            if 'if predicate bm:p59/storm run scoreboard players set #lv bm.rng 2' in l:
                L.insert(i + 1, 'execute if entity @s[tag=bm.kweth,tag=bm.eth] run scoreboard players set #lv bm.rng 2')
                break
    # what they strike floats; a fling leaves you hanging in the air a moment
    for f_ in ('p59/kw/mob', 'p59/kw/stab', 'p59/kw/arc'):
        if f_ in G.FUNCS:
            G.FUNCS[f_].append('execute if entity @a[tag=bm.kwme,tag=bm.kweth] run effect give @s minecraft:levitation 1 2')
    G.FUNCS['p59/kw/flung'].append('execute if entity @s[tag=bm.kweth] run function bm:p83/hang')
    fn('p83/hang', ['effect give @s minecraft:levitation 1 0 true', 'effect give @s minecraft:slow_falling 3 0 true', 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.05 12'])
    # their look: the ethereal skins in place of the green-and-gold ones
    LOOKS = {'off': 'kw_tendrils_eth', 'rng': 'kw_tendrils_eth_r', 'hit': 'kw_tendrils_eth_s'}
    for lk, asset in LOOKS.items():
        wjson(f'bm/item_modifier/p83/kw_{lk}.json', {'function': 'minecraft:set_components', 'components': {'minecraft:equippable': {
            'slot': 'chest', 'swappable': True, 'asset_id': f'bm:{asset}', 'equip_sound': 'minecraft:intentionally_empty'}}})
    fn('p83/look', ['execute if score @s bm.kwmd matches 1 run return run item modify entity @s armor.chest bm:p83/kw_rng', 'item modify entity @s armor.chest bm:p83/kw_off'])
    G.FUNCS['p59/kw/look'].insert(0, f'execute if {eth} run return run function bm:p83/look')
    G.FUNCS['p59/kw/flash'].insert(0, f'execute if {eth} unless score @s bm.kwfl matches 1.. run item modify entity @s armor.chest bm:p83/kw_hit')
    G.FUNCS['p59/kw/flash'].insert(1, f'execute if {eth} run return run scoreboard players set @s bm.kwfl 6')
    # their fling: the same tags as his Tendrils, half again the impulse
    import phase59 as P59
    def fling(tagname, direction, scale, mag):
        return {'requirements': {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % tagname}},
                'effect': {'type': 'minecraft:all_of', 'effects': [
                    {'type': 'minecraft:apply_impulse', 'direction': direction, 'coordinate_scale': scale, 'magnitude': mag},
                    {'type': 'minecraft:run_function', 'function': 'bm:p59/kw/flung'}]}}
    wjson('bm/enchantment/kw_tendrils_eth.json', {
        'anvil_cost': 1, 'description': T('Ethereal Tendrils', ETH), 'max_level': 1, 'weight': 1,
        'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0},
        'slots': ['chest'], 'supported_items': 'minecraft:totem_of_undying',
        'effects': {'minecraft:tick': [fling('bm.kwl1', [0, 0, 1], [1, 1, 1], 1.9), fling('bm.kwl2', [0, 0, 1], [1, 1, 1], 2.8), fling('bm.kwl3', [0, 0, 1], [1, 1, 1], 3.7),
                                       fling('bm.kwup', [0, 1, 0], [0.2, 1, 0.2], 1.7)],
                    'minecraft:damage_immunity': [{'requirements': {'condition': 'minecraft:damage_source_properties', 'predicate': {'tags': [
                        {'id': '#minecraft:is_fall', 'expected': True}]}}, 'effect': {}}]}})
    fn('admin/ethereal_tendrils', [give('ethereal_tendrils')])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def rp(R):
    """the ethereal skins: his Tendrils' worn skins and held model, recoloured - black steel, iridescent blades"""
    import colorsys
    from PIL import Image

    def irid(im):
        im = im.convert('RGBA'); out = im.copy(); w, h = im.size
        for y in range(h):
            for x in range(w):
                r, g, b, a = im.getpixel((x, y))
                if a == 0: continue
                L = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                if L < 0.22:                                                     # (the dark spine and harness: black steel)
                    out.putpixel((x, y), (int(12 + 40 * L), int(12 + 40 * L), int(18 + 60 * L), a)); continue
                rr, gg, bb = colorsys.hsv_to_rgb(((x * 1.1 + y * 1.7) / max(w, h) * 1.4 + L * 0.3) % 1.0, 0.55, 0.45 + 0.55 * L)
                out.putpixel((x, y), (int(rr * 255), int(gg * 255), int(bb * 255), a))
        return out

    def post(R2):
        import json, os
        import phase59_tendrils as TD
        for nm in TD.LOOKS:
            enm = nm.replace('kw_tendrils', 'kw_tendrils_eth')
            irid(TD.skin(nm)).save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'wings', f'{enm}.png'))
            R2.wj(f'assets/bm/equipment/{enm}.json', {'layers': {'wings': [{'texture': f'bm:{enm}'}], 'humanoid': [{'texture': 'bm:kw_harness'}]}})
        # the held model: his Tendrils' model, every texture re-coloured
        src = json.load(open(R2.p('assets', 'bm', 'models', 'item', 'killerwatt_tendrils.json')))
        tex = {}
        for k, v in src.get('textures', {}).items():
            ns, path = v.split(':') if ':' in v else ('minecraft', v)
            f = R2.p('assets', ns, 'textures', *path.split('/')) + '.png'
            if ns == 'bm' and os.path.exists(f):
                nm = path.split('/')[-1] + '_eth'
                irid(Image.open(f)).save(R2.p('assets', 'bm', 'textures', *path.split('/')[:-1], nm + '.png'))
                tex[k] = f'bm:{"/".join(path.split("/")[:-1] + [nm])}'
            else:
                tex[k] = v
        R2.wj('assets/bm/models/item/ethereal_tendrils.json', dict(src, textures=tex))
        R2.wj('assets/bm/items/ethereal_tendrils.json', {'model': {'type': 'minecraft:model', 'model': 'bm:item/ethereal_tendrils'}})
    R.POST.append(post)

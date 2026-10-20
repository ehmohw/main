"""2.83: THE LESS URGENT LIST, part one - the drowned that never fought, full bags, the Trophy Stand, cases to stand on,
Emma and Leo for everyone, money that breaks back down.

THE SUNKEN THRONE  (p2/data.py, p2/logic.py, p2/bosses.py) the drowned only hunt someone in water or out at night, so on the
                   temple's dry floors they stood about. The Tyrant's crew are Tidebound Sailors (zombies in turtle shells,
                   tridents and swords) and Barnacle Bowmen (bogged) now - spawners, waves, his calls and the fail mob. The
                   Tyrant himself is still a drowned in his pool: he answers a blow, and his slam and surge need no water.
FULL BAGS          the Vacuum Satchel and the Prime Cooler say so when something they'd take won't fit (every 10 seconds at
                   most): "Your Vacuum Satchel is full."
THE TROPHY STAND   (phase161) it stood back to front - an item display shows a model's back toward the way it faces - so the
                   tall back panel faced you, the trophies hovered over the low step and the laurels sat inside the panel.
                   The stand and its trophies turn round (stands already set down turn by themselves); the steps stop at the
                   back panel instead of running through it (no more flickering at the back).
DISPLAY CASES      a floor case is solid now - stand on it (an invisible barrier fills its block; picked up, the barrier
                   goes too). Its click box is a hair bigger than the block, so right-click and punch still reach it.
EMMA AND LEO       (phase57, phase96) every player can find each of them - Emma hums for anyone without her ribbon, and a
                   fort that's been held stays open to anyone who hasn't got Leo's crest yet (he takes up his watch again).
                   Emma also turns up in plains and birch woods now, a little more often; the forts are a little closer.
INVASION NIGHTS    harder, and better paid - nearer a Blood Moon, never past it: the Vorn come down more often (a surge
                   every 3 seconds or so, up to 12 about you, was 1 in 5 and 8), troopers 40 health and 6 damage (30 / 4),
                   saucers 50 health; half the night's monsters are bioengineered (was a third), with 80% more health
                   (was 50%) and a third more bite. Every Vorn and every bioengineered monster may drop a Token (troopers,
                   saucers, big slimes and bio phantoms 1 in 2; the rest 1 in 5) - on top of their shards.
BLOOD MOON HEISTS  harder than Tier V, but a solo raider in an upgraded kit can win: the night's guards were the overworld
                   Blood Moon vindicator (120 health, full netherite, a Sharpness VI netherite axe, Strength II and
                   Resistance). A heist's Blood Moon guard is its own now: Tier V's health and half again, diamond armour, a
                   Sharpness III diamond axe, Strength I, no Resistance - still red-eyed, still dropping Blood Crystals.
                   Your followers stand firm under the red sky: near a Blood Moon foe in the gutter they have Resistance I
                   and Regeneration I.
THE RAT BANK       (phase31, gen_dp) Medallions and Trophies break back down at the rates they're made (1 Medallion = 5
                   Tokens, 1 Trophy = 4 Medallions) at Old Barnaby and the Fence - and the Banker's Card has an Exchange
                   page that changes your account up or down, no fee.
"""
import json
import os
import re
from items import T, item, TOTEM
from useitem import hold, HOLD
from nbt import snbt, F

SEA = '#3fb8a8'

# ------------------------------------------------------------------ (2.83) the collectors: Dennis's and Pistachio's
COLLECTORS = {
    'ore': dict(iid='ore_magnet', name="Dennis's Ore Magnet", col='#e8b04a', price=16, code=2140, menu=2100, tag='p174_ore',
                lore=['A horseshoe of dwarf-iron that hums near ore.', ('Right-click: switch it on or off.', 'blue'),
                      ('While on, anywhere in your pack: ores, raw metals,', 'blue'), ('gems and the like within 8 blocks fly to you.', 'blue'),
                      ('"Saves the knees, lad."', 'dark_gray')],
                items=['coal', 'charcoal', 'raw_copper', 'raw_iron', 'raw_gold', 'copper_ingot', 'iron_ingot', 'gold_ingot', 'iron_nugget', 'gold_nugget',
                       'redstone', 'lapis_lazuli', 'quartz', 'amethyst_shard', 'diamond', 'emerald', 'ancient_debris', 'netherite_scrap', 'flint',
                       'glowstone_dust', 'echo_shard', '#minecraft:coal_ores', '#minecraft:iron_ores', '#minecraft:copper_ores', '#minecraft:gold_ores',
                       '#minecraft:redstone_ores', '#minecraft:lapis_ores', '#minecraft:diamond_ores', '#minecraft:emerald_ores', 'nether_quartz_ore',
                       'raw_iron_block', 'raw_gold_block', 'raw_copper_block']),
    'mob': dict(iid='spirit_jar', name="Pistachio's Spirit Jar", col='#9ae8c8', price=16, code=2190, menu=2151, tag='p174_mob',
                lore=['A little jar with something polite inside.', ('Right-click: switch it on or off.', 'blue'),
                      ('While on, anywhere in your pack: whatever', 'blue'), ('monsters and beasts drop within 8 blocks floats to you.', 'blue'),
                      ('"It insists on carrying them, sir."', 'dark_gray')],
                items=['rotten_flesh', 'bone', 'bone_meal', 'string', 'spider_eye', 'gunpowder', 'slime_ball', 'leather', 'feather', 'ink_sac', 'glow_ink_sac',
                       'ender_pearl', 'blaze_rod', 'magma_cream', 'phantom_membrane', 'prismarine_shard', 'prismarine_crystals', 'breeze_rod', 'arrow',
                       'ghast_tear', 'rabbit_hide', 'rabbit_foot', 'beef', 'porkchop', 'mutton', 'chicken', 'rabbit', 'cod', 'salmon', 'tropical_fish',
                       'pufferfish', 'shulker_shell', 'nautilus_shell', 'armadillo_scute', 'turtle_scute', 'egg', 'honeycomb', 'wither_skeleton_skull',
                       'skeleton_skull', 'zombie_head', 'creeper_head', 'piglin_head', 'sugar', 'glass_bottle', 'stick', '#minecraft:wool',
                       'carrot', 'potato', 'iron_ingot', 'gold_nugget', 'copper_ingot', 'trident', 'bow', 'crossbow', 'golden_sword', 'iron_sword',
                       'saddle', 'emerald', 'totem_of_undying', 'heavy_core', 'trial_key', 'wind_charge', 'blaze_powder', 'goat_horn']),
}
for _k, _c in COLLECTORS.items():
    item(_c['iid'], TOTEM, _c['name'], _c['col'], _c['lore'] + [(f'{_c["price"]} Tokens.', 'gray')], model=f'bm:{_c["iid"]}', stack=1, cat='builder', comps=hold('none'))
    HOLD[_c['iid']] = f'bm:p174/col/use_{_k}'


def buy_btn(k):
    import phase28 as P28
    c = COLLECTORS[k]
    return P28.btn([T(f'Buy the {c["name"].split(" ", 1)[1]}', c['col'], bold=True), T(f'  {c["price"]} Tokens', 'gray')], c['code'], width=230,
                   tooltip=T(c['lore'][2][0] + ' ' + c['lore'][3][0], 'gray'))


def generate(G):
    import phase98 as P98
    fn, title = G.fn, G.title
    F_ = G.FUNCS
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    objs = ['bm.vfcd']
    F_['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ================================================================== FULL BAGS
    # (p33/vac/take: what's left of the stack after merging and a free slot - unchanged means nothing fit)
    tk = F_['p33/vac/take']
    k = next(i for i, l in enumerate(tk) if l.startswith('execute store result score #vn bm.rng run data get storage bm:tmp vac.in.count'))
    tk.insert(k + 1, 'scoreboard players operation #vn0 bm.rng = #vn bm.rng')
    k = next(i for i, l in enumerate(tk) if 'run function bm:p33/vac/newslot' in l)
    tk.insert(k + 1, 'execute if score #vn bm.rng = #vn0 bm.rng run scoreboard players set #vfull bm.rng 1')
    for pull, name in (('p33/vac/pull', 'Vacuum Satchel'), ('p148/cool/pull', 'Prime Cooler')):
        pl = F_[pull]
        k = next(i for i, l in enumerate(pl) if l == 'scoreboard players set #vtak bm.rng 0')
        pl.insert(k + 1, 'scoreboard players set #vfull bm.rng 0')
        pl.append(f'execute if score #vfull bm.rng matches 1 unless score @s bm.vfcd matches 1.. run function bm:p174/full {{n:"{name}"}}')
    fn('p174/full', ['scoreboard players set @s bm.vfcd 10', '$' + title('@s', 'actionbar', [T('Your $(n) is full', '#ffb060'), T(' - it leaves the rest on the ground.', 'gray')]),
                     'playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.6 0.8'])
    F_['loop/second'].append('scoreboard players remove @a[scores={bm.vfcd=1..}] bm.vfcd 1')

    # ================================================================== THE TROPHY STAND: stands already set down turn round
    F_['loop/second'].append('execute as @e[type=minecraft:item_display,tag=bm.tsbase,tag=!bm.ts283] run function bm:p174/ts_turn')
    fn('p174/ts_turn', ['tag @s add bm.ts283', 'data modify entity @s transformation.left_rotation set value [0f,1f,0f,0f]'])

    # ================================================================== DISPLAY CASES: a floor case you can stand on
    sf = F_['p72/dc/spawn_floor']
    sf.insert(0, 'setblock ~ ~ ~ minecraft:barrier keep')
    k = next(i for i, l in enumerate(sf) if l.startswith('tp @e[tag=bm.dcnew'))
    sf.insert(k, 'execute as @e[type=minecraft:interaction,tag=bm.dcnew,distance=..0.1] run function bm:p174/dc_floor')
    fn('p174/dc_floor', ['tag @s add bm.dcfloor', 'tag @s add bm.dc283', 'data merge entity @s[type=minecraft:interaction] {width:1.02f,height:1.02f}'])
    F_['p72/dc/gone'].insert(0, 'execute if entity @s[tag=bm.dcfloor] if block ~ ~ ~ minecraft:barrier run setblock ~ ~ ~ minecraft:air')
    # (cases already in the world: a floor case's box was 0.85 wide)
    F_['loop/second'].append('execute as @e[type=minecraft:interaction,tag=bm.dchit,tag=!bm.dc283] at @s run function bm:p174/dc_old')
    fn('p174/dc_old', ['tag @s add bm.dc283', 'execute unless data entity @s {width:0.85f} run return 0',
                       'setblock ~ ~ ~ minecraft:barrier keep', 'tag @s add bm.dcfloor', 'data merge entity @s[type=minecraft:interaction] {width:1.02f,height:1.02f}'])
    # (the place-check looked for another case within 0.7 of a floor spot: the bigger box doesn't change where it sits)

    # ================================================================== LEO: a held fort opens again for anyone without his crest
    crest = '*[minecraft:custom_data~{bm:"leo_crest"}]'
    F_['loop/second'].append('execute as @e[type=minecraft:marker,tag=bm.lefort,tag=bm.ledone] at @s if entity @a[distance=..32,gamemode=!spectator] '
                             'run function bm:p174/fort_open')
    fn('p174/fort_open', ['tag @a[distance=..32] remove bm.lenocrest',
                          f'execute as @a[distance=..32,gamemode=!spectator] unless items entity @s container.* {crest} unless items entity @s weapon.offhand {crest} run tag @s add bm.lenocrest',
                          'execute unless entity @a[tag=bm.lenocrest,distance=..32] run return 0', 'tag @a remove bm.lenocrest',
                          'tag @s remove bm.ledone', 'particle minecraft:splash ~ ~1.5 ~ 0.5 0.8 0.5 0.1 20'])

    # ================================================================== INVASION NIGHTS: harder, and better paid
    sg = F_['p32/inv/surge']
    sg[:] = [l.replace('random value 1..5', 'random value 1..3').replace('matches 8.. run return 0', 'matches 12.. run return 0') for l in sg]
    assert any('1..3' in l for l in sg) and any('12..' in l for l in sg), sg
    for t, (hp, dmg) in (('trooper', (40, 6)), ('saucer', (50, None))):
        L = F_[f'p32/spawn/{t}']
        n0 = sum(1 for l in L if 'summon minecraft:' in l)
        for i, l in enumerate(L):
            if 'summon minecraft:' not in l: continue
            l = re.sub(r'Health:\d+f', f'Health:{hp}f', l)
            l = re.sub(r'(max_health",base:)\d+d', rf'\g<1>{hp}d', l)
            if dmg: l = re.sub(r'(attack_damage",base:)\d+d', rf'\g<1>{dmg}d', l)
            L[i] = l
        assert n0 and any(f'Health:{hp}f' in l for l in L), t
    k = 0
    for name, L in F_.items():
        if name.startswith('p32/bio/roll_'):
            L[:] = [l.replace('matches 1..35 run return run', 'matches 1..50 run return run') for l in L]; k += 1
    assert k >= 10, k
    ap = F_['p32/bio/apply']
    ap[:] = [l.replace('modifier add bm:bio 0.5 add_multiplied_base', 'modifier add bm:bio 0.8 add_multiplied_base') for l in ap]
    ap.insert(-1, 'attribute @s minecraft:attack_damage modifier add bm:bio 0.33 add_multiplied_base')
    # (the Tokens: a pool on each Vorn table and each bioengineered one)
    # (this pass runs after the 26.3 loot migration, so the entry is cloned from a migrated Token pool, not built fresh)
    root = G.path('data', 'bm', 'loot_table', 'p32')
    with open(os.path.join(root, 'trooper.json')) as h:
        tent = next(p['entries'][0] for p in json.load(h)['pools'] if '{bm:\\"token\\"' in json.dumps(p['entries'][0]))
    tok = lambda chance: {'rolls': 1, 'entries': [json.loads(json.dumps(tent))],
                          'condition': {'type': 'minecraft:all_of', 'terms': [{'type': 'minecraft:killed_by_player'}, {'type': 'minecraft:random_chance', 'chance': chance}]}}
    nlt = 0
    for f, ch in [('trooper', 0.5), ('saucer', 0.5), ('bigslime', 0.5), ('bphantom', 0.5)] + \
                 [(f'bio/{x[:-5]}', 0.2) for x in sorted(os.listdir(os.path.join(root, 'bio'))) if x.endswith('.json')]:
        p = os.path.join(root, f + '.json')
        with open(p) as h: lt = json.load(h)
        lt['pools'].append(tok(ch))
        with open(p, 'w') as h: json.dump(lt, h)
        nlt += 1
    assert nlt >= 14, nlt

    # ================================================================== BLOOD MOON HEISTS: a guard you can beat with a good kit
    gs = F_['p70/guard_set1']
    old = 'execute if score #gn bm.rng matches 1 if entity @s[type=minecraft:vindicator] run function bm:mobs/blood/vindicator'
    assert old in gs, 'p70/guard_set1 changed'
    gs[gs.index(old)] = 'execute if score #gn bm.rng matches 1 if entity @s[type=minecraft:vindicator] run function bm:p174/gv_blood'
    dia = lambda slot, it: f'item replace entity @s armor.{slot} with minecraft:diamond_{it}'
    fn('p174/gv_blood', ['data merge entity @s {drop_chances:{head:0f,chest:0f,legs:0f,feet:0f,mainhand:0f,offhand:0f},DeathLootTable:"bm:entities/blood/vindicator",'
                         'CustomName:{text:"Blood Moon Guard",color:"dark_red",bold:true}}',
                         'tag @s add bm.blood', 'tag @s add bm.tiered', 'team join bm.blood @s',
                         dia('head', 'helmet'), dia('chest', 'chestplate'), dia('legs', 'leggings'), dia('feet', 'boots'),
                         'item replace entity @s weapon.mainhand with minecraft:diamond_axe[enchantments={"minecraft:sharpness":3}]',
                         'effect give @s minecraft:strength infinite 0 true', 'effect give @s minecraft:fire_resistance infinite 0 true',
                         # (health: what the tier gave it - p70/guard_set1 set it just before - and half again)
                         'execute store result score #bh bm.rng run attribute @s minecraft:max_health base get',
                         'scoreboard players operation #bh bm.rng *= #3 bm.rng', 'scoreboard players operation #bh bm.rng /= #2 bm.rng',
                         'execute store result storage bm:gv h double 1 run scoreboard players get #bh bm.rng', 'function bm:p70/hp with storage bm:gv',
                         'execute store result entity @s Health float 1 run scoreboard players get #bh bm.rng',
                         'attribute @s minecraft:follow_range base set 48', 'attribute @s minecraft:knockback_resistance base set 0.4',
                         'attribute @s minecraft:movement_speed modifier add bm:blood 0.05 add_multiplied_base',
                         'particle minecraft:dust{color:[0.6,0.0,0.0],scale:2.0} ~ ~1 ~ 0.5 1 0.5 0 20'])
    pets = sorted({(v[3], v[4]) for v in P98.CALLED if v[3] and v[4]} | {('wolf', v[3]) for v in P98.HIRED})
    F_['loop/second'] += [f'execute in bm:gutter as @e[type=minecraft:{h},tag={t},distance=0..] at @s if entity @e[tag=bm.blood,distance=..24] '
                          f'run function bm:p174/blood_pet' for h, t in pets]
    fn('p174/blood_pet', ['effect give @s minecraft:resistance 3 0 true', 'effect give @s minecraft:regeneration 3 0 true'])

    # ================================================================== THE COLLECTORS: Dennis's Ore Magnet, Pistachio's Spirit Jar
    for k, c in COLLECTORS.items():
        iid, tg = c['iid'], c['tag']
        G.wjson(f'bm/tags/item/{tg}.json', {'values': [x if x.startswith('#') else f'minecraft:{x}' for x in c['items']]})
        has = f'*[minecraft:custom_data~{{bm:"{iid}"}}]'
        on = f'*[minecraft:custom_data~{{bm:"{iid}",bm_on:1b}}]'
        # buying it (as the trader's menu button: Tokens from your pockets)
        act = F_['p162/dw/act' if k == 'ore' else 'p162/ps/act']
        act.insert(1, f'execute if score #act bm.pay matches {c["code"]} run return run function bm:p174/col/buy_{k}')
        who = c['name'].split("'")[0]
        fn(f'p174/col/buy_{k}', [f'execute store result score #n bm.pay run clear @s *[minecraft:custom_data~{{bm:"token"}}] 0',
                                 f'execute if score #n bm.pay matches ..{c["price"] - 1} run return run ' + say(f'{who}: "That\'s {c["price"]} Tokens, friend - on you."', c['col']),
                                 f'clear @s *[minecraft:custom_data~{{bm:"token"}}] {c["price"]}', G.give(iid),
                                 'playsound minecraft:entity.villager.yes neutral @s ~ ~ ~ 0.6 1.1', say(f'{who}: "Pleasure. Right-click it to switch it on."', c['col'])])
        use = []
        for slot in ('weapon.mainhand', 'weapon.offhand'):
            use += [f'execute if items entity @s {slot} {on} run return run function bm:p174/col/off {{slot:"{slot}"}}',
                    f'execute if items entity @s {slot} {has} run return run function bm:p174/col/on {{slot:"{slot}"}}']
        fn(f'p174/col/use_{k}', use)
        # at work: once a quarter second, its kind within 8 blocks flies to you (what's lying at your feet already: your pockets are full)
        F_['loop/fast'].append(f'execute as @a[gamemode=!spectator] if items entity @s container.* {on} at @s run function bm:p174/col/pull_{k}')
        fn(f'p174/col/pull_{k}', [f'execute if entity @e[type=minecraft:item,distance=..1.2,nbt={{PickupDelay:0s}}] unless score @s bm.vfcd matches 1.. '
                                  f'if function bm:p174/col/feet_{k} run function bm:p174/full {{n:"{c["name"].split(" ", 1)[1]}"}}',
                                  f'execute as @e[type=minecraft:item,distance=1.2..8,nbt={{PickupDelay:0s}}] if items entity @s contents #bm:{tg} run tp @s ~ ~0.3 ~'])
        fn(f'p174/col/feet_{k}', ['scoreboard players set #ff bm.rng 0',
                                  f'execute as @e[type=minecraft:item,distance=..1.2,nbt={{PickupDelay:0s}}] if items entity @s contents #bm:{tg} run function bm:p174/col/age',
                                  'return run scoreboard players get #ff bm.rng'])
    fn('p174/col/age', ['execute store result score #ag bm.rng run data get entity @s Age', 'execute if score #ag bm.rng matches 60.. run scoreboard players set #ff bm.rng 1'])
    # switching it on and off (the held one; both kinds share the two modifiers)
    G.wjson('bm/item_modifier/p174/col_on.json', [{'function': 'minecraft:set_custom_data', 'tag': '{bm_on:1b}'},
                                                 {'function': 'minecraft:set_components', 'components': {'minecraft:enchantment_glint_override': True}}])
    G.wjson('bm/item_modifier/p174/col_off.json', [{'function': 'minecraft:set_custom_data', 'tag': '{bm_on:0b}'},
                                                  {'function': 'minecraft:set_components', 'components': {'minecraft:enchantment_glint_override': False}}])
    for to, w in (('on', 'ON'), ('off', 'off')):
        fn(f'p174/col/{to}', [f'$item modify entity @s $(slot) bm:p174/col_{to}', 'playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.5 1.5',
                              title('@s', 'actionbar', T(f'Switched {w}.', 'gray'))])
    fn('admin/collectors', [G.give(c['iid']) for c in COLLECTORS.values()])


    # ================================================================== FOLLOWERS COME BACK ONLY TO THEIR ITEM; ONE WILFREY
    # (2.82t's after-a-faint return called the follower whether or not you still carried its item, and Wilfrey - who had no
    #  "put the item away and he goes home" rule - piled up: a test bot without the locket had four of him, and the follower
    #  cap counted them. The return now waits until you carry the item; Wilfrey goes home three seconds after the locket
    #  leaves you, like every other follower.)
    import phase68 as P68, phase173 as P173
    has = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    tag_iid = {v[3]: v[1] for v in P68.KINDS.values()}
    for w, (cd, typ, tag, call) in P173.AR.items():
        i, iid = P173.AR_IDX[w], tag_iid.get(tag)
        assert iid, (w, tag)
        L = F_[f'p173/ar/back_{i}']
        k = L.index(f'function bm:{call}')
        L.insert(k, f'execute unless items entity @s container.* {has(iid)} unless items entity @s weapon.offhand {has(iid)} run return run tag @s add bm.arw{i}')
    loc = tag_iid['bm.wilfrey']
    F_['loop/second'].append('execute as @e[type=minecraft:wolf,tag=bm.wilfrey] at @s run function bm:p174/wil_item')
    own = '@a[tag=bm.fown,limit=1]'
    fn('p174/wil_item', ['scoreboard players operation #me bm.pid = @s bm.pid', 'tag @a remove bm.fown',
                         'execute as @a if score @s bm.pid = #me bm.pid run tag @s add bm.fown',
                         'execute unless entity @a[tag=bm.fown] run return 0',
                         'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0',
                         'execute if dimension bm:gutter run return run scoreboard players set @s bm.fmis 0',
                         f'execute if items entity {own} container.* {has(loc)} run return run scoreboard players set @s bm.fmis 0',
                         f'execute if items entity {own} weapon.offhand {has(loc)} run return run scoreboard players set @s bm.fmis 0',
                         f'execute if items entity {own} player.cursor {has(loc)} run return run scoreboard players set @s bm.fmis 0',
                         'scoreboard players add @s bm.fmis 1',
                         'execute if score @s bm.fmis matches 3.. run function bm:p2/wil/fade', 'tag @a remove bm.fown'])

def rp(R):
    g = R.grid
    R.ICONS['ore_magnet'] = g(['................', '................', '...rrr....rrr...', '...rRr....rRr...', '...rRr....rRr...', '...rRr....rRr...', '...rRr....rRr...',
                               '...rRrr..rrRr...', '....rRRrrRRr....', '.....rrRRrr.....', '.......rr.......', '..y..........y..', '...y...gg...y...',
                               '......gGGg......', '.......gg.......', '................'],
                              dict(r='#5a2a20', R='#c84a3a', y='#ffe060', g='#4ad8ff', G='#c8f4ff'))
    R.ICONS['spirit_jar'] = g(['................', '......kkkk......', '......cccc......', '.....kwwwwk.....', '....kw.ee.wk....', '....kweeeewk....', '....kwe.e.ewk...',
                               '....kweeeewk....', '....kw.ee.wk....', '....kweeeewk....', '....kwwwwwwk....', '.....kkkkkk.....', '................', '................',
                               '................', '................'],
                              dict(k='#2a4a40', c='#8a6a3a', w='#c8f0e8', e='#6affc8'))

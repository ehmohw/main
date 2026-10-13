"""2.65: THE VAULT'S KITS FIGHT LIKE THEIR GEAR, HIRELINGS, THE ENDLESS VAULT AND THE PIT.

KITS - each loaner kit now has an ability (right-click, with a cooldown you can see) and gear that behaves like what it is:
  TANK     the BULWARK HORN (30 s): Absorption IV and Resistance II for you, Resistance for the crew near you, and every
           guard within 7 is slowed and weakened. Sneaking behind the Juggernaut plate: Resistance. The Kokiri Sword's
           blows slow what they hit.
  OFFENSE  the SHADOWSTEP CHARM (18 s): blink up to seven blocks ahead (never through walls), unseen for 2 seconds, with
           Strength II. BLOODRUSH: every guard you drop gives you a burst of speed and healing. The Cutlass now and then
           finds a gap (+4).
  RANGED   the VOLLEY QUIVER (14 s): five arrows in a fan. The Fairy Bow's arrows pin what they hit (Slowness).
  SUPPORT  the TIDAL WARD (24 s): heals and shields the crew near you and washes off poison, wither, slowness, weakness,
           blindness and darkness (alone: a stronger heal for you). LIFELINE: once a minute, falling low wraps you in
           absorption and regeneration.
HIRELINGS (Goldtooth sells their contracts; yours for good - but they never leave the vault): use the contract in the
  vault and your hireling joins you, and comes along to every heist after (sneak + use: send them off). One at a time.
  KNUCKLES the brawler (tough, hits hard) - DOC WHISKERS the medic (keeps the crew topped up) - FINGERS the pickpocket
  (lifts coins off guards into the pot, sniffs out loose bricks) - TICK-TOCK the clockwork turret (shoots guards) -
  BOOMER the demolitions rat (lobs bombs into crowds). Knocked out: back in 45 seconds.
THE ENDLESS VAULT (Plan a Heist; after a Tier I clear): the rooms never end, and they get harder - and richer - every four
  rooms (the theme changes with the tier). Every fifth room is a Rats' Rest with a cash-out plate: step on it and the haul
  is paid (one share per room cleared, on top of the usual). Tries as usual - run out and it's all lost.
THE PIT (Plan a Heist; after a Tier I clear): an arena. Waves of the tier's guards, harder every three waves, a guardian
  every fifth. Between waves, the emerald plate cashes out (one share per wave survived)."""
from items import item, T, TOTEM, ITEMS, consumable
from nbt import snbt, B, F, D, Int
from useitem import hold, HOLD
from structures import Build
import phase70 as P70
import phase70_rooms as RM
import phase72 as P72
import phase75 as P75
import phase75_rooms as R5

GOLD = '#ffcf40'
LUCKY = '#7dff6a'

# ---------------------------------------------------------------- the kits' abilities
ABIL = {1: ('kit_horn', 'Bulwark Horn', '#c0392b', 'minecraft:goat_horn', 30,
            ['A Juggernaut\'s war horn.', ('Use: Absorption IV + Resistance II for', 'blue'), ('you, Resistance for the crew near you;', 'blue'),
             ('guards within 7 slowed and weakened.', 'blue'), ('Every 30 seconds.', 'gray')]),
        2: ('kit_step', 'Shadowstep Charm', '#ff7a1a', 'minecraft:ender_eye', 18,
            ['It folds a few steps of shadow.', ('Use: blink up to 7 blocks ahead', 'blue'), ('(never through walls) - unseen, and', 'blue'),
             ('Strength II, for a moment.', 'blue'), ('Every 18 seconds.', 'gray')]),
        3: ('kit_volley', 'Volley Quiver', '#5ad84a', 'minecraft:spectral_arrow', 14,
            ['A quiver with a trick to it.', ('Use: five arrows in a fan.', 'blue'), ('Every 14 seconds.', 'gray')]),
        4: ('kit_tidal', 'Tidal Ward', '#7ad0ea', 'minecraft:heart_of_the_sea', 24,
            ['The tide answers a Tidecaller.', ('Use: heal and shield the crew near you,', 'blue'), ('and wash off poison, wither, slowness,', 'blue'),
             ('weakness, blindness and darkness.', 'blue'), ('Alone: a stronger heal for you.', 'blue'), ('Every 24 seconds.', 'gray')])}
for _r, (_iid, _nm, _col, _model, _cd, _lore) in ABIL.items():
    item(_iid, TOTEM, _nm, _col, _lore, model=_model, stack=1, cat='weapon', glint=True,
         comps={'minecraft:consumable': consumable(0.15, 'none', 'minecraft:intentionally_empty', False),
                'minecraft:use_cooldown': {'seconds': float(_cd), 'cooldown_group': f'bm:{_iid}'}})
    _nm0, _c0, _d0, _arm0, _hand0 = P72.ROLES[_r]
    _hand0.insert(1, _iid)
P72.ROLES[1] = P72.ROLES[1][:2] + ('Juggernaut plate, Hylian Shield, Kokiri Sword, the BULWARK HORN. +8 health, half knockback; '
                                   'sneak for Resistance; the sword slows what it hits.',) + P72.ROLES[1][3:]
P72.ROLES[2] = P72.ROLES[2][:2] + ("Shadowstep (iron-strong), Captain's Cutlass, the SHADOWSTEP CHARM. Strength; every guard you drop: "
                                   "speed and healing; the cutlass finds gaps.",) + P72.ROLES[2][3:]
P72.ROLES[3] = P72.ROLES[3][:2] + ("Smuggler's set, Fairy Bow, arrows, the VOLLEY QUIVER. Speed; foes near you glow for the crew; "
                                   "your arrows pin what they hit.",) + P72.ROLES[3][3:]
P72.ROLES[4] = P72.ROLES[4][:2] + ("Tidecaller (iron-strong), Staff of Sparks, Bloomheart, healing potions, the TIDAL WARD. "
                                   "The crew near you regenerates; LIFELINE when you fall low.",) + P72.ROLES[4][3:]

# ---------------------------------------------------------------- hirelings: (key, name, rat, colour, health, damage, speed, price, what they do)
HIRE = {1: ('brawler', 'Knuckles', 'soldier', '#c0392b', 60, 7.0, 0.32, 48, ['A brawler. Tough, and hits hard.']),
        2: ('medic', 'Doc Whiskers', 'prof', '#7ad0ea', 30, 1.0, 0.33, 56, ['A medic. Keeps you and your crew', 'topped up, and patches the badly hurt.']),
        3: ('pickpocket', 'Fingers', 'grey', '#d9a066', 26, 3.0, 0.38, 40, ['A pickpocket. Lifts coins off guards', 'into the pot; sniffs out loose bricks.']),
        4: ('turret', 'Tick-Tock', 'teller', GOLD, 34, 0.0, 0.30, 64, ['A clockwork turret. Shoots the nearest', 'guard every couple of seconds.']),
        5: ('boomer', 'Boomer', 'pirate', '#ff7a1a', 30, 2.0, 0.32, 60, ['A demolitions rat. Lobs bombs', 'into crowds of guards.'])}
for _i, (_k, _nm, _rat, _col, _hp, _dmg, _sp, _price, _what) in HIRE.items():
    item(f'contract_{_k}', TOTEM, f'Hireling Contract: {_nm}', _col,
         ['Signed in the Fixer\'s den. Yours for good.'] + [(w, 'blue') for w in _what] +
         [('Use in the vault: they join you - and', 'blue'), ('come along to every heist after.', 'blue'), ('Sneak + use: send them off.', 'gray'),
          ('Hirelings never leave the vault.', 'dark_gray')],
         model='minecraft:paper', glint=True, stack=1, cat='misc', comps=hold('none'))
    HOLD[f'contract_{_k}'] = f'bm:p77/hire/use{_i}'
    P70.GOLDTOOTH_STOCK.append((_price, f'contract_{_k}', 1))
P72.KEEP += [f'contract_{v[0]}' for v in HIRE.values()]

# ---------------------------------------------------------------- the Pit's arena (39 x 20 x 39; entry door west, z 18-20)
AW, AH = 39, 20
AC = 19                                         # its controller at (19.5, 4, 19.5)
ASPOT = [(4, 4, 4), (34, 4, 4), (4, 4, 34), (34, 4, 34), (19, 4, 3), (19, 4, 35), (35, 4, 19), (27, 4, 12), (27, 4, 26)]
ACASH = (4, 4, 23)


def arena():
    b = Build(AW, AH, AW)
    b.fill(0, 0, 0, AW - 1, 2, AW - 1, BASE_C)
    b.room(0, 3, 0, AW - 1, AH - 1, AW - 1, R5.BASE['wall'], floor=R5.BASE['floor'], ceil=R5.BASE['ceil'])
    for r in (8, 14):                                       # rings of trim in the sand of the floor
        for x in range(AW):
            for z in range(AW):
                d = ((x - AC) ** 2 + (z - AC) ** 2) ** 0.5
                if abs(d - r) < 0.5: b.set(x, 3, z, R5.BASE['trim'])
    for y in range(4, 8):
        for z in (18, 19, 20): b.set(0, y, z, 'minecraft:air')
    for y in (4, 5, 6, 7, 8):
        b.set(0, y, 17, R5.BASE['metal']); b.set(0, y, 21, R5.BASE['metal'])
    for z in range(17, 22): b.set(0, 8, z, R5.BASE['metal'])
    for (px, pz) in ((9, 9), (27, 9), (9, 27), (27, 27)):    # four pillars to fight round
        for x in range(px, px + 3):
            for z in range(pz, pz + 3):
                for y in range(4, 11): b.set(x, y, z, R5.BASE['pillar'])
        b.set(px + 1, 11, pz + 1, R5.BASE['glow'])
    for (x1, z1, x2, z2) in ((17, 6, 21, 6), (17, 32, 21, 32), (32, 17, 32, 21)):   # low walls
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1): b.set(x, 4, z, R5.BASE['wall']); b.set(x, 5, z, R5.BASE['slab'] + '[type=bottom]')
    for (gx, gz) in ((19, 0), (19, AW - 1), (AW - 1, 19)):  # the gates the guards come through (barred, for the look of it)
        for y in range(4, 8):
            for d in (-1, 0, 1):
                if gz in (0, AW - 1): b.set(gx + d, y, gz, 'minecraft:iron_bars')
                else: b.set(gx, y, 19 + d, 'minecraft:iron_bars')
    for x in range(1, AW - 1):                              # a gallery round the top, where the rats watch
        for z in (1, 2, AW - 3, AW - 2): b.set(x, 11, z, R5.BASE['slab'] + '[type=top]')
    for z in range(3, AW - 3):
        for x in (1, 2, AW - 3, AW - 2): b.set(x, 11, z, R5.BASE['slab'] + '[type=top]')
    for x in range(4, AW - 3, 6):
        for z in (6, AW - 7):
            b.set(x, AH - 2, z, R5.BASE['chain']); b.set(x, AH - 3, z, R5.BASE['lantern'] + '[hanging=true]')
    for x in (8, 19, 30):
        for z in (0, AW - 1):
            if x != 19: b.set(x, 7, z, R5.BASE['glow'])
    cx, cy, cz = ACASH
    b.set(cx, cy, cz, 'minecraft:heavy_weighted_pressure_plate'); b.set(cx, cy - 1, cz, 'minecraft:emerald_block')
    b.marker(AC + 0.5, 4, AC + 0.5, ['bm.gvr', 'bm.gvr_arena', 'bm.gvnew'])
    return b


BASE_C = 'minecraft:blackstone'
P75.EXTRA_ROOMS['arena'] = arena
P75.SIZE['arena'] = (AW, AH, AW)


def ra(x, y, z):
    f = lambda v: '~' if v == 0 else f'~{v:g}'
    return f'{f(x - AC)} {f(y - 4)} {f(z - AC)}'


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = [T('[Heist] ', GOLD, bold=True)]
    rel = RM.rel
    tick, fast, second = [], [], []
    ident = [F(0), F(0), F(0), F(1)]
    objs = ['bm.gvhr', 'bm.gvhd', 'bm.gvhc', 'bm.gvmd', 'bm.gvxw', 'bm.gvll', 'bm.gvex']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + ['scoreboard players set #1000 bm.rng 1000', 'scoreboard players set #200000 bm.rng 200000',
                                                                                       'scoreboard players set #64000 bm.rng 64000']
    G.OBJECTIVES += objs
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    kit_arg = P72.kit_arg

    # ================================================================== KIT ABILITIES (consumed in a blink, handed straight back, cooldown shown)
    for r, (iid, nm, col, model, cd, lore) in ABIL.items():
        G.consume_adv(iid, f'bm:p77/kit/{iid}')
        fn(f'p77/kit/{iid}', [f'advancement revoke @s only bm:consume/{iid}',
                              f'execute unless items entity @s weapon.mainhand * run item replace entity @s weapon.mainhand with {kit_arg(iid)}',
                              f'execute unless items entity @s container.* *[minecraft:custom_data~{{bm:"{iid}"}}] unless items entity @s weapon.offhand * run item replace entity @s weapon.offhand with {kit_arg(iid)}',
                              f'execute unless items entity @s container.* *[minecraft:custom_data~{{bm:"{iid}"}}] unless items entity @s weapon.offhand *[minecraft:custom_data~{{bm:"{iid}"}}] run give @s {kit_arg(iid)}',
                              'execute unless entity @s[tag=bm.gvp] run return run ' + say('Its power sleeps outside the vault.'),
                              f'function bm:p77/kit/{iid}_go'])
    # the Bulwark Horn
    fn('p77/kit/kit_horn_go', ['playsound minecraft:item.goat_horn.sound.2 player @a[distance=..40] ~ ~ ~ 1 0.8', 'effect give @s minecraft:absorption 10 3 true',
                               'effect give @s minecraft:resistance 6 1 true', 'tag @s add bm.kself',
                               'effect give @a[tag=bm.gvp,distance=..8,tag=!bm.kself] minecraft:resistance 6 0 true', 'tag @s remove bm.kself',
                               'execute as @e[tag=bm.gvg,distance=..7] run effect give @s minecraft:slowness 4 2',
                               'execute as @e[tag=bm.gvg,distance=..7] run effect give @s minecraft:weakness 4 0',
                               'execute as @e[tag=bm.gvboss,distance=..7] run effect give @s minecraft:slowness 3 0',
                               'particle minecraft:gust_emitter_small ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:crit ~ ~1 ~ 3 0.4 3 0.3 60'])
    # the Shadowstep Charm: a probe walks ahead while there's room for you
    pass_tag = 'bm:kpass'
    wjson('bm/tags/block/kpass.json', {'values': ['#minecraft:replaceable', '#minecraft:wool_carpets', 'minecraft:moss_carpet', '#minecraft:pressure_plates',
                                                  'minecraft:light', 'minecraft:pink_petals', 'minecraft:leaf_litter', 'minecraft:firefly_bush', 'minecraft:lily_pad',
                                                  '#minecraft:buttons', 'minecraft:ladder', 'minecraft:vine', '#minecraft:rails', 'minecraft:redstone_wire']})
    fn('p77/kit/kit_step_go', ['particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 20', 'execute rotated ~ 0 run summon minecraft:marker ~ ~ ~ {Tags:["bm.kstep"]}',
                               'execute rotated ~ 0 as @e[type=minecraft:marker,tag=bm.kstep,limit=1,sort=nearest] run tp @s ~ ~ ~ ~ 0',
                               'scoreboard players set #st bm.rng 14', 'execute as @e[type=minecraft:marker,tag=bm.kstep,limit=1,sort=nearest] at @s run function bm:p77/kit/ray',
                               'execute at @e[type=minecraft:marker,tag=bm.kstep,limit=1,sort=nearest] run tp @s ~ ~ ~', 'kill @e[type=minecraft:marker,tag=bm.kstep]',
                               'effect give @s minecraft:invisibility 2 0 true', 'effect give @s minecraft:strength 4 1 true', 'effect give @s minecraft:speed 2 1 true',
                               'execute at @s run particle minecraft:portal ~ ~1 ~ 0.3 0.6 0.3 0.5 30', 'execute at @s run playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 0.8 1.4'])
    fn('p77/kit/ray', ['execute if score #st bm.rng matches ..0 run return 0',
                       f'execute unless block ^ ^ ^0.5 #{pass_tag} run return 0', f'execute unless block ^ ^1 ^0.5 #{pass_tag} run return 0',
                       f'execute if block ^ ^-1 ^0.5 #{pass_tag} if block ^ ^-2 ^0.5 #{pass_tag} run return 0',          # (no blinking off a ledge)
                       'tp @s ^ ^ ^0.5', 'scoreboard players remove #st bm.rng 1', 'execute at @s run function bm:p77/kit/ray'])
    # the Volley Quiver: five arrows, their motion found by a marker swung round the coat check's (always loaded) corner
    fn('p77/kit/kit_volley_go', [f'function bm:p77/kit/arrow {{a:{a}}}' for a in (-16, -8, 0, 8, 16)] + ['playsound minecraft:entity.arrow.shoot player @a[distance=..16] ~ ~ ~ 1 0.8'])
    fn('p77/kit/arrow', ['$execute in bm:gutter positioned -200.0 64.0 -200.0 rotated as @s rotated ~$(a) ~ run summon minecraft:marker ^ ^ ^2.6 {Tags:["bm.kvm"]}',
                         'execute in bm:gutter store result score #mx bm.rng run data get entity @e[type=minecraft:marker,tag=bm.kvm,limit=1] Pos[0] 1000',
                         'execute in bm:gutter store result score #my bm.rng run data get entity @e[type=minecraft:marker,tag=bm.kvm,limit=1] Pos[1] 1000',
                         'execute in bm:gutter store result score #mz bm.rng run data get entity @e[type=minecraft:marker,tag=bm.kvm,limit=1] Pos[2] 1000',
                         'execute in bm:gutter run kill @e[type=minecraft:marker,tag=bm.kvm]',
                         'scoreboard players operation #mx bm.rng += #200000 bm.rng', 'scoreboard players operation #my bm.rng -= #64000 bm.rng', 'scoreboard players operation #mz bm.rng += #200000 bm.rng',
                         'execute anchored eyes positioned ^ ^-0.1 ^0.8 run summon minecraft:arrow ~ ~ ~ {Tags:["bm.kva"],pickup:0b,damage:3.0d,crit:1b}',
                         'execute store result entity @e[type=minecraft:arrow,tag=bm.kva,limit=1,sort=nearest] Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                         'execute store result entity @e[type=minecraft:arrow,tag=bm.kva,limit=1,sort=nearest] Motion[1] double 0.001 run scoreboard players get #my bm.rng',
                         'execute store result entity @e[type=minecraft:arrow,tag=bm.kva,limit=1,sort=nearest] Motion[2] double 0.001 run scoreboard players get #mz bm.rng',
                         'data modify entity @e[type=minecraft:arrow,tag=bm.kva,limit=1,sort=nearest] Owner set from entity @s UUID',
                         'tag @e[type=minecraft:arrow,tag=bm.kva] remove bm.kva'])
    # the Tidal Ward
    bad = ['poison', 'wither', 'slowness', 'weakness', 'blindness', 'darkness', 'mining_fatigue', 'nausea']
    fn('p77/kit/kit_tidal_go', ['effect give @a[tag=bm.gvp,distance=..8] minecraft:instant_health 1 0 true', 'effect give @a[tag=bm.gvp,distance=..8] minecraft:regeneration 6 1 true',
                                'effect give @a[tag=bm.gvp,distance=..8] minecraft:absorption 10 1 true'] +
       [f'effect clear @a[tag=bm.gvp,distance=..8] minecraft:{e}' for e in bad] +
       ['tag @s add bm.kself', 'execute unless entity @a[tag=bm.gvp,tag=!bm.kself,distance=..8] run effect give @s minecraft:instant_health 1 1 true', 'tag @s remove bm.kself',
        'particle minecraft:splash ~ ~1 ~ 4 0.5 4 0.2 120', 'particle minecraft:bubble_pop ~ ~1 ~ 3 1 3 0.05 60',
        'playsound minecraft:block.conduit.activate player @a[distance=..20] ~ ~ ~ 1 1.4'])
    # passives: the tank's guard, the offense's bloodrush, the support's lifeline
    fast.append('effect give @a[tag=bm.gvp,scores={bm.gvrole=1,bm.sneak=1..}] minecraft:resistance 1 0 true')
    G.FUNCS['p75/kill_guard'].append('execute if score @s bm.gvrole matches 2 run function bm:p77/kit/bloodrush')
    fn('p77/kit/bloodrush', ['effect give @s minecraft:speed 4 1 true', 'effect give @s minecraft:regeneration 4 0 true', 'particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0 4'])
    second += ['scoreboard players remove @a[scores={bm.gvll=1..}] bm.gvll 1',
               'execute as @a[tag=bm.gvp,scores={bm.gvrole=4}] unless score @s bm.gvll matches 1.. if score @s bm.hp matches 1..6 at @s run function bm:p77/kit/lifeline']
    fn('p77/kit/lifeline', ['scoreboard players set @s bm.gvll 60', 'effect give @s minecraft:absorption 8 1 true', 'effect give @s minecraft:regeneration 4 1 true',
                            'particle minecraft:heart ~ ~1.8 ~ 0.4 0.3 0.4 0 6', 'playsound minecraft:block.conduit.ambient.short player @s ~ ~ ~ 1 1.6',
                            say('LIFELINE - the tide holds you up.', '#7ad0ea')])
    # the kit weapons' blows
    def hit_adv(name, iid, func, proj=False):
        dmg = {'type': {'is_direct': not proj, 'tags': [{'id': '#minecraft:is_projectile', 'expected': proj}]}}
        wjson(f'bm/advancement/p77/{name}.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {
            'player': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'mainhand': {'predicates': {
                'minecraft:custom_data': f'{{bm:"{iid}",bm_kit:1b}}'}}}}}], 'damage': dmg}}}, 'rewards': {'function': f'bm:{func}'}})
    hit_adv('kokiri', 'kokiri_sword', 'p77/kit/kokiri')
    fn('p77/kit/kokiri', ['advancement revoke @s only bm:p77/kokiri', 'execute at @s as @e[type=#bm:hostile,distance=..6,nbt={HurtTime:10s},sort=nearest,limit=1] run effect give @s minecraft:slowness 2 0'])
    hit_adv('cutlass', 'pirate_cutlass', 'p77/kit/cutlass')
    fn('p77/kit/cutlass', ['advancement revoke @s only bm:p77/cutlass', 'execute store result score #r bm.rng run random value 1..4', 'execute unless score #r bm.rng matches 1 run return 0',
                           'tag @s add bm.katk', 'execute at @s as @e[type=#bm:hostile,distance=..6,nbt={HurtTime:10s},sort=nearest,limit=1] at @s run function bm:p77/kit/gap', 'tag @s remove bm.katk'])
    fn('p77/kit/gap', ['damage @s 4 minecraft:player_attack by @a[tag=bm.katk,limit=1]', 'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.3 12',
                       'playsound minecraft:entity.player.attack.crit player @a[distance=..12] ~ ~ ~ 1 1.2'])
    hit_adv('fairy', 'fairy_bow', 'p77/kit/pin', proj=True)
    fn('p77/kit/pin', ['advancement revoke @s only bm:p77/fairy', 'execute at @s as @e[type=#bm:hostile,distance=..48,nbt={HurtTime:10s},sort=nearest,limit=1] run effect give @s minecraft:slowness 2 0'])

    # ================================================================== HIRELINGS
    for i, (k, nm, rat, col, hp, dmg, sp, price, what) in HIRE.items():
        host = {'Tags': ['bm.hire', f'bm.hire_{k}', 'bm.hnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'CustomName': T(nm, col, bold=True),
                'CustomNameVisible': B(0), 'Health': F(hp), 'DeathLootTable': 'minecraft:empty',
                'attributes': [{'id': 'minecraft:max_health', 'base': D(hp)}, {'id': 'minecraft:attack_damage', 'base': D(dmg)},
                               {'id': 'minecraft:movement_speed', 'base': D(sp)}, {'id': 'minecraft:follow_range', 'base': D(24)}] +
                              ([{'id': 'minecraft:knockback_resistance', 'base': D(0.6)}] if k == 'brawler' else []),
                'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}],
                'drop_chances': {s: F(0.0) for s in ('mainhand', 'head', 'chest', 'legs', 'feet', 'body')}}
        body = {'Tags': ['bm.hired', 'bm.hnew'], 'teleport_duration': Int(2), 'shadow_radius': F(0.3),
                'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:rat3d_{rat}'}},
                'item_display': 'fixed', 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(-0.55), F(0)], 'scale': [F(0.6)] * 3}}
        plate = {'Tags': ['bm.hired', 'bm.hnew'], 'billboard': 'center', 'view_range': F(0.25), 'default_background': B(0), 'background': Int(0x60000000),
                 'text': [T(nm, col, bold=True), T('\nHireling', 'gray')],
                 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.2), F(0)], 'scale': [F(0.45)] * 3}}
        fn(f'p77/hire/summon{i}', [f'summon minecraft:wolf ~ ~ ~ {snbt(host)}',
                                   'data modify entity @e[type=minecraft:wolf,tag=bm.hnew,limit=1,sort=nearest] Owner set from entity @s UUID',
                                   f'summon minecraft:item_display ~ ~ ~ {snbt(body)}', f'summon minecraft:text_display ~ ~ ~ {snbt(plate)}',
                                   'execute as @e[tag=bm.hired,tag=bm.hnew,distance=..2] run ride @s mount @e[type=minecraft:wolf,tag=bm.hnew,limit=1,sort=nearest]',
                                   'scoreboard players operation @e[tag=bm.hnew,distance=..3] bm.pid = @s bm.pid', 'scoreboard players set @e[type=minecraft:wolf,tag=bm.hnew,distance=..3] bm.gvx 0',
                                   'tag @e[tag=bm.hnew,distance=..3] remove bm.hnew', 'tag @s add bm.gvhon',
                                   'particle minecraft:poof ~ ~0.5 ~ 0.4 0.4 0.4 0.02 15', 'playsound minecraft:entity.villager.yes neutral @a[distance=..16] ~ ~ ~ 0.8 1.6',
                                   title('@s', 'actionbar', [T(nm, col, bold=True), T(' is with you.', 'gray')])])
        fn(f'p77/hire/use{i}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                                'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                                'execute if predicate bm:p20/sneaking run return run function bm:p77/hire/send_off',
                                f'scoreboard players set @s bm.gvhr {i}',
                                'execute unless dimension bm:gutter run return run ' + say(f'{nm} works the vault only - they\'ll meet you in the den next heist.', col),
                                'function bm:p77/hire/dismiss', 'scoreboard players set @s bm.gvhd 0', f'function bm:p77/hire/summon{i}'])
    fn('p77/hire/send_off', ['scoreboard players set @s bm.gvhr 0', 'function bm:p77/hire/dismiss', say('Your hireling goes off duty. (Use the contract to call them back.)')])
    fn('p77/hire/dismiss', ['scoreboard players operation #hp bm.rng = @s bm.pid', 'execute as @e[type=minecraft:wolf,tag=bm.hire] if score @s bm.pid = #hp bm.rng at @s run function bm:p77/hire/gone',
                            'tag @s remove bm.gvhon'])
    fn('p77/hire/gone', ['execute at @s run particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.02 10', 'execute on passengers run kill @s', 'tp @s ~ -300 ~', 'kill @s'])
    second += ['scoreboard players remove @a[scores={bm.gvhc=1..}] bm.gvhc 1', 'scoreboard players remove @a[scores={bm.gvhd=1..}] bm.gvhd 1',
               'execute as @a[tag=bm.gvp,scores={bm.gvhr=1..}] at @s if dimension bm:gutter run function bm:p77/hire/check',
               'execute as @e[type=minecraft:wolf,tag=bm.hire] at @s run function bm:p77/hire/sec',
               'execute as @e[tag=bm.hired] at @s unless entity @e[type=minecraft:wolf,tag=bm.hire,distance=..2.5] run kill @s']
    fn('p77/hire/check', ['scoreboard players operation #hp bm.rng = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                          'execute as @e[type=minecraft:wolf,tag=bm.hire] if score @s bm.pid = #hp bm.rng run scoreboard players set #has bm.rng 1',
                          'execute if score #has bm.rng matches 1 run return 0',
                          'execute if entity @s[tag=bm.gvhon] run return run function bm:p77/hire/downed',
                          'execute if score @s bm.gvhd matches 1.. run return 0', 'execute if entity @s[tag=bm.gvdead] run return 0'] +
       [f'execute if score @s bm.gvhr matches {i} run function bm:p77/hire/summon{i}' for i in HIRE])
    fn('p77/hire/downed', ['tag @s remove bm.gvhon', 'scoreboard players set @s bm.gvhd 45', say('Your hireling is knocked out - back in 45 seconds.', 'red')])
    # (each second, every hireling: no owner in the heist - gone; then its trade)
    fn('p77/hire/sec', ['execute unless dimension bm:gutter run return run function bm:p77/hire/gone', 'scoreboard players operation #hp bm.rng = @s bm.pid',
                        'scoreboard players set #has bm.rng 0', 'execute as @a[tag=bm.gvp] if score @s bm.pid = #hp bm.rng run scoreboard players set #has bm.rng 1',
                        'execute if score #has bm.rng matches 0 run return run function bm:p77/hire/gone', 'scoreboard players add @s bm.gvx 1'] +
       [f'execute if entity @s[tag=bm.hire_{k}] run return run function bm:p77/hire/{k}' for i, (k, *_r) in HIRE.items()])
    fn('p77/hire/brawler', ['effect give @s minecraft:resistance 2 0 true'])
    fn('p77/hire/medic', ['effect give @a[tag=bm.gvp,distance=..8] minecraft:regeneration 3 0 true', 'particle minecraft:happy_villager ~ ~0.8 ~ 2 0.4 2 0 3',
                          'execute if score @s bm.gvx matches 10.. as @a[tag=bm.gvp,distance=..10,scores={bm.hp=1..8},limit=1,sort=nearest] at @s run function bm:p77/hire/patch'])
    fn('p77/hire/patch', ['effect give @s minecraft:instant_health 1 0 true', 'particle minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 5',
                          'playsound minecraft:entity.villager.work_cleric neutral @a[distance=..16] ~ ~ ~ 1 1.4',
                          'scoreboard players set @e[type=minecraft:wolf,tag=bm.hire_medic,distance=..12,limit=1,sort=nearest] bm.gvx 0'])
    fn('p77/hire/pickpocket', ['execute as @e[type=minecraft:interaction,tag=bm.gvsec,distance=..14] at @s run particle minecraft:wax_on ~ ~0.5 ~ 0.3 0.3 0.3 0 4',
                               'execute if score @s bm.gvx matches 6.. if entity @e[tag=bm.gvg,distance=..5] run function bm:p77/hire/lift'])
    fn('p77/hire/lift', ['scoreboard players set @s bm.gvx 0', 'execute as @e[tag=bm.gvg,distance=..5,limit=1,sort=nearest] run effect give @s minecraft:weakness 3 0',
                         'execute as @a[tag=bm.gvp] if score @s bm.pid = #hp bm.rng run scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #c bm.rng 2',
                         inst('bm:p75/pot_add'), 'particle minecraft:wax_on ~ ~0.8 ~ 0.3 0.3 0.3 0 10', 'playsound minecraft:entity.experience_orb.pickup neutral @a[distance=..12] ~ ~ ~ 0.6 1.8'])
    fn('p77/hire/turret', ['execute if score @s bm.gvx matches ..1 run return 0', 'scoreboard players set @s bm.gvx 0', 'tag @s add bm.htme',
                           'execute as @e[tag=bm.gvg,distance=..14,sort=nearest,limit=1] at @s run function bm:p77/hire/zap', 'tag @s remove bm.htme'])
    fn('p77/hire/zap', ['damage @s 5 minecraft:magic by @e[type=minecraft:wolf,tag=bm.htme,limit=1]', 'effect give @s minecraft:slowness 1 0',
                        'execute facing entity @e[type=minecraft:wolf,tag=bm.htme,limit=1] eyes run function bm:p77/hire/beam',
                        'playsound minecraft:block.dispenser.launch neutral @a[distance=..16] ~ ~ ~ 0.8 1.6'])
    fn('p77/hire/beam', [f'particle minecraft:dust{{color:[1.0,0.8,0.25],scale:0.8}} ^ ^1 ^{d / 2} 0 0 0 0 1' for d in range(1, 28)])
    fn('p77/hire/boomer', ['execute if score @s bm.gvx matches ..4 run return 0', 'execute unless entity @e[tag=bm.gvg,distance=..10] run return 0', 'scoreboard players set @s bm.gvx 0',
                           'execute as @e[tag=bm.gvg,distance=..10,sort=nearest,limit=1] at @s run summon minecraft:marker ~ ~ ~ {Tags:["bm.hbomb"]}',
                           'playsound minecraft:entity.tnt.primed neutral @a[distance=..16] ~ ~ ~ 0.8 1.4'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.hbomb] at @s run function bm:p77/hire/fuse')
    fn('p77/hire/fuse', ['scoreboard players add @s bm.gvx 1', 'particle minecraft:smoke ~ ~0.3 ~ 0.1 0.1 0.1 0.01 2', 'execute if score @s bm.gvx matches 30.. run function bm:p77/hire/boom'])
    fn('p77/hire/boom', ['particle minecraft:explosion ~ ~0.5 ~ 0.6 0.3 0.6 0 4', 'playsound minecraft:entity.generic.explode neutral @a[distance=..24] ~ ~ ~ 0.8 1.3',
                         'execute as @e[tag=bm.gvg,distance=..3.5] run damage @s 7 minecraft:explosion', 'kill @s'])
    G.FUNCS['p70/unraid'] += ['function bm:p77/hire/dismiss']
    G.FUNCS['p75/after_fail'] += ['tag @s remove bm.gvhon', 'scoreboard players set @s bm.gvhd 0']
    G.FUNCS['admin/uninstall'][0:0] = ['execute as @e[type=minecraft:wolf,tag=bm.hire] at @s run function bm:p77/hire/gone']

    # ================================================================== THE ENDLESS VAULT AND THE PIT: picking them
    import phase28 as P28
    MENU = P28.MENU['heist']
    TIER_NAME, TIER_TITLE = P70.TIER_NAME, P70.TIER_TITLE
    tbtn = lambda t: P28.btn([T(f'Tier {TIER_NAME[t]}  ', GOLD, bold=True), T(TIER_TITLE[t], 'white')], 7600 + t,
                             tooltip=T(f'{t + 2} rooms, then the Vault. ' + ('' if t == 1 else f'(Clear Tier {TIER_NAME[t - 1]} to unlock.)'), 'gray'), width=300)
    dlg = P28.multi([T('Plan a Heist', GOLD, bold=True)],
                    [P28.body([T('Pick the job. ', 'gray'), T('Unlocked: up to Tier ', 'gray'), T('$(u)', GOLD, bold=True), T('.', 'gray')]),
                     P28.body([T('Your party (within 24 blocks) comes with you. Your market standing is never affected.', 'dark_gray')])],
                    [tbtn(t) for t in range(1, 6)] +
                    [P28.btn([T('THE ENDLESS VAULT  ', '#b080ff', bold=True), T('rooms without end', 'white')], 7606, width=300,
                             tooltip=T('Harder - and richer - every four rooms. Cash out in a Rats\' Rest. (Clear Tier I to unlock.)', 'gray')),
                     P28.btn([T('THE PIT  ', '#ff5a5a', bold=True), T('an arena of waves', 'white')], 7607, width=300,
                             tooltip=T('Survive wave after wave; a guardian every fifth. Cash out between waves. (Clear Tier I to unlock.)', 'gray'))],
                    columns=1, exit_label='Not tonight')
    G.FUNCS['p70/menu_show'] = [f'$dialog show @s {snbt(dlg)}']
    G.FUNCS['p28/act'].append('execute if score #act bm.pay matches 7606..7607 run return run function bm:p77/pick_mode')
    holds_plans = '*[minecraft:custom_data~{bm:"fixers_ledger"}]'      # (2.75: the Ledger plans heists now - the Heist Plans folded into it)
    fn('p77/pick_mode', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                         f'execute unless items entity @s container.* {holds_plans} unless items entity @s weapon.offhand {holds_plans} run return run function bm:p28/stale',
                         'execute unless score @s bm.gvu matches 2.. run return run ' + say('Clear Tier I first - then the Endless Vault and the Pit are open to you.', 'red'),
                         'execute if dimension bm:gutter run return 0',
                         'scoreboard players operation @s bm.gvpt = #act bm.pay', 'scoreboard players remove @s bm.gvpt 7600', 'function bm:p75/lives_menu'])
    pl = G.FUNCS['p75/pick_lives']
    pl[:] = [l.replace('bm.gvpt matches 1..5', 'bm.gvpt matches 1..7') for l in pl]
    k = pl.index('scoreboard players operation #t bm.rng = @s bm.gvpt')
    pl[k + 1:k + 1] = ['scoreboard players set #md bm.rng 0', 'execute if score #t bm.rng matches 6 run scoreboard players set #md bm.rng 2',
                       'execute if score #t bm.rng matches 6 run scoreboard players set #t bm.rng 1',
                       'execute if score #t bm.rng matches 7 run scoreboard players set #md bm.rng 1',
                       'execute if score #t bm.rng matches 7 run scoreboard players operation #t bm.rng = @s bm.gvu',
                       'execute if score #t bm.rng matches 6.. run scoreboard players set #t bm.rng 5']
    SL = P70.SLOTS
    for s in range(SL):
        z0 = P75.zoff(s)
        G.FUNCS[f'p70/s{s}/claim'].insert(0, f'scoreboard players operation #md{s} bm.gvmd = #md bm.rng')
        b = G.FUNCS[f'p70/s{s}/build']
        k = next(i for i, l in enumerate(b) if 'function bm:p75/lay/rooms' in l)
        cur = '@e[type=minecraft:marker,tag=bm.gvcur,tag=!bm.gvcurk,limit=1]'
        b[k:k + 1] = [f'execute if score #md{s} bm.gvmd matches 0 in bm:gutter as {cur} run function bm:p75/lay/rooms',
                      f'execute if score #md{s} bm.gvmd matches 1 in bm:gutter as {cur} at @s run function bm:p77/arena/lay',
                      f'execute if score #md{s} bm.gvmd matches 2 in bm:gutter as {cur} run function bm:p77/endless/lay{s}']
        b[:] = [l.replace('kill @e[type=minecraft:marker,tag=bm.gvcur]', 'kill @e[type=minecraft:marker,tag=bm.gvcur,tag=!bm.gvcurk]') for l in b]
        b.insert(0, f'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvcurk,scores={{bm.gvi={s + 1}}}] run kill @s')
        # (cleaning up: the Endless Vault reaches far east - wider kills, and its extra forceloads)
        for f_ in (f'p70/s{s}/clean', f'p75/s{s}/reset'):
            G.FUNCS[f_] = [l.replace(f'dx={P75.FL_X[1] - P75.FL_X[0] + 8},', 'dx=3000,') for l in G.FUNCS[f_]] + ([f'function bm:p77/endless/unload{s}'] if 'clean' in f_ else [])
        G.FUNCS[f'p75/s{s}/reset'].insert(0, f'function bm:p77/endless/unload{s}')
        fn(f'p77/endless/unload{s}', [f'execute in bm:gutter run forceload remove {x} {z0 - 32} {x + 255} {z0 + 48}' for x in range(P75.FL_X[1] + 1, 3000, 256)] +
           [f'scoreboard players set #ex{s} bm.gvex 0', f'scoreboard players set #pd{s} bm.gvex 0'])
    G.FUNCS['p70/inst_init'][-1:-1] = [f'execute if score @s bm.gvi matches {s + 1} run scoreboard players operation @s bm.gvmd = #md{s} bm.gvmd' for s in range(SL)] + \
        ['scoreboard players set @s bm.gvxw 0']
    # the haul: rooms or waves count as shares; no records, first-clear prizes or unlocks from the modes
    pay = G.FUNCS['p70/payout_inst']
    k = next(i for i, l in enumerate(pay) if l == 'scoreboard players operation #pot bm.rng = @s bm.gvpot')
    pay[k:k] = ['scoreboard players operation #sh bm.rng += @s bm.gvxw', 'scoreboard players operation #gmd bm.rng = @s bm.gvmd']
    pay[:] = [l.replace('function bm:p70/record', 'execute if score @s bm.gvmd matches 0 run function bm:p70/record') if l == 'function bm:p70/record' else l for l in pay]
    hl = G.FUNCS['p70/haul']
    hl[:] = [('execute if score #gmd bm.rng matches 0 ' + l[len('execute '):]) if (l.startswith('execute if score #q bm.rng matches 0 run function bm:p70/first_clear') or
                                                                                   l.startswith('execute if score #gt bm.rng >= @s bm.gvu')) else l for l in hl]
    # the sheet tells the mode
    sh = G.FUNCS['p70/sheet']
    k = next(i for i, l in enumerate(sh) if 'p75/sheet_tries' in l)
    sh.insert(k, inst('bm:p77/sheet_mode'))
    fn('p77/sheet_mode', ['execute if score @s bm.gvmd matches 1 run data modify storage bm:gv sheet append value {text:"\\nTHE PIT: survive the waves - cash out between them.\\n",color:"#ff5a5a",bold:true}',
                          'execute if score @s bm.gvmd matches 2 run data modify storage bm:gv sheet append value {text:"\\nTHE ENDLESS VAULT: harder every four rooms. Cash out in a Rats\' Rest.\\n",color:"#b080ff",bold:true}'])
    # (as a room: its heist's mode -> #md)
    fn('p77/mode', ['scoreboard players set #md bm.rng 0', 'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run scoreboard players operation #md bm.rng = @s bm.gvmd'])
    # leaving after a cash-out
    for s in range(SL):
        second.append(f'execute if score #out{s} bm.gvex matches 1.. run function bm:p77/out{s}')
        fn(f'p77/out{s}', [f'scoreboard players remove #out{s} bm.gvex 1',
                           f'execute if score #out{s} bm.gvex matches 0 as @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}] at @s run function bm:p70/leave'])
    fn('p77/cashed', [f'execute if score #gi bm.rng matches {s + 1} run scoreboard players set #out{s} bm.gvex 10' for s in range(SL)] +
       ['execute as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' + tellraw('@s', P + [T('Cashed out! ', GOLD, bold=True), T('The Fixer pulls the crew out in ten seconds.', 'gray')])])

    # ================================================================== THE ENDLESS VAULT
    for s in range(SL):
        z0 = P75.zoff(s)
        fn(f'p77/endless/lay{s}', ['scoreboard players set #q bm.rng 0', 'scoreboard players set #nev bm.rng 0', 'scoreboard players set #lk bm.rng 3', 'function bm:p75/lay/loop',
                                   'tag @s add bm.gvcurk', f'scoreboard players set @s bm.gvi {s + 1}',
                                   f'scoreboard players operation #eq{s} bm.gvex = #q bm.rng', f'scoreboard players set #eb{s} bm.gvex 3', f'scoreboard players set #ex{s} bm.gvex 0',
                                   f'scoreboard players set #pd{s} bm.gvex 0'])
        second.append(f'execute if score #ex{s} bm.gvex matches 1.. run function bm:p77/endless/s{s}/tick')
        fn(f'p77/endless/s{s}/tick', [f'scoreboard players remove #ex{s} bm.gvex 1', f'execute if score #ex{s} bm.gvex matches 0 run function bm:p77/endless/s{s}/extend',
                                     f'execute if score #ex{s} bm.gvex matches 0 if score #pd{s} bm.gvex matches 1.. run function bm:p77/endless/s{s}/load'])
        # (a room to build: load the ground ahead now, build it in two seconds - one at a time, however fast the crew is)
        fn(f'p77/endless/s{s}/ahead', [f'scoreboard players add #pd{s} bm.gvex 1', f'execute unless score #ex{s} bm.gvex matches 1.. run function bm:p77/endless/s{s}/load'])
        fn(f'p77/endless/s{s}/load', [f'execute in bm:gutter at @e[type=minecraft:marker,tag=bm.gvcurk,scores={{bm.gvi={s + 1}}},limit=1] run forceload add ~ {z0 - 32} ~80 {z0 + 48}',
                                     f'scoreboard players set #ex{s} bm.gvex 2'])
        fn(f'p77/endless/s{s}/extend', [f'scoreboard players set #gi bm.rng {s + 1}', f'scoreboard players set #z0 bm.rng {z0}', f'scoreboard players operation #q bm.rng = #eq{s} bm.gvex',
                                        'scoreboard players operation #gt bm.rng = #q bm.rng', 'scoreboard players operation #gt bm.rng /= #4 bm.rng', 'scoreboard players add #gt bm.rng 1',
                                        'execute if score #gt bm.rng matches 6.. run scoreboard players set #gt bm.rng 5',
                                        inst('bm:p77/endless/tier'),
                                        'scoreboard players set #pool bm.rng 0', 'scoreboard players set #nev bm.rng 1',
                                        f'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvcurk,scores={{bm.gvi={s + 1}}},limit=1] at @s run function bm:p77/endless/step',
                                        f'scoreboard players operation #eq{s} bm.gvex = #q bm.rng', f'scoreboard players add #eb{s} bm.gvex 1', f'scoreboard players remove #pd{s} bm.gvex 1',
                                        f'scoreboard players operation #gpl bm.rng = #np{s} bm.gvx',
                                        f'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr,scores={{bm.gvi={s + 1}}}] if score @s bm.gvq = #q bm.rng at @s run function bm:p70/r/init'])
    fn('p77/endless/tier', ['execute unless score @s bm.gvt = #gt bm.rng run function bm:p77/endless/deeper', 'scoreboard players operation @s bm.gvt = #gt bm.rng'])
    fn('p77/endless/deeper', ['function bm:p70/tag_mine', 'title @a[tag=bm.gvme] times 10 50 20',
                              'execute if score #gt bm.rng matches 2 run ' + title('@a[tag=bm.gvme]', 'title', T(TIER_TITLE[2], '#c8d0d8', bold=True)),
                              'execute if score #gt bm.rng matches 3 run ' + title('@a[tag=bm.gvme]', 'title', T(TIER_TITLE[3], GOLD, bold=True)),
                              'execute if score #gt bm.rng matches 4 run ' + title('@a[tag=bm.gvme]', 'title', T(TIER_TITLE[4], '#7ae8ff', bold=True)),
                              'execute if score #gt bm.rng matches 5 run ' + title('@a[tag=bm.gvme]', 'title', T(TIER_TITLE[5], GOLD, bold=True)),
                              title('@a[tag=bm.gvme]', 'subtitle', T('Deeper... harder, and richer', 'gray')), 'tag @a[tag=bm.gvme] remove bm.gvme'])
    fn('p77/endless/step', ['execute at @s run function bm:p75/lay/cn', 'scoreboard players operation #k bm.rng = #q bm.rng', 'scoreboard players add #k bm.rng 1',
                            'scoreboard players operation #k bm.rng %= #5 bm.rng',
                            'execute if score #k bm.rng matches 0 at @s run return run function bm:p77/endless/rest', 'execute at @s run function bm:p75/lay/room'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #5 bm.rng 5']
    fn('p77/endless/rest', ['scoreboard players add #q bm.rng 1', 'function bm:p75/pc/rest', 'execute as @e[type=minecraft:marker,tag=bm.gvnew] run function bm:p75/claim'])
    # (a room beaten in the Endless Vault: a room cleared; near the end of what's built, build on)
    G.FUNCS['p70/solved'].append('function bm:p77/endless/solved')
    fn('p77/endless/solved', ['function bm:p77/mode', 'execute unless score #md bm.rng matches 2 run return 0', 'scoreboard players operation #sq bm.rng = @s bm.gvq',
                              inst('bm:p77/endless/cleared')] +
       [f'execute if score #gi bm.rng matches {s + 1} run function bm:p77/endless/s{s}/more' for s in range(SL)])
    fn('p77/endless/cleared', ['scoreboard players add @s bm.gvxw 1'])
    for s in range(SL):
        fn(f'p77/endless/s{s}/more', [f'scoreboard players operation #lim bm.rng = #eb{s} bm.gvex', 'scoreboard players remove #lim bm.rng 2',
                                      'execute if score #sq bm.rng >= #lim bm.rng run function bm:p77/endless/s' + str(s) + '/ahead'])
    # the cash-out plate in each Rats' Rest
    G.FUNCS['p76/r/rest/init'] += ['function bm:p77/mode',
                                   'execute if score #md bm.rng matches 2 run summon minecraft:text_display ' + rel(12, 5.6, 21) + ' ' +
                                   snbt({'Tags': ['bm.gvprop'], 'billboard': 'center', 'brightness': {'block': 15, 'sky': 15}, 'background': Int(0x90000000 - 2 ** 32),
                                         'text': [T('CASH OUT\n', LUCKY, bold=True), T('the haul so far - or press on, deeper', 'gray')],
                                         'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0.5)] * 3}})]
    G.FUNCS['p76/r/rest/tick'] += [f'execute positioned {rel(12, 4, 21)} if entity @a[tag=bm.gvp,distance=..0.8] positioned as @s run function bm:p77/endless/cashout']
    fn('p77/endless/cashout', ['function bm:p77/mode', 'execute unless score #md bm.rng matches 2 run return 0', 'scoreboard players set #st bm.rng 0',
                               'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng store result score #st bm.rng run scoreboard players get @s bm.gvst',
                               'execute unless score #st bm.rng matches 2..3 run return 0', 'function bm:p70/payout', 'function bm:p77/cashed'])

    # ================================================================== THE PIT
    rat = lambda v, x, y, z, yaw: f'summon minecraft:item_display {ra(x, y, z)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvrat'], 'Rotation': [F(yaw), F(0)],
                                                                                        'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:rat3d_{v}'}},
                                                                                        'item_display': 'fixed', 'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                                                                    'translation': [F(0), F(0.5), F(0)], 'scale': [F(0.9)] * 3}})
    fn('p77/arena/lay', ['execute at @s run function bm:p75/cn/st', 'scoreboard players set #q bm.rng 1',
                         'execute at @s positioned ~ ~ ~-7 run function bm:p75/pc/arena', 'execute as @e[type=minecraft:marker,tag=bm.gvnew] run function bm:p75/claim'])
    G.FUNCS['p70/r/init'] += ['execute if entity @s[tag=bm.gvr_arena] run return run function bm:p77/arena/init']
    G.FUNCS['p70/r/tick'] += ['execute if entity @s[tag=bm.gvr_arena] run return run function bm:p77/arena/tick']
    fn('p77/arena/init', ['scoreboard players set @s bm.gvw 0', 'tag @s add bm.gvnopick',
                          f'summon minecraft:text_display {ra(2.5, 7.5, 19.5)} ' + snbt({'Tags': ['bm.gvprop'], 'billboard': 'vertical', 'background': Int(0x90000000 - 2 ** 32),
                                                                                       'text': [T('THE PIT\n', '#ff5a5a', bold=True), T('Survive the waves. Between them, the emerald plate cashes out.', 'gray')],
                                                                                       'line_width': Int(200), 'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                                                                   'translation': [F(0)] * 3, 'scale': [F(0.6)] * 3}}),
                          f'summon minecraft:text_display {ra(ACASH[0], 5.6, ACASH[2])} ' + snbt({'Tags': ['bm.gvprop'], 'billboard': 'center', 'brightness': {'block': 15, 'sky': 15},
                                                                                                'background': Int(0x90000000 - 2 ** 32), 'text': T('CASH OUT', LUCKY, bold=True),
                                                                                                'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                                                   'translation': [F(0)] * 3, 'scale': [F(0.5)] * 3}})] +
       [rat(v, x, 12, z, yaw) for v, x, z, yaw in (('pirate', 6, 1.5, 0), ('grey', 14, 1.5, 0), ('lucky', 24, 1.5, 0), ('chef', 32, 1.5, 0),
                                                    ('soldier', 8, 37.5, 180), ('prof', 20, 37.5, 180), ('merc', 30, 37.5, 180), ('teller', 37.5, 12, 90), ('madame', 37.5, 26, 90))])
    fn('p77/arena/tick', ['scoreboard players set @a[tag=bm.gvp,distance=..26] bm.gvmz 9',
                          'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..14] run function bm:p77/arena/open',
                          'execute if score @s bm.gvs matches 1 run function bm:p77/arena/between', 'execute if score @s bm.gvs matches 2 run function bm:p77/arena/fight',
                          f'execute if score @s bm.gvs matches 3 positioned {ra(*ACASH)} as @a[tag=bm.gvp,distance=..0.8] at @s run function bm:p70/leave'])
    fn('p77/arena/open', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0', 'scoreboard players set @s bm.gvw 0',
                          'title @a[tag=bm.gvp,distance=..30] times 10 50 15', title('@a[tag=bm.gvp,distance=..30]', 'title', T('THE PIT', '#ff5a5a', bold=True)),
                          title('@a[tag=bm.gvp,distance=..30]', 'subtitle', T('The crowd roars. Here they come...', 'gray')),
                          'playsound minecraft:entity.ravager.roar hostile @a[distance=..40] ~ ~ ~ 1 0.6'])
    fn('p77/arena/between', ['scoreboard players set #len bm.rng 240', 'execute if score @s bm.gvw matches 0 run scoreboard players set #len bm.rng 100',
                             'scoreboard players operation #left bm.rng = #len bm.rng', 'scoreboard players operation #left bm.rng -= @s bm.gvtm',
                             'scoreboard players operation #q bm.rng = #left bm.rng', 'scoreboard players operation #q bm.rng %= #20 bm.rng',
                             'scoreboard players operation #sec bm.rng = #left bm.rng', 'scoreboard players operation #sec bm.rng /= #20 bm.rng',
                             'execute if score #q bm.rng matches 0 as @a[tag=bm.gvp,distance=..30] run ' + title('@s', 'actionbar', [T('Next wave in ', '#ff5a5a'), {'score': {'name': '#sec', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                                                                                                       T(' s', '#ff5a5a')]),
                             f'execute if score @s bm.gvw matches 1.. positioned {ra(*ACASH)} if entity @a[tag=bm.gvp,distance=..0.8] positioned as @s run return run function bm:p77/arena/cashout',
                             'execute if score #left bm.rng matches ..0 run function bm:p77/arena/wave'])
    fn('p77/arena/wave', ['scoreboard players set @s bm.gvs 2', 'scoreboard players add @s bm.gvw 1', 'scoreboard players set @s bm.gvtm 0', 'function bm:p70/ctx',
                          'scoreboard players operation #q bm.rng = @s bm.gvw', 'scoreboard players remove #q bm.rng 1', 'scoreboard players operation #q bm.rng /= #3 bm.rng',
                          'scoreboard players operation #gt bm.rng += #q bm.rng', 'execute if score #gt bm.rng matches 6.. run scoreboard players set #gt bm.rng 5',
                          'execute store result score #n bm.rng if entity @a[tag=bm.gvp,distance=..40]', 'scoreboard players operation #n bm.rng += @s bm.gvw', 'scoreboard players add #n bm.rng 2',
                          'execute if score #n bm.rng matches 13.. run scoreboard players set #n bm.rng 12',
                          'scoreboard players operation #q bm.rng = @s bm.gvw', 'scoreboard players operation #q bm.rng %= #5 bm.rng',
                          'execute if score #q bm.rng matches 0 run function bm:p77/arena/boss', 'execute if score #q bm.rng matches 0 run scoreboard players set #n bm.rng 3',
                          'scoreboard players set #i bm.rng 0', 'function bm:p77/arena/spawn',
                          'title @a[tag=bm.gvp,distance=..40] times 5 30 10',
                          title('@a[tag=bm.gvp,distance=..40]', 'title', [T('WAVE ', '#ff5a5a', bold=True), {'score': {'name': '@s', 'objective': 'bm.gvw'}, 'color': 'white', 'bold': True}]),
                          'playsound minecraft:event.raid.horn hostile @a[distance=..60] ~ ~ ~ 0.8 1.1'])
    fn('p77/arena/spawn', ['execute if score #i bm.rng >= #n bm.rng run return 0', f'execute store result score #k bm.rng run random value 0..{len(ASPOT) - 1}'] +
       [f'execute if score #k bm.rng matches {j} positioned {ra(*p)} run function bm:p70/guard' for j, p in enumerate(ASPOT)] +
       ['scoreboard players add #i bm.rng 1', 'function bm:p77/arena/spawn'])
    fn('p77/arena/boss', [f'execute positioned {ra(AC, 4, AC + 8)} run function bm:p75/boss_tier', 'execute as @e[tag=bm.gvbnew,limit=1] run function bm:p70/boss/setup',
                          'tag @e[tag=bm.gvbnew] add bm.gvnoshell', 'tag @e[tag=bm.gvbnew] remove bm.gvbnew',
                          'particle minecraft:explosion_emitter ' + ra(AC, 5, AC + 8) + ' 0 0 0 0 1'])
    G.FUNCS['p70/boss/sec'] = [l.replace('execute if score @s bm.gvc matches 0 if score #hp', 'execute unless entity @s[tag=bm.gvnoshell] if score @s bm.gvc matches 0 if score #hp')
                               .replace('execute if score @s bm.gvc matches 2 if score #hp', 'execute unless entity @s[tag=bm.gvnoshell] if score @s bm.gvc matches 2 if score #hp')
                               for l in G.FUNCS['p70/boss/sec']]
    fn('p77/arena/fight', ['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng', 'execute unless score #q bm.rng matches 0 run return 0',
                           'execute if entity @e[tag=bm.gvg,distance=..34] run return 0', 'execute if entity @e[tag=bm.gvboss,distance=..34] run return 0',
                           'scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0',
                           inst('bm:p77/arena/survived'), 'scoreboard players operation #c bm.rng = @s bm.gvw', 'scoreboard players operation #c bm.rng *= #3 bm.rng', inst('bm:p75/pot_add')] +
       [f'execute if score #gi bm.rng matches {s + 1} run bossbar set bm:gvb{s} players' for s in range(SL)] +
       ['execute as @a[tag=bm.gvp,distance=..40] run ' + tellraw('@s', P + [T('Wave ', '#ff5a5a'), {'score': {'name': '@e[type=minecraft:marker,tag=bm.gvr_arena,limit=1,sort=nearest]', 'objective': 'bm.gvw'}, 'color': 'white', 'bold': True},
                                                                         T(' cleared! ', '#ff5a5a', bold=True), T('Cash out on the emerald plate - or stand fast for the next.', 'gray')]),
        'playsound minecraft:ui.toast.challenge_complete block @a[distance=..40] ~ ~ ~ 0.8 1.2'])
    fn('p77/arena/survived', ['scoreboard players add @s bm.gvxw 1'])
    fn('p77/arena/cashout', ['function bm:p70/payout', 'function bm:p77/cashed'])

    # ================================================================== admin
    fn('admin/hirelings', [give(f'contract_{v[0]}') for v in HIRE.values()])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s_ = G.FUNCS['loop/second']
    s_[-1:-1] = second


def extend_offers(O, offer):
    pass


def rp(R):
    pass

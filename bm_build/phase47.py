"""Phase 2.26: more Blood Moon goods.

- MOON PACT (6 Crystals): sign it under a Blood Moon. Until dawn, every horror you slay drops double Crystals - but you take
  half again as much damage from everything. It can't be torn up.
- THIRSTING BLADE (24 Crystals): a sword that drinks. Each kill you make with it under a Blood Moon adds +1 attack damage
  (up to +6). The thirst fades at dawn.
- VAMPIRE'S MIRROR (12 Crystals): use it to mark where you stand; use it again within 60 seconds to step back through the glass
  to that spot (any dimension). 30-second cooldown. It won't work in dungeons or the Market.
- CRIMSON HOURGLASS (10 Crystals): turn it under a Blood Moon and the moon stands still for 2 minutes. Once a moon.
- MUSIC DISC - BLOOD MOON: an original track. 1 in 4 riders of Blood Moon steeds drop it."""
from items import item, T, TOTEM, consumable
from useitem import hold, HOLD

SONG_SECONDS = 97
HOURGLASS = 120                  # seconds the moon stands still
THIRST_MAX = 6
MIRROR_WINDOW, MIRROR_CD = 60, 30
BLADE = 'minecraft:diamond_sword'

item('moon_pact', TOTEM, 'Moon Pact', '#c42a2e',
     ['A contract signed in something red.', ('Sign it under a Blood Moon. Until dawn:', 'blue'), ('  horrors you slay drop double Crystals,', 'blue'),
      ('  but you take 50% more damage.', 'red'), ('It cannot be torn up.', 'dark_gray')],
     model='bm:moon_pact', stack=16, cat='blood',
     comps={'minecraft:consumable': consumable(1.2, 'none', 'minecraft:item.book.page_turn', False)})
item('thirsting_blade', BLADE, 'Thirsting Blade', '#e8504a',
     ['The edge is never quite dry.', ('Under a Blood Moon, every kill with it', 'blue'), (f'adds +1 attack damage (up to +{THIRST_MAX}).', 'blue'),
      ('The thirst fades at dawn.', 'dark_gray')],
     model='bm:thirsting_blade', stack=1, cat='blood')
item('vampire_mirror', TOTEM, "Vampire's Mirror", '#9a3a4a',
     ['It shows the room, but never you.', ('Use: mark where you stand.', 'blue'), (f'Use again within {MIRROR_WINDOW}s: step back to the mark.', 'blue'),
      (f'{MIRROR_CD}s cooldown. Not in dungeons or the Market.', 'dark_gray')],
     model='bm:vampire_mirror', stack=1, cat='blood', comps=hold('none'))
HOLD['vampire_mirror'] = 'bm:p47/mirror/use'
item('crimson_hourglass', TOTEM, 'Crimson Hourglass', '#c8a040',
     ['The sand inside is red, and runs upward.', ('Turn it under a Blood Moon:', 'blue'), (f'the moon stands still for {HOURGLASS // 60} minutes.', 'blue'),
      ('Once a moon. Everyone will notice.', 'dark_gray')],
     model='bm:crimson_hourglass', stack=4, cat='blood',
     comps={'minecraft:consumable': consumable(1.0, 'none', 'minecraft:block.sand.fall', False)})
item('music_disc_blood_moon', 'minecraft:music_disc_13', 'Music Disc', 'aqua',
     [('Dropped by the riders of Blood Moon steeds.', 'gray')],
     model='bm:music_disc_blood_moon', stack=1, cat='blood', comps={'minecraft:jukebox_playable': 'bm:blood_moon'})


def extend_offers(O, offer):
    O['blood'] += [offer(('blood_crystal', 6), ('moon_pact', 1)), offer(('blood_crystal', 24), ('thirsting_blade', 1)),
                   offer(('blood_crystal', 12), ('vampire_mirror', 1)), offer(('blood_crystal', 10), ('crimson_hourglass', 1))]


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    objs = ['bm.pdmg minecraft.custom:minecraft.damage_taken', 'bm.pq dummy', 'bm.thirst dummy', 'bm.mirt dummy', 'bm.mircd dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    denies = {}
    def refuse(iid, msg):
        name = f'p47/deny/{iid}_{len(denies.setdefault(iid, []))}'
        denies[iid].append(name)
        fn(name, [give(iid), say(msg + ' (Refunded)')])
        return f'return run function bm:{name}'
    held = lambda iid, slot='weapon.mainhand': f'items entity @s {slot} *[minecraft:custom_data~{{bm:"{iid}"}}]'
    blood_kill = lambda name, func: wjson(f'bm/advancement/p47/{name}.json', {
        'criteria': {'slain': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
            {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': func}]}}},
        'rewards': {'function': f'bm:p47/{name}'}})

    # ------------------------------------------------------------------ MOON PACT
    G.consume_adv('moon_pact', 'bm:p47/pact')
    fn('p47/pact', ['advancement revoke @s only bm:consume/moon_pact',
                    'execute unless score #active bm.bm matches 1 run ' + refuse('moon_pact', 'A pact needs a Blood Moon overhead.'),
                    'execute if entity @s[tag=bm.pact] run ' + refuse('moon_pact', 'You are already bound by a pact tonight.'),
                    'tag @s add bm.pact', 'scoreboard players set @s bm.pdmg 0', 'scoreboard players set @s bm.pq 0',
                    tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'red'}, T(' signed a ', 'gray'), T('Moon Pact', '#c42a2e', bold=True),
                                            T('. Double Crystals until dawn - and every wound cuts deeper.', 'gray')]),
                    'particle minecraft:dust{color:[0.75,0.05,0.08],scale:1.6} ~ ~1 ~ 0.4 0.7 0.4 0 40',
                    'playsound minecraft:entity.wither.ambient player @s ~ ~ ~ 0.6 1.4', 'playsound minecraft:item.book.put player @s ~ ~ ~ 1 0.6'])
    blood_kill('pact_kill', {'minecraft:nbt': '{Tags:["bm.blood"]}'})
    fn('p47/pact_kill', ['advancement revoke @s only bm:p47/pact_kill', 'execute unless entity @s[tag=bm.pact] run return 0',
                         'execute store result score #r bm.rng run random value 1..2',
                         'execute if score #r bm.rng matches 1 run ' + give('blood_crystal', 1),
                         'execute if score #r bm.rng matches 2 run ' + give('blood_crystal', 2),
                         'particle minecraft:dust{color:[0.75,0.05,0.08],scale:1.2} ~ ~1 ~ 0.3 0.5 0.3 0 10'])
    # every wound cuts deeper: half as much again of whatever was taken. It lands once the hit's invulnerability frames are over
    # (HurtTime back to 0), or it would be swallowed by them; blood_drain bypasses armour, so it's exactly +50%.
    tick += ['execute as @a[tag=bm.pact,scores={bm.pdmg=1..}] run function bm:p47/pact_owe',
             'execute as @a[tag=bm.pact,scores={bm.pq=1..}] if data entity @s {HurtTime:0s} run function bm:p47/pact_hurt']
    fn('p47/pact_hurt', ['execute store result storage bm:tmp pact.d float 0.05 run scoreboard players get @s bm.pq',
                         'scoreboard players set @s bm.pq 0', 'function bm:p47/pact_dmg with storage bm:tmp pact', 'scoreboard players set @s bm.pdmg 0'])
    fn('p47/pact_owe', ['scoreboard players operation @s bm.pq += @s bm.pdmg', 'scoreboard players set @s bm.pdmg 0'])
    fn('p47/pact_dmg', ['$damage @s $(d) bm:blood_drain'])
    second.append('execute unless score #active bm.bm matches 1 run tag @a[tag=bm.pact] remove bm.pact')

    # ------------------------------------------------------------------ THIRSTING BLADE
    blood_kill('thirst_kill', {'minecraft:entity_type': '#bm:hostile'})
    fn('p47/thirst_kill', ['advancement revoke @s only bm:p47/thirst_kill', 'execute unless score #active bm.bm matches 1 run return 0',
                           f'execute unless {held("thirsting_blade")} run return 0',
                           f'execute if score @s bm.thirst matches {THIRST_MAX}.. run return run ' + say(f'The blade is sated: +{THIRST_MAX} damage until dawn.', '#e8504a'),
                           'scoreboard players add @s bm.thirst 1',
                           title('@s', 'actionbar', [T('The blade drinks.  ', '#e8504a'), T('+', 'red'), {'score': {'name': '@s', 'objective': 'bm.thirst'}, 'color': 'red'},
                                                     T(' damage', 'red')]),
                           'execute at @s run particle minecraft:dust{color:[0.8,0.05,0.1],scale:1.2} ~ ~1.2 ~ 0.3 0.4 0.3 0 12',
                           'execute at @s run playsound minecraft:entity.generic.drink player @s ~ ~ ~ 0.6 0.6'])
    # the bonus lives on the player only while the blade is in hand, the moon is up and the thirst is there
    fast.append(f'execute as @a if {held("thirsting_blade")} run tag @s add bm.thirsty')
    fast.append('execute as @a[tag=bm.thirsty] run function bm:p47/thirst_apply')
    fn('p47/thirst_apply', ['attribute @s minecraft:attack_damage modifier remove bm:thirst',
                            'execute unless score #active bm.bm matches 1 run return run tag @s remove bm.thirsty',
                            'execute unless score @s bm.thirst matches 1.. run return run tag @s remove bm.thirsty',
                            f'execute unless {held("thirsting_blade")} run return run tag @s remove bm.thirsty',
                            'execute store result storage bm:tmp thirst.v int 1 run scoreboard players get @s bm.thirst',
                            'function bm:p47/thirst_set with storage bm:tmp thirst'])
    fn('p47/thirst_set', ['$attribute @s minecraft:attack_damage modifier add bm:thirst $(v) add_value'])

    # ------------------------------------------------------------------ VAMPIRE'S MIRROR
    fn('p47/mirror/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                          'execute store result storage bm:tmp mir.pid int 1 run scoreboard players get @s bm.pid',
                          'execute if score @s bm.mircd matches 1.. run return run ' + say('The glass is still clouded. Give it a moment.'),
                          'execute unless function bm:p37/allowed run return run ' + say('The mirror shows only darkness here.'),
                          'execute if entity @s[tag=bm.mirset] run return run function bm:p47/mirror/back',
                          'function bm:p47/mirror/mark'])
    fn('p47/mirror/mark', ['function bm:p47/mirror/save with storage bm:tmp mir',
                           'tag @s add bm.mirset', f'scoreboard players set @s bm.mirt {MIRROR_WINDOW}',
                           'summon minecraft:marker ~ ~ ~ {Tags:["bm.mirmark","bm.mirnew"]}',
                           'scoreboard players operation @e[type=minecraft:marker,tag=bm.mirnew] bm.pid = @s bm.pid', 'tag @e[type=minecraft:marker,tag=bm.mirnew] remove bm.mirnew',
                           'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.8 0.3 0.02 40', 'playsound minecraft:block.glass.hit player @s ~ ~ ~ 1 1.6',
                           say(f'Your reflection stays behind. Use the mirror within {MIRROR_WINDOW}s to return to it.', '#c06070')])
    fn('p47/mirror/save', ['$data modify storage bm:mirror p$(pid) set value {}',
                           '$data modify storage bm:mirror p$(pid).x set from entity @s Pos[0]', '$data modify storage bm:mirror p$(pid).y set from entity @s Pos[1]',
                           '$data modify storage bm:mirror p$(pid).z set from entity @s Pos[2]', '$data modify storage bm:mirror p$(pid).yaw set from entity @s Rotation[0]',
                           '$data modify storage bm:mirror p$(pid).pitch set from entity @s Rotation[1]', '$data modify storage bm:mirror p$(pid).d set from entity @s Dimension'])
    fn('p47/mirror/back', ['particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.8 0.3 0.05 50', 'particle minecraft:dust{color:[0.6,0.05,0.12],scale:1.4} ~ ~1 ~ 0.3 0.7 0.3 0 20',
                           'playsound minecraft:block.glass.break player @a[distance=..16] ~ ~ ~ 0.8 1.4',
                           'function bm:p47/mirror/load with storage bm:tmp mir', 'function bm:p47/mirror/tp with storage bm:tmp mtp',
                           'execute at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.8 0.3 0.05 50',
                           'execute at @s run playsound minecraft:entity.illusioner.mirror_move player @a[distance=..16] ~ ~ ~ 1 1',
                           'function bm:p47/mirror/clear', f'scoreboard players set @s bm.mircd {MIRROR_CD}',
                           say('You step back through the glass.', '#c06070')])
    fn('p47/mirror/load', ['$data modify storage bm:tmp mtp set from storage bm:mirror p$(pid)'])
    fn('p47/mirror/tp', ['$execute in $(d) run tp @s $(x) $(y) $(z) $(yaw) $(pitch)'])
    fn('p47/mirror/clear', ['tag @s remove bm.mirset', 'scoreboard players set @s bm.mirt 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                            'execute as @e[type=minecraft:marker,tag=bm.mirmark] if score @s bm.pid = #me bm.pid run kill @s'])
    fn('p47/mirror/expire', ['function bm:p47/mirror/clear', say('Your reflection fades from the glass.', 'gray'),
                             'playsound minecraft:block.glass.step player @s ~ ~ ~ 1 0.6'])
    second += ['scoreboard players remove @a[tag=bm.mirset] bm.mirt 1', 'execute as @a[tag=bm.mirset,scores={bm.mirt=..0}] at @s run function bm:p47/mirror/expire',
               'scoreboard players remove @a[scores={bm.mircd=1..}] bm.mircd 1',
               'execute as @e[type=minecraft:marker,tag=bm.mirmark] at @s run particle minecraft:dust{color:[0.6,0.05,0.12],scale:1.0} ~ ~1 ~ 0.2 0.6 0.2 0 6']

    # ------------------------------------------------------------------ CRIMSON HOURGLASS: the overworld clock stops for 2 minutes
    G.consume_adv('crimson_hourglass', 'bm:p47/hourglass')
    fn('p47/hourglass', ['advancement revoke @s only bm:consume/crimson_hourglass',
                         'execute unless score #active bm.bm matches 1 run ' + refuse('crimson_hourglass', 'The sand will only run under a Blood Moon.'),
                         'execute if score #hg bm.bm matches 1 run ' + refuse('crimson_hourglass', 'Tonight\'s moon has already been held once.'),
                         'scoreboard players set #hg bm.bm 1', f'scoreboard players set #hgt bm.bm {HOURGLASS}',
                         'time of minecraft:overworld pause',
                         tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'red'}, T(' turned a ', 'gray'), T('Crimson Hourglass', '#c8a040', bold=True),
                                                 T(f'. The Blood Moon stands still for {HOURGLASS // 60} minutes!', 'red')]),
                         'execute as @a at @s run playsound minecraft:block.bell.resonate ambient @s ~ ~ ~ 0.8 0.5',
                         'particle minecraft:falling_dust{block_state:"minecraft:red_sand"} ~ ~2 ~ 0.4 0.3 0.4 0 30'])
    second.append('execute if score #hgt bm.bm matches 1.. run function bm:p47/hg_tick')
    fn('p47/hg_tick', ['scoreboard players remove #hgt bm.bm 1',
                       'execute if score #hgt bm.bm matches 10 run ' + tellraw('@a', PREFIX + [T('The red sand is nearly spent...', 'gray', italic=True)]),
                       'execute if score #hgt bm.bm matches ..0 run function bm:p47/hg_done'])
    fn('p47/hg_done', ['time of minecraft:overworld resume', 'scoreboard players set #hgt bm.bm 0',
                       tellraw('@a', PREFIX + [T('The hourglass runs dry. The moon moves on.', 'gray')]),
                       'execute as @a at @s run playsound minecraft:block.bell.use ambient @s ~ ~ ~ 0.6 0.5'])
    G.FUNCS['bloodmoon/start'].append('scoreboard players set #hg bm.bm 0')

    # ------------------------------------------------------------------ MUSIC DISC: riders of Blood Moon steeds (1 in 4)
    wjson('bm/jukebox_song/blood_moon.json', {'sound_event': {'sound_id': 'bm:music_disc.blood_moon'}, 'description': T('Black Market - Blood Moon', 'gray'),
                                              'length_in_seconds': float(SONG_SECONDS), 'comparator_output': 15})
    for m in ('blood_skeleton_horse', 'blood_zombie_horse'):
        G.FUNCS[f'mounts/{m}'].append('tag @s add bm.bmrider')             # (only reached when the steed was summoned)
    blood_kill('disc_kill', {'minecraft:nbt': '{Tags:["bm.bmrider"]}'})
    fn('p47/disc_kill', ['advancement revoke @s only bm:p47/disc_kill', 'execute store result score #r bm.rng run random value 1..4',
                         'execute unless score #r bm.rng matches 1 run return 0', give('music_disc_blood_moon'),
                         say('The rider drops a record, still warm.', '#e8504a'), 'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 1 0.8'])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack
def icons():
    import vanilla as v
    from PIL import Image
    V, hx, ramp = v.V, v._hex, v.ramp
    BL = [hx(h) for h in v.BLOOD]

    def thirsting_blade():
        im = v._load(V + 'iron_sword.png')
        steel = lambda c: v._hsv(c)[1] < 0.2
        return v.recolor_where(im, steel, [hx(h) for h in ('#2a0508', '#5a0c14', '#8a1420', '#b82a30', '#e05048', '#ff8a7a', '#ffc8b8')])

    def moon_pact():
        im = v._load(V + 'paper.png')
        ink = hx('#5a3a2a')
        px = im.load()
        for y in range(16):
            for x in range(16):
                if px[x, y][3] and y in (6, 8) and 4 <= x <= 10 and px[x, y][0] > 200: px[x, y] = ink
        for (x, y), c in {(9, 10): BL[3], (10, 10): BL[4], (11, 10): BL[3], (9, 11): BL[2], (10, 11): BL[3], (11, 11): BL[2], (10, 12): BL[2],
                          (10, 9): BL[4], (9, 10): BL[4]}.items():
            im.putpixel((x, y), c)                                     # a red wax seal with a drip
        im.putpixel((10, 10), hx('#ff8a7a'))
        return im

    def crimson_hourglass():
        g = ramp('#c8a040', 5, 2); w = ramp('#5a2a14', 4, 1); gl = hx('#e8eef4'); gs = hx('#b8c4d0'); s = [hx(h) for h in ('#6e1018', '#a82024', '#d84034')]
        rows = ['................', '...KGGGGGGGGK...', '...KWWWWWWWWK...', '....KgRRRRgK....', '....KgRRRRgK....', '.....KgRRgK.....',
                '......KgRK......', '.......KK.......', '......KgsK......', '.....Kg.sgK.....', '....Kg..s.gK....', '....KgsRsRgK....',
                '....KRRRRRRK....', '...KWWWWWWWWK...', '...KGGGGGGGGK...', '................']
        pal = {'K': w[0], 'G': g[3], 'W': w[2], 'g': gl, 'R': s[1], 's': s[2]}
        im = Image.new('RGBA', (16, 16))
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                if ch != '.': im.putpixel((x, y), pal[ch])
        for x in range(4, 12): im.putpixel((x, 1), g[4] if x < 8 else g[3]); im.putpixel((x, 14), g[2])
        for y in (3, 4, 9, 10): im.putpixel((5 if y < 6 else 5, y), gl)
        im.putpixel((10, 3), gs); im.putpixel((10, 4), gs)
        im.putpixel((5, 3), s[2]); im.putpixel((6, 3), s[2])
        for x in (3, 12): im.putpixel((x, 1), w[0]); im.putpixel((x, 14), w[0])
        return im

    def vampire_mirror():
        fr = ramp('#7a1a24', 5, 2); gold = ramp('#c89a2a', 4, 2); gl = ramp('#8aa0b8', 4, 2); dk = hx('#1a0608')
        im = Image.new('RGBA', (16, 16))
        for y in range(16):
            for x in range(16):
                dx, dy = (x - 9.5) / 4.6, (y - 5.5) / 5.4
                r = (dx * dx + dy * dy) ** 0.5; lit = -(dx + dy)
                if r <= 1.0:
                    if r > 0.78: im.putpixel((x, y), fr[min(4, max(1, round(2 + lit * 1.4)))])
                    else: im.putpixel((x, y), gl[min(3, max(0, round(1.4 + lit * 1.2)))])
                elif r <= 1.2: im.putpixel((x, y), dk)
        for (x, y) in ((8, 3), (8, 4), (9, 3), (7, 5)): im.putpixel((x, y), hx('#eef4fa'))      # a glint
        handle = [(7, 11), (6, 12), (5, 13), (4, 14), (3, 15)]
        for i, (x, y) in enumerate(handle):
            im.putpixel((x, y), gold[2] if i % 2 == 0 else gold[1])
            for ox, oy in ((-1, 0), (0, 1)):
                if 0 <= x + ox < 16 and 0 <= y + oy < 16 and im.getpixel((x + ox, y + oy))[3] == 0: im.putpixel((x + ox, y + oy), dk)
            if x + 1 < 16 and im.getpixel((x + 1, y))[3] == 0: im.putpixel((x + 1, y), dk)
        im.putpixel((8, 10), gold[3]); im.putpixel((7, 10), gold[2])
        return im

    def disc():
        im = v._load(V + 'music_disc_13.png')
        lab = lambda c: v._hsv(c)[1] > 0.45
        return v.recolor_where(im, lab, [hx(h) for h in ('#6e1018', '#c42a2e', '#ff5a4a')])

    return {'thirsting_blade': thirsting_blade, 'moon_pact': moon_pact, 'crimson_hourglass': crimson_hourglass,
            'vampire_mirror': vampire_mirror, 'music_disc_blood_moon': disc}


def rp(R):
    import vanilla, shutil
    from PIL import Image
    for k, f in icons().items():
        R.ICONS[k] = Image.new('RGBA', (16, 16))
        vanilla.OVERRIDES[k] = f
    R.HANDHELD_EXTRA.add('thirsting_blade')

    def post(R2):
        dst = R2.p('assets', 'bm', 'sounds', 'records', 'blood_moon.ogg')
        shutil.copy('/home/claude/bm_build/vendor/blood_moon.ogg', dst)
        R2.wj('assets/bm/sounds.json', {'music_disc.blood_moon': {'sounds': [{'name': 'bm:records/blood_moon', 'stream': True}]}})
    R.POST.append(post)

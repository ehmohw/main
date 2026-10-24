"""2.94: THE GLITCHED CARTRIDGE - and the followers' pixel costumes.

A grey cartridge with a scratched label, found in a won heist's haul (5% for every raider, any tier). Blow on it, use it:
  beside your Emma, Leo or Cecil - the game glitches, and their 8-bit self tumbles out (phase213: a hidden follower of its own);
  beside any other follower - it glitches THEM: from then on they can wear their PIXEL COSTUME, a PixelLab sprite of them
    (ref/pixellab/chars/<key>) that stands in for their model, always facing you, walking, sitting and fighting as they do.
  The cartridge is spent either way (one each). The costume is a row in the follower's own wardrobe (2.94b: it had a
  Pixel Wardrobe of its own, off the cartridge): locked until the cartridge, then on or off.
How a costume is worn: a flat two-sided sprite (its back drawn too - 2.94c: it was billboarded, always turned to you) stands on
the follower's host, turned as it is; the follower's own displays are hidden (their view
range to 0, the old one kept in a score) and come back when it's taken off."""
import os
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import pxart
import phase28 as P28
import phase138 as P138

HERE = os.path.dirname(os.path.abspath(__file__))
COL = '#7aff9a'
FIND = 5                                          # (% a won heist, every raider)
# the costumes: follower -> (its name, how tall it stands in blocks, the displays to hide: a base tag found by bm.pid - or None: the host's passengers)
COSTUMES = {'celi': ('Celi', 1.9, 'bm.cep'), 'demo': ('Democratus', 3.0, 'bm.dmp'), 'kw': ('KillerWatt', 2.8, 'bm.kxp'), 'tul': ('Tullius', 2.6, 'bm.tup'),
            'fishy': ('Fishy', 1.9, 'bm.fyp'), 'bloo': ('Bloo', 1.7, 'bm.bop'), 'apo': ('Apophiss', 3.6, 'bm.app'), 'chef': ('the Chef', 2.0, 'bm.kkp'),
            'neighbor': ('the Neighbor', 1.9, 'bm.nbp'), 'stalker': ('the Stalker', 2.4, 'bm.svp'), 'lantern': ('the Arachno-Lantern', 2.0, 'bm.lnp'),
            'ava': ('Queen Ava', 2.0, 'bm.avp'), 'pistachio': ('Pistachio', 1.6, 'bm.pip'), 'pearl': ('Pearlman', 1.1, 'bm.pmd'),
            'pearlq': ('Queen Pearl', 2.0, 'bm.pqp'), 'omega': ('King Omega', 3.0, 'bm.omp'), 'ashur': ('Ashur', 2.2, 'bm.asp'), 'bones': ('Bones', 2.0, 'bm.bjp'),
            'bender': ('Bender', 1.1, 'bm.bvp'), 'zib': ('Zib', 1.3, None), 'frog': ('the Frog', 1.2, None), 'don': ('Donado', 1.3, None),
            'wil': ('Wilfrey', 1.8, None), 'dennis': ('Dennis', 1.9, 'bm.dwp'), 'capshun': ('Mr. Capshun', 2.2, 'bm.mzp')}
ANIMS = ('idle', 'walk', 'sit', 'attack')
# (2.94c) a costume drawn from another character's art: Apophiss wears his Hollow boss sprite (the spines down his back and
# head the follower sprite lost) - its animations by ours
SRC = {'apo': ('apo_boss', {'idle': 'idle', 'walk': 'move', 'sit': 'idle', 'attack': 'bite'})}
PIXEL = {'emma': 'p213e', 'leo': 'p213l', 'cecil': 'p213c'}      # (theirs is a follower of its own)
MET = {'emma': 'bm.xmmet', 'leo': 'bm.xlmet', 'cecil': 'bm.xcmet'}


def _have(k):
    k = SRC.get(k, (k,))[0]
    d = os.path.join(HERE, 'ref', 'pixellab', 'chars', k)
    return os.path.isdir(d) and all(a in pxart.anims_of(k) for a in ('idle',))


KEYS = [k for k in COSTUMES if _have(k)]
_SPR = {}


def spr(k):
    if k not in _SPR:
        src, names = SRC.get(k, (k, {}))
        have = pxart.anims_of(src)
        _SPR[k] = pxart.Sprite(src, f'pk_{k}_', COSTUMES[k][1], {a: (names.get(a, a) if names.get(a, a) in have else 'idle', None) for a in ANIMS})
    return _SPR[k]


item('glitch_cart', TOTEM, 'Glitched Cartridge', COL,
     ['A grey game cartridge. The label is scratched,', 'and the picture on it keeps changing.',
      ('Use beside your Emma, Leo or Cecil: their 8-bit self tumbles out.', 'blue'),
      ('Use beside any other follower: their pixel costume,', 'blue'), ('on or off in their wardrobe from then on.', 'blue'),
      ('"Have you tried blowing on it?"', 'dark_gray')],
     model='bm:glitch_cart', stack=16, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['glitch_cart'] = 'bm:p214/use'


def textures():
    T_ = {}
    for k in KEYS:
        T_.update(spr(k).textures())
    return T_


def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((2, 1, 13, 14), fill=hexc('#7a7a82'), outline=hexc('#2a2a32'))
    d.rectangle((4, 4, 11, 10), fill=hexc('#202028'))
    for x, y, c in ((4, 5, '#ff4a8a'), (6, 6, '#4aff9a'), (8, 4, '#4ab0ff'), (10, 7, '#ffe04a'), (5, 8, '#b070ff'), (9, 9, '#4aff9a'), (7, 8, '#ff4a8a')):
        d.point((x, y), fill=hexc(c)); d.point((x + 1, y), fill=hexc(c))
    d.line((12, 3, 13, 6), fill=hexc('#c8c8d0'))
    for x in range(4, 12, 2):
        d.point((x, 13), fill=hexc('#d8c070'))
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    R.ICONS['glitch_cart'] = _icon()
    for k in KEYS:
        S = spr(k)
        for name, (tex, els) in S.models().items():
            R.HATS[name] = (tex, els)
        R.DISPLAY_3D_EXTRA = R.DISPLAY_3D_EXTRA + (S.prefix,)

    def post(R2):
        for k in KEYS:
            spr(k).item_def(R2, f'pk_{k}')
    R.POST.append(post)


def generate(G):
    import phase148 as P148
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    P = G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, second = [], []
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.pxf dummy', 'scoreboard objectives add bm.pxvr dummy']
    G.OBJECTIVES += ['bm.pxf', 'bm.pxvr']

    # ---- found in a won heist (any tier, every raider)
    G.wjson('bm/loot_table/p214/cart.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('glitch_cart')]}]})
    G.FUNCS['p105/finds'] += ['execute store result score #r bm.rng run random value 1..100', f'execute if score #r bm.rng matches ..{FIND} run function bm:p214/find']
    fn('p214/find', [f'execute in bm:gutter unless data block {P148.HA} Items[26] run loot insert {P148.HA} loot bm:p214/cart',
                     f'execute in bm:gutter if data block {P148.HA} Items[26] run loot insert {P148.HB} loot bm:p214/cart',
                     tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' found a ', 'gray'), T('Glitched Cartridge', COL, bold=True),
                                        T(' in a won heist - the picture on it keeps changing...', 'gray')]),
                     'playsound minecraft:block.note_block.bit player @s ~ ~ ~ 1 0.5', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.4'])

    # ---- use: beside which follower?
    hosts = [(w, P138.HOST[w]) for w in list(PIXEL) + KEYS]
    use = ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
           'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
           'tag @s add bm.pxuser', 'scoreboard players set #done bm.rng 0']
    for w, (ht, tag) in hosts:
        use.append(f'execute if score #done bm.rng matches 0 as @e[type=minecraft:{ht},tag={tag},distance=..6,sort=nearest] if score @s bm.pid = #me bm.pid at @s run function bm:p214/on/{w}')
    use += ['execute if score #done bm.rng matches 0 run ' + say('The cartridge buzzes. Use it beside one of your followers.', COL),
            'execute if score #done bm.rng matches 0 run playsound minecraft:block.note_block.bit player @s ~ ~ ~ 1 0.5', 'tag @s remove bm.pxuser']
    fn('p214/use', use)
    glitch = ['particle minecraft:electric_spark ~ ~1 ~ 0.5 0.8 0.5 0.3 40', 'particle minecraft:dust{color:[0.3,1.0,0.5],scale:1.4} ~ ~1 ~ 0.6 0.8 0.6 0 30',
              'playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 1 0.5', 'playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 1 1.8']
    spend = 'execute as @a[tag=bm.pxuser,limit=1] run clear @s *[minecraft:custom_data~{bm:"glitch_cart"}] 1'
    U = '@a[tag=bm.pxuser,limit=1]'
    for w, pfx in PIXEL.items():
        nm = {'emma': '8-Bit Emma', 'leo': '8-Bit Leo', 'cecil': '8-Bit Cecil'}[w]
        fn(f'p214/on/{w}', ['scoreboard players set #done bm.rng 1',
                            f'execute if entity @a[tag=bm.pxuser,tag={MET[w]}] run return run execute as {U} run ' + say(f'The cartridge flickers - but {nm} is already out.', COL),
                            f'execute as {U} positioned ^ ^ ^1.5 run function bm:{pfx}/enc/glitch', spend] + glitch +
           [f'execute as {U} run ' + tellraw('@s', [T('The cartridge glitches - colours smear across the air - and out of the static tumbles ', COL, italic=True),
                                                     T(nm, COL, bold=True), T('.', COL, italic=True)])])
    for k in KEYS:
        nm = COSTUMES[k][0]
        fn(f'p214/on/{k}', ['scoreboard players set #done bm.rng 1',
                            f'execute if entity @a[tag=bm.pxuser,tag=bm.pxu_{k}] run return run execute as {U} run ' +
                            say(f'{nm[0].upper() + nm[1:]} already has a pixel costume - it\'s in their wardrobe.', COL),
                            f'tag {U} add bm.pxu_{k}', f'tag {U} add bm.pxo_{k}', spend] + glitch +
           [f'execute as {U} run ' + tellraw('@s', P + [T('The cartridge glitches - and ', 'gray'), T(nm, COL, bold=True),
                                                         T(' flickers into sixteen colours. ', 'gray'), T('(A pixel costume - on or off in their wardrobe.)', 'dark_gray')])])

    # ---- the switch, from the follower's own wardrobe (phase99: the "Pixel costume" row; 2.94b - it was the Pixel Wardrobe)
    import phase99 as P99
    for k in KEYS:
        nm = COSTUMES[k][0]
        fn(f'p214/t/{k}', [f'execute unless entity @s[tag=bm.pxu_{k}] run return run function bm:p214/locked/{k}',
                           f'execute if entity @s[tag=bm.pxo_{k}] run return run function bm:p214/t/{k}_off', f'tag @s add bm.pxo_{k}',
                           'playsound minecraft:block.note_block.bit player @s ~ ~ ~ 1 1.6', f'function bm:p99/menu/{k}'])
        fn(f'p214/t/{k}_off', [f'tag @s remove bm.pxo_{k}', 'playsound minecraft:block.note_block.bit player @s ~ ~ ~ 1 0.6', f'function bm:p99/menu/{k}'])
        fn(f'p214/locked/{k}', [tellraw('@s', P + [T('Pixel costume', COL, bold=True), T(f' is locked - use a ', 'gray'), T('Glitched Cartridge', COL),
                                                     T(f' beside {nm} (a find in any won heist).', 'gray')]), f'function bm:p99/menu/{k}'])

    # ---- wearing it (each second, as each follower's host): the sprite on, its own displays hidden - or the other way round
    hide1 = ['execute store result score @s bm.pxvr run data get entity @s view_range 100', 'data modify entity @s view_range set value 0f', 'tag @s add bm.pxhid']
    fn('p214/hide1', hide1)
    fn('p214/keep', ['execute unless data entity @s {view_range:0.0f} run function bm:p214/hide1'])
    fn('p214/show1', ['execute store result entity @s view_range float 0.01 run scoreboard players get @s bm.pxvr', 'tag @s remove bm.pxhid'])
    for k in KEYS:
        nm, h, base = COSTUMES[k]
        ht, tag = P138.HOST[k]
        S = spr(k)
        if base:
            mine = f'@e[type=minecraft:item_display,tag={base},tag=!bm.pxcos,distance=..12]'
            hide = [f'execute as {mine} if score @s bm.pid = #me bm.pid run function bm:p214/keep']
            show = [f'execute as @e[type=minecraft:item_display,tag={base},tag=bm.pxhid,distance=..12] if score @s bm.pid = #me bm.pid run function bm:p214/show1']
        else:
            hide = ['execute on passengers if entity @s[type=#bm:p214_displays,tag=!bm.pxcos] run function bm:p214/keep']
            show = ['execute on passengers if entity @s[type=#bm:p214_displays,tag=bm.pxhid] run function bm:p214/show1']
        nbt = {'Tags': ['bm.pxcos', f'bm.pxcos_{k}', 'bm.pxnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:pk_{k}'}},
               'item_display': 'fixed', 'teleport_duration': Int(1), 'view_range': F(1.6),
               'brightness': {'block': Int(13), 'sky': Int(13)}, 'shadow_radius': F(0.4), 'shadow_strength': F(0.5),
               'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0), F(0)],
                                  'scale': [F(round(S.size, 4))] * 3}}
        up = round(S.size / 2 - 6 * S.size / S.N, 3)                  # (the quad's middle above the ground: the feet on it)
        cos = f'@e[type=minecraft:item_display,tag=bm.pxcos_{k},distance=..12]'
        fn(f'p214/s/{k}', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #on bm.rng 0',
                           f'execute as @a[tag=bm.pxo_{k}] if score @s bm.pid = #me bm.pid run scoreboard players set #on bm.rng 1',
                           f'execute if score #on bm.rng matches 0 if entity @s[tag=bm.pxhost] run return run function bm:p214/off/{k}',
                           'execute if score #on bm.rng matches 0 run return 0', 'tag @s add bm.pxhost',
                           'scoreboard players set #has bm.rng 0', f'execute as {cos} if score @s bm.pid = #me bm.pid run scoreboard players set #has bm.rng 1',
                           f'execute if score #has bm.rng matches 0 positioned ~ ~{up} ~ run function bm:p214/new/{k}'] + hide)
        fn(f'p214/new/{k}', [f'summon minecraft:item_display ~ ~ ~ {snbt(nbt)}', 'scoreboard players operation @e[type=minecraft:item_display,tag=bm.pxnew,distance=..1] bm.pid = #me bm.pid',
                             'tag @e[type=minecraft:item_display,tag=bm.pxnew,distance=..1] remove bm.pxnew', 'particle minecraft:electric_spark ~ ~ ~ 0.4 0.6 0.4 0.2 16'])
        fn(f'p214/off/{k}', ['tag @s remove bm.pxhost', f'execute as {cos} if score @s bm.pid = #me bm.pid run kill @s'] + show +
           ['particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.2 16'])
        second.append(f'execute as @e[type=minecraft:{ht},tag={tag}] at @s run function bm:p214/s/{k}')
        # (every tick: the sprite stands on its host, and plays what the host is doing - sitting, walking, fighting, or idling)
        n = {a: len(S.frames[a]) for a in ANIMS}
        anim = ['scoreboard players set #st bm.rng 0', 'execute if data entity @s {Sitting:1b} run scoreboard players set #st bm.rng 2',
                'execute if score #st bm.rng matches 0 store result score #vx bm.rng run data get entity @s Motion[0] 1000',
                'execute if score #st bm.rng matches 0 store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                'execute if score #st bm.rng matches 0 run scoreboard players operation #vx bm.rng *= #vx bm.rng',
                'execute if score #st bm.rng matches 0 run scoreboard players operation #vz bm.rng *= #vz bm.rng',
                'execute if score #st bm.rng matches 0 run scoreboard players operation #vx bm.rng += #vz bm.rng',
                'execute if score #st bm.rng matches 0 if score #vx bm.rng matches 500.. run scoreboard players set #st bm.rng 1',
                'execute if score #st bm.rng matches 0 if entity @e[type=#bm:hostile,tag=!bm.npc,distance=..3] run scoreboard players set #st bm.rng 3',
                'scoreboard players operation #me bm.pid = @s bm.pid',
                f'execute as {cos} if score @s bm.pid = #me bm.pid positioned ~ ~{up} ~ run function bm:p214/f/{k}']
        fn(f'p214/h/{k}', anim)
        fr = ['tp @s ~ ~ ~ ~ 0', 'scoreboard players add @s bm.pxf 1', 'scoreboard players operation #fi bm.rng = @s bm.pxf',
              'scoreboard players operation #fi bm.rng %= #3 bm.rng', 'execute unless score #fi bm.rng matches 0 run return 0',
              'scoreboard players operation #fi bm.rng = @s bm.pxf', 'scoreboard players operation #fi bm.rng /= #3 bm.rng']
        for st, a in enumerate(('idle', 'walk', 'sit', 'attack')):
            if a == 'sit':                                              # (sitting down once, then still)
                fr.append(f'execute if score #st bm.rng matches {st} run return run function bm:p214/f/{k}_sit')
                continue
            fr += [f'execute if score #st bm.rng matches {st} run scoreboard players set #n bm.rng {n[a]}',
                   f'execute if score #st bm.rng matches {st} run scoreboard players operation #fi bm.rng %= #n bm.rng'] + \
                  [f'execute if score #st bm.rng matches {st} if score #fi bm.rng matches {i} run return run '
                   f'data modify entity @s item.components."minecraft:custom_model_data" set value {{strings:["{a}_{i}"]}}' for i in range(n[a])]
        fn(f'p214/f/{k}', fr)
        fn(f'p214/f/{k}_sit', [f'execute if score #fi bm.rng matches {i} run return run data modify entity @s item.components."minecraft:custom_model_data" set value {{strings:["sit_{i}"]}}'
                               for i in range(n['sit'])] +
           [f'data modify entity @s item.components."minecraft:custom_model_data" set value {{strings:["sit_{n["sit"] - 1}"]}}'])
        tick.append(f'execute as @e[type=minecraft:{ht},tag={tag},tag=bm.pxhost] at @s run function bm:p214/h/{k}')
    # (a costume whose host is gone - sent home, fainted - goes with it)
    second.append('execute as @e[type=minecraft:item_display,tag=bm.pxcos] at @s run function bm:p214/orphan')
    fn('p214/orphan', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #al bm.rng 0'] +
       [f'execute if entity @s[tag=bm.pxcos_{k}] as @e[type=minecraft:{P138.HOST[k][0]},tag={P138.HOST[k][1]},tag=bm.pxhost,distance=..8] if score @s bm.pid = #me bm.pid run scoreboard players set #al bm.rng 1'
        for k in KEYS] + ['execute if score #al bm.rng matches 0 run kill @s'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #3 bm.rng 3']
    G.wjson('bm/tags/entity_type/p214_displays.json', {'values': ['minecraft:item_display', 'minecraft:block_display']})
    G.FUNCS['tick'] += tick
    G.FUNCS['loop/second'][-1:-1] = second
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.pxcos]')
    fn('admin/glitch_cart', [give('glitch_cart'), say('A Glitched Cartridge. (Use it beside a follower.)', COL)])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/glitch_cart', 'yellow'), T('  a Glitched Cartridge - 8-bit followers and pixel costumes', 'gray')]))

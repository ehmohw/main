"""Phase 141 (2.78): A DOLL OF EVERY FOLLOWER, in the Emma doll's chibi style. Emma had a doll; now they all do - Cecil, Celi, Leo,
Democratus, KillerWatt, Apophiss, Tullius, Zib, Pearlman, Donado, Wilfrey and the Frog with Mustache - each a big-headed, big-eyed
little figure in their own colours with their signature thing (dolls_art). Cecil sells them beside Emma's (3 Trophies each).
Right-click a block: set it down. Right-click it: it twirls, in its own colours and sounds. It shimmers now and then while it
stands. Sneak + punch: pick it up.

Importing registers the items; generate(G) runs after phase46 (it copies the Emma doll's placer); rp(R) adds the models."""
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, Int

# (doll, name, colour, what it is, click particle, click sound, idle shimmer)
DOLLS = [('doll_cecil', 'Cecil', '#9a6ad8', 'A felt doll of Cecil, staff and all.', 'minecraft:witch', 'minecraft:block.amethyst_block.chime', 'minecraft:enchant'),
         ('doll_celi', 'Celi', '#a8e4ff', 'A doll of Celi, spear on her shoulder.', 'minecraft:snowflake', 'minecraft:block.powder_snow.step', 'minecraft:snowflake'),
         ('doll_leo', 'Leo', '#4a8ad8', 'A doll of Sir Leo, ready for anything.', 'minecraft:nautilus', 'minecraft:block.bell.use', 'minecraft:bubble_pop'),
         ('doll_demo', 'Democratus', '#c0c8e0', 'A doll of Democratus, scythe and storm-cloak.', 'minecraft:electric_spark', 'minecraft:item.trident.thunder', 'minecraft:electric_spark'),
         ('doll_kw', 'KillerWatt', '#ffe04a', 'A doll of KillerWatt, tendrils crackling.', 'minecraft:electric_spark', 'minecraft:block.beacon.power_select', 'minecraft:wax_off'),
         ('doll_apo', 'Apophiss', '#3a7a3a', 'A doll of the Serpent King. It looks back.', 'minecraft:soul_fire_flame', 'minecraft:entity.wither.ambient', 'minecraft:soul'),
         ('doll_tul', 'Tullius', '#7ab0c0', 'A doll of Captain Tullius, dripping wet.', 'minecraft:splash', 'minecraft:entity.player.splash', 'minecraft:dripping_water'),
         ('doll_zib', 'Zib', '#7aff9a', 'A doll of Zib the Donadian. Batteries not included.', 'minecraft:glow', 'minecraft:block.beacon.activate', 'minecraft:glow'),
         ('doll_pearl', 'Pearlman', '#e8e8f0', 'A doll of Pearlman, salespenguin of the year.', 'minecraft:happy_villager', 'minecraft:block.note_block.pling', 'minecraft:end_rod'),
         ('doll_don', 'Donado', '#e8d29a', 'A plush Donado. Squeeze it and it wags.', 'minecraft:heart', 'minecraft:entity.wolf.ambient', 'minecraft:happy_villager'),
         ('doll_wil', 'Wilfrey', '#f4f4f4', 'A doll of Wilfrey, the Kind Lord, sword raised.', 'minecraft:end_rod', 'minecraft:block.bell.resonate', 'minecraft:white_ash'),
         ('doll_frog', 'Frog', '#5aa83a', 'A doll of the Frog with Mustache. Distinguished.', 'minecraft:happy_villager', 'minecraft:entity.frog.ambient', 'minecraft:spore_blossom_air')]
PRICE = ('trophy', 3)
SIZE = 1.0                   # (the same size as Emma's doll)

for _d, _n, _c, _what, *_ in DOLLS:
    item(_d, TOTEM, f'{_n} Doll' if _n != 'Frog' else 'Frog with Mustache Doll', _c, [_what, ('Right-click a block: set it down.', 'blue'), ('Right-click it: it twirls.', 'blue'),
                                       ('Sneak + punch: pick it up.', 'gray')],
         model=f'bm:{_d}', stack=16, cat='fun', comps=hold('none'))
    HOLD[_d] = f'bm:p141/{_d}/use'


# WILFREY IN A FRAME, AND IN A DISPLAY CASE (2.78a): his locket hung in a frame brings him out to keep watch by it, as every
# other follower's item does (bare bones - a framed Wilfrey carries no gear); in a display case he stands as his doll.
import phase68 as _P68, phase134 as _P134
_P68.KINDS['wil'] = (max(v[0] for v in _P68.KINDS.values()) + 1, 'wilfrey_locket', 'wolf', 'bm.wilfrey', 'p2/wil/summon', 'p141/wil_frame_off',
                     'bm.wlsel', 'Wilfrey', '#f4f4f4')
_P68.HE.add('wil')
_figures0 = _P134.figures


def _figures():
    F_ = _figures0()
    F_['wilfrey_locket'] = ('Wilfrey', [('bm:doll_wil', (0.0, 0.5, 0.0), _P134.IDENT, _P134.IDENT, 1.0)])
    return F_


_P134.figures = _figures
_P134.FIT['wilfrey_locket'] = (0.000, 1.350, -0.312, 0.275, -0.244, 0.238)      # (measured: phase134.measure)


def extend_offers(O, offer):
    O['wizard'] += [offer(PRICE, (d, 1)) for d, *_ in DOLLS]


def generate(G):
    fn, give, title = G.fn, G.give, G.title
    # (a framed Wilfrey goes home: he fades, as he does when his locket sends him)
    fn('p141/wil_frame_off', ['execute as @e[type=minecraft:wolf,tag=bm.wlsel] at @s run function bm:p2/wil/fade'])
    ident = [F(0), F(0), F(0), F(1)]
    fast, second = [], []
    for d, name, col, what, ptc, snd, idle in DOLLS:
        P = f'p141/{d}/'
        fn(P + 'use', [l.replace('p46/emma/', P).replace('"emma_doll"', f'"{d}"') for l in G.FUNCS['p46/emma/use']])
        fn(P + 'ray', [l.replace('p46/emma/', P) for l in G.FUNCS['p46/emma/ray']])
        fn(P + 'hit', [l.replace('p46/emma/', P) for l in G.FUNCS['p46/emma/hit']])
        disp = snbt({'Tags': ['bm.dolld', f'bm.{d}d', 'bm.p45new'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:{d}'}},
                     'item_display': 'fixed', 'teleport_duration': Int(6),
                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.5 * SIZE), F(0)], 'scale': [F(SIZE)] * 3}})   # (as Emma's: feet at the block's top)
        hit = snbt({'Tags': ['bm.dollhit', f'bm.{d}hit', 'bm.p45hit', 'bm.p45new'], 'width': F(0.55), 'height': F(1.2 * SIZE), 'response': B(1)})
        fn(P + 'spawn', [f'summon minecraft:item_display ~ ~ ~ {disp}', f'summon minecraft:interaction ~ ~ ~ {hit}', 'tp @e[tag=bm.p45new,distance=..0.5] ~ ~ ~ ~ 0',
                         'tag @e[tag=bm.p45new,distance=..0.5] remove bm.p45new', 'playsound minecraft:block.wool.place block @a[distance=..12] ~ ~ ~ 1 1.2',
                         f'particle {ptc} ~ ~0.4 ~ 0.25 0.25 0.25 0.02 8'])
        fast.append(f'execute as @e[type=minecraft:interaction,tag=bm.{d}hit] if data entity @s interaction at @s run function bm:{P}click')
        fn(P + 'click', [f'execute as @e[type=minecraft:item_display,tag=bm.{d}d,distance=..0.4] at @s run tp @s ~ ~ ~ ~120 0',
                         f'playsound {snd} block @a[distance=..12] ~ ~ ~ 0.6 1.4', f'particle {ptc} ~ ~0.8 ~ 0.3 0.3 0.3 0.02 8', 'data remove entity @s interaction'])
        fast.append(f'execute as @e[type=minecraft:interaction,tag=bm.{d}hit] if data entity @s attack at @s run function bm:{P}punch')
        fn(P + 'punch', ['tag @s add bm.p45me', f'execute on attacker if predicate bm:p20/sneaking run function bm:{P}pick', 'tag @s remove bm.p45me', 'data remove entity @s attack'])
        fn(P + 'pick', [give(d), f'execute as @e[type=minecraft:interaction,tag=bm.p45me] at @s run function bm:{P}gone', 'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 1 1'])
        fn(P + 'gone', [f'kill @e[type=minecraft:item_display,tag=bm.{d}d,distance=..0.6]', 'particle minecraft:poof ~ ~0.3 ~ 0.2 0.2 0.2 0.02 6', 'kill @s'])
        # (it shimmers now and then while it stands)
        second.append(f'execute as @e[type=minecraft:item_display,tag=bm.{d}d] at @s if predicate bm:p141/now_and_then run particle {idle} ~ ~0.7 ~ 0.2 0.25 0.2 0 2')
    G.wjson('bm/predicate/p141/now_and_then.json', {'condition': 'minecraft:random_chance', 'chance': 0.25})
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    G.FUNCS['loop/second'][-1:-1] = second
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.dolld]', 'kill @e[type=minecraft:interaction,tag=bm.dollhit]']


# ================================================================================================= the dolls' models
def rp(R):
    import dolls_art as DA
    R.TEXTURE_MODS.append(DA)
    R.HATS.update(DA.models())
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('doll_',)

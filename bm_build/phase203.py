"""2.92: every structure on the ground settles into the land (settle.py) - no sheer dirt walls where a hill met its box, no
floating corners, no square plinths of stone under it.

  Jigsaw templates (the graveyard, the Frostbound Spire, the Hexbound Cathedral, Wilfrey's Keep, the Sunken Throne) carry a
  marker at each corner; once someone comes near, the low corner settles the footprint, whichever way the piece was turned.
  Runtime builders (sword shrines, Seawatch Forts, the Dread ruins, the Underwater Kingdom, the Nether outposts) settle as
  they build. The Omega Palace already builds its own skirt; the crash sites are craters on purpose; the End's places float
  on their own rock; the Frog's hut stands on stilts in the water."""
import settle

P2 = {  # d: settle.make's options (each template's floor is how deep its start sits: -start_height)
    'frost': dict(cut=12, fill=8, under=True, deep=14),
    'hex': dict(cut=12, fill=8, under=True, deep=10, water=True),
    'keep': dict(cut=14, fill=8, under=True, deep=14),
    'tide': dict(cut=10, fill=6, under=True, deep=12, water=True, clear='water', high=18),
}


def _inside_tag(G, name, Bd, floor):
    """terrain blocks a template doesn't use itself above its floor: those may be cleared out of its footprint"""
    used = {st.split(':')[-1].split('[')[0] for (x, y, z), st in Bd.b.items() if y >= floor}
    keep = [b for b in settle.CUT if b not in used]
    G.wjson(f'bm/tags/block/settle_in_{name}.json', {'values': [f'minecraft:{b}' for b in keep] +
                                                     [p for p in settle.PLANTS if p.split(':')[-1].lstrip('#') not in used]})
    return f'#bm:settle_in_{name}'


def mark_graveyard(top):
    """(gen_tags_worldgen, as it exports the yard)"""
    settle.mark(top, 'graveyard', 0, 0, top.size[0] - 1, top.size[2] - 1, 1)


def generate(G):
    fn = G.fn
    second = []
    settle.setup(G)

    # ---------------------------------------------------------------- the dungeons' templates: corner markers
    import p2
    from p2.data import WORLDGEN
    B = p2.builds()
    for d, kw in P2.items():
        Bd = B[d]
        floor = -WORLDGEN[d][2]['absolute']
        SX, SY, SZ = Bd.size
        if kw.get('clear') != 'water': kw = dict(kw, inside=_inside_tag(G, f'p2_{d}', Bd, floor))
        if kw.get('under'): kw = dict(kw, base=floor)
        settle.make(G, f'p2_{d}', SX, SZ, turn=True, **kw)
        settle.corners(G, Bd, f'p2_{d}', 0, 0, SX - 1, SZ - 1, floor, second)
        Bd.export(G.path('data', 'bm', 'structure', f'p2_{d}.nbt'))

    # the graveyard's yard (its crypt hangs under it: nothing is filled under the floor); gen_tags_worldgen marks the template
    import structures as S
    sx, _, sz = S.graveyard_pieces(S.build_graveyard())[0].size
    settle.make(G, 'graveyard', sx, sz, turn=True, cut=10, fill=6)
    settle.corners(G, None, 'graveyard', 0, 0, sx - 1, sz - 1, 1, second)

    # ---------------------------------------------------------------- runtime builders
    # sword shrines: 7 x 7 round the seed, on the ground it found
    settle.make(G, 'shrine', 7, 7, cut=5, fill=4)
    G.FUNCS['p39/shrine/build'] += settle.run('shrine', -3, 0, -3)

    # Seawatch Forts: the plinth only under the walls; round them a mound of the shore's own sand (or grass, or stone)
    settle.make(G, 'lefort', 11, 11, cut=7, fill=6, under=True, deep=8, water=True)
    b2 = G.FUNCS['p96/fort/build2']
    i = next(k for k, l in enumerate(b2) if l.startswith('fill ~-6 ~-7 ~-6 ~6 ~-1 ~6 minecraft:stone_bricks'))
    b2[i] = 'fill ~-4 ~-7 ~-4 ~4 ~-1 ~4 minecraft:stone_bricks replace #bm:p96_fill'
    b2[i + 1:i + 1] = settle.run('lefort', -5, 0, -5)

    # the Dread ruins: 21 x 21 courts (the shark's sunken one is only cut into the sea floor)
    settle.make(G, 'dbruin', 21, 21, cut=8, fill=6, under=True, deep=10)
    settle.make(G, 'dbshark', 21, 21, cut=8, fill=0, clear='water', high=14)
    for k, nm in (('snow', 'dbruin'), ('witch', 'dbruin'), ('shark', 'dbshark')):
        f = G.FUNCS[f'p197/{k}/ruin/build']
        j = next(n for n, l in enumerate(f) if l.startswith('fill ~-11 ~ ~-11 ~11'))
        f[j + 1:j + 1] = settle.run(nm, -10, 0, -10)

    # the Underwater Kingdom: the sea floor banked up to its dome in sand, the slopes round it cut back to water
    import kingdom as K
    settle.make(G, 'kingdom', K.SX, K.SZ, cut=10, fill=8, under=True, water=True, deep=12, high=20, clear='water')
    f = G.FUNCS['p199/k/build']
    f[1:1] = settle.run('kingdom', -35, 1, -35)

    # the Nether's outposts: on the ledge the scan found (low cuts: the Nether has a ceiling, and lava behind its walls)
    import hellend as H
    for k, dims, (ox, oz) in (('ember_outpost', H.EO, (-11, -11)), ('colossus_forge', H.CF, (-20, -23))):
        settle.make(G, f'p200_{k}', dims['SX'], dims['SZ'], cut=8, fill=8, under=True, base=dims['FLOOR'] + 1, deep=10, high=8)
        G.FUNCS[f'p200/{k}/place'][1:1] = settle.run(f'p200_{k}', ox, 0, oz)

    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:marker,tag=bm.settle]']
    G.FUNCS['loop/second'][-1:-1] = second

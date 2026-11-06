"""2.92: every structure on the ground settles into the land (settle.py) - no sheer dirt walls where a hill met its box, no
floating corners, no square plinths of stone under it.

  Jigsaw templates (the graveyard, the Frostbound Spire, the Hexbound Cathedral, Wilfrey's Keep, the Sunken Throne) carry a
  marker at each corner; once someone comes near, the low corner settles the footprint, whichever way the piece was turned.
  Runtime builders (sword shrines, Seawatch Forts, the Dread ruins, the Underwater Kingdom, the Nether outposts) settle as
  they build (3.0h: and the Omega Palace, round its own skirt).
  (3.0h) Every one of them is laid knowing a worldgen seed - a jigsaw start's bottom layer - stands IN the ground's top block.
  The rest: the crash sites are craters on purpose; the End's places float
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


# (3.0h) the yard's ground (its paths and podzol, template y1) sits IN the turf's top block, as a jigsaw start's bottom layer
# does: the first layer above the ground is y2 (settled from y1, its first ring had cut a trench round the yard)
GY = 2


def mark_graveyard(top):
    """(gen_tags_worldgen, as it exports the yard)"""
    settle.mark(top, 'graveyard', 0, 0, top.size[0] - 1, top.size[2] - 1, GY)


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
        # (3.0h) the template's layer -start_height sits IN the ground's top block (a jigsaw start's bottom layer is set into the
        # ground: getGroundLevelDelta 1) - its floor plate, flush with the turf - so the first layer ABOVE the ground is the next:
        # settled from there. (At -start_height, the first ring cut the turf round it: a trench a block deep round every one)
        floor = -WORLDGEN[d][2]['absolute'] + 1
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
    settle.corners(G, None, 'graveyard', 0, 0, sx - 1, sz - 1, GY, second)

    # ---------------------------------------------------------------- runtime builders
    # sword shrines: 7 x 7 round the seed, on the ground it found
    # (3.0h: it had stood a block low - phase39 - and its first ring cut the turf round it into a trench. Flush now; banked under
    #  its edges too, so a shrine on a slope doesn't hang a corner over the drop)
    settle.make(G, 'shrine', 7, 7, cut=6, fill=5, under=True, deep=6)
    G.FUNCS['p39/shrine/build'] += settle.run('shrine', -3, 0, -3)

    # Seawatch Forts: the plinth only under the walls; round them a mound of the shore's own sand (or grass, or stone)
    settle.make(G, 'lefort', 11, 11, cut=7, fill=6, under=True, deep=8, water=True)
    b2 = G.FUNCS['p96/fort/build2']
    i = next(k for k, l in enumerate(b2) if l.startswith('fill ~-6 ~-7 ~-6 ~6 ~-1 ~6 minecraft:stone_bricks'))
    b2[i] = 'fill ~-4 ~-7 ~-4 ~4 ~-1 ~4 minecraft:stone_bricks replace #bm:p96_fill'
    b2[i + 1:i + 1] = settle.run('lefort', -5, 0, -5)

    # the Dread ruins: 21 x 21 courts (the shark's sunken one is only cut into the sea floor)
    # (3.0h, the owner: "often messy, other terrain cutting into it". They had stood a block low - phase197: the turf closed over
    #  their floors - and only plants were ever cleared from the court: a hillside stood on through it. Now the court is cleared
    #  of the land above its floor first (to its sky, 28 up), the rings round it cut wider and banked deeper; the shark's court
    #  and rings cut to water only through rock and weed, never air - no water left standing over the sea)
    import phase197 as P197
    settle.make(G, 'dbruin', 21, 21, cut=10, fill=8, under=True, deep=12)
    settle.make(G, 'dbshark', 21, 21, cut=8, fill=0, clear='water', high=14, cutset='#bm:settle_wet')
    assert 10 + 10 < P197.SEED_R, 'a Dread ruin\'s seed must wait for all its settling to be loaded'
    for k, nm in (('snow', 'dbruin'), ('witch', 'dbruin'), ('shark', 'dbshark')):
        f = G.FUNCS[f'p197/{k}/ruin/build']
        f[0:0] = (['fill ~-11 ~ ~-11 ~11 ~14 ~11 minecraft:water replace #bm:settle_wet'] if nm == 'dbshark' else
                  ['fill ~-11 ~ ~-11 ~11 ~28 ~11 minecraft:air replace #bm:settle_cut'])
        j = next(n for n, l in enumerate(f) if l.startswith('fill ~-11 ~ ~-11 ~11') and 'settle' not in l)
        f[j + 1:j + 1] = settle.run(nm, -10, 0, -10)

    # the Underwater Kingdom: the sea floor banked up to its dome in sand, the slopes round it cut back to water
    import kingdom as K
    # (3.0g: high 16, was 20 - its water cut reached the seed + 30, above the sea for a kingdom set down at y 34: a "watery
    #  square" standing out of the surface. Now its top is the seed + 26: y 59 at most, the seed being 33 at most - phase199)
    import phase199 as P199
    # (3.1c, the owner: "the kingdom needs to sit deep enough ... and it should naturally mix with the terrain as it digs a hole
    #  into the ocean floor". It's set down to SEED_MAX 22 now (its top at y 50 at most: twelve blocks of sea over it). First its
    #  whole square is cleared of the sea floor to water, up to its top (the template only sets the dome: the bed it was sunk
    #  into stood round the dome, up its sides); then 18 rings round it are cut back 1:1 to water - a crater, its slopes the
    #  sea floor's own, down to the dome)
    KHIGH, KCAP = 18, P199.SEA_Y - 4 - (P199.SEED_MAX + 1)        # (every ring cleared up to y 59 at most: never water above the sea)
    assert P199.SEED_MAX + 1 + KCAP < P199.SEA_Y - 3, 'the kingdom\'s settling would cut water above the sea'
    assert P199.SEED_MAX - K.FY + K.SY < P199.SEA_Y - 10, 'the kingdom\'s top must stand well under the sea'
    settle.make(G, 'kingdom', K.SX, K.SZ, cut=P199.KCUT, fill=8, under=True, water=True, deep=12, high=KHIGH, clear='water', steep=9, cap=KCAP, sub='minecraft:sandstone')
    f = G.FUNCS['p199/k/build']
    per = max(1, 32768 // (K.SX * K.SZ))
    pre = [f'fill ~-35 ~{y} ~-35 ~{K.SX - 36} ~{min(y + per - 1, KCAP + 1)} ~{K.SZ - 36} minecraft:water replace #bm:settle_wet'
           for y in range(1, KCAP + 2, per)][::-1]          # (top-down: the sea floor's sand never left hanging over a cleared layer)
    f[0:0] = pre
    j = next(n for n, l in enumerate(f) if l.startswith('place template bm:p199_kingdom '))
    f[j + 1:j + 1] = settle.run('kingdom', -35, 1, -35)

    # (3.0h) the Omega Palace: its own skirt of stone under it, and now the land round it settled too - the dark wood's hills cut
    # back from its walls, its trees off them, the ground banked to its edge (the floor: the seed's block + 1, where it builds)
    import palace as PAL
    import phase169 as P169
    settle.make(G, 'palace', PAL.SX, PAL.SZ, cut=P169.PAL_SETTLE, fill=8, deep=12)
    G.FUNCS['p169/pal/build'][-1:-1] = settle.run('palace', P169.OX, 0, P169.OZ)

    # the Nether's outposts: on the ledge the scan found (low cuts: the Nether has a ceiling, and lava behind its walls)
    import hellend as H
    for k, dims, (ox, oz) in (('ember_outpost', H.EO, (-11, -11)), ('colossus_forge', H.CF, (-20, -23))):
        settle.make(G, f'p200_{k}', dims['SX'], dims['SZ'], cut=8, fill=8, under=True, base=dims['FLOOR'] + 1, deep=10, high=8)
        G.FUNCS[f'p200/{k}/place'][1:1] = settle.run(f'p200_{k}', ox, 0, oz)

    # (3.0g) an outpost settled before 3.0g in a biome no vanilla tag names (the Undercrown's own, filled over its box) got the
    # Overworld's default - grass on top, dirt banked under: once each, round its core, that ground is the Nether's again
    for tag, r in (('bm.outpost', 24), ('bm.forge', 36)):
        nm = tag.split('.')[1]
        per = max(1, 32768 // ((2 * r + 1) ** 2))
        body = [f'fill ~-{r} ~{y} ~-{r} ~{r} ~{min(y + per - 1, 10)} ~{r} minecraft:netherrack replace minecraft:{b}'
                for b in ('grass_block', 'dirt') for y in range(-14, 11, per)]
        fn(f'settle/regrass_{nm}', body + ['tag @s add bm.st30g'])
        second.append(f'execute as @e[type=minecraft:marker,tag={tag},tag=!bm.st30g] at @s if dimension minecraft:the_nether '
                      f'if loaded ~-{r} ~ ~-{r} if loaded ~{r} ~ ~{r} if loaded ~-{r} ~ ~{r} if loaded ~{r} ~ ~-{r} run function bm:settle/regrass_{nm}')

    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:marker,tag=bm.settle]']
    G.FUNCS['loop/second'][-1:-1] = second

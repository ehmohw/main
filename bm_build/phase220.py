"""2.94r: THE FOLLOWER GALLERY - a Pokedex of partners, off the Partner Wheel.

THE LIST    the wheel's page has a GALLERY button: every follower in the pack, numbered (#01 Emma ... #32 the Sky Buddies), and how
            many you've met. One you've met (held their item - bm:met/<kind>, as the Recruiter and Cecil's dolls use) is in their
            own colour; one you haven't is "???" - hover it for a hint where to look.
VIEW IN 3D  a page of eight at a time: their own figurines (phase134's, from their real rigs), life-ish size (about 1.4 blocks),
            in an arc in front of you, each on a slow turntable with its number and name over it. One you haven't met stands
            there as a dark silhouette under "???" - who's that? A page stays a minute (or until you open another).
(Codes, in the wheel's block - its router checks the wheel's menu: 3352 the list, 3353-3358 a page in 3D (then 3422 on), 3359 back to the wheel.)"""
from items import T
from nbt import snbt, F, Int
import phase28 as P28
import phase125 as P125
import phase134 as P134

PURPLE = '#b48cff'
GAL, PAGE0, BACK = 3352, 3353, 3359
PAGE6 = 3422                                  # (2.99: a seventh page on - 3353..3358 were full; the wheel's free codes from 3422)
pg_code = lambda i: PAGE0 + i if i < 6 else PAGE6 + i - 6
PER, RADIUS, ARC = 8, 4.6, 20               # (eight to a page, 4.6 blocks out, 20 degrees apart)
TALL, WIDE = 1.4, 1.15                      # (a figure fits in this: tall, and wide or deep)
MET_KEY = {'kw': 'killerwatt', 'don': 'donado'}          # (the met/ advancements' older names)
HINT = {
    'emma': 'Someone hums in the flowers on a sunny day.', 'celi': 'Someone mutters impatiently out in the snow.',
    'zib': 'Defend a mothership from its attackers.', 'cecil': 'The wizard at the Black Market sells his own Summoning Gem.',
    'kw': 'A storm-alien, called down with an effigy in a thunderstorm - beat him.', 'leo': 'A little stone fort on a beach - someone keeps watch.',
    'demo': 'Lightning, in a thunderstorm, under the open sky... someone kneels where it fell.', 'apo': 'The serpent king. Win his oath.',
    'tul': 'A ghost ship on the cold seas - take Leo aboard.', 'frog': 'A hut in the swamp; he works for a Medallion.',
    'don': 'Held in a mothership\'s pen. Set him free.', 'pearl': 'Collect all nine of Pearlman\'s gems out in the world.',
    'wil': 'Beat the Hollow King; his grandson sleeps in a grave.', 'fishy': 'A gentleman at his desk in the Cabinet of Curiosities.',
    'dennis': 'Trade with the dwarf in the Assay Office - a lot.', 'pistachio': 'Trade with the ghost in the Pantry - a lot.',
    'omega': 'The king of the dead - make your peace with him.', 'ashur': 'Hard mode: a hot, open land, and something to burn.',
    'chef': 'Taste every Prime meat once.', 'neighbor': 'Music at night, in a village. Someone next door hears it.',
    'ava': 'Hard mode: the kingdom\'s old light, at night, with Emma beside you.', 'pearlq': 'A cake by the sea, by day - if Emma is your friend.',
    'bloo': 'Hard mode: plant a sapling in a forest at night.', 'stalker': 'Hard mode: wear its face through a Dread Night, to dawn.',
    'lantern': 'Hard mode: fell the great Arachno-Lantern.', 'bender': 'Spend time in a village. Bring a bone.',
    'bones': 'A fin, out on the ocean. Bring a fish.', 'capshun': 'Spend time near a painting you\'ve hung.', 'kettle': 'A sunny day in a meadow or a flower field. Bring paper.', 'rufus': 'The Dark Auction sells his contract.', 'henry': 'A village, at night. Bring a fish.', 'gem': 'Walk with Mr. Capshun, Kettle and Emma at once.', 'batty': 'Beat the Gutter Gentry.', 'eggbert': 'Beat the Gutter Gentry, twice.', 'count': 'Beat the Gutter Gentry, three times.', 'dragon': 'Walk with Kettle. Bring a dye (crayons!).', 'eraser': 'Walk with the Gem of Creativity. Bring paper - a fresh start.', 'cursor': 'A Glitched Cartridge, used with no one beside you.', 'inkblot': 'Walk with Mr. Capshun. Bring an ink sac.', 'speech': 'Walk with Mr. Capshun. Bring a book and quill.', 'lightbringer': "Hard mode, before the Dread's master: by day, in the open, wearing something holy.", 'dryad': 'A Pale Garden, at night. Bring a mushroom.', 'sovereign': 'Hard mode: fell the Dread Sovereign at the bottom of the Undercrown. Its Eye is in the ashes, the first time.', 'vexis': 'Hard mode: fell Admiral Vexis at the helm of the Vorn Armada, out in the End.', 'mireling': 'Hard mode: slay the Dread Mires that rise in the dark. After three, the next leaves something behind - for you.', 'keeper': 'Meet every other friend there is. Then follow the Compass of Bonds - up, into the sky.', 'nia': 'A clear, starry night, with Henry beside you.',
    'pxcecil': 'A Glitched Cartridge, used beside Cecil.', 'pxleo': 'A Glitched Cartridge, used beside Leo.',
    'pxemma': 'A Glitched Cartridge, used beside Emma.', 'sky': 'Watch the sky: a clear noon, a full-moon midnight, a storm.'}


def generate(G):
    import phase179 as P179
    fn, title, tellraw = G.fn, G.title, G.tellraw
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    cap = lambda s: s[0].upper() + s[1:]
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.galt dummy']
    G.OBJECTIVES.append('bm.galt')
    FIG = P134.figures()
    E = []                                   # (number, key, name, colour, figure item, met advancement)
    for n, (w, (nm, pron, col, host, tag, try_, home)) in enumerate(P125.WHO.items(), 1):
        e = P179.FOLLOW.get(tag.split(',')[0])
        iid = e[3] if e else ('wilfrey_locket' if w == 'wil' else None)
        assert iid in FIG and iid in P134.FIT, (w, iid)
        E.append((n, w, cap(nm), col, iid, f'bm:met/{MET_KEY.get(w, w)}'))
    assert set(HINT) == set(P125.WHO), set(HINT) ^ set(P125.WHO)
    met = lambda a: f'entity @s[advancements={{{a}=true}}]'
    pages = [E[i:i + PER] for i in range(0, len(E), PER)]
    assert len(pages) <= 6 + 28, len(pages)

    # ================================================================== the list
    btns = [P28.btn([T('◈ View in 3D: ', PURPLE), T(f'#{pg[0][0]:02d}-#{pg[-1][0]:02d}', 'white')], pg_code(i),
                    tooltip=T(f'Followers #{pg[0][0]:02d} to #{pg[-1][0]:02d} as figurines in front of you - the ones you haven\'t met, as shadows', 'gray'))
            for i, pg in enumerate(pages)]
    btns.append(P28.btn(T('« Partner Wheel', 'gray'), BACK))
    d = P28.multi([T('Follower Gallery', PURPLE, bold=True)],
                  [P28.body([T('Met: ', 'gray'), T('@@N@@', 'white', bold=True), T(f' of {len(E)}', 'gray'),
                             T('   (hover a ??? for a hint)', 'dark_gray')], 300),
                   P28.body('@@RAW:r_gal@@', 300)], btns, columns=2)
    fn('p220/show', ['$dialog show @s ' + P28.inline(d).replace('@@N@@', '$(n)')])
    op = [f'scoreboard players set @s bm.menu {P179.WMENU}', 'scoreboard players set #galn bm.rng 0', 'data modify storage bm:tmp gal.r_gal set value [""]']
    for n, w, nm, col, iid, a in E:
        sep = '\n' if n % 3 == 1 and n > 1 else ''
        yes = T(f'{sep}#{n:02d} {nm}   ', col, hover_event={'action': 'show_text', 'value': T(f'{nm} - met', col)})
        no = T(f'{sep}#{n:02d} ???   ', '#6a6a6a', hover_event={'action': 'show_text', 'value': T(HINT[w], 'gray', italic=True)})
        op += [f'execute if {met(a)} run scoreboard players add #galn bm.rng 1',
               f'execute if {met(a)} run data modify storage bm:tmp gal.r_gal append value {snbt(yes)}',
               f'execute unless {met(a)} run data modify storage bm:tmp gal.r_gal append value {snbt(no)}']
    op += ['execute store result storage bm:tmp gal.n int 1 run scoreboard players get #galn bm.rng',
           'function bm:p220/show with storage bm:tmp gal', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.2']
    fn('p220/open', op)

    # ================================================================== the figures, in 3D
    def figure(n, w, nm, col, iid, seen):
        lo, h, x0, x1, z0, z1 = P134.FIT[iid]
        f = min(TALL / h, WIDE / (x1 - x0), WIDE / (z1 - z0))
        cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
        lit = {'block': Int(13), 'sky': Int(13)} if seen else {'block': Int(0), 'sky': Int(0)}
        out = []
        for model, (x, y, z), L, R, sc in FIG[iid][1]:
            nb = {'Tags': ['bm.galx', 'bm.galsp', 'bm.galnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
                  'item_display': 'fixed', 'brightness': lit, 'teleport_duration': Int(20),
                  'transformation': {'left_rotation': [F(round(v, 5)) for v in L], 'right_rotation': [F(round(v, 5)) for v in R],
                                     'translation': [F(round((x - cx) * f, 4)), F(round((y - lo) * f, 4)), F(round((z - cz) * f, 4))], 'scale': [F(round(sc * f, 4))] * 3}}
            out.append(f'summon minecraft:item_display ~ ~ ~ {snbt(nb)}')
        label = [T(f'#{n:02d} ', 'gray'), T(nm, col, bold=True)] if seen else [T(f'#{n:02d} ', 'gray'), T('???', '#8a8a8a', bold=True)]
        tx = {'Tags': ['bm.galx', 'bm.galnew'], 'text': {'text': '', 'extra': label}, 'billboard': 'center', 'background': Int(0x40000000),
              'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                 'translation': [F(0), F(0), F(0)], 'scale': [F(0.6)] * 3}}
        out.append(f'summon minecraft:text_display ~ ~{round(h * f + 0.25, 3)} ~ {snbt(tx)}')
        return out + ['execute as @e[type=minecraft:item_display,tag=bm.galnew,distance=..0.1] run tp @s ~ ~ ~ ~ 0']
    for n, w, nm, col, iid, a in E:
        fn(f'p220/f/{w}_m', figure(n, w, nm, col, iid, True))
        fn(f'p220/f/{w}_u', figure(n, w, nm, col, iid, False))
    for i, pg in enumerate(pages):
        L = ['scoreboard players operation #me bm.pid = @s bm.pid', 'function bm:p220/clear']
        for j, (n, w, nm, col, iid, a) in enumerate(pg):
            off = round((j - (len(pg) - 1) / 2) * ARC, 2)
            at = f'at @s rotated ~ 0 rotated ~{off} 0 positioned ^ ^ ^{RADIUS} rotated ~180 0'
            L += [f'execute if {met(a)} {at} run function bm:p220/f/{w}_m', f'execute unless {met(a)} {at} run function bm:p220/f/{w}_u']
        L += ['scoreboard players operation @e[tag=bm.galnew] bm.pid = #me bm.pid', 'scoreboard players set @e[tag=bm.galnew] bm.galt 60',
              'tag @e[tag=bm.galnew] remove bm.galnew',
              'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.4', 'particle minecraft:enchant ~ ~1 ~ 3 0.6 3 0.6 60',
              say(f'The Gallery, #{pg[0][0]:02d}-#{pg[-1][0]:02d}: in front of you for a minute - walk round them. (The wheel\'s Gallery for another page.)', PURPLE)]
        fn(f'p220/view{i}', ['dialog clear @s'] + L)
    fn('p220/clear', ['execute as @e[tag=bm.galx] if score @s bm.pid = #me bm.pid run kill @s'])
    # (each second: the turntables turn; a page a minute old goes)
    G.FUNCS['loop/second'][-1:-1] = ['execute as @e[type=minecraft:item_display,tag=bm.galsp] at @s run tp @s ~ ~ ~ ~12 ~',
                                     'scoreboard players remove @e[tag=bm.galx] bm.galt 1', 'kill @e[tag=bm.galx,scores={bm.galt=..0}]']
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[tag=bm.galx]')

    # ================================================================== on the wheel's page, and its router
    gb = P28.btn([T('❖ ', PURPLE), T('Gallery', 'white')], GAL, width=150,
                 tooltip=T('Every follower in the pack - who you\'ve met, and who\'s still out there. (And their figurines, in 3D.)', 'gray'))
    W = G.FUNCS['p179/w/open']
    k = W.index('function bm:p179/w/show with storage bm:tmp pw')
    W.insert(k, f'data modify storage bm:tmp pw.acts append value {snbt(gb)}')
    A = G.FUNCS['p179/w/act']
    A[1:1] = [f'execute if score #act bm.pay matches {GAL} run return run function bm:p220/open',
              f'execute if score #act bm.pay matches {BACK} run return run function bm:p179/w/open'] + \
             [f'execute if score #act bm.pay matches {pg_code(i)} run return run function bm:p220/view{i}' for i in range(len(pages))]

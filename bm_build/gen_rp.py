"""Generates the Black Market resource pack: original pixel art + 3D hat models (vanilla textures)."""
import sys, json, os, shutil
from PIL import Image, ImageDraw

OUT = None


def p(*parts):
    full = os.path.join(OUT, *parts)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    return full


def hexc(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def grid(rows, pal, size=16):
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    for y, row in enumerate(rows[:size]):
        row = (row + '.' * size)[:size]
        for x, ch in enumerate(row):
            if ch != '.':
                im.putpixel((x, y), hexc(pal[ch]))
    return im


ICONS = {}
POST = []          # 1.18: hooks that write extra files at the end of build()

ICONS['token'] = grid([
    '................',
    '.....GGGGGG.....',
    '...GGYYYYYYGG...',
    '..GYYWDDDDYYYG..',
    '..GYWDDDDDDDYG..',
    '.GYDDYDDDDYDDYG.',
    '.GYDYPYDDYPYDYG.',
    '.GYDDYYYYYYDDYG.',
    '.GYDDYKYYKYDDYG.',
    '.GYDDDYYYYDDDYG.',
    '.GYDDDDYPDDDDYG.',
    '..GYDDDDDDDDYG..',
    '..GYYDDDDDDYYG..',
    '...GGYYYYYYGG...',
    '.....GGGGGG.....',
    '................'], dict(G='#7a5a0c', Y='#e8b923', W='#fff2a8', D='#2a2230', K='#0d0d0d', P='#e88aa0'))

ICONS['medallion'] = grid([
    '...RR......RR...',
    '...RRr....rRR...',
    '....RRr..rRR....',
    '.....RRrrRR.....',
    '......RRRR......',
    '.....SSSSSS.....',
    '....SVVVVVVS....',
    '...SVVVWVVVVS...',
    '...SVVWWWVVVS...',
    '...SVWWWWWVVS...',
    '...SVVWWWVVVS...',
    '...SVVWVWVVVS...',
    '....SVVVVVVS....',
    '.....SSSSSS.....',
    '................',
    '................'], dict(R='#7b2fbe', r='#4e1a80', S='#c9c9dc', V='#a560e8', W='#ffffff'))

ICONS['trophy'] = grid([
    '................',
    '..YYYYYYYYYYYY..',
    '.YYWYYYYYYYYYOY.',
    'Y.YWYYYYYYYYYO.Y',
    'Y.YWYYYYYYYYYO.Y',
    '.YYYYYYYYYYYYOY.',
    '...YYYYYYYYYO...',
    '....YYYYYYYO....',
    '.....OYYYYO.....',
    '......YYYY......',
    '.......YY.......',
    '.......YO.......',
    '.....OOOOOO.....',
    '....DDDDDDDD....',
    '....DDDDDDDD....',
    '................'], dict(Y='#f2c230', W='#fff6c0', O='#a77d10', D='#4a2f1a'))

ICONS['lucky_token'] = grid([
    '.....GGGGGG.....',
    '...GGLLLLLLGG...',
    '..GLLLLLLLLLLG..',
    '.GLLLCCLLCCLLLG.',
    '.GLLCcCCCCcCLLG.',
    'GLLLCCCCCCCCLLLG',
    'GLLLLCCCCCCLLLLG',
    'GLLLLLCCCCLLLLLG',
    'GLLLLCCCCCCLLLLG',
    'GLLLCCCCCCCCLLLG',
    '.GLLCcCLLCcCLLG.',
    '.GLLLCCLLCCLLLG.',
    '..GLLLLLSLLLLG..',
    '...GGLLLSLLGG...',
    '.....GGGGGG.....',
    '................'], dict(G='#b38a1a', L='#f2e3a1', C='#1f8a34', c='#5fd06c', S='#1f6a2c'))

ICONS['scratch_card'] = grid([
    '................',
    '.WWWWWWWWWWWWWW.',
    '.WYYYYYYYYYYYYW.',
    '.WYRYYGGGGYYRYW.',
    '.WYYYYYYYYYYYYW.',
    '.WSSSSSSSSSSSSW.',
    '.WSSRRRRRSSSSSW.',
    '.WSSSSSSRSSsSSW.',
    '.WSSSSSRSSSSSSW.',
    '.WSSSSRSSSsSSSW.',
    '.WSSSSRSSSSSSSW.',
    '.WSSsSSSSSSSSSW.',
    '.WYYYYYYYYYYYYW.',
    '.WWWWWWWWWWWWWW.',
    '................',
    '................'], dict(W='#3a2a4a', Y='#f7d23c', R='#d22b2b', G='#2c8a3a', S='#b8bcc8', s='#e8ecf4'))

ICONS['gauntlet'] = grid([
    '................',
    '.....B.B.B......',
    '....BLBLBLB.....',
    '....BLBLBLB.....',
    '....BLBLBLB.B...',
    '....BLLLLLBLB...',
    '....BLLLLLLLB...',
    '....BLLlLLLB....',
    '....BLLLLlLB....',
    '....BLLLLLLB....',
    '....GGGGGGGG....',
    '....GYYYYYYG....',
    '....GGGGGGGG....',
    '................',
    '................',
    '................'], dict(B='#3d240f', L='#a0662e', l='#c98a48', G='#7a5a0c', Y='#e8b923'))

ICONS['frying_pan'] = grid([
    '................',
    '.........KKKKK..',
    '........KDDDDDK.',
    '.......KDGGDDDDK',
    '.......KDGDDDDDK',
    '.......KDDDDDDDK',
    '.......KDDDDDDDK',
    '........KDDDDDK.',
    '.......BKKKKKK..',
    '......BB........',
    '.....BB.........',
    '....BB..........',
    '...BB...........',
    '..BB............',
    '.BB.............',
    '................'], dict(K='#111114', D='#3a3a40', G='#9a9aa4', B='#5a3a1e'))

ICONS['rubber_chicken'] = grid([
    '................',
    '..........RR....',
    '.........RYYY...',
    '.........YYKYO..',
    '.........YYYYOO.',
    '........YYYY....',
    '.......YYYY.....',
    '......YYYYY.....',
    '.....YYYYyY.....',
    '....YYYYyYY.....',
    '...YYYyYYY......',
    '...YYYYYY.......',
    '..YYYYYY........',
    '..OO.OO.........',
    '................',
    '................'], dict(R='#d82020', Y='#f7e04a', y='#d9b92a', K='#111111', O='#f08a1e'))


def key_icon():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    out, gold, purple = hexc('#2a1240'), hexc('#e8b923'), hexc('#a96bff')
    d.ellipse((1, 1, 7, 7), outline=out, width=1)
    d.ellipse((2, 2, 6, 6), outline=gold, width=1)
    d.point((4, 4), fill=purple)
    d.line((6, 6, 13, 13), fill=out, width=3)
    d.line((6, 6, 13, 13), fill=gold, width=1)
    d.line((10, 12, 8, 14), fill=out, width=2)
    d.line((12, 14, 11, 15), fill=out, width=2)
    d.point((9, 13), fill=gold); d.point((11, 15), fill=gold)
    d.point((3, 3), fill=hexc('#fff6c0'))
    return im


ICONS['market_key'] = key_icon()


ICONS['blood_crystal'] = grid([
    '................',
    '.......D........',
    '......DRD.......',
    '.....DRrRD......',
    '....DRrrWRD.....',
    '...DRRrrWWRD....',
    '...DRRRrrWRD....',
    '..DRRRRRrrRRD...',
    '..DRRRRRRrRRD...',
    '...DRRRRRRRD....',
    '...DdRRRRRdD....',
    '....DddRRdD.....',
    '.....DddddD.....',
    '......DddD......',
    '.......DD.......',
    '................'], dict(D='#2a0005', R='#c0142a', r='#e8455a', W='#ffc0c8', d='#7a0a18'))

ICONS['bloodforge_sigil'] = grid([
    '................',
    '....KKKKKKK.....',
    '...KRRRRRRRK....',
    '..KRRRRYRRRRK...',
    '.KRRRRYYYRRRRK..',
    '.KRRRYYYYYRRRK..',
    '.KRRRYYYYYRRRK..',
    '.KRRRRYYYRRRRK..',
    '.KRRRRRRRRRRRK..',
    '..KRRrRRRrRRK...',
    '...KRRRrRRRK....',
    '....KKKKKKK.....',
    '.....R...R......',
    '....RR...RR.....',
    '....R.....R.....',
    '................'], dict(K='#3a0008', R='#b3122a', r='#7a0a18', Y='#e8b923'))

ICONS['blood_almanac'] = grid([
    '................',
    '..BBBBBBBBBBBB..',
    '..BRRRRRRRRRRB..',
    '..BRRRRMMRRRRB..',
    '..BRRRMMMMRRRB..',
    '..BRRRMMMmRRRB..',
    '..BRRRRMMRRRRB..',
    '..BRRRRRRRRRRB..',
    '..BRRRRRRRRRRB..',
    '..BGGGGGGGGGGB..',
    '..BRRRRRRRRRRB..',
    '..BRRRRRRRRRRB..',
    '..BWWWWWWWWWWB..',
    '..BBBBBBBBBBBB..',
    '................',
    '................'], dict(B='#2b1010', R='#5a1020', M='#ff3b3b', m='#ffb0b0', G='#e8b923', W='#e8e0c8'))

ICONS['crimson_effigy'] = grid([
    '................',
    '......KKKK......',
    '.....KRRRRK.....',
    '.....KRYRYK.....',
    '.....KRRRRK.....',
    '......KRRK......',
    '....KKRRRRKK....',
    '...KRRRRRRRRK...',
    '...KR.KRRK.RK...',
    '......KRRK......',
    '......KRRK......',
    '.....KRKKRK.....',
    '.....KR..RK.....',
    '....KKK..KKK....',
    '...DDDDDDDDDD...',
    '................'], dict(K='#1a0004', R='#a3122a', Y='#ffd700', D='#3b2a2a'))

ICONS['ravenous_heart'] = grid([
    '................',
    '...KK....KK.....',
    '..KRRK..KRRK....',
    '.KRrrRKKRRrRK...',
    '.KRrWRRRRRrRK...',
    '.KRRRRRRRRRRK...',
    '.KRKWKWKWKWRK...',
    '.KRKKKKKKKKRK...',
    '.KRKWKWKWKWRK...',
    '..KRRRRRRRRK....',
    '...KRdRRdRK.....',
    '....KRddRK......',
    '.....KRdK.......',
    '......KK........',
    '................',
    '................'], dict(K='#1a0003', R='#9e0f22', r='#d8324a', W='#f2ead2', d='#5a0610'))

ICONS['sanguine_tonic'] = grid([
    '................',
    '......CCCC......',
    '.......WW.......',
    '.......WW.......',
    '......WGGW......',
    '.....WRRRRW.....',
    '....WRRrRRRW....',
    '....WRrRRRRW....',
    '....WRRRRRRW....',
    '....WRRRRRRW....',
    '.....WRRRRW.....',
    '......WWWW......',
    '................',
    '................',
    '................',
    '................'], dict(C='#8a5a2b', W='#cfe0f0', G='#8aa0b8', R='#b0102a', r='#ff6070'))


def gold_recolor(path, edge=True):
    im = Image.open(path).convert('RGBA')
    out = Image.new('RGBA', im.size)
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = im.getpixel((x, y))
            if a == 0: continue
            l = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            l = min(1.0, max(0.0, (l - 0.2) / 0.6))
            c0, c1 = (35, 18, 4), (255, 214, 70)
            out.putpixel((x, y), tuple(int(c0[i] + (c1[i] - c0[i]) * l) for i in range(3)) + (a,))
    return out


from paths import MC as _MC
VANILLA_ASSETS = _MC + 'ast/assets/minecraft/textures'
ICONS['golden_wings'] = gold_recolor('/home/claude/bm_build/vendor/elytra_item.png')


def dragon_recolor(path, veins=True):
    """1.10 Wings of the Elder Dragon: black-violet membrane shading to magenta, with darker diagonal ribs."""
    im = Image.open(path).convert('RGBA')
    out = Image.new('RGBA', im.size)
    stops = [(0.0, (8, 3, 12)), (0.5, (62, 14, 74)), (1.0, (200, 72, 230))]
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = im.getpixel((x, y))
            if a == 0: continue
            l = min(1.0, max(0.0, ((0.3 * r + 0.59 * g + 0.11 * b) / 255 - 0.15) / 0.65))
            (l0, c0), (l1, c1) = (stops[0], stops[1]) if l < 0.5 else (stops[1], stops[2])
            t = (l - l0) / (l1 - l0)
            c = tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))
            if veins and (x * 3 + y) % 9 == 0: c = (24, 6, 30)
            out.putpixel((x, y), c + (a,))
    return out


ICONS['dragon_wings'] = dragon_recolor('/home/claude/bm_build/vendor/elytra_item.png', veins=False)
ICONS['grappling_hook'] = grid([
    '..........SS..SS', '...........S.S..', '..........SSSSS.', '...........SSS..', '..........SSSSS.', '.........SS.S.SS',
    '........RR..S...', '.......RR.......', '......RR........', '.....RRR........', '....RR.R........', '...RR..RR.......',
    '..RRRRRRR.......', '..R.....R.......', '..RR...RR.......', '...RRRRR........'],
    {'S': '#b8bec6', 'R': '#8a6a42'})
ICONS['prospector_paxel'] = grid([
    '..CCCCCCC.......', '.CDDDDDDDC......', 'CDDCCCCDDDC.....', 'CDC....CDDDC....', 'CC....CB.CDDC...', '.....CBB..CDC...',
    '....CBB....CC.AA', '...CBB.....AAAAA', '..CBB.....AAAA..', '.CBB.......AA...', 'CBB.............', 'BB..............',
    'SS..............', 'SSS.............', '.SS.............', '................'],
    {'C': '#1e8c84', 'D': '#5fe6d6', 'B': '#6b4a2b', 'A': '#9fe9ff', 'S': '#a8b4bd'})

# ---------------------------------------------------------------- rat sprites (32x32)
def rat(variant):
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OL, FUR, BELLY, PINK, EYE = hexc('#2b2b33'), hexc('#8e8e9a'), hexc('#c4c4cc'), hexc('#f0a0b4'), hexc('#0b0b0f')

    def blob(box, fill):
        x1, y1, x2, y2 = box
        d.ellipse((x1 - 1, y1 - 1, x2 + 1, y2 + 1), fill=OL)
        d.ellipse(box, fill=fill)
    d.line((22, 27, 27, 25, 29, 21, 30, 17), fill=OL, width=3)
    d.line((22, 27, 27, 25, 29, 21, 30, 17), fill=PINK, width=1)
    blob((5, 1, 12, 8), FUR); blob((20, 1, 27, 8), FUR)
    d.ellipse((7, 3, 10, 6), fill=PINK); d.ellipse((22, 3, 25, 6), fill=PINK)
    blob((9, 14, 23, 29), FUR)
    d.ellipse((12, 18, 20, 28), fill=BELLY)
    blob((7, 17, 10, 23), FUR); blob((22, 17, 25, 23), FUR)
    d.ellipse((7, 22, 10, 24), fill=PINK); d.ellipse((22, 22, 25, 24), fill=PINK)
    blob((10, 27, 14, 30), PINK); blob((18, 27, 22, 30), PINK)
    blob((9, 5, 23, 17), FUR)
    d.ellipse((12, 11, 20, 16), fill=BELLY)
    d.rectangle((12, 8, 13, 9), fill=EYE); d.rectangle((19, 8, 20, 9), fill=EYE)
    d.point((12, 8), fill=(255, 255, 255, 255)); d.point((19, 8), fill=(255, 255, 255, 255))
    d.rectangle((15, 12, 17, 13), fill=PINK)
    for y in (12, 14):
        d.line((5, y, 11, 13), fill=OL); d.line((21, 13, 27, y), fill=OL)
    if variant == 'chef':
        W = hexc('#f6f6f6'); G = hexc('#b9b9c4')
        d.ellipse((9, -3, 23, 6), fill=G); d.ellipse((10, -2, 22, 5), fill=W)
        d.rectangle((11, 3, 21, 6), fill=W); d.line((11, 6, 21, 6), fill=G)
        d.rectangle((12, 16, 20, 18), fill=hexc('#d22b2b'))
    elif variant == 'prof':
        BR = hexc('#4a2c12')
        d.ellipse((10, 6, 15, 11), outline=BR); d.ellipse((17, 6, 22, 11), outline=BR); d.line((15, 8, 17, 8), fill=BR)
        d.polygon([(13, 16), (16, 17), (13, 18)], fill=hexc('#c0262d')); d.polygon([(19, 16), (16, 17), (19, 18)], fill=hexc('#c0262d'))
        d.rectangle((8, 2, 24, 4), fill=hexc('#222222')); d.rectangle((13, 0, 19, 3), fill=hexc('#222222'))
        d.point((24, 5), fill=hexc('#e8b923')); d.point((24, 6), fill=hexc('#e8b923'))
    elif variant == 'lucky':
        GR = hexc('#1f9a3a')
        d.rectangle((9, 4, 23, 6), fill=GR); d.ellipse((11, 5, 21, 9), fill=hexc('#3fcf5a'))
        d.rectangle((11, 16, 21, 27), fill=hexc('#b3202a')); d.ellipse((13, 18, 19, 26), fill=BELLY)
        blob((23, 18, 28, 23), hexc('#f2c230')); d.point((25, 20), fill=hexc('#fff6c0'))
    elif variant == 'soldier':
        IR, IRD = hexc('#c8c8d0'), hexc('#7a7a86')
        d.ellipse((8, 0, 24, 9), fill=IRD); d.ellipse((9, 1, 23, 8), fill=IR)
        d.rectangle((8, 5, 24, 6), fill=IRD)
        d.rectangle((15, -1, 17, 2), fill=hexc('#c0262d')); d.rectangle((14, 0, 18, 1), fill=hexc('#c0262d'))
        d.rectangle((10, 16, 22, 27), fill=hexc('#6f7380')); d.rectangle((12, 18, 20, 26), fill=hexc('#9aa0ad'))
        blob((3, 16, 9, 25), hexc('#8a5a2b')); d.ellipse((5, 19, 7, 22), fill=hexc('#e8b923'))
    elif variant == 'pirate':
        BK = hexc('#151515')
        d.polygon([(4, 6), (16, -1), (28, 6), (22, 4), (16, 5), (10, 4)], fill=BK)
        d.rectangle((9, 1, 23, 5), fill=BK)
        d.rectangle((15, 2, 17, 3), fill=hexc('#f0f0f0'))
        d.rectangle((18, 7, 21, 10), fill=BK); d.line((10, 6, 22, 9), fill=BK)
        d.point((27, 7), fill=hexc('#e8b923')); d.point((27, 8), fill=hexc('#e8b923'))
        d.rectangle((12, 16, 20, 18), fill=hexc('#c0262d'))
    return im


# ---------------------------------------------------------------- 3D hats
def cube(fr, to, tex, faces=('north', 'south', 'east', 'west', 'up', 'down')):
    def cl(v): return max(0.0, min(16.0, v))
    x1, y1, z1 = fr; x2, y2, z2 = to
    uv = {'north': [x1, 16 - y2, x2, 16 - y1], 'south': [x1, 16 - y2, x2, 16 - y1],
          'east': [z1, 16 - y2, z2, 16 - y1], 'west': [z1, 16 - y2, z2, 16 - y1],
          'up': [x1, z1, x2, z2], 'down': [x1, z1, x2, z2]}
    out = {}
    for f in faces:
        u = [cl(v % 16 if v > 16 else v) for v in uv[f]]
        if u[0] == u[2]: u[2] = min(16, u[0] + 1)
        if u[1] == u[3]: u[3] = min(16, u[1] + 1)
        out[f] = {'uv': u, 'texture': '#' + tex}
    return {'from': list(fr), 'to': list(to), 'faces': out}


HATS = {}
HATS['crown'] = ({'g': 'minecraft:block/gold_block', 'r': 'minecraft:block/redstone_block', 'e': 'minecraft:block/emerald_block'}, [
    cube((3, 15, 3), (13, 18, 4), 'g'), cube((3, 15, 12), (13, 18, 13), 'g'),
    cube((3, 15, 4), (4, 18, 12), 'g'), cube((12, 15, 4), (13, 18, 12), 'g'),
    *[cube((x, 18, 3), (x + 1.5, 20, 4), 'g') for x in (3, 7.25, 11.5)],
    *[cube((x, 18, 12), (x + 1.5, 20, 13), 'g') for x in (3, 7.25, 11.5)],
    cube((7, 16, 2.5), (9, 17.5, 3), 'r'), cube((7, 16, 13), (9, 17.5, 13.5), 'e')])
HATS['party_hat'] = ({'p': 'minecraft:block/pink_wool', 'l': 'minecraft:block/lime_wool', 'w': 'minecraft:block/white_wool'}, [
    cube((4, 16, 4), (12, 18, 12), 'p'), cube((5, 18, 5), (11, 20, 11), 'l'), cube((6, 20, 6), (10, 22, 10), 'p'),
    cube((7, 22, 7), (9, 24, 9), 'l'), cube((7.25, 24, 7.25), (8.75, 25.5, 8.75), 'w')])
HATS['top_hat'] = ({'b': 'minecraft:block/black_wool', 'r': 'minecraft:block/red_wool'}, [
    cube((1, 15, 1), (15, 16, 15), 'b'), cube((4, 16, 4), (12, 18, 12), 'r'), cube((4, 18, 4), (12, 25, 12), 'b')])
HATS['halo'] = ({'g': 'minecraft:block/glowstone'}, [
    cube((3, 21, 3), (13, 22, 4), 'g'), cube((3, 21, 12), (13, 22, 13), 'g'),
    cube((3, 21, 4), (4, 22, 12), 'g'), cube((12, 21, 4), (13, 22, 12), 'g')])
HATS['pirate_hat'] = ({'b': 'minecraft:block/black_wool', 'w': 'minecraft:block/bone_block_side', 'y': 'minecraft:block/gold_block'}, [
    cube((-1, 15, 2), (17, 16, 14), 'b'), cube((3, 16, 3), (13, 20, 13), 'b'),
    cube((-1, 16, 2), (17, 18, 3), 'b'), cube((-1, 16, 13), (17, 18, 14), 'b'),
    cube((7, 17, 2.5), (9, 19, 3), 'w'), cube((3, 16, 2.9), (13, 16.5, 3.1), 'y')])
HATS['minish_cap'] = ({'g': 'minecraft:block/lime_wool', 'd': 'minecraft:block/green_wool', 'w': 'minecraft:block/white_wool'}, [
    cube((3, 14, 3), (13, 18, 13), 'g'), cube((4, 18, 6), (12, 20, 14), 'g'), cube((5, 18, 13), (11, 19, 17), 'd'),
    cube((6, 16, 17), (10, 18, 20), 'd'), cube((7, 13, 19), (9, 16, 21), 'd'), cube((3, 14, 2.5), (13, 15, 3), 'w')])
HATS['lens_goggles'] = ({'c': 'minecraft:block/copper_block', 'k': 'minecraft:block/black_wool', 'l': 'minecraft:block/light_blue_stained_glass'}, [
    cube((-0.5, 9, -0.5), (16.5, 11, 0.5), 'k'), cube((-0.5, 9, 15.5), (16.5, 11, 16.5), 'k'),
    cube((-0.5, 9, 0.5), (0.5, 11, 15.5), 'k'), cube((15.5, 9, 0.5), (16.5, 11, 15.5), 'k'),
    cube((2, 7.5, -1.5), (7, 12.5, -0.5), 'c'), cube((9, 7.5, -1.5), (14, 12.5, -0.5), 'c'),
    cube((3, 8.5, -1.75), (6, 11.5, -1.5), 'l'), cube((10, 8.5, -1.75), (13, 11.5, -1.5), 'l')])

GUI_3D = {'gui': {'rotation': [30, 225, 0], 'translation': [0, -3, 0], 'scale': [0.7, 0.7, 0.7]},
          'ground': {'rotation': [0, 0, 0], 'translation': [0, -4, 0], 'scale': [0.5, 0.5, 0.5]},
          'fixed': {'rotation': [0, 180, 0], 'translation': [0, -4, 0], 'scale': [0.8, 0.8, 0.8]},
          'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, -1, 0], 'scale': [0.375, 0.375, 0.375]},
          'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, -2, 0], 'scale': [0.4, 0.4, 0.4]}}


# ================================================================ 3D RATS (block-model figures on the rat traders, face = model north)
RAT_TEX = {'g': 'minecraft:block/gray_wool', 'l': 'minecraft:block/light_gray_wool', 'p': 'minecraft:block/pink_wool',
           'k': 'minecraft:block/black_wool', 'w': 'minecraft:block/white_wool', 'r': 'minecraft:block/red_wool',
           'y': 'minecraft:block/gold_block', 'b': 'minecraft:block/brown_wool', 'd': 'minecraft:block/green_wool',
           'e': 'minecraft:block/lime_wool', 's': 'minecraft:block/iron_block', 'o': 'minecraft:block/stripped_oak_log'}
RAT_BASE = [
    cube((5, 0, 6), (7, 1, 9), 'p'), cube((9, 0, 6), (11, 1, 9), 'p'),                       # feet
    cube((4.5, 1, 6.5), (11.5, 6, 11), 'g'), cube((6, 2, 6.4), (10, 6, 6.5), 'l'),            # haunches + belly
    cube((5, 6, 7), (11, 11, 10.5), 'g'), cube((6.5, 6, 6.9), (9.5, 10.5, 7), 'l'),           # torso + chest fur
    cube((3.5, 6.5, 7.5), (5, 10, 9), 'g'), cube((11, 6.5, 7.5), (12.5, 10, 9), 'g'),         # arms
    cube((3.5, 5.5, 7.5), (5, 6.5, 9), 'p'), cube((11, 5.5, 7.5), (12.5, 6.5, 9), 'p'),       # paws
    cube((5, 11, 6), (11, 16, 10.5), 'g'),                                                     # head
    cube((6.5, 11.5, 4), (9.5, 14, 6), 'l'), cube((7.3, 13, 3.5), (8.7, 14, 4), 'p'),         # snout + nose
    cube((5.8, 14, 5.9), (7, 15, 6), 'k'), cube((9, 14, 5.9), (10.2, 15, 6), 'k'),            # eyes
    cube((3.8, 15, 7.5), (6.3, 18, 8.5), 'g'), cube((4.3, 15.5, 7.4), (5.8, 17.5, 7.5), 'p'),  # ears
    cube((9.7, 15, 7.5), (12.2, 18, 8.5), 'g'), cube((10.2, 15.5, 7.4), (11.7, 17.5, 7.5), 'p'),
    cube((3.5, 12.8, 4.8), (6.5, 12.9, 4.9), 'w'), cube((9.5, 12.8, 4.8), (12.5, 12.9, 4.9), 'w'),   # whiskers
    cube((7.5, 1, 11), (8.5, 2, 14), 'p'), cube((7.5, 0.5, 14), (8.5, 1.5, 17), 'p')]        # tail
RAT_KIT = {
    'chef': [cube((5.2, 16, 6.2), (10.8, 17.5, 10.3), 'w'), cube((4.5, 17.5, 5.5), (11.5, 20.5, 11), 'w'),
             cube((5.8, 3, 6.3), (10.2, 10, 6.4), 'w'), cube((5.5, 10.4, 6.8), (10.5, 11.2, 7.2), 'r')],
    'prof': [cube((5.6, 13.7, 5.8), (7.2, 15.3, 5.85), 'y'), cube((8.8, 13.7, 5.8), (10.4, 15.3, 5.85), 'y'),
             cube((7.2, 14.4, 5.8), (8.8, 14.6, 5.85), 'y'), cube((7, 10.3, 6.7), (9, 11.3, 7), 'r'),
             cube((12, 6, 6.5), (13.5, 9.5, 9), 'b')],
    'lucky': [cube((4.8, 16, 5.8), (11.2, 17, 10.7), 'd'), cube((5.8, 17, 6.8), (10.2, 19, 9.8), 'd'),
              cube((5.8, 17, 6.75), (10.2, 17.6, 6.8), 'y'), cube((4.8, 6, 6.85), (11.2, 10.8, 10.65), 'd'),
              cube((12.3, 9.5, 7.6), (14.3, 11.5, 7.8), 'e'), cube((13.1, 7, 7.6), (13.5, 9.5, 7.8), 'e')],
    'pirate': [cube((4, 16, 5), (12, 17, 11.5), 'k'), cube((5.5, 17, 6), (10.5, 19, 10), 'k'),
               cube((4, 16.9, 4.9), (12, 17.2, 5), 'y'), cube((8.9, 13.8, 5.85), (10.3, 15.2, 5.95), 'k'),
               cube((4.8, 6, 6.8), (11.2, 11, 10.7), 'r'), cube((12.3, 4, 7.8), (12.8, 11, 8.2), 's')],
    'soldier': [cube((4.6, 15, 5.6), (11.4, 18, 10.9), 's'), cube((7.5, 18, 6), (8.5, 19.5, 10.5), 'r'),
                cube((5, 6.5, 6.6), (11, 10.8, 10.8), 's'), cube((12.6, 0, 7.9), (13.4, 20, 8.7), 'o'),
                cube((12.5, 20, 7.8), (13.5, 22, 8.8), 's')],
}
# ================================================================ Sir Croaksworth, the mustachioed frog (face = model north)
FROG_TEX = {'e': 'minecraft:block/lime_wool', 'd': 'minecraft:block/green_wool', 'c': 'minecraft:block/sandstone_top',
            'w': 'minecraft:block/white_wool', 'k': 'minecraft:block/black_wool', 'r': 'minecraft:block/red_wool',
            'p': 'minecraft:block/pink_wool', 'y': 'minecraft:block/gold_block'}
FROG = [
    cube((4, 1, 5), (12, 6, 13), 'e'), cube((4.5, 1.2, 4.9), (11.5, 5, 5), 'c'),                 # body + cream belly
    cube((3.5, 6, 4), (12.5, 9, 11), 'e'), cube((4, 6, 3.9), (12, 6.6, 4), 'c'),                  # wide flat head + chin
    cube((4, 6.6, 3.9), (12, 6.9, 4), 'p'),                                                       # mouth line
    cube((3.5, 9, 5), (6.5, 11.5, 8), 'w'), cube((9.5, 9, 5), (12.5, 11.5, 8), 'w'),              # eyes
    cube((4.2, 9.6, 4.9), (5.8, 11, 5), 'k'), cube((10.2, 9.6, 4.9), (11.8, 11, 5), 'k'),         # pupils
    cube((3.4, 11.3, 4.9), (6.6, 11.8, 8.1), 'e'), cube((9.4, 11.3, 4.9), (12.6, 11.8, 8.1), 'e'),  # sleepy lids
    cube((7.1, 8.2, 3.9), (7.5, 8.5, 4), 'k'), cube((8.5, 8.2, 3.9), (8.9, 8.5, 4), 'k'),         # nostrils
    # the magnificent handlebar moustache
    cube((6.4, 7, 3.3), (9.6, 8, 4), 'k'), cube((4.6, 6.8, 3.4), (6.4, 7.7, 3.9), 'k'), cube((9.6, 6.8, 3.4), (11.4, 7.7, 3.9), 'k'),
    cube((3.6, 7.2, 3.5), (4.6, 8.8, 3.9), 'k'), cube((11.4, 7.2, 3.5), (12.4, 8.8, 3.9), 'k'),
    cube((3.2, 8.5, 3.5), (4.0, 9.3, 3.9), 'k'), cube((12.0, 8.5, 3.5), (12.8, 9.3, 3.9), 'k'),
    cube((6.5, 4.6, 4.6), (9.5, 5.8, 4.9), 'r'), cube((7.6, 4.8, 4.4), (8.4, 5.6, 4.6), 'y'),    # bow tie + gold pin
    cube((4, 0, 4), (5.5, 3, 5.5), 'd'), cube((10.5, 0, 4), (12, 3, 5.5), 'd'),                  # front legs
    cube((3.3, 0, 2.8), (6.2, 0.5, 4.5), 'd'), cube((9.8, 0, 2.8), (12.7, 0.5, 4.5), 'd'),        # front feet
    cube((2.5, 0.5, 8), (4.5, 4, 13), 'd'), cube((11.5, 0.5, 8), (13.5, 4, 13), 'd'),            # haunches
    cube((1.5, 0, 6.5), (4.5, 0.5, 10), 'd'), cube((11.5, 0, 6.5), (14.5, 0.5, 10), 'd'),        # back feet
    cube((5, 6, 11.3), (7, 6.2, 12.6), 'd'), cube((9, 6, 11.1), (10.6, 6.2, 12.4), 'd'),          # spots
    cube((6.6, 4, 13), (8, 5.4, 13.1), 'd')]
HATS['frog3d'] = (FROG_TEX, FROG)
# 1.10: the companion wears a little knight's helm matching the helmet you give him
HELM_TEX = {'leather': 'minecraft:block/brown_wool', 'chain': 'minecraft:block/light_gray_concrete', 'iron': 'minecraft:block/iron_block',
            'gold': 'minecraft:block/gold_block', 'diamond': 'minecraft:block/diamond_block', 'netherite': 'minecraft:block/netherite_block',
            'turtle': 'minecraft:block/lime_terracotta', 'copper': 'minecraft:block/copper_block'}
for _m, _t in HELM_TEX.items():
    _helm = [cube((3.3, 8.4, 3.7), (12.7, 9.2, 11.3), 'h'), cube((6.6, 9.2, 4.6), (9.4, 10.8, 11.2), 'h'),
             cube((3.4, 9.2, 8.2), (12.6, 10.4, 11.2), 'h'), cube((7.7, 8.0, 3.5), (8.3, 9.2, 3.7), 'h')]
    if _m in ('iron', 'gold', 'diamond', 'netherite', 'copper'): _helm.append(cube((7.6, 10.8, 5.5), (8.4, 12.4, 10.5), 'r'))
    if _m == 'leather': _helm.append(cube((9.6, 10.4, 9.0), (10.2, 13.2, 9.6), 'w'))
    HATS[f'frog3d_{_m}'] = (dict(FROG_TEX, h=_t), FROG + _helm)
# 1.12 field traders: the Ember Rat (Nether) and the Void Rat (End)
RAT_KIT['ember'] = [cube((4.8, 14.4, 5.8), (11.2, 15.0, 6.0), 'k'), cube((5.4, 13.8, 5.7), (7.4, 15.4, 5.85), 'o'),
                    cube((8.6, 13.8, 5.7), (10.6, 15.4, 5.85), 'o'), cube((5.8, 3, 6.3), (10.2, 10, 6.4), 'b'),
                    cube((5.6, 10.2, 6.3), (10.4, 10.8, 6.6), 'k')]
RAT_KIT['void'] = [cube((5.8, 14, 5.85), (7, 15, 5.95), 'v'), cube((9, 14, 5.85), (10.2, 15, 5.95), 'v'),
                   cube((1.5, 15, 8), (2.5, 16, 9), 'v'), cube((13.5, 12, 7), (14.5, 13, 8), 'v'), cube((7.5, 19, 7.5), (8.5, 20, 8.5), 'v')]
RAT_TEXV = {'ember': dict(RAT_TEX, g='minecraft:block/black_wool', l='minecraft:block/gray_wool', p='minecraft:block/orange_wool',
                          o='minecraft:block/shroomlight', b='minecraft:block/brown_wool'),
            'void': dict(RAT_TEX, g='minecraft:block/black_concrete', l='minecraft:block/purple_wool', p='minecraft:block/magenta_wool',
                         v='minecraft:block/amethyst_block')}
RAT_DISPLAY = dict(GUI_3D, fixed={'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]})


# ---------------------------------------------------------------- 1.11 POSES (flip-book animation via custom_model_data)
def _tex(c): return list(c['faces'].values())[0]['texture'][1:]


def _mv(c, dx=0.0, dy=0.0, dz=0.0):
    (x1, y1, z1), (x2, y2, z2) = c['from'], c['to']
    return cube((x1 + dx, y1 + dy, z1 + dz), (x2 + dx, y2 + dy, z2 + dz), _tex(c))


FROG_UPPER = set(range(0, 22)) | {30, 31, 32}         # body, head, face, moustache, bow tie, spots


def frog_pose(pose):
    """sit / breathe / blink / crouch / leap -> (cubes, dy, dz of the head for the helm)"""
    if pose == 'sit': return list(FROG), 0.0, 0.0
    if pose == 'breathe':
        return [_mv(c, dy=0.2) if i in FROG_UPPER else c for i, c in enumerate(FROG)] + \
               [cube((5.2, 5.1, 3.4), (10.8, 6.4, 4.3), 'c')], 0.2, 0.0
    if pose == 'blink':
        out = [c for i, c in enumerate(FROG) if i not in (7, 8)]
        return out + [cube((3.45, 9.05, 4.85), (6.55, 11.45, 4.95), 'e'), cube((9.45, 9.05, 4.85), (12.55, 11.45, 4.95), 'e')], 0.0, 0.0
    if pose == 'crouch':
        out = [_mv(c, dy=-0.8) if i in FROG_UPPER else c for i, c in enumerate(FROG) if i not in (22, 23, 26, 27)]
        out += [cube((4, 0, 4), (5.5, 2.2, 5.5), 'd'), cube((10.5, 0, 4), (12, 2.2, 5.5), 'd'),
                cube((2.5, 0.5, 8), (4.5, 3.2, 13), 'd'), cube((11.5, 0.5, 8), (13.5, 3.2, 13), 'd')]
        return out, -0.8, 0.0
    if pose == 'leap':
        out = [_mv(c, dy=1.6, dz=-0.6) if i in FROG_UPPER else c for i, c in enumerate(FROG) if i not in range(22, 30)]
        out += [cube((4, 0.8, 2.6), (5.5, 3.6, 4.1), 'd'), cube((10.5, 0.8, 2.6), (12, 3.6, 4.1), 'd'),        # front legs reach
                cube((3.3, 0, 1.2), (6.2, 0.6, 2.9), 'd'), cube((9.8, 0, 1.2), (12.7, 0.6, 2.9), 'd'),
                cube((2.5, 1.2, 11.5), (4.5, 3.2, 15.5), 'd'), cube((11.5, 1.2, 11.5), (13.5, 3.2, 15.5), 'd'),  # back legs kick
                cube((2.0, 0, 15), (4.6, 0.8, 18.5), 'd'), cube((11.4, 0, 15), (14.0, 0.8, 18.5), 'd')]
        return out, 1.6, -0.6
    raise ValueError(pose)


def frog_helm(m, dy, dz):
    if m == 'none': return []
    h = [cube((3.3, 8.4, 3.7), (12.7, 9.2, 11.3), 'h'), cube((6.6, 9.2, 4.6), (9.4, 10.8, 11.2), 'h'),
         cube((3.4, 9.2, 8.2), (12.6, 10.4, 11.2), 'h'), cube((7.7, 8.0, 3.5), (8.3, 9.2, 3.7), 'h')]
    if m in ('iron', 'gold', 'diamond', 'netherite', 'copper'): h.append(cube((7.6, 10.8, 5.5), (8.4, 12.4, 10.5), 'r'))
    if m == 'leather': h.append(cube((9.6, 10.4, 9.0), (10.2, 13.2, 9.6), 'w'))
    return [_mv(c, dy=dy, dz=dz) for c in h]


FROG_POSE_NAMES = ['sit', 'breathe', 'blink', 'crouch', 'leap']
FROG_HELMS = ['none'] + list(HELM_TEX)
for _p in FROG_POSE_NAMES:
    _cubes, _dy, _dz = frog_pose(_p)
    for _m in FROG_HELMS:
        HATS[f'frogp_{_p}_{_m}'] = (dict(FROG_TEX, h=HELM_TEX.get(_m, 'minecraft:block/iron_block')), _cubes + frog_helm(_m, _dy, _dz))


def rat_pose(v, pose):
    base, kit = list(RAT_BASE), list(RAT_KIT[v])
    if pose == 'sniff':
        head = {10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
        b = [_mv(c, dy=-0.5, dz=-0.5) if i in head else c for i, c in enumerate(base)]
        b[11], b[12] = _mv(b[11], dz=-0.3), _mv(b[12], dz=-0.4)
        k = [_mv(c, dy=-0.5, dz=-0.5) if c['from'][1] >= 13.5 and c['from'][0] < 12 else c for c in kit]
        return b + k
    if pose == 'ears' and v == 'void':          # the Void Rat's ears blink to odd places
        b = [(_mv(c, dx=3.0, dy=2.5) if i in (15, 16) else _mv(c, dx=-1.0, dy=3.5, dz=3.0) if i in (17, 18) else c) for i, c in enumerate(base)]
        return b + kit
    if pose == 'ears':
        b = [(_mv(c, dx=-0.5, dy=0.6) if i in (15, 16) else _mv(c, dx=0.5, dy=0.6) if i in (17, 18) else c) for i, c in enumerate(base)]
        return b + kit
    if pose == 'tail':
        b = [c for i, c in enumerate(base) if i not in (21, 22)]
        return b + kit + [cube((8.5, 1, 11), (9.5, 2, 13.5), 'p'), cube((9.2, 1.5, 13), (12.5, 2.5, 14), 'p'), cube((12, 2.2, 12), (13, 3.5, 13.5), 'p')]
    raise ValueError(pose)


RAT_POSES = ['sniff', 'ears', 'tail']
for _v in RAT_KIT:
    for _p in RAT_POSES:
        HATS[f'rat3dp_{_v}_{_p}'] = (RAT_TEXV.get(_v, RAT_TEX), rat_pose(_v, _p))
HATS['statue_void_rat'] = (dict(RAT_TEXV['void'], q='minecraft:block/obsidian', u='minecraft:block/purpur_block'),
                           [cube((2, 0, 2), (14, 1, 14), 'q'), cube((3, 1, 3), (13, 3, 13), 'u')] +
                           [_mv(c, dy=3) for c in RAT_BASE + RAT_KIT['void']])
for _v, _kit in RAT_KIT.items():
    HATS[f'rat3d_{_v}'] = (RAT_TEXV.get(_v, RAT_TEX), RAT_BASE + _kit)


HANDHELD_EXTRA = set()       # item icons drawn held like a tool (later phases add to these)
DISPLAY_3D_EXTRA = ()        # 3D model name prefixes shown at display-entity scale
TEXTURE_MODS = []            # modules with textures() -> {name: PIL image} for assets/bm/textures/block
LANG = {}                    # extra en_us entries (death messages...)


def wj(rel, obj):
    with open(p(*rel.split('/')), 'w') as f:
        json.dump(obj, f, indent=1)


def build(out_dir):
    global OUT
    OUT = out_dir
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    wj('pack.mcmeta', {'pack': {'description': [{'text': 'Black Market ', 'color': 'dark_purple', 'bold': True},
                                                {'text': 'textures & models (Java 26.3)', 'color': 'gray'}],
                                'min_format': [97, 1], 'max_format': 97}})
    import phase18
    import phase22
    import phase24
    handheld = {'frying_pan', 'rubber_chicken'} | phase18.HANDHELD | phase22.HANDHELD | phase24.HANDHELD | HANDHELD_EXTRA
    for name, im in phase24.textures().items():                      # 1.14: crystal + alien block-atlas textures
        im.save(p('assets', 'bm', 'textures', 'block', name + '.png'))
    HATS.update(phase24.models())
    import phase25                                                     # 1.15: Donado, the Donadians (replace the grey alien3d)
    for name, im in phase25.textures().items():
        im.save(p('assets', 'bm', 'textures', 'block', name + '.png'))
    HATS.update(phase25.models())
    for mod in TEXTURE_MODS:                                           # 2.13+: later phases' block-atlas textures
        for name, im in mod.textures().items():
            im.save(p('assets', 'bm', 'textures', 'block', name + '.png'))
    for name, im in ICONS.items():
        im.save(p('assets', 'bm', 'textures', 'item', name + '.png'))
        wj(f'assets/bm/models/item/{name}.json', {'parent': 'minecraft:item/handheld' if name in handheld else 'minecraft:item/generated',
                                                    'textures': {'layer0': f'bm:item/{name}'}})
        wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
    for v in ('chef', 'prof', 'lucky', 'pirate', 'soldier'):
        rat(v).save(p('assets', 'bm', 'textures', 'item', f'rat_{v}.png'))
        wj(f'assets/bm/models/item/rat_{v}.json', {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'bm:item/rat_{v}'}})
        wj(f'assets/bm/items/rat_{v}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/rat_{v}'}})
    for name, (tex, els) in HATS.items():
        t = dict(tex); t['particle'] = list(tex.values())[0]
        wj(f'assets/bm/models/item/{name}.json', {'textures': t, 'elements': els, 'display': RAT_DISPLAY if name.startswith(('rat3d', 'trophy3d_', 'frog3d', 'frogp_', 'statue_') + phase24.DISPLAY_3D + phase25.DISPLAY_3D + DISPLAY_3D_EXTRA) else GUI_3D})
        wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
    # 1.11 flip-book poses: the item definitions choose a pose (and the frog's helm) from custom_model_data strings
    def mdl(n): return {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
    def helm_sel(pose): return {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 1,
                                'cases': [{'when': m, 'model': mdl(f'frogp_{pose}_{m}')} for m in FROG_HELMS], 'fallback': mdl(f'frogp_{pose}_none')}
    wj('assets/bm/items/frog.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                               'cases': [{'when': pz, 'model': helm_sel(pz)} for pz in FROG_POSE_NAMES], 'fallback': helm_sel('sit')}})
    for v in RAT_KIT:
        wj(f'assets/bm/items/rat3d_{v}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                         'cases': [{'when': pz, 'model': mdl(f'rat3dp_{v}_{pz}')} for pz in RAT_POSES],
                                                         'fallback': mdl(f'rat3d_{v}')}})
    for name, d in phase25.item_defs(mdl).items():                   # Donado's pose x helmet, the Donadians' idle poses
        wj(f'assets/bm/items/{name}.json', d)
    # legendary elytra wings (equipment asset) + death message
    gold_recolor('/home/claude/bm_build/vendor/elytra_wings.png').save(p('assets', 'bm', 'textures', 'entity', 'equipment', 'wings', 'golden_wings.png'))
    wj('assets/bm/equipment/golden_wings.json', {'layers': {'wings': [{'texture': 'bm:golden_wings'}]}})
    dragon_recolor('/home/claude/bm_build/vendor/elytra_wings.png').save(p('assets', 'bm', 'textures', 'entity', 'equipment', 'wings', 'dragon_wings.png'))
    wj('assets/bm/equipment/dragon_wings.json', {'layers': {'wings': [{'texture': 'bm:dragon_wings'}]}})
    LANG.update({'death.attack.bm.blood_drain': '%1$s was drained by a Blood Moon horror',
                 'death.attack.bm.blood_drain.player': '%1$s was drained dry by %2$s'})
    wj('assets/bm/lang/en_us.json', LANG)
    for hook in POST: hook(sys.modules[__name__])
    # pack icon
    icon = ICONS['token'].resize((64, 64), Image.NEAREST)
    icon.save(p('pack.png'))
    # contact sheet preview
    tiles = [(n, ICONS[n].resize((64, 64), Image.NEAREST)) for n in ICONS] + \
            [(f'rat_{v}', rat(v).resize((96, 96), Image.NEAREST)) for v in ('chef', 'prof', 'lucky', 'pirate', 'soldier')]
    sheet = Image.new('RGBA', (len(tiles) * 100, 110), (54, 48, 60, 255))
    d = ImageDraw.Draw(sheet)
    for i, (n, t) in enumerate(tiles):
        sheet.paste(t, (i * 100 + 2, 2), t); d.text((i * 100 + 2, 98), n, fill=(255, 255, 255, 255))
    return sheet


if __name__ == '__main__':
    PHASE2 = '--phase2' in sys.argv
    import phase17, phase18
    ICONS.update(phase17.icons(grid))
    ICONS.update(phase18.icons(grid))
    import phase22
    ICONS.update(phase22.icons(grid))
    import phase24
    ICONS.update(phase24.icons(grid))
    import phase26
    ICONS.update(phase26.icons(grid))
    import phase28, phase29, phase30          # 1.18: keys, ledger, new goods, auction rats
    phase28.rp(sys.modules[__name__])
    phase29.rp(sys.modules[__name__])
    POST.append(phase29.rp_post)
    import phase32                            # 2.13: the Vorn
    phase32.rp(sys.modules[__name__])
    TEXTURE_MODS.append(phase32)
    import phase33
    phase33.rp(sys.modules[__name__])
    import phase34
    phase34.rp(sys.modules[__name__])
    import phase35
    phase35.rp(sys.modules[__name__])
    import phase36
    phase36.rp(sys.modules[__name__])
    import phase37
    phase37.rp(sys.modules[__name__])
    import phase38
    phase38.rp(sys.modules[__name__])
    import phase39
    phase39.rp(sys.modules[__name__])
    import phase41
    phase41.rp(sys.modules[__name__])
    import phase42
    phase42.rp(sys.modules[__name__])
    import phase43
    phase43.rp(sys.modules[__name__])
    import phase44
    phase44.rp(sys.modules[__name__])
    import phase45
    phase45.rp(sys.modules[__name__])
    import phase46
    phase46.rp(sys.modules[__name__])
    LANG.update({'death.attack.bm.plasma': '%1$s was vaporised by Vorn plasma', 'death.attack.bm.plasma.player': '%1$s was vaporised by %2$s',
                 'death.attack.bm.quake': '%1$s was flattened by a shockwave', 'death.attack.bm.quake.player': '%1$s was flattened by %2$s'})
    if PHASE2:
        import p2.art  # adds Phase 2 icons/models into ICONS and EXTRA
        p2.art.register(sys.modules[__name__])
        import p2.regalia
        p2.regalia.rp(sys.modules[__name__])
    s = build('/home/claude/bm_build/' + ('out_p2' if PHASE2 else 'out') + '/BlackMarket_RP')
    s.save('/home/claude/bm_build/preview/rp_sheet.png')

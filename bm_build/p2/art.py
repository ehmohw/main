"""Phase 2 item art (16x16 pixel icons) for the resource pack. register(G) adds them to gen_rp.ICONS."""
from PIL import Image, ImageDraw
from p2.config import D

KEY = ['................', '................', '...KKKK.........', '..KYYYYK........', '.KYK..KYK.......', '.KY....YK.......',
       '.KYK..KYKKKKKKK.', '..KYYYYKYYYYYYYK', '...KKKK.KKYKKYK.', '.........KYK.KYK', '..........K...K.', '................',
       '................', '................', '................', '................']
VKEY = ['................', '.....KKKKK......', '....KYYYYYK.....', '...KYWKKKYYK....', '...KYK...KYK....', '...KYK...KYK....',
        '...KYYKKKYYK....', '....KYYYYYK.....', '.....KKYKK......', '......KYK.......', '......KYKK......', '......KYYYK.....',
        '......KYKK......', '......KYYK......', '......KKKK......', '................']
BKEY = ['................', '....KKKKKKK.....', '...KYYYYYYYK....', '..KYYKGGGKYYK...', '..KYKGWWGGKYK...', '..KYKGGGGGKYK...',
        '..KYYKGGGKYYK...', '...KYYYYYYYK....', '....KKKYKKK.....', '......KYK.......', '......KYKKK.....', '......KYYYYK....',
        '......KYKKK.....', '......KYYK......', '......KKKK......', '................']
SIGIL = ['................', '......KKKK......', '.....KYYYYK.....', '....KYKKKKYK....', '...KYKWWPPKYK...', '...KYKWPPPKYK...',
         '...KYKPPPPKYK...', '...KYKPPPDKYK...', '....KYKKKKYK....', '.....KYYYYK.....', '......KKKK......', '................',
         '................', '................', '................', '................']
SHARD = ['................', '..........K.....', '.........KSK....', '........KSLK....', '.......KSLLK....', '......KSLLK.....',
         '.....KSLLSK.....', '....KSLLSK......', '....KSLSK.......', '...KSLSK........', '...KSSK.........', '..KSSK..........',
         '..KSK...........', '..KK............', '................', '................']
TROPHY = ['................', '..KKKKKKKKKKKK..', '.KYYYYYYYYYYYYK.', 'KYKYYYGGYYYYKYK.', 'KYKYYGGGGYYYKYK.', 'KYKYYYGGGYYYKYK.',
          '.KYYYYYGYYYYYK..', '..KYYYYYYYYYK...', '...KKYYYYYKK....', '.....KYYYK......', '......KYK.......', '.....KYYYK......',
          '....KYYYYYK.....', '....KKKKKKK.....', '................', '................']
SHOE = ['................', '....KKKKKKKK....', '...KYYYYYYYYK...', '..KYYKKKKKKYYK..', '..KYK......KYK..', '.KYYK......KYYK.',
        '.KYK........KYK.', '.KYYK......KYYK.', '.KYK........KYK.', '.KYYK......KYYK.', '..KYK......KYK..', '..KYK......KYK..',
        '..KKK......KKK..', '................', '................', '................']
# emblems: medal ring (R) + per-boss motif (M)
RING = ['................', '.....KKKKKK.....', '...KKRRRRRRKK...', '..KRRMMMMMMRRK..', '.KRMMMMMMMMMMRK.', '.KRMMMMMMMMMMRK.',
        'KRMMMMMMMMMMMMRK', 'KRMMMMMMMMMMMMRK', 'KRMMMMMMMMMMMMRK', 'KRMMMMMMMMMMMMRK', '.KRMMMMMMMMMMRK.', '.KRMMMMMMMMMMRK.',
        '..KRRMMMMMMRRK..', '...KKRRRRRRKK...', '.....KKKKKK.....', '................']
MOTIF = {
    'brood': ['................', '................', '................', '.....S....S.....', '......S..S......', '...SS.SSSS.SS...',
              '.....SSSSSS.....', '....SSSSSSSS....', '.....SSSSSS.....', '...SS.SSSS.SS...', '......S..S......', '.....S....S.....',
              '................', '................', '................', '................'],
    'frost': ['................', '................', '................', '.......S........', '.....S.S.S......', '......SSS.......',
              '...S.SSSSS.S....', '....SSSSSSS.....', '...S.SSSSS.S....', '......SSS.......', '.....S.S.S......', '.......S........',
              '................', '................', '................', '................'],
    'tide': ['................', '................', '................', '.....S.S.S......', '.....S.S.S......', '.....SSSSS......',
             '.......S........', '.......S........', '.......S........', '.......S........', '.......S........', '......SSS.......',
             '................', '................', '................', '................'],
    'hex': ['................', '................', '................', '......SSSS......', '....SS....SS....', '...S..SSSS..S...',
            '...S.SS..SS.S...', '...S..SSSS..S...', '....SS....SS....', '......SSSS......', '................', '................',
            '................', '................', '................', '................'],
    'keep': ['................', '................', '................', '.....SSSSSS.....', '....SSSSSSSS....', '....S.SSSS.S....',
             '....SSSSSSSS....', '.....SS..SS.....', '......SSSS......', '.....S.SS.S.....', '................', '................',
             '................', '................', '................', '................'],
    'hollow': ['................', '................', '................', '................', '....S..S..S.....', '....SS.SS.SS....',
               '....SSSSSSSS....', '....SSSSSSSS....', '....SSSSSSSS....', '................', '................', '................',
               '................', '................', '................', '................'],
}


def hexc(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def shade(c, f):
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(v * f))) for v in hexc(c)[:3])


def map_tiles():
    """A 48x48 parchment map of the Gilded Roost, cut into nine 16x16 fragments (they tile in a 3x3 grid)."""
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([1, 1, 46, 46], fill=(222, 196, 140, 255), outline=(120, 90, 50, 255))
    for i in range(0, 48, 5):                                  # paper texture
        d.point([(i, (i * 7) % 47), ((i * 3) % 47, i)], fill=(200, 170, 115, 255))
    d.ellipse([28, 6, 42, 20], outline=(150, 110, 40, 255))    # the Roost: a little golden tower
    d.rectangle([32, 10, 38, 18], fill=(230, 180, 30, 255), outline=(140, 100, 20, 255))
    d.polygon([(31, 10), (35, 4), (39, 10)], fill=(250, 220, 80, 255))
    pts = [(6, 40), (10, 36), (14, 37), (18, 32), (22, 30), (24, 26), (28, 24), (31, 21)]
    for x, y in pts: d.point((x, y), fill=(160, 40, 30, 255))  # dotted path
    d.line([(4, 42), (8, 38)], fill=(160, 40, 30, 255)); d.line([(4, 38), (8, 42)], fill=(160, 40, 30, 255))
    d.line([(10, 8), (16, 14)], fill=(90, 130, 60, 255)); d.line([(14, 6), (8, 18)], fill=(90, 130, 60, 255))  # trees
    d.text((3, 2), 'N', fill=(100, 70, 40, 255))
    tiles = {}
    k = 1
    for ty in range(3):
        for tx in range(3):
            t = im.crop((tx * 16, ty * 16, tx * 16 + 16, ty * 16 + 16))
            tiles[k] = t; k += 1
    return tiles, im


def register(G):
    grid, ICONS = G.grid, G.ICONS
    from p2.trophy_models import TEX, models
    for d, els in models(G.cube).items():
        G.HATS[f'trophy3d_{d}'] = (TEX, els)
    for d, cfg in D.items():
        c = cfg['color']
        if d in ('brood', 'frost', 'tide', 'hex', 'keep'):
            ICONS[f'key_{d}'] = grid(KEY, dict(K='#1b1410', Y=c))
        ICONS[f'vkey_{d}'] = grid(VKEY, dict(K='#20180f', Y=shade(c, 1.1), W='#ffffff'))
        ICONS[f'bkey_{d}'] = grid(BKEY, dict(K='#140c08', Y='#d9b44a', G=c, W='#ffffff'))
        if d in MOTIF:
            ring = [list(r) for r in RING]
            for y, row in enumerate(MOTIF[d]):
                for x, ch in enumerate(row):
                    if ch == 'S' and ring[y][x] == 'M': ring[y][x] = 'S'
            ICONS[f'emblem_{d}'] = grid([''.join(r) for r in ring], dict(K='#120c08', R='#d9b44a', M=shade(c, 0.55), S='#f4ecd8'))
    for k, col in enumerate(['#dfe6f0', '#5fd1c8', '#1f4e79'], 1):
        ICONS[f'pearl_sigil_{k}'] = grid(SIGIL, dict(K='#0f1a1f', Y='#5e8f8a', W='#ffffff', P=col, D=shade(col, 0.6)))
    ICONS['hollow_summons'] = grid(SHARD, dict(K='#05060a', S='#3d4b5c', L='#a7b4c6'))
    ICONS['wilfrey_locket'] = grid([                     # 2.4: a silver locket on a fine chain, a white enamel heart inside
        '.....CC..CC.....', '....C..CC..C....', '....C......C....', '.....C....C.....', '......C..C......', '.......CC.......',
        '......SSSS......', '....SSLLLLSS....', '...SLLWWWWLLS...', '..SLLWWRRWWLLS..', '..SLWWRRRRWWLS..', '..SLWWWRRWWWLS..',
        '...SLWWWWWWLS...', '....SSLLLLSS....', '......SSSS......', '................'],
        dict(C='#9aa3ad', S='#7d8791', L='#dfe5ea', W='#ffffff', R='#d9b44a'))
    ICONS['lucky_trophy'] = grid(TROPHY, dict(K='#5a3d00', Y='#ffd700', G='#2e8b57'))
    ICONS['horseshoe'] = grid(SHOE, dict(K='#5a3d00', Y='#ffd700'))
    tiles, whole = map_tiles()
    for k, t in tiles.items():
        ICONS[f'lucky_fragment_{k}'] = t
    whole.resize((192, 192), Image.NEAREST).save('/home/claude/bm_build/preview/lucky_map_whole.png')

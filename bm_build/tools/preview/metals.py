"""2.80c: the three metal looks - Leo and Emma in gold, diamond and netherite (front and three-quarter), and every follower's
metal textures - gilded, diamond, netherite - beside the plain one they come from, from a pack.
    python3 tools/preview/metals.py [out.png] [rp root]   (default: out_p2's shipped resource pack)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from PIL import Image, ImageDraw
import draftkit as K
import phase57_art as EM, phase96_art as LE
import math
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(K.OUT, 'metals.png')
rp = sys.argv[2] if len(sys.argv) > 2 else K.REAL_RP
MD = os.path.join(rp, 'assets', 'bm', 'models', 'item')


def put(s, mod, prefix, pose, suffix, parts, yaw=0):
    """put_shipped, but each part wearing its look's model (prefix_part + suffix) where the pack has one"""
    sc = mod.RIG_SCALE; U = sc / 16
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    for p in parts:
        x, y, z = mod.joint(p) if hasattr(mod, 'joint') else mod.PIVOT[p]
        rot, tr = mod.part_xf(pose, p)
        tr = (tr[0] * cy - tr[2] * sy, tr[1], tr[0] * sy + tr[2] * cy) if yaw else tr
        wx, wz = -x * U, -z * U
        nm = f'{prefix}_{p}{suffix}' if os.path.exists(os.path.join(MD, f'{prefix}_{p}{suffix}.json')) else f'{prefix}_{p}'
        s.display(f'bm:item/{nm}', pos=(wx * cy - wz * sy, y * U, wx * sy + wz * cy), scale=sc, left=tuple(rot), translation=tr, yaw=yaw)


tiles = []
for mod, pre, nm, looks in ((LE, 'le', 'Leo', (('Golden Champion', '_c4'), ('Diamond Champion', '_c5'), ('Netherite Champion', '_c6'))),
                            (EM, 'em', 'Emma', (('Gilded Gown', '_d6_m4'), ('Diamond Gown', '_d7_m4'), ('Netherite Gown', '_d8_m4')))):
    for look, suf in looks:
        for view, cam in (('front', (0, 1.5, -6)), ('3/4', (3.5, 1.6, -4.8))):
            s = K.multi_scene(rp)
            put(s, mod, pre, mod.POSES['idle_a'], suf, ('body', 'head', 'armr', 'arml', 'legr', 'legl'))
            tiles.append(K.label(s.render(cam, size=300, span=2.4, center=(0, 1.05 if pre == 'em' else 1.25, 0)), f'{nm} - {view}', look))
K.sheet(tiles, out, cols=6, title='Gold, diamond and netherite looks')
# every follower's metal textures: plain, gilded, diamond, netherite
TB = os.path.join(rp, 'assets', 'bm', 'textures', 'block')
rows = [('Leo', 'le_tunic', '_c4', '_c5', '_c6'), ('Leo (steel)', 'le_steel', '_c4', '_c5', '_c6'), ('Democratus', 'dm_cape', '_c4', '_c5', '_c6'),
        ('Cecil', 'cec_robe', '_c4', '_c5', '_c6'), ('KillerWatt', 'kw_hide', '_c4', '_c5', '_c6'), ('Apophiss', 'apo_scale', '_c4', '_c5', '_c6'),
        ('Tullius', 'tu_coat', '_c4', '_c5', '_c6'), ('Donado', 'don_fur', '_c5', '_c6', '_c7'), ('Pearlman', 'pm_blue', '_c4', '_c5', '_c6'),
        ('Fishy', 'fy_hat', '_c4', '_c5', '_c6'), ('Emma', 'em2_blue', '_d6', '_d7', '_d8'), ('Celi', 'ce_tunic', '_o5', '_o6', '_o7'),
        ('Zib', 'adon_trooper', '_u3', '_u4', '_u5'), ('The Frog', None, 'frog_gold_lt', 'frog_diamond_lt', 'frog_netherite_lt')]
cell = 72
W = 150 + 4 * (cell + 10) + 10
sw = Image.new('RGBA', (W * 2, (len(rows) + 1) // 2 * (cell + 12) + 40), (40, 44, 52, 255)); d = ImageDraw.Draw(sw)
for c, h in enumerate(('plain', 'gilded', 'diamond', 'netherite')):
    for half in (0, 1):
        d.text((half * W + 150 + c * (cell + 10), 10), h, fill=(240, 220, 160))
for i, (who, base, *metals) in enumerate(rows):
    x0, y0 = (i % 2) * W, 30 + (i // 2) * (cell + 12)
    d.text((x0 + 12, y0 + cell // 2 - 6), who, fill=(230, 230, 230))
    names = [base] + ([base + m for m in metals] if base else metals)
    for c, n in enumerate(names):
        if n and os.path.exists(os.path.join(TB, n + '.png')):
            im = Image.open(os.path.join(TB, n + '.png')).convert('RGBA'); im = im.crop((0, 0, min(im.width, 32), min(im.height, 32)))
            sw.alpha_composite(im.resize((cell, cell), Image.NEAREST), (x0 + 150 + c * (cell + 10), y0))
base_im = Image.open(out).convert('RGBA')
full = Image.new('RGBA', (max(base_im.width, sw.width), base_im.height + sw.height), (255, 255, 255, 255))
full.alpha_composite(base_im, (0, 0)); full.alpha_composite(sw, (0, base_im.height)); full.save(out)
print(out)

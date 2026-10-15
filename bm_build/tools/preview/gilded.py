"""2.79a: the gilded looks - Leo and Emma beside their plain selves (front and three-quarter), and every gilded texture
in polished gold beside the plain one it comes from, from a pack.
    python3 tools/preview/gilded.py [out.png] [rp root]   (default: out_p2's shipped resource pack)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import math
from PIL import Image, ImageDraw
import draftkit as K
import phase57_art as EM, phase96_art as LE
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(K.OUT, 'gilded.png')
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
for mod, pre, nm, parts, plain, gold in ((LE, 'le', 'Leo', ('body', 'head', 'armr', 'arml', 'legr', 'legl'), '', '_c4'),
                                        (EM, 'em', 'Emma', ('body', 'head', 'armr', 'arml', 'legr', 'legl'), '_d4_m4', '_d6_m4')):
    for look, suf, sub in (('plain', plain, 'her own' if pre == 'em' else 'his own'), ('gilded', gold, 'Gilded Gown' if pre == 'em' else 'Golden Champion')):
        for view, cam in (('front', (0, 1.5, -6)), ('3/4', (3.5, 1.6, -4.8))):
            s = K.multi_scene(rp)
            put(s, mod, pre, mod.POSES['idle_a'], suf, parts)
            tiles.append(K.label(s.render(cam, size=360, span=2.4, center=(0, 1.05 if pre == 'em' else 1.25, 0)), f'{nm} - {look}, {view}', sub))
K.sheet(tiles, out, cols=4, title='Gilded looks')
# every gilded texture beside its plain self
TB = os.path.join(rp, 'assets', 'bm', 'textures', 'block')
pairs = [('le_tunic', 'le_tunic_c4'), ('dm_cape', 'dm_cape_c4'), ('cec_robe', 'cec_robe_c4'), ('kw_hide', 'kw_hide_c4'), ('apo_scale', 'apo_scale_c4'),
         ('tu_coat', 'tu_coat_c4'), ('don_fur', 'don_fur_c5'), ('pm_blue', 'pm_blue_c4'), ('fy_hat', 'fy_hat_c4'), ('em2_blue', 'em2_blue_d6'),
         ('ce_tunic', 'ce_tunic_o5'), ('adon_trooper', 'adon_trooper_u3'), (None, 'frog_gild_lt'), (None, 'frog_gild_dk')]
cell = 96
sw = Image.new('RGBA', (len(pairs) * (cell * 2 + 12) + 12, cell + 40), (40, 44, 52, 255)); d = ImageDraw.Draw(sw); x = 12
for a, b in pairs:
    for i, n in enumerate((a, b)):
        if n and os.path.exists(os.path.join(TB, n + '.png')):
            im = Image.open(os.path.join(TB, n + '.png')).convert('RGBA'); im = im.crop((0, 0, min(im.width, 32), min(im.height, 32)))
            sw.alpha_composite(im.resize((cell, cell), Image.NEAREST), (x + i * cell, 8))
    d.text((x, cell + 14), b, fill=(240, 220, 160)); x += cell * 2 + 12
base = Image.open(out).convert('RGBA')
full = Image.new('RGBA', (max(base.width, sw.width), base.height + sw.height), (255, 255, 255, 255))
full.alpha_composite(base, (0, 0)); full.alpha_composite(sw, (0, base.height)); full.save(out)
print(out)

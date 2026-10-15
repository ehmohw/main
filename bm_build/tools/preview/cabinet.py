"""A cutaway render of Fishy's hall (the Cabinet of Curiosities), straight from the commands that build it.

    python3 tools/preview/cabinet.py [out.png] [wing]

Reads out_p2's p145/hall/build.mcfunction (fill / setblock, the case and label summons), textures the blocks from the
26.3 client jar's assets (extracted at /home/claude/mc263/client - tools/setup_test_env.sh fetches it) and the cases'
icons from out_p2's resource pack. The roof and the near (south and east) walls are cut down so the room shows; the
wing given (default: the Hollow) is drawn as if half its exhibits had been shown.
"""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BMB = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, BMB)
import cabinet_data as CAB                                     # noqa: E402

TEX = '/home/claude/mc263/client/assets/minecraft/textures/block/'
RP = os.path.join(BMB, 'out_p2', 'BlackMarket_RP', 'assets', 'bm')
DP = os.path.join(BMB, 'out_p2', 'BlackMarket_DP', 'data', 'bm')
A, B, C = 22, 11, 26                                           # (px per block: screen x, screen y per x/z, screen y per y)

# block -> (top texture, side texture, height in 16ths, see-through)
BLOCKS = {
    'dark_oak_planks': ('dark_oak_planks', 'dark_oak_planks', 16, False),
    'polished_deepslate': ('polished_deepslate', 'polished_deepslate', 16, False),
    'polished_blackstone_bricks': ('polished_blackstone_bricks', 'polished_blackstone_bricks', 16, False),
    'red_carpet': ('red_wool', 'red_wool', 1, False),
    'gold_block': ('gold_block', 'gold_block', 16, False),
    'bookshelf': ('oak_planks', 'bookshelf', 16, False),
    'stripped_dark_oak_log': ('stripped_dark_oak_log_top', 'stripped_dark_oak_log', 16, False),
    'smooth_quartz': ('quartz_block_bottom', 'quartz_block_bottom', 16, False),
    'sea_lantern': ('sea_lantern', 'sea_lantern', 16, False),
    'dark_oak_slab': ('dark_oak_planks', 'dark_oak_planks', 8, False),
}
for col in ('cyan', 'light_blue', 'lime', 'magenta', 'orange', 'pink', 'purple', 'yellow'):
    BLOCKS[f'{col}_stained_glass'] = (f'{col}_stained_glass', f'{col}_stained_glass', 16, True)


def tex(name, cache={}):
    if name not in cache:
        im = Image.open(TEX + name + '.png').convert('RGBA')
        cache[name] = im.crop((0, 0, 16, 16))                # (animated textures: the first frame)
    return cache[name]


def P(x, y, z):
    return ((x - z) * A, (x + z) * B - y * C)


def face(canvas, im, p0, e1, e2, shade, ox, oy):
    """im (16x16) onto the parallelogram p0 + s*e1 + t*e2 (s, t in 0..1), darkened by shade."""
    xs = [p0[0], p0[0] + e1[0], p0[0] + e2[0], p0[0] + e1[0] + e2[0]]
    ys = [p0[1], p0[1] + e1[1], p0[1] + e2[1], p0[1] + e1[1] + e2[1]]
    x0, y0, x1, y1 = int(min(xs)) - 1, int(min(ys)) - 1, int(max(xs)) + 2, int(max(ys)) + 2
    det = e1[0] * e2[1] - e1[1] * e2[0]
    if abs(det) < 1e-6:
        return
    # output (u, v) -> texture: s = ((u-px)*e2y - (v-py)*e2x)/det, t = ((v-py)*e1x - (u-px)*e1y)/det; texture px = 16 s, 16 t
    px, py = p0[0] - x0, p0[1] - y0
    a, b = 16 * e2[1] / det, -16 * e2[0] / det
    d, e = -16 * e1[1] / det, 16 * e1[0] / det
    c, f = -(a * px + b * py), -(d * px + e * py)
    w, h = x1 - x0, y1 - y0
    big = im.resize((16, 16), Image.NEAREST)
    out = big.transform((w, h), Image.AFFINE, (a, b, c, d, e, f), resample=Image.NEAREST)
    # mask: only inside the parallelogram (the transform repeats edge pixels outside it)
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).polygon([(p0[0] - x0, p0[1] - y0), (p0[0] + e1[0] - x0, p0[1] + e1[1] - y0),
                               (p0[0] + e1[0] + e2[0] - x0, p0[1] + e1[1] + e2[1] - y0), (p0[0] + e2[0] - x0, p0[1] + e2[1] - y0)], fill=255)
    al = out.getchannel('A').point(lambda v: v)
    from PIL import ImageChops
    out.putalpha(ImageChops.multiply(al, m))
    if shade < 1:
        r, g, bb, aa = out.split()
        r, g, bb = (ch.point(lambda v, s=shade: int(v * s)) for ch in (r, g, bb))
        out = Image.merge('RGBA', (r, g, bb, aa))
    canvas.alpha_composite(out, (x0 + ox, y0 + oy))


def parse():
    blocks, slots, labels, others = {}, [], [], []
    for line in open(os.path.join(DP, 'function', 'p145', 'hall', 'build.mcfunction')):
        line = line.strip()
        m = re.match(r'fill (-?\d+) (-?\d+) (-?\d+) (-?\d+) (-?\d+) (-?\d+) minecraft:([a-z_]+)(\[[^\]]*\])?( hollow)?$', line)
        if m:
            x0, y0, z0, x1, y1, z1 = map(int, m.groups()[:6]); b = m.group(7); hollow = bool(m.group(9))
            for x in range(min(x0, x1), max(x0, x1) + 1):
                for y in range(min(y0, y1), max(y0, y1) + 1):
                    for z in range(min(z0, z1), max(z0, z1) + 1):
                        edge = x in (x0, x1) or y in (y0, y1) or z in (z0, z1)
                        blocks[(x, y, z)] = b if (edge or not hollow) else 'air'
            continue
        m = re.match(r'setblock (-?\d+) (-?\d+) (-?\d+) minecraft:([a-z_]+)', line)
        if m:
            blocks[tuple(map(int, m.groups()[:3]))] = m.group(4); continue
        m = re.match(r'summon minecraft:(item_display|text_display) (-?[\d.]+) (-?[\d.]+) (-?[\d.]+) (.*)', line)
        if m:
            kind, x, y, z, nbt = m.group(1), float(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(5)
            if 'bm.cabslot' in nbt:
                slots.append((x, y, z))
            elif 'bm.cablbl' in nbt:
                labels.append((x, y, z))
            else:
                others.append((kind, x, y, z, nbt))
    return blocks, slots, labels, others


def icon_for(iid):
    """the exhibit's flat icon from the resource pack (its layer0), or None for a 3D model."""
    own = os.path.join(RP, 'textures', 'item', iid + '.png')
    if os.path.exists(own):
        return Image.open(own).convert('RGBA')
    try:
        lt = json.dumps(json.load(open(os.path.join(DP, 'loot_table', 'items', iid + '.json'))))
        mdl = re.search(r'item_model\\?"?:\s*\\?"bm:([^"\\]+)', lt).group(1)
        idef = json.load(open(os.path.join(RP, 'items', mdl + '.json')))
        mref = json.dumps(idef)
        mname = re.search(r'"model": "bm:([^"]+)"', mref).group(1)
        mj = json.load(open(os.path.join(RP, 'models', mname + '.json')))
        t = mj.get('textures', {})
        ref = t.get('layer0') or (list(t.values())[0] if t else None)
        if not ref:
            return None
        path = os.path.join(RP, 'textures', ref.split(':')[1] + '.png')
        im = Image.open(path).convert('RGBA')
        if 'layer0' not in t:                                 # (a 3D model: its texture sheet is no icon)
            return None
        return im
    except Exception:
        return None


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'cabinet_279.png')
    wing = sys.argv[2] if len(sys.argv) > 2 else 'hollow'
    blocks, slots, labels, others = parse()
    # (seen from the south-west: x mirrored - u = -x - 1 for a block - so the doorway's west wall and the south wall are
    #  the near ones, cut away, and Fishy's desk stands against the far east wall)
    blocks = {(-k[0] - 1, k[1], k[2]): v for k, v in blocks.items()}
    slots = [(-x, y, z) for x, y, z in slots]
    xs = [k[0] for k in blocks]; zs = [k[2] for k in blocks]; ys = [k[1] for k in blocks]
    X0, X1, Z0, Z1, Y0, Y1 = min(xs), max(xs), min(zs), max(zs), min(ys), max(ys)
    SX, SZ = 294, -237                                         # (the shell's west wall (u) and south wall (z))
    cut = {k for k in blocks if k[1] >= 74 or ((k[2] >= SZ or k[0] >= SX) and k[1] > 68)}
    solid = {k: v for k, v in blocks.items() if v in BLOCKS and k not in cut}
    pts = [P(x, y, z) for x in (X0, X1 + 1) for z in (Z0, Z1 + 1) for y in (Y0, Y1 + 1)]
    mnx, mxx = min(p[0] for p in pts), max(p[0] for p in pts)
    mny, mxy = min(p[1] for p in pts), max(p[1] for p in pts)
    pad = 40
    W, H = int(mxx - mnx) + 2 * pad, int(mxy - mny) + 2 * pad + 60
    ox, oy = int(-mnx + pad), int(-mny + pad + 50)
    img = Image.new('RGBA', (W, H), (24, 22, 30, 255))

    def opaque(k):
        v = solid.get(k)
        return v is not None and not BLOCKS[v][3] and BLOCKS[v][2] == 16

    def draw_block(k, v):
        x, y, z = k
        top, side, h, _see = BLOCKS[v]
        hh = h / 16
        if not opaque((x, y + 1, z)) or h < 16:
            p = P(x, y + hh, z)
            e1 = (P(x + 1, y + hh, z)[0] - p[0], P(x + 1, y + hh, z)[1] - p[1])
            e2 = (P(x, y + hh, z + 1)[0] - p[0], P(x, y + hh, z + 1)[1] - p[1])
            face(img, tex(top), p, e1, e2, 1.0, ox, oy)
        if not opaque((x, y, z + 1)):                         # (south face: z+1)
            p = P(x, y + hh, z + 1)
            e1 = (A, B)                                       # (+x)
            e2 = (0, C * hh)                                  # (down)
            face(img, tex(side).crop((0, 16 - h, 16, 16)).resize((16, 16), Image.NEAREST) if h < 16 else tex(side), p, e1, e2, 0.78, ox, oy)
        if not opaque((x + 1, y, z)):                         # (east face: x+1)
            p = P(x + 1, y + hh, z)
            e1 = (-A, B)                                      # (+z)
            e2 = (0, C * hh)
            face(img, tex(side).crop((0, 16 - h, 16, 16)).resize((16, 16), Image.NEAREST) if h < 16 else tex(side), p, e1, e2, 0.62, ox, oy)

    # the cases' exhibits: half the wing shown (its icons), half veiled
    keys = [k for k, _ids, _r in CAB.EXHIBITS[wing]]
    veiled = Image.open(os.path.join(RP, 'textures', 'item', 'cab_veiled.png')).convert('RGBA')
    shown = {i for i in range(20) if i % 2 == 0}
    sprites = []
    for i, (sx, sy, sz) in enumerate(sorted(slots, key=lambda s: (s[2], s[0]))[:20]):
        ic = icon_for(CAB.EXHIBITS[wing][i][1][0]) if i in shown else None
        if i in shown and ic is None:                         # (a 3D replica: a gold star stands in for its model)
            ic = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
            import math
            pts = [(8 + (7 if j % 2 == 0 else 3) * math.sin(j * math.pi / 5), 8 - (7 if j % 2 == 0 else 3) * math.cos(j * math.pi / 5)) for j in range(10)]
            ImageDraw.Draw(ic).polygon(pts, fill=(255, 205, 60, 255), outline=(150, 100, 20, 255))
        sprites.append(((sx, sy, sz), ic if ic is not None else veiled))
    # painter's order: far to near (x + z), low to high; sprites slotted in by their own depth
    items = [((k[0] + k[2]), k[1], 0, k, v) for k, v in solid.items()]
    items += [((s[0][0] + s[0][2]) - 0.1, s[0][1], 1, s[0], s[1]) for s in sprites]
    for _d, _y, kind, k, v in sorted(items, key=lambda t: (t[0], t[1], t[2])):
        if kind == 0:
            draw_block(k, v)
        else:
            sx, sy = P(*k)
            ic = v.resize((26, 26), Image.NEAREST)
            glow = Image.new('RGBA', (40, 40), (0, 0, 0, 0))
            ImageDraw.Draw(glow).ellipse((2, 2, 38, 38), fill=(255, 235, 170, 70))
            img.alpha_composite(glow, (int(sx + ox - 20), int(sy + oy - 20)))
            img.alpha_composite(ic, (int(sx + ox - 13), int(sy + oy - 13)))
    # Fishy at his desk (a marker - his rig is item displays, not blocks), and the doorway
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
        small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    except Exception:
        font = small = ImageFont.load_default()
    fx, fy = P(280.5, 69.2, -243.5)
    d.ellipse((fx + ox - 9, fy + oy - 9, fx + ox + 9, fy + oy + 9), fill=(255, 160, 64, 255), outline=(60, 30, 0, 255), width=2)
    d.text((fx + ox + 12, fy + oy - 22), 'Fishy (his desk)', fill=(255, 200, 140, 255), font=small)
    gx, gy = P(296, 68, -243.5)
    d.text((gx + ox + 6, gy + oy + 4), '<- the gate from the Lounge', fill=(230, 210, 160, 255), font=small)
    wname = {w: n for w, n, *_ in CAB.WINGS}[wing]
    d.text((16, 10), "FISHY'S CABINET OF CURIOSITIES - the hall", fill=(255, 215, 120, 255), font=font)
    d.text((16, 30), f"{wname} set out: half shown (replicas), half veiled. Roof and near walls cut away.", fill=(220, 200, 160, 255), font=small)
    img.convert('RGB').save(out)
    print(out, img.size)


if __name__ == '__main__':
    main()

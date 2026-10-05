"""Dungeon building kit: a Build subclass with palettes, data markers, containers, trial spawners/vaults and
placers for every puzzle element. Every placer also records what it placed in `self.meta`, which the
verifier (p2/verify.py) uses to prove the puzzles are wired correctly and the gates cannot be bypassed."""
import random
from structures import Build
from nbt import Int, Byte, Double, Float
import items as I
from p2.config import D, OPEN_LIGHT, ADOOR_LIGHT, GATE_H, BIG_W, BIG_H

# horizontal facing helpers -----------------------------------------------------------------------------------
VEC = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}
OPP = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
RIGHT = {'north': 'west', 'south': 'east', 'east': 'north', 'west': 'south'}   # viewer's right when the wall faces <f>
YAW = {'south': 0.0, 'west': 90.0, 'north': 180.0, 'east': -90.0}


def stack_nbt(iid, count=1, slot=None):
    it = I.ITEMS[iid]
    comps = {k: v for k, v in it['comps'].items()}
    s = {'id': it['base'], 'count': Int(count), 'components': comps}
    if slot is not None: s['Slot'] = Byte(slot)
    return s


SOILS = {'minecraft:grass_block', 'minecraft:dirt', 'minecraft:coarse_dirt', 'minecraft:rooted_dirt', 'minecraft:podzol', 'minecraft:mycelium',
         'minecraft:moss_block', 'minecraft:pale_moss_block', 'minecraft:mud', 'minecraft:muddy_mangrove_roots', 'minecraft:farmland'}


class DBuild(Build):
    def __init__(self, d, sx, sy, sz, seed=0):
        super().__init__(sx, sy, sz)
        self.d = d
        self.cfg = D[d]
        self.rnd = random.Random(seed or hash(d) & 0xffff)
        self.meta = {'gates': [], 'big': [], 'sdoors': [], 'xdoors': [], 'puzzles': {}, 'elements': [], 'markers': [],
                     'entrance': None, 'arena': None, 'altar': None, 'plates': [], 'chests': [], 'spawners': [], 'vaults': []}

    # ---------------- palettes
    def pick(self, pal):
        if isinstance(pal, str): return pal
        r = self.rnd.random() * sum(w for _, w in pal)
        for b, w in pal:
            r -= w
            if r <= 0: return b
        return pal[-1][0]

    def fillp(self, x1, y1, z1, x2, y2, z2, pal):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.set(x, y, z, self.pick(pal))

    def shell(self, x1, y1, z1, x2, y2, z2, wall, floor=None, ceil=None):
        self.fill(x1, y1, z1, x2, y2, z2, 'air')
        self.fillp(x1, y1, z1, x2, y1, z2, floor or wall)
        self.fillp(x1, y2, z1, x2, y2, z2, ceil or wall)
        for y in range(y1 + 1, y2):
            for x in range(x1, x2 + 1):
                self.set(x, y, z1, self.pick(wall)); self.set(x, y, z2, self.pick(wall))
            for z in range(z1, z2 + 1):
                self.set(x1, y, z, self.pick(wall)); self.set(x2, y, z, self.pick(wall))

    def carve(self, x1, y1, z1, x2, y2, z2):
        self.fill(x1, y1, z1, x2, y2, z2, 'air')

    def blob(self, cx, cy, cz, rx, ry, rz, wall, floor=None, rough=0.18):
        """Organic cavern: ellipsoid of air inside a rough shell (used for caves/nests)."""
        for x in range(int(cx - rx - 2), int(cx + rx + 3)):
            for y in range(int(cy - ry - 2), int(cy + ry + 3)):
                for z in range(int(cz - rz - 2), int(cz + rz + 3)):
                    if not (0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2]): continue
                    v = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 + ((z - cz) / rz) ** 2
                    if v <= 1.0 - self.rnd.random() * rough:
                        self.set(x, y, z, 'air')
                    elif v <= 1.6 and self.get(x, y, z) in (None,):
                        self.set(x, y, z, self.pick(wall if y > cy - ry * 0.6 or floor is None else floor))

    # ---------------- markers (every Phase 2 marker carries bm.p2 + its dungeon tag)
    def m(self, x, y, z, tags, yaw=0.0, data=None):
        tags = ['bm.p2', f'bm.d_{self.d}'] + list(tags)
        self.marker(x, y, z, tags, yaw)
        if data: self.ents[-1]['nbt']['data'] = data
        self.meta['markers'].append((x, y, z, tags))
        return self.ents[-1]

    def mb(self, x, y, z, tags, data=None):
        """Marker centred in block (x,y,z)."""
        return self.m(x + 0.5, y + 0.5, z + 0.5, tags, 0.0, data)

    # ---------------- signs: sign text colour is a DYE colour (not a text colour) in 26.2
    DYE = {'aqua': 'cyan', 'light_purple': 'magenta', 'gold': 'yellow', 'dark_red': 'red', 'dark_aqua': 'cyan', 'dark_purple': 'purple',
           'dark_gray': 'gray', 'gray': 'light_gray', 'dark_green': 'green', 'green': 'lime', 'dark_blue': 'blue'}

    def sign(self, x, y, z, state, lines, color='black', glow=False):
        super().sign(x, y, z, state, lines, color=self.DYE.get(color, color), glow=glow)

    # ---------------- containers & block entities
    def chest(self, x, y, z, facing, loot=None, items=None, kind='chest'):
        st = f'{kind}[facing={facing}]' if kind != 'barrel' else f'barrel[facing={facing},open=false]'
        if kind == 'chest': st = f'chest[facing={facing},type=single,waterlogged=false]'
        nbt = {'id': f'minecraft:{kind}'}
        if loot: nbt['LootTable'] = loot
        if items: nbt['Items'] = items
        self.set(x, y, z, st, nbt)
        self.meta['chests'].append((x, y, z, loot))
        if loot: self.mb(x, y, z, ['bm.chestm'], data={'loot': loot})      # 2.13: a dungeon reset refills it

    def lectern(self, x, y, z, facing, title, author, pages):
        pages = [p if isinstance(p, dict) else {'text': p} for p in pages]
        book = {'id': 'minecraft:written_book', 'count': Int(1),
                'components': {'minecraft:written_book_content': {'title': title, 'author': author, 'pages': pages}}}
        self.set(x, y, z, f'lectern[facing={facing},has_book=true,powered=false]', {'id': 'minecraft:lectern', 'Book': book, 'Page': Int(0)})

    def trial_spawner(self, x, y, z, config, cooldown=36000, rng=14):
        self.set(x, y, z, 'trial_spawner[ominous=false,trial_spawner_state=inactive]',
                 {'id': 'minecraft:trial_spawner', 'normal_config': f'bm:{self.d}/{config}', 'ominous_config': f'bm:{self.d}/{config}_ominous',
                  'required_player_range': Int(rng), 'target_cooldown_length': Int(cooldown)})
        self.meta['spawners'].append((x, y, z, config))

    def vault(self, x, y, z, facing, key_iid, loot):
        key = stack_nbt(key_iid)
        om = 'true' if key_iid.startswith('bkey_') else 'false'      # victor's vault = ominous, spoils vault = regular
        self.set(x, y, z, f'vault[facing={facing},ominous={om},vault_state=inactive]',
                 {'id': 'minecraft:vault', 'config': {'key_item': key, 'loot_table': loot,
                                                      'activation_range': Double(4.0), 'deactivation_range': Double(4.5)}})
        self.meta['vaults'].append((x, y, z, key_iid, loot, facing))
        self.mb(x, y, z, ['bm.vaultm'])                                   # 2.13: a dungeon reset re-opens it to everyone
        if om == 'true': self.mb(x, y + 1, z, ['bm.vbeacon'])             # 2.13: a sign and a beam of light over every victor's vault

    # ---------------- structural pieces with logic
    def entrance(self, x, y, z):
        self.meta['entrance'] = (x, y, z)
        self.mb(x, y, z, ['bm.entr'])

    def controller(self, x, y, z):
        """One per dungeon: holds puzzle progress (bm.pz), idle timers and resets."""
        self.mb(x, y, z, ['bm.dg'])

    def zone(self, x, y, z):
        self.mb(x, y, z, ['bm.zone_d'])

    def fx(self, x, y, z):
        self.mb(x, y, z, ['bm.dgfx'])

    def gate(self, x, y, z, axis, n, big=False):
        """Gate in a wall plane. axis='x': the gate spans x (wall runs along x), players pass along z.
        Bottom-centre at (x,y,z). Normal gates 3x4; big (arena battle doors) 5x5 and start OPEN."""
        hw, h = (BIG_W, BIG_H) if big else (1, GATE_H)
        blk = ADOOR_LIGHT if big else self.cfg['gate']
        for dw in range(-hw, hw + 1):
            for dy in range(h):
                gx, gz = (x + dw, z) if axis == 'x' else (x, z + dw)
                self.set(gx, y + dy, gz, blk)
        if big:
            self.mb(x, y, z, ['bm.adoor'])
            self.meta['big'].append((x, y, z, axis))
        else:
            self.mb(x, y, z, ['bm.gate', f'bm.g{n}'])
            self.meta['gates'].append((x, y, z, axis, n))

    def sdoor(self, x, y, z, k):
        """Secret 1x2 doorway (dungeon's secret block), opened by the hidden button with the same k."""
        b = self.cfg['secret']
        self.set(x, y, z, b); self.set(x, y + 1, z, b)
        self.mb(x, y, z, ['bm.sdoor', f'bm.sk{k}'])
        self.meta['sdoors'].append((x, y, z, k))

    def drain(self, x, y, z, n):
        """Water in a 7x6x7 box around this marker is drained the moment puzzle n is solved (before its gate opens)."""
        self.mb(x, y, z, ['bm.drain', f'bm.g{n}'])

    def sbutton(self, x, y, z, state, k):
        self.set(x, y, z, state)
        self.mb(x, y, z, ['bm.sbtn', f'bm.sk{k}'])
        self.meta['elements'].append(('sbtn', x, y, z, k))

    def xdoor(self, x, y, z):
        """Arena exit: a 1x2 column of the secret block that opens after victory (a way out that never crosses a puzzle gate)."""
        block = self.cfg['secret']
        self.set(x, y, z, block); self.set(x, y + 1, z, block)
        self.mb(x, y, z, ['bm.xdoor'])
        self.meta['xdoors'].append((x, y, z, block))

    def arena(self, x, y, z, door_axis=None):
        self.mb(x, y, z, ['bm.arena'])
        self.meta['arena'] = (x, y, z)

    def altar(self, x, y, z):
        self.mb(x, y, z, ['bm.altar'])
        self.meta['altar'] = (x, y, z)

    def mspawn(self, x, y, z):
        self.mb(x, y, z, ['bm.mspawn'])

    def perch(self, x, y, z):
        self.mb(x, y, z, ['bm.perch'])

    # ---------------- puzzle controllers + elements
    def pz(self, n, kind, x, y, z, data=None, extra_tags=()):
        self.mb(x, y, z, ['bm.pz', f'bm.pz{n}', f'bm.pzt_{kind}'] + list(extra_tags), data)
        rec = self.meta['puzzles'].setdefault(n, dict(elements=[]))
        rec.update(kind=kind, ctrl=(x, y, z), data=data or {})

    def el(self, n, kind, x, y, z, tags=(), data=None):
        self.mb(x, y, z, ['bm.pe', f'bm.pz{n}', f'bm.pet_{kind}'] + list(tags), data)
        rec = (kind, x, y, z, tuple(tags))
        self.meta['puzzles'].setdefault(n, dict(elements=[]))['elements'].append(rec)
        self.meta['elements'].append(rec)

    def lever(self, n, x, y, z, facing, want, face='wall'):
        self.set(x, y, z, f'lever[face={face},facing={facing},powered=false]')
        self.el(n, 'lever', x, y, z, [f'bm.want{1 if want else 0}'])

    def keypad(self, n, x, y, z, facing, code, legend_color='white'):
        """3 wide x 4 tall button pad on a wall that faces `facing` (players stand on that side).
        (x,y,z) is the top-left button as the player sees it. Layout: 1 2 3 / 4 5 6 / 7 8 9 / C 0 E.
        A legend sign sits directly above the pad; the controller sits behind the pad's centre.
        Every key is a stone-type button: arrows can't press those (they do press wooden buttons)."""
        rx, rz = VEC[RIGHT[facing]]
        nx, nz = VEC[facing]
        keys = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['C', '0', 'E']]
        for row, ks in enumerate(keys):
            for col, k in enumerate(ks):
                bx, bz = x + rx * col, z + rz * col
                by = y - row
                btn = {'C': 'polished_blackstone_button', 'E': 'polished_blackstone_button'}.get(k, 'stone_button')
                self.set(bx, by, bz, f'{btn}[face=wall,facing={facing},powered=false]')
                tag = {'C': 'bm.kclr', 'E': 'bm.kent'}.get(k, f'bm.k{k}')
                self.el(n, 'key', bx, by, bz, [tag])
        lx, lz = x + rx * 1, z + rz * 1
        self.sign(lx, y + 1, lz, f'{self.cfg.get("sign_wood", "dark_oak")}_wall_sign[facing={facing},waterlogged=false]',
                  ['1  2  3', '4  5  6', '7  8  9', 'Clr 0 Ent'], color=legend_color, glow=True)
        # controller lives in the wall block behind the middle of the pad
        cx, cz = x + rx * 1 - nx, z + rz * 1 - nz
        self.pz(n, 'keypad', cx, y - 2, cz, data={'code': Int(int(code)), 'len': Int(len(code))})

    def seq_button(self, n, x, y, z, state, order, sound=None):
        self.set(x, y, z, state)
        tags = [f'bm.s{order}'] + ([f'bm.snd{sound}'] if sound is not None else [])
        self.el(n, 'seq', x, y, z, tags)

    def listen_button(self, n, x, y, z, state):
        self.set(x, y, z, state)
        self.el(n, 'listen', x, y, z)

    def target(self, n, x, y, z, order=None):
        self.set(x, y, z, 'target[power=0]')
        self.el(n, 'target', x, y, z, [f'bm.s{order}'] if order else [])

    def bulb(self, n, x, y, z, i):
        self.set(x, y, z, 'waxed_copper_bulb[lit=false,powered=false]')
        self.el(n, 'bulb', x, y, z, [f'bm.i{i}'])

    def lo_button(self, n, x, y, z, state, i):
        self.set(x, y, z, state)
        self.el(n, 'lo', x, y, z, [f'bm.i{i}'])

    def plate(self, x, y, z, trap, plate='minecraft:polished_blackstone_pressure_plate', safe_under='minecraft:tuff'):
        """Pressure-plate tile at feet level y (floor at y-1, tell-tale block at y-2)."""
        self.set(x, y, z, plate.replace('minecraft:', '') + '[powered=false]' if 'weighted' not in plate else plate.replace('minecraft:', '') + '[power=0]')
        self.set(x, y - 2, z, self.cfg['trap'] if trap else safe_under)
        self.meta['plates'].append((x, y, z, trap))

    def goal(self, n, x, y, z):
        self.el(n, 'goal', x, y, z)

    def start(self, n, x, y, z):
        self.el(n, 'start', x, y, z)

    def altar_offer(self, n, x, y, z, k):
        self.el(n, 'offer', x, y, z, [f'bm.o{k}'])

    def restock(self, x, y, z, iid, slot=13):
        self.mb(x, y, z, ['bm.restock', f'bm.ri_{iid}'], {'slot': Int(slot)})

    def reel(self, n, x, y, z, i):
        self.set(x, y, z, 'gold_block')
        self.el(n, 'reel', x, y, z, [f'bm.i{i}'])

    def pull(self, n, x, y, z, state):
        self.set(x, y, z, state)
        self.el(n, 'pull', x, y, z)

    # ---------------- decoration helpers
    def pillar(self, x, z, y1, y2, pal, cap=None):
        for y in range(y1, y2 + 1):
            self.set(x, y, z, self.pick(pal))
        if cap: self.set(x, y2, z, cap)

    def scatter(self, x1, y, z1, x2, z2, block, chance, only_air=True, soil=None, soil_on=()):
        """soil: a plant that needs soil gets it - a floor block in soil_on under it becomes `soil` (2.12: eyeblossoms on bare
        stone dropped as items at the first block update). Same random draws as before, so nothing else moves."""
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                if self.rnd.random() < chance and (not only_air or self.get(x, y, z) in (None, 'minecraft:air')):
                    if soil:
                        below = (self.get(x, y - 1, z) or '').split('[')[0]
                        if below in soil_on: self.set(x, y - 1, z, soil)
                        elif below != soil and below not in SOILS: continue
                    self.set(x, y, z, block)

    def ceiling_scatter(self, x1, y, z1, x2, z2, block, chance):
        """Hang things from a ceiling at y+1 (only where the ceiling is solid)."""
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                above = self.get(x, y + 1, z)
                if self.rnd.random() < chance and self.get(x, y, z) in (None, 'minecraft:air') and above and 'air' not in above:
                    self.set(x, y, z, block)


# ===================================================================== cave / tunnel helpers (used by underground builds)
SOLIDISH_SKIP = ('air', 'light', 'cobweb', 'lichen', 'button', 'lever', 'torch', 'lantern', 'sign', 'plate', 'candle', 'ladder',
                 'vine', 'rail', 'carpet', 'skull', 'head', 'dripstone', 'chain', 'water', 'lava', 'bars', 'pane', 'fence', 'wall')


def is_solid(st):
    return bool(st) and not any(k in st for k in SOLIDISH_SKIP)


def cave(B, x1, z1, x2, z2, yf, h, floor_pal, rough=0.12):
    """Carve a domed cavern over the rectangle with a flat floor at yf (walkable air starts at yf+1)."""
    cx, cz = (x1 + x2) / 2, (z1 + z2) / 2
    rx, rz = (x2 - x1) / 2 + 0.5, (z2 - z1) / 2 + 0.5
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            d2 = ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2
            if d2 > 1.0 - B.rnd.random() * rough: continue
            top = yf + max(3, int(round(h * (1 - d2 * 0.75) ** 0.5 + B.rnd.random() * 1.2)))
            for y in range(yf + 1, top + 1):
                B.set(x, y, z, 'air')
            B.set(x, yf, z, B.pick(floor_pal))


def tunnel(B, x1, z1, x2, z2, yf, floor_pal, w=3, h=4):
    """Axis-aligned straight tunnel, w wide (odd) x h tall, floor at yf, between (x1,z1) and (x2,z2) on its centre line."""
    hw = w // 2
    if x1 == x2:
        for z in range(min(z1, z2), max(z1, z2) + 1):
            for dx in range(-hw, hw + 1):
                B.set(x1 + dx, yf, z, B.pick(floor_pal))
                for y in range(yf + 1, yf + 1 + h): B.set(x1 + dx, y, z, 'air')
    else:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for dz in range(-hw, hw + 1):
                B.set(x, yf, z1 + dz, B.pick(floor_pal))
                for y in range(yf + 1, yf + 1 + h): B.set(x, y, z1 + dz, 'air')


def lichen(B, x, y, z):
    """Glow lichen on whatever solid faces surround (x,y,z)."""
    faces = {'north': (0, 0, -1), 'south': (0, 0, 1), 'east': (1, 0, 0), 'west': (-1, 0, 0), 'up': (0, 1, 0), 'down': (0, -1, 0)}
    on = {f: is_solid(B.get(x + dx, y + dy, z + dz)) for f, (dx, dy, dz) in faces.items()}
    if not any(on.values()) or B.get(x, y, z) not in (None, 'minecraft:air'): return
    B.set(x, y, z, 'glow_lichen[' + ','.join(f'{f}={"true" if v else "false"}' for f, v in sorted(on.items())) + ',waterlogged=false]')


def decorate_cave(B, x1, z1, x2, z2, y1, y2, web=0.04, lich=0.02, deco=()):
    """Cobwebs in upper corners, glow lichen on walls, optional floor deco [(block, chance)]."""
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            for y in range(y1, y2 + 1):
                if B.get(x, y, z) != 'minecraft:air': continue
                above = B.get(x, y + 1, z)
                if is_solid(above) and B.rnd.random() < web:
                    B.set(x, y, z, 'cobweb'); continue
                if B.rnd.random() < lich:
                    lichen(B, x, y, z)
            for blk, ch in deco:
                y = y1
                if B.get(x, y, z) == 'minecraft:air' and is_solid(B.get(x, y - 1, z)) and B.rnd.random() < ch:
                    B.set(x, y, z, blk)


# ===================================================================== arena volume probes
def arena_probes(B, max_sq=7):
    """Cover the boss arena's floor plan exactly with odd-sized squares, one marker at the centre of each.
    `bm:p2/<d>/ina` tags players standing inside any square (a symmetric volume box), so fight targeting,
    credit and the abandon timer only count players actually inside the arena - never the antechamber behind
    a wall. Squares are symmetric about their markers, so this works in every structure rotation."""
    from p2.verify import passable
    ax, ay, az = B.meta['arena']
    def opn(x, z):
        a, b = B.b.get((x, ay, z)), B.b.get((x, ay + 1, z))
        if a == ADOOR_LIGHT or a is None: return False
        return passable(a) or (b is not None and passable(b))
    seen, todo = {(ax, az)}, [(ax, az)]
    while todo:
        x, z = todo.pop()
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, z + dz)
            if n not in seen and 0 <= n[0] < B.size[0] and 0 <= n[1] < B.size[2] and opn(*n):
                seen.add(n); todo.append(n)
        if len(seen) > 4000: raise ValueError(f'{B.d}: arena flood leaked')
    h = 0
    while h < 24 and passable(B.b.get((ax, ay + h + 1, az)) or 'minecraft:air'): h += 1      # open-air arenas count 24 up
    B.meta['arena_h'] = h + 1
    left = set(seen)
    sizes = set()
    for (x, z) in sorted(seen, key=lambda c: (c[1], c[0])):
        if (x, z) not in left: continue
        s = 1
        while s + 2 <= max_sq and all((x + i, z + j) in left for i in range(s + 2) for j in range(s + 2)): s += 2
        for i in range(s):
            for j in range(s): left.discard((x + i, z + j))
        c = s // 2
        B.mb(x + c, ay, z + c, ['bm.aprobe', f'bm.aps{s}'])
        sizes.add(s)
    B.meta['arena_cells'] = seen
    B.meta['probe_sizes'] = sorted(sizes)
    return len(seen)


# ===================================================================== 2.2 summoning-altar shrines (overworld dungeons)
SHRINE = {  # core (under the altar), inner ring, outer ring, corner pillar (2 high), pillar cap, idle particle
    'brood': ('chiseled_tuff', 'mossy_cobblestone', 'mossy_stone_bricks', 'mossy_stone_brick_wall', 'ochre_froglight', 'minecraft:mycelium'),
    'frost': ('blue_ice', 'packed_ice', 'polished_diorite', 'packed_ice', 'pearlescent_froglight', 'minecraft:snowflake'),
    'tide': ('dark_prismarine', 'prismarine_bricks', 'prismarine', 'prismarine_wall', 'sea_lantern', 'minecraft:nautilus'),
    'hex': ('amethyst_block', 'purpur_block', 'polished_blackstone_bricks', 'purpur_pillar', 'amethyst_block', 'minecraft:witch'),
    'keep': ('gilded_blackstone', 'polished_blackstone', 'polished_blackstone_bricks', 'polished_blackstone_brick_wall', 'shroomlight', 'minecraft:crimson_spore'),
    'lucky': ('gold_block', 'emerald_block', 'smooth_quartz', 'quartz_pillar', 'glowstone', 'minecraft:wax_on'),
}
_KEEP_OUT = ('gate', 'pressure_plate', 'vault', 'spawner', 'target', 'button', 'lever', 'bulb', 'sign', 'door', 'chest', 'barrel',
             'light', 'lectern', 'bell', 'water', 'lava', 'stairs', 'slab', 'reinforced', 'carpet', 'pot', 'skull', 'campfire')


def shrine(B):
    """A 5x5 inlaid dais around the altar, four capped corner pillars, and a hanging lantern if there's a ceiling.
    Only plain floor is re-laid and pillars only go where the column is open, so doors, gates and puzzle parts are safe."""
    if B.d not in SHRINE or not B.meta['altar']: return
    core, r1, r2, pillar, cap, _ = SHRINE[B.d]
    ax, ay, az = B.meta['altar']
    plain = lambda s: s and not any(k in s for k in _KEEP_OUT) and s not in (B.cfg['gate'], B.cfg['secret'])
    air = lambda s: s is None or s.split('[')[0].split(':')[-1] in ('air', 'cave_air')
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            x, z = ax + dx, az + dz
            if plain(B.get(x, ay - 1, z)) and air(B.get(x, ay, z)):
                ring = max(abs(dx), abs(dz))
                B.set(x, ay - 1, z, core if ring == 0 else r1 if ring == 1 else r2)
    for dx, dz in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
        x, z = ax + dx, az + dz
        if all(air(B.get(x, ay + h, z)) for h in range(4)) and not air(B.get(x, ay - 1, z)):
            B.set(x, ay, z, pillar); B.set(x, ay + 1, z, pillar); B.set(x, ay + 2, z, cap)
    for top in range(ay + 4, min(ay + 10, B.size[1])):            # lantern on a chain from the ceiling, if there is one
        if not air(B.get(ax, top, az)):
            if all(air(B.get(ax, y, az)) for y in range(ay, top)) and top - ay >= 5:
                for y in range(ay + 4, top): B.set(ax, y, az, 'iron_chain[axis=y,waterlogged=false]')
                B.set(ax, ay + 3, az, 'soul_lantern[hanging=true,waterlogged=false]')
            break

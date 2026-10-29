"""2.98: THE UNDERCROWN's shared configuration - read by its builder (p2/dungeons/undercrown.py), its runtime (phase237), its
master's fight (phase238) and the layout verifier, so they can't drift apart.

It is a Phase 2 dungeon in all but registration: the framework's puzzles, gates, secret doors, waves, vaults and resets run it
(p2/logic, called for it alone by phase237), but it is NOT in p2.config.D for the rest of the framework - no worldgen, keys,
maps, emblems, trophies or conquest index. register() puts it in D/FLAVOR/WAVES for the moment someone needs it (the logic
generator, the builder's DBuild, the verifier).

Placed once per world by command, cut into the Nether's rock: LOCAL (0..223, 0..111, 0..223) is WORLD ORIGIN + local, in
minecraft:the_nether. Only the cells the builder sets are placed (an unset cell is a structure void), so the rock around it
stays the Nether's own. A sealing pass (UBuild.seal) wraps every room in two more layers (reinforced deepslate, then rock),
so nothing digs in from outside; only the Hidden Gate opens on the approach cave."""
from nbt import Int, Byte as B_, F
from items import T
from p2.kit import DBuild, YAW
import p2.underitems  # noqa: F401  (the vaults name their keys)
import undercrown_lore as L

d = 'under'
SIZE = (224, 112, 224)
ORIGIN = (2560, 6, -2560)               # world corner, in the Nether (y 6..117, between the bedrock floor and roof); 3.0: its centre ~3.6k from 0,0 (2.98-2.99a: 1536, -1536)
COL = L.SOV_COL

# ---- the arena (the fight, phase238, reads these; the builder builds exactly this)
ARENA = dict(c=(112, 12, 42),           # centre of the floor's TOP layer (walk y = 13)
             r=34,                      # floor radius
             inner=14,                  # the inner ring never falls
             pil_r=26, pil_n=6,         # six pillars at 0,60..300 deg (x=cos, z=sin) on islands that never fall
             pil_w=3, isl_r=6,
             floor=(11, 12),            # the floor's two layers (y)
             lava=(2, 6),               # the lava sea under it (y)
             dome=64,                   # the dome's top (y)
             throne=(112, 13, 11),      # the throne seat (walk y) - the boss kneels here, facing south
             well_y=16)                 # the six Wellsprings' crystals, on each pillar's inward face
# ---- the order of the trials: (n, kind) - one chain, ward by ward
PUZZLES = [(1, 'sigil'),     # FROZEN WARD   Pistachio's sigil: the hat-lock door                     -> G1
           (2, 'targets'),   #               the Frozen Falls (five targets, in the verse's order)    -> G2
           (3, 'sigil'),     #               Celi + Tullius: the ice bridge over the lava lake        -> bridge 3 (+ G3)
           (4, 'waves'),     #               the Frostbound Thralls                                   -> G4
           (5, 'echo'),      #               the Echo of the Snowbeast (Crown Shard of Fear)          -> G5: the Hexed Ward's door, the stair down
           (6, 'sigil'),     # HEXED WARD    Cecil's sigil: the library                               -> G6
           (7, 'lights'),    #               the hex sigils (lights-out)                               -> G7
           (8, 'sigil'),     #               Apophiss: the serpent crawl                               -> G8
           (9, 'sigil'),     #               King Omega: the ossuary                                   -> G9
           (10, 'echo'),     #               the Echo of the Witch (Crown Shard of Hunger)             -> G10: the Drowned Ward's door, the stair down
           (11, 'sigil'),    # DROWNED WARD  Queen Pearl wakes the wreck                               -> G11
           (12, 'simon'),    #               the Kingdom's Song (bells)                                -> G12
           (13, 'sigil'),    #               Emma + Bones: the keel                                    -> G13
           (14, 'waves'),    #               the Dried Drowned                                         -> G14
           (15, 'echo'),     #               the Echo of the Sawshark (Crown Shard of War)             -> G15: the stair down to the hub floor
           (16, 'shards'),   # THE THRONE GATE  the three Crown Shards, dropped on their sockets       -> G16
           (17, 'reach')]    # THE STAIR OF A THOUSAND EYES  top to bottom                              -> G17: the antechamber
WARD = {1: 'frozen', 6: 'hexed', 11: 'drowned'}
ECHO_OF = {5: 'snow', 10: 'witch', 15: 'shark'}
SHARD = {'snow': 'ushard_snow', 'witch': 'ushard_witch', 'shark': 'ushard_shark'}
# every sigil's follower: phase125's WHO key -> (who, its host tag). The wards' are the three Dread trios (anyone who gets here
# has won each of them); the hidden rooms' are followers nobody is promised.
SIGILS = {1: ['pistachio'], 3: ['celi', 'tul'], 6: ['cecil'], 8: ['apo'], 9: ['omega'], 11: ['pearlq'], 13: ['emma', 'bones']}
# ---- the hidden rooms: key -> (title, who opens it (WHO keys), its unique relic item)
HIDDEN = {'last_light': ('The Last Light', ['lightbringer'], 'dawnshard'),
          'lantern': ('The Lantern Crawl', ['lantern'], 'ulantern_wick'),
          'archive': ('The Erased Archive', ['eraser'], 'unwriting'),
          'forge': ("The Chainmaker's Forge", ['bender'], 'chainwhip'),
          'nine': ('Nine Lives', ['henry', 'nia'], 'nine_lives'),
          'ossuary': ('The Ossuary of the Unbound', ['wil'], 'unbound_helm')}
SECRETS = 2                             # classic secret doors (a hidden button each): sdoor k = 1, 2
WELLS = 6

CFG = dict(idx=7, title='The Undercrown', boss=L.SOV, color=COL,
           gate='minecraft:crying_obsidian', secret='minecraft:cracked_nether_bricks', trap='minecraft:soul_soil',
           radius=170, arena_r=ARENA['r'], guard={16: 'dread'},
           puzzles=PUZZLES, key=None, vkey='ukey', bkey='ukey_victor', next_map=None,
           fx=['particle minecraft:ash ~ ~4 ~ 20 6 20 0 12', 'particle minecraft:dust{color:[0.75,0.05,0.12],scale:1.2} ~ ~3 ~ 18 5 18 0 4',
               'particle minecraft:soul ~ ~1 ~ 16 2 16 0.01 1'],
           amb=[('minecraft:entity.warden.heartbeat', 0.5, 0.6), ('minecraft:block.chain.step', 0.7, 0.4),
                ('minecraft:ambient.basalt_deltas.mood', 0.8, 0.6), ('minecraft:entity.warden.ambient', 0.25, 0.4),
                ('minecraft:block.sculk_shrieker.shriek', 0.15, 0.3)])
_MOB = lambda ent, extra='': f'execute at @p[distance=..24,gamemode=!creative,gamemode=!spectator] run summon minecraft:{ent} ~ ~ ~ {{Tags:["bm.seen","bm.dgmob","bm.udread","bm.udk_{ent}"]{extra}}}'
FLAVOR = dict(open='The crying obsidian weeps itself away...', osnd='minecraft:block.respawn_anchor.deplete', osnd2='minecraft:entity.warden.sonic_charge',
              block_part='minecraft:crying_obsidian', tone='minecraft:block.note_block.bell',
              fail=['effect give @a[distance=..16,gamemode=!creative,gamemode=!spectator] minecraft:darkness 5 0',
                    'execute as @a[distance=..16,gamemode=!creative,gamemode=!spectator] run damage @s 4 minecraft:magic',
                    _MOB('wither_skeleton')],
              failmsg='"Wrong." The voice sounds pleased.', failsnd='minecraft:entity.warden.roar',
              trap=['effect give @s minecraft:wither 3 1', 'effect give @s minecraft:darkness 4 0'], trapmsg='The soul soil drinks from you!')


def _w(ent, name, main=None, head=None):
    """a wave foe: a Dread one (phase237 dresses anything tagged bm.udread as its kind's Dread - p176/mk/<type>)"""
    n = {'CustomName': T(name, COL), 'Tags': ['bm.udread', f'bm.udk_{ent}']}
    eq, dc = {}, {}
    for slot, it in (('mainhand', main), ('head', head)):
        if it: eq[slot] = {'id': f'minecraft:{it}', 'count': Int(1)}; dc[slot] = F(0)
    if eq: n['equipment'] = eq; n['drop_chances'] = dc
    return (ent, n)


WAVES = {4: ('The Frostbound Thralls', [[_w('stray', 'Frostbound Thrall', 'bow'), _w('zombie', 'Frostbound Thrall', 'iron_sword')],
                                        [_w('stray', 'Frostbound Thrall', 'bow'), _w('zombie', 'Frostbound Thrall', 'iron_axe'), _w('skeleton', 'Frostbound Archer', 'bow')],
                                        [_w('stray', 'Frostbound Thrall', 'bow'), _w('vindicator', 'Frostbound Executioner', 'iron_axe'), _w('zombie', 'Frostbound Thrall', 'iron_sword')]]),
         14: ('The Dried Drowned', [[_w('husk', 'Dried Drowned', 'trident'), _w('husk', 'Dried Drowned', 'iron_sword')],
                                    [_w('husk', 'Dried Drowned', 'trident'), _w('skeleton', 'Barnacled Bowman', 'bow'), _w('husk', 'Dried Drowned', 'iron_axe')],
                                    [_w('husk', 'Dried Drowned', 'trident'), _w('wither_skeleton', 'Drowned Captain', 'stone_sword'), _w('husk', 'Dried Drowned', 'trident')]])}


def register():
    """D/FLAVOR/WAVES learn the Undercrown (idempotent)"""
    from p2.config import D
    from p2 import logic, data
    D[d] = CFG
    logic.FLAVOR[d] = FLAVOR
    data.WAVES[d] = WAVES
    data.WAVE_PER[d] = (2, 3)


class UBuild(DBuild):
    """DBuild with the Undercrown's own placers. Every one records in self.meta['under'] for the verifier and the runtime."""

    def __init__(self, seed=0):
        register()
        super().__init__(d, *SIZE, seed=seed)
        self.meta['under'] = {'sigils': [], 'bridges': [], 'echoes': [], 'sockets': [], 'hidden': {}, 'relics': [], 'voices': [],
                              'eyes': [], 'eyesp': [], 'wells': [], 'gate': None, 'gsocks': [], 'outer': None, 'rifts': [], 'hoard': None,
                              'throne': None}
        self.outside = set()                 # the approach cave's cells: left out of the sealing pass

    def emblem(self, x, y, z):
        """a sigil's floor: a 3x3 inlay under feet level y"""
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                self.set(x + dx, y - 1, z + dz, 'chiseled_polished_blackstone' if dx == dz == 0 else
                         'polished_blackstone' if dx and dz else 'gilded_blackstone')

    def sigil(self, n, x, y, z, who):
        """puzzle n's sigil for follower `who` (a phase125 WHO key), at feet level y: lit while that follower is within 1.8 of it"""
        self.emblem(x, y, z)
        self.el(n, 'sigil', x, y, z, [f'bm.sw_{who}'])
        self.meta['under']['sigils'].append((n, x, y, z, who))

    def bridge(self, n, x1, y1, z1, x2, y2, z2, block='packed_ice'):
        """cells (all air in the template) filled with `block` the moment puzzle n is solved (cleared again on reset)"""
        x1, x2 = sorted((x1, x2)); y1, y2 = sorted((y1, y2)); z1, z2 = sorted((z1, z2))
        self.mb(x1, y1, z1, ['bm.ubridge', f'bm.g{n}'], data={'dx': Int(x2 - x1), 'dy': Int(y2 - y1), 'dz': Int(z2 - z1), 'b': f'minecraft:{block}'})
        self.meta['under']['bridges'].append((n, x1, y1, z1, x2, y2, z2, block))

    def echo(self, n, x, y, z, k, r=14):
        """puzzle n: walk within r of here and the echo of Dread boss k ('snow'/'witch'/'shark') rises here; it falls -> solved"""
        self.pz(n, 'echo', x, y, z, data={'r': Int(r), 'k': k})
        self.el(n, 'echo', x, y, z, [f'bm.ek_{k}'])
        self.meta['under']['echoes'].append((n, x, y, z, k, r))

    def socket(self, n, x, y, z, k):
        """puzzle n: the Throne Gate's socket for Crown Shard k (dropped on it - Q); the block at y is set to the socket's look"""
        self.set(x, y - 1, z, 'chiseled_polished_blackstone')
        self.el(n, 'socket', x, y, z, [f'bm.ok_{k}'])
        self.meta['under']['sockets'].append((n, x, y, z, k))

    def hidden(self, k, x, y, z, axis, w, h, block, sigils):
        """hidden room k's door: centred bottom at (x, y, z), half-width w, height h, in a wall plane (axis 'x': spans x), made of
        `block`; it opens (for good, till the next reset or rebuild) while every follower of `sigils` [(who, sx, sy, sz)] stands
        on its own sigil. Behind it there must be no other way in."""
        for dw in range(-w, w + 1):
            for dy in range(h):
                gx, gz = (x + dw, z) if axis == 'x' else (x, z + dw)
                self.set(gx, y + dy, gz, block)
        self.mb(x, y, z, ['bm.uhs', f'bm.uhs_{k}'], data={'ax': axis, 'w': Int(w), 'h': Int(h), 'b': f'minecraft:{block}'})
        for who, sx, sy, sz in sigils:
            self.emblem(sx, sy, sz)
            self.mb(sx, sy, sz, ['bm.uhsg', f'bm.uhs_{k}', f'bm.sw_{who}'])
        self.meta['under']['hidden'][k] = dict(door=(x, y, z, axis, w, h, block), sigils=sigils)

    def relic(self, k, x, y, z):
        """a hidden room's relic pedestal (feet level y - the block below is the pedestal): right-click it for the room's Black
        Seal (once a player each rebuild) and its relic (once a player, ever)"""
        self.mb(x, y, z, ['bm.urelic', f'bm.urel_{k}'])
        self.meta['under']['relics'].append((k, x, y, z))

    def voice(self, key, x, y, z, r=6):
        """the Sovereign speaks (undercrown_lore.VOICE[key]) to each player the first time they come within r"""
        self.mb(x, y, z, ['bm.uvoice', f'bm.uv_{key}'], data={'r': Int(r)})
        self.meta['under']['voices'].append((key, x, y, z))

    def eye(self, x, y, z, facing):
        """an eye in the Stair's wall: (x,y,z) is the AIR cell in front of the wall face it opens on; `facing` is the way it looks"""
        self.m(x + 0.5, y + 0.5, z + 0.5, ['bm.ueye'], YAW[facing])
        self.meta['under']['eyes'].append((x, y, z, facing))

    def eyesp(self, x, y, z):
        """where the Stair's Dread Knights step out when an eye catches someone"""
        self.mb(x, y, z, ['bm.ueyesp'])
        self.meta['under']['eyesp'].append((x, y, z))

    def well(self, i, x, y, z):
        """Wellspring i's crystal (an AIR cell against its pillar's inward face, at ARENA well_y)"""
        self.mb(x, y, z, ['bm.uwell', f'bm.uw{i}'])
        self.meta['under']['wells'].append((i, x, y, z))

    def throne(self, x, y, z):
        self.mb(x, y, z, ['bm.uthrone'])
        self.meta['under']['throne'] = (x, y, z)

    def hoard(self, x, y, z, axis, w, h, block):
        """the Sovereign's Hoard's door (behind the throne): opens after the fall for someone carrying six Black Seals"""
        for dw in range(-w, w + 1):
            for dy in range(h):
                gx, gz = (x + dw, z) if axis == 'x' else (x, z + dw)
                self.set(gx, y + dy, gz, block)
        self.mb(x, y, z, ['bm.uhoard'], data={'ax': axis, 'w': Int(w), 'h': Int(h), 'b': f'minecraft:{block}'})
        self.meta['under']['hoard'] = (x, y, z, axis, w, h, block)

    def rift(self, x, y, z):
        """a way home: step in and you're carried out to the Hidden Gate's approach (phase237)"""
        self.mb(x, y, z, ['bm.urift'])
        self.meta['under']['rifts'].append((x, y, z))

    def hidden_gate(self, x, y, z, axis, w, h, socks, outer):
        """THE HIDDEN GATE: the seam (crying obsidian, centred bottom (x,y,z), half-width w, height h) opens when the three Dread
        Tokens are set in its three hollows: socks = {'snow': (x,y,z), 'witch': ..., 'shark': ...} (each at feet level, on the
        approach side); outer = the point the Summons points at (in the approach cave)"""
        for dw in range(-w, w + 1):
            for dy in range(h):
                gx, gz = (x + dw, z) if axis == 'x' else (x, z + dw)
                self.set(gx, y + dy, gz, 'crying_obsidian')
        self.mb(x, y, z, ['bm.ugate'], data={'ax': axis, 'w': Int(w), 'h': Int(h), 'b': 'minecraft:crying_obsidian'})
        for k, (sx, sy, sz) in socks.items():
            self.mb(sx, sy, sz, ['bm.ugsock', f'bm.ugs_{k}'])
        self.mb(*outer, ['bm.uouter'])
        self.meta['under']['gate'] = (x, y, z, axis, w, h)
        self.meta['under']['gsocks'] = list(socks.items())
        self.meta['under']['outer'] = outer

    def seal(self, rock=(('blackstone', 3), ('basalt[axis=y]', 2), ('netherrack', 2), ('magma_block', 0.2))):
        """wrap everything set (but the approach cave) in reinforced deepslate, then rock, where the Nether's own rock would be"""
        sx, sy, sz = self.size
        inside = [p for p in self.b if p not in self.outside]
        N6 = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))

        def ring(src):
            out = set()
            for (x, y, z) in src:
                for dx, dy, dz in N6:
                    q = (x + dx, y + dy, z + dz)
                    if q in self.b or q in out or q in self.outside: continue
                    if 0 <= q[0] < sx and 0 <= q[1] < sy and 0 <= q[2] < sz: out.add(q)
            return out
        r1 = ring(inside)
        for p in r1: self.set(*p, 'reinforced_deepslate')
        r2 = ring(r1)
        for p in r2: self.set(*p, self.pick(list(rock)))

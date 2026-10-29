"""2.99: THE VORN ARMADA's shared configuration - read by its builder (p2/dungeons/armada.py), its runtime (phase241), the
Admiral's fight (phase242) and the layout verifier, so they can't drift apart.

Like the Undercrown it is a Phase 2 dungeon in all but registration: the framework's trials, gates, secret doors, waves and vaults
run it (p2/logic, called for it alone by phase241), but it is NOT in p2.config.D for the rest of the framework. register() puts
it in D/FLAVOR/WAVES for the moment someone needs it (the logic generator, the builder's DBuild, the verifier).

Placed once per world by command, in THE END, far out in the void: LOCAL (0..239, 0..95, 0..239) is WORLD ORIGIN + local, in
minecraft:the_end. The volume is cleared of outer islands before it is placed; an unset cell is a structure void (the void).

THE FLEET. The Hive-Star burns at the centre (STAR); seven ships circle it on the orbit (SHIPS: each ship's rough centre - the
builder keeps each within ~12 of it). Ships are joined by HARD-LIGHT BRIDGES that switch on as trials are solved (ABuild.bridge).
The trials run in one chain, ship by ship, round the orbit: the Dock, the Brood-Carrier, the Star-Forge, the Navigator, the Twin
Dreadnoughts, the Flagship. Fall into the void and the fleet's tractor beam sets you back where you last stood (phase241)."""
import math
from nbt import Int
from items import T
from p2.kit import DBuild, YAW
import p2.armadaitems  # noqa: F401  (the vaults name their keys)
import armada_lore as L

d = 'armada'
SIZE = (240, 96, 240)
ORIGIN = (2560, 24, -3328)              # world corner, in the End (y 24..119); 3.0: its centre ~4.2k from 0,0 (2.99-2.99a: 2560, -4608)
COL, RED = L.VX_COL, L.RED
STAR = dict(c=(120, 48, 120), r=22, burn=30)     # the Hive-Star: its sphere, and the radius within which it scorches
ORBIT = 86
SHIPS = {'dock': (120, 50, 206), 'brood': (192, 46, 168), 'forge': (204, 52, 92), 'nav': (148, 58, 30),
         'dread_a': (66, 48, 26), 'dread_b': (26, 50, 98), 'flag': (52, 54, 180)}

# ---- the Admiral's bridge, aboard the Flagship (the fight, phase242, reads these; the builder builds exactly this)
_ac = (52, 54, 180)                     # centre of the floor's TOP layer (walk y = 55)
_toward = math.atan2(STAR['c'][2] - _ac[2], STAR['c'][0] - _ac[0])          # (radians: the way to the star - the window)
ARENA = dict(c=_ac,
             r=30,                      # the floor's radius (a round hall 61 across)
             dome=84,                   # the dome's top (y)
             window=math.degrees(_toward),   # the great window's centre bearing (degrees, x=cos z=sin): it faces the star, +-55
             helm=(round(_ac[0] + 22 * math.cos(_toward)), 55, round(_ac[2] + 22 * math.sin(_toward))),   # Vexis waits here (walk y)
             door=(round(_ac[0] - 29 * math.cos(_toward)), 55, round(_ac[2] - 29 * math.sin(_toward))),  # the way in, opposite
             pylon_r=17,                # four shield pylons, 3x3, 7 tall, at window+45, +135, +225, +315 deg
             pylon_y=(55, 61),
             pylon_cy=56)              # each crystal at chest height on its pylon's inward face (a blow must reach it)

# ---- the order of the trials: (n, kind) - one chain, ship by ship
PUZZLES = [(1, 'levers'),    # THE DOCK        the gravity lifts (levers: up, down, up - the manifest)            -> G1, bridge 1 to the Brood-Carrier
           (2, 'simon'),     # BROOD-CARRIER   the specimen tanks pulse - repeat them                            -> G2
           (3, 'waves'),     #                 the bio-wave                                                      -> G3
           (4, 'lights'),    #                 the quarantine grid (lights-out)                                  -> G4
           (5, 'vboss'),     #                 THE BROOD-WARDEN rises: Command Cipher I                          -> G5, bridge 5 to the Star-Forge
           (6, 'seq'),       # STAR-FORGE      reroute the conduits (press them in the schematic's order)        -> G6
           (7, 'waves'),     #                 forge drones                                                      -> G7
           (8, 'xsock'),     #                 feed the furnaces: green, violet, cyan Xenite (dropped on slots)  -> G8
           (9, 'vboss'),     #                 THE FORGEMASTER rises: Command Cipher II                          -> G9, bridge 9 to the Navigator
           (10, 'targets'),  # NAVIGATOR       the star-chart: shoot the constellations in the chart's order      -> G10
           (11, 'path'),     #                 the zero-G crossing (plates over the void; a wrong one shocks)    -> G11
           (12, 'waves'),    #                 saucer squadrons                                                  -> G12
           (13, 'vboss'),    #                 THE STAR-SEER rises: Command Cipher III                           -> G13, bridge 13 to Dreadnought A
           (14, 'reactor'),  # DREADNOUGHT A   sabotage its reactor under fire (four conduits)                   -> G14, bridge 14 to Dreadnought B
           (15, 'waves'),    # DREADNOUGHT B   Vorn Guardians                                                    -> G15
           (16, 'reactor'),  #                 sabotage its reactor                                              -> G16, bridge 16 to the Flagship
           (17, 'xsock'),    # THE FLAGSHIP    the Command Lock: the three Ciphers                               -> G17
           (18, 'gauntlet')] #                 the Gauntlet: the boarding corridor, swept by sentry lasers       -> G18: the antechamber, the bridge
SHIP_OF = {1: 'dock', 2: 'brood', 6: 'forge', 10: 'nav', 14: 'dread_a', 15: 'dread_b', 17: 'flag'}
VBOSS = {5: 'brood', 9: 'forge', 13: 'nav'}                  # guardian trials -> L.GUARD key (and the Cipher they drop: CIPHER)
CIPHER = {'brood': 'cipher_1', 'forge': 'cipher_2', 'nav': 'cipher_3'}
XSOCK = {8: {'green': 'xenite_green', 'violet': 'xenite_violet', 'cyan': 'xenite_cyan'},
         17: {'c1': 'cipher_1', 'c2': 'cipher_2', 'c3': 'cipher_3'}}
REACTOR = {14: 'dread_a', 16: 'dread_b'}                    # the dreadnoughts you attack again (after the fall) to bring the invasions back
CONDUITS = 4

# ---- the hidden rooms: key -> (title, who opens it (phase125 WHO keys), its unique relic item)
HIDDEN = {'squad': ("Zib's Lost Squad", ['zib'], 'squad_jetpack'),
          'kennel': ('The Specimen Kennel', ['don'], 'hover_collar'),
          'mainframe': ('The Mainframe Core', ['cursor'], 'hive_override'),
          'garden': ('The Hull Garden', ['sky'], 'stardust_kite')}
SECRETS = 2                             # classic secret doors (a hidden button each): sdoor k = 1, 2
SIGILS_FOR_VAULT = 6                    # Hive Sigils that open the Hive Vault behind the helm (4 relic rooms + 2 secrets give one each)

CFG = dict(idx=8, title='The Vorn Armada', boss=L.VX, color=COL,
           gate='minecraft:lime_stained_glass', secret='minecraft:polished_deepslate', trap='minecraft:redstone_block',
           radius=180, arena_r=ARENA['r'], guard={17: 'vorn'},
           puzzles=PUZZLES, key=None, vkey='akey', bkey='akey_victor', next_map=None,
           fx=['particle minecraft:end_rod ~ ~4 ~ 20 6 20 0.01 6', 'particle minecraft:dust{color:[0.5,1.0,0.35],scale:1.0} ~ ~3 ~ 18 5 18 0 4',
               'particle minecraft:electric_spark ~ ~2 ~ 14 3 14 0.02 3'],
           amb=[('minecraft:block.beacon.ambient', 0.5, 0.6), ('minecraft:block.conduit.ambient', 0.6, 0.5),
                ('minecraft:block.respawn_anchor.ambient', 0.5, 0.8), ('minecraft:entity.guardian.ambient', 0.3, 0.5),
                ('minecraft:block.trial_spawner.ambient', 0.4, 0.4)])
_MOB = lambda ent, extra='': (f'execute at @p[distance=..24,gamemode=!creative,gamemode=!spectator] run summon minecraft:{ent} ~ ~ ~ '
                              f'{{Tags:["bm.seen","bm.dgmob","bm.avorn","bm.avk_{ent}"]{extra}}}')
FLAVOR = dict(open='The hard-light barrier dissolves...', osnd='minecraft:block.beacon.deactivate', osnd2='minecraft:block.respawn_anchor.charge',
              block_part='minecraft:lime_stained_glass', tone='minecraft:block.note_block.bit',
              fail=['execute as @a[distance=..16,gamemode=!creative,gamemode=!spectator] run damage @s 4 minecraft:lightning_bolt',
                    'effect give @a[distance=..16,gamemode=!creative,gamemode=!spectator] minecraft:slowness 4 2',
                    _MOB('husk', ',CustomName:{"text":"Vorn Trooper","color":"#7aff6a"}')],
              failmsg='"INCORRECT. COMPLY."', failsnd='minecraft:entity.elder_guardian.curse',
              trap=['effect give @s minecraft:levitation 1 4', 'damage @s 4 minecraft:lightning_bolt'], trapmsg='The plate shocks you off it!')


def _w(ent, name, col=COL, main=None, head=None, extra=None):
    """a wave foe: a Vorn one (phase241 dresses anything tagged bm.avorn as its kind: bm.avk_<ent>)"""
    n = {'CustomName': T(name, col), 'Tags': ['bm.avorn', f'bm.avk_{ent}']}
    eq, dc = {}, {}
    for slot, it in (('mainhand', main), ('head', head)):
        if it: eq[slot] = {'id': f'minecraft:{it}', 'count': Int(1)}; dc[slot] = 0.0
    if eq: n['equipment'] = eq; n['drop_chances'] = dc
    if extra: n.update(extra)
    return (ent, n)


WAVES = {3: ('The Bio-Wave', [[_w('slime', 'Bio-Slime', extra={'Size': Int(2)}), _w('zombie', 'Improved Specimen')],
                              [_w('slime', 'Bio-Slime', extra={'Size': Int(3)}), _w('zombie', 'Improved Specimen'), _w('husk', 'Vorn Trooper')],
                              [_w('phantom', 'Bio-Phantom'), _w('zombie', 'Improved Specimen'), _w('husk', 'Vorn Trooper')]]),
         7: ('The Forge Drones', [[_w('vex', 'Forge Drone', RED), _w('husk', 'Vorn Trooper')],
                                  [_w('vex', 'Forge Drone', RED), _w('vex', 'Forge Drone', RED), _w('husk', 'Vorn Trooper')],
                                  [_w('vex', 'Forge Drone', RED), _w('husk', 'Vorn Smelter', RED, 'iron_axe'), _w('blaze', 'Slag Wisp', RED)]]),
         12: ('The Saucer Squadrons', [[_w('phantom', 'Scout Saucer'), _w('phantom', 'Scout Saucer')],
                                       [_w('phantom', 'Scout Saucer'), _w('husk', 'Vorn Trooper'), _w('phantom', 'Scout Saucer')],
                                       [_w('phantom', 'Scout Saucer'), _w('phantom', 'Scout Saucer'), _w('husk', 'Vorn Gunner', main='crossbow')]]),
         15: ('The Vorn Guardians', [[_w('husk', 'Vorn Guardian', RED, 'iron_sword', 'iron_helmet'), _w('husk', 'Vorn Gunner', main='crossbow')],
                                     [_w('husk', 'Vorn Guardian', RED, 'iron_sword', 'iron_helmet'), _w('husk', 'Vorn Guardian', RED, 'iron_axe', 'iron_helmet'),
                                      _w('husk', 'Vorn Gunner', main='crossbow')],
                                     [_w('husk', 'Vorn Guardian', RED, 'diamond_sword', 'iron_helmet'), _w('vindicator', 'Vorn Enforcer', RED, 'iron_axe'),
                                      _w('husk', 'Vorn Gunner', main='crossbow')]])}


def register():
    """D/FLAVOR/WAVES learn the Armada (idempotent)"""
    from p2.config import D
    from p2 import logic, data
    D[d] = CFG
    logic.FLAVOR[d] = FLAVOR
    data.WAVES[d] = WAVES
    data.WAVE_PER[d] = (2, 3)


class ABuild(DBuild):
    """DBuild with the Armada's own placers. Every one records in self.meta['armada'] for the verifier and the runtime."""

    def __init__(self, seed=0):
        register()
        super().__init__(d, *SIZE, seed=seed)
        self.meta['armada'] = {'bridges': [], 'vbosses': [], 'socks': [], 'conduits': [], 'sentries': [], 'pads': [], 'hidden': {}, 'relics': [],
                               'voices': [], 'rifts': [], 'dock': None, 'home': None, 'helm': None, 'pylons': [], 'vault': None, 'bench': None,
                               'star': None, 'lecterns': []}

    def emblem(self, x, y, z):
        """a follower sigil's floor: a 3x3 inlay under feet level y"""
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                self.set(x + dx, y - 1, z + dz, 'verdant_froglight' if dx == dz == 0 else 'polished_deepslate' if dx and dz else 'lime_concrete')

    def bridge(self, n, x1, y1, z1, x2, y2, z2, block='lime_stained_glass'):
        """a HARD-LIGHT BRIDGE: cells (all air or void in the template) filled with `block` the moment trial n is solved
        (cleared again on reset). Make each 3 wide, its deck one layer; pads (ABuild.pad) at both ends."""
        x1, x2 = sorted((x1, x2)); y1, y2 = sorted((y1, y2)); z1, z2 = sorted((z1, z2))
        self.mb(x1, y1, z1, ['bm.abridge', f'bm.g{n}'], data={'dx': Int(x2 - x1), 'dy': Int(y2 - y1), 'dz': Int(z2 - z1), 'b': f'minecraft:{block}'})
        self.meta['armada']['bridges'].append((n, x1, y1, z1, x2, y2, z2, block))

    def vboss(self, n, x, y, z, k, r=14):
        """trial n: walk within r of here and the Cipher guardian k (VBOSS: 'brood'/'forge'/'nav') rises here; it falls -> solved,
        and everyone near is given its Cipher. Put it in an open room at least 9 tall (the Star-Seer flies)."""
        self.pz(n, 'vboss', x, y, z, data={'r': Int(r), 'k': k})
        self.el(n, 'vboss', x, y, z, [f'bm.vk_{k}'])
        self.meta['armada']['vbosses'].append((n, x, y, z, k, r))

    def sock(self, n, x, y, z, key):
        """trial n (XSOCK[n]): the slot for item XSOCK[n][key], dropped on it (Q); (x, y, z) is the AIR cell over its plinth"""
        self.set(x, y - 1, z, 'chiseled_polished_blackstone' if n == 17 else 'blast_furnace[facing=north,lit=false]')
        self.el(n, 'sock', x, y, z, [f'bm.sk_{key}'])
        self.meta['armada']['socks'].append((n, x, y, z, key))

    def conduit(self, n, i, x, y, z):
        """reactor trial n's conduit i (0..CONDUITS-1): an AIR cell (a glowing conduit is summoned there; strike it 8 times).
        The trial's controller (pz) should be at the reactor core between them."""
        self.el(n, 'conduit', x, y, z, [f'bm.ci{i}'])
        self.meta['armada']['conduits'].append((n, i, x, y, z))

    def sentry(self, n, x, y, z, facing, length):
        """the Gauntlet's sentry i: a laser emitter in a wall; (x, y, z) the AIR cell in front of it; its beam crosses the corridor
        `length` blocks toward `facing`, sweeping up and down (phase241)"""
        self.m(x + 0.5, y + 0.5, z + 0.5, ['bm.asentry', f'bm.pz{n}', 'bm.d_armada'], YAW[facing])
        self.meta['armada']['sentries'].append((n, x, y, z, facing, length))

    def pad(self, x, y, z):
        """a landing pad (feet level y): where the tractor beam may set someone who fell, if it has nowhere better"""
        self.mb(x, y, z, ['bm.apad'])
        self.meta['armada']['pads'].append((x, y, z))

    def dock(self, x, y, z, facing):
        """where the tractor beam sets you down, arriving (feet level y), facing the Fleet Map"""
        self.m(x + 0.5, y, z + 0.5, ['bm.adock'], YAW[facing])
        self.meta['armada']['dock'] = (x, y, z, facing)

    def home(self, x, y, z):
        """the Dock's beam-out pad: step on it and you're carried back to where you signalled from"""
        self.mb(x, y, z, ['bm.ahome'])
        self.meta['armada']['home'] = (x, y, z)

    def rift(self, x, y, z):
        """a beam-out pad elsewhere (the antechamber, the vault): back to where you signalled from"""
        self.mb(x, y, z, ['bm.arift'])
        self.meta['armada']['rifts'].append((x, y, z))

    def hidden(self, k, x, y, z, axis, w, h, block, sigils):
        """hidden room k's door (as the Undercrown's): opens while every follower of `sigils` [(who, sx, sy, sz)] stands on its
        own sigil. Behind it there must be no other way in."""
        for dw in range(-w, w + 1):
            for dy in range(h):
                gx, gz = (x + dw, z) if axis == 'x' else (x, z + dw)
                self.set(gx, y + dy, gz, block)
        self.mb(x, y, z, ['bm.ahs', f'bm.ahs_{k}'], data={'ax': axis, 'w': Int(w), 'h': Int(h), 'b': f'minecraft:{block}'})
        for who, sx, sy, sz in sigils:
            self.emblem(sx, sy, sz)
            self.mb(sx, sy, sz, ['bm.ahsg', f'bm.ahs_{k}', f'bm.sw_{who}'])
        self.meta['armada']['hidden'][k] = dict(door=(x, y, z, axis, w, h, block), sigils=sigils)

    def relic(self, k, x, y, z):
        """a hidden room's relic pedestal (feet level y; the block below is the pedestal): right-click it for the room's Hive
        Sigil (once a player each rebuild) and its relic (once a player, ever). Secret rooms 'secret1'/'secret2' have one too."""
        self.mb(x, y, z, ['bm.arelic', f'bm.arel_{k}'])
        self.meta['armada']['relics'].append((k, x, y, z))

    def voice(self, key, x, y, z, r=6):
        """the hive speaks (armada_lore.VOICE[key]) to each player the first time they come within r"""
        self.mb(x, y, z, ['bm.avoice', f'bm.av_{key}'], data={'r': Int(r)})
        self.meta['armada']['voices'].append((key, x, y, z))

    def helm(self, x, y, z):
        """the Admiral's helm (ARENA['helm']): Vexis waits here in its warframe"""
        self.mb(x, y, z, ['bm.ahelm'])
        self.meta['armada']['helm'] = (x, y, z)

    def pylon(self, i, x, y, z):
        """shield pylon i's crystal: an AIR cell on the pylon's arena-facing side, at ARENA['pylon_cy']"""
        self.mb(x, y, z, ['bm.apylon', f'bm.ap{i}'])
        self.meta['armada']['pylons'].append((i, x, y, z))

    def hive_vault(self, x, y, z, axis, w, h, block):
        """the Hive Vault's door (behind the helm): opens after the fall for someone carrying six Hive Sigils"""
        for dw in range(-w, w + 1):
            for dy in range(h):
                gx, gz = (x + dw, z) if axis == 'x' else (x, z + dw)
                self.set(gx, y + dy, gz, block)
        self.mb(x, y, z, ['bm.avault'], data={'ax': axis, 'w': Int(w), 'h': Int(h), 'b': f'minecraft:{block}'})
        self.meta['armada']['vault'] = (x, y, z, axis, w, h, block)

    def bench(self, x, y, z):
        """the Starforge bench aboard the Dock (feet level y; the block below is the bench: a smithing table look)"""
        self.set(x, y - 1, z, 'smithing_table')
        self.mb(x, y, z, ['bm.abench'])
        self.meta['armada']['bench'] = (x, y, z)

    def star(self):
        """the Hive-Star's centre (markers for its corona, flares and burn)"""
        self.mb(*STAR['c'], ['bm.astar'])
        self.meta['armada']['star'] = STAR['c']

    # ---- 2.99a (phase249): THE HANGAR - the dormant Mecha Rex, behind the Flagship's third secret door
    def hangar(self, x, y, z, yaw):
        """the dormant Mecha Rex's spot (feet level y, facing yaw): phase249 raises its rig there (no host, dim) and an
        interaction at its chest - bring the three blueprints and the core and right-click it"""
        self.m(x + 0.5, y, z + 0.5, ['bm.rxhang'], float(yaw))
        self.meta['armada']['hangar'] = (x, y, z, yaw)

"""THE SUNKEN THRONE: a sealed prismarine temple on the deep-ocean floor, 56 x 40 x 56 (floor level y4).
Enter through the tower door (doors hold back the sea) and climb down the shaft.
L1 Tide Hall (trial spawners; Pearl Sigil I) -> P1 Valve Room (levers on warm/cold copper pipes; Sigil II) -> G1 + a flooded
tunnel that drains when the valves are set -> P2 Conduit Hymn (simon, 5 notes; Sigil III) -> G2 -> P3 Tyrant's Table
(offer the three sigils) -> G3 -> Antechamber (spoils vault) -> battle door -> Throne Hall arena (a pool for the Tyrant).
Secret: Smuggler's Grotto (floor button hidden among dead coral in the Tide Hall)."""
from p2.kit import DBuild, lichen
from p2.config import SEQS
from nbt import Byte, Int

BODY = [('prismarine_bricks', 4), ('dark_prismarine', 3), ('prismarine', 2), ('cracked_stone_bricks', 0.3)]
FLOOR = [('dark_prismarine', 3), ('prismarine_bricks', 2), ('polished_andesite', 1)]
PIPE_WARM, PIPE_COLD = 'waxed_copper_block', 'waxed_oxidized_copper'


def build():
    B = DBuild('tide', 56, 40, 56, seed=3301)
    B.fillp(4, 0, 4, 51, 22, 51, BODY)                       # the temple body: solid; rooms are carved out
    for i in range(1, 4):                                     # stepped roof
        B.fillp(4 + i * 3, 22 + i, 4 + i * 3, 51 - i * 3, 22 + i, 51 - i * 3, BODY)
    B.fillp(6, 4, 6, 49, 4, 49, FLOOR)

    def room(x1, z1, x2, z2, h=6, yf=4):
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                B.set(x, yf, z, B.pick(FLOOR))
                for y in range(yf + 1, yf + 1 + h): B.set(x, y, z, 'air')

    def tun(x1, z1, x2, z2, w=3, h=4):
        hw = w // 2
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for z in range(min(z1, z2), max(z1, z2) + 1):
                for d in range(-hw, hw + 1):
                    cx, cz = (x, z + d) if z1 == z2 else (x + d, z)
                    B.set(cx, 4, cz, B.pick(FLOOR))
                    for y in range(5, 5 + h): B.set(cx, y, cz, 'air')

    # ---------------- entrance tower (x5..9, z5..9) up to y38, door in its north wall at y35
    for x in range(5, 10):
        for z in range(5, 10):
            for y in range(22, 39):
                B.set(x, y, z, B.pick(BODY) if x in (5, 9) or z in (5, 9) or y == 38 else 'air')
    for y in range(5, 38):
        for x in range(6, 9):
            for z in range(6, 9): B.set(x, y, z, 'air')
    for y in range(5, 37): B.set(7, y, 8, 'ladder[facing=north,waterlogged=false]')
    for x in range(6, 9):
        for z in (6, 7): B.set(x, 34, z, B.pick(FLOOR))
    B.set(7, 35, 5, 'oak_door[facing=south,half=lower,hinge=left,open=false,powered=false]')
    B.set(7, 36, 5, 'oak_door[facing=south,half=upper,hinge=left,open=false,powered=false]')
    B.set(7, 37, 6, 'sea_lantern')
    B.entrance(7, 35, 6)

    # ---------------- L1 Tide Hall (combat): x6..20, z6..18
    room(6, 6, 20, 18, h=7)
    for y in range(5, 12):
        for x in range(6, 9):
            for z in range(6, 9): B.set(x, y, z, 'air')
    B.trial_spawner(11, 5, 14, 'drowned')
    B.trial_spawner(16, 5, 9, 'drowned_melee')
    B.chest(19, 5, 16, 'west', items=[{'Slot': Byte(13), **_stack('pearl_sigil_1')}])
    B.restock(19, 5, 16, 'pearl_sigil_1')
    for (x, z) in [(10, 7), (18, 12), (13, 17)]: B.set(x, 5, z, 'sea_lantern')
    for (x, z) in [(12, 10), (14, 12), (9, 16)]: B.set(x, 5, z, 'dead_brain_coral_block')
    # secret: floor button among dead coral fans in the north-east corner
    for (x, z) in [(19, 7), (18, 7), (19, 8)]: B.set(x, 5, z, 'dead_tube_coral_fan[waterlogged=false]')
    B.sbutton(20, 5, 7, 'stone_button[face=floor,facing=north,powered=false]', 1)
    B.sdoor(9, 5, 19, 1)
    for z in (20,):
        B.set(9, 4, z, B.pick(FLOOR)); B.set(9, 5, z, 'air'); B.set(9, 6, z, 'air')
    room(6, 21, 13, 27, h=4)
    B.chest(7, 5, 26, 'east', loot='bm:p2/tide/hidden')
    B.chest(12, 5, 26, 'west', loot='minecraft:chests/buried_treasure')
    B.sign(9, 6, 27, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ["Smuggler's", 'Grotto', 'Finders keepers.', '- R.G.'], color='aqua', glow=True)
    B.m(10.5, 5, 23.5, ['bm.npc_spawn', 'bm.npc.deco_rat'], 0)
    B.fx(13, 8, 12); B.zone(13, 6, 12)

    # ---------------- P1 Valve Room: x24..36, z6..16. Combat waves (the Tyrant's Tide).
    tun(20, 12, 24, 12)
    room(24, 6, 35, 14, h=6)
    for i, x in enumerate(range(25, 35, 2)):
        for y in range(5, 11): B.set(x, y, 6, PIPE_WARM if i % 2 == 0 else PIPE_COLD)
    B.sign(30, 7, 14, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ["The Tyrant's", 'Tide rises.', 'Hold the', 'valve room!'], color='aqua', glow=True)
    B.pz(1, 'waves', 30, 5, 10)
    B.el(1, 'wsp', 26, 5, 9)
    B.el(1, 'wsp', 33, 5, 9)
    B.el(1, 'wsp', 26, 5, 12)
    B.el(1, 'wsp', 33, 5, 12)
    B.set(34, 5, 13, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel', 'Items': [{'Slot': Byte(13), **_stack('pearl_sigil_2')}]})
    B.restock(34, 5, 13, 'pearl_sigil_2')
    B.fx(30, 8, 11); B.zone(30, 6, 11)
    # G1 east wall x37, then a FLOODED tunnel x38..42 that drains on solve; an oak door holds the water back from P2
    tun(36, 11, 42, 11)
    B.gate(37, 5, 11, 'z', 1)
    for x in range(38, 43):
        for z in range(10, 13):
            for y in range(5, 9): B.set(x, y, z, 'water[level=0]')
    B.drain(40, 6, 11, 1)
    B.set(40, 5, 13, 'oak_door[facing=south,half=lower,hinge=left,open=false,powered=false]')
    B.set(40, 6, 13, 'oak_door[facing=south,half=upper,hinge=left,open=false,powered=false]')

    # ---------------- P2 Conduit Hymn (simon): x34..48, z14..28
    room(38, 14, 49, 28, h=8)
    plinths = [(39, 17), (48, 17), (39, 26), (48, 26), (43, 15)]
    order = {0: 3, 1: 1, 2: 4, 3: 5, 4: 2}           # plinth index -> position in the melody
    for i, (x, z) in enumerate(plinths):
        B.set(x, 5, z, 'prismarine_bricks'); B.set(x, 6, z, 'prismarine_bricks')
        B.seq_button(2, x, 7, z, 'stone_button[face=floor,facing=north,powered=false]', order[i], sound=i + 1)
    B.set(43, 5, 22, 'dark_prismarine'); B.set(43, 6, 22, 'conduit[waterlogged=false]')
    B.listen_button(2, 44, 5, 22, 'stone_button[face=wall,facing=east,powered=false]')
    B.sign(42, 5, 22, 'dark_oak_wall_sign[facing=west,waterlogged=false]', ['Press the conch', 'to hear the', 'Hymn. Then sing', 'it back.'], color='aqua', glow=True)
    B.pz(2, 'simon', 43, 3, 21)
    SEQS.setdefault('tide', {})[2] = 5
    B.chest(39, 5, 27, 'east', items=[{'Slot': Byte(13), **_stack('pearl_sigil_3')}])
    B.restock(39, 5, 27, 'pearl_sigil_3')
    B.fx(43, 9, 21); B.zone(43, 7, 21)

    # ---------------- G2 (south) -> P3 Tyrant's Table: x36..48, z34..46
    tun(43, 28, 43, 34)
    B.gate(43, 5, 31, 'x', 2)
    room(38, 34, 49, 46, h=7)
    for (x, z, k) in [(42, 39, 1), (44, 37, 2), (46, 39, 3)]:
        B.set(x, 5, z, 'prismarine_bricks')
        B.altar_offer(3, x, 6, z, k)
    B.set(44, 5, 41, 'chiseled_stone_bricks'); B.set(44, 6, 41, 'dark_prismarine_slab[type=bottom,waterlogged=false]')
    B.sign(44, 7, 46, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ['Return the three', 'pearls to the', "Tyrant's table.", 'Drop them on it.'], color='aqua', glow=True)
    B.pz(3, 'offering', 44, 3, 40)
    B.fx(44, 9, 40)

    # ---------------- G3 (west) -> Antechamber x22..30, z36..44 -> battle door -> Throne Hall x6..20, z28..50
    tun(30, 40, 38, 40)
    B.gate(34, 5, 40, 'z', 3)
    room(22, 36, 30, 44, h=6)
    B.vault(26, 5, 43, 'north', 'vkey_tide', 'bm:p2/tide/vault')
    B.sign(26, 7, 36, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['The Throne Hall.', 'Kneel at the', 'trident altar', 'with his key.'], color='aqua', glow=True)
    tun(17, 40, 23, 40, w=5, h=5)
    B.gate(20, 5, 40, 'z', 0, big=True)
    room(6, 29, 18, 50, h=12)
    for x in range(9, 16):
        for z in range(35, 46):
            B.set(x, 3, z, B.pick(FLOOR)); B.set(x, 4, z, 'water[level=0]')
    B.arena(12, 5, 40)
    B.altar(16, 5, 40)
    B.set(17, 5, 38, 'dark_prismarine'); B.set(17, 5, 42, 'dark_prismarine')
    for (x, z) in [(8, 31), (16, 31), (8, 48), (16, 48)]: B.mspawn(x, 5, z)
    for (x, z) in [(7, 30), (17, 30), (7, 49), (17, 49)]: B.pillar(x, z, 5, 15, [('prismarine_bricks', 2), ('dark_prismarine', 1)], cap='sea_lantern')
    B.vault(6, 5, 40, 'east', 'bkey_tide', 'bm:p2/tide/victor')
    B.fx(12, 10, 40); B.zone(12, 7, 40)
    B.controller(28, 8, 28)
    return B


def _stack(iid):
    from p2.kit import stack_nbt
    return stack_nbt(iid)

"""3.0k: GAITS DRIVEN BY THE GROUND - a rig's walk cycle advanced by how far its host has really moved, not by a clock.

A clock-driven cycle (a frame every N ticks) only plants its feet at one speed: slower, the feet skate forward; faster, they
skate back; standing still, the legs pedal the air until a check every few ticks notices. Here, every tick, as the host:

  THE GROUND   how far it moved since last tick (milliblocks, horizontal: the longer leg plus 3/8 of the shorter, within 3%
               of the true length; a jump of 1.5 blocks or more in a tick is a teleport, not a step, and counts nothing), and
               its speed, smoothed (3/4 last tick's + 1/4 this tick's).
  THE TURN     its facing, eased: a third of the way to the host's yaw each tick (a mob's own turn snaps up to 90 degrees in a
               tick when its path bends), put in storage bm:tmp gk.y for the rig's own turn function (a macro).
  THE GAIT     picked from the smoothed speed with hysteresis (no flicker at a threshold): 0 still, 1, 2 ... each gait a cycle
               of NF frames that covers L milliblocks of ground - its phase (bm.gkp, 0..NF*1000) advanced by the distance
               moved, so a foot on the ground stays where it was put. Changing gait keeps the phase (the stride goes on).
  THE FRAME    drawn when the phase reaches the next one, with an interpolation as long as the next frame is away at this
               speed (1..4 ticks): the displays glide frame to frame and arrive as the next is due.
  STILL        stopping eases into the idle (8 ticks), then breathes (idle a / idle b, 30 ticks each way, every 40); starting
               again, the first frames take 4 ticks each (bm.gkb): out of the idle, not snapped into the stride.

build(G, pfx, gaits, ...) writes bm:<pfx>/motion (the ground and the turn - run every tick, as the host) and bm:<pfx>/gait
(the gait and its frame). The caller writes the frames: bm:<pfx>/f/<g>_<k>_<d> (gait g, frame k, interpolation d) and
bm:<pfx>/f/0_a_8, 0_a_30, 0_b_30 (the idle), and the turn: bm:<pfx>/turn (a macro taking $(y), the eased yaw)."""

OBJ = ['bm.gkx', 'bm.gkz', 'bm.gks', 'bm.gkp', 'bm.gkf', 'bm.gkg', 'bm.gkb', 'bm.gky', 'bm.gki']
CONST = {'#gk2': 2, '#gk3': 3, '#gk4': 4, '#gk8': 8, '#gk80': 80, '#gk100': 100, '#gk1000': 1000, '#gk36k': 36000, '#gkm1': -1}
DURS = (1, 2, 3, 4)
BLEND = 4                      # (the first frames out of the idle: this many ticks each)
TELEPORT = 1500                # (milliblocks in one tick: more is a teleport)


def objectives(G):
    """the shared scores and constants (once, whoever builds first)"""
    if 'bm.gkx' in G.OBJECTIVES:
        return
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in OBJ] + \
        [f'scoreboard players set {k} bm.rng {v}' for k, v in CONST.items()]
    G.OBJECTIVES += OBJ


def init_lines():
    """as the host, when its rig is made: start from where it stands and the way it faces, still"""
    return ['execute store result score @s bm.gkx run data get entity @s Pos[0] 1000', 'execute store result score @s bm.gkz run data get entity @s Pos[2] 1000',
            'execute store result score @s bm.gky run data get entity @s Rotation[0] 100',
            'scoreboard players set @s bm.gks 0', 'scoreboard players set @s bm.gkp 0', 'scoreboard players set @s bm.gkf -1',
            'scoreboard players set @s bm.gkg 0', 'scoreboard players set @s bm.gkb 0', 'scoreboard players set @s bm.gki 0']


def motion_lines():
    """as the host, every tick: #gkd the distance moved (milliblocks), @s bm.gks its smoothed speed, storage bm:tmp gk.y its eased yaw"""
    S = 'scoreboard players operation'
    return ['execute store result score #gkx bm.rng run data get entity @s Pos[0] 1000', 'execute store result score #gkz bm.rng run data get entity @s Pos[2] 1000',
            f'{S} #gkd bm.rng = #gkx bm.rng', f'{S} #gkd bm.rng -= @s bm.gkx', f'{S} #gke bm.rng = #gkz bm.rng', f'{S} #gke bm.rng -= @s bm.gkz',
            f'{S} @s bm.gkx = #gkx bm.rng', f'{S} @s bm.gkz = #gkz bm.rng',
            f'execute if score #gkd bm.rng matches ..-1 run {S} #gkd bm.rng *= #gkm1 bm.rng',
            f'execute if score #gke bm.rng matches ..-1 run {S} #gke bm.rng *= #gkm1 bm.rng',
            f'execute if score #gkd bm.rng < #gke bm.rng run {S} #gkd bm.rng >< #gke bm.rng',
            f'{S} #gke bm.rng *= #gk3 bm.rng', f'{S} #gke bm.rng /= #gk8 bm.rng', f'{S} #gkd bm.rng += #gke bm.rng',
            f'execute if score #gkd bm.rng matches {TELEPORT}.. run scoreboard players set #gkd bm.rng 0',
            f'{S} #gks bm.rng = @s bm.gks', f'{S} #gks bm.rng *= #gk3 bm.rng', f'{S} #gks bm.rng += #gkd bm.rng', f'{S} #gks bm.rng /= #gk4 bm.rng',
            f'{S} @s bm.gks = #gks bm.rng',
            # the turn, eased: a third of the (wrapped) difference each tick
            'execute store result score #gky bm.rng run data get entity @s Rotation[0] 100', f'{S} #gky bm.rng -= @s bm.gky',
            'scoreboard players add #gky bm.rng 18000', f'{S} #gky bm.rng %= #gk36k bm.rng', 'scoreboard players remove #gky bm.rng 18000',
            f'{S} #gky bm.rng /= #gk3 bm.rng', f'{S} @s bm.gky += #gky bm.rng', f'{S} @s bm.gky %= #gk36k bm.rng',
            'execute store result storage bm:tmp gk.y float 0.01 run scoreboard players get @s bm.gky']


def build(G, pfx, gaits, nf=8, call=None):
    """gaits: [(L milliblocks a cycle, enter speed, leave speed)] for gaits 1, 2, ... (speeds in milliblocks a tick, smoothed;
    leave < enter; gait 1's leave is back to still). Writes bm:<pfx>/motion and bm:<pfx>/gait. call(name) -> the command that
    runs a frame (default: as the host; a rig of passengers: 'execute on passengers run function bm:<name>')."""
    objectives(G)
    call = call or (lambda name: f'function bm:{name}')
    fn = G.fn
    S = 'scoreboard players operation'
    fn(f'{pfx}/motion', motion_lines() + [f'function bm:{pfx}/turn with storage bm:tmp gk'])
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #gkL{pfx.replace("/", "_")}_{g} bm.rng {L}' for g, (L, _e, _l) in enumerate(gaits, 1)] + \
        [f'scoreboard players set #gkN bm.rng {nf * 1000}']
    sel = [f'{S} #gkg bm.rng = @s bm.gkg']
    top = len(gaits)
    for g, (_L, enter, leave) in enumerate(gaits, 1):
        sel.append(f'execute if score #gkg bm.rng matches {g - 1} if score @s bm.gks matches {enter}.. run scoreboard players set #gkg bm.rng {g}')
    for g, (_L, enter, leave) in reversed(list(enumerate(gaits, 1))):
        sel.append(f'execute if score #gkg bm.rng matches {g}.. if score @s bm.gks matches ..{leave} run scoreboard players set #gkg bm.rng {g - 1}')
    fn(f'{pfx}/gait', ['execute if score @s bm.gkb matches 1.. run scoreboard players remove @s bm.gkb 1'] + sel +
       [f'execute unless score #gkg bm.rng = @s bm.gkg run function bm:{pfx}/shift', f'{S} @s bm.gkg = #gkg bm.rng',
        f'execute if score @s bm.gkg matches 0 run return run function bm:{pfx}/idle'] +
       [f'execute if score @s bm.gkg matches {g} run scoreboard players operation #gkl bm.rng = #gkL{pfx.replace("/", "_")}_{g} bm.rng' for g in range(1, top + 1)] +
       [f'{S} #gka bm.rng = #gkd bm.rng', f'{S} #gka bm.rng *= #gkN bm.rng', f'{S} #gka bm.rng /= #gkl bm.rng',
        f'{S} @s bm.gkp += #gka bm.rng', f'{S} @s bm.gkp %= #gkN bm.rng',
        f'{S} #gkk bm.rng = @s bm.gkp', f'{S} #gkk bm.rng /= #gk1000 bm.rng',
        f'{S} #gkq bm.rng = @s bm.gkg', f'{S} #gkq bm.rng *= #gk100 bm.rng', f'{S} #gkk bm.rng += #gkq bm.rng',
        'execute if score #gkk bm.rng = @s bm.gkf run return 0', f'{S} @s bm.gkf = #gkk bm.rng',
        # how long until the next frame at this speed: a frame is L/nf of ground
        f'{S} #gkt bm.rng = @s bm.gks', f'{S} #gkt bm.rng *= #gk8 bm.rng', f'function bm:{pfx}/dur',
        f'execute if score @s bm.gkb matches 1.. run scoreboard players set #gkw bm.rng {BLEND}'] +
       [f'execute if score @s bm.gkg matches {g} run return run function bm:{pfx}/g{g}' for g in range(1, top + 1)])
    # (#gkt = 8 x speed against the cycle's length #gkl: 1 tick a frame at L or more, 2 at L/2, 3 at L/3, else 4)
    fn(f'{pfx}/dur', ['scoreboard players set #gkw bm.rng 4',
                      f'{S} #gkh bm.rng = #gkl bm.rng', f'{S} #gkh bm.rng /= #gk3 bm.rng',
                      'execute if score #gkt bm.rng >= #gkh bm.rng run scoreboard players set #gkw bm.rng 3',
                      f'{S} #gkh bm.rng = #gkl bm.rng', f'{S} #gkh bm.rng /= #gk2 bm.rng',
                      'execute if score #gkt bm.rng >= #gkh bm.rng run scoreboard players set #gkw bm.rng 2',
                      'execute if score #gkt bm.rng >= #gkl bm.rng run scoreboard players set #gkw bm.rng 1'])
    for g in range(1, top + 1):
        fn(f'{pfx}/g{g}', [f'execute if score #gkk bm.rng matches {g * 100 + k} run return run function bm:{pfx}/g{g}/{k}' for k in range(nf)])
        for k in range(nf):
            fn(f'{pfx}/g{g}/{k}', [f'execute if score #gkw bm.rng matches {d} run return run ' + call(f'{pfx}/f/{g}_{k}_{d}') for d in DURS[:-1]] +
               [call(f'{pfx}/f/{g}_{k}_{DURS[-1]}')])
    # a change of gait: draw at once; into the idle - ease in, then breathe; out of it - the first frames slow
    fn(f'{pfx}/shift', ['scoreboard players set @s bm.gkf -1', 'execute if score #gkg bm.rng matches 0 run scoreboard players set @s bm.gki 0',
                        f'execute if score @s bm.gkg matches 0 run scoreboard players set @s bm.gkb {BLEND + 2}'])
    fn(f'{pfx}/idle', ['scoreboard players add @s bm.gki 1', f'{S} #gki bm.rng = @s bm.gki', f'{S} #gki bm.rng %= #gk80 bm.rng',
                       f'execute if score @s bm.gki matches 1 run return run ' + call(f'{pfx}/f/0_a_8'),
                       f'execute if score #gki bm.rng matches 0 run return run ' + call(f'{pfx}/f/0_a_30'),
                       f'execute if score #gki bm.rng matches 40 run ' + call(f'{pfx}/f/0_b_30')])

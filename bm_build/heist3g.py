"""3.0g: THE HEISTS, MENDED AND WIDENED - nine of the owner's notes on the gutter's heists.

NO BAGS ON A JOB   (the owner: "Backpacks can be taken into a heist sometimes. They should never be allowed, even if they contain
               a whitelisted item.") Every bag (phase248's BAGS: the Backpack, the Vacuum Satchel, the Prime Cooler, Dennis's Ore
               Magnet, Pistachio's Spirit Jar) - or anything with one packed inside it (a bundle, a box, a Haul) - is taken off a
               coat-checked player in the gutter within a quarter second, wherever it came from: a bag left unfolded outside,
               which folded itself back into its owner's hands once they were through the door (the way they got in); one handed
               back by a crewmate's bag; one on the cursor or in the crafting grid. It joins the rest of their gear with the
               Fixer (the coat check's carry-back, cb.p<pid>) and comes home with it.
THE MIRROR MAGE    (the owner: "Sometimes the mirror mage spawns in a heist boss fight and just stands there with no AI and is
               invulnerable.") The guardian's entrance (phase151) freezes it and its rider, and releases the rider only if it is
               still riding when the entrance ends; a rider thrown off on the way up (the guardian teleported under the floor
               and lifted back) stayed frozen - NoAI, Invulnerable - for good. Now any heist rider found frozen with no entrance
               of its own and no frozen mount under it is released at once (each second).
PARKOUR CHECKPOINTS  (the owner: "The checkpoint in the parkour rooms saves even on new heists. Players can purposely fail to skip
               half the room.") A Spire's checkpoint was keyed by the room's number along the run, so the next plan (a failed
               attempt's fresh plan, a new heist) with a Spire at the same number started you from it. Every checkpoint is cleared
               when a heist is laid out (a new one, or a fresh plan after a failure) and when you leave one, any way at all.
THE GUARDIAN KEPT IN ITS HALL  (the owner: "it's possible to clip the boss thru the wall in corners. In one scenario, I pushed the
               boss into the sealed vault and was no longer able to fight them.") Four times a second every vault guardian (and
               the hard-mode guardians below) and every Champion's Pit champion is checked against its room: its middle outside
               the hall's floor (inside the walls, through them, out of the doorways, down a hole, up in the ceiling) or its body
               inside a solid block, it is put back in the middle of its room. The vault's guardians also stand their ground a
               little better (+0.4 knockback resistance).
NO SOUL VIALS IN THE GUTTER  (the owner: "A zombie in a heist dropped a soul vial.") The 1-in-700 Soul Vial (phase44) is never
               caught in the gutter or by anyone on a heist.
HEIST BARRELS VANISH  (the owner: "Breaking a heist barrel with your fist lets it drop as an item instead of vanishing.") A Haul,
               a Haul Crate or a Crate Desk crate set down and broken by hand drops what's inside - but never the barrel: any fresh
               barrel drop (no contents of its own, not thrown by anyone) where it stood is taken away at once, whatever the
               crate's name. (Only The Haul and the Haul Crate were caught by name; the Desk's crates, named another way, came
               back as plain barrels.) And no plain barrel can drop from a block anywhere in the gutter.
THE RAT KING, CROWNED  (the owner: "The rat king boss in heists looks unimpressive and has no animations.") He is a rig now
               (ratking_art): a great crowned rat in a royal cape with a sceptre of golden cheese, and he moves - he idles and
               waddles, hauls his sceptre back and brings it down on you (his blows are his own now, not the zombie's), and now
               and then rears up for THE ROYAL DECREE: a screech, the sceptre slammed into the floor (a shockwave round him) and
               two Plague Rats out of the dark. He flinches when he's hurt; he comes out of the dark crouched, then roars; he
               dies on the staging kit's timeline (cine: he staggers, topples onto his back, his crown knocked off), and his fall
               still counts as the crew's kill (the Rat King's finds).
FOUR VAULT HALLS   (the owner: "More boss room variety in heists would be nice. It's always the same 4 pressure plate puzzle
               fight.") The guardian's hall is one of four, drawn when the heist is laid out (a sign at the door says which):
  THE WEIGHING FLOOR   as before: when it shells itself in gold, the crew on the four plates cracks it.
  THE PYLON HALL       when it shells, four soul pylons rise in the corners and shield it - three blows smash each one; while
                       they stand they spit sparks at the crew. All four down: the shell cracks.
  THE CRUMBLING HALL   all fight long the floor cracks under a raider and gives way a moment later (a 3 x 3 pit; fall in and
                       you're hurt and thrown back to the hall's door); it mends 8 s later. Lure the shelled guardian over the
                       cracks: when the floor falls away under it, its shell breaks.
  THE TURNING BLADE    a blade of soul-fire sweeps the hall round its hub - jump it or be cut. Hold the hub (stand in the middle)
                       while the blade passes through the shelled guardian: its shell cracks.
HARD-MODE GUARDIANS  (the owner: "In hard mode, dread mires, the alien alt, and the knight mini bosses could be cool to appear in
               heists as bosses.") In hard mode about one vault in three is guarded instead by a DREAD MIRE (phase246's own,
               rising from its puddle), a BROOD-MIRE (phase258's) or a STATUE KNIGHT (phase245's - a Dread or a Vorn Sentinel,
               waking from stone), each made by its own summon and fighting its own fight, with heist-scaled health (by tier
               and crew) and the guardian's bar. Its fall pays the pot (20 + 10 a tier coins) and a Champion's find for every
               raider, and opens the vault as the guardian's would. (A Mire never comes once its master has fallen - the Dread
               Sovereign, Admiral Vexis: a knight comes instead; the knight's statue stays in the hall, stone, and isn't handed out.)
THE ELEMENTAL GEMS LEAVE THE SHOP; FORMS COME IN  (the owner: "Remove the elemental gems from the heist shop and allow players to
               bring over ethereal/wraithfire forms from the overworld.") Goldtooth no longer sells the nine gems (phase89). And
               the gem or form Cecil, KillerWatt and Apophiss wear in the overworld - an Ethereal or Wraithfire form included -
               comes with them through the Fixer's door: nothing is swapped at the gutter any more (phase126/phase144). A gem
               one of them was given in the lobby before 3.0g is handed back to its owner as the item, the first time they come
               in. A vault gem bought before (still in someone's pockets) still fades when they leave.

Importing does nothing; generate(G) runs late (after phase184 / phase175: every room, guardian, bag and follower it hooks)."""
from items import T
from nbt import snbt, B, F, Int, D as Dd

GOLD = '#ffcf40'
P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
HB_PCT = 35                         # (% of hard-mode vaults with a hard-mode guardian)
LAYOUTS = {0: ('THE WEIGHING FLOOR', 'When the guardian shells itself in gold, the crew on the four gold plates cracks it.'),
           1: ('THE PYLON HALL', 'When the guardian shells, four soul pylons shield it - smash them (three blows each). They spit sparks while they stand.'),
           2: ('THE CRUMBLING HALL', 'The floor gives way under the crew. Lure the shelled guardian over the cracks: when the floor falls under it, its shell breaks.'),
           3: ('THE TURNING BLADE', 'A blade of soul-fire sweeps the hall - jump it. Hold the hub in the middle while the blade cuts the shelled guardian.')}
PYLONS = [(6, 6), (18, 6), (6, 18), (18, 18)]
FOES = 'gamemode=!spectator,gamemode=!creative'


def generate(G):
    import phase70 as P70
    from phase70_rooms import rel
    fn, title, tellraw = G.fn, G.title, G.tellraw
    F_ = G.FUNCS
    tick, fast, second = F_['tick'], F_['loop/fast'], F_['loop/second']
    say = lambda txt, col='gray': tellraw('@s', P + [T(txt, col)])
    objs = ['bm.h3gl', 'bm.h3gt', 'bm.h3gph', 'bm.h3gba', 'bm.h3gbc', 'bm.rkid', 'bm.rks', 'bm.rkt', 'bm.rka', 'bm.rkc', 'bm.rkd', 'bm.rkx', 'bm.rkz']
    F_['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    n = 0

    # ================================================================== 1. NO BAGS ON A JOB
    import phase248 as P248
    bag = P248.BAG
    inside = lambda k: (f'*[minecraft:container~{{items:{{contains:[{{predicates:{{"minecraft:custom_data":{{bm:"{k}"}}}}}}]}}}}]',
                        f'*[minecraft:bundle_contents~{{items:{{contains:[{{predicates:{{"minecraft:custom_data":{{bm:"{k}"}}}}}}]}}}}]')
    nested = [p for k in P248.BAGS for p in inside(k)]
    slots = ('container.*', 'weapon.offhand', 'player.cursor', 'player.crafting.*', 'armor.*')
    fn('h3g/bag/has', [f'execute if items entity @s {sl} {bag} run return 1' for sl in slots] +
       [f'execute if items entity @s {sl} {p} run return 1' for sl in ('container.*', 'weapon.offhand') for p in nested] + ['return 0'])
    fast += ['execute as @a[tag=bm.gvp] at @s if dimension bm:gutter if function bm:h3g/bag/has run function bm:h3g/bag/take',
             'execute as @a[tag=bm.lgbag,tag=!bm.gvp] at @s if dimension bm:gutter if function bm:h3g/bag/has run function bm:h3g/bag/take']
    fn('h3g/bag/take', ['function bm:p155/hands', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                        'execute store result storage bm:gv tmp.pid int 1 run scoreboard players get @s bm.pid', 'function bm:h3g/bag/take2 with storage bm:gv tmp',
                        'playsound minecraft:item.bundle.remove_one player @s ~ ~ ~ 1 0.8',
                        say('No bags on a job - not even with heist gear packed inside. The Fixer keeps it with the rest of your things; '
                            'you\'ll have it back at home.', '#ffcf40')])
    has_nbt = lambda k: f'{{components:{{"minecraft:custom_data":{{bm:"{k}"}}}}}}'
    in_nbt = lambda k: [f'{{components:{{"minecraft:container":[{{item:{has_nbt(k)}}}]}}}}', f'{{components:{{"minecraft:bundle_contents":[{has_nbt(k)}]}}}}']
    fn('h3g/bag/take2', ['$execute unless data storage bm:gv bag.p$(pid) run data modify storage bm:gv bag.p$(pid) set value {inv:[],eq:{}}',
                         'data modify storage bm:gv h3gb set value []'] +
       [f'data modify storage bm:gv h3gb append from entity @s Inventory[{has_nbt(k)}]' for k in P248.BAGS] +
       [f'execute if items entity @s weapon.offhand {bag} run data modify storage bm:gv h3gb append from entity @s equipment.offhand'] +
       [f'execute if items entity @s weapon.offhand {p} run data modify storage bm:gv h3gb append from entity @s equipment.offhand' for p in nested] +
       [f'execute if items entity @s container.{i} {p} run data modify storage bm:gv h3gb append from entity @s Inventory[{{Slot:{i}b}}]' for p in nested for i in range(36)] +
       [f'execute if items entity @s armor.{a} {bag} run data modify storage bm:gv h3gb append from entity @s equipment.{a}' for a in ('head', 'chest', 'legs', 'feet')] +
       ['$data modify storage bm:gv cb.p$(pid) append from storage bm:gv h3gb[]', f'clear @s {bag}'] + [f'clear @s {p}' for p in nested] +
       ['data remove storage bm:gv h3gb'])

    # ================================================================== 2. THE MIRROR MAGE (any heist rider left frozen)
    second.append('execute in bm:gutter as @e[tag=bm.v93ride,tag=!bm.cfrz,distance=0..] if data entity @s {NoAI:1b} unless function bm:h3g/rider/held '
                  'run function bm:cine/release_v')
    fn('h3g/rider/held', ['execute on vehicle if entity @s[tag=bm.cfrz] run return 1', 'return 0'])

    # ================================================================== 3. PARKOUR CHECKPOINTS: cleared with every plan, and on the way out
    for s in range(P70.SLOTS):
        F_[f'p70/s{s}/build'].insert(0, f'scoreboard players reset @a[scores={{bm.gvi={s + 1}}}] bm.gvcpk')
        for f in (f'p70/s{s}/enter', f'p70/s{s}/join'):
            F_[f].insert(0, 'scoreboard players reset @s bm.gvcpk')
        n += 3
    F_['p70/unraid'].insert(0, 'scoreboard players reset @s bm.gvcpk')

    # ================================================================== 4. THE GUARDIAN KEPT IN ITS HALL (and the pit's champion in its pit)
    G.wjson('bm/tags/block/h3g_open.json', {'values': ['#minecraft:replaceable', '#minecraft:slabs', '#minecraft:pressure_plates', '#minecraft:wool_carpets',
                                                  '#minecraft:buttons', '#minecraft:candles', 'minecraft:light', 'minecraft:cobweb', 'minecraft:moss_carpet',
                                                  'minecraft:pale_moss_carpet', 'minecraft:ladder', 'minecraft:iron_chain', 'minecraft:lantern',
                                                  'minecraft:soul_lantern', 'minecraft:lever', '#minecraft:rails']})
    fast += ['execute in bm:gutter as @e[tag=bm.gvboss,distance=0..] at @s run function bm:h3g/arena/keep {r:"vault"}',
             'execute in bm:gutter as @e[tag=bm.h3gb,distance=0..] at @s run function bm:h3g/arena/keep {r:"vault"}',
             'execute in bm:gutter as @e[tag=bm.gvchamp,distance=0..] at @s run function bm:h3g/arena/keep {r:"pit"}']
    fn('h3g/arena/keep', ['execute if entity @s[tag=bm.carr] run return 0', 'scoreboard players operation #gi bm.rng = @s bm.gvi', 'tag @s add bm.h3gme',
                          '$execute as @e[type=minecraft:marker,tag=bm.gvr_$(r),distance=..80] if score @s bm.gvi = #gi bm.rng at @s run function bm:h3g/arena/chk',
                          'tag @s remove bm.h3gme'])
    fn('h3g/arena/chk', ['execute store result score #mx bm.rng run data get entity @s Pos[0] 10', 'execute store result score #my bm.rng run data get entity @s Pos[1] 10',
                         'execute store result score #mz bm.rng run data get entity @s Pos[2] 10',
                         'execute as @e[tag=bm.h3gme,limit=1] store result score #bx bm.rng run data get entity @s Pos[0] 10',
                         'execute as @e[tag=bm.h3gme,limit=1] store result score #by bm.rng run data get entity @s Pos[1] 10',
                         'execute as @e[tag=bm.h3gme,limit=1] store result score #bz bm.rng run data get entity @s Pos[2] 10',
                         'scoreboard players operation #bx bm.rng -= #mx bm.rng', 'scoreboard players operation #by bm.rng -= #my bm.rng',
                         'scoreboard players operation #bz bm.rng -= #mz bm.rng', 'scoreboard players set #out bm.rng 0',
                         'execute unless score #bx bm.rng matches -112..112 run scoreboard players set #out bm.rng 1',
                         'execute unless score #bz bm.rng matches -112..112 run scoreboard players set #out bm.rng 1',
                         'execute unless score #by bm.rng matches -15..110 run scoreboard players set #out bm.rng 1',
                         'execute if score #out bm.rng matches 0 as @e[tag=bm.h3gme,limit=1] at @s unless block ~ ~1.2 ~ #bm:h3g_open run scoreboard players set #out bm.rng 1',
                         'execute if score #out bm.rng matches 0 run return 0',
                         'execute as @e[tag=bm.h3gme,limit=1] positioned ~ ~ ~ run function bm:h3g/arena/back'])
    fn('h3g/arena/back', ['tp @s ~ ~ ~', 'particle minecraft:reverse_portal ~ ~1 ~ 0.5 1 0.5 0.05 30', 'playsound minecraft:entity.enderman.teleport hostile @a[distance=..30] ~ ~ ~ 1 0.6',
                          'execute as @a[tag=bm.gvp,distance=..30] run ' + title('@s', 'actionbar', T('The hall drags it back into the fight.', 'gray'))])
    F_['p70/boss/setup'].append('attribute @s minecraft:knockback_resistance modifier add bm:h3g_kr 0.4 add_value')

    # ================================================================== 5. NO SOUL VIALS IN THE GUTTER
    import phase44 as P44
    for m in P44.VIALS:
        F_[f'p44/vial/got_{m}'][1:1] = ['execute if entity @s[tag=bm.gvp] run return 0', 'execute at @s if dimension bm:gutter run return 0']

    # ================================================================== 6. HEIST BARRELS VANISH (broken, they never drop themselves)
    fresh_barrel = 'minecraft:barrel[!minecraft:container]'
    F_['p74/haul/broke'].insert(0, f'execute as @e[type=minecraft:item,distance=..1.6] if items entity @s contents {fresh_barrel} unless data entity @s Thrower '
                                   'if function bm:h3g/fresh run kill @s')
    fn('h3g/fresh', ['execute store result score #age bm.rng run data get entity @s Age', 'execute if score #age bm.rng matches ..6 run return 1', 'return 0'])
    fast.append('execute in bm:gutter as @e[type=minecraft:item,distance=0..] if items entity @s contents minecraft:barrel[!minecraft:custom_data,!minecraft:container] '
                'unless data entity @s Thrower unless data entity @s Owner run kill @s')

    # ================================================================== 7. THE RAT KING, CROWNED
    n += rat_king(G)

    # ================================================================== 8. FOUR VAULT HALLS; HARD-MODE GUARDIANS
    n += halls(G, rel)
    n += hard_guardians(G, rel)

    # ================================================================== 9. THE GEMS LEAVE THE SHOP (phase89); FORMS COME IN
    gems_in(G)
    return n


# ---------------------------------------------------------------------------------------------------- 9. gems and forms
def gems_in(G):
    import phase144 as P144
    fn, tellraw = G.fn, G.tellraw
    F_ = G.FUNCS
    old_out = list(F_['p126/gem/out'])
    fn('h3g/gem/out_old', old_out[1:])                                     # (a crossing made before 3.0g: undone the old way)
    ap_back = [f'execute if score @s bm.apell matches {k} run loot give @s loot bm:items/{it}' for k, (it, *_r) in P144.FORMS.items()]
    fn('p126/gem/in', ['tag @s add bm.gemlob', 'tag @s add bm.gem3g',
                       # (a gem one of them was given in the lobby before 3.0g: back to you, as the item)
                       'execute if score @s bm.cpell matches 1.. run function bm:h3g/gem/ref_c',
                       'execute if score @s bm.kxell matches 1.. run function bm:h3g/gem/ref_k'] + ap_back +
       ['execute if score @s bm.apell matches 1.. run ' + tellraw('@s', P + [T('Apophiss\'s lobby form comes back to you as its gem - ', GOLD),
                                                                           T('he wears his own form on both sides of the door now.', 'gray')]),
        'scoreboard players set @s bm.apell 0', 'scoreboard players set @s bm.kxelo 0', 'scoreboard players set @s bm.cpelo 0', 'scoreboard players set @s bm.apelo 0',
        'scoreboard players set @s bm.vgk 0', 'scoreboard players set @s bm.vgc 0', 'scoreboard players set @s bm.vgkl 0', 'scoreboard players set @s bm.vgcl 0',
        'function bm:p126/gem/redress'])
    for who, el, vg, back, nm in (('c', 'bm.cpel', 'bm.vgc', 'p69/give_back', 'Cecil'), ('k', 'bm.kxel', 'bm.vgk', 'p79/el/give_back', 'KillerWatt')):
        fn(f'h3g/gem/ref_{who}', [f'scoreboard players operation #c bm.rng = @s {el}', f'scoreboard players operation @s {el} = @s {el}l',
                                  f'scoreboard players operation @s {vg} = @s {vg}l', f'function bm:{back}', f'scoreboard players operation @s {el} = #c bm.rng',
                                  f'scoreboard players set @s {vg} 0', f'scoreboard players set @s {el}l 0', f'scoreboard players set @s {vg}l 0',
                                  tellraw('@s', P + [T(f'The gem {nm} wore in the vault comes back to you - ', GOLD),
                                                     T('he keeps the one he wears outside on both sides of the door now.', 'gray')])])
    fn('p126/gem/out', ['execute unless entity @s[tag=bm.gem3g] run return run function bm:h3g/gem/out_old_t',
                        'tag @s remove bm.gemlob', 'tag @s remove bm.gem3g',
                        # (a vault gem given in the vault still fades at the door)
                        'execute if score @s bm.vgk matches 1 run scoreboard players set @s bm.kxel 0', 'execute if score @s bm.vgc matches 1 run scoreboard players set @s bm.cpel 0',
                        'scoreboard players set @s bm.vgk 0', 'scoreboard players set @s bm.vgc 0', 'function bm:p126/gem/redress'])
    fn('h3g/gem/out_old_t', ['tag @s remove bm.gemlob', 'function bm:h3g/gem/out_old'])


# ---------------------------------------------------------------------------------------------------- 7. the Rat King
def rat_king(G):
    import ratking_art as A
    import rigfol as RF
    import cine as C
    import phase75 as P75
    import phase76 as P76
    fn, title, tellraw = G.fn, G.title, G.tellraw
    F_ = G.FUNCS
    S = A.SCALE
    sel = lambda p: f'@e[type=minecraft:item_display,tag=bm.rksel,tag=bm.rkr_{p}]'
    ME = '@e[type=minecraft:zombie,tag=bm.rkme,limit=1]'
    at = lambda t, cmd: f'execute if score @s bm.rkt matches {t} {cmd[8:]}' if cmd.startswith('execute ') else f'execute if score @s bm.rkt matches {t} run {cmd}'
    snd = lambda s, v, p: f'playsound minecraft:{s} hostile @a[distance=..32] ~ ~ ~ {v} {p}'
    DUR = {'idle_a': 20, 'idle_b': 20, 'walk_0': 5, 'walk_1': 5, 'walk_2': 5, 'walk_3': 5, 'atk_0': 7, 'atk_1': 3, 'sp_0': 10, 'sp_1': 3, 'hurt': 2,
           'death_0': 12, 'death_1': 16, 'arrive_0': 4, 'arrive_1': 10}
    for name, pz in A.POSES.items():
        fn(f'h3g/rk/pose/{name}', RF.pose(A, pz, S, DUR.get(name, 6), sel))
        if name in ('idle_a', 'arrive_0', 'arrive_1', 'death_0', 'death_1'): fn(f'h3g/rk/do/{name}', ['function bm:h3g/rk/mine', f'function bm:h3g/rk/pose/{name}', 'tag @e[type=minecraft:item_display,tag=bm.rksel] remove bm.rksel'])
    fn('h3g/rk/place', RF.place(A, S / 16, sel))
    fn('h3g/rk/rig', [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.rkr", f"bm.rkr_{p}", "bm.rknew", "bm.gvprop"], S, model=A.model_id(p), extra=dict(view_range=F(3.0)))}'
                      for p in A.PARTS])
    fn('h3g/rk/mine', ['scoreboard players operation #me bm.rkid = @s bm.rkid',
                       'execute as @e[type=minecraft:item_display,tag=bm.rkr,distance=..8] if score @s bm.rkid = #me bm.rkid run tag @s add bm.rksel'])

    # ---- the summon (phase76's pit): the zombie host carries the rig now, not the little rat model
    w, key, ty, nm, col, extra, attrs = next(c for c in P76.CHAMPS if c[1] == 'ratking')
    nbt = {'Tags': ['bm.gvg', 'bm.gvchamp', 'bm.gvnew2', 'bm.tiered', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T(nm, col, bold=True), 'CustomNameVisible': B(1),
           'DeathLootTable': 'minecraft:empty', 'drop_chances': {k: F(0) for k in ('head', 'chest', 'legs', 'feet', 'mainhand', 'offhand')}}
    nbt.update(extra)
    nbt['attributes'] = [{'id': f'minecraft:{a}', 'base': Dd(v)} for a, v in dict(attrs, scale=1.4, movement_speed=0.27, knockback_resistance=0.6).items()]
    L = F_['p76/champ/ratking']
    assert L[0].startswith('summon minecraft:zombie ') and any('bm.gvrkd' in l for l in L), L[:3]
    L = [f'summon minecraft:zombie ~ ~ ~ {snbt(nbt)}'] + [l for l in L[1:] if 'bm.gvrkd' not in l]
    k = L.index('tag @e[tag=bm.gvnew2,distance=..4] remove bm.gvnew2')
    L.insert(k + 1, 'execute as @e[type=minecraft:zombie,tag=bm.gvratking,distance=..4,sort=nearest,limit=1] at @s run function bm:h3g/rk/born')
    F_['p76/champ/ratking'] = L
    fn('h3g/rk/born', ['scoreboard players add #rkid bm.rkid 1', 'scoreboard players operation @s bm.rkid = #rkid bm.rkid',
                       'execute store result score @s bm.rkd run attribute @s minecraft:attack_damage base get',
                       'attribute @s minecraft:attack_damage base set 0',          # (his blows are his sceptre's now - the zombie's own swing does nothing)
                       'execute if score @s bm.rkd matches ..4 run scoreboard players set @s bm.rkd 5',
                       'scoreboard players set @s bm.rks 0', 'scoreboard players set @s bm.rkt 0', 'scoreboard players set @s bm.rka 0', 'scoreboard players set @s bm.rkc 80',
                       'execute rotated as @s rotated ~ 0 run function bm:h3g/rk/rig',
                       'scoreboard players operation @e[type=minecraft:item_display,tag=bm.rknew,distance=..2] bm.rkid = @s bm.rkid',
                       'tag @e[type=minecraft:item_display,tag=bm.rknew] remove bm.rknew',
                       'function bm:h3g/rk/do/arrive_0', 'function bm:cine/arr/start'])

    # ---- each tick, as him: his rig on him, and (unless the staging kit has him) what he's doing
    F_['tick'].append('execute as @e[type=minecraft:zombie,tag=bm.gvratking] at @s run function bm:h3g/rk/tick')
    fn('h3g/rk/tick', ['tag @s add bm.rkme', 'function bm:h3g/rk/mine', 'execute unless entity @s[tag=bm.cfrz] run function bm:h3g/rk/fsm',
                       'execute rotated as @s rotated ~ 0 run function bm:h3g/rk/place',
                       'tag @e[type=minecraft:item_display,tag=bm.rksel] remove bm.rksel', 'tag @s remove bm.rkme'])
    fn('h3g/rk/fsm', ['scoreboard players add @s bm.rkt 1', 'scoreboard players add @s bm.rka 1', 'scoreboard players add @s bm.rkc 1',
                      'execute if score @s bm.rks matches 0 store result score #ht bm.rng run data get entity @s HurtTime',
                      'execute if score @s bm.rks matches 0 if score #ht bm.rng matches 9.. run return run function bm:h3g/rk/hurt0',
                      'execute if score @s bm.rks matches 0 run return run function bm:h3g/rk/s/move',
                      'execute if score @s bm.rks matches 1 run return run function bm:h3g/rk/s/atk',
                      'execute if score @s bm.rks matches 2 run return run function bm:h3g/rk/s/sp',
                      'execute if score @s bm.rks matches 3 run return run function bm:h3g/rk/s/hurt'])
    near = f'@a[distance=..3.2,{FOES}]'
    fn('h3g/rk/s/move', ['execute store result score #x bm.rng run data get entity @s Pos[0] 100', 'execute store result score #z bm.rng run data get entity @s Pos[2] 100',
                         'scoreboard players operation #dx bm.rng = #x bm.rng', 'scoreboard players operation #dx bm.rng -= @s bm.rkx',
                         'scoreboard players operation #dz bm.rng = #z bm.rng', 'scoreboard players operation #dz bm.rng -= @s bm.rkz',
                         'scoreboard players operation @s bm.rkx = #x bm.rng', 'scoreboard players operation @s bm.rkz = #z bm.rng',
                         'execute if score #dx bm.rng matches ..-1 run scoreboard players operation #dx bm.rng *= #-1 bm.rng',
                         'execute if score #dz bm.rng matches ..-1 run scoreboard players operation #dz bm.rng *= #-1 bm.rng',
                         'scoreboard players operation #dx bm.rng += #dz bm.rng',
                         'scoreboard players operation #f bm.rng = @s bm.rkt', 'scoreboard players operation #f bm.rng %= #20 bm.rng',
                         'scoreboard players operation #g bm.rng = @s bm.rkt', 'scoreboard players operation #g bm.rng %= #40 bm.rng',
                         'execute if score #dx bm.rng matches 3.. if score #f bm.rng matches 0 run function bm:h3g/rk/pose/walk_0',
                         'execute if score #dx bm.rng matches 3.. if score #f bm.rng matches 5 run function bm:h3g/rk/pose/walk_1',
                         'execute if score #dx bm.rng matches 3.. if score #f bm.rng matches 10 run function bm:h3g/rk/pose/walk_2',
                         'execute if score #dx bm.rng matches 3.. if score #f bm.rng matches 15 run function bm:h3g/rk/pose/walk_3',
                         'execute if score #dx bm.rng matches 3.. if score #f bm.rng matches 0 run ' + snd('entity.ravager.step', 0.6, 1.4),
                         'execute if score #dx bm.rng matches 3.. if score #f bm.rng matches 10 run ' + snd('entity.ravager.step', 0.6, 1.5),
                         'execute if score #dx bm.rng matches ..2 if score #g bm.rng matches 0 run function bm:h3g/rk/pose/idle_a',
                         'execute if score #dx bm.rng matches ..2 if score #g bm.rng matches 20 run function bm:h3g/rk/pose/idle_b',
                         'execute if score #g bm.rng matches 30 run ' + snd('entity.silverfish.ambient', 0.9, 0.5),
                         f'execute if score @s bm.rkc matches 170.. if entity @a[distance=..9,{FOES}] run return run function bm:h3g/rk/sp0',
                         f'execute if score @s bm.rka matches 24.. if entity {near} run return run function bm:h3g/rk/atk0'])
    face = f'execute facing entity @p[distance=..16,{FOES}] feet run tp @s ~ ~ ~ ~ 0'
    # ---- the sceptre: hauled back over his shoulder, brought down in front of him
    fn('h3g/rk/atk0', ['scoreboard players set @s bm.rks 1', 'scoreboard players set @s bm.rkt 0', 'scoreboard players set @s bm.rka 0',
                       'data merge entity @s {NoAI:1b}', face, 'function bm:h3g/rk/pose/atk_0', snd('entity.rabbit.attack', 1.2, 0.5), snd('item.trident.throw', 0.8, 0.6)])
    fn('h3g/rk/s/atk', [at(7, 'function bm:h3g/rk/pose/atk_1'), at(9, 'function bm:h3g/rk/strike'), at(16, 'function bm:h3g/rk/pose/idle_a'),
                        at(18, 'data merge entity @s {NoAI:0b}'), at(18, 'scoreboard players set @s bm.rks 0')])
    fn('h3g/rk/strike', ['execute store result storage bm:gv rk.d int 1 run scoreboard players get @s bm.rkd', 'function bm:h3g/rk/strike2 with storage bm:gv rk',
                         'execute positioned ^ ^ ^1.6 run particle minecraft:sweep_attack ~ ~1 ~ 0.6 0.2 0.6 0 3',
                         'execute positioned ^ ^ ^1.6 run particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.3 ~ 0.6 0.1 0.6 0.1 14',
                         snd('entity.player.attack.knockback', 1.2, 0.6), snd('block.anvil.land', 0.5, 1.4)])
    fn('h3g/rk/strike2', [f'$execute positioned ^ ^ ^1.6 as @a[distance=..2.4,{FOES}] run damage @s $(d) minecraft:mob_attack by {ME}'])
    # ---- THE ROYAL DECREE: rearing up, a screech, the sceptre slammed down - a shockwave, and two Plague Rats
    ty_, rat = P75._mob('silverfish', 'Plague Rat', '#8a7a5a', {}, {}, {'scale': 1.6, 'movement_speed': 0.3, 'attack_damage': 3.0})
    fn('h3g/rk/sp0', ['scoreboard players set @s bm.rks 2', 'scoreboard players set @s bm.rkt 0', 'scoreboard players set @s bm.rkc 0',
                      'data merge entity @s {NoAI:1b}', face, 'function bm:h3g/rk/pose/sp_0', snd('entity.ravager.roar', 1.4, 1.6), snd('entity.silverfish.hurt', 1.4, 0.5),
                      'execute as @a[tag=bm.gvp,distance=..30] run ' + title('@s', 'actionbar', [T('THE ROYAL DECREE! ', '#ffd040', bold=True), T('Get clear of him!', 'gray')])])
    fn('h3g/rk/s/sp', ['execute if score @s bm.rkt matches 2..20 run particle minecraft:dust{color:[1.0,0.82,0.25],scale:1.5} ~ ~3.2 ~ 0.6 0.6 0.6 0 4',
                       'execute if score @s bm.rkt matches 2..20 run particle minecraft:squid_ink ~ ~0.2 ~ 2.5 0.1 2.5 0.02 3',
                       at(20, 'function bm:h3g/rk/pose/sp_1'), at(23, 'function bm:h3g/rk/decree'), at(40, 'function bm:h3g/rk/pose/idle_a'),
                       at(44, 'data merge entity @s {NoAI:0b}'), at(44, 'scoreboard players set @s bm.rks 0')])
    fn('h3g/rk/decree', ['execute store result storage bm:gv rk.d int 1 run scoreboard players get @s bm.rkd', 'function bm:h3g/rk/decree2 with storage bm:gv rk',
                         'particle minecraft:explosion ~ ~0.3 ~ 2 0.1 2 0 8', 'particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.2 ~ 3 0.1 3 0.2 60'] +
       C.ring('minecraft:dust{color:[1.0,0.82,0.25],scale:2.0}', 3.0, 24, 0.2) + C.ring('minecraft:dust{color:[0.55,0.45,0.3],scale:2.0}', 5.0, 36, 0.2) +
       [snd('item.mace.smash_ground_heavy', 1.4, 0.8), snd('entity.generic.explode', 0.8, 1.2),
        'scoreboard players operation #gi bm.rng = @s bm.gvi', 'function bm:p70/ctx', 'execute store result score #ng bm.rng if entity @e[tag=bm.gvg,distance=..20]',
        'execute if score #ng bm.rng matches ..6 positioned ^1.6 ^ ^1 run summon minecraft:' + ty_ + ' ~ ~ ~ ' + snbt(rat),
        'execute if score #ng bm.rng matches ..6 positioned ^1.6 ^ ^1 run function bm:p70/guard_set',
        'execute if score #ng bm.rng matches ..6 positioned ^-1.6 ^ ^1 run summon minecraft:' + ty_ + ' ~ ~ ~ ' + snbt(rat),
        'execute if score #ng bm.rng matches ..6 positioned ^-1.6 ^ ^1 run function bm:p70/guard_set'])
    fn('h3g/rk/decree2', [f'$execute as @a[distance=..5.5,{FOES}] run damage @s $(d) minecraft:mob_attack by {ME}',
                          f'execute as @a[distance=..5.5,{FOES}] run effect give @s minecraft:slowness 2 1'])
    # ---- hurt: a flinch
    fn('h3g/rk/hurt0', ['scoreboard players set @s bm.rks 3', 'scoreboard players set @s bm.rkt 0', 'function bm:h3g/rk/pose/hurt', snd('entity.silverfish.hurt', 1.2, 0.6)])
    fn('h3g/rk/s/hurt', [at(7, 'function bm:h3g/rk/pose/idle_a'), at(8, 'scoreboard players set @s bm.rks 0')])
    F_['load'][-1:-1] = ['scoreboard players set #-1 bm.rng -1', 'scoreboard players set #20 bm.rng 20', 'scoreboard players set #40 bm.rng 40']

    # ---- the entrance and the fall: the staging kit's timelines (arrival 40 ticks; death 56, then killed as by the crew)
    a = lambda t, *c: C.at('bm.cat', t, *c)
    d = lambda t, *c: C.at('bm.cdt', t, *c)
    arr = [*a(1, 'particle minecraft:squid_ink ~ ~0.3 ~ 1.2 0.1 1.2 0.05 30', C.snd('entity.silverfish.ambient', 1.4, 0.4)),
           *a(14, 'function bm:h3g/rk/do/arrive_1', C.snd('entity.ravager.roar', 1.4, 1.5), C.snd('entity.silverfish.death', 1.0, 0.5)),
           *a(16, 'particle minecraft:dust{color:[1.0,0.82,0.25],scale:1.8} ~ ~3.4 ~ 0.6 0.4 0.6 0 30'),
           *C.shake('bm.cat', 14, 10, 0.6, r=24),
           *a(34, 'function bm:h3g/rk/do/idle_a')]
    die = [*d(1, 'function bm:h3g/rk/do/death_0', C.snd('entity.silverfish.death', 1.6, 0.4), C.snd('entity.ravager.hurt', 1.0, 1.4)),
           *d(20, 'function bm:h3g/rk/do/death_1'), *d(22, C.snd('entity.ravager.step', 1.4, 0.5), C.snd('block.anvil.land', 0.6, 0.7),
                                                        'particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.3 ~ 1.4 0.1 1.4 0.1 30'),
           *C.shake('bm.cdt', 22, 8, 0.5, r=24),
           *d(54, 'particle minecraft:poof ~ ~0.6 ~ 1.2 0.4 1.2 0.02 30', 'function bm:h3g/rk/mine',
              'kill @e[type=minecraft:item_display,tag=bm.rksel]')]
    C.stage(G, 'rk', 'zombie', 'bm.gvratking', arr, die, None, arrive_len=40, die_len=56, arm=True)
    # (a part left behind - its king gone - goes; a rig short a part, rebuilt)
    G.FUNCS['loop/second'] += ['execute as @e[type=minecraft:item_display,tag=bm.rkr] at @s unless entity @e[type=minecraft:zombie,tag=bm.gvratking,distance=..6] run kill @s',
                               'execute as @e[type=minecraft:zombie,tag=bm.gvratking,tag=!bm.cdie] at @s run function bm:h3g/rk/sec']
    fn('h3g/rk/sec', ['function bm:h3g/rk/mine', 'execute store result score #np bm.rng if entity @e[type=minecraft:item_display,tag=bm.rksel]',
                      f'execute unless score #np bm.rng matches {len(A.PARTS)} run function bm:h3g/rk/rerig',
                      'tag @e[type=minecraft:item_display,tag=bm.rksel] remove bm.rksel'])
    fn('h3g/rk/rerig', ['kill @e[type=minecraft:item_display,tag=bm.rksel]', 'execute rotated as @s rotated ~ 0 run function bm:h3g/rk/rig',
                        'scoreboard players operation @e[type=minecraft:item_display,tag=bm.rknew,distance=..2] bm.rkid = @s bm.rkid',
                        'tag @e[type=minecraft:item_display,tag=bm.rknew] remove bm.rknew', 'function bm:h3g/rk/do/idle_a'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.rkr]']
    return 1


# ---------------------------------------------------------------------------------------------------- 8. the four halls
def halls(G, rel):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    F_ = G.FUNCS
    snd = lambda s, v, p, r=30: f'playsound minecraft:{s} hostile @a[distance=..{r}] ~ ~ ~ {v} {p}'
    crew = lambda: '@a[tag=bm.gvp,distance=..40]'
    ident = [F(0), F(0), F(0), F(1)]

    # ---- the draw (as the vault's marker, when the heist is laid out); the plates only for the Weighing Floor; a sign at the door
    init = F_['p70/r/vault/init']
    plates = [i for i, l in enumerate(init) if l.startswith('setblock ') and l.endswith('minecraft:light_weighted_pressure_plate')]
    assert len(plates) == 4, plates
    for i in plates:
        init[i] = 'execute if score @s bm.h3gl matches 0 run ' + init[i]
    init[0:0] = ['execute store result score @s bm.h3gl run random value 0..3',
                 'execute if score #flay bm.gvv matches 0..3 run scoreboard players operation @s bm.h3gl = #flay bm.gvv']
    for k, (nm, txt) in LAYOUTS.items():
        sign = {'Tags': ['bm.gvprop', 'bm.h3gsign'], 'billboard': 'vertical', 'brightness': {'block': Int(15), 'sky': Int(15)}, 'background': Int(0x90000000 - 2 ** 32),
                'text': [T(nm + '\n', GOLD, bold=True), T(txt, 'gray')], 'alignment': 'center', 'line_width': Int(200),
                'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0.55)] * 3}}
        init.append(f'execute if score @s bm.h3gl matches {k} run summon minecraft:text_display {rel(3, 7.2, 8)} {snbt(sign)}')
    init.append(f'execute if score @s bm.h3gl matches 3 run summon minecraft:marker ~ ~ ~ {{Tags:["bm.gvprop","bm.h3gbl"]}}')
    init.append('execute if score @s bm.h3gl matches 3 run scoreboard players operation @e[type=minecraft:marker,tag=bm.h3gbl,distance=..0.5] bm.gvi = @s bm.gvi')
    for k, (nm, txt) in LAYOUTS.items():
        fn(f'h3g/lay/say{k}', ['execute as @a[tag=bm.gvp,distance=..40] run ' + tellraw('@s', P + [T(nm + ': ', GOLD, bold=True), T(txt, 'gray')])])
    F_['p70/boss/spawn'].append('function bm:h3g/lay/say')
    fn('h3g/lay/say', [f'execute if score @s bm.h3gl matches {k} run function bm:h3g/lay/say{k}' for k in LAYOUTS])
    for k, nm in (('flay', 'layout'),):
        pass
    for v in LAYOUTS:
        fn(f'admin/heist_hall_{v}', [f'scoreboard players set #flay bm.gvv {v}', tellraw('@s', P + [T(f'Every vault hall is {LAYOUTS[v][0]} now.', 'gray')])])
    fn('admin/heist_hall_any', ['scoreboard players reset #flay bm.gvv', tellraw('@s', P + [T('The vault hall is drawn by chance again.', 'gray')])])

    # ---- the shell: what cracks it, hall by hall (count_plates runs as the vault's marker; #n 4 cracks it)
    cp = F_['p70/boss/count_plates']
    cp[0:0] = ['execute if score @s bm.h3gl matches 1 run return run function bm:h3g/lay/py/count',
               'execute if score @s bm.h3gl matches 2..3 run return run function bm:h3g/lay/crk']
    fn('h3g/lay/crk', ['execute if entity @e[tag=bm.gvboss,tag=bm.h3gcrk,distance=..40] run scoreboard players set #n bm.rng 4',
                       'tag @e[tag=bm.h3gcrk,distance=..40] remove bm.h3gcrk'])
    sh = F_['p70/boss/shell']
    k = next(i for i, l in enumerate(sh) if 'Press the hall' in l)
    sh[k] = 'execute if score #h3gl bm.rng matches 0 run ' + sh[k]
    sh[k + 1:k + 1] = [f'execute if score #h3gl bm.rng matches {v} as @a[tag=bm.gvp,distance=..30] run ' +
                       title('@s', 'actionbar', [T('It shells itself in gold! ', GOLD, bold=True), T(msg, 'gray')])
                       for v, msg in ((1, 'Smash the four soul pylons to crack it.'), (2, 'Lure it over the cracking floor.'),
                                      (3, 'Hold the hub while the blade cuts it.'))]
    sh[0:0] = ['scoreboard players set #h3gl bm.rng 0', 'tag @s remove bm.h3gcrk',
               'execute as @e[type=minecraft:marker,tag=bm.gvr_vault,distance=..40,sort=nearest,limit=1] run scoreboard players operation #h3gl bm.rng = @s bm.h3gl',
               'execute if score #h3gl bm.rng matches 1 as @e[type=minecraft:marker,tag=bm.gvr_vault,distance=..40,sort=nearest,limit=1] at @s run function bm:h3g/lay/py/up']
    F_['p70/boss/unshell'] += ['tag @s remove bm.h3gcrk',
                               'execute as @e[type=minecraft:marker,tag=bm.gvr_vault,distance=..40,sort=nearest,limit=1] at @s run function bm:h3g/lay/py/down']

    # ---- the hall's own hazards, each tick of the fight (as the vault's marker)
    vt = F_['p70/r/vault/tick']
    vt.append('execute if score @s bm.gvs matches 1 if score @s bm.h3gl matches 1..3 run function bm:h3g/lay/tick')
    fn('h3g/lay/tick', ['execute if entity @e[tag=bm.gvboss,tag=bm.carr,distance=..30] run return 0',
                        'execute if score @s bm.h3gl matches 1 run function bm:h3g/lay/py/tick',
                        'execute if score @s bm.h3gl matches 2 run function bm:h3g/lay/cr/tick',
                        'execute if score @s bm.h3gl matches 3 as @e[type=minecraft:marker,tag=bm.h3gbl,distance=..2,limit=1] at @s run function bm:h3g/lay/bl/tick'])
    # (the vault open: every hazard put away, the floor mended)
    F_['p70/r/vault/opened'].append('function bm:h3g/lay/end')
    fn('h3g/lay/end', ['function bm:h3g/lay/py/down', 'execute as @e[type=minecraft:marker,tag=bm.h3gcr,distance=..20] at @s run function bm:h3g/lay/cr/mend',
                       'kill @e[type=minecraft:marker,tag=bm.h3gbl,distance=..2]'])

    # ---- THE PYLON HALL
    pyl = {'Tags': ['bm.gvprop', 'bm.h3gpy', 'bm.h3gpn'], 'width': F(1.3), 'height': F(2.6), 'response': B(0)}
    base = {'Tags': ['bm.gvprop', 'bm.h3gpyd'], 'block_state': {'id': 'minecraft:respawn_anchor', 'properties': {'charges': '4'}}, 'brightness': {'block': Int(15), 'sky': Int(15)},
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(-0.5), F(0), F(-0.5)], 'scale': [F(1.0)] * 3}}
    top = {'Tags': ['bm.gvprop', 'bm.h3gpyd'], 'block_state': {'id': 'minecraft:soul_lantern', 'properties': {'hanging': 'false'}}, 'brightness': {'block': Int(15), 'sky': Int(15)},
           'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(-0.6), F(1.0), F(-0.6)], 'scale': [F(1.2), F(1.5), F(1.2)]}}
    fn('h3g/lay/py/up', ['function bm:h3g/lay/py/down'] +
       sum(([f'summon minecraft:interaction {rel(x, 4, z)} {snbt(pyl)}', f'summon minecraft:block_display {rel(x, 4, z)} {snbt(base)}',
             f'summon minecraft:block_display {rel(x, 4, z)} {snbt(top)}', f'particle minecraft:soul_fire_flame {rel(x, 5, z)} 0.3 0.8 0.3 0.05 30']
            for (x, z) in PYLONS), []) +
       ['scoreboard players set @e[type=minecraft:interaction,tag=bm.h3gpn,distance=..20] bm.h3gph 3', 'tag @e[tag=bm.h3gpn] remove bm.h3gpn',
        snd('block.respawn_anchor.charge', 1.4, 0.6, 40), snd('block.beacon.activate', 1, 0.6, 40)])
    fn('h3g/lay/py/down', ['kill @e[type=minecraft:interaction,tag=bm.h3gpy,distance=..20]', 'kill @e[type=minecraft:block_display,tag=bm.h3gpyd,distance=..20]'])
    fn('h3g/lay/py/count', ['execute store result score #n bm.rng if entity @e[type=minecraft:interaction,tag=bm.h3gpy,distance=..20]',
                            'scoreboard players set #q bm.rng 4', 'scoreboard players operation #q bm.rng -= #n bm.rng',
                            'scoreboard players operation #n bm.rng = #q bm.rng',
                            'execute unless entity @e[type=minecraft:interaction,tag=bm.h3gpy,distance=..20] run scoreboard players set #n bm.rng 4'])
    fn('h3g/lay/py/tick', ['execute as @e[type=minecraft:interaction,tag=bm.h3gpy,distance=..20] if data entity @s attack at @s run function bm:h3g/lay/py/hit',
                           'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #40 bm.rng',
                           'execute if score #q bm.rng matches 0 as @e[type=minecraft:interaction,tag=bm.h3gpy,distance=..20] at @s run function bm:h3g/lay/py/zap',
                           'execute if score #q bm.rng matches 10 as @e[type=minecraft:interaction,tag=bm.h3gpy,distance=..20] at @s run particle minecraft:soul ~ ~2.2 ~ 0.3 0.4 0.3 0.02 4'])
    fn('h3g/lay/py/hit', ['data remove entity @s attack', 'scoreboard players remove @s bm.h3gph 1',
                          'particle minecraft:electric_spark ~ ~1.4 ~ 0.4 0.6 0.4 0.2 20', snd('block.amethyst_block.hit', 1.4, 0.6, 20), snd('block.respawn_anchor.deplete', 0.8, 1.4, 20),
                          'execute if score @s bm.h3gph matches ..0 run function bm:h3g/lay/py/break'])
    fn('h3g/lay/py/break', ['particle minecraft:explosion ~ ~1 ~ 0.3 0.6 0.3 0 3', 'particle minecraft:soul_fire_flame ~ ~1.2 ~ 0.4 0.8 0.4 0.1 40',
                            snd('block.glass.break', 1.4, 0.6, 30), snd('entity.generic.explode', 0.6, 1.4, 30),
                            'kill @e[type=minecraft:block_display,tag=bm.h3gpyd,distance=..1.2]',
                            'execute as @a[tag=bm.gvp,distance=..30] run ' + title('@s', 'actionbar', T('A pylon shatters!', '#7ae8ff', bold=True)), 'kill @s'])
    fn('h3g/lay/py/zap', [f'execute as @a[tag=bm.gvp,distance=..22,{FOES},sort=random,limit=1] at @s run function bm:h3g/lay/py/zap1'])
    fn('h3g/lay/py/zap1', ['damage @s 3 minecraft:magic', 'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.1 12',
                           'execute facing entity @e[type=minecraft:interaction,tag=bm.h3gpy,sort=nearest,limit=1] feet run function bm:h3g/lay/py/beam',
                           'playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..20] ~ ~ ~ 0.8 1.6'])
    fn('h3g/lay/py/beam', [f'particle minecraft:soul_fire_flame ^ ^1.2 ^{d / 2} 0 0 0 0 1' for d in range(1, 30)])

    # ---- THE CRUMBLING HALL (a crack every 2 s under a raider on the hall's floor - never near the middle, the walls, another crack)
    fn('h3g/lay/cr/tick', ['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #40 bm.rng',
                           'execute if score #q bm.rng matches 0 as @a[tag=bm.gvp,distance=..16,' + FOES + ',sort=random,limit=1] at @s run function bm:h3g/lay/cr/try',
                           'execute as @e[type=minecraft:marker,tag=bm.h3gcr,distance=..20] at @s run function bm:h3g/lay/cr/step'])
    fn('h3g/lay/cr/try', ['execute store result score #px bm.rng run data get entity @s Pos[0] 10', 'execute store result score #py bm.rng run data get entity @s Pos[1] 10',
                          'execute store result score #pz bm.rng run data get entity @s Pos[2] 10',
                          'execute store result score #vx bm.rng run data get entity @e[type=minecraft:marker,tag=bm.gvr_vault,sort=nearest,limit=1] Pos[0] 10',
                          'execute store result score #vy bm.rng run data get entity @e[type=minecraft:marker,tag=bm.gvr_vault,sort=nearest,limit=1] Pos[1] 10',
                          'execute store result score #vz bm.rng run data get entity @e[type=minecraft:marker,tag=bm.gvr_vault,sort=nearest,limit=1] Pos[2] 10',
                          'scoreboard players operation #px bm.rng -= #vx bm.rng', 'scoreboard players operation #py bm.rng -= #vy bm.rng', 'scoreboard players operation #pz bm.rng -= #vz bm.rng',
                          'execute unless score #py bm.rng matches -3..3 run return 0',
                          'execute unless score #px bm.rng matches -80..80 run return 0', 'execute unless score #pz bm.rng matches -80..80 run return 0',
                          'execute if score #px bm.rng matches -25..25 if score #pz bm.rng matches -25..25 run return 0',
                          'execute align xz positioned ~0.5 ~ ~0.5 if entity @e[type=minecraft:marker,tag=bm.h3gcr,distance=..4.5] run return 0',
                          'execute align xz positioned ~0.5 ~ ~0.5 if block ~ ~-1 ~ minecraft:air run return 0',
                          'execute align xz positioned ~0.5 ~ ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["bm.gvprop","bm.h3gcr","bm.h3gcrn"]}',
                          'execute store result entity @e[type=minecraft:marker,tag=bm.h3gcrn,limit=1] Pos[1] double 1 run data get entity '
                          '@e[type=minecraft:marker,tag=bm.gvr_vault,sort=nearest,limit=1] Pos[1]',
                          'scoreboard players set @e[type=minecraft:marker,tag=bm.h3gcrn] bm.h3gt 0', 'tag @e[type=minecraft:marker,tag=bm.h3gcrn] remove bm.h3gcrn',
                          snd('block.pointed_dripstone.break', 1.2, 0.6, 16)])
    crack = 'particle minecraft:block{block_state:"minecraft:polished_blackstone"} ~ ~0.1 ~ 0.9 0.05 0.9 0 10'
    fn('h3g/lay/cr/step', ['scoreboard players add @s bm.h3gt 1',
                           f'execute if score @s bm.h3gt matches ..29 run {crack}',
                           'execute if score @s bm.h3gt matches ..29 run particle minecraft:dust{color:[0.9,0.3,0.1],scale:1.0} ~ ~0.05 ~ 1 0 1 0 2',
                           'execute if score @s bm.h3gt matches 10 run ' + snd('block.deepslate.break', 1, 0.6, 16),
                           'execute if score @s bm.h3gt matches 30 run function bm:h3g/lay/cr/fall',
                           'execute if score @s bm.h3gt matches 31..190 positioned ~-1.5 ~-3 ~-1.5 as @a[dx=2,dy=2.5,dz=2] at @s run function bm:h3g/lay/cr/pit',
                           'execute if score @s bm.h3gt matches 190.. run function bm:h3g/lay/cr/mend'])
    fn('h3g/lay/cr/fall', ['clone ~-1 ~-1 ~-1 ~1 ~-1 ~1 ~-1 ~-4 ~-1', 'fill ~-1 ~-2 ~-1 ~1 ~-1 ~1 minecraft:air',
                           'particle minecraft:block{block_state:"minecraft:polished_blackstone"} ~ ~ ~ 1 0.2 1 0.2 50', 'particle minecraft:large_smoke ~ ~ ~ 1 0.2 1 0.02 12',
                           snd('block.stone.break', 1.4, 0.5, 24), snd('entity.generic.explode', 0.6, 0.8, 24),
                           'execute positioned ~-1.5 ~-0.5 ~-1.5 as @e[tag=bm.gvboss,tag=bm.gvshell,dx=2,dy=3,dz=2] run tag @s add bm.h3gcrk'])
    fn('h3g/lay/cr/pit', ['damage @s 3 minecraft:fall', 'execute at @e[type=minecraft:marker,tag=bm.gvr_vault,sort=nearest,limit=1] run tp @s ~-10 ~ ~ -90 0',
                          title('@s', 'actionbar', T('The floor gave way - back to the hall\'s door!', 'red'))])
    fn('h3g/lay/cr/mend', ['execute if score @s bm.h3gt matches 30.. run clone ~-1 ~-4 ~-1 ~1 ~-4 ~1 ~-1 ~-1 ~-1',
                           'execute if score @s bm.h3gt matches 30.. run fill ~-1 ~-2 ~-1 ~1 ~-2 ~1 minecraft:blackstone',
                           'execute if score @s bm.h3gt matches 30.. run fill ~-1 ~-4 ~-1 ~1 ~-4 ~1 minecraft:blackstone',
                           'execute if score @s bm.h3gt matches 30.. run particle minecraft:wax_on ~ ~0.2 ~ 1 0.1 1 0 12', 'kill @s'])

    # ---- THE TURNING BLADE (as its marker, at the hall's middle: the blade's angle its yaw, 3 a tick - 5 while the guardian shells)
    fn('h3g/lay/bl/tick', ['scoreboard players add @s bm.h3gba 3',
                           'execute if entity @e[tag=bm.gvboss,tag=bm.gvshell,distance=..20] run scoreboard players add @s bm.h3gba 2',
                           'execute if score @s bm.h3gba matches 360.. run scoreboard players remove @s bm.h3gba 360',
                           'execute store result entity @s Rotation[0] float 1 run scoreboard players get @s bm.h3gba',
                           'scoreboard players set #hub bm.rng 0', 'execute if entity @a[tag=bm.gvp,distance=..1.6] run scoreboard players set #hub bm.rng 1',
                           'execute rotated as @s rotated ~ 0 run function bm:h3g/lay/bl/sweep',
                           'scoreboard players operation #q bm.rng = @s bm.h3gba', 'scoreboard players operation #q bm.rng %= #10 bm.rng'] +
       ['execute if score #q bm.rng matches 0..2 run ' + l for l in __import__('cine').ring('minecraft:dust{color:[1.0,0.82,0.3],scale:1.2}', 1.5, 12, 0.1)])
    sweep = []
    for r in range(2, 12):
        sweep += [f'execute positioned ^ ^0.3 ^{r} run particle minecraft:soul_fire_flame ~ ~ ~ 0.05 0.08 0.05 0.005 1',
                  f'execute positioned ^ ^0.3 ^{r} run particle minecraft:dust{{color:[0.4,0.9,1.0],scale:1.0}} ~ ~ ~ 0.05 0.05 0.05 0 1',
                  f'execute positioned ^ ^0.3 ^{r} as @a[tag=bm.gvp,distance=..0.9,{FOES}] unless score @s bm.h3gbc matches 1.. at @s run function bm:h3g/lay/bl/cut',
                  f'execute if score #hub bm.rng matches 1 positioned ^ ^1 ^{r} as @e[tag=bm.gvboss,tag=bm.gvshell,distance=..1.6] run tag @s add bm.h3gcrk']
    fn('h3g/lay/bl/sweep', sweep)
    fn('h3g/lay/bl/cut', ['damage @s 4 minecraft:magic', 'scoreboard players set @s bm.h3gbc 10', 'particle minecraft:soul_fire_flame ~ ~0.5 ~ 0.2 0.3 0.2 0.05 12',
                          'playsound minecraft:item.trident.riptide_1 hostile @a[distance=..16] ~ ~ ~ 0.8 1.6',
                          title('@s', 'actionbar', T('The blade! Jump it.', '#7ae8ff', bold=True))])
    F_['tick'].append('scoreboard players remove @a[scores={bm.h3gbc=1..}] bm.h3gbc 1')
    return 1


# ---------------------------------------------------------------------------------------------------- 8. hard-mode guardians
def hard_guardians(G, rel):
    HBARS = {}
    def hbar(k, nm, col):
        HBARS[k] = (nm, col)
        return f'function bm:h3g/hb/bar_{k}'
    import phase70 as P70
    import phase245 as P245
    import phase246 as P246
    import phase258 as P258
    fn, title, tellraw = G.fn, G.title, G.tellraw
    F_ = G.FUNCS
    SL = P70.SLOTS
    # ---- the roll (as the vault's marker, its fight just begun): hard mode, a vault in three (an admin's flag: #fhb 1 always, -1 never)
    sp = F_['p70/boss/spawn']
    k = sp.index('function bm:p70/ctx')
    sp.insert(k + 1, 'execute if function bm:h3g/hb/roll run return run function bm:h3g/hb/go')
    fn('h3g/hb/roll', ['execute unless score #hard bm.cfg matches 1 run return 0', 'execute if score #fhb bm.gvv matches -1 run return 0',
                       'execute if score #fhb bm.gvv matches 1 run return 1',
                       'execute store result score #r bm.rng run random value 1..100', f'execute if score #r bm.rng matches ..{HB_PCT} run return 1', 'return 0'])
    fn('h3g/hb/go', ['execute store result score #hk bm.rng run random value 1..3', 'execute if score #fhbk bm.gvv matches 1..3 run scoreboard players operation #hk bm.rng = #fhbk bm.gvv',
                     'execute if score #hk bm.rng matches 1 if score #dfell bm.cfg matches 1 run scoreboard players set #hk bm.rng 3',
                     'execute if score #hk bm.rng matches 2 if score #vfell bm.cfg matches 1 run scoreboard players set #hk bm.rng 3',
                     'execute store result score #np bm.rng if entity @a[tag=bm.gvp,distance=..40]',
                     'execute if score #hk bm.rng matches 1 run function bm:h3g/hb/mire',
                     'execute if score #hk bm.rng matches 2 run function bm:h3g/hb/brood',
                     'execute if score #hk bm.rng matches 3 run function bm:h3g/hb/knight',
                     'function bm:h3g/lay/say'])
    # ---- the Mires: their own summon (a puddle that rises for the crew), kept to the hall, never melted by its lamps
    fn('h3g/hb/mire', ['function bm:p246/spawn',
                       'execute as @e[type=minecraft:husk,tag=bm.mire,tag=!bm.h3gb,distance=..40] if score @s bm.mid = #mid bm.mid run function bm:h3g/hb/set {f:100,c:"red"}',
                       'execute as @e[type=minecraft:husk,tag=bm.mire,tag=bm.h3gb,distance=..40] if score @s bm.mid = #mid bm.mid run tag @s add bm.muc',
                       hbar('mire', T(P246.NAME, P246.COL, bold=True), 'red'),
                       'execute as @a[tag=bm.gvp,distance=..40] run ' + title('@s', 'title', T('A Dread Mire guards the vault', P246.COL, bold=True)),
                       'execute as @a[tag=bm.gvp,distance=..40] run ' + title('@s', 'subtitle', T('Hard mode: the Dread has found its way in', 'gray', italic=True))])
    fn('h3g/hb/brood', ['function bm:p258/spawn',
                        'execute as @e[type=minecraft:husk,tag=bm.bmire,tag=!bm.h3gb,distance=..40] if score @s bm.mid = #mid bm.mid run function bm:h3g/hb/set {f:100,c:"green"}',
                        'execute as @e[type=minecraft:husk,tag=bm.bmire,tag=bm.h3gb,distance=..40] if score @s bm.mid = #mid bm.mid run tag @s add bm.bxroam',
                        hbar('brood', T(P258.NAME, P258.COL, bold=True), 'purple'),
                        'execute as @a[tag=bm.gvp,distance=..40] run ' + title('@s', 'title', T('A Brood-Mire guards the vault', P258.COL, bold=True)),
                        'execute as @a[tag=bm.gvp,distance=..40] run ' + title('@s', 'subtitle', T('Hard mode: the Vorn have been here first', 'gray', italic=True))])
    assert P246.FLOOR == 100 and P258.FLOOR == 100 and P245.FLOOR == 100
    # ---- the Statue Knights: a statue raised on a marker of its own (phase245's raise), and its host woken from it
    for kind, c in P245.KN.items():
        host = {'Tags': ['bm.khost', f'bm.kh_{kind}', 'bm.seen', 'bm.knewh', 'bm.h3gkn'], 'NoAI': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
                'CustomName': T(c['name'], c['col']), 'DeathLootTable': 'minecraft:empty', 'CanPickUpLoot': B(0),
                'attributes': [{'id': 'minecraft:max_health', 'base': Dd(c['hp'] + P245.FLOOR)}, {'id': 'minecraft:scale', 'base': Dd(P245.HOSTSC)},
                               {'id': 'minecraft:armor', 'base': Dd(10)}, {'id': 'minecraft:knockback_resistance', 'base': Dd(1.0)},
                               {'id': 'minecraft:attack_damage', 'base': Dd(0)}, {'id': 'minecraft:movement_speed', 'base': Dd(0.2)},
                               {'id': 'minecraft:follow_range', 'base': Dd(40)}],
                'Health': F(c['hp'] + P245.FLOOR),
                'active_effects': [{'id': 'minecraft:invisibility', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)},
                                   {'id': 'minecraft:fire_resistance', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)}]}
        fn(f'h3g/hb/kn_{kind}', [f'summon minecraft:marker ~ ~ ~ {{Tags:["bm.gvprop","bm.kstat","bm.knk_{kind}","bm.h3gkm"],Rotation:[90f,0f]}}',
                                 'execute as @e[type=minecraft:marker,tag=bm.h3gkm,distance=..0.5,limit=1] at @s run function bm:p245/raise',
                                 'scoreboard players set @e[type=minecraft:marker,tag=bm.h3gkm,distance=..0.5] bm.kst 2',
                                 f'execute rotated 90 0 run summon minecraft:husk ~ ~ ~ {snbt(host)}',
                                 'scoreboard players operation @e[type=minecraft:husk,tag=bm.knewh,distance=..1] bm.kid = @e[type=minecraft:marker,tag=bm.h3gkm,distance=..0.5,limit=1] bm.kid',
                                 'scoreboard players set @e[type=minecraft:husk,tag=bm.knewh,distance=..1] bm.ks 0',
                                 'scoreboard players set @e[type=minecraft:husk,tag=bm.knewh,distance=..1] bm.kt 0',
                                 f'execute as @e[type=minecraft:husk,tag=bm.knewh,distance=..1,limit=1] run function bm:h3g/hb/set {{f:100,c:"{"red" if kind == "dread" else "green"}"}}',
                                 'tag @e[type=minecraft:husk,tag=bm.knewh,distance=..1] remove bm.knewh',
                                 hbar(f'knight_{kind}', T(c["name"], c["col"], bold=True), "red" if kind == "dread" else "green"),
                                 'execute as @a[tag=bm.gvp,distance=..40] run ' + title('@s', 'title', T(f'A {c["name"]} guards the vault', c['col'], bold=True)),
                                 'execute as @a[tag=bm.gvp,distance=..40] run ' + title('@s', 'subtitle', T('Hard mode: the stone wakes', 'gray', italic=True))])
    fn('h3g/hb/knight', ['execute store result score #r bm.rng run random value 0..1',
                         'execute if score #r bm.rng matches 0 run function bm:h3g/hb/kn_dread', 'execute if score #r bm.rng matches 1 run function bm:h3g/hb/kn_vorn'])
    # (its heist: the slot, persistence, health for the tier and the crew - over its floor. 3.0i: the vault's own guardian's health
    #  (p70/boss/setup: 160 + 90 a tier, Iron Guards half again, the crew's scaling, x1.1-1.6 by tier) and a fifth more - it was
    #  120 + 56 a tier, under half of theirs at tier V; up to 924 over its floor of 100 (a mob's most is 1024) - and every kind's
    #  hit cap, 20 a half-second (hitcap.py: the Dread Mire's and now the Brood-Mire's own, the knights' phase245 one))
    fn('h3g/hb/set', ['tag @s add bm.h3gb', 'scoreboard players operation @s bm.gvi = #gi bm.rng', 'data merge entity @s {PersistenceRequired:1b}',
                      'scoreboard players operation #h bm.rng = #gt bm.rng', 'scoreboard players set #q bm.rng 90', 'scoreboard players operation #h bm.rng *= #q bm.rng',
                      'scoreboard players add #h bm.rng 160',
                      'execute if function bm:p70/mod8 run scoreboard players operation #h bm.rng *= #3 bm.rng',
                      'execute if function bm:p70/mod8 run scoreboard players operation #h bm.rng /= #2 bm.rng',
                      'function bm:p87/hpscale'] +
                     [f'execute if score #gt bm.rng matches {t} run scoreboard players operation #h bm.rng *= #k{k} bm.rng' for t, k in ((2, 110), (3, 125), (4, 140), (5, 160))] +
                     ['execute if score #gt bm.rng matches 2.. run scoreboard players operation #h bm.rng /= #k100 bm.rng',
                      'scoreboard players set #q bm.rng 12', 'scoreboard players operation #h bm.rng *= #q bm.rng', 'scoreboard players operation #h bm.rng /= #10 bm.rng',
                      'execute if score #h bm.rng matches 925.. run scoreboard players set #h bm.rng 924',
                      'scoreboard players operation @s bm.gvx = #h bm.rng', 'scoreboard players operation #hb bm.rng = #h bm.rng',
                      'execute unless entity @s[tag=bm.hcap] run tag @s add bm.hcap', 'execute unless score @s bm.hcc matches 1.. run scoreboard players set @s bm.hcc 200',
                      'function bm:hitcap/sync',
                      '$scoreboard players add #h bm.rng $(f)',
                      'execute store result storage bm:gv h double 1 run scoreboard players get #h bm.rng', 'function bm:p70/hp with storage bm:gv',
                      'execute store result entity @s Health float 1 run scoreboard players get #h bm.rng'])
    for key, (nm, col) in HBARS.items():      # (one per boss kind: a macro'd bossbar name can't be checked - and needn't be one)
        fn(f'h3g/hb/bar_{key}', [f'execute if score #gi bm.rng matches {s + 1} run bossbar set bm:gvb{s} name {snbt(nm)}' for s in range(SL)] +
           [f'execute if score #gi bm.rng matches {s + 1} run bossbar set bm:gvb{s} color {col}' for s in range(SL)] +
           [f'execute if score #gi bm.rng matches {s + 1} store result bossbar bm:gvb{s} max run scoreboard players get #hb bm.rng' for s in range(SL)] +
           [f'execute if score #gi bm.rng matches {s + 1} store result bossbar bm:gvb{s} value run scoreboard players get #hb bm.rng' for s in range(SL)] +
           [f'execute if score #gi bm.rng matches {s + 1} run bossbar set bm:gvb{s} visible true' for s in range(SL)] +
           [f'execute if score #gi bm.rng matches {s + 1} run bossbar set bm:gvb{s} players @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]' for s in range(SL)])
    F_['p70/r/vault/fight'].insert(F_['p70/r/vault/fight'].index('function bm:p70/r/vault/open'),
                                   'execute if entity @e[tag=bm.h3gb,distance=..40] run return 0')
    # ---- each second: its bar (health over its floor), and its fall (a Mire melting down, a knight on its knee) paid once
    G.FUNCS['loop/second'].append('execute in bm:gutter as @e[type=minecraft:husk,tag=bm.h3gb,distance=0..] at @s run function bm:h3g/hb/sec')
    fn('h3g/hb/sec', ['execute store result score #h bm.rng run data get entity @s Health', 'scoreboard players remove #h bm.rng 100',
                      'execute if score #h bm.rng matches ..-1 run scoreboard players set #h bm.rng 0'] +
       [f'execute if score @s bm.gvi matches {s + 1} store result bossbar bm:gvb{s} value run scoreboard players get #h bm.rng' for s in range(SL)] +
       ['execute unless entity @s[tag=bm.h3gdn] if function bm:h3g/hb/down run function bm:h3g/hb/fell'])
    fn('h3g/hb/down', ['execute if entity @s[tag=bm.mire] if score @s bm.ms matches 7 run return 1', 'execute if entity @s[tag=bm.bmire] if score @s bm.ms matches 7 run return 1',
                       'execute if entity @s[tag=bm.khost] if score @s bm.ks matches 5 run return 1', 'return 0'])
    fn('h3g/hb/fell', ['tag @s add bm.h3gdn', 'scoreboard players operation #gi bm.rng = @s bm.gvi', 'function bm:p70/ctx',
                       'scoreboard players operation #c bm.rng = #gt bm.rng', 'scoreboard players operation #c bm.rng *= #10 bm.rng', 'scoreboard players add #c bm.rng 20',
                       'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function bm:p75/pot_add',
                       'execute as @a[tag=bm.gvp,distance=..40] if score @s bm.gvi = #gi bm.rng at @s run function bm:p76/find {t:"bm:p76/champion"}',
                       tellraw('@a[tag=bm.gvp,distance=..40]', P + [T('The vault\'s guardian falls! ', GOLD, bold=True), {'score': {'name': '#c', 'objective': 'bm.rng'}, 'color': GOLD},
                                                                  T(' coins into the pot, and a find for every one of you.', 'gray')])] +
       [f'execute if score @s bm.gvi matches {s + 1} run bossbar set bm:gvb{s} players' for s in range(SL)])
    # (a heist knight's fall hands out no statue - the pot and the finds are its prize; it stays in the hall, stone)
    sf = F_['p245/s/fall']
    gifts = [i for i, l in enumerate(sf) if '/gift_' in l]
    assert len(gifts) == len(P245.KN), gifts
    for i in gifts:
        sf[i] = sf[i].replace(' if entity @s[tag=bm.kh_', ' unless entity @s[tag=bm.h3gkn] if entity @s[tag=bm.kh_', 1)
        assert 'h3gkn' in sf[i], sf[i]
    fn('admin/heist_hard_always', ['scoreboard players set #fhb bm.gvv 1', tellraw('@s', P + [T('In hard mode every vault has a hard-mode guardian now.', 'gray')])])
    fn('admin/heist_hard_never', ['scoreboard players set #fhb bm.gvv -1', tellraw('@s', P + [T('No hard-mode guardians in the vault now.', 'gray')])])
    fn('admin/heist_hard_any', ['scoreboard players reset #fhb bm.gvv', 'scoreboard players reset #fhbk bm.gvv',
                                tellraw('@s', P + [T('Hard-mode guardians come by chance again (any kind).', 'gray')])])
    for v, nm in ((1, 'mire'), (2, 'brood'), (3, 'knight')):
        fn(f'admin/heist_hard_{nm}', [f'scoreboard players set #fhbk bm.gvv {v}', tellraw('@s', P + [T(f'Hard-mode vault guardians: always the {nm} now.', 'gray')])])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #4 bm.rng 4', 'scoreboard players set #10 bm.rng 10']
    return 1


def rp(R):
    import ratking_art
    ratking_art.rp(R)

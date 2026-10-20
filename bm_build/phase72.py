"""2.61: display cases, Zib the Donadian trooper, Skiff Escorts, and the vault's coat check and loaner kits.

GLASS DISPLAY CASES (Goldtooth, for Gutter Coins: Oak, Dark Oak, Quartz, Gilded)
- Use one on a floor and it stands there; use it on a wall and it hangs there. Right-click it holding anything: in it
  goes (one of the stack). Right-click it empty-handed: you take it back out. Sneak + right-click: it slowly turns.
  Sneak + punch: you pick the case up (whatever was in it drops out).
ZIB, THE DONADIAN TROOPER (the Donadian Medal - the reward for defending a mothership - now calls him)
- Use the medal: Zib beams down beside you (use again: he comes running; sneak + use: he beams home). A teal Donadian in
  a navy tunic with a ray gun: 7 damage a shot at the nearest monster within 16 blocks, every fifth shot overcharged
  (12 damage, the monster stunned and lit up). Jointed rig: idle, walk, run (and both with the gun up while a monster
  is near), aim, recoil, a charging crouch, jump, sit (right-click him empty-handed, like any pet). 40 health; if he
  faints, 5 minutes. He counts toward the three-follower limit.
SKIFF ESCORTS (beat a Vorn Dreadnought's reactor on an invasion night)
- Everyone near when the reactor goes offline gets a Skiff Escort beacon - a colour they don't have yet, while any are
  left. Eight colours; collect them all for "Squadron Leader". Use it: a little skiff flies at your shoulder and
  lasers monsters within 16 (5 damage a second). It can't be ridden or painted. Only 16 health - archers, blazes,
  witches and Vorn troopers take shots at it - and if it's shot down, 5 minutes. Not a follower (no limit).
THE VAULT'S COAT CHECK AND LOANER KITS (phase70)
- Going in, the Fixer checks your gear at the door: everything goes into safekeeping, except heist tools (Smoke Bombs,
  lockpicks, the Cracking Rig, the Cipher Monocle, the Thief's Cowl, the Smuggler's Boots, Gutter Coins, Clockwork bits,
  your Ledger and your Bond Sigil). Your followers can't come either.
- In the den, four kit racks: TANK (Juggernaut I, Hylian Shield, Kokiri Sword; +8 health, half knockback), OFFENSE
  (Shadowstep I, Captain's Cutlass; Strength), RANGED (Smuggler's set, Fairy Bow; monsters near you glow for the whole
  crew), SUPPORT (Tidecaller I, Staff of Sparks, Emma's Bloomheart; crewmates near you regenerate). Pick one (change your
  mind until the heist begins; anyone without one gets Offense). Knocked out? The kit is re-issued.
- Coming out - any way at all (the plate, the haul, a cleanup, a crash) - the kit stays behind and your own gear goes
  back exactly where it was; whatever you picked up inside comes with you.
- A FIXER'S CONTRACT on every job (on the sheet): Ghost (finish with the alarm under 25), Clean Sweep (nobody knocked
  out) or Against the Clock (90 seconds a room): +2 shares and an extra purse of coins."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, D, Int
import phase72_art as ART
import phase70 as P70
from phase70_rooms import rel
from phase36 import COLOURS

PET_CD = 300
TEAL = '#3ad8c8'
GOLD = '#ffcf40'
ZB_HP = 40
ESK_HP = 16
CNAME = {c: (nm, col) for c, nm, col in COLOURS}

# ---------------------------------------------------------------- display cases (Goldtooth sells them)
for v, (nm, col, *_r) in ART.CASES.items():
    item(f'display_case_{v}', TOTEM, f'{nm} Display Case', col,
         ['A glass case for showing things off.', ('Use on a floor: it stands there.', 'blue'), ('Use on a wall: it hangs there.', 'blue'),
          ('Right-click it holding an item: in it goes.', 'blue'), ('Right-click it empty-handed: take it out.', 'blue'),
          ('Sneak + right-click: it turns slowly.', 'blue'), ('Sneak + punch: pick the case up.', 'gray')],
         model=f'bm:display_case_{v}', stack=16, cat='builder', comps=hold('none'))
    HOLD[f'display_case_{v}'] = f'bm:p72/dc/place_{v}'
P70.GOLDTOOTH_STOCK += [(3, 'display_case_oak', 1), (3, 'display_case_dark_oak', 1), (5, 'display_case_quartz', 1), (8, 'display_case_gilded', 1)]

# ---------------------------------------------------------------- the Donadian Medal calls Zib
item('donadian_medal', TOTEM, 'Donadian Medal', TEAL,
     ['For defending a Donadian mothership from the Vorn.', ('Use: call Zib, a Donadian trooper', 'blue'), ('(or call him back). Sneak + use: he beams home.', 'blue'),
      ('His ray gun: 7 damage a shot, 16 blocks;', 'blue'), ('every fifth shot overcharged - 12 damage,', 'blue'), ('and the monster is stunned.', 'blue'),
      ('Right-click him empty-handed: sit / follow.', 'gray'), ('If he faints: 5 minutes.', 'gray')],
     model='bm:donadian_medal', stack=1, cat='alien', glint=True, comps=hold('none'))
HOLD['donadian_medal'] = 'bm:p72/zb/use'

# ---------------------------------------------------------------- Skiff Escorts (the reactor's reward)
for i, c in enumerate(ART.ESCORT_COLS):
    nm, col = CNAME[c]
    item(f'skiff_escort_{c}', TOTEM, f'Skiff Escort: {nm}', col,
         ['A pocket-sized Vorn Skiff, reprogrammed.', ('Use: it flies at your shoulder and lasers', 'blue'), ('monsters within 16 blocks (5 damage).', 'blue'),
          ('Use again, or sneak + use: it flies home.', 'blue'), ("It can't be ridden, and won't take paint -", 'gray'), (f"it's {nm}, and that's that.", 'gray'),
          ("Fragile: if it's shot down, 5 minutes.", 'gray'), ('Eight colours to collect.', 'light_purple')],
         model=f'bm:skiff_escort_{c}', stack=1, cat='alien', glint=True, comps=hold('none'))
    HOLD[f'skiff_escort_{c}'] = f'bm:p72/esk/use_{i}'

# ---------------------------------------------------------------- the vault: what you may bring, what you're lent
KEEP = ['smoke_bomb', 'skeleton_lockpick', 'vorn_cracking_rig', 'cipher_monocle', 'thiefs_cowl', 'smugglers_boots', 'gutter_coin',
        'clockwork_fragment', 'clockwork_key', 'bond_sigil']
ROLES = {1: ('Tank', '#c0392b', 'Juggernaut I (the heaviest armour), Hylian Shield, Kokiri Sword, 2 golden apples, a plain Infinity bow. +8 health, half knockback.',
             {'head': 'juggernaut_helmet_1', 'chest': 'juggernaut_chestplate_1', 'legs': 'juggernaut_leggings_1', 'feet': 'juggernaut_boots_1',
              'offhand': 'hylian_shield'}, ['kokiri_sword', ('minecraft:golden_apple', 2)]),
         2: ('Offense', '#ff7a1a', "Shadowstep I (iron-strong), Captain's Cutlass, a golden apple, a plain Infinity bow. Strength while you fight.",
             {'head': 'shadowstep_helmet_1', 'chest': 'shadowstep_chestplate_1', 'legs': 'shadowstep_leggings_1', 'feet': 'shadowstep_boots_1'},
             ['pirate_cutlass', ('minecraft:golden_apple', 1)]),
         3: ('Ranged', '#5ad84a', "Smuggler's set (iron-strong), Fairy Bow (no Infinity), 64 arrows and 32 spectral - more turn up in every room - "
                                  "a backup sword, a golden apple. Speed, and monsters near you glow for the whole crew.",
             {'head': 'smuggler_helmet', 'chest': 'smuggler_chestplate', 'legs': 'smuggler_leggings', 'feet': 'smuggler_boots'},
             ['fairy_bow', ('minecraft:arrow', 64), ('minecraft:spectral_arrow', 32),
              ('minecraft:iron_sword', 1, {'minecraft:enchantments': {'minecraft:sharpness': 2, 'minecraft:knockback': 1}}), ('minecraft:golden_apple', 1)]),
         4: ('Support', '#7ad0ea', "Tidecaller I (iron-strong), Staff of Sparks, Emma's Bloomheart, 3 splash potions of Healing II, a golden apple, a plain Infinity bow. "
                                   "Crewmates near you regenerate.",
             {'head': 'tidecaller_helmet_1', 'chest': 'tidecaller_chestplate_1', 'legs': 'tidecaller_leggings_1', 'feet': 'tidecaller_boots_1'},
             ['staff_of_sparks', 'bloomheart_gem', ('minecraft:splash_potion', 3, {'minecraft:potion_contents': {'potion': 'minecraft:strong_healing'}}),
              ('minecraft:golden_apple', 1)])}
SLOT_OF = {'head': 'armor.head', 'chest': 'armor.chest', 'legs': 'armor.legs', 'feet': 'armor.feet', 'offhand': 'weapon.offhand', 'body': 'armor.body'}
STAGE = '-200 64 -200'                # the coat-check barrel (bm:gutter, kept loaded)
CONTRACTS = {1: ('Ghost', 'finish with the alarm under 25'), 2: ('Clean Sweep', 'nobody gets knocked out'), 3: ('Against the Clock', '90 seconds a room')}


# (2.63) the loaners' armour: iron-tier for Offense, Ranged and Support, the tank the heaviest (diamond-tier and tougher), and nothing in a kit
# takes away from your swing (Shadowstep's light-armour penalty is off for the heist)
KIT_TIER = {1: ({'head': 3, 'chest': 8, 'legs': 6, 'feet': 3}, 3.0),          # Tank: diamond-tier, extra toughness
            2: ({'head': 2, 'chest': 6, 'legs': 5, 'feet': 2}, 0.0),          # Offense, Ranged, Support: iron-tier
            3: ({'head': 2, 'chest': 6, 'legs': 5, 'feet': 2}, 0.0),
            4: ({'head': 2, 'chest': 6, 'legs': 5, 'feet': 2}, 0.0)}
VANILLA_ARMOR = {'leather': ((1, 3, 2, 1), 0), 'chainmail': ((2, 5, 4, 1), 0), 'iron': ((2, 6, 5, 2), 0), 'golden': ((2, 5, 3, 1), 0),
                 'diamond': ((3, 8, 6, 3), 2), 'netherite': ((3, 8, 6, 3), 3), 'copper': ((2, 4, 3, 1), 0), 'turtle': ((2, 0, 0, 0), 0)}
KIT_FOOD = ('minecraft:cooked_beef', 32)             # (2.74: was 16)
PIECE = {'_helmet': ('head', 'helmet'), '_chestplate': ('chest', 'chestplate'), '_leggings': ('legs', 'leggings'), '_boots': ('feet', 'boots')}


def kit_armor(it, role):
    """the kit copy's attribute modifiers: armour/toughness raised to the role's floor, no negative attack damage"""
    base = it['base'].split(':')[1]
    m = next(((sl, nm) for suf, (sl, nm) in PIECE.items() if base.endswith(suf)), None)
    if not m or role not in KIT_TIER: return None
    slot, nm = m; mat = base[:-len(nm) - 1]
    mods = it['comps'].get('minecraft:attribute_modifiers')
    if mods is None:                                     # (no component: the base item's own armour applies)
        arm, tough = VANILLA_ARMOR.get(mat, ((0, 0, 0, 0), 0))
        mods = [{'type': 'minecraft:armor', 'id': f'minecraft:armor.{nm}', 'amount': float(arm[('head', 'chest', 'legs', 'feet').index(slot)]), 'operation': 'add_value', 'slot': slot},
                {'type': 'minecraft:armor_toughness', 'id': f'minecraft:armor.{nm}_toughness', 'amount': float(tough), 'operation': 'add_value', 'slot': slot}]
    floor, tfloor = KIT_TIER[role][0][slot], KIT_TIER[role][1]
    out = []
    for md in mods:
        md = dict(md)
        if md['type'] == 'minecraft:attack_damage' and float(md['amount']) < 0: continue
        if md['type'] == 'minecraft:armor': md['amount'] = float(floor)                     # (exactly the role's tier: the tank is the heaviest)
        if md['type'] == 'minecraft:armor_toughness': md['amount'] = tfloor
        out.append(md)
    return out


WEARS = ('_sword', '_axe', '_pickaxe', '_shovel', '_hoe', '_spear', 'bow', 'crossbow', 'trident', 'shield', 'mace', 'fishing_rod', 'shears', 'flint_and_steel', 'brush',
         '_helmet', '_chestplate', '_leggings', '_boots', 'elytra')          # (2.74: the loaned armour too - every kit, every rank)


def _unbreakable(base, comps):
    """(2.68) a loaned weapon or tool never wears out: unbreakable, and it says nothing about it (2.74: and its armour)"""
    if not (any(base.endswith(w) for w in WEARS) or 'minecraft:max_damage' in comps): return {}
    td = dict(comps.get('minecraft:tooltip_display', {}))
    td['hidden_components'] = list(td.get('hidden_components', [])) + ['minecraft:unbreakable']
    return {'minecraft:unbreakable': {}, 'minecraft:tooltip_display': td}


# (2.80g) the kit never burns: dropped into lava or fire it floats there unharmed until it's back in your hands
FIREPROOF = 'minecraft:damage_resistant={types:"#minecraft:is_fire"}'


def kit_arg(iid, role=None, extra=None):
    """an item argument for a loaner: the BM item, marked bm_kit, with a line saying so"""
    if ':' in iid:
        ex = dict(_unbreakable(iid, {}), **(extra or {}))
        more = ''.join(f',{k}={snbt(v)}' for k, v in ex.items())
        return (f'{iid}[minecraft:custom_data={{bm_kit:1b}},minecraft:lore=[{snbt(T("Loaned by the Fixer - stays in the vault.", "dark_gray"))}]{more},'
                f'{FIREPROOF}]')
    it = ITEMS[iid]; parts = []
    comps = dict(it['comps'])
    am = kit_armor(it, role)
    comps.update(_unbreakable(it['base'], comps))
    if am is not None:
        from nbt import D
        comps['minecraft:attribute_modifiers'] = [dict(md, amount=D(md['amount'])) for md in am]
        # (2.67) loaned armour stays on until the heist is over: Curse of Binding (the exit takes it off you)
        comps['minecraft:enchantments'] = dict(comps.get('minecraft:enchantments', {}), **{'minecraft:binding_curse': 1})
    comps.setdefault('minecraft:damage_resistant', {'types': '#minecraft:is_fire'})
    for k, v in comps.items():
        if k == 'minecraft:custom_data': v = dict(v, bm_kit=B(1))
        if k == 'minecraft:lore': v = list(v) + [T('Loaned by the Fixer - stays in the vault.', 'dark_gray')]
        parts.append(k if k.startswith('!') else f'{k}={snbt(v)}')
    return f"{it['base']}[{','.join(parts)}]"


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    zsay = lambda txt, who='@s': title(who, 'actionbar', [T('Zib: ', TEAL, bold=True), T(txt, '#c8fff4')])
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    tick, fast, second = [], [], []
    objs = ['bm.dcv', 'bm.dca', 'bm.zbcd', 'bm.zbc', 'bm.zbk', 'bm.zbn', 'bm.zbs', 'bm.eskcd', 'bm.eskc', 'bm.esf', 'bm.esb', 'bm.esn', 'bm.gvrole',
            'bm.gvko', 'bm.gvct', 'bm.bagt']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + ['execute in bm:gutter run forceload add -200 -200']
    G.OBJECTIVES += objs
    foe = 'type=#bm:hostile,tag=!bm.npc'
    ident = [F(0), F(0), F(0), F(1)]
    q = lambda deg: [F(0), F(round(__import__('math').sin(__import__('math').radians(deg) / 2), 4)), F(0), F(round(__import__('math').cos(__import__('math').radians(deg) / 2), 4))]

    # ================================================================== DISPLAY CASES
    CV = list(ART.CASES)
    for i, v in enumerate(CV):
        fn(f'p72/dc/place_{v}', ['execute unless function bm:p37/allowed run return run ' + say('Not here.'), f'scoreboard players set #dcv bm.rng {i}',
                                 'function bm:p72/dc/place',
                                 f'execute if score #placed bm.rng matches 1 unless entity @s[gamemode=creative] run clear @s {holds("display_case_" + v)} 1'])
    fn('p72/dc/place', ['scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 50', 'tag @s add bm.placer',
                        'execute anchored eyes positioned ^ ^ ^ run function bm:p72/dc/ray', 'tag @s remove bm.placer',
                        'execute if score #placed bm.rng matches 0 run return run ' + say('Look at a floor or a wall within 5 blocks.'),
                        'execute if score #placed bm.rng matches 2 run return run ' + say("There's a case there already."),
                        'execute if score #placed bm.rng matches 3 run return run ' + say('Floors and walls only (not ceilings or corners).'),
                        'playsound minecraft:block.glass.place block @a[distance=..16] ~ ~ ~ 1 1.2', 'playsound minecraft:block.wood.place block @a[distance=..16] ~ ~ ~ 0.8 1'])
    # the ray steps in tenths; at the first solid block, which face did it come through? (the air cell it left vs the block)
    fn('p72/dc/ray', ['execute unless block ^ ^ ^0.1 #minecraft:replaceable run return run function bm:p72/dc/hit',
                      'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.1 run function bm:p72/dc/ray'])
    fn('p72/dc/hit', ['execute positioned ^ ^ ^0.1 align xyz positioned ~0.5 ~0.5 ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["bm.dcm"]}',
                      'execute align xyz positioned ~0.5 ~0.5 ~0.5 run function bm:p72/dc/face', 'kill @e[type=minecraft:marker,tag=bm.dcm]'])
    near_m = 'if entity @e[type=minecraft:marker,tag=bm.dcm,distance=..0.1]'
    fn('p72/dc/face', [f'execute positioned ~ ~-1 ~ {near_m} run return run function bm:p72/dc/floor',
                       f'execute positioned ~1 ~ ~ {near_m} positioned ~-0.75 ~-0.4 ~ rotated 90 0 run return run function bm:p72/dc/wall',
                       f'execute positioned ~-1 ~ ~ {near_m} positioned ~0.75 ~-0.4 ~ rotated -90 0 run return run function bm:p72/dc/wall',
                       f'execute positioned ~ ~ ~1 {near_m} positioned ~ ~-0.4 ~-0.75 rotated 180 0 run return run function bm:p72/dc/wall',
                       f'execute positioned ~ ~ ~-1 {near_m} positioned ~ ~-0.4 ~0.75 rotated 0 0 run return run function bm:p72/dc/wall',
                       'scoreboard players set #placed bm.rng 3'])
    # (run at the floor block's centre - face() moved down to find it - so the case stands half a block up, on its top)
    fn('p72/dc/floor', ['execute positioned ~ ~0.5 ~ if entity @e[type=minecraft:interaction,tag=bm.dchit,distance=..0.7] run return run scoreboard players set #placed bm.rng 2',
                        'execute positioned ~ ~0.5 ~ rotated as @a[tag=bm.placer,limit=1] rotated ~180 0 run function bm:p72/dc/spawn_floor',
                        'scoreboard players set #placed bm.rng 1'])
    fn('p72/dc/wall', ['execute if entity @e[type=minecraft:interaction,tag=bm.dchit,distance=..0.5] run return run scoreboard players set #placed bm.rng 2',
                       'function bm:p72/dc/spawn_wall', 'scoreboard players set #placed bm.rng 1'])

    def case_nbt(kind):
        tr = [F(0), F(0.5), F(0)] if kind == 'floor' else [F(0), F(0.4), F(0.25)]
        return snbt({'Tags': ['bm.dcase', 'bm.dcnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:dcase_oak_{kind}'}},
                     'item_display': 'fixed', 'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': tr, 'scale': [F(1)] * 3}})
    def inner_nbt(kind):
        tr = [F(0), F(0.6), F(0)] if kind == 'floor' else [F(0), F(0.41), F(-0.03)]
        return snbt({'Tags': ['bm.dcitem', 'bm.dcnew'], 'item_display': 'fixed',
                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': tr, 'scale': [F(0.5)] * 3}})
    hitbox = {'floor': snbt({'Tags': ['bm.dchit', 'bm.dcnew'], 'width': F(0.85), 'height': F(1.0), 'response': B(1)}),
              'wall': snbt({'Tags': ['bm.dchit', 'bm.dcnew'], 'width': F(0.6), 'height': F(0.85), 'response': B(1)})}
    for kind in ('floor', 'wall'):
        fn(f'p72/dc/spawn_{kind}', [f'summon minecraft:item_display ~ ~ ~ {case_nbt(kind)}', f'summon minecraft:item_display ~ ~ ~ {inner_nbt(kind)}',
                                    f'summon minecraft:interaction ~ ~ ~ {hitbox[kind]}',
                                    'scoreboard players operation @e[tag=bm.dcnew,distance=..0.1] bm.dcv = #dcv bm.rng',
                                    'scoreboard players set @e[tag=bm.dcnew,distance=..0.1] bm.dca 0'] +
           [f'execute if score #dcv bm.rng matches {i} run data modify entity @e[type=minecraft:item_display,tag=bm.dcase,tag=bm.dcnew,distance=..0.1,limit=1] '
            f'item.components."minecraft:item_model" set value "bm:dcase_{v}_{kind}"' for i, v in enumerate(CV)] +
           ['tp @e[tag=bm.dcnew,distance=..0.1] ~ ~ ~ ~ 0', 'tag @e[tag=bm.dcnew,distance=..0.1] remove bm.dcnew',
            'particle minecraft:wax_on ~ ~0.5 ~ 0.3 0.3 0.3 0 8'])
    # using it: put in / take out / spin; sneak + punch takes the case
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.dchit] if data entity @s interaction at @s run function bm:p72/dc/click',
             'execute as @e[type=minecraft:interaction,tag=bm.dchit] if data entity @s attack at @s run function bm:p72/dc/punch']
    sel = '@e[type=minecraft:item_display,tag=bm.dcsel,limit=1]'
    fn('p72/dc/click', ['tag @s add bm.dcme', 'tag @e[type=minecraft:item_display,tag=bm.dcitem,distance=..0.05,limit=1] add bm.dcsel',
                        'execute on target run function bm:p72/dc/who', 'tag @s remove bm.dcme', 'tag @e[tag=bm.dcsel] remove bm.dcsel', 'data remove entity @s interaction'])
    fn('p72/dc/who', ['execute if predicate bm:p20/sneaking run return run function bm:p72/dc/spin_toggle',
                      f'execute if data entity {sel} item unless items entity @s weapon.mainhand * run return run function bm:p72/dc/take',
                      f'execute if data entity {sel} item run return run ' + say('Empty-handed to take it out first.'),
                      'execute if items entity @s weapon.mainhand * run return run function bm:p72/dc/put',
                      say('Right-click holding something to put it in the case.')])
    fn('p72/dc/take', [f'item replace entity @s weapon.mainhand from entity {sel} contents', f'item replace entity {sel} contents with minecraft:air',
                       'playsound minecraft:block.chiseled_bookshelf.pickup block @a[distance=..16] ~ ~ ~ 1 1.1'])
    fn('p72/dc/put', [f'item replace entity {sel} contents from entity @s weapon.mainhand', f'item modify entity {sel} contents {{function:"minecraft:set_count",count:1}}',
                      'execute unless entity @s[gamemode=creative] run item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                      'playsound minecraft:block.chiseled_bookshelf.insert block @a[distance=..16] ~ ~ ~ 1 1.1',
                      'execute as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s run particle minecraft:wax_on ~ ~0.6 ~ 0.2 0.2 0.2 0 6'])
    fn('p72/dc/spin_toggle', [f'execute if entity {sel.replace("limit=1", "tag=bm.dcspin,limit=1")} run return run function bm:p72/dc/spin_off',
                              f'tag {sel} add bm.dcspin', 'playsound minecraft:block.note_block.chime block @s ~ ~ ~ 0.6 1.6', say('The case turns its treasure slowly.')])
    fn('p72/dc/spin_off', [f'tag {sel} remove bm.dcspin', f'scoreboard players set {sel} bm.dca 0',
                           f'data merge entity {sel} {{start_interpolation:0,interpolation_duration:10,transformation:{{left_rotation:[0f,0f,0f,1f]}}}}',
                           'playsound minecraft:block.note_block.chime block @s ~ ~ ~ 0.6 1.0', say('The case stands still.')])
    second.append('execute as @e[type=minecraft:item_display,tag=bm.dcspin] run function bm:p72/dc/spin')
    fn('p72/dc/spin', ['scoreboard players add @s bm.dca 1', 'execute if score @s bm.dca matches 6.. run scoreboard players set @s bm.dca 0'] +
       [f'execute if score @s bm.dca matches {k} run data merge entity @s {{start_interpolation:0,interpolation_duration:20,transformation:{{left_rotation:{snbt(q(60 * k))}}}}}'
        for k in range(6)])
    fn('p72/dc/punch', ['tag @s add bm.dcme', 'execute on attacker if predicate bm:p20/sneaking run function bm:p72/dc/pick',
                        'execute on attacker unless predicate bm:p20/sneaking run ' + say('Sneak + punch to pick the case up.'),
                        'tag @s remove bm.dcme', 'data remove entity @s attack'])
    fn('p72/dc/pick', ['execute as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s run function bm:p72/dc/drop'] +
       [f'execute if score @e[type=minecraft:interaction,tag=bm.dcme,limit=1] bm.dcv matches {i} run loot give @s loot bm:items/display_case_{v}' for i, v in enumerate(CV)] +
       ['execute as @e[type=minecraft:interaction,tag=bm.dcme,limit=1] at @s run function bm:p72/dc/gone', 'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 1 1'])
    fn('p72/dc/drop', ['execute as @e[type=minecraft:item_display,tag=bm.dcitem,distance=..0.05,limit=1] if data entity @s item at @s run function bm:p72/dc/drop2'])
    fn('p72/dc/drop2', ['summon minecraft:item ~ ~0.5 ~ {Item:{id:"minecraft:stone",count:1},PickupDelay:10s,Tags:["bm.dcdrop"]}',
                        'data modify entity @e[type=minecraft:item,tag=bm.dcdrop,limit=1,sort=nearest] Item set from entity @s item', 'tag @e[tag=bm.dcdrop] remove bm.dcdrop'])
    fn('p72/dc/gone', ['kill @e[type=minecraft:item_display,tag=bm.dcase,distance=..0.05]', 'kill @e[type=minecraft:item_display,tag=bm.dcitem,distance=..0.05]',
                       'particle minecraft:block{block_state:"minecraft:glass"} ~ ~0.5 ~ 0.3 0.3 0.3 0 12', 'playsound minecraft:block.glass.break block @a[distance=..16] ~ ~ ~ 0.5 1.4',
                       'kill @s'])

    # ================================================================== ZIB, THE DONADIAN TROOPER
    rig, poses = ART.zib_rig(), ART.zib_poses()
    S = rig.S
    DUR = {'aim': 3, 'fire': 1, 'charge': 4, 'jump': 3, 'sit': 8}
    for pid, (name, pose) in enumerate(poses.items(), 1):
        dur = DUR.get(name, 10 if name.startswith('idle') else 2)
        sol = rig.solve(pose)
        fn(f'p72/zb/p/{name}', [f'execute if score @s bm.rgp matches {pid} run return 0', f'scoreboard players set @s bm.rgp {pid}'] +
           [rig.merge(n, R, J, dur) for n, (R, J) in sol.items()])
    def part(n):
        return 'summon minecraft:item_display ~ ~ ~ ' + snbt({
            'Tags': ['bm.fp_disp', 'bm.zbr', f'bm.zbr_{n}', 'bm.rnew'], 'item_display': 'fixed', 'teleport_duration': Int(2),
            'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:zbr_{n}'}},
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(S)] * 3}})
    fn('p72/zb/rig', ['tag @s add bm.zbhost', 'execute on passengers run kill @s'] + [part(n) for n in rig.parts] +
       ['execute as @e[type=minecraft:item_display,tag=bm.rnew,distance=..2] run ride @s mount @e[type=minecraft:wolf,tag=bm.zbhost,limit=1]',
        'scoreboard players operation #wp bm.rng = @s bm.pid', 'execute on passengers run scoreboard players operation @s bm.pid = #wp bm.rng',
        'tag @e[tag=bm.rnew] remove bm.rnew', 'scoreboard players set @s bm.rgp 0', 'scoreboard players set @s bm.zbs -1', 'tag @s remove bm.zbhost'])
    fn('p72/zb/has_parts', ['execute on passengers if entity @s[tag=bm.zbr_torso] run return 1', 'return 0'])
    second.append('execute as @e[type=minecraft:wolf,tag=bm.zibpet] unless function bm:p72/zb/has_parts at @s run function bm:p72/zb/rig')
    # every tick (near players): timers, a target, the shot, the frames, which way he faces
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.zibpet] at @s if entity @a[distance=..48] run function bm:p72/zb/tick')
    fn('p72/zb/tick', ['scoreboard players add @s bm.rgf 1',
                       'execute if score @s bm.zbc matches 1.. run scoreboard players remove @s bm.zbc 1',
                       'execute if score @s bm.zbk matches 1.. run scoreboard players remove @s bm.zbk 1',
                       f'execute unless data entity @s {{Sitting:1b}} run tag @e[{foe},distance=..16,sort=nearest,limit=1] add bm.zbt',
                       'execute if score @s bm.zbk matches 1.. run function bm:p72/zb/act',
                       'execute unless score @s bm.zbk matches 1.. unless score @s bm.zbc matches 1.. if entity @e[tag=bm.zbt] run function bm:p72/zb/fire_go',
                       'execute unless score @s bm.zbk matches 1.. run function bm:p72/zb/anim',
                       'execute if entity @e[tag=bm.zbt] facing entity @e[tag=bm.zbt,limit=1] feet on passengers run rotate @s ~ 0',
                       'execute unless entity @e[tag=bm.zbt] on passengers run rotate @s ~ 0',
                       'tag @e[tag=bm.zbt] remove bm.zbt'])
    fn('p72/zb/state', ['execute if predicate bm:p21/airborne if predicate bm:swim run return run scoreboard players set #st bm.rng 10',
                        'execute if predicate bm:p21/airborne run return run scoreboard players set #st bm.rng 3',
                        'execute if data entity @s {Sitting:1b} run return run scoreboard players set #st bm.rng 4',
                        'execute if entity @e[tag=bm.zbt] if predicate bm:p21/running run return run scoreboard players set #st bm.rng 6',
                        'execute if entity @e[tag=bm.zbt] if predicate bm:p21/walking run return run scoreboard players set #st bm.rng 5',
                        'execute if entity @e[tag=bm.zbt] run return run scoreboard players set #st bm.rng 7',
                        'execute if predicate bm:p21/running run return run scoreboard players set #st bm.rng 2',
                        'execute if predicate bm:p21/walking run return run scoreboard players set #st bm.rng 1',
                        'scoreboard players set #st bm.rng 0'])
    fn('p72/zb/anim', ['function bm:p72/zb/state', 'execute unless score #st bm.rng = @s bm.zbs run scoreboard players set @s bm.rgf 0',
                       'scoreboard players operation @s bm.zbs = #st bm.rng',
                       'execute if score #st bm.rng matches 3 run return run function bm:p72/zb/p/jump',
                       'execute if score #st bm.rng matches 4 run return run function bm:p72/zb/p/sit',
                       'execute if score #st bm.rng matches 7 run return run function bm:p72/zb/p/aim',
                       'execute if score #st bm.rng matches 0 run return run function bm:p72/zb/idle',
                       'execute if score #st bm.rng matches 1 run return run function bm:p72/zb/c_walk',
                       'execute if score #st bm.rng matches 5 run return run function bm:p72/zb/c_walkaim',
                       'execute if score #st bm.rng matches 2 run return run function bm:p72/zb/c_run',
                       'execute if score #st bm.rng matches 6 run return run function bm:p72/zb/c_runaim',
                       'execute if score #st bm.rng matches 10 run return run function bm:p72/zb/c_swim'])
    # a cycle: frame i every 2 ticks
    for cyc, n in (('walk', 8), ('walkaim', 8), ('run', 6), ('runaim', 6), ('swim', 8)):
        fn(f'p72/zb/c_{cyc}', ['scoreboard players operation #f bm.rng = @s bm.rgf', f'scoreboard players operation #f bm.rng %= #{2 * n} bm.rng'] +
           [f'execute if score #f bm.rng matches {2 * i} run function bm:p72/zb/p/{cyc}{i}' for i in range(n)])
    fn('p72/zb/idle', ['scoreboard players operation #f bm.rng = @s bm.rgf', 'scoreboard players operation #f bm.rng %= #80 bm.rng'] +
       [f'execute if score #f bm.rng matches {10 * i} run function bm:p72/zb/p/idle{i}' for i in range(8)] +
       ['execute if score #f bm.rng matches 35 on passengers if entity @s[tag=bm.zbr_eyes] run data modify entity @s item.components."minecraft:item_model" set value "bm:zbr_eyes_blink"',
        'execute if score #f bm.rng matches 38 on passengers if entity @s[tag=bm.zbr_eyes] run data modify entity @s item.components."minecraft:item_model" set value "bm:zbr_eyes"',
        'execute if score #f bm.rng matches 60 if entity @a[distance=..6] run particle minecraft:dust{color:[0.5,1.0,0.4],scale:0.6} ~ ~1.3 ~ 0.15 0.05 0.15 0 3'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #2 bm.rng 2', 'scoreboard players set #12 bm.rng 12', 'scoreboard players set #16 bm.rng 16',
                              'scoreboard players set #80 bm.rng 80']
    # the shot: aim (3 ticks), FIRE, recover; every fifth, a charging crouch and an overcharged blast
    fn('p72/zb/fire_go', ['scoreboard players add @s bm.zbn 1', 'scoreboard players set @s bm.zbs 9',
                          'execute if score @s bm.zbn matches 5.. run return run function bm:p72/zb/charge_go',
                          'scoreboard players set @s bm.zbk 10', 'scoreboard players set @s bm.zbc 24', 'function bm:p72/zb/p/aim'])
    fn('p72/zb/charge_go', ['scoreboard players set @s bm.zbk 16', 'scoreboard players set @s bm.zbc 34', 'function bm:p72/zb/p/charge',
                            'playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 0.6 1.8'])
    fn('p72/zb/act', ['execute if score @s bm.zbn matches 5.. run return run function bm:p72/zb/act_charged',
                      'execute if score @s bm.zbk matches 6 run function bm:p72/zb/shot', 'execute if score @s bm.zbk matches 6 run function bm:p72/zb/p/fire',
                      'execute if score @s bm.zbk matches 4 run function bm:p72/zb/p/aim'])
    fn('p72/zb/act_charged', ['execute if score @s bm.zbk matches 9.. at @s run particle minecraft:dust{color:[0.4,1.0,0.5],scale:0.9} ^-0.2 ^0.6 ^0.7 0.08 0.08 0.08 0 3',
                              'execute if score @s bm.zbk matches 8 run scoreboard players set #zch bm.rng 1', 'execute if score @s bm.zbk matches 8 run function bm:p72/zb/shot',
                              'execute if score @s bm.zbk matches 8 run function bm:p72/zb/p/fire', 'execute if score @s bm.zbk matches 8 run scoreboard players set @s bm.zbn 0',
                              'execute if score @s bm.zbk matches 5 run function bm:p72/zb/p/aim', 'scoreboard players set #zch bm.rng 0'])
    fn('p72/zb/shot', ['execute unless entity @e[tag=bm.zbt] run return 0', 'tag @s add bm.zbme', 'scoreboard players set #ray bm.rng 36',
                       'execute at @s positioned ~ ~0.62 ~ facing entity @e[tag=bm.zbt,limit=1] eyes positioned ^-0.2 ^ ^0.7 run function bm:p72/zb/beam',
                       'execute if score #zch bm.rng matches 0 run playsound minecraft:entity.firework_rocket.blast neutral @a[distance=..20] ~ ~ ~ 0.5 2',
                       'execute if score #zch bm.rng matches 0 run playsound minecraft:block.beacon.deactivate neutral @a[distance=..20] ~ ~ ~ 0.3 2',
                       'execute if score #zch bm.rng matches 1 run playsound minecraft:entity.generic.explode neutral @a[distance=..24] ~ ~ ~ 0.4 1.8',
                       'execute if score #zch bm.rng matches 1 run playsound minecraft:block.beacon.activate neutral @a[distance=..24] ~ ~ ~ 0.6 2',
                       'tag @s remove bm.zbme'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #zch bm.rng 0']
    fn('p72/zb/beam', ['execute if score #zch bm.rng matches 0 run particle minecraft:dust{color:[0.35,1.0,0.45],scale:0.7} ~ ~ ~ 0 0 0 0 1',
                       'execute if score #zch bm.rng matches 1 run particle minecraft:dust{color:[0.6,1.0,0.7],scale:1.4} ~ ~ ~ 0.03 0.03 0.03 0 2',
                       'execute if score #zch bm.rng matches 1 run particle minecraft:end_rod ~ ~ ~ 0 0 0 0 1',
                       'execute positioned ~ ~-0.8 ~ if entity @e[tag=bm.zbt,distance=..1.1] run return run function bm:p72/zb/zap',
                       'execute unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:electric_spark ~ ~ ~ 0.1 0.1 0.1 0.1 6',
                       'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.5 run function bm:p72/zb/beam'])
    fn('p72/zb/zap', ['execute as @e[tag=bm.zbt,limit=1] at @s run function bm:p72/zb/hurt'])
    fn('p72/zb/hurt', ['execute if score #zch bm.rng matches 1 run return run function bm:p72/zb/hurt_big',
                       'damage @s 7 minecraft:mob_projectile by @e[type=minecraft:wolf,tag=bm.zbme,limit=1]',
                       'particle minecraft:electric_spark ~ ~1 ~ 0.25 0.4 0.25 0.2 10'])
    fn('p72/zb/hurt_big', ['damage @s 12 minecraft:mob_projectile by @e[type=minecraft:wolf,tag=bm.zbme,limit=1]',
                           'effect give @s minecraft:slowness 2 4 true', 'effect give @s minecraft:weakness 2 1 true', 'effect give @s minecraft:glowing 2 0 true',
                           'particle minecraft:explosion ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:dust{color:[0.5,1.0,0.5],scale:1.6} ~ ~1 ~ 0.4 0.5 0.4 0 20'])
    # out of a fight he patches himself up
    second.append(f'execute as @e[type=minecraft:wolf,tag=bm.zibpet] at @s unless entity @e[{foe},distance=..16] run effect give @s minecraft:regeneration 3 0 true')

    # ---- the medal: call, recall, send home
    sel_pet = 'execute as @e[type=minecraft:wolf,tag=bm.zibpet] if score @s bm.pid = #me bm.pid'
    pet = {'Tags': ['bm.zibpet', 'bm.zbnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(ZB_HP),
           'CustomName': T('Zib', TEAL, bold=True), 'CustomNameVisible': B(0),
           'attributes': [{'id': 'minecraft:max_health', 'base': D(ZB_HP)}, {'id': 'minecraft:armor', 'base': D(4)}, {'id': 'minecraft:attack_damage', 'base': D(1)},
                          {'id': 'minecraft:movement_speed', 'base': D(0.34)}, {'id': 'minecraft:follow_range', 'base': D(32)}, {'id': 'minecraft:step_height', 'base': D(1.0)}],
           'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    fn('p72/zb/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      f'{sel_pet} run tag @s add bm.zbsel',
                      'execute if entity @e[type=minecraft:wolf,tag=bm.zbsel] if predicate bm:p20/sneaking run function bm:p72/zb/dismiss',
                      'execute if entity @e[type=minecraft:wolf,tag=bm.zbsel] unless predicate bm:p20/sneaking run function bm:p72/zb/recall',
                      'execute unless entity @e[type=minecraft:wolf,tag=bm.zbsel] unless predicate bm:p20/sneaking run function bm:p72/zb/try_summon',
                      'execute unless entity @e[type=minecraft:wolf,tag=bm.zbsel] if predicate bm:p20/sneaking run ' + say("Zib isn't with you. (Use the medal to call him.)"),
                      'tag @e[tag=bm.zbsel] remove bm.zbsel'])
    fn('p72/zb/recall', ['tp @e[type=minecraft:wolf,tag=bm.zbsel,limit=1] @s', 'data modify entity @e[type=minecraft:wolf,tag=bm.zbsel,limit=1] Sitting set value 0b',
                         'particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 16', 'playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 0.6 1.6',
                         zsay('On my way, commander!')])
    fn('p72/zb/try_summon', ['execute if function bm:p58/full run return 0',
                             'execute if score @s bm.zbcd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.zbcd',
                             'execute if score @s bm.zbcd matches 1.. run scoreboard players add #m bm.rng 59', 'execute if score @s bm.zbcd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                             'execute if score @s bm.zbcd matches 1.. run return run ' + title('@s', 'actionbar', [T('Zib is still in the mothership sick bay: about ', 'gray'),
                                                                                                                 {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                             'execute unless function bm:p37/allowed run return run ' + say("The mothership can't get a lock on you here."),
                             'execute positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p72/zb/summon',
                             'function bm:p72/zb/summon'])
    fn('p72/zb/summon', [f'summon minecraft:wolf ~ ~ ~ {snbt(pet)}',
                         'data modify entity @e[type=minecraft:wolf,tag=bm.zbnew,limit=1,sort=nearest] Owner set from entity @s UUID',
                         f'attribute @e[type=minecraft:wolf,tag=bm.zbnew,limit=1,sort=nearest] minecraft:max_health base set {ZB_HP}',
                         f'data modify entity @e[type=minecraft:wolf,tag=bm.zbnew,limit=1,sort=nearest] Health set value {ZB_HP}f',
                         'scoreboard players operation @e[type=minecraft:wolf,tag=bm.zbnew,limit=1,sort=nearest] bm.pid = @s bm.pid',
                         'scoreboard players set @e[type=minecraft:wolf,tag=bm.zbnew,limit=1,sort=nearest] bm.zbc 20',
                         'scoreboard players set @e[type=minecraft:wolf,tag=bm.zbnew,limit=1,sort=nearest] bm.zbn 0',
                         'execute as @e[type=minecraft:wolf,tag=bm.zbnew,limit=1,sort=nearest] at @s run function bm:p72/zb/rig',
                         'tag @e[type=minecraft:wolf,tag=bm.zbnew] remove bm.zbnew',
                         'particle minecraft:end_rod ~ ~1 ~ 0.2 1.2 0.2 0.02 40', 'particle minecraft:dust{color:[0.4,1.0,0.5],scale:1.5} ~ ~1 ~ 0.3 1.0 0.3 0 30',
                         'playsound minecraft:block.beacon.activate neutral @a[distance=..20] ~ ~ ~ 1 1.6', 'advancement grant @s only bm:story/zib',
                         zsay('Trooper Zib reporting! Point me at something ugly.')])
    fn('p72/zb/dismiss', ['execute as @e[type=minecraft:wolf,tag=bm.zbsel] at @s run function bm:p72/zb/beamup', zsay('Beaming up. Call if you need me!')])
    fn('p72/zb/beamup', ['particle minecraft:end_rod ~ ~1 ~ 0.2 1.2 0.2 0.02 40', 'playsound minecraft:block.beacon.deactivate neutral @a[distance=..20] ~ ~ ~ 1 1.6',
                         'execute on passengers run kill @s', 'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    # fainting: his head part left without the wolf; the medal rests 5 minutes
    s = G.FUNCS['loop/second']
    k = next(i for i, l in enumerate(s) if 'tag=bm.fp_disp] unless function bm:p20/frog/has_vehicle run kill @s' in l)
    s.insert(k, 'execute as @e[type=minecraft:item_display,tag=bm.zbr_head] unless function bm:p20/frog/has_vehicle if score @s bm.pid matches 1.. at @s run function bm:p72/zb/faint')
    fn('p72/zb/faint', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players reset @s bm.pid',
                        'particle minecraft:end_rod ~ ~0.5 ~ 0.3 0.6 0.3 0.05 24', 'playsound minecraft:block.beacon.deactivate neutral @a[distance=..20] ~ ~ ~ 1 1.2',
                        'execute as @a if score @s bm.pid = #me bm.pid run function bm:p72/zb/fainted'])
    fn('p72/zb/fainted', [f'scoreboard players set @s bm.zbcd {PET_CD}',
                          tellraw('@s', PREFIX + [T('Zib faints! ', TEAL, bold=True), T('"Trooper down... beaming to sick bay..." ', '#c8fff4'),
                                                  T(f'The medal needs {PET_CD // 60} minutes before he can come back.', 'gray')])])
    second.append('scoreboard players remove @a[scores={bm.zbcd=1..}] bm.zbcd 1')
    G.FUNCS['p62/died'].insert(-1, 'execute as @e[type=minecraft:wolf,tag=bm.zibpet] if score @s bm.pid = #me bm.pid at @s run function bm:p72/zb/beamup')
    # he's a follower (the limit of three)
    cnt = G.FUNCS['p58/count']
    cnt.insert(len(cnt) - 1, 'execute as @e[type=minecraft:wolf,tag=bm.zibpet] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1')

    # ================================================================== SKIFF ESCORTS
    EC = ART.ESCORT_COLS
    host = snbt({'Tags': ['bm.eskhost', 'bm.esknew'], 'NoAI': B(1), 'NoGravity': B(1), 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(ESK_HP),
                 'attributes': [{'id': 'minecraft:max_health', 'base': D(ESK_HP)}],
                 'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]})
    edisp = snbt({'Tags': ['bm.eskd', 'bm.esknew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:skiff_{EC[0]}_none'}},
                  'item_display': 'fixed', 'teleport_duration': Int(4), 'interpolation_duration': Int(20),
                  'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.1), F(0)], 'scale': [F(0.7)] * 3}})
    for i, c in enumerate(EC):
        fn(f'p72/esk/use_{i}', [f'scoreboard players set #ec bm.rng {i}', 'function bm:p72/esk/use'])
    sel_host = 'execute as @e[type=minecraft:bat,tag=bm.eskhost] if score @s bm.pid = #me bm.pid'
    fn('p72/esk/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       'scoreboard players set #has bm.rng -1', f'{sel_host} store result score #has bm.rng run scoreboard players get @s bm.eskc',
                       'execute if score #has bm.rng matches 0.. if predicate bm:p20/sneaking run return run function bm:p72/esk/send_home',
                       'execute if score #has bm.rng = #ec bm.rng run return run function bm:p72/esk/send_home',
                       'execute if predicate bm:p20/sneaking run return run ' + say("Your escort isn't flying. (Use the beacon to launch it.)"),
                       'execute if score @s bm.eskcd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.eskcd',
                       'execute if score @s bm.eskcd matches 1.. run scoreboard players add #m bm.rng 59', 'execute if score @s bm.eskcd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                       'execute if score @s bm.eskcd matches 1.. run return run ' + title('@s', 'actionbar', [T('Your escort is still being patched up: about ', 'gray'),
                                                                                                           {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                       'execute unless function bm:p37/allowed run return run ' + say('The escort refuses to launch here.'),
                       'execute if score #has bm.rng matches 0.. run function bm:p72/esk/vanish',
                       'function bm:p72/esk/launch'])
    fn('p72/esk/launch', ['execute rotated ~ 0 positioned ^-1.1 ^2.3 ^-0.7 run summon minecraft:bat ~ ~ ~ ' + host,
                          'execute rotated ~ 0 positioned ^-1.1 ^2.3 ^-0.7 run summon minecraft:item_display ~ ~ ~ ' + edisp,
                          'scoreboard players operation @e[tag=bm.esknew] bm.pid = @s bm.pid', 'scoreboard players operation @e[tag=bm.esknew] bm.eskc = #ec bm.rng',
                          'scoreboard players set @e[tag=bm.esknew] bm.esf 10', 'scoreboard players set @e[tag=bm.esknew] bm.esb 0'] +
       [f'execute if score #ec bm.rng matches {i} run data modify entity @e[type=minecraft:item_display,tag=bm.esknew,limit=1] item.components."minecraft:item_model" set value "bm:skiff_{c}_none"'
        for i, c in enumerate(EC)] +
       ['tag @e[tag=bm.esknew] remove bm.esknew', 'particle minecraft:end_rod ^-1.1 ^2.3 ^-0.7 0.3 0.2 0.3 0.05 16',
        'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 0.8 2', title('@s', 'actionbar', T('Escort launched.', '#7dff6a'))])
    fn('p72/esk/send_home', ['function bm:p72/esk/vanish', 'playsound minecraft:block.beacon.deactivate player @s ~ ~ ~ 0.6 2', say('Your escort flies home.')])
    fn('p72/esk/vanish', [f'{sel_host} at @s run particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.05 10', f'{sel_host} at @s run tp @s ~ -500 ~', f'{sel_host} run kill @s',
                          'execute as @e[type=minecraft:item_display,tag=bm.eskd] if score @s bm.pid = #me bm.pid run kill @s'])
    # every tick: at its owner's shoulder (the display glides after it), facing a target or the way they look; lasers
    tick.append('execute as @e[type=minecraft:bat,tag=bm.eskhost] at @s run function bm:p72/esk/tick')
    fn('p72/esk/tick', ['scoreboard players operation #me bm.pid = @s bm.pid', 'tag @s add bm.eskme',
                        'execute as @a if score @s bm.pid = #me bm.pid run tag @s add bm.eskown',
                        'execute unless entity @a[tag=bm.eskown] run return run function bm:p72/esk/orphan',
                        'execute as @a[tag=bm.eskown,limit=1] at @s rotated ~ 0 positioned ^-1.1 ^2.3 ^-0.7 run tp @e[type=minecraft:bat,tag=bm.eskme,limit=1] ~ ~ ~',
                        'execute if score @s bm.esf matches 1.. run scoreboard players remove @s bm.esf 1',
                        f'execute at @s run tag @e[{foe},distance=..16,sort=nearest,limit=1] add bm.eskt',
                        'execute if score @s bm.esf matches ..0 if entity @e[tag=bm.eskt] run function bm:p72/esk/fire',
                        'execute if entity @e[tag=bm.eskt] at @s facing entity @e[tag=bm.eskt,limit=1] feet rotated ~ 0 run function bm:p72/esk/disp',
                        'execute unless entity @e[tag=bm.eskt] at @s rotated as @a[tag=bm.eskown,limit=1] rotated ~ 0 run function bm:p72/esk/disp',
                        'tag @e[tag=bm.eskt] remove bm.eskt', 'tag @a[tag=bm.eskown] remove bm.eskown', 'tag @s remove bm.eskme'])
    fn('p72/esk/disp', ['execute as @e[type=minecraft:item_display,tag=bm.eskd] if score @s bm.pid = #me bm.pid run tp @s ~ ~ ~ ~ 0'])
    fn('p72/esk/orphan', ['execute as @e[type=minecraft:item_display,tag=bm.eskd] if score @s bm.pid = #me bm.pid run kill @s', 'tp @s ~ -500 ~', 'kill @s'])
    fn('p72/esk/fire', ['scoreboard players set @s bm.esf 20', 'scoreboard players set #ray bm.rng 34', 'scoreboard players add @s bm.esn 1',
                        'execute if score @s bm.esn matches 2.. run scoreboard players set @s bm.esn 0',
                        'execute if score @s bm.esn matches 0 at @s facing entity @e[tag=bm.eskt,limit=1] eyes positioned ^0.22 ^ ^0.4 run function bm:p72/esk/beam',
                        'execute if score @s bm.esn matches 1 at @s facing entity @e[tag=bm.eskt,limit=1] eyes positioned ^-0.22 ^ ^0.4 run function bm:p72/esk/beam',
                        'execute at @s run playsound minecraft:entity.guardian.attack neutral @a[distance=..20] ~ ~ ~ 0.25 2',
                        'execute at @s run playsound minecraft:block.respawn_anchor.charge neutral @a[distance=..20] ~ ~ ~ 0.2 2'])
    fn('p72/esk/beam', ['particle minecraft:dust{color:[1.0,0.3,0.3],scale:0.6} ~ ~ ~ 0 0 0 0 1',
                        'execute positioned ~ ~-0.8 ~ if entity @e[tag=bm.eskt,distance=..1.1] run return run function bm:p72/esk/zap',
                        'execute unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:electric_spark ~ ~ ~ 0.1 0.1 0.1 0.1 4',
                        'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.5 run function bm:p72/esk/beam'])
    fn('p72/esk/zap', ['execute as @e[tag=bm.eskt,limit=1] at @s run damage @s 5 minecraft:mob_projectile by @e[type=minecraft:bat,tag=bm.eskme,limit=1]',
                       'execute as @e[tag=bm.eskt,limit=1] at @s run particle minecraft:electric_spark ~ ~1 ~ 0.2 0.3 0.2 0.15 8'])
    # archers, blazes, witches and Vorn troopers take shots at it (a quarter of the time, 2 damage); out of a fight it mends
    wjson('bm/tags/entity_type/p72_ranged.json', {'values': ['minecraft:skeleton', 'minecraft:stray', 'minecraft:bogged', 'minecraft:pillager', 'minecraft:blaze',
                                                            'minecraft:ghast', 'minecraft:witch', 'minecraft:breeze', 'minecraft:shulker', 'minecraft:illusioner']})
    second.append('execute as @e[type=minecraft:bat,tag=bm.eskhost] at @s run function bm:p72/esk/sec')
    fn('p72/esk/sec', ['tag @s add bm.eskflak',
                       'execute as @e[type=#bm:p72_ranged,distance=..14] at @s run function bm:p72/esk/potshot',
                       'execute as @e[tag=bm.vtroop,distance=..14] at @s run function bm:p72/esk/potshot',
                       'tag @s remove bm.eskflak',
                       f'execute unless entity @e[{foe},distance=..16] run effect give @s minecraft:regeneration 3 0 true',
                       # the bob: up and down, slowly (the display interpolates between)
                       'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players add @s bm.esb 1',
                       'execute if score @s bm.esb matches 2.. run scoreboard players set @s bm.esb 0',
                       'execute if score @s bm.esb matches 0 as @e[type=minecraft:item_display,tag=bm.eskd] if score @s bm.pid = #me bm.pid run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{translation:[0f,0.18f,0f]}}',
                       'execute if score @s bm.esb matches 1 as @e[type=minecraft:item_display,tag=bm.eskd] if score @s bm.pid = #me bm.pid run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{translation:[0f,0f,0f]}}'])
    fn('p72/esk/potshot', ['execute store result score #r bm.rng run random value 1..4', 'execute unless score #r bm.rng matches 1 run return 0',
                           'damage @e[type=minecraft:bat,tag=bm.eskflak,limit=1] 2 minecraft:mob_projectile by @s',
                           'execute at @e[type=minecraft:bat,tag=bm.eskflak,limit=1] run particle minecraft:crit ~ ~ ~ 0.2 0.2 0.2 0.2 6'])
    # shot down: the display without its host
    second.append('execute as @e[type=minecraft:item_display,tag=bm.eskd] at @s run function bm:p72/esk/check')
    fn('p72/esk/check', ['scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_host} run return run scoreboard players set #me bm.rng 1',
                         'particle minecraft:explosion ~ ~ ~ 0 0 0 0 1', 'particle minecraft:smoke ~ ~ ~ 0.2 0.2 0.2 0.05 12',
                         'playsound minecraft:entity.generic.explode neutral @a[distance=..24] ~ ~ ~ 0.5 1.6',
                         'execute as @a if score @s bm.pid = #me bm.pid run function bm:p72/esk/downed', 'kill @s'])
    fn('p72/esk/downed', [f'scoreboard players set @s bm.eskcd {PET_CD}',
                          tellraw('@s', PREFIX + [T('Your Skiff Escort is shot down! ', '#ff7a5a', bold=True), T(f'It needs {PET_CD // 60} minutes of repairs.', 'gray')])])
    second.append('scoreboard players remove @a[scores={bm.eskcd=1..}] bm.eskcd 1')
    G.FUNCS['p62/died'].insert(-1, 'execute at @s run function bm:p72/esk/vanish')
    # the reactor's reward: a colour you haven't got (while there are any)
    G.FUNCS['p52/rx/win'].append('execute as @a[gamemode=!spectator,distance=..40] run function bm:p72/esk/reward')
    fn('p72/esk/reward', ['scoreboard players set #pick bm.rng -1', f'execute store result score #r bm.rng run random value 0..{len(EC) - 1}',
                          'scoreboard players set #n bm.rng 0', 'function bm:p72/esk/try',
                          'execute if score #pick bm.rng matches -1 run scoreboard players operation #pick bm.rng = #r bm.rng'] +
       [f'execute if score #pick bm.rng matches {i} run function bm:p72/esk/give_{i}' for i in range(len(EC))])
    fn('p72/esk/try', [f'execute if score #r bm.rng matches {i} unless entity @s[advancements={{bm:story/escort_all={{c{i}=true}}}}] run return run scoreboard players operation #pick bm.rng = #r bm.rng'
                       for i in range(len(EC))] +
       ['scoreboard players add #r bm.rng 1', f'execute if score #r bm.rng matches {len(EC)}.. run scoreboard players set #r bm.rng 0',
        'scoreboard players add #n bm.rng 1', f'execute if score #n bm.rng matches ..{len(EC) - 1} run function bm:p72/esk/try'])
    for i, c in enumerate(EC):
        nm, col = CNAME[c]
        fn(f'p72/esk/give_{i}', [give(f'skiff_escort_{c}'),
                                 tellraw('@s', PREFIX + [T('Zorp\'s engineers salvage a skiff from the wreck: ', 'gray'), T(f'a {nm} Skiff Escort', col, bold=True),
                                                         T(' is yours!', 'gray')])])
    for i, c in enumerate(EC):
        fn(f'admin/escort_{c}', [give(f'skiff_escort_{c}')])
    crit = {f'c{i}': {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': 'minecraft:totem_of_undying',
                                                                                          'predicates': {'minecraft:custom_data': f'{{bm:"skiff_escort_{c}"}}'}}]}}
            for i, c in enumerate(EC)}
    icon = lambda m: {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': m}}
    wjson('bm/advancement/story/escort.json', {'parent': 'bm:story/reactor', 'criteria': crit, 'requirements': [list(crit)],
                                               'display': {'icon': icon('bm:skiff_escort_crimson'), 'title': T('Wingman', 'yellow'),
                                                           'description': T('Earn a Skiff Escort from a Dreadnought reactor', 'gray'),
                                                           'frame': 'task', 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    wjson('bm/advancement/story/escort_all.json', {'parent': 'bm:story/escort', 'criteria': crit,
                                                   'display': {'icon': icon('bm:skiff_escort_gold'), 'title': T('Squadron Leader', 'yellow'),
                                                               'description': T(f'Collect all {len(EC)} colours of Skiff Escort', 'gray'),
                                                               'frame': 'challenge', 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    wjson('bm/advancement/story/zib.json', {'parent': 'bm:story/defend', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                            'display': {'icon': icon('bm:donadian_medal'), 'title': T('Trooper Zib Reporting', 'yellow'),
                                                        'description': T('Call Zib down with the Donadian Medal', 'gray'),
                                                        'frame': 'task', 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})

    # ================================================================== THE VAULT: coat check, loaner kits, contracts
    keep_any = '*[' + '|'.join(f'minecraft:custom_data~{{bm:"{t}"}}' for t in KEEP) + ']'
    keep_not = '*[' + ','.join(f'!minecraft:custom_data~{{bm:"{t}"}}' for t in KEEP) + ']'
    kit_pred = '*[minecraft:custom_data~{bm_kit:1b}]'
    fn('p72/bag/stage', [f'execute unless block {STAGE} minecraft:barrel run setblock {STAGE} minecraft:barrel'])
    # going in: everything but heist tools into safekeeping (a bag left from a crash goes back first)
    fn('p72/bag/check', ['execute store result storage bm:gv tmp.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p72/bag/check2 with storage bm:gv tmp'])
    fn('p72/bag/check2', [# (a bag still held from before - a crash mid-heist - is never overwritten: it waits, and this time you keep your things)
                          '$execute if data storage bm:gv bag.p$(pid) run return run ' + tellraw('@s', PREFIX + [T('The Fixer is still minding your last lot of gear - ', GOLD),
                                                                                                                 T('this time you keep what you carry.', 'gray')]),
                          '$data modify storage bm:gv bag.p$(pid) set value {inv:[],eq:{}}',
                          '$data modify storage bm:gv bag.p$(pid).inv set from entity @s Inventory',
                          '$data modify storage bm:gv bag.p$(pid).eq set from entity @s equipment'] +
       [f'$data remove storage bm:gv bag.p$(pid).inv[{{components:{{"minecraft:custom_data":{{bm:"{t}"}}}}}}]' for t in KEEP] +
       sum(([f'$execute if items entity @s {sl} {keep_any} run data remove storage bm:gv bag.p$(pid).eq.{k}',
             f'execute unless items entity @s {sl} {keep_any} run item replace entity @s {sl} with minecraft:air'] for k, sl in SLOT_OF.items()), []) +
       [f'clear @s {keep_not}',
        tellraw('@s', PREFIX + [T('The Fixer checks your gear at the door. ', GOLD), T('You\'ll have every bit of it back the moment you leave. ', 'gray'),
                                T('Pick a kit from the racks in the den.', 'white')])])
    # coming out: the kit stays; your own things go back where they were; what you found inside comes too
    fn('p72/bag/restore', ['execute store result storage bm:gv tmp.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p72/bag/restore2 with storage bm:gv tmp'])
    fn('p72/bag/restore2', ['$execute unless data storage bm:gv bag.p$(pid) run return 0',
                            # what you're carrying now (your finds) waits a moment in storage, then is handed over once you've landed
                            '$data modify storage bm:gv cb.p$(pid) append from entity @s Inventory[]'] +
       [f'$data modify storage bm:gv cb.p$(pid) append from entity @s equipment.{k}' for k in SLOT_OF] +
       ['clear @s', '$data modify storage bm:gv rs set from storage bm:gv bag.p$(pid)', '$data remove storage bm:gv bag.p$(pid)',
        'execute in bm:gutter run function bm:p72/bag/stage', 'function bm:p72/bag/put_inv'] +
       [f'execute if data storage bm:gv rs.eq.{k} run function bm:p72/bag/eq_{k}' for k in SLOT_OF] +
       ['scoreboard players set @s bm.bagt 2', tellraw('@s', PREFIX + [T('The Fixer hands back your gear.', GOLD)])])
    second.append('execute as @a[scores={bm.bagt=1..}] run function bm:p72/bag/later')
    fn('p72/bag/later', ['scoreboard players remove @s bm.bagt 1', 'execute if score @s bm.bagt matches 1.. run return 0', 'scoreboard players reset @s bm.bagt',
                         'execute store result storage bm:gv tmp.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p72/bag/later2 with storage bm:gv tmp'])
    fn('p72/bag/later2', ['$data modify storage bm:gv carry set from storage bm:gv cb.p$(pid)', '$data remove storage bm:gv cb.p$(pid)',
                          'execute at @s run function bm:p72/bag/carry_back'])
    fn('p72/bag/put_inv', ['execute unless data storage bm:gv rs.inv[0] run return 0',
                           'data modify storage bm:gv one set from storage bm:gv rs.inv[0]', 'data remove storage bm:gv rs.inv[0]',
                           'execute store result storage bm:gv sl.s int 1 run data get storage bm:gv one.Slot', 'data modify storage bm:gv one.Slot set value 0b',
                           f'execute in bm:gutter run data modify block {STAGE} Items set value []',
                           f'execute in bm:gutter run data modify block {STAGE} Items append from storage bm:gv one',
                           'function bm:p72/bag/to with storage bm:gv sl', 'function bm:p72/bag/put_inv'])
    fn('p72/bag/to', ['$function bm:p72/bag/s/$(s)'])
    for n in range(36):
        fn(f'p72/bag/s/{n}', [f'execute in bm:gutter run item replace entity @s {"hotbar." + str(n) if n < 9 else "inventory." + str(n - 9)} from block {STAGE} container.0'])
    for k, sl in SLOT_OF.items():
        fn(f'p72/bag/eq_{k}', [f'data modify storage bm:gv one set from storage bm:gv rs.eq.{k}', 'data modify storage bm:gv one.Slot set value 0b',
                               f'execute in bm:gutter run data modify block {STAGE} Items set value []',
                               f'execute in bm:gutter run data modify block {STAGE} Items append from storage bm:gv one',
                               f'execute in bm:gutter run item replace entity @s {sl} from block {STAGE} container.0'])
    fn('p72/bag/carry_back', ['execute unless data storage bm:gv carry[0] run return 0',
                              'data modify storage bm:gv one set from storage bm:gv carry[0]', 'data remove storage bm:gv carry[0]', 'data remove storage bm:gv one.Slot',
                              'summon minecraft:item ~ ~0.3 ~ {Item:{id:"minecraft:stone",count:1},PickupDelay:0s,Tags:["bm.bagnew"]}',
                              'data modify entity @e[type=minecraft:item,tag=bm.bagnew,limit=1,sort=nearest] Item set from storage bm:gv one',
                              'tag @e[type=minecraft:item,tag=bm.bagnew] remove bm.bagnew', 'function bm:p72/bag/carry_back'])
    # hooks: in (fresh or joining) - check the gear; out (every way out passes p70/unraid) - drop the kit, give it back
    for s_ in range(P70.SLOTS):
        for f in (f'p70/s{s_}/enter', f'p70/s{s_}/join'):
            L = G.FUNCS[f]; k = L.index('function bm:p70/save_ret'); L.insert(k + 1, 'function bm:p72/bag/check')
    G.FUNCS['p70/unraid'][0:0] = [f'clear @s {kit_pred}', 'function bm:p72/kit/strip', 'scoreboard players reset @s bm.gvrole',
                                  'execute at @s run function bm:p72/bag/restore']
    # kit items never leave: anyone outside a heist loses them; the den racks' kits are re-issued after a knock-out
    second.append(f'clear @a[tag=!bm.gvp,tag=!bm.gvdead] {kit_pred}')
    rev = G.FUNCS['p70/revive']
    k = next(i for i, l in enumerate(rev) if 'function bm:p70/alarm_inst' in l)
    rev[k + 1:k + 1] = ['execute if score @s bm.gvrole matches 1.. run function bm:p72/kit/reissue',
                        'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run scoreboard players add @s bm.gvko 1']
    fn('p72/kit/reissue', [f'execute in bm:gutter as @e[type=minecraft:item] if items entity @s contents {kit_pred} run kill @s', f'clear @s {kit_pred}'] +
       [f'execute if score @s bm.gvrole matches {r} run function bm:p72/kit/give_{r}' for r in ROLES] +
       [tellraw('@s', PREFIX + [T('The Fixer tosses you a fresh kit.', 'gray')])])
    fn('p72/kit/strip', ['attribute @s minecraft:max_health modifier remove bm:gv_role_tank', 'attribute @s minecraft:knockback_resistance modifier remove bm:gv_role_tank'])
    for r, (nm, col, desc, armor, hand) in ROLES.items():
        lines = []
        for k, iid in armor.items():
            sl = SLOT_OF[k]
            lines += [f'execute unless items entity @s {sl} * run item replace entity @s {sl} with {kit_arg(iid, r)}',
                      f'execute if items entity @s {sl} {keep_any} run give @s {kit_arg(iid, r)}']
        for h in hand:
            iid, n, extra = (h, 1, None) if isinstance(h, str) else (h + (None,))[:3]
            lines.append(f'give @s {kit_arg(iid, extra=extra)} {n}')
        lines.append(f'give @s {kit_arg(KIT_FOOD[0])} {KIT_FOOD[1]}')                   # (2.63) and something to eat
        if r == 1:
            lines += ['attribute @s minecraft:max_health modifier add bm:gv_role_tank 8 add_value',
                      'attribute @s minecraft:knockback_resistance modifier add bm:gv_role_tank 0.5 add_value']
        fn(f'p72/kit/give_{r}', lines)
        fn(f'p72/kit/pick_{r}', ['execute unless entity @s[tag=bm.gvp] run return 0',
                                 'scoreboard players operation #pi bm.rng = @s bm.gvi', 'scoreboard players set #st bm.rng 0',
                                 'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #pi bm.rng store result score #st bm.rng run scoreboard players get @s bm.gvst',
                                 f'execute if score @s bm.gvrole matches {r} run return run ' + say(f'You already carry the {nm} kit.', col),
                                 'execute if score #st bm.rng matches 2.. if score @s bm.gvrole matches 1.. run return run ' + say('Kits are locked once the heist is on.', 'red'),
                                 f'clear @s {kit_pred}', 'function bm:p72/kit/strip', f'scoreboard players set @s bm.gvrole {r}', f'function bm:p72/kit/give_{r}',
                                 'playsound minecraft:item.armor.equip_iron player @s ~ ~ ~ 1 1', title('@s', 'actionbar', [T(f'{nm} kit. ', col, bold=True), T(desc, 'gray')])])
    # nobody goes in bare: no kit picked when the heist begins - Offense
    beg = G.FUNCS['p70/begin']
    k = next(i for i, l in enumerate(beg) if l.startswith('tag @a[tag=bm.gvme] remove bm.gvme'))
    beg.insert(k, 'execute as @a[tag=bm.gvme] unless score @s bm.gvrole matches 1.. at @s run function bm:p72/kit/pick_2')
    # role passives (each second, in a heist)
    second += ['effect give @a[tag=bm.gvp,scores={bm.gvrole=2}] minecraft:strength 3 0 true',
               'effect give @a[tag=bm.gvp,scores={bm.gvrole=3}] minecraft:speed 3 0 true',              # (2.64) the ranged crew keeps its distance
               f'execute as @a[tag=bm.gvp,scores={{bm.gvrole=3}}] at @s run effect give @e[{foe},distance=..24] minecraft:glowing 3 0 true',
               'execute as @a[tag=bm.gvp,scores={bm.gvrole=4}] at @s run function bm:p72/kit/mend']
    fn('p72/kit/mend', ['tag @s add bm.gvself', 'effect give @a[tag=bm.gvp,tag=!bm.gvself,distance=..8] minecraft:regeneration 3 0 true',
                        'particle minecraft:happy_villager ~ ~1 ~ 3 0.5 3 0 4', 'tag @s remove bm.gvself'])
    # the racks: four armour stands in the den wearing each kit (right-click to take it)
    racks = []
    for r, (nm, col, desc, armor, hand) in ROLES.items():
        x = 7 + 3 * r
        eq = {k: G.stack(iid) for k, iid in armor.items() if k != 'offhand'}
        eq['mainhand'] = G.stack(hand[0])
        if 'offhand' in armor: eq['offhand'] = G.stack(armor['offhand'])
        stand = {'Tags': ['bm.gvprop', 'bm.gvkitstand'], 'NoGravity': B(1), 'Invulnerable': B(1), 'ShowArms': B(1), 'NoBasePlate': B(1),
                 'DisabledSlots': Int(4144959), 'Rotation': [F(180), F(0)], 'equipment': eq}
        racks += [f'summon minecraft:armor_stand {rel(x, 4, 21)} {snbt(stand)}',
                  f'summon minecraft:interaction {rel(x, 4, 21)} {snbt({"Tags": ["bm.gvprop", "bm.gvkithit", f"bm.gvk{r}"], "width": F(0.9), "height": F(2.0), "response": B(1)})}',
                  f'summon minecraft:text_display {rel(x, 6.6, 21)} ' + snbt({'Tags': ['bm.gvprop'], 'billboard': 'vertical', 'line_width': Int(110),
                                                                            'background': Int(1879048192),
                                                                            'text': [T(nm.upper() + '\n', col, bold=True), T(desc, 'gray')],
                                                                            'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                               'translation': [F(0)] * 3, 'scale': [F(0.55)] * 3}})]
    racks.append(f'summon minecraft:text_display {rel(14.5, 7.6, 21)} ' + snbt({'Tags': ['bm.gvprop'], 'billboard': 'vertical',
                                                                              'text': T('THE FIXER\'S LOANERS - right-click a rack', GOLD, bold=True),
                                                                              'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                                 'translation': [F(0)] * 3, 'scale': [F(0.7)] * 3}}))
    G.FUNCS['p70/r/lobby/init'] += racks
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.gvkithit] if data entity @s interaction at @s run function bm:p72/kit/click')
    fn('p72/kit/click', ['tag @s add bm.gvkme', 'execute on target run function bm:p72/kit/who', 'tag @s remove bm.gvkme', 'data remove entity @s interaction'])
    fn('p72/kit/who', [f'execute if entity @e[type=minecraft:interaction,tag=bm.gvkme,tag=bm.gvk{r}] run return run function bm:p72/kit/pick_{r}' for r in ROLES])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.gvkithit] if data entity @s attack run data remove entity @s attack')

    # ---- the Fixer's contract (one per job): on the sheet; +2 shares and a purse when met
    ini = G.FUNCS['p70/inst_init']
    ini[-1:-1] = ['execute store result score @s bm.gvct run random value 1..3', 'scoreboard players set @s bm.gvko 0',
                  'scoreboard players operation #gct bm.rng = @s bm.gvct']
    sh = G.FUNCS['p70/sheet']
    k = next(i for i, l in enumerate(sh) if 'Press a button by the door to begin' in l)
    sh[k:k] = ['execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run scoreboard players operation #gct bm.rng = @s bm.gvct'] + \
              [f'execute if score #gct bm.rng matches {c} run data modify storage bm:gv sheet append value {{text:"\\nCONTRACT: {nm}","color":"#d9a066",bold:true}}'
               for c, (nm, d) in CONTRACTS.items()] + \
              [f'execute if score #gct bm.rng matches {c} run data modify storage bm:gv sheet append value {{text:" - {d} (+2 shares)\\n",color:"gray"}}'
               for c, (nm, d) in CONTRACTS.items()]
    pay = G.FUNCS['p70/payout_inst']
    k = next(i for i, l in enumerate(pay) if 'execute if score #sh bm.rng matches ..1 run scoreboard players set #sh bm.rng 2' in l)
    pay[k + 1:k + 1] = ['scoreboard players set #cok bm.rng 0',
                        'execute if score @s bm.gvct matches 1 if score @s bm.gva matches ..24 run scoreboard players set #cok bm.rng 1',
                        'execute if score @s bm.gvct matches 2 if score @s bm.gvko matches 0 run scoreboard players set #cok bm.rng 1',
                        'scoreboard players operation #lim bm.rng = @s bm.gvk', 'scoreboard players operation #lim bm.rng *= #1800 bm.rng',
                        'execute if score @s bm.gvct matches 3 if score @s bm.gvtm <= #lim bm.rng run scoreboard players set #cok bm.rng 1',
                        'execute if score #cok bm.rng matches 1 run scoreboard players add #sh bm.rng 2',
                        'execute if score #cok bm.rng matches 1 run ' + tellraw('@a[tag=bm.gvme]', PREFIX + [T('Contract met! ', '#d9a066', bold=True),
                                                                                                             T('The Fixer adds two shares and a purse.', 'gray')]),
                        'execute if score #cok bm.rng matches 1 as @a[tag=bm.gvme] run loot give @s loot bm:gv/coins']
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #1800 bm.rng 1800']

    # ================================================================== admin, uninstall
    fn('admin/zib', ['function bm:p72/zb/try_summon'])
    fn('admin/display_cases', [give(f'display_case_{v}', 4) for v in CV])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.dcase]', 'kill @e[type=minecraft:item_display,tag=bm.dcitem]',
                                       'kill @e[type=minecraft:interaction,tag=bm.dchit]', 'kill @e[type=minecraft:item_display,tag=bm.eskd]',
                                       'kill @e[type=minecraft:bat,tag=bm.eskhost]', 'execute as @e[type=minecraft:wolf,tag=bm.zibpet] on passengers run kill @s',
                                       'kill @e[type=minecraft:wolf,tag=bm.zibpet]']

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def rp(R):
    import sys
    R.TEXTURE_MODS.append(ART)
    for name, (tex, els) in ART.case_models(R.cube).items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('dcase_',)
    for v in ART.CASES:
        R.ICONS[f'display_case_{v}'] = ART.case_icon(R, v)
    for c in ART.ESCORT_COLS:
        R.ICONS[f'skiff_escort_{c}'] = ART.escort_icon(R, CNAME[c][1])
    def post(R2):
        rig = ART.zib_rig()
        _p, blink = ART.zib_parts()
        def model(name, els):
            used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
            t = {k: ART.ZB_TEX[k] for k in used}; t['particle'] = ART.ZB_TEX['f']
            R2.wj(f'assets/bm/models/item/{name}.json', {'textures': t, 'elements': els, 'display': {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}})
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
        for n in rig.parts:
            model(f'zbr_{n}', rig.shifted(n))
        model('zbr_eyes_blink', rig.shifted('eyes', blink))
    R.POST.append(post)

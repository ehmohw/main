"""2.98: THE BOUND SOVEREIGN - what's left of the Dread Sovereign (phase238), bound by its own chains to whoever broke it. HARD MODE:
the Sovereign's Eye comes from its ashes, the first time it falls (dread_sovereign_art.py, form 'bound'; undercrown_lore.py).
Somewhere in it, very faintly, Aurel - the first light - is listening.

  CLEAVE    a foe within 3, every 1.5 s: the greatsword (7).
  EYE BOLT  a foe within 14, every 4 s: a bolt from its eye (8, withering).
  CHAINS    (charged, every minute) its chains lash out at every monster within 7: 12, dragged in and held (slowed).
  DREAD WARD you, hurt in a fight, every 10 s: Resistance and Absorption - and the Dread near you weakened (they know whose it was).
  VIGIL     out of a fight, every minute: it kneels beside you - Night Vision and Fire Resistance; "he remembers the light, a little".
  THE DREAD BOW TO IT  Dread mobs within 10 of it are weakened while it's out.
Everything else is every follower's: sitting, a wardrobe, a rare aura, a shiny, the Partner Wheel, a frame, a display case, Cecil's
doll, the honours, a Raid Contract; pairs with Bender, Mr. Capshun, Henry and Nia - and THE FIRST AND THE LAST LIGHT, with the
Lightbringer, if she was ever yours."""
from items import T, ITEMS
from useitem import hold, HOLD
import dread_sovereign_art as DA
import rigpet as RP
import rigface as RF2
import phase141 as P141
import phase134 as P134
import phase235 as P235
import phase95 as FX
import undercrown_lore as L
import phase238  # noqa: F401  (its Eye, the follower's summoning item, is the Sovereign's spoils)

COL = L.SOV_COL


class Sovereign(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'sovereign', 'The Bound Sovereign', COL, '#ff9a9a', 'p239', 'xv', 'xq'
    A = RF2.art(DA)
    MENU, PET_HP, PET_CD, ITEM = 4950, 60, 150, 'sov_eye'
    pron, they = 'him', 'he'
    FACE = {'happy': None, 'surprised': 'wide', 'hurt': 'dim', 'sleepy': 'closed', 'blink': 'closed', 'squint': 'narrowed', 'serious': 'narrowed'}
    ATTRS = dict(armor=12, attack_damage=7, movement_speed=0.36, follow_range=32, step_height=1.1)
    SCALE, HIT = 1.15, (1.1, 2.4)
    SWAP = tuple(DA.PARTS)                      # (every part: none of its models is a plain 'ds_<part>')
    SWAP_START = True
    CYCLE = P235.cycle((240, [(0, 'idle_a'), (120, 'idle_b')]), (240, [(0, 'sit_a'), (120, 'sit_b')]),
                       (None, [(0, 'happy')]),
                       {7: (None, [(0, 'slash_up'), (5, 'slash')]), 8: (None, [(0, 'bolt_up'), (8, 'bolt')]),
                        12: (None, [(0, 'slash_up'), (8, 'slash'), (16, 'happy')]), 13: (None, [(0, 'happy'), (16, 'idle_a')]),
                        14: (None, [(0, 'sit_b'), (40, 'idle_a')])})
    DUR = dict(P235._DUR, slash_up=4, slash=2, bolt_up=6, bolt=3)
    QUIPS = ['(the chains on it clink. It looks at them for a long time.)', '"...light. There was light, once. I remember the shape of it."',
             '"You broke me. I am... grateful. I think."', '(it stands very still, and very tall, between you and the dark)',
             '"The Dread still listen for my voice. I have nothing to say to them."', '(its eye dims, and brightens, like something breathing)']
    HELLO = ('(the Bound Sovereign strides back to your side, chains dragging)', '(the chains go taut - and the Bound Sovereign is there, kneeling) "...I answer."',
             '(it bows its crowned head, and the chains draw it away into the dark)')
    SIT = ('"As you will."', '(it kneels, the greatsword planted before it, like a knight at a vigil)')
    FAINT = '"...the chains... hold..."'
    NOT_YOURS = '"I am bound to another. Go."'
    POWERS = [('Cleave', 'a foe within 3, every 1.5 s: the greatsword - 7'),
              ('Eye Bolt', 'a foe within 14, every 4 s: a bolt from its eye - 8, withering'),
              ('Chains', 'charged, every minute: its chains lash every monster within 7 - 12, dragged in and held fast'),
              ('Dread Ward', 'you, hurt in a fight, every 10 s: Resistance and Absorption - and the Dread near you weakened'),
              ('Vigil', 'out of a fight beside you, every minute: it kneels - Night Vision and Fire Resistance'),
              ('The Dread Bow', 'while it is out, the Dread near it (10) are weakened: they know whose it was')]
    INTRO = [T('The Bound Sovereign', COL, bold=True), T(' - what is left of the Dread Sovereign, bound by its own chains. ', 'gray'),
             T('Somewhere in it, Aurel is listening.', '#fff4d0', italic=True)]
    BUTTONS = ()
    BURST = ['particle minecraft:sculk_soul ~ ~1.4 ~ 0.4 0.8 0.4 0.03 20', 'particle minecraft:dust{color:[0.82,0.1,0.18],scale:1.4} ~ ~1.2 ~ 0.5 0.8 0.5 0 20',
             'particle minecraft:block{block_state:"minecraft:iron_chain"} ~ ~1 ~ 0.4 0.6 0.4 0 16']
    FADE_SOUND = 'playsound minecraft:block.chain.break neutral @a[distance=..20] ~ ~ ~ 1 0.6'
    SUMMON_EXTRA = ['playsound minecraft:block.chain.place neutral @a[distance=..24] ~ ~ ~ 1.2 0.5', 'playsound minecraft:entity.warden.heartbeat neutral @a[distance=..24] ~ ~ ~ 0.8 0.6']
    ENC_POSES = [(0, 'sit_b'), (40, 'idle_a')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:sculk_soul ~ ~2 ~ 0.3 0.3 0.3 0.01 4'
    ADV = ('Bound', 'Take the Sovereign\'s Eye from its ashes - and what is left of it with you')
    ADMIN_HINT = 'Hard mode: fell the Dread Sovereign at the bottom of the Undercrown. Its Eye is in the ashes, the first time.'
    MEET_HINT = 'Hard mode: fell the Dread Sovereign. Its Eye is in the ashes.'


RP.register(Sovereign)
RF2.setup(Sovereign, 'head')

# its Eye (phase238 defines it) calls it
_e = ITEMS['sov_eye']
_e['comps'].update(hold('none'))
HOLD['sov_eye'] = f'bm:{Sovereign.pfx}/use'
_DOLL = 'A doll of the Bound Sovereign - a crown far too big for it, and a very small sword.'
from items import item, TOTEM
item('doll_sovereign', TOTEM, 'Bound Sovereign Doll', COL, [_DOLL, ('Right-click a block: set it down.', 'blue'), ('Right-click it: it twirls.', 'blue'),
                                                          ('Sneak + punch: pick it up.', 'gray')], model='bm:doll_sovereign', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_sovereign'] = 'bm:p141/doll_sovereign/use'
P141.DOLLS.append(('doll_sovereign', Sovereign.NAME, COL, _DOLL, 'minecraft:sculk_soul', 'minecraft:block.chain.place', 'minecraft:poof'))
P141.DOLL_FROM['doll_sovereign'] = ('sov_eye', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
P134.FIT['sov_eye'] = (0.0, 2.3, -0.9, 0.9, -0.6, 0.6)                 # (re-measured: phase134.measure)

# ---- its pairs with Bender and Mr. Capshun - and with the Lightbringer (Henry's and Nia's: cat_bonds)
import phase188 as P188
_O = P188.O
_eff = lambda *es: [f'effect give {_O} minecraft:{e} {15 if e == "night_vision" else 3} {a} true' for e, a in es]
P188.VNAME.update({'sovereign': 'the Bound Sovereign'})
P188.PAIRS.update({
    'xv_bender': ('sovereign', 'bender', 'Good Boy, Dread King', '#e0a860', 'The Bound Sovereign and Bender - the goodest boy is not afraid of it at all',
                  _eff(('strength', 0), ('speed', 0)),
                  [('bender', '(drops a stick at its armoured feet, tail going)'), ('sovereign', '"...I do not throw sticks." (it throws the stick)')],
                  [('sovereign', '"Why does it not fear me?"', 'bender', '(licks its gauntlet)')]),
    'xv_capshun': ('sovereign', 'capshun', 'The Villain\'s Epilogue', '#f0f0f0', 'The Bound Sovereign and Mr. Capshun - every story needs a last chapter',
                   _eff(('resistance', 0), ('haste', 0)),
                   [('capshun', '[Mr. Capshun narrates: "And the villain, defeated, found he had nowhere left to go but along."]'), ('sovereign', '"...Is that how it ends?"')],
                   [('capshun', '[Mr. Capshun narrates: "He drew it a halo. It did not fit. It never had."]', 'sovereign', '(it looks at the drawing for a very long time)')]),
    'xv_lightbringer': ('sovereign', 'lightbringer', 'The First and the Last Light', '#fff4d0', 'The Bound Sovereign and the Lightbringer - Aurel, and the one who came after',
                        _eff(('regeneration', 1), ('resistance', 0)),
                        [('lightbringer', '"Aurel. Do you know me?"'), ('sovereign', '"...No. But I know that you are kind. I remember kind."')],
                        [('sovereign', '"Why do you walk beside me, herald?"', 'lightbringer', '"Because light holds. It always holds. Even for you."')]),
})
P188.ICON.update({'xv_bender': 'bm:sov_eye', 'xv_capshun': 'bm:sov_eye', 'xv_lightbringer': 'bm:sov_eye'})


def extend_offers(O, offer):
    pass


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(Sovereign, R, R.ICONS.get('sov_eye'))
    RF2.faces(Sovereign, 'head', R)


def textures():
    return {}                                   # (the art's own textures go in with the boss, phase238)


def generate_early(G):
    RP.contract(Sovereign, G)


def _abilities(G, X):
    fn, pfx, foe = G.fn, X.pfx, X.foe
    K = dict(melee=dict(st=7, x=8, at=5, cd=30, reach=3.0),
             ranged=dict(st=8, x=16, at=10, cd=80, near=3, far=14, face='serious', go=['playsound minecraft:entity.warden.sonic_charge neutral @a[distance=..16] ~ ~ ~ 0.4 1.6']),
             charged=dict(st=12, x=24, at=10, cd=1200, r=7, face='serious', go=['playsound minecraft:block.chain.break neutral @a[distance=..16] ~ ~ ~ 1 0.5']),
             support=dict(st=13, x=20, at=8, cd=200, face='happy'),
             kind=dict(st=14, x=44, at=20, cd=1200, face='blink'))
    lines = P235.kit(G, X, K)
    P235.melee(G, X, 7, 3.0, ['particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.2 0.3 0 2', 'particle minecraft:dust{color:[0.6,0.0,0.1],scale:1.2} ~ ~1 ~ 0.4 0.4 0.4 0 10'],
               'minecraft:entity.player.attack.sweep')
    tg = f'@e[{foe},distance=..14,sort=nearest,limit=1]'
    fn(f'{pfx}/ranged', X.hit(8) + [f'execute anchored eyes positioned ^ ^ ^1 facing entity {tg} eyes run function bm:{pfx}/bolt_fx', f'execute as {tg} at @s run function bm:{pfx}/bolted'] + X.end)
    fn(f'{pfx}/bolt_fx', [f'particle minecraft:dust{{color:[0.95,0.12,0.2],scale:1.4}} ^ ^ ^{d} 0.05 0.05 0.05 0 2' for d in range(1, 13)] +
       ['playsound minecraft:entity.blaze.shoot neutral @a[distance=..16] ~ ~ ~ 0.6 0.5'])
    fn(f'{pfx}/bolted', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:wither 3 0', 'particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.4 0.3 0.02 10'])
    fn(f'{pfx}/charged', X.hit(12) + [f'execute as @e[{foe},distance=..7] at @s run function bm:{pfx}/chained'] + X.end)
    fn(f'{pfx}/chained', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 4 3',
                          'execute facing entity @e[tag=bm.xvme,limit=1] feet if block ^ ^ ^1.5 #bm:grap_pass if block ^ ^1 ^1.5 #bm:grap_pass run tp @s ^ ^ ^1.5',
                          'particle minecraft:block{block_state:"minecraft:iron_chain"} ~ ~1 ~ 0.3 0.6 0.3 0 16'])
    fn(f'{pfx}/support', ['execute on owner if entity @s[distance=..16] at @s run function bm:p239/ward_you'])
    fn('p239/ward_you', ['effect give @s minecraft:resistance 8 0 true', 'effect give @s minecraft:absorption 20 1 true',
                         'effect give @e[tag=bm.dread,distance=..10] minecraft:weakness 6 1', 'particle minecraft:dust{color:[0.82,0.1,0.18],scale:1.2} ~ ~1 ~ 0.6 0.8 0.6 0 16',
                         'playsound minecraft:block.chain.place player @s ~ ~ ~ 1 0.6'])
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p239/vigil_you'])
    fn('p239/vigil_you', ['effect give @s minecraft:night_vision 60 0 true', 'effect give @s minecraft:fire_resistance 60 0 true',
                          'particle minecraft:end_rod ~ ~1.6 ~ 0.3 0.3 0.3 0.01 6',
                          'execute unless entity @s[tag=bm.hush] run ' + G.title('@s', 'actionbar', [T('The Bound Sovereign: ', COL, bold=True), T('(it kneels, and for a moment its eye is almost gold)', '#fff4d0', italic=True)])])
    return lines


def generate(G):
    RP.build(Sovereign, G, _abilities, lambda G_, X: G_.fn(f'{Sovereign.pfx}/enc/talk', ['function bm:p239/enc/joined']))   # (no encounter: its Eye comes from the ashes)
    # THE DREAD BOW TO IT: the Dread near it weakened while it's out
    G.FUNCS['loop/second'] += ['execute as @e[type=minecraft:wolf,tag=bm.xvpet,tag=!bm.ffpet] at @s run effect give @e[tag=bm.dread,distance=..10] minecraft:weakness 2 0 true']

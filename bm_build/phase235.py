"""2.97: THE DOODLES - five of the Gem of Creativity's makings, out of the drawn and written world of Kettle and Mr. Capshun (their
art: doodle_dragon_art, eraser_art, cursor_art, ink_blot_art, speech_bubble_art; the machinery is rigpet's, and rigface's for
the ones whose shape is a model). Normal mode, every one.

THE DOODLE DRAGON (Kettle's Dragon Drawing)   Kettle drew him in crayon, and the Gem made him real. Walk with Kettle and, now and then,
  his dragon climbs off the page - offer him a dye (crayons!) and he's yours. CLAW a foe within 2.4 (6). CRAYON FIRE a foe 2.5-8 off,
  every 4 s: a scribbled flame - 7 to each monster in it, set alight. STOMP two or more foes within 3.5, every 12 s (5, slowed).
  BIG BLAZE (charged, every minute): a long breath of crayon fire, twice through everything in front of him (8 each, alight). WARM
  out of a fight: Fire Resistance and Regeneration for you.
THE ERASER (The Eraser's Lucky Crumb)   the Gem's mistake: it can UNMAKE - and it knows it, and it's very sorry. Mr. Capshun is
  terrified of it. Walk with the Gem and you may find it hiding; offer it paper (a fresh start) and it comes along. RUB OUT a foe
  within 2.4 (6). BOUNCE two or more foes within 3.2, every 12 s: a hop and a belly-flop (7, slowed). UNMAKE (charged, every
  minute): it scrubs one monster nearly out of existence (8, then 12). TIDY UP out of a fight: your troubles rubbed out (poison,
  wither, slowness, weakness, fatigue, nausea, blindness, darkness, hunger) and Regeneration. Every blow LEAVES PINK CRUMBS behind:
  they lie on the ground a few seconds.
THE CURSOR (The Cursor's Mouse)   "the player's hand", out of the Glitched Cartridge: use a cartridge with nobody beside you and it
  slips out of the screen. CLICK a foe within 2.4 (6). SELECT a foe 3-10 off, every 4 s: it glows, weakened (3). DRAG two or more foes
  within 5, every 12 s: pulled in to it, slowed (4). LOADING... (charged, every minute): an hourglass - everything round it frozen,
  then 10 each. UNDO out of a fight: a little health back, and Regeneration.
THE INK BLOT (A Little Ink Pot)   spilled from Mr. Capshun's pen - a shapeshifter. Walk with Mr. Capshun and a blot may drip off his
  page; offer it an ink sac. PUNCH as a fist (7). QUILL SPIKE a foe 2.5-7 off, every 4 s (8). SPLASH two or more foes within 4, every
  10 s: ink in the eyes (4, blinded, slowed). INK SHIELD (charged, every minute): you and your followers Resistance II and Absorption;
  the monsters at your feet pushed off. WONDER out of a fight: Luck and Haste.
THE SPEECH BUBBLE (A Blank Caption Card)   Mr. Capshun's narration, come to life. Walk with Mr. Capshun and one may pop up beside
  him; offer it a book and quill. SHOUT a foe within 2.4: BAM! or POW! (6, knocked back). ALARM two or more foes within 10, every 15
  s: "!" - they glow, and you get Speed. KRAK! ZAP! (charged, every minute): it puffs itself up and blasts everything round it (8,
  then 6, knocked back). THINK out of a fight: "..." - Haste II and Luck for you (inspiration).
Every one of them: sitting, a wardrobe of three colours and the gilded / diamond / netherite looks, a rare aura, a shiny, the
Partner Wheel, a frame, a display case figure, Cecil's doll, the honours (Champion blow and Piercing Blow), a Raid Contract, and a
pair with Bender, Mr. Capshun, Henry and Nia."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import doodle_dragon_art as DA, eraser_art as EA, cursor_art as UA, ink_blot_art as IA, speech_bubble_art as SA
import rigpet as RP
import rigface as RF2
import phase141 as P141
import phase134 as P134

GEM = '#5ae0a0'
_MOVE = {0: None, 1: (16, [(0, 'walk_0'), (4, 'walk_1'), (8, 'walk_2'), (12, 'walk_3')]),
         2: (12, [(0, 'run_0'), (3, 'run_1'), (6, 'run_2'), (9, 'run_3')]), 3: (None, [(0, 'jump')]),
         10: (16, [(2 * i, f'swim_{i}') for i in range(8)])}
_DUR = {'idle_a': 20, 'idle_b': 16, 'idle_c': 16, 'idle_d': 16, 'idle_e': 16, 'walk_0': 4, 'walk_1': 4, 'walk_2': 4, 'walk_3': 4,
        'run_0': 3, 'run_1': 3, 'run_2': 3, 'run_3': 3, 'jump': 4, 'sit_a': 20, 'sit_b': 24, 'happy': 8, 'hurt': 3, 'tired': 12}


def cycle(idle, sit, happy, acts):
    """the cycles: idle (0), the moves, sit (4), happy (6), and the actions {state: frames}"""
    c = {k: v for k, v in _MOVE.items() if v}
    c.update({0: idle, 4: sit, 6: happy})
    c.update(acts)
    return c


def item_particle(model, at='~ ~0.6 ~', d='0.3 0.2 0.3', v=0.08, n=8):
    """a particle that's one of our own sprites (an item's model)"""
    return f'particle minecraft:item{{item:{{id:"minecraft:paper",components:{{"minecraft:item_model":"bm:{model}"}}}}}} {at} {d} {v} {n}'


# ---------------------------------------------------------------------------------------------------- the followers
class Dragon(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'dragon', 'The Doodle Dragon', '#5ac048', '#d4f4c8', 'p235d', 'dd', 'dz'
    A = RF2.art(DA)
    MENU, PET_HP, PET_CD, ITEM = 4600, 34, 120, 'doodle_drawing'
    pron, they = 'him', 'he'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious', 'roar', 'puff')
    FACE = {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'sad', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'happy', 'serious': 'fierce',
            'roar': 'roar', 'puff': 'puff'}
    ATTRS = dict(armor=4, attack_damage=5, movement_speed=0.38, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.8, (0.9, 1.4)
    SWAP = RF2.swapping(DA)
    SWAP_START = True
    CYCLE = cycle((240, [(0, 'idle_a'), (80, 'idle_b'), (160, 'idle_c'), (200, 'idle_a')]), (240, [(0, 'sit_a'), (120, 'sit_b')]),
                  (None, [(0, 'happy'), (8, 'flap_0'), (12, 'flap_1'), (16, 'flap_0'), (20, 'happy')]),
                  {7: (None, [(0, 'swipe_up'), (3, 'swipe')]), 8: (None, [(0, 'breathe_up'), (6, 'breathe'), (16, 'idle_a')]),
                   11: (None, [(0, 'stomp_up'), (5, 'stomp')]), 12: (None, [(0, 'breathe_up'), (8, 'breathe'), (26, 'happy')]),
                   14: (None, [(0, 'idle_c'), (20, 'happy')])})
    DUR = dict(_DUR, swipe_up=3, swipe=2, breathe_up=5, breathe=3, stomp_up=4, stomp=2, flap_0=3, flap_1=3)
    QUIPS = ['"RAWR! ...Did that sound scary? Kettle says it sounds scary."', '"Crayon fire is the BEST fire."', '(he hiccups a little puff of smoke)',
             '"I\'m a REAL dragon now. Real-ish."', '"Kettle drew my teeth extra pointy. On purpose."', '(he flaps his little wings very proudly)']
    HELLO = ('(the Doodle Dragon scrambles back to you, tail swinging)', '(a page flutters - and the Doodle Dragon climbs out of it) "RAWR! Hi!"',
             '(he folds himself back into a drawing, and is gone)')
    SIT = ('"Up! Up! Adventure!"', '(he curls up like a cat, tail over his nose)')
    FAINT = '"...the crayon... ran out..."'
    NOT_YOURS = '"You\'re not Kettle! ...You\'re not my friend\'s friend either."'
    POWERS = [('Claw', 'a foe within 2.4, every second: 6'),
              ('Crayon Fire', 'a foe 2.5-8 off, every 4 s: a big scribbled flame - 7 to every monster in it, and it sets them alight'),
              ('Stomp', 'two or more foes within 3.5, every 12 s: a sumo stomp - 5, and slowed'),
              ('Big Blaze', 'charged, every minute: a long breath of crayon fire, twice through everything in front of him (8 each, alight)'),
              ('Warm', 'out of a fight beside you, every minute: Fire Resistance and Regeneration for you')]
    INTRO = [T('The Doodle Dragon', '#5ac048', bold=True), T(' - Kettle drew him in crayon, and the Gem made him real. ', 'gray'),
             T('He breathes crayon fire. He is VERY proud of it.', 'white')]
    BUTTONS = ()
    BURST = [item_particle('dd_fx_smoke', '~ ~0.8 ~', '0.3 0.4 0.3', 0.02, 10), 'particle minecraft:poof ~ ~0.6 ~ 0.3 0.3 0.3 0.02 6']
    FADE_SOUND = 'playsound minecraft:item.book.page_turn neutral @a[distance=..20] ~ ~ ~ 1 0.8'
    SUMMON_EXTRA = ['playsound minecraft:entity.ender_dragon.ambient neutral @a[distance=..24] ~ ~ ~ 0.3 2.0']
    ENC_POSES = [(0, 'idle_a'), (30, 'idle_c'), (60, 'happy')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run ' + item_particle('dd_fx_smoke', '~ ~1.4 ~', '0.1 0.1 0.1', 0.01, 2)
    ADV = ('Here Be Dragons', 'Befriend the Doodle Dragon, Kettle\'s drawing')
    ADMIN_HINT = 'Walk with Kettle - now and then his dragon climbs off the page. Offer it a dye.'
    MEET_HINT = 'Walk with Kettle. Bring a dye (crayons!).'


class Eraser(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'eraser', 'The Eraser', '#f08aa0', '#fcdce4', 'p235e', 'ez', 'ea'
    A = RF2.art(EA)
    MENU, PET_HP, PET_CD, ITEM = 4650, 30, 120, 'eraser_crumb'
    pron, they = 'it', 'it'
    FACE = {'happy': 'happy', 'surprised': 'scared', 'hurt': 'wince', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'happy', 'serious': 'focus'}
    ATTRS = dict(armor=4, attack_damage=4, movement_speed=0.36, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.75, (0.8, 0.9)
    SWAP = RF2.swapping(EA)
    SWAP_START = True
    CYCLE = cycle((240, [(0, 'idle_a'), (80, 'idle_b'), (150, 'idle_a'), (200, 'idle_c')]), (240, [(0, 'sit_a'), (120, 'sit_b')]),
                  (None, [(0, 'happy')]),
                  {7: (None, [(0, 'rub_0'), (3, 'rub_1'), (6, 'rub_0')]), 11: (None, [(0, 'hop_up'), (4, 'hop'), (9, 'slam'), (16, 'wince')]),
                   12: (None, [(0, 'rub_0'), (3, 'rub_1'), (6, 'rub_0'), (9, 'rub_1'), (12, 'rub_0'), (15, 'rub_1'), (18, 'rub_0'), (22, 'wince'), (26, 'idle_c')]),
                   14: (None, [(0, 'idle_c'), (16, 'happy')]), 13: (None, [(0, 'hide')])})     # (13: hiding - how you find it)
    DUR = dict(_DUR, rub_0=2, rub_1=2, hop_up=3, hop=3, slam=2, wince=4, hide=4)
    QUIPS = ['"S-sorry! Sorry. Was that too much?"', '(it brushes off a few pink crumbs, embarrassed)', '"I only erase BAD things now. Promise."',
             '"Mr. Capshun still won\'t stand next to me..."', '"Oops. I mean - good job, me?"', '(it peeks out from behind your leg)']
    HELLO = ('(the Eraser hurries back to you, shedding a crumb or two)', '(a little pink eraser shuffles out from behind you) "H-hi. I\'m here."',
             '(it bows - "sorry!" - and rubs itself out of sight)')
    SIT = ('"Okay! I\'m ready. I think."', '(it sits down very carefully, so as not to erase anything)')
    FAINT = '"I\'m... all worn down..."'
    NOT_YOURS = '"S-sorry, I\'m somebody else\'s. Sorry!"'
    POWERS = [('Rub Out', 'a foe within 2.4, every second: 6 - and it leaves pink crumbs behind'),
              ('Bounce', 'two or more foes within 3.2, every 12 s: a hop and a belly-flop - 7, slowed'),
              ('Unmake', 'charged, every minute: it scrubs one monster nearly out of existence - 8, then 12. Mr. Capshun can\'t watch'),
              ('Tidy Up', 'out of a fight beside you, every 45 s: your troubles rubbed out (poison, wither, slowness, weakness, fatigue, nausea, blindness, darkness, hunger) and Regeneration')]
    INTRO = [T('The Eraser', '#f08aa0', bold=True), T(' - the Gem\'s mistake: it can unmake. ', 'gray'),
             T('It is very, very sorry about that, and it would like to help now.', 'white')]
    BUTTONS = ()
    BURST = [item_particle('er_crumb_i', '~ ~0.4 ~', '0.3 0.2 0.3', 0.08, 12), 'particle minecraft:poof ~ ~0.4 ~ 0.3 0.2 0.3 0.02 4']
    FADE_SOUND = 'playsound minecraft:item.brush.brushing.generic neutral @a[distance=..20] ~ ~ ~ 1 1.2'
    SUMMON_EXTRA = ['playsound minecraft:item.brush.brushing.sand neutral @a[distance=..24] ~ ~ ~ 1 1.4']
    ENC_POSES = [(0, 'hide'), (40, 'idle_b'), (60, 'hide')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run ' + item_particle('er_crumb_i', '~ ~0.2 ~', '0.2 0 0.2', 0.02, 2)
    ADV = ('A Clean Slate', 'Offer the Eraser a fresh start')
    ADMIN_HINT = 'Walk with the Gem of Creativity - its Eraser hides nearby, ashamed. Offer it paper.'
    MEET_HINT = 'Walk with the Gem of Creativity. Bring paper - a fresh start.'


class Cursor(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'cursor', 'The Cursor', '#cfe8ff', '#e8f4ff', 'p235c', 'ux', 'uq'
    A = RF2.art(UA)
    MENU, PET_HP, PET_CD, ITEM = 4700, 28, 120, 'cursor_mouse'
    pron, they = 'it', 'it'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious', 'glitch')
    FACE = {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'hurt', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'happy', 'serious': 'determined',
            'glitch': 'glitch'}
    ATTRS = dict(armor=3, attack_damage=4, movement_speed=0.42, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.7, (0.8, 1.6)
    SWAP = RF2.swapping(UA)
    SWAP_START = True
    CYCLE = cycle((240, [(0, 'idle_a'), (60, 'idle_b'), (90, 'idle_a'), (140, 'idle_c'), (180, 'idle_e'), (210, 'idle_a')]),
                  (240, [(0, 'sit_a'), (120, 'sit_b')]), (None, [(0, 'happy'), (8, 'wave_a'), (14, 'wave_b'), (20, 'wave_a')]),
                  {7: (None, [(0, 'click_up'), (4, 'click')]), 8: (None, [(0, 'select'), (10, 'idle_a')]),
                   11: (None, [(0, 'drag_0'), (5, 'drag_1')]), 12: (None, [(0, 'wait_0'), (8, 'wait_1'), (16, 'wait_0'), (24, 'wait_1'), (32, 'happy')]),
                   14: (None, [(0, 'wave_a'), (6, 'wave_b'), (12, 'wave_a'), (18, 'happy')])})
    DUR = dict(_DUR, click_up=3, click=2, select=4, drag_0=4, drag_1=4, wait_0=4, wait_1=4, wave_a=4, wave_b=4)
    QUIPS = ['"*click*"', '"Selected!"', '"Did you know you can right-click almost anything? I know. I\'m a hand."', '"Loading... just kidding."',
             '(it does a little double-click of joy)', '"Ctrl+Z! ...it didn\'t work. Real life is weird."']
    HELLO = ('(the Cursor glides back beside you)', '(the air flickers - and a little white pointer drops into place beside you) "Hello, player!"',
             '(the Cursor clicks itself shut and is gone)')
    SIT = ('"Ready! Point me at something."', '(it hovers down to rest, blinking slowly like a text cursor)')
    FAINT = '"Error... not... responding..."'
    NOT_YOURS = '"Access denied! ...Sorry. You\'re not my player."'
    POWERS = [('Click', 'a foe within 2.4, every second: 6'),
              ('Select', 'a foe 3-10 off, every 4 s: selected - it glows, and it\'s weakened (3)'),
              ('Drag', 'two or more foes within 5, every 12 s: dragged in to it, slowed (4)'),
              ('Loading...', 'charged, every minute: it turns into an hourglass - everything round it frozen, then 10 each'),
              ('Undo', 'out of a fight beside you, every minute: a little of your health back, and Regeneration')]
    INTRO = [T('The Cursor', '#f4f4f4', bold=True), T(' - "the player\'s hand", out of the Glitched Cartridge. ', 'gray'),
             T('It clicks, it drags, it selects. It would like to point at things for you.', 'white')]
    BUTTONS = ()
    BURST = ['particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.2 16', 'particle minecraft:dust{color:[1.0,1.0,1.0],scale:1.2} ~ ~1 ~ 0.3 0.4 0.3 0 10']
    FADE_SOUND = 'playsound minecraft:ui.button.click neutral @a[distance=..20] ~ ~ ~ 1 0.8'
    SUMMON_EXTRA = ['playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 1 1.6']
    ENC_POSES = [(0, 'idle_b'), (30, 'idle_a'), (60, 'idle_c')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.1 3'
    ADV = ('Player One', 'Take the hand that came out of the cartridge')
    ADMIN_HINT = 'Use a Glitched Cartridge with nobody beside you: the Cursor slips out of the screen.'
    MEET_HINT = 'A Glitched Cartridge, used with no one beside you.'


class InkBlot(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'inkblot', 'The Ink Blot', '#7a7aaa', '#c8c8dc', 'p235i', 'ib', 'iq'
    A = RF2.art(IA)
    MENU, PET_HP, PET_CD, ITEM = 4750, 30, 120, 'ink_pot'
    pron, they = 'it', 'it'
    FACE = {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'hurt', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'shy', 'serious': 'determined'}
    ATTRS = dict(armor=3, attack_damage=5, movement_speed=0.38, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.75, (0.8, 1.0)
    SWAP = RF2.swapping(IA)
    SWAP_START = True
    CYCLE = cycle((240, [(0, 'idle_a'), (60, 'idle_b'), (120, 'idle_c'), (170, 'idle_d'), (210, 'idle_a')]), (240, [(0, 'sit_a'), (120, 'sit_b')]),
                  (None, [(0, 'happy'), (8, 'wave_a'), (14, 'wave_b'), (20, 'wave_a')]),
                  {7: (None, [(0, 'punch_up'), (3, 'punch')]), 8: (None, [(0, 'spike_up'), (5, 'spike'), (12, 'idle_a')]),
                   11: (None, [(0, 'splash_up'), (4, 'splash')]), 12: (None, [(0, 'guard'), (10, 'guard_b'), (20, 'happy')]),
                   14: (None, [(0, 'wonder'), (10, 'wonder_b'), (20, 'happy')])})
    DUR = dict(_DUR, punch_up=3, punch=2, spike_up=4, spike=2, splash_up=3, splash=2, guard=4, guard_b=4, wonder=5, wonder_b=5, wave_a=4, wave_b=4)
    QUIPS = ['(it reshapes into a little thumbs-up)', '(a tiny "?" forms over its head, then pops)', '(it splats happily)', '(it holds a fist up, very proud)',
             '(it wobbles back into a blot and blinks at you)', '(it draws a little heart with its own ink, and it drips)']
    HELLO = ('(the Ink Blot slides back to you across the ground)', '(a drop of ink falls from nowhere - splat - and blinks up at you)',
             '(it soaks into the ground and is gone)')
    SIT = ('(it gathers itself back up into a blot)', '(it melts into a puddle with its eyes on top)')
    FAINT = '(it dries up into a little smudge)'
    NOT_YOURS = '(the blot shakes its head, rippling)'
    POWERS = [('Punch', 'a foe within 2.4, every second: a fist - 7'),
              ('Quill Spike', 'a foe 2.5-7 off, every 4 s: it sharpens into a pen nib - 8'),
              ('Splash', 'two or more foes within 4, every 10 s: ink in their eyes - 4, blinded and slowed'),
              ('Ink Shield', 'charged, every minute: it becomes a shield round you - Resistance II and Absorption for you and your followers, and the monsters at your feet pushed off'),
              ('Wonder', 'out of a fight beside you, every minute: a question mark - Luck and Haste for you')]
    INTRO = [T('The Ink Blot', '#7a7aaa', bold=True), T(' - spilled from Mr. Capshun\'s pen. ', 'gray'),
             T('It never says a word, and it never keeps one shape for long.', 'white')]
    BUTTONS = ()
    BURST = ['particle minecraft:squid_ink ~ ~0.5 ~ 0.3 0.3 0.3 0.02 14', 'particle minecraft:poof ~ ~0.4 ~ 0.2 0.2 0.2 0.02 4']
    FADE_SOUND = 'playsound minecraft:entity.slime.squish_small neutral @a[distance=..20] ~ ~ ~ 1 0.8'
    SUMMON_EXTRA = ['playsound minecraft:entity.slime.squish neutral @a[distance=..24] ~ ~ ~ 1 1.2']
    ENC_POSES = [(0, 'sit_b'), (30, 'idle_a'), (60, 'wonder')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:squid_ink ~ ~0.2 ~ 0.2 0 0.2 0.005 2'
    ADV = ('Blot on the Landscape', 'Take in the ink blot that fell off Mr. Capshun\'s page')
    ADMIN_HINT = 'Walk with Mr. Capshun - now and then his pen leaks. Offer the blot an ink sac.'
    MEET_HINT = 'Walk with Mr. Capshun. Bring an ink sac.'


class Speech(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'speech', 'The Speech Bubble', '#ffd060', '#ffe0a0', 'p235b', 'wb', 'wq'
    A = RF2.art(SA)
    MENU, PET_HP, PET_CD, ITEM = 4800, 28, 120, 'caption_card'
    pron, they = 'it', 'it'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious', 'shout', 'puff')
    FACE = {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'hurt', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'smug', 'serious': 'fierce',
            'shout': 'shout', 'puff': 'puff'}
    ATTRS = dict(armor=3, attack_damage=4, movement_speed=0.38, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.75, (0.8, 1.2)
    SWAP = RF2.swapping(SA)
    SWAP_START = True
    CYCLE = cycle((240, [(0, 'idle_a'), (60, 'idle_b'), (120, 'idle_c'), (170, 'idle_d'), (210, 'idle_a')]), (300, [(0, 'sit_a'), (100, 'sit_b'), (200, 'sleep')]),
                  (None, [(0, 'happy')]),
                  {7: (None, [(0, 'shout_up'), (3, 'shout')]), 9: (None, [(0, 'shout_up'), (3, 'shout_b')]), 11: (None, [(0, 'alarm')]),
                   12: (None, [(0, 'puff_up'), (6, 'puff_b'), (12, 'blast'), (23, 'blast_b'), (30, 'happy')]),
                   14: (None, [(0, 'think'), (20, 'happy')]), 13: (None, [(0, 'awkward')])})
    DUR = dict(_DUR, shout_up=3, shout=2, shout_b=2, alarm=3, puff_up=4, puff_b=4, blast=2, blast_b=2, think=6, sleep=20, awkward=6)
    QUIPS = ['"BAM!"', '"POW! ...was that a good one? That was a good one."', '"And our hero struck true!"', '"*dramatic pause*"',
             '"KA-BLAM! ...okay, I\'m done. KA-BLAM! Now I\'m done."', '"Tell me I\'m not the best sound effect you\'ve ever heard."']
    HELLO = ('(the Speech Bubble hops back beside you: "Present!")', '(a speech bubble pops up out of thin air) "MEANWHILE... I\'m here!"',
             '"To be continued..." (it pops)')
    SIT = ('"Next panel!"', '(it settles down and lets a thought cloud drift up: "...")')
    FAINT = '"...the end..."'
    NOT_YOURS = '"Sorry, pal, I\'m in somebody else\'s comic."'
    POWERS = [('Shout', 'a foe within 2.4, every second: BAM! or POW! - 6, knocked back'),
              ('Alarm', 'two or more foes within 10, every 15 s: "!" - they glow, and you get Speed'),
              ('KRAK! ZAP!', 'charged, every minute: it puffs itself up and blasts everything round it - 8, then 6, knocked back'),
              ('Think', 'out of a fight beside you, every minute: "..." - Haste II and Luck for you. Inspiration!')]
    INTRO = [T('The Speech Bubble', '#ffd060', bold=True), T(' - Mr. Capshun\'s narration, come to life. ', 'gray'),
             T('It fights in sound effects. LOUD ones.', 'white')]
    BUTTONS = ()
    BURST = ['particle minecraft:end_rod ~ ~0.8 ~ 0.3 0.4 0.3 0.02 8', 'particle minecraft:poof ~ ~0.6 ~ 0.3 0.3 0.3 0.02 6']
    FADE_SOUND = 'playsound minecraft:entity.chicken.egg neutral @a[distance=..20] ~ ~ ~ 1 1.4'
    SUMMON_EXTRA = ['playsound minecraft:block.note_block.pling neutral @a[distance=..24] ~ ~ ~ 1 1.6']
    ENC_POSES = [(0, 'idle_c'), (30, 'idle_a'), (60, 'awkward')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:end_rod ~ ~1.2 ~ 0.2 0.2 0.2 0.01 2'
    ADV = ('Speech! Speech!', 'Give Mr. Capshun\'s narration something to say')
    ADMIN_HINT = 'Walk with Mr. Capshun - now and then his narration pops up beside him. Offer it a book and quill.'
    MEET_HINT = 'Walk with Mr. Capshun. Bring a book and quill.'


DOODLES = (Dragon, Eraser, Cursor, InkBlot, Speech)
FACE_PART = {'dragon': 'head', 'eraser': 'body', 'cursor': 'body', 'inkblot': 'head', 'speech': 'face'}
for _C in DOODLES:
    RP.register(_C)
    RF2.setup(_C, FACE_PART[_C.W])

_ITEMS = {'dragon': ("Kettle's Dragon Drawing", ['A page of crayon: a green dragon with purple wings and a big toothy grin.',
                                                 'Signed in the corner, in big wobbly letters: KETTLE.', 'Now and then it smells of smoke.']),
          'eraser': ("The Eraser's Lucky Crumb", ['A little pink crumb, rubbed off an eraser.', 'It feels sorry for something.']),
          'cursor': ("The Cursor's Mouse", ['An old computer mouse, its cable cut. When you hold it,', 'something white and pointy follows your hand.']),
          'inkblot': ('A Little Ink Pot', ['A pot of Mr. Capshun\'s ink. It\'s never quite still.', 'Sometimes it makes a little "?" on its own.']),
          'speech': ('A Blank Caption Card', ['A white card with a pointy tail, waiting for words.', 'Hold it up and it says "!"'])}
_DOLL = {'dragon': 'A doll of the Doodle Dragon - crayon green, wings and all.', 'eraser': 'A doll of the Eraser - pink, worried, very soft.',
         'cursor': 'A doll of the Cursor - a little white pointer with a smile.', 'inkblot': 'A doll of the Ink Blot - a soft black blot with big eyes.',
         'speech': 'A doll of the Speech Bubble - it says "BAM!" when you squeeze it.'}
# (each figure's extent, measured: phase134.measure)
FIT = {'dragon': (-0.015, 1.610, -0.950, 0.950, -0.095, 0.051), 'eraser': (0.000, 0.744, -0.350, 0.349, -0.140, 0.231),
       'cursor': (0.638, 0.897, -0.319, 0.228, -0.031, 0.031), 'inkblot': (-0.017, 1.138, -0.588, 0.550, -0.011, 0.013),
       'speech': (-0.046, 1.408, -0.658, 0.656, -0.045, 0.051)}
for _C in DOODLES:
    _w = _C.W
    nm, desc = _ITEMS[_w]
    item(_C.ITEM, TOTEM, nm, _C.COL, desc + [('One of the Gem of Creativity\'s makings.', GEM),
                                                                                    (f'Use: call {_C.pron} (again: call {_C.pron} over).', 'blue'),
                                                                                    (f'Sneak + use: {RP.POS[_C.pron]} menu.', 'blue'),
                                                                                    (f'If {_C.they} faint{"s" if _C.they != "they" else ""}: 2 minutes before {_C.they} can return.', 'gray')],
         model=f'bm:{_C.ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
    item(f'doll_{_w}', TOTEM, f'{_C.NAME[4:]} Doll', _C.COL,
         [_DOLL[_w], ('Right-click a block: set it down.', 'blue'), ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
         model=f'bm:doll_{_w}', stack=16, cat='fun', comps=hold('none'))
    HOLD[f'doll_{_w}'] = f'bm:p141/doll_{_w}/use'
    P141.DOLLS.append((f'doll_{_w}', _C.NAME, _C.COL, _DOLL[_w], 'minecraft:end_rod', 'minecraft:item.book.page_turn', 'minecraft:poof'))
    P141.DOLL_FROM[f'doll_{_w}'] = (_C.ITEM, {'kh': 1.55, 'kb': 0.82, 'kl': 0.62, **_C.DOLL_GROUPS} if hasattr(_C, 'DOLL_GROUPS') else {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
    P134.FIT[_C.ITEM] = FIT[_w]

# ---- their pairs with the everyone-partners: Bender and Mr. Capshun (Henry's and Nia's come from cat_bonds)
import phase100 as P100
import phase188 as P188
_O = P188.O
P188.VNAME.update({'dragon': 'the Doodle Dragon', 'eraser': 'the Eraser', 'cursor': 'the Cursor', 'inkblot': 'the Ink Blot', 'speech': 'the Speech Bubble'})
_eff = lambda *es: [f'effect give {_O} minecraft:{e} {15 if e == "night_vision" else 3} {a} true' for e, a in es]
P188.PAIRS.update({
    'dd_bender': ('dragon', 'bender', 'Dragon Fetch', '#e0a860', 'The Doodle Dragon and Bender - a dog who would like, very much, to fetch a dragon',
                  _eff(('speed', 0), ('fire_resistance', 0)),
                  [('bender', '(sniffs the dragon. Smells like crayons. Wags.)'), ('dragon', '"Fetch? I can fetch! Watch me fetch!"')],
                  [('dragon', '"RAWR!" (a puff of crayon smoke)', 'bender', '(barks at the smoke, delighted)')]),
    'dd_capshun': ('dragon', 'capshun', 'Here Be Dragons', '#f0f0f0', 'The Doodle Dragon and Mr. Capshun - two drawings, one of them very fiery',
                   _eff(('strength', 0), ('fire_resistance', 0)),
                   [('capshun', '[Mr. Capshun narrates: "And from the margins of the page - a DRAGON."]'), ('dragon', '"That\'s me! Say it again!"')],
                   [('dragon', '"Am I drawn better than you?"', 'capshun', '[Mr. Capshun narrates: "He was drawn in crayon. Mr. Capshun said nothing."]')]),
    'er_bender': ('eraser', 'bender', 'Chew Toy', '#e0a860', 'The Eraser and Bender - it squeaks, he\'s very interested',
                  _eff(('speed', 0), ('regeneration', 0)),
                  [('bender', '(play-bows at the Eraser. It looks squeaky.)'), ('eraser', '"P-please don\'t chew me. ...Okay, a little."')],
                  [('bender', '(licks the Eraser; comes away with a pink tongue)', 'eraser', '"Sorry! Sorry. That\'s just my crumbs."')]),
    'er_capshun': ('eraser', 'capshun', 'Mortal Terror', '#f0f0f0', 'The Eraser and Mr. Capshun - a stick figure walking beside the one thing that can unmake him',
                   _eff(('resistance', 0), ('speed', 1)),
                   [('capshun', '[Mr. Capshun narrates: "He did NOT like where this was going."]'), ('eraser', '"I\'d never erase you! I promise! ...I\'ll stand over here."')],
                   [('eraser', '"Mr. Capshun? Want a hug?"', 'capshun', '[Mr. Capshun narrates: "He did not want a hug. He ran."]')]),
    'cu_bender': ('cursor', 'bender', 'Laser Pointer', '#e0a860', 'The Cursor and Bender - it moves, so he chases it. Forever',
                  _eff(('speed', 1),),
                  [('cursor', '"Hey, Bender. Watch the pointer."'), ('bender', '(watches the pointer with his ENTIRE soul)')],
                  [('cursor', '(zips left; zips right)', 'bender', '(zips left; zips right; falls over; is happy)')]),
    'cu_capshun': ('cursor', 'capshun', 'Point and Click', '#f0f0f0', 'The Cursor and Mr. Capshun - a narrator meets the hand that turns the page',
                   _eff(('haste', 0), ('luck', 0)),
                   [('capshun', '[Mr. Capshun narrates: "The Hand of the Player itself!"]'), ('cursor', '"*click* Hi! Can I select you?"')],
                   [('cursor', '"Right-click: Mr. Capshun."', 'capshun', '[Mr. Capshun narrates: "Mr. Capshun had no context menu. He was hurt."]')]),
    'ib_bender': ('inkblot', 'bender', 'Ink Paws', '#e0a860', 'The Ink Blot and Bender - he stepped in it. Now there are inky paw prints everywhere',
                  _eff(('speed', 0), ('jump_boost', 0)),
                  [('bender', '(steps in the Ink Blot. Looks at his paw. Wags.)'), ('inkblot', '(reshapes into a little paw print)')],
                  [('inkblot', '(turns into a ball)', 'bender', '(FETCHES the Ink Blot. It does not mind.)')]),
    'ib_capshun': ('inkblot', 'capshun', 'Back to the Pen', '#f0f0f0', 'The Ink Blot and Mr. Capshun - the blot that fell off his page, home again',
                   _eff(('haste', 0), ('resistance', 0)),
                   [('capshun', '[Mr. Capshun narrates: "His own ink. Spilled, and - somehow - alive."]'), ('inkblot', '(it forms a little heart)')],
                   [('inkblot', '(turns into a quill and points at him)', 'capshun', '[Mr. Capshun narrates: "Did his own ink just... make a pun?"]')]),
    'sb_bender': ('speech', 'bender', 'WOOF!', '#e0a860', 'The Speech Bubble and Bender - every bark gets a caption',
                  _eff(('strength', 0), ('speed', 0)),
                  [('bender', '(barks)'), ('speech', '"WOOF! ...that\'s his line. I just wrote it big."')],
                  [('bender', '(barks twice)', 'speech', '"WOOF WOOF! He says you\'re the best!"')]),
    'sb_capshun': ('speech', 'capshun', 'The Narrator and the Narration', '#f0f0f0', 'The Speech Bubble and Mr. Capshun - he talks, it gets LOUD',
                   _eff(('strength', 0), ('haste', 0)),
                   [('capshun', '[Mr. Capshun narrates: "Our heroes walked on."]'), ('speech', '"OUR HEROES WALKED ON!!"')],
                   [('capshun', '[Mr. Capshun narrates: "Quietly."]', 'speech', '"...quietly."')]),
})
P188.ICON.update({'dd_bender': 'bm:doodle_drawing', 'dd_capshun': 'bm:doodle_drawing', 'er_bender': 'bm:eraser_crumb', 'er_capshun': 'bm:eraser_crumb',
                  'cu_bender': 'bm:cursor_mouse', 'cu_capshun': 'bm:cursor_mouse', 'ib_bender': 'bm:ink_pot', 'ib_capshun': 'bm:ink_pot',
                  'sb_bender': 'bm:caption_card', 'sb_capshun': 'bm:caption_card'})


def extend_offers(O, offer):
    pass


# ---------------------------------------------------------------------------------------------------- icons (16 x 16, by hand)
def _icon(w):
    from PIL import Image, ImageDraw
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if w == 'dragon':                                  # a page with a green crayon dragon
        d.rectangle((1, 1, 14, 14), fill=(250, 246, 232, 255), outline=(190, 180, 150, 255))
        d.ellipse((4, 6, 10, 12), fill=(90, 190, 70, 255)); d.ellipse((8, 3, 12, 7), fill=(90, 190, 70, 255))
        d.polygon([(4, 7), (2, 4), (6, 6)], fill=(150, 90, 200, 255)); d.point((10, 4), fill=(20, 20, 20, 255))
        d.line((12, 5, 14, 4), fill=(240, 120, 40, 255)); d.line((12, 6, 14, 7), fill=(250, 210, 60, 255))
    elif w == 'eraser':                                # a pink crumb, a bit worn
        d.polygon([(4, 9), (8, 5), (12, 8), (9, 12)], fill=(240, 140, 160, 255), outline=(170, 80, 100, 255))
        d.line((5, 9, 8, 6), fill=(255, 200, 210, 255)); d.point((9, 10), fill=(120, 120, 130, 255))
        d.point((3, 12), fill=(240, 140, 160, 255)); d.point((13, 11), fill=(240, 140, 160, 255))
    elif w == 'cursor':                                # an old mouse, a cut cable
        d.ellipse((4, 4, 11, 14), fill=(232, 232, 236, 255), outline=(110, 110, 120, 255))
        d.line((7, 4, 7, 8), fill=(110, 110, 120, 255)); d.line((4, 8, 11, 8), fill=(110, 110, 120, 255))
        d.line((7, 4, 7, 1), fill=(60, 60, 70, 255)); d.point((8, 1), fill=(60, 60, 70, 255))
    elif w == 'inkblot':                               # a little ink pot
        d.rectangle((4, 7, 11, 14), fill=(40, 40, 56, 255), outline=(15, 15, 20, 255)); d.rectangle((6, 4, 9, 7), fill=(90, 90, 110, 255))
        d.point((5, 8), fill=(140, 140, 170, 255)); d.ellipse((10, 11, 14, 14), fill=(20, 20, 28, 255))
    else:                                              # a blank caption card with a tail
        d.ellipse((1, 1, 14, 11), fill=(250, 250, 250, 255), outline=(20, 20, 20, 255))
        d.polygon([(4, 10), (3, 15), (8, 10)], fill=(250, 250, 250, 255), outline=(20, 20, 20, 255)); d.line((4, 10, 8, 10), fill=(250, 250, 250, 255))
        d.line((7, 3, 7, 6), fill=(220, 40, 40, 255)); d.point((7, 8), fill=(220, 40, 40, 255))
    return im.resize((32, 32), 0)


def _crumb():
    """(the Eraser's pink crumbs: a particle, and a scatter left on the ground)"""
    import eraser_art as E
    return E.textures()['er_crumb_bit']


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for _C in DOODLES:
        RP.rp(_C, R, _icon(_C.W))
        RF2.faces(_C, FACE_PART[_C.W], R)
    R.ICONS['er_crumb_i'] = _crumb()


def textures():
    T_ = {}
    for A in (DA, EA, UA, IA, SA):
        T_.update(A.textures())
    return T_


def generate_early(G):
    for _C in DOODLES:
        RP.contract(_C, G)


# ---------------------------------------------------------------------------------------------------- the abilities: one shape, each their own
CDO = {'charged': 'gc', 'support': 'sc', 'crowd': 'k2', 'melee': 'mc', 'ranged': 'rc', 'kind': 'k', 'melee2': 'mc'}


def kit(G, X, K):
    """K: {event: dict(st (state), x (ticks), at (tick(s) left when it lands: int or list), cd, face, go (extra lines on the go),
    and how it's started: reach (melee), near/far (ranged), r/n (crowd: n foes within r), r (charged), during ((lo, hi): a tick
    function while it runs)}. Writes {pfx}/<event>_go and act_tick; the follower writes {pfx}/<event> (and <event>2 for a
    second landing, <event>_tick for during). Returns the tick lines."""
    fn, S, go, foe, pfx, idle, face = G.fn, X.S, X.go, X.foe, X.pfx, X.idle_fight, X.face
    lines = [f'execute if score @s {S("k")} matches 1.. run scoreboard players remove @s {S("k")} 1',
             f'execute if score @s {S("k2")} matches 1.. run scoreboard players remove @s {S("k2")} 1']
    fn(f'{pfx}/near_owner', ['execute on owner if entity @s[distance=..8] run return 1', 'return 0'])
    acts = [f'scoreboard players remove @s {S("x")} 1']
    for ev in ('charged', 'support', 'crowd', 'melee', 'ranged', 'kind'):
        if ev not in K:
            continue
        k, cdo = K[ev], CDO[ev]
        if ev == 'charged':
            cond = f'if entity @e[{foe},distance=..{k["r"]}]'
        elif ev == 'support':
            cond = f'if entity @e[{foe},distance=..12] if function bm:p235/owner_hurt'
        elif ev == 'crowd':
            lines.append(f'execute store result score #nf bm.rng if entity @e[{foe},distance=..{k["r"]}]')
            cond = f'if score #nf bm.rng matches {k.get("n", 2)}..'
        elif ev == 'melee':
            cond = f'if entity @e[{foe},distance=..{k["reach"]}]'
        elif ev == 'ranged':
            cond = f'unless entity @e[{foe},distance=..{k["near"]}] if entity @e[{foe},distance=..{k["far"]}]'
        else:
            cond = f'unless entity @e[{foe},distance=..12] if function bm:{pfx}/near_owner'
        lines.append(f'execute {idle} unless score @s {S(cdo)} matches 1.. {cond} run function bm:{pfx}/{ev}_go')
        alt = k.get('alt')                                         # (a second version of the move, one time in two: its own state)
        g = go(k['st'], k['x'], cdo, k['cd'], (face(k['face'], k['x']) if k.get('face') else []) + list(k.get('go', ())))
        if alt:
            fn(f'{pfx}/{ev}_go', ['execute store result score #r bm.rng run random value 1..2',
                                  f'execute if score #r bm.rng matches 2 run return run function bm:{pfx}/{ev}_go2'] + g)
            fn(f'{pfx}/{ev}_go2', go(alt, k['x'], cdo, k['cd'], (face(k['face'], k['x']) if k.get('face') else []) + list(k.get('go', ()))))
        else:
            fn(f'{pfx}/{ev}_go', g)
        ats = k['at'] if isinstance(k['at'], (list, tuple)) else [k['at']]
        for st in [k['st']] + ([alt] if alt else []):
            for i, at in enumerate(ats):
                acts.append(f'execute if score @s {S("a")} matches {st} if score @s {S("x")} matches {at} run function bm:{pfx}/{ev}{i + 1 if i else ""}')
            if k.get('during'):
                lo, hi = k['during']
                acts.append(f'execute if score @s {S("a")} matches {st} if score @s {S("x")} matches {lo}..{hi} run function bm:{pfx}/{ev}_tick')
    fn(f'{pfx}/act_tick', acts)
    return lines


def melee(G, X, d, reach, fx, snd, extra_at_foe=()):
    """{pfx}/melee: d to the nearest foe within reach; fx at it"""
    fn, foe, pfx = G.fn, X.foe, X.pfx
    fn(f'{pfx}/melee', X.hit(d) + [f'execute as @e[{foe},distance=..{reach + 0.4},sort=nearest,limit=1] at @s run function bm:{pfx}/meleed'] + X.end)
    fn(f'{pfx}/meleed', [f'function bm:{pfx}/hurt'] + list(fx) + [f'playsound {snd} neutral @a[distance=..16] ~ ~ ~ 0.8 1.2'] + list(extra_at_foe))


def _crumbs(at='~ ~0.6 ~', n=10):
    """the Eraser's PINK CRUMBS: a shower of them (our own crumb sprite, and pink dust)"""
    return [item_particle('er_crumb_i', at, '0.3 0.25 0.3', 0.1, n), f'particle minecraft:dust{{color:[1.0,0.62,0.7],scale:0.6}} {at} 0.3 0.2 0.3 0 {n // 2}']


def _dragon(G, X):
    fn, pfx, foe, face = G.fn, X.pfx, X.foe, X.face
    K = dict(melee=dict(st=7, x=6, at=3, cd=20, reach=2.4, go=['playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.4 1.6']),
             ranged=dict(st=8, x=18, at=12, cd=80, near=2.5, far=8, face='roar', during=(5, 13),
                         go=['playsound minecraft:entity.blaze.shoot neutral @a[distance=..16] ~ ~ ~ 0.6 1.4']),
             crowd=dict(st=11, x=12, at=7, cd=240, r=3.5, face='serious'),
             charged=dict(st=12, x=30, at=[22, 11], cd=1200, r=7, face='roar', during=(5, 22),
                          go=['playsound minecraft:entity.ender_dragon.growl neutral @a[distance=..24] ~ ~ ~ 0.5 1.8']),
             kind=dict(st=14, x=24, at=12, cd=1200, face='happy'))
    lines = kit(G, X, K)
    melee(G, X, 6, 2.4, ['particle minecraft:sweep_attack ~ ~0.8 ~ 0.1 0.1 0.1 0 1', 'particle minecraft:dust{color:[0.9,0.2,0.2],scale:1.0} ~ ~0.9 ~ 0.3 0.3 0.3 0 6'],
          'minecraft:entity.player.attack.sweep')
    # CRAYON FIRE: a scribbled cone of it (our crayon flame sprite, and fire), aimed at the nearest monster; what's in it burns
    tgt = f'@e[{foe},distance=..12,sort=nearest,limit=1]'
    fire = lambda d: [item_particle('dd_fx_fire', f'^ ^ ^{d}', f'{0.12 * d:.2f} {0.1 * d:.2f} {0.12 * d:.2f}', 0.02, 2 + d),
                      f'particle minecraft:dust{{color:[1.0,0.45,0.1],scale:1.3}} ^ ^ ^{d} {0.12 * d:.2f} {0.1 * d:.2f} {0.12 * d:.2f} 0 {1 + d // 2}',
                      f'particle minecraft:dust{{color:[1.0,0.85,0.2],scale:1.0}} ^ ^ ^{d} {0.12 * d:.2f} {0.1 * d:.2f} {0.12 * d:.2f} 0 {1 + d // 2}']
    fn(f'{pfx}/breath_fx', ['execute if entity ' + tgt + f' facing entity {tgt} eyes positioned ^ ^1.1 ^0.6 run function bm:{pfx}/breath_cone',
                            f'execute unless entity {tgt} rotated as @s rotated ~ 10 positioned ^ ^1.1 ^0.6 run function bm:{pfx}/breath_cone'])
    fn(f'{pfx}/breath_cone', [l for d in (1, 2, 3, 4, 5, 6) for l in fire(d)] + ['particle minecraft:flame ^ ^ ^2 0.3 0.2 0.3 0.04 4'])
    fn(f'{pfx}/ranged_tick', [f'function bm:{pfx}/breath_fx'])
    fn(f'{pfx}/charged_tick', [f'function bm:{pfx}/breath_fx', f'execute if score @s {X.S("x")} matches 14 run playsound minecraft:entity.blaze.shoot neutral @a[distance=..16] ~ ~ ~ 0.8 1.1'])
    burn = lambda d, secs, reach: X.hit(d) + [f'execute if entity {tgt} facing entity {tgt} feet run function bm:{pfx}/burn_{reach}', f'tag @e[tag=bm.ddburnt] remove bm.ddburnt'] + X.end
    for reach, secs in ((8, 4), (10, 6)):
        fn(f'{pfx}/burn_{reach}', [f'execute positioned ^ ^ ^{k} as @e[{foe},tag=!bm.ddburnt,distance=..{1.4 + 0.25 * k:.2f}] at @s run function bm:{pfx}/burnt_{secs}'
                                   for k in range(1, reach + 1, 2)])
        fn(f'{pfx}/burnt_{secs}', ['tag @s add bm.ddburnt', f'function bm:{pfx}/hurt', f'data merge entity @s {{Fire:{secs * 20}s}}',
                                   'particle minecraft:flame ~ ~0.8 ~ 0.3 0.4 0.3 0.02 6'])
    fn(f'{pfx}/ranged', burn(7, 4, 8))
    fn(f'{pfx}/charged', burn(8, 6, 10))
    fn(f'{pfx}/charged2', burn(8, 6, 10))
    fn(f'{pfx}/crowd', X.hit(5) + [f'execute as @e[{foe},distance=..3.5] at @s run function bm:{pfx}/stomped', 'particle minecraft:poof ~ ~0.1 ~ 1.2 0.05 1.2 0.05 20',
                                   'playsound minecraft:entity.generic.explode neutral @a[distance=..16] ~ ~ ~ 0.4 1.6'] + X.end)
    fn(f'{pfx}/stomped', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 1', 'particle minecraft:dust{color:[0.6,0.4,0.25],scale:1.2} ~ ~0.1 ~ 0.3 0.05 0.3 0 6'])
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p235d/warm_you'])
    fn('p235d/warm_you', ['effect give @s minecraft:fire_resistance 60 0 true', 'effect give @s minecraft:regeneration 10 0 true',
                          item_particle('dd_fx_fire', '~ ~1 ~', '0.4 0.4 0.4', 0.02, 6), 'playsound minecraft:block.fire.ambient player @s ~ ~ ~ 1 1.4'])
    return lines


def _eraser(G, X):
    fn, pfx, foe = G.fn, X.pfx, X.foe
    K = dict(melee=dict(st=7, x=9, at=5, cd=20, reach=2.4),
             crowd=dict(st=11, x=18, at=9, cd=240, r=3.2, face='serious', go=['playsound minecraft:entity.slime.jump neutral @a[distance=..16] ~ ~ ~ 0.8 1.4']),
             charged=dict(st=12, x=30, at=[22, 11], cd=1200, r=3.5, face='serious'),
             kind=dict(st=14, x=24, at=12, cd=900, face='happy'))
    lines = kit(G, X, K)
    # PINK CRUMBS: a shower at every blow - and a little scatter left lying on the ground (ez/crumbs: gone after 6 s)
    leave = ['execute if entity @e[type=minecraft:item_display,tag=bm.ezcrumb,distance=..1.2] run return 0',
             'summon minecraft:item_display ~ ~0.02 ~ {Tags:["bm.ezcrumb","bm.ezcnew"],item_display:"fixed",item:{id:"minecraft:paper",count:1,'
             'components:{"minecraft:item_model":"bm:er_crumb_i"}},transformation:{left_rotation:[-0.7071f,0f,0f,0.7071f],right_rotation:[0f,0f,0f,1f],'
             'translation:[0f,0f,0f],scale:[0.55f,0.55f,0.55f]}}',
             'execute store result entity @e[type=minecraft:item_display,tag=bm.ezcnew,limit=1,sort=nearest] Rotation[0] float 1 run random value 0..359',
             'scoreboard players set @e[type=minecraft:item_display,tag=bm.ezcnew,limit=1,sort=nearest] bm.eal 120',
             'tag @e[type=minecraft:item_display,tag=bm.ezcnew] remove bm.ezcnew']
    fn('p235e/crumbs', _crumbs() + ['execute positioned over motion_blocking run function bm:p235e/leave'])
    fn('p235e/leave', leave)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.eal dummy']
    G.OBJECTIVES += ['bm.eal']
    X.tick += ['scoreboard players remove @e[type=minecraft:item_display,tag=bm.ezcrumb] bm.eal 1',
               'kill @e[type=minecraft:item_display,tag=bm.ezcrumb,scores={bm.eal=..0}]']
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.ezcrumb]')
    melee(G, X, 6, 2.4, ['function bm:p235e/crumbs'], 'minecraft:item.brush.brushing.generic')
    fn(f'{pfx}/crowd', X.hit(7) + [f'execute as @e[{foe},distance=..3.2] at @s run function bm:{pfx}/flopped', 'particle minecraft:poof ~ ~0.1 ~ 1.0 0.05 1.0 0.05 16',
                                   'playsound minecraft:entity.slime.squish neutral @a[distance=..16] ~ ~ ~ 1 0.8'] + _crumbs('~ ~0.3 ~', 14) + X.end)
    fn(f'{pfx}/flopped', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 1', 'function bm:p235e/crumbs'])
    # UNMAKE: one monster, scrubbed (8, then 12) - and Mr. Capshun, if he's with you, can't watch
    tg = f'@e[{foe},distance=..4,sort=nearest,limit=1]'
    for i, d in ((0, 8), (1, 12)):
        fn(f'{pfx}/charged{i + 1 if i else ""}', X.hit(d) + [f'execute as {tg} at @s run function bm:{pfx}/unmade'] + X.end +
           (['scoreboard players operation #me bm.pid = @s bm.pid',
             'execute as @e[type=minecraft:wolf,tag=bm.mzpet,distance=..16] if score @s bm.pid = #me bm.pid on owner if entity @s[tag=!bm.hush] run ' +
             X.title('@s', 'actionbar', [T('Mr. Capshun: ', '#f0f0f0', bold=True), T('[Mr. Capshun narrates: "He could not look. He looked anyway. He wished he hadn\'t."]', '#e0e0e0')])] if i else []))
    fn(f'{pfx}/unmade', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:weakness 6 1', 'effect give @s minecraft:slowness 3 2', 'function bm:p235e/crumbs',
                         'particle minecraft:white_ash ~ ~1 ~ 0.4 0.6 0.4 0 30', 'playsound minecraft:item.brush.brushing.sand neutral @a[distance=..16] ~ ~ ~ 1 0.7'])
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p235e/tidy_you'])
    fn('p235e/tidy_you', [f'effect clear @s minecraft:{e}' for e in ('poison', 'wither', 'slowness', 'weakness', 'mining_fatigue', 'nausea', 'blindness', 'darkness', 'hunger')] +
       ['effect give @s minecraft:regeneration 6 0 true'] + _crumbs('~ ~1 ~', 8) + ['playsound minecraft:item.brush.brushing.generic player @s ~ ~ ~ 1 1.4'])
    return lines


def _cursor(G, X):
    fn, pfx, foe = G.fn, X.pfx, X.foe
    K = dict(melee=dict(st=7, x=8, at=4, cd=20, reach=2.4),
             ranged=dict(st=8, x=12, at=8, cd=80, near=3, far=10, face='serious'),
             crowd=dict(st=11, x=12, at=6, cd=240, r=5, face='serious'),
             charged=dict(st=12, x=36, at=[33, 8], cd=1200, r=7, face='glitch', go=['playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 1 0.5']),
             kind=dict(st=14, x=24, at=12, cd=1200, face='happy'))
    lines = kit(G, X, K)
    click = 'playsound minecraft:ui.button.click neutral @a[distance=..16] ~ ~ ~ 0.8 1.4'
    melee(G, X, 6, 2.4, ['particle minecraft:enchanted_hit ~ ~1 ~ 0.2 0.3 0.2 0.2 8', 'particle minecraft:dust{color:[1.0,0.85,0.2],scale:0.9} ~ ~1.2 ~ 0.2 0.2 0.2 0 6'],
          'minecraft:ui.button.click')
    tg = f'@e[{foe},distance=..10,sort=nearest,limit=1]'
    fn(f'{pfx}/ranged', X.hit(3) + [f'execute as {tg} at @s run function bm:{pfx}/selected', click] + X.end)
    fn(f'{pfx}/selected', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:glowing 6 0', 'effect give @s minecraft:weakness 6 0',
                           'particle minecraft:dust{color:[0.3,0.6,1.0],scale:1.0} ~ ~1 ~ 0.4 0.6 0.4 0 16'])
    fn(f'{pfx}/crowd', X.hit(4) + [f'execute as @e[{foe},distance=..5] at @s run function bm:{pfx}/dragged', 'playsound minecraft:block.note_block.bit neutral @a[distance=..16] ~ ~ ~ 1 1.2'] + X.end)
    fn(f'{pfx}/dragged', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 1',
                          f'execute facing entity @e[type=minecraft:wolf,tag={X.me},limit=1] feet positioned ^ ^ ^1.5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~',
                          'particle minecraft:dust{color:[0.9,0.9,0.9],scale:0.8} ~ ~1 ~ 0.3 0.4 0.3 0 8'])
    # LOADING...: frozen (an hourglass over them), then 10 each as it finishes
    fn(f'{pfx}/charged', [f'execute as @e[{foe},distance=..7] at @s run function bm:{pfx}/frozen', 'playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 1 0.5'])
    fn(f'{pfx}/frozen', ['effect give @s minecraft:slowness 2 9', 'effect give @s minecraft:weakness 2 2', 'particle minecraft:dust{color:[1.0,0.8,0.3],scale:1.0} ~ ~2.2 ~ 0.1 0.2 0.1 0 6'])
    fn(f'{pfx}/charged2', X.hit(10) + [f'execute as @e[{foe},distance=..8] at @s run function bm:{pfx}/loaded', 'playsound minecraft:entity.player.levelup neutral @a[distance=..16] ~ ~ ~ 0.5 2'] + X.end)
    fn(f'{pfx}/loaded', [f'function bm:{pfx}/hurt', 'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.3 20'])
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p235c/undo_you'])
    fn('p235c/undo_you', ['effect give @s minecraft:instant_health 1 0 true', 'effect give @s minecraft:regeneration 8 0 true', click,
                          'particle minecraft:dust{color:[0.6,0.85,1.0],scale:1.0} ~ ~1 ~ 0.3 0.5 0.3 0 12'])
    return lines


def _inkblot(G, X):
    fn, pfx, foe = G.fn, X.pfx, X.foe
    K = dict(melee=dict(st=7, x=6, at=3, cd=20, reach=2.4),
             ranged=dict(st=8, x=14, at=9, cd=80, near=2.5, far=7, face='serious'),
             crowd=dict(st=11, x=10, at=6, cd=200, r=4, face='serious'),
             charged=dict(st=12, x=24, at=20, cd=1200, r=5),
             kind=dict(st=14, x=24, at=12, cd=1200, face='happy'))
    lines = kit(G, X, K)
    ink = 'particle minecraft:squid_ink ~ ~0.8 ~ 0.3 0.3 0.3 0.05 12'
    melee(G, X, 7, 2.4, [ink, 'particle minecraft:crit ~ ~1 ~ 0.2 0.3 0.2 0.2 6'], 'minecraft:entity.player.attack.strong')
    tg = f'@e[{foe},distance=..7,sort=nearest,limit=1]'
    fn(f'{pfx}/ranged', X.hit(8) + [f'execute as {tg} at @s run function bm:{pfx}/spiked',
                                    f'execute facing entity {tg} eyes run particle minecraft:squid_ink ^ ^1 ^2 0.1 0.1 1.2 0.01 16'] + X.end)
    fn(f'{pfx}/spiked', [f'function bm:{pfx}/hurt', 'particle minecraft:crit ~ ~1 ~ 0.2 0.3 0.2 0.3 10', 'playsound minecraft:item.trident.hit neutral @a[distance=..16] ~ ~ ~ 0.8 1.4'])
    fn(f'{pfx}/crowd', X.hit(4) + [f'execute as @e[{foe},distance=..4] at @s run function bm:{pfx}/splashed', 'particle minecraft:squid_ink ~ ~0.6 ~ 1.5 0.4 1.5 0.05 40',
                                   'playsound minecraft:entity.slime.squish neutral @a[distance=..16] ~ ~ ~ 1 0.7'] + X.end)
    fn(f'{pfx}/splashed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:blindness 3 0', 'effect give @s minecraft:slowness 3 1', ink])
    # INK SHIELD: round you - Resistance II and Absorption, your followers too; the monsters at your feet pushed off
    fn(f'{pfx}/charged', ['execute on owner if entity @s[distance=..16] at @s run function bm:p235i/shield_you'])
    fn('p235i/shield_you', ['effect give @s minecraft:resistance 8 1 true', 'effect give @s minecraft:absorption 20 0 true', 'scoreboard players operation #me bm.pid = @s bm.pid',
                            *[f'execute as @e[type=minecraft:{t},distance=..16] if score @s bm.pid = #me bm.pid run effect give @s minecraft:resistance 8 1 true' for t in ('wolf', 'cat')],
                            'tag @s add bm.ibme', 'execute as @e[type=#bm:hostile,tag=!bm.npc,distance=..3.5] at @s run function bm:p235i/shoved', 'tag @s remove bm.ibme',
                            'particle minecraft:squid_ink ~ ~1 ~ 0.8 0.8 0.8 0.02 30', 'playsound minecraft:item.shield.block player @s ~ ~ ~ 1 0.8'])
    fn('p235i/shoved', ['execute facing entity @a[tag=bm.ibme,limit=1] feet positioned ^ ^0.2 ^-2.5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~',
                        'particle minecraft:squid_ink ~ ~1 ~ 0.2 0.3 0.2 0.02 6'])
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p235i/wonder_you'])
    fn('p235i/wonder_you', ['effect give @s minecraft:luck 60 0 true', 'effect give @s minecraft:haste 30 0 true', 'particle minecraft:squid_ink ~ ~2 ~ 0.2 0.1 0.2 0 4',
                            'playsound minecraft:entity.slime.squish_small player @s ~ ~ ~ 1 1.4'])
    return lines


def _speech(G, X):
    fn, pfx, foe = G.fn, X.pfx, X.foe
    K = dict(melee=dict(st=7, alt=9, x=7, at=4, cd=20, reach=2.4, face='shout'),
             crowd=dict(st=11, x=12, at=10, cd=300, r=10, face='surprised'),
             charged=dict(st=12, x=34, at=[22, 11], cd=1200, r=5, face='puff', go=['playsound minecraft:entity.puffer_fish.blow_up neutral @a[distance=..16] ~ ~ ~ 1 0.8']),
             kind=dict(st=14, x=24, at=12, cd=1200, face='happy'))
    lines = kit(G, X, K)
    knock = f'execute facing entity @e[type=minecraft:wolf,tag={X.me},limit=1] feet positioned ^ ^0.2 ^-1.5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~'
    melee(G, X, 6, 2.4, ['particle minecraft:explosion ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:dust{color:[1.0,0.85,0.2],scale:1.4} ~ ~1.2 ~ 0.4 0.4 0.4 0 10', knock],
          'minecraft:entity.player.attack.knockback')
    fn(f'{pfx}/crowd', [f'execute as @e[{foe},distance=..10] run effect give @s minecraft:glowing 8 0', 'execute on owner if entity @s[distance=..16] run effect give @s minecraft:speed 5 0 true',
                        'particle minecraft:dust{color:[1.0,0.2,0.2],scale:1.5} ~ ~2 ~ 0.1 0.3 0.1 0 10', 'playsound minecraft:block.note_block.bell neutral @a[distance=..24] ~ ~ ~ 1 1.6'] +
       ['execute on owner if entity @s[distance=..16,tag=!bm.hush] run ' + X.csay('"!!! LOOK OUT!"')])
    for i, (d, extra) in enumerate(((8, []), (6, ['effect give @s minecraft:slowness 3 1']))):
        fn(f'{pfx}/charged{i + 1 if i else ""}', X.hit(d) + [f'execute as @e[{foe},distance=..5] at @s run function bm:{pfx}/blasted{i}', 'particle minecraft:explosion ~ ~1 ~ 1 0.5 1 0 4',
                                                             f'playsound minecraft:entity.generic.explode neutral @a[distance=..16] ~ ~ ~ 0.6 {1.6 if i else 1.2}'] + X.end)
        fn(f'{pfx}/blasted{i}', [f'function bm:{pfx}/hurt', knock] + extra)
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p235b/think_you'])
    fn('p235b/think_you', ['effect give @s minecraft:haste 30 1 true', 'effect give @s minecraft:luck 30 0 true', 'particle minecraft:end_rod ~ ~2.2 ~ 0.3 0.1 0.3 0.01 6',
                           'playsound minecraft:block.note_block.chime player @s ~ ~ ~ 1 1.4'])
    return lines


_ABIL = {'dragon': _dragon, 'eraser': _eraser, 'cursor': _cursor, 'inkblot': _inkblot, 'speech': _speech}


# ---------------------------------------------------------------------------------------------------- generate: the followers, how you meet them
def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    fn('p235/owner_hurt', ['execute on owner if entity @s[distance=..12] run return run function bm:p235/hurt_q', 'return 0'])
    fn('p235/hurt_q', ['execute store result score #h bm.rng run data get entity @s Health 10', 'execute store result score #mx bm.rng run attribute @s minecraft:max_health get 10',
                       'execute if score #h bm.rng < #mx bm.rng run return 1', 'return 0'])
    mine = lambda tag: (f'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #hy bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={tag},distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #hy bm.rng 1',
                        'execute if score #hy bm.rng matches 0 run return 0')

    def walker(C, X, tag, chance, line, extra=()):
        """an encounter that turns up beside you while you walk with someone (tag: their host), now and then"""
        p, ab = C.pfx, C.ab
        X.second.append(f'execute as @a[tag=!bm.{ab}met,gamemode=!spectator] at @s if dimension minecraft:overworld run function bm:{p}/enc/check')
        fn(f'{p}/enc/check', [*mine(tag), *extra, f'execute store result score #r bm.rng run random value 1..{chance}', 'execute unless score #r bm.rng matches 1 run return 0',
                              f'execute if entity @e[type=minecraft:interaction,tag=bm.{ab}enc,distance=..64] run return 0',
                              f'execute positioned ^ ^ ^4 run function bm:{p}/enc/place'])
        fn(f'{p}/enc/place', [f'execute if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~-1 ~ #bm:grap_pass run return run function bm:{p}/enc/step',
                              f'execute positioned ~ ~1 ~ if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run function bm:{p}/enc/step'])
        fn(f'{p}/enc/step', [f'function bm:{p}/enc/spawn'] + C.BURST + [X.tellraw(f'@a[tag=!bm.{ab}met,distance=..16]', line)])

    def offer(C, X, items, have_line, no_line, joined_line, used=True):
        p = C.pfx
        csay = lambda txt: title('@s', 'actionbar', [T(f'{C.NAME}: ', C.COL, bold=True), T(txt, C.LINE)])
        fn(f'{p}/enc/talk', [f'execute if items entity @s container.* {X.holds(C.ITEM)} run return run ' + csay(have_line)] +
           [f'execute if items entity @s weapon.mainhand {i} run return run function bm:{p}/enc/recruit' for i in items] + [csay(no_line)])
        fn(f'{p}/enc/recruit', (['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}'] if used else []) +
           [f'execute as {X.here} at @s run particle minecraft:heart ~ ~1 ~ 0.3 0.3 0.3 0 4', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6',
            X.tellraw('@s', joined_line), f'function bm:{p}/enc/joined'])

    # ---- THE DOODLE DRAGON: walk with Kettle; his drawing climbs off the page. A dye wins it over
    def e_dragon(G, X):
        walker(Dragon, X, 'bm.ktpet', 200, [T('Kettle stops dead. "My DRAGON! He\'s REAL!" ', '#8ad8ff', italic=True),
                                            T('A crayon dragon climbs off a page in his hand, sneezes a puff of smoke, and grins at you.', 'gray', italic=True)])
        dyes = [f'minecraft:{c}_dye' for c in ('white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black')]
        offer(Dragon, X, dyes, '"You already have my drawing! I live in it. Sometimes."', '"Do you have crayons? Any colour! Green\'s my favourite. Obviously."',
              [T('He sniffs the dye, sneezes rainbow smoke, and scribbles himself a brand new spot on his tail. ', '#d4f4c8', italic=True),
               T('Then he hands you his drawing: KETTLE, it says in the corner. He\'s coming with you.', 'gray', italic=True)])
    # ---- THE ERASER: walk with the Gem; its mistake hides nearby, ashamed. Paper - a fresh start
    def e_eraser(G, X):
        walker(Eraser, X, 'bm.cgpet', 220, [T('The Gem flickers: :c - and from behind a stone, something pink peeks out. ', GEM, italic=True),
                                            T('A little eraser, worn at one corner, looking very, very sorry.', 'gray', italic=True)])
        offer(Eraser, X, ['minecraft:paper'], '"You already have my crumb! Th-that means you\'re stuck with me."', '"I c-could only erase it. Do you have something... I could keep clean?"',
              [T('It takes the sheet very carefully, and doesn\'t erase a thing. It looks up at you, astonished at itself. ', '#fcdce4', italic=True),
               T('Then it brushes off a pink crumb and gives it to you. A fresh start.', 'gray', italic=True)])
    # ---- THE CURSOR: a Glitched Cartridge with nobody beside you (phase214's "use it beside a follower") - the player's hand
    def e_cursor(G, X):
        fn('p235c/enc/glitch', ['function bm:p235c/enc/spawn'] + Cursor.BURST + ['playsound minecraft:block.note_block.bit neutral @a[distance=..24] ~ ~ ~ 1 1.8'])
        csay = lambda txt: title('@s', 'actionbar', [T('The Cursor: ', Cursor.COL, bold=True), T(txt, Cursor.LINE)])
        fn('p235c/enc/talk', [f'execute if items entity @s container.* {X.holds("cursor_mouse")} run return run ' + csay('"You\'ve already got me! I\'m your hand, remember?"'),
                              'function bm:p235c/enc/recruit'])
        fn('p235c/enc/recruit', [f'execute as {X.here} at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.2 16',
                                 'playsound minecraft:ui.button.click player @s ~ ~ ~ 1 1.2',
                                 X.tellraw('@s', [T('It clicks on you. ', '#d8f0ff', italic=True), T('Selected. ', '#f4f4f4', bold=True, italic=True),
                                                  T('Then it hands you an old mouse with a cut cable - and wherever your hand goes, it follows.', 'gray', italic=True)]),
                                 'function bm:p235c/enc/joined'])
    # ---- THE INK BLOT, THE SPEECH BUBBLE: walk with Mr. Capshun
    def e_ink(G, X):
        walker(InkBlot, X, 'bm.mzpet', 200, [T('Mr. Capshun\'s pen leaks. A drop falls - splat - and the blot it makes blinks up at you. ', '#c8c8dc', italic=True),
                                             T('[Mr. Capshun narrates: "That was not in the script."]', 'gray', italic=True)])
        offer(InkBlot, X, ['minecraft:ink_sac', 'minecraft:glow_ink_sac'], '(it points at the ink pot in your pocket, as a little arrow)', '(it makes a "?" at your empty hand)',
              [T('It drinks up the ink, grows a size, and shapes itself into a little thumbs-up. ', '#c8c8dc', italic=True),
               T('Then it pours itself into a pot and offers it to you. It\'s coming along.', 'gray', italic=True)])

    def e_speech(G, X):
        walker(Speech, X, 'bm.mzpet', 200, [T('[Mr. Capshun narrates: "And then-"] ', '#e0e0e0', italic=True),
                                            T('...and his narration pops out of the air beside him, a speech bubble with a face, and grins at you: "AND THEN!!"', 'gray', italic=True)])
        offer(Speech, X, ['minecraft:writable_book'], '"You\'ve already got my card! I\'m with you, pal!"', '"I\'ve got nothing to SAY! Got a book and quill?"',
              [T('It flips through the empty pages and shouts every word it can think of into them. ', '#ffe0a0', italic=True),
               T('Then it hands you a blank caption card: "Call me when it gets EXCITING."', 'gray', italic=True)], used=False)
    ENC = {'dragon': e_dragon, 'eraser': e_eraser, 'cursor': e_cursor, 'inkblot': e_ink, 'speech': e_speech}
    for _C in DOODLES:
        RP.build(_C, G, (lambda w: lambda G, X: _ABIL[w](G, X))(_C.W), ENC[_C.W])
    # (the Cursor: a cartridge used with nobody beside you - instead of "use it beside one of your followers")
    U = G.FUNCS['p214/use']
    k = next(i for i, l in enumerate(U) if 'Use it beside one of your followers' in l)
    U.insert(k, 'execute if score #done bm.rng matches 0 unless entity @s[tag=bm.uxmet] run function bm:p235c/enc/cart')
    fn('p235c/enc/cart', ['scoreboard players set #done bm.rng 1',
                          'execute if entity @e[type=minecraft:interaction,tag=bm.uxenc,distance=..32] run return run ' + title('@s', 'actionbar', T('The cartridge flickers - the Cursor is already out, nearby.', '#9affb0')),
                          'clear @s *[minecraft:custom_data~{bm:"glitch_cart"}] 1', 'execute positioned ^ ^ ^2 run function bm:p235c/enc/glitch',
                          tellraw('@s', [T('The cartridge glitches - nobody there to glitch - and the screen\'s own pointer slips out of it into the air: ', '#9affb0', italic=True),
                                         T('a little white hand-arrow, blinking at you.', 'white', italic=True)])])

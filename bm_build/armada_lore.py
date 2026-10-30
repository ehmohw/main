"""2.99: THE VORN ARMADA's words - the hive's voice, Admiral Vexis, the books aboard, and its items' names. Shared by p2/armadacfg
(the builder's lecterns and signs), p2/armadaitems, phase241 (the fleet), phase242 (the Admiral's fight) and phase243 (Vexis).

THE LORE. The Vorn are a hive: every ship and every trooper answers one voice. The fleet's heart is the Hive-Star, a dying red
giant; the Armada circles it and drinks it - red Xenite is condensed star-mass, which is why it grows only aboard Dreadnoughts.
The voice is ADMIRAL VEXIS, once a single Vorn, one of the first the hive "improved". Every invasion night is Vexis reaching
across the stars for your world. Cut the hive-link and the voice goes silent - and Vexis, alone in its own head for the first time
in an age, is only one."""

VX = 'Admiral Vexis'
VX_COL = '#7aff6a'            # (the hive's green)
RED = '#ff4a4a'               # (the Vorn's war-red)
STAR = '#ff8a3a'              # (the Hive-Star)
HIVE = '#b6ff3c'              # (the hive's voice)
TEAL = '#3ad8c8'              # (Donadian - the friendly ones)

# ---- the hive's voice, to each player the first time they come near (builder: ABuild.voice(key, ...))
VOICE = {
    'dock': '"A SPECIMEN HAS BOARDED. HOW WONDERFUL. WE WILL IMPROVE IT."',
    'brood': '"OUR NURSERIES. EVERYTHING HERE WAS SOMETHING ELSE, ONCE."',
    'forge': '"THE STAR BLEEDS FOR US. WE MAKE IT INTO WAR."',
    'nav': '"EVERY LIGHT ON THESE CHARTS IS A WORLD WE HAVE TAKEN. YOURS IS MARKED."',
    'dread': '"OUR WARSHIPS. THEY HAVE NEVER LOST."',
    'flag': '"COME, THEN. THE ADMIRAL WILL SEE YOU NOW."',
    'gauntlet': '"COMPLY. COMPLY. COMPLY."',
    'helm': '"WE ARE VEXIS. VEXIS IS WE."',
}

# ---- the fight (phase242)
FIGHT = {
    'wake': ('"YOU HAVE COME A LONG WAY TO BE IMPROVED."', 'Admiral Vexis wakes.'),
    'p1': 'THE WARFRAME',
    'turn1': '"INTERESTING. THE SHELL IS DAMAGED. WE WILL NOT NEED IT."',
    'p2': 'THE HIVE-LINK',
    'turn2': '"THE STAR. GIVE US THE STAR."',
    'p3': 'STARFIRE',
    'frenzy': '"IMPROVE. IMPROVE. IMPROVE."',
    'fall': '"...the voices... where are... the voices..."',
    'fall2': 'Admiral Vexis has fallen. The hive-link is cut: the invasion nights are over.',
    'pylon': 'A shield pylon overloads - the Warframe\'s shield flickers!',
    'pylons_all': 'Every pylon is down! The Warframe is exposed!',
    'clone': 'Which one is real?',
    'abandon': '"RUN. WE WILL FIND YOU AGAIN. WE ALWAYS DO."',
}
# ---- its unlinking (the fall's cinematic)
UNLINK = {
    'cut': 'The hive-link burns out. For the first time in an age, the hive falls silent.',
    'one': '"...one. I am only one."',
    'name': '"Vexis. That was my name. Before."',
    'you': '"You cut the strings. I do not know what I am without them. Show me?"',
    'crack': 'Light breaks through every seam of it...',
    'dust': '...and Vexis comes apart into star dust.',
}

# ---- the Cipher guardians' names (phase241's 'vboss' trials: an existing Vorn boss, renamed and stronger)
GUARD = {'brood': ('The Brood-Warden', '#8aff6a', 'It wants specimens.'),
         'forge': ('The Forgemaster', RED, 'The Warlord\'s elder. It forged the Warlord.'),
         'nav': ('The Star-Seer', '#c8a0ff', 'It charts the worlds the hive will take.')}

# ---- books on the lecterns
BOOKS = {
    'dock': ('Boarding Manifest', ['ARRIVALS: one (1) specimen. Unscheduled.\n\nINSTRUCTIONS: hold it until the Admiral is free.',
                                   'NOTE, in a different hand: the lifts answer to levers. Up, down, up - like breathing. Like the old ships.']),
    'brood': ('Brood Log 7', ['Tank 1 pulses first. Then 4. Then 2. Then 3.\n\nIt always pulses in the order the subject was improved.',
                              'Subject 117 (canine, Earth) escaped through the kennel vent. The vent is too small for us. Not for a dog.']),
    'nav': ('The Star-Chart', ['Mark the worlds in the order we took them:\n\nTHE EYE\nTHE CROWN\nTHE SERPENT\nTHE HAND\nTHE STAR',
                               'Your world is next on the chart. It has been next for a long time.']),
    'forge': ('Forge Orders', ['Feed the furnaces: GREEN, then VIOLET, then CYAN.\n\nGreen is energy. Violet is gravity. Cyan is resonance. Red is mass: red, we keep.',
                               'Reroute the conduits until every reactor glows. The Forgemaster checks the lights.']),
    'helm': ('Vexis\'s Last Log', ['I was a navigator once. I had a name. I gave it to the hive, gladly, and the hive gave me a fleet.',
                                   'Sometimes, when the link is quiet, I remember the name. Then the link is never quiet.']),
}

ITEMS = {
    'coords': ('Hive-Star Coordinates', ['A star-chart the hive never meant to lose.', 'In the End, use it: the Armada will answer.']),
    'cipher_1': ('Command Cipher I', ['Pried from the Brood-Warden.', 'One of three for the Flagship\'s Command Lock.']),
    'cipher_2': ('Command Cipher II', ['Forged into the Forgemaster\'s core.', 'One of three for the Flagship\'s Command Lock.']),
    'cipher_3': ('Command Cipher III', ['The Star-Seer\'s eye, still watching.', 'One of three for the Flagship\'s Command Lock.']),
    'hive_sigil': ('Hive Sigil', ['A sigil from a room the hive forgot.', 'Six open the Hive Vault behind the helm.']),
    'star_core': ('Star-Core', ['A sliver of the Hive-Star, cooled just enough to hold.', 'The Starforge bench aboard the Dock works it.']),
    'link': ('The Severed Link', ['The hive-link that bound Admiral Vexis.', 'Cut. Quiet. Something on the other end is listening for you.']),
}

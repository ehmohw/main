"""2.98: THE LORE OF THE UNDERCROWN - one source for every book, voice, line and item text of the final dungeon (phase237),
its master's fight (phase238) and what's left of him afterwards (phase239). Nothing here runs; it is read.

THE STORY, IN ORDER
  AUREL, THE FIRST LIGHT   before the Lightbringer there was another herald of the Divine One - the first, and the brightest.
      He was sent down into the Nether to keep the dark beneath the world from rising. He kept it for an age. Then he began
      to listen to it, and then it began to answer, and then there was no difference. The first light went out, and something
      wore what was left: the DREAD SOVEREIGN.
  THE UNDERCROWN   the Divine One could not unmake what had been a herald, so it was BOUND: chained beneath the Nether's
      crust in a hall cut for it, the Undercrown, with its own chains forged at its own forge. Its throne was sealed, and a
      warden set over it - a king, to sit in his own hollow throne above and hold the lid shut. Over the ages the warden
      grew hollow too. (THE HOLLOW KING.) When you broke him, the lid slid: the world turned (hard mode), and the Sovereign
      "turned its gaze on this world" (phase176).
  THE DREAD   everything the Sovereign touches through the gap it wears like armour - cracked void-plate, red seams of its
      light. Dread mobs are its reach; Stalkers its hounds, made of the dark between stars, which come for those who kill its
      own on the Dread Nights (phase181). Dread Tokens are the coin it pays in (Vesper deals them, and asks no questions).
  ITS THREE   chained, it could not walk the world, so it made itself three hands out of three things that were already
      there - each out of a weakness it understood. FEAR: Pistachio's hat, frightened, came down on a snowman (THE MALEVOLENT
      SNOWBEAST). HUNGER: Cecil's old friend studied the dark too long, and it studied her back (THE WATCHFUL WITCH). WAR: the
      Underwater Kingdom fought the Dread in the great war, and it woke the deep's oldest jailer against them (THE CHOMPING
      SAWSHARK - which swallowed Democratus). Break all three, and it has nothing left to reach with: it has to answer itself.
      "YOU BROKE MY THREE. COME, THEN."
  THE THRONE   at the bottom of the Undercrown, below the Hall of Chains and the Stair of a Thousand Eyes, it kneels on its
      throne, bound, waiting. Three forms: ARMORED (still bound, the chains its strength), BROKEN (its wings, every eye in
      them open - and it remembers its three), and TRUE (the helm gone: inside, only a vast red eye and the void).
  THE RECKONING   it falls. The Dread Nights end - its hunger goes out with it (bm.dfin on everyone who faced it; the
      world's #dfell). The Lightbringer's vigil is over; she goes home (she is no longer to be found). What remains of its
      hunger is a coal in your hand: THE DREAD EMBER, which can kindle the Nights again for anyone who misses them.
      And what remains of IT is bound - by its own chains - to whoever broke it: THE BOUND SOVEREIGN, a follower (hard mode).
      Somewhere in it, very faintly, Aurel is listening."""

SOV = 'The Dread Sovereign'
SOV_COL = '#d0182e'
VOICE_COL = '#ff5a64'
HOLY = '#fff4d0'

# ---- what it says as you come down (the dungeon's voice markers, phase237; keyed by marker) - one line, first time each player passes
VOICE = {
    'gate': '"So. You broke my three. Come, then."',
    'hall': '"Do you hear them? My chains. They have sung for an age. They are tired."',
    'frozen': '"Fear was the easiest. Everything that lives is afraid of something."',
    'hexed': '"She came looking for me. I only answered."',
    'drowned': '"A kingdom at war will open any door. I only knocked."',
    'shards': '"Three pieces of my crown. You carry them as if they were yours."',
    'eyes': '"I see you. I have always seen you. Since the King fell, I have watched."',
    'ante': '"Kneel, and I will make you a fourth."',
    'hoard': '"Mine. All of it was always mine."',
    'last_light': '"...Her? She sent another. Of course she did."',
}
# ---- (2.98c) THE LAST LIGHT: as it falls, the Divine One comes down into the Undercrown and ends it (phase238's finale)
DIVINE_NAME = 'The Divine One'
DIVINE = {
    'pulled': 'Light pours through the dome - and the Sovereign is dragged into it.',
    'title': 'THE DIVINE ONE',
    'sub': 'who made the first light',
    'sov1': '"...You. After all this time. You came down... for this?"',
    'name': '"AUREL."',
    'sov2': '"...that name. I had forgotten it was mine."',
    'raise': 'His hand rises. The light gathers in it.',
    'burn': 'His light takes it - and it burns, white and gold, from the ground up.',
    'end': 'And the Dread Sovereign is unmade - the last of it, light.',
    'rest': '"Rest now, my first light. It is over."',
    'you': '"You have done well, little ones. The dark is quiet."',
}
# ---- the fight (phase238)
FIGHT = {
    'wake': ('"Rise? I have been rising since your King fell."', 'The Dread Sovereign wakes.'),
    'p1': 'ARMORED',
    'turn1': '"Enough. LOOK at me."',
    'p2': 'BROKEN',
    'turn2': '"I was LIGHT. I was the FIRST light. And I will be the last thing you see."',
    'p3': 'TRUE',
    'frenzy': '"UNMAKE. UNMAKE. UNMAKE."',
    'fall': '"...it is... so quiet..."',
    'fall2': 'The Dread Sovereign has fallen. The Dread Nights are over.',
    'abandon': '"Run, then. The chains will hold me. For now."',
    'wellspring': 'A Wellspring shatters - its light stops feeding the Sovereign.',
    'wells_all': 'Every Wellspring is dark! It cannot mend.',
    'grounded': 'Its wings are blind - it crashes down! Its heart is open!',
    'echo_snow': '"Remember the cold, little hat."',
    'echo_witch': '"Look closer, Witch."',
    'echo_shark': '"Bite."',
}
# ---- the echoes in the wards
ECHO = {
    'snow': ('Echo of the Malevolent Snowbeast', '#9ad8ff', 'The cold remembers its shape.'),
    'witch': ('Echo of the Watchful Witch', '#7aff5a', 'Something is watching. It is only an echo. It is enough.'),
    'shark': ('Echo of the Chomping Sawshark', '#ffd21a', 'It swims through the air as if the sea still held it.'),
}
# ---- the books on the lecterns (title, author, pages)
BOOKS = {
    'warden': ('The Warden\'s Last Entry', 'the Hollow King', [
        'I am to sit above it and hold the lid. That is all. A king on a throne, and under the throne, a door, and under the '
        'door, IT.\n\nI am told I will not grow tired.',
        'Year uncounted. It speaks when the castle is quiet. It is never quiet now. It knows my name and says it kindly.',
        'I have stopped going down to look at the chains. I can hear them from the throne. I can hear them in my sleep. I do '
        'not sleep.',
        'Whoever reads this: I was not hollow when I came. Do not let it make you a fourth.']),
    'frozen': ('Verse of the Frozen Falls', 'cut in the ice', [
        'Strike them in the order fear arrives:\n\nFIRST the hat that flinched,\nTHEN the snow that caught it,\nTHEN the cold that kept it,',
        'THEN the beast that rose,\nLAST the silence after.\n\n(The five falls are marked: a hat, a flake, an icicle, a '
        'claw, an empty frame.)']),
    'witch': ('Her Notes, Unfinished', 'the Watchful Witch', [
        'Cecil says I read too late into the night. Cecil says a lot of things. There is a voice under the Nether and it '
        'knows more than every library in the Overworld.',
        'It told me where to dig. It told me how to listen. I have never been so close to knowing EVERYTHING.',
        'It is watching me while I write this. That is all right. I am watching it back.\n\nI think.',
        '(The last pages are covered in one word, over and over, until the ink runs out: LOOK.)']),
    'drowned': ('Log of the Leviathan\'s Lament', 'a captain of the Kingdom', [
        'Day 40 of the war. The Dread came up through the trenches like smoke through water. Our tridents go straight through it.',
        'We followed it down to find where it came from. The sea floor opened. Something old and full of teeth woke under us. '
        'It was not the Dread\'s. It was OURS - the deep\'s old jailer - and it turned on us.',
        'The Queen ordered the Kingdom down, under the sea, where the jailer keeps it still. Democratus would not go. The '
        'last we saw of him was the inside of its mouth.',
        'They chained our ship and dragged it here, into the fire, as a trophy. If you are reading this: ring the bells in '
        'the Kingdom\'s song. The ship still knows it.']),
    'unwritten': ('The Unwritten History', '(the name has been rubbed out)', [
        'Before the Lightbringer there was another. The Divine One sent him down first, into the fire, to keep the dark from '
        'rising. His name was AUREL, and he was the brightest of them.',
        'He kept the dark for an age. Then he began to listen to it. Then it began to answer. Then there was no difference.',
        'The Divine One could not unmake what had been a herald. So it was bound: chained here, under the crust of the '
        'Nether, with chains forged at its own forge, and a warden set over it.',
        'Every account of Aurel was unwritten, so that no one would remember there had ever been a light down here. '
        'Someone missed a page.']),
    'chains': ('Forge Ledger', 'the Chainmaker', [
        'Six chains, one for each wing. Each link quenched in a herald\'s tears.\n\nThey asked me if they would hold forever.',
        'I told them nothing holds forever. They told me to make them hold until someone strong enough came along to finish it.',
        'I asked what happens to the chains then.\n\nThey said: whoever breaks him holds the other end.']),
    'vigil': ('The Vigil', 'the heralds', [
        'Here we keep the last light, so that the first one is never wholly dark.',
        'We do not pray that he be destroyed. We pray that he be stopped. They are not the same prayer.',
        'If one of us comes to this chapel after we are gone, she will know what to do. Light holds. It always holds.']),
    'ante': ('A Note, Nailed to the Door', 'someone who turned back', [
        'Do not go in tired. Do not go in alone. Break the braziers on its pillars or it mends faster than you can cut. '
        'When its wings open, put out their eyes and it falls. When the helm comes off -',
        '- I don\'t know. I ran. The floor was falling.']),
}
# ---- the Lightbringer, at the Last Light (she knows the place)
LAST_LIGHT = ['"This is where we kept the vigil. I did not think I would see it again."',
              '"Aurel. He was the first of us. He was the brightest of us."',
              '"Take this. When the eye opens, hold it up. Light holds."']
# ---- item texts
ITEMS = {
    'summons': ('The Sovereign\'s Summons', ['A black compass with a red needle.', 'In the Nether it points to the Undercrown;',
                                          'everywhere else it spins.', '"You broke my three. Come, then."']),
    'shard_snow': ('Crown Shard of Fear', ['A splinter of a black crown, rimed with frost.', 'Set it in the Throne Gate.']),
    'shard_witch': ('Crown Shard of Hunger', ['A splinter of a black crown. An eye opens in it', 'when you look away. Set it in the Throne Gate.']),
    'shard_shark': ('Crown Shard of War', ['A splinter of a black crown, crusted with salt.', 'Set it in the Throne Gate.']),
    'black_seal': ('Black Seal', ['A wax seal, black as the Undercrown, stamped with a chain.', 'Six of them open the Sovereign\'s Hoard.',
                                 'They are spent when it opens.']),
    'ember': ('The Dread Ember', ['All that is left of its hunger. It is still warm.', 'Kindle it (hold right-click): the Dread Nights return - and the Sovereign rises for you again.',
                                 'Kindle it again: they end.']),
    'edge': ('Sovereign\'s Edge', ['Its greatsword: void-glass, veined in red.', 'It is lighter than it looks. It wants to be swung.']),
    'crown': ('The Black Crown', ['It does not sit on your head so much as close around it.', 'The Dread know whose it was.']),
    'heart': ('Heart of the Dread', ['A dark-red crystal, beating slowly.', 'It does not want you to die. Not yet.']),
    'eye': ('The Sovereign\'s Eye', ['Its eye, closed. Something in it is listening.', 'Hold it to call what is left of it - bound by its own chains.']),
    'dawnshard': ('Dawnshard', ['A sliver of the last light, from the heralds\' vigil.', 'Held when the great eye opens, it turns the beam.']),
    'unwriting': ('Page of Unwriting', ['A page with every word rubbed out but one: AUREL.', 'Read it (use): the monsters near forget you.']),
    'chainwhip': ('Sovereign\'s Chain', ['One link of the six chains, and the rest of it.', 'It still remembers holding something down.']),
    'nine_lives': ('Ninth Life', ['A little silver bell on a ribbon. It smells of cat.', 'Carried, it saves you from one fall a day.']),
}

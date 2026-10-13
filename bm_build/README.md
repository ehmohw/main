# Black Market — v2.69 (Java 26.3)

The Black Market now ships as **one complete pack, boss dungeons included** (the old "Phase 2 TEST" build is the main version). This README covers the market and the world; `README_PHASE2.md` covers the seven boss dungeons and the Hollow King's gear.

A data pack + resource pack. No mods required, and it works alongside Fabric.

## Install

**Single-player:** put `BlackMarket_DP.zip` in your world's `datapacks` folder. Then enable `BlackMarket_RP.zip` in Options → Resource Packs.

**Server (multiplayer):**
1. Put `BlackMarket_DP.zip` in `world/datapacks/`, then run `/reload` (or restart).
2. Host `BlackMarket_RP.zip` somewhere with a direct download link. In `server.properties`, set:
   ```
   resource-pack=<direct link>
   resource-pack-sha1=<sha1 from SHA1.txt>
   require-resource-pack=true
   ```

New structures only generate in **chunks that haven't been explored yet**. Fly out to fresh land, or use the admin commands below to place one for testing.

Without the resource pack, the tokens, keys, hats and rats show as missing textures. Everything still works.

## New in 2.69: three ways through every puzzle, a fight over the void, a harder climb, rooms you build, craft and dig, and three new games

### Every puzzle room now comes in three variants
Each puzzle room is drawn as one of three variants when the heist is laid. Each variant is solved a different way; none is just the old puzzle with new paint. Every puzzle is worked out when the pack is built and checked to have exactly one answer.

| Room | A (as before) | B | C |
|---|---|---|---|
| The Combination Room | the ledger's gold and coal, read in the mirror | **The Weighed Ledger**: each lever carries a number (1, 2, 4, 8, 16, shuffled); pull the ones that add up to the ledger's sum | **The Logic Ledger**: three to five clues ("Levers II and IV are set differently") pin down the one setting that fits |
| The Weighing Room | every golden scale at once | **The Order of the Scales**: scales marked crown, key, coin and skull, and a riddle gives the order. Step on them one at a time. Only feet count, and the scales give no answer until all four are down | **The Baton Run**: carry the Relay Baton to the scale that lights up before its light runs out, 5–7 in a row. There's one baton, so camping doesn't help |
| The Gauntlet | the sweeping laser planes | **The Low and the High**: the beams never go out. Jump the red ankle beams; sneak under the violet head-height ones | **The Mirror Gauntlet**: turn the glass mirrors (right-click) until the laser hits the gold target. Exactly one setting works, and it bends the beam four times or more |
| The Tile Floor | the hidden path and the peek button | **The Colour Trail**: follow the colours in the sign's order; only one trail reaches the far side | **The Counted Floor**: numbers along the edges give the safe tiles in each row and column |
| The Dial Lock | the blueprint's arrows | **The Numbered Dials**: three or four sums ("Left + middle = 9", "Right is odd") fix the setting | **The Geared Dials**: the blueprint's arrows, but the dials turn each other. Work out the turns |
| The Three Coffers | the riddle of places | **The Lying Coffers**: each coffer says where the honest one is, and exactly one of them tells the truth | **The Shell Game**: the gold goes into one of four plain chests and they shuffle. Open the right one; a wrong one lets a Mimic out and they shuffle again |
| The Signal Lamps | repeat the sequence | **Backwards**: last flash first | **The Cipher**: the wall says what each colour really means; press what the flashes mean |
| The Lamp Floor | each button flips its lamp and the four beside it | each button flips its lamp and the four at its corners | each button flips its lamp and its whole row and column |
| The Tumbler Lock | catch the light on the gold gate | **The Wandering Gate**: the gate is the lamp marked green, and the mark moves after every hit | **The Blind Tumbler**: you see the light run once, then only hear it tick in the dark. Count your way to the gate |
| The Bell Tower | the broad spiral steps | **The South Stair**: single posts, longer jumps | **The Falling Stair**: the steps give way a moment after you land |
| The Crumbling Rafters | beams that fall once stood on | **The Blinking Beams**: beams wink out and back in a travelling wave | **The Ghost Beams**: an invisible winding path that shimmers only when you're right beside it |

### New rooms
- **The Sky Isles** (a fight room, Tiers II–V): islands joined by one-block bridges over a drop, with two waves of guards.
  - Knock a guard off the edge and it's gone.
  - From Tier III the drop is the void: falling in knocks you out and costs a try, and breezes join the second wave to blow you off.
  - On Tier II there's hay at the bottom, and a fall just sends you back to the start.
- **The Spire** (Tiers III–V): single blocks spiral up a tall pillar, with long jumps, one block up at a time. There's a gold **checkpoint** halfway: touch it, and a fall brings you back there instead of to the bottom.
- **The Tinker's Bench** (crafting): the Fixer wants something made (a compass, clock, lantern, bow, crossbow, spyglass, hopper, piston, observer or dispenser).
  - You get the parts, plus a few you don't need.
  - Craft it at the benches and hand it in at his hatch. Higher tiers need a part made first.
  - Leftovers go back to the Fixer.
- **The Mason's Plan** (building, Tiers I–IV): lay coloured blocks on the lodestone grid to match the plan by the door.
  - The blocks can only be placed on lodestone.
  - From Tier III the plan is drawn rotated: line up its gold corner with the grid's.
  - RESET clears the grid.
- **The Dig** (mining): a deepslate wall threaded with mud-brick veins. The Fixer's pick only breaks the mud. Most veins dead-end; one goes all the way through.

### Three new games (events)
- **Block Party**: a colour is called; get onto it before the rest of the floor drops away. There are 8–10 rounds and each is quicker than the last. Every round someone survives earns a coin, and surviving most of them wins the prize.
- **Red Light, Green Light**: run while the watcher looks away; freeze when it turns. Anyone it sees moving goes back to the line.
- **Memory Match**: sixteen face-down cards. Find the eight pairs before your misses run out.

### No shortcuts
- **Tile floors:** they now judge the tile you're standing over, not just its middle, so creeping along the seams between tiles drops you like any other false step.
- **Rooms crossed on foot:** in the tiles, rafters, gauntlet, bell tower and spire, the Fixer holds your wind charges and ender pearls until you're through. They come back the moment you leave the room. Flying higher than a jump over a tile floor, the rafters or the gauntlet sends you back to the start.

### Your secondary
A Ranged raider already carries a bow, so if they pick the Crossbow secondary they get a battle axe instead.

### For admins
- `admin/variant_a`, `_b`, `_c` and `_random` force the variant of every puzzle room laid from then on.
- `admin/rooms_only_<kind>` lays only that kind of room (no events) until you run `admin/rooms_any`.
- `admin/room_party`, `admin/room_redlight` and `admin/room_memory` force the next event room.

### Fixed
- **The Baton Run:** the last catch could mark the room beaten without opening its door.

## New in 2.68: a win pays in money, the Crate Desk and tip-offs, a laurel for every tier, three new finds, and the vault's loose ends

### A win pays in money now
A won heist no longer buries you in ingots, building supplies and heist gear. It pays:
- **Black Market Tokens:** your fee back, with a chance of a few more (as before).
- **Gutter Coins:** every share is coins now (2-3 a share at Tier I, 3-4 at II, 4-6 at III, 5-8 at IV, 7-10 at Tier V), plus the pot and the Fixer's cash.
- **Spoils and Captain's Insignia,** straight into your Gutter Bank (as before).
- **The metal Gutter Trophies** you earn, **BM Medallions** and the rare **BM Trophy** (the Fixer's prize, as before).
- **A Shifting Core:** 1 in 100 now, at every tier.
- **The night's own currency,** more at the higher tiers (3-6 at Tier I up to 7-14 at Tier V):

  | Heist | Pays | ...and an 8% chance of |
  |---|---|---|
  | Blood Moon | Blood Moon Crystals | the Crimson Ledger |
  | Lucky Night, or any Lucky Raid | Lucky Tokens (and a few coins) | the Gambler's Coin |
  | Alien | Green Xenite | the Vorn Cracking Rig |

Gone from the haul: vanilla ingots and gems, the stack of building supplies and food, Netherite Scrap, the Fence's curios, and the heist gear Goldtooth sells anyway. **The haul lectern's three kinds of haul are retired**; every haul pays this way, and the lectern is now the Crate Desk (below).

**The vault's own gear is rarer, and worth more:** one roll per raider per win. That's 6% at Tier I, then 7%, 8%, 9% and 10% at Tier V, for a piece of that tier's raid-only gear:

| Tier | Raid-only gear |
|---|---|
| I | the Heister's Shiv |
| II | the Heister's Shiv or the Vault Breaker |
| III | the Vault Breaker or the Coinslinger |
| IV | the Coinslinger or the Gutter Cutlass |
| V | the Gutter Cutlass or the Treasurer's Scepter |

Hidden vaults, the Gutter Gentry and the rare guards keep their own treasures.

### Three new finds
Every raider rolls for each of these on every win, at any tier:
- **Forgeheart** (rare, 5%): carry it anywhere in your inventory and the raw iron, gold and copper in your pack smelt themselves every few seconds. About one in five comes out as an extra ingot, raw ore blocks become metal blocks, and you get the furnace's experience.
- **The Alibi** (legendary, 3%): use it to snap back to where you stood five seconds ago. Any harm taken in those seconds is mended, any fire goes out, and you're unseen for a moment. It works once a minute and won't cross between worlds.
- **The Counterfeiter's Press** (mythical, 1%): use it on a floor to set it down. It prints one Black Market Token every in-game day for whoever set it there, with up to seven waiting; right-click it to collect. One press per player. Sneak + punch to pick it up (it pays out what's waiting first).

Each does something nothing else in the pack does: smelting on the go, a five-second rewind, and a steady Token income. All three work anywhere in the Overworld, Nether and End, and none can be carried into a heist (the coat check keeps them).

### The Crate Desk
The den's old haul lectern, and **The Crate Desk** button in the Ledger's Office. It's paid from your Gutter Bank first, then your pockets (a Gutter Medallion counts as 16 coins and a Trophy as 128; the change goes into your bank).

| | Price | What's in it |
|---|---|---|
| **Raw Materials Crate** | 16 coins | 4-5 stacks: iron, copper, coal, redstone, lapis, quartz, logs, stone, glass, string, leather, obsidian, gunpowder... |
| **Adventurer's Crate** | 32 coins | 2-3: experience bottles, enchanted books, ender pearls, golden apples, blaze rods, golden carrots, rockets... rarely an enchanted golden apple |
| **Mineral Crate** | 48 coins | 3-4: gold, emeralds, iron, gold, lapis and redstone blocks; sometimes diamonds; rarely netherite scrap or ancient debris |
| **Crimson Tip-off** | 64 coins | your next heist is a Blood Moon heist |
| **Vorn Signal** | 64 coins | your next heist is an Alien heist |

- **Crates:** set one down and open it. What's inside is decided only when it's opened, so there's no telling what you'll get. Walk away and anything left folds into your pack, like The Haul; walk away without opening it and the crate comes back as it was.
- **Tip-offs:** use one to call your next heist. It counts the next time you plan a heist yourself, whatever the night and whatever the admin's chance settings. **A Lucky Raid can never be called**; it's the luck of the draw.

### A laurel and an achievement for every tier
- **The first clear of each tier gives its own laurel:** Copper (I), Silver (II), Gilded (III), Pearl (IV) and Ember (V). That's on top of the Gilded piece and the Raid Banner.
- **Each tier has its own achievement,** from *Into the Gutter* (Tier I) to *Keeper of the Hoard* (Tier V).
- **Hold a laurel in your off hand** for a crown of its light over your head.
- Tiers you cleared before 2.68 count: their laurels and achievements arrive the next time you're on.

### The vault's loose ends
- **Leave from anywhere:** on a heist, the Fixer's Ledger opens the Office as usual, with **Leave the heist** at the bottom. It asks first, then sends you home with your own gear back; the fee and any share stay behind. You don't have to walk back to the den.
- **The vault counts its guests:** the crew's size is checked every second, not just when it walks in.
  - If someone leaves (by the door, the Ledger or a dropped connection), the guards still standing lose the extra health and damage they had for them.
  - If someone joins, the guards gain it.
  - The crew is told either way ("1 in the crew now - the guards ease off"). The tries you started with stay.
- **A dropped connection:**
  - If the whole crew disconnects at once, the vault waits **three minutes** before clearing, so a quick rejoin finds the heist still there. A crew that walks out still frees its vault within 20 seconds.
  - If the leader drops out while the crew waits on their call, the choice passes to the crew straight away. A leader who comes back finds it has moved on.
  - Rejoining also clears a half-finished Ledger trip or exit question.
- **Knocked out:** what you dropped where you fell is held for you (nobody else can pick it up) and comes back to your pockets once you're back on your feet in the den. Lava still takes what it takes.
- **Safe plans:** the Heist Plans bring you back to the exact spot you planned from, so they now start a heist only from safe ground. The rules are the same as the Ledger's Locker Hall trip: on the ground, not mounted or in water or lava, not hurt in the last 10 seconds, not in a boss dungeon.
  - A crewmate who isn't on safe ground isn't pulled in, or charged, and is told why. They can join with their own plans once they're safe.
- **A full city:** when all eight vault crews are busy, whoever was turned away is told the moment one frees up.
- **A full Locker Hall:**
  - While fewer than five bays are free, it's **one bay each**: nobody claims a second or third.
  - If every bay is taken and someone with no bay needs one, the Fixer frees one up: a spare (someone's second or third bay), or the bay of someone not seen for 20 in-game days.
  - The freed bay's contents go into its keeper's other bays if they fit. Whatever doesn't fit becomes **Lost & Found** crates (like The Haul), handed to the keeper the next time they step into the Locker Hall.
- **The tile floor:** the pit now runs wall to wall, so nobody can walk round the tiles along the side walls.
- **The Locker Key lives in the gutter:** you're handed one whenever you're in the gutter (the den, the vault, the Locker Hall), and it's taken back the moment you leave.
  - It can't be dropped: a dropped key is gone and a fresh one is back in your pack.
  - It can't be stored: one put in a locker bay or your ender chest is taken out.
  - It isn't kept through a death.
- **Puzzles and fights take turns:** a heist's rooms alternate between a puzzle (or a climb) and a fight: the Counting House, an Ambush or the Pit. Any room can still be an event room now and then.
- **What a room lends, it takes back:** the Shooting Gallery's bow and arrows, the Rat Ball game's snowballs and the Brawl's wind charges are taken from the whole crew the moment the room is beaten.
- **Another job, fresh supplies:** going again from the vault tops your loaned kit back up to 3 paperweights and 16 cooked beef.
- **Loaned weapons and tools never wear out:** every kit weapon, tool and shield is unbreakable.
- **No shield as a secondary:** the Tank already carries one, so the Armory's second choice is now **Slowness potions** (3 splash potions of Slowness II, to pin a crowd down). If you'd picked the shield, you get the potions.
- **Guards stay in their room:** a guard or guardian that wanders out through a door (into a corridor, the water or the room before) is pulled back to the middle of its own room.
- **The den, tidied:**
  - The shop counter is one block high, so Goldtooth, the Recruiter and the Tailor show over it.
  - The Fixer's Door now fills the den's west doorway, which used to open onto the void.
  - The den makes sure there's only one of each shopkeeper; an extra copy, from a heist that was never swept up, goes.

### For admins
- `/function bm:admin/raid_finds` gives the new items: the crates, the tip-offs, the five laurels, Forgeheart, the Alibi and the Press.
- `/function bm:admin/heist_plans_anywhere` lets the Heist Plans start a heist from anywhere again (safe ground or not); `/function bm:admin/heist_plans_safe` restores the rule.

### Fixed
- The Ledger's Office (Raid Crew) and Emma's Wardrobe button showed a developer note in their tooltips.
- "You're already in the vault" pointed at the old plates; it points at the Fixer's Door now.
- The knock-out message said your things stayed where you fell.
- **The Blueprint** (the dial lock) listed its arrows in the wrong order: the dials are read left to right as you face them now.
- **A hireling hired before 2.67** (Boomer, say) was on duty for good: their contract had never been filed, so Raid Crew couldn't switch them off. They're filed now, the first time you open the Ledger.
- Display parts stranded deep in the void (left by a follower that fell out of the world) are cleared away; enough of them could stall the server.

## New in 2.67: Democratus, Leo of the shore, after the heist (home or another job), the vault smoothed out (the Fixer's Door, three shopkeepers), follower trios, followers swim, faces that move, the Raid Crew, follower wardrobes, game night in the vault, the Frisbee Shield, the Gutter Gentry, the Arachno-Lantern

### What a heist costs, and what it pays
- **The fee rises with the tier:** 2 Tokens at Tier I, 3 at II, 4 at III, 5 at IV and 6 at Tier V (it still goes into the Lucky Pool). **Every raider pays their own fee,** not just whoever plans the heist: anyone in the party without the Tokens stays behind. The bigger tiers pay more to match: more shares, higher prize caps and the better rooms.
- **Win, and your fee comes back:** every won heist pays each raider at least their fee, with a chance of a few Tokens more that grows with the tier: 1 at Tier I, 1-2 at Tier II, 1-3 at III, 1-4 at IV and 1-5 at Tier V (see the table below).
- **Lucky Raids are rarer and only from Tier III:** one heist in 150 (three in 150 on a Lucky Night), and never at Tiers I or II. **They're harder by default:** the guards and the guardian have half again as much health, the guards hit harder, and the heist rolls one modifier more. **Win one and the pool is split evenly between the crew.** If it doesn't divide evenly, the leader takes the odd Tokens (a pool of 100 between three: 34 for the leader, 33 each for the others). A solo raider takes the lot.
- **The alarm is optional now, and off by default.** Turn it on from the tries page before the heist begins. With it on, mistakes ring it as before (patrols at 50, lockdown at 100), and you earn one more share, or two if you keep it under 50.
- **The Fixer's prize:** Tokens, Medallions and BM Trophies come from one capped roll per player per heist, never from loot tables:

  | Tier | Fee | Tokens back (for sure) | ...and the chance of more | Medallions | BM Trophy |
  |---|---|---|---|---|---|
  | I | 2 | 2 | 15% chance of 1 | none | none |
  | II | 3 | 3 | 20% chance of 1-2 | none | none |
  | III | 4 | 4 | 25% chance of 1-3 | 5% chance of 1 | none |
  | IV | 5 | 5 | 30% chance of 1-4 | 12% chance of 1 | none |
  | V | 6 | 6 | 35% chance of 1-5 | 22% chance of 1-2 | 1.5% chance |

  Fewer tries and a clean run raise the odds of the extra Tokens; a Lucky Raid always pays the most extra for its tier. Every haul (plain, Black Market or gutter) pays your fee back; the extra Tokens, Medallions and Trophies come with the Black Market haul. Daring fewer tries pays by the tier too: a little at Tier I, the full bonus only at Tier V.

### After the heist: home, or another job
- **Win or lose, the leader decides what's next.** A few seconds after the haul is paid out, or once a failed crew is back in the den, the leader (whoever planned the heist; if they've left, whoever's still there) gets a choice:
  - **Back to the Overworld:** the whole crew goes home, just as through the plates.
  - **Start a new raid:** the Heist Plans open for the leader, right there in the vault. Pick the tier and the tries, and pay your fee. Everyone else is asked to **opt in or out**:
    - **Out:** you go home as usual.
    - **In:** you come along when the leader sets the plan, and pay your own fee. Opt in without even a Tier I fee (2 Tokens) and you go home there and then; if the leader picks a tier you can't pay for, you're left behind and go home.
  - **A leader who can't cover even a Tier I fee** goes home when they press "Start a new raid", and the choice passes to the crew. A leader who picks a tier they can't afford gets the plans back to pick a cheaper one (or go home).
    - **No answer** by the time the plan is set: you go home.
- **Tokens go through the coat check.** You keep your Black Market Tokens on you in the vault, and a new raid's fee comes out of your pocket.
- **Carry on and the Fixer unpacks your haul there and then** (when the leader starts a new raid, or when you opt in). That covers the crate in your pack and any you've set down:
  - **Tokens** stay on you, ready for the next fee.
  - **Gutter Coins**, Gutter Medallions and Gutter Trophies go into your **Gutter Bank** as coins; spoils go in as spoils.
  - **Everything else** goes into your **Locker Hall bays**, then into your pack once they're full (or if you haven't claimed a bay).
  - **Bays and pack both full:** the Fixer scraps what's left for Gutter Coins, into your bank, and warns you. Heist goods fetch their Scrap Box price, Black Market currency its worth in Tokens at 32 coins each, and a few rare vanilla goods a fair price (a diamond 12, netherite scrap 16, a golden apple 6). Anything else fetches a coin a stack. Tokens that don't fit anywhere are banked at 32 coins each, and you can buy them back at the bank.
  - **Go home instead** and the haul comes with you as a crate, as ever.
- **Straight from one heist into the next, you keep your way home and your own spawn** from before the first. Your gear stays at the coat check the whole time (your Tokens stay with you).
- Closed the window by mistake? The same choices are in chat as buttons. If the leader takes the plate home before deciding, the choice passes to whoever's still in the heist.
- **A failed heist no longer rebuilds itself for free.** Another try is a new plan and a new fee, for everyone who comes.
- **Netherite Scrap** is no longer sold for coins. (2.68: it's in the Mineral Crate now.) It was a rare find in a won heist's haul: 3% at Tier I, then 6%, 10%, 15% and 22% at Tier V (+3% if nobody was knocked out).
- **Everything goes into The Haul.** Every reward is packed there. (2.68: no more building supplies in it - they're in the Raw Materials Crate.)
- **Fewer coins, bigger pieces.** The pot pays about a third of what it did and the haul's coins are halved. **Gutter Medallions** (16 coins) and **Gutter Trophies** (128 coins) are new; Goldtooth changes them either way and the bank counts them as coins. **A Token now costs 32 coins** (2 Medallions), at Goldtooth and at the bank. Goldtooth's dearest goods are priced in Medallions.
- **Three kinds of haul** (retired in 2.68 - every haul pays in money now; see above). They were picked at the den's haul lectern or in the Ledger.
  - **Plain:** vanilla goods (iron, gold, diamonds, emeralds, XP bottles, enchanted books, golden apples; ancient debris at the top tiers) and a full load of supplies.
  - **Black Market** (the default): heist gear, the Fence's curios and the Fixer's prize. Only this haul pays Tokens and Medallions.
  - **Gutter:** coins, spoils, Insignia, Medallions from Tier III and heist supplies.
- **The Scrap Box,** in the den and the Locker Hall, buys spare heist gear, curios, vault trophies, sigils and banners for coins.
- **No farming the vault.** Nothing that spawns in the vault drops loot of its own: no shulker shells, blaze rods, skulls or armour.
- Larders in about a third of the rooms (and every Rats' Rest), much more food in Endless Vault kits, and three **paperweights** in every kit to hold a golden scale down.

### New rooms
- **Game night.** Seven rooms after games everyone knows:
  - **The Shooting Gallery** *(timed):* targets pop up on the walls. Hit 6 + the tier (+2 per crewmate) in 30 seconds. Run out of time and it costs a try, then you go again. No bow? The gallery lends one.
  - **The Button Dash** *(timed):* six buttons on six perches. Press them all in time (about 33 seconds at Tier I, 27 at Tier V) or lose a try and go again.
  - **Pipe Plaza:** bonk the ? blocks for coins, stomp the Grumbas (one per jump), grab enough coins and touch the flagpole.
  - **The Block Temple:** push the stone blocks onto the gold switches (hit a block to push it away from you). Easy at Tiers I-II and properly hard at IV-V. Every layout is checked solvable when the pack is built. The button by the door resets it.
  - **The Girder Climb:** a big rat rolls barrels down the girders. Climb the ladders, jump the barrels (a coin each) and reach the gold plate at the top.
  - **The Mead Hall:** raiders, then berserkers, shieldmaidens and axe throwers, then Jarl Ironbeard himself.
  - **The Tall Grass** *(Tiers I-IV):* throw Rat Balls (snowballs) at the critters to catch them. Something wild might jump out of the grass. The Rat Center by the door hands out more balls.
- **Nether, End and Hollow rooms:**
  - **The Blaze Forge** *(Tier II+):* three waves, then the Forge Keeper.
  - **The Void Garden** *(Tier III+):* end islands, floating shulkers and three Eye shrines to wake.
  - **The Hollow Reliquary** *(rare, Tier III+):* a memory puzzle of glowing seals; solve it and each of you gets a Hollow relic.
- **The Sanctuary** *(rare):* a full heal, and a boon from one of three shrines (Strength, Speed or Resistance) once per heist.
- **The Stalker's Ward:** pitch dark, with unkillable creakings hunting you. Pull three levers to get out.
- **Party rooms:** Whack-a-Rat, Rat Says, and two contests for a crew only (Coin Scramble and Bumper Brawl).
- **Double Heists** (1 in 10): twice the rooms, two extra shares and better prize odds. **Alien Heists** (1 in 8): every room in the Vorn's white-and-cyan steel, Vorn troopers on guard, invasion loot.
- **Hidden vaults:** about a third of heists (half at Tier V) hide a secret door to a treasure room with a hoard share each. Only these hoards carry the **Rat King's Signet** (loose items come to you), **Whisperstep Boots** (sneak: unseen and quick) and the **Gilded Grin** (see in the dark).
- **The Gutter Gentry** (behind a hidden door, Tier II+): Batty, Eggbert and the Count, a three-boss fight. They're blocky, with faces taken from the art (Batty's toothy grin, the Count's empty white eyes), and they walk, run, jump and attack with smooth animations. Their hoard holds the Echo Bell, the Yolkshell Helm, Blobsworth's Cane and the Top Hat.
- **The Locker Hall,** off the den or through the Ledger: claim up to three double-chest bays and open them all with one Locker Key. The Ledger's trip brings you back to where you stood, so it only works from safe ground (see below).

### Guards and guardians
- **Twice the guards.** Every tier's roster draws on the whole hostile pool:
  - **Tier I:** Gutter Urchins, Copper Bruisers, Vault Crawlers, Coin Mites, Gutter Goo and Copper Jockeys.
  - **Tier II:** Rimelings, Silver Widows, Ex-Tellers, Iron Brutes and Vault Bats.
  - **Tier III:** Gilded Hogs, Gutter Gamblers, Gilt Wisps, Gilded Archers, Molten Coins and Golden Jockeys.
  - **Tier IV:** Abyss Crawlers, Gem Mites, Mirror Thieves, Rime Archers and a little Vault Ravager.
  - **Tier V:** Ash Imps, Reaper Giants, Ravager Riders, Gale Wardens, Hoard Turrets, Void Mites and Twin Embers.
- **Odd ones.** Any guard may turn up **Tiny** (small, quick, frail), **Hulking** (huge, slow, hits hard), **Swift** or, from Tier III, **Ironclad**. Now and then you'll meet a **Blur** (tiny and swift) or a **Juggernaut** (hulking and ironclad).
- **A second guardian for every tier.** Half of all heists meet a different one at the vault:
  - **The Mite Mother** (I) and her brood.
  - **The Widow Queen** (II): she webs you down and calls her spiderlings.
  - **The Golden Jockey** (III): a great hog with the Gambler King riding it.
  - **The Abyssal Ravager** (IV), ridden by the Mirror Mage.
  - **The Ashen Colossus** (V): a wither skeleton three men tall. He stamps the ground and calls Ash Imps.
- **A crew makes it harder:** +35% health and +10% damage per crewmate for guards, captains and champions (+50% health for the guardian), and extra guards for a crew.

### Kits and crew
- **The Ranged kit's Fairy Bow has no Infinity any more,** so the spectral arrows really get shot. You start with 64 arrows and 32 spectral (64 at Fletcher). Every room you enter has a quiver just inside the door for each Ranged raider (theirs alone to pick up), and every room you beat slips them 8 more.
- **Health over heads:** in a heist, every raider's health floats above them, and the heart turns yellow, then red, as they get hurt. It's hidden while they're invisible.

### The Frisbee Shield
A rare find in the vault: shiny guards, loose bricks, champions, the Rat King, or one Shooting Gallery in twenty. It blocks like any shield. **Sneak + use to throw it:** it skips off walls and floors and off monsters, hitting each monster once and then heading for the next one near. After five skips it flies home to the hand it left. If you're gone, it drops where it is and waits. It goes through the coat check with you.

### Democratus, the storm reaper
- **In a thunderstorm, very rarely,** lightning strikes near someone out under the open sky, and where it fell a hooded warrior kneels in vigil: green cloak, mint hair, violet eyes, one fist on the haft of his great electric scythe, stood upright before him, the other forearm across his knee. He keeps his vigil while the storm lasts. **Right-click him** and he gives you his **Storm Seal** and walks with you (achievement *Eye of the Storm*).
- **Taller and broader than Leo,** blocky but less boxy: a stepped hood with a curled peak, a layered beard, ragged cloak strips and a jagged-edged breastplate. **His pupils glow violet in the dark,** like a glow squid.
- **Built like a warrior:** a V-shaped frame of cobbled plates (broad shoulders, a deep plated chest, a narrow waist), heavy pauldrons, thick forearms and gauntlets, and solid armoured legs. He carries the scythe over his left shoulder, the shaft rising past his pauldron and the blade arcing out above his head, clear of his body. Kneeling in his vigil, his left elbow bends forward to grip the planted shaft and his right forearm rests across his knee. His head stays upright on his shoulders whichever way he leans.
- **The storm is his:** out in the rain (under the open sky) he's stronger, with Resistance and harder blows: the sweep 20, his lightning 12, the slam 15. **In a thunderstorm** he's stronger still: Resistance II and Regeneration, the sweep 26, lightning 15, the slam 18, and every blow charges him twice. A line under your hotbar tells you when the weather turns him. The duel goes the same way: challenge him in a thunderstorm at your peril.
- **Slow, devastating blows:** a great sweep of the scythe every 2.5 seconds (16 damage, 8 to anything beside it). He plants his feet for each one. Every blow charges him, and at five comes his **Storm Reap**: he spins the scythe round him, the monsters near are lifted off their feet, lightning comes down on each one, and he slams them into the ground with a thud you feel.
- **Old Rivals, with Cecil:** you hit harder (Strength), Cecil is tougher, and Democratus charges twice as fast, out to outdo him (they glare). **The Storm's Heir, with KillerWatt:** you're quicker (Speed, Jump Boost), KillerWatt is tougher and charges faster, and Democratus regenerates. **With both:** Resistance for you as well. Each pairing has its own banter and hidden achievement.
- **Like the others:** an item frame, right-click him to sit, 5 minutes if he faints, his face moves (smirks, glares, a grimace when he's hurt), Emma's pulses reach him, and a raid contract at the Recruiter.
- **His challenge:** sneak + use the seal for his menu: **Duel him**, his wardrobe, or send him home. Duelling, you get **ten seconds to put some distance between you**, then he fights you for real: 400 health, heavy sweeps, a lunging slash, lightning called down where you stand, and his Storm Reap. **Drop to three hearts** (or fall, or run more than 64 blocks) and you've lost: he simply goes home, to be called again, and **challenged again right away, with no cooldown**. **Bring him to his knee and you win:** the first time, **Democratus' Scythe** is yours (achievement *Reaper's Due*). It's one per player; later wins earn only his respect.
- **His scythe:** heavy and slow (15 damage, a long reach). Every blow arcs lightning to two monsters close by and charges the blade, and at eight charges you unleash a **Storm Reap** of your own.

### Leo, the knight of the shore
- **Seawatch forts:** a small stone fort now and then stands on a beach (sandy, snowy or stony shore), with a watchtower, a signal fire and a blue banner. **Leo** keeps watch inside. The drowned have been coming up the beach at his walls all week.
- **Defend the fort:** talk to him, then right-click him holding a **sword or a trident**. Three waves of drowned in turtle shells come up the beach; the third brings their **Tidecaller**. Leo holds the gate with his trident. If everyone falls back more than 32 blocks the defence is lost and you can try again. Win and he gives you **Leo's Crest** (and the fort's chest is yours; achievement *Hold the Line*).
- **Leo's Crest:** use it to call him or call him back; sneak + use opens his menu (send him home, or his wardrobe). 50 health and good armour; if he faints, the crest rests 5 minutes.
- **He fights with a trident:** a thrust up close (9 damage, with a little sweep), and at range (6-14 blocks) he throws it. It comes back to him (Loyalty), and in a thunderstorm it calls down lightning (Channeling), never within 6 blocks of you.
- **Strong but caring:** drop to 4 hearts with a monster about and he's at your side, on guard. The monsters around you turn on him, and you get Resistance II and some absorption (30 seconds to recover). In a fight with him close by: Resistance I. **While he's with you, you breathe underwater** (no particles, no fuss); in the water with him you swim like he does (Dolphin's Grace).
- **With Celi, Steel and Frost:** you get Strength, he covers her (Resistance), and his thrusts freeze like her spear. **With Emma, the Knight's Vow:** you regenerate, he shields her (Resistance II), and his guard comes back twice as fast. **With both:** Speed as well. Celi bickers, Emma cheers, and he smiles. Each pairing has its own hidden achievement.
- He has his own raid contract at the Recruiter (1 Gutter Trophy and 5 Medallions).
- **Right-click him to sit him down** (or stand him up): he sits on the ground leaning back on one hand, the trident across his knees, breathing, looking out to sea, and now and then standing the trident up beside him like a staff.
- **He can be hung in an item frame** like Cecil, Emma and Celi: put his crest in a frame and he lives by it (right-click the frame: sit / stand; sneak + right-click: in / out).
- He animates: a watchful idle with an eye on the sea, a steady stride, a levelled charge, a salute when he arrives, the thrust, the throw, and on guard.

### Followers swim
- **In deep water every follower swims** instead of standing in it (Wilfrey excepted: he's a plain wither skeleton). They sink to the chest and paddle, and each in their own way:
  - **Emma:** a happy dog-paddle, chin up.
  - **Celi:** her spear held high out of the water (she is *not* getting it wet) and a grudging one-armed paddle.
  - **Leo:** a strong crawl, his trident levelled ahead like a lance.
  - **Democratus:** a heavy one-armed stroke, the scythe held up out of the water in his other fist (he never lets go of it), his cloak floating out behind.
  - **Cecil:** he hates it. His staff is held up out of the water while he paddles furiously, rocking side to side.
  - **KillerWatt:** a four-armed breaststroke, the tendrils stroking a beat behind.
  - **Zib** and **Donado** paddle with their tails as rudders, and the **Frog** does a proper frog kick.
- Wading in the shallows is still walking: the swim starts once their feet leave the bottom.

### Three together: follower trios
With three particular followers at your side at once (within 24 blocks), you get something more than the pairs:

| Trio | Who | For you | For the three |
|---|---|---|---|
| **The Serpent's Bane** | Emma, Leo, Cecil | Regeneration, Resistance, and a shield of Absorption II that comes back every 30 seconds | Strength and Regeneration |
| **The Storm Court** | Cecil, Democratus, KillerWatt | Strength II and Speed | Resistance, and another charge every 4 seconds for their charged attacks |
| **The Princess's Guard** | Emma, Leo, Celi | Health Boost (two more hearts) and Regeneration | Resistance |
| **The Odd Ones** | Emma, Cecil, KillerWatt | Speed II, Jump Boost and Haste | Regeneration, and Emma's charge fills faster |

- A trio's buffs come on top of the pairs' (Old Rivals, the Knight's Vow and the rest still apply).
- Each trio has its own banter every couple of minutes and a hidden achievement the first time it forms.
- No trio in the vault: a heist allows two followers at most.

### Faces that move
- **Emma, Celi, Cecil and Leo blink**, and their expressions change with their mood and with what's going on:
  - **Hurt:** a hit shows on the face for a moment: Emma's and Cecil's > <, Celi's angry squint, Leo's gritted teeth.
  - **Fighting** (a monster within 10 blocks): serious. Emma lowers her lids, Celi bares both fangs, Cecil's slits narrow and Leo sets his jaw.
  - **Low on health** (a third or less): Emma looks sad, with a tear; Celi is furious; Cecil and Leo turn grim.
  - **Calm, each their own way:** Emma blinks often and beams or winks at you now and then. Celi blinks fast, cuts her eyes away (tsk) and huffs. Cecil spends a lot of time half-lidded and deadpan, rolls his eyes and gives you a sly look. Leo blinks slowly, smiles when you're close, and looks worried when *you're* hurt.
  - **Arriving:** Emma beams, Celi tsks, Cecil rolls his eyes, Leo smiles. Emma also beams when her healing lands, and Celi tsks after a kill quip.
  - **Startled:** the moment a monster first comes within 10 blocks, all four look surprised (wide eyes, brows up, a little "o") before their fighting face.
  - **Sleepy:** tell them to sit at night with nothing the matter, and their lids grow heavy.
- **KillerWatt's maw moves too:** it snarls in a fight, clenches when he's hit, gapes open as he strikes or arrives, and now and then, calm, twists into a lopsided smirk. It works in all ten of his forms; the boss snarls at anyone within 20 blocks.
- **Rufus Gnaw, the Mercenary,** no longer glides along like a statue: he bobs and sways as he walks, breathes while he stands, and leans into a fight.
- **Pearlman** follows you with his eyes smoothly instead of turning in a jerk once a second.
- **Emma walks and runs playfully now:** her arms swing out wide from her sides, her hands flare, and each foot steps in front of the other.

### The vault, smoothed out
- **The way out asks first while a heist is on.** Step into the Fixer's Door mid-run and you're asked: leave now (your share stays behind, and the crew carries on) or stay. Before the heist begins, after a win or after a fail, it's instant as ever. Standing in the door asks once; step out and back in to be asked again.
- **The Fixer's Door** replaces the old exit plates. It's an archway in the tier's metal with a swirl you walk into: in the den against the west wall, and in the treasury against the far wall (it starts swirling once the vault opens).
- **Nobody has to wait on the leader.** When a heist ends, the crew get their own card: **Head home now**, or **I'm in if we go again**. Say you're in and you're taken along without being asked again (you pay your own fee then).
- **A leader who hasn't chosen in 75 seconds** passes the choice on to the crew. A solo raider takes as long as they like.
- **Closed the card?** Use the Fixer's Ledger: while the choice is yours it opens again. Its Office button carries on to the Office.
- **One card at the end.** The payout's string of chat lines is one line now ("Heist won! The Haul: 5 Tokens, 23 coins"). The end-of-heist card, the leader's and the crew's, opens with how it went: won (the tier, your shares, Tokens, coins, any Medallions or a BM Trophy) or failed. It comes up three seconds after the payout. The Lucky split, first clears, Shifting Cores and BM Trophies still go to chat.
- **The den, laid out by job:**
  - **The market counter** (south-west): Goldtooth, the Recruiter and the Tailor stand behind it, with nothing behind them.
  - **The office counter** (north wall): the Gutter Bank, the Armory, the haul lectern and a new **Raid Crew board** side by side.
  - **The Lockers** are through a copper door on the north wall (right-click it), well away from the way out.
  - **"Back to the crew"** is a plate you can see, by the far door.
- **Three shopkeepers** instead of one Goldtooth with 101 trades:
  - **Goldtooth** keeps the heist supplies: tools, potions, food, spoils, Bond Sigils, the Ledger and a Token.
  - **The Recruiter** sells the Raid Contracts, the hirelings' contracts and the vault gems.
  - **The Tailor** sells the follower outfits and the display cases from a menu that shows what you own. Pick a follower, then an outfit, and it's in their wardrobe for good. (Holding that outfit already? It tells you to use it instead.) The Tailor takes coins from your Gutter Bank and your pockets (a Gutter Medallion counts as 16, a Trophy as 128), and the change goes into your bank.
  - Goldtooth no longer changes coins; the Gutter Bank does that.
- **The Raid Crew page says where everyone is:** IN THE VAULT, RESTING (with the seconds left), WAITING (crew full), ON THE WAY, ON, OFF or no contract. On a heist it also shows "2/2 with you now".
- **Who comes first** is whoever you switched ON first. Switch one off and on again to send it to the back. The page lists them in that order, then the OFF ones, then the rest. If the crew is over the limit (someone joined your heist), the one last in line goes home.
- **Your Overworld followers wait outside.** A follower you leave behind going into a heist says it "waits outside the vault", and three seconds after you're home again it's called back to you (if it isn't resting and you're under the cap).
- **BEGIN has a ready check.** It starts the heist at once only if everyone has a kit and nobody's at the Lockers. Otherwise it names who isn't ready; press BEGIN again within ten seconds to go anyway (anyone without a kit takes the Offense loaners, as before).
- **The Ledger's Locker Hall trip has rules.** The Office pages still open anywhere, but the trip to the Locker Hall brings you back to the exact spot you left, so it only starts from a safe one:
  - the Overworld, the Nether or the End (not the Hollow, and not the gutter itself);
  - standing on the ground: not falling, flying, climbing, mounted or in water or lava;
  - not hurt in the last 10 seconds (it tells you how long to wait);
  - not inside a boss dungeon.
  - Then **hold still for 3 seconds** (a countdown shows on the action bar). Moving or getting hurt cancels it. Each refusal says why.
  - The den's copper door to the Lockers, before a heist begins, works as before.

### Follower wardrobes
- **An outfit is yours for good:** use a cosmetic once and it's unlocked in that follower's wardrobe (the item is used up).
- **Every follower has a menu:** sneak + use their own item, any time in the Overworld, whether they're out or not. From it you can send them home, or change them into any outfit they own, or back into their own clothes. Locked outfits say where to get them. With Emma out, sneak + use still opens her buff menu, which now has a **Wardrobe** button; Democratus' challenge menu has one too.
- **New at the Tailor** (Goldtooth sold them before 2.67d):
  - **Leo's Tabards:** Crimson Crusader, Royal Purple, Greenwood.
  - **Democratus' Cloaks:** Crimson Reaper, Ashen Shroud, Royal Violet. His hood changes with his cloak, and his face still moves on it.
  - **Cecil's Robes:** Crimson, Midnight, Bone.
  - **KillerWatt's Colours:** Midnight, Bone, Neon.
  - Each set has a rare hidden fourth (Golden Champion, Gilded Storm, Gilded and Golden Thunder) for 128 coins (a Gutter Trophy's worth). The rest cost 64 coins (4 Gutter Medallions).
  - Cecil's robe and KillerWatt's colours are their own look: with a gem in them, the gem's element shows instead, and the outfit comes back when the gem comes out.
- Every follower keeps their cosmetics through a recall, being sent home and called again, a new support role (Emma) and a rebuilt rig.
- **Emma's ethereal form keeps its own armour and wings.** Your outfit choices are for her normal form: when she comes back down she's wearing them again (dress her while she's ethereal and she changes when she lands). The Cozy Sweater now shows her support role's colour too, with a heart pin.

### The Ethereal Gem
- **Goldtooth no longer sells it.** It's a hidden prize again: hold all nine elemental gems and use one, and they rise and circle you and fuse into the **Ethereal Gem** in your hands (or set all nine on display, as before). Achievement: *Nine Made One*.
- **One Ethereal Gem per heist:** the first raider through the door keeps one. Any others (and any brought in later in the same run) are held in your coat-check bag until you leave.

### Followers in the vault: the Raid Crew
- **Raid contracts** at the Recruiter: once signed, Cecil, Emma, Celi, Leo, Democratus, Zib, the Skiff Escorts or KillerWatt can come into the vault. The **Frog** and **Donado** contracts bring a vault hire in his own iron kit; the one you hired at home stays home.
- **The Fixer's Ledger has a Raid Crew page.** Every follower you've signed for, every vault hire and every hireling you've hired is listed, each switched **ON** or **OFF** with a click. On a heist the ones switched on come along by themselves (and come back after a faint once they've recovered); switch one off and they go home. Hirelings are one at a time, as before.
- **Summoning items stay at the coat check:** the ledger is how your crew comes in.
- **Contracts are filed:** a hireling's or vault hire's contract, used once, goes into the ledger and isn't needed after.
- **A party raids light:** one follower each when two or more of you go in, two when you raid alone (a hireling doesn't count). If someone joins mid-heist, the extra follower heads home.
- **Leave the heist, any way at all, and the raid crew goes home there and then.**
- **Raid followers are back sooner:** one who faints in the vault comes back after 45 seconds instead of 5 minutes (a heist can be over quickly). Outside the vault it's still 5 minutes.
- **The followers' wardrobe** at the Tailor: Emma's ribbons and dresses, Celi's and Zib's outfits (the hidden ones for 128 coins). Pearlman's gems are at the Recruiter.
- **Emma's new outfits:** the Flower Top and the Cozy Sweater, each with a high ponytail.

### The vault's own rules
- **The kit is on loan:**
  - Loaned armour is bound to you until the heist is over (Curse of Binding).
  - Loaned weapons and the rest of the kit bounce straight back into your hands if you drop them.
  - Kit gear is pulled back out of lockers, your ender chest, bundles, boxes and The Haul.
  - Only the paperweights and food can be put down.
- **The Locker Hall:** an unclaimed bay is locked; claim it first.
- **Vault gems:** the gems the Recruiter sells belong to the vault and stay in it.
  - They're taken at the door on the way out.
  - They can't be set down as decorations or fused.
  - Hand one to Cecil or KillerWatt and take it back, and you get the vault gem back.
  - When you leave, the element a vault gem gave them fades.
- **The Haul folds up:** set one down, open it, and walk away. Emptied, it simply vanishes; with something still in it, it folds back into your pack. Broken by hand, what's inside spills out, but the barrel itself never ends up in your pockets.

### KillerWatt
- **A better rig:** his head and arms follow his torso, his head no longer tips too far back, and his tendrils are animated. They're shaped like lightning now: hard, angled bends that carry them out around his chest, so they strike in front of him without cutting through it. **The Tendril Lunge:** he coils all four scythes back and drives them at you.
- **He goes out with an explosion of electricity.**
- **He reacts:** the follower roars as he arrives, flinches when he's hurt, swipes his tendrils at a monster in bite reach and spreads his arms when he's in the air. The boss flinches when you land a hit while he's between attacks, and up close he throws a quick right-left jab. The pose of the rider's Thunder Leap now holds all the way to the landing.
- **The follower's charged attacks:** every blow charges him, and at full charge he unleashes his form's attack (riding, the Spark lets it go when you choose). Stormbreaker, Supernova, Maelstrom, Plague Bloom, Tectonic Slam, Avalanche, Tempest, Overgrowth, Absolute Zero and, in his Ethereal Form, Void Requiem.
- **Ethereal KillerWatt:** set down an Ethereal Gem near him mid-fight and he ascends. He heals whole with far more health, hits harder and faster, floats, and throws Void Lances. Beat that form for the **Ethereal Tendrils** (instead of his plain Tendrils; his Spark and hoard as ever), which hit half again as hard and fling you half again as far.

### The Scorching Arachno-Lantern
On a Blood Moon, very rarely, a monster spawning under the open sky becomes the **Arachno-Lantern**: a burning pumpkin the size of a house on eight long legs. It's blocky like the Gutter Gentry: the pumpkin in square tiers with ribs down its sides, its face carved square-cut, square legs and square flames. It glares with red crescent pupils (wide U's, horns up), breathes fire from the corners of its mouth, stomps, lashes you in with its tongue, rains embers and, at half health, shrieks out ember spiderlings and glares fire. It drops the **Scorching Heart**: carry it and fire can't touch you, or set it down as the **Hearthfire** (no monster spawns within 48 blocks, and Blood Moon horrors near it burn).
- **Its legs never pass through each other or the fires.** They come out of the pumpkin's sides now, the front pair highest, so they rise over the fires at the corners of its mouth instead of through them. It walks in a wave, each leg stepping a little after the one behind it, the way a spider does, so neighbouring legs never swing into each other.

### For admins
`/function bm:admin/heist_double`, `heist_alien` and `heist_variants_off` / `heist_variants_never` force the heist variants; `heist_boss_alt` / `heist_boss_std` / `heist_boss_any` pick the guardian; `room_<kind>` (e.g. `room_temple`) lays that event room next; `frisbee` gives the Frisbee Shield. `leo` puts Leo's fort encounter in front of you, `leo_fort` builds a seawatch fort where you stand, `leo_crest` gives his crest, and `faces` runs every follower nearby through each of their expressions. `democratus` puts Democratus' storm vigil in front of you (it needs `/weather thunder`); `demo_seal` and `demo_scythe` give his seal and his scythe. `wardrobe_all` unlocks every follower outfit, `wardrobe_items` gives the new ones, and `contracts_all` signs every raid contract.

### Fixed
- **Emma and Leo keep their heads up while they swim:** their heads tipped back behind their shoulders; now they sit level, chin up, looking ahead.
- **Emma's upper arms no longer sit inside her chest:** her shoulders are a little wider apart, and her hands still meet in front of her.
- **A Rats' Rest is never the first room of a heist** (there's nothing to rest from yet), and **a heist has one rest room at most**: a Rats' Rest or the Sanctuary, never both and never two. (The Endless Vault keeps its own cash-out Rest every fifth room and draws neither.)
- **Celi and Leo count toward the three-follower limit** (they slipped past it); so does Democratus.
- The Gutter Bank and Armory click boxes and signs sat half a block off-centre.
- The Locker Hall no longer sends visitors who aren't in a heist home.
- The Crumbling Rafters' edges are closed.
- **Found by playing every tier through, five times each:**
  - **The Fixer's prize keeps to its caps.** An older, richer table was still in charge: a Token 45% of the time at Tier I, up to 4 Tokens and 2 Medallions at Tier IV. It now pays what the table above says.
  - **The Girder Climb opens its door.** Reaching the gold plate at the top beat the room but left the exit barred. **Pipe Plaza** did the same if you walked into the flagpole instead of hitting it.
  - **The fourth coffer's Mimic** dropped a full Mimic's loot in the vault (Tokens, a Medallion, accessories). Like the other three, it drops nothing now.
  - **A follower can't jam the Block Temple.** A follower or hireling standing where a block was going stopped the push; now it steps back beside you.
  - **Odd guards wear their names.** Tiny, Hulking, Swift, Ironclad, Blur and Juggernaut guards lost the prefix on their name.
  - The server log no longer fills with an error for every item frame in the Combination Room and the Dial Lock.
- **Found by reading the code through:**
  - **Your weapons no longer hit your own followers.** Every weapon and spell that skips "friends" had its own list of who that meant, and the newer followers were missing from most of them. KillerWatt, Zib, raid hirelings and Skiff Escorts were missing from all of them, Celi and Leo from about half, and the Mercenary was listed under the wrong name. Now one list covers everyone, and new followers join it automatically.
  - **The Hex and Keep sequence puzzles:** their two highest buttons played the same note, so the melody to copy was ambiguous. Each button has its own note now.
  - **Zorp sells the Vorn Green paint kit**, so a skiff you repainted can go back to its own colour.
  - About 80 leftover functions from features that were later rewritten are gone, along with a few dead checks.
- A Lucky Raid's pool pays out whichever haul you picked (it's the crew's fees coming back), so a plain or gutter haul can carry those Tokens.

## New in 2.66: the Fixer's Office, metal trophies, Bond Sigils, KillerWatt rides

### The Fixer's Office
Everything the vault owes you, in one set of menus. Open it with **the Fixer's Ledger** (everyone gets one on their first heist; Goldtooth keeps spares for 1 coin), or use the two new stations in the den beside the kit racks: **the Armory** bench and **the Gutter Bank** vault.

- **Spoils.** The vault's guards now carry the materials for your upgrades. About one in three drops its tier's spoil: **Copper Cogs** (Tier I), **Silver Seals** (II), **Gilded Leaves** (III), **Deep Pearls** (IV) or **Hoard Embers** (V). Captains, champions and guardians drop more, for the whole crew, plus **Captain's Insignia**. Like the pot, spoils are only yours if the crew gets out. At the payout they go straight into your bank.
- **The Gutter Bank** keeps your coins and spoils under your name. Deposit everything in one click, take coins (16, 64 or all) or any spoil back out, and **buy Black Market Tokens at 16 coins each**. The Armory and the bank pay from your bank first, then from your pockets.
- **The Armory: permanent kit ranks.** Every loaner kit has six ranks, each leaning further into its job. Clearing a tier unlocks the next rank (Tier I opens rank II, and so on up to Tier V and rank VI). Then pay in coins, that tier's spoil and Insignia:

  | Rank | Coins | Spoil | Insignia |
  |---|---|---|---|
  | II | 32 | 10 Copper Cogs | 0 |
  | III | 64 | 12 Silver Seals | 1 |
  | IV | 112 | 12 Gilded Leaves | 2 |
  | V | 176 | 12 Deep Pearls | 3 |
  | VI | 256 | 12 Hoard Embers | 5 |

  Ranks are yours for good and apply to every kit you take.
  - **Tank:** Reinforced (Juggernaut II, +12 health) · Spiked Guard (attackers take damage back while you sneak; Horn every 24 s) · Bastion (Juggernaut III; the Horn shields the crew) · Last Stand (+16 health; once a heist, at 4 hearts, Resistance IV and Absorption IV) · Colossus (no knockback; the Horn hurls guards back).
  - **Offense:** Keen Edge (Shadowstep II; Bloodrush heals more) · Executioner (+5 damage to foes under a third of their health; Charm every 14 s) · Ambush (Shadowstep III; the blink strikes for 8) · Bloodlust (Strength II; every fourth hit is a sure critical) · Phantom (unseen after the blink, and your next hit deals +10).
  - **Ranged:** Fletcher (64 spectral arrows plus 8 arrows of Harming) · Wide Volley (7 arrows, every 10 s) · Searing Shots (Flame on the Fairy Bow) · Hawkeye (Speed II; bow hits heal you) · Storm of Arrows (volley arrows hit twice as hard and pierce two foes).
  - **Support:** Tidewater (Tidecaller II; a wider, stronger aura) · Spring Tide (Ward every 16 s, and it speeds the crew) · Undertow (Tidecaller III; Lifeline catches crewmates) · High Tide (the Ward gives the crew Resistance and Strength; 5 potions) · Tidal Wave (the Ward hurls guards back and heals twice as much).
- **Your secondary and your signature.** Whatever kit you take, add one weapon and one effect of your own. More options open as you clear tiers, and you can change them freely.
  - **Weapons:** a Crossbow, Slowness potions (a Shield before 2.68b), Wind Charges, a Trident, an Iron Spear, Harming potions, a Diamond Spear or a Mace.
  - **Effects:** Fleet-Footed, Iron Skin, Cat's Eyes, Featherfall, Leech, Spring-Heeled, Fortune's Favour, Second Skin or Adrenaline.
- **More for gutter coins at Goldtooth:** a Token for 16, Ender Pearls, Golden Carrots, Golden Apples, and better goods for coins plus spoils (XP bottles, Diamonds, an Enchanted Golden Apple, Netherite Scrap, a Totem of Undying).

### Trophies in six metals
- There are twelve trophy rooms now (the original seven plus the Signal Lamps, Lamp Floor, Tumbler Lock, Bell Tower and Crumbling Rafters), each in six metals:
  - **Copper** for a flawless clear on Tier I, **Iron** on II, **Gold** on III, **Emerald** on IV and **Diamond** on V.
  - **Netherite** needs Tier V with three tries and nobody knocked out all heist.
- **Harder to earn.** A flawless room only *promises* its trophy. You get it at the payout if the crew gets out, and lose it if you're knocked out along the way. You can own one of each room and metal; a duplicate pays 3 coins into your bank instead.
- **3D statues.** Each trophy is a little cup on a plinth bearing the room's emblem, grander metal by metal: handles, a lid, a gem, a star and finally a netherite crown with an ember. Sneak + use to set one down; sneak + punch to pick it up. The old gold trophies now look like the new gold ones.
- **Full shelves.** Completing all twelve rooms in one metal pays BM Trophies, once: copper 1, iron 2, gold 3, emerald 4, diamond 6, netherite 10. The **Trophy Case** page in the Office shows your whole collection.

### Bond Sigils: eight powers, two per heist
- **The sigils:** **Mending** (regeneration), **Fury** (Strength), **Bulwark** (Resistance), **Swiftness** (Speed), **Warding** (no poison, wither, slowness or burning), **Fortune** (+1 coin a guard, and more spoils), **Vigor** (+2 hearts) and **Sight** (night vision; guards glow).
- **How they attune:** when the heist begins, the sigils your crew carries are attuned, off-hands first and then pockets, **two at most**. Their powers apply to the whole crew for that heist. The Office's **Bond Sigils** page shows which are attuned.
- **Where to get them:** Mending still comes free with your first party heist. Goldtooth sells all eight for coins and Insignia, and champions and hidden stashes sometimes drop one. Outside the vault, Mending still mends your party.

### KillerWatt, the follower, grows up
- **Ride him.** Use the Spark beside him to climb onto his back.
  - He goes where you look; walk to stride and jump to hop. He fights while you ride.
  - A wall ahead is no obstacle: he climbs it on his tendrils.
  - **The Spark while riding: Thunder Leap.** He jumps up and forward and slams where he lands.
  - Sneak to get off.
- **New fighting:**
  - **The Tendril Stab:** the scythes drive down and pin a foe, then he lands a right and a left.
  - **The Leap:** he crouches, then comes down on a foe a little way off.
  - **Chain Lightning:** arcs from his hands strike three foes at once.
  - He still slams and calls lightning, and **he climbs walls to follow you**.
- **His element.** Right-click him with one of Pearlman's gems. His hide takes its colours and every blow gets its touch: fire burns, water slows, poison poisons, earth roots, rock weakens, air throws foes up, grass heals him, ice freezes. Electric is his own element. Sneak + right-click him empty-handed to get the gem back.
- **The Ethereal Gem** gives him his **Ethereal Form**: metallic black, iridescent tendrils, glowing seams and jagged spikes. He hits **half again as hard** and **floats**, and **when ridden he flies**: look up to rise, down to sink.

### Fixed
- The vault dimension's silent background music named a sound the game didn't recognise, so a server starting fresh with the pack could refuse to load the world. It's now defined inline, and the checker catches this mistake.

## New in 2.65: the Vault rebuilt, KillerWatt, follower wardrobes

### The Gilded Gutter Vault, rebuilt
The heist is now a proper dungeon run: non-linear, different in every tier, full of surprises, and playable solo.

- **Tries: 3, 5 or 7.** After picking a tier you choose how many knock-outs your crew can take (each crewmate past the first adds one). **Fewer tries pay more:** +4 shares for 3 tries, +2 for 5, and +2 more for a run with no knock-outs (+1 for just one). Run out and **the heist fails**: everyone goes back to the den, everything gathered is lost, and the Fixer draws up a fresh plan.
- **The fee and the Lucky Pool.** The Fixer charges 3 Tokens a head, once per heist (stepping out and back in is free), and every fee goes into the **Lucky Pool**. One heist in twenty (one in seven on a Lucky Night) is a **Lucky Raid**: win it and the crew splits the pool.
- **The pot.** Guards drop nothing now. They pay into the crew's pot (watch the boss bar), as do secrets, rare foes and trophies you've already earned. Everything goes into The Haul at the end, but only if you win.
- **Respawn in the den.** Your spawn point is moved to the den for the heist and restored the moment you leave (your bed, or world spawn). The emerald plate takes you back to the last door you opened.
- **The way through bends:** passages climb and drop, turn left and right, run up a ladder shaft, plunge into a pool and cross a chasm on stepping stones. **Every tier is built in its own stone** and has its own crew of guards, no longer only vindicators: Copper Thugs and crossbowmen at Tier I; Silver archers, strays, enforcers and alchemists at II; drowned divers, bog archers and breezes at IV; wither-skeleton reavers, blazes and conjurers at V. Each tier also has a captain and a guardian of its own (the Copper Foreman, the Silver Marksman, the Drowned Treasurer, the Gutter King).
- **New rooms:** the Signal Lamps (repeat the sequence), the Lamp Floor (light all nine), the Tumbler Lock (time the gate), the Bell Tower climb, the Crumbling Rafters, the Arcane Study ambush and the Champion's Pit (the Gold Ooze, the Bone Duelist, the Vault Ravager, the Illusionist, the Twin Gales, and very rarely **the Rat King**).
- **Random events:** the **Rat Rave** (stand on the DJ's colour when the beat drops), the **Rats' Rest** (a tavern with a peddler; get knocked out after it and you wake there), the **Storm Vault** (pull three levers while dodging lightning), a **Vorn Landing** (smash the saucer's cores) and the **Enchanted Grove** (catch the wisps).
- **Secrets and rarities:** loose bricks (right-click a cracked block) hide coins, rare finds or a **Phantom Thief** who runs off with your pot. Look out for the **Coin Rat** and **shiny guards** (1 in 150). Hidden gear only drops from these: the **Phantom Regalia** (invisible while sneaking, soft falls), the **Gutter Master Key**, the **Lantern of Lost Things** and the **Lucky Rat's Foot**.
- **Kits that fight like their gear:** the Tank's **Bulwark Horn** (shields you and the crew, slows guards), the Offense's **Shadowstep Charm** (blink forward, unseen, Strength; kills give a burst of speed and healing), the Ranged kit's **Volley Quiver** (five arrows; the Fairy Bow pins what it hits) and Support's **Tidal Ward** (heals, shields, cleanses; Lifeline when you fall low).
- **Hirelings** (contracts from the Recruiter, yours for good, but they never leave the vault): Knuckles the brawler, Doc Whiskers the medic, Fingers the pickpocket, Tick-Tock the turret and Boomer the demolitions rat.
- **Two new modes** (after a Tier I clear): **the Endless Vault**, where rooms never end and get harder and richer every four, with a cash-out plate at every fifth room's Rest; and **the Pit**, an arena of waves with a guardian every fifth and a cash-out plate between waves.
- **Music and ambience:** every tier has its own track, plus themes for the guardian, the Rave, the Rest and the Pit, along with room ambience.
- **Goldtooth's new stock:** Healing Draughts, Second Wind (+1 try), a Treasure Map Scrap, the Golden Compass and the Fixer's Lucky Purse.

### Fixed
- **Respawning in the vault** puts you in the den, not back at world spawn.
- The **dial room** has a button again, and the **clockwork room's signs** no longer overlap.
- The **Gutter Laurel, puzzle trophies and the Bond Sigil** are given once each. After that they pay coins into the pot. **The Bond Sigil** now works with your party: you both regenerate near a party member carrying one.
- **The den** only heals before the heist starts and after it's won, not during the run.

### KillerWatt
- **The Storm Effigy** (Cecil sells it): use it outdoors in a **thunderstorm** and KillerWatt crashes down in front of you. It does nothing in clear weather or under a roof.
- **The fight:** a four-and-a-half-block storm brute with smooth animation throughout. He breathes and sways standing, strides as he walks, and winds up before each blow. His attacks:
  - **Thunder Slam:** a shockwave around him.
  - **Tendril Sweep:** a wide scythe circle.
  - **Call Lightning:** sparks gather under you. Move, or the bolt hits.
  - **The Roar** at half health: throws everyone back, summons Static Wisps, and makes him faster from then on, with bolts falling around his slams.
  He gets tougher with each player fighting him, and leaves if nobody's near for a minute.
- **The reward:** his **Tendrils** (no longer sold by Cecil) and **KillerWatt's Spark**, both certain on your first kill and a chance after, plus Medallions, Trophies and Tokens.
- **KillerWatt's Spark** makes him a follower: a three-block KillerWatt who slams monsters that come close and calls lightning onto ones further off. He counts toward your three followers, goes home if you go far or put the Spark away, and rests 5 minutes if he falls.

### Follower wardrobes (Madame Velour)
- **Emma:** five ribbons (Gold, Midnight, Mint, Snow, Crimson) and four dresses (Sundress, Midnight Gown, Sakura, Royal Gown). Her scarf still shows her buff's colour.
- **Celi:** the Aurora, Rosehip and Midnight outfits. **Zib:** the Crimson Guard and Forest Ranger uniforms.
- **Hidden ones** drop only from the vault's rare foes and secrets: Emma's **Phantom Ribbon** and **Starlight Gown**, Celi's **Frostfire** outfit and Zib's **Golden Ace** uniform.
- Use one while they're out to dress them. Items are kept, so you can switch back and forth. Sneak + use returns them to their own clothes. Outfits stay on the next time you call them.

### Prices
2.63's half prices were too cheap. Prices are now **70% of the old list** (Trophies, Blood Crystals, Lucky Tokens), and the Scrap Bin follows. Unchanged: a Diamond is still 2 Tokens at the Fence, Heist Plans 3 Tokens, and Pearlman's gems a Medallion.

## New in 2.64: heist fixes, a tidier haul, fairer kits

### Fixed
- **The guardian no longer vanishes when you're knocked out.** The cleanup for far-away mobs was removing the vault boss while you were briefly away, and the vault then opened as a win. It now ignores everything in the vault; a heist cleans up after itself.
- **Party members come too:** re-planning your party's unfinished heist brings everyone in the party within 24 blocks, not just the leader.
- **No Mimic loot in the vault:** the Three Coffers' Mimics drop nothing, so there's no reward for picking wrong.
- **Buttons you can see:** every heist button is now **pale oak** on the dark stone, with a glowing label above it (BEGIN, TRY THE LEVERS, PEEK). Each room also places its button again as it sets up.
- **The guardian can be knocked back.** Its knockback resistance is gone (the Netherite-armoured guardian keeps a little from its armour).
- **Adventure mode in the vault:** you can't break the vault's blocks. You're back in survival on every way out.
- **Water Walking Boots** no longer launch you into the sky. You float just over the water on Slow Falling, with a gentle lift if you dip in. (They used Levitation 255, which used to mean "no pull" and now means a launch.)
- **Floor display cases** sit on top of the block instead of inside it. Cases placed before this update are lifted out automatically.

### The Haul
Prizes no longer pour into your pockets. At the payout the Fixer hands you **The Haul**: a single barrel holding everything you won. Set it down anywhere and open it. Your Bond Sigil still comes loose so you can keep it on you. A huge tier V haul may fill two crates.

### Loaner kits, rebalanced
| Kit | Armour | Gear | Passive |
|---|---|---|---|
| **Tank** | Juggernaut I, the heaviest (20 armour + toughness) | Hylian Shield, Kokiri Sword, 2 golden apples | +8 health, half knockback |
| **Offense** | Shadowstep I, iron-strong (15), no attack penalty | Captain's Cutlass, 1 golden apple | Strength |
| **Ranged** | Smuggler's set, iron-strong (15) | Fairy Bow, 32 spectral arrows, a backup sword (Sharpness II, Knockback I), 1 golden apple | **Speed**, nearby monsters glow for the crew |
| **Support** | Tidecaller I, iron-strong (15) | Staff of Sparks, Emma's Bloomheart, 3 splash potions of Healing II, 1 golden apple | Crewmates nearby regenerate |

- **Food:** every kit also has 16 steaks.
- **The den heals:** standing in the den gives Regeneration and Saturation.
- **What you can bring in:** your own weapons stay in the coat check (the kits are the heist's gear). Heist tools still come with you: lockpicks, the Clockwork Key, Smoke Bombs, the Cowl, the Monocle, Gutter Coins, the plans and your Bond Sigil (and your Black Market Tokens).

## New in 2.63: half prices, an easier way in and out, ruins underground

### Prices
Everything in the Black Market costs about **half** what it did. That covers prices in Tokens, Medallions, Trophies, Blood Crystals and Lucky Tokens, and the tier upgrades too.

| Example | Before | Now |
|---|---|---|
| Smuggler's Chestplate | 18 Tokens | 9 Tokens |
| Tier II armour upgrade | +10 Medallions | +5 Medallions |
| Tier III upgrade | +5 Trophies | +3 Trophies |
| Pegasus Boots | 4 Medallions | 2 Medallions |
| Cecil's Gem | 4 Trophies | 2 Trophies |
| Shifting Core | 8 Trophies + 16 Blood Crystals | 4 Trophies + 8 Blood Crystals |
| Shifting Armour (a piece) | 6 Trophies + 1 Netherite | a **Shifting Core** + 1 Netherite (like the Shifting arms) |

Other price changes:
- **Diamonds:** the Fence buys a Diamond for **2 Tokens** (it was 4 Diamonds for 1 Token). Old Barnaby sells one back for 4 Tokens.
- **Heist Plans:** 3 Tokens.
- **Pearlman's gems:** 1 Medallion each.
- **What stays the same:** the money-changing rates (9 Tokens = 1 Medallion, 6 Medallions = 1 Trophy) and the Netherite in the Shifting arms.

- **The Scrap Bin** pays half of the **new** prices. For example, a Smuggler's Chestplate (9 Tokens) scraps for 4. Before, some refunds still used the old prices, so you got back more than half. The Fortuna (a Lucky Trophy) now scraps for 1 Trophy instead of a full refund.

The trade audit confirms you still can't buy anything and sell it back for a profit, at a trader or in the Scrap Bin.

### Earning
- **Fishing:** a Token is a rare catch (3%) and a Medallion a very rare one (0.5%), on top of the crates.
- **Heists:** every heist won pays each player **at least 1 Token**, plus a chance at more. Higher tiers pay more, and now and then a Medallion. It's yours to take out of the vault.

### The way in
- **Ladders:** the entrance shaft's ladders now reach the top. The last three were missing.
- **Landing pool:** there's a **pool of water** at the bottom, so you can just jump.
- **The LIFT:** a button **inside the vault door, on the right-hand wall**, with a glowing sign. Press it and you're back on the surface beside the shaft.
- **Existing markets** get all three the next time someone comes near.

### The newcomers' book
Now a short **who sells what**: one line per trader, saying where to find them and what they deal in, plus how to earn. It no longer lists every item. The book in existing markets is replaced automatically.

### Followers
Cecil, Emma, Celi, Zib, Skiff Escorts and framed followers are now welcome **in the market and in the Overworld's dungeons**. They still won't enter the vault (the Gilded Gutter) or the Hollow Throne.

### Emma
- **Mining (new):** her fifth buff gives **Haste II** to everyone near her, or Haste III with harmony or in her Ethereal Form. She wears amber and ochre for it.
- **Menu colours:** each buff's name is now the colour of its outfit, so Defense is pink and Healing is blue.

### Shifting arms (Vinny)
- **Shifting Blade (Smite):** the same five forms, with **Smite V** in place of Sharpness for the undead. The trident form keeps Impaling. Price: Core + 3 Netherite.
- **Shifting Chestplate (No Thorns):** Protection IV, Unbreaking and Mending, without Thorns, for players who don't want the enchantment. It has the same seven looks. The original chestplate is still sold.

### Underground ruins
Small crumbling **rooms, shrines and halls** now turn up in fresh chunks:
- **Overworld:** stone brick or deepslate, deep underground (y −48 to 36).
- **Nether:** blackstone.
- **End:** end stone and purpur, on the outer islands.

Each ruin has a loot chest (halls have a barrel too) with ores, tools, food and enchanted books. There's a good chance of Tokens and a 1-in-5 chance of a **Heartstone**. Rarely there's a Medallion or a Black Market accessory. To find one, use `/locate structure #bm:ruins`.

**Heartstones** are also **three times as common** in vanilla loot chests in every dimension.

### Smaller changes
- **The Minish Cap** moved to **Madame Velour**, next to the Mini and Mega Mushrooms (5 Tokens). It's a size-changer, not a lucky charm, so it didn't belong in the Lucky Den.
- **The Wings of the Golden Rat** now cost 5 Trophies **plus an elytra** to build on.
- **The Grimoire Key** has its own magenta-and-violet look, so it no longer looks like the Black Market key.
- **The Portable Trash Can's** icon fits its inventory slot.

## New in 2.62: creatures on show, the Calling Card, wider crypts

### Display cases: bottled creatures
- **Any item** can go in a display case.
- **A full Smuggler's Jar** shows the creature itself, not the jar. It sits on the cushion, shrunk to fit the case (floor or wall), still as a statue: no AI, can't be hurt, can't be pushed out. Sneak + right-click turns it slowly.
- **Getting it back:** take the jar out empty-handed, or pick the case up, and the creature goes back in its jar unharmed (name, gear and all).

### Cecil
- **Sitting:** right-click anywhere on Cecil to make him sit or follow. Before, only the invisible dog under him could be clicked, so clicking his body did nothing.
- **Gems:** handing him a gem and taking it back (sneak + empty hand) work the same as before, through the same click.
- **Cooking:** with **fire** magic (or his Ethereal Form), right-click him holding raw food and he breathes on it. The whole stack comes out cooked: beef, pork, chicken, mutton, rabbit, cod, salmon, potatoes and kelp.

### Emma
She now wears her **original blue dress** by default (Healing, the buff she's called in with). The rose-and-white dress moved to Defense.

### The Fixer's Calling Card
A raid reward: you get one on your first Tier II clear, and Goldtooth sells more for 40 Gutter Coins. It leaves the vault with you.
- **Using it:** pick a player from the list, then **Go to** them or **Bring** them to you.
- **The other player** gets **[Accept] / [Deny]** in chat, open for 60 seconds.
- **Limits:** any distance, any dimension, but no signal into or out of the vault. Infinite uses, no cooldown.

### The crypt
- **Wider tunnels:** the labyrinth's tunnels are **3 wide** (they were 2), so there's room to sneak past the Warden. It's now a 6×6 maze in the same footprint, with the same altar chamber, entrance and escape shaft.
- **Existing crypts** are rebuilt automatically the first time someone comes near, while nobody is inside and the Warden is asleep. Only the blocks that change are touched.

### Glowing signs
Every sign in the graveyard, the crypt and the market glows now. Signs in existing structures are lit the next time you come by.

### Followers go home cleanly
This applies to Cecil, Emma, Celi, Zib and Skiff Escorts. Each one goes home quietly, with no cooldown, when:
- you get too far away: another dimension, a long teleport, or logging off;
- its summoning item leaves your inventory (into a chest or barrel, dropped) for 3 seconds.

Use the item again to call them back. Each call issues a fresh ticket, so a copy left behind in some far-off chunk dismisses itself when it loads; you never end up with two. (The Frog and Donado are hired companions, not summoned, so like vanilla pets they wait where you left them.)

### Fixes
- **Dockmaster:** only one per market; extras are removed.
- **Pearlman:** his model now disappears with him, however he goes.
- **The Fence:** no longer trades emeralds for Tokens (a raid farm could exploit it).
- **Celi:** her spear no longer clips through her hair and ear while she idles and walks.
- **Crash sites:** the built-in Xenite Altar can be picked up (sneak + punch).

## New in 2.61: display cases, Zib, Skiff Escorts, the vault's coat check

### Glass display cases
The Tailor sells four in the Fixer's Den, for Gutter Coins: **Oak** (3), **Dark Oak** (3), **Quartz** (5) and **Gilded** (8).
- **Placing one:** use it while looking at a floor and it stands there. Use it on a wall and it hangs there, facing out. (Not ceilings or corners.)
- **Using one:** right-click it holding anything and one of the stack goes in. Right-click it empty-handed to take it out. Sneak + right-click and it slowly turns its treasure.
- **Taking it back:** sneak + punch picks the case up. Whatever was inside drops out.

### Zib, the Donadian trooper
The **Donadian Medal** (the reward for defending a mothership) was only a keepsake. Now it calls **Zib**, a teal Donadian in a navy tunic with a ray gun.
- **The medal:** use it to call him, or to call him back. Sneak + use sends him home. Right-click him empty-handed to make him sit or follow.
- **Fighting:** he shoots the nearest monster within 16 blocks for 7 damage. Every fifth shot is overcharged: 12 damage, and the monster is stunned and lit up.
- **Health:** he has 40 health and mends himself out of a fight. If he faints, the medal needs 5 minutes, like the other followers. He counts toward the three-follower limit.
- **Animation:** a jointed rig with idle, walk, run (and both again with the gun raised while a monster is near), aim, recoil, a charging crouch before an overcharged shot, jump and sit.

### Skiff Escorts
Sabotage a Vorn Dreadnought's reactor on an invasion night and everyone nearby gets a **Skiff Escort** beacon.
- **Colours:** there are eight (Crimson, Gilded, Midnight, Abyssal, Rose, Verdant, Pearl, Ember). Each reward is a colour you don't have yet, while any are left. Collect all eight for the **Squadron Leader** advancement.
- **In use:** a little skiff flies at your shoulder and lasers monsters within 16 blocks (5 damage a second). Use the beacon again, or sneak + use, to send it home.
- **It's not the mount:** it can't be ridden, and paint kits don't touch it.
- **Fragile:** it has only 16 health, and archers, blazes, witches and Vorn troopers take shots at it. If it's shot down, it needs 5 minutes of repairs. It isn't a follower, so it doesn't count toward the limit.

### The Gilded Gutter Vault: coat check, loaner kits and contracts
- **Coat check:** going in, the Fixer checks your gear at the door, so nobody can bring in end-game gear. Heist tools stay with you: Smoke Bombs, lockpicks, the Cracking Rig, the Cipher Monocle, the Thief's Cowl, the Smuggler's Boots, Gutter Coins, Clockwork bits, the plans and your Bond Sigil (and, from 2.67, your Black Market Tokens). Followers can't be called inside.
- **Loaner kits:** four racks in the den, each an armour stand wearing its kit. Right-click one to take it:
  - **Tank:** Juggernaut I, Hylian Shield, Kokiri Sword. +8 health, half knockback.
  - **Offense:** Shadowstep I, Captain's Cutlass. Strength.
  - **Ranged:** Smuggler's set, Fairy Bow. Monsters near you glow for the whole crew.
  - **Support:** Tidecaller I, Staff of Sparks, Emma's Bloomheart. Crewmates near you regenerate.

  You can change kits until the heist begins. Anyone without one gets Offense. If you're knocked out, the kit is re-issued.
- **Getting your gear back:** however you come out (the gold plate, after the haul, a cleanup, a crash), the kit stays behind. Your own gear goes back exactly where it was, and anything you picked up inside comes with you.
- **A Fixer's contract** on every heist sheet: **Ghost** (finish with the alarm under 25), **Clean Sweep** (nobody knocked out) or **Against the Clock** (90 seconds a room). Meet it for +2 shares and an extra purse of coins.

### Fixes
- **Display skiff dyes:** the display skiff now takes all sixteen dyes. White, light grey, grey and brown did nothing, and lime/green gave the silver Vorn hull. There are six new skiff colours (Verdant, Pearl, Graphite, Bronze, Ember, Cobalt), and Zorp sells paint kits for them too.

## New in 2.60: the Gilded Gutter Vault, Cecil's elements

### The Gilded Gutter Vault: a party raid
A raid with puzzles, guards, an alarm and five tiers. It works solo too, and it never touches your market standing.

- **Getting in:** buy the **Heist Plans** from the Fence (6 Tokens, reusable). Use them and pick a tier you've unlocked. You, and every member of your party within 24 blocks, are taken down into the vault, which is a separate world. Party members who arrive later use their own plans to join the heist in progress.
- **A run:**
  - First the **Fixer's Den** (the lobby): Goldtooth's stall, the heist sheet (tier, special night, modifiers), this week's records, and a copper door that only a Clockwork Key opens. Press a button by the far door to begin.
  - Then 3 to 7 rooms (tier + 2), drawn at random from seven. Each room's exit stays barred until you beat it:
    - **The Combination Room:** set five levers to match the ledger on the far wall, then press the button. The ledger faces the levers, not you.
    - **The Weighing Room:** every golden scale must be pressed at once. That's 2 to 4 scales depending on party size, and a dropped item counts.
    - **The Gauntlet:** a corridor of sweeping lasers. Getting touched zaps you back to the start.
    - **The Tile Floor:** only a hidden path holds. A button shows the path for a moment (free the first time).
    - **The Dial Lock:** turn three dials (item frames) to the arrows on the blueprint.
    - **The Counting House:** two waves of guards, the second with a captain.
    - **The Three Coffers:** a riddle names the honest coffer. The others are Mimics.
  - Then **the Vault**. Its guardian, the **Gilded Sentinel**, fights with coin barrages, ground slams and called guards. Twice it shells itself in gold; press the hall's four plates at once to crack the shell.
  - Behind its gold door is the treasury. Everyone stands on the ring of plates round the Grand Strongbox together, and **every player gets their own haul**, so there's nothing to fight over. The emerald plate takes you home.
- **The alarm:** mistakes ring it (wrong combinations, lasers, falling tiles, Mimics, getting knocked out). At 50, guards start patrolling. At 100 the vault goes into **lockdown**: guards keep coming and the haul shrinks. Finishing under 50 is a clean getaway and earns an extra share.
- **Knocked out?** The gang drags you back to the den, and your things are where you fell.
- **Tiers I to V:** clearing a tier unlocks the next one for you. The first clear of each tier pays a Gilded armour piece (tier V: the Treasurer's Scepter) and a finer Raid Banner.
- **Modifiers:** each run rolls some, more at higher tiers, and each one adds extra shares:
  - **Lights Out**
  - **Hot Floor**
  - **Speed Run**
  - **Iron Guards**
  - **Glass Cannon:** you hit harder but have half your health.
  - **Greedy Vault:** more loot, and the alarm rings twice as loud.
  - **Silent Alarm:** the alarm starts at 40.
- **Special nights** change the vault:
  - **Blood Moon Heist:** crimson guards and the Crimson Treasurer (blood aura). Adds Blood Crystals and the Crimson Ledger.
  - **Lucky Night Heist:** golden guards and the Golden Gambler (it throws gold). Adds more coins, Lucky Tokens and the Gambler's Coin.
  - **Invasion Heist:** the Vorn got there first. Troopers and the Vorn Vault-Breaker (lasers). Adds Xenite, Power Cells and the Vorn Cracking Rig.
- **Records:** the fastest clear of each tier this week is posted in every den. Whoever sets one gets the **Gutter Laurel**.

### The vault's treasures
- **Gutter Coins:** the vault's own money, spent with **Goldtooth** in the den.
  - Goldtooth sells smoke bombs, lockpicks, Clockwork Key fragments, the Thief's Cowl, Smuggler's Boots, the Cipher Monocle and the Vault Hound Whistle. (The follower outfits are the Tailor's now, and the contracts the Recruiter's.)
  - Coins are never used in the market and never counted for standing.
- **Gilded set** (first clears of tiers I to IV): diamond-grade armour, +1 Luck per piece. The full set gives no fall damage, and nearby drops fly to you.
- **Thief's Cowl:** invisible and quick while you sneak.
- **Smuggler's Boots:** faster, step up a whole block, and fall further unhurt.
- **Cipher Monocle** (worn on the head): pressure plates and tripwires glint within 6 blocks. In the vault it also shows the tiles that won't hold and the coffers that bite.
- **Weapons:**
  - **Heister's Shiv:** an ambush second stab on monsters that aren't after you.
  - **Vault Breaker:** each blow sends a shockwave through nearby monsters.
  - **Coinslinger:** a crossbow whose bolts burst into coins.
  - **Gutter King's Cutlass:** bleeding cuts, and coins from the slain.
  - **The Treasurer's Scepter:** COIN STORM.
- **Together:**
  - **Bond Sigils** (every member of a party of 2+): regenerate when near someone carrying a sigil from the same heist.
  - **Raid Banners I to V:** set one down to heal and quicken your party nearby. Tier III and up also strengthens; tier V also resists.
- **Puzzles:**
  - **Clockwork Key Fragments:** four make a **Clockwork Key**, which opens the den's **Clockwork Cache** (three more shares each).
  - **Seven puzzle trophies:** beat a room cleanly to earn its trophy, a little gold statue you can set down.
- **Followers:**
  - **Gilded Staff Topper:** gilds Cecil's staff in every element.
  - **Golden Spearhead:** turns Celi's spear gold.
  - **Frog's Monocle:** for the Frog with Mustache.
  - **Vault Hound Whistle:** a gold-collared hound that sniffs out unopened loot chests within 12 blocks.
- **Shifting Cores:** a very rare drop from tier III to V hauls.

### Cecil
- **His arms**, redone again from his portrait: two sleeves of the same length and thickness, built as smooth curves.
  - The staff arm reaches out from his side to the staff.
  - The free arm is the curved one: forward from the shoulder, curling down in front with its claws dangling.
  - The free arm is now its own part, so it swings as he walks. This applies to the market Cecil and the follower.
- **His whole cloak** takes a gem's colours: robe, both sleeves, hood and staff.
- **Take a gem back:** sneak + right-click your Cecil with an empty hand. He hands it back and is his poison self again.
  - Handing him a new gem gives you back the old one, so gems are never lost.
- **The Ethereal Gem** gives him his **Ethereal Form**:
  - A pale, glowing, half-there Cecil with a prism crystal and white eyes.
  - He casts a bolt every second (8 damage, each carrying a random element).
  - He heals you sooner, and his charge fills faster.
- **Charged spells:** every 7 bolts (5 in Ethereal Form) his staff gathers light and he casts his element's own spell. They only ever touch monsters.

  | Element | Spell |
  |---|---|
  | Poison (his own) | Plague Bloom |
  | Fire | Meteor |
  | Water | Tidal Surge |
  | Earth | Root Prison |
  | Electric | Thunderstorm |
  | Rock | Rockslide |
  | Air | Cyclone |
  | Grass | Overgrowth |
  | Ice | Glacial Nova |
  | Ethereal | Prismatic Cataclysm |

## New in 2.59: framed followers, Cecil's arms and walk

- **Framed followers.** Put Cecil's Summoning Gem, Emma's Ribbon or Celi's Moon Charm in an item frame (or a glow item frame), and that follower steps out and wanders around it. If they stray too far, they walk back.
  - **Right-click the frame:** they sit down or get up. The item in the frame doesn't turn.
  - **Sneak + right-click the frame:** send them back into the frame, so the item hangs as plain decoration, or call them out again.
  - Take the item out or break the frame, and they leave with it.
  - If they faint, they're back by the frame 5 minutes later.
  - A framed follower doesn't belong to anyone: it doesn't follow or buff players, and you can still have your own follower out. Cecil keeps the element of whoever hung his gem.
  - As with summoning, they won't come out of a frame inside the market or a dungeon.
- **Cecil's arms**, redone from his original art: both arms are now the same length and thickness. His staff arm reaches forward with a slight bend, his claw closed round the staff. His free arm is curved at the elbow, with its claw hanging in front of him. This applies to the market Cecil and the follower.
- **Follower Cecil walks with his staff.** It plants ahead of him, he vaults past it, it trails behind and swings through again, while he sways and dips with each step.
  - Running is the same stride, quicker and lower.
  - When he jumps, he leans back and thrusts the staff forward.
  - He has a sitting pose: settled low, leaning on his staff.

## New in 2.58: parties, boss scaling, Cecil v2

- **Parties.** Press the Quick Actions key (or run `/trigger bm.party`) to open the Party menu. From there you can invite players nearby, accept or decline invites, leave, and see who's in. Parties hold up to 6 players, and invites expire after 60 seconds.
  - Party members can't hurt each other, share a name colour, and see each other's health on the sidebar.
  - The leader can kick members. If the leader leaves, leadership passes to another member. A party of one dissolves.
- **Boss scaling.** Each extra player near a boss (party or not) gives it +50% max health and +10% damage. Its current health percentage is kept and the boss bar follows. Covers every dungeon boss, the Headless Horseman, the Voidwalker, the Pharaoh, the Roc, the Treant, the Colossus, the Monstrosity and the alien warlords.
- **Cecil v2**, both in the market and as a follower:
  - His face is now his original art: glowing eyes over a grey, jagged open mouth, with no white teeth.
  - His staff gem is translucent and glows in the dark, in every element colour.
  - New detail: a collar, a button, a ragged hem, curled claw fingers, a rounder hood with its tip curling to one side, and crown stitching.
  - His sleeve no longer bends at an odd angle.
  - In the market he keeps his idle breathing and spell-casting animations, adjusted to the new body.
  - As a follower, Pearlman's gems still recolour his hood and staff.
- **Fix:** bosses and mobs that wandered out of range and got stuck in the void (for example a Voidwalker with Resistance) are now removed properly, instead of piling up out of sight.

## New in 2.57: fixes

- **Cecil's staff** is taller, so the crescent rides above his hood instead of clipping through his head.
- **Celi** lays her spear along her legs when she sits, instead of through her face.

## New in 2.56: Celi, a slimmer Cecil, followers faint

**Celi**, a rare follower from the snow:
- **Finding her:** in snowy biomes (snowy plains and taiga, slopes, groves, frozen and jagged peaks, ice spikes, frozen rivers, snowy beaches) you may hear someone muttering impatiently. Celi is standing about 14 blocks away, hand on her hip, tapping her boot.
  - Right-click her with a **snowball** and she decides you've got guts.
  - She gives you her **Moon Charm**.
  - She waits 10 minutes. Empty-handed, all you get is attitude.
- **The Moon Charm:** use it to call her, or to call her back. Sneak + use sends her home.
- **Her ice spear:**
  - Up close, she **thrusts** for 10 damage.
  - At 5 to 16 blocks, she **throws** it for 8 damage, and it flies back to her.
  - Every hit **freezes** the monster in place for 3 seconds: frosted over, no walking, no jumping.
  - She picks her own fights; she doesn't wait for you.
- **Reckless:** only 30 health and no armour. She hits harder than anyone, but she gets hurt far more easily.
- **Animations:**
  - at rest, hand on her hip, tapping her foot, head tilted, with the odd eye-roll
  - a brisk stride, and a run with her spear levelled like a lance
  - a leap
  - sitting back on one hand (right-click her empty-handed)
  - the thrust and the throw
- Emma's buffs reach her too.

**Cecil (your follower)** is redrawn:
- a little shorter than Emma, with a fuller robe and a hood slightly bigger than before
- his elements still colour his hood and staff
- the market's Cecil keeps his tall look

**Followers faint.** Every follower comes back 5 minutes after fainting:
- **Cecil, Emma and Celi:** their summoning items rest 5 minutes (it was 10 for Cecil and Emma).
- **The Frog with Mustache and Donado** used to be lost for good. Now they limp home. Five minutes later, right-click the Frog's hut or Donado's cell and they rejoin you for free.

**Shifting Core:** now 8 Trophies + 16 Blood Crystals.

## New in 2.55: the rats come alive

Every rat in the market has a much bigger set of poses now. Each one is still a single entity, so the market costs no more lag than before.
- **Walking:** the market walkers step through a real four-frame walk. Their paws stride, their arms swing, their bodies bob and their tails sway. When they stop to look at you, they fidget like everyone else.
- **Idle fidgets (every rat):**
  - they look left and right, and blink
  - they groom their faces with their paws (a rat holding a weapon uses its free paw)
  - they scratch behind an ear, swish their tails, sniff and flick their ears
  - all over their slow breathing
- **A playful routine for every job**, with a little sound:

  | Rat | Routine |
  |---|---|
  | Chef | flips a pancake in his pan |
  | Professor | reads his book, turns a page, pushes up his glasses |
  | Lucky | flicks a coin and catches it |
  | Pirate | takes a swig, then hiccups |
  | Soldier | salutes, then stamps to attention |
  | Ember Rat | juggles embers |
  | Void Rat | motes orbit his head |
  | Auctioneer | bangs his gavel |
  | Concierge | gives a deep bow |
  | Teller | counts out a stack of coins |
  | The Lord | gives a regal wave |
  | Madame | gazes into her crystal ball |
  | The Gentleman in Grey | checks his pocket watch |
  | The Mercenary | sharpens his knife |
  | The Rat Familiar (on your shoulder) | chases its tail |

## New in 2.54: shifting tools and armour, worn Tendrils, elemental Cecil

**Shifting arms** (Vinny):
- **Price:** first buy a **Shifting Core** (8 Trophies + 16 Blood Crystals). Then trade the Core plus **one Netherite Ingot for every netherite form** the item can take, so you can't skip mining netherite.

  | Item | Price |
  |---|---|
  | Shifting Blade | Core + 3 Netherite |
  | Shifting Pick (Fortune) | Core + 4 Netherite |
  | Shifting Pick (Silk Touch) | Core + 4 Netherite |
  | Shifting Bow | Core |

- **Shifting Blade:** its axe form now has Fire Aspect II, and its trident form has Riptide III.
- **Shifting Picks:** the old pick is now the **Fortune** set. A new **Silk Touch** set has the same eight forms, with Silk Touch in place of Fortune.
- **Shifting armour** (6 Trophies + 1 Netherite Ingot a piece):
  - Press F to cycle the look through leather, chainmail, copper, iron, gold, diamond and netherite (and turtle shell for the helmet).
  - It always protects like netherite. The look is only a model swap.
  - Max enchantments; it never breaks.

**KillerWatt's Tendrils** are a true worn layer now:
- They're drawn as part of your character model (re-skinned elytra wings), so they never fall behind, and they flare out wide when you sneak.
- OFFENSE shows them spread. RANGED shows them coiled with charged blue tips. Each strike flashes them white-hot.
- The old teleported display entities are gone.

**Cecil takes an element:**
- Right-click your Cecil with one of Pearlman's elemental gems. He swallows it, and his hood and staff take its colours.
- His bolts take its effect:

  | Gem | His bolts |
  |---|---|
  | Fire | set monsters alight |
  | Water | drench and slow |
  | Poison | poison (his own) |
  | Earth | root in place |
  | Electric | lightning that jumps to a second monster |
  | Rock | heavy hits |
  | Air | toss monsters into the air |
  | Grass | drain life to mend you |
  | Ice | freeze |

- He keeps the element between summons. Each change uses up one gem.

**Emma dresses for her role.** Her dress, sleeves and scarf re-dye for the buff you choose:
- Speed: sea-green
- Offense: crimson and gold
- Defense: rose and white
- Healing (her default): her own blue

**Bosses:**
- **The Voidwalker** no longer kills his own Voidlings. They share a team, and his homing stars only ever hit players.
- **The Elder Treant** can't be stared down any more. While he stands rooted near you, roots erupt under your feet (move!) and he hurls logs at everyone close.

**Other changes:**
- **The dock master's blue axolotl** is a baby, so a Golden Dandelion keeps it small.
- **Wireless redstone:**
  - A Receiver touching a Transmitter powered it and latched on forever, so that spot is now refused.
  - Placing either one tells you its channel.
- **Sorting Chests:** place two side by side, facing the same way, and they join into a **double chest** that sorts both halves together.

## New in 2.51: Donado and the Frog move smoothly

**Donado** and **the Frog with Mustache** have jointed rigs now, like Emma. Each limb, the head and Donado's tail is its own part, riding the companion and turning smoothly about its joint instead of swapping between baked poses.
- **Donado:** at rest he breathes, looks about, blinks and wags his tail. He walks and runs with swinging arms and legs, leaning into a run, jumps with his arms flung forward, and sits back with his legs out. His weapon stays in his paw.
- **The Frog:** at rest he breathes, looks about and blinks. He moves in proper hops: a crouch, a push-off with his legs kicking back, a sail through the air and a landing.
- **Helmets** sit on their heads. Companions you already have are re-rigged automatically.

## New in 2.50: the Ethereal Gem's wider power

- **Emma:** while an Ethereal Gem is set down within 30 blocks of her, or her summoner carries one:
  - she charges 2.5× as fast
  - her Ethereal Form lasts 50 seconds instead of 30
  - her strikes deal 13 instead of 8
- **Blood Moon and invasion foes, and Elite and Champion mobs** (since 2.52), within 30 blocks of a placed gem, or 16 blocks of a carried one:
  - greatly slowed (Slowness III)
  - greatly weakened (Weakness III)
  - slowly burned away by its light
  Ordinary monsters aren't affected.

## New in 2.49: smoother companions, Shifting Arms, Tendril modes

- **Fading:** Emma and Cecil no longer shrink away. They flare bright and vanish in a burst of magic, and when called they appear whole in a burst.
- **When you die:** Emma and Cecil vanish too, since their ribbon and gem drop with your things. There's no cooldown; pick the item up and call them again.
- **Emma's Ethereal Form:**
  - When she isn't travelling, she hovers with a 2.4-second idle loop: she bobs, sways, looks about, her legs dangle and her wings beat.
  - Her crescent axe is now gripped properly in her fist and points forward. It rests low while she hovers, winds up behind her head and chops down in front.
- **Cecil** waddles when he walks: his robe sways and bobs, he leans in, his head bobs and his staff plants like a walking stick. At rest he breathes slowly.
- **KillerWatt's Tendrils:**
  - Double-tap sneak to switch between two modes. **Ranged** lashes the nearest monster ahead of you, up to about 20 blocks, with no aiming needed. **Offense** gives your melee hits the tendril stab, and every 3 seconds the tendrils drag a monster 4–12 blocks ahead in to you.
  - The tendrils are now placed where you'll be next tick, so they keep up when you move fast.
- **Shifting Arms**, sold by Vinny "Two-Blades" for 16 Trophies + 32 Blood Crystals each. Press F for the next form, or sneak + F for the one before. Every form carries its best vanilla enchantments and never breaks.
  - **Shifting Blade:** sword, axe, mace, spear, trident.
  - **Shifting Pick:** pickaxe, axe, shovel, hoe, shears, fishing rod, brush, flint and steel.
  - **Shifting Bow:** bow, crossbow, trident.
- **The Hollow Throne:** wither skeletons and piglin brutes fight each other, so they never share a wave now. Undead waves alternate with beast waves, and the Hollow King's summoned court is all undead.
- **Pearlman's trade menu** no longer closes by itself. Turning to face you used to teleport him, and any teleport ends a trade; now only his model turns.

## New in 2.48: the Hollow Gate

**The way into the Hollow Throne is now a real portal.** The **Hollow Gate** is a worn deepslate archway, 4 blocks tall, with five empty sockets running up one pillar, over the keystone and down the other.
- **Getting one:** it's your reward for conquering Wilfrey's Keep, replacing the old Shard. The Fence also sells it for 10 Tokens, in case you lose yours.
- **Setting it up:** use it on the ground. It squares itself to face you and needs a clear space 4 wide and 5 high. You can set it up anywhere except inside the Hollow Throne itself, and gates must be at least 10 blocks apart.
- **The sockets:** each socket is cut for one Conquest Emblem, in conquest order: Broodmother, Frost, Drowned Tyrant, Archmage, Wilfrey. Right-click a socket holding its Emblem to set it in. The wrong Emblem won't go in, and the gate tells you whose socket it is.
- **Opening:** when the fifth Emblem goes in, the arch fills with the swirling dark of the Hollow. It hums, and ash and soul-light drift out of it.
- **Passing through:** walk into the open gate. Only players whose record shows all five conquests may pass. Anyone else is thrown back out. Your way home is the rift in the Hollow Throne, which drops you just in front of the gate.
- **Taking it down:** sneak + punch a socket to take its Emblem back, which shuts the gate. Once every socket is empty, sneak + punch the gate to pack it back into your inventory.
- **The Shard of the Hollow Throne is retired.** Using an old one turns it into a Hollow Gate.
- **The Warpstone** (in and out of the Hollow Throne from anywhere) still comes only from defeating the Hollow King, so you first have to go through the gate.
- **Admin:** `/function bm:admin/hollow_gate`. `bm:admin/p2/shard` now gives a gate and all five Emblems and sets your conquests to 5.

## New in 2.47: the Ethereal Gem shimmers

**Carrying the Ethereal Gem** anywhere in your inventory (hotbar, backpack slots or off-hand) brings a passive shimmer. Motes in the nine element colours drift about you, cycling from fire to ice, with a soft glint of light. It's purely for looks, and it stops the moment the gem leaves your inventory. Ethereal Gems you already have get the new tooltip line automatically.

## New in 2.46: Pearlman visits like a wandering trader

**Pearlman comes less often now**, on the wandering trader's rules:
- **One roll a day:** each in-game day (20 minutes of play) there is one roll for a visit.
- **Rising odds:** 10% the first day, then 20%, then 30% each day after until he comes. After a visit it starts again at 10%.
- **Overall:** that works out to about one visit every 4 in-game days, roughly 80 minutes of play.
- **Where:** he still only turns up beside a player standing under the open sky in the Overworld.

## New in 2.45: Pearlman, the Traveling Salespenguin

**Pearlman** is a dapper penguin in a top hat and blue bow tie, with a globe gem on his belly and a briefcase in his flipper.
- **Visits:** now and then he waddles up to you when you're out under the open sky in the Overworld (since 2.46, about once every 4 in-game days, like a wandering trader).
- **Stay:** he sets up shop for 8 minutes, calls "Last call!" a minute before he goes, then tips his hat and waddles off.
- **Stock:** he sells three of his nine elemental gems each visit, a different three each time, for Medallions.
- He chatters when you buy, and he knows more than he lets on.

**The nine elemental gems:** fire, water, poison, earth, electric, rock, air, grass and ice. They are polished trophies, each cut a little differently (a flame, a droplet, venom spikes, a tiny globe, a bolt, a chunk of stone, a wisp, a leaf, ice crystals).
- **Use:** the gem glints toward the nearest biome of its element and tells you the direction and distance (for example, "the Ice Gem glints north-west, about 202 blocks"). A sparkling trail points the way.
  - Fire: badlands and deserts, or the Nether.
  - Water: oceans and rivers.
  - Poison: swamps.
  - Earth: the deep old woods.
  - Electric: savannas.
  - Rock: stony peaks and shores.
  - Air: windswept hills.
  - Grass: plains, meadows and flower forests.
  - Ice: the frozen north.
- **Sneak + use:** set the gem on display, where it floats and spins slowly. Punch it to take it back. Gems on display hum when other kinds of gem are near.
- **Admin:** `/function bm:admin/pearlman`, `bm:admin/elemental_gems`, `bm:admin/ethereal_gem`.

<details><summary><b>Spoiler: the secret of the nine</b></summary>

Set all nine gems on display within 4 blocks of each other. They rise, circle together and fuse into the **Ethereal Gem** (hidden achievement: *Nine Made One*).

Use the Ethereal Gem to set it down as a prismatic, singing shrine. It turns slowly, nine element motes circle it, light rises from it, chimes ring out, and a ring of light marks its reach. Everyone within **30 blocks** is **Ethereal**:
- light as air: low gravity, high leaps, no fall damage, faster
- +3 attack, +4 armour, Regeneration and Resistance
- wings of shimmering light on your back
- every melee blow unleashes one of the nine elements on the target half a second later:
  - fire: burns it
  - water: drenches and slows it
  - poison: poisons it (withers the undead)
  - earth: roots it
  - electric: arcs to two more
  - rock: crushes it for 10
  - air: hurls it skyward
  - grass: heals you
  - ice: freezes it

Sneak + punch the shrine to take it back. Only one shrine can sing in any 60-block area.
</details>

## New in 2.44: a free tractor beam

**The Vorn Skiff's tractor beam needs no power any more.** Look up and right-click the key to switch it on, and it runs for as long as you like. It no longer draws Violet Xenite. Skiff Keys you already have update their description automatically.

## New in 2.43: tendrils up close

**KillerWatt's Tendrils** now fight hand to hand, too.
- **Reach:** wearing them gives +2 reach (5 blocks).
- **Tendril stab:** when you hit something in melee, both upper tendrils rise over your shoulders. Half a second later they lunge forward and stab it for 6 lightning damage (8 in rain, 10 in a thunderstorm). The stab pierces one monster just behind for half damage. The delay lets the stab land after your own blow, so it adds its full damage; it fires about once every 0.7 s.
- **Charged jump:** on a sneak+jump fling, the upper tendrils reach up and ahead and the lower ones plant down beside your legs and push off, then they settle.
- The long-range lash is unchanged: an electric bolt out to 24 blocks.

## New in 2.42: sharper tendrils, the true crown

**KillerWatt's Tendrils** are rebuilt as jagged lightning. Each of the four is now two zig-zag blades with a sharp elbow, white-hot barbs on the corners and a hooked point.
- **The strike:** when one lashes, it climbs past your head (or out past your arm), then lunges forward over your shoulder at the target before settling back.
- **No clipping:** every pose, and every frame between poses, keeps clear of your head, body and arms.

**Apophiss's Crown** now matches the serpent king's own:
- A black band on speckled white fur, with ball-tipped spikes of uneven height.
- A great faceted emerald set inside and rising over the band.
- A diamond ruby on the tall front spike, and oval rubies in gold settings round the band.

## New in 2.41: the relics come into their own

**KillerWatt's Tendrils are worn in the chest slot** and give no armour. Four lightning tendrils grow from your back and drift on their own.
- **Lash:** look at a monster and a tendril lashes it, about once a second. It deals 10 lightning damage, arcing to two more for 5 each. Sneak to yank the monster to you instead.
- **Fling:** sneak + jump to launch yourself where you're looking, or up the wall in front of you.
- **Snatch:** they grab dropped items within 8 blocks.
- **Worn:** 15% faster, a taller step, and no fall damage.
- **In the rain:** lashes deal 13, arc to three, come faster, and you get Speed I.
- **In a thunderstorm:** lashes deal 16 and call lightning down on monsters 6+ blocks away. You get Speed II and Strength.

**Apophiss's Crown** gives no armour any more; it's a crown, not a helm.
- **At night:** Strength and Night Vision.
- **Serpent's Fangs at night:** recharge in 3 seconds instead of 6, and there are 16 of them.

**Leo's Trident:** in water, in the rain, or in an ocean, river, beach or swamp, it gives Strength, Dolphin's Grace and Conduit Power.

**Emma's Bloomheart:** the Bloomheart gem was always Emma's.
- **By day, or with Emma following you:** it reaches 12 blocks, lasts 12 seconds, adds Absorption, and recharges faster.
- **Both at once:** it adds Resistance as well.

## New in 2.40: relics of an old adventure (sold by Cecil)

**KillerWatt's Tendrils** (6 Trophies): the storm-alien's lightning arms (worn on the chest since 2.41; see above).
- **Use:** a tendril lashes out up to 24 blocks.
  - A monster is struck for 10 lightning damage, which arcs to two more nearby for 5 each.
  - An item is snatched back to you.
  - A block: the tendril grabs it and flings you toward it. The farther it is, the harder the fling.
- **Sneak + use:** yank a monster to you, or heave yourself up a wall.
- **Held:** 15% faster, a taller step, and no fall damage.

**Apophiss's Crown** (7 Trophies): the serpent king's grey crown with its great emerald.
- **Worn:** you grow a size, deal +3 damage, reach 1.5 blocks further, and gain +4 health and +2 armour.
- **Venom:** your blows wither living foes. The undead are immune to Wither, so they take +3 damage instead.
- **Sneak + jump:** Serpent's Fangs, a line of 12 dark fangs bursting from the ground ahead. It recharges in 6 seconds.

**Leo's Trident** (5 Trophies): Sir Leo's weapon. It uses the vanilla trident and spear, enchanted.
- **Trident form:** Loyalty III and Impaling III. Throw it and it comes back.
- **Spear form:** Lunge III.
- **Switching:** press swap-hands (F).
- **Both forms:** quick to swing, carry you 15% faster, and every hit gives a burst of Speed II.

**Cecil's Staff** (2 Trophies): a lesser copy of his own.
- **Use:** a poisoned bolt for 5 damage, plus Poison on living foes.
- **Sneak + use:** mends you and friends within 5 blocks. It recharges in 20 seconds.

Admin: `/function bm:admin/cecil_relics` gives all four.

## New in 2.39: Emma moves more naturally

- **Her steps match her speed.** She steps as fast as she actually moves, so she no longer slides along the ground.
- **Walking blends into running.** Her pose shifts smoothly with her speed, from a slow amble through a jog to a full skipping run.
- **Her wings ripple.** In Ethereal Form each wing bends in the middle: the outer half beats a moment after the inner half, so the motion travels from root to tip. She also bobs with each beat.
- **Updates on their own.** An Emma who's already with you picks up the new wings by herself, even mid-flight.

## New in 2.38

- **At most 3 followers.** You can have three companions with you at once, from: Cecil, Emma, the Frog with Mustache and the mercenary rat. Calling, hiring or recruiting a fourth is refused with "send one home first", and nothing is charged for the refused call.
- **Emma's story.** Emma is the orphaned princess of the kingdom under the sea. Long ago she fought the serpent king Apophiss beside Cecil and Sir Leo. Her lines, Cecil's hint and three new chats between them now tell her story.
- Emma's chats with Cecil now also happen while she's sitting.

## New in 2.37: Emma, a hidden friend

**Finding her.** On a sunny day in a cherry grove, flower forest, meadow or sunflower plains, you may hear someone humming a little tune nearby. Emma is sitting in the flowers, about 14 blocks away. Hold any flower and right-click her: she joins you and gives you **Emma's Ribbon**. If you leave her be, she wanders off after 10 minutes, or when nobody is near. She never turns up for someone already carrying her ribbon. Cecil drops a hint the first time you summon him.

**Emma's Ribbon.** Use it to call her, or to call her back to you. **Sneak + use** opens her menu: pick her buff, see her charge, or send her home. Right-click her empty-handed to make her sit or stand, like any pet.

**Support, not fighting.** Every 3 seconds she buffs you, other players within 10 blocks, and Cecil. Pick one of four buffs:
- **Speed:** Speed and Jump Boost.
- **Offense:** Strength.
- **Defense:** Resistance.
- **Healing:** Regeneration, plus a quick heal for anyone below 4 hearts (at most once every 6 seconds).

Monsters leave her alone.

**Ethereal Form.** While monsters are near, she charges by 2% a second. At 100%, with a monster within 14 blocks, she takes her Ethereal Form for 30 seconds: steel armour, white wings and a crescent axe. She flies and strikes the nearest monster every second for 8 damage, plus 4 to anything beside it. Her buffs also get one level stronger.

**With Cecil: Harmony.** Summon them together (within 12 blocks) and they help each other:
- **Cecil** casts every second instead of every 2, and his bolts hit for 7 instead of 5.
- **Emma** charges twice as fast, and her buffs get a bonus.

Now and then they stop to chat: she waves, and he answers.

**How she moves.** When she stands still, she folds her arms politely and sways. She has a bouncy walk and a skipping run, cheers when she jumps, and swings her feet when she sits. In her Ethereal Form she hovers with her wings beating.

If she faints, the ribbon needs 5 minutes before she can come back (2.56). New achievements: **A Friend Among the Flowers**, **Ethereal** and **Best of Friends**.

Admin commands:
- `/function bm:admin/emma`: Emma sits in front of you.
- `/function bm:admin/emma_ribbon`: gives you her ribbon.
- `/function bm:admin/emma_charge`: charges your Emma to 100%.

## Fixed in 2.36

- **Trading screens no longer close by themselves.** Every 10 seconds, the market teleported Vinny, the Fence and Old Barnaby back onto the spot they already stood on. In 26.3, teleporting a trader ends its trade, even when it doesn't move.
- **Old Barnaby** no longer stands directly behind the counter post at his stall. He steps one block to the side. Markets you've already found are fixed automatically.
- **Nameplates follow their trader.** Zorp's name stayed behind where he first stood, and three moved traders had the same problem. A nameplate that has drifted away from its trader now jumps back over them.
- **Cecil (the companion)** no longer appears half inside the ground when you summon him facing a slope or a step. He's placed on top of the step, or at your feet if there's no room.
- **Starting a Blood Moon by hand:** the new `/function bm:admin/blood_moon` starts one tonight, and jumps to nightfall if it's day. Calling `bloodmoon/start` directly now works too; before, it ended on the next tick.

## New in 2.35: honest gear — the Xenite Altar rewards vanilla gear

**Only vanilla gear takes sockets and infusions now.** The altar refuses Black Market goods, and it also refuses vanilla gear bought from a trader: you have to earn it. Anything you socketed before keeps its socket.

**How many sockets an item has depends on what it's made of:**

| Material | Sockets |
|---|---|
| Leather, wood, stone, chainmail | none |
| Copper, iron | 1 |
| Gold | 1, and its shard counts **double** |
| Diamond, trident, mace | 2 |
| Netherite | 2, plus a **Masterwork** socket |
| Bow, crossbow, shield, elytra, fishing rod, shears, turtle shell, flint and steel, brush | 1 |

To socket, hold the item, put a shard in your off hand and right-click the altar. Each click fills the next socket.

**What each shard gives:**

| Shard | Bonus |
|---|---|
| Green | +1.5 Attack Damage |
| Violet | +3 Safe Fall, +10% Knockback Resistance |
| Cyan | +1.5 Luck, +0.5 Reach |
| **Red (new)** | **Vitality: +2 Max Health** |

A red socket doesn't change your size any more. To turn size back on, sneak + right-click the altar with a red shard: each click cycles the item between growth, shrink and off.

**Combos.** Two shards in the same item combine:

| Pair | Combo | Bonus |
|---|---|---|
| Green + green | Ferocity | +15% attack speed |
| Violet + violet | Featherweight | −20% gravity, +3 safe fall |
| Cyan + cyan | Farsight | +1 reach |
| Red + red | Lifeblood | +4 max health |
| Green + violet | Juggernaut | +2 armor toughness, +10% knockback resistance |
| Green + cyan | Precision | +1 attack damage, +0.5 reach |
| Green + red | **Bloodlust** | every kill heals you 2 hearts |
| Violet + cyan | Wayfarer | +10% speed |
| Violet + red | **Second Wind** | below 3 hearts: Regeneration II and Speed (1-minute recharge) |
| Cyan + red | Fortune's Favour | +2 luck, +2 mining efficiency |

**Masterworks (netherite only).** Once both shard sockets are full, the third socket takes a Masterwork. It costs **4 shards in your off hand and a Medallion** in your pack. The shard colour picks the Masterwork:

| Item | Green | Violet | Cyan | Red |
|---|---|---|---|---|
| Sword, axe, spear | Cleave (sweeping hits +50%) | Relentless (+0.4 attack speed) | Reaver (+1 reach) | Vampiric (1 hit in 4 heals you) |
| Pickaxe, shovel, hoe | Haste (+30% mining speed) | Aqua Miner (full speed underwater) | Deep Reach (+1.5 block reach) | Prospector (+3 luck) |
| Armor | Bulwark (+2 toughness) | Fleet (+5% speed) | Ember-proof (fire barely takes hold; blasts barely push you) | Stalwart (+4 max health) |

**Relic Essences.** Put a spare relic in the Scrap Bin and you get **10 Tokens, 2 Medallions and that boss's Essence**. To infuse an Essence, sneak + right-click the altar with the Essence in your off hand. It only goes into **netherite** gear, one per item:
- **On a sword, axe or spear:**
  - *Horseman:* hits set the target alight.
  - *Pharaoh:* +3 damage in daylight.
  - *Roc:* 1 hit in 10 calls down a thunderbolt.
- **On a chestplate:**
  - *Treant:* slow, steady regeneration.
  - *Colossus:* whoever hits you burns.
  - *Voidwalker:* 1 hit in 10 blinks you away.

**Resonance.** Put an Essence and a socket of its colour on the same item and it awakens an AoE power, plus a particle aura while you hold or wear it:

| Essence | Socket colour | Resonance | Effect |
|---|---|---|---|
| Horseman | green | Hellfire | hits may burst into flame around the target |
| Pharaoh | cyan | Sunburst | hits may blaze with sunlight around the target |
| Roc | violet | Stormcall | hits may send bolts to two more foes |
| Treant | green | Thornmail | whoever hits you is torn and rooted |
| Colossus | red | Magma Aura | everything close to you burns |
| Voidwalker | cyan | Void Shroud | when hit you blink away and nearby foes float |

**Admin command:** `/function bm:admin/essences` gives every Essence, plus shards and Medallions.

## New in 2.34: relics are guaranteed

Every roaming boss now **always** drops its relic when a player slays it (it was 1 in 10, or 1 in 6 for the Voidwalker). The bosses are rare and each relic has four forms to unlock with catalysts, so one kill is enough.

## New in 2.33: three more roaming bosses

Every roaming boss is now a vanilla mob, scaled up:

| Boss | Body | Health |
|---|---|---|
| Sand Pharaoh | a husk 2.6× normal size, in a golden crown | 320 |
| Storm Roc | a phantom 4.5× normal size | 260 |
| Elder Treant | a creaking 2.6× normal size (about 7 blocks tall) | 340 |
| Magma Colossus | a Size 7 magma cube (over 4 blocks wide) | 420 |
| Voidwalker | an enderman 2.5× normal size (about 7 blocks tall) | 450 |

The Sand Pharaoh's and Storm Roc's custom models are gone; any left in a 2.32 world are cleaned up automatically. The Headless Horseman is unchanged.

**The Elder Treant** roams the forest at night:
- **When it appears:** after day 10, rarely, at night in a forest, about 20 blocks from someone under the open sky. Everyone nearby sees "The trees lean closer... something old is walking." Its song is "Mellohi", and spores and leaves drift around it.
- **The fight:** like every creaking, it freezes while you look at it, but its magic doesn't stop:
  - roots that pin you in place;
  - logs it throws at you;
  - Twigs (little creakings) that join the fight.
- **At half health** it draws life back from the forest (Regeneration) and bursts brambles around itself.
- **When it leaves:** at dawn.
- **Loot:** Tokens, Medallions, a chance of a Trophy, logs, saplings, apples and moss. It always drops **the Heartwood Branch**.

**The Magma Colossus** roams the Nether:
- **When it appears:** after day 10, now and then in the Nether Wastes or Basalt Deltas. Everyone nearby sees "The ground shakes... something molten rises." Its song is "Pigstep", and ash and lava pop around it.
- **The fight:**
  - ground slams that throw you and set you alight;
  - magma boulders it throws;
  - lava geysers under your feet (watch for the dripping lava first).
- **As it's hurt:** it sheds Magma Spawn at two-thirds and one-third health. When it dies it bursts apart into smaller cubes.
- **Loot:** Tokens, Medallions, a chance of a Trophy, magma cream, Blaze Rods and netherite scrap. It always drops **the Molten Gauntlet**.

**The Voidwalker** is the End boss:
- **When it appears:** out on the outer islands (700+ blocks from the centre), now and then. Everyone nearby sees "The stars go out... something is watching you." Its song is "5".
- **The fight:** it is always angry at the nearest player and never carries blocks off. It:
  - blinks behind you and strikes;
  - fires homing shulker bullets;
  - smothers you in darkness;
  - calls Voidlings (endermites).
- **Loot:** extra Tokens and Medallions, shulker shells, ender pearls and dragon's breath. It always drops **the Void Scepter**.

The new relics use the same catalysts as the others (off hand, look straight up, right-click): Blaze Rod for Offense, Armadillo Scute for Defense, Breeze Rod for Ranged, Heartstone for Support.

**The Heartwood Branch** is stronger in a forest. Each form's right-click:
- **Thornlash — Offense:** a thorn whip (8 blocks) that slows its victim and heals you.
- **Barkskin — Defense:** Resistance II and Regeneration for 8 seconds. Anything that hits you is pricked and rooted.
- **Seedcaster — Ranged:** three seeds fan out (24 blocks), hurting and rooting what they hit.
- **Bloomheart — Support:** Regeneration II for you and every ally within 8 blocks, and the crops around you ripen.

**The Molten Gauntlet** is stronger in the Nether. Each form's right-click:
- **Volcanic — Offense:** its punches knock foes flying. An Eruption Punch blasts everything in front of you up into the air and sets it alight.
- **Obsidian — Defense:** Fire Resistance and Resistance II. Anything that hits you burns.
- **Magmashot — Ranged:** a magma shot (30 blocks) that sets its target alight but never the ground.
- **Hearthfire — Support:** Fire Resistance, Regeneration and Absorption for you and every ally within 8 blocks.

**The Void Scepter** is stronger in the End. Each form's right-click:
- **Voidrend — Offense:** blink to the monster you're looking at (16 blocks) and strike it.
- **Phaseguard — Defense:** Resistance II. Anything that hits you floats away.
- **Starseeker — Ranged:** three homing shulker bullets at the nearest monsters.
- **Riftcall — Support:** every player within 32 blocks blinks to your side, and all of you get Resistance, Regeneration and Slow Falling.

**The Bounty Board** now lists all six roaming bosses as WANTED. Each pays 8 Tokens + 2 Medallions to whoever slays it.

**New achievements:**
- *Heart of the Forest:* slay the Elder Treant.
- *Cooled Off:* slay the Magma Colossus.
- *Stare Down:* slay the Voidwalker.
- *Legendary Hunter:* slay all six roaming bosses.
- *Grand Relic Hunter:* hold a relic from every roaming boss.

**Admin commands:** `/function bm:admin/treant`, `/function bm:admin/colossus` and `/function bm:admin/voidwalker`. `/function bm:admin/relics` now gives all six relics.

## New in 2.32: weapon classes, and two new roaming bosses

**The Horseman's Head now comes in four classes.** Each form plays differently:
- **Horseman's Head — Offense:** hits harder (9). Hold right-click for a short, fierce stream of fire (5 seconds, more damage). Sneak + hold charges a Fire Blast. When stoked, its **Hellfire Nova** hits harder than before.
- **Soulfire Head — Defense:** its blows slow and weaken. Hold right-click for a **Frost Ward**: Resistance II, no knockback, and anything that hits you is chilled. Its **Glacial Nova** freezes everything nearby for 3 seconds and gives you Absorption.
- **Venomfire Head — Ranged:** a weak club. Hold right-click for **Venom Bolts** that poison targets up to 40 blocks away. Sneak + hold charges a **Plague Burst**: let go to lob it, and it leaves a poison cloud for 6 seconds.
- **Hallowed Head — Support:** unchanged. It still heals with its beam, sets down a circle of Regeneration, and fills everyone nearby with life.

**Catalysts.** Hold one in your off hand, look straight up and right-click (the catalyst is used up):

| Catalyst | Class |
|---|---|
| Blaze Rod | Offense |
| Armadillo Scute | Defense |
| Breeze Rod | Ranged |
| Heartstone | Support |

The lanterns still work on the Head. These catalysts also work on the two new relics.

**The Sand Pharaoh** is a roaming boss of the desert day:
- **When he appears:** after day 10, rarely, when someone is under open sky in a desert by day. A sandstorm rises and he walks out of it, about 20 blocks away. Everyone nearby sees "The wind turns to sand... something ancient wakes." His song ("Relic") plays, and blowing sand and the hiss of the dunes follow him.
- **The fight:** a towering mummy king in gold and lapis, with 320 health. He sends scarab swarms, throws sand in your eyes (blindness), raises Tomb Guards and burns you with a beam of sunlight. At half health the storm thickens and the sand erupts under you.
- **When he leaves:** he sinks back into the dunes at dusk.
- **Loot:** Tokens, Medallions, a chance of a Trophy, gold, lapis and Armadillo Scutes. He always drops **the Pharaoh's Crook**.

**The Storm Roc** is a roaming boss of thunderstorms:
- **When it appears:** after day 10, now and then during a thunderstorm in any biome. A huge storm-blue bird comes down out of the clouds. Everyone nearby sees "Thunder rolls... something vast circles above.", and its song ("Precipice") plays.
- **The fight:** it has 260 health. It circles and dives at you. It calls down lightning (sparks gather over your head first) and beats gusts of wind that throw you off your feet. At half health, Stormlings join it.
- **When it leaves:** when the storm ends.
- **Loot:** Tokens, Medallions, a chance of a Trophy, feathers, phantom membranes and Breeze Rods. It always drops **the Thunderbird Talon**.

When either boss dies or leaves, its model fades away.

**The Pharaoh's Crook** is stronger by day, under the sun. Each form's right-click:
- **Crook of Scarabs — Offense:** heavy blows. A scarab swarm eats through everything in its path.
- **Crook of the Sands — Defense:** its blows slow. A **Sandstone Shell** lasts 8 seconds: Resistance II, and anything that hits you gets sand in its eyes.
- **Crook of the Sun — Ranged:** a **Sunbeam Lance** pierces everything within 40 blocks and sets it alight.
- **Crook of Ra — Support:** the **Blessing of Ra** gives Strength and Haste II to you and every ally within 8 blocks.

**The Thunderbird Talon** is stronger in a thunderstorm. Each form's right-click:
- **Thunderbird Talon — Offense:** its blows often call down a thunderbolt. A **Thunderclap** strikes every monster within 5 blocks.
- **Static Talon — Defense:** a **Static Field** lasts 8 seconds: Resistance, and it shocks anything near you or anything that hits you.
- **Stormcaller Talon — Ranged:** **Chain Lightning** reaches 32 blocks and leaps on to 4 targets.
- **Tailwind Talon — Support:** a **Tailwind** gives Speed II, Jump Boost II and Slow Falling to you and every ally within 8 blocks.

**The Bounty Board posts WANTED bosses.** The Headless Horseman, the Sand Pharaoh and the Storm Roc are standing bounties: whoever slays one collects **8 Tokens + 2 Medallions** on top of its loot.

**New achievements:**
- *Curse of the Pharaoh:* slay the Sand Pharaoh.
- *Eye of the Storm:* slay the Storm Roc.
- *Monster Slayer:* slay all three roaming bosses.
- *Relic Hunter:* hold a relic of each.

**Admin commands:** `/function bm:admin/pharaoh`, `/function bm:admin/storm_roc` (it stays only while it's thundering) and `/function bm:admin/relics` (every relic form plus the catalysts).

## New in 2.31: the special nights come alive

**Ambience.** Each special night now feels different inside every Black Market:
- **Blood Moon:** a red haze and a slow heartbeat.
- **Lucky Night:** drifting gold and chimes.
- **Invasion Night:** green static and a far-off hum.
- **Aboard the ships, on an Invasion Night:** the Donadian motherships go to red alert, with red light, warning tones and "RED ALERT" on your screen. The Vorn Dreadnought's alarms never stop.

**Lucky Night: Happy Hour.** From dusk to dawn:
- **Black Market traders:** every one sells at its base price, without the market's usual 1.5× markup. A Filter Hopper is 3 Tokens instead of 5.
- **Zorp:** takes a third off his Xenite prices.
- **Night-only trades:**
  - *Lucky Whiskers:* the **Four-Leaf Charm** (8 Lucky Tokens, permanent Luck while carried), a Heartstone for 10 Lucky Tokens, and Jackpot Scratch Cards for 3.
  - *Zorp:* a Red Xenite shard for 6 cyan, and a Power Cell for 20 green + 20 violet.

**The Lucky Den's slot machines work.** Pull a lever:
- **Lucky Slots** (the two outer machines, 1 Token a pull): three of a kind pays ♣ 4, ♦ 6, ♥ 10, ★ 25, ♛ 60, or 7 150 Tokens. Any pair gives your Token back.
- **The Progressive Jackpot** (the middle machine, 5 Tokens a pull): every pull adds 2 Tokens to a jackpot shared by **every market on the server** (4 on a Lucky Night). **Three 7s win the whole pot**, announced to everyone. The pot then starts again at 50. Three crowns pay 30, three stars 15, and two 7s give your 5 Tokens back.
- **The sign:** above the Jackpot machine, it shows the current pot.

**The Leprechaun Rat.** On a Lucky Night, a little rat in a green bowler sometimes turns up near you outdoors and bolts. Catch it (it has 8 health) before it vanishes and it drops a **Pot of Gold**: tip it out for 8–16 Tokens and 3–6 Lucky Tokens.

**Defend the Mothership.** On an Invasion Night, board a Donadian mothership and the Vorn beam onto its deck in three waves (3, 5, then 7 troopers):
- **Win:** everyone aboard gets 6 green, 6 violet and 6 cyan Xenite, plus a **Donadian Medal**.
- **Once a night per ship.** If everyone leaves, the attack is called off and can be tried again that night.

**Sabotage the Reactor.** On an Invasion Night, the Vorn Dreadnought's reactor runs hot behind **four power conduits** round its core:
- **Smash all four** (8 hits each) while reinforcements beam in every 20 seconds.
- **Then:** the reactor goes offline, the alarms stop for a while, and the **Dreadnought Vault** opens next to the core. Inside: 6–10 Red Xenite, the **Warlord's Banner**, Green Xenite and a 1-in-4 chance of a Power Cell.

**Invasion stock at the Fence** (Invasion Nights only):
- **Signal Jammer:** switch it on and no Vorn trooper, saucer or beast drops in within 48 blocks of you until dawn.
- **Flak Rockets** (4 a bundle): right-click to fire at the nearest Vorn Scout Saucer within 48 blocks, for 14 damage.
- **Salvage:** he buys Xenite (3 shards of any colour for a Token) and Power Cells (2 Medallions each).

**New advancements:**
- **Lucky Night:** Happy Hour, One-Armed Bandit, Jackpot!, Top o' the Mornin'.
- **Invasion Night:** Hold the Line, Meltdown, Radio Silence.

## New in 2.30: the Scrap Bin, and a day count you can't scramble

**The Scrap Bin.** Put Black Market goods in a Scrap Bin and, a second later, they're scrapped for **half what they cost**, paid into the bin. If the bin is full, the refund pops out on top.
- **What can be scrapped:** anything bought from a Black Market trader, a back room or Zorp (the pack's own goods, and vanilla goods like the Spectral Arrows, Bottles o' Enchanting or Nether Star).
- **Refunds come in what you paid:** Tokens, Medallions, Trophies, Blood Crystals, Xenite or Lucky Tokens.
- **Rounding:** something that cost **1 Token gives the Token back**. A 1-Medallion buy returns 4 Tokens, and a 1-Trophy buy returns 3 Medallions.
- **Bundles go back as bundles:** 16 Spectral Arrows bought for 3 Tokens return 1 Token per 16.
- **Upgraded gear:** returns half of its whole upgrade chain, as Old Barnaby always paid.
- **Old buy-backs:** gear that's only found in the world, and the **Lucky 7** (3 Trophies), scrap at Barnaby's old buy-back prices.
- **Never scrapped:** money (Tokens, Medallions, Trophies, Crystals, Xenite...), and vanilla items you mined or found yourself. Vanilla goods bought from a trader carry a hidden "bought" mark, so only those count.
- **Where to find one:** every Black Market has a Scrap Bin at the west end of **Old Barnaby's counter**, with a sign. Markets already in your world get theirs automatically. Barnaby also sells them (5 Tokens) to place anywhere: right-click a block face, and break it to pick it back up. Hoppers can feed one and empty it.
- **Old Barnaby** no longer buys things back (the bin does that), so his list is short again: his goofy goods (Lava Lamp, Portable Trash Can, Whoopee Cushion, Boombox, Ocarina), breaking Medallions and Trophies into change, Tokens for Diamonds, and the Scrap Bin.
- Black Market goods no longer say "no refunds".

**Blood Moons can't be knocked off schedule by `/time set`.** The pack used to count days from the world's total time, so typing a raw number such as `/time set 1000` sent the count back to day 0 and pushed the next Blood Moon up to 29 days away. The named commands (`/time set day`, `noon`, `night`, `midnight`) were always fine on 26.3. The pack now counts sunrises itself, and the count only goes up:
- **Counts as a new day:** a sunrise, a night slept through, or `/time set` to an earlier hour.
- **Also on the new count:** Lucky Nights, Invasion Nights, the Dark Auction's week and the mercenary's payday.
- **Existing worlds:** carry on from the day they were on.

**The Grave Charm costs exactly 10 Tokens** (the market's usual 1.5× markup no longer applies to it).

## New in 2.29: finding your way, and keeping your things

**The Newcomers' book is always up to date.** The book on the "Newcomers, Start Here" lectern is now built from the traders' real stock every time the pack is built. It lists where every trader stands (Cecil and Zorp included), the Bounty Board, then **who sells what**, by name only (no prices). Markets already in your world get the new book automatically the next time someone is nearby.

**A Black Market advancement tab.** Your first Black Market Token opens it. Goals include: your first trade, living through a Blood Moon, Lucky Night and Invasion Night, the Blood Moon record, assembling a Vorn Skiff, Cecil's gem, a Heartstone, placing a tinkering block, reclaiming a grave, and challenges for the Monstrosity, the Blood Eclipse, the Headless Horseman, a mothership boss and all six dungeon bosses in order.

**Crafting recipes** for the simpler tinkering goods. They appear in your recipe book once you've earned a token:

| Item | Recipe (shaped) |
|---|---|
| Tinker's Wrench | 3 iron ingots in a diagonal |
| Wireless Transmitter | ender pearl on top, redstone lamp in the middle, 3 redstone around it |
| Wireless Receiver | ender pearl on top, copper block in the middle, 3 redstone around it |
| Redstone Clock | a clock with 4 redstone around it |
| Sorting Chest | a chest with 4 comparators around it |
| Filter Hopper | item frame on top, then comparator, hopper, comparator |
| Vacuum Hopper | ender pearl on top, then ender pearl, hopper, ender pearl |
| Block Breaker | iron pickaxe over a dispenser |
| Block Placer | piston over a dropper |
| Item Compactor | a copper grate with 4 pistons around it |
| Lag Lens | a spyglass with 4 glass around it |

The Filter Hopper's recipe is 2 rows: the frame sits in the top-middle slot.

**Server settings** for ops: `/function bm:admin/settings`. Click to change:
- **Blood Moon interval:** every 10, 20, 30 (default), 45 or 60 days, or never on its own. A Crimson Effigy can still call one.
- **Block Breaker** on/off.
- **Skiff TNT bombs** on/off.
- **Magic hurts players** on/off: Cecil's staffs and bows, the Tidal Tear, the Gravewell, Prism and Starcaller blasts.

**The Grave Charm** (the Fence, 10 Tokens). Keep it anywhere in your inventory. When you die, everything you were carrying is laid in a grave where you fell instead of scattering, and you're told the grave's coordinates. **Only you can open it:** right-click the gravestone and your things come back, the charm included. Without the charm, death works as usual.

**`/function bm:admin/help`** now lists every admin command, including the settings. Click one to fill it into chat.

## New in 2.28: tinkering goods, and a glass cockpit

**Prof. Whiskerton** now sells redstone helpers (prices in Black Market Tokens). Each is a real vanilla block, so hoppers, redstone and pistons treat it normally. Right-click a block face with one to place it; break it to get it back.

| Item | Price | What it does |
|---|---|---|
| Filter Hopper | 5 | A hopper that only takes the items shown in **item frames on its sides**. It watches the item at the front of the line above it (a hopper or chest) or the loose items on top, and waits while that item isn't on its list. Wanted items move at normal hopper speed. With no frames it's an ordinary hopper. |
| Vacuum Hopper | 6 | Pulls loose items within 8 blocks onto itself every second. Lock it with redstone to switch it off. |
| Item Compactor | 6 | Every 5 seconds, gathers loose items and XP within 12 blocks onto itself, where they merge into full stacks. Fewer item entities means less lag. |
| Wireless Transmitter | 3 | A redstone lamp. While it's powered, every Wireless Receiver on the same channel turns on, at any distance (in loaded chunks). |
| Wireless Receiver | 3 | A copper block that becomes a redstone block while a transmitter on its channel is powered. **The channel is the item's name:** rename a transmitter and a receiver to the same name in an anvil. Unnamed ones share one channel. |
| Redstone Clock | 3 | Gives a redstone pulse every 1–60 seconds (it starts at 1). |
| Block Breaker | 6 | A dispenser that, when powered, breaks the block in front of it. The block drops as if mined. It won't break bedrock, portals or spawners. |
| Block Placer | 6 | A dropper that places the blocks it drops (when the space in front is free). Anything that isn't a block is dropped as usual. |
| Sorting Chest | 5 | Tidies itself every time it's opened: stacks are merged (respecting each item's stack size) and sorted A to Z. |
| Lag Lens | 3 | Right-click for the entity and dropped-item counts in the 3×3 chunks around you, plus the dimension's totals. |
| Tinker's Wrench | 2 | Right-click a tinkering block to read it. On a Redstone Clock, right-click adds 1 s and sneak + right-click takes 1 s off. On a Sorting Chest, it sorts it now. |

**Glass canopy.** The Vorn Skiff's dome (every paint, the UFO mount and the Display Skiff) is now clear tinted glass, so you can see the pilot sitting inside. The hull also sits a touch higher around the pilot, so your head clears the top of the dome.

## New in 2.27: the skiff's tractor beam, and a cockpit that fits

**Tractor beam.** Aboard your Vorn Skiff, **look up and right-click the key** to switch on a tractor beam. A column of violet light reaches 20 blocks down from the saucer (about 5 blocks across):
- creatures and other players under you are lifted up to just below the hull and held there until you switch the beam off or fly away. Then they drop, so mind the fall;
- dropped items and XP orbs float up into the saucer and straight into your inventory;
- it won't lift bosses (anything with more than 100 max health), NPCs, or players in creative or spectator.

*(Since 2.44 it needs no power.)* Look up and right-click again to turn it off yourself. The laser (right-click), the TNT bomb (look down and right-click) and sneak-to-land all work as before, even with the beam running.

**The pilot fits the cockpit.** Seated players used to perch on top of the dome with their legs sticking out over the hull. The skiff is now 1.5x bigger (about 4 blocks across), and the hull sits so your legs are inside the upper hull and your body and head are inside the glass dome. Skiffs already in your world pick up the new size the next time you board.

## New in 2.26: Blood Moon goods

Four new wares at the Blood Moon stall, paid in Blood Crystals, and a record to hunt for:

| Item | Price | What it does |
|---|---|---|
| Moon Pact | 6 Crystals | Sign it under a Blood Moon. Until dawn, every horror you slay pays 1-2 extra Crystals straight into your pack, but you take 50% more damage from everything. One pact a night, and it can't be torn up. |
| Thirsting Blade | 24 Crystals | A diamond-grade sword. Under a Blood Moon, every monster you kill with it adds +1 attack damage, up to +6. The bonus only applies while the blade is in your hand, and fades at dawn. |
| Vampire's Mirror | 12 Crystals | Use it to mark where you stand; use it again within 60 seconds to step back to that spot, even from another dimension. 30-second cooldown. It won't work in dungeons or the Market. |
| Crimson Hourglass | 10 Crystals | Turn it under a Blood Moon and the moon stands still for 2 minutes (the night is that much longer). Once per Blood Moon, announced to everyone. |

**Music Disc - Blood Moon** is an original track (about 1.5 minutes). Riders of Blood Moon steeds drop it 1 time in 4. It plays in any jukebox.

The disc's song is a new registry entry, so **restart the server** (not just `/reload`) after updating. The resource pack carries the track.

The Blood Moon item icons were also redrawn on vanilla bases in 2.25.

## New in 2.24: Cecil the Wizard, the chef's new menu, goofy goods and music

**Cecil the Wizard** has moved into the purple fortune teller's tent on the plaza. He's a hooded, grinning sorcerer with a crescent-bladed staff. He breathes, sways, turns to watch you as you walk past, and now and then raises his staff to cast a little spell. Markets already in your world get him automatically. He sells magic:

| Item | Price | What it does |
|---|---|---|
| Staff of Sparks | 24 Tokens | Right-click: a bolt hits the creature you aim at (16 blocks) and jumps to up to 3 more nearby, 6 damage each. 1.5 s recharge. |
| Gravewell Staff | 8 Medallions | Right-click: opens a gravewell where you look. For 3 seconds it drags monsters in, then bursts: 8 damage and they're thrown up. 12 s recharge. |
| Cecil's Crescent Staff | 4 Trophies | Hits like an axe (11 damage). Right-click: three homing crystal shards seek the nearest monsters, 7 damage each. 4 s recharge. |
| Prism Bow | 6 Medallions | Arrows burst into a rainbow nova where they land: 5 damage to monsters nearby. |
| Starcaller Bow | 3 Trophies | A fully drawn arrow calls five falling stars down where it lands, 6 damage each. One volley every 3 seconds. |
| Bloomheart (gem) | 9 Medallions | Right-click: you and everyone within 8 blocks get Regeneration II for 8 s (45 s recharge). While it's in your off hand, poison and wither won't stick to you. |
| Tidal Tear (gem) | 9 Medallions | Right-click: a wave rolls 10 blocks ahead. It shoves monsters back, deals 4 damage, slows them, and puts out fires (including you). 20 s recharge. |

Staffs, bows and the Tidal Tear hit monsters, animals and other players. They never hit you or anyone's companion.

**Chef Fromage's new menu.** Prime meat is now a great food on its own: eat it as it is for as much food as two steaks, plus a moment of Regeneration. The chef also cooks six new dishes from it:

| Dish | Price | Effect |
|---|---|---|
| Fire-Eater's Chili | 2 Prime Porkchop + 6 Tokens | Fire Resistance 8:00 |
| Deep-Sea Chowder | 2 Prime Chicken + 6 Tokens | Water Breathing 8:00, Dolphin's Grace 3:00 |
| Moonlit Kebab | 2 Prime Mutton + 5 Tokens | Night Vision 10:00 |
| Lucky Rabbit Pot Pie | 3 Prime Rabbit + 3 Medallions | Luck II 20:00, Jump Boost 5:00 |
| Hunter's Roast | 3 Prime Beef + 3 Medallions | Absorption III 4:00, fills you up |
| Featherlight Drumsticks | 2 Prime Chicken + 2 Medallions | Slow Falling 5:00 |

He also sells the **Grand Banquet** (6 Medallions + 2 Prime Beef). Set it down on a block and anyone can right-click it for a helping: food, Regeneration and Absorption. It has 8 helpings, and each person can take one every 30 seconds.

**Goofy goods.** Old Barnaby sells these, and they can also turn up in loot chests across the world:
- **Groovy Lava Lamp** (6 Tokens): set it on a block and it glows, with blobs drifting up and down. Right-click it to cycle through six colours.
- **Portable Trash Can** (5 Tokens): right-click and a trash can pops up in front of you. Anything you put in it is destroyed. It folds away when you walk off.
- **Whoopee Cushion** (3 Tokens): hide it on a block. Whoever steps on it (player or mob) finds out.
- **Boombox** (2 Medallions): set it down and right-click it to play the next track; it cycles through every music disc. Sneak + right-click to stop it.
- **Pocket Ocarina** (8 Tokens): right-click to play a note. Look up for high notes and down for low ones, across two octaves. Sneak + right-click to switch between nine instruments.
- **Display Skiff** (from Zorp, see below): a Vorn Skiff ornament that doesn't fly. Right-click it with a dye to repaint it (six colours), or sneak + right-click to change its decal.

Sneak + punch picks up a lamp, cushion, boombox or display skiff.

**Cecil joins the fight.** Cecil sells **Cecil's Summoning Gem** (4 Trophies). Use it and he appears beside you and follows you around:
- He fights from range: every 2 seconds he fires a poisoned bolt at the nearest monster within 14 blocks (5 damage + Poison II).
- He heals you when you're hurt: below 7 hearts, every 5 seconds.
- He has 60 health and 20 armour.
- Use the gem again to call him back to your side. Sneak + use to send him home; he bows and fades away.
- If he faints in battle, he fades away and the gem needs **5 minutes** before it can call him again (2.56).

**Magic hurts players now.** Cecil's staffs, bows and the Tidal Tear hit other players as well as monsters. That includes the Staff of Sparks' chain, the Gravewell's pull and burst, the crescent shards, the Prism and Starcaller blasts, and the wave. The Horseman's Heads, Soulreaver's Soul Rend, the Quake Maul and the Wither Nova already did. None of them ever hit **the player using them**, and none of them hit **companions** (Cecil, Wilfrey, the Frog with Mustache, Rufus the mercenary).

**Every bow in the market is sold by Cecil**, including the Fairy Bow, which used to be Vinny's. (The Flintlock is a gun, so Salty Sal still sells it.)

**Chef Fromage's Portrait** is a 2x2 painting of the man himself, sold by the chef (6 Tokens).

**The Emma Doll** (Cecil, 3 Trophies; only sold in the Black Market, never found in chests) is a chibi Emma, mid-wave. Set her on a block and right-click her to make her twirl. While she stands, anyone within 10 blocks of her is cured of harmful effects: poison, wither, slowness, weakness, mining fatigue, nausea, blindness, hunger, darkness, bad luck, and the infested, oozing, weaving and wind-charged effects. Good effects are left alone. Sneak + punch picks her up.

**Also in 2.24 (fixes and moves)**
- **The Bounty Board** is now the wooden notice board on the plaza, in front of the fountain. Tonight's bounty is pinned flat across its 3 x 2 plank face; right-click it to sign up. Its old joke signs are gone, and so is the balcony board from 2.23.
- **Vorn Skiff:** you now sit inside the cockpit, with the glass dome around you and the saucer at your feet. Before, you were perched on top of the dome.
- **The Fairy Bow, the Hero's Bow and the Bow of Light** have moved from Vinny to Cecil, with the same upgrades (Fairy Bow + 6 Medallions -> Hero's Bow; Hero's Bow + 3 Trophies -> Bow of Light).
- **The Display Skiff** is sold by Zorp now (6 Violet Xenite + 4 Green Xenite), not Salty Sal.
- **Zorp** stands in front of his counter aboard the motherships, so you can reach him. Zorps already aboard step out on their own.
- **Counters:** the Dockmaster's, the Fence's, Old Barnaby's and the Forge Pit's (and every other market counter) lose the floating slab that older markets had on top.

**The Vorn** no longer stand on a hoverboard. They walk on their own feet, with a walking animation. Vorn already in your world update automatically.

## New in 2.23: the Hollow King's tools wake up, and a round of fixes

**The Hollow King's tools** each have their own power now. All of them, plus two new pieces, are in his victor's vault:
- **Soulreaver** (sword). Right-click for **Soul Rend**: a sweep that hits everything within 5 blocks in front of you (12 damage and Wither II) and heals you a little for each one it hits. 8 s cooldown.
- **Gravedigger's Maw** (pickaxe) and **Barrow Spade** (shovel). Right-click to **dig out the 3 × 3 face** you're looking at. Containers are left alone, and it doesn't work inside dungeons or the market. **Sneak + right-click** switches between **Fortune** and **Silk Touch**.
- **Headsman's Grief** (axe). Now a proper weapon: Sharpness X, Smite VIII, **Looting V, Fire Aspect III**. Chop one log of a tree and **the whole tree falls**. This only works on natural trees (logs touching natural leaves), so log houses are safe. Sneak + right-click: Fortune / Silk Touch.
- **NEW: Reaper's Sickle** (hoe). Right-click for **Harvest Moon**: every crop within 6 blocks ripens at once (30 s cooldown). Sneak + right-click: Fortune / Silk Touch. It hits like a sword.
- **Witherstring** (bow). Its arrows leave a trail of souls and inflict Wither II.
- **NEW: Wings of the Damned** (elytra). Unbreakable, +6 armour (as tough as a chestplate), and flying into a wall never hurts you. **Hold sneak while gliding** and the wings push you forward, so you don't need rockets. On the ground, **crouch and look straight up for a second** to launch into the air. Then jump to start gliding. You leave a trail of souls, wither smoke and flames.

All of them show their evil names (☠ … ☠).

**Fixes and changes**
- **Mailboxes work.** When you placed a mailbox, its model ended up at your feet, away from the box you actually click. That's why it couldn't be opened, posted to or picked up. Mailboxes already in your world are repaired automatically.
- **Vacuum Satchel:** **sneak + right-click** now unfolds it into a barrel in front of you, the same way the Ender Pouch works. Walk away and it folds back up, keeping what's inside. A plain right-click still turns the auto pick-up ON and OFF. Items already inside an old satchel move over the first time you open it.
- **Soul Vials (new, very rare):** about 1 in 700 zombies, skeletons and spiders you kill leaves a Zombie, Skeleton or Spider Soul Vial. Use it on any monster spawner, including an empty Caged Spawner you've set down, and that spawner spawns that monster from then on.
- **Glowing mobs** (Blood Moon horrors, bioengineered beasts, Jackpot monsters) now only glow when you're **within 30 blocks** of them.
- **The Dimension Shifter** now comes only after the Ender Dragon: Zorp makes it from **4 Shulker Shells** + 6 Red Xenite. Where it takes you: in the Overworld or Nether, your **spawn point** there (your bed or respawn anchor), or a safe spot near 0, 0 if you don't have one. In the End, the obsidian platform.
- **Zorp** only leaves crash sites. He stays aboard the motherships, and you can trade with him there again.
- **UFO tractor beams** stop at the ground instead of going down to the bottom of the world.
- **Horseman's Head:** its attacks now hit **every mob**, animals included. Animals killed by the fire attack drop cooked meat. The Hallowed Head heals every mob except undead ones, which it still burns.
- **Golden Cheese Wheel:** feeds everyone within **25 blocks**. The Rat King now sells it for **10 Trophies + 64 Golden Carrots**.
- **Kraken:** the rider now sits in the middle of the body, and the body keeps up with you instead of trailing behind.
- **The Bounty Board** is now a real wooden notice board on the wall, with the current bounty pinned to it. **Where to find it:** in every Black Market, on the upper balcony, right beside the Newcomers' lectern (the one with the "Newcomers, Start Here" sign). Right-click the board on a Blood Moon, Lucky Night or Invasion Night to sign up for that night's bounty. On other nights it says there's no bounty.

## New in 2.22: fixes

- **Fixed:** the graveyard ghosts' (and the Banshee's), the Mimics' and Wilfrey's models vanished. Like the Vorn models in 2.20, a cleanup was only counting models that ride wolves.
- **Fixed:** Vorn guards on Dreadnoughts were spawning, but invisible, because the same bug removed their models. They show up again.
- **Bioengineered beasts glow green again**, and keep their sickly particles.
- **Vorn Skiff:** the pilot now sits over the saucer's centre, and the saucer's overlapping faces no longer flicker (z-fighting) when it moves. The bomb bay recharges in **20 s** (was 60).
- **Wind Burst I, II and III** enchanted books are sold by Prof. Whiskerton: 14 Tokens, 3 Medallions and 6 Medallions.
- **The Headless Horseman** no longer drops vanilla jack o'lanterns, so they can't be mistaken for his head. His head still drops 1 time in 10 when a player gets the kill.

## New in 2.21: night cosmetics, wings, the Experience Charm

- **Night cosmetics.** Blood Moon horrors, Lucky monsters and the Vorn (troopers, saucers, bioengineered beasts) sometimes carry a cosmetic charm, and they **wear its particles**, so you can see which ones to hunt. There are three per night, each rarer than the last: 3%, 1% and 0.3% of those monsters carry one. Kill a carrier and it drops its charm half the time.

  | Night | Uncommon | Rare | Very rare |
  | --- | --- | --- | --- |
  | Blood Moon | Crimson Drip Charm | Bloodbat Charm | Blood Moon Halo |
  | Lucky Night | Clover Charm | Gold Rush Charm | Jackpot Crown |
  | Invasion | Xenite Glow Charm | Tractor Beam Charm | Saucer Orbit Charm |

  The Vorn charms also turn up, rarely, in mothership stores and crash wrecks.
- **Angelic Wings and Evil Wings**: particle wings, hidden in the Hollow Throne's secret vault.
- **The Experience Charm** (Capt. Cheddarbeard, Rat Gang HQ, 10 Trophies): anywhere in your inventory, everything you kill drops twice the experience.
- **The Headless Horseman's song**: when he comes near you, music disc 13 starts playing for you and any other music goes quiet. It stops when he falls or rides away.
- **The Hollow Throne's loot chests** refill after every Blood Moon.
- **Fixed:** the Vorn and UFO models vanished in 2.20. They're back.

Charms work like the other cosmetics: keep one anywhere in your inventory, and one shows at a time.

## New in 1.27: the Headless Horseman, and a big round of fixes

Still Java 26.3. **Restart the server (or reopen the world) after updating.** This version adds new enchantments and damage types, and `/reload` can't load those. Items already in your world update to their new names and lore on their own.

### The Headless Horseman

He's a roaming boss of the Overworld night.
- **When he rides:** never in the first **15 days** of a world. After that he comes very rarely on an ordinary night, and much more often under a **full moon** or a **new moon**. He appears about 24 blocks from someone standing under open sky. Everyone within 30 blocks hears the cave stir and sees *"You sense an evil presence nearby..."*.
- **What he is:** a towering headless rider in black, carrying his own jack-o'-lantern head and a netherite spear. He rides a huge, fast **Hellsteed**. He has 360 health, Resistance and Fire Resistance, and hunts from 96 blocks away. Flames burn at his neck and under the steed's hooves, ash falls around him, and the night laughs and moans.
- **How he fights:** he **breathes fire** at the nearest player, **charges with his spear**, and calls up **Pumpkin Thralls** (skeletons with lit pumpkin heads, at most 6). At half health he enrages: Strength, more speed, more thralls and a ring of flame.
- **When he leaves:** at dawn he rides away, taking his thralls and steed. He also leaves if nobody is within 128 blocks for a minute and a half.
- **What he drops:** 10 to 16 Tokens, 2 to 4 Medallions, a Trophy (40%), a Heartstone (15%), netherite scrap, pumpkins and pie. **He always drops his head** (since 2.34; it was 1 time in 10).

### The Horseman's Head

The head is a weapon, and it can't be placed. Hold it in your **main hand**.

| Use | What it does |
| --- | --- |
| Melee | Hits as hard as a netherite sword but swings slower. Hits set the target alight. |
| Hold right-click | Breathes a **stream of fire**. The stream shrinks over 10 seconds, then the head needs 10 seconds to rekindle. Let go early and the fuel recovers on its own. |
| Sneak + hold right-click | Charges a **Fire Blast**. Let go to fire it. It hits up to about 35 blocks away, bursts over 4 blocks, and never breaks blocks. |
| Sneak + look straight down + right-click | Fires the **Nova** once the head is stoked. Kill monsters with the head to stoke it: 20 kills, or 12 under a full moon, a new moon or a Blood Moon. Blood Moon monsters count double. The Nova hits every hostile mob and every other player within 10 blocks, never you. |

Undead killed with the head drop extra experience.

**It grows stronger with the night** (Overworld only, while you hold it):

| When | Power |
| --- | --- |
| Night | Night Vision, ×1.5 damage, a glow of its fire around you |
| Full or new moon | As above, but ×2 damage, a 6 s cooldown, a faster blast charge and a smaller Nova requirement |
| Blood Moon | As above, but ×2.5 damage, +1.5 reach, Strength II, Speed II and Regeneration |

**Changing its fire:** hold the item in your **off hand**, look straight up, and right-click the head. This uses up one of the off-hand item.
- **Soul Lantern:** the head becomes the **Soulfire Head**. Its fire freezes instead of burning, and hits chill and slow the target.
- **Any Copper Lantern:** the head becomes the **Venomfire Head**. Its fire poisons. Undead wither instead, since poison doesn't work on them.
- **Plain Lantern:** the head goes back to the Horseman's Head.
- **A beating heart (a Heartstone):** the head becomes the hidden **Hallowed Head**, a support relic and a poor club.
  - Hold right-click: a **healing beam** that heals whoever it touches (players, villagers, pets and mounts). If nobody is in the beam, it heals you at half the pace. It burns the undead. It runs 10 seconds, then needs 10 to rekindle.
  - Sneak + right-click: sets down a **circle of Regeneration** (radius 5) for 10 seconds, with a 30 s cooldown.
  - Healing and kills stoke it. Then sneak, look down and right-click: everyone near you is healed and gets Regeneration II and Absorption II. Undead nearby are seared.
  - It gets the same night, moon and Blood Moon power-ups as the other heads, as faster healing, stronger circles and shorter cooldowns.

### Fixes and changes

**The Black Market**
- **Every market has a ladder shaft** from the end of its entrance tunnel up to the surface, with a signposted top. A market whose tunnel ends sealed in rock can always be reached now. Markets already in your world get their shaft the first time they load.
- **No more flooding.** Every block in a market that can hold water (iron bars, chains, dripstone, stairs, slabs...) is set dry. Older markets are fixed the first time they load under this version.
- Decor that floated after the counters were lowered sits on the counters again. The Blood Alcove's cages hang lanterns, the dock steps run the right way down to the pier, and the DOCKS sign hangs over the office's open side.
- **Salty Sal the Dockmaster is a rat**, at the same size as the other traders.
- **Rat Gang HQ:** the wall to the docks now reaches the ceiling, so you can't ender-pearl in anymore. The Captain sells two new prizes:
  - the **Hoard Sack**: your private 27-slot stash. Use it and a locked barrel appears in front of you that only your sack opens. It folds away, contents kept, when you walk off.
  - the **Golden Cheese Wheel**: a placeable trophy that keeps everyone within 50 blocks fed, like a full beacon. Sneak + punch to pick it up, right-click to turn it.
- **Who sells what:** all the armour (Smuggler, Kingpin, Hero and the Dawnbringer set) is with Sgt. Steelwhisker. The mail kit is at the Fence. The Newcomers' book now lists every trader and what they sell.
- **Rebalanced:** the Dawnbringer (Solar) set now costs Trophies. So do the Vampire Lord and Crimson sets, on top of their Blood Crystals.
- The market's lecterns were checked at all four turns a market can generate at. Each one faces the same way relative to the market in every turn.

**The Vorn**
- Their models vanish with them, so no bodies are left standing.
- Fewer of them at once on an Invasion Night, and Invasion Nights now hum, beam and crackle.
- Invasion Nights only start once someone has killed a Vorn aboard a Dreadnought.
- Bioengineered monsters lose the green outline and drip sickly particles instead.
- Vorn troopers and saucers drop **Red Xenite** 1 time in 100.
- The **Vorn Skiff** hides its harness (no more "helmet"), and its hull now rides on the skiff instead of trailing a tick behind.
- The **Dimension Shifter** works again. Its buttons had collided with the mercenary's.

**Items**
- The **Experience Flask** works in your main hand. It used to only work in the off hand.
- **Triple-jump boots** grant each jump's boost the moment you leave the ground, and you have 0.8 s to chain the next jump. They used to miss quick hops.
- The **Pocket Ender Chest** and the **Void Hinge** are retired. The new **Ender Pouch** (from the Void Rat) sets a real ender chest down in front of you, which folds away when you leave. Pocket Ender Chests you already have turn into Ender Pouches, and the Void Rat buys your Void Hinges back. Shulker boxes hinged before still open.
- The **Blue Marlin** has a new sprite, drawn from the reference art.

**Admin:** `/function bm:admin/horseman` summons the Horseman 10 blocks ahead. `/function bm:admin/horseman_heads` gives you all four heads.

## New in 1.26: the Bounty Board

Every Black Market now has a **Bounty Board** on the balcony beside the Newcomers' lectern. On special nights it posts a bounty. Right-click the board to sign it. Only kills made after you sign count, you can carry one bounty at a time (the Bloodbroker's Blood Bounty counts as your one), you get one per night, and bounties expire at dawn. Your progress shows on the action bar.

| Night | Bounty | Reward |
| --- | --- | --- |
| Blood Moon | Slay 8 Blood Moon horrors | 10 Blood Crystals + a Medallion |
| Lucky Night | Defeat 6 Lucky monsters | 3 Lucky Tokens + a Jackpot Scratch Card |
| Invasion Night | Down 8 Vorn invaders or bioengineered monsters | 6 Tokens + 4 Green Xenite, with a 10% chance of a Vorn Skiff part |

If two special nights overlap, the board posts the Blood Moon bounty first, then Invasion, then Lucky. The older Blood Bounty paper still works alongside it. Markets already in your world get the board automatically.

Also fixed: the Band of Regeneration now heals right after its 5 seconds (it used to wait about 10).

## New in 1.25: treasure of the wide world

Still Java 26.3. Inspired by Terraria.

**Accessories and tools**: each is a rare find in the vanilla chests that suit it, and also comes from Mimics and fishing crates. "Inventory" means anywhere in your inventory, off hand included.

| Item | Where | What it does |
| --- | --- | --- |
| Climbing Claws | jungle temples | In the air, push into a wall to climb; let go of forward to slide down slowly (inventory) |
| Umbrella | shipwreck supplies, outposts | Held in either hand, you drift down gently |
| Ice Skates | igloos | Boots: Speed II on any ice |
| Water Walking Boots | buried treasure, ocean ruins | Stride across water; fall in and you bob back up. Sneak to sink |
| Rod of Discord | ancient cities | Teleport where you look (24 blocks). Costs 2 hearts, more if used again within a few seconds. It can kill you |
| Bottomless Water / Lava Bucket | shipwreck supplies / ruined portals | Pour forever. Sneak + use soaks the fluid up (5x5x5) |
| Extendo Grip | outposts, mansions | +3 block reach in the off hand |
| Lifeform Analyzer | strongholds | Names the nearest rare monster within 64 blocks and points the way (inventory; held, it always reports) |
| Metal Detector | mineshafts | Held: counts ancient debris, diamond, emerald and gold ore within 8 blocks |
| Enchanted Sundial | desert temples | At night, skip to morning. Recharges in one full day; won't work on Blood Moons, Invasion or Lucky Nights |
| Band of Regeneration | dungeon chests | Regeneration I after 5 seconds without taking damage (inventory) |
| Cobalt Shield | fortresses | Immune to knockback while held |
| Obsidian Skull | bastions | Fire, campfires and magma blocks can't hurt you; lava still can (inventory) |

**Other new things to find**
- **Mimics**: 1 in 100 vanilla loot chests is a Mimic. It snaps shut and hops at you. Kill it and the chest comes back with its loot, plus a guaranteed accessory, 3-6 Tokens and maybe a Medallion. There are no Mimics inside the pack's own structures.
- **Fallen Stars**: on clear Overworld nights, stars streak down near players and land glowing. Ones still on the ground fade at dawn. Right-click with 9 to make a **Star Cloak**: when you're hurt, stars strike up to 3 nearby monsters (3-second cooldown). The Professor buys 3 for a Token and Lucky Whiskers buys 5 for a Lucky Token.
- **Fishing crates**: any catch can also bring up a Wooden (5%), Iron (1.5%) or Golden (0.4%) Crate. Right-click to open: Tokens, ingots, gems and a chance at an accessory (4% / 10% / 30%).
- **Sword shrines**: a very rare mossy shrine in grassy and wooded biomes, with a sword in stone. Pull it out to get the **Enchanted Sword** (Sharpness IV). At full health, right-click fires a sword beam. Ops can build one with `/function bm:admin/shrine`.

## New in 1.24: getting out of trouble, and rare monsters

Still Java 26.3.

- **The Surface Charm** is a rare find in Overworld loot chests (2-4% of dungeon, mineshaft, temple, stronghold, treasure, shipwreck, ruined portal, mansion, outpost, ancient city and igloo chests). Underground, right-click it to rise straight up to the surface. It's reusable with no cooldown. It refuses under open sky, outside the Overworld, inside the pack's own structures, or if only lava waits above.
- **The Lava Charm** is found in Nether chests: 15% of bastion treasure, 8% of other bastion chests and 8% of fortress chests.
  - If you're in lava with one anywhere in your inventory, it pulls you out on its own. Right-clicking it in lava also works.
  - It takes you back to the last safe ground you stood on, if that's within 64 blocks and still safe. Otherwise it searches the columns around you for safe footing.
  - It puts the fire out and gives 10 seconds of Fire Resistance. One use.
- **The Rainbow Charm** (Lucky Whiskers, 6 Lucky Tokens): a little rainbow arcs over your head.
- **Rare monsters**: about 3 in 1000 natural spawns of these mobs are a rare variant with double health and its own particles:

  | Mob | Rare variant | Charm |
  | --- | --- | --- |
  | Zombie | Cinder Revenant | Cinderheart Charm (embers) |
  | Skeleton | Starlit Skeleton | Starfall Charm (starlight) |
  | Spider | Glimmerweave Spider | Glimmer Charm (glowing motes) |
  | Creeper | Bloomcreeper | Bloom Charm (spores) |
  | Enderman | Voidwalker | Void Charm (void sparks) |
  | Blaze | Ashen Blaze | Ashfall Charm (falling ash) |

  Each rare monster has a 35% chance (+10% per Looting level) to drop its charm, plus 2-4 Tokens. A charm gives you the same particles. Like the other cosmetic charms, keep one anywhere in your inventory; one shows at a time, and the rare ones show before the shop ones. Ops can spawn them with `/function bm:admin/rare/<name>`.
- **Specter Sheets**: the Banshee now drops one half the time, +10% per Looting level. Each sheet gives **5 phases**, at least 5 seconds apart. Its first lore line shows the phases left, and the fifth phase tears it apart.

## New in 1.23: the Banshee's shroud

Still Java 26.3.

- **Specter Sheets**: the Banshee (Blood Moon graveyards, once per moon) drops them (rates changed in 1.24, see above). Face a wall and right-click one to **phase through it** (up to 12 blocks of wall, horizontally). The sheet is used up only when it works. Sheets refuse to work in or near the pack's own structures: the dungeons, the Black Market, graveyards, motherships, crash sites and the Hollow Throne. They also refuse if the far side lands in one of those places.
- **The Specter Charm**: sneak + right-click with 9 sheets to stitch one. Wear it in the **chest** slot.
  - Always: 30 blocks of safe fall, but 4 armor is taken away. Every other player within 5 blocks is shrouded in Darkness. The wearer isn't.
  - At night, or anywhere with light 7 or less: Speed III, Jump Boost II, Regeneration I, Night Vision and Fire Resistance.
  - On a Blood Moon, add Strength II and Resistance II.
  - In daylight under open sky you get none of that, and you catch fire (the charm's **Sunbane** curse).

## New in 1.22: the docks get busier, the dead get restless, and the mail goes through

Still Java 26.3. Anything that needs a real player was checked by the checkers, not hand-played.

**New goods**
- **The Blue Marlin** (Salty Sal, 6 Medallions): a sword with a marlin's bill for a blade (Sharpness VI, Looting III, +1 damage, +0.5 reach). Sneak + right-click a wall to **mount it** there as a trophy; it keeps its enchantments. Punch the trophy to take it back down.
- **Storm Balls** (Salty Sal, 4 for 3 Tokens): throw one and lightning strikes where it lands, clear skies or not.
- **The weather vials** now come from Salty Sal instead of Prof. Whiskerton.
- **Black Market Coffee** (Chef Fromage, 3 for a Token): every cup raises Speed and Jump Boost one level for a minute, up to V. When it wears off, the crash is just as big: Slowness and Weakness at the same level.
- **Skiff Paint and Decal Kits** (Zorp): six hull colours (Vorn Green, Crimson, Gilded, Midnight, Abyssal, Rose) and four decals (Clean, Racing Stripes, Rat Crest, Flames). Use a kit and your skiff wears it from then on.
- **Hostile UFOs** (Scout Saucers, the Abductor and the Overseer) have a 1-in-200 chance to drop a Vorn Skiff part.

**The Restless Dead** (Blood Moon nights)
- Every graveyard with a living visitor wakes.
- Restless Spirits rise from the graves every few seconds: ghostly, flying, and they drop **Ectoplasm**. Up to six at a time.
- At midnight **the Banshee** climbs out, once per moon. She's big and tough, and her wail brings darkness, slowness and a chill. She drops a pile of Ectoplasm, Blood Crystals, a Medallion and sometimes the **Ghost Veil** cosmetic.
- The Bloodbroker takes Ectoplasm for Blood Crystals, Tokens or the Ghost Veil.
- The dead lie down again at dawn.

**Mailboxes and couriers**
- **Mailbox** (Old Barnaby, 4 Tokens): set it down and you get its numbered **key**.
  - Anyone can right-click it to post the item in their hand.
  - Only the key (or the owner) opens it.
  - It's a ledger, not a chest, so breaking things around it spills nothing.
  - Sneak + punch your empty mailbox to pick it up.
- **Courier Whistle** (the Fence, 6 Tokens): hold the item to send in your off hand, blow the whistle and type a mailbox number. A courier rat delivers it anywhere, even to a mailbox far away, for 1 Token. The owner hears "You've got mail!" if they're online.

**The market**
- **Trader rats are bigger** (about 1.4×), so it's clear which rats trade. Existing markets catch up automatically.

**Less lag**
- A final build pass (`optimize.py`) makes the pack's commands cheaper without changing what they do:
  - **Typed entity searches.** Searches that tested every loaded entity now test only the kinds that can carry that tag. That's 329 of them, and they're only typed where the build can prove which kinds those are, including mobs that convert.
  - **Quiet dungeons and markets.** Dungeon puzzles, gates, effects and altars, and market effects, neon signs, crowds, traders' chatter and syncs, now run only while someone is nearby.
  - **Split once-a-second work.** The dungeon and market chores run half a second after the rest, so they don't all land on the same tick.
- **Measured on the 26.3 test server** with the stress-test world (about 2,600 loaded entities: several markets, ~20 dungeons, motherships), no players online:
  - The pack's average cost per tick fell from about **7.8 ms to about 3 ms**.
  - Its worst ticks (95th percentile) fell from about **33 ms to about 24 ms** (8 ms without the pack).
  - In the server profiler, the pack's share of tick time fell from about 19% to about 7.5%.
- **Cleanup:** 50 stale preview images, an unused copy of old loot tables, a superseded reference-builder tool, the retired 1.7 market builder and an unused alien model are gone. The built packs are unchanged. Structure files are now written byte-for-byte the same on every build.

**Checked**
- Every trader was spawned on the 26.3 server and its offers read back: 742 recipes (768 on the TEST build), 0 problems.
- Every trade price and exact item check accepts the item exactly as it drops from its loot table: 325 items (409 on the TEST build).
- Every macro function parses, and every entity data write was replayed without errors.

## New in 1.21: the Vorn Skiff, the Dawnbringer set, the Mining Drill and a friendlier market

Still Java 26.3. As with 1.20, anything that needs a real player was checked by the checkers, not hand-played.

**The Vorn Skiff** (rare)
- Six salvaged parts make one flying saucer.
  - **Crash-site wreckage** holds the Hull Plating, Canopy Dome and Gravitic Coil (about 1 crate in 8).
  - **Mothership store barrels** hold the Navigation Core, Plasma Emitter and Micro-Reactor (about 1 barrel in 20).
  - **The Dreadnought's armory** always holds one or two parts of any kind.
- With all six in your inventory, right-click any part to assemble the **Vorn Skiff Key**.
- **Right-click the key** to call your skiff and climb in. It's a harnessed happy ghast in a saucer hull, about **four times faster**. Fly it like a happy ghast; sneak to get out, and it folds itself away a few seconds later.
- **Aboard:**
  - Right-click fires a **plasma laser** (64 blocks, 5 hearts).
  - Right-click while looking steeply down drops a **charged TNT bomb**: twice a normal blast, one TNT from your inventory, 60-second recharge.
- It won't fly in or near dungeons, crypts, the Hollow Throne or a Black Market, and it sets you down if you try.

**The Dawnbringer set** (Madame Velour; Medallions + gold blocks): the Vampire Lord's opposite.
- **Full set in daylight under open sky:** Strength, Haste and Fire Resistance.
- **Sunburst:** look straight up and hold sneak for a second to **arm** it (do it again to disarm, so ordinary sneaking stays ordinary). While armed, hold sneak for 1.5 seconds. A 10-second healing sun gives Regeneration II to every player and tame creature within 8 blocks. It recharges in 5 minutes.

**The Vorn Mining Drill** (Zorp: 2 Power Cells + 8 Red Xenite)
- Hold right-click to drill in any direction, one block every other tick. Drops fly to you.
- It runs on **Red Xenite**: each shard is 64 blocks, it refuels itself from your inventory, and the bar shows its charge.
- The **Vorn Drill Bit** (Zorp, or sometimes the Dreadnought) upgrades it to **Mk II**. Sneak + right-click then switches **3 × 3** drilling on or off.
- It won't bite inside dungeons, crypts or a Black Market, and leaves containers and unbreakable blocks alone.
- Fortune's Favor's 3 × 3 mining now respects the same places.

**Rat portraits**
- The five rat sprites (Chef, Lucky, Captain, Professor, Sergeant) are now framed **2 × 2 paintings**, **banners** and **shields**.
- They're found in crash sites and motherships (and in dungeon chests on the TEST build).

**The market**
- **Vinny, the Fence and Old Barnaby** stood two blocks behind their counters, just out of reach. They now stand at them, in existing markets too.
- **"Newcomers, Start Here":** a lectern just inside the vault door, under a floating sign. Its book lists every trader, where they stand and what they sell.
- **The Rat Gang HQ** (behind the mouse hole) is worth the crawl now:
  - Capt. Cheddarbeard sells the **Whisker Lantern**. In your off hand it gives Night Vision, and every hostile mob within 20 blocks glows.
  - His **Rat King's Crown** makes the rats bow to their king: Hero of the Village prices from every villager trader in a Black Market.

## New in 1.20: the Vorn, new goods and a tidier market

Still Java 26.3. Mechanics that need a player (jumps, flight, rides, the satchel) were checked by the command, NBT and logic checkers but not hand-played: please report anything odd.

**The Visitors, part 3: the Vorn**
- **There are two fleets.** The Donadians (Zorp's people) are friendly traders. The **Vorn** are a hive that bioengineers whatever it finds. Books and NPC chatter tell the story.
- **Crash sites** are carved into the real ground the first time someone comes near. The crater follows the hillside, so no more floating wrecks or square patches of flattened land. Zorp has left them (existing ones pack up). A wrecked supply chest holds a Mothership Chart.
- **Motherships** are about three times rarer. Their stores now hold loot barrels: shards and supplies, never Zorp's goods. Zorp lives only on the mothership.
- **Zorp** no longer sells what the Xenite Altar can make (ray gun, tractor beam, cloaking device, dowser, gravity boots). He sells new tech instead.
- **The Donadians look like Donado** in a teal palette, without the green disc underneath. The disc became the Vorn hoverboard.
- **Invasion nights:** about 1 night in 30 that isn't a Blood Moon or Lucky Night (or `/function bm:admin/invasion_now`).
  - Vorn Troopers ride hoverboards and fire plasma. Scout Saucers (UFOs) swoop and shoot back; shoot them down.
  - Bioengineered monsters glow green: oversized slimes, giant phantoms that dive from the open sky whether or not anyone slept, and a third of ordinary night spawns.
  - Everything drops Xenite shards, every colour.
  - At midnight a boss lands: the **Warlord** or the **Abductor**. Both drop Power Cells.
- **The Overcharged Beacon** (Zorp, for Power Cells) summons the **Supercharged Overseer**, on invasion nights only. Only the Overseer drops the **Gravitic Core**: hover-flight in survival.
- **The Vorn Dreadnought** is an incredibly rare, hostile red mothership. It has Vorn guards, the **Quake Maul** (right-click: a shockwave) and the **Vorn Saucer Crown** cosmetic.
- **Red Xenite** can be socketed at the altar so the item makes you grow while held or worn. A second red shard flips it to shrink. Infuse a crossbow or a bow with 8 red shards for a **Growth Ray** or **Shrink Ray**. The effect is permanent on mobs (never the Ender Dragon) and lasts 30 seconds on players.

**New goods**
- **Vacuum Satchel** (Zorp, the Fence's back room): 27 slots. Right-click switches it on or off; while on, it pulls dropped items within 6 blocks into itself. Sneak + right-click opens it.
- **Tool fusion** at the Xenite Altar: sneak + right-click with a tool in each hand. The main tool also mines like the off-hand one. Costs 8 levels; at most two capabilities.
- **Dimension Shifter** (Zorp): a menu to the Overworld, the Nether or the End, each to a safe spot. Never the Hollow Throne.
- **Triple Jump Boots** jump higher on the second and third hop. **Spring-Loaded Boots** charge while you hold sneak (2 to 5 blocks).
- **Void Totem** (the Void Rat) pulls you out of the void. **Pocket Ender Chest** (the Void Rat). The **Void Hinge** upgrades a shulker box so sneak + right-click opens it from your hand.
- **Experience Flask** (Prof. Whiskerton) stores and returns your XP.
- **Sanguine Fang** (the Bloodbroker): in your off hand, each kill heals half a heart. The **Vampire Lord** set now really heals: two full hearts per kill.
- **Rocket boots** kick about twice as hard (~15 blocks a burst).
- **The Rat Bank** also keeps Blood Crystals, all four Xenite colours, Ember Scales and Void Shards.

**The market, tidied**
- **Counters** are one block high. The old ones had a slab floating on top.
- **The Dark Auction's tiers** now rise away from the podium. **Cushions** (new in 26.3) are the seats there, in the tavern and on the plaza benches.
- **Signs** face the walkway they belong to.
- **Water:** every market sweeps away any water that isn't the fountain, the river or the falls. It runs when the market is first visited and again every minute while someone is inside, and it restores the docks' floor where water took it.
- **Salty Sal, Dockmaster**, now works the dock office (existing markets get him too):
  - **MLG Water Bucket**: carry it and it splashes water under a long fall, then scoops it back. 3 charges, one returns every 20 s. Not in the Nether.
  - **Water Charm**: puts you out when you catch fire, 5 times.
  - **Kraken Conch**: blow it in water to ride a kraken. Very fast swimming, and you breathe while riding.
  - **Gold Doubloon** (5 Trophies + 5 Hearts of the Sea): while you carry it, every hostile mob you kill has a 1-in-200 chance to drop a Token.
  - **Rare Blue Axolotls**, the Fishbowl Helmet, the Coral Crown, Bubble Trail Boots, the Captain's Cutlass, a Flintlock Pistol, Anchor Boots and Messages in a Bottle (treasure maps).
- **Black Market Keys** return to looted crypts every Blood Moon.
- **Graveyards** have 23 new epitaphs, and about half the graves have none.
- **Lucky Prime animals** only glow while someone is within 10 blocks.
- **The Golden Donado** (still a Dark Auction lot here) no longer tends crops. Set it down and no monster spawns within 32 blocks of it, a 64 x 64 area.

## New in 1.19: Minecraft 26.3

1.19 is the same pack as 1.18, rebuilt for **Java 26.3**. It needs 26.3 and won't load on 26.2. Keep using 1.18 on a 26.2 world.

**Fixed while porting.** These were caught by running the pack inside the real 26.3 server:
- **Trade payments.** Tokens, keys and gear that come from loot tables stored their hidden version number as a different number type than the trades ask for, and the game compares that exactly. Every one of the 124 payment items failed to match its trades.
  - Loot tables now write that data exactly the way trades do.
  - Items already in players' inventories are fixed automatically within a second, by the existing item auto-update.
  - This mismatch most likely existed in the 26.2 builds too.
- **Explorer maps.** In 26.3 the map function draws onto whatever item it's given, so a map started from a blank map came out as a blank map with map data attached. The Smuggler's, Gravedigger's, Croaker's and Mothership maps (and the TEST build's dungeon maps) now start from a filled map. Cheddarbeard's Treasure Map is now 26.3's own Buried Treasure Map item, and the Sealed Explorer's Map opens into 26.3's own Trial Chamber or Woodland Mansion map item.
- **Display blocks.** The lectern ledger, the portrait plinths, the dowsing outlines and the bloom flowers used the old block format, which 26.3 rejects. They would have shown as nothing.
- **Falling lanterns.** 23 of the market's hanging lanterns hung from thin air or from a sideways chain, so the first block update near them (and placing a market) dropped them as items. This was a layout bug from the 1.13 market rebuild.
  - The terrace and balcony rows now hang under the floor edge, and the alley festoon's lanterns hang from upright links.
  - The rest got a short chain up to the rock.
  - The build now refuses any lantern without support. The Frog Hut's two firefly bushes and the Keep's eyeblossoms (TEST build) also had no soil and now do.
  - Markets already in your world keep their old layout. New markets, and any placed with the admin command, are fixed.
- **Motherships are rarer:** about one every 120 chunks of spread instead of 56, so roughly a fifth as many. Ones that already generated stay.
- **Rocket Boots kick harder:** each mid-air burst now lifts you about 7 blocks instead of about 3. The Mk II's two bursts stack.
- **Vanilla mob drops** (blaze, enderman, ghast, hoglin, magma cube, piglin brute, shulker, wither skeleton) are rebuilt from 26.3's own tables, with the Black Market currency drops added on top as before.

**Unchanged.** Every trade (630 offers across all traders), every price, every item and every mechanic is identical to 1.18.

## New in 1.18: Standing, the Dark Auction and the Gilded Gutter

**Standing** is your reputation at the market, one score across every market in the world.
- **Earning it:**
  - Buying from a market trader earns the price in Token value: a Token is 1, a Lucky Token 5, a Blood Moon Crystal 3, a Medallion 9 and a Trophy 54.
  - Currency swaps and Old Barnaby's buy-backs earn nothing.
  - Deeds: +20 for a finished Blood Bounty, +10 for a Jackpot monster, +50 for each first boss victory (Phase 2).
- **Tiers:** Stranger 0, **Regular** 150, **Associate** 500, **Partner** 1,500, **Family** 4,000.
- **Checking it:** type `/trigger bm.standing`. It works for every player, operators or not, and shows your title, your points and a bar to the next tier.
- **Regulars and above** are greeted by name by the traders.

**Your key follows your Standing.** At Associate, Partner and Family, any older Black Market key you carry turns into the **Silver Key**, the **Gold Key**, then the **Rat King's Key**, in the same slot. The vault door accepts every key, so nothing that worked before stops working.

**Back rooms.** A ledger on every trader's counter opens a menu of extra stock:
- One item for Regulars, another for Associates, and a signature item for Family.
- You pay from your inventory; no trade is involved.
- The full list is in the table below.

**Members' gates.** The iron bars stay shut. The ledger at each gate waves a good-enough key through.
- **The Auction Hall:** a Silver Key or better.
- **The Gilded Gutter:** a Gold Key or better.
- **The Captain's den front door:** the Rat King's Key. The mouse hole still works too.

**The Dark Auction.**
- **When:** every 7th in-game night, and on every Blood Moon night. Doors open at dusk; the first lot is called at midnight.
  - The sign by the gate counts the days.
  - A sale night you sleep through is held the next night instead.
- **No key?** While the doors are open, the gate ledger sells a **one-night pass** for 2 Medallions.
- **Bidding:** five lots are sold one at a time.
  - Right-click the **Bidding Paddle** handed out at the door, or the ledger on the podium, to bid +1, +2, +5 or +10 Medallions.
  - Each lot sells when a 10-second countdown runs out with no new bid. Every bid restarts it.
- **Paying:** your Medallions are taken when you bid, in this order:
  1. your inventory;
  2. your Rat Bank balance;
  3. Trophies, broken into 6 Medallions each, with the change handed back.
- **Escrow:** your bid is held against your name.
  - **Outbid:** you're refunded at once, or the next time you're online.
  - **Win:** the lot is handed over, on your next login if you'd left.
  - **A crash, restart or `/reload` mid-sale:** everyone is refunded.
- **Rival bidders:** Lord Squeakington, Madame Nibbles and the Gentleman in Grey sit in the stands and push prices toward a hidden reserve. If one of them wins, the lot goes back into the pool.
- **The lot pool:**
  - **Headline lots (★):** one per sale, always called last.
    - Wings of the Rat King, the Golden Donado and the Rat King's Signet are one per world.
    - The Mercenary Contract and the Ring of Three Burrows are one per player.
    - The Pocket Rift has no limit.
  - **Very rare cosmetics (✿):** about one sale in three.
  - **Regular goods** fill the rest.
  - The Lucky 7 and the Ravenous Heart are **not** sold.

**The Gilded Gutter** is the Partners' lounge.
- **The Concierge:**
  - Three goods that change every in-game week.
  - Repairs to the item in your hand for 2 Medallions.
- **The Rat Bank (the Teller):**
  - Deposit Tokens, Lucky Tokens, Medallions and Trophies, kept against your name. They're safe from death and lava.
  - Take back 1, 10 or all of any of them.
  - A **Banker's Card** opens your account from anywhere.
  - Interest is off unless an operator turns it on.

**New goods:**

| Item | What it does | Where |
|---|---|---|
| Ring of Three Burrows | Set three homes in any dimension and travel to them: 3 seconds standing still, 2-minute recharge, not in dungeons or the Hollow | Auction ★ (one per player) |
| Pocket Rift | Raises a lit End portal 3 blocks ahead. 3 charges: sneak + use beside it to fold it back up and get the charge back, or sneak + use with 4 Eyes of Ender to add a charge | Auction ★ |
| Smuggler's Jar | Bottles a creature 3–8 blocks away with all of its data (name, gear, owner, trades, health, age) and lets it out anywhere. Other players' pets are refused | Auction, Fence's back room (Family) |
| Mercenary Contract | Hires **Rufus Gnaw**, rat for hire: crossbow at range and a blade up close. Orders: follow, guard a spot, or scavenge loot. Wages are 1 Token a day; he ranks up with service (Recruit, Veteran, Captain); if he falls, he's patched up for 2 Medallions | Auction ★ (one per player) |
| Golden Donado | Statue. Crops within 8 blocks grow a stage every minute, and baby animals grow up faster | Auction ★ (one per world) |
| Donado Trophy | Decorative statue; right-click to turn it, sneak + punch to pick it up | Auction, Velour's back room |
| Wings of the Rat King | Unbreakable elytra: +6 armor, +3 toughness, Regeneration while gliding | Auction ★ (one per world) |
| Rat King's Signet | +2 Luck in the off hand; Standing earned ×1.25 while you carry it | Auction ★ (one per world) |
| Spawner Crowbar (3 uses) / Caged Spawner | Pries a monster spawner loose and sets it down elsewhere | Auction, Barnaby's back room (Family) |
| Lodestone Locket | Toggle; pulls dropped items and XP within 7 blocks | Auction, Steelwhisker's back room |
| Banker's Card | Opens your Rat Bank account anywhere | Auction, Fence's back room |
| Fair Weather Bell | Clears rain and storms for a day, once a day | Auction, Barnaby's back room |
| Sealed Explorer's Map | A map to a Trial Chamber or Woodland Mansion | Auction, Fence's back room |
| Rat Gang Portrait | A 2×2 painting | Auction, Velour's back room |
| ✿ Auroral Crown | Hat with a slow ribbon of northern lights | Auction, Whiskerton's back room (Family) |
| ✿ Brass Wing Scroll | Turns a plain elytra into clockwork brass wings (Restore undoes it) | Auction, Velour's back room (Family) |
| ✿ Rat Familiar | A tiny rat rides on your shoulder | Auction, Cheddarbeard's back room (Family) |
| ✿ Bloomwalker Boots | Flowers bloom in your footsteps and fade | Auction, Lucky's back room (Family) |
| ✿ Showstopper Charm | Every kill ends in gold confetti | Auction, Vinny's back room (Family) |
| ✿ Market Crest Scroll | Puts the Black Market crest on your shield | Auction, Steelwhisker's back room (Family) |

**Back rooms:**

| Trader | Regular | Associate | Family |
|---|---|---|---|
| The Fence | Sealed Explorer's Map, 3 Tokens | Banker's Card, 3 Medallions | Smuggler's Jar, 6 Medallions |
| Old Barnaby | Fair Weather Bell, 6 Tokens | 2 Totems of Undying, 4 Medallions | Spawner Crowbar, 8 Medallions |
| Madame Velour | Rat Gang Portrait, 4 Tokens | Donado Trophy, 4 Medallions | Brass Wing Scroll, 2 Trophies |
| Vinny 'Two-Blades' | 16 Spectral Arrows, 3 Tokens | Netherite Upgrade Template, 3 Medallions | Showstopper Charm, 2 Trophies |
| Sgt. Steelwhisker | Lodestone Locket, 8 Tokens | 3 Wither Skeleton Skulls, 4 Medallions | Market Crest Scroll, 2 Trophies |
| Chef Fromage | A whole cake, 2 Tokens | Enchanted Golden Apple, 6 Medallions | 3 Enchanted Golden Apples, 2 Trophies |
| Prof. Whiskerton | 16 Bottles o' Enchanting, 3 Tokens | Book of Mending, 4 Medallions | Auroral Crown, 2 Trophies |
| Lucky Whiskers | Jackpot Scratch Card, 4 Lucky Tokens | Heartstone, 15 Lucky Tokens | Bloomwalker Boots, 2 Trophies |
| Capt. Cheddarbeard | Buried Treasure Map, 3 Tokens | Heart of the Sea, 3 Medallions | Rat Familiar, 2 Trophies |
| The Bloodbroker | Ominous Bottle, 6 Crystals | Nether Star, 24 Crystals | 3 Heartstones, 1 Trophy |

**Family** members' portraits (their player heads) also go up on plinths around Fountain Plaza, four at most.

**What stayed the same:**
- **Trades:** `tradediff.py` against 1.17 shows every trader's offers unchanged, on both builds.
- Scratch cards, Lucky Tokens, the graveyard, the crypt and the Warden are untouched.
- Everything new is bought through menus that match currency by its Black Market id only, so it can't hit the NBT mismatch that broke trades before.
- **Markets already in your world** get the new ledgers, rats and counters automatically the first time you visit.

## New in 1.17: Lucky Nights get luckier

**Lucky Nights:**
- **Every Overworld hostile can be Lucky now.**
  - Slimes, silverfish, endermites, evokers, vexes, ravagers and guardians join the Lucky roll. They can only be Lucky, not Elite, Champion or a Blood Moon horror.
  - The 26.x parched skeleton joins every tier.
- **Monsters already out when a Lucky Night begins** get their 10% Lucky chance too.
- **Lucky monsters sparkle four times a second** near players, so they're easier to spot.
- **Jackpot monsters**, on Lucky Nights only, at about 1 in 250 Overworld hostile spawns:
  - 35% bigger, with triple health, Strength II and 15% more speed.
  - A gold glow you can see through walls, and enchanted gold armour on anything that can wear it.
  - They drop 6–10 Tokens, 3–5 Lucky Tokens, a 50% chance of a Medallion, and a **Jackpot Scratch Card**: one card, five plays, using the normal scratch-card prizes.
- **Lucky Prime animals:**
  - About 1 in 250 farm animals, or 1 in 50 on a Lucky Night.
  - They glow gold, are bigger, and drop **5 pieces** of their Prime meat.

**Fixes:**
- **Rocket Boots** only fire on a fresh press of jump once you're properly airborne. The take-off jump no longer triggers a burst.
- **Xenite Altar:**
  - A plain click (right or left) now works the altar: socketing, or the reminder.
  - Picking up a placed altar is now **sneak + punch**, so the altar can't vanish while you're trying to socket.
- **Market:**
  - The Void Rat customer has left the Blood Alcove; Void Rats stay rare finds in the outer End.
  - The VIP room (the Gilded Gutter) had its south side open to the cavern. It's walled up now, including in markets you've already found.

**Not changed:** trades. `tradediff.py` against 1.15 shows the only differences are Zorp's (the rocket boots and the updated descriptions on the Tractor Beam, Dowser and Altar).

## New in 1.16: playtest fixes and rocket boots

**Fixed:**
- **Xenite trades.** Zorp (and the mothership quartermaster) refused real shards. Prices now check only the item's identity, name, model and stack size, never its glint. The Chef's Prime-meat prices and Old Barnaby's buy-backs for six builder items had the same glint check and lost it too. Every other price is unchanged.
- **The Xenite Altar does something now.** Every right-click was being thrown away before the altar could see who clicked. Socketing and infusing work as described below.
- **Donado:**
  - His sword sits in his right paw, blade forward and up, and it follows his paw as he walks, runs and jumps.
  - He sits with his legs out in front of him; before, he knelt.
  - Donados you already have update the next time they move.
- **Market:**
  - **Chef Fromage** and **Lucky Whiskers** stand in front of their counters; behind them, a rat-sized trader was hidden. Markets you've already found are fixed automatically.
  - Crowd rats sitting on stairs now sit on the seat, not inside the step.
- **Grappling Hook:** no more Slow Falling when you let go. Letting go mid-air is a real fall now.
- **Levitation Wand (Void Rat):**
  - It only lifts off from solid ground now.
  - Before, using it again in mid-air every 2 seconds stacked the hops into an endless climb.

**New:**
- **Nameplates.**
  - Every trader shows their name above their head, in their colour: market traders, Zorp, the quartermaster, and the Ember and Void Rats.
  - The plates only render within about 13 blocks and never through walls.
- **Rocket Boots** (Zorp: 12 green + 8 violet):
  - Press jump again in mid-air for a rocket burst of about 7 blocks (1.19; it was about 3). You get 1 extra jump, plus +3 Safe Fall.
  - Landing reloads it.
  - It won't fire while flying, gliding or in water.
- **Rocket Boots Mk II** (Zorp: your Rocket Boots + 12 cyan): 2 extra jumps, more armour and toughness, +5 Safe Fall.
- **The Tractor Beam runs on Violet Xenite**, at 5 pulls per shard taken from your inventory, like the Ray Gun's green ammo.
- **The Xenite Dowser** outlines each diamond, emerald and ancient debris block it finds with a glowing shape that shows **through stone** for 10 seconds. Diamonds glow cyan, emeralds green and debris orange.

**Trades:**
- Every trader's offers were compared with 1.15 using `tradediff.py`. Apart from the glint fix above, the only changes are Zorp's: the two rocket boot offers, plus the new descriptions on the Tractor Beam and Dowser.
- A new check, `check_logic.py`, catches the two mistakes behind this round's bugs:
  - a click handler that clears the click before reading who clicked;
  - a price that tests anything beyond the safe item fields.
  It flags the 1.15 build and passes this one.

## New in 1.15: Donado and the Donadians (the Visitors, part 2)

**The Donadians** are the alien race now. They're modelled on your alien Donado build: teal patterned skin, red eyes, a black forehead stripe and open muzzle, pointed ears, white antennae, and a dark coat with teal trim, standing on a glowing lime hover-disc.
- **Zorp is a Donadian now.** His offers are the same, plus one new item (below).
- They have three idle moves: the antennae wiggle, they blink, and the jaw drops when they talk. They also breathe and turn to look at you. Crew members mutter now and then in speech bubbles.
- They come in three outfits: crew (dark coat), scientist (lab coat) and officer (red coat).

**Motherships** (first version) hover about **200 blocks up** over most Overworld biomes. They avoid the high peaks and caves, and they're rare: roughly one every 900 blocks. They only appear in new chunks.
- **Boarding:**
  - Stand in the **green tractor beam** under the ship and it lifts you aboard. The beam reaches down to the ground or the sea.
  - To leave, step back into the beam hole and **tap sneak once**: you float gently down until you land.
- **Lower deck:**
  - the holding pen, with abducted cows, sheep and pigs, and Donado in a cell
  - a Xenite reactor ringed with six crystal deposits you can mine
  - the stores
- **Main deck:** the bridge with its viewport, a lab, crew quarters and a mess hall where the **quartermaster** trades (Zorp's goods). A glass dome sits in the middle with a spinning Xenite hologram.
- Ten Donadian crew are spread around the ship.
- The whole ship is lit, and monsters can't spawn inside.
- To find one, buy a **Sealed Mothership Chart** from Zorp (4 green + 4 cyan) or use `/locate structure bm:mothership`. To build one over your head, use `/function bm:admin/place_mothership`.

**Donado** is a scrappy cream-coloured dog in a patched grey shirt, locked in a mothership cell.
- **Getting him:**
  - Right-click him to set him free. It's free, and he becomes your companion, just like the Frog with Mustache.
  - The cell stays empty for 5 minutes after he leaves (2.56).
  - If you already have a Donado, right-clicking the cell calls yours back to you.
- **Gear:**
  - Right-click him holding a **weapon** (sword, axe, spear, trident or mace) or **armour** and he equips it. His helmet shows on his head, in all 8 vanilla helmet types.
  - **Sneak + right-click** him empty-handed and he drops your gear back.
- **Behaviour:**
  - Right-click empty-handed to make him wait or follow.
  - He fights what you fight and defends you.
  - He has 40 health and heals slowly. Feed him meat to heal him faster.
  - When you take the beam down, he teleports to you once you land.
- **Animations:**
  - **idle:** he breathes, blinks and wags his tail
  - **walking** and **running** (2 frames each, arms and legs swinging; he leans in when he runs)
  - **jumping**
  - **sitting** while he waits

**Nothing existing changed:**
- Zorp's offer list gained the chart, so only Zorp re-syncs (on his own checksum).
- No other trader's offers and no existing item changed. Every trader function and item was compared against 1.14 and is byte-identical, so no items are re-stamped.
- The Frog with Mustache and Wilfrey share the equipping code with Donado and are unaffected.

**Coming later:** the full mothership dungeon (puzzles, the Overseer) and Visitor Night.

## New in 1.14: the Visitors, part 1

**Crashed saucers** appear on the surface in plains, deserts, savannas, badlands, snowy plains, meadows, taigas, forests, windswept hills, cherry groves and pale gardens. They only generate in new chunks. Each is a smoking crater with a tilted saucer, scattered wreckage, Xenite crystal deposits, a **Xenite Altar**, and **Zorp, Collector of Shinies**, an alien trader who stays put. To find one, use `/locate structure bm:crash_site` or `/function bm:admin/place_crash_site`.

**Xenite crystals:**
- Mine a glowing deposit (pickaxe) for 2–4 shards of its colour: **green** (energy), **violet** (gravity) or **cyan** (resonance).
- Deposits only exist at crash sites, so each site is worth about 15–20 shards.

**Zorp's goods (priced in shards):**

| Price | Goods |
|---|---|
| 16 green | **Ray Gun**: a beam of light dealing 7 damage to the first creature it hits, up to 40 blocks. 4 shots per Green Xenite shard, drawn from your inventory. It never hits players, villagers, traders or your allies. |
| 12 violet | **Tractor Beam**: pulls items and XP along your gaze straight to you, and floats creatures in the beam up into the air |
| 12 cyan | **Cloaking Device**: 45 s of invisibility plus Speed. Reusable, with a 4-minute recharge. |
| 10 cyan | **Xenite Dowser**: lights up any diamond, emerald or ancient debris within 8 blocks. Reusable, with a 10-second recharge. |
| 16 violet | **Gravity Boots**: iron boots with lower gravity, higher jumps and +4 safe fall |
| 6 green + 6 violet | **Xenite Altar**, so you can have your own at home |
| 2 of one colour | 1 of the next (green → violet → cyan → green) |
| 3 of any colour | 1 Token |

**The Xenite Altar:**
- **Right-click** with gear in your hand and a shard in your off hand to **socket** it. Each item gets one socket.
  - Green: +1.5 Attack Damage.
  - Violet: +3 Safe Fall and +10% Knockback Resistance.
  - Cyan: +1.5 Luck and +0.5 Reach.
- **Sneak + right-click** to **infuse**. Keep the shards in your off hand:
  - any boots + 6 violet → gravity-infused (your boots keep their enchantments)
  - compass + 6 cyan → Xenite Dowser
  - crossbow + 8 green → Ray Gun
  - glass bottle + 4 cyan → Cloaking Device
  - ender pearl + 6 violet → Tractor Beam
- Right-click with an empty hand for a reminder.
- Placed altars can be punched to pick them up. The one at a crash site stays put.
- Sockets and infusions survive future item updates.

**Nothing existing changed:**
- Zorp is a brand-new trader with his own offers.
- No other trader's offers, and no existing item, changed in this update. The build compared every one byte-for-byte against 1.13.1, so no trader re-syncs and no items get re-stamped.

## Changed in 1.13.1

- **Pickpocket rats are gone.** Any that were mid-heist in a 1.13 world vanish and hand the stolen Tokens back to their owner, if the owner is online. The little holes in the walls stay, as decoration.

## New in 1.13: the market, rebuilt

**New markets generate in new chunks.** Markets you've already found keep their old layout and keep working, with the same traders, trades and key door. To see the new one straight away, run `/function bm:admin/place_market`. It puts you at the end of the new market's entrance tunnel.

**The way in:** dig into the entrance tunnel, carry your key through the vault door, and step out onto a balcony overlooking a domed cavern. Twin stairs lead down to the plaza.

| District | Who | What's there |
|---|---|---|
| **Fountain Plaza** (centre) | Mike the Spikefish | A waterfall falls from a crack in the dome into Mike's pond, with a rumour board, a busker rat on a barrel, and a potion stall, rug seller, fortune teller and skewer grill |
| **Pawn Alley** (north) | The Fence, Old Barnaby | A grimy street under a timber terrace, with festoon lanterns, banners and stacked crates |
| **Plaza corner** | Madame Velour (Outfitter) | Her purple-and-white stall |
| **The Stacks** (terrace) | Prof. Whiskerton | A library up on the terrace |
| **The Docks** (west bank) | Capt. Cheddarbeard, *secretly* | An underground river with a pier, a crane and moored rowboats. The Captain hides in the Rat Gang HQ behind a mouse hole by the dockmaster's office. Wear a **Minish Cap** to crawl in. |
| **The Lucky Den** (far bank) | Lucky Whiskers | A gold-and-blackstone casino with marquee lights, slot-machine props, card tables and a roulette wheel. Scratch cards and Lucky Tokens are unchanged. |
| **The Forge Pit** (east) | Vinny, Sgt. Steelwhisker | A lava channel behind bars, a hot catwalk, hanging crucibles and **steam vents** |
| **The Gnawed Flagon** (east) | Chef Fromage | A crowded tavern with cheese wheels on the bar and a chimney |
| **The Blood Alcove** (south-east) | The Bloodbroker | Red-lit, behind a raised portcullis, with hanging cages, a debtors' list and gibbets outside |
| **The Dark Auction** and **The Gilded Gutter** (behind the north wall) | *(coming next)* | Built and visible through their gates. They open with the slots, the auction and the upgrading key. |

**It feels alive:**
- **Neon signs** flicker over every district.
- **The crowd:** about 20 rats sit in the tavern, play cards, haul on the docks and guard the balcony and terrace. They turn to watch you as you pass.
- **Walkers:** three rats stroll round the fountain, down Pawn Alley and along the far bank, and stop to look at you up close.
- **Speech bubbles:** traders and the crowd mutter when you come near.
- **Sound:** each district has its own ambience (forge clangs, tavern burps, dripping water, card-table chimes, a slow heartbeat in the Blood Alcove), and the busker plays an original tune.
- **The cavern itself:** dripstone, spore blossoms and glow lichen.

**It's a little dangerous:**
- **Steam vents** in the Forge Pit hiss, then blow. If you're standing on the grate, you're scalded and popped into the air.
- **The Drop** is a rickety plank shortcut over the river with missing boards and no rail. The stone bridge is the safe way across.
- The riverbank railing has gaps, and the Forge's catwalk runs right over the lava.

**No mob spawning, by design:**
- The structure forbids natural monster spawns inside its bounds.
- Every walkable spot is lit.
- Hostile mobs that wander in are removed, as before.
- The cavern walls are made of stone that worldgen springs, lichen and dripstone can't attach to.
- Markets never generate in the Deep Dark.
- On first load, a market clears any monster spawner or sculk shrieker that worldgen squeezed into its walls.
- Nothing flammable is within reach of the lava.

**Trades and items can't silently break again.**
- Every build now runs a trade and item audit (`check_trades.py`). It proves all of the following:
  - every item carries the current version stamp;
  - every price matches the real item exactly;
  - what one trader sells is accepted by every other;
  - mob drops match the item definitions;
  - spawn offers equal refresh offers;
  - every trader marker has a spawner;
  - every price can actually be obtained;
  - no scoreboard is used before it exists.
- In worlds, held items are restamped and traders re-sync whenever their offers change (from 1.12.1).

**Also fixed:** on a brand-new world, rat traders could stretch into tall pillars until the first reload. A score constant was set before its objective existed. The load function now creates every objective first.

## Fixed in 1.12.1

- **Custom-currency trades work again (Lucky Whiskers and everyone else).**
  - Trade costs must match an item exactly, including its hidden version stamp. When 1.12 re-stamped everyone's Tokens, Trophies and Lucky Tokens to the new version, the traders kept asking for the old stamp, so those trades refused.
  - Traders now re-sync automatically whenever their offer list or the item version changes.
- **The Outfitter (Madame Velour) has her full stock back.** An old one-time refresh was overwriting her offers, and every new market's, with a pre-1.10 list. That dropped the **Grappling Hook** and the **Wings of the Elder Dragon**. Her name now reads "Madame Velour, Outfitter", and the stall sign in newly generated markets says OUTFITTER.
- **Grappling Hook rework.**
  - The hook now reels you in on an invisible, weightless carrier, so your camera stays steady (no more jitter).
  - You **stick wherever it bites**, wall or ceiling, and hang there until you let go: right-click again, or sneak.
  - Slow Falling only kicks in when you let go.


- **Lucky Nights.** At dusk on any night that isn't a Blood Moon, there's a **1% chance** of a Lucky Night. Until dawn, Overworld monsters are **Lucky about 10% of the time** (normally 0.6%), with Elites and Champions at their usual rates. A gold title, a yellow boss bar and drifting gold motes mark the night. Lucky Nights and Blood Moons never overlap: a Blood Moon day can't roll one, and raising an Effigy cancels it.
- **Blood Moons are Overworld-only, in presentation as well as mechanics.** Players in the Nether, the End or the Hollow Throne no longer get the titles, sounds, boss bar or chat. Its mobs were already Overworld-only.
- **Bloodforge Sigil, new rules:**
  - It only works **under a Blood Moon, in the Overworld**. Otherwise it refunds itself.
  - Each use costs **one max heart, forever**, with no cap. It refuses (and refunds) once you're down to a single heart.
  - **Heartstones** pay back a Bloodforge heart before they add a bonus heart.
- **Two new field traders**, each with its own currency. Every minute, each player has a **1 in 25** chance of one setting up shop within about 24 blocks. Only one of each can be out at a time; it packs up after 20 minutes. Follow the column of particles to find it.
  - **The Ember Rat** appears in **the Nether**. Pay in **Ember Scales**, a 30% drop from blazes, wither skeletons, magma cubes, ghasts, hoglins and piglin brutes killed in the Nether.

    | Price | Goods |
    |---|---|
    | 6 | **Lava Wader Charm**: for 60 s, lava sources under you crust into magma, then cool back once you've passed. Fire Resistance is included. |
    | 4 | 2 Wither Roses |
    | 20 | **Fire Charge Launcher skin** for Snake Eyes. It's reusable: use it with Snake Eyes in your off hand to switch the look on or off. |
    | 24 | **Blaze-forged Netherite Upgrade** (a netherite upgrade smithing template) |
    | 3 | 1 Token |

  - **The Void Rat** appears in **the outer End** (more than 700 blocks from the centre). It has purple eyes, floats a little off the ground, and its ears blink from place to place. Pay in **Void Shards**, a 25% drop from endermen and shulkers killed in the End.

    | Price | Goods |
    |---|---|
    | 10 | **Pearl of Return**: one teleport to where you last died. It won't work for void deaths, in dungeons or for deaths in the Hollow. |
    | 6 | 2 Shulker Shells |
    | 8 | **Elytra Repair Kit**: fully mends the elytra you're wearing, or the one in your off hand |
    | 16 | **Levitation Wand**: a short, floaty hop with a soft landing (2 s recharge) |
    | 12 | **Chorus Compass**: use it in the End to point it at the nearest End City; use it again to re-tune |
    | 30 | **Void Rat Statue**: placeable like the boss trophies. Punch it to pick it up, right-click to turn it. |
    | 3 | 1 Token |

## New in 1.11

- **The Bloodforge Sigil has a blood price.**
  - It costs **48 Blood Crystals + 1 Trophy**.
  - Every use permanently takes **one heart** of max health, and the sigil can take five at most. After that it refuses and refunds itself. Heartstones still add hearts back on top.
- **Prices, round two:**
  - Utility and cosmetic boots are back to Medallions: Pegasus 4, Bouncy 3, Flame/Heart/Soul 2.
  - The OP tiers cost more: tier II upgrades are +10 Medallions for armour and +12 for weapons and tools; tier III is +5 Trophies (Biggoron's Sword +6). The Blood Moon armour sets now take 8 (Crimson) or 10 (Vampire) Medallions.
  - The two unbreakable elytras stay at 10 and 12 Trophies.
- **Grappling Hook** (Outfitter, 12 Tokens). Right-click a block up to 32 away and you're reeled to it along a rope. Right-click again to let go. It won't bite inside dungeons. (Since 1.16, letting go gives no Slow Falling.)
- **Scratch cards, new prize table** (Medallions and Trophies are now much rarer):
  - Prime meat (a pair).
  - Back-shelf goodies (weather vials, aged cheddar, Sanguine Tonic).
  - A piece of tier I gear.
  - The Grappling Hook.
  - Rare: the **Prospector's Paxel** (pickaxe, shovel and axe in one).
  - Rare: **Snake Eyes** (a quick dagger with Looting IV and +2 Luck).
  - Rare: the **High Roller** (crossbow with Multishot and Piercing IV).
  - Rare: a Heartstone.
  - Jackpot: **Lucky 7**, a netherite sword in a gold-sword skin, unchanged.
- **Prime animals** are four times as common (1 in 25).
- **Animation.**
  - The Frog with Mustache hops when he walks: sit, crouch, leap. He bounds faster when running, kicks out mid-air, and when idle he breathes and blinks.
  - The rats breathe, sniff, flick their ears and swish their tails.
  - It's done with pose models swapped like flip-book frames, plus smooth bobbing.

## New in 1.10

- **Prices rebalanced.**
  - Unbreakable gear is now the most expensive thing in the market, because you never have to replace it:
    - Wings of the Golden Rat: **10 Trophies**.
    - Pegasus Boots: **2 Trophies**.
    - Bouncy Boots: **1 Trophy + 6 Medallions**.
    - Flame, Heart and Soul Boots: **1 Trophy** each.
  - Tier upgrades now cost the same at every armourer: tier II is +8 Medallions, tier III is +3 Trophies. The Bloodforge armory's upgrades were cheaper before.
  - Two exploits are gone. The Captain sold Medallions for 8 Tokens; now it's 9, like the Fence. The Bloodbroker sold a Trophy for 24 Crystals; now it's 48.
  - The pawn shop still pays half, and a one-Trophy item pawns for 3 Medallions.
- **Wings of the Elder Dragon** (Outfitter: 12 Trophies + a dragon head). An unbreakable violet-and-black elytra with +5 Armor, +3 Toughness and Protection IV. It gives Fire Resistance while worn and leaves a trail of violet flame while gliding.
- **The Frog with Mustache** (formerly Sir Croaksworth) has left the market for his own **stilt hut in swamps and mangrove swamps**. The Fence and the Professor sell a **Sealed Croaker's Map** (3 Tokens) to find one.
  - **Hiring:** right-click him and pay one Medallion, and he follows you everywhere. He fights whatever you fight, defends you, keeps up with you and heals slowly. If you already have him, right-clicking him in a hut calls him back to your side.
  - **Equipping:** right-click him holding a sword, axe, spear, trident or mace and he takes it, handing back whatever he held before. Do the same with any helmet, chestplate, leggings or boots. The gear really counts: its damage, armor and enchantments all apply. He wears a little knight's helm matching your helmet, and you can see the weapon in his hand.
  - **Commands:** right-click him empty-handed to make him wait or follow. Sneak and right-click empty-handed to take all your gear back. Feed him any meat to heal him.
  - **If he falls**, everything he was carrying drops, and you can hire him again.
  - Admins: `/function bm:admin/place_frog_hut`, `/locate structure bm:frog_hut`.

## New in 1.9

- **Graveyards are rarer and don't float.** There's now about one per 64×64 chunks, up from one per 26×26. Every column under the yard is solid soil over stone down to the crypt floor, so on a cliff or riverbank the yard sits on a plug of ground instead of hanging over the drop. Graveyards that already generated aren't changed; only new chunks get the new placement.
- **Blood Moons are much nastier.**
  - Of the hostile mobs that spawn in the Overworld during a Blood Moon, about **35% are Elite** (up from 15%), **20% are Champion** (up from 5%) and **8% are horrors** (up from 3%).
  - On top of normal spawning, a **surge** spawns extra mobs 14–30 blocks from any player outdoors. Each player has about a 1-in-3 chance per second, capped at 6 surge mobs within 64 blocks. Most are **Nether mobs**: blazes, wither skeletons, magma cubes, piglin brutes with golden axes, and hoglins. The piglins and hoglins don't zombify. The rest are zombies, skeletons and spiders.
  - Surge mobs get the same Elite/Champion/horror roll as everything else.
  - At dawn the Nether mobs are dragged home in a puff of soul fire.
  - The Moon Ward lantern still only stops horrors, not the surge.
- **Frog with Mustache**, a frog with a handlebar moustache, red bow tie and gold pin, sits on a lily pad in Mike's pond. He's a 3D model only, with no trades yet. He also hops into markets placed with 1.8.
- **The rats (and the frog) turn to watch you.** They swivel to face the nearest player within 10 blocks and glance around when nobody's near. They only turn left and right, never tilt, so their feet stay on the floor.

## New in 1.8

**Upgrade trade-ins fixed.** An upgrade now asks for the *exact* previous-tier item as it was sold: same name, lore, enchantments and attributes. The trade screen shows that full item. To make sure your items qualify, every Black Market item in your inventory, armor slots and off hand is re-synced to its current definition when you pick it up or log in. That includes items bought in older versions, whose names or data may have drifted. Re-syncing resets a gear piece's enchantments to its original set, but keeps its durability, custom name and skin.

**The new Black Market** (newly generated markets only) is a two-storey thieves' den around a flooded cistern:
- **Ground floor:** the Fence, Vinny, Madame Velour, Old Barnaby, Chance Corner, Steelwhisker and the Bloodbroker trade around a pond. A waterfall fountain pours into it, and **Mike the Spikefish** lives there. Mike is persistent and invulnerable; his name shows when you look at him, and he will puff at you.
- **Upper floor:** two timber staircases lead up to Prof. Whiskerton's library, **the Gnawed Flagon** (a tavern with Chef Fromage's kitchen), **the Nest** (a resting room with bunks and a barred hearth), and **the Armory & Treasury**, a vault of gold behind iron bars.
- **Atmosphere:** water drips from the ceiling, fireflies drift over the cistern, and lantern chandeliers hang above it.
- **Unchanged:** Cheddarbeard's den behind the mouse hole and the vault door are still there.

**Flashier names.** Every custom item now has a bold name framed by a themed symbol: ⚔ weapons, ⛏ tools, ⛨ armor, ➶ bows, ❖ ⛃ ✪ ♛ currency, ☽ Blood Moon goods, ✿ cosmetics, and more. Tier III and legendary items also get gold ✦ stars.

**Rat-themed currency art.** Medallions now carry a rat's face on a purple ribbon. Trophies are a golden cup with rat ears, a rat face and a tail.

**New skin scrolls** (Prof. Whiskerton): Bag of Rocks, RPG Launcher, Butter Sock, Pool Noodle and Rubber Duck.

## New in 1.7

**Economy.** Everything bought with Tokens or Medallions costs about **50% more** (rounded up), including trade-in upgrades. Currency exchanges and buy-backs are unchanged.

**3D rats.** The rat traders are now blocky 3D figures: Chef Fromage in a chef's hat and apron, Prof. Whiskerton with spectacles and a book, Lucky Whiskers in a green bowler holding a four-leaf clover, Capt. Cheddarbeard in a tricorn, eyepatch and red coat, and Sgt. Steelwhisker in an iron helmet with a spear. Rats in existing markets switch over automatically.

**Trade fix.** Every trade now shows and charges the right item: Tokens, Medallions, Trophies, and the named previous-tier piece for upgrades. Before, the trade screen showed plain totems and every price collapsed to 1. Upgrades accept your previous-tier piece even if you've enchanted or worn it since. Traders also hide their names until you look at them, so they don't show through walls. Traders in existing markets are fixed automatically.

**The graveyard is now a gothic one.** A 3-high wall of stone-brick piers and iron bars surrounds it, with an arched gatehouse. The mausoleum sits at the back, with a steep slate roof, pinnacles and barred windows. Some graves now carry an epitaph.

**The crypt is now a labyrinth.** The Warden wakes the moment you enter. The altar is at the heart of the maze, and the way out opens in a far corner, so you have to cross the maze twice. Crypt floors are bottom slabs, so nothing else spawns down there. The key on the altar no longer glows through walls. *(Graveyards you've already found keep their old layout. New ones generate in unexplored chunks, or use `/function bm:admin/place_graveyard`.)*

**Heartstones (permanent hearts).** Rare finds in loot chests across the world: 1–2% in most chests, 3–5% in bastion treasure, end cities, mansions and ancient cities. Eat one for **+1 max heart, forever**, up to **+10** (two full rows). They're kept through death. Once you're at the cap, a Heartstone refunds itself.

**Health hard cap: three rows (60 health).** Base health, Heartstones, armor bonuses, feasts and Health Boost add up normally, but max health never goes above three full rows. Anything past that is trimmed off. Golden absorption hearts are temporary shields and aren't counted.

**Weather vials** (Prof. Whiskerton):

| Vial | Price | Effect |
|---|---|---|
| Vial of Clear Skies | 3 Tokens | Clears the weather for 10 minutes |
| Vial of Rainfall | 3 Tokens | Rain for 10 minutes |
| Vial of Thunder | 6 Tokens | A thunderstorm for 10 minutes |

Vials work only in the Overworld. Everyone is told who drank one, and all vials share a **5-minute cooldown**. If you can't use a vial, it's refunded.

**New Blood Moon goods** (the Bloodbroker):

| Item | Crystals | What it does |
|---|---|---|
| **Moon Ward** | 6 | Holds the *next* Blood Moon back one cycle (30 days). It's announced to everyone. It can't stop a moon that's already rising or one an Effigy called. The Almanac shows the delay |
| **Warding Lantern** | 4 | Use during a Blood Moon. Until dawn, no horror (and no Monstrosity) can rise within 48 blocks of you. Ordinary monsters still spawn |
| **Crimson Compass** | 6 | Reusable. Hold it during a Blood Moon to see an arrow and distance to the nearest horror, or to the Monstrosity if it's out |
| **Blood Bounty** | 3 | Sign it during a Blood Moon, then slay 5 horrors before dawn for **8 Crystals and a Medallion**. Unfinished bounties expire at dawn |

**Cosmetic charms** (Lucky Whiskers): Ember, Frost, Petal, Soul, Gilded and Sweetheart cost 5 Lucky Tokens each. The **Storm Cloud Charm** costs 7 and puts a little raincloud over your head, with the occasional spark of lightning. Keep a charm anywhere in your inventory to show it. They're cosmetic only, and one shows at a time. They hide while you sneak, so Shadowstep stays invisible.

**Legendary: Blood Eclipse.** It can't be bought. It's a 10% drop from killing the Blood Moon Monstrosity. A dark red moon hangs over your head, a ring of blood-red light circles you, and red dust drifts down. If you carry it alongside other charms, the Eclipse is the one that shows.

Traders in markets that already exist pick up the new trades automatically.

## How the loop works

1. **Find a haunted graveyard.** It's a fenced field of graves with a mausoleum, in plains, forests, taigas, swamps, meadows, savannas and pale gardens. Use `/locate structure bm:graveyard` to cheat.
2. **Read the gravedigger's book** on the lectern by the gate.
3. **Walk to the mausoleum at the back of the graveyard** and go down. A long catacomb gallery, lined with skull niches, leads to the crypt. The crypt is protected: you're switched to Adventure mode inside it, and digging near it gives you Mining Fatigue.
4. **The moment you step into the antechamber, the Warden wakes.** Darkness falls, a shriek echoes from below, and the Warden digs out of the altar chamber at the heart of the crypt. It stays until every player has left the crypt, then sinks back into the ground.
5. **Find your way through the labyrinth.** It's a maze of narrow, sculk-crusted tunnels, about 150 blocks of walking to the centre, with dead ends full of cobwebs. Every floor is a bottom slab, so no other mobs spawn down there. Sneak, and don't run.
6. **Crouch beside the altar** to take the **Black Market Key** and a Sealed Smuggler's Map. A hidden door grinds open in **a far corner of the maze** and stays open. Get there with the Warden still hunting, and **climb the ladder** up to a well behind the graveyard wall. **Each crypt holds only one key.** Once it's taken, that crypt is spent for good, so other players need to find their own graveyard.
7. **Break the map's seal** (hold right-click) and follow the red X to a buried **Black Market**.
8. Dig down to the vault entrance tunnel. Doors open for anyone carrying a key. Players without a key are tossed out by rat bouncers, even if they dig in.

## Inside the market

*(Stall positions below are for markets generated before 1.13. See "New in 1.13" for the new layout. Every trader sells the same things in both.)*

| Stall | Who | Sells |
|---|---|---|
| North counter | **The Fence** | Diamonds/netherite → Tokens; Token → Medallion → Trophy; maps |
| West stall | **Vinny 'Two-Blades'** | Tier I weapons and tools, plus the Tier II and III upgrades |
| East stall | **Madame Velour** | Armor sets and upgrades, builder gear, hats and trail boots |
| Upstairs library | **Prof. Whiskerton** (rat) | Lore books, maps, skin scrolls |
| Upstairs tavern | **Chef Fromage** (rat) | Permanent-buff feasts from Prime meat; buys Prime meat |
| SE corner | **Lucky Whiskers** (rat) | Scratch cards, Minish Cap, Four-Leaf Charm |
| SW counter | **Old Barnaby** | Buys back any gear at about 50%, and breaks big currency into small |
| South wall, west | **Sgt. Steelwhisker** (rat) | Specialty armor sets (Shadowstep, Juggernaut, Architect, Tidecaller), all three tiers |
| South wall, east | **The Bloodbroker** | Trades Blood Moon Crystals for currency, Crimson Revenant and Vampire Lord sets, Sigils, Effigies, Tonics, Almanacs |
| Behind the west wall | **Capt. Cheddarbeard** (rat) | Secret trades. Wear a **Minish Cap** and crawl through the mouse hole |

All trades are unlimited, have no cooldown, and give no XP. The traders are invulnerable and never move.

**Upgrades work by trade-in.** You hand over the lower-tier item plus higher-tier currency. For example, *Kokiri Sword + 12 Medallions → Master Sword*.

## Earning currency

- **Elite mobs** (about 5% of hostiles) wear maxed armor or carry buffs. They drop 1 Token, with a 35% chance of 1–2 more.
- **Champion mobs** (about 1.2%) are bigger and faster, and bring minions. They drop 3–5 Tokens, with a 30% chance of a Medallion.
- **Lucky mobs** (about 0.6%) sparkle gold and drop Lucky Tokens. The **Lucky Golden Goose** is a rare warm-variant chicken that drops 2–4 Lucky Tokens.
- **Prime animals** (1%: pigs, cows, mooshrooms, sheep, chickens, rabbits) drop glinting Prime meat.
- **Loot chests** in dungeons, temples, strongholds, bastions, end cities, ancient cities and similar places can hide Tokens, Medallions and Lucky Tokens.

## Specialty armor sets

Every specialty set has a trade-off: perks are listed in blue on the item, drawbacks in red. Each set comes in three tiers. Tier I costs Tokens. Tier II costs the Tier I piece plus 10 Medallions. Tier III costs the Tier II piece plus 5 Trophies. Wearing all four pieces of a set, in any mix of tiers, gives a full-set bonus and a particle display unique to that set: two orbiting particle streams plus a signature effect.

| Set | Trade-off | Full-set bonus | Particles |
|---|---|---|---|
| **Shadowstep** | +6–10% speed per piece, -0.5 attack per piece, faster sneaking, higher jumps | Invisible while sneaking | Smoke wisps (hidden while sneaking) |
| **Juggernaut** | +attack, +health, heavy armor, knockback resistance, -3–5% speed per piece | Resistance | Crit sparks and an ember ring |
| **Architect** | +block reach, +mining speed, boots that step up blocks and soften falls. **Drawback:** -0.5 attack and -0.25 melee reach per piece (a builder, not a brawler) | Haste | Blue blueprint dust and end-rod sparks |
| **Tidecaller** | Faster swimming, longer breath, fast underwater mining. **Drawback:** -5% speed per piece **on land only** (it lifts the moment you're in water), and you burn 25% longer per piece | Conduit Power and Dolphin's Grace while in water | Bubbles and nautilus |
| **Crimson Revenant** | Netherite base, +2 max health per piece | When you're hurt, **3 undead Revenants** rise to fight for you (2 zombies and a skeleton). They last 30 seconds, with a 45-second cooldown | Blood dust and souls |
| **Vampire Lord** | Netherite base, +1 max health per piece | Hitting a monster **drains its life** (heals you about 2 hearts, at most once every 2 seconds). Night Vision, but Weakness in direct sunlight | Dark red dust and falling blood drips |

The existing Smuggler, Kingpin and Hero sets now have full-set bonuses and particles too: Smuggler gets Luck with wax sparks, Kingpin gets Fire Resistance with violet dust and enchant runes, and Hero gets Regeneration with a glow ring and golden halo.

**Golden Wings:** a legendary unbreakable elytra with armor, toughness, Protection IV and golden wing art. It leaves a gold trail while you glide. Madame Velour sells it as the Wings of the Golden Rat for 10 Trophies.

## Blood Moons

Every **30th night** (day 29, 59, 89 and so on, from the world's day counter), a Blood Moon rises at dusk:

- An hour beforehand, chat warns that the sky is turning red.
- At dusk, every player in the Overworld sees a **"The Blood Moon Rises"** title with a raid horn, even underground. (Since 1.12, players in other dimensions are left out.) Two seconds later comes a distant wither cry; the heartbeats start a few seconds after that. A red boss bar tracks the night's progress, red ash falls when you can see the sky, and you can hear heartbeats.
- **You can't sleep.** Anyone who lies down gets woken.
- In the Overworld, about 35% of hostile spawns are Elite and 20% are Champion, and a surge of extra mobs (mostly from the Nether) spawns around players who are outdoors. See "New in 1.9".
- **Blood Moon horrors** (8% of hostile spawns) appear. They glow **red**, track you from **96 blocks** away, have 5× health, Strength II and Resistance I, wear netherite with a rib trim, and are bigger and faster. Their hits ignore armor and enchantments with 1.5 hearts of extra **blood damage** plus a short Wither. Their creepers are always **charged**. They're survivable in top gear, but two or three at once is a real fight.
- Horrors **always drop 1–2 Blood Moon Crystals**, plus Tokens and a 15% chance of a Medallion.
- At dawn, the moon sets and a title announces it.

### What Blood Moon Crystals are for (sold by the Bloodbroker)

| Crystals | Get |
|---|---|
| 1 | 3 Tokens |
| 8 | 1 Medallion |
| 48 | 1 Trophy |
| 2 | **Sanguine Tonic**: Instant Health II, Strength II (1:00), Absorption (0:30) |
| 2 | **Blood Moon Almanac**: reusable, tells you how many nights until the next Blood Moon |
| 16 | **Bloodforge Sigil**: hold any tool, weapon or armor piece in your off hand and use the sigil to make it **permanently unbreakable** |
| 24 | **Crimson Effigy**: summons a Blood Moon *tonight*, announced to every player |
| 10–16 + 5–6 Medallions | Crimson Revenant and Vampire Lord set pieces |

## Mounted mobs

Mounts only appear where they make sense: open sky with room overhead for riders, and in water for the nautilus. They never appear in caves, the Nether or the End.

| Rider | Mount | Chance |
|---|---|---|
| Champion zombie, Champion zombie villager | Zombie horse | 35% |
| Champion skeleton, Champion stray | Skeleton horse | 35% |
| Champion husk | Camel husk | 35% |
| Champion drowned (in water) | Zombie nautilus | 35% |
| Champion spider | Carries an **Elite skeleton** (spider jockey) | 40% |
| Blood Moon skeleton or stray | Red-glowing **Blood Moon Steed** (skeleton horse) | 40% |
| Blood Moon zombie | Red-glowing **Blood Moon Steed** (zombie horse) | 30% |

Horses and camels come **tamed and saddled**. Kill the rider and the mount is yours. Once a player has ridden one, it stays for good, and a Blood Moon Steed stops glowing. Unclaimed mounts more than 100 blocks from every player are cleaned up.

## Elite, Champion and Lucky mobs everywhere

Tiering now applies in the **Nether and the End** as well: zombified piglins, piglins, piglin brutes, hoglins, ghasts, blazes, wither skeletons, endermen, shulkers, plus phantoms, breezes and zombie villagers. Tiered mobs that wander more than 100 blocks from every player are removed, so they don't pile up.

## Who hears what

- **Global events** play for every player wherever they are: Blood Moon rise, warning and dawn, and the Crimson Effigy.
- **Local events** only reach the players involved. The Warden emergence plays only for players **inside the crypt**, not for people walking the graveyard above. The Monstrosity's intro, roars and boss bar reach only players within about 48–64 blocks. Champion spawn cues are positional and play at most once per second per player. Scratch-card and item sounds play only for the user.

## Feasts (permanent buffs)

Each feast's effect lasts until you die. Milk only removes it for a second before it comes back. A Tier II feast requires that you've already eaten its Tier I feast; if not, the dish is refunded. Available buffs: Health Boost, Strength, Resistance, Haste and Speed.

## Scratch cards

| Prize | Chance |
|---|---|
| 1–3 Tokens | 28% |
| Prime meat (a pair) | 16% |
| Nothing | 12% |
| 2 Lucky Tokens | 12% |
| A back-shelf goodie (weather vial, Aged Cheddar or Sanguine Tonic) | 11% |
| A piece of tier I gear | 9% |
| Grappling Hook | 5% |
| A Medallion | 3% |
| Prospector's Paxel | 1.6% |
| Snake Eyes | 1.2% |
| High Roller | 0.6% |
| Heartstone | 0.2% |
| A Trophy | 0.2% |
| **Lucky 7** sword | 0.2% |

The Lucky 7 plays the challenge-complete fanfare, then your own fireworks a second later, and chat tells everyone you won.

Scratching makes a brushing sound. There's a half-second pause before the result, so the reveal lands on its own.

## Skin scrolls

Hold the item to reskin in your **off hand**, then use the scroll in your **main hand**. Enchantments are kept. Use the Restore scroll to get the original look back.

## Admin commands (operators)

- `/function bm:admin/help`
- `/function bm:admin/give/<currency|gear|builder|cosmetic|feast|food|meat|skin|book|lucky|key|map|jackpot>`
- `/function bm:admin/give/gear` now includes every armor set and the Golden Wings. `/function bm:admin/give/blood` gives the blood goods, and `currency` includes Blood Moon Crystals
- `/function bm:admin/spawn_monstrosity` spawns the hidden boss at your feet. It needs an active Blood Moon or it retreats
- `/scoreboard players set #forced bm.bm 1` forces a Blood Moon at the next dusk, the same as using an Effigy
- `/function bm:admin/place_market` builds the 1.13 market with you at the end of its entrance tunnel. `/function bm:admin/place_graveyard` builds a graveyard at your feet
- `/function bm:admin/lucky_night` makes tonight a Lucky Night. `/function bm:admin/ember_rat` and `/function bm:admin/void_rat` summon a field trader near you
- `/function bm:admin/place_crash_site` builds a crashed saucer around you. `/function bm:admin/give/alien` gives the Xenite shards and alien tech
- `/function bm:admin/place_mothership` builds a mothership 40 blocks above you, with its tractor beam right where you stand
- `/function bm:admin/invasion_now` makes tonight an invasion night (`invasion_stop` ends it). `/function bm:admin/spawn_warlord`, `spawn_abductor` and `spawn_overseer` summon a Vorn boss. `/function bm:admin/place_dreadnought` builds the Vorn Dreadnought 40 blocks above you
- `/function bm:admin/auction_now` starts a Dark Auction right away; `/function bm:admin/auction_stop` stops it and refunds every bid
- `/scoreboard players set <player> bm.stand 500` sets someone's Standing (their tier, key and portrait catch up within a second)
- `/function bm:admin/bank_interest_on` / `bank_interest_off` turns Rat Bank interest on or off (1 Token per 50, paid at each auction)
- `/function bm:admin/uninstall` stops all loops before you remove the pack

## How 1.21 was checked

- The real 26.3 server loads both packs with **0 errors**.
- The command, NBT, structure, resource pack, trade and logic checkers report **0 errors**. That's 12,962 command lines (17,171 on the TEST build), 624 NBT blobs (773), and 703 trades (729), at item version 22.
- **Checked live in the server:**
  - A happy ghast with a harness accepts a rider, and primed TNT takes the fuse and blast-power fields the bomb uses.
  - The drill's dig step mines diamond ore into a diamond.
  - On a freshly placed market, the three traders step up to their counters (facing kept) and the newcomers' lectern and sign appear.
- **Not hand-played:** anything that needs a real player (flying the skiff, Sunburst, drilling by hand). Those passed the static checks only.

## How 1.20 was checked

- The real 26.3 server loads both packs with **0 errors**, after a restart for the new worldgen.
- The command, NBT, structure, resource pack, trade and logic checkers all report **0 errors**. That's 12,576 command lines (16,610 on the TEST build), 768 NBT blobs on the TEST build, and 689 trades (715 on the TEST build).
- **Checked live in the server:**
  - A crash site carved on a real hillside.
  - Every Vorn mob and boss spawned.
  - The Dreadnought and a mothership placed, with loot barrels and guards.
  - A fresh market placed: all 44 cushions spawn and stay put.
  - The Dockmaster spawns behind his counter in an existing market.
  - The water sweep removes stray water and leaves the river and fountain alone.
- **Not hand-played:** anything that needs a real player (jumps, flight, rides, the satchel, the rays). Those passed the static checks only.

## How this was verified against 26.3

1.19 was checked against the **official 26.3 server and client jars**. Wherever possible the check is the real game, not a model of it:

- **The real 26.3 server loads both packs with zero errors.** It runs headless in its built-in test mode and reports every function, loot table, advancement, predicate, enchantment, worldgen file and dialog it can't parse.
- **Runtime test inside that server:**
  - **Trades:** every trader (11 market NPCs, their refresh functions and both field rats) is spawned and its offers are read back from the live entity: 630 recipes (646 on the TEST build).
    - All come back identical to what the pack writes. The only differences are 26.3 dropping fields that are already at their default.
  - **Payments:** every trade cost, and every exact item check in the pack's commands, is tested against the item exactly as a player receives it from its loot table. That's 355 checks (440 on the TEST build), all passing.
  - **Entity data:** every summon and every entity data write in the pack is replayed so 26.3 decodes it: 605 (731 on the TEST build). Two deliberately broken samples are included to prove the check catches errors, and nothing else is flagged.
  - **Structures:** every structure template is placed with `/place template`, exactly like the admin commands. Nothing breaks or drops (`tools/droptest.py`).
  - **Command templates:** every command template, the lines filled in at run time, is parsed by the server with sample values.
- **Static checks** run on 26.3 reference data generated from the jars (the server's data generator and the client's assets):
  - About 9,000 command lines (13,000 on the TEST build) are parsed through the 26.3 command grammar with every id checked against the 26.3 registries.
  - The NBT, structure, JSON, resource pack, trade, dialog and logic checks from earlier phases all run too. Every check reports 0 errors.
- **Trade diff:** `tradediff.py` against the 1.18 release shows every trader unchanged.
- **Multiplayer audit:**
  - Per-player data (bank, burrows, mercenary, auction deliveries) is keyed by player id.
  - Every "this player" tag is set and cleared within the same action.
  - Server-wide messages are only the intended announcements (boss kills, jackpots, weather vials, Family portraits).
  - The weather cooldown and the auction timer are deliberately shared.
  - Menu buttons are enabled for every player each tick.
  - Nothing needs more than the default function permission level (2).

The 26.3 format changes the build handles: loot conditions and functions keyed by `type`, `modifier` instead of `functions` on loot entries, pools and tables, single-condition predicates, `#` on map destinations, the renamed explorer-map structure tags and the `mansion` map marker, the new block-state format in entity data, the dedicated explorer-map items, `slot_source` slots, and pack formats 121 (data) and 97.1 (resources). The generators keep their source shapes, and a translation layer (`mig263.py`) writes 26.3. It refuses to build if a removed 26.2 form shows up.

Run `python3 check262.py && python3 check262_nbt.py && python3 check262_assets.py && python3 check_trades.py && python3 check_logic.py` from the source zip to repeat the static checks, and `python3 tradediff.py <old build> <new build>` to list every trade that changed between two builds. The build also proves, for the market structure, that every trader can be walked to from the vault, nothing flammable is within lava's reach, every walkable spot is lit, and the market is sealed from the world outside except for the tunnel's end.

## Fixed in 1.6

- **Mob setup ran at world spawn.** Since Phase 1, Elite/Champion/Lucky setup ran at the world spawn point instead of at the mob. Champion bodyguards spawned at world spawn, Champion sounds played there, and the Blood Moon's Overworld-only check passed for mobs in every dimension. It now runs at the mob itself.
- **Warden entrance re-timed.** Three escalating Warden warnings, heartbeats that speed up and swell, the shriek, then a beat of silence before the Warden digs out. Previously the shriek and the emergence overlapped.
- **Item use sounds** no longer repeat harsh clips while held. The Sigil hammers, the Effigy whispers, and the big sounds play once on completion, staggered.

## What still needs an in-game test

These are about behavior, not syntax:

**1.19 (26.3):**
- **Trades:** trade once with every trader and check each offer goes through, paying with currency picked up from mobs and chests, not just currency bought from a trader. This is the standing rule after every update. The live-server test above covers it, but an in-game trade is the final word.
- **Explorer maps:** open a Smuggler's Map and a Sealed Explorer's Map, and check both show the marker.
- **Display blocks:** the lectern ledger, portrait plinths, dowsing outlines and bloom flowers should all be visible.
- **Lanterns:** place a market with `/function bm:admin/place_market` and check every lantern stays up, including when you place blocks next to them.

**1.18:**
- **Standing:** check that a purchase adds points (on the actionbar) and that `/trigger bm.standing` opens the status menu as a non-operator.
- **Keys:** at 500 points your key should turn Silver in place. Check that the vault door, the Auction Hall gate and the Gilded Gutter gate (at 1,500) all let you through.
- **Back rooms:** buy one item at a Regular stall, and check that a locked line refuses you.
- **Dark Auction:**
  - Run `/function bm:admin/auction_now` and bid.
  - Bid from a second account to check you're refunded when outbid.
  - Win a lot.
  - Log off while you hold the top bid, then rejoin.
  - `/reload` mid-lot and check everyone's Medallions come back.
  - Watch whether the rivals push prices sensibly.
- **Rat Bank:** deposit, die, check the balance, then withdraw everything.
- **Smuggler's Jar:** bottle a named, tamed animal and a villager with trades, release them, and check they come back exactly as they were.
- **Pocket Rift:** check it places, works as a portal, and folds back up.
- **Ring of Three Burrows:** set a burrow in the Nether and travel there from the Overworld.
- **Rufus Gnaw:**
  - Whether he picks fights and shoots sensibly.
  - Guard mode keeping him at his post.
  - His health after switching modes.
- **Positions:** check the ledger, NPC and statue positions and sizes (judgement calls).

- **Warden emerge animation.** The `is_emerging` memory format is verified, but whether it plays the crawl-out animation can only be seen in game.
- **Hat and rat sprite sizes and positions.** The models are valid, but how big they look is a judgment call.
- **Lucky Golden Goose:** a 1-in-30 roll on warm-variant chickens.
- **Revenant loyalty in multiplayer.** A player wearing the full Crimson set joins a hidden team so their Revenants won't target them. If your server already puts players on teams, such as a nametag-color plugin, Revenants may attack that player. They never attack the wearer otherwise.
- **Blood Moon difficulty** is tuned on paper: 5× health, Strength II, armor-piercing blood damage. Tell me if it's too spicy or too mild after a real night.
- **Mounted mobs steering.** Riders are expected to steer their mounts toward you. If one just stands there, tell me and I'll adjust.
- **Monstrosity balance:** 500 health, armor-piercing bites and periodic roars. It's meant to be a real fight in endgame gear.
- **Heartstones after death:** the bonus hearts are re-applied within a second of respawning and topped up with instant health. Check that your hearts come back after you die.
- **Crimson Compass arrow:** it points relative to where you're facing, and updates once a second.
- **Golden Wings texture:** the wing art is a gold recolor of vanilla's, so check how it looks in flight.
- **Donado's size, poses and helmet fit**, and where his weapon sits in his paw. These are judgement calls that need a look in game.
- **Tractor beam feel:** the lift speed (about 10 blocks a second) and the one-tap sneak to float down.

## Updating to the next Minecraft version

Send the new version's **server jar and client jar**. That's everything the port needs: the server jar provides the reference data and a real server to test in, and the client jar provides the vanilla models and textures. Trades get the same live-server check every time.

## Secrets (spoilers!)

<details><summary>Click to reveal</summary>

**The Blood Moon Monstrosity.** About 1 in 1,000 hostile spawns under open sky during a Blood Moon becomes a giant, red-glowing ravager. A pillager called the **Crimson Herald** rides it, firing blood-cursed bolts. Only one can exist at a time.

- **On first sight:** a title and roar for players within 48 blocks, and a boss bar for anyone within 64.
- **Bite:** 5 armor-ignoring damage, Wither II and **Hunger III**.
- **Every 12 seconds:** a roar that slows and knocks back anyone close. Every other roar raises two Blood Moon zombies (they drop no crystals).
- **At half health** it enrages.
- **At dawn** it retreats if it hasn't been killed.
- **Drops:** the **Ravenous Heart**, 10–16 crystals, a Trophy and 2–4 Medallions. The Herald drops 2–3 crystals.

**Ravenous Heart:** while it's anywhere in your inventory, every kill refills your hunger completely.

The Blood Moon Almanac's last page hints at it.
</details>

## Coming in Phase 2

Bosses (with Bobbery as the semi-final), progression locks, boss intros and ambience, the Final Boss set's full-set aura, the Lucky Dungeon with its Golden Goose jockey boss, and the **9 Lucky Map Fragments**. The fragments ship together with the dungeon they lead to.

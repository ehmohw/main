# Black Market — Phase 2 TEST build v2.15 (Java 26.3)

This is a **test build**: all of Phase 1.22 plus the seven boss dungeons. It **replaces** `BlackMarket_DP.zip`, so don't load both. Use a test world (or a copy of your world) until it has been played through once.

Install it like Phase 1.6. Put `BlackMarket_Phase2_TEST_DP.zip` in `datapacks`, then use `BlackMarket_Phase2_TEST_RP.zip` as the resource pack. `SHA1.txt` has the resource pack hash for `server.properties`. The dungeons only generate in **new chunks**.

## New in 2.15

Includes everything in Phase 1.22: the Blue Marlin, Storm Balls, coffee, the weather vials at the docks, skiff kits, the Restless Dead, mailboxes and couriers, bigger trader rats and the lag work. See the main README. On the TEST build:
- **Each dungeon's per-tick and 5-tick work** (puzzles, secret buttons, gates, the arena intro, effects, the altar) runs only while a player is within its radius (+24 blocks) of its controller. That's checked once a second.
- **Each dungeon's once-a-second work** (ambience, resets, the boss fight) runs half a second after the main loop.
- The layout verifier (`tools/verify_dungeons.py`) still reports **0 errors** on all seven dungeons.
- **Trades:** every trader on the TEST build was spawned on the 26.3 server and read back. That's 768 recipes with 0 problems, and payment checks pass for all 409 items.

## New in 2.14

Includes everything in Phase 1.21 (the Vorn Skiff, the Dawnbringer set, the Vorn Mining Drill, rat portraits, the newcomers' lectern, the Whisker Lantern and the Rat King's Crown upgrade; see the main README). On the TEST build:
- **Rat portraits, banners and shields** are also in every dungeon's hidden chest (1 in 2) and spoils vault (about 1 in 7).
- **The Skiff and the Drill respect the dungeons.** Neither works within 40 blocks of a dungeon, nor in the Hollow Throne. A skiff that strays near one sets its rider down.

**Access audit: nobody gets soft-locked**
- **Getting in.** A new tool, `tools/access.py`, places a dungeon in real terrain on the 26.3 server (using its real terrain adaptation) and scans the blocks. It then proves a player can **walk** from the surrounding land or sea to the entrance: stepping up, falling, climbing ladders and swimming, with no digging and no block placing.
  - **Passed:** the Brood nest, the Gilded Roost, the Frostbound Spire, the Hexbound Cathedral and Wilfrey's Keep, at 3 sites each, with Roost entrances down to y −19. Graveyard crypts passed at 3 sites too, from the surface down to the key altar.
  - **Fixed: the Sunken Throne failed at all 3 ocean sites.** The temple often breaks the surface, and its only door is high on the tower, 14 to 22 blocks above the sea at the test sites. You had to build your way up. It now has a ladder from the sea floor up the temple wall and the tower to a ledge at the door. Temples already in your world get the same ladder the first time they load, and all six test temples (old and new) pass.
- **Inside.** The layout verifier (`tools/verify_dungeons.py`) now runs on all seven dungeons with **0 errors**. It proves:
  - Every puzzle's buttons, levers, targets and plates are reachable (and clickable or shootable) once the gates before it are open.
  - Nothing further on can be reached early.
  - Every pressure-plate path has a safe route.
  - The altar and arena open only after the last gate.
  - Every spoils vault and victor's vault, including the Hollow King's throne vault, can be walked up to.
- **What "solvable" means here:** each puzzle's answer is fixed in the build and the verifier proves the controls are reachable. Nothing was hand-played.
- **The Black Market:**
  - Every trader is reachable on foot from the vault door.
  - Three of them (Vinny, the Fence, Old Barnaby) were just out of reach across their counters; they now stand at them.
  - It's still entered by digging down to its entrance tunnel. There's no adventure mode or Mining Fatigue there, so that can't lock anyone out.

## New in 2.13

Includes everything in Phase 1.20 (the Vorn, the new goods, the tidier market and the Dockmaster; see the main README). On the TEST build:

**Getting through the dungeons**
- **Where Sealed Maps come from:**
  - The Fence sells the first one (the Sealed Nest Map), and now sells **every** Sealed Map.
  - Each boss's first victory gives you the next map.
  - The next map is also in that boss's **Victor's Vault**.
- **Why the Broodmother gave no map:** victory credit only went to players the arena counted at the start of the fight. Now everyone in the arena when the boss falls is a victor.
- **Playing together:** every player in the arena gets their own Victor's Key and their own credit. Each vault rewards each player once, so everyone loots it.
- **Underground entrances always reach the surface.** You can't dig inside a dungeon (adventure mode and Mining Fatigue), so the Broodmother's Nest and the Gilded Roost build a lit ladder shaft from their door up to a marked well-head on the surface. This happens the first time the dungeon loads, and it also covers nests already in your world.
- **Key of New Beginnings** (the Fence, 3 Tokens): resets *your* conquest record to zero, so every dungeon and first-victory reward can be won again. You keep everything you own.
- **Conquered dungeons reset fully.** After a day with nobody inside: puzzles, gates and doors reset, every vault can be opened again by everyone, and every loot chest refills. This applies to dungeons generated with 2.13.

**Victor's Vaults**
- Every Victor's Vault has a floating sign and a beam of light over it.
- The Hollow King's vault sits **on his throne**.
- Victor's Vaults now give:
  - Currency: Tokens, Medallions and Xenite.
  - That boss's prizes: its trophy, the next Sealed Map, sometimes its signature weapon, and a Lucky Map fragment.
  - One rare vanilla treasure: a Heavy Core, emerald blocks, diamonds, a diamond block, an enchanted golden apple or a netherite upgrade template.

**The Hollow Throne**
- **The waves are brutal.** The phantom Wraiths are gone (they flew off and never fought). Hollow Brutes, Hollow Tuskers (hoglins) and a Hollow Ravager take their place. Each trial now has four waves and more mobs at each spawn point. The King's court also brings brutes and tuskers.
- **The Cinder Crossing's lava** no longer pours out of the castle into the void. A rock rim holds it in.
- **It's safe for conquerors.** While everyone in the Hollow has already beaten the King, the trials sleep and the citadel doesn't reset. They wake as soon as someone who hasn't beaten him is there.
- The citadel is rebuilt in place automatically. Its old markers are cleared first, and puzzle progress inside it starts fresh.

**Bosses and puzzles**
- **Every boss summons minions.** Their search for summoning points is wider, so minions still come if the boss wanders.
- **Puzzles get harder further along the road.** The layouts and clues are unchanged. Now:
  - A wrong answer from the Spire on also summons something: a stray, a trident drowned, evoker fangs plus a vindicator, a wither skeleton, then two Hollow Knights.
  - Combat trials send more mobs (the Cathedral, the Keep, the Hollow).
  - The Hollow's target trial gives you 20 seconds; the Spire's gives you 40.
- **The Broodmother's egg puzzle** spawns its cave spider again on a wrong press. The trap looked for a player within 8 blocks of a controller hidden under the floor, which usually found no one.

**Exteriors** (generated with 2.13)
- **The Frostbound Spire:** banded ice-and-slate courses, frozen streaks, eight buttresses with ice pinnacles, an icicle-hung parapet, ice needles on the crown, and banners and lamps at the door.
- **The Sunken Throne:** pilasters with sea-lantern capitals, a ruined colonnade around a conduit on the roof, sea pickles on the terraces, and a coral reef with kelp around the base.
- **The Hexbound Cathedral:** a slate roof over the Apse, skull-capped pinnacles, violet windows in the Apse, a ceiled porch with hanging lanterns, and vines and moss everywhere.
- **Wilfrey's Keep:** Bobbery's black banners and Wilfrey's white ones on the walls, and a lamp on every buttress.

**The Gilded Roost** is now **underground and about three times rarer**. Its door opens onto a stairwell and a shaft up to a gilded well-head. The Roost's vaults hold:
- **The Golden Donado**, always, in the Victor's Vault. Set it down and no monster spawns within 32 blocks of it, a 64 x 64 area. It's no longer sold at the Dark Auction.
- One treasure from the following:
  - The **Gilded Fortune** set: netherite armour in gold, +2 Luck and +4 Max Health per piece; the full set gives Luck III.
  - The **Blinding Light of Destiny**: Looting V, and a random one-minute blessing every 10 kills.
  - **Fortune's Favor**: Fortune V; sneak + right-click switches 3 x 3 mining on or off.
  - The **Gilded Felling Axe** and the **Gilded Spade**.
  - The **Rabbit's Foot of Fortune**: Lucky Nights ten times as likely while it's carried in the Overworld.
  - The **Pocket Slot Machine**.
  - The **Halo of Fortune** and **Midas Treads** cosmetics.
- **The Pocket Slot Machine** is a reusable scratch card: 10 levels a pull, and a 1-in-40 jackpot of the **Lucky Pocket Watch**. One is always in Whiskers' Stash, the Roost's secret room.
- **The Lucky Pocket Watch** freezes any creature in place and frees it again on a second use. It never works on players, bosses, wardens, withers or the Ender Dragon.

**Worlds already in play:** the market fixes and the Dockmaster reach existing markets, and the Hollow rebuilds itself. New layouts (exteriors, the underground Roost, vault signs and resets) appear in dungeons generated after updating. As always, test on a copy first.

## New in 2.12: Minecraft 26.3

2.12 is 2.11 rebuilt for **Java 26.3**, with every Phase 1.19 fix (see the main README). It needs 26.3; keep 2.11 for a 26.2 world.
- **Dungeon maps** now start from a filled map. In 26.3 a blank map would have come out unusable.
- **Boss keys and vault keys from loot** now match the vaults, gates and trades exactly. The same number-type fix as the main pack covers them.
- **All seven dungeon templates** were placed by the real 26.3 server without a single entity-data error, and nothing breaks or drops when they're placed. The Keep's eyeblossoms used to drop because they sat on bare stone; they now grow from pale moss.
- **646 trades** were read back from live traders, and **440 payment and item checks** passed. Everything is unchanged from 2.11.

## New in 2.11

Includes everything in Phase 1.18: Standing, the upgrading keys, back rooms, the Dark Auction, the Gilded Gutter and the new goods. On the TEST build:
- **Each first boss victory** is worth **+50 Standing**.
- **The Dark Auction's lot pool** gains a **Next Boss Key** lot. The winner gets the key for the next boss on *their* conquest record, or a Shard of the Hollow Throne once the record is complete.

`tradediff.py` against 2.10 shows every trader's offers unchanged.

## New in 2.10

- **Wilfrey is a wither skeleton knight now.**
  - He used to be an empty, floating set of armour. He's now a full wither skeleton who walks beside you, wearing your real gear and holding your weapon in his hand; empty slots show bare bones.
  - Equipping, hold/follow and the locket work as before.
  - A Wilfrey you've already called gets his new body within a few seconds.
- **The locket's 30-minute cooldown was really 90 seconds.** It shared a timer with the Levitation Wand. It now has its own.
- Everything in **Phase 1.17**: Lucky Night upgrades, Jackpot monsters, Lucky Prime animals, and the rocket boots, altar and market fixes.

## Fixed in 2.9

- **Wilfrey's tomb and Wilfrey himself respond to clicks.**
  - Every click was thrown away before the pack could see who clicked, which was the real cause of the tomb bug.
  - The same mistake broke right-clicking Wilfrey to hand him gear.
  - The tomb's click box is also a little bigger than the stone now, so a click on the sarcophagus always lands on it.
  - Existing worlds are fixed automatically.
- Everything in **Phase 1.16**: the Xenite trade fix, the working altar, Donado's sword and sitting pose, nameplates, rocket boots, and the tractor beam and dowser changes.

## New in 2.8

- Everything in **Phase 1.15**: Donado (a companion you rescue), the Donadian alien race (Zorp is one now), and the first mothership. The dungeons are unchanged.

## New in 2.7

- Everything in **Phase 1.14**: crashed saucers, Xenite crystals, Zorp, the alien tech and the Xenite Altar. The dungeons are unchanged.

## Changed in 2.6.1

- Pickpocket rats removed (see Phase 1.13.1).

## New in 2.6

- Everything in **Phase 1.13**: the rebuilt Black Market (new markets only, or `/function bm:admin/place_market`), the crowd, the steam vents, the trade/item audit and the new-world load fix. The dungeons are unchanged.

## Fixed in 2.5.1

- **Right-clicking Wilfrey's tomb works.** Its click box sat in front of the tomb, over the dais, so walking up to the tomb put you *inside* it, and Minecraft ignores clicks from inside an interaction box. It now covers the sarcophagus itself and ends at the dais edge. Existing worlds get moved automatically.
- Everything in 1.12.1 (trades re-sync, the Outfitter's stock, the grappling hook).

## New in 2.5

- **Wilfrey's Rest has been restyled** to suit the Hollow: quieter, greyer and sadder.
  - Weathered tuff and deepslate, with podzol and pale moss underfoot and fallen leaves.
  - A dead dark oak and a weeping pale oak hung with pale moss.
  - Eight leaning, broken standing stones with guttering grey candles and cobwebs.
  - A still black pool ringed with mud.
  - Soul lanterns, and a plain tuff tomb under a grey and a white mourning banner. It reads "HERE LIES WILFREY, the Kind Lord. Rest well."
  - The old islet is cleared and replaced automatically the next time it loads.
  - Wilfrey's grave and summoning effects are now ash and soul motes.
- Everything in **Phase 1.12** (Lucky Nights, the Overworld-only Blood Moon, the Sigil's new rules, and the Ember and Void Rats). Blood Moons never reach the Hollow.

## New in 2.4

- **The Warpstone of the Hollow Throne.** Defeating the Hollow King gives you a permanent warpstone; anyone who already has, gets one automatically. Use it anywhere, in any dimension, to step into the Hollow Throne. Use it there to go back to exactly where you left. It's never used up and has a 10-second cooldown.
- **Wilfrey's Rest**, a hidden islet floating beside the Hollow Throne, reachable only by elytra.
  - (Restyled in 2.5. See above.)
  - If you have defeated the Hollow King, right-click the tomb to receive **Wilfrey's Locket**.
- **Wilfrey, the Kind Lord** (ally).
  - **Calling him:** use the locket and he rises as a spectral knight who follows and fights for you, and now and then lends you a little Regeneration. Use it again to call him back to you; sneak + use it to let him rest (your gear is returned).
  - **Equipping:** right-click him holding a weapon or armour and he equips it, handing back what it replaces. You see his real gear on him; empty slots shimmer as pale spectral leather.
  - **Commands:** sneak + right-click empty-handed takes everything back. Right-click empty-handed to make him hold position or follow.
  - **If he falls**, his gear drops and the locket needs **30 minutes** before it can call him again.

## New in 2.2

- **The Hollow Throne is rebuilt** as a black citadel floating in a crimson void:
  - It's built over several levels: courtyard, undercroft, three keep halls, and a throne room under a red roof with spires.
  - Hazards: a broken bridge with gaps over the void, a lava lake you cross by jumping pillars, and a stair of floating steps around an outer spire.
  - Five trials: two battles, two crossings and the Gallery of Seals.
  - The throne room has lava channels, great columns and a grand summoning altar.
  - Five floating islets surround it, each with a dead tree, a chest of rare loot (netherite, god apples, totems, Heartstones) and a wayshrine back to the arrival rock. Only an elytra glide reaches them.
- **The sky** in the Hollow Throne is now a crimson void with drifting ash.
- **Mob griefing** is switched off while anyone is in the Hollow Throne, so the King's Wither form can't wreck the castle. It switches back on (if it was on) once the dimension is empty. While someone is in there, creepers won't break blocks anywhere.
- **The Hollow King's court** is bigger and louder. In phase 1, knights and an archer rise from smoking rifts every 10 seconds. In phase 2, knights, archers and **Hollow Wraiths** (phantoms) come every 8 seconds.
- **Bobbery rides a giant spider** ("Mutton").
- **Fewer repeated puzzles, more fighting.** Three keypads and the Sunken Throne's valve levers are now **wave battles**: the Tyrant's Tide, the Choir Militant, Bobbery's Bonecrew and the Gilded Guard. Walk in and the room fights you; clear three waves and the gate opens. Only the Frostbound Spire keeps its keypad. Dungeons that already generated still work: their old keypad and valve rooms become wave rooms.
- **Summoning altars:** every dungeon's altar now sits on an inlaid dais with four capped pillars, a hanging lantern where there's a ceiling, and themed particles.
- **Existing worlds:** the new Hollow Throne is built at a new spot in its dimension the first time the pack loads. The Shard takes you there, and the old one is left behind.

## New in 2.1

- **Boss trophies.** Every victor's vault now gives that boss's placeable 3D trophy: the Broodmother's spider, the Frost Marksman's hooded skull and longbow, the Drowned Tyrant's crowned trident, the Archmage's hat and orb, Bobbery's masked skull with his axe and stolen gold, the Hollow King's three crowned skulls, and the Golden Goose with its egg.
  - **Use** a trophy while looking at the top of a block within 5 blocks to set it there, facing you.
  - **Right-click** a placed trophy to turn it 45°. **Punch** it to pick it back up.
- **Vaults.** Victor's (boss) vaults are now **ominous** vaults; spoils vaults stay regular. Every vault in a dungeon you've already found is updated to accept the current keys and to the right vault type. This happens the first time you come within 24 blocks of it.
- **No pearl skips.** An ender pearl thrown near an unsolved pressure-plate puzzle (the Broodmother's Nest, Frostbound Spire, Hollow Throne and Gilded Roost) fizzles and you get it back.
- **Frostbound Spire fixes.** The 4th Frost-Eye target was built outside the wall; it's now in the inner wall face. The staircase from the thin-ice floor to the roof had a step under the roof's floor, so you hit your head and couldn't climb; it now starts one block further north. Spires that already exist are repaired automatically when you get close.
- The puzzle checker now also requires every target, button and lever to have an open face toward the inside, and every step up to have head clearance.

## The road to the Hollow King

| # | Dungeon | Where | Boss | Key (sold by the Fence) |
|---|---|---|---|---|
| 1 | The Broodmother's Nest | underground, below forests/taigas/jungles/dark forests/pale gardens/lush and dripstone caves | The Broodmother | Silkbound Key — 24 tokens |
| 2 | The Frostbound Spire | snowy plains, ice spikes, groves, snowy slopes and peaks | The Frost Marksman | Rimeglass Key — 42 tokens |
| 3 | The Sunken Throne | deep oceans | The Drowned Tyrant | Coral Throne Key — 6 medallions |
| 4 | The Hexbound Cathedral | swamps and mangroves | The Archmage | Hexed Key — 9 medallions |
| 5 | Wilfrey's Keep | pale gardens and dark forests | **Bobbery** | Wilfrey's Signet — 2 trophies |
| 6 | The Hollow Throne | its own dimension | **The Hollow King** | — (needs all five emblems) |
| — | The Gilded Roost | plains, meadows, cherry groves, flower forests | The Golden Goose | — (find all 9 Lucky Map Fragments) |

- **Maps:** the Fence sells the first Sealed Map for 5 tokens. Each first victory gives you the sealed map to the next dungeon. Beating Bobbery gives you the **Shard of the Hollow Throne**, which takes you to the final dimension. The Shard only works in the Overworld. Anyone within 3 blocks of you who also has all five emblems comes along.
- **No skipping:**
  - Every dungeon has 3 puzzles (the Hollow Throne has 5). They unlock strictly in order: a puzzle ignores you until the one before it is solved, and it re-arms itself the moment it becomes current, so nothing can be solved early. Each solved puzzle opens the next gate.
  - The boss altar stays cold until every puzzle is solved **and** your conquest record shows the previous boss.
  - Inside a dungeon you're in Adventure mode, and near one you get Mining Fatigue III, so you can't dig around the gates.
- **Summoning:** stand at the altar inside the boss room, hold the key, and **sneak**. The battle doors seal behind everyone inside.
  - Only players **inside the boss room** count as fighters. Someone waiting in the antechamber isn't targeted, doesn't get credit, and doesn't keep the fight alive.
  - If everyone leaves or dies for 30 seconds, the boss sinks away and the key drops back onto the altar.
  - Every player in the room when the boss falls gets credit. First kills earn the Conquest Emblem, the next map and a lore book.
- **Dungeon payouts (1.7 economy):** trial spawners drop a token half the time, plus the vault key. Spoils vaults pay 2–4 tokens, victor's vaults 4–6 tokens and 1–2 medallions, and bosses 4–10 tokens depending on tier.
- **Replay:**
  - Trial spawners drop the dungeon's **Vault Key** for the spoils vault before the boss room. Each boss victory gives a **Victor's Key** for the vault inside.
  - Vaults reward each player once, like trial chambers.
  - A dungeon re-locks itself 20 minutes after the last player leaves. Gates you opened stay open after a victory, but the puzzles re-arm for the next summoning.
- **Ambience:** each dungeon has its own floating particles and low ambient sounds. Wilfrey's Keep has a sparse wither haze, ash and drifting souls.

## How the puzzles are built

There are **no redstone circuits or piston doors**. Every input is a real button, lever, target block, pressure plate or copper bulb that you use normally, and the data pack reads them. This works in any rotation the structure generates in.

Gates are blocks that commands remove from the top down, with sound and particles. Keypads are 3×4 grids of stone buttons (1–9, **Clr**, 0, **Ent**). Nothing relies on signs being clickable, which behaves differently for non-operators on servers. Every keypad and sequence button is stone, so skeleton arrows can't press them by accident.

## How this was verified against 26.3

Everything in the main README's 26.3 section applies, run on the TEST build: the real server loads it with 0 errors; 646 recipes are read back identical; 440 payment and item checks pass; 731 entity-data writes decode cleanly; all 13 templates place; and every command template parses. About 13,000 command lines pass the 26.3 grammar check, and the key audit finds no problems.

The checks below are from the 26.2 build and still hold. The dungeon geometry didn't change.

- **6,518 command lines** checked against the 26.2 command grammar and registries: 0 errors. **253 NBT blobs** checked field by field: 0 errors. Every structure block state, block entity, trial spawner and vault config, loot table, worldgen file, the custom dimension and the resource pack: 0 errors.
  - The checker caught one real bug that's now fixed: sign text colors like `aqua` and `gold` are not valid **dye** colors on signs in 26.2.
- **A walkability prover** (`p2/verify.py`) walks each dungeon block by block: walking, stepping up stairs, falling, climbing ladders and swimming. It walks from the entrance and, for surface dungeons, from all the ground around the building. For every number of open gates, it proves:
  - the next puzzle **can** be reached, and the one after it, the altar and the boss room **cannot**;
  - each hidden room is sealed until its secret door opens, and its hidden button can be reached;
  - every pressure-plate path has a safe route, and no route avoids the plates.

  To prove it isn't rubber-stamping, it was tested by punching holes in walls: it flagged every breach that a player could actually walk through.
- **The Hollow King's arena** is reinforced deepslate on all six sides, including the battle doors while closed. The Wither cannot break it (`#minecraft:wither_immune`, 26.2). Its vaults sit outside the arena so the Wither can't break them either.

## What still needs an in-game test (Phase 2)

- **Boss balance and AI:**
  - the Frost Marksman blinking between perches;
  - the Tyrant's riptide;
  - Bobbery's fire pillars (the floor glows red about 1–2 s before they erupt);
  - the Hollow King's second form;
  - the Golden Goose jockey steering.
- **The Hollow Throne** is placed into its void dimension by command the first time the pack loads (it takes a few seconds). Check that `/function bm:admin/p2/hollow` takes you there.
- **Trial spawner and vault configs** are format-checked. Spawn rates and rewards are a first pass.
- **Worldgen spacing:**
  - The Roost is rare by design: roughly one per 80×80-chunk region.
  - The Keep only spawns in pale gardens and dark forests.
  - Use `/locate structure bm:p2_<name>` to find one.
- **The copper-bulb puzzles** (Cathedral 3×3, Throne 4×4) can always be solved. The scramble is built from real button presses.

## Admin

```
/function bm:admin/p2/place_<brood|frost|tide|hex|keep|lucky>   place one at your feet (natural mob spawns not suppressed)
/function bm:admin/p2/conquest_<0-6>                            set your conquest record
/function bm:admin/p2/reset                                     re-lock the nearest dungeon
/function bm:admin/p2/hollow                                    go to the Hollow Throne
/function bm:admin/p2/shard                                     get a Shard of the Hollow Throne (and the 5 conquests it needs)
/locate structure bm:p2_<name>
```

## Solutions (spoilers!)

<details><summary>Click to reveal every puzzle and secret</summary>

**Broodmother's Nest**
1. Levers on the Silk Loom: raise a lever under each white wool column and leave the grey ones down.
2. Press the egg sacs from smallest to largest.
3. Web Walk: step only where cobwebs hang from the ceiling.

Secrets:
- Weaver's Cache: a button under a bone ledge.
- Rat Gang hideout: a button in a nook near the entrance.

**Frostbound Spire**
1. Hit all four targets within 30 seconds (snowballs in the barrel).
2. Keypad **7041**: the four winter tallies.
3. Thin ice: follow the sea lanterns in the roof.

Secret: the Huntsman's Cache, behind a button under the table.

**Sunken Throne**
1. The Tyrant's Tide: survive three waves of drowned in the valve room.
2. Press the listen button, then repeat the melody on the plinths.
3. Drop the three Pearl Sigils on the tribute altar.

Secret: Smuggler's Grotto, through a floor button on the first level.

**Hexbound Cathedral**
1. Light all nine candles (lights-out).
2. The Choir Militant: survive three waves in the library (vindicators, pillagers, witches, then an evoker).
3. Press the runes in the rose window's clockwise order: purple, red, lime, orange, blue, yellow.

Secret: the Forbidden Archive, via an oak button among the bookshelves.

**Wilfrey's Keep**
1. Raise the levers under the **white** banners (Wilfrey's colors). Leave the black ones down.
2. Bobbery's Bonecrew: clear three waves of wither skeletons, skeletons and blazes from the Great Hall.
3. Press the tombs in the order the knights fell: Bertram, Isolde, Edmund, Rowena, Aldric, Cedric.

Secrets:
- Bobbery's Stash: a button on the gravestone by the gatehouse.
- Wilfrey's Tomb: a blackstone button on the crypt ceiling above the aisle. It holds **Wilfrey's Oathblade and Aegis**.

**The Hollow Throne**
1. The Siege of the Gate: survive three waves in the courtyard. The Ossuary door (west side) then opens.
2. The Cinder Crossing: jump the basalt pillars across the lava lake to the far ledge. The archers on the rest island will try to knock you in.
3. Gallery of Seals: shoot the five seals in conquest order: white wool, packed ice, prismarine, amethyst, gilded blackstone. Snowballs are in the barrels by the stair.
4. The Shattered Stair: climb the floating steps around the Spire of Ash to the balcony. The void is below.
5. The Knights' Vigil: survive three waves (knights, archers, wraiths, a captain).

Secret: the Crown Room, via a button low on the Gallery's west wall, just inside from the north-west column. It holds the **Crown of the Hollow King**. The victor's vault holds the full **Conqueror's set**.

**The Gilded Roost**
1. Pull until three reels match.
2. Step only beneath the glowstone "lucky stars."
3. The Gilded Guard: survive three waves in the Counting House.

Secret: Whiskers' Stash, via a button tucked into the hay. It holds the **Lucky Horseshoe**.
</details>

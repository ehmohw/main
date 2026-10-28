# The Undercrown: the final dungeon (draft for approval)

**The boss:** the Dread Sovereign, the thing that empowered the Dread.

**Map:** `undercrown_map.png` (plan and section). **Boss art:** the `dread_sovereign_*.png` sheets.

## Where it is, and how you find it
- **Location.** One per world, cut into the Nether's rock at a fixed far spot. It is 224 x 224 blocks and spans y 6-118, between the bedrock floor and roof. The Hollow Throne is 152 x 152, so this is about twice its volume.
- **Disguise.** The template uses structure voids. Only its own rooms and thick walls replace the rock, so the natural Nether stays around it. From outside it is a basalt cliff with a cracked seam of crying obsidian, and nothing more.
- **Biome.** Inside, it has a biome of its own, *the Undercrown*:
  - no natural spawns;
  - red-black fog and falling ash;
  - its own ambience.
- **Griefing.** Mob griefing is off while anyone is inside, as in the Hollow.
- **Locked until you've beaten all three Dread bosses.** Beat the third (the Snowbeast, the Witch and the Sawshark, all three tracked by `bm.dbwin_*`) and a voice speaks: *"You broke my three. Come, then."* You receive **the Sovereign's Summons**, a compass that only works in the Nether and points to the gate. **Hard mode only.**
- **The Hidden Gate.** Bring the three Dread Tokens. Set them into the three hollows of the seam, and the cliff opens.

## The way in (the red path)
1. **The Hidden Gate**, then a long tunnel down into:
2. **The Hall of Chains**, the hub.
   - A shaft 56 across and 80 deep. Colossal chains hang into a lava pool, and a spiral stair and chain-bridges wind down it.
   - The **Throne Gate** waits at the bottom. It has three empty sockets, one for each Crown Shard.
   - Three wards branch off the shaft, and you can take them **in any order**.
3. **Each ward** is sealed by the trio its Dread boss demanded. Anyone who reaches this place has beaten that boss, so they own all three. **Sigil mechanic:** each sigil is cut with a follower's emblem. Lead that follower to it and have it **sit** there; the sigil lights while it stays. Doors that need two followers need both seated at once, on sigils far apart. In co-op, anyone's followers count.
   - **The Frozen Ward:** Pistachio, Celi and Tullius. The Snowbeast's corruption: frozen lavafalls and black ice.
     1. Pistachio's sigil opens the hat-lock door.
     2. ◆ *The Frozen Falls*: strike the targets in the order a frozen lectern's verse gives.
     3. Celi and Tullius, both seated, freeze an ice bridge across a lava lake.
     4. ⚔ Frostbound Thrall waves.
     5. ☠ **Echo of the Snowbeast**, a smaller shade of the real boss, which drops the **Frost Shard**.
   - **The Hexed Ward:** Cecil, Apophiss and King Omega. The Witch's library, inverted.
     1. Cecil's sigil opens the library.
     2. ◆ Hex-sigils (lights-out).
     3. Apophiss opens the serpent crawl.
     4. King Omega makes the ossuary's dead step aside.
     5. ☠ **Echo of the Witch**, which drops the **Hex Shard**.
   - **The Drowned Ward:** Emma, Bones and Queen Pearl. An Underwater Kingdom warship, dragged dry into the Nether and hung in chains over a cavern of lava.
     1. Pearl wakes the wreck.
     2. ◆ *The Kingdom's Song*: ring the bells (a Simon puzzle).
     3. Emma and Bones open the keel.
     4. ⚔ Dried Drowned waves.
     5. ☠ **Echo of the Sawshark**, which drops the **Tide Shard**.
4. **The Throne Gate.** Set in the three shards, and the gate opens.
5. **⚔ The Stair of a Thousand Eyes.** A descending gallery whose walls are lids.
   - When the eyes open, anyone in their sight is marked: Darkness, and Dread Knights pour out.
   - Move while they're shut, and fight when you're caught.
6. **The Antechamber.**
   - The spoils vault.
   - A rift home.
   - The battle door.
7. **THE THRONE OF THE DREAD.**
   - A round hall 72 across and 52 tall, with a floor of cracked void-glass over the lava sea.
   - Six chained pillars, and the throne on a dais.
   - The Sovereign kneels on the throne, dormant, until someone crosses the hall.

## The fight: three phases
The boss is a scaled host about 12 blocks tall, so its hitbox is its body, plus its rig. It is built on the Dread bosses' framework (`phase197`), including the Dread theme, the turn and the Lament.

Health:
- About 1000 per phase.
- Each phase is its own pool, so no burst can skip one.
- Health scales by +50% for each fighter beyond the first.

The boss bar is renamed in each phase.

**Phase 1, ARMORED (it is still bound).**
- **Attacks:**
  - Overhead slam: a shockwave ring, so jump it.
  - Wide sweep: duck behind a pillar.
  - Lunging stab.
  - Hurled chains that drag you in.
  - It calls Dread Knights.
- **The puzzle in the fight:** six **Wellsprings** (red braziers on the pillars) mend it while they burn. Shatter them, by hitting or shooting each one's crystal, to stop the healing. They re-light over time.

**Turn 1.** It drops to one knee. Its plate cracks off, it roars (a knockback wave), and **six wings unfurl, every eye in them opening.**

**Phase 2, BROKEN (it remembers its three).**
- **Movement:** it hovers.
- **Attacks:**
  - A wing gust pushes you toward the edge.
  - The wing-eyes fire homing bolts.
  - A heart-pulse (Wither) ripples out in rings.
- **It uses its Dread's moves:** the Snowbeast's ice volley, the Witch's curse circles (step out!), and the Sawshark's whirlpool pull.
- **Grounding it:** shoot out the six wing-eyes and it **crashes down**. Its heart is exposed, and it takes double damage for a few seconds.

**Turn 2.** The helm shatters. A vast red eye looks out of the void inside. The **outer ring of the floor cracks and falls into the lava sea**, with a five-second warning glow first, leaving islands and the inner ring.

**Phase 3, TRUE (the Unmaking).**
- **Attacks:**
  - The great eye charges, then sweeps a **beam**. Break line of sight behind obsidian.
  - Void tendrils root you in place.
  - Darkness pulses.
  - The islands keep falling, one by one.
- **The frenzy:** at the end it frenzies, as the Dread bosses do (it can't be hurt; sigils burst under everyone). Then it tires, and the eye **closes and has to be struck**.

**Its fall.** The rig unravels into smoke and a last scream. Everyone in the arena:
- is tagged **`bm.dfin`**: the reckoning, so the Lightbringer no longer appears;
- gets the victor vault and the spoils;
- receives a world-wide chat line, like the Hollow King's.

## The reset (after it falls)
After the kill the Throne crumbles over **three minutes**:
- the victor vault stays open;
- the Hoard opens, for those who earned it;
- the Sovereign's voice counts down.

Then everyone still inside is carried out to the Hidden Gate, and the whole Undercrown is **rebuilt**:
- every block is re-placed, including the floor that fell;
- every chest is restocked;
- every puzzle and sigil is re-armed;
- the shards are re-hidden in their Echoes;
- the Throne Gate is re-sealed.

No one can enter while it re-forms. Separately, the usual idle reset still applies: it re-locks 20 minutes after the last player leaves.

## Hidden rooms (purple, optional)
These are sealed by **followers that aren't guaranteed**, so they reward a wide collection. Each holds a unique item and one of the **6 Black Seals**.

| Room | Who opens it | What's inside |
|---|---|---|
| The Last Light | the Lightbringer (she knows this place) | a sealed chapel; the **Dawnshard** |
| Lantern Crawl | the Arachno-Lantern | a pitch-dark maze (Darkness everywhere, except her light) |
| Erased Archive | the Eraser rubs out a painted-over wall | the Sovereign's history; the **Page of Unwriting** |
| Chainmaker's Forge | Bender chomps the chain-gate | where its chains were forged; **Sovereign's Chain** (a whip) |
| Nine Lives | Henry and Nia, through the cat-flap | a little vault |
| Ossuary of the Unbound | Wilfrey (the knights answer him) | the Unbound Knights' gear |

There are also **two classic secrets** that need no follower (a button behind a hanging chain, and a look-up button), and **elytra ledges** in the Hall of Chains shaft.

**The Sovereign's Hoard** is behind the throne. It opens only after the boss falls, and only for someone carrying all 6 Black Seals.

## Unique items and loot
- **From the Sovereign:**
  - **Sovereign's Edge**: its greatsword. Fully charged blows cut a void arc.
  - **The Black Crown**: a helmet.
  - **Heart of the Dread**: a once-a-day revive.
  - Music discs for its theme.
  - A trophy.
  - **The Sovereign's Eye**, which summons the follower. Hard mode; guaranteed on your first win.
- **From the dungeon:**
  - **Dawnshard**: holy. Held, it shields you from the eye-beam.
  - **Page of Unwriting**.
  - **Sovereign's Chain**.
  - The Unbound Knights' set pieces.
  - The 6 Black Seals.
- **Vaults:** spoils, victor and the Hoard.
- **Once each:** items you get once per player (the follower, the Dawnshard) are tracked per player, so a rebuild can't hand them out twice.

## The follower (afterwards)
**The Bound Sovereign** is the same being at follower size, chained to you. It gets the full owner's checklist:
- UI test, frame gimmick, figurine, Cecil doll;
- sitting;
- cosmetics, a rare aura, the Partner Wheel, a shiny;
- duos with Bender, Mr. Capshun, Henry and Nia.

## Build size
This is the largest update yet. Roughly:
- the boss rig and its three forms;
- about 30 rooms;
- a new wards/sigil layer on the dungeon logic (the existing strict puzzle order is per-ward here, and the wards can be done in any order);
- the fight;
- the rebuild;
- items and the follower;
- bot tests that walk it as a player.

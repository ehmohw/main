# Bond Abilities - the Keeper of Bonds' capstone (design draft, v3.00)

The Keeper of Bonds (phase254) is the 51st follower and the last. Its capstone gives each of the other 50 followers (every key
in `phase125.WHO` except `keeper`) one new **Bond Ability**. A follower unlocks its ability for good the first time it's out
at the same time as the Keeper. From then on the ability works whenever that follower is out, whether the Keeper is there
or not, and it can be switched on or off in that follower's menu.

This is a design only: no code, no build.

---

## How unlocking and toggling work

**State.** Each player gets one score per follower: `bm.bd_<key>` (0 = locked, 1 = on, 2 = off). Fifty objectives are easier
to test in commands, loot predicates (`entity_scores`) and advancements than a packed bitfield. A one-second pass also keeps
a derived score, `bm.bA_<key>`, set to 1 only while the ability is unlocked, switched on, and that player's follower is out
(its host is tagged and owned by them). Every mechanism below checks only `bm.bA_<key>=1`, so a loot table or advancement
never has to know where the follower is.

**Unlock.** On the same one-second pass: for each player whose Keeper (`bm.tkpet`) is out, every other follower of theirs that
is out and still locked (`bm.bd_<key>=0`) is set to 1, which unlocks it already switched on. The Keeper turns to the follower,
a pink thread (`#ffd6f0`) is drawn between them for about 2 s, a chime plays, and the chat says:

> *The Keeper ties a thread between you and Dennis.* **Bond unlocked: Rich Seam** - *a 10% chance that blocks you mine drop
> one more.* (17/50)

The three-follower limit means each outing is the Keeper plus two others, so all fifty takes at least 25 outings. That's
intended: it's the long tail of the final follower. The Sky Buddies count as one follower and get one bond. The Skiff Escort
isn't a follower and gets none. Carrying the Partner Wheel doesn't count: the follower has to be out.

**Menu row.** Every follower's menu (from its summoning item) gets one more row:
- unlocked: **`Bond: Rich Seam - on`** (gold) or **`Bond: Rich Seam - off`** (grey). Clicking it toggles, says so in the
  action bar, and refreshes the menu;
- locked: **`Bond: ??? - walk with the Keeper`** (dark grey, no click event), so the row itself is the hint.

**Button codes.** This needs one new code, a shared **BOND TOGGLE**: a free code from the Keeper's block, for example **5260**
(5260-5269 is free according to `BUTTON_CODES.md`). It's routed exactly, and the router decides which follower to toggle from
`bm.menu`, because every follower's menu already sets its own `bm.menu`. A follower menu that is mid-rebuild sends nothing.
**5253** (one of the Keeper menu's free slots) opens a new **Bonds** page in the Keeper's own menu: all 50 rows, unlocked ones
named with their on/off state, locked ones as `???`. The page is a ledger only: toggling stays in each follower's own menu.
Both codes go in the legend with their `bm.menu` requirement.

**Gallery and wheel indicators.**
- **Follower Gallery:** a pink **∞** (Keeper colour) beside each follower whose bond is unlocked, next to the existing gold ✦
  for a found shiny. The gallery header adds **Bonds woven: 17/50**.
- **Partner Wheel (phase179):** an unlocked follower's slot label gets a small `∞` suffix, dimmed while the bond is switched
  off. Nothing is saved by slot number, so `SLOTS` doesn't change. The suffix comes from the player's scores at render time.
- **All 50 woven:** a hidden challenge (*"Every Thread"*), and the Keeper's GIFT (phase254) has a small chance to be one more
  thread mote on its rings, as a cosmetic.

**Rules that apply to every bond.**
- **Defaults:** on when unlocked.
- **Heists:** off inside the vault and heist dimensions, like other carried perks (the coat check keeps them out). Bonds that
  are attribute modifiers are removed when the player goes in.
- **Attribute modifiers:** each one has its own id `bm:bond/<key>`. It's added while `bm.bA_<key>=1` and removed when that
  score drops, and removed when the player dies, when the follower goes home, and when the bond is switched off.
- **Cooldowns:** one per bond, stored in `bm.bdc_<key>`, counting down in seconds.
- **Messages:** the Ledger's chatter switch also hushes bond messages. The unlock line is always shown.

---

## The fifty bonds

**Kind:** **P** = passive player buff · **U** = utility · **W** = world effect · **C** = combat.
**Cost:** `cheap` = an attribute, a single advancement, or a per-second check on the player; `med` = a marker, a raycast, a
storage snapshot or a scan near the player; `hard` = flagged, with a simpler fallback given.

| # | Follower | Bond ability | What it does | Kind | Mechanism (Java 26.3) | Cost |
|---|---|---|---|---|---|---|
| 1 | Emma | **Green Thumb** | Every 2 s, one random crop, sapling-free stem or sweet berry bush within 6 blocks of you grows one stage. Roughly doubles growth on a small plot without bone meal. | W | 1/2 s: a marker scatters to a random spot in a 13x13x5 box (random score + macro); generated `if block <crop>[age=N] run setblock ...[age=N+1]` ladders for `#minecraft:crops`, stems, berries, nether wart | med |
| 2 | Celi | **Hard Freeze** | Still water you walk over freezes into frosted ice under you (radius 2), which melts as usual. You can cross rivers and lakes on foot. | W | 4/s: `execute at @s if block ~ ~-1 ~ water[level=0] run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 frosted_ice replace water[level=0]`; skipped while sneaking so you can still swim down | cheap |
| 3 | Zib | **Beam Me Home** | A menu button: a 3-second beam-up, then you're teleported to your bed or respawn anchor (world spawn if you have none). 10-minute cooldown, cancelled if you're hurt while it charges. The Wayfarer's Lodestar returns you to a spot you mark; this returns you to your bed. | U | read the player's `respawn` compound (pos, dimension) into storage; macro `execute in <dim> run tp`; channel tag + `hurt_time` check; blocked in heists, the Hollow and the Den | cheap |
| 4 | Cecil | **Arcane Rebate** | When you enchant at an enchanting table, there's a 1-in-3 chance one of the levels you spent is handed back. | P | `enchanted_item` advancement → 33% `xp add @s 1 levels`; revoke | cheap |
| 5 | KillerWatt | **Tendril Climb** | Sneak facing a wall and you climb it slowly, as if it were a ladder; let go of sneak and you hang for a moment, then drop. | U | 10/s: sneaking (predicate) + the block at `^ ^ ^0.7` is solid → Levitation II while it holds, then cleared; safe_fall for 1 s afterwards | cheap |
| 6 | Leo | **Squire's Care** | A shield you block with recovers the durability the block cost 75% of the time, and you have +20% knockback resistance while you're blocking. | C | `minecraft.custom:damage_blocked_by_shield` stat delta → `item modify` the shield hand with `set_damage` (add, relative); `using_item` shield → knockback_resistance modifier | cheap |
| 7 | Democratus | **Reaper's Tithe** | Each hostile mob you kill gives 2 extra XP points (5 for a boss or a Dread mob), which adds up over a night. | P | `player_killed_entity` advancement (`#bm:hostile`, with a boss/Dread branch) → `xp add @s 2 points`; revoke | cheap |
| 8 | Apophiss | **Slither** | You move almost at walking speed while sneaking (sneaking speed 0.3 → 0.75), so bridging and edging along a cliff are quick. | P | attribute `minecraft:sneaking_speed` `add_value 0.45` | cheap |
| 9 | Tullius | **Captain's Haul** | Each fish you reel in has a 15% chance to bring up a second catch from the vanilla fishing table, ordinary fish and junk only (no treasure). | P | `fishing_rod_hooked` advancement → 15% `loot give @s fish minecraft:gameplay/fishing ~ ~ ~ mainhand` (no hook entity, so no open-water treasure) | cheap |
| 10 | the Frog | **Webbed Feet** | You walk and swim in water a third faster (as with Depth Strider I), and still have your boots slot free. | P | attribute `minecraft:water_movement_efficiency` `add_value 0.33` | cheap |
| 11 | Donado | **Kindred Spirits** | Taming always works on the first try: wolves (bone), cats and ocelots (fish), parrots (seeds), and horses, donkeys, mules and llamas (first ride). | U | `player_interacted_with_entity` advancement with the right item and an untamed target → copy the player's UUID into the target's `Owner` (horse family: `Tame:1b` + `Temper:100`); revoke | cheap |
| 12 | Pearlman | **House Call** | A menu button: he rings up a wandering trader, who arrives within 10 blocks of you with two trader llamas and stays 20 minutes. Once per in-game day. Pearlman visits on the trader's rules himself, but this brings a real wandering trader with its own stock. | U | `summon wandering_trader` (+ 2 `trader_llama` leashed) at a safe spot near the player, `DespawnDelay:24000`; cooldown 1200 s; Overworld surface only | cheap |
| 13 | Wilfrey | **Second Chance** | Zombie villagers you cure (Weakness + golden apple) turn back in 5 seconds instead of 3-5 minutes. They still give the curing discount. | W | 1/s: zombie villagers within 16 with `ConversionTime>100` and `ConversionPlayer` = you → set `ConversionTime` to 100 | cheap |
| 14 | Fishy | **Curator's Find** | The first time you open a structure's loot chest, there's a 25% chance Fishy finds a curio in it: an extra item from a small table for that structure (a name tag, an enchanted book, a golden apple, a disc, a diamond...). | P | `player_generates_container_loot` advancements (one per vanilla chest table, generated) → 25% `loot give @s loot bm:bond/curio/<group>`; revoke | cheap (many small files) |
| 15 | Dennis | **Rich Seam** | Blocks you mine (stone, deepslate, netherrack, end stone, tuff, sand, gravel, dirt, clay, logs) have a 10% chance to drop one more. He already gives Fortune V on ores, so ores are left out. | P | extra pool in those blocks' loot tables: `random_chance 0.1` + `entity_properties this` `bm.bA_dennis=1` + `match_tool` without Silk Touch; merged with phase162's overrides | med (many loot tables, generated) |
| 16 | Pistachio | **Valet** | When a hotbar stack runs out (blocks, torches, food, arrows...), he refills that slot from the same item elsewhere in your inventory. | U | 4/s: snapshot the selected slot's id and count into storage; slot empty and the snapshot's id `if items entity @s container.*` → macro `item replace ... from entity @s container.N` + clear the source | med (fallback: refill only the selected slot, only on the stat tick) |
| 17 | King Omega | **Rest in Peace** | Ordinary phantoms coming for you are dismissed: they fade away in soul fire before they reach you. Sleep only when you want to. The pack's own phantoms (Vorn bio phantoms, vault and curse phantoms) are left alone. | W | 1/s: `execute as @e[type=phantom,tag=!bm.*,distance=..48] on target if entity <owner>` → particles + `tp ~ -300 ~`/kill (setting a stat score doesn't reset insomnia, so they're culled instead) | cheap |
| 18 | Ashur | **Stoke the Fire** | Furnaces, smokers and blast furnaces you've opened in the last 10 minutes cook twice as fast while you're within 16 blocks. Fuel burns at the normal rate, so each piece of fuel goes twice as far. | W | `interact_with_furnace` / `_smoker` / `_blast_furnace` stats → raycast to the looked-at block, tag it with a marker (timeout 600 s); each tick +1 to its `cooking_time_spent` when it's cooking (check the 26.3 field names against the reference data) | med |
| 19 | the Chef | **Second Helping** | Crafting bread, cookies, cake, pumpkin pie, stews, soups or beetroot soup has a 20% chance to make one more. Golden food is left out. | P | `recipe_crafted` advancements (one per recipe id) → 20% `give` of the result; revoke (check how shift-click crafts fire it) | cheap |
| 20 | the Neighbor | **Neighborhood Watch** | In a village (3+ villagers within 32 blocks), once every 20 minutes he "knocks next door": an iron golem is built for the village if it has fewer than two. | W | 1/s village check (as his own find); cooldown 1200 s; count `iron_golem` within 32 < 2 → summon one with `PlayerCreated:0b` at a villager | cheap |
| 21 | Queen Ava | **Kingdom's Grace** | You mine underwater at full speed (as with Aqua Affinity), with no helmet enchantment needed. | P | attribute `minecraft:submerged_mining_speed` `add_value 0.8` | cheap |
| 22 | Queen Pearl | **Sweet Tooth** | Sweets are twice as filling: cake slices, cookies, pumpkin pie, honey bottles, sweet and glow berries give double hunger and saturation. | P | `consume_item` advancement (those items) + `minecraft.custom:eat_cake_slice` → a one-tick Saturation pulse sized to the food (players' `foodLevel` can't be written; check the pulse size on 26.3) | cheap |
| 23 | Bloo | **Regrowth** | Saplings you plant grow into a tree after 60-120 seconds (if there's room), so a felled forest can be replanted and back in one sitting. | W | `placed_block` (`#minecraft:saplings`, propagule) → raycast, marker with a random timer → remove the sapling, `place feature <tree>` for its kind; skip it and retry later if blocked | med |
| 24 | The Stalker | **Nightstride** | At night or anywhere dark (light 7 or less), you move 12% faster and fall 2 blocks further before taking damage. | P | 1/s: `location` light predicate → `movement_speed add_multiplied_base 0.12` + `safe_fall_distance +2`, removed when it's light | cheap |
| 25 | The Arachno-Lantern | **Cooked Through** | Raw meat and fish in your inventory slowly cook in its embers: one item every 10 seconds. Forgeheart smelts ore; this cooks food. | U | 1/10 s: first match of a raw-food list in inventory → `clear @s <raw> 1` + `give @s <cooked> 1`, smoke particles | cheap |
| 26 | Bender | **Fetch!** | Arrows and tridents you shoot that land and stay put are brought back to you after 2 seconds. No more digging arrows out of walls or diving for a trident. | U | 2/s: `@e[type=arrow,nbt={inGround:1b}]` / `trident` with `pickup:1` and `on origin` = you, older than 40 ticks → `tp` to you (they're picked up as usual) | cheap |
| 27 | Bones | **Shell Collector** | Drowned you kill have an 8% chance to drop a nautilus shell (vanilla: only if they carry one), and squid and glow squid drop one more ink sac. Conduits become a sea hunt, not a fishing grind. | P | `player_killed_entity` advancements (drowned / squid / glow_squid) → `loot spawn` at the kill (via `execute at` the newest corpse) or `give`; revoke | cheap |
| 28 | Mr. Capshun | **Autosave** | When you die you keep 75% of your experience levels. *"I've saved your progress. Mostly."* The Grave Charm keeps your items; this keeps your levels. | P | 1/s: `execute store result score @s bm.bdxp run xp query @s levels`; `deathCount` delta → kill XP orbs at `LastDeathLocation`, on respawn set levels to `bm.bdxp*3/4` | cheap |
| 29 | Kettle | **Hopscotch** | You step up full blocks without jumping (step height 0.6 → 1.1): stairs, slopes and hillsides at a run. | P | attribute `minecraft:step_height` `add_value 0.5`; removed in heist and puzzle rooms where it would skip parkour | cheap |
| 30 | Rufus Gnaw | **Thrifty Quiver** | Each arrow you fire from a bow or crossbow has a 20% chance to come straight back to your quiver, tipped and spectral arrows included. A mercenary never wastes a bolt. | P | `minecraft.used:bow` / `crossbow` stat → your newest `arrow` / `spectral_arrow` (`on origin`, age 0, `pickup:1`) → 20%: summon its `item` as an item entity at you, set its arrow to `pickup:2` | cheap |
| 31 | Henry | **Morning Gift** | After you sleep through a night, Henry has left you a present, as a tame cat does: a roll from the vanilla cat morning-gift table (string, feathers, rabbit's foot, rotten flesh, rarely a phantom membrane). | P | `slept_in_bed` advancement → tag; the next morning (`daytime` < 1000, awake) → `loot give @s loot minecraft:gameplay/cat_morning_gift` | cheap |
| 32 | Nia | **A New Litter** | Animals you breed have a 25% chance of twins. | W | `bred_animals` advancement → in the reward, find the newest baby within 8 (`Age:-24000`, no `bm.bdtw` tag) and summon a second of the same type (variant copied by macro); tag both; revoke | cheap |
| 33 | The Gem of Creativity | **Endless Supply** | Each block you place has a 10% chance not to be used up, so long builds go further. | P | `placed_block` advancement → 10%: `item modify entity @s weapon.mainhand` `set_count add 1` if that hand still holds a block item (else the offhand); revoke | cheap |
| 34 | Batty | **Echo Sense** | In the dark, Batty clicks a warning when you walk toward a drop of 5+ blocks or toward lava within 3 blocks ahead, and the edge sparkles. No more stepping into a ravine. | U | 4/s while moving with light < 8: raycast `^ ^ ^1..3`, a column check for 5 air blocks below / `lava` → sound + particles at the edge; a 3 s cooldown per warning | cheap |
| 35 | Eggbert | **Free Range** | Chickens within 16 blocks of you lay eggs about three times as often. | W | 1/s: `@e[type=chicken,distance=..16]` → subtract 40 from `EggLayTime` (check the field name on 26.3) | cheap |
| 36 | The Count | **Count Your Blessings** | When the tool or weapon in your hand reaches 10 durability left, he chimes and swaps it into a free inventory slot so it never breaks. You can repair it later. | U | 4/s: `execute if items entity @s weapon.mainhand *[minecraft:damage~{durability:{max:10}}]` → move it to the first empty `container.N` (macro), action bar line; skipped if the inventory is full | cheap |
| 37 | The Doodle Dragon | **Colour Outside the Lines** | Sheep you shear drop one more wool, and 20% of the time it comes in a random crayon colour. | W | `player_interacted_with_entity` (shears, sheep) advancement → summon a wool item at the sheep (random colour from a 16-entry table); revoke | cheap |
| 38 | The Eraser | **Clean Slate** | Junk from blocks you break (cobblestone, cobbled deepslate, netherrack, dirt, gravel, granite, diorite, andesite, tuff) is erased instead of picked up, but only once you already carry a full stack of it. Rubbed out in a puff of pink crumbs. | U | 4/s: freshly dropped junk items within 4 blocks (`Age<10`, block-drop `PickupDelay`, so things you throw are never touched) and you hold 64+ of that id → kill + crumb particles | med (fallback: a fixed list, a single stack check per id) |
| 39 | The Cursor | **Long Click** | You can reach 1.5 blocks further when breaking and placing blocks. | P | attribute `minecraft:block_interaction_range` `add_value 1.5` (it stacks with the Gnawing Pick's +2 while held; cap the total at +3) | cheap |
| 40 | The Ink Blot | **Puddle Form** | Hold sneak for 1 second and you spread into a blot half your size: you can walk through 1-block gaps and crawlspaces. Stand up and you regrow, once there's headroom. | U | sneaking 20 ticks → `minecraft:scale` `add_multiplied_base -0.5`; removed when you stop sneaking and the 2 blocks above are free (otherwise it waits) | cheap |
| 41 | The Speech Bubble | **Heads Up!** | A **"!"** pops up over any monster that's targeting you from behind or out of sight within 16 blocks, with a sharp note, so creepers and sneaking spiders can't surprise you. | C | 2/s: `execute as @e[type=#bm:hostile,distance=..16] on target if entity <you>` and outside your view cone (raycast/facing check) → text display "!" over it (1 s) + sound; a 3 s cooldown per mob | med |
| 42 | The Lightbringer | **Light Your Way** | A soft light follows you: the air around your head is lit to level 12, so caves and night paths light up as you walk, with nothing left behind. | W | 4/s: place `light[level=12]` in the air block at your head (only where it is air), marker remembers it; remove the old one when you move 1+ block. **Hard-ish** (block updates, multiplayer cleanup, chunk unloads); **fallback:** automatically place a torch from your inventory at your feet when block light < 1 | hard |
| 43 | The Pale Dryad | **Forager** | Leaves you break drop saplings, sticks and apples three times as often, and mushrooms you pick drop two. | P | extra pools in `#minecraft:leaves` and mushroom loot tables, conditioned on `bm.bA_dryad=1` (no shears / Silk Touch) | med (generated loot tables) |
| 44 | The Bound Sovereign | **Unmoved** | Its chains hold you: +40% knockback resistance and +50% explosion knockback resistance, so blasts and blows don't knock you off ledges. | C | attributes `knockback_resistance +0.4`, `explosion_knockback_resistance +0.5` | cheap |
| 45 | Vexis, the Unlinked | **Field Notes** | Vexis is curious about everything: the first time you set foot in each biome, you get 50 XP points and a line of its puzzled field notes. 65+ biomes to log. | P | one `location` advancement per biome (generated), per player, once → `xp add 50 points` + a note line; the Keeper's Bonds page shows "biomes logged" | cheap (many small files) |
| 46 | The Mireling | **Mirewalk** | Soul sand, soul soil and honey no longer slow you down. It moves through muck as a puddle, and so do you. | P | attribute `minecraft:movement_efficiency` `add_value 1.0` | cheap |
| 47 | 8-Bit Cecil | **Potion Refill** | Each potion you drink has a 20% chance to refill (the bottle comes back full, the same potion). | P | `using_item` (potion) → snapshot the hand item into storage; `consume_item` (potion) → 20%: summon an item from the snapshot at you (or `item replace` if the hand is empty) | med |
| 48 | 8-Bit Leo | **Cut the Grass** | Grass, ferns and dead bushes you break have a small chance to drop something: 4% 1-3 arrows, 3% a little **heart** (picked up: heals 2 hearts), 1% an emerald. | P | extra pool in those loot tables (`bm.bA_pxleo=1`); the heart is a custom item, and an `inventory_changed` advancement → `clear` + `instant_health` | cheap |
| 49 | 8-Bit Emma | **Goomba Stomp** | Fall 2+ blocks onto a monster's head and you stomp it: 6 damage, you bounce back up, and you take no fall damage. | C | each tick while `fall_distance > 2`: a hostile within 0.8 under your feet → `damage` 6 (player attack), Levitation V for 3 ticks, `fall_damage_multiplier 0` for 1 s; stomp sound | med |
| 50 | The Sky Buddies | **Change the Weather** | Two menu buttons: **Ask Nimbus for rain** or **Ask Sunny for sun**. The weather turns for 10 minutes. Once per in-game day. It can't end or start a pack event (Blood Moon, Dread Night, a storm needed for Democratus or KillerWatt's Effigy). | W | menu buttons → `weather rain 600` / `weather clear 600`; cooldown 1200 s; refused while an event flag is set; announced to everyone, because weather is server-wide | cheap |

**How they're spread:** 23 passive buffs, 11 utilities, 12 world effects and 4 combat (Leo, the Speech Bubble, the Sovereign
and 8-Bit Emma). Democratus's kill-XP bond leans towards combat but is marked as a passive. They cover:
- mining: Dennis, Ava, the Cursor, the Eraser;
- farming and animals: Emma, Bloo, Eggbert, Nia, the Dragon, Donado, Wilfrey;
- food: the Chef, Pearl, the Lantern;
- fishing and the sea: Tullius, Bones, the Frog;
- travel: Celi, KillerWatt, Kettle, Apophiss, the Mireling, the Stalker, Zib, the Ink Blot;
- inventory: Pistachio, the Count, the Gem, Rufus, Bender;
- XP and enchanting: Cecil, Democratus, Capshun, Vexis;
- brewing: 8-Bit Cecil;
- trading: Pearlman;
- exploration: Fishy, Vexis;
- light and safety: the Lightbringer, Batty, the Speech Bubble, Omega;
- weather and villages: the Sky Buddies, the Neighbor.

---

## Overlap check (against what the pack already has)

| Bond | Existing thing it avoids or differs from |
|---|---|
| Rich Seam (Dennis) | his Fortune V on ores (phase162) and the Ore Magnet: ores are excluded |
| Valet (Pistachio) | his Spirit Jar gathers mob drops; this refills hotbar slots |
| Stoke the Fire (Ashur) | Forgeheart smelts raw ore in your pack; this speeds up real furnaces |
| Cooked Through (Lantern) | Forgeheart covers ore only; this cooks food |
| Beam Me Home (Zib) | the Wayfarer's Lodestar returns you to a spot you mark; this returns you to your bed |
| Autosave (Capshun) | the Grave Charm keeps your items; this keeps your XP. (The Navigator's Astrolabe already shows coordinates, so that idea was dropped.) |
| Second Chance (Wilfrey) | replaces a gravestone idea, which overlapped the Grave Charm |
| Green Thumb (Emma) | the Harvest Scythe reaps and replants; this grows crops |
| Echo Sense (Batty) | the Xenite Dowser finds ores; this warns of drops and lava |
| Kindred Spirits (Donado) | replaces a low-gravity idea, which overlapped the gravity boots |
| House Call (Pearlman) | his own discounts and haggling are about villagers; this brings a wandering trader |
| Rest in Peace (Omega) | leaves the pack's own phantoms (Vorn, vault, curses) alone |
| Long Click (Cursor) | stacks with the Gnawing Pick's +2; the total is capped |
| Kingdom's Grace (Ava) | her Tide of Crowns gives Conduit Power for 20 s only; this is always on |
| Shell Collector (Bones) | his Dolphin's Grace and Water Breathing stay as they are; no water-breathing bond was added |

None repeats a follower's own power (each one's POWERS list, passives and "out of a fight" buffs were checked), and no two
bonds touch the same attribute or trigger with the same effect.

---

## Build notes (for later, not now)

- **Where it lives:** one new module (`phase255.py`, "the bonds") holds a `BONDS = {key: (name, kind, blurb)}` table keyed
  like `phase125.WHO`. It asserts it has exactly the WHO keys minus `keeper`, generates the 50 objectives, the unlock pass,
  the derived `bm.bA_*` pass, the menu row (patched into each follower's menu builder, as phase179 patches the wheel), and
  each bond's own functions, advancements and loot pools.
- **Loot-table bonds** (Dennis, the Dryad, 8-Bit Leo) must merge with the overrides already in the pack (phase162's Fortune and
  Looting tables), not replace them. `check262_nbt` / `check_xref` will catch a dangling function.
- **The costly ones** are Emma, Pistachio, Ashur, Bloo, the Eraser, the Speech Bubble, the Lightbringer, 8-Bit Cecil and 8-Bit
  Emma. Each runs only for players with `bm.bA_<key>=1`, at the rate given, never globally.
- **Tests (the owner's rule):** one bot test (t-next) as a regular player, after rcon sets the stage (Keeper + Dennis given and
  called):
  1. Walk the Keeper and a follower out together and see the unlock line.
  2. Open the follower's menu from its item and press `Bond: ... - on` as the button the client received, then see it turn off.
  3. Mine 200 stone and count the extra drops (Rich Seam).
  4. Send the Keeper home and check the bond still works.
  5. Open the Keeper's Bonds page.

  Add a bond assertion to the every-follower tests (the `KINDS` lists in t145 and t158), so each follower's row shows up.

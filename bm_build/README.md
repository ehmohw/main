# Black Market — v2.24 (Java 26.3)

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
- If he falls in battle, he fades away and the gem needs **10 minutes** before it can call him again.

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
- **What he drops:** 10 to 16 Tokens, 2 to 4 Medallions, a Trophy (40%), a Heartstone (15%), netherite scrap, pumpkins and pie. **1 time in 10, he drops his head.**

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
  - The cell stays empty for 10 minutes after he leaves.
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
| North counter | **The Fence** | Diamonds/emeralds/netherite → Tokens; Token → Medallion → Trophy; maps |
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

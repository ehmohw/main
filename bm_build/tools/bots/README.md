# Playtest bots

Real players for the Black Market datapack. Each bot is a minecraft-protocol client that logs into a local 26.3
server as an ordinary, non-operator player and plays: it holds and uses items, right-clicks entities, presses the
dialog buttons the server sent it, rides, and walks. rcon (the server console) only sets the stage: building an
arena, teleporting, handing out items with loot tables, reading scores and NBT to check results.

## Running them

From `bm_build/`, once per fresh container and again after a restart:

    tools/setup_test_env.sh --start

That fetches the 26.3 jars, builds the checkers' reference data, creates the test server in `~/bm_srv`, installs
these packages and starts the server with the built pack. Then:

    cd tools/bots
    node t133.js          # a whole test; prints PASS/FAIL lines and "N/M passed"
    node t133.js air      # some tests take a section filter
    node rc.js "list"     # run console commands
    node cmd.js "cmd"     # run commands with TestRat online

After rebuilding the pack, `tools/dev.sh --no-build` installs it and `/reload`s. Use `--restart` when a change adds
dimensions or worldgen.

`npm install` also runs `postinstall.js`, which patches minecraft-protocol 1.68.0 and minecraft-data 3.117.0 for
26.3: the 26.3 packet table (`patches/`), the 26.3 protocol number in the handshake (`PV=777`, set by the libraries)
and bundle packets passed straight through. The versions are pinned; the patch stops loudly if they change.

## Writing a test (the owner's rule)

Never rely on just running functions. Play as a regular player:
- **Check the bot isn't an operator first:** `A.cmd('gamemode creative')` must answer "unknown or incomplete command".
- **Press what the client was shown:** `await A.press(/words/)` sends exactly the command of the on-screen button
  whose words match, and waits for the next screen. `A.buttons()` lists the buttons, and `bm_build/BUTTON_CODES.md`
  says which menu each code needs.
- **Use items as items:** `A.slot(n)`, `A.use()` then `A.release()`, `await A.useWait()` (use, then wait for a
  screen), `A.useOn(x, y, z, face)` for blocks, `A.interact(entityId, sneaking)` for entities, `A.attack(id)`.
- **Move like a client:** `A.stand()` keeps reporting the bot's position; `A.walkTo(x, z)`; `A.input({shift: true})`
  to sneak; `A.ride(yaw, pitch, inputs)` / `A.unride()` while riding.
- **Watch what it gets:** `A.chats`, `A.bars` (action bar), `A.dialogN` (dialogs received), `A.ents` (entities in view).

`lib_resp.js` is the current library: `bot(name)`, `rcon()` (returns `run(cmd)` and `end()`), `sleep(ms)`. `lib.js` is
the older one, without dialog tracking, and many early tests use it. `h110.js` holds helpers for single-room heists.

## Things that have bitten before

- The bot doesn't fall by itself. After a drop, simulate the fall a tick at a time (`fall()` in `t133.js`), or the
  bot hangs in the air and an "unhurt" check proves nothing.
- `execute if entity` answers "Test passed. Count: N" (capital C).
- `execute as <player> ...` sends its feedback to that player, not to rcon.
- A dying mob keeps its rider for its 20-tick death animation, and `@e` can't select it.
- Zombies burn in daylight. Use husks when fire matters.
- A follower called without its item in the bot's pockets goes home after 3 seconds. Give the bot the item and use it.
- The Black Market expels anyone without a market key.
- The server kicks a client that moves twice in one tick; the libraries close each tick with `tick_end`.
- Clean up between sections: kill test mobs, reset scores and tags, clear followers.
- A ladder's plate is solid. A climbing bot keeps to the middle of the ladder's block, or the server rejects every step.
  At the top, climb a little past the floor's height, then step over.
- `execute if function` can't end a command. To check riding, use `execute as <bot> on vehicle if entity @s[...]`.
- 26.x doesn't save `NoAI:0b` or `Invulnerable:0b` at all. Check for "not 1b".
- Freeze damage reads "froze to death" even when a mob dealt it.
- Two presses of a held-use item less than 3 ticks apart count as one press. Wait 150 ms or more between them.
- Killing a follower's host is a faint, and its 5-minute rest lands a few ticks later. Reset cooldowns after that.
- A player name can't take selector arguments (`TestRat[...]`). Use `@a[name=TestRat,...]`.
- Followers in a boss fight push the boss past its thresholds. Hold its health with rcon between steps, so each threshold
  is the test's own.
- Give the bot Resistance as well as health for a boss fight. A dead bot respawns far away and every check after fails.
- `bossbar get <id> visible` answers "is currently visible" or "is currently hidden" (not shown / true / false).
- Staging the bot into a guarded place (the Serpent's Den): mark it and move it in **one** command (an admin function).
  Two rcon commands leave a tick between them, and the guard can find the bot unmarked and throw it out.
- A sequence that plays out in a few seconds (a boss's coming) needs one tight loop that samples everything, timed by the
  boss's own tick counter. Separate checks with waits between them miss what they're looking for.
- An item taken back out of a case lands in the hand that took it. Clear the inventory before reusing that slot.
- Titles and subtitles are in `A.titles` (lib_resp.js).
- The server's rcon reads one request per read. A second request sent with it (for example, two `run()`s inside a
  `Promise.all`) is lost, and the connection goes quiet after it. `lib_resp.js` now queues requests one at a time, and
  a reply that never comes gives up after 15 s with `RCON TIMEOUT: <command>`.

## Index

The newest tests (t128 onward, especially t131-t133) follow the owner's rule throughout. Older ones lean on rcon
and function calls. Three are known to be stale.

| Script | What it covers |
|---|---|
| `t5lay.js` | - |
| `t23.js` | first check: mailbox model on its hitbox |
| `t23b.js` | - |
| `t23c.js` | - |
| `t24i.js` | first check: sparks: first target and chain hit, far one spared |
| `t24m.js` | Cecil in a freshly placed market: spawn, rig, facing, trades, animation |
| `t25.js` | first check: notice text sits on the plank face, open in front |
| `t26.js` | first check: tidal tear hurts another player, not the caster |
| `t27.js` | first check: pact refused (and refunded) with no Blood Moon |
| `t28.js` | first check: skiff called, pilot aboard |
| `t29.js` | first check: filter hopper placed (pointing down) |
| `t29c.js` | - |
| `t29e.js` | - |
| `t30.js` | first check: newcomers' book: accepted by the game, every page |
| `t31.js` | first check: raw `time set 1000` no longer sends the count back to day 0 |
| `t32.js` | first check: Lucky Night started |
| `t33.js` | v2.32: the Horseman's Head in four classes, catalysts, the Pharaoh's Crook and Thunderbird Talon (all forms), the Sand Pharaoh, |
| `t33p.js` | v2.32: the Horseman's Head in four classes, catalysts, the Pharaoh's Crook and Thunderbird Talon (all forms), the Sand Pharaoh, |
| `t34.js` | v2.33: the Heartwood Branch, Molten Gauntlet and Void Scepter (all forms, catalysts); the Elder Treant, Magma Colossus and |
| `t35.js` | v2.34: every roaming boss always drops its relic to a player's kill (3 kills each) |
| `t36.js` | v2.35: sockets by material (vanilla only), red Vitality + size cycle, combos (incl. Bloodlust, Second Wind), Masterworks, |
| `t37.js` | v2.35: sockets by material (vanilla only), red Vitality + size cycle, combos (incl. Bloodlust, Second Wind), Masterworks, |
| `t38.js` | v2.35: the chestplate essences/resonances against a real attacker (a husk with AI: the damage command never triggers on-hit enchantments) |
| `t39.js` | v2.36 fixes: trades stay open (no re-teleport), Barnaby's spot, nameplates follow, Cecil's spawn on a step, admin/blood_moon |
| `t39b.js` | - |
| `t40.js` | v2.37 Emma: encounter + recruit, rig follows, states, modes + buffs, quick heal, charge, ethereal strike, harmony with Cecil, falling **(stale: expects the 10-minute faint rest and send-home on 7305)** |
| `t41.js` | v2.38: the follower cap (3), the shifter and Emma's menu don't cross, Emma's lore lines **(stale: summons by function, so the 3-second item rule sends followers home)** |
| `t42.js` | v2.40: KillerWatt's Tendrils, Apophiss's Crown, Leo's Trident, Cecil's Staff |
| `t42b.js` | - |
| `t43.js` | v2.42: two-blade tendrils + lunge; v2.41: tendrils worn on the chest (4 at the back, look-to-lash, sneak+jump fling, snatch, weather), crown at nig... |
| `t44.js` | v2.43: tendril melee stab (+2 reach, both upper tendrils, pierce) and the charged-jump pose |
| `t45.js` | v2.45: Pearlman, the gems (finder, display, kin), the fusion, the Ethereal shrine and status |
| `t46.js` | v2.46: Pearlman visits like a wandering trader - one roll a day, 10% rising by 10 to 30%, reset when he comes |
| `t47.js` | v2.47: carrying the Ethereal Gem anywhere in your inventory: a shimmer of the nine follows you |
| `t48.js` | v2.48: the Hollow Gate - set up, five Emblem sockets, opens, only 5-conquest players pass, way home, take back, pack up; |
| `t49.js` | v2.49: Shifting arms, followers vanish on death, Tendril modes (toggle / ranged auto-lash / offense grab), Pearlman's trades stay open |
| `t49b.js` | v2.49: Pearlman's trade window stays open while he turns to face you |
| `t50.js` | first check: Blood Moon foe near a placed Ethereal Gem: slowed, weakened, slowly burned |
| `t51.js` | first check: Donado gets his jointed rig (8 parts riding him, the old body gone) |
| `t52.js` | first check: Both placed (a marker each) |
| `t53.js` | first check: A receiver touching a transmitter is refused (it would latch on) |
| `t54.js` | first check: Cecil summoned with his own (poison) look |
| `t55.js` | first check: Summoned in Healing: rose dress |
| `t56.js` | first check: Stars home in on the player (levitation from a hit) |
| `t56b.js` | first check: Stars home in on the player (levitation from a hit) |
| `t57.js` | first check: Each rat learns its variant |
| `t58.js` | first check: Encounter: Celi stands there (9 rig parts + her hitbox) |
| `t59.js` | first check: Cecil comes in his new (shorter, slimmer) look |
| `t60.js` | first check: Invite: PartyPal gets an [Accept] invite |
| `t61.js` | - |
| `t62.js` | first check: Market Cecil wears the new model (5 parts incl. the free arm, old body gone) |
| `t63.js` | first check: Hang Cecil's gem in a frame: an anchor appears, and Cecil comes out |
| `t64.js` | first check: In the vault: adventure mode |
| `t65.js` | first check: Cecil has five parts now (his free arm is its own), all on the new rig |
| `t65c.js` | v2.65 content: the new rooms and events, secrets, rare foes, the heist items, the layout's connectivity |
| `t65k.js` | v2.65: kit abilities, hirelings, the Endless Vault, the Pit |
| `t65m.js` | v2.65: who guards each tier, the tier guardians, the music, the themed stone |
| `t65o.js` | v2.65: the 2.60 rooms still work in their new tiers (levers, plates, guards at I; tiles, lasers, dial at III), on a bench |
| `t65r.js` | v2.65 raid core: tries + fee + lucky pool, respawn in the den (and back), fail-reset, the pot, passages, dial button, one-time rewards, bond |
| `t66.js` | first check: The Heist Plans: pick tier V - you're led down into the vault |
| `t67.js` | first check: The full Gilded set: no fall damage (fall damage x0) |
| `t68.js` | first check: A party member (not the leader) can't plan the heist |
| `t72.js` | first check: Display case: use it looking at the floor - a floor case stands there (case, contents, hitbox) |
| `t73.js` | first check: A bottled cow goes in a floor case: she appears on the cushion |
| `t74.js` | first check: …: ladders all the way up (… rows) |
| `t78.js` | v2.65: follower cosmetics - Emma's ribbons and dresses, Celi's outfits, Zib's uniforms; Velour's stock; the hidden ones |
| `t79.js` | v2.65: KillerWatt - the Storm Effigy, the boss (rig, animation, attacks, roar, reward), the Spark follower, Cecil's shop |
| `t79b.js` | v2.66: KillerWatt the follower - riding, wall climbing, the Thunder Leap, the tendril stab, the leap, chain lightning, gems and the Ethereal Form |
| `t80.js` | v2.66: the Fixer's Office - the Gutter Bank, spoils, kit ranks, secondaries and signatures; metal trophies; the Bond Sigils |
| `t86.js` | v2.67: haul themes + the capped prize, everything in The Haul, the pot nerf, the bank's medallions, the Scrap Box, |
| `t87.js` | v2.67: crew scaling, hidden vaults, the hidden treasures, and the Gutter Gentry |
| `t89.js` | v2.67: followers in the vault (raid contracts), the follower wardrobe at Goldtooth, Emma's new outfits |
| `t90.js` | v2.67: fees by tier, double and alien heists, the five new rooms |
| `t91.js` | v2.67: game night in the vault - the seven game rooms |
| `t91p.js` | v2.67: game night in the vault - the seven game rooms |
| `t92.js` | v2.67: the Frisbee Shield, the Ranged kit's arrows, the crew's health bars |
| `t93.js` | v2.67: the rogues' gallery - new guards, odd ones, second guardians |
| `t96.js` | v2.67: Leo (the seawatch fort, the defence, the follower, his pairs), the faces, cosmetics that stay on, the Ethereal Gem |
| `t97.js` | v2.67: Leo sits (a click box the size of him, a seated cycle), Leo in an item frame; the blocky Arachno-Lantern spawns whole |
| `t98.js` | v2.67 check: the Scorching Heart / Hearthfire, Ethereal KillerWatt and the Ethereal Tendrils |
| `t99.js` | v2.67 (code pass): friendly fire spares every follower; KillerWatt's held reaction poses (arrival roar, flinch, tendril swipe, |
| `t100.js` | v2.67: Democratus - the storm vigil, recruiting him, his sweep and Storm Reap, the Cecil / KillerWatt pairs, sitting, fainting, |
| `t101.js` | v2.67: the vault's own rules - the Raid Crew (ledger roster, the follower cap, the crew going home), the kit on loan |
| `t102.js` | v2.67: follower wardrobes - an outfit used once is unlocked for good (and used up); each follower's menu changes into it, |
| `t103.js` | v2.67b: Democratus in rain and thunder, Leo's water breathing, the follower trios, followers swimming, one rest room a heist |
| `t104.js` | v2.67c: after the heist - every raider pays their own fee (Tokens pass the coat check); a win pays the fee back and maybe a few |
| `t105.js` | v2.67d: the vault smoothed out - the way out asks first mid-run (instant otherwise); the crew needn't wait on the leader |
| `t106.js` | v2.67d: the Ledger's Locker Hall trip - from safe ground in the Overworld, the Nether or the End (not the Hollow or the gutter; |
| `t107.js` | v2.68: the vault's loose ends - the tile floor's sides, crew changes rescale the guards, leave from the Ledger, a dropped |
| `t108.js` | v2.68: currency wins, the Crate Desk, tip-offs, laurels + achievements, Forgeheart, the Alibi, the Counterfeiter's Press |
| `t109.js` | 2.68 follow-ups: Locker Key in the gutter only, Office leave button, Boomer filing, den NPC dedupe, door in the doorway, |
| `t110.js` | 2.69 (I): the Combination Room, the Weighing Room, the Gauntlet and the Tile Floor in their B and C variants; the tile seam |
| `t111.js` | 2.69 (II): the Dial Lock, the Three Coffers, the Signal Lamps, the Lamp Floor, the Tumbler Lock, the Bell Tower and the |
| `t112.js` | 2.69 new rooms: the Sky Isles, the Spire, the Tinker's Bench, the Mason's Plan, the Dig; Block Party, Red Light Green Light, Memory Match |
| `t113.js` | 2.70: the throne rooms (gold, diamond, netherite - and their odds) and Prime fights |
| `t114.js` | 2.71: the B and C versions of the Spire, the Tinker's Bench, the Mason's Plan and the Dig |
| `t115a.js` | 2.72 (I): the Library, the Pipes, the Apothecary, the Grapple, the Minecart Run - three ways each |
| `t115b.js` | 2.72 (II): room curses, forks in the road, corridor traps |
| `t115c.js` | 2.72 (III): Smelling Salts, the Thief's Hourglass, the Alarm Jammer, Masterworks, the Codex, each tier's own finds |
| `t118.js` | 2.73: a raid boss's minions fall with it |
| `t119.js` | 2.74: outfits and Emma's buff from the Ledger; Emma remembers her buff **(stale: its helper hands out the retired Heist Plans)** |
| `t120.js` | 2.74: checkpoint respawn + kept pockets, kit 32/4, Lights Out / Glass Cannon only out on the heist, den names + carpet, |
| `t121.js` | 2.74: the Fixer's Lounge; Leo's size |
| `t122.js` | 2.74b: Speed Run with the alarm off, patrols stop at the vault, puzzle skip, a mistake's guard cleared, solo crew of 3, |
| `t123.js` | 2.74: Block Party keeps you in the room; a failed puzzle's mobs go on solve |
| `t124.js` | 2.75: the bank's exchange both ways; chatter in follower menus; modifiers at BEGIN |
| `t125.js` | 2.75b: records, the hidden cache, Democratus (size, seat, duel), KillerWatt sits, Sparks Fly, Call-for menus, the Lounge on the |
| `t126.js` | 2.75c: invisible armour, Pearlman's bell, builders' crates, the Netherite Laurel, one set of gems per world, hand-run tier |
| `t127.js` | repro: the end-of-heist Go to the Lounge, then the den/lounge menus, by real clicks (triggers, right-clicks, item use) |
| `t128.js` | 2.76: the Wraithfire Heart - Pearlman's fusion, carried, the hearth, Cecil / KillerWatt / Emma - by real clicks where a player would click |
| `t129.js` | 2.76: a vault beside each trial spawner - placed in a new dungeon, patched into an old one, opened with the dungeon's key once per player |
| `t130.js` | 2.76: Pearlman's collection (real trades), the Golden Statue, Pearlman the follower |
| `t131.js` | URGENT (2.76): the Ledger, played as a regular (non-op) player - every step is a real packet: the item used, the buttons |
| `t131mp.js` | URGENT (2.76), two players (both regular, non-op): the end-of-heist "Go to the Lounge" for a crew - pressed from the screens |
| `t132.js` | 2.76: Wraithfire Emma (as a regular player, every step a real packet) + the Fence's heist item. |
| `t133.js` | 2.76 regression (regular players, real packets): Emma's everyday life after the Wraithfire update - Cecil's harmony, |
| `t134.js` | 2.77: Apophiss (regular player, real packets): the serpent seal in the Hollow throne room (Emma, Leo, Cecil called with |
|  | their items), the den, both phases of the fight, the bot's last blow, the drops, the pad back up; the Serpent's Oath - |
|  | sitting, the saddle, riding (walk, fangs), his menu, his fights, fainting. Sections: `seal`, `fight`, `pet`. |
|  | 2.77b: section `den` (a teleport into the den, a stand on its dome: thrown back up; no boss without a Hollow conqueror |
|  | back with Emma, Leo and Cecil); his coming in black fire watched as one loop by his own clock; the feint at half (the |
|  | bar gone, the court gone, the three wondering, nothing won) before THE SERPENT UNBOUND; the follower at full size. |
| `t135.js` | 2.77: Tullius (regular player, real packets): the ghost ship found by `locate` and built by its seed, swum to and climbed |
|  | aboard by its ladder; "Tullius needs Leo" (no captain alone - the hint - then Leo's crest on deck); the fight (harpoon |
|  | hook + point-blank, crew, frost, put overboard he leaps back aboard), drops, the setting off; his blunderbuss and harpoon |
|  | in the bot's hands; the Doubloon follower (sit, menu, harpoon pull, swimming, buffs at sea, faint, contract). |
|  | Sections: `ship`, `weapons`, `pet`. |
| `t136.js` | 2.77: the new pairs and trios, every follower called with its own item: Frost and Brine, Old Rivals, the Tidewatch (and |
|  | at sea), Forgiven, Venom and Volts, An Uneasy Truce, the Dread Court, the hidden Royal Retinue - and Pearlman as a fourth |
|  | never displacing the Serpent's Bane. Sections: `tul`, `apo`, `retinue`. |
| `t137.js` | 2.77b: the Wraithfire Heart forged on the ground - an Ethereal Gem and a Scorching Heart set down with the items |
|  | themselves (both orders): the forging starts, both rise, circle closer, merge; the bot picks the heart up, Burning Blue; |
|  | nothing left behind; six blocks apart nothing happens; Pearlman no longer offers the fusion. |
| `t138.js` | 2.77b: follower figurines - a case set down with the case item, every follower's item right-clicked in (all ten), |
|  | punch for the item and back, sneak + right-click turns it, empty-handed out; a wall case (Apophiss's Oath), picked up. |
| `bounty.js` | Bounty Board play-test: a market marker in the arena gets the board from the p35 patch; a bot signs it during a |
| `fixes.js` | 2.20 fixes: XP flask (main hand), triple-jump boots logic, Ender Pouch, Hoard Sack, Golden Cheese Wheel, orphan Vorn models. |
| `head.js` | The Horseman's Head: stream, overheat, charged blast, stoking + Nova, undead XP, lantern/heart variants, night tiers, healing. |
| `horseman.js` | Headless Horseman play-test: spawn him near a survival bot at night, watch him fight, then kill him. |
| `lecterns.js` | Place the market at all four turns; check every lectern (blocks and ledger displays) faces the same way relative to the market. |
| `mpatch.js` | A market placed deep underground (as an old market would be): the 2.20 patch - shaft to the surface, dock rat, docks sign, water dried. |
| `play.js` | Play-test suite: two real (bot) players exercise the custom items on the live 26.3 server. |
| `regalia.js` | The Hollow King's Regalia + Sepulchre: names, wither immunity, waking by tier (trims, buffs), Wither Nova, Grave Quake. |
| `skiff3.js` | skiff: the hull boards the skiff (2nd passenger) at the right height, steps off when the pilot leaves, re-boards after them |
| `sweep.js` | Use every right-click / consumable item once as a real player and record what visibly happened. |

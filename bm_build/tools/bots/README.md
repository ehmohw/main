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
- Sounds the client was sent are in `A.sounds` (`{name, cat, t}`: `cat` is the channel - 1 music, 2 record/jukebox, ...) and stopped sounds in `A.stops` (`{source, sound, t}`; a bare `stopsound @s music` has no `sound`). Setting a staged boss's real health below its rage line freezes it for its rage moment (invulnerable) - wait for its rage tag and `bm.cfrz` gone before the killing blow.
- A player's `Health` can't be set with `data modify` (players' data is read-only). Hurt the bot for real:
  `damage TestRat <n> minecraft:magic` (magic ignores armour).
- A bot's max health can carry bonuses earned in earlier tests. Measure its own baseline before checking a health bonus.
- A real jump (for the jump statistic): the bot leaves the ground going up, a tick a step, and lands (`jump()` in t139.js).
  To jump while sneaking, press sneak a few ticks first. The server only counts the crouch on its next tick.
- Inline item modifiers in commands take `type:`, not `function:` (`item modify ... {type:"minecraft:set_name",...}`).
- A bot put up in the air (beside a flying boss) stays there. Set it on the floor before it walks to pick something up.
- The screen shake (`rotate` on players) reaches the client as `player_rotation` packets; count them to see it happen.
- The server's rcon reads one request per read. A second request sent with it (for example, two `run()`s inside a
  `Promise.all`) is lost, and the connection goes quiet after it. `lib_resp.js` now queues requests one at a time, and
  a reply that never comes gives up after 15 s with `RCON TIMEOUT: <command>`.
- A trader's price in its phase file isn't always what it charges: later passes (the BM price retune) change counts. Read
  the price from the trader itself (`data get entity <npc> Offers.Recipes[i].buy.count`) before paying for a real trade.
  To find a trade, walk `Offers.Recipes[i].sell.components."minecraft:custom_data".bm` until it names the item.
- `bm:p45/cecil/spawn` sets Cecil (the trader, with his whole stall) down wherever it runs - a stage for any trade of his.
- In 26.3 a used consumable leaves the hand only after its advancement's function has run. A check made at once still sees
  it held; to prove an item isn't used up, look again a second later (t144).
- A test that changes dimension (the Lounge, the Hollow, a Warpstone crossing) needs `lib_resp.js`: it reports
  `player_loaded` after each respawn or dimension change, and until a client has, the server ignores its moves and uses.
  `lib.js` doesn't.
- The Recruiter only lists a follower you've met (`bm:met/<kind>`, earned by holding that follower's token), and a follower
  contract used before then is refused and kept. A test that buys or signs a follower's contract grants it first:
  `advancement grant TestRat only bm:met/<kind>`. Revoke `bm:met/*` to start clean.
- A solo player's raid crew holds three (since 2.74). A fourth follower waits on the bench.
- To get past a heist room that isn't under test, set `#gi bm.rng` to the heist's id, run `bm:p70/ctx`, then run
  `bm:p70/solved` as that room's marker (`bm.gvr`) - its exit opens as if it had been beaten.
- An empty list answers "Found no elements matching ..." (a villager with no trades: `data get entity <npc> Offers.Recipes`).

- Follower items (bowls, coins, tokens) and contracts share one use debounce, `bm.gvhc`: set to 2 on a use, counted down
  once a second. A second item used within 1-2 s of the first (a menu opened with sneak + use, say) does nothing. Wait
  ~2.2 s between them (t163).
- An item taken out of a display case empty-handed comes back into the slot that was selected - the empty one. Put the
  follower's item back where the test expects it before using that slot again (t138, t163).
- A hostile mob summoned for a follower to fight can be rolled into an elite or Champion by the second loop (new health,
  new speed). Summon it with the `bm.seen` tag so the roll skips it (t162, t163).
- Dialogs the client receives come wrapped as `{data:{...}}`; unwrap with `d => d && (d.data || d)` before reading `title`
  or `body`. Body text components put `extra` before `text`, so find a row by its `contents.text`, not a JSON regex.
- In the Fixer's Lounge the game puts a Locker Key in hotbar.0; the Cabinet's NPC treats it (and the Ledger, and Fishy's
  bowl) as an empty hand, but a test that wants a truly empty hand should select slot 8.
- A new painting variant (`data/bm/painting_variant/`) loads only when the server starts: a `/reload` that adds one fails
  with "Failed to load registries due to errors", and nothing else reloads either. After `tools/dev.sh --no-build`, stop
  the server (rcon `stop`) and start it again with `tools/setup_test_env.sh --start` (t164).
- `A.use()` sends use_item, a right-click into the air. Hanging a painting, frame or anything else placed on a block face
  needs `A.useOn(x, y, z, face)` (block_place on that face; 2 north, 3 south, 4 west, 5 east) (t164).
- A mob's `CustomName` is stored as a plain string when it's plain text: match it with `nbt={CustomName:"Rex"}`, not
  `{CustomName:{text:"Rex"}}`, even though it was summoned that way (t164).
- A plain `run('execute as TestRat run function bm:p28/act')` does nothing: `p28/act` copies `#act` from the player's own
  `bm.act` first. Press the button with `A.cmd('trigger bm.act set N')` and the menu set (t121, t150).
- The bot keeps its health, tags and scores between runs. Heal it (`effect give TestRat minecraft:instant_health 1 4 true`)
  before anything that reads its health: Democratus's duel is lost if you're on three hearts or less when it starts (t125).
  A run that ends mid-countdown leaves the bot "in a duel" (`bm.dmduel`, `bm.dmd`), and the seal then refuses to call
  him. Clear both when setting the stage.
- Summoning several followers one after another: wait ~2.3 s between the items (the shared `bm.gvhc` debounce, above),
  or one of them silently doesn't come (t134).
- Particles reach the bot raw (`world_particles` gives `{data: Buffer}`, not parsed fields). In 26.3 the particle comes
  first (its type as a varint, then its own data), then the two flags, then x, y and z as big-endian doubles. A dust
  particle is type 21 with a colour int and a scale float, so its x is at byte 11 and its z at byte 27 (t165).
- Tailor purchases of follower outfits go straight into the follower's wardrobe (the `bm.wu<w>` bits); no item lands in
  the pack. Test the item's own use with `loot replace ... bm:items/<id>` and clear the wardrobe bit first (t165).
- The Tailor's stock codes are positional (7750 on, overflowing to 8111 on): a new outfit shifts every code after it.
- `#gt`, `#gn`, `#r` and most `#x bm.rng` scores are shared scratch: other ticking functions overwrite them between two rcon
  commands. Set them right before the call that reads them, each time - never once before a loop of separate commands (t166).
- A Wraithfire Emma left switched on (`bm.emwf` 1, `bm.emst` 1) keeps every Emma the bot calls ethereal for good: no dress,
  other buffs. Reset both when a test dresses Emma or checks her pair buffs (t96).
- The Raid Crew page has a row for every follower: scan 20+ rows for one at the back of the line (t105).
- A dungeon placed with `place structure bm:p2_<d>` turns with a random rotation: find its blocks from its `bm.dg` marker,
  `execute as <marker> at @s rotated ~ 0 positioned ^dx ^dy ^dz` with the template offsets from the marker (t167).
  Count from the legend (`BUTTON_CODES.md`) or press by label, never by an old offset (t105).
- A staged boss (2.80: the roaming and dungeon bosses) arrives frozen and invulnerable: nothing lands for its first 2-5 s
  (`bm.carr`, `bm.cfrz`). Wait for `bm.carm` before hitting it. Its health carries a buffer (`bm.cbuf`, up to max health
  1024): its real health is `Health - bm.cbuf`, its bar already shows that. To bring it to a threshold, set
  `Health` to `bm.cbuf + n`. A killing blow starts its death (`bm.cdie`): it falls 4-5 s later (t168, t169).
- `NoAI:0b` isn't stored: `data get entity <e> NoAI` finds nothing for a mob with its AI on. Test for "not 1b".
- `bossbar get <id> visible` says "currently visible" / "currently hidden" (never true/false).
- Switching to a weapon resets the attack cooldown: a hit right after `A.slot(n)` lands at a fifth of its damage. Wait
  ~1.3 s before `A.attack()` (t168).
- Placing a structure where a run before placed one stacks a second set of markers: kill the area's entities first (t169).
- Remove every chunk a test forceloads. Hundreds of leftover forceloaded chunks slow the server to "Can't keep up".
- 26.x: `#minecraft:dirt` is dirt, coarse and rooted dirt only. Grass has `#minecraft:grass_blocks`;
  `#minecraft:substrate_overworld` and `#minecraft:supports_vegetation` cover both.
- Donado (and anything else with a rig) gets new parts on its first second out: the old one-piece body is killed. Read
  the rig's parts (`bm.dnr_torso` and so on), not `bm.dn_body` (t165).
- 26.3's player actions gained `CHANGE_DESTROY_DIRECTION` at 1: 6 is RELEASE_USE_ITEM (what `A.release()` sends) and 7 is
  SWAP_ITEM_WITH_OFFHAND, the F key. Press it with `A.swap()`; hold `A.input({ shift: true })` first for sneak + F (t174).
- 26.3 leaves an effect's `amplifier` out when it is 0: `active_effects[{id:...}].amplifier` finds nothing for a level I
  effect. Test that the effect is there, then read the amplifier or take 0 (t174).
- `effect give ... 255` is amplifier -1 (a signed byte), and the effect does nothing. Use 120 or so for "a lot" (t173).
- Saturation is an instant effect: `effect give @s saturation 2` lasts 2 ticks, not 2 seconds, so it is almost never in
  `active_effects`. Test it by the food bar (`foodLevel`) refilling after a Hunger drain (t173).
- A selector with no position (`@e[tag=x]`) matches entities in every dimension, whatever `execute in` says. Give it a
  box or `x/y/z,distance` to keep it to one place (t162).
- Apophiss's den: its floor is at y4, so you walk at y5. A bot teleported to y3 stands inside the floor. Standing still
  works, but every step is silently undone (the server's "colliding with something new" check, which isn't logged) (t174).
- `walkTo` keeps the bot at one height and doesn't step up. A move into a block is undone with a teleport, and `walkTo`
  stops at the first one. Walk over ground you know is flat.
- Hurting a bot to a set health with `damage ... minecraft:magic`: Protection reduces magic damage. Use
  `minecraft:out_of_world` when the bot wears protected gear (t139).
- The Lounge's coat check keeps what isn't heist gear: put test gear in slots that don't overwrite the kit (`item replace
  ... hotbar.1` replaced the Tokens there) (t173).
- A follower killed with rcon counts as fainted: clear its cooldown (Apophiss: `bm.apcd`) before calling it again (t174).
- Market zones expel anyone without a market key: give the bot one (`loot ... bm:items/market_key`) before staging it in a
  market. A placed market's own install (the Cabinet hall) runs from its per-second loop, which only runs with a player
  within 100 blocks of its marker (t162).

- 2.80a: the vault's catch-all sees out anyone in `bm:gutter` who is neither on a heist (`bm.gvp`) nor checked (`bm.lgbag`),
  within 5 ticks. A test that puts a survival bot in the vault by command (the Locker Hall, the Lounge, a heist room)
  must give it the operator's pass first, `tag <bot> add bm.gvok`, and take it off at the end (t101, t107, t126...).
- Every button press is a command, and the server kicks a client for about 10 commands in a burst (`disconnect.spam`).
  Space presses about a second apart (t175).
- Dialog labels can start with an icon (`⬆ `, `✦ `): match them without `^`, or strip non-ASCII first (t175).
- The safe-ground rule for planning heists is a world setting (`#plany bm.rng`): `admin/plan_anywhere` turns it off,
  `admin/plan_safe` back on. A test that turns it off should turn it back (t107); the old `heist_plans_*` names are gone.
- The heist's knock-out keeps your pockets from a snapshot a few ticks old: wait half a second after changing a bot's
  inventory before killing it (t107).
- A follower fights whatever hostile mob is near: clear the test field of stray mobs, or a sit or a ride is interrupted by
  a swing at a creeper (t100, t125).
- Two crews in a row: a heist now closes when its last raider leaves (2.80a). Before, a quick second plan joined the old
  heist and no end-of-heist screen came (t131mp).
- 26.3 answers an `execute ... if entity` that finds nothing with "Test failed", not "Count: 0" (t23).
- One RCON reply holds about 4 KB: a trader's whole `Offers` list is cut short. Read it one recipe at a time (t25, t32).
- Count by area, not world-wide: other tests leave their own markers, boards and slot machines behind (t25, t32).
- 2.80: a roaming boss stages its arrival (about 5 s, untouchable, health buffered) and its death (about 5 s). Wait both
  out before checking it (t33, t34, t35).
- A mob summoned without `bm.seen` gets the pack's tiering on its next tick (an Elite, more health). Tag test mobs
  `bm.seen` when their health matters.

- Gear carried through a coat-check door (the Lounge's, a heist's) comes back a moment later, wherever it lands - not
  always in the slot it left. Wait for the item, then select its own slot before using it (t131's `holdLedger`).

## Index

The newest tests (t128 onward, especially t131-t133) follow the owner's rule throughout. Older ones lean on rcon
and function calls. The ones known to be stale (wholly or in part) are marked.

| Script | What it covers |
|---|---|
| `t5lay.js` | - |
| `t23.js` | first check: mailbox model on its hitbox |
| `t23b.js` | - |
| `t23c.js` | - |
| `t24i.js` | first check: sparks: first target and chain hit, far one spared |
| `t24m.js` | Cecil in a freshly placed market: spawn, rig, facing, trades, animation |
| `t25.js` | first check: notice text sits on the plank face, open in front |
| `t26.js` | first check: tidal tear hurts another player, not the caster **(summons by function, so the 3-second item rule sends followers home)** |
| `t27.js` | first check: pact refused (and refunded) with no Blood Moon |
| `t28.js` | first check: skiff called, pilot aboard |
| `t29.js` | first check: filter hopper placed (pointing down) |
| `t29c.js` | - |
| `t29e.js` | - |
| `t30.js` | 2.29 checks, kept current: the newcomers' book (the real lectern book, placed by the market's own function - no helper pack), the first-token tab and recipes, boss and dawn advancements, the crafter recipe, the server settings (2.80: a dialog), the Blood Moon period (a risen Blood Moon lasts till dawn - the change shows the next night) and "Never", the Block Breaker / skiff bombs / magic PvP switches, the Grave Charm (owner and stranger), admin help |
| `t31.js` | first check: raw `time set 1000` no longer sends the count back to day 0 |
| `t32.js` | first check: Lucky Night started |
| `t33.js` | v2.32: the Horseman's Head in four classes, catalysts, the Pharaoh's Crook and Thunderbird Talon (all forms), the Sand Pharaoh, |
| `t33p.js` | v2.32: the Horseman's Head in four classes, catalysts, the Pharaoh's Crook and Thunderbird Talon (all forms), the Sand Pharaoh, **(stale: superseded by t33, which waits out the 2.80 arrivals)** |
| `t34.js` | v2.33: the Heartwood Branch, Molten Gauntlet and Void Scepter (all forms, catalysts); the Elder Treant, Magma Colossus and |
| `t35.js` | v2.34: every roaming boss always drops its relic to a player's kill (3 kills each; 2.80: after its arrival, and its staged death) |
| `t36.js` | v2.35: sockets by material (vanilla only), red Vitality + size cycle, combos (incl. Bloodlust, Second Wind), Masterworks, |
| `t37.js` | v2.35: sockets by material (vanilla only), red Vitality + size cycle, combos (incl. Bloodlust, Second Wind), Masterworks, |
| `t38.js` | v2.35: the chestplate essences/resonances against a real attacker (a husk with AI: the damage command never triggers on-hit enchantments) |
| `t39.js` | v2.36 fixes: trades stay open (no re-teleport), Barnaby's spot, nameplates follow, Cecil's spawn on a step, admin/blood_moon |
| `t39b.js` | - |
| `t40.js` | v2.37 Emma: encounter + recruit, rig follows, states, modes + buffs, quick heal, charge, ethereal strike, harmony with Cecil, falling **(stale: expects the 10-minute faint rest and send-home on 7305)** |
| `t41.js` | v2.38: the follower cap (3), the shifter and Emma's menu don't cross, Emma's lore lines **(stale: summons by function, so the 3-second item rule sends followers home)** |
| `t42.js` | v2.40: KillerWatt's Tendrils, Apophiss's Crown, Leo's Trident, Cecil's Staff **(partly stale: Cecil no longer sells KillerWatt's gear (2.79b), and the chest-worn tendrils' yank and snatch went with 2.4x's equippable tendrils)** |
| `t42b.js` | - |
| `t43.js` | v2.42: two-blade tendrils + lunge; v2.41: tendrils worn on the chest (4 at the back, look-to-lash, sneak+jump fling, snatch, weather), crown at nig... **(partly stale: the chest-worn tendrils' checks predate the equippable tendrils)** |
| `t44.js` | v2.43: tendril melee stab (+2 reach, both upper tendrils, pierce) and the charged-jump pose |
| `t45.js` | v2.45: Pearlman, the gems (finder, display, kin), the fusion, the Ethereal shrine and status |
| `t46.js` | v2.46: Pearlman visits like a wandering trader - one roll a day, 10% rising by 10 to 30%, reset when he comes |
| `t47.js` | v2.47: carrying the Ethereal Gem anywhere in your inventory: a shimmer of the nine follows you |
| `t48.js` | v2.48: the Hollow Gate - set up, five Emblem sockets, opens, only 5-conquest players pass, way home, take back, pack up; |
| `t49.js` | v2.49: Shifting arms, followers vanish on death, Tendril modes (toggle / ranged auto-lash / offense grab), Pearlman's trades stay open |
| `t49b.js` | v2.49: Pearlman's trade window stays open while he turns to face you |
| `t50.js` | first check: Blood Moon foe near a placed Ethereal Gem: slowed, weakened, slowly burned **(summons by function, so the 3-second item rule sends followers home)** |
| `t51.js` | first check: Donado gets his jointed rig (8 parts riding him, the old body gone) **(summons by function, so the 3-second item rule sends followers home)** |
| `t52.js` | first check: Both placed (a marker each) |
| `t53.js` | first check: A receiver touching a transmitter is refused (it would latch on) |
| `t54.js` | first check: Cecil summoned with his own (poison) look **(summons by function, so the 3-second item rule sends followers home)** |
| `t55.js` | first check: Summoned in Healing: rose dress **(summons by function, so the 3-second item rule sends followers home)** |
| `t56.js` | first check: Stars home in on the player (levitation from a hit) |
| `t56b.js` | first check: Stars home in on the player (levitation from a hit) |
| `t57.js` | first check: Each rat learns its variant |
| `t58.js` | first check: Encounter: Celi stands there (9 rig parts + her hitbox) |
| `t59.js` | first check: Cecil comes in his new (shorter, slimmer) look **(summons by function, so the 3-second item rule sends followers home)** |
| `t60.js` | first check: Invite: PartyPal gets an [Accept] invite |
| `t61.js` | - |
| `t62.js` | first check: Market Cecil wears the new model (5 parts incl. the free arm, old body gone) |
| `t63.js` | first check: Hang Cecil's gem in a frame: an anchor appears, and Cecil comes out |
| `t64.js` | first check: In the vault: adventure mode |
| `t65.js` | first check: Cecil has five parts now (his free arm is its own), all on the new rig |
| `t65c.js` | v2.65 content: the new rooms and events, secrets, rare foes, the heist items, the layout's connectivity **(partly stale: the raid flow it drives was reworked; t100 onward cover it as a regular player)** |
| `t65k.js` | v2.65: kit abilities, hirelings, the Endless Vault, the Pit |
| `t65m.js` | v2.65: who guards each tier, the tier guardians, the music, the themed stone |
| `t65o.js` | v2.65: the 2.60 rooms still work in their new tiers (levers, plates, guards at I; tiles, lasers, dial at III), on a bench **(partly stale: the raid flow it drives was reworked; t100 onward cover it as a regular player)** |
| `t65r.js` | v2.65 raid core: tries + fee + lucky pool, respawn in the den (and back), fail-reset, the pot, passages, dial button, one-time rewards, bond **(partly stale: the raid flow it drives was reworked; t100 onward cover it as a regular player)** |
| `t66.js` | first check: The Heist Plans: pick tier V - you're led down into the vault **(partly stale: the raid flow it drives was reworked; t100 onward cover it as a regular player)** |
| `t67.js` | first check: The full Gilded set: no fall damage (fall damage x0) **(partly stale: the raid flow it drives was reworked; t100 onward cover it as a regular player)** |
| `t68.js` | first check: A party member (not the leader) can't plan the heist **(partly stale: the raid flow it drives was reworked; t100 onward cover it as a regular player)** |
| `t72.js` | first check: Display case: use it looking at the floor - a floor case stands there (case, contents, hitbox) **(partly stale: the raid flow it drives was reworked; t100 onward cover it as a regular player)** |
| `t73.js` | first check: A bottled cow goes in a floor case: she appears on the cushion |
| `t74.js` | first check: …: ladders all the way up (… rows) |
| `t78.js` | v2.65: follower cosmetics - Emma's ribbons and dresses, Celi's outfits, Zib's uniforms; Velour's stock; the hidden ones |
| `t79.js` | v2.65: KillerWatt - the Storm Effigy, the boss (rig, animation, attacks, roar, reward), the Spark follower, Cecil's shop **(partly stale: using the Spark while he's out opens his menu since 2.78, rather than calling him over)** |
| `t79b.js` | v2.66: KillerWatt the follower - riding, wall climbing, the Thunder Leap, the tendril stab, the leap, chain lightning, gems and the Ethereal Form |
| `t80.js` | v2.66: the Fixer's Office - the Gutter Bank, spoils, kit ranks, secondaries and signatures; metal trophies; the Bond Sigils **(partly stale: the Gutter Bank became a page per currency in 2.80a (t175))** |
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
| `t120.js` | 2.74: checkpoint respawn + kept pockets, kit 32/4, Lights Out / Glass Cannon only out on the heist, den names + carpet, **(partly stale: its Gutter Bank steps predate the page-per-currency bank of 2.80a; t175 covers it)** |
| `t121.js` | 2.74: the Fixer's Lounge - held still into it, every counter working there, its door home; the end-of-heist Go to the Lounge pressed (2.79: the real trigger, not a direct call); Leo's size |
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
|  | 2.77c: every courtier rises in open air; his defeat - the roar and the screen shake (the bot's view jolted, counted |
|  | from its rotation packets), the black fire, the burst, the seal opening and closing, the crown drifting down and landing |
|  | for the bot alone (glowing, never despawning) - walked to and picked up; nothing left behind; his rig never doubled |
|  | (sampled through the whole fight) and the win counted once. |
| `t135.js` | 2.77: Tullius (regular player, real packets): the ghost ship found by `locate` and built by its seed, swum to and climbed |
|  | aboard by its ladder; "Tullius needs Leo" (no captain alone - the hint - then Leo's crest on deck); the fight (harpoon |
|  | hook + point-blank, crew, frost, put overboard he leaps back aboard), drops, the setting off; his blunderbuss and harpoon |
|  | in the bot's hands; the Doubloon follower (sit, menu, harpoon pull, swimming, buffs at sea, faint, contract). |
|  | Sections: `ship`, `weapons`, `pet`. |
| `t136.js` | 2.77: the new pairs and trios, every follower called with its own item: Frost and Brine, Old Rivals, the Tidewatch (and |
|  | at sea), Forgiven, Venom and Volts, An Uneasy Truce, the Dread Court, the hidden Royal Retinue - and Pearlman as a fourth |
|  | never displacing the Serpent's Bane (2.77c: Pearlman counts toward the three - refused as a fourth, and with him out, |
|  | Cecil is). Sections: `tul`, `apo`, `retinue`. |
| `t137.js` | 2.77b: the Wraithfire Heart forged on the ground - an Ethereal Gem and a Scorching Heart set down with the items |
|  | themselves (both orders): the forging starts, both rise, circle closer, merge; the bot picks the heart up, Burning Blue; |
|  | nothing left behind; six blocks apart nothing happens; Pearlman no longer offers the fusion. |
| `t138.js` | 2.77b: follower figurines - a case set down with the case item, every follower's item right-clicked in (all fourteen - 2.78a: the Frog, Donado, Wilfrey; 2.79: Fishy), |
|  | punch for the item and back, sneak + right-click turns it, empty-handed out; a wall case (Apophiss's Oath), picked up. |
| `t139.js` | 2.77c: Apophiss's True Crown - worn with a use (swapping with the helmet), its stats measured against the shadow-crown |
|  | and the heaviest chestplate, its passives (wither/poison gone, fire-proof, water-breathing, night sight, Regeneration when |
|  | badly hurt, monsters weakened, Strength II at night), sneak + a real jump for five lines of fangs, the Wrath near death |
|  | (once, then 2 minutes), set atop a block (its name kept; it turns), refused to another player (a second bot), taken back |
|  | with sneak + punch, dropped when its block breaks. |
| `t140.js` | 2.77c: weapons on the wall - the blunderbuss, harpoon, scythe and both tendril sets hung with sneak + use on all four |
|  | walls (plaque, facing, name kept), taken down with sneak + punch (a plain punch doesn't), a broken wall drops one; the |
|  | blunderbuss with a monster close fires instead; the scythe's plain use says how; the tendrils' use still puts them on. |
| `t141.js` | 2.77d: the Emma doll Cecil sells - bought with trophies in a real trade (his window, the doll's trade picked, |
|  | shift-clicked out; his price read from his offers), set down with the doll itself looking at the floor, right-clicked to |
|  | twirl (a third of a turn), her charm curing poison but not resistance, a plain punch leaving her, sneak + punch taking her up. |
| `t142.js` | 2.78: the Frog with Mustache and Donado carry a token like every follower - the Frog hired (his Signet; again, no |
|  | charge), armed, sent home and called back from its menu, fainting (the Signet rests, nothing dropped), his gear handed |
|  | back; Donado freed from a pen (his Collar Tag, counted in the three-follower limit); both tokens in a case and a frame. |
| `t143.js` | 2.78: the Key of New Beginnings - bought from the Fence, its dialog ("No" changes nothing, "Yes" clears the record); |
|  | what was earned stays (the Warpstone, the Hollow asleep mid-climb, Wilfrey's locket, no second Warpstone); it won't turn |
|  | on a clear record or beside an awake boss; a pre-2.78 reset rebuilt from the Warpstone carried. |
| `t144.js` | 2.78: "never used up" items aren't - the Tome of Blinking (7 blocks, stays in hand), a Jackpot card (the next card, one |
|  | play fewer), a lucky map piece (stays; the ninth makes the map with none left over). |
| `t145.js` | 2.78: the Recruiter only deals in names you know - into the Lounge with the Ledger, a click on him opens his book: no |
|  | follower before you've met one (and no free Cecil); Celi met, her contract bought from the wallet ("IN YOUR PACK"), used |
|  | and "SIGNED"; an unmet follower's contract refused and kept; a hireling and a vault gem bought from their pages. |
| `t146.js` | 2.78: every follower in a frame - Zib's medal, KillerWatt's spark, Pearlman's card (2.78a: Wilfrey's locket, his bones too; 2.79: Fishy's Pocket Bowl) each hung in an item frame |
|  | with a right-click: the follower climbs out (nobody's), still there ten seconds on, gone with the item punched out. |
| `t147.js` | 2.78: Wilfrey counts toward the three-follower limit - the locket refused with three out, answered once one goes |
| `t148.js` | 2.78: wardrobes for the rest + auras + the tidied Office - Tullius's coat (away, then worn, arm re-dressed after poses, put back), his aura (locked, used, switched off), Pearlman's bow tie, Wilfrey's shield, the Office order and even widths, Raid Crew -> Outfits -> Pearlman |
| `t149.js` | 2.78: Apophiss slithers - phase 1, jump strength 0 and step height 2: no hop between attacks, and he climbs a 2-high ledge after the bot (the old settings' run is logged for comparison; it never hopped here) |
| `t150.js` | 2.78: the end-of-heist Go to the Lounge keeps your overworld gear at the coat check; the Lounge's door hands it back, once |
| `t151.js` | 2.78: Apophiss's phase II can't be skipped - the bot's blows take him under half: he transforms at once, health held at half, twice over (a rematch); the den's dome whole over its chains |
| `t152.js` | 2.78: Cecil, Emma and Leo called in the Serpent's Den by a player who never beat the Hollow King - no conquest asked |
| `t153.js` | 2.78: bosses don't sit frozen - Tullius leaves when his lone fighter dies, or when his chunk reloads a minute later; Apophiss leaves on a lone death in his den |
| `t154.js` | 2.78: the Wings of the Damned flown with the real keys - crouch then jump: a Levitation burst skyward, cut off after a few ticks; a plain jump does nothing; gliding with sneak held: pushed on every tick, without: left be |
| `t155.js` | 2.78: more weapons on the wall by sneak + drop (Q) - Cecil's staff, Leo's trident (his own model, both forms), Apophiss's mace, the Frisbee Shield, a ray gun, the Sepulchre; a plain drop or no wall just drops; sneak + punch takes one down |
| `t156.js` | 2.78: a doll of every follower (2.78a: twelve, the Frog, Donado and Wilfrey too; 2.79: thirteen, Fishy) - Cecil sells them; each set down on a block by a real use, its own model, twirls when right-clicked, back into the pack with sneak + punch |
| `t157.js` | 2.78: Captain Tullius makes an entrance - his title card on the player's screen, a ring of his colours that sweeps in and goes, the light dipping. (2.80: the six roaming bosses stage their own arrivals - t168) |
| `t158.js` | 2.78: Apophiss and Tullius on the Recruiter's book - not before you've met them; met (their Oath / coin in your pocket), their contracts priced in coins, bought from the book, used, and "SIGNED" |
| `t159.js` | 2.78a: Apophiss's forms - the Ethereal Gem given by a right-click on him (ethereal scales, wings out and posed), the Wraithfire Heart (soul-blue scales and wings, fire-proof; the gem handed back), a colour picked meanwhile kept under the form, sneak + right-click empty-handed takes the heart back (his scales, wings away) |
| `t161.js` | 2.78c: ridden Apophiss flies in his forms - saddle, Ethereal Gem and Oath by real clicks, then riding as a client does: look up and walk to climb, level to glide, jump for a wingbeat, down to dive; off, his weight back; his click box with him far from take-off; the gem taken back - he only slithers |
| `t160.js` | 2.78b: Emma with a Wraithfire Heart blesses at level II - her Offense form gives Strength I; the heart given by a right-click, her Wraithfire Form switched off in her menu (she keeps it): Strength II; the heart taken back: Strength I again |
| `t162.js` | 2.79: Fishy's Cabinet of Curiosities - (2.80) a Black Market placed fresh builds his hall itself (twenty cases, Fishy at his desk; the old Lounge hall gone); Fishy at his desk, right-clicked empty-handed: he joins you (his Pocket Bowl); again: the Cabinet's menu, a wing's page (twenty veiled exhibits with riddles), set out in the hall; a rare thing shown to him: recorded world-wide with your name, announced, its case and plaque in the hall - and the thing itself kept; shown twice: "already"; an ordinary thing: not for the cabinet; a lost bowl reissued; shown to your own Fishy out in the world. As an admin, a wing filled: its rosette and advancement to who gave to it (set up and taken back by sneak + use / sneak + punch), his power learned on the powers page, his claws wither a husk |
| `t163.js` | 2.79: Fishy, the owner's follower checklist - called with his bowl (nine-part rig; a poor fighter: 30 health, 1-point claw); his menu (Sit / follow, Send him home, The Cabinet, Fishy's powers, Wardrobe); sat from the menu and by a right-click (state 4, sit/sit_b), up again; a top hat used while he's out (worn, kept across send-home and Call, put back); his aura (locked row, used, on, off); his Raid Contract signed; the bowl in an item frame (he climbs out, stays, goes when punched out); his display-case figurine (nine parts, inside the glass); Cecil's doll bought in a real trade, set down, twirled, picked up; struck down: he faints, five minutes on the bowl. As an admin, every wing filled: the Golden Bowl - gilded limbs, 130 health, armour 10, the Grand Exhibition on a foe (replicas, then gone) |
| `t164.js` | 2.79: the Portrait of Two - bought from the Fence in a real trade (his window, its trade picked, taken out), a painting that carries its picture; used on a wall (a block-face click): it hangs the portrait, 5 x 4; punched down: it comes back as the portrait, not a random painting. The mob roll's manners: twenty named zombies and twenty frozen (NoAI) ones seen and never renamed; two hundred plain ones - some still rolled |
| `t165.js` | 2.79a: Gilded - the Lounge Tailor's Leo page shows the Golden Champion at 2,560 coins; pressed: in his wardrobe for good, 2,560 coins out of the bank (3000 -> 440); Donado's page lists his new Gilded coat at the same price; the item's lore (polished gold, the Tailor's dearest). Leo called, the outfit used: worn (c4 tabard), and gold motes reach the client round him (decoded from the raw particle packets); his own clothes: none. Wilfrey in the Gilded Sun: the sun shield with a glint, a golden chestplate (asset gold) where he wore none; the Crimson Cross: his own gear and a red shield. Donado called (rigged) in his Gilded coat: torso and head `_c5`, his eyes his own; back in his own coat: plain parts |
| `t166.js` | 2.79b: calling the bosses, as a player - the Horseman's Lantern by day (he comes, called, and stays in daylight; a second Lantern refused and kept), the Smouldering Idol refused in the Overworld and the Elder Acorn under a roof (both kept); the Pharaoh's Scarab by night (he stays; uncalled, he sinks back at once); the Thunderhead Feather in clear weather (the Roc outlasts the 10 s of clear sky); the Elder Acorn by day; the Smouldering Gourd on an ordinary day (the Arachno-Lantern grows and stays; uncalled, it leaves); the Idol in the Nether and the Eye in the End. The haul's rolls sampled (Tier V Blood Moon: summons and gourds; Tier II: neither; Tier V ordinary night: no gourds) and the vault's rare stores (Tier V: diamonds, scrap, templates among the gear; Tier II: none) |
| `t167.js` | 2.79c: the Hex Cathedral's witch spawner (it was built under a pew row and never existed) - a Hex dungeon placed with `place structure`: the witch spawner among the pews (`bm:hex/witches`, its ominous twin) and the vindicator spawner; walking up as a regular player, witches come (dungeon mobs); an old dungeon without it: the 2.79c patch puts it back once a player is near, and only once |
| `t168.js` | 2.80: the roaming bosses staged - each of the six called with its own item: it arrives frozen in its own way (the Horseman's steed galloping in from far off, the Pharaoh and Treant out of the ground and growing, the Roc out of the sky, the Colossus out of the floor, the Voidwalker out of a rift), its title card and song, released and armed with its bar true; a second player near grows its health half again (bar and buffer right) and back; the Colossus's slam and the Pharaoh's sandblast wind up first; its rage freezes it for a moment; the player's blow starts its death (frozen, bar gone, still there two seconds on) and it falls as the player's kill (its relic); the Horseman's head falls and his steed goes; the Treant leaves a sapling; the Colossus still bursts into Magma Spawn, awake and visible |
| `t169.js` | 2.80: a dungeon boss staged - the Broodmother in a placed Brood Nest, woken at the altar with her key: she materialises (frozen, small, growing), then moves, armed, her bar true; her web spit winds up before the web lands; her rage is a moment; the player's blow starts her death (frozen, curling up, bar gone) and she falls - "has fallen" on screen, her loot, no marker left |
| `t170.js` | 2.80: the heist's climax - a Tier V heist: the treasury dressed (chandeliers in the tier's lanterns, candles, sconces, hidden lights, gems; the ring and the way clear); a heist room dressed in its own look (the Lever Room's copper frieze, ceiling lights and pipes, nothing below the trim touched); walking in, the guardian rises (frozen, below the floor, shrunk, the hall dark), its title card, then it stands free at full size; its fall parts the great door from the middle out, then all open, "The vault is open", the way out swirls, the sequence over; the heist's music hushes as the door parts and the vault's fanfare plays on the jukebox channel, then the heist's music comes back |
| `t171.js` | 2.80: boss themes - as a regular player, the Horseman called with his summon item starts THE WILD HUNT (jukebox channel, not his old vanilla record; the vanilla soundtrack stopped while it plays); a step back (80 blocks) keeps it, 130 stops it, coming back restarts it; its minute up, it plays again; the Pharaoh called too: SANDS OF THE DEAD takes over; the Pharaoh's death (the player's blow) hands back to the Hunt; the Horseman's death silences it at once, nothing plays while he dies |
| `t172.js` | 2.80: menus as regular players - the Rat Bank (Banker's Card): the account page lists all 11 currencies with balances; a currency's page (icon, in the account, on you); Deposit all / Take 10 come back to that page; « back; Deposit everything. The Armory: a card per kit, each kit's page lists its ranks (owned ticked, next marked), Rank up buys and returns. The party's members as a dialog (names, health, leader starred; Kick only for the leader, and it kicks). Server settings as an operator's dialog (state on each button, a click flips it; a regular player can't open it) |
| `t173.js` | 2.80: the Fixer's Lounge's coat check, as a regular player - in through the Ledger's "Fixer's Lounge" (hold still): the Fixer keeps the sword and helmet, the Ledger and Tokens come in; the lounge heals (Regeneration II, Saturation refilling a drained food bar); out through its door: home where you stood, gear handed back; a death inside: gear back at home, nothing left with the Fixer; a heist planned from the lounge (Plan a Heist > Tier I > 3 tries): the fee paid, what was picked up inside set aside, the way home and respawn point are the spot you came from; left from the Ledger (Leave the heist > Leave now): home, sword, helmet and the lounge's diamonds back, respawn point your own |
| `t174.js` | 2.80: Apophiss revised (`node t174.js [boss|mace|crown]`) - the boss: 1024 health, attack 12, armour 18; his Judgement stood in (16 through full Regalia and Resistance) and sprinted out of (nothing). The Mace: Wind Burst III; F to the next form, sneak + F back, all seven round; the pickaxe's Haste II; the sword's poison, the shovel's lift, the hoe's heal (with the Wither); the Wrath used (a husk struck, its 12 s cooldown) and again too soon. The True Crown worn with a use: Protection X, Thorns III, Respiration V; with three Regalia pieces the set wakes; Apophiss called with his Oath: Resistance II and Regeneration II from the Crown, Strength II from the Mace |
| `t175.js` | 2.80a: the Gutter Bank a page per currency, as a regular player - every currency on its own button with its balance; Copper Cogs taken and deposited 1, 10 and all; coins taken loose only (no Medallion broken); a Medallion out and back; Deposit everything; a stale action button moves nothing |
| `t176.js` | 2.80a: the coat check, airtight - the Locker Hall's door checks your gear and its plate hands it back; a death in the hall, then a Pearl of Return refused (and refunded); a stray put in a heist's den seen out, home, with their gear; a stray in the Lounge checked on the spot; a stale bag at the heist's door (what you carry joins it); enchanted heist boots kept at the Lounge's door |
| `t177.js` | 2.80b: the special nights, as a regular player (rcon only picks the night and moves the clock on) - the Blood Moon rises (title, word, bar), refuses an Invasion that day, won't let a bed sleep it away, sets at dawn; a Lucky Night starts, a Leprechaun Rat caught drops a Pot of Gold, picked up and tipped out for Tokens, dawn ends it; an Invasion Night starts, the Vorn land near you, and at dawn every one lifts away - troopers, saucers and the bioengineered beasts |
| `t178.js` | 2.80b: Cecil's dolls wait until you've met their follower - a player who has met no one finds all thirteen wrapped (out of stock, a pick buys nothing); holding KillerWatt's Spark unwraps his doll in its own slot and it's bought for real; a second player at the counter doesn't change the list until the first walks off, then sees their own; no one there, all wrapped |
|  | home (from her menu), and with Wilfrey out a fourth follower refused. |
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

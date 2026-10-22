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

## Chunks: every test leaves them as it found them (the standard)

A test may force-load whatever it needs - `R.run('forceload add ...')`, in any dimension - and never has to remove
it: `chunks.js`, which both rcon helpers (`lib.js`, `lib_resp.js`) send every command through, does it for every test.
- Before each `forceload add` it asks the server what that dimension already holds; afterwards it remembers only the
  chunks the test itself added. When the process exits - finished, crashed, a failed check, Ctrl+C or a sweep's
  timeout (SIGTERM) - exactly those are released (`rc.js` runs the `forceload remove`s). Only SIGKILL skips it.
- A chunk the pack holds is never released, even when a test asks for it again: the gutter's den, Lounge and Locker
  Hall chunks (force-loaded for good by `bm:load` - t101 loads the den's own chunk), a raid instance's claimed slot,
  the Hollow while it's being built. (A forceload has no owner count: removing one the pack holds unloads it for the
  pack too, until the next `/reload`.)
- The pack never force-loads the Overworld, the Nether or the End, so after a test or a sweep `node chunkcheck.js`
  should list none there (`--clear` releases anything a SIGKILLed test left). The pack's own gutter and Hollow
  chunks are listed for information only.
- So: no `forceload remove` boilerplate in new tests, and no `forceload remove all` anywhere.

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
- A mob's head is its own rotation: `rotate` turns only the body of a mob with no AI, and its head stays put. Setting its
  saved `Rotation` reloads it and turns both. The client is sent `entity_head_rotation` packets; listen for them to check (t184).
- Mining is `A.mine(x, y, z, ms)`. 26.3 numbers the dig actions 0 start, 1 change direction, 2 abort, 3 stop; sending the
  old "2" to finish gives the block up. A block that breaks in one tick needs only the start. Set ores on top of the floor,
  not in it: a mined floor block drops its loot into the hole (or the void), out of the bot's reach (t183).
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
- Dropping an item: 26.3's `block_dig` statuses are 5 (drop one, Q) and 4 (drop the stack, ctrl+Q); 6 is release-use and 7
  swap hands. lib_resp's `A.drop(stack)` sends the right one (t180).
- A heist tag left on a bot (an rcon tp out of a heist) made followers and Bond Sigils treat it as still raiding. The pack
  now counts anyone out of the gutter 30 s as off the heist (2.80d), and t120 sends its raider home at the end.
- One RCON reply holds about 4 KB: a trader's whole `Offers` list is cut short. Read it one recipe at a time (t25, t32).
- Count by area, not world-wide: other tests leave their own markers, boards and slot machines behind (t25, t32).
- 2.80: a roaming boss stages its arrival (about 5 s, untouchable, health buffered) and its death (about 5 s). Wait both
  out before checking it (t33, t34, t35).
- A mob summoned without `bm.seen` gets the pack's tiering on its next tick (an Elite, more health). Tag test mobs
  `bm.seen` when their health matters.

- Gear carried through a coat-check door (the Lounge's, a heist's) comes back a moment later, wherever it lands - not
  always in the slot it left. Wait for the item, then select its own slot before using it (t131's `holdLedger`).
- A boss's arrival buffer stays on its health: `bm.cbuf` (up to +1000) sits on top of the real health, and `bm.cmx` holds
  the real maximum. Set a boss's health as N + cbuf, read its max from cmx, and wait out `bm.cfrz` (an enrage's frozen,
  untouchable moment) before the killing blow (t33, t34, t56's `cbuf`).
- Cecil's dolls for followers not yet met are wrapped (2.80b), and a wrapped doll has no `bm` id. When scanning a trader's
  list, stop at the end of the list (`Offers.Recipes[i]` missing), not at the first recipe without the field (t163).
- The rcon connection answers one command at a time: never send several at once (`Promise.all` over `run`) - the replies
  get crossed and the test hangs. Loop and `await` each one.
- A spot picked by fixed offsets can land in the world's own terrain: the ghost ship can lie beside an iceberg, so t135
  checks for open water before putting Tullius overboard, and watches for him from the moment he lands (he can be back
  aboard within a second and a half).
- A Lucky Night (or an Invasion) is never set on a Blood Moon day: move on to a morning that isn't one first (t177's
  `morning`, t125).
- rcon cuts a long reply short (about 4 KB): a whole item with its components - a Haul with five stacks inside - comes back
  truncated, and what you were looking for may be past the cut. Ask for the one path you need (`...container[{item:{id:
  "minecraft:diamond_sword"}}].item.id`, `...lore[1].text`), as t191 does.
- A Haul (or Haul Crate) set down is found by looking along the player's line of sight from the eyes: place it where the
  bot is looking (t191 looks 45° down and places one block ahead), or it opens nothing and no marker minds it.
- `bm.gvr_lobby,limit=1` finds the first lobby on the server, not your heist's: after a test that left a second instance
  open, a test staging that way (t86) works on the wrong heist. Address your own (`scores={bm.gvi=N}`), or run it alone.
- 2.81: a market marker without `bm.m281` is an OLD market - the first time a player comes within 200 blocks it is rebuilt
  as the new town, right there (t32 and t39 once grew a whole town around their stand-in markers this way). A stand-in
  market marker carries the town tag, `market3.TOWN_TAG` (`bm.m281a` since 2.81a), and the done-tags of every install it
  shouldn't run. Every market install waits for that tag, so an untagged stand-in gets none of them. Bumping the tag
  rebuilds every town once more (2.81a did, for the counters).
- The traders aren't all villagers: the Fence is a wandering trader. Find a trader by its own `bm.npc_<name>` tag, not
  by `type=villager` (t194's counter-book step).
- `/place template` with a turn still wants the UNturned box from its origin loaded (pos to pos + size): load both (t194,
  phase168).
- `forceload remove` isn't counted per owner: it unloads a chunk even when something else force-loaded it too. The
  rebuild's own remove can take a test's chunks with it - a manual check afterwards may find markers "gone" (unloaded).
  `node chunkcheck.js` after manual pokes; `forceload remove` what's left.
- A test fixture structure: write it into the server's copy of the pack (`world/datapacks/BlackMarket_DP/data/bm/structure/`)
  and `/reload` - `world/generated/bm/structure(s)` isn't read. `dev.sh` puts a clean pack back.
- Natural markets generate near test spots (304,288 / 5472,5376 / 34000,34144 ...): `locate structure bm:black_market`
  from a spot before using it; t194 stands 555 blocks off the nearest. The void (`bm:gutter`) won't do: it sends away
  anyone not on a heist.
- A keyless player on a market floor is sent back to the vestibule (`market/kick`) - give the Market Key to a bot that's
  meant to be inside (t194). Back rooms are registry dialogs (the client gets `{"dialog": n}`, not text); the Bounty
  Board answers on the action bar (`A.bars`).
- A stand-in follower must be a real one or a plain animal: a wolf tagged `bm.cecilpet` with no owner and no `bm.pid` set
  Cecil's rig respawning (t194 uses a tamed wolf owned by the bot). Likewise a bare `bm.kxboss` husk (no `bm.kxid`) used to
  rig itself twice a tick - thousands of displays, a 60 s watchdog stop; 2.81 gives such a KillerWatt an id first.

- **Hard mode on the test server.** TestRat has beaten the Hollow King, so hard mode would wake by itself: the server keeps it off with `#hardoff bm.cfg 1`. A test that needs it sets `#hard bm.cfg 1` (t224) or `#hardoff 0` (t223, to see it wake) and puts it back at the end.
- **The market bounces a survival player without a Black Market Key** (`bm.haskey`) to the exit. A test that clears the inventory in town gives the key back first (t224 keeps it in hotbar.8).

## Index

The newest tests (t128 onward, especially t131-t133) follow the owner's rule throughout. Older ones lean on rcon
and function calls. The ones known to be stale (wholly or in part) are marked.

| Script | What it covers |
|---|---|
| `t5lay.js` | - |
| `t23.js` | first check: mailbox model on its hitbox (2.80d: trimmed to what still holds) |
| `t23b.js` | - |
| `t23c.js` | - |
| `t24i.js` | first check: sparks: first target and chain hit, far one spared |
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
| `t34.js` | v2.33: the Heartwood Branch, Molten Gauntlet and Void Scepter (all forms, catalysts); the Elder Treant, Magma Colossus and |
| `t35.js` | v2.34: every roaming boss always drops its relic to a player's kill (3 kills each; 2.80: after its arrival, and its staged death) |
| `t36.js` | v2.35: sockets by material (vanilla only), red Vitality + size cycle, combos (incl. Bloodlust, Second Wind), Masterworks, |
| `t37.js` | v2.35: sockets by material (vanilla only), red Vitality + size cycle, combos (incl. Bloodlust, Second Wind), Masterworks, |
| `t38.js` | v2.35: the chestplate essences/resonances against a real attacker (a husk with AI: the damage command never triggers on-hit enchantments) |
| `t39.js` | v2.36 fixes: trades stay open (no re-teleport), nameplates follow, Cecil's spawn on a step, admin/blood_moon |
| `t39b.js` | - |
| `t42.js` | v2.40: KillerWatt's Tendrils, Apophiss's Crown, Leo's Trident, Cecil's Staff (2.80d: trimmed to what still holds) |
| `t42b.js` | - |
| `t43.js` | v2.42: two-blade tendrils + lunge; v2.41: tendrils worn on the chest (4 at the back, look-to-lash, sneak+jump fling, weather; 2.82: they no longer pull items in), crown at nig... (2.80d: trimmed to what still holds) |
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
| `t59.js` | Cecil's model: his shorter, slimmer look and the hood's height (summoned by function with his gem carried; fainting moved to t219) |
| `t60.js` | first check: Invite: PartyPal gets an [Accept] invite |
| `t61.js` | - |
| `t62.js` | first check: Market Cecil wears the new model (5 parts incl. the free arm, old body gone) |
| `t63.js` | first check: Hang Cecil's gem in a frame: an anchor appears, and Cecil comes out |
| `t64.js` | first check: In the vault: adventure mode |
| `t65.js` | first check: Cecil has five parts now (his free arm is its own), all on the new rig |
| `t65k.js` | v2.65: kit abilities, hirelings, the Endless Vault, the Pit |
| `t65m.js` | v2.65: who guards each tier, the tier guardians, the music, the themed stone |
| `t65o.js` | v2.65: the 2.60 rooms still work in their new tiers (levers, plates, guards at I; tiles, lasers, dial at III), on a bench |
| `t67.js` | first check: The full Gilded set: no fall damage (fall damage x0) (2.80d: trimmed to what still holds) |
| `t72.js` | first check: Display case: use it looking at the floor - a floor case stands there (case, contents, hitbox) (2.80d: trimmed to what still holds) |
| `t73.js` | first check: A bottled cow goes in a floor case: she appears on the cushion |
| `t74.js` | first check: …: ladders all the way up (… rows) |
| `t78.js` | v2.65: follower cosmetics - Emma's ribbons and dresses, Celi's outfits, Zib's uniforms; the Tailor's stock (raid exclusives, none at Velour's - 2.82); the hidden ones |
| `t79.js` | v2.65: KillerWatt - the Storm Effigy, the boss (rig, animation, attacks, roar, reward), the Spark follower, Cecil's shop **(partly stale: using the Spark while he's out opens his menu since 2.78, rather than calling him over)** |
| `t79b.js` | v2.66: KillerWatt the follower - riding, wall climbing, the Thunder Leap, the tendril stab, the leap, chain lightning, gems and the Ethereal Form (2.80d: trimmed to what still holds) |
| `t80.js` | v2.66: the Fixer's Office - the Gutter Bank, spoils, kit ranks, secondaries and signatures; metal trophies; the Bond Sigils (2.80d: trimmed to what still holds) |
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
| `t106.js` | v2.67d: the Ledger's Locker Hall trip - from safe ground in the Overworld, the Nether or the End (not the Hollow or the gutter; (2.83b: trimmed to the 2.82o rule - the Hollow and boss dungeons start the hold too.) |
| `t107.js` | v2.68: the vault's loose ends - the tile floor's sides, crew changes rescale the guards, leave from the Ledger, a dropped |
| `t108.js` | v2.68: currency wins, the Crate Desk, tip-offs, laurels + achievements, Forgeheart, the Alibi, the Counterfeiter's Press |
| `t109.js` | 2.68 follow-ups: Locker Key in the gutter only, Office leave button, Boomer filing, den NPC dedupe, door in the doorway, |
| `t110.js` | 2.69 (I): the Combination Room, the Weighing Room, the Gauntlet and the Tile Floor in their B and C variants; the tile seam |
| `t111.js` | 2.69 (II): the Dial Lock, the Three Coffers, the Signal Lamps, the Lamp Floor, the Tumbler Lock, the Bell Tower and the |
| `t112.js` | 2.69 new rooms: the Sky Isles, the Spire, the Tinker's Bench, the Mason's Plan, the Dig; Block Party, Red Light Green Light, Memory Match |
| `t113.js` | 2.70: the throne rooms (gold, diamond, netherite - and their odds) and Prime fights |
| `t114.js` | 2.71: the B and C versions of the Spire, the Tinker's Bench, the Mason's Plan and the Dig (2.82b: the Mosaic is retired - the Mason's Plan steps cover its other variant. 2.83a: in the Sculptor Dig, the bot climbs the step-up beside the calcite cube and chisels its top-middle block from the ledge.) |
| `t115a.js` | 2.72 (I): the Library (2.82: three shelves of twelve, all in reach without a jump), the Pipes, the Apothecary, the Grapple, the Minecart Run - three ways each |
| `t115b.js` | 2.72 (II): room curses, forks in the road, corridor traps |
| `t115c.js` | 2.72 (III): Smelling Salts, the Thief's Hourglass, the Alarm Jammer, Masterworks, the Codex, each tier's own finds |
| `t118.js` | 2.73: a raid boss's minions fall with it |
| `t120.js` | 2.74: checkpoint respawn + kept pockets, kit 32/4, Lights Out / Glass Cannon only out on the heist, den names + carpet, (2.80d: trimmed to what still holds) |
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
| `t136.js` | 2.77: the new pairs and trios, every follower called with its own item: Frost and Brine, Old Rivals, the Tidewatch (and 2.82 (`node t136.js om`): Apophiss + Omega (The Serpent Kings: their words, Strength and Resistance, Resistance II on both, their bickering) and Apophiss + Pistachio + Cecil (The Palace Household: Speed, Regeneration, supper from the palace kitchen) |
|  | at sea), Forgiven, Venom and Volts, An Uneasy Truce, the Dread Court, the hidden Royal Retinue - and Pearlman as a fourth |
|  | never displacing the Serpent's Bane (2.77c: Pearlman counts toward the three - refused as a fourth, and with him out, |
|  | Cecil is). Sections: `tul`, `apo`, `retinue`. |
|  | 2.80d (`node t136.js dw`): Spade and Spoon (Dennis + Pistachio: Haste II, Luck), the Omega Palace (Cecil + Pistachio: Regeneration, Pistachio's supper), the Crown's Prospect (Emma, Leo and Dennis). |
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
| `t179.js` | 2.80c: the diamond and netherite looks - Tullius's Diamond Captain used (his rig wears it), his wardrobe (Netherite locked, where to find it), the Netherite Captain bought at the Tailor through his dialog (6,144 coins, OWNED) and worn; Leo's diamond helm; Wilfrey's Netherite Sun shield and netherite armour |
| `t180.js` | 2.80d: the ground forges, as a regular player - ingredients tossed with Q (ctrl+Q for a stack): the Huntmaster's Relic (the Overworld roaming bosses' weapons, F to turn, a catalyst), the Riftbound Relic, the Starheart (by night under the sky; eaten: +1 heart), the Talisman of the Three Nights (Luck II on a Lucky Night); a forge that loses a piece goes cold. 2.80e: the hint lines on every ingredient, the Newcomers' Book's GROUND FORGES pages, and each forge's advancement on pickup |
| `t181.js` | 2.80d: the Trophy Stand, as a regular player - set down with a use, opened and folded with right-clicks (bosses on the top step, heist rooms in their best metal, laurels in front, the plaque's counts), folds itself when walked away from, picked up with sneak + punch; Madame Velour sells it |
|  | home (from her menu), and with Wilfrey out a fourth follower refused. |
| `t182.js` | 2.80d: Dennis and Pistachio, the traders, as a regular player - a market placed fresh digs out their rooms; right-clicked, each one's page (the record, the favour, a button per lot with today's count); coal and rotten flesh by the 32, a diamond for 2, Pistachio's rare parts (a wither skeleton skull: 5 Tokens); the daily limit, a lot short, a new day; favour full - the Prospector's Rune, the Tithe Seal, and earned again; the rune onto a pickaxe in the other hand (not twice), its hundredth block a Token (not past the day's 8, not with a plain pick); the seal onto a sword, a zombie slain a Token; the fiftieth trade - he joins you (his horn, his cloche), a lost horn given again. |
| `t183.js` | 2.80d: Dennis and Pistachio, the followers - the owner's checklist for each (`node t183.js dennis` / `pistachio`; both by default): called with his item, his menu, sat from the menu and by a right-click (his seated cycle), his ways, a look worn and kept across a recall, his aura, his Raid Contract, the frame, the display case, Cecil's doll bought in a real trade; his fighting (his great blow first, ranged, crowd, melee - and what each does for you), Pistachio's Phantom Escape; Fortune V (six diamond ores, a plain pickaxe: far more than six) and Looting V (a zombie dropping more flesh than a zombie can), neither without him; knocked out, he faints. |
| `t184.js` | 2.80d: a Smuggler's Jar in a display case, as a regular player - a pig right-clicked into a floor case (on the cushion, facing out, small enough that the circle it sweeps turning stays inside the glass); sneak + right-click - it turns, and the head-turn packets the client gets follow its body round (no twisted neck); again - it stops; out again; a wolf the same; a pig in a wall case - side-on, fits the shallow case, and doesn't turn there. |
| `t185.js` | 2.80f: no glowing outline on a custom-modelled mob's invisible host, as a regular player - the Xeno Visor (right-click to wear) lights a zombie but not a Vorn trooper's invisible husk; the Cipher Monocle outlines a Mimic's chest model, not its rabbit; an outside glow on a host is put out within a second |
| `t186.js` | 2.80f: Apophiss's Unbound Crown, as a regular player - the pieces' hints; True Crown + Wraithfire Heart + Deathmask tossed with Q forge it, picked up, the Unbound advancement; right-click to wear; by night it is the whole Regalia alone (an iron chestplate stays untrimmed); a real jump then sneak in mid-air: two wingbeats, a third refused, Slow Falling, beats back on landing; soul fire on a fire-immune husk; the Fangs sear a husk 7 blocks ahead; badly hurt: the Wrath and three Void Orbs that fade |
| `t187.js` | 2.80g: the coat check sees the crafting grid and the cursor, as a regular player - a sword parked in the 2x2 grid and ingots held on the cursor during the Ledger's 3-second hold are checked with the rest (closing the inventory inside brings nothing in); the Lounge's door hands them back at home |
| `t188.js` | 2.80g: a straggler out of reach is flushed out, as a regular player - in a Counting House, the last guard sealed in a ceiling pocket is flushed onto the room's floor within 40-odd seconds, glows and the crew is told; killed, the room moves on to its next wave |
| `t189.js` | 2.80g: the heist kit is never lost, as a regular player - the main weapon dropped (Q) over lava is straight back in hand, nothing burns; a kit weapon lying in lava doesn't burn (fireproof); a paperweight can still be put down |
| `t190.js` | 2.80g: the vault's guardian scaled for every crew, as regular players (TestRat + TestMouse, Tier V) - whole health past 1024 (1464 for two), 1024 in the mob and the rest a reserve; the bar opens full; a sword hit and a heavy blow are paid from the reserve and the bar falls by it; the second raider leaves: the whole eases to a crew of one's and what's left keeps its share; under half of the whole, its shell goes up |
| `t191.js` | 2.80h: the prize roll, Haul Crates and the win streak, as a regular player - stepping onto the strongbox ring pays out; THE HAUL (tier, shares, coins), then the Tokens 1.5 s later; the card says HEIST WON, streak one; "Start a new raid" seals the leftovers (a found sword) into one Haul Crate in the pack, labelled with the tier, no loose sword; the next job won: WIN STREAK x2 on screen and card; home ends the streak; the crate set down is a Haul (minded, the sword inside) (2.82b: the prize roll is retired - its steps check it never rolls.) |
| `t192.js` | 2.80h: the Fixer's mercy and the crew bonuses, as regular players (TestRat + TestMouse) - on the last try [Skip this puzzle] asks the mercy (half the pot: 20 of 40, and a share); paid, the room opens, the pot halves, the last try is kept, the crew is told; a second room: spent; won by both on the ring: CREW OF 2 and CLEAN CREW in the prize roll, and the card shows crew +1 share, clean crew +1 Token and the mercy's cost (2.82b: the prize roll is retired - its steps check it never rolls.) |
| `t193.js` | 2.80i: tough mobs, not health sponges, as a regular player at the end of a 30-block runway at night - chase speeds measured (blocks/s, a sprint is 5.6): a Blood Moon horror and a Champion zombie, both on their steeds, a Blood Moon and a Champion spider all under a sprint; a Blood Moon, Champion and Elite creeper at a plain creeper's pace (no boost); an unarmored Champion has no Speed and Resistance I; twelve each of Elites, Champions and horrors - no full Protection sets, bare pieces, light on average |
| `t194.js` | 2.81: THE BLACK MARKET, REBUILT - an old (2.80) market, placed turned a quarter as a fixture with its traders, a player's dog, a dropped diamond and a ladder shaft past the tunnel; the player (Market Key) walks in: rebuilt as the new town - one marker (`bm.m281a`), the player and the diamond moved to the Lookout, the dog kept, the shaft untouched; the new blocks turned like the old market; every trader once, all 16 ledgers (every back-room book on its trader's counter: no lectern, no slab, nothing on top, the trader beside it), Teller, Concierge, Auctioneer, Fishy's Cabinet, Dennis's and Pistachio's rooms, 3 slots, board, lectern, Scrap Bin, lift button, 7 ambience emitters, nothing old left; then as the player: Barnaby's trades and back room, `/trigger bm.standing`, the Bounty Board, the Dark Auction's and the Gilded Gutter's gates, the Rat Bank Teller, Rat Gang HQ |
| `t195.js` | 2.82: the new market's river and clock tower, as a regular player - a ladder up the quay wall from under the water on either bank, climbed out onto the street; dropped twelve blocks into the clock tower onto hay (a scratch at most), its door opened and walked out; the town's labels - every name plate and door/ledger label shown through what's in the way, the PROGRESSIVE JACKPOT sign out of the machine's top |
| `t196.js` | 2.82: KillerWatt pays on any death, once - on a stone floor of his own: brought down by lightning (no player) or by the player's blow, a first win gives his Tendrils, his Spark and the hoard, exactly once, one announcement |
| `t197.js` | 2.82: fishing crates only for a real catch, as a regular player with a real rod - a pig hooked and reeled in (5 times) counts no catch (no crate, no Token roll); a bite in a pond, reeled in, counts |
| `t198.js` | 2.82: Blood Moon drops, as a regular player striking real blows - five horrors, 1 to 3 Crystals each (never none) and their Tokens; a horror that drowned into a Drowned keeps a horror's loot |
| `t199.js` | 2.82: King Omega, the follower - the owner's checklist as a regular player: his Monocle used (his twelve-part rig; 80 health, armour 12), sneak + use for his menu; sat from the menu and by a right-click (his seated cycle), up again; his ways; his Soul Court - a foe slain beside him (his claw or the player's blow) gives one soul, never two, and his menu counts it; Blood Moon worn, kept across a send-home and a call, put back; his aura (locked, used, on, off); his Raid Contract; a display case figurine; Cecil's doll of him bought, set down, twirled, picked up; knocked out - he faints, five minutes before he can be called |
| `t200.js` | 2.82: the Omega Palace, as a regular player (2.89: a soldier's blade and something sweet offered from his court - chapters VI, the War of Brothers, and IX, the boy who cursed the island dark) - placed by `admin/omega_palace` on a cleared stage: the tomb asleep, six pedestals; a pedestal refuses the wrong Emblem; all six seated by right-clicks; without Apophiss the tomb waits ("Apophiss must be here"); his Oath used - he comes, the tomb wakes, the King crawls up ("Who dares disturb-- ...YOU."), the fight begins; worn to 100 health, a blow that would kill him outright - his ward takes it, he yields, the brothers talk, the Monocle is given, the peace advancement and 60 favour; he takes his throne - right-clicked, his court (the Peerage: Squire already, the Ghost Garrison, the Chronicle). 2.87: out of hard mode the tomb won't stir ("Hard mode only"); from his court, "Re-challenge the King" - he wakes and fights again, yields again, and the rematch wins another Monocle; a second rematch that day: "Once a day". 2.88: nothing spawns in the palace (a fresh zombie and a bat turned away within the second, a seen one left alone); he holds court three blocks out from the throne, 0.9 up |
| `t201.js` | 2.82b: finding your way, protected ground, savings - in the rat town as a regular player: the five Town Directory boards; WHO'S WHERE (every trader and place, never the Captain); a guide marker and the action bar to Old Barnaby, gone on arrival; adventure mode on shop floors, docks, stairs and the Lookout (survival again outside); the savings account (only the Teller opens one; two days on, interest paid in by currency). |
| `t202.js` | 2.82b: a crew of three (TestRat, TestMouse, TestVole) - the Ledger, Tier V, 3 TRIES: exactly 3 tries for the crew; four Tier V heists laid puzzle, fight, puzzle, fight (an event room stands in only for a puzzle), about half and half; no Mosaic; BEGIN pressed by the player (the ready check, then again); knocked out on the last try in the vault: THE HEIST HAS FAILED, no word of the vault opening, back in the den. |
| `t203.js` | 2.82b: the presses as a regular player - the Counterfeiter's Press set down by use, the ink still wet the same day, a week's printing; 420 days of printing: Tokens, a Medallion about 1 day in 25, a Trophy rarely, one thing a day; the Blood, Xenite and Lucky Presses set down (one of each per crook), a week on 14 Blood Crystals / 14 Green Xenite / 7 Lucky Tokens; sneak + punch folds one up; the 6% win rolls by heist kind. |
| `t204.js` | 2.82b: Cecil's tent, the Curio Walk (2.82c: rock again, and the Cabinet's front wall brown terracotta, out of the forge pit's fire), a crew page that doesn't spoil - the market's model-hosts (Cecil, the Chef, the Armory) stay invisible and get it back if it wears off; the tent dressed; a straight walk from the Dark Auction's plaza to Fishy's Cabinet door; met only Cecil: the Raid Crew page lists Cecil and no one unmet, its Outfits page only Cecil's wardrobe and nothing of Emma's buff. |
| `t205.js` | 2.82b: the crowns no longer make you bigger, as a regular player - an old (2.82) True Crown with its size modifier re-synced to this version; used and worn: scale 1, its +12 health kept; Apophiss's Crown and the Unbound Crown worn: scale 1. |
| `t206.js` | 2.82c, as a regular player: the Tailor lists only the followers met (Cecil only: no other name, outfits or auras; an unmet page code goes back to the main page); King Omega called with his Monocle - a Blood Moon kill pays triple currency (at least 6 Tokens, 3 Crystals), 400 regular kills pay a handful of tithes; sent home, a kill pays as before and regular kills none; an Arachno-Lantern and a Monstrosity risen 120 blocks off still there 5 s on, gone with nobody within 160; a palace's great door fits its arch (and an old palace's 4 x 4 arch is filled in); the Fence's Associate shelf sells Ominous Trial Keys. |
| `t207.js` | 2.82d, as a regular player: the Bloodbroker sells the Crimson War Horn for 13 Blood Crystals; blown with no Blood Moon it is refused and kept; on a Blood Moon the Monstrosity rises about 10 blocks ahead and the horn is spent; blown again while it is out, refused. With the fleet not yet noticed (#vornmet 0) Zorp does not stock the Vorn Fleet Beacon and switching it on is dead air (kept); once noticed Zorp stocks it, switching it on brings an Invasion Night tonight (spent), and again says the Vorn are already coming. The heist finds roll 5% for the Crimson Effigy, 5% for the beacon (only once noticed) and 5% for the horn on Blood Moon heists. |
| `t208.js` | 2.82e, as a regular player: the Dreadnought alarm's guards carry the bm:p32/guardian loot table; TestRat kills 60 of them with real hits - their other shards drop as before, Red Xenite only about one kill in ten (at most 15 of 60); 10 invasion troopers still drop Red Xenite every time. Counts what TestRat picked up plus what still lies on the deck. |
| `t209.js` | 2.82f, as a regular player: a Tier III heist planned through the Ledger's buttons; the tank kit (rank 2) staged; TestRat eats a kit golden apple (a real right-click); the heist paid out, the heist-over dialog's Start a new raid pressed, Tier III planned again - into the new den with the kit's golden apples topped back up to the rank's own count; a Lights Out heist's bar (the boss-bar packets as received) says LIGHTS OUT, and without it doesn't. |
| `t210.js` | 2.82g, as a regular player: a Tier III job through the Ledger with Memory Match drawn; Goldtooth stocks the Fixer's Lamp; lit in the den on a Lights Out job (right-click) the Lights Out goes (bar packets, crew chat) and the lamp is spent, refused and kept with no Lights Out, refused and kept after BEGIN; Memory Match out of misses (two mismatched cards turned with real clicks): the door stays shut, a try lost, misses back; the skip dialog's own button opens it; out of tries: in the den within seconds, and walking back into the heist is walked straight back out. |
| `t211.js` | 2.82h, with a regular player standing by: on a patch of gutter with a magma half-floor, a heist monster on the magma is fireproofed within seconds and stays unhurt, one on a plain floor isn't; a baby heist piglin grows up within seconds; the built Golden Jockey summons (roster and boss) carry an adult piglin, and no function summons a baby piglin. |
| `t212.js` | 2.82i/j, as a regular player: Chef Fromage sells the Prime Cooler (8 Tokens); carried, it gathers Prime Mutton lying 4 blocks off (one stack) and leaves plain mutton on the ground; right-clicked, it unfolds into a barrel in front of TestRat (no boat) holding what it held, and a right-click on the barrel opens "Prime Cooler"; Prime cuts put in stay, plain beef and a steak come straight back out (none lost) with a word; sneaking packs it up holding only the cuts; unfolded again, all there; a raw porkchop slipped in and TestRat walking off: it packs itself up and the porkchop comes back; beside the Black Market it won't unfold. |
| `t213.js` | 2.82k, as a regular player: a mothership and a Vorn Dreadnought placed overhead; on the ground beneath each, still survival; stood on each ship's deck, adventure mode within seconds (with a word) and digging the deck (real dig packets) leaves it whole; walked away, survival again; a trader NPC given a milk bucket has its hands emptied within seconds. |
| `t214.js` | 2.82l, as a regular player: the Prime Cooler's barrel, the Vacuum Satchel's barrel and the Ender Pouch's ender chest, each set down with a real right-click and broken with real dig packets, give no barrel / ender chest / obsidian (on the ground or in the pack); the goods inside are not lost; the cooler comes back to its owner. |
| `t215.js` | 2.82m, two regular players (TestRat leads, TestMouse): a heist planned through the Ledger, Ranged and Support kits with the wind-charge secondary; wind charges and a potion used up with real right-clicks; the Arcane Study springs on TestRat and its bars drop, and TestMouse, walking up to them, is let through; the leader presses Start a new raid, the member Count me in, and both walk into the new den with the whole kit back (12 wind charges each, the potions); neither raider is in survival down there for a second. |
| `t216.js` | 2.82n, two regular players: both through to the Locker Hall in adventure (one put in survival there is back in adventure within a second); every kit carries a Crew Flare, dead before BEGIN; once begun, the flare takes TestMouse to TestRat, and sneak + flare to the checkpoint before the room ahead; a solved room's entrance is barred as its exit opens; the heist won, the vault's entrance is barred and a raider out in the old rooms is put back in the treasury. |
| `t217.js` | 2.82o, as a regular player: a heist planned from inside the Black Market's zone goes through; a Swinging Lamps Grapple room lends one hook - dropped, it's cleared and exactly one comes back; on the cursor, no second is lent; hooking a lamp's chain from the ledge hangs TestRat under the lamp over its island; 2.82p: leaving mid-puzzle with the hook (the Ledger's Leave the heist) - the hook doesn't come home. |
| `t218.js` | 2.82q/r, a regular player as the winner, the payout's rolls run 600 times a tier: the fee multiplier ~5% at Tier I/II (nearly always 2x) and 5/10/15% at Tier III/IV/V (2x/3x/4x, 4x rarest), every hit paying exactly 1-3 extra fees; the title reaches the client; a hit multiplies the Haul's gutter coins, BM Medallions and Trophies the same; Medallions ~10-30% and Trophies ~1-8% a win by tier, three at a time on a 3x win. |
| `t219.js` | 2.82t, as a regular player: the Ledger dropped in the gutter comes back; the Regalia's Depth Strider III and Aqua Affinity; Wilfrey's locket a click (never leaves the hand), his menu (Call him over, Send him home, Wardrobe), knocked out - a 2-minute rest and back by himself, "Back after a faint" switched off - not back; two satchels two bags, a filter (the diamond taken, the dirt left), a barrel broken - all back in the bag; the Prime Cooler off and on; eight map pieces carried - every new piece the ninth; a sale night - the doors at dusk, slept through - the first lot at daybreak. |
| `t220.js` | 2.83, as a regular player: the Banker's Card - Exchange (5 Tokens ⇄ 1 Medallion, no fee) and Auto-deposit (Medallions banked, Tokens down to 8, rests after a withdrawal); Dennis's Ore Magnet off, switched on by a right-click (raw iron flies in, rotten flesh doesn't), Pistachio's Spirit Jar, a full pack says so; a floor case solid (a barrier) and picked back up; the Trophy Stand faces you; a heist's Blood Moon Guard (diamond, Sharpness III axe, health half again over a plain guard); Celi on a snow layer; a held fort opens again. |
| `t221.js` | 2.83a, as a regular player in the test market's auction hall: on a sale night the gate sign says tonight; at dusk the doors open (with the chat message) and a bidding paddle is handed out; at midnight the first lot is called (bossbar, `#lotn`). With a 20-day Blood Moon, day 29 does not say tonight; day 39 does, and the doors open. |
| `t222.js` | 2.83b, as a regular player: into a heist through the Ledger; Goldtooth's trades (right-click, pick, take) - a Bond Sigil of Fury and a golden apple (marked as his); the den's copper door into the Locker Hall and its plate back to the den with both in hand (it used to turn you away: stuck); home with them; the next heist's door lets the sigil and his apple in while the sword and plain apples from outside wait with the Fixer, and come home. |
| `t223.js` | 2.84a, as a regular player: hard mode wakes for a Hollow King conqueror (title, darkness, Blood Moons every 15 days); a pen of plain zombies rolls again (some Elite/Champion/Dread, most of the rest Strength + Resistance); a Dread zombie's Pulse or Mark lands through netherite on a player who stands still and misses one who walks off; killing it counts (bm.dkill and the world's #dk). The test server keeps hard mode off (`#hardoff 1`): this test wakes it and puts it back. |
| `t224.js` | 2.84a, as a regular player: Vesper appears in the plaza's red-and-white stall when hard mode is on and leaves when it's off; his window turns 10 Trophies into exactly 2 Dread Tokens; the Banker's Card lists Dread Tokens, its Exchange makes one from 5 banked Trophies, its savings page pays 1 in 50 (up to 2 a day); his Ledger (the book on the counter): Ward I (paid pockets first, then the bank) shows on a follower, Swift Return I cuts a faint to 80 s, two Attack Damage tunings and an unbind (every token back), Hero of Time's Tunic reforged into the Fierce Deity's; then, on a pad out of town, the Auctioneer's Writ, the Tome of Eternity, the Dread Compass, the Bottomless Bucket and the Echo of the Hollow King. (2.84d: staged as a King-slayer; once the Echo steps the record back to 5, every trade is veiled and the Ledger refuses, and with conquest 6 again the trades come back.) |
| `t225.js` | 2.84b, as a regular player: the Banker's Card's Community Pots page (a pot staged at 280/300; Give 50 takes only the 20 it needs, unlocks it, tells the world, Luck I for everyone, switched off again); an Infusion of Lifesteal onto the sword in the off hand (marked, a second one refused, a kill heals), Vitality on a worn chestplate (Regeneration); the Drowned Bell set down and picked up, and its Scrap Bin price; the Rimeheart clears slowness; a hard-mode Dark Auction's first lot is a ☠ artifact; a hard replay's boss buff (175% health, healed to full). |
| `t226.js` | 2.84c, as a regular player: an old (item version 40) Crimson Ribcage with a Dread tuning and an infusion re-syncs with the rebalance on it and keeps both; the Partner Wheel (Emma's Ribbon goes on from the off hand; its page lists only her; Call Emma, she stays while the ribbon is on the wheel; 2.88: the wheel's Menu button opens her own menu; Send Emma home; Take the item back; on again, called, and the wheel dropped: she goes home); Zorp's stock (Xenoplate, the Donadian blades; in hard mode the Warplate, Annihilator and Graviton Pick) and a Xenoplate Helm bought through his window; the Plasma Cutter's burn and glow, full Xenoplate's Jump Boost and Deflector, full Warplate's Strength/Speed and its Shockwave. |
| `t227.js` | 2.84d, as a regular player: a Dread Token, 16 Ember Scales and 16 Void Shards tossed down are forged into an Omni Token; the Ember Rat sells the Golden Cecil Doll (Cecil met) while the Frog's stays wrapped (not met); the doll bought through his window, set down (sneak + use: Fire Resistance nearby) and punched back into the pack; the Void Rat sells the Eldritch Panoply, and the Gnawing Pick bought (Haste while held); the full Panoply (Night Vision, Darkness cleared, a zombie's blow lashed back); a Maw kill gives Absorption; Dread rolls: none in 400 for a conquest-0 player, some for a King-slayer. (Vesper's veil and his Ledger's refusal are t224's last steps.) |
| `t228.js` | 2.85a, as a regular King-slayer: Vesper sells the Golden Cross (a Dread Token) and the Dread Bell (3 Dread Essence); the bell rung by day makes tonight a Dread Night; at nightfall the night's own monsters are left alone (one already out stays, a fresh one rises; 2.88), Emma won't come out, and the player is hunted; a Stalker rises 30+ blocks off, bound to them with its whole ten-part rig; a netherite sword can't hurt it; its blow takes a third of a full Eldritch-armoured player's health (measured by damage taken); the cross set on the floor throws a Stalker back out of its ground and the player beside it is untouched; one on a wall hangs facing out; both punched back into the pack; standing still 8 s brings a boxed-in Stalker out behind you; outrun (70 blocks), it loses you; dawn ends it and pays 3 Essence + 1 for the one outrun; 16 Essence and 4 Dread Tokens tossed down forge a Dread Totem, which by day stops a fresh monster rising and puts one already out on its side, until it's dropped. (Stages: hard mode, conquest 6, Blood Moons off, the hour.) |
| `t229.js` | 2.85b, as a regular player: the Deathmask tossed down beside a Golden Cross: light gathers, and it comes up angelic (its model, gold trim, the name), its Protection kept and the cross spent; the True Crown the same way; the purified Regalia worn wakes by day (+15%), more at high noon (+30%), sleeps at night; one corrupt piece and night wakes it again; the angelic crown gives Strength II by day, not by night; an old item version re-syncs and stays angelic; tossed onto Apophiss's seal in the Hollow it's corrupted back to the netherite look. (Stages: Blood Moons off, the hour, the other three angelic pieces, the trip to the Hollow.) |
| `t230.js` | 2.85c, as a regular player: the Lounge's Goldtooth sells a Starter's Pistol (2 Gutter Medallions), bought at his counter; fired in the Lounge it's handed back (the Overworld only); it comes home with you; fired at night, too late, handed back; fired in the morning the Rat Race is on (the word, the gold bar), fired again until the job is one to mine; alone the base target, a second player joins and it grows, they leave and it stays; ore set back down and mined again counts for nothing; the world's own ore mined: halfway word, then WON, the bar gone, Tokens and a prize; the pistol again the same day refused; a race not done by sunset is lost with no Tokens taken; the Lucky Horseshoe hung up by day makes tonight a Lucky Night, a second won't hang; the prize draw rolled 40 times by rcon gives Tokens every time and a spread of prizes. (Stages: Blood Moons off, the hour, a Lounge pass, the ore, the call-off between tries.) |
| `t231.js` | 2.85d, as a regular player: each of the seven new fight rooms (`node t231.js <kind>` for one), the heist planned through the Ledger at Tier III with rooms of only that kind and begun at the den's button; walked in, it springs - its door barred, its own foes out; TestRat strikes one down with a real swing; wave after wave (and its boss) until it's won and the exit opens. The Siege: the Teller and his strongbox's bar, safecrackers at the box wear it down, cracked costs a try and the siege starts over. The Sinking Vault: a square of floor gives way, the hay pit sends you back to the door, won mends the floor. The Gallery: archers on the balconies. The Larder: everyone out for ten seconds and a fight starts over, unbarred. (Stages: Tokens, the Ledger, one kind of room, where TestRat stands, each wave's foes killed.) |
| `t232.js` | 2.85d, as a regular player: the Ember Rat's Call blown in the Overworld does nothing and is kept; in the Nether the Ember Rat sets up shop and the call is used; a second call with him out is kept; the Void Rat's Call in the End past the dragon's isle brings the Void Rat; the haul (the win's per-raider finds rolled by rcon): Ember Scales for a raider who saw the Blaze Forge beaten (about 60%), Void Shards for the Void Garden, neither for neither; a found call lands in the haul. (Stages: floors in the Nether and the End, the calls in hand.) |
| `t234.js` | 2.86: Ashur, the owner's checklist as a regular player - found in the hot country and won with coal; her menu, sit, Heat; fireball, Flamethrower, Eruption; Blue Flame worn and kept; her aura; her Raid Contract; the Cinder in a frame; her figurine; Cecil's doll; she faints (two minutes). |
| `t235.js` | 2.86: the Chef, the owner's checklist as a regular player - the five Prime meats eaten, then found by Chef Fromage and won with a Prime cut; his menu, sit; Prime Presence (a cow drops Prime Beef near him, plain 25 blocks off); all five feasts fed (Well Fed 5, the Master Chef); pie and Meatball Barrage; Midnight Brigade kept across a call; his aura; his contract; the wheel; frame, figurine, doll; he faints. |
| `t236.js` | 2.86: the Neighbor, the owner's checklist as a regular player - a record put on by day (nobody), then at night in a village (he comes to listen), won with a note block; his menu, sit; Tempo, the Healing Song, a Sharp Note, Dissonance, the Crescendo; Navy Bandmaster kept across a call; his aura; his contract; the wheel; frame, figurine, doll; he faints. |
| `t237.js` | 2.86: the bonds, as a regular player - the Neighbor and the Chef called with their items: "Dinner and a Show" (achievement, intro, Speed); Fishy joins: "The Dinner Party" trio (achievement, Luck), gone when they go; Ashur and Leo: "The Sunfire Oath" (achievement, Fire Resistance, Strength). |
| `rigpet_t.js` | 2.87: the shared as-a-player checklist for a rigpet follower (Queen Ava, Queen Pearl, Bloo, the Stalker, the Arachno-Lantern) - each test gives its encounter and its abilities; the runner does the rest as a regular player: the item called and called over (the rig's parts and health), the menu (sit / send home, ways, wardrobe, story, form), sitting from the menu and by a right-click (the seated cycle), the first look worn and kept across a send-home, Call for her/him/it, the form with the look on it, the plain look back, the rare aura, the Raid Contract signed (and the Recruiter selling it), the Partner Wheel, the frame trick, a display-case figurine, Cecil's doll bought in his window, set down, twirled and picked up, and fainting with its cooldown. Not run on its own. |
| `t238.js` | 2.87: Queen Ava (rigpet_t) - hard mode: a conduit set down at night with Emma out raises her ghost; with Emma near, she joins (the Locket); her living fight (Royal Ward, Tidal Lash, Undertow, Tide of Crowns), her ghost form (Spectral Touch, the Lament, Requiem) and Mother's Watch; her story; then the shared list |
| `t239.js` | 2.87: Queen Pearl (rigpet_t) - a cake set down by day on a beach after meeting Emma; handed a cake, she joins (the Pearls); her Whims, Pearl Flick, the Wink, Royal Proclamation; the regal form (By Royal Decree, her grumbles); then the shared list |
| `t240.js` | 2.87: Bloo (rigpet_t) - hard mode: a sapling planted in a forest at night; empty-handed, he wants something worth eating; given raw salmon he joins (the Claw); Claw Rake (Wither, Frenzy), Pounce, Feral Roar, the Wild Hunt; then the shared list |
| `t241.js` | 2.87: the bonds of the deep, as a regular player - Emma, Queen Ava and Queen Pearl called with their own items: "The Royal Family" (its achievement; Resistance II, Conduit Power, more hearts; the Ethereal Echo hurts and lights up foes; the Bloodline Ward catches the player at 2 hearts) and "Mother and Daughter"; Leo, Emma and Ava, "The Queen's Oath" (Strength II, Resistance II, Absorption IV); Bloo and Democratus, "Old Wounds" |
| `t242.js` | 2.87: the Stalker (rigpet_t) - hard mode: a Dread Night's dawn survived wearing the Stalker's Grin - one stays behind; empty-handed it only waits; given Dread Essence it follows (the Hollow Hook); Rend through full netherite (the third blow takes a quarter of a 300-health foe), Step from the Dark (behind its foe), the Stare (frozen), the Harrowing; Night-Born; Kin - it still comes on a Dread Night; then the shared list |
| `t243.js` | 2.87: the Arachno-Lantern (rigpet_t) - hard mode: the great Lantern's reward leaves a Kindled Gourd; used, it cracks and the little one unfolds; right-clicked with the gourd, it's yours; Ember Bite (burning), Tongue Lash (dragged in), Stomp, Ember Rain, Hallowfire; ridden from its menu - it strides where you look, leaps, the Glare from the saddle burns a foe ahead, sneak to get off; then the shared list |
| `t244.js` | 2.88: Bender (rigpet_t) - round a village (three villagers) he trots out; empty-handed he sniffs for a bone; given one, his ball; Bite, Tackle (slowed), Guard Bark (weakened foes, Resistance for you), Good Boy! (both foes bitten, Regeneration II); his menu: Dig! on dirt (something comes up; pressed again, "Dig again in..."), Sniff out treasure (which way and how far, or nothing near); then the shared list |
| `t245.js` | 2.88: Bones (rigpet_t) - out on the ocean a fin cuts the water; empty-handed he wants fish; given a cod, CHOMP - his whistle; Bite, Thrash (slowed), Torpedo, Feeding Frenzy (Regeneration for you); Dolphin's Grace in the water near him; ridden from his menu (he floats along where you look on land, Water Breathing for the rider), CHOMP from his back, sneak off; then the shared list |
| `t246.js` | 2.88: the Dread bosses, as a regular player - hard mode: a ruin's altar right-clicked without its trio lists who's missing; with Pistachio, Celi and Tullius beside you the Malevolent Snowbeast rises, fights (ice-shard volleys) and falls - the Frostbitten Token, the spoils, the advancement; the token carried (Resistance), set down as a ward and taken back; the Watchful Witch's altar refuses you too; Vesper's maps and token scrapping. |
| `t247.js` | 2.88: the Stalker remade, on a Dread Night as a regular player - the night's own monsters left alone (one out before nightfall stays, a fresh one rises); the Stalker's body the follower's jointed rig (ten parts, none riding it); held still it stands tall with its rig at its feet; let go it comes on all fours and runs you down flat out; walled into a stone hut it can't get closer, winds up ("Walls won't stop it.", no AI) and comes straight through the stone to come out beside you, the walls still standing; then the chase goes on with a cooldown |
| `t248.js` | 2.89: the old stories, as a regular player - a Fire Gem's lore (a shard of the Ethereal Gem) and the Ethereal Gem's (the heart of a kingdom not always under the sea, broken in the great war); an old gem (old lore, an old version stamp) re-synced to it; the Dread Court called with their own items, their banter heard until the serpent's campaign comes up ("what is left of their gem" - "My land is still dying"), past the trio's first three exchanges. (King Omega's chapters VI and IX: t200.) |
| `t249.js` | 2.90: Mr. Capshun, the narrator, as a regular player (rigpet_t) - by a hung painting a doodle steps out; empty-handed he wants colour, given a dye he joins (his pencil); brush swipe / pencil jab, paint splat, sketch (Slowness IV + Weakness), wet paint (Slowness III on three foes), the Rainbow Stroke (foes hurt, Strength); his menu: Palette -> Blue, then Fresh Coat (Speed), The story so far; narration when badly hurt; then the shared list (sit, wardrobe, aura, contract, wheel, frame, figurine, doll, faint). |
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

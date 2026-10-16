# Black Market datapack - notes for Claude

Everything lives in `bm_build/`.

- **Fresh container, or after a restart:** run `bm_build/tools/setup_test_env.sh --start`. It fetches the 26.3 jars, builds the checkers' reference data, creates and starts the test server (`~/bm_srv`), and installs the bots. Each step is skipped when it's already done.
- **Build:** `python3 gen_dp.py --phase2` (the datapack; it also rewrites `BUTTON_CODES.md`). Add `python3 gen_rp.py --phase2` when art changes.
- **Checks** (from `bm_build/`, with `BM_OUT=$PWD/out_p2`): `check262.py`, `check_logic.py`, `check262_nbt.py`, `check262_assets.py`, `check_trades.py`, `check_xref.py`. Each must report 0 errors and 0 dead functions.
- **Deploy** to the test server: `tools/dev.sh --no-build`.
- **Package:** `python3 package.py`, which writes `dist/BlackMarket_DP.zip` and `dist/BlackMarket_RP.zip`.
- **Version:** `VERSION2` in `gen_dp.py`. Bump the letter for every package sent, and give it a README section.

## Menu buttons: read `bm_build/BUTTON_CODES.md` first

It is the living legend of every `/trigger bm.act set N` code. For each one it lists:
- the button's words, where it's shown, and the menu (`bm.menu`) it needs;
- how the routers send it;
- the blocks each router owns, and the codes still free;
- any problems, plus a revision log per version.

Before adding a button:
1. Pick a free code.
2. Route it with an exact code (a range only over a block you own).
3. Have the router check `bm.menu`.
4. For a button that only closes its menu, use `P28.NOOP` (code 2).

The build rewrites the legend and fails if any button is unrouted. Keep lessons in its **Notes** section; the build preserves it.

## New followers: the owner's checklist

Every follower ships with all of these, built alongside it (never "later"):
1. **UI test:** the follower's menu (from its summon item), pressed through by a bot test as a regular player.
2. **Frame gimmick:** the summon item in an item frame does that follower's trick.
3. **Display case figurine:** the follower's real model in the floor and wall display cases, never clipping out.
4. **Matching doll from Cecil:** a chibi doll baked from its real model (`dolls_bake.py`), sold by Cecil, framable.
5. **Sitting animations:** right-click (or sneak + right-click) to sit, with a seated pose and idle cycle.
6. **Cosmetics:** at least one, with per-form colour variants, persisting across recall.
7. **Rare cosmetics:** a rare, expensive particle-aura cosmetic, hard to earn from raids.

`tools/bots/t163.js` (Fishy) walks the whole list as a regular player; copy it for the next follower. Also add the new
follower to the every-follower tests (t138 figurines, t146 frames, t156 dolls, the `KINDS` lists in t145 and t158).

## Testing (the owner's rule)

Never rely on just running functions. Playtest as a regular, non-operator player:
- press the dialog buttons the client actually received (send that button's own command);
- use items as real items.

Use rcon only to set the stage.

Chunks a test force-loads are released when it ends - every test, automatically (`tools/bots/chunks.js`, through the
rcon helpers): only the chunks the test itself added, never one the pack holds (the gutter's den, Lounge and Locker Hall
are force-loaded for good). After a sweep, `node chunkcheck.js` should show none left in the Overworld, Nether or End.
Retire a test once newer as-a-player tests cover it, or trim its stale steps; don't leave stale tests in the index.

The bots that play this way live in `bm_build/tools/bots` (`node t133.js`, for example). Its README covers the library, the gotchas learned so far, and an index of every test. Add new tests there.

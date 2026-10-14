# Black Market datapack - notes for Claude

Everything lives in `bm_build/`.

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

## Testing (the owner's rule)

Never rely on just running functions. Playtest as a regular, non-operator player:
- press the dialog buttons the client actually received (send that button's own command);
- use items as real items.

Use rcon only to set the stage.

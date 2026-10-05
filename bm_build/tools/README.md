# Port / verification tools (26.3)

- `build_ref263.py` builds the static checkers' reference data straight from the 26.3 jars (the server's data
  generator reports + the client's assets). Expects `$BM_MC/server.jar` and `$BM_MC/client.jar` (default `/home/claude/mc263`).
- `gt263.sh <out|out_p2> [extra pack] [test selector]` runs the real server headless in GameTest mode
  (`-DbundlerMainClass=net.minecraft.gametest.Main`) with the built data pack. Load errors land in its log.
  Set `BM_SCRATCH`, `JAVA` and `BM_SERVER_JAR` for your machine.
- `harness.py build|check <out|out_p2>` writes and evaluates a runtime test pack (`BM_SCRATCH` sets where):
  - every trader is spawned and its offers are saved;
  - every trade cost and exact custom_data test is checked against the loot-table item;
  - every summon and entity data write is replayed, with canaries that must be reported;
  - every template is placed by the framework;
  - every macro line is parsed with sample arguments.
  The test pack also runs in an ordinary server: put it in the world's datapacks next to the pack, `/reload`, run
  `function bm_test:setup`, then `function bm_test:run`, and copy that part of the server log to `$BM_SCRATCH/gt/run.log`
  for `harness.py check`.
- `tradecmp.py <out|out_p2>` deep-compares the offers the pack writes with the offers the live trader stored.
- `keyaudit.py` audits the Phase 2 vault, boss and spawner keys.
- `verify_dungeons.py [dungeon...]` runs the layout verifier (`p2/verify.py`) on the Phase 2 dungeons: every puzzle reachable
  in order, nothing skippable, safe plate routes, vaults reachable.
- `access.py <dungeon> <x> <z> | all | recheck <dungeon> <x> <z>` places a dungeon (or the graveyard) in real terrain on the
  local test server and proves a player can walk from the surrounding land or sea to its entrance.
- `dev.sh [--no-build] [--restart]` builds the Phase 2 packs, installs the data pack into the local test server and reloads it.
- `rcon.py`, `scan.py`: a minimal RCON client and a region-file block reader used by the tools above.
- `droptest.py`: places every template and checks nothing breaks or drops.

Paths inside some tools still point at the original build machine's scratch folder; adjust them (or `BM_SCRATCH`) before reuse.

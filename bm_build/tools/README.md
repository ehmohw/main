# Port / verification tools (26.3)

- `build_mc263.py` builds the static checkers' reference data from the server jar's data generator
  (`java -DbundlerMainClass=net.minecraft.data.Main -jar server.jar --reports --server`) and the client jar's assets.
- `gt263.sh <out|out_p2> [extra pack] [test selector]` runs the real server headless in GameTest mode
  (`-DbundlerMainClass=net.minecraft.gametest.Main`) with the built data pack. Load errors land in its log.
- `harness.py build|check <out|out_p2>` writes and evaluates a runtime test pack:
  - every trader is spawned and its offers are saved;
  - every trade cost and exact custom_data test is checked against the loot-table item;
  - every summon and entity data write is replayed, with canaries that must be reported;
  - every template is placed by the framework;
  - every macro line is parsed with sample arguments.
- `tradecmp.py <out|out_p2>` deep-compares the offers the pack writes with the offers the live trader stored.
- `keyaudit.py` audits the Phase 2 vault, boss and spawner keys.

Paths inside the tools point at the build machine's scratch folder; adjust `S` before reuse.

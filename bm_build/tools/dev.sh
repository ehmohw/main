#!/bin/bash
# Build the Phase 2 packs, install the data pack into the local test server and /reload it.
# Prints every load problem the server reports for this reload.
#   usage: tools/dev.sh [--no-build]
set -e
cd "$(dirname "$0")/.."
SRV=${BM_SRV:-/tmp/claude-0/-home-user-main/5487f497-06f9-53d0-b240-d8be6367a14d/scratchpad/srv}
BUILD=1; RESTART=0
for a in "$@"; do case $a in --no-build) BUILD=0;; --restart) RESTART=1;; esac; done
if [ $BUILD = 1 ]; then
  python3 gen_dp.py --phase2 | tail -1
  python3 gen_rp.py --phase2 > /dev/null
fi
if [ $RESTART = 1 ]; then
  python3 tools/rcon.py "stop" > /dev/null 2>&1 || true
  for i in $(seq 1 40); do kill -0 $(cat "$SRV/server.pid") 2>/dev/null || break; sleep 1; done
  rm -rf "$SRV/world/datapacks/"*
  cp -r out_p2/BlackMarket_DP "$SRV/world/datapacks/BlackMarket_DP"
  n=0
  "$SRV/start.sh" > /dev/null
  sleep 6
else
  rm -rf "$SRV/world/datapacks/"*
  cp -r out_p2/BlackMarket_DP "$SRV/world/datapacks/BlackMarket_DP"
  n=$(wc -l < "$SRV/run.log")
  python3 tools/rcon.py "reload" > /dev/null
  sleep 4
fi
tail -n +$((n + 1)) "$SRV/run.log" | grep -vE "^\s+at |JAVA_TOOL" | grep -E "ERROR|WARN|Failed|Couldn't|Exception|Unknown|error" | grep -vE "Minecraft Services|^WARNING|authlib|BEGIN_OBJECT|OFFLINE|authenticate|hackers|online-mode" | cut -c1-500 | head -${MAXERR:-40} || true
echo "reload done ($(tail -n +$((n + 1)) "$SRV/run.log" | grep -c ERROR || true) errors)"

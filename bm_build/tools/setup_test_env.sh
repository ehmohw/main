#!/bin/bash
# Set up the build + playtest environment in a fresh container, or bring it back after a restart. Safe to run again:
# each step is skipped when it's already done.
#   1. /home/claude/bm_build -> this bm_build      (gen_dp writes its output through that path)
#   2. the 26.3 server and client jars in $BM_MC   (default /home/claude/mc263; from Mojang, SHA-1 checked)
#   3. the static checkers' reference data         (tools/build_ref263.py, from the jars)
#   4. a local test server in $BM_SRV              (default ~/bm_srv: offline mode, rcon 127.0.0.1:25575 "bmtest",
#                                                   seed 20261005, flight allowed - the bots expect all of it)
#   5. the playtest bots' packages                 (tools/bots: npm install, which also patches the protocol for 26.3)
#   6. with --start: start the server if it isn't running (the pack goes in first: its dimensions load only at start),
#      or reinstall the pack and /reload if it is
#   usage: tools/setup_test_env.sh [--start]
set -e
BM="$(cd "$(dirname "$0")/.." && pwd)"
MC="${BM_MC:-/home/claude/mc263}"
SRV="${BM_SRV:-$HOME/bm_srv}"
VER=26.3
JAVA="${JAVA:-/usr/lib/jvm/java-25-openjdk-amd64/bin/java}"
[ -x "$JAVA" ] || JAVA="$(command -v java)"
START=0; for a in "$@"; do [ "$a" = --start ] && START=1; done
say() { echo "setup: $*"; }

# 1. the build's path
if [ ! -e /home/claude/bm_build ]; then mkdir -p /home/claude && ln -s "$BM" /home/claude/bm_build && say "linked /home/claude/bm_build -> $BM"; fi

# 2. the jars
mkdir -p "$MC"
if [ ! -f "$MC/server.jar" ] || [ ! -f "$MC/client.jar" ]; then
  say "fetching the $VER server and client jars"
  url=$(curl -fsS https://piston-meta.mojang.com/mc/game/version_manifest_v2.json |
        python3 -c "import json,sys; print(next(v['url'] for v in json.load(sys.stdin)['versions'] if v['id'] == '$VER'))")
  curl -fsS "$url" -o "$MC/$VER.json"
  for k in server client; do
    read -r u h < <(python3 -c "import json; d = json.load(open('$MC/$VER.json'))['downloads']['$k']; print(d['url'], d['sha1'])")
    curl -fsS "$u" -o "$MC/$k.jar.part"
    [ "$(sha1sum < "$MC/$k.jar.part" | cut -c1-40)" = "$h" ] || { say "$k.jar: wrong checksum"; exit 1; }
    mv "$MC/$k.jar.part" "$MC/$k.jar"
  done
fi

# 3. the checkers' reference data
if [ ! -f "$MC/commands.json" ]; then say "building the checkers' reference data"; (cd "$BM" && python3 tools/build_ref263.py); fi

# 4. the test server
if [ ! -f "$SRV/server.properties" ]; then
  say "creating the test server in $SRV"
  mkdir -p "$SRV/world/datapacks"
  echo "eula=true" > "$SRV/eula.txt"
  cat > "$SRV/server.properties" <<EOF
motd=Black Market test server
online-mode=false
enable-rcon=true
rcon.port=25575
rcon.password=bmtest
broadcast-rcon-to-ops=false
level-seed=20261005
gamemode=survival
difficulty=easy
allow-flight=true
spawn-protection=0
enable-command-block=true
op-permission-level=4
max-players=4
white-list=false
generate-structures=true
EOF
  cat > "$SRV/start.sh" <<EOF
#!/bin/bash
cd "\$(dirname "\$0")"
nohup "$JAVA" -Xmx4G -Xms1G -jar "$MC/server.jar" --nogui < /dev/null > run.log 2>&1 &
echo \$! > server.pid
for i in \$(seq 1 180); do grep -q 'RCON running' run.log && break; sleep 1; done
grep -E 'Done \(|RCON running' run.log
EOF
  chmod +x "$SRV/start.sh"
fi

# 5. the bots
if [ ! -d "$BM/tools/bots/node_modules/minecraft-protocol" ]; then
  say "installing the bots' packages"; (cd "$BM/tools/bots" && npm install --no-audit --no-fund)
fi

# 6. running
if [ $START = 1 ]; then
  [ -d "$BM/out_p2/BlackMarket_DP" ] || { say "building the pack"; (cd "$BM" && python3 gen_dp.py --phase2 | tail -1); }
  if [ -f "$SRV/server.pid" ] && kill -0 "$(cat "$SRV/server.pid")" 2>/dev/null; then
    say "the server is running - installing the pack and reloading"
  else
    say "starting the server with the pack in place"
    rm -rf "$SRV/world/datapacks/"*; mkdir -p "$SRV/world/datapacks"
    cp -r "$BM/out_p2/BlackMarket_DP" "$SRV/world/datapacks/BlackMarket_DP"
    "$SRV/start.sh"
  fi
  BM_SRV="$SRV" "$BM/tools/dev.sh" --no-build
fi
say "ready (server: $SRV)"

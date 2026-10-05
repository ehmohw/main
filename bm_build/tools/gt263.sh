#!/bin/bash
# Load a built data pack into the real 26.3 GameTest server and print every load problem it reports.
# usage: gt263.sh <out|out_p2> [extra pack dir]
S=${BM_SCRATCH:-/tmp/claude-0/-home-claude/3b068e51-eb2f-56d1-b54d-7ae7b9353a7e/scratchpad}   # 2.15: set BM_SCRATCH / JAVA / BM_SERVER_JAR
OUT=${1:-out}
rm -rf $S/gt/packs $S/gt/uni; mkdir -p $S/gt/packs
cp -r /home/claude/bm_build/$OUT/BlackMarket_DP $S/gt/packs/
[ -n "$2" ] && cp -r $2 $S/gt/packs/
cd $S/gt && timeout 1200 ${JAVA:-/usr/lib/jvm/java-25-openjdk-amd64/bin/java} -Xmx4G -DbundlerMainClass=net.minecraft.gametest.Main -jar ${BM_SERVER_JAR:-$S/gen263/server.jar} --packs packs --universe uni --tests "${3:-bm_test:*}" > $S/gt/run.log 2>&1
echo "exit $?"
grep -vE "^WARNING:|JAVA_TOOL|^\s+at |^\s+\.\.\. [0-9]+ more" $S/gt/run.log | grep -E "ERROR|WARN|Failed|Couldn't|Exception|Caused by|Unknown|error" | grep -v "Failed to load vanilla datapack, bit oops" | cut -c1-400 | head -${4:-60}

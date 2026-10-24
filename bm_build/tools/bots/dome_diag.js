// (diagnostic, not a test) the dome raised after a shatter: how much water is left inside, and where
const { rcon, sleep } = require('./lib_resp');
const C = require(process.argv[2]);
(async () => { const R = await rcon(); const run = c => R.run(c);
  const O = 'execute in minecraft:overworld run ', X = 18200, Y = 40, Z = 16000;
  const CORE = `@e[type=minecraft:marker,tag=bm.kingdom,x=${X},y=${Y},z=${Z},distance=..80,limit=1]`;
  await run(`${O}forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`); await sleep(2000);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..90]`);
  for (let z = Z - 46; z <= Z + 46; z += 8) {
    await run(`${O}fill ${X - 46} ${Y - 5} ${z} ${X + 46} ${Y - 1} ${Math.min(z + 7, Z + 46)} minecraft:sand`);
    await run(`${O}fill ${X - 46} ${Y} ${z} ${X + 46} ${Y + 31} ${Math.min(z + 7, Z + 46)} minecraft:water`);
  }
  await run(`${O}execute positioned ${X} ${Y} ${Z} run function bm:admin/kingdom`); await sleep(3000);
  await run(`${O}execute as ${CORE} at @s run function bm:p199/dome/shatter`); await sleep(6000);
  await run(`${O}execute as ${CORE} at @s run function bm:p199/dome/mend`); await sleep(4000);
  let tot = 0; const where = [];
  for (const [x, z, y0, y1, a, b] of C.cols) {
    const r = await run(`${O}execute as ${CORE} at @s run fill ${a} ${b} minecraft:air replace minecraft:water`);
    const m = r.match(/(\d+) block/); if (m) { tot += +m[1]; where.push(`${x},${z}:${m[1]}`); }
  }
  console.log('water left inside:', tot); console.log(where.slice(0, 40).join(' '));
  await run(`${O}forceload remove ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`); R.end(); process.exit(0);
})();

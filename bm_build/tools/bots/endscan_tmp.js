// temporary: End surface heights over areas (grid), via positioned over world_surface
const { rcon, sleep } = require('./lib_resp');
const E = 'execute in minecraft:the_end run ';
(async () => { const R = await rcon(); const run = c => R.run(c);
  const areas = JSON.parse(process.argv[2]); const step = +(process.argv[3] || 8);
  for (const [name, x0, z0, x1, z1] of areas) {
    // forceload in <=256-chunk pieces
    for (let x = x0; x <= x1; x += 240) for (let z = z0; z <= z1; z += 240) await run(`${E}forceload add ${x} ${z} ${Math.min(x1, x + 239)} ${Math.min(z1, z + 239)}`);
    await sleep(15000);
    await run(`${E}kill @e[type=minecraft:marker,tag=bmscan]`); await run(`${E}summon minecraft:marker ${x0} 100 ${z0} {Tags:["bmscan"]}`);
    let mx = -1, at = null, n = 0, hist = {};
    for (let x = x0; x <= x1; x += step) for (let z = z0; z <= z1; z += step) {
      await run(`execute in minecraft:the_end positioned ${x} 0 ${z} positioned over world_surface run tp @e[type=minecraft:marker,tag=bmscan,limit=1] ~ ~ ~`);
      const m = (await run(`${E}data get entity @e[type=minecraft:marker,tag=bmscan,limit=1] Pos[1]`)).match(/(-?[\d.]+)d?$/);
      const y = m ? +m[1] : NaN; n++; const b = Math.floor(y / 20) * 20; hist[b] = (hist[b] || 0) + 1;
      if (y > mx) { mx = y; at = [x, z]; }
    }
    console.log(name, 'samples', n, 'max surface y', mx, 'at', at, 'hist', JSON.stringify(hist));
    for (let x = x0; x <= x1; x += 240) for (let z = z0; z <= z1; z += 240) await run(`${E}forceload remove ${x} ${z} ${Math.min(x1, x + 239)} ${Math.min(z1, z + 239)}`);
  }
  await run(`${E}kill @e[type=minecraft:marker,tag=bmscan]`); R.end(); process.exit(0); })();

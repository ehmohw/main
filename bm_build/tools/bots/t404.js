// 3.1q: THE UNDERCROWN'S FIRST SITE, WORN BACK INTO THE NETHER (phase237 p237/oldc, p2/oldcarve). A world that built the Undercrown
// at its first spot (2.98 - 2.99a) had that copy taken down when it moved (p2/oldsite) - its whole box filled with netherrack. rcon
// only sets the stage (the cube, the teardown's flag); then a regular player walks up to it and the pack does the rest: it looks
// (a grid of points deep in the box, all netherrack), carves the cube into a cavern a step a second, holds the box loaded only
// while it carves, and never carves it twice. Also: a world with no cube there (natural Nether) is left alone.
const { bot, rcon, sleep } = require('./lib_resp');
const N = 'execute in minecraft:the_nether run ';
(async () => { const R = await rcon(); const run = c => R.run(c); const res = [];
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (h) => { const m = (await run(`scoreboard players get ${h} bm.p2`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const probes = []; for (let i = 0; i < 5; i++) for (let j = 0; j < 5; j++) for (const y of [40, 64, 88]) probes.push([1568 + 40 * i, y, -1504 + 40 * j]);
  const rack = async () => { let n = 0; for (const [x, y, z] of probes) if (/passed/.test(await run(N + `execute if block ${x} ${y} ${z} minecraft:netherrack`))) n++; return n; };
  const Q = ['1528 -1544 1647 -1424', '1648 -1544 1768 -1424', '1528 -1423 1647 -1304', '1648 -1423 1768 -1304'];
  // ---- the stage: the cube, as the teardown left it
  for (const q of Q) await run(N + 'forceload add ' + q);
  for (let i = 0; i < 60; i++) { if (/passed/.test(await run(N + 'execute if loaded 1536 64 -1536 if loaded 1759 64 -1313 if loaded 1536 64 -1313 if loaded 1759 64 -1536'))) break; await sleep(2000); }
  for (let x = 0; x < 224; x += 32) for (let y = 0; y < 112; y += 32) for (let z = 0; z < 224; z += 32)
    await run(N + `fill ${1536 + x} ${6 + y} ${-1536 + z} ${1536 + Math.min(224, x + 32) - 1} ${6 + Math.min(112, y + 32) - 1} ${-1536 + Math.min(224, z + 32) - 1} minecraft:netherrack`);
  await run(N + 'fill 1647 118 -1425 1649 120 -1423 minecraft:air');
  await run('scoreboard players set #p237_old bm.p2 1'); await run('scoreboard players reset #uoldc bm.p2');
  const full = await rack();
  for (const q of Q) await run(N + 'forceload remove ' + q);
  ok('the stage: a solid netherrack cube (75 of 75 test points), nothing held loaded after', full === 75 && /No force/.test(await run(N + 'forceload query')), `${full}/75`);
  // ---- nobody near: nothing happens
  await sleep(3000);
  ok('nobody near: it isn\'t looked at (no chunk loaded for it)', (await sc('#uoldc')) === null);
  // ---- a regular player walks up to it
  const A = await bot('TestRat'); await sleep(3000);
  await run('deop TestRat'); await run('gamemode survival TestRat');
  await run(N + 'tp TestRat 1648 118 -1424'); await run('effect give TestRat minecraft:resistance 200 4 true');
  let seen = new Set(), held = false;
  for (let i = 0; i < 150; i++) {
    const s = await sc('#uoldc'); seen.add(s);
    if (s === 2 && !held) held = /1528|1648|chunk/i.test(await run(N + 'forceload query 1600 -1500'));
    if (s === 1) break; await sleep(1000);
  }
  ok('someone near: the cube is found, carved (#uoldc 2) and done (1)', seen.has(2) && (await sc('#uoldc')) === 1, [...seen].join(','));
  ok('...the box held loaded while it carved', held);
  ok('...and let go after', /No force/.test(await run(N + 'forceload query')));
  const left = await rack();
  ok('...a cavern now: most of the test points opened', left <= 25, `${left}/75 still netherrack`);
  const cnt = async (b, y0, y1) => { let n = 0; for (let x = 1556; x < 1740; x += 6) for (let z = -1516; z < -1330; z += 6) for (let y = y0; y <= y1; y += 2) if (/passed/.test(await run(N + `execute if block ${x} ${y} ${z} ${b}`))) n++; return n; };
  ok('...lava pools on its floor (under y 31)', (await cnt('minecraft:lava', 21, 31)) > 0);
  ok('...its roof shut: the cube\'s top 6 rows still rock', (await cnt('minecraft:netherrack', 112, 116)) > 900);
  ok('the player unharmed, standing where they were', /118\.0/.test(await run('data get entity TestRat Pos[1]')));
  // ---- never twice: a second look finds no cube
  await run(N + 'setblock 1648 64 -1424 minecraft:netherrack');
  await run('scoreboard players reset #uoldc bm.p2'); await sleep(4000);
  ok('looked at again: no cube there now - left alone (1, no carve)', (await sc('#uoldc')) === 1 && (await sc('#uock')) !== null);
  A.end(); R.end();
  console.log(`${res.filter(x => x).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

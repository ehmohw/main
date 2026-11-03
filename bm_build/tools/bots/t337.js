// 3.0g: THE UNDERWATER KINGDOM, ALL OF IT UNDER THE SEA (phase199's seed, phase203's settling), as a regular (non-op) player. rcon
// sets the stage - a deep sea whose floor is high (y 45, 18 under the surface), an island beside it standing out of the sea, a
// kingdom's seed on the floor - and checks the blocks; the bot swims in and the dome puts it in Adventure, saying so once.
//   - the seed is set down to y 33: the dome's crown (glass) at y 60, nothing of it at 61 or above;
//   - no water anywhere above the sea's surface (y 62) round it - not over the island, not over the settled square;
//   - an old kingdom's over-the-sea water (staged at y 63-64, its once-only tag taken off) is let go within seconds.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const block = async (x, y, z, b) => /passed/i.test(await run(`${O}execute if block ${x} ${y} ${z} ${b}`));
  const count = async (x1, y1, z1, x2, y2, z2, b) => {      // (how many of a block a box holds: to structure voids and straight back)
    const per = Math.max(1, Math.floor(32768 / ((x2 - x1 + 1) * (z2 - z1 + 1)))); let n = 0;
    for (let y = y1; y <= y2; y += per) { const yb = Math.min(y2, y + per - 1);
      const m = (await run(`${O}fill ${x1} ${y} ${z1} ${x2} ${yb} ${z2} minecraft:structure_void replace ${b} strict`)).match(/(\d+) block/);
      await run(`${O}fill ${x1} ${y} ${z1} ${x2} ${yb} ${z2} ${b} replace minecraft:structure_void strict`); n += m ? +m[1] : 0; }
    return n; };
  const gm = async () => ((await run('data get entity TestRat playerGameType')).match(/(-?\d+)$/) || [])[1];
  const X = 26000, F = 45, Z = 26000, S = 62;          // (the sea floor's top water cell; the surface's top water cell)
  const CORE = `@e[type=minecraft:marker,tag=bm.kingdom,x=${X},y=40,z=${Z},distance=..60,limit=1]`;

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance 1200 4 true'); await run('effect give TestRat minecraft:water_breathing 1200 0 true');
  await run(`${O}tp TestRat ${X} 110 ${Z + 100}`); await sleep(1500); A.stand();
  // ---- the stage: a high-floored deep sea, an island, the seed
  await run(`${O}forceload add ${X - 72} ${Z - 72} ${X + 72} ${Z + 72}`); await sleep(3000);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${F},z=${Z},distance=..100]`);
  for (let z = Z - 64; z <= Z + 64; z += 8) {
    const z2 = Math.min(z + 7, Z + 64);
    await run(`${O}fill ${X - 64} ${F - 14} ${z} ${X + 64} ${F - 1} ${z2} minecraft:sand`);
    await run(`${O}fill ${X - 64} ${F} ${z} ${X + 64} ${S} ${z2} minecraft:water`);
    await run(`${O}fill ${X - 64} ${S + 1} ${z} ${X + 64} ${S + 20} ${z2} minecraft:air`);
  }
  await run(`${O}fill ${X + 40} ${F} ${Z - 10} ${X + 52} ${S + 6} ${Z + 10} minecraft:stone`);          // (the island, out of the sea)
  for (let z = Z - 64; z <= Z + 64; z += 16) await run(`${O}fillbiome ${X - 64} ${F - 14} ${z} ${X + 64} ${S + 20} ${Math.min(z + 15, Z + 64)} minecraft:deep_ocean`);
  await run(`${O}summon minecraft:marker ${X + 0.5} ${F} ${Z + 0.5} {Tags:["bm.kseed"]}`);
  ok('the seed on the high sea floor (y 45) builds a kingdom', await wait(15000, async () => (await cnt(CORE)) === 1, 500));
  await sleep(2000);
  const cy = +(((await run(`${O}data get entity ${CORE} Pos[1]`)).match(/(-?[\d.]+)d$/) || [0, NaN])[1]);
  ok('...set down to y 33 (its core marker at 37)', Math.abs(cy - 37) < 0.6, `core y ${cy}`);
  ok('...its crown is the glass at y 60, under the sea', await block(X, 60, Z, 'minecraft:glass') && await block(X, 61, Z, 'minecraft:water'));
  const g = await count(X - 36, 61, Z - 36, X + 36, S + 10, Z + 36, 'minecraft:glass');
  ok('...nothing of the dome at y 61 or above', g === 0, `${g} glass`);
  const w = await count(X - 64, S + 1, Z - 64, X + 64, S + 14, Z + 64, 'minecraft:water');
  ok('no water above the sea\'s surface anywhere round it (not over the island, not over its settled square)', w === 0, `${w} water blocks above y ${S}`);

  // ---- an old kingdom's over-the-sea water: let go once
  await run(`${O}fill ${X + 10} ${S + 1} ${Z - 4} ${X + 20} ${S + 2} ${Z + 4} minecraft:water`);
  await run(`tag ${CORE} remove bm.k30g`);
  ok('an old kingdom\'s water cut above the sea (staged): let go within seconds', await wait(6000, async () => (await count(X + 8, S + 1, Z - 6, X + 22, S + 3, Z + 6, 'minecraft:water')) === 0, 500) &&
     /bm\.k30g/.test(await run(`${O}tag ${CORE} list`)));

  // ---- the bot swims into the dome: Adventure, said once
  A.bars.length = 0;
  await run(`${O}tp TestRat ${X + 0.5} 39 ${Z - 2.5}`); await sleep(1500); A.stand();
  ok('TestRat in the dome: Adventure mode', await wait(5000, async () => (await gm()) === '2', 250));
  await sleep(6000);
  ok('...its word on the action bar once', A.bars.filter(b => /not for digging/.test(b)).length === 1, `${A.bars.filter(b => /digging/.test(b)).length} times`);
  await run(`${O}tp TestRat ${X} 110 ${Z + 100}`); await sleep(4000);
  ok('...out of it: Survival again', await wait(5000, async () => (await gm()) === '0', 250));

  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

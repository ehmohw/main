// 2.82q: THE FEE MULTIPLIER - a won Tier III / IV / V heist pays a raider's fee back doubled, tripled or quadrupled 5 / 10 / 15% of
// the time (2x 45%, 3x 40%, 4x 15% of hits), on top of the fee itself. With a regular (non-op) player TestRat as the winner (rcon
// sets the stage: the payout's tier, then the payout's own roll run for TestRat - 600 times a tier - and its Tokens counted).
//   Each tier's hit rate lands near its 5 / 10 / 15%; every hit pays exactly 1, 2 or 3 extra fees (the tier's fee 4 / 5 / 6); 4x is
//   the rarest; Tier I and II: 5%, nearly always 2x (3x 10%, 4x 5% of hits). TestRat sees the big title (as the client receives it).
//   2.82r/s: a hit multiplies the Haul's gutter coins, BM Medallions and Trophies the same; every win has a tier-scaled chance at a Gutter Medallion (10-30%)
//   and Trophy (1-8%), which come multiplied on a multiplier win.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const tok = async () => { const o = await run('clear TestRat *[minecraft:custom_data~{bm:"token"}] 0'); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/) || [0, 0])[1]); };
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  const seen = []; A.on('set_title_text', p => seen.push(JSON.stringify(p)));
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await run('clear TestRat');
  const FEE = { 1: 2, 2: 3, 3: 4, 4: 5, 5: 6 }; const N = 600;
  const stats = {};
  for (const t of [1, 2, 3, 4, 5]) {
    const k = { hits: 0, m2: 0, m3: 0, m4: 0, bad: 0 };
    for (let i = 0; i < N; i++) {
      await run(`scoreboard players set #gt bm.rng ${t}`);
      await run('execute as TestRat at @s run function bm:p148/feex');
      if (i % 20 === 19 || i === N - 1) { /* (tally by Tokens only at the end of batches) */ }
      const n = await tok();
      if (n > 0) { k.hits++; const m = n / FEE[t] + 1; if (m === 2) k.m2++; else if (m === 3) k.m3++; else if (m === 4) k.m4++; else k.bad++; await run('clear TestRat'); }
    }
    stats[t] = k;
  }
  const lo = { m2: stats[1].m2 + stats[2].m2, m34: stats[1].m3 + stats[1].m4 + stats[2].m3 + stats[2].m4, bad: stats[1].bad + stats[2].bad };
  ok('Tier I and II: about 5% of wins multiply the fee - nearly always 2x, 3x and 4x only now and then', [1, 2].every(t => Math.abs(stats[t].hits / N - 0.05) <= 0.035 && stats[t].hits > 0) && lo.bad === 0 && lo.m2 > 3 * lo.m34,
     `${stats[1].hits}, ${stats[2].hits} hits: 2x ${lo.m2}, 3x/4x ${lo.m34}`);
  const near = (h, p) => Math.abs(h / N - p) <= Math.max(0.035, p * 0.45);
  ok('Tier III / IV / V: hit rates near 5 / 10 / 15%, rising with the tier', near(stats[3].hits, 0.05) && near(stats[4].hits, 0.10) && near(stats[5].hits, 0.15) && stats[3].hits < stats[5].hits,
     `${stats[3].hits}/${N}, ${stats[4].hits}/${N}, ${stats[5].hits}/${N}`);
  const all = [3, 4, 5].reduce((a, t) => ({ m2: a.m2 + stats[t].m2, m3: a.m3 + stats[t].m3, m4: a.m4 + stats[t].m4, bad: a.bad + stats[t].bad }), { m2: 0, m3: 0, m4: 0, bad: 0 });
  ok('every hit pays exactly one, two or three extra fees (2x / 3x / 4x), and 4x is the rarest', all.bad === 0 && all.m4 < all.m2 && all.m4 < all.m3 && all.m4 > 0,
     `2x ${all.m2}, 3x ${all.m3}, 4x ${all.m4}, odd ${all.bad}`);
  ok('...and TestRat sees the big "x YOUR FEE!" title', seen.some(s => /YOUR FEE/.test(s)), `${seen.length} titles`);
  // ---- the coins: 10 in the Haul (the stage), a Tier V win until the multiplier hits - extra coins match the multiplier
  const coin = '*[minecraft:custom_data~{bm:"gutter_coin"}]';
  const cnt = async (q) => { const o = await run(`clear TestRat ${q} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/) || [0, 0])[1]); };
  let cm = null, tm = null;
  for (let i = 0; i < 400 && cm === null; i++) {
    await run('execute in bm:gutter run setblock -200 64 -197 minecraft:air'); await run('execute in bm:gutter run setblock -198 64 -197 minecraft:air');
    await run('execute in bm:gutter run setblock -200 64 -197 minecraft:barrel'); await run('execute in bm:gutter run setblock -198 64 -197 minecraft:barrel');
    for (let k = 0; k < 10; k++) await run('execute in bm:gutter run loot insert -200 64 -197 loot bm:items/gutter_coin');
    for (let k = 0; k < 2; k++) await run('execute in bm:gutter run loot insert -200 64 -197 loot bm:items/medallion');
    await run('execute in bm:gutter run loot insert -200 64 -197 loot bm:items/trophy');
    await run('scoreboard players set #gt bm.rng 5'); await run('execute as TestRat at @s run function bm:p148/feex');
    const t = await tok(), c = await cnt(coin), md = await cnt('*[minecraft:custom_data~{bm:"medallion"}]'), tr = await cnt('*[minecraft:custom_data~{bm:"trophy"}]');
    if (t > 0) { tm = t / 6 + 1; cm = (c / 10 + 1 === md / 2 + 1 && md / 2 + 1 === tr + 1) ? c / 10 + 1 : `mismatch c${c} m${md} t${tr}`; }
    await run('clear TestRat');
  }
  ok('a multiplier hit pays the Haul\'s gutter coins, BM Medallions and Trophies over by the same multiplier', cm !== null && cm === tm, `tokens x${tm}, coins x${cm}`);
  await run('execute in bm:gutter run setblock -200 64 -197 minecraft:air'); await run('execute in bm:gutter run setblock -198 64 -197 minecraft:air');
  await run('execute in bm:gutter run kill @e[type=minecraft:item,x=-199,y=64,z=-197,distance=..8]');
  // ---- medallions and trophies: a chance on every win, rising with the tier, and multiplied too
  const MED = '*[minecraft:custom_data~{bm:"gutter_medallion"}]', TRO = '*[minecraft:custom_data~{bm:"gutter_trophy"}]';
  const gx = {};
  for (const t of [1, 5]) {
    await run('clear TestRat');
    for (let i = 0; i < N; i++) { await run(`scoreboard players set #gt bm.rng ${t}`); await run('scoreboard players set #fmul bm.rng 1'); await run('execute as TestRat at @s run function bm:p148/gutx'); }
    gx[t] = { m: await cnt(MED), t: await cnt(TRO) };
  }
  ok('every win: a Gutter Medallion about 10% (Tier I) to 30% (Tier V), a Trophy 1% to 8%', Math.abs(gx[1].m / N - 0.10) < 0.05 && Math.abs(gx[5].m / N - 0.30) < 0.07 && gx[1].t <= 18 && Math.abs(gx[5].t / N - 0.08) < 0.04 && gx[5].t > gx[1].t,
     `T1 ${gx[1].m} med / ${gx[1].t} tro, T5 ${gx[5].m} med / ${gx[5].t} tro (of ${N})`);
  await run('clear TestRat');
  for (let i = 0; i < 200; i++) { await run('scoreboard players set #gt bm.rng 5'); await run('scoreboard players set #fmul bm.rng 3'); await run('execute as TestRat at @s run function bm:p148/gutx'); }
  const m3 = await cnt(MED), t3 = await cnt(TRO);
  ok('...and on a 3x win they come three at a time', m3 > 0 && m3 % 3 === 0 && t3 % 3 === 0, `${m3} medallions, ${t3} trophies`);
  await run('clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

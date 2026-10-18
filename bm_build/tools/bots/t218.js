// 2.82q: THE FEE MULTIPLIER - a won Tier III / IV / V heist pays a raider's fee back doubled, tripled or quadrupled 5 / 10 / 15% of
// the time (2x 45%, 3x 40%, 4x 15% of hits), on top of the fee itself. With a regular (non-op) player TestRat as the winner (rcon
// sets the stage: the payout's tier, then the payout's own roll run for TestRat - 600 times a tier - and its Tokens counted).
//   Each tier's hit rate lands near its 5 / 10 / 15%; every hit pays exactly 1, 2 or 3 extra fees (the tier's fee 4 / 5 / 6); 4x is
//   the rarest; Tier I and II never hit. TestRat sees the big title (as the client receives it).
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
  const FEE = { 3: 4, 4: 5, 5: 6 }; const N = 600;
  const stats = {};
  for (const t of [1, 2, 3, 4, 5]) {
    const k = { hits: 0, m2: 0, m3: 0, m4: 0, bad: 0 };
    for (let i = 0; i < N; i++) {
      await run(`scoreboard players set #gt bm.rng ${t}`);
      await run('execute as TestRat at @s run function bm:p148/feex');
      if (i % 20 === 19 || i === N - 1) { /* (tally by Tokens only at the end of batches) */ }
      const n = await tok();
      if (n > 0) { k.hits++; const m = t >= 3 ? n / FEE[t] + 1 : 0; if (m === 2) k.m2++; else if (m === 3) k.m3++; else if (m === 4) k.m4++; else k.bad++; await run('clear TestRat'); }
    }
    stats[t] = k;
  }
  ok('Tier I and II wins never multiply the fee', stats[1].hits === 0 && stats[2].hits === 0, `${stats[1].hits}, ${stats[2].hits}`);
  const near = (h, p) => Math.abs(h / N - p) <= Math.max(0.035, p * 0.45);
  ok('Tier III / IV / V: hit rates near 5 / 10 / 15%, rising with the tier', near(stats[3].hits, 0.05) && near(stats[4].hits, 0.10) && near(stats[5].hits, 0.15) && stats[3].hits < stats[5].hits,
     `${stats[3].hits}/${N}, ${stats[4].hits}/${N}, ${stats[5].hits}/${N}`);
  const all = [3, 4, 5].reduce((a, t) => ({ m2: a.m2 + stats[t].m2, m3: a.m3 + stats[t].m3, m4: a.m4 + stats[t].m4, bad: a.bad + stats[t].bad }), { m2: 0, m3: 0, m4: 0, bad: 0 });
  ok('every hit pays exactly one, two or three extra fees (2x / 3x / 4x), and 4x is the rarest', all.bad === 0 && all.m4 < all.m2 && all.m4 < all.m3 && all.m4 > 0,
     `2x ${all.m2}, 3x ${all.m3}, 4x ${all.m4}, odd ${all.bad}`);
  ok('...and TestRat sees the big "x YOUR FEE!" title', seen.some(s => /YOUR FEE/.test(s)), `${seen.length} titles`);
  await run('clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

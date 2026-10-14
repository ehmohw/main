// 2.74: Block Party keeps you in the room; a failed puzzle's mobs go on solve
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const H = mk(run); const A = await bot('TestRat'); await sleep(2500);
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');
  await run('function bm:admin/room_party'); await H.heist('levers', 'a', 1); await H.begin(); await sleep(1000);
  const q = (await H.qs('party'))[0];
  const local = async () => H.local('party', q);
  await H.at('party', q, `tp TestRat ${rel(12, 4, 12)}`); await sleep(1200);
  ok('Block Party starts when you walk in', (await H.sc('party', q, 'bm.gvs')) >= 1);
  // stand off the called colour: drop through; you land on the pad, not in the void
  let worst = 0, inroom = true;
  for (let t = 0; t < 40; t++) {
    const p = await local(); if (!p) { inroom = false; break; }
    if (p[0] < -0.5 || p[0] > 24.5 || p[2] < -0.5 || p[2] > 24.5 || p[1] < -1) inroom = false;
    await sleep(500);
  }
  ok('Rounds come and go: you never leave the room', inroom);
  const lv = await local();
  await H.at('party', q, 'function bm:p70/ctx'); await H.at('party', q, 'function bm:p112/party/end'); await sleep(800);
  const p = await local();
  ok('It ends: you\'re set down in the middle of the room (not under it)', p && Math.abs(p[0] - 12.5) < 1.5 && Math.abs(p[2] - 12.5) < 1.5 && p[1] > 3, `${p}`);
  await run('function bm:admin/prime_chance'); await run('function bm:admin/fork_chance'); await run('function bm:admin/traps_chance'); await run('function bm:admin/curse_chance'); await run('function bm:admin/rooms_any');
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

// 3.0g: A SPIRE'S CHECKPOINT IS THE HEIST'S, NOT THE ROOM NUMBER'S - as a regular player (rcon sets the stage: a Tier III heist
// of Spires). TestRat touches the gold checkpoint; the crew fails the attempt (a fresh plan is laid - the same rooms at the same
// numbers): his checkpoint is gone, and a fall in the new Spire takes him back to the START, not halfway up. He touches it again
// and leaves the heist: gone again. A new heist: no checkpoint carried in.
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel, fnText } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = mk(run); const { num, at, qs, go, heist, begin, local } = H;
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  ok('TestRat is a regular player (no operator commands)', await new Promise(r => { const n0 = A.chats.length; A.cmd('gamemode creative');
    setTimeout(() => r(A.chats.slice(n0).some(c => /unknown or incomplete|Unknown command/i.test(c))), 1200); }));
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');
  const cpk = () => num('scoreboard players get TestRat bm.gvcpk');
  const fell = fnText('p112/spire/fell'); const cp = fell.match(/run tp @s (~\S* ~\S* ~\S*)\n/)[1];

  await heist('spire', 'a', 3); await begin();
  let Q = await qs('spire'); const q = Q[0];
  ok('A heist of Spires', Q.length >= 1, `${Q}`);
  await go('spire', q, 2, 12); await at('spire', q, `tp TestRat ${cp}`); await sleep(500);
  ok('He touches the gold checkpoint: it\'s his', (await cpk()) === q, `${await cpk()}`);

  // ---- the attempt fails: a fresh plan (same crew)
  const GI = await num('scoreboard players get TestRat bm.gvi');
  await run(`scoreboard players set #fl${GI - 1} bm.gvfail 1`);
  ok('The attempt fails: a fresh plan is laid', await wait(8000, async () => /BEGIN/.test(A.chats.slice(-6).join(' '))), A.chats.slice(-3).join(' | ').slice(0, 160));
  ok('...and his checkpoint is gone with the old plan', (await cpk()) < 1, `${await cpk()}`);
  await begin(); Q = await qs('spire');
  ok('...the new plan has a Spire at the same number', Q.includes(q), `${Q}`);
  await go('spire', q, 2, 12); await sleep(300);
  await at('spire', q, `tp TestRat ${rel(18, 4, 20)}`); await sleep(600);
  const l = await local('spire', q);
  ok('A fall into the new Spire\'s hay: back to the START (no half-room skip)', l && l[0] < 3 && l[1] < 4.5, `${l}`);

  // ---- touched again, and the heist left
  await at('spire', q, `tp TestRat ${cp}`); await sleep(500);
  ok('He touches the checkpoint again', (await cpk()) === q);
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(2500);
  ok('Leaving the heist clears it', (await cpk()) < 1, `${await cpk()}`);

  // ---- a new heist: nothing carried in
  await run('scoreboard players set TestRat bm.gvcpk ' + q);           // (as if left over from an old world)
  await heist('spire', 'a', 3);
  ok('A new heist starts with no checkpoint', (await cpk()) < 1, `${await cpk()}`);

  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  await run('function bm:admin/prime_chance'); await run('function bm:admin/fork_chance'); await run('function bm:admin/traps_chance'); await run('function bm:admin/curse_chance');
  await run('function bm:admin/rooms_any'); await run('function bm:admin/variant_random');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

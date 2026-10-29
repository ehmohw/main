// 2.98a: THE UNDERCROWN's SOUNDTRACK (phase240) as a regular (non-op) player - what the client actually hears (the sound and
// stop-sound packets, on the music channel). rcon sets the stage - the bot in the Undercrown, the trials solved (the dungeon's
// bm.pz), a Dread foe set beside it and taken away, the Sovereign's fall - and the bot listens: from silence, the swell, then the
// Descent 2 s on; a tier solved: the swell over the last bar of a section, the next tier on its boundary (a whole number of
// 16 s sections into the old one); a foe near: the fight on the next bar (an even second), the old track stopped; the foe gone:
// back through the swell on the fight's section boundary; the deep fight from the Drowned Ward down; the Last Door; after the
// fall, Aurel; leaving the Undercrown stops it.
//   node t313.js
const { bot, rcon, sleep } = require('./lib_resp');
const OX = 1536, OZ = -1536;
const N = 'execute in minecraft:the_nether run ';

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 100) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { const v = await fn(); if (v) return v; await sleep(step); } return null; };
  const pos = async (sel) => { const m = (await run(`${N}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const DG = '@e[type=minecraft:marker,tag=bm.dg,tag=bm.d_under,limit=1]';
  const progress = async (n) => run(`${N}scoreboard players set ${DG} bm.pz ${n}`);
  // (the next time the client is told to play a sound, after t0, on the music channel)
  const heard = (name, t0, ms) => wait(ms, async () => A.sounds.find(s => s.name === `bm:music.${name}` && s.cat === 1 && s.t >= t0));
  const off = (dt, grid) => { const r = ((dt / 1000) % grid + grid) % grid; return Math.min(r, grid - r); };   // (how far from the grid, s)

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('tag TestRat add bm.lkpass');      // (2.99a: phase251's pass - this test sets its stages by teleport; t322 plays the lockout itself)
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('scoreboard players set #ufell bm.p2 0');
  if (+((await run('scoreboard players get #uver bm.p2')).match(/has (-?\d+)/) || [0, 0])[1] < 1) {
    await run('function bm:admin/under/place');
    await wait(240000, async () => /has [1-9]/.test(await run('scoreboard players get #uver bm.p2')), 2000);
  }
  await run(`${N}forceload add ${OX} ${OZ} ${OX + 223} ${OZ + 223}`); await sleep(3000);
  const hub = await pos(DG);
  ok('the stage: the Undercrown is there (its controller found)', !!hub);
  // (arrive, and let a long-idle dungeon reset itself before the stage is set)
  await run(`${N}tp TestRat ${hub[0]} ${hub[1] + 1} ${hub[2]}`); await sleep(4000);
  await run(`${N}kill @e[tag=bm.udread,x=${hub[0]},y=${hub[1]},z=${hub[2]},distance=..40]`);
  await progress(0);

  // ---- FROM SILENCE: the swell, the Descent two seconds on
  let t0 = Date.now(); A.sounds.length = 0; A.stops.length = 0;
  await run('execute as TestRat run function bm:p240/stop');
  const sw = await heard('uc_swell', t0, 4000);
  const d1 = sw && await heard('uc_t1', sw.t, 4000);
  ok('inside, trials 0 solved: the swell leads in', !!sw);
  ok('...and THE DESCENT begins 2 s after it, on the music channel', d1 && Math.abs(d1.t - sw.t - 2000) < 700, d1 ? `${d1.t - sw.t} ms` : 'nothing');
  ok('...the Nether\'s own music is silenced in the Undercrown (its biome plays the silence)',
     /gv_silence/.test(require('fs').readFileSync(require('path').join(__dirname, '../../out_p2/BlackMarket_DP/data/bm/worldgen/biome/undercrown.json'), 'utf8')));

  // ---- A WARD CLEARED: the next tier on a section boundary, the swell over the bar before it
  await sleep(3000); await progress(5); t0 = Date.now();
  const d2 = await heard('uc_t2', t0, 20000);
  const sw2 = d2 && A.sounds.filter(s => s.name === 'bm:music.uc_swell' && s.t < d2.t).pop();
  ok('the Frozen Ward behind (5 solved): THE HEXED DARK', !!d2);
  ok('...on a section boundary of the Descent (a whole number of 16 s in)', d2 && d1 && off(d2.t - d1.t, 16) < 0.7, d2 && d1 ? `${((d2.t - d1.t) / 1000).toFixed(2)} s in` : '');
  ok('...the swell over the bar before it', sw2 && Math.abs(d2.t - sw2.t - 2000) < 700, sw2 ? `${d2.t - sw2.t} ms` : 'none');
  ok('...the Descent stopped as it came in', A.stops.some(s => /uc_t1/.test(s.sound || '') && Math.abs(s.t - d2.t) < 700));

  // ---- A FIGHT: on the next bar
  await sleep(2500);
  const foe = `summon minecraft:zombie ${hub[0] + 4} ${hub[1] + 1} ${hub[2]} {NoAI:1b,Silent:1b,PersistenceRequired:1b,Tags:["bm.udread","bm.t313"]}`;
  t0 = Date.now(); await run(N + foe);
  const c1 = await heard('uc_c1', t0, 4000);
  ok('a Dread foe near: THE THRALLS cut in within a bar or so', c1 && c1.t - t0 < 3300, c1 ? `${c1.t - t0} ms` : 'nothing');
  ok('...on a bar of the Hexed Dark (an even second in)', c1 && off(c1.t - d2.t, 2) < 0.6, c1 ? `${((c1.t - d2.t) / 1000).toFixed(2)} s in` : '');
  ok('...the Hexed Dark stopped', A.stops.some(s => /uc_t2/.test(s.sound || '') && c1 && Math.abs(s.t - c1.t) < 700));
  await sleep(3000); await run(`${N}kill @e[tag=bm.t313]`); t0 = Date.now();
  const back = await heard('uc_t2', t0, 26000);
  ok('the foe gone: back to the Hexed Dark', !!back);
  ok('...not before the fight\'s 6 s of calm', back && back.t - t0 > 5000, back ? `${back.t - t0} ms` : '');
  ok('...on a section boundary of the fight, through the swell', back && off(back.t - c1.t, 16) < 0.7 && A.sounds.some(s => s.name === 'bm:music.uc_swell' && Math.abs(back.t - s.t - 2000) < 700),
     back ? `${((back.t - c1.t) / 1000).toFixed(2)} s in` : '');

  // ---- THE DEEP: the Drowned Ward, its fight
  await progress(10);
  const d3 = await heard('uc_t3', Date.now(), 20000);
  ok('the Hexed Ward behind (10 solved): THE DROWNED DEEP', !!d3);
  await sleep(1000); t0 = Date.now(); await run(N + foe);
  ok('...a foe there: THE DREAD KNIGHTS (the deep fight)', !!(await heard('uc_c2', t0, 4000)));
  await run(`${N}kill @e[tag=bm.t313]`);
  ok('...and back to the Drowned Deep', !!(await heard('uc_t3', Date.now(), 26000)));

  // ---- DOWN TO THE THRONE
  for (const [n, name, what] of [[15, 'uc_t4', 'THE THRONE GATE (the Shards)'], [16, 'uc_t5', 'A THOUSAND EYES (the Stair)'], [17, 'uc_t6', 'THE LAST DOOR (every trial solved)']]) {
    await progress(n);
    ok(`${n} solved: ${what}`, !!(await heard(name, Date.now(), 20000)));
  }

  // ---- THE FALL: Aurel, once
  await run('scoreboard players set #ufell bm.p2 1'); t0 = Date.now();
  ok('after the Sovereign\'s fall: AUREL', !!(await heard('uc_after', t0, 20000)));
  await sleep(3000);
  ok('...once (it does not start over while it plays)', A.sounds.filter(s => s.name === 'bm:music.uc_after' && s.t >= t0).length === 1);
  await run('scoreboard players set #ufell bm.p2 0');

  // ---- LEAVING
  t0 = Date.now(); await run('execute in minecraft:overworld run tp TestRat 0 200 0'); await sleep(2500);
  ok('out of the Undercrown: its music stops', A.stops.some(s => s.t >= t0 && /uc_/.test(s.sound || '')) && /has 0/.test(await run('scoreboard players get TestRat bm.ucm')));

  await progress(0);
  await run(`${N}forceload remove ${OX} ${OZ} ${OX + 223} ${OZ + 223}`);
  await run('tag TestRat remove bm.lkpass');      // (phase251's pass off again)
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();

// t416 (3.2e): NULLIFIED, AND THE CAMERA HOLDS STILL - as a regular (non-op) player; rcon sets the stage only (the effects a follower
// or gear would grant, and the Nullify a boss's pulse lays on, p280/on).
//   The owner: "the player's screen can constantly jerk in and out because, if they have speed buffs, the speed buffs are constantly
//   being granted and cleared". Speed moves the camera (FOV); a follower re-grants it every second and Nullify cleared it every tick.
//   Now Speed is left on and its push cancelled (a movement-speed modifier, bm:nul_speed): while Nullified, re-granted every second,
//   Speed is never off (no flicker) and you walk at your own pace (movement_speed back to the base 0.1); Strength is still stripped;
//   when it ends, Speed's push is back (0.14 at Speed II) and the modifier gone.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('scoreboard players reset TestRat bm.nul');
  const spd = async () => +(((await run('attribute TestRat minecraft:movement_speed get')).match(/is (-?[\d.]+)/) || [])[1]);
  const hasEff = async e => /Found|minecraft:/.test(await run(`data get entity TestRat active_effects[{id:"minecraft:${e}"}].id`)) && !/Found no/.test(await run(`data get entity TestRat active_effects[{id:"minecraft:${e}"}].id`));
  await run('effect give TestRat minecraft:speed 30 1 true'); await sleep(300);
  const s0 = await spd();
  ok('Speed II on: faster than your own pace (0.1)', s0 > 0.13, `speed ${s0}`);
  // (Nullified for 10 s - and Speed re-granted every second, as a follower does; Strength too)
  await run('scoreboard players set #nd bm.rng 200'); await run('execute as TestRat at @s run function bm:p280/on');
  let off = 0, n = 0, sMin = 9, sMax = 0;
  for (let i = 0; i < 24; i++) {
    if (i % 4 === 0) { await run('effect give TestRat minecraft:speed 2 1 true'); await run('effect give TestRat minecraft:strength 2 1 true'); }
    await sleep(250); n++;
    if (!(await hasEff('speed'))) off++;
    const s = await spd(); sMin = Math.min(sMin, s); sMax = Math.max(sMax, s);
  }
  ok('Nullified, Speed re-granted every second: it never drops off (no flicker)', off === 0, `${off}/${n} samples without Speed`);
  ok('...and you walk at your own pace - its push cancelled, steadily (movement speed ~0.1)', Math.abs(sMin - 0.1) < 0.002 && Math.abs(sMax - 0.1) < 0.002, `${sMin.toFixed(4)}..${sMax.toFixed(4)}`);
  ok('...Strength still stripped', !(await hasEff('strength')));
  await run('scoreboard players set TestRat bm.nul 1'); await sleep(600); await run('effect give TestRat minecraft:speed 30 1 true'); await sleep(1500);
  const s1 = await spd();
  ok('when it ends: Speed\'s push is back (Speed II: 0.14), the modifier gone', Math.abs(s1 - 0.14) < 0.002, `speed ${s1} (with the modifier left on it would be ~0.1)`);
  await run('effect clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

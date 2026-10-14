// v2.46: Pearlman visits like a wandering trader - one roll a day, 10% rising by 10 to 30%, reset when he comes
const { bot, rcon, sleep } = require('./lib');
const X = 10400, Y = 200, Z = 10400;
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (n) => { const m = (await run(`scoreboard players get ${n} bm.bm`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  await run('gamemode survival TestRat'); await run(`forceload add ${X - 20} ${Z - 20} ${X + 20} ${Z + 20}`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(2000);
  await run(`fill ${X - 15} ${Y} ${Z - 15} ${X + 15} ${Y} ${Z + 15} grass_block`); await run(`fill ${X - 15} ${Y + 1} ${Z - 15} ${X + 15} ${Y + 30} ${Z + 15} air`);
  await run('kill @e[tag=bm.pearl]'); await run('kill @e[tag=bm.pearld]'); await sleep(300);
  ok('A day lasts 20 minutes of play', (await sc('#pmcd')) > 0 && (await sc('#pmcd')) <= 1200, '' + await sc('#pmcd'));
  // a miss: chance 0 -> no visit, the chance climbs by 10
  await run('scoreboard players set #pmch bm.bm 0'); await run('scoreboard players set #pmcd bm.bm 1'); await sleep(2200);
  ok('A missed roll: no Pearlman, and tomorrow\'s chance goes up by 10', (await cnt('@e[tag=bm.pearl]')) === 0 && (await sc('#pmch')) === 10 && (await sc('#pmcd')) > 1190, `chance ${await sc('#pmch')}, next roll in ${await sc('#pmcd')} s`);
  await run('scoreboard players set #pmch bm.bm 30'); await run('scoreboard players set #r bm.rng 0'); 
  // cap: from 30 a miss stays at 30 (force a miss by putting another Pearlman... use chance 30 and loop until a miss)
  let capped = null; for (let i = 0; i < 12 && capped === null; i++) { await run('scoreboard players set #pmch bm.bm 30'); await run('scoreboard players set #pmcd bm.bm 1'); await sleep(1500);
    if (await cnt('@e[tag=bm.pearl]')) { await run('kill @e[tag=bm.pearl]'); await run('kill @e[tag=bm.pearld]'); continue; } capped = await sc('#pmch'); }
  ok('...it tops out at 30%', capped === 30, '' + capped);
  // a sure roll: he comes, near the player, and the chance resets to 10
  await run('scoreboard players set #pmch bm.bm 100'); await run('scoreboard players set #pmcd bm.bm 1'); await sleep(2200);
  ok('A winning roll: Pearlman waddles up to you', (await cnt(`@e[type=villager,tag=bm.pearl,x=${X},y=${Y},z=${Z},distance=..12]`)) === 1, '');
  ok('...and the chance resets to 10%', (await sc('#pmch')) === 10, '' + await sc('#pmch'));
  await run('scoreboard players set #pmch bm.bm 100'); await run('scoreboard players set #pmcd bm.bm 1'); await sleep(2200);
  ok('No second Pearlman while one is visiting', (await cnt('@e[type=villager,tag=bm.pearl]')) === 1);
  await run('kill @e[tag=bm.pearl]'); await run('kill @e[tag=bm.pearld]'); await run('scoreboard players set #pmch bm.bm 10');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

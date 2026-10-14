// skiff: the hull boards the skiff (2nd passenger) at the right height, steps off when the pilot leaves, re-boards after them
const { bot, rcon, sleep } = require('./lib');
const X = 5000, Y = 100, Z = 5000;
(async () => {
  const R = await rcon(); const run = (c) => R.run(c);
  const A = await bot('TestRat'); await sleep(1000);
  const res = []; const ok = (n, p, d) => { res.push(p); console.log((p ? 'PASS ' : 'FAIL ') + n + '  -- ' + d); };
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(500);
  await run('loot give TestRat loot bm:items/skiff_key'); A.slot(0); await sleep(400);
  A.use(); await sleep(250); A.release(); await sleep(800);
  const y = async (sel) => parseFloat((await run(`data get entity ${sel} Pos[1]`)).replace(/.*: /, ''));
  const tr = async () => parseFloat((await run('data get entity @e[type=minecraft:item_display,tag=bm.skdisp,limit=1] transformation.translation[1]')).replace(/.*: /, ''));
  const onGhast = async () => (await run('execute as @e[type=minecraft:item_display,tag=bm.skdisp] on vehicle if entity @s[type=minecraft:happy_ghast]')).includes('passed');
  const pilotFirst = async () => (await run('execute as @e[type=minecraft:happy_ghast,tag=bm.skiff] if predicate bm:p29/has_vehicle')).includes('x');
  let G = await y('@e[type=minecraft:happy_ghast,tag=bm.skiff,limit=1]'), D = await y('@e[type=minecraft:item_display,tag=bm.skdisp,limit=1]'), T = await tr();
  ok('piloted: the hull rides the skiff at its middle', await onGhast() && Math.abs(D + T - (G + 1.0)) < 0.05, `ghast ${G}, hull ${D} + ${T} = ${(D + T).toFixed(2)} (want ${(G + 1).toFixed(2)})`);
  // fly: the hull keeps up on the same tick
  await run('execute as @e[type=minecraft:happy_ghast,tag=bm.skiff] at @s run tp @s ~3 ~2 ~3'); await sleep(150);
  const gx = (await run('data get entity @e[type=minecraft:happy_ghast,tag=bm.skiff,limit=1] Pos[0]')).replace(/.*: /, ''), dx = (await run('data get entity @e[type=minecraft:item_display,tag=bm.skdisp,limit=1] Pos[0]')).replace(/.*: /, '');
  ok('it moves with the skiff', Math.abs(parseFloat(gx) - parseFloat(dx)) < 0.01, `ghast x ${gx}, hull x ${dx}`);
  // the pilot leaves: hull steps off; the pilot gets back on (right-click the skiff): first passenger again, hull re-boards
  await run('ride TestRat dismount'); await sleep(400);
  const off = !(await onGhast()); T = await tr();
  ok('pilot gone: the hull steps off and parks', off && Math.abs(T - 1.0) < 0.01, `on skiff ${!off}, translation ${T}`);
  await run('ride TestRat mount @e[type=minecraft:happy_ghast,tag=bm.skiff,limit=1]'); await sleep(400);
  const first = await run('execute as @e[type=minecraft:happy_ghast,tag=bm.skiff] on controller if entity @s[type=minecraft:player]');
  ok('back aboard: the hull re-boards, the pilot still steers', (await onGhast()) && first.includes('passed'), `controller: ${first.slice(0, 80)}`);
  await run('execute as @e[tag=bm.skiff] at @s run function bm:p35/skiff/gone').catch(() => {});
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });

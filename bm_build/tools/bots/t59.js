const { bot, rcon, sleep } = require('./lib');
const X = 12200, Y = 200, Z = 12200; const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const sc = async (who, o) => ((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [])[1];
  await run(`fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} stone`); await run(`fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 6} ${Z + 10} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..30]`); await run('kill @e[type=wolf,tag=bm.frogpet]'); await run('kill @e[type=wolf,tag=bm.cecilpet]');
  await run('clear TestRat'); await run('scoreboard players reset TestRat bm.fgcd'); await run('tag TestRat remove bm.fgowed'); await run('scoreboard players reset TestRat bm.cpcd');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(1500);
  // Cecil v2 (a follower leaves within seconds if its owner doesn't carry its summoning item: give them first)
  await run('loot give TestRat loot bm:items/cecil_gem'); await sleep(300);
  await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(1500);
  ok('Cecil comes in his new (shorter, slimmer) look', /cec2_head/.test(await run('data get entity @e[tag=bm.cp_head,limit=1] item.components')) && (await cnt('@e[tag=bm.cpet,tag=bm.cp2]')) === 5);
  const hy = (await run('data get entity @e[tag=bm.cp_head,limit=1] Pos[1]')).match(/([\d.]+)d/)[1], wy = (await run('data get entity @e[type=wolf,tag=bm.cecilpet,limit=1] Pos[1]')).match(/([\d.]+)d/)[1];
  ok('...his hood sits 0.94 above the ground (was 1.38)', Math.abs(hy - wy - 0.94) < 0.05, (hy - wy).toFixed(2));
  await run('kill @e[type=wolf,tag=bm.cecilpet]'); await sleep(800);
  // (fainting - the 2-minute rest, coming back by itself - is played through as a player in t219; the Frog's hut steps were retired with it)
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

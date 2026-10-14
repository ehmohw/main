const { bot, rcon, sleep } = require('./lib');
const X = 12000, Y = 200, Z = 12000; const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  await run(`fill ${X - 6} ${Y} ${Z - 6} ${X + 6} ${Y} ${Z + 6} stone`); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(1000);
  await run(`kill @e[type=item_display,x=${X},y=${Y},z=${Z},distance=..20]`);
  const sum = (tag, v) => run(`summon item_display ${X + 3} ${Y + 1} ${Z} {Tags:["${tag}","bm.t57","bm.t57${v}"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"bm:rat3d_${v}"}}}`);
  await sum('bm.rat_sprite', 'chef'); await sum('bm.rat_sprite', 'lucky'); await sum('bm.walker', 'pirate'); await sleep(1500);
  const sc = async (t, o) => ((await run(`scoreboard players get @e[tag=${t},limit=1] ${o}`)).match(/has (-?\d+)/) || [])[1];
  ok('Each rat learns its variant', (await sc('bm.t57chef', 'bm.rv')) > 0 && (await sc('bm.t57lucky', 'bm.rv')) > 0, `${await sc('bm.t57chef', 'bm.rv')} ${await sc('bm.t57lucky', 'bm.rv')}`);
  // play the chef's pancake routine (q 8 = the job, after the 7 fidgets)
  await run('execute as @e[tag=bm.t57chef] at @s run function bm:p64/go {q:8}');
  const seen = new Set(); for (let i = 0; i < 16; i++) { const m = (await run('data get entity @e[tag=bm.t57chef,limit=1] item.components."minecraft:custom_model_data".strings[0]')).match(/"(\w+)"/); if (m) seen.add(m[1]); await sleep(250); }
  ok('The chef flips his pancake (all four frames play)', ['chef_1', 'chef_2', 'chef_3', 'chef_4'].every(p => seen.has(p)), [...seen].join(','));
  await sleep(1500);
  ok('...then rests', !/strings/.test(await run('data get entity @e[tag=bm.t57chef,limit=1] item.components')) || (await sc('bm.t57chef', 'bm.rq')) > 0);
  // fidgets start on their own
  const fid = new Set(); for (let i = 0; i < 60; i++) { const m = (await run('data get entity @e[tag=bm.t57lucky,limit=1] item.components."minecraft:custom_model_data".strings[0]')).match(/"(\w+)"/); if (m) fid.add(m[1]); await sleep(250); }
  ok('Lucky fidgets by himself (several different poses in 15 s)', fid.size >= 3, [...fid].join(','));
  // walker: walking frames while on the move
  await run('tag @e[tag=bm.t57pirate] add bm.wmov'); const wk = new Set();
  for (let i = 0; i < 8; i++) { const m = (await run('data get entity @e[tag=bm.t57pirate,limit=1] item.components."minecraft:custom_model_data".strings[0]')).match(/"(\w+)"/); if (m) wk.add(m[1]); await sleep(110); }
  ok('A walker steps through the walk cycle', ['walk1', 'walk2', 'walk3', 'walk4'].filter(p => wk.has(p)).length >= 3, [...wk].join(','));
  await run('kill @e[tag=bm.t57]');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

const { bot, rcon, sleep } = require('./lib');
const X = 12400, Y = 200, Z = 12400; const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  await run(`fill ${X - 6} ${Y} ${Z - 6} ${X + 6} ${Y} ${Z + 6} stone`); await run(`fill ${X - 6} ${Y + 1} ${Z - 6} ${X + 6} ${Y + 6} ${Z + 6} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..20]`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 4.5}`); await sleep(1000);
  await run(`summon villager ${X + 0.5} ${Y + 1} ${Z + 0.5} {NoAI:1b,Tags:["bm.npc","bm.npc_wizard","bm.t62"],Silent:1b}`);
  // an old, tall market Cecil body is swapped out for the new look
  await run(`summon item_display ${X + 0.5} ${Y + 1} ${Z + 0.5} {Tags:["bm.npc","bm.cecil","bm.cec_body"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"bm:cec_body"}}}`);
  await run(`execute as @e[tag=bm.t62] at @s if entity @e[type=minecraft:item_display,tag=bm.cec_body,tag=!bm.cec2,distance=..1] run function bm:p45/cecil/rerig`); await sleep(500);
  console.log(await cnt('@e[tag=bm.cecil,tag=bm.cec2]'), await cnt('@e[tag=bm.cec_body,tag=!bm.cec2]'), await cnt('@e[tag=bm.cecil]'), (await run('data get entity @e[tag=bm.cec_head,tag=bm.cec2,limit=1] Tags')).slice(-90));
  ok('Market Cecil wears the new model (5 parts incl. the free arm, old body gone)', (await cnt('@e[tag=bm.cecil,tag=bm.cec2]')) === 5 && (await cnt('@e[tag=bm.cec_body,tag=!bm.cec2]')) === 0 && (await cnt('@e[tag=bm.cec_larm]')) === 1);
  const hy = (await run('data get entity @e[tag=bm.cec_head,tag=bm.cec2,limit=1] Pos[1]')).match(/([\d.]+)d/)[1];
  ok('...his hood sits at the new height (0.94)', Math.abs(hy - (Y + 1) - 0.94) < 0.05, (hy - Y - 1).toFixed(2));
  const seen = new Set(); for (let i = 0; i < 8; i++) { seen.add(await run('data get entity @e[tag=bm.cec_head,tag=bm.cec2,limit=1] transformation.translation')); await sleep(400); }
  ok('...and he still breathes (idle animation)', seen.size >= 2, [...seen].map(x => x.slice(-22)).join(' / '));
  await run('kill @e[tag=bm.cecil]'); await run('kill @e[tag=bm.t62]');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

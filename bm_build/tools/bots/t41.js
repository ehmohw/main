// v2.38: the follower cap (3), the shifter and Emma's menu don't cross, Emma's lore lines
const { bot, rcon, sleep } = require('./lib');
const X = 9800, Y = 100, Z = 9800;
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const score = async (who, obj) => { const r = await run(`scoreboard players get ${who} ${obj}`); const m = r.match(/has (-?\d+)/); return m ? +m[1] : null; };
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run(`forceload add ${X - 20} ${Z - 20} ${X + 20} ${Z + 20}`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2500);
  await run(`fill ${X - 15} ${Y} ${Z - 15} ${X + 15} ${Y} ${Z + 15} grass_block`); await run(`fill ${X - 15} ${Y + 1} ${Z - 15} ${X + 15} ${Y + 6} ${Z + 15} air`);
  await run('kill @e[type=cat,tag=bm.emmapet]'); await run('kill @e[type=wolf,tag=bm.cecilpet]'); await run('kill @e[type=wolf,tag=bm.frogpet]'); await run('kill @e[type=wolf,tag=bm.mercpet]');
  for (const o of ['bm.emcd', 'bm.cpcd']) await run(`scoreboard players reset TestRat ${o}`); await sleep(1500);
  await run('execute as TestRat at @s run function bm:p46/pet/try_summon'); await sleep(300);
  await run('execute as TestRat at @s run function bm:p57/try_summon'); await sleep(300);
  await run('execute as TestRat at @s run function bm:p20/frog/summon'); await sleep(800);
  await run('execute as TestRat run function bm:p58/count');
  ok('three followers counted (Cecil, Emma, the Frog)', (await score('#fc', 'bm.rng')) === 3);
  await run('kill @e[type=wolf,tag=bm.cecilpet]'); await sleep(1500); await run('scoreboard players reset TestRat bm.cpcd');
  await run(`summon wolf ${X + 2} ${Y + 1} ${Z + 2} {Tags:["bm.cecilpet","bm.t41"]}`); await run('data modify entity @e[tag=bm.t41,limit=1] Owner set from entity TestRat UUID');
  A.bars.length = 0; await run('execute as TestRat at @s run function bm:p46/pet/try_summon'); await sleep(600);
  ok('a fourth (Cecil) is refused: "send one home first"', (await cnt('@e[type=wolf,tag=bm.cecilpet,tag=!bm.t41]')) === 0 && A.bars.some(b => b.includes('Send one home')), A.bars.slice(-1)[0]);
  await run('kill @e[type=wolf,tag=bm.frogpet]'); await sleep(300);
  await run('give TestRat totem_of_undying[custom_data={bm:"medallion"}] 2');
  // the frog's hire with a 4th... (Emma + merc + Cecil? Cecil was refused, so 2 now: summon Cecil to make 3)
  await run('execute as TestRat at @s run function bm:p46/pet/try_summon'); await sleep(500);
  await run('execute as TestRat at @s run function bm:p20/frog/hire'); await sleep(500);
  { const fr = await cnt('@e[type=wolf,tag=bm.frogpet]'), md = await run('clear TestRat totem_of_undying[custom_data~{bm:"medallion"}] 0'), cc = await cnt('@e[type=wolf,tag=bm.cecilpet]'); ok('hiring the Frog as a 4th: refused, and no Medallion taken', fr === 0 && /Found 2 /.test(md), `frog ${fr} cecil ${cc} ${md}`); }
  await run('kill @e[tag=bm.t41]'); await sleep(300);
  await run('execute as TestRat at @s run function bm:p20/frog/hire'); await sleep(500);
  ok('...with room, the Frog signs on (a Medallion)', (await cnt('@e[type=wolf,tag=bm.frogpet]')) === 1 && /Found 1 /.test(await run('clear TestRat totem_of_undying[custom_data~{bm:"medallion"}] 0')));
  // menus: Emma's menu open, a shifter button is stale; shifter open, Emma's button is stale
  await run('give TestRat totem_of_undying[custom_data={bm:"dimension_shifter"}] 1'); await run('give TestRat totem_of_undying[custom_data={bm:"emma_ribbon"}] 1');
  await run('scoreboard players reset TestRat bm.shcd');
  await run('tag @e[type=cat,tag=bm.emmapet] add bm.emsel2'); await run('execute as TestRat run function bm:p57/menu'); await run('tag @e[type=cat,tag=bm.emmapet] remove bm.emsel2');
  ok("Emma's menu opens (menu 960)", (await score('TestRat', 'bm.menu')) === 960);
  A.bars.length = 0; A.cmd('trigger bm.act set 7201'); await sleep(800);
  ok('...a Dimension Shifter button pressed now: "menu has closed", no shift', A.bars.some(b => b.includes('menu has closed')) && !((await score('TestRat', 'bm.shcd')) > 0), A.bars.slice(-1)[0]);
  await run('execute as TestRat at @s run function bm:p33/shift/use');
  ok('the Shifter menu opens (menu 900)', (await score('TestRat', 'bm.menu')) === 900);
  const m0 = await score('@e[type=cat,tag=bm.emmapet,limit=1]', 'bm.emm');
  A.bars.length = 0; A.cmd('trigger bm.act set 7302'); await sleep(800);
  ok("...an Emma button pressed now: stale, her mode unchanged", A.bars.some(b => b.includes('menu has closed')) && (await score('@e[type=cat,tag=bm.emmapet,limit=1]', 'bm.emm')) === m0);
  await run('execute as TestRat at @s run function bm:p33/shift/use'); A.bars.length = 0; A.cmd('trigger bm.act set 7201'); await sleep(800);
  ok('...and the Shifter itself still answers ("already in the Overworld")', A.bars.some(b => b.includes('already in the Overworld')), A.bars.slice(-1)[0]);
  // lore
  A.chats.length = 0; await run('tag TestRat remove bm.emhint'); await run('clear TestRat'); await run('execute as TestRat run function bm:p57/hint'); await sleep(400);
  ok("Cecil's hint tells her story", A.chats.some(c => c.includes('Apophiss')), A.chats.slice(-1)[0]);
  await run('kill @e[type=cat,tag=bm.emmapet]'); await run('kill @e[type=wolf,tag=bm.cecilpet]'); await run('kill @e[type=wolf,tag=bm.frogpet]');
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..30]`); await run(`forceload remove ${X - 20} ${Z - 20} ${X + 20} ${Z + 20}`);
  console.log(`\n${res.filter(x => x).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.log('FATAL', e); process.exit(1); });

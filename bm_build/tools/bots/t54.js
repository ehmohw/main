const { bot, rcon, sleep } = require('./lib');
const X = 11700, Y = 200, Z = 11700; const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  await run(`fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} stone`); await run(`fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 6} ${Z + 12} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('kill @e[type=wolf,tag=bm.cecilpet]'); await run('clear TestRat'); await run('gamemode survival TestRat');
  await run('scoreboard players reset TestRat bm.cpel'); await run('scoreboard players reset TestRat bm.cpcd');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(4000);
  await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(1500);
  ok('Cecil summoned with his own (poison) look', /"bm:cec2_head"/.test(await run('data get entity @e[type=item_display,tag=bm.cp_head,limit=1] item.components')));
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/gem_fire'); await sleep(300);
  const wp = (await run('data get entity @e[type=wolf,tag=bm.cecilpet,limit=1] Pos')).match(/\[([-\d.]+)d, ([-\d.]+)d, ([-\d.]+)d\]/);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} facing ${wp[1]} ${+wp[2] + 0.4} ${wp[3]}`); await sleep(500);
  const ids = Object.values(A.ents).filter(e => Math.hypot(e.x - X, e.z - Z) < 8).map(e => e.entityId); console.log("ents", Object.keys(A.ents).length, JSON.stringify(Object.values(A.ents).slice(-3).map(e=>[e.type,Math.round(e.x),Math.round(e.z)]))); console.log(JSON.stringify(Object.values(A.ents).slice(0, 2)).slice(0, 300));
  for (const id of ids) A.interact(id); await sleep(800);
  const hd = await run('data get entity @e[type=item_display,tag=bm.cp_head,limit=1] item.components');
  ok('Right-click him with a Fire Gem: his hood and staff turn to fire, the gem is used', /cec2_head_fire/.test(hd) && /cec2_arm_fire/.test(await run('data get entity @e[type=item_display,tag=bm.cp_arm,limit=1] item.components'))
     && !/passed/.test(await run('execute if items entity TestRat weapon.mainhand *')), hd.slice(-40) + ' ids:' + ids.length + ' ' + (A.bars.slice(-1)[0] || ''));
  await run(`summon husk ${X + 0.5} ${Y + 1} ${Z + 6.5} {Tags:["bm.t54"],PersistenceRequired:1b,NoAI:1b,Health:40f,attributes:[{id:"minecraft:max_health",base:40}]}`);
  let fire = 0; for (let i = 0; i < 10 && !fire; i++) { await sleep(500); const f = (await run('data get entity @e[tag=bm.t54,limit=1] Fire')).match(/(-?\d+)s/); if (f && +f[1] > 0) fire = +f[1]; }
  ok('His bolts now set monsters alight', fire > 0, 'Fire ' + fire + ' hp ' + (await run('data get entity @e[tag=bm.t54,limit=1] Health')).slice(-6));
  await run('kill @e[tag=bm.t54]');
  // dismiss + resummon keeps the element
  await run('execute as TestRat at @s run function bm:p46/pet/use'.replace('use', 'use')); 
  await run('kill @e[type=wolf,tag=bm.cecilpet]'); await sleep(1500); await run('scoreboard players reset TestRat bm.cpcd');
  await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(1200);
  ok('Called again later, he is still a fire mage', /cec2_head_fire/.test(await run('data get entity @e[type=item_display,tag=bm.cp_head,tag=!bm.cpfade,limit=1] item.components')));
  await run('kill @e[type=wolf,tag=bm.cecilpet]'); await run('scoreboard players reset TestRat bm.cpcd');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

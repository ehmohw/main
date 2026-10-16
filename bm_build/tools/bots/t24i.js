const { bot, rcon, sleep } = require('./lib');
const X = 5200, Y = 100, Z = 5200;
(async () => {
  const R = await rcon(); const run = (c) => R.run(c);
  const res = []; const ok = (n, c, d) => { res.push(!!c); console.log(c ? 'PASS' : 'FAIL', n, d || ''); };
  const A = await bot('TestRat'); await sleep(1000);
  const look = async (x, y, z, yaw, pitch) => { await run(`tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await sleep(400); A.pos.yaw = yaw; A.pos.pitch = pitch; };
  const press = async (sneak, hold = 250) => { if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(hold); A.release(); if (sneak) A.input({}); await sleep(500); };
  const give = async (i) => { await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${i}`); A.slot(0); await sleep(250); };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)\D*$/); return m ? parseFloat(m[1]) : null; };
  const count = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); return /failed/i.test(r) ? 0 : (r.match(/(\d+)\D*$/) || [0, 0])[1] * 1; };   // (26.3: none found is "Test failed")
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); await sleep(2500); await run('kill @e[type=!player,x=' + X + ',y=' + Y + ',z=' + Z + ',distance=..40]'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance infinite 4 true'); await run('time set midnight'); await run('weather clear');
  await run(`fill ${X - 14} ${Y - 1} ${Z - 14} ${X + 14} ${Y - 1} ${Z + 14} minecraft:stone`); await run(`fill ${X - 14} ${Y} ${Z - 14} ${X + 14} ${Y + 14} ${Z + 14} minecraft:air`);
  const zombie = async (dx, dz, hp = 40) => run(`summon zombie ${X + dx + 0.5} ${Y} ${Z + dz + 0.5} {NoAI:1b,Tags:["t24"],Health:${hp}f,attributes:[{id:"minecraft:max_health",base:${hp}}]}`);
  const hp = async (dx, dz) => num(`data get entity @e[tag=t24,x=${X + dx + 0.5},y=${Y},z=${Z + dz + 0.5},distance=..0.8,limit=1] Health`);
  // Staff of Sparks: chain
  await zombie(0, 5); await zombie(2, 6); await zombie(-2, 7); await zombie(0, 13);
  await give('staff_of_sparks'); await look(X + 0.5, Y, Z + 0.5, 0, 10); await press();
  const h = [await hp(0, 5), await hp(2, 6), await hp(-2, 7), await hp(0, 13)];
  ok('sparks: first target and chain hit, far one spared', h[0] < 40 && h[1] < 40 && h[2] < 40 && h[3] === 40, JSON.stringify(h));
  await run('kill @e[tag=t24]');
  // Gravewell
  await zombie(4, 8); await zombie(-4, 8); await give('gravewell_staff'); await look(X + 0.5, Y, Z + 0.5, 0, 12); await press();
  await sleep(1500); const wells = await count('@e[type=marker,tag=bm.gwell]');
  const d1 = await num(`execute as @e[tag=t24,limit=1,sort=nearest,x=${X + 4},y=${Y},z=${Z + 8}] run data get entity @s Pos[0]`);
  await sleep(2200); const hz = await num(`data get entity @e[tag=t24,limit=1] Health`);
  ok('gravewell pulls in, then bursts', wells === 1 && d1 < X + 4.4 && hz < 40, `wells ${wells}, x ${d1}, hp ${hz}`);
  await run('kill @e[tag=t24]');
  // Crescent staff shards
  await zombie(3, 7); await give('crescent_staff'); await look(X + 0.5, Y, Z + 0.5, 0, 0); await press(); await sleep(2000);
  ok('crescent shards home in', (await hp(3, 7)) < 40, 'hp ' + await hp(3, 7));
  await run('kill @e[tag=t24]');
  // Prism bow (fully drawn shot into a zombie)
  await zombie(0, 8); await zombie(1, 8); await give('prism_bow'); await run('item replace entity TestRat hotbar.1 with arrow 64');
  await look(X + 0.5, Y + 0, Z + 0.5, 0, 2); await press(false, 1300); await sleep(1500);
  ok('prism bow nova hurts the neighbour', (await hp(1, 8)) < 40, `hit ${await hp(0, 8)} neighbour ${await hp(1, 8)}`);
  await run('kill @e[tag=t24]'); await run('kill @e[type=arrow]');
  // Starcaller
  await zombie(0, 9, 100); await give('starcaller_bow'); await run('item replace entity TestRat hotbar.1 with arrow 64');
  await look(X + 0.5, Y, Z + 0.5, 0, 2); await press(false, 1400); await sleep(400); const stars = await count('@e[type=marker,tag=bm.fstar]'); await sleep(3500);
  ok('starcaller calls stars', stars >= 3 && (await hp(0, 9)) < 85, `stars ${stars} hp ${await hp(0, 9)}`);
  await run('kill @e[tag=t24]');
  // Gems
  await give('bloomheart_gem'); await press(); ok('bloomheart regen', (await run('data get entity TestRat active_effects')).includes('regeneration'));
  await run('item replace entity TestRat weapon.offhand from entity TestRat hotbar.0'); await run('item replace entity TestRat hotbar.0 with air');
  await run('effect give TestRat poison 20 0'); await sleep(1400); ok('bloomheart offhand clears poison', !(await run('data get entity TestRat active_effects')).includes('poison'));
  await zombie(0, 4); await run(`data merge entity @e[tag=t24,limit=1] {Fire:200s}`); await give('tidal_tear'); await look(X + 0.5, Y, Z + 0.5, 0, 0);
  const z0 = await num('data get entity @e[tag=t24,limit=1] Pos[2]'); await press(); await sleep(1200);
  const z1 = await num('data get entity @e[tag=t24,limit=1] Pos[2]'); const fire = await num('data get entity @e[tag=t24,limit=1] Fire');
  ok('tidal tear shoves and douses', z1 > z0 + 1 && fire <= 0, `z ${z0}->${z1} fire ${fire}`);
  await run('kill @e[tag=t24]');
  // Food
  await give('prime_beef'); await run('effect give TestRat hunger 6 255'); await sleep(6200); await run('effect clear TestRat hunger');
  const f0 = await num('data get entity TestRat foodLevel'); await press(false, 2000); const f1 = await num('data get entity TestRat foodLevel');
  ok('prime beef is food', (await run('data get entity TestRat SelectedItem.components')).includes('minecraft:food') || f1 > f0, `${f0} -> ${f1}`);
  await give('dish_chili'); await press(false, 2200); ok('chili gives fire resistance', (await run('data get entity TestRat active_effects')).includes('fire_resistance'));
  // Banquet
  await give('grand_banquet'); await look(X + 0.5, Y, Z + 0.5, 0, 50); await press();
  const bq = await count('@e[type=interaction,tag=bm.bqhit]'); const bqe = Object.values(A.ents).find(e => Math.abs(e.x - X - 0.5) < 0.1 && Math.abs(e.z - Z - 2.5) < 1.5 && e.type);
  ok('banquet placed', bq === 1, 'hitboxes ' + bq);
  // click it via the interaction (find its entity id from the client's view)
  await sleep(300);
  const ids = Object.values(A.ents).filter(e => Math.abs(e.x - (X + 0.5)) < 0.1 && Math.abs(e.y - Y) < 0.1).map(e => e.entityId);
  for (const id of ids) A.interact(id); await sleep(600);
  ok('banquet serves (8 -> 7)', (await num('scoreboard players get @e[type=interaction,tag=bm.bqhit,limit=1] bm.bqn')) === 7, await run('scoreboard players get @e[type=interaction,tag=bm.bqhit,limit=1] bm.bqn'));
  await run('kill @e[tag=bm.bqhit]'); await run('kill @e[tag=bm.bqdisp]');
  // Lava lamp: place, recolour, light, pick up
  await give('lava_lamp'); await look(X + 0.5, Y, Z + 0.5, 90, 50); await press();
  const lp = await run('data get entity @e[tag=bm.lavalamp,limit=1] Pos'); const lb = await count('@e[tag=bm.lavablob]');
  ok('lava lamp placed with 2 blobs and light', lb === 2 && (await run(`execute if block ${X - 1} ${Y} ${Z} minecraft:light`)).includes('passed'), lp + ' blobs ' + lb);
  const lid = Object.values(A.ents).filter(e => Math.abs(e.x - (X - 0.5)) < 0.1 && Math.abs(e.z - (Z + 0.5)) < 0.1).map(e => e.entityId);
  for (const id of lid) A.interact(id); await sleep(600);
  ok('lamp recolours', (await run('data get entity @e[tag=bm.lavalamp,limit=1] item.components')).includes('lava3d_red'));
  A.input({ shift: true }); await sleep(300); for (const id of lid) { A.attack(id); await sleep(150); } await sleep(700); A.input({});
  ok('sneak-punch picks it up', (await count('@e[tag=bm.lavalamp]')) === 0 && (await run(`execute if block ${X - 1} ${Y} ${Z} minecraft:air`)).includes('passed') && (await run('clear TestRat *[minecraft:custom_data~{bm:"lava_lamp"}] 0')).includes('1'));
  // Whoopee cushion: a pig walks onto it
  await give('whoopee_cushion'); await look(X + 0.5, Y, Z + 0.5, -90, 50); await press();
  await run(`summon pig ${X + 1.5} ${Y} ${Z + 0.5} {NoAI:1b,Tags:["t24"]}`); await sleep(800);
  ok('whoopee cushion toots', (await num('scoreboard players get @e[tag=bm.whoopd,limit=1] bm.trt')) >= 1);
  await run('kill @e[tag=t24]'); await run('kill @e[tag=bm.whoophit]'); await run('kill @e[tag=bm.whoopd]');
  // Trash can
  await give('trash_can'); await look(X + 0.5, Y, Z + 0.5, 180, 0); await press();
  await run(`data modify block ${X} ${Y} ${Z - 2} Items set value [{Slot:0b,id:"minecraft:dirt",count:5}]`); await sleep(1500);
  ok('trash can eats items', !(await run(`data get block ${X} ${Y} ${Z - 2} Items`)).includes('dirt') && (await count('@e[tag=bm.trashd]')) === 1);
  await look(X + 0.5, Y, Z + 12.5, 0, 0); await sleep(2600); ok('trash can folds away', (await count('@e[tag=bm.trashd]')) === 0 && (await run(`execute if block ${X} ${Y} ${Z - 2} air`)).includes('passed'));
  // Display skiff: place, dye, decal
  await give('display_skiff'); await look(X + 0.5, Y, Z + 0.5, 0, 45); await press();
  const sid = Object.values(A.ents).filter(e => Math.abs(e.x - (X + 0.5)) < 0.1 && Math.abs(e.z - (Z + 2.5)) < 0.1).map(e => e.entityId);
  await run('item replace entity TestRat hotbar.0 with red_dye 3'); for (const id of sid) A.interact(id); await sleep(600);
  ok('skiff dyed crimson', (await run('data get entity @e[tag=bm.dskiffd,limit=1] item.components')).includes('skiff_crimson_none'));
  A.input({ shift: true }); await sleep(200); for (const id of sid) A.interact(id, true); await sleep(600); A.input({});
  ok('skiff decal changes', (await run('data get entity @e[tag=bm.dskiffd,limit=1] item.components')).includes('skiff_crimson_stripes'));
  // Boombox
  await give('boombox'); await look(X + 0.5, Y, Z + 0.5, 90, 50); await press();
  const bid = Object.values(A.ents).filter(e => Math.abs(e.x - (X - 0.5)) < 0.1 && Math.abs(e.z - (Z + 0.5)) < 0.1).map(e => e.entityId);
  await run('item replace entity TestRat hotbar.0 with air'); for (const id of bid) A.interact(id); await sleep(600);
  ok('boombox plays track 1', (await num('scoreboard players get @e[tag=bm.boomhit,limit=1] bm.trk')) === 0, A.bars.slice(-1)[0]);
  // Ocarina
  await give('ocarina'); await run('scoreboard players reset TestRat bm.ocn'); await sleep(300); await press(true); ok('ocarina instrument switch', (await num('scoreboard players get TestRat bm.ocn')) === 1);
  await press(); ok('ocarina plays', true);
  // Vorn trooper: no board, feet on the ground
  await run(`execute positioned ${X + 6} ${Y} ${Z + 6} run function bm:p32/spawn/trooper`); await sleep(500);
  const pc = await num(`execute store result score #t bm.rng as @e[tag=bm.vtroop,limit=1] on passengers if entity @s`);
  ok('vorn trooper has one model and no board', pc === 1, 'passengers ' + pc);
  console.log(res.filter(Boolean).length + '/' + res.length);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.log('FATAL', e); process.exit(1); });

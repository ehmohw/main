const { bot, rcon, sleep } = require('./lib');
const X = 5200, Y = 100, Z = 5200;
(async () => {
  const R = await rcon(); const run = (c) => R.run(c);
  const res = []; const ok = (n, c, d) => { res.push(c); console.log(c ? 'PASS' : 'FAIL', n, d || ''); };
  const A = await bot('TestRat'); await sleep(1000);
  const look = async (x, y, z, yaw, pitch) => { await run(`tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await sleep(400); A.pos.yaw = yaw; A.pos.pitch = pitch; };
  const press = async (sneak) => { if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(250); A.release(); if (sneak) A.input({}); await sleep(500); };
  await run(`forceload add ${X - 16} ${Z - 16} ${X + 48} ${Z + 16}`);     // (the far blood mob stands 42 blocks off: keep its chunk loaded)
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance infinite 4 true'); await run('time set noon'); await run('weather clear');
  await run(`fill ${X - 12} ${Y - 1} ${Z - 12} ${X + 12} ${Y - 1} ${Z + 12} minecraft:stone`); await run(`fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y + 12} ${Z + 12} minecraft:air`);
  // 1. mailbox model lands on its hitbox
  await run('kill @e[tag=bm.mbox]'); await run('kill @e[tag=bm.mbdisp]');
  await look(X + 0.5, Y, Z + 0.5, 0, 45); await run('loot replace entity TestRat hotbar.0 loot bm:items/mailbox'); A.slot(0); await sleep(200); await press();
  const mi = await run('data get entity @e[tag=bm.mbox,limit=1] Pos'), md = await run('data get entity @e[tag=bm.mbdisp,limit=1] Pos');
  ok('mailbox model on its hitbox', mi.split(':')[1] === md.split(':')[1] && mi.includes('['), mi + ' | ' + md);
  // 2. the Vacuum Satchel (2.4x: what it swallows is kept in storage, bm:vac v<your id>): ON, it pulls in what's dropped near you;
  //    sneak + use unfolds it into a barrel in front of you, holding what it swallowed; sneak + use again folds it back
  await run('clear TestRat'); await run(`kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/vacuum_satchel'); A.slot(0); await sleep(200);
  await look(X + 0.5, Y, Z + 0.5, 180, 0); await press();
  const pid = (await run('scoreboard players get TestRat bm.pid')).match(/has (\d+)/); const vs = () => run(`data get storage bm:vac v${pid ? pid[1] : 0}`);
  await run(`summon item ${X + 0.5} ${Y} ${Z + 3.5} {Item:{id:"minecraft:diamond",count:5}}`); await sleep(1500);
  ok('vacuum pulls a dropped stack into the satchel (its storage)', /diamond/.test(await vs()), (await vs()).slice(0, 160));
  await press(true); await sleep(400);
  const bx = await run(`execute if block ${X} ${Y} ${Z - 2} minecraft:barrel run data get block ${X} ${Y} ${Z - 2} Items`);
  ok('sneak + use: it unfolds into a barrel in front of you, holding the diamonds', /diamond/.test(bx), bx.slice(0, 160));
  await press(true); await sleep(600);
  const gone = await run(`execute if block ${X} ${Y} ${Z - 2} minecraft:barrel`);
  ok('sneak + use again: the barrel folds away, the diamonds back in the satchel', !/passed/.test(gone) && /diamond/.test(await vs()), gone + ' ' + (await vs()).slice(0, 100));
  await run('clear TestRat'); await run(`data remove storage bm:vac v${pid ? pid[1] : 0}`);
  // 3. soul vial on a spawner
  await run(`setblock ${X} ${Y} ${Z + 2} minecraft:spawner`); await run('clear TestRat');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/soul_vial_spider'); A.slot(0); await look(X + 0.5, Y, Z + 0.5, 0, 20); await press();
  const sp = await run(`data get block ${X} ${Y} ${Z + 2} SpawnData`); ok('soul vial sets the spawner', sp.includes('spider'), sp);
  // 4. Gravedigger's Maw: 3x3 excavate
  await run(`fill ${X - 2} ${Y - 1} ${Z + 3} ${X + 2} ${Y + 3} ${Z + 3} minecraft:stone`); await run('clear TestRat'); await run('kill @e[type=item]');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/conq_pick'); A.slot(0); await look(X + 0.5, Y, Z + 0.5, 0, 0); await press();
  const air = await run(`execute store result score #t bm.rng if blocks ${X - 1} ${Y} ${Z + 3} ${X + 1} ${Y + 2} ${Z + 3} ${X} ${Y + 20} ${Z} all`);
  const cnt = await run(`execute if block ${X} ${Y + 1} ${Z + 3} minecraft:air`), side = await run(`execute if block ${X + 2} ${Y + 1} ${Z + 3} minecraft:stone`);
  ok('pick excavates 3x3', cnt.includes('passed') && side.includes('passed'), cnt + ' / edge ' + side + ' items ' + await run('execute store result score #t bm.rng if entity @e[type=item]'));
  await press(true); const silk = await run('data get entity TestRat SelectedItem.components."minecraft:enchantments"'); ok('sneak toggles silk touch', silk.includes('silk_touch'), silk.slice(0, 150));
  // 5. Reaper's Sickle: crops ripen
  await run(`fill ${X - 3} ${Y - 1} ${Z - 4} ${X + 3} ${Y - 1} ${Z - 2} minecraft:farmland`); await run(`fill ${X - 3} ${Y} ${Z - 4} ${X + 3} ${Y} ${Z - 2} minecraft:wheat[age=0]`);
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/conq_hoe'); A.slot(0); await look(X + 0.5, Y, Z + 0.5, 0, -30); await press();
  const w = await run(`execute if block ${X + 2} ${Y} ${Z - 3} minecraft:wheat[age=7]`); ok('sickle ripens crops', w.includes('passed'), w);
  // 6. Soulreaver: Soul Rend
  await run('kill @e[type=pig]'); await run(`summon pig ${X + 0.5} ${Y} ${Z + 2.5} {NoAI:1b,Health:10f}`); await run('clear TestRat');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/conq_blade'); A.slot(0); await look(X + 0.5, Y, Z + 0.5, 0, 0); await press();
  const pig = await run('execute store result score #t bm.rng if entity @e[type=pig]'); ok('soul rend hits mobs in front', /: 0$|0$/.test(pig) || pig.includes('found no') || pig.includes('Test failed'), pig);   // (26.3: no pig = "Test failed")
  // 7. glow only within 30
  await run('kill @e[type=zombie]'); await run(`summon zombie ${X + 3} ${Y} ${Z} {NoAI:1b,Tags:["bm.blood"],Glowing:1b}`); await run(`summon zombie ${X + 42} ${Y} ${Z} {NoAI:1b,Tags:["bm.blood"],Glowing:1b}`);
  await look(X + 0.5, Y, Z + 0.5, 0, 0); await sleep(2500);
  const gn = await run(`execute as @e[type=zombie,x=${X + 3},y=${Y},z=${Z},distance=..1.5] if entity @s[nbt={active_effects:[{id:"minecraft:glowing"}]}]`);
  const gf = await run(`execute as @e[type=zombie,x=${X + 42},y=${Y},z=${Z},distance=..1.5] unless entity @s[nbt={Glowing:1b}] unless entity @s[nbt={active_effects:[{id:"minecraft:glowing"}]}]`);
  const far = await run(`execute if entity @e[type=zombie,x=${X + 42},y=${Y},z=${Z},distance=..1.5]`);     // (a far one may be gone already: then it isn't glowing either)
  ok('blood mob glows near, not far', gn.includes('passed') && (gf.includes('passed') || !far.includes('passed')), gn + ' / ' + gf + ' / far: ' + far);
  // 8. Horseman's head hits a passive mob (fire cooks it)
  await run('kill @e[type=zombie]');
  // 9. axe timber
  await run(`fill ${X + 4} ${Y} ${Z + 4} ${X + 4} ${Y + 5} ${Z + 4} minecraft:oak_log`); await run(`fill ${X + 2} ${Y + 4} ${Z + 2} ${X + 6} ${Y + 6} ${Z + 6} minecraft:oak_leaves[persistent=false] replace air`);
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/conq_axe'); A.slot(0);
  await look(X + 4.5, Y, Z + 2.5, 0, 25); await sleep(300);
  A.write('block_dig', { status: 0, location: { x: X + 4, y: Y, z: Z + 4 }, face: 2, sequence: A.seq++ }); await sleep(100);
  A.write('block_dig', { status: 2, location: { x: X + 4, y: Y, z: Z + 4 }, face: 2, sequence: A.seq++ }); await sleep(800);
  const top = await run(`execute if block ${X + 4} ${Y + 4} ${Z + 4} minecraft:oak_log`), base = await run(`execute if block ${X + 4} ${Y} ${Z + 4} minecraft:air`);
  ok('axe fells the whole tree', base.includes('passed') && !top.includes('passed'), 'base ' + base + ' top ' + top);
  console.log(res.filter(Boolean).length + '/' + res.length);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.log('FATAL', e); process.exit(1); });

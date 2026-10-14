// v2.67: Leo sits (a click box the size of him, a seated cycle), Leo in an item frame; the blocky Arachno-Lantern spawns whole
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 18800, Y = 110, Z = 18800;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const cnt = async sel => { const o = await run(`execute store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  await run(`forceload add ${X - 40} ${Z - 40} ${X + 40} ${Z + 40}`);
  await run(`fill ${X - 30} ${Y - 2} ${Z - 30} ${X + 30} ${Y - 1} ${Z + 30} minecraft:stone`); await run(`fill ${X - 30} ${Y} ${Z - 30} ${X + 30} ${Y + 20} ${Z + 30} minecraft:air`);
  await run('weather clear'); await run('time set day'); await run('gamerule doMobSpawning false');
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 6.5} 180 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat resistance 300 4 true');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid'); await run('scoreboard players reset TestRat bm.lecd');
  await run('execute as @e[type=wolf,tag=bm.leopet] run tp @s ~ -400 ~'); await run('kill @e[type=item_display,tag=bm.lep]'); await run('kill @e[type=interaction,tag=bm.lehit]');
  await run('loot replace entity TestRat container.20 loot bm:items/leo_crest'); await sleep(800);
  const U = (await run('data get entity TestRat UUID')).replace(/^.*data: /, '').trim();

  // ---- SITTING
  await run('execute as TestRat at @s run function bm:p96/summon_here'); await sleep(2600);
  ok('Leo has a click box the size of him, riding his host', (await cnt('@e[type=interaction,tag=bm.lehit]')) === 1 &&
     /passed/i.test(await run('execute as @e[type=wolf,tag=bm.leopet] on passengers if entity @s[type=interaction,tag=bm.lehit]')));
  const hit = async () => { await run(`data merge entity @e[type=interaction,tag=bm.lehit,limit=1] {interaction:{timestamp:1L,player:${U}}}`); await sleep(700); };
  await hit();
  ok('Right-click him: he sits down', /1b/.test(await run('data get entity @e[type=wolf,tag=bm.leopet,limit=1] Sitting')) && /A rest, then/.test(A.bars.slice(-2).join(' ')), A.bars.slice(-1)[0]);
  ok('...his state is sitting', (await num('scoreboard players get @e[type=wolf,tag=bm.leopet,limit=1] bm.les')) === 4);
  const seen = new Set(); for (let i = 0; i < 40; i++) { seen.add(await run('data get entity @e[type=item_display,tag=bm.lp_head,tag=!bm.leencp,limit=1] transformation.left_rotation')); await sleep(200); }
  const tri = await run('data get entity @e[type=item_display,tag=bm.lp_trident,tag=!bm.leencp,limit=1] transformation.translation[1]');
  ok('...and the seated poses play (he breathes, looks about)', seen.size >= 2, `${seen.size} head turns`);
  ok('...down on the ground (the rig lowered)', /-0\.\d/.test(await run('data get entity @e[type=item_display,tag=bm.lp_body,tag=!bm.leencp,limit=1] transformation.translation[1]')));
  await hit(); await sleep(400);
  ok('Right-click again: he stands up', /0b/.test(await run('data get entity @e[type=wolf,tag=bm.leopet,limit=1] Sitting')) && /Up we go/.test(A.bars.slice(-2).join(' ')), A.bars.slice(-1)[0]);
  await run('execute as @e[type=wolf,tag=bm.leopet] at @s run function bm:p96/go'); await sleep(600);
  ok('Sent home: his click box goes with him', (await cnt('@e[type=interaction,tag=bm.lehit]')) === 0);

  // ---- THE FRAME
  await run(`summon item_frame ${X} ${Y + 2} ${Z - 2} {Facing:3b,Tags:["t97f"]}`);
  await run('loot replace entity @e[tag=t97f,limit=1] contents loot bm:items/leo_crest'); await sleep(2600);
  ok('Hang Leo\'s crest in a frame: an anchor, and Leo comes out', (await cnt('@e[type=armor_stand,tag=bm.ffa]')) === 1 && (await cnt('@e[type=wolf,tag=bm.leopet,tag=bm.ffpet]')) === 1,
     `${await cnt('@e[type=armor_stand,tag=bm.ffa]')} ${await cnt('@e[type=wolf,tag=bm.leopet]')}`);
  ok('..."himself" (he makes himself at home)', /makes himself at home/.test(A.bars.join(' ')), A.bars.slice(-1)[0]);
  await run('execute as @e[type=wolf,tag=bm.leopet] on owner run tag @s add t97own');
  ok('...he belongs to the frame, with his own rig', (await cnt('@e[type=armor_stand,tag=bm.ffa,tag=t97own]')) === 1 && (await cnt('@e[type=item_display,tag=bm.lp_body,tag=!bm.leencp]')) === 1);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 1.5} 180 0`); await sleep(600);
  await run('data modify entity @e[tag=t97f,limit=1] ItemRotation set value 1b'); await sleep(900);
  ok('Right-click the frame: he sits', /1b/.test(await run('data get entity @e[type=wolf,tag=bm.leopet,limit=1] Sitting')));
  await run('item replace entity @e[tag=t97f,limit=1] contents with minecraft:air'); await sleep(2400);
  ok('Take the crest out: he goes with it', (await cnt('@e[type=wolf,tag=bm.leopet]')) === 0 && (await cnt('@e[type=armor_stand,tag=bm.ffa]')) === 0);
  await run('kill @e[tag=t97f]');

  // ---- THE ARACHNO-LANTERN, blocky
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(500);
  await run('kill @e[tag=bm.salboss]');
  const forced = await num('scoreboard players get #forced bm.bm'); await run('scoreboard players set #forced bm.bm 1');     // (it only stays on a Blood Moon)
  await run('execute as TestRat at @s run function bm:admin/arachno_lantern'); await sleep(3000);
  const parts = await cnt('@e[type=item_display,tag=bm.salp]');
  const models = await run('data get entity @e[type=item_display,tag=bm.salp,limit=1] item.components."minecraft:item_model"');
  ok('The Arachno-Lantern spawns whole (its body, stem, tongue, two fires and 24 leg segments - no collar)', parts === 29 && (await cnt('@e[type=item_display,tag=bm.salp,nbt={item:{components:{"minecraft:item_model":"bm:sal_collar"}}}]')) === 0, `${parts} parts ${models.replace(/.*data: /, '')}`);
  await sleep(3000);
  ok('...and it walks (still whole a few seconds later)', (await cnt('@e[type=item_display,tag=bm.salp]')) === parts);
  await run('execute as @e[tag=bm.salboss] at @s run tp @s ~ -400 ~'); await run('kill @e[tag=bm.salboss]'); await run('kill @e[type=item_display,tag=bm.salp]');
  if (isNaN(forced)) await run('scoreboard players reset #forced bm.bm'); else await run(`scoreboard players set #forced bm.bm ${forced}`);

  await run('gamerule doMobSpawning true'); await run(`forceload remove ${X - 40} ${Z - 40} ${X + 40} ${Z + 40}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`); process.exit(0);
})();

// t415 (3.2c): a relic an older version put on the Rat Pack comes back off it - as a regular player.
//   The owner, updating from a much older version: every relic said "That one wouldn't come off". The hand-back checked that the
//   item handed over had the row's own id - an item stored by an older version carries an older one, so it was refused, always.
//   rcon sets the stage only: a Heartstone kept on the Pack under an old id (bm:"heartstone_v1"), as an old world would have it.
//   Then, as the player: the Rat Pack -> Relics -> Materials -> the Heartstone row: it comes off, into the pockets, and the row goes.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  const pid = +((await run('scoreboard players get TestRat bm.pid')).match(/has (\d+)/) || [])[1];
  await run('loot replace entity TestRat hotbar.0 loot bm:items/partner_wheel');
  // (the stage: a Heartstone on the Pack, stored as an older version stored it - its id not today's)
  await run('loot replace entity TestRat hotbar.8 loot bm:items/heartstone');
  await run(`data modify storage bm:pw p${pid}.rq_heartstone set from entity TestRat Inventory[{Slot:8b}]`);
  await run(`data remove storage bm:pw p${pid}.rq_heartstone.Slot`);
  await run(`data modify storage bm:pw p${pid}.rq_heartstone.components."minecraft:custom_data".bm set value "heartstone_v1"`);
  await run('item replace entity TestRat hotbar.8 with minecraft:air'); await run('scoreboard players set TestRat bm.rq_heartstone 1');
  const openP = async () => { A.slot(0); await sleep(200); await run('scoreboard players set TestRat bm.gvhc 0'); return A.useWait(2500); };
  await openP(); await A.press(/Relics/); await A.press(/Materials/); await sleep(400);
  ok('Relics › Materials lists the old Heartstone', A.buttons().some(b => /Heartstone/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  A.chats.length = 0; await A.press(/Heartstone/); await sleep(1200);
  ok('pressed: it comes off the Pack (no "wouldn\'t come off")', !A.chats.some(c => /wouldn't come off/.test(c)) && A.chats.some(c => /comes off your Rat Pack/.test(c)), A.chats.slice(-2).join(' / '));
  ok('...into your pockets', /Found 1/.test(await run('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"heartstone_v1"}] 0')));
  ok('...and off the Pack: its row and its stored copy gone', /has 0/.test(await run('scoreboard players get TestRat bm.rq_heartstone')) && /Found no/.test(await run(`data get storage bm:pw p${pid}.rq_heartstone`)));
  // (3.2d) stored in an OLDER FORMAT - before item components (Count, tag): today's game can't build an item from it at all, so
  // it came out as nothing and was refused. Rebuilt from its own loot table, with its count and its custom data (a ring's number).
  await run('clear TestRat');
  await run(`data modify storage bm:pw p${pid}.rq_heartstone set value {id:"minecraft:totem_of_undying",Count:3b,tag:{bm:"heartstone"}}`);
  await run('scoreboard players set TestRat bm.rq_heartstone 3');
  await openP(); await A.press(/Relics/); await A.press(/Materials/); await sleep(400);
  A.chats.length = 0; await A.press(/Heartstone/); await sleep(1200);
  ok('an old-format stack of 3 Heartstones: it comes off (no "wouldn\'t come off")', !A.chats.some(c => /wouldn't come off/.test(c)) && A.chats.some(c => /comes off/.test(c)), A.chats.slice(-2).join(' / '));
  ok('...all 3, into your pockets', /Found 3/.test(await run('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"heartstone"}] 0')));
  // an elemental gem, the same way (a stack of 4 Fire Gems, old format)
  await run(`data modify storage bm:pw p${pid}.rq_gem_fire set value {id:"minecraft:emerald",Count:4b,tag:{bm:"gem_fire"}}`);
  await run('scoreboard players set TestRat bm.rq_gem_fire 4');
  await sleep(800); await openP(); await sleep(300); await A.press(/Relics/); await A.press(/Materials/); await sleep(400);
  A.chats.length = 0; await A.press(/Fire/); await sleep(1200);
  ok('an old-format stack of 4 Fire Gems: it comes off', !A.chats.some(c => /wouldn't come off/.test(c)) && A.chats.some(c => /comes off/.test(c)), A.chats.slice(-2).join(' / '));
  ok('...all 4 Fire Gems, into your pockets', /Found 4/.test(await run('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"gem_fire"}] 0')));
  await run(`data modify storage bm:pw p${pid}.rq_ring_burrows2 set value {id:"minecraft:compass",Count:1b,tag:{bm:"ring_burrows",bm_rid:77}}`);
  await run('scoreboard players set TestRat bm.rq_ring_burrows2 1');
  await sleep(800); await openP(); await sleep(300); await A.press(/Pocket/); await sleep(600);
  const ringRow = A.buttons().find(b => /Ring of Ten Burrows 2/.test(b.label));
  ok('an old-format Ring of Ten Burrows 2 on the Pocket page', !!ringRow, A.buttons().map(b => b.label).join(' | '));
  if (!/Take back/.test(A.buttons().map(b => b.label).join(' '))) { const sw = A.buttons().find(b => /Press to:/.test(b.label)); if (sw) { await A.press(/Press to:/); await sleep(400); } }
  A.chats.length = 0; await A.press(/Ring of Ten Burrows 2/); await sleep(1200);
  ok('...taken back: it comes off', !A.chats.some(c => /wouldn't come off/.test(c)) && A.chats.some(c => /comes off/.test(c)), A.chats.slice(-2).join(' / '));
  ok('...the same ring - its number (77) and so its burrows kept', /Found 1/.test(await run('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"ring_burrows",bm_rid:77}] 0')));
  await run('clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

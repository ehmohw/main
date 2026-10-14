const { bot, rcon, sleep } = require('./lib');
const X = 12800, Y = 200, Z = 12800; const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 3.5} 180 0`); await sleep(4000);
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  await run(`fill ${X - 14} ${Y} ${Z - 14} ${X + 14} ${Y} ${Z + 14} grass_block`); await run(`fill ${X - 14} ${Y + 1} ${Z - 14} ${X + 14} ${Y + 6} ${Z + 14} air`);
  await run(`fill ${X - 3} ${Y + 1} ${Z - 3} ${X + 3} ${Y + 3} ${Z - 3} stone_bricks`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..60]`); await run('clear TestRat'); await run('gamemode survival TestRat');
  await run('kill @e[type=wolf,tag=bm.cecilpet]'); await run('kill @e[type=cat,tag=bm.emmapet]'); await run('kill @e[type=wolf,tag=bm.celipet]');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 3.5} 180 0`); await sleep(4000);
  await run(`summon item_frame ${X} ${Y + 2} ${Z - 2} {Facing:3b,Tags:["t63f"]}`);
  await run('loot replace entity @e[tag=t63f,limit=1] contents loot bm:items/cecil_gem'); await sleep(2600);
  ok('Hang Cecil\'s gem in a frame: an anchor appears, and Cecil comes out', (await cnt('@e[type=armor_stand,tag=bm.ffa]')) === 1 && (await cnt('@e[type=wolf,tag=bm.cecilpet,tag=bm.ffpet]')) === 1,
     `${await cnt('@e[type=armor_stand,tag=bm.ffa]')} ${await cnt('@e[type=wolf,tag=bm.cecilpet]')} ${A.bars.slice(-1)[0] || ''}`);
  await run('execute as @e[type=wolf,tag=bm.cecilpet] on owner run tag @s add t63own');
  ok('...he belongs to the frame (its anchor), not to a player', (await cnt('@e[type=armor_stand,tag=bm.ffa,tag=t63own]')) === 1 && (await cnt('@e[type=item_display,tag=bm.cp_body]')) === 1);
  const p0 = await run('data get entity @e[type=wolf,tag=bm.cecilpet,limit=1] Pos');
  await run(`tp TestRat ${X + 12.5} ${Y + 1} ${Z + 12.5}`); let moved = false;
  for (let i = 0; i < 15 && !moved; i++) { await sleep(1000); moved = (await run('data get entity @e[type=wolf,tag=bm.cecilpet,limit=1] Pos')) !== p0; }
  ok('...and wanders about (he doesn\'t follow anyone)', moved);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 1.5} 180 0`); await sleep(4000);
  const fid = Object.values(A.ents).find(e => Math.abs(e.x - X - 0.5) < 0.7 && Math.abs(e.z - (Z - 2)) < 1.2 && Math.abs(e.y - Y - 2.5) < 1.2);
  const click = async (sneak) => { if (sneak) { A.input({ shift: true }); await sleep(300); } if (fid) A.interact(fid.entityId, sneak); else await run('data modify entity @e[tag=t63f,limit=1] ItemRotation set value 1b'); await sleep(900); if (sneak) { A.input({}); await sleep(200); } };
  console.log('frame entity seen by the bot:', !!fid);
  await click(false);
  ok('Right-click the frame: he sits (and the item turns back)', /1b/.test(await run('data get entity @e[type=wolf,tag=bm.cecilpet,limit=1] Sitting')) && /: 0b/.test(await run('data get entity @e[tag=t63f,limit=1] ItemRotation')),
     (await run('data get entity @e[type=wolf,tag=bm.cecilpet,limit=1] Sitting')).slice(-3) + ' rot ' + (await run('data get entity @e[tag=t63f,limit=1] ItemRotation')).slice(-3) + ' ' + (A.bars.slice(-1)[0] || ''));
  await sleep(2500);
  const sitT = await run('data get entity @e[type=item_display,tag=bm.cp_body,limit=1] transformation.translation');
  ok('...settled low over his staff (his sitting pose)', /-0\.1/.test(sitT) || /, 0\.3[0-9]*f/.test(sitT), sitT.slice(-40));
  await click(false);
  ok('Again: he gets up', /0b/.test(await run('data get entity @e[type=wolf,tag=bm.cecilpet,limit=1] Sitting')));
  await click(true);
  ok('Sneak + right-click: he goes back into the frame (just decoration now)', (await cnt('@e[type=wolf,tag=bm.cecilpet]')) === 0 && (await sc('@e[type=armor_stand,tag=bm.ffa,limit=1]', 'bm.ffon')) === 0,
     A.bars.slice(-1)[0] || '');
  await sleep(3000);
  ok('...and stays in', (await cnt('@e[type=wolf,tag=bm.cecilpet]')) === 0);
  await click(true); await sleep(1000);
  ok('Sneak + right-click again: he comes back out', (await cnt('@e[type=wolf,tag=bm.cecilpet,tag=bm.ffpet]')) === 1);
  // he faints: back by the frame later (the countdown is shortened here)
  await run('kill @e[type=wolf,tag=bm.cecilpet]'); await sleep(4500);
  const cd = await sc('@e[type=armor_stand,tag=bm.ffa,limit=1]', 'bm.ffcd');
  ok('He faints: the frame counts down 5 minutes', cd > 290 && (await cnt('@e[type=wolf,tag=bm.cecilpet]')) === 0, 'cd ' + cd + ' ' + A.chats.slice(-1)[0]);
  await run('scoreboard players set @e[type=armor_stand,tag=bm.ffa] bm.ffcd 2'); await sleep(2600);
  ok('...then he\'s back', (await cnt('@e[type=wolf,tag=bm.cecilpet]')) === 1);
  // take the gem out: he goes, the anchor too
  await run('item replace entity @e[tag=t63f,limit=1] contents with minecraft:air'); await sleep(1500);
  ok('Take the gem out of the frame: he goes with it', (await cnt('@e[type=wolf,tag=bm.cecilpet]')) === 0 && (await cnt('@e[type=armor_stand,tag=bm.ffa]')) === 0 && (await cnt('@e[tag=t63f,tag=bm.ff]')) === 0);
  // Emma and Celi: in, out; and breaking the frame
  await run('loot replace entity @e[tag=t63f,limit=1] contents loot bm:items/emma_ribbon'); await sleep(2600);
  ok('Emma\'s Ribbon in the frame: Emma comes out', (await cnt('@e[type=cat,tag=bm.emmapet,tag=bm.ffpet]')) === 1);
  await run('item replace entity @e[tag=t63f,limit=1] contents with minecraft:air'); await sleep(1500);
  await run('loot replace entity @e[tag=t63f,limit=1] contents loot bm:items/celi_charm'); await sleep(2600);
  ok('Swap it for Celi\'s Moon Charm: Emma goes, Celi comes out', (await cnt('@e[type=cat,tag=bm.emmapet]')) === 0 && (await cnt('@e[type=wolf,tag=bm.celipet,tag=bm.ffpet]')) === 1);
  await run('kill @e[tag=t63f]'); await sleep(1500);
  ok('Break the frame: she goes too', (await cnt('@e[type=wolf,tag=bm.celipet]')) === 0 && (await cnt('@e[type=armor_stand,tag=bm.ffa]')) === 0);
  // his owner's own Cecil isn't affected by a framed one
  await run(`kill @e[type=item,x=${X},y=${Y},z=${Z},distance=..10]`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

// 2.68 follow-ups: Locker Key in the gutter only, Office leave button, Boomer filing, den NPC dedupe, door in the doorway,
// lower counter, guard leash, Blueprint order
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => +(((await run(c)).match(/(?:Count: |has |data: |Found )(-?\d+)/) || [0, -1])[1]);
  const cnt = async (sel, dim = 'bm:gutter') => +(((await run(`execute in ${dim} store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/) || [0, 0])[1]);
  const KEY = '*[minecraft:custom_data~{bm:"locker_key"}]';
  const hasKey = async () => /passed/.test(await run(`execute if items entity TestRat container.* ${KEY}`));
  const A = await bot('TestRat'); await sleep(2500);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/heist_plans_anywhere'); await run('function bm:admin/heist_variants_never');
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 600 4 true');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await run('execute in minecraft:overworld run fill 12998 119 12998 13002 119 13002 stone'); await sleep(2500);
  ok('In the Overworld: no Locker Key', !(await hasKey()));
  for (let i = 0; i < 6; i++) await run('loot give TestRat loot bm:items/token'); await run('loot give TestRat loot bm:items/fixers_ledger');
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7601');
  await run('execute as TestRat at @s run function bm:p70/pick_tier'); await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives');
  await sleep(7000);
  const gi = await num('scoreboard players get TestRat bm.gvi');
  ok('In the den: the Locker Key is in your pack', /gutter/.test(await run('data get entity TestRat Dimension')) && await hasKey());
  const kc = await num(`execute store result score #t bm.rng run clear TestRat ${KEY} 0`);
  ok('...just the one', kc === 1, `${kc}`);
  const kd = await run(`data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"locker_key"}}}].components`);
  ok('...stamped with your pid, cursed to vanish (unseen)', /bm_lk: \d+/.test(kd) && /vanishing_curse/.test(kd) && /hidden_components/.test(kd), kd.slice(0, 200));
  // drop it: gone - and a fresh one back
  await run(`clear TestRat ${KEY}`); await run('execute at TestRat run summon minecraft:item ~ ~1 ~ {Tags:["bm.t109k"],PickupDelay:200s,Item:{id:"minecraft:trial_key",count:1,components:{"minecraft:custom_data":{bm:"locker_key",bm_lk:1}}}}');
  await sleep(2400);
  ok('A dropped key is gone; a fresh one is in your pack', (await cnt('@e[type=minecraft:item,tag=bm.t109k]')) === 0 && await hasKey());
  // put in a locker: pulled out
  await run('execute in bm:gutter run data modify block -254 64 -255 Items set value [{Slot:3b,id:"minecraft:trial_key",count:1,components:{"minecraft:custom_data":{bm:"locker_key",bm_lk:1}}},{Slot:4b,id:"minecraft:dirt",count:1}]');
  await run('execute in bm:gutter run tp TestMouse -253 64 -253');
  const B = await bot('TestMouse'); await sleep(1500); await run('execute in bm:gutter run tp TestMouse -253 64 -253'); await sleep(2500);
  const bay = await run('execute in bm:gutter run data get block -254 64 -255 Items');
  ok('A key left in a Locker Hall bay is taken out (the rest stays)', !/locker_key/.test(bay) && /dirt/.test(bay), bay.slice(0, 160));
  await run('execute in bm:gutter run data modify block -254 64 -255 Items set value []');
  // ender chest
  await run('item replace entity TestRat enderchest.5 with minecraft:trial_key[minecraft:custom_data={bm:"locker_key",bm_lk:1}]'); await sleep(1500);
  ok('...and from your ender chest', !/passed/.test(await run(`execute if items entity TestRat enderchest.* ${KEY}`)));
  // the Office on a heist: its dialog with Leave the heist
  const off = await run('execute as TestRat run function bm:p80/office');
  ok('On a heist the Ledger opens the Office (its heist page, no error)', !/error|Unknown/i.test(off) && (await num('scoreboard players get TestRat bm.menu')) === 7800, off.slice(0, 120));
  await run('scoreboard players set TestRat bm.act 7899'); await sleep(700);
  ok('"Leave the heist" asks first (still on the heist)', /gutter/.test(await run('data get entity TestRat Dimension')));
  // den NPCs: an extra Goldtooth goes
  await run('execute in bm:gutter at @e[type=minecraft:villager,tag=bm.gvgt,limit=1] run summon minecraft:villager ~1 ~ ~ {Tags:["bm.gvgt","bm.npc","bm.gvprop"],NoAI:1b,CustomName:"Goldtooth"}');
  await sleep(2400);
  ok('A second Goldtooth in the den is cleared away (one stays)', (await cnt('@e[type=minecraft:villager,tag=bm.gvgt]')) === 1, `${await cnt('@e[type=minecraft:villager,tag=bm.gvgt]')}`);
  ok('...and one Recruiter, one Tailor', (await cnt('@e[type=minecraft:villager,tag=bm.gvrec]')) === 1 && (await cnt('@e[type=minecraft:villager,tag=bm.gvtail]')) === 1);
  // the counter, the door
  const L = 'execute in bm:gutter positioned as @e[type=minecraft:marker,tag=bm.gvr_lobby,limit=1] run';
  ok('The shop counter is one block high (no slab on top)', /passed/.test(await run(`${L} execute if block ~-7 ~ ~7 minecraft:dark_oak_planks unless block ~-7 ~1 ~7 minecraft:dark_oak_slab`)));
  ok('The Fixer\'s Door fills the west doorway (the swirl, and a wall behind it)', (await cnt('@e[type=minecraft:block_display,tag=bm.exdoor,x=0,y=67,z=11,dx=1,dy=1,dz=2]')) === 1 &&
     /passed/.test(await run(`${L} execute if block ~-13 ~1 ~ minecraft:polished_blackstone_bricks`)));
  ok('...the old side arch is gone', /passed/.test(await run(`${L} execute unless block ~-11 ~1 ~-9 minecraft:gold_block`)));
  ok('...its way-out marker sits in the doorway', (await cnt('@e[type=minecraft:marker,tag=bm.exitm,x=0,y=67,z=12,dx=1,dy=2,dz=1]')) === 1);
  // a guard wandering out of its room is pulled back
  await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,limit=1] at @s run tag @s add bm.t109r');
  await run('execute in bm:gutter positioned as @e[type=minecraft:marker,tag=bm.gvr,tag=!bm.gvr_lobby,limit=1,sort=nearest] run summon minecraft:vindicator ~2 ~ ~2 {Tags:["bm.gvg","bm.t109g"],NoAI:1b,PersistenceRequired:1b}');
  await sleep(2400);
  const rid = await num('execute in bm:gutter run scoreboard players get @e[tag=bm.t109g,limit=1] bm.gvrid');
  await run('execute in bm:gutter as @e[tag=bm.t109g] at @s run tp @s ~ ~ ~-30'); await sleep(2400);
  const gp = await run('execute in bm:gutter run data get entity @e[tag=bm.t109g,limit=1] Pos');
  const mp = await run('execute in bm:gutter run data get entity @e[type=minecraft:marker,tag=bm.gvr,scores={bm.gvrid=' + rid + '},limit=1] Pos');
  const d = (s) => (s.match(/-?[\d.]+d/g) || []).map(parseFloat);
  const [gx, , gz] = d(gp), [mx, , mz] = d(mp);
  ok('A guard that wanders out of its room is pulled back into it', rid >= 1 && Math.abs(gx - mx) < 2 && Math.abs(gz - mz) < 2, `rid ${rid} guard ${gx},${gz} room ${mx},${mz}`);
  await run('execute in bm:gutter run kill @e[tag=bm.t109g]');
  // Boomer: on duty from before filing - filed now, and Raid Crew turns him off
  await run('scoreboard players set TestRat bm.gvhr 5'); await run('scoreboard players set TestRat bm.crew 0'); await run('execute as TestRat run function bm:p98/init');
  ok('A hireling on duty from before 2.67 is filed in the Ledger', (await num('scoreboard players get TestRat bm.crew')) === 64, `${await num('scoreboard players get TestRat bm.crew')}`);
  await run('scoreboard players set TestRat bm.act 7935'); await sleep(700);
  ok('...so Raid Crew can send him off duty', (await num('scoreboard players get TestRat bm.gvhr')) === 0);
  // a room's loans go when it's beaten
  await run('give TestRat minecraft:bow[minecraft:custom_data={bm_kit:1b,bm_room:1b}] 1'); await run('give TestRat minecraft:arrow[minecraft:custom_data={bm_kit:1b,bm_room:1b}] 24');
  await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi');
  await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr,tag=!bm.gvr_lobby,tag=!bm.gvr_vault,limit=1,sort=nearest] at @s run function bm:p70/solved');
  ok('A room\'s loans (the Gallery bow and arrows) are taken back when it\'s beaten', !/passed/.test(await run('execute if items entity TestRat container.* *[minecraft:custom_data~{bm_room:1b}]')));
  // the kit: weapons and tools never wear out
  const kitw = await run('execute as TestRat run function bm:p80/kit/give_1_1');
  const sw = await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"kokiri_sword"}}}].components');
  ok('Kit weapons are unbreakable (and say nothing of it)', /unbreakable/.test(sw) && /hidden_components/.test(sw), sw.slice(0, 120) + ' ' + kitw.slice(0, 80));
  // rooms alternate: puzzle, fight, puzzle, fight
  const order = [];
  for (let q = 1; q <= 8; q++) { for (const k of ['levers', 'plates', 'lasers', 'tiles', 'dial', 'guards', 'coffers', 'lamps', 'lightsout', 'tumbler', 'climb', 'rafters', 'ambush', 'pit']) {
    if ((await cnt(`@e[type=minecraft:marker,tag=bm.gvr_${k},scores={bm.gvq=${q},bm.gvi=${gi}}]`)) >= 1) order.push(`${q}:${k}`); } }
  const fights = ['guards', 'ambush', 'pit'];
  const bad = order.filter(o => { const [q, k] = o.split(':'); return (+q % 2 === 0) !== fights.includes(k); });
  ok('The rooms alternate: a puzzle, then a fight, then a puzzle...', order.length >= 1 && bad.length === 0, order.join(' '));
  // leaving the gutter takes the key
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(3000);
  ok('Home again: the key stays behind', /overworld/.test(await run('data get entity TestRat Dimension')) && !(await hasKey()));
  // the Blueprint: left to right
  const txt = 'function bm:p70/r/dial/text';
  await run('data modify storage bm:gv dial merge value {a:"A",b:"B",c:"C"}'); 
  await run('execute in bm:gutter run summon minecraft:text_display 0 200 0 {Tags:["bm.gvbp","bm.t109t"]}');
  await run(`execute in bm:gutter positioned 0 200 0 run function bm:p70/r/dial/text with storage bm:gv dial`);
  const bp = await run('execute in bm:gutter run data get entity @e[tag=bm.t109t,limit=1] text');
  ok('The Blueprint lists the dials left to right as you face them', /C\s+B\s+A/.test(bp), bp.slice(-80));
  await run('execute in bm:gutter run kill @e[tag=bm.t109t]');
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('scoreboard players set TestRat bm.gvhr 0'); await run('scoreboard players set TestRat bm.crew 0');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); B.end(); R.end(); process.exit(0);
})();

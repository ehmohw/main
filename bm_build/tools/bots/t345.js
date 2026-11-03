// 3.0g: NO BAGS ON A JOB, as a regular player (rcon sets the stage: the plan bought, the items handed over). A Backpack with a
// whitelisted Gutter Coin packed inside is refused at the coat check (a loose coin still goes in); a Backpack left UNFOLDED in
// the overworld - used as an item, a barrel in front of TestRat - folds itself back into his hands once he's through the door,
// and is taken off him inside within a moment; a Backpack picked up off the vault floor, and a bundle with a Backpack in it,
// the same. Every one of them waits with the Fixer and comes home with him when he leaves.
const { bot, rcon, sleep } = require('./lib_resp');
const { mk } = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = mk(run); const { num, begin } = H;
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  ok('TestRat is a regular player (no operator commands)', await new Promise(r => { const n0 = A.chats.length; A.cmd('gamemode creative');
    setTimeout(() => r(A.chats.slice(n0).some(c => /unknown or incomplete|Unknown command/i.test(c))), 1200); }));
  const BAG = '*[minecraft:custom_data~{bm:"backpack"}]';
  const bags = async () => Math.max(0, await num(`clear TestRat ${BAG} 0`));
  const coins = async () => Math.max(0, await num('clear TestRat *[minecraft:custom_data~{bm:"gutter_coin"}] 0'));
  const pid = await num('scoreboard players get TestRat bm.pid');
  const packCoin = (slot) => run(`item modify entity TestRat ${slot} {type:"minecraft:set_contents",component:"minecraft:container",entries:[{type:"minecraft:loot_table",value:"bm:items/gutter_coin"}]}`);
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');

  // ---- the stage: the overworld platform, the plan (as h110's heist(), with the bags handed over before the door)
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/plan_anywhere'); await run('function bm:admin/heist_variants_never'); await run('function bm:admin/rooms_only_levers'); await run('function bm:admin/variant_a');
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat saturation 900 0 true');
  await run('tag TestRat remove bm.gvzap'); await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players set TestRat bm.gvhc 0');
  await run('execute in minecraft:overworld run fill 12996 119 12996 13004 119 13004 stone'); await run('execute in minecraft:overworld run fill 12996 120 12996 13004 123 13004 air');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5 0 0'); await sleep(2500);
  // (1) a backpack with a whitelisted coin inside, in the hotbar; a loose coin beside it
  await run('item replace entity TestRat hotbar.0 with minecraft:air'); await run('loot replace entity TestRat hotbar.0 loot bm:items/backpack'); await packCoin('hotbar.0');
  await run('loot replace entity TestRat hotbar.2 loot bm:items/gutter_coin');
  ok('(stage) a Backpack with a Gutter Coin packed inside, and a loose coin', (await bags()) === 1 && /gutter_coin/.test(await run('data get entity TestRat Inventory[{Slot:0b}].components."minecraft:container"')));
  // (2) a second backpack, USED as an item: it unfolds into a barrel in front of him
  await run('loot replace entity TestRat hotbar.1 loot bm:items/backpack'); await packCoin('hotbar.1');
  A.slot(1); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(800);
  ok('A Backpack used in the overworld unfolds into a barrel in front of him', /Found 1|passed/i.test(await run('execute in minecraft:overworld positioned 13000.5 120 13000.5 if entity @e[type=minecraft:marker,tag=bm.bxm,distance=..4]')) &&
     (await bags()) === 1);
  A.slot(2);
  for (let i = 0; i < 8; i++) await run('loot give TestRat loot bm:items/token');
  await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players set TestRat bm.gval 1');
  await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7601'); await run('execute as TestRat at @s run function bm:p70/pick_tier');
  await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives');
  A.chats.length = 0;
  ok('Through the coat check into the heist', await wait(12000, async () => /bm\.gvp/.test(await run('data get entity TestRat Tags'))));
  await sleep(1500);
  ok('...the Backpack with heist gear inside stays with the Fixer', (await bags()) === 0, `${await bags()} carried`);
  ok('...while the loose Gutter Coin goes in', (await coins()) >= 1);
  ok('...the unfolded Backpack folded back to him in the gutter - and was taken off him at once', await wait(4000, async () => (await bags()) === 0 &&
     !/Found/.test(await run('execute in minecraft:overworld positioned 13000.5 120 13000.5 if entity @e[type=minecraft:marker,tag=bm.bxm,distance=..4]'))) &&
     A.chats.some(c => /No bags on a job/.test(c)), A.chats.slice(-4).join(' | ').slice(0, 200));
  const cntBags = (t) => (t.match(/bm: "backpack"/g) || []).length;
  const held = async () => cntBags(await run(`data get storage bm:gv cb.p${pid}`)) + cntBags(await run(`data get storage bm:gv bag.p${pid}.inv`));
  ok('...both Backpacks are minded by the Fixer (the coat check\'s bag and carry-back)', (await held()) >= 2, `${await held()}`);

  // (3) one picked up off the floor inside, (4) a bundle with one packed in it
  await begin(); await sleep(800);
  A.chats.length = 0;
  await run('execute at TestRat run summon minecraft:item ~ ~0.3 ~ {Item:{id:"minecraft:totem_of_undying",count:1,components:{"minecraft:custom_data":{bm:"backpack"},"minecraft:item_model":"bm:backpack"}},PickupDelay:0s}');
  ok('A Backpack picked up off the vault floor: taken at once', await wait(3000, async () => A.chats.some(c => /No bags on a job/.test(c))) && (await bags()) === 0);
  A.chats.length = 0;
  await run('execute at TestRat run summon minecraft:item ~ ~0.3 ~ {Item:{id:"minecraft:bundle",count:1,components:{"minecraft:bundle_contents":[{id:"minecraft:totem_of_undying",count:1,components:{"minecraft:custom_data":{bm:"backpack"}}}]}},PickupDelay:0s}');
  ok('A bundle with a Backpack packed inside: taken too', await wait(3000, async () => A.chats.some(c => /No bags on a job/.test(c))) &&
     (await num('clear TestRat minecraft:bundle 0')) <= 0);
  ok('...four bags minded now', (await held()) >= 4, `${await held()}`);

  // ---- home again: every one of them back
  await run('execute as TestRat at @s run function bm:p70/leave');
  ok('Leaving the heist: home, every bag handed back (the coins still packed inside)', await wait(8000, async () => (await bags()) >= 3) &&
     /gutter_coin/.test(await run(`data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"backpack"}}}].components."minecraft:container"`)), `${await bags()} bags`);
  ok('...and the bundle', (await num('clear TestRat minecraft:bundle 0')) >= 1);

  await run('clear TestRat'); for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/prime_chance'); await run('function bm:admin/fork_chance'); await run('function bm:admin/traps_chance'); await run('function bm:admin/curse_chance'); await run('function bm:admin/rooms_any');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

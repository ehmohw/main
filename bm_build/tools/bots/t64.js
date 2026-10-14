const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel, dim = 'bm:gutter') => { const m = (await run(`execute in ${dim} store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2500);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  // ---- a heist: adventure mode, the boss survives a knock-out
  await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 1');
  await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7601');
  for (let i = 0; i < 6; i++) await run('loot give TestRat loot bm:items/token'); await run('execute as TestRat at @s run function bm:p70/pick_tier');
  await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4000);   // (2.65: the fee, then the tries)
  ok('In the vault: adventure mode', /adventure|2/.test(await run('data get entity TestRat playerGameType')), await run('data get entity TestRat playerGameType'));
  ok('The den BEGIN buttons are pale oak', /passed/.test(await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s if block ~11 ~1 ~3 minecraft:pale_oak_button if block ~11 ~1 ~-3 minecraft:pale_oak_button')));
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run function bm:p70/begin');
  await run('execute in bm:gutter at @e[type=marker,tag=bm.gvr_vault,limit=1] run tp TestRat ~ ~ ~'); await sleep(3000);
  ok('The guardian appears', (await cnt('@e[tag=bm.gvboss]')) === 1);
  ok('...and can be knocked back (no knockback resistance)', /0\.0|is 0/.test(await run('execute in bm:gutter run attribute @e[tag=bm.gvboss,limit=1] minecraft:knockback_resistance base get')));
  await run('kill TestRat'); await sleep(4500);
  ok('Knocked out mid-fight: the guardian is still there when you come back', (await cnt('@e[tag=bm.gvboss]')) === 1 &&
     /bm:gutter/.test(await run('data get entity TestRat Dimension')));
  ok('...and the vault is NOT open', /has 1/.test(await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,limit=1] run scoreboard players get @s bm.gvs')));
  ok('...still adventure after the knock-out', /adventure|2/.test(await run('data get entity TestRat playerGameType')));
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  ok('Out of the vault: survival again', /survival|: 0/.test(await run('data get entity TestRat playerGameType')), await run('data get entity TestRat playerGameType'));
  // ---- water walking boots
  await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(1500);
  await run(`fill ${X - 6} ${Y} ${Z - 6} ${X + 6} ${Y} ${Z + 6} stone`); await run(`fill ${X - 5} ${Y - 3} ${Z - 5} ${X + 5} ${Y} ${Z + 5} water`);
  await run(`fill ${X - 6} ${Y + 1} ${Z - 6} ${X + 6} ${Y + 8} ${Z + 6} air`);
  await run('loot replace entity TestRat armor.feet loot bm:items/water_walking_boots'); await run(`tp TestRat ${X + 0.5} ${Y + 0.6} ${Z + 0.5}`);
  await sleep(600); const e1 = await run('data get entity TestRat active_effects');
  await run(`tp TestRat ${X + 0.5} ${Y + 1.1} ${Z + 0.5}`); await sleep(600); const e2 = await run('data get entity TestRat active_effects');
  const lev = s => { const m = s.match(/amplifier: (\d+)b, id: "minecraft:levitation"|id: "minecraft:levitation"[^}]*amplifier: (\d+)b/); return m ? +(m[1] || m[2]) : (/levitation/.test(s) ? 0 : -1); };
  ok('Water Walking Boots, feet in water: a gentle lift (Levitation I, not a launch)', lev(e1) === 0, e1.slice(-160));
  ok('...just above the water: hover on Slow Falling, no levitation at all', /slow_falling/.test(e2) && lev(e2) === -1, e2.slice(-160));
  await run('item replace entity TestRat armor.feet with air'); await run(`fill ${X - 6} ${Y - 3} ${Z - 6} ${X + 6} ${Y} ${Z + 6} stone`); await run('effect clear TestRat');
  // ---- display case on the floor: on top, not inside
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 60`); await sleep(500); await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..20]`);
  await run('execute as TestRat at @s run function bm:p72/dc/place_oak'); await sleep(200);
  const p = await run(`data get entity @e[type=item_display,tag=bm.dcase,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] Pos[1]`);
  ok('A floor display case stands ON the floor', /101\.0d/.test(p), p);
  // an old, sunken one is lifted out
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..20]`);
  await run(`execute positioned ${X + 2.5} ${Y} ${Z + 2.5} run function bm:p72/dc/spawn_floor`); await sleep(1500);
  const q = await run(`data get entity @e[type=item_display,tag=bm.dcase,limit=1,sort=nearest,x=${X + 2.5},y=${Y},z=${Z + 2.5}] Pos[1]`);
  ok('...and an old sunken case is lifted onto the floor', /101\.0d/.test(q), q);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..20]`);
  // ---- mimic in the heist drops nothing
  await run(`execute positioned ${X + 0.5} ${Y + 1} ${Z + 3.5} run function bm:p39/mimic/spawn_chest`);
  await run(`data merge entity @e[type=rabbit,tag=bm.mnew,limit=1] {DeathLootTable:"minecraft:empty"}`); await run('kill @e[type=rabbit,tag=bm.mnew]'); await sleep(500);
  ok('A vault Mimic (its loot emptied) drops nothing', (await cnt(`@e[type=item,x=${X},y=${Y},z=${Z},distance=..10]`, 'minecraft:overworld')) === 0);
  // ---- the haul comes packed in one crate
  await run('clear TestRat'); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(500);
  for (const [k, v] of [['#gt', 3], ['#sh', 6], ['#gn', 1], ['#np', 1], ['#glk', 0], ['#grun', 77]]) await run(`scoreboard players set ${k} bm.rng ${v}`);
  await run('scoreboard players set TestRat bm.gvcl 0'); await run('execute as TestRat at @s run function bm:p70/haul'); await sleep(1200);
  const inv = await run('data get entity TestRat Inventory');
  const n = +((await run('execute store result score #t bm.rng run data get entity TestRat Inventory')).match(/(\d+)/) || [0, 0])[1];
  console.log('   inventory list:', await run('scoreboard players get #t bm.rng'));
  const cont = await run('data get entity TestRat Inventory[{id:"minecraft:barrel"}].components."minecraft:container"');
  const hauls = (+(((await run('execute store result score #t bm.rng run clear TestRat minecraft:barrel[minecraft:custom_data~{bm_haul:1b}] 0')).match(/Found (\d+)/) || [0, 0])[1]));
  ok('The haul: one crate in your pockets (plus nothing loose)', hauls === 1, `${hauls} crates`);
  const hasIn = async k => /Test passed/.test(await run(`execute if data entity TestRat Inventory[{id:"minecraft:barrel"}].components."minecraft:container"[{item:{components:{"minecraft:custom_data":{bm:"${k}"}}}}]`));
  ok('...packed with the prizes: Gutter Coins and the Blood Moon\'s crystals', (await hasIn('gutter_coin')) && (await hasIn('blood_crystal')), cont.slice(0, 300));
  await run(`setblock ${X + 2} ${Y + 1} ${Z} air`);
  await run(`setblock ${X + 2} ${Y + 1} ${Z} minecraft:barrel`); await run(`data modify block ${X + 2} ${Y + 1} ${Z} Items set from entity TestRat Inventory[{id:"minecraft:barrel"}].components."minecraft:container"`);
  console.log('   (placed:', (await run(`data get block ${X + 2} ${Y + 1} ${Z} Items`)).slice(0, 200), ')');
  await run(`setblock ${X + 2} ${Y + 1} ${Z} air`); await run('clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0); })();

// 2.85d: THE RATS' CALLS AND THE NETHER/END ROOMS' COIN - as a regular player TestRat (rcon sets the stage: a floor in each
// dimension, the calls in hand, and - for the haul - the heist win's per-raider finds rolled by rcon).
//   the Ember Rat's Call blown in the Overworld: nothing answers, it's kept. In the Nether: the Ember Rat sets up shop nearby, the
//   call used up; a second call with him out: "already out", kept.
//   the Void Rat's Call blown in the End past the dragon's isle: the Void Rat sets up shop, the call used up.
//   the haul: a raider who saw the Blaze Forge beaten this run gets Ember Scales (the Ember Rat's coin) about 60% of wins, one who
//   saw the Void Garden, Void Shards (the Void Rat's); one who saw neither, neither. A rat's call found turns up in the haul.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const has = async id => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const cnt = async (dim, sel) => { const m = (await run(`execute in ${dim} if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const blow = async id => { let s = -1; for (let i = 0; i < 9 && s < 0; i++) if (new RegExp(`"${id}"`).test(await run(`data get entity TestRat Inventory[{Slot:${i}b}].components."minecraft:custom_data".bm`))) s = i;
    A.slot(s); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(1200); };
  const SPOTS = { 'minecraft:the_nether': [2000, 100, 2000], 'minecraft:the_end': [3000, 70, 3000] };
  const clearRats = async () => { for (const d of ['minecraft:the_nether', 'minecraft:the_end']) {
    await run(`execute in ${d} as @e[type=minecraft:wandering_trader,tag=bm.field_rat] at @s run tp @s ~ -300 ~`); await run(`execute in ${d} run kill @e[tag=bm.field_rat]`);
    await run(`execute in ${d} run kill @e[type=minecraft:item_display,tag=bm.field_sprite]`); } };

  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(700);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat resistance 600 4 true'); await run('effect give TestRat fire_resistance 600 0 true');
  await clearRats();
  for (const [d, [x, y, z]] of Object.entries(SPOTS)) {
    await run(`execute in ${d} run forceload add ${x - 32} ${z - 32} ${x + 32} ${z + 32}`);
    await run(`execute in ${d} run fill ${x - 20} ${y - 1} ${z - 20} ${x + 20} ${y - 1} ${z + 20} minecraft:stone`);
    await run(`execute in ${d} run fill ${x - 20} ${y} ${z - 20} ${x + 20} ${y + 6} ${z + 20} minecraft:air`);
  }

  // ================================================================== the Ember Rat's Call
  await run('loot give TestRat loot bm:items/ember_call'); await run('loot give TestRat loot bm:items/ember_call');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await run('execute in minecraft:overworld run fill 12996 119 12996 13004 119 13004 stone'); await sleep(2000);
  A.bars.length = 0; await blow('ember_call');
  ok('The Ember Rat\'s Call blown in the Overworld: nothing answers - kept', (await has('ember_call')) === 2 && A.bars.some(b => /Nothing answers/.test(b)), A.bars.slice(-1).join(''));
  let [x, y, z] = SPOTS['minecraft:the_nether'];
  await run(`execute in minecraft:the_nether run tp TestRat ${x + 0.5} ${y} ${z + 0.5}`); await sleep(3500); A.stand();
  A.chats.length = 0; await blow('ember_call');
  const rat = '@e[type=minecraft:wandering_trader,tag=bm.frat_ember]';
  ok('...in the Nether: the Ember Rat sets up shop nearby - the call used up', await wait(4000, async () => (await cnt('minecraft:the_nether', rat)) === 1) && (await has('ember_call')) === 1,
     `rats ${await cnt('minecraft:the_nether', rat)} calls ${await has('ember_call')} ${A.chats.slice(-1).join('')}`);
  A.chats.length = 0; await blow('ember_call');
  ok('...a second call with him out: "already out" - kept', (await has('ember_call')) === 1 && A.chats.some(c => /already out/.test(c)) && (await cnt('minecraft:the_nether', rat)) === 1);

  // ================================================================== the Void Rat's Call
  await run('loot give TestRat loot bm:items/void_call');
  [x, y, z] = SPOTS['minecraft:the_end'];
  await run(`execute in minecraft:the_end run tp TestRat ${x + 0.5} ${y} ${z + 0.5}`); await sleep(3500); A.stand();
  await blow('void_call');
  const vrat = '@e[type=minecraft:wandering_trader,tag=bm.frat_void]';
  ok('The Void Rat\'s Call blown in the End (past the dragon\'s isle): the Void Rat sets up shop - the call used up',
     await wait(4000, async () => (await cnt('minecraft:the_end', vrat)) === 1) && (await has('void_call')) === 0);
  await clearRats();
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5'); await sleep(2500);

  // ================================================================== the haul (rcon rolls the win's per-raider finds)
  const HA = 'execute in bm:gutter run data get block -200 64 -197 Items', HB = 'execute in bm:gutter run data get block -198 64 -197 Items';
  const empty = async () => { await run('execute in bm:gutter run data merge block -200 64 -197 {Items:[]}'); await run('execute in bm:gutter run data merge block -198 64 -197 {Items:[]}'); };
  const hauls = async id => ((await run(HA)) + (await run(HB))).split(`bm: "${id}"`).length - 1;
  const roll = async n => { let got = 0; for (let i = 0; i < n; i++) { await empty(); await run('execute as TestRat at @s run function bm:p105/finds'); if (await hauls('ember_scale')) got++; } return got; };
  await run('execute in bm:gutter run forceload add -200 -197');
  await run('scoreboard players set TestRat bm.gvrun 777'); await run('scoreboard players set TestRat bm.gvemb 777'); await run('scoreboard players set TestRat bm.gvvsh 0');
  const e30 = await roll(30);
  ok(`A raider who saw the Blaze Forge beaten: Ember Scales in the haul ${e30} of 30 wins (about 60%)`, e30 >= 10 && e30 <= 27);
  await run('scoreboard players set TestRat bm.gvemb 0'); await run('scoreboard players set TestRat bm.gvvsh 777');
  let v = 0; for (let i = 0; i < 20; i++) { await empty(); await run('execute as TestRat at @s run function bm:p105/finds'); if (await hauls('void_shard')) v++; }
  ok(`...one who saw the Void Garden: Void Shards ${v} of 20`, v >= 5 && v <= 19);
  await run('scoreboard players set TestRat bm.gvvsh 0');
  const none = await roll(20);
  ok('...one who saw neither: no Ember Scales', none === 0);
  await empty(); await run('execute as TestRat at @s run function bm:p184/find/void_call');
  ok('A rat\'s call found: in the haul', (await hauls('void_call')) === 1);
  await empty();

  // ---- put things back
  for (const [d, [x2, , z2]] of Object.entries(SPOTS)) await run(`execute in ${d} run forceload remove ${x2 - 32} ${z2 - 32} ${x2 + 32} ${z2 + 32}`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode creative TestRat');
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

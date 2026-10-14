// 2.78: the end-of-heist "Go to the Lounge" keeps your overworld gear at the coat check - as a regular (non-op) player: a heist
// staged with the bot's own gear checked at the door (rcon sets the stage: the bag, the heist tags), the leader's Go to the Lounge
// pressed (the trigger its button sends): into the Lounge with empty pockets - the gear still with the Fixer; then through the
// Lounge's door: home, and every piece handed back.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const has = async (id) => /Found [1-9]/.test(await run(`clear TestRat ${id} 0`));
  const dim = async () => await run('data get entity TestRat Dimension');
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect clear TestRat');
  await run('tag TestRat remove bm.gvp'); await run('tag TestRat remove bm.lgbag'); await run('scoreboard players reset TestRat bm.gvi');
  await run('execute in minecraft:overworld run fill 12998 120 12998 13002 120 13002 stone');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 121 13000.5'); await sleep(2500); A.stand();
  // the stage: the bot's own things, checked at the door as a heist begins; home is where it stood
  await run('item replace entity TestRat hotbar.3 with minecraft:diamond_sword'); await run('item replace entity TestRat inventory.5 with minecraft:golden_apple 7');
  await run('item replace entity TestRat armor.head with minecraft:iron_helmet');
  await run('execute as TestRat run function bm:p72/bag/check'); await sleep(300);
  ok('(stage) the gear is with the Fixer', !(await has('minecraft:diamond_sword')) && !(await has('minecraft:golden_apple')));
  await run('execute as TestRat at @s run function bm:p70/save_home').catch(() => {});
  await run('tag TestRat add bm.gvask'); await run('scoreboard players set TestRat bm.gvnx 1'); await run('tag TestRat add bm.gvp'); await run('scoreboard players set TestRat bm.gvi 1');
  await run('scoreboard players set TestRat bm.menu 7720');
  // the leader's Go to the Lounge
  A.chats.length = 0; A.cmd('trigger bm.act set 7730');
  ok('Go to the Lounge: into the Lounge', await wait(4000, async () => /gutter/.test(await dim())), await dim());
  await sleep(1500);
  ok('...pockets empty of the overworld gear - it stays at the coat check', !(await has('minecraft:diamond_sword')) && !(await has('minecraft:golden_apple')) && !(await has('minecraft:iron_helmet')),
     await run('data get entity TestRat Inventory'));
  ok('..."Your own gear waits at the coat check"', A.chats.some(c => /gear waits at the coat check/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
  // out through the Lounge's door
  await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.lgexit,limit=1] at @s run tp TestRat ~ ~ ~');
  ok('the Lounge\'s door: home', await wait(4000, async () => /overworld/.test(await dim())), await dim());
  await sleep(2500);
  ok('...and every piece handed back (sword, apples, helmet)', (await has('minecraft:diamond_sword')) && (await has('minecraft:golden_apple')) && (await has('minecraft:iron_helmet')),
     await run('data get entity TestRat Inventory'));
  ok('...once (no second set)', /Found 1\b/.test(await run('clear TestRat minecraft:diamond_sword 0')));
  await run('clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

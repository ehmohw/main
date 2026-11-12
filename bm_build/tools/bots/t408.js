// 3.1v: THE HEIST SWEEP'S FIXES, as a regular (non-op) player TestRat - every step a real packet (rcon sets the stage only: Tokens,
// the Ledger, the room drawn, the room's curse and skull, a find already in the pot).
// A job planned through the Ledger with the alarm OFF (the default):
//  - its contract is never "Ghost" (keep the alarm under 25%) - there is no alarm to keep down (it was a free +2 shares);
//  - the Alarm Jammer, used: "This job has no alarm" - and kept (it was spent on nothing, and the bar lost its tries/pot);
//  - a cursed, hard-way (skull) room skipped through the Ledger: the way opens for a try, and the pot gets nothing - no "curse lifts"
//    coins, no "hard way pays" cut (the skip says "no coins for the pot");
//  - a find waiting in the pot, then out through the den door's "Leave the heist?" -> "Leave now": the find is gone - it stays behind
//    with the share, as the card says (it used to wait and pay out at the next win).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found )(-?\d+)/) || [0, -1])[1]);
  const passes = async c => /passed/i.test(await run(c));
  const has = async iid => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const MINE = 'if score @s bm.gvi = TestRat bm.gvi';
  const iget = async (obj) => +(((await run(`execute as @e[type=minecraft:marker,tag=bm.gvinst] ${MINE} run scoreboard players get @s ${obj}`)).match(/has (-?\d+)/) || [0, -99])[1]);

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  // ---- the stage: a job with the Girder Climb (a puzzle, skippable), alarm off
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/plan_anywhere'); await run('function bm:admin/heist_variants_never'); await run('function bm:admin/rooms_only_levers');
  await run('function bm:admin/room_girder');
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat saturation 900 0 true');
  await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players set TestRat bm.gvhc 0');
  await run('execute in minecraft:overworld run fill 12998 119 12998 13002 119 13002 stone'); await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  await sleep(2000);
  for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/token');
  await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players set TestRat bm.gval 0');
  A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(800);
  A.cmd('trigger bm.act set 7603'); await sleep(1500); A.cmd('trigger bm.act set 7613');
  if (!ok('a job planned through the Ledger (alarm off)', await wait(40000, async () => passes('execute if entity @a[name=TestRat,tag=bm.gvp]'), 500))) return done();
  await sleep(2000);
  const GI = await num('scoreboard players get TestRat bm.gvi');
  ok('...the alarm is off on it', (await iget('bm.gval')) !== 1, `gval ${await iget('bm.gval')}`);
  ok('...and its contract isn\'t "Ghost" (no alarm to keep down)', (await iget('bm.gvct')) !== 1, `contract ${await iget('bm.gvct')}`);
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run tp TestRat ~ ~ ~`); await sleep(600);
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run setblock ~11 ~1 ~3 minecraft:pale_oak_button[face=wall,facing=west,powered=true]`);
  await wait(6000, async () => (await iget('bm.gvst')) === 2, 300);
  // ---- the jammer, on a job with no alarm
  await run('loot replace entity TestRat hotbar.3 loot bm:items/alarm_jammer'); A.slot(3); await sleep(300);
  A.bars.length = 0; A.use(); await sleep(500); A.release(); await sleep(700);
  ok('the Alarm Jammer used on a job with no alarm: "This job has no alarm"', A.bars.some(b => /no alarm/.test(b)), A.bars.join(' | '));
  ok('...and it\'s kept', (await has('alarm_jammer')) === 1);
  ok('...nothing jammed', (await iget('bm.gvjam')) === 0, `${await iget('bm.gvjam')}`);
  // ---- a cursed, hard-way room, skipped
  const room = `@e[type=minecraft:marker,tag=bm.gvr_girder,scores={bm.gvi=${GI}},limit=1]`;
  if (!ok('the job has the Girder Climb', await passes(`execute in bm:gutter if entity ${room}`))) return done();
  await run(`execute in bm:gutter as ${room} at @s run tp TestRat ~ ~ ~`); await sleep(3500); A.stand();
  await run(`execute in bm:gutter run scoreboard players set ${room} bm.gvcrs 1`); await run(`execute in bm:gutter run tag ${room} add bm.gvskull`);   // (the stage: cursed, the hard way)
  const pot0 = await iget('bm.gvpot'), lv0 = await iget('bm.gvlv');
  A.slot(7); await sleep(300); await A.useWait(); await sleep(400);
  const lb = await A.press(/Skip this room/); await sleep(800); const yb = await A.press(/Skip it/); await sleep(1500);
  const gvs = await num(`execute in bm:gutter run scoreboard players get ${room} bm.gvs`);
  ok('a cursed hard-way room skipped through the Ledger: the way opens for a try', !!lb && !!yb && gvs === 3 && (await iget('bm.gvlv')) === lv0 - 1,
     `ledger ${!!lb}, yes ${!!yb}, state ${gvs}, tries ${lv0} -> ${await iget('bm.gvlv')}`);
  ok('...and the pot gets nothing (no "curse lifts", no "hard way pays")', (await iget('bm.gvpot')) === pot0 && !A.bars.some(b => /curse lifts|hard way pays/i.test(b)),
     `pot ${pot0} -> ${await iget('bm.gvpot')}; ${A.bars.slice(-3).join(' | ')}`);
  // ---- a find in the pot, then out through the den door
  const pid = await num('scoreboard players get TestRat bm.pid');
  await run(`data modify storage bm:gv pot.p${pid} set value [{t:"t408 find"}]`);   // (the stage: something found on the way, waiting for a win)
  ok('(the stage: a find waiting in the pot)', /t408 find/.test(await run(`data get storage bm:gv pot.p${pid}`)));
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run tp TestRat ~ ~ ~`); await sleep(1000);
  const n0 = A.dialogN.length;
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.exitm] at @s if entity @e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${GI}},distance=..60] run tp TestRat ~ ~ ~`);
  ok('the den door: "Leave the heist?"', await wait(4000, async () => A.dialogN.length > n0), '');
  const lv = await A.press(/Leave now/); await sleep(2500);
  ok('..."Leave now": off the heist', !!lv && !(await passes('execute if entity @a[name=TestRat,tag=bm.gvp]')));
  ok('...and the find stayed behind (not waiting for the next win)', !/t408 find/.test(await run(`data get storage bm:gv pot.p${pid}`)), await run(`data get storage bm:gv pot.p${pid}`));
  return done();

  async function done() {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run('function bm:admin/rooms_any'); await run('function bm:admin/plan_safe'); await run('clear TestRat'); await run('effect clear TestRat');
    await run('execute as @a[name=TestRat,tag=bm.gvp] at @s run function bm:p70/home');
    await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
    const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
    A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
  }
})().catch(e => { console.error(e); process.exit(1); });

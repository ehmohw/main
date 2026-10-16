// 2.80h: the Fixer's mercy and the crew bonuses - as regular (non-op) players, TestRat and TestMouse. rcon sets the stage: a
// Tier I heist of Lever Rooms with both in the crew, down to its last try, 40 coins in the pot; the guardian put down.
//   In an unsolved Lever Room, [Skip this puzzle] on the last try: THE FIXER'S MERCY asks first - half the pot and a share.
//   Pay: the way on opens, the pot is halved, the crew keeps its last try. A second room: the mercy is spent.
//   Won (stepping onto the strongbox ring): a crew of two, nobody knocked out - CREW OF 2 and CLEAN CREW in the prize roll,
//   and the card says crew +1 share, clean crew +1 Token, and what the mercy cost.
const { bot, rcon, sleep } = require('./lib_resp');
const H_ = require('./h110'); const { rel } = H_;
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = H_.mk(run); const { num, cnt } = H;
  const G = 'execute in bm:gutter run ';
  const A = await bot('TestRat'); await sleep(1500); const M = await bot('TestMouse'); await sleep(2500); A.stand(); M.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  for (const f of ['prime_never', 'fork_never', 'traps_never', 'curse_never']) await run(`function bm:admin/${f}`);
  const seen = []; let nT = 0; const tick = setInterval(() => { while (nT < A.titles.length) seen.push(A.titles[nT++]); }, 50);

  await H.heist('levers', 'a', 1); await H.begin(); await sleep(1500);
  await H.mouse();                                                                  // (the stage: TestMouse in the crew)
  const GI = await num('scoreboard players get TestRat bm.gvi');
  const I = `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI}},limit=1]`;
  await run(`${G}scoreboard players set ${I} bm.gvlv 1`); await run(`${G}scoreboard players set ${I} bm.gvpot 40`);   // (the last try; 40 coins gathered)
  const qs = await H.qs('levers');
  ok('a heist of Lever Rooms, a crew of two, down to its last try', qs.length >= 2 && (await num(`${G}scoreboard players get ${I} bm.gvlv`)) === 1, `rooms ${qs}`);
  await H.go('levers', qs[0], 4, 12); await run(`execute as TestMouse at TestRat run tp @s ~1 ~ ~`); await sleep(800);

  // ---- [Skip this puzzle] on the last try: the mercy asks first
  A.dialogN.length = 0; A.cmd('trigger bm.act set 7733'); await sleep(900);
  const d = JSON.stringify(A.dialogN.slice(-1)[0] || '');
  ok('[Skip this puzzle] on the last try: the Fixer\'s mercy asks first (half the pot, 20 of 40, and a share)', /Fixer's mercy/.test(d) && /20 of 40 coins/.test(d), d.slice(0, 160));
  await A.press(/Pay the Fixer/); await sleep(1200);
  ok('...paid: the way on opens', await H.solved('levers', qs[0]));
  ok('...the pot is halved, the crew keeps its last try', (await num(`${G}scoreboard players get ${I} bm.gvpot`)) === 20 && (await num(`${G}scoreboard players get ${I} bm.gvlv`)) === 1,
     `pot ${await num(`${G}scoreboard players get ${I} bm.gvpot`)}, tries ${await num(`${G}scoreboard players get ${I} bm.gvlv`)}`);
  ok('...and the crew is told', M.chats.some(c => /called in the Fixer's mercy/.test(c)), M.chats.slice(-2).join(' | ').slice(0, 160));
  // ---- once a heist
  await H.go('levers', qs[1], 4, 12); await sleep(600);
  A.chats.length = 0; A.dialogN.length = 0; A.cmd('trigger bm.act set 7733'); await sleep(900);
  ok('a second room on the last try: the mercy is spent (no dialog, it says so)', A.chats.some(c => /mercy is spent/.test(c)) && !A.dialogN.length, A.chats.slice(-1).join(''));

  // ---- won: crew bonuses
  const V = `@e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${GI}},limit=1]`;
  const B = `@e[tag=bm.gvboss,scores={bm.gvi=${GI}},limit=1]`;
  await run(`execute in bm:gutter as ${V} at @s run tp TestRat ${rel(6, 4, 12)} -90 0`); await run(`execute in bm:gutter as ${V} at @s run tp TestMouse ${rel(6, 4, 14)} -90 0`);
  await wait(12000, async () => (await cnt(B)) === 1 && !/bm\.cfrz/.test(await run(`${G}data get entity ${B} Tags`)));
  await run(`${G}data modify entity ${B} DeathLootTable set value "minecraft:empty"`); await run(`${G}kill ${B}`);
  await wait(12000, async () => (await num(`${G}scoreboard players get ${V} bm.gvs`)) === 2);
  const vp = (await run(`${G}data get entity ${V} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  const vx = Math.floor(+vp[1]), vz = Math.floor(+vp[3]);
  await run(`execute in bm:gutter as ${V} at @s run tp TestRat ${rel(24, 4, 9)} -90 0`); await run(`execute in bm:gutter as ${V} at @s run tp TestMouse ${rel(24, 4, 15)} -90 0`); await sleep(600);
  seen.length = 0;
  await Promise.all([A.walkTo(vx + 16.5, vz - 2.5), M.walkTo(vx + 16.5, vz + 3.5)]); await sleep(300);
  ok('both on the strongbox ring: the payout', await wait(5000, async () => seen.some(t => /THE HAUL/.test(t))));
  ok('the prize roll: CREW OF 2 (+1 share)...', await wait(16000, async () => seen.some(t => /CREW OF 2/.test(t))), seen.join(' | ').slice(0, 300));
  ok('...and CLEAN CREW (+1 Token)', seen.some(t => /CLEAN CREW/.test(t)));
  await run('execute as TestRat run function bm:p103/res_load'); const rr = await run('data get storage bm:ui res.r_res');
  ok('the card: crew +1 share, clean crew +1 Token, and what the mercy cost', /crew \+1 share/.test(rr) && /clean crew \+1 Token/.test(rr) && /mercy took half the pot and a share/.test(rr), rr.slice(-300));

  clearInterval(tick);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('tag TestMouse remove bm.gvp'); await run('clear TestRat'); await run('clear TestMouse'); await run('scoreboard players set TestRat bm.gstk 0'); await run('scoreboard players set TestMouse bm.gstk 0');
  for (const f of ['prime_chance', 'fork_chance', 'traps_chance', 'curse_chance', 'rooms_any', 'variant_random', 'plan_safe']) await run(`function bm:admin/${f}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); A.end(); M.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

// 2.94q: THE PARTNER WHEEL'S "KEEP UP", as a regular (non-op) player. Emma goes on the wheel (her ribbon in the off hand + use)
// and is called from its page; Bender is called with his own ball (carried, not on the wheel). Pressed on the wheel's page:
// "Keep up: off" -> on. rcon carries the bot 200 blocks off (the stage, as an ender pearl or a horse would):
//   mid-air: both "fell behind" (gone home) - and not back while falling; landed: both back at your side.
//   into deep water far off: both back while swimming.
//   in creative: not back; survival again: back.
//   in the Nether: both back there.
//   Bender's ball dropped: Emma back, Bender not (no item, not on the wheel).
//   "Keep up" pressed off: Emma "couldn't keep up and went home", and not back.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const O = 'execute in minecraft:overworld run ', N = 'execute in minecraft:the_nether run ';
  const cnt = async (sel, D = O) => { const m = (await run(`${D}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const EMMA = '@e[type=minecraft:cat,tag=bm.emmapet]', BEN = '@e[type=minecraft:wolf,tag=bm.bvpet]';
  const near = (sel, D = O) => cnt(`${sel.slice(0, -1)},distance=..6]`, `${D}execute at TestRat run `);
  const both = async (D = O) => (await near(EMMA, D)) === 1 && (await near(BEN, D)) === 1;
  const none = async () => (await cnt(EMMA)) + (await cnt(BEN)) + (await cnt(EMMA, N)) + (await cnt(BEN, N)) === 0;
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const SITES = [[18200, 100, 16100], [18400, 100, 16100], [18600, 100, 16100], [18800, 100, 16100]];
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run('tag TestRat remove bm.pwkeep');
  for (const [x, y, z] of SITES) {
    await run(`${O}forceload add ${x - 8} ${z - 8} ${x + 8} ${z + 8}`);
    await run(`${O}fill ${x - 8} ${y} ${z - 8} ${x + 8} ${y} ${z + 8} minecraft:sandstone`); await run(`${O}fill ${x - 8} ${y + 1} ${z - 8} ${x + 8} ${y + 40} ${z + 8} minecraft:air`);
  }
  // (two pools: a tamed host left in a loaded chunk teleports to you by itself - vanilla's own follow - when there's ground by
  // you; not to you swimming, gliding or riding, which is when a partner is left behind for good)
  for (const i of [2, 3]) { const [x, y, z] = SITES[i]; await run(`${O}fill ${x - 4} ${y + 1} ${z - 4} ${x + 4} ${y + 6} ${z + 4} minecraft:water`); }
  await run(`${N}forceload add 2000 2000 2016 2016`); await run(`${N}fill 2000 100 2000 2016 100 2016 minecraft:netherrack`); await run(`${N}fill 2000 101 2000 2016 106 2016 minecraft:air`);
  await run(`${O}execute as ${EMMA} run function bm:p62/emma_go`); await run(`${O}execute as ${BEN} run function bm:p195/go`);
  for (const t of ['wolf', 'cat']) await run(`${O}execute as @e[type=minecraft:${t}] if score @s bm.pid = TestRat bm.pid run tp @s ~ -300 ~`);
  await sleep(2500);
  await run('scoreboard players set TestRat bm.emcd 0'); await run('scoreboard players set TestRat bm.bvcd 0'); await run('scoreboard players set TestRat bm.pw0 0');
  const go = async (i, dy = 1, D = O, xyz = null) => { const [x, y, z] = xyz || SITES[i]; await run(`${D}tp TestRat ${x + 0.5} ${y + dy} ${z + 0.5} -90 0`); };
  await go(0); await sleep(1500); A.stand();
  await run('loot replace entity TestRat hotbar.0 loot bm:items/partner_wheel'); await run('loot replace entity TestRat hotbar.1 loot bm:items/bv_ball');
  await run('loot replace entity TestRat weapon.offhand loot bm:items/emma_ribbon'); await sleep(400);
  await use(0); await sleep(600);
  ok('Emma\'s Ribbon in the off hand + use the wheel: it goes on', (await sc('TestRat', 'bm.pw0')) === 1);

  // ---- the wheel's page: "Keep up: off" -> pressed: on, the page back
  await sleep(2500); let n0 = A.dialogN.length; await use(0); await wait(3000, async () => A.dialogN.length > n0);
  const kb = () => (A.buttons().map(b => JSON.stringify(b)).find(t => /Keep up/.test(t)) || '');
  ok('the wheel\'s page shows "Keep up: off"', /off/.test(kb()), kb());
  A.chats.length = 0; n0 = A.dialogN.length; await A.press(/Keep up/); await sleep(800);
  ok('pressed: "Keep up: on", the page back reading on', /Keep up: on/.test(A.chats.join(' ')) && A.dialogN.length > n0 && /on/.test(kb()) && !/off/.test(kb()), kb());
  await A.press(/Call Emma/); await sleep(800);
  ok('Emma called from the wheel\'s page', await wait(5000, async () => (await cnt(EMMA)) === 1));
  await sleep(1500); await use(1);
  ok('Bender called with his ball', await wait(5000, async () => (await cnt(BEN)) === 1));
  await sleep(2500);

  // ---- 200 blocks off, in mid-air: they fall behind - and aren't back until you land
  A.unstand(); const air = setInterval(() => { try { A.ground(false); } catch (e) {} }, 50);      // (the bot doesn't fall by itself: it tells the server it's airborne)
  A.chats.length = 0; await go(1, 30); await sleep(150);
  ok('carried 200 blocks off, 30 up: Emma and Bender "fell behind"', await wait(5000, async () => A.chats.filter(c => /fell behind/.test(c)).length >= 2),
     A.chats.filter(c => /fell behind|keep up/.test(c)).join(' | '));
  ok('...both gone home (not left standing back there)', await none());
  await sleep(2500);
  ok('...still falling: not back yet', (await cnt(EMMA)) + (await cnt(BEN)) === 0);
  clearInterval(air); await go(1); await sleep(300); A.stand();                                  // (landed)
  ok('landed: both back at your side', await wait(9000, both));

  // ---- into water far off
  await sleep(1500); A.chats.length = 0; await go(2, 3);
  ok('into deep water 200 blocks on: both back while you swim', await wait(9000, both), A.chats.filter(c => /fell behind|keep up/.test(c)).join(' | '));

  // ---- creative (in the far pool): not back; survival: back
  await sleep(1500); await run('gamemode creative TestRat'); A.chats.length = 0; await go(3, 3);
  ok('in creative, carried off: they fall behind', await wait(5000, async () => A.chats.filter(c => /fell behind/.test(c)).length >= 2), `${A.chats.join(' | ')} ${await cnt(EMMA)} ${await cnt(BEN)} ${await run('data get entity TestRat Pos')} ${await run(`${O}data get entity ${EMMA.slice(0, -1)},limit=1] Pos`)}`);
  await sleep(3000);
  ok('...and not back while in creative', (await cnt(EMMA)) + (await cnt(BEN)) === 0);
  await run('gamemode survival TestRat');
  ok('survival again: back', await wait(9000, both));

  // ---- the Nether
  await sleep(1500); A.chats.length = 0; await go(0, 1, N, [2008, 100, 2008]);
  ok('through to the Nether: both back there', await wait(12000, async () => both(N)), A.chats.filter(c => /fell behind|keep up/.test(c)).join(' | '));

  // ---- Bender's ball dropped: Emma back (the wheel), Bender not
  await sleep(1500); await go(0); await sleep(500); A.chats.length = 0;
  await wait(9000, both);
  await run('item replace entity TestRat hotbar.1 with minecraft:air'); await go(2, 3);   // (into a pool: no vanilla follow-teleport)
  await wait(5000, async () => A.chats.some(c => /Emma fell behind/.test(c)));
  ok('his ball gone (no item, not on the wheel): Emma back, Bender not', await wait(9000, async () => (await near(EMMA)) === 1) && (await cnt(BEN)) === 0,
     `${await cnt(EMMA)} ${await cnt(BEN)} | ${A.chats.join(' | ').slice(0, 300)} | ball: ${/bv_ball/.test(await run('data get entity TestRat Inventory'))} tags: ${await run('tag TestRat list')}`.slice(0, 900));

  // ---- switched off: "couldn't keep up", and not back
  await sleep(2500); n0 = A.dialogN.length; await use(0); await wait(3000, async () => A.dialogN.length > n0);
  A.chats.length = 0; await A.press(/Keep up/); await sleep(800);
  ok('"Keep up" pressed again: off', /Keep up: off/.test(A.chats.join(' ')) && !/bm\.pwkeep/.test(await run('tag TestRat list')));
  A.chats.length = 0; await go(3, 3);
  ok('carried off (into the far pool): Emma "couldn\'t keep up and went home"', await wait(5000, async () => A.chats.some(c => /couldn't keep up/.test(c))), `${A.chats.join(' | ')} ${await cnt(EMMA)}`);
  await sleep(4000);
  ok('...and stays home', (await cnt(EMMA)) === 0);

  // ---- clean up
  await run(`${O}execute as ${EMMA} run function bm:p62/emma_go`); await run(`${O}execute as ${BEN} run function bm:p195/go`); await run(`${N}execute as ${BEN} run function bm:p195/go`);
  await run(`${N}execute as ${EMMA} run function bm:p62/emma_go`);
  await run('scoreboard players set TestRat bm.pw0 0'); await run('tag TestRat remove bm.pw_emma'); await run('tag TestRat remove bm.pwkeep'); await run('clear TestRat');
  await go(0);
  for (const [x, y, z] of SITES) await run(`${O}forceload remove ${x - 8} ${z - 8} ${x + 8} ${z + 8}`);
  await run(`${N}forceload remove 2000 2000 2016 2016`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

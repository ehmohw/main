// 2.80a: the coat check, airtight - as a regular (non-op) player (rcon sets the stage: a platform, gear in the pack, a death,
// a stray arrival in the vault the way a command or a mod would put you there).
//   the Locker Hall from the Ledger (Office > Locker Hall, hold still): the Fixer checks your gear at its door now (it
//     could be put in a locker and fetched out later); the hall's plate takes you home with it all handed back.
//   a death in the vault, then a Pearl of Return at home: it won't take you back into the vault (refunded).
//   a stray in a heist's rooms (not on the job, not checked): seen out, home, within a second - their own gear with them.
//   a stray in the Lounge: checked on the spot; its door hands it all back at home.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const passes = async c => /passed/i.test(await run(c));
  const fnTrue = async (pre, f) => /returned [1-9]/.test(await run(`execute ${pre} run function ${f}`));
  const dim = async () => (await run('data get entity TestRat Dimension')).replace(/.*data: /, '');
  const has = async (id, slot = 'container.*') => passes(`execute if items entity TestRat ${slot} minecraft:${id}`);
  const hasBm = async (id) => passes(`execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"${id}"}]`);
  const tags = async () => (await run('tag TestRat list')).replace(/.*: /, '');
  const pos = async () => { const m = (await run('data get entity TestRat Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const press = async (re) => { const b = await A.press(re); await sleep(900); return b; };
  const O = 'execute in minecraft:overworld run ', GU = 'execute in bm:gutter run ';
  const HX = 13400, HY = 121, HZ = 13400;
  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  // ---- the stage
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run(`${O}forceload add ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`); await run(`${O}fill ${HX - 4} ${HY - 1} ${HZ - 4} ${HX + 4} ${HY - 1} ${HZ + 4} minecraft:stone`);
  await run(`${O}fill ${HX - 4} ${HY} ${HZ - 4} ${HX + 4} ${HY + 3} ${HZ + 4} minecraft:air`);
  await run(`${O}tp TestRat ${HX + 0.5} ${HY} ${HZ + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run(`spawnpoint TestRat ${HX} ${HY} ${HZ}`);
  for (const t of ['bm.gvp', 'bm.lgbag', 'bm.lgstart', 'bm.lkadv', 'bm.lgadv', 'bm.gvok']) await run(`tag TestRat remove ${t}`);
  await run('execute store result storage bm:lg tmp.pid int 1 run scoreboard players get TestRat bm.pid');
  const pid = +((await run('scoreboard players get TestRat bm.pid')).match(/has (\d+)/) || [0, 0])[1];
  for (const k of ['bag', 'cb', 'ret']) await run(`data remove storage bm:gv ${k}.p${pid}`);
  const kit = async () => {
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger'); await run('loot give TestRat loot bm:items/token');
    await run('item replace entity TestRat hotbar.5 with minecraft:diamond_sword'); await run('item replace entity TestRat armor.head with minecraft:iron_helmet');
  };
  const home = async () => { const p = await pos(); return /overworld/.test(await dim()) && p && Math.abs(p[0] - HX - 0.5) < 2 && Math.abs(p[2] - HZ - 0.5) < 2; };
  const gear = async () => (await has('diamond_sword')) && (await has('iron_helmet', 'armor.head'));
  await kit(); await sleep(1200); A.stand();

  // ================================================================== 1. the Locker Hall, through the Ledger
  A.slot(0); await sleep(300); await A.useWait(); A.chats.length = 0; await press(/Locker Hall/);
  const inHall = await wait(8000, async () => /gutter/.test(await dim()), 300); await sleep(1500); A.stand();
  ok('Office > Locker Hall (hold still): in the Locker Hall', inHall && await fnTrue('as TestRat', 'bm:p84/lk/inside'), await dim());
  ok('...the Fixer checks your gear at its door (he says so)', A.chats.some(c => /Locker Hall.*checks your gear/.test(c)), A.chats.slice(-2).join(' / ').slice(0, 220));
  ok('...your sword and helmet stay with him; the Ledger and Tokens come in', !(await has('diamond_sword')) && !(await has('iron_helmet', 'armor.head')) && (await hasBm('fixers_ledger')) && (await hasBm('token')));
  // the hall's exit plate
  await A.walkTo(-248.5, -241.5); await wait(6000, async () => /overworld/.test(await dim()), 300); await sleep(3500); A.stand();
  ok('The hall\'s plate: home where you stood, gear handed back', (await home()) && (await gear()), `${await dim()} ${await pos()} sword ${await has('diamond_sword')}`);

  // ================================================================== 2. a death in the vault - then a Pearl of Return
  A.slot(0); await sleep(300); await A.useWait(); await press(/Locker Hall/); await wait(8000, async () => /gutter/.test(await dim()), 300); await sleep(1200); A.stand();
  await run('kill TestRat'); await wait(8000, async () => /overworld/.test(await dim()), 300); await sleep(4000); A.stand();
  ok('Dying in the Locker Hall: you wake at home, your gear handed back', /overworld/.test(await dim()) && (await gear()));
  await run('loot replace entity TestRat hotbar.3 loot bm:items/pearl_of_return'); A.slot(3); await sleep(500); A.bars.length = 0;
  A.use(); await sleep(2200); A.release(); await sleep(1200);
  ok('...a Pearl of Return now: it won\'t take you into the vault (and it\'s refunded)', /overworld/.test(await dim()) && (await hasBm('pearl_of_return')) && A.bars.some(b => /vault's doors/.test(b)),
     `${await dim()} | ${A.bars.slice(-1).join('')}`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"pearl_of_return"}]');

  // ================================================================== 3. a stray in the heist rooms
  await kit(); await sleep(500);
  A.chats.length = 0; await run(`${GU}tp TestRat 3.5 68 12.5`);
  const out = await wait(5000, async () => /overworld/.test(await dim()), 200); await sleep(2500); A.stand();
  ok('Put into a heist\'s den by a command (not on the job): seen out within moments', out && A.chats.some(c => /not on a job/.test(c)), `${await dim()} | ${A.chats.slice(-1).join('')}`);
  ok('...home - their own gear with them', (await home()) && (await gear()), `${await pos()}`);

  // ================================================================== 4. a stray in the Lounge
  A.chats.length = 0; await run(`${GU}tp TestRat -315.5 68 -243.5 -90 0`); await sleep(2500); A.stand();
  ok('Put into the Lounge by a command: checked on the spot - the sword and helmet with the Fixer', /gutter/.test(await dim()) && !(await has('diamond_sword')) && /bm\.lgbag/.test(await tags()),
     `${await dim()} sword ${await has('diamond_sword')} | ${A.chats.slice(-1).join('').slice(0, 160)}`);
  const ex = (await run(`${GU}data get entity @e[type=minecraft:marker,tag=bm.lgexit,limit=1] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  if (ex) await A.walkTo(+ex[1], +ex[3]);
  await wait(6000, async () => /overworld/.test(await dim()), 300); await sleep(3500); A.stand();
  ok('...the Lounge\'s door: home, gear back', /overworld/.test(await dim()) && (await gear()), `${await dim()} ${await pos()}`);

  await run('clear TestRat'); await run(`${O}forceload remove ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

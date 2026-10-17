// 2.82: THE NEW MARKET'S RIVER AND CLOCK TOWER - nobody stuck, as a regular (non-op) player, every move a real packet (rcon
// sets the stage: t162's market, rebuilt into the current town if it's older). Fallen into the river: a ladder up the quay
// wall every few blocks - climbed out onto the street (the wall stands four blocks over the water). Parkoured onto the clock
// tower and dropped inside: a soft landing on hay (barely a scratch from twelve blocks), a ladder back up the inside, and a
// door at the foot - opened, walked out.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const passes = async c => /passed/i.test(await run(c));
  const blk = (x, y, z, b) => passes(`${O}execute if block ${x} ${y} ${z} ${b}`);
  const pos = async () => (await run('data get entity TestRat Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
  const health = async () => +((await run('data get entity TestRat Health')).match(/(-?[\d.]+)f/) || [0, 0])[1];
  const at = async (x, y, z) => { await run(`${O}tp TestRat ${x} ${y} ${z} 0 0`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(400); };
  // (a move the way a client makes it: one step a tick, closed with tick_end; off the ground while climbing or falling)
  const step = async (x, y, z, onGround) => { A.pos.x = x; A.pos.y = y; A.pos.z = z; A.write('position', { x, y, z, flags: { onGround, hasHorizontalCollision: false } }); A.write('tick_end', {}); await sleep(50); };
  // (t162's market: template (x, y, z) is the world's (CX + x, CY + y, CZ + z))
  const CX = 24000, CY = 30, CZ = 24000, W = 10, GF = 9, WATER_TOP = 5;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('loot replace entity TestRat hotbar.8 loot bm:items/market_key');          // (a member: no rat bouncer tossing him out)

  // ---- the stage: the market (rebuilt into the current town on the way in if it's an old one)
  await run(`${O}forceload add ${CX - 16} ${CZ - 16} ${CX + 127} ${CZ + 127}`);
  const MK = `@e[type=minecraft:marker,tag=bm.mkt,x=${CX + 38.5},y=${CY + 12},z=${CZ + 46.5},distance=..2,limit=1]`;
  await sleep(2500);
  if (!(await passes(`${O}execute if entity ${MK}`))) {
    for (let t = 0; t < 30; t++) { const pl = await run(`${O}place template bm:black_market ${CX} ${CY} ${CZ}`); if (!/not loaded/.test(pl)) break; await sleep(2000); }
  }
  await at(CX + 38.5, CY + W, CZ + 72.5);
  ok('the market is the current town (bm.m282)', await wait(40000, async () => passes(`${O}execute if entity ${MK.replace(',limit=1', ',tag=bm.m282,limit=1')}`), 500));
  await sleep(8000);                                 // (a rebuild moves everyone inside up to the Lookout, then runs every install: let it settle)

  // ---- the river: two of the ladders the build placed (market3.LADDERS - on the market side and the far bank), climbed out
  for (const [lx, z, wx, bank] of [[22, 33, 23, 'the market side'], [17, 34, 16, 'the far bank']]) {
    let ladders = 0;
    for (let y = 4; y <= GF; y++) if (await blk(CX + lx, CY + y, CZ + z, 'minecraft:ladder')) ladders++;
    ok(`fallen in the river (${bank}): a ladder from under the water up the quay wall`, ladders === GF - 3 && (await blk(CX + lx, CY + 4, CZ + z, 'minecraft:ladder[waterlogged=true]')) &&
       !(await blk(CX + wx, CY + GF, CZ + z, 'minecraft:air')) && !(await blk(CX + wx, CY + GF, CZ + z, 'minecraft:water')), `${ladders} rungs`);
    ok('...the wall stands four blocks over the water, and the top opens onto the street', (await blk(CX + wx, CY + W, CZ + z, 'minecraft:air')) && (await blk(CX + wx, CY + W + 1, CZ + z, 'minecraft:air')));
    await at(CX + lx + 0.5, CY + WATER_TOP - 0.4, CZ + z + 0.5); A.unstand();
    const tp0 = A.pos.teleportId;
    for (let y = CY + WATER_TOP - 0.4; y <= CY + W + 0.05; y += 0.12) await step(CX + lx + 0.5, Math.min(y, CY + W + 0.02), CZ + z + 0.5, false);
    for (let k = 1; k <= 6; k++) await step(CX + lx + 0.5 + (wx - lx) * k * 0.15, CY + W + 0.02, CZ + z + 0.5, false);
    for (let k = 0; k < 4; k++) await step(CX + wx + 0.5, CY + W, CZ + z + 0.5, true);
    A.stand(); await sleep(1500);
    const p1 = await pos();
    ok('...climbed out: standing on the quay at street level', A.pos.teleportId === tp0 && Math.abs(p1[1] - (CY + W)) < 0.1 && Math.floor(p1[0]) === CX + wx,
       `at ${p1.map(v => v.toFixed(1)).join(' ')}, sent back by the server: ${A.pos.teleportId !== tp0}`);
  }

  // ---- the clock tower: dropped in from the belfry - hay, the ladder, the door
  const TX = CX + 45, TZ = CZ + 32;
  ok('inside the clock tower: hay on the floor, a ladder up the inside to the belfry\'s sill', (await blk(CX + 46, CY + GF, CZ + 33, 'minecraft:hay_block')) &&
     (await blk(CX + 46, CY + W, CZ + 34, 'minecraft:ladder')) && (await blk(CX + 46, CY + 21, CZ + 34, 'minecraft:ladder')));
  await run('effect give TestRat minecraft:instant_health 1 5 true'); await sleep(600);
  const h0 = await health();
  await at(TX + 0.5, CY + 22, TZ + 0.5); A.unstand();
  for (let y = CY + 22; y > CY + W; y -= 0.6) await step(TX + 0.5, y, TZ + 0.5, false);
  for (let k = 0; k < 4; k++) await step(TX + 0.5, CY + W, TZ + 0.5, true);
  A.stand(); await sleep(1000);
  const h1 = await health();
  ok('dropped twelve blocks inside: the hay takes the fall (a scratch at most)', h1 >= h0 - 3, `${h0} -> ${h1}`);
  await at(CX + 46.5, CY + W, CZ + 32.5);
  A.useOn(CX + 46, CY + W, CZ + 31, 3); await sleep(700);
  ok('the door at the foot opens', await blk(CX + 46, CY + W, CZ + 31, 'minecraft:dark_oak_door[open=true]'));
  await A.walkTo(CX + 46.5, CZ + 29.6); await sleep(800);
  const p2 = await pos();
  await sleep(1500); const p3 = await pos();
  ok('...and he walks out of the tower (and stays out)', p2[2] < CZ + 31 && p3[2] < CZ + 31 && Math.abs(p3[1] - (CY + W)) < 0.1, `at ${p3.map(v => v.toFixed(1)).join(' ')}`);

  await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

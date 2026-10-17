// 2.82: FISHING CRATES ONLY FOR A REAL CATCH - as a regular (non-op) player with a real rod, every cast and reel a real use (rcon
// sets the stage: a floor, a pond, a pig on a lead of nothing). Hook a pig and reel it in (the rod's "hooked" trigger fires with no
// item on the line): no catch is counted - no crate, no Token roll. Cast into the pond and reel in on a bite: the catch counts
// (bm.fishr, the roll for crates and Tokens). Five pig reels (each would have been a ~10% crate/Token chance before).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const O = 'execute in minecraft:overworld run ';
  const num = async c => +(((await run(c)).match(/has (-?\d+)/) || [0, 0])[1]);
  const fishr = () => num('scoreboard players get TestRat bm.fishr');
  const X = 5300, Y = 120, Z = 5300;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run(`${O}tp TestRat ${X}.5 ${Y + 1} ${Z}.5`); await sleep(3000);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 16} minecraft:stone`);
  await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 12} ${Z + 16} minecraft:air`);
  await run(`${O}fill ${X - 3} ${Y - 3} ${Z + 6} ${X + 3} ${Y} ${Z + 12} minecraft:water`);          // (a pond, open to the sky)
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('time set day'); await run('weather clear');
  await run('item replace entity TestRat hotbar.0 with minecraft:fishing_rod[minecraft:enchantments={"minecraft:lure":3}]'); A.slot(0);
  await run(`${O}tp TestRat ${X}.5 ${Y + 1} ${Z}.5 0 10`); await sleep(1200);
  const look = (yaw, pitch) => { A.pos.yaw = yaw; A.pos.pitch = pitch; A.write('look', { yaw, pitch, flags: { onGround: true, hasHorizontalCollision: false } }); };
  const bobber = async () => /passed/i.test(await run(`${O}execute if entity @e[type=minecraft:fishing_bobber,x=${X},y=${Y},z=${Z},distance=..30]`));

  // ---- hook a pig and reel it in: no catch
  await run('execute as TestRat run scoreboard players set @s bm.fishr 0');
  let hooked = 0;
  for (let k = 0; k < 5; k++) {
    await run(`${O}kill @e[type=minecraft:pig,x=${X},y=${Y},z=${Z},distance=..30]`);
    await run(`${O}summon minecraft:pig ${X}.5 ${Y + 1} ${Z + 3}.5 {NoAI:1b,Tags:["bm.t197pig"]}`); await sleep(300);
    look(0, 18); await sleep(200);
    A.use(); await sleep(1500);                                   // cast: the bobber flies into the pig and bites it
    const p0 = (await run(`${O}data get entity @e[type=minecraft:pig,tag=bm.t197pig,limit=1] Pos[2]`)).match(/(-?[\d.]+)d/);
    A.use(); await sleep(800);                                    // reel in: the pig is yanked toward the rod
    const p1 = (await run(`${O}data get entity @e[type=minecraft:pig,tag=bm.t197pig,limit=1] Motion[2]`)).match(/(-?[\d.]+)d/);
    if (p1 && +p1[1] < -0.05) hooked++;
    await sleep(500);
  }
  const f0 = await fishr();
  ok('a pig hooked and reeled in (5 times): no catch counted - no crate, no Token roll', hooked >= 3 && f0 === 0, `pulled ${hooked}/5, catches ${f0}`);
  await run(`${O}kill @e[type=minecraft:pig,x=${X},y=${Y},z=${Z},distance=..30]`);

  // ---- a real catch: cast into the pond, reel in on the bite
  await run(`${O}tp TestRat ${X}.5 ${Y + 1} ${Z + 3}.5 0 30`); await sleep(1200);
  let caught = 0;
  for (let k = 0; k < 3 && caught < 2; k++) {
    look(0, 35); await sleep(200); A.use(); await sleep(1500);
    let bit = false; const t0 = Date.now();
    while (Date.now() - t0 < 30000) {
      const m = (await run(`${O}data get entity @e[type=minecraft:fishing_bobber,limit=1] Motion[1]`)).match(/(-?[\d.E-]+)d/);
      if (m && +m[1] < -0.15) { bit = true; break; }
      await sleep(100);
    }
    const before = await fishr();
    A.use(); await sleep(1200);
    if (bit && (await fishr()) === before + 1) caught++;
  }
  ok('a real catch from the pond (reeled in on the bite): it counts - the crate and Token roll happen', caught >= 1, `${caught} counted, catches now ${await fishr()}`);

  await run('clear TestRat');
  await run(`${O}fill ${X - 8} ${Y - 3} ${Z - 8} ${X + 8} ${Y + 12} ${Z + 16} minecraft:air`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

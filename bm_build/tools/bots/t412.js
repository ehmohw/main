// 3.1x: THE CREW STILL CROSSING, PART TWO - as a regular (non-op) player TestRat (rcon sets the stage only: Tokens, the Ledger, the
// job's rooms all of one kind and variant, a beam that gave way, the room beaten by the crew ahead - its own finish run as it would
// be - a straggler's slip, an arrow on a plate).
//  - The Crumbling Rafters (A), beaten: the beam that gave way comes back; a straggler in the hay is hauled to the far ledge, no alarm;
//  - The Bell Tower (A): an arrow lobbed onto the landing plate doesn't count - TestRat standing on it does;
//  - The Sky Isles, won: a slip off the bridges carries you to the east island, by the way out - no knock-out.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found )(-?\d+)/) || [0, -99])[1]);
  const passes = async c => /passed/i.test(await run(c));
  const MINE = 'if score @s bm.gvi = TestRat bm.gvi';
  const iget = async (obj) => +(((await run(`execute as @e[type=minecraft:marker,tag=bm.gvinst] ${MINE} run scoreboard players get @s ${obj}`)).match(/has (-?\d+)/) || [0, -99])[1]);
  const eidOf = async sel => { const m = (await run(`execute in bm:gutter run data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  for (const o of ['bm.crew', 'bm.crewoff', 'bm.crewoff2', 'bm.crewoff3', 'bm.fcon', 'bm.fcon2', 'bm.gvhr']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const f of ['plan_anywhere', 'heist_hard_never', 'heist_variants_never', 'prime_never', 'fork_never', 'traps_never', 'curse_never', 'variant_a']) await run(`function bm:admin/${f}`);

  let GI = 0;
  const plan = async (room) => {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run(`function bm:admin/rooms_only_${room}`);
    await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat saturation 900 0 true');
    await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players set TestRat bm.gvhc 0');
    await run('execute in minecraft:overworld run fill 12998 119 12998 13002 119 13002 stone'); await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
    await sleep(2000);
    for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players set TestRat bm.gval 1');
    A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(800);
    A.cmd('trigger bm.act set 7603'); await sleep(1500); A.cmd('trigger bm.act set 7613');
    if (!await wait(40000, async () => passes('execute if entity @a[name=TestRat,tag=bm.gvp]'), 500)) return false;
    await sleep(2000); GI = await num('scoreboard players get TestRat bm.gvi');
    await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run tp TestRat ~ ~ ~`); await sleep(600);
    await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run setblock ~11 ~1 ~3 minecraft:pale_oak_button[face=wall,facing=west,powered=true]`);
    await wait(6000, async () => (await iget('bm.gvst')) === 2, 300);
    return true;
  };
  const RM = room => `@e[type=minecraft:marker,tag=bm.gvr_${room},scores={bm.gvi=${GI},bm.gvq=1},limit=1]`;
  const beat = async room => {        // (the stage: the crew ahead finishes it - the room's own finish)
    await run(`execute in bm:gutter as ${RM(room)} run scoreboard players operation #gi bm.rng = @s bm.gvi`);
    await run(`execute in bm:gutter as ${RM(room)} at @s run function bm:p70/solved`); await sleep(1200);
  };
  const near = async (room, dx, dy, dz, r) => passes(`execute in bm:gutter as ${RM(room)} at @s positioned ~${dx} ~${dy} ~${dz} if entity @a[name=TestRat,distance=..${r}]`);
  const alarm = async () => iget('bm.gva');

  // ================================================================== THE CRUMBLING RAFTERS (A)
  if (ok('a job of Crumbling Rafters planned through the Ledger', await plan('rafters'))) {
    await run(`execute in bm:gutter as ${RM('rafters')} at @s run tp TestRat ~-11 ~ ~ -90 0`); await sleep(2500); A.stand();
    const BEAM = `@e[type=minecraft:marker,tag=bm.gvraf,distance=..16,sort=nearest,limit=1]`;
    await run(`execute in bm:gutter as ${RM('rafters')} at @s as ${BEAM} run scoreboard players set @s bm.gvx 1`); await sleep(600);   // (the stage: a beam gives way)
    const fallen = await passes(`execute in bm:gutter as ${RM('rafters')} at @s as ${BEAM} at @s if block ~ ~-1 ~ minecraft:air`);
    await beat('rafters');
    ok('...a beam gave way, then the room was beaten by the crew ahead', fallen && (await num(`execute in bm:gutter run scoreboard players get ${RM('rafters')} bm.gvs`)) === 3);
    ok('...the beam comes back for the crew still crossing', await wait(3000, async () => passes(`execute in bm:gutter as ${RM('rafters')} at @s as ${BEAM} at @s unless block ~ ~-1 ~ minecraft:air`), 200));
    const a0 = await alarm();
    A.unstand(); await run(`execute in bm:gutter as ${RM('rafters')} at @s run tp TestRat ~-2 ~-3 ~ -90 0`);    // (the stage: a slip into the hay)
    ok('a straggler in the hay is hauled to the far ledge', await wait(3000, async () => near('rafters', 10, 0, 0, 1.5), 150), await run('data get entity TestRat Pos'));
    A.stand(); await sleep(400);
    ok('...and no alarm for it', (await alarm()) === a0, `${a0} -> ${await alarm()}`);
  }

  // ================================================================== THE BELL TOWER (A)
  if (ok('a job of Bell Towers planned through the Ledger', await plan('climb'))) {
    await run(`execute in bm:gutter as ${RM('climb')} at @s run tp TestRat ~-10 ~ ~ -90 0`); await sleep(2500); A.stand();
    await run(`execute in bm:gutter as ${RM('climb')} at @s run summon minecraft:arrow ~9.5 ~10.1 ~0.5 {Tags:["bm.t412a"],pickup:0b,life:1100s}`); await sleep(2500);   // (the stage: an arrow lobbed onto the plate)
    const pressed = await passes(`execute in bm:gutter as ${RM('climb')} at @s unless block ~9 ~10 ~ minecraft:light_weighted_pressure_plate[power=0]`);
    ok('an arrow on the landing plate: pressed - but the tower isn\'t beaten by it', pressed && (await num(`execute in bm:gutter run scoreboard players get ${RM('climb')} bm.gvs`)) !== 3, `pressed ${pressed}`);
    await run('execute in bm:gutter run kill @e[type=minecraft:arrow,tag=bm.t412a]');
    await run(`execute in bm:gutter as ${RM('climb')} at @s run tp TestRat ~9.5 ~10 ~0.5 -90 0`);   // (the stage: the climb made - TestRat steps onto the plate)
    ok('...TestRat standing on it: beaten', await wait(4000, async () => (await num(`execute in bm:gutter run scoreboard players get ${RM('climb')} bm.gvs`)) === 3, 200));
  }

  // ================================================================== THE SKY ISLES
  if (ok('a job of Sky Isles planned through the Ledger', await plan('isles'))) {
    await run(`execute in bm:gutter as ${RM('isles')} at @s run tp TestRat ~-10 ~ ~ -90 0`); await sleep(2500); A.stand();
    await beat('isles'); await run(`execute in bm:gutter as ${RM('isles')} at @s run kill @e[tag=bm.gvg,distance=..30]`);
    A.unstand(); await run(`execute in bm:gutter as ${RM('isles')} at @s run tp TestRat ~4 ~-5 ~3 -90 0`);    // (the stage: a slip off a bridge on the way out)
    ok('won: a slip off the bridges carries you to the east island, by the way out', await wait(3000, async () => near('isles', 10, 0, 0, 1.5), 150), await run('data get entity TestRat Pos'));
    A.stand(); await sleep(400);
    ok('...still on the heist (no knock-out)', await passes('execute if entity @a[name=TestRat,tag=bm.gvp]'));
  }

  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const f of ['rooms_any', 'plan_safe', 'heist_hard_any', 'heist_variants_off', 'prime_chance', 'fork_chance', 'traps_chance', 'curse_chance', 'variant_random']) await run(`function bm:admin/${f}`);
  await run('execute as @a[name=TestRat,tag=bm.gvp] at @s run function bm:p70/home'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

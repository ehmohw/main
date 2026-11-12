// 3.1w: THE CREW STILL CROSSING, AND THE FIXER'S OWN KIT - as a regular (non-op) player TestRat (rcon sets the stage only: Tokens,
// the Ledger, the job's rooms all of one kind, the room beaten by someone else - its own finish run as it would be - a straggler's
// slip into the pit, a kit bow in hand).
//  - The Tile Floor, beaten by the crew ahead: a straggler who drops into the coin pit is hauled over to the far side (not back to
//    the start, behind bars), and no alarm for it;
//  - The Grapple, beaten: the Fixer's hook still answers for the crew still crossing; a fall into the hay carries you to the far ledge;
//  - The Tinker's Bench: the kit's own bow held out at the hatch (a real click) - refused ("my own kit"), kept, and the room not solved.
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
  for (const f of ['plan_anywhere', 'heist_hard_never', 'heist_variants_never', 'prime_never', 'fork_never', 'traps_never', 'curse_never']) await run(`function bm:admin/${f}`);

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

  // ================================================================== THE TILE FLOOR
  if (ok('a job of Tile Floors planned through the Ledger', await plan('tiles'))) {
    await run(`execute in bm:gutter as ${RM('tiles')} at @s run tp TestRat ~-10 ~ ~ -90 0`); await sleep(2500); A.stand();
    await beat('tiles');
    ok('...beaten by the crew ahead', (await num(`execute in bm:gutter run scoreboard players get ${RM('tiles')} bm.gvs`)) === 3);
    const a0 = await alarm();
    A.unstand(); await run(`execute in bm:gutter as ${RM('tiles')} at @s run tp TestRat ~-2 ~-3 ~ -90 0`);    // (the stage: a slip into the coin pit)
    ok('a straggler in the coin pit is hauled over to the far side', await wait(3000, async () => near('tiles', 10, 0, 0, 1.5), 150),
       await run('data get entity TestRat Pos'));
    A.stand(); await sleep(400);
    ok('...and no alarm for it', (await alarm()) === a0, `${a0} -> ${await alarm()}`);
  }

  // ================================================================== THE GRAPPLE
  if (ok('a job of Grapples planned through the Ledger', await plan('grapple'))) {
    await run(`execute in bm:gutter as ${RM('grapple')} at @s run tp TestRat ~-10 ~ ~ -90 0`); await sleep(2500); A.stand();
    await beat('grapple'); await sleep(600);
    ok('...beaten by the crew ahead; the Fixer\'s hook still answers on the near ledge', (await num('scoreboard players get TestRat bm.gvhk')) >= 1,
       `gvs ${await num(`execute in bm:gutter run scoreboard players get ${RM('grapple')} bm.gvs`)}, hk ${await num('scoreboard players get TestRat bm.gvhk')}`);
    A.unstand(); await run(`execute in bm:gutter as ${RM('grapple')} at @s run tp TestRat ~-2 ~-4 ~ -90 0`);   // (the stage: a slip into the hay)
    ok('a fall into the hay carries you to the far ledge', await wait(3000, async () => near('grapple', 10, 0, 0, 1.5), 150), await run('data get entity TestRat Pos'));
    A.stand();
  }

  // ================================================================== THE TINKER'S BENCH
  if (ok('a job of Tinker\'s Benches planned through the Ledger', await plan('bench'))) {
    const HT = `@e[type=minecraft:interaction,tag=bm.gvhatch,limit=1,sort=nearest]`;
    await run(`execute in bm:gutter as ${RM('bench')} at @s run tp TestRat ~ ~ ~`); await sleep(2500); A.stand();
    await run('clear TestRat minecraft:bow');
    A.slot(0); await sleep(300);
    await run('item replace entity TestRat hotbar.0 with minecraft:bow[minecraft:custom_data={bm_kit:1b}]');
    await run(`execute in bm:gutter as ${RM('bench')} at @s as ${HT} at @s run tp TestRat ~ ~ ~`); await sleep(1500);
    const eid = await eidOf(`@e[type=minecraft:interaction,tag=bm.gvhatch,limit=1,sort=nearest,distance=0..]`);
    // (the hatch nearest the bot, by its own position)
    const eid2 = eid || await eidOf('@e[type=minecraft:interaction,tag=bm.gvhatch,limit=1,sort=nearest]');
    A.bars.length = 0;
    if (ok('the hatch is there to click', eid2 != null)) {
      A.interact(eid2); await sleep(900);
      ok('the kit\'s own bow at the hatch: refused - "my own kit"', A.bars.some(b => /own kit/.test(b)), A.bars.join(' | ').slice(0, 200));
      ok('...kept', /Found [1-9]/.test(await run('clear TestRat minecraft:bow[minecraft:custom_data~{bm_kit:1b}] 0')));
      ok('...and the room not solved by it', (await num(`execute in bm:gutter run scoreboard players get ${RM('bench')} bm.gvs`)) !== 3);
    }
  }

  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const f of ['rooms_any', 'plan_safe', 'heist_hard_any', 'heist_variants_off', 'prime_chance', 'fork_chance', 'traps_chance', 'curse_chance']) await run(`function bm:admin/${f}`);
  await run('execute as @a[name=TestRat,tag=bm.gvp] at @s run function bm:p70/home'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

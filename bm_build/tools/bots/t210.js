// 2.82g: THE FIXER'S LAMP, MEMORY MATCH AS A PUZZLE, AND A FAILED HEIST THAT STAYS FAILED - as a regular (non-op) player TestRat,
// every step a real packet (rcon sets the stage: Tokens, the Ledger, the next event room drawn, the modifiers, the tries left).
//   THE LAMP: Goldtooth stocks the Fixer's Lamp. In the den, on a Lights Out job, TestRat lights one (a real right-click): the job's
//   Lights Out is gone (bar and all) and the lamp is spent. Another on a job without it: refused, kept. After BEGIN: too late, kept.
//   MEMORY MATCH: out of misses, the door stays shut - a try lost, the cards reshuffled, the misses back. It offers the puzzle skip
//   like any puzzle; TestRat takes it (the dialog's own button) and the way opens.
//   A FAILED HEIST: out of tries, TestRat is in the den within a couple of seconds; walking back into the heist, TestRat is walked
//   straight back out to the den.
const { bot, rcon, sleep } = require('./lib_resp');
const H = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found )(-?\d+)/) || [0, -1])[1]);
  const passes = async c => /passed/i.test(await run(c));
  const LAMP = '*[minecraft:custom_data~{bm:"fixers_lamp"}]';
  const lamps = async () => { const o = await run(`clear TestRat ${LAMP} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/) || [0, 0])[1]); };
  const MINE = 'if score @s bm.gvi = TestRat bm.gvi';
  const inst = (cmd) => run(`execute as @e[type=minecraft:marker,tag=bm.gvinst] ${MINE} at @s run ${cmd}`);
  const iget = async (obj) => +(((await run(`execute as @e[type=minecraft:marker,tag=bm.gvinst] ${MINE} run scoreboard players get @s ${obj}`)).match(/has (-?\d+)/) || [0, -99])[1]);

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  const bars = []; A.on('boss_bar', p => { try { bars.push(Buffer.from(p.data && p.data.data ? p.data.data : p.data).toString('latin1')); } catch (e) {} });
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));

  // ---- the stage: a Tier III job with Memory Match as its first event room, planned through the Ledger's buttons
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/plan_anywhere'); await run('function bm:admin/heist_variants_never'); await run('function bm:admin/rooms_only_levers');
  await run('function bm:admin/room_memory');
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true');
  await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players set TestRat bm.gvhc 0');
  await run('execute in minecraft:overworld run fill 12998 119 12998 13002 119 13002 stone'); await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  await sleep(2000);
  for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/token');
  await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players set TestRat bm.gval 1');
  A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(800);
  A.cmd('trigger bm.act set 7603'); await sleep(1500); A.cmd('trigger bm.act set 7613');
  ok('a Tier III job planned through the Ledger: TestRat is in its den', await wait(40000, async () => passes('execute if entity @a[name=TestRat,tag=bm.gvp]'), 500));
  await sleep(2000);
  const GI = await num('scoreboard players get TestRat bm.gvi');
  const SPOT = (await run(`data get entity TestRat Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);

  // ---- the lamp
  ok('Goldtooth stocks the Fixer\'s Lamp', await passes('execute if entity @e[type=minecraft:villager,tag=bm.gvgt,nbt={Offers:{Recipes:[{sell:{components:{"minecraft:custom_data":{bm:"fixers_lamp"}}}}]}}]'));
  await inst('scoreboard players set @s bm.gvmod 1'); await inst('function bm:p70/bar'); await sleep(500);   // (the stage: Lights Out rolled)
  await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_lamp'); await run('loot replace entity TestRat hotbar.1 loot bm:items/fixers_lamp');
  bars.length = 0; A.chats.length = 0;
  A.slot(0); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(900);
  const mod = await iget('bm.gvmod');
  ok('lit in the den on a Lights Out job: no more Lights Out, the bar says so, the lamp is spent', mod % 2 === 0 && (await lamps()) === 1 &&
     bars.length > 0 && !bars.some(b => /LIGHTS OUT/.test(b)) && A.chats.some(c => /lit a Fixer's Lamp/.test(c)), `mod ${mod}, ${bars.length} bar packets, ${A.chats.slice(-1).join('').slice(0, 120)}`);
  A.bars.length = 0; A.slot(1); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(900);
  ok('...another, on a job with no Lights Out: refused, kept', (await lamps()) === 1 && A.bars.some(b => /No Lights Out on this job/.test(b)), A.bars.slice(-1).join(''));

  // ---- BEGIN (the den's own button), then the lamp is too late
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run tp TestRat ~ ~ ~`); await sleep(600);
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run setblock ~11 ~1 ~3 minecraft:pale_oak_button[face=wall,facing=west,powered=true]`);
  await wait(6000, async () => (await iget('bm.gvst')) === 2, 300);
  await inst('scoreboard players set @s bm.gvmod 1');
  A.bars.length = 0; A.slot(1); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(900);
  ok('after BEGIN: too late - the lamp is kept', (await lamps()) === 1 && A.bars.some(b => /Too late/.test(b)), A.bars.slice(-1).join(''));
  await inst('scoreboard players set @s bm.gvmod 0');

  // ---- Memory Match: out of misses
  const room = `@e[type=minecraft:marker,tag=bm.gvr_memory,scores={bm.gvi=${GI}},limit=1]`;
  const rget = async (obj) => num(`execute in bm:gutter run scoreboard players get ${room} ${obj}`);
  ok('the job has a Memory Match', await passes(`execute in bm:gutter if entity ${room}`));
  await run(`execute in bm:gutter as ${room} at @s run tp TestRat ~ ~ ~`); await sleep(2500);
  // (the interaction's type number, from a probe in view; then each card's id by where it stands)
  const seen = new Set(Object.keys(A.ents));
  const mp = (await run(`execute in bm:gutter run data get entity ${room} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
  await run(`execute in bm:gutter run summon minecraft:interaction ${mp[0]} ${mp[1] + 6} ${mp[2]} {Tags:["bm.t210probe"]}`); await sleep(700);
  const pk = Object.keys(A.ents).find(k => !seen.has(k) && Math.abs(A.ents[k].y - mp[1] - 6) < 0.1 && Math.abs(A.ents[k].x - mp[0]) < 0.1);
  const ITYPE = pk ? A.ents[pk].type : null; await run('execute in bm:gutter run kill @e[tag=bm.t210probe]');
  const cards = [];
  for (let i = 0; i < 16; i++) {
    const sel = `@e[type=minecraft:interaction,tag=bm.gvmm${i},limit=1,sort=nearest,x=${mp[0]},y=${mp[1]},z=${mp[2]},distance=..20]`;
    const sym = await num(`execute in bm:gutter run scoreboard players get ${sel} bm.gvy1`);
    const p = (await run(`execute in bm:gutter run data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    if (!p) continue; const [x, y, z] = p.slice(1).map(Number);
    const e = Object.values(A.ents).find(e => e.type === ITYPE && Math.abs(e.x - x) < 0.1 && Math.abs(e.z - z) < 0.1 && Math.abs(e.y - y) < 0.1);
    cards.push({ i, sym, x, y, z, id: e ? e.entityId : null });
  }
  const a = cards[0], b = cards.find(c => c.sym !== a.sym);
  const lv0 = await iget('bm.gvlv');
  await run(`execute in bm:gutter run scoreboard players set ${room} bm.gvy3 1`);                    // (the stage: one miss left)
  const turn = async (c) => { await run(`execute in bm:gutter run tp TestRat ${c.x} ${c.y} ${c.z + 1.6}`); await sleep(500); A.interact(c.id); await sleep(500); };
  A.chats.length = 0; await turn(a); await turn(b); await sleep(2500);
  const lv1 = await iget('bm.gvlv'), gvs = await rget('bm.gvs'), miss = await rget('bm.gvy3');
  ok('Memory Match, out of misses: the door stays shut - a try lost, the misses back (the cards reshuffled)', !!a.id && !!b.id && gvs !== 3 && lv1 === lv0 - 1 && miss > 1,
     `cards ${cards.filter(c => c.id).length}/16, tries ${lv0} -> ${lv1}, room state ${gvs}, misses ${miss}`);

  // ---- ...and it offers the puzzle skip, which TestRat takes
  A.cmd('trigger bm.act set 7733'); await sleep(1200);
  const sk = await A.press(/Skip it/); await sleep(1500);
  ok('...it can be skipped like any puzzle: the dialog\'s Skip it opens the way', !!sk && (await rget('bm.gvs')) === 3, `skip ${!!sk}, room state ${await rget('bm.gvs')}`);

  // ---- a failed heist
  await inst('scoreboard players set @s bm.gvlv 1');                                                   // (the stage: the last try)
  await run(`execute in bm:gutter as ${room} at @s run tp TestRat ~ ~ ~`); await sleep(500);
  await inst('function bm:p90/lose_try');                                                              // (and it goes)
  const near = async () => { const p = (await run('data get entity TestRat Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
    return Math.hypot(p[0] - SPOT[0], p[2] - SPOT[2]) < 4 && Math.abs(p[1] - SPOT[1]) < 3; };
  ok('out of tries: TestRat is in the den within a couple of seconds', (await iget('bm.gvst')) === 5 && await wait(3000, near, 200));
  await sleep(1500);
  A.bars.length = 0;
  await run(`execute in bm:gutter as ${room} at @s run tp TestRat ~ ~ ~`); await sleep(300);           // (walking back into the dead heist)
  ok('...walking back into the heist: straight back out to the den, told the choice is in the Ledger', await wait(3000, near, 200) &&
     A.bars.some(b => /job's off/.test(b)), A.bars.slice(-1).join('').slice(0, 120));

  // ---- clean up
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/rooms_any'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

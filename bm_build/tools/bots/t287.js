// 2.95a: EVERY ROOM THAT ISN'T A FIGHT CAN BE SKIPPED - as a regular (non-op) player TestRat, every step a real packet (rcon sets the
// stage: Tokens, the Ledger, the next event room drawn). For each of the Stalker's Ward, the Minecart Run, the Girder Climb, Block
// Party and Pipe Plaza (none of them skippable before), TestRat plans a job through the Ledger, presses BEGIN, walks into the room
// and is offered the skip in the chat; then the Ledger's own "Skip this room" -> "Skip it": the way opens, the crew loses a try, and
// what the room's own finish would have cleared is gone (the Stalker's creakings, the carts, the girder's barrels and rat, the
// Party's floor whole again, the Plaza's Grumbas and coins). And a fight (the Blaze Forge) can't be skipped: no try spent.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found )(-?\d+)/) || [0, -1])[1]);
  const passes = async c => /passed/i.test(await run(c));
  const cnt = async sel => +(((await run(`execute in bm:gutter if entity ${sel}`)).match(/count: (\d+)/i) || [0, 0])[1]);
  const MINE = 'if score @s bm.gvi = TestRat bm.gvi';
  const iget = async (obj) => +(((await run(`execute as @e[type=minecraft:marker,tag=bm.gvinst] ${MINE} run scoreboard players get @s ${obj}`)).match(/has (-?\d+)/) || [0, -99])[1]);

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  const K = [['hunted', 'the Stalker\'s Ward', async () => (await cnt('@e[type=minecraft:creaking,tag=bm.gvstalk]')) === 0, 'no creaking left stalking'],
             ['minecart', 'the Minecart Run', async () => (await cnt('@e[type=minecraft:minecart,tag=bm.gvcart]')) === 0 && !(await passes('execute if entity @a[name=TestRat,predicate=bm:p21/riding]')), 'no carts, nobody stuck riding'],
             ['girder', 'the Girder Climb', async () => (await cnt('@e[tag=bm.gvbar]')) + (await cnt('@e[tag=bm.gvgrat]')) === 0, 'no barrels, no rat'],
             ['party', 'Block Party', null, 'the floor whole again'],
             ['plaza', 'Pipe Plaza', async () => (await cnt('@e[tag=bm.gvgrum]')) + (await cnt('@e[tag=bm.gvpzc]')) === 0, 'no Grumbas, no coins'],
             ['forge', 'the Blaze Forge (a fight)', null, '']];
  for (const [kind, nm, tidy, what] of K.filter(k => !process.env.KINDS || process.env.KINDS.split(',').includes(k[0]))) {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run('function bm:admin/plan_anywhere'); await run('function bm:admin/heist_variants_never'); await run('function bm:admin/rooms_only_levers');
    await run(`function bm:admin/room_${kind}`);
    await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat saturation 900 0 true');
    await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players set TestRat bm.gvhc 0');
    await run('execute in minecraft:overworld run fill 12998 119 12998 13002 119 13002 stone'); await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
    await sleep(2000);
    for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players set TestRat bm.gval 1');
    A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(800);
    A.cmd('trigger bm.act set 7603'); await sleep(1500); A.cmd('trigger bm.act set 7613');
    if (!ok(`${nm}: a job planned through the Ledger`, await wait(40000, async () => passes('execute if entity @a[name=TestRat,tag=bm.gvp]'), 500))) continue;
    await sleep(2000);
    const GI = await num('scoreboard players get TestRat bm.gvi');
    await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run tp TestRat ~ ~ ~`); await sleep(600);
    await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby] ${MINE} at @s run setblock ~11 ~1 ~3 minecraft:pale_oak_button[face=wall,facing=west,powered=true]`);
    await wait(6000, async () => (await iget('bm.gvst')) === 2, 300);
    const room = `@e[type=minecraft:marker,tag=bm.gvr_${kind},scores={bm.gvi=${GI}},limit=1]`;
    if (!ok(`...the job has ${nm}`, await passes(`execute in bm:gutter if entity ${room}`))) continue;
    A.chats.length = 0;
    await run(`execute in bm:gutter as ${room} at @s run tp TestRat ~ ~ ~`); await sleep(3500); A.stand();
    if (kind === 'party') await run(`execute in bm:gutter as ${room} at @s run fill ~-11 ~-1 ~-11 ~-1 ~-1 ~-1 minecraft:air replace minecraft:white_concrete`);  // (the stage: a round's holes)
    const offered = A.chats.some(c => /Skip this room/.test(c));
    const lv0 = await iget('bm.gvlv');
    A.slot(7); await sleep(300); await A.useWait(); await sleep(400);
    const lb = await A.press(/Skip this room/); await sleep(800);
    if (kind === 'forge') {
      ok('A fight (the Blaze Forge) isn\'t offered the skip, and the Ledger\'s says so - no try spent, the room still to win',
         !offered && !!lb && A.chats.some(c => /fights can't be skipped|Stand in the room/.test(c)) && (await iget('bm.gvlv')) === lv0 && (await num(`execute in bm:gutter run scoreboard players get ${room} bm.gvs`)) !== 3,
         `offered ${offered}; ${A.chats.slice(-1).join('').slice(0, 120)}; tries ${lv0} -> ${await iget('bm.gvlv')}`);
      continue;
    }
    const yb = await A.press(/Skip it/); await sleep(1500);
    const gvs = await num(`execute in bm:gutter run scoreboard players get ${room} bm.gvs`);
    ok(`...walking in, ${nm} offers the skip; the Ledger's "Skip this room" -> "Skip it" opens the way for a try`,
       offered && !!lb && !!yb && gvs === 3 && (await iget('bm.gvlv')) === lv0 - 1, `offered ${offered}, ledger ${!!lb}, yes ${!!yb}, state ${gvs}, tries ${lv0} -> ${await iget('bm.gvlv')}`);
    const t = kind === 'party' ? await passes(`execute in bm:gutter as ${room} at @s if blocks ~-11 ~-1 ~-11 ~11 ~-1 ~11 ~-11 ~-1 ~-11 all`) &&
                                  !(await passes(`execute in bm:gutter as ${room} at @s unless block ~-6 ~-1 ~-6 minecraft:white_concrete`)) : await tidy();
    if (!ok(`...and tidied as its own finish would: ${what}`, t))
      for (const e of ['minecraft:creaking', 'minecraft:minecart']) console.log(`   ${e}: ` + (await run(`execute in bm:gutter as ${room} at @s as @e[type=${e},distance=..80] run data get entity @s Pos`)) + ' | marker ' + (await run(`execute in bm:gutter run data get entity ${room} Pos`)));
  }
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/rooms_any'); await run('clear TestRat'); await run('effect clear TestRat'); await run('tag TestRat remove bm.gvp');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

// 2.94f: THE SKY BUDDIES, FULLY HONOURED, as a regular (non-op) player - the trio called with the Sky Mobile (a real use), their
// menu opened (sneak + use) and its buttons pressed as the client got them: without their Honour at its height, "Change the
// weather" and "A bed on Nimbus" only say not yet; with it (rcon sets Queen Ava's rank III: hn_sky 1555), the weather page -
// Rain (it rains), again at once (the sky needs a moment), Clear skies after the 2 minutes (it clears); then at night "A bed
// on Nimbus" puts a light grey bed beside you, the bot sleeps in it (right-click), the night passes and it wakes with its spawn
// where it slept - and half a minute on the bed is gone, nothing left behind. (rcon sets the stage: a floor, the night.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const passes = async c => /passed/i.test(await run(c));
  const X = 18100, Y = 100, Z = 16000;
  const BED = `${X + 1} ${Y + 1} ${Z}`;
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const menu = async () => { const n0 = A.dialogN.length; await use(0, true); return await wait(3000, async () => A.dialogN.length > n0); };
  const raining = async () => passes(`${O}execute positioned ${X} ${Y + 1} ${Z} if predicate bm:p29/raining`);
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await sleep(2500);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.ybpet]'); await sleep(3000); await run('scoreboard players set TestRat bm.ybcd 0');
  await run('scoreboard players set TestRat bm.hn_sky 0'); await run('scoreboard players set TestRat bm.ybwx 0');
  await run('weather clear'); await run('time set 1000');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} -90 0`); await sleep(1500); A.stand();
  await run('loot replace entity TestRat hotbar.0 loot bm:items/sky_mobile'); await sleep(400);
  await use(0);
  ok('the Sky Mobile used: the Sky Buddies come', await wait(5000, async () => (await cnt('@e[type=minecraft:wolf,tag=bm.ybpet]')) === 1));
  await sleep(2500);                                                                  // (the mobile's 2-second use guard)

  // ---- not yet: their Honour isn't at its height
  ok('their menu (sneak + use) has "Change the weather" and "A bed on Nimbus"', await menu() && A.buttons().some(b => /Change the weather/.test(b.label)) &&
     A.buttons().some(b => /A bed on Nimbus/.test(b.label)), A.buttons().map(b => b.label).join(' | ').slice(0, 200));
  A.bars.length = 0; await A.press(/Change the weather/); await sleep(600);
  ok('...not yet honoured: "Change the weather" only says not yet (rank III)', A.bars.some(b => /rank III/.test(b)) && !(await raining()), A.bars.slice(-1).join(''));
  await menu(); A.bars.length = 0; await A.press(/A bed on Nimbus/); await sleep(600);
  ok('...nor a bed', A.bars.some(b => /rank III/.test(b)) && !(await passes(`${O}execute if block ${BED} minecraft:light_gray_bed`)), A.bars.slice(-1).join(''));

  // ---- their Honour at its height (Queen Ava's rank III: Vitality, Bulwark and Might all V)
  await run('scoreboard players set TestRat bm.hn_sky 1555');
  await menu(); await A.press(/Change the weather/); await sleep(600);
  ok('honoured: "Change the weather" opens the sky\'s page (Clear skies, Rain, Thunderstorm)', ['Clear skies', 'Rain', 'Thunderstorm'].every(l => A.buttons().some(b => new RegExp('^' + l).test(b.label))),
     A.buttons().map(b => b.label).join(' | '));
  A.bars.length = 0; await A.press(/^Rain/); await sleep(800);
  ok('...Rain: it rains (Nimbus: "Rain! Rain! :3")', await wait(3000, raining) && A.bars.some(b => /Rain! Rain/.test(b)), A.bars.slice(-1).join(''));
  await menu(); await A.press(/Change the weather/); await sleep(400); A.bars.length = 0; await A.press(/^Clear skies/); await sleep(800);
  ok('...again at once: the sky needs a moment (still raining)', A.bars.some(b => /needs a moment/.test(b)) && await raining(), A.bars.slice(-1).join(''));
  await run('scoreboard players set TestRat bm.ybwx 0');                              // (the 2 minutes wound forward)
  await menu(); await A.press(/Change the weather/); await sleep(400); A.bars.length = 0; await A.press(/^Clear skies/); await sleep(800);
  ok('...after the 2 minutes, Clear skies: it clears', await wait(3000, async () => !(await raining())) && A.bars.some(b => /Sun's out/.test(b)), A.bars.slice(-1).join(''));

  // ---- the bed, at night
  await run('time set 14000'); await sleep(500);
  await menu(); A.bars.length = 0; await A.press(/A bed on Nimbus/); await sleep(800);
  ok('"A bed on Nimbus": a light grey bed beside you, foot and head (Nimbus: "Hop on!")', await passes(`${O}execute if block ${BED} minecraft:light_gray_bed[part=foot]`) &&
     await passes(`${O}execute if block ${X + 2} ${Y + 1} ${Z} minecraft:light_gray_bed[part=head]`) && A.bars.some(b => /Hop on/.test(b)), A.bars.slice(-1).join(''));
  A.useOn(X + 1, Y + 1, Z, 1); await sleep(1500);
  ok('...right-clicked: the bot sleeps in it', /has the following/.test(await run('data get entity TestRat sleeping_pos')), await run('data get entity TestRat sleeping_pos'));
  ok('...the night passes', await wait(15000, async () => { const m = (await run('time query day')).match(/is at (\d+)/); return m && +m[1] % 24000 < 2000; }, 500), await run('time query day'));
  const sp = await run('data get entity TestRat respawn');
  ok('...and it wakes with its spawn where it slept (the bed\'s foot - kept when the bed\'s gone)', new RegExp(`${X + 1}, ${Y + 1}, ${Z}`).test(sp), sp.slice(0, 200));
  ok('half a minute on, awake: the bed is gone - nothing left behind (no bed, no marker, no bed item)', await wait(45000, async () =>
     !(await passes(`${O}execute if block ${BED} minecraft:light_gray_bed`)) && (await cnt('@e[type=minecraft:marker,tag=bm.ybbed]')) === 0, 1000) &&
     (await cnt(`@e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..6]`)) === 0 && !/light_gray_bed/.test(await run('data get entity TestRat Inventory')));

  // ---- clean up
  await run('scoreboard players set TestRat bm.hn_sky 0'); await run('scoreboard players set TestRat bm.ybwx 0'); await run('weather clear'); await run('time set 1000');
  await run('kill @e[type=minecraft:wolf,tag=bm.ybpet]'); await run('clear TestRat'); await run(`${O}spawnpoint TestRat 0 100 0`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

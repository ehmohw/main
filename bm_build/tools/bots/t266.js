// 2.94j: THE PARTNER WHEEL'S RECALL, as a regular (non-op) player - sneak + use the wheel and every partner of yours out in
// this world comes back to your side at once. Emma goes on the wheel (her ribbon in the off hand + use) and is called from its
// page; the Sky Buddies are called with their own Sky Mobile (a partner not on the wheel comes too). rcon carries both 9
// blocks off (the stage - short of vanilla's own 12-block follow teleport); sneak + use the wheel: both are back beside the bot (within 3 blocks - and the Sky Buddies' model with
// them, not left behind); again a moment later: the wheel is still turning (8 s); with no one out: none of your partners are out.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const X = 18200, Y = 100, Z = 16100;
  const EMMA = '@e[type=minecraft:cat,tag=bm.emmapet]', SKY = '@e[type=minecraft:wolf,tag=bm.ybpet]';
  const near = (sel, d) => cnt(`${sel.slice(0, -1)},x=${X},y=${Y + 1},z=${Z},distance=..${d}]`);
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 48} ${Z + 16}`); await sleep(2500);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 40} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 40} ${Y + 6} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X + 15},y=${Y},z=${Z},distance=..40]`);
  await run(`${O}execute as ${EMMA} run function bm:p62/emma_go`); await run(`kill ${SKY}`); await sleep(2500);
  await run('scoreboard players set TestRat bm.emcd 0'); await run('scoreboard players set TestRat bm.ybcd 0'); await run('scoreboard players set TestRat bm.pw0 0');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} -90 0`); await sleep(1500); A.stand();
  await run('loot replace entity TestRat hotbar.0 loot bm:items/partner_wheel'); await run('loot replace entity TestRat hotbar.1 loot bm:items/sky_mobile');
  await run('loot replace entity TestRat weapon.offhand loot bm:items/emma_ribbon'); await sleep(400);

  // ---- no one out yet
  A.bars.length = 0; await use(0); await sleep(600);               // (the ribbon goes on)
  ok('Emma\'s Ribbon in the off hand + use the wheel: it goes on', (await sc('TestRat', 'bm.pw0')) === 1);
  await sleep(2500); A.bars.length = 0; await use(0, true); await sleep(600);
  ok('sneak + use the wheel, no one out: "None of your partners are out"', A.bars.some(b => /None of your partners/.test(b)), A.bars.slice(-1).join(''));

  // ---- Emma from the wheel's page, the Sky Buddies from their mobile
  await sleep(2500); const n0 = A.dialogN.length; await use(0); await wait(3000, async () => A.dialogN.length > n0);
  await A.press(/Call Emma/); await sleep(800);
  ok('Emma called from the wheel\'s page', await wait(5000, async () => (await cnt(EMMA)) === 1));
  await use(1);
  ok('the Sky Buddies called with their Sky Mobile', await wait(5000, async () => (await cnt(SKY)) === 1));
  await sleep(3000);

  // ---- the stage: both carried 9 blocks off
  await run(`${O}tp ${EMMA} ${X + 9.5} ${Y + 1} ${Z + 4.5}`); await run(`${O}tp ${SKY} ${X + 9.5} ${Y + 1} ${Z + 0.5}`); await sleep(400);
  ok('(staged: both 9 blocks off - short of the 12 at which a tamed host teleports to you by itself)', (await near(EMMA, 6)) === 0 && (await near(SKY, 6)) === 0,
     (await run(`${O}data get entity ${EMMA.slice(0, -1)},limit=1] Pos`)) + ' / ' + (await run(`${O}data get entity ${SKY.slice(0, -1)},limit=1] Pos`)) + ' / ' + await cnt(EMMA) + ' ' + await cnt(SKY));
  A.bars.length = 0; await use(0, true); await sleep(150);            // (checked at once: once beside you they're free to wander again)
  ok('sneak + use the wheel: Emma is back beside you', (await near(EMMA, 3)) === 1, await run(`${O}data get entity ${EMMA.slice(0, -1)},limit=1] Pos`));
  ok('...and the Sky Buddies', (await near(SKY, 3)) === 1, await run(`${O}data get entity ${SKY.slice(0, -1)},limit=1] Pos`));
  ok('...their model with them (not left behind)', await wait(2000, async () => (await cnt(`@e[type=minecraft:item_display,tag=bm.ybp,x=${X},y=${Y + 1},z=${Z},distance=..5]`)) > 0 &&
     (await cnt(`@e[type=minecraft:item_display,tag=bm.ybp,x=${X + 9},y=${Y + 1},z=${Z},distance=..3]`)) === 0));
  ok('..."your partners are back at your side"', A.bars.some(b => /partners are back at your side/.test(b)), A.bars.slice(-1).join(''));
  A.bars.length = 0; await sleep(2500); await use(0, true); await sleep(600);
  ok('again a moment later: the wheel is still turning (8 s)', A.bars.some(b => /still turning/.test(b)), A.bars.slice(-1).join(''));

  // ---- clean up
  await run(`${O}execute as ${EMMA} run function bm:p62/emma_go`); await run(`kill ${SKY}`);
  await run('scoreboard players set TestRat bm.pw0 0'); await run('tag TestRat remove bm.pw_emma'); await run('clear TestRat');
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

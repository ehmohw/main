// 2.94t: SHINY FOLLOWERS (shiny.py, phase221), as a regular (non-op) player - followers called with their own items:
//   Leo called, his next summon shiny (rcon: admin/shiny_next - the stage for a one-in-a-hundred roll): "✦ Shiny! ✦", "Leo is
//     trying something new today", his own line about it, "Shiny Rosegold" in his wardrobe for good, and he's wearing it now;
//   his wardrobe (sneak + use his crest -> Wardrobe) lists Shiny Rosegold, unlocked;
//   the Follower Gallery shows a gold star by his name;
//   called again (another shiny_next): he has it - no second shiny, nothing said;
//   Emma (her ribbon): the same - her Shiny Lilac Gown;
//   rolled a hundred times by chance alone (his roll, as his summon calls it, for a follower not yet shiny): it comes about once.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const sc = async (o) => +(((await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const X = 17940, Y = 100, Z = 16120;
  const LEO = '@e[type=minecraft:wolf,tag=bm.leopet]', EMMA = '@e[type=minecraft:cat,tag=bm.emmapet]';
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  const home = async () => { await run(`${O}execute as ${LEO} run function bm:p96/go`); await run(`${O}execute as ${EMMA} run function bm:p62/emma_go`);
    for (const t of ['wolf', 'cat']) await run(`${O}execute as @e[type=minecraft:${t}] if score @s bm.pid = TestRat bm.pid run tp @s ~ -300 ~`); await sleep(2500);
    await run('scoreboard players set TestRat bm.lecd 0'); await run('scoreboard players set TestRat bm.emcd 0'); };
  await home();
  // (the stage: Leo and Emma met, neither's shiny look had; their own looks on)
  await run('scoreboard players set TestRat bm.wuleo 0'); await run('scoreboard players set TestRat bm.cosl 0');
  await run('scoreboard players set TestRat bm.wud 0'); await run('scoreboard players set TestRat bm.cosd 0'); await run('scoreboard players reset TestRat bm.shnext');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1000); A.stand();
  await run('loot replace entity TestRat hotbar.0 loot bm:items/leo_crest'); await run('loot replace entity TestRat hotbar.1 loot bm:items/emma_ribbon');
  await run('loot replace entity TestRat hotbar.2 loot bm:items/partner_wheel'); await run('scoreboard players set TestRat bm.pw0 1'); await sleep(800);

  // ---- Leo, his next summon shiny
  await run('execute as TestRat run function bm:admin/shiny_next'); A.chats.length = 0; A.titles && (A.titles.length = 0);
  await use(0); await wait(5000, async () => (await cnt(LEO)) === 1); await sleep(1200);
  const t = JSON.stringify(A.titles || []) + A.chats.join(' | ') + ' || shnext ' + (await run('scoreboard players get TestRat bm.shnext')) + ' leos ' + (await cnt(LEO)) + ' bars ' + A.bars.slice(-3).join(' / ');
  ok('Leo called, his summon shiny: "✦ Shiny! ✦" - "Leo is trying something new today"', /Shiny!/.test(t) && /Leo is trying something new today/.test(t), t.slice(0, 300));
  ok('...his own line about it in chat', A.chats.some(c => /Leo: .*trying something new today/.test(c)), A.chats.slice(-3).join(' | ').slice(0, 300));
  ok('..."Shiny Rosegold" in his wardrobe for good, and he\'s wearing it now', (((await sc('bm.wuleo')) >> 7) & 1) === 1 && (await sc('bm.cosl')) === 7 &&
     A.chats.some(c => /Shiny Rosegold/.test(c)), `wu ${await sc('bm.wuleo')} cos ${await sc('bm.cosl')}`);
  const lep = await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.lep,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] item.components`);
  ok('...his model wearing it (the look\'s pick, 7, on his parts)', /"c7"|_c7/.test(lep), lep.slice(0, 200));
  // ---- his wardrobe lists it
  await sleep(2600); let n0 = A.dialogN.length; await use(0, true); await wait(3000, async () => A.dialogN.length > n0);
  n0 = A.dialogN.length; await A.press(/Wardrobe/); await wait(3000, async () => A.dialogN.length > n0);
  const wd = JSON.stringify(A.dialogN[A.dialogN.length - 1] || '');
  ok('his wardrobe lists Shiny Rosegold', /Shiny Rosegold/.test(wd), wd.slice(0, 300));
  A.cmd('trigger bm.act set 2'); await sleep(400);
  // ---- the Gallery: a gold star by his name
  await sleep(2600); n0 = A.dialogN.length; await use(2); await wait(3000, async () => A.dialogN.length > n0);
  await A.press(/Gallery/); await sleep(600);
  const g = JSON.stringify(A.dialogN[A.dialogN.length - 1] || '');
  const i6 = g.indexOf('#06 Leo'), i7 = g.indexOf('#07 '), st = g.indexOf('\u2726', i6);
  ok('the Follower Gallery: a gold star after #06 Leo (before #07)', i6 > 0 && st > i6 && st < i7, `${i6} ${st} ${i7}`);
  A.cmd('trigger bm.act set 2'); await sleep(400);
  // ---- called again: he has it - no second shiny
  await home(); await run('execute as TestRat run function bm:admin/shiny_next'); A.chats.length = 0; A.titles && (A.titles.length = 0);
  await use(0); await wait(5000, async () => (await cnt(LEO)) === 1); await sleep(1200);
  ok('called again with it had: no second shiny, nothing said', !/Shiny!/.test(JSON.stringify(A.titles || [])) && !A.chats.some(c => /trying something new/.test(c)));
  // ---- Emma
  await home(); A.chats.length = 0; A.titles && (A.titles.length = 0);
  await use(1); await wait(5000, async () => (await cnt(EMMA)) === 1); await sleep(1200);   // (the shiny_next still waiting: Leo had it already)
  ok('Emma called next: her Shiny Lilac Gown - trying something new today', A.chats.some(c => /Emma: .*trying something new today/.test(c)) && (await sc('bm.cosd')) === 9 &&
     (((await sc('bm.wud')) >> 9) & 1) === 1, `${await sc('bm.cosd')} ${await sc('bm.wud')} | ${A.chats.slice(-3).join(' | ').slice(0, 200)}`);
  // ---- by chance alone: one in a hundred (Celi's roll, as her summon calls it - 600 rolls, not had)
  let hits = 0;
  for (let i = 0; i < 600; i++) { await run('scoreboard players set TestRat bm.wuc 0'); await run('execute as TestRat at @s run function bm:p221/roll/celi');
    if ((((await sc('bm.wuc')) >> 8) & 1) === 1) hits++; }
  ok('by chance alone: about one summon in a hundred (600 rolls: 1-16)', hits >= 1 && hits <= 16, `${hits}`);
  await run('scoreboard players set TestRat bm.wuc 0'); await run('scoreboard players set TestRat bm.cosc 0');

  // ---- clean up
  await home(); await run('scoreboard players set TestRat bm.cosl 0'); await run('scoreboard players set TestRat bm.cosd 0');
  await run('scoreboard players set TestRat bm.wuleo 0'); await run('scoreboard players set TestRat bm.wud 0'); await run('scoreboard players set TestRat bm.pw0 0'); await run('clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

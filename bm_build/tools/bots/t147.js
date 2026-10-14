// 2.78: Wilfrey counts toward the three-follower limit - as a regular (non-op) player, every follower called with its own
// item: with Cecil, Emma and Celi out, the locket is refused ("3 followers with you") and no Wilfrey comes; one sent home,
// the locket calls him; with Wilfrey out, a fourth follower is refused in turn. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const hold = async (slot, ms = 1500) => { A.slot(slot); await sleep(250); A.use(); await sleep(ms); A.release(); await sleep(300); };
  const PETS = { cecil: ['wolf', 'bm.cecilpet', 'cecil_gem'], emma: ['cat', 'bm.emmapet', 'emma_ribbon'], celi: ['wolf', 'bm.celipet', 'celi_charm'],
                 leo: ['wolf', 'bm.leopet', 'leo_crest'] };
  const sel = k => `@e[type=minecraft:${PETS[k][0]},tag=${PETS[k][1]}]`;
  const WIL = '@e[type=minecraft:wolf,tag=bm.wilfrey]';
  const X = 16480, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 6} ${Z + 10} minecraft:air`);
  for (const k in PETS) await run(`${O}kill @e[tag=${PETS[k][1]}]`); await run(`${O}kill ${WIL}`); await sleep(1500);
  for (const o of ['bm.cpcd', 'bm.emcd', 'bm.cecd', 'bm.lecd', 'bm.wlcd']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  const keys = ['cecil', 'emma', 'celi', 'leo'];
  for (let i = 0; i < keys.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${PETS[keys[i]][2]}`);
  await run('loot replace entity TestRat hotbar.5 loot bm:items/wilfrey_locket');
  for (let i = 0; i < 3; i++) { await use(i); await wait(4000, async () => (await cnt(sel(keys[i]))) === 1); await sleep(2300); }
  ok('Cecil, Emma and Celi called with their own items', (await cnt(sel('cecil'))) === 1 && (await cnt(sel('emma'))) === 1 && (await cnt(sel('celi'))) === 1);
  A.bars.length = 0; await hold(5); await sleep(1500);
  ok('the locket with three out: Wilfrey doesn\'t come', (await cnt(WIL)) === 0);
  ok('..."You already have 3 followers with you"', A.bars.some(b => /3 followers/.test(b)), A.bars.slice(-1).join(''));
  const n0 = A.dialogN.length; await use(2, true); await wait(3000, async () => A.dialogN.length > n0);
  await A.press(/send .*home/i); await wait(4000, async () => (await cnt(sel('celi'))) === 0); await sleep(2300);
  ok('Celi sent home (sneak + use her charm: her menu, "Send home")', (await cnt(sel('celi'))) === 0);
  await hold(5); await sleep(1500);
  ok('...now the locket calls Wilfrey', await wait(3000, async () => (await cnt(WIL)) === 1));
  A.bars.length = 0; await use(3); await sleep(2500);
  ok('with Wilfrey out, a fourth follower (Leo) is refused', (await cnt(sel('leo'))) === 0 && A.bars.some(b => /3 followers/.test(b)), A.bars.slice(-1).join(''));
  for (const k in PETS) await run(`${O}kill @e[tag=${PETS[k][1]}]`); await run(`${O}kill ${WIL}`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();

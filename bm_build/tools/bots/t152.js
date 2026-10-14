// 2.78: followers can be called in the Serpent's Den - no conquest asked. As a regular (non-op) player who has never beaten the
// Hollow King (conquest 0, best 0), in the den (rcon sets the stage: put there as the seal would), Cecil, Emma and Leo each called
// with their own item: all three come, and are still there ten seconds on.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = 'execute in bm:hollow_throne run ';
  const cnt = async (sel) => { const m = (await run(`${H}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const use = async (slot) => { A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(400); };
  const PETS = [['Cecil', 'cecil_gem', '@e[type=minecraft:wolf,tag=bm.cecilpet]'], ['Emma', 'emma_ribbon', '@e[type=minecraft:cat,tag=bm.emmapet]'],
                ['Leo', 'leo_crest', '@e[type=minecraft:wolf,tag=bm.leopet]']];
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  for (const t of ['bm.cecilpet', 'bm.emmapet', 'bm.leopet', 'bm.appet', 'bm.tupet']) { await run(`${H}kill @e[tag=${t}]`); await run(`execute in minecraft:overworld run kill @e[tag=${t}]`); }
  for (const o of ['bm.cpcd', 'bm.emcd', 'bm.lecd']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('scoreboard players set TestRat bm.conq 0'); await run('scoreboard players set TestRat bm.conqb 0');
  await run('execute as TestRat run function bm:admin/apophiss_den'); await run('scoreboard players set #apwake bm.p2 0'); await sleep(1500); A.stand();
  await run(`${H}tp TestRat 1076.5 3 1080.5 180 0`); await sleep(1000); A.stand();
  ok('(in the Serpent\'s Den, never having beaten the Hollow King)', /hollow_throne/.test(await run('data get entity TestRat Dimension')));
  for (let i = 0; i < PETS.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${PETS[i][1]}`);
  for (let i = 0; i < PETS.length; i++) {
    const [nm, , sel] = PETS[i];
    A.bars.length = 0; await use(i);
    ok(`${nm} called with their own item: comes`, await wait(5000, async () => (await cnt(sel)) === 1), A.bars.slice(-1).join(''));
    await sleep(2200);
  }
  await sleep(10000);
  ok('...all three still there ten seconds on', (await cnt(PETS[0][2])) === 1 && (await cnt(PETS[1][2])) === 1 && (await cnt(PETS[2][2])) === 1);
  for (const t of ['bm.cecilpet', 'bm.emmapet', 'bm.leopet']) await run(`${H}kill @e[tag=${t}]`);
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.conqb 6');
  await run('tag TestRat remove bm.apin'); await run('execute in minecraft:overworld run tp TestRat 13000.5 121 13000.5');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

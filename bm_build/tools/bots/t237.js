// 2.86: THE BONDS, as a regular (non-op) player - followers called with their own items (real uses): the Neighbor and the
// Chef side by side make "Dinner and a Show" (its hidden achievement, their intro, Speed for the player); Fishy joins them for
// "The Dinner Party" trio (its achievement, Luck); sent home, the trio is gone. Then Ashur and Leo, "The Sunfire Oath" (Fire
// Resistance and Strength). (rcon sets the stage: a floor, the items, no cooldowns.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const fx = async () => await run('data get entity TestRat active_effects');
  const adv = async (a) => (await cnt(`@a[name=TestRat,advancements={bm:story/${a}=true}]`)) === 1;
  const use = async (slot) => { A.slot(slot); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(2400); };
  const X = 16820, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.seen]'); await run('kill @e[type=minecraft:cat,tag=bm.seen]'); await sleep(2000);   // (every follower out anywhere counts toward the three; their faint lands a few ticks on)
  for (const o of ['bm.nbcd', 'bm.kkcd', 'bm.fycd', 'bm.ascd', 'bm.lecd']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const a of ['pair_show', 'trio_dinner', 'pair_sunfire']) await run(`advancement revoke TestRat only bm:story/${a}`);
  for (const t of ['bm.nbmet', 'bm.kkmet', 'bm.fymet', 'bm.asmet', 'bm.leomet']) await run(`tag TestRat add ${t}`);
  for (const [i, iid] of ['neighbor_baton', 'chef_ladle', 'fy_bowl'].entries()) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${iid}`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);

  // ---------------------------------------------------------------- a pair: the Neighbor and the Chef
  A.chats.length = 0; A.bars.length = 0;
  await use(0); await use(1);
  ok('the baton and the Ladle used: the Neighbor and the Chef both come', (await cnt('@e[type=minecraft:wolf,tag=bm.nbpet]')) === 1 && (await cnt('@e[type=minecraft:wolf,tag=bm.kkpet]')) === 1, A.bars.slice(-3).join(' | ') + ' || ' + A.chats.slice(-2).join(' | '));
  ok('...side by side: "Dinner and a Show" - its hidden achievement', await wait(5000, async () => adv('pair_show')));
  ok('...and their intro in chat', A.chats.some(c => /Dinner and a Show!/.test(c)) && A.chats.some(c => /soundtrack/.test(c)), A.chats.slice(-3).join(' | ').slice(0, 200));
  ok('...Speed for you', /minecraft:speed/.test(await fx()));
  // ---------------------------------------------------------------- the trio: Fishy joins
  await use(2);
  ok('Fishy\'s bowl used: Fishy comes too', await wait(3000, async () => (await cnt('@e[type=minecraft:wolf,tag=bm.fypet]')) === 1));
  ok('...all three: "The Dinner Party" - its hidden achievement', await wait(5000, async () => adv('trio_dinner')));
  ok('...Luck for you', await wait(3000, async () => /minecraft:luck/.test(await fx())));
  for (const iid of ['neighbor_baton', 'chef_ladle', 'fy_bowl']) await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}]`);   // (carried, they'd come straight back)
  await run('kill @e[type=minecraft:wolf,tag=bm.fypet]'); await run('kill @e[type=minecraft:wolf,tag=bm.kkpet]'); await run('kill @e[type=minecraft:wolf,tag=bm.nbpet]');
  await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await sleep(4500);
  for (const o of ['bm.nbcd', 'bm.kkcd', 'bm.fycd', 'bm.ascd', 'bm.lecd']) await run(`scoreboard players set TestRat ${o} 0`);
  ok('...all gone: no Luck any more', !/minecraft:luck/.test(await fx()));
  // ---------------------------------------------------------------- Ashur and Leo
  await run('loot replace entity TestRat hotbar.3 loot bm:items/ashur_cinder'); await run('loot replace entity TestRat hotbar.4 loot bm:items/leo_crest');
  await sleep(3000); A.bars.length = 0; await use(3); await use(4);
  ok('Ashur\'s Cinder and Leo\'s crest used: both come', (await cnt('@e[type=minecraft:wolf,tag=bm.aspet]')) === 1 && (await cnt('@e[type=minecraft:wolf,tag=bm.leopet]')) === 1, A.bars.slice(-3).join(' | '));
  ok('..."The Sunfire Oath": its achievement, Fire Resistance and Strength', await wait(5000, async () => adv('pair_sunfire')) &&
     await wait(3000, async () => { const e = await fx(); return /fire_resistance/.test(e) && /strength/.test(e); }), (await fx()).slice(0, 200));

  // ---------------------------------------------------------------- clean up
  await run('clear TestRat'); await run('effect clear TestRat');
  for (const t of ['bm.nbpet', 'bm.kkpet', 'bm.fypet', 'bm.aspet', 'bm.leopet']) await run(`kill @e[type=minecraft:wolf,tag=${t}]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

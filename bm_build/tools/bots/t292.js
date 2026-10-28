// 2.96: RUFUS GNAW's bonds, as a regular (non-op) player - followers called with their own items (real uses), Rufus with his
// Mercenary Contract (unpaid today, so his own Luck doesn't muddy it):
//   Rufus and Bender, "Rat Terrier" (its hidden achievement, their intro, Speed); Rufus and Mr. Capshun, "The Hired Pen" (Strength);
//   Rufus and Dennis, "Gold Diggers" (Haste); Rufus and Emma, "The Princess's Bodyguard" (Regeneration);
//   trios: Rufus, Leo and Tullius, "Soldiers of Fortune" (Strength); Rufus, Bender and Mr. Capshun, "Odd Jobs" (Jump Boost);
//   Rufus, Dennis and Pistachio, "The Heist Crew" (Night Vision).
// (rcon sets the stage: an empty field, the followers met, their rests cleared.)
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
  const X = 17860, Y = 100, Z = 16100;
  const HOSTS = ['wolf,tag=bm.rupet', 'wolf,tag=bm.bvpet', 'wolf,tag=bm.mzpet', 'wolf,tag=bm.dwpet', 'cat,tag=bm.emmapet', 'wolf,tag=bm.leopet', 'wolf,tag=bm.tupet', 'wolf,tag=bm.pipet'];
  const CDS = ['bm.rucd', 'bm.bvcd', 'bm.mzcd', 'bm.dwcd', 'bm.emcd', 'bm.lecd', 'bm.tucd', 'bm.picd'];
  const reset = async () => {
    await run('clear TestRat'); for (const t of HOSTS) await run(`kill @e[type=minecraft:${t}]`);
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await sleep(3500);
    for (const o of CDS) await run(`scoreboard players set TestRat ${o} 0`);
    await run('scoreboard players set TestRat bm.mpaid -1'); await run('scoreboard players operation TestRat bm.mday = #day bm.bm');
  };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('scoreboard players reset TestRat bm.fret');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  for (const a of ['pair_rf_bender', 'pair_rf_capshun', 'pair_rf_dennis', 'pair_rf_emma', 'trio_fortune', 'trio_odd_jobs', 'trio_heist_crew']) await run(`advancement revoke TestRat only bm:story/${a}`);
  for (const t of ['bm.rumet', 'bm.bvmet', 'bm.mzmet', 'bm.dwmet', 'bm.emmet', 'bm.leomet', 'bm.tumet', 'bm.pimet']) await run(`tag TestRat add ${t}`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await reset();

  const bond = async (name, adv_, items, hosts, effect) => {
    for (const [i, iid] of items.entries()) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${iid}`);
    await sleep(500); A.chats.length = 0; A.bars.length = 0;
    for (let i = 0; i < items.length; i++) await use(i);
    const here = [];
    for (const h of hosts) here.push(await cnt(`@e[type=minecraft:${h}]`));
    ok(`${items.join(' and ')} used: ${hosts.length === 2 ? 'both' : 'all three'} come`, here.every(n => n >= 1), here.join(',') + ' || ' + A.bars.slice(-2).join(' | ') + ' || ' + A.chats.slice(-2).join(' | '));
    ok(`...together: "${name}" - its hidden achievement`, await wait(6000, async () => adv(adv_)));
    if (adv_.startsWith('pair_')) ok('...and their intro in chat', A.chats.some(c => c.includes(name + '!')), A.chats.slice(-3).join(' | ').slice(0, 300));
    ok(`...${effect} for you`, await wait(4000, async () => new RegExp(`minecraft:${effect}`).test(await fx())), (await fx()).slice(0, 160));
  };
  await bond('Rat Terrier', 'pair_rf_bender', ['merc_contract', 'bv_ball'], ['wolf,tag=bm.rupet', 'wolf,tag=bm.bvpet'], 'speed');
  await reset();
  await bond('The Hired Pen', 'pair_rf_capshun', ['merc_contract', 'capshun_pencil'], ['wolf,tag=bm.rupet', 'wolf,tag=bm.mzpet'], 'strength');
  await reset();
  await bond('Gold Diggers', 'pair_rf_dennis', ['merc_contract', 'dw_horn'], ['wolf,tag=bm.rupet', 'wolf,tag=bm.dwpet'], 'haste');
  await reset();
  await bond('The Princess\'s Bodyguard', 'pair_rf_emma', ['merc_contract', 'emma_ribbon'], ['wolf,tag=bm.rupet', 'cat,tag=bm.emmapet'], 'regeneration');
  await reset();
  await bond('Soldiers of Fortune', 'trio_fortune', ['merc_contract', 'leo_crest', 'tul_coin'], ['wolf,tag=bm.rupet', 'wolf,tag=bm.leopet', 'wolf,tag=bm.tupet'], 'strength');
  await reset();
  await bond('Odd Jobs', 'trio_odd_jobs', ['merc_contract', 'bv_ball', 'capshun_pencil'], ['wolf,tag=bm.rupet', 'wolf,tag=bm.bvpet', 'wolf,tag=bm.mzpet'], 'jump_boost');
  await reset();
  await bond('The Heist Crew', 'trio_heist_crew', ['merc_contract', 'dw_horn', 'pi_cloche'], ['wolf,tag=bm.rupet', 'wolf,tag=bm.dwpet', 'wolf,tag=bm.pipet'], 'night_vision');
  await reset();
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

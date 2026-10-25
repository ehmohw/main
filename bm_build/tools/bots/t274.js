// 2.94r: MORE BONDS (phase219), as a regular (non-op) player - followers called with their own items (real uses):
//   Bender and Queen Pearl, "Spoiled Rotten" (its hidden achievement, their intro, Luck) - and every 30 s her cake (a bite to eat);
//   Mr. Capshun and Leo, "The Hero's Journey" (Strength); Tullius and Bones, "Shark and Sailor" (Conduit Power);
//   Pearlman, Dennis and Pistachio, "The Market Guild" trio (its achievement, Hero of the Village) - and every minute your cut, an emerald.
// (rcon sets the stage: an empty field, the followers met, their rests cleared; the extras' counters wound on.)
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
  const X = 17860, Y = 100, Z = 16040;
  const HOSTS = ['wolf,tag=bm.bvpet', 'wolf,tag=bm.pqpet', 'wolf,tag=bm.mzpet', 'wolf,tag=bm.leopet', 'wolf,tag=bm.tupet', 'wolf,tag=bm.bjpet',
                 'cat,tag=bm.pmpet', 'wolf,tag=bm.dwpet', 'wolf,tag=bm.pipet'];
  const CDS = ['bm.bvcd', 'bm.pqcd', 'bm.mzcd', 'bm.lecd', 'bm.tucd', 'bm.bjcd', 'bm.pmcd', 'bm.dwcd', 'bm.picd'];
  const reset = async () => {
    await run('clear TestRat'); for (const t of HOSTS) await run(`kill @e[type=minecraft:${t}]`);
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await sleep(3500);
    for (const o of CDS) await run(`scoreboard players set TestRat ${o} 0`);
  };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('scoreboard players reset TestRat bm.fret');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  for (const a of ['pair_spoiled', 'pair_journey', 'pair_sharksailor', 'trio_guild']) await run(`advancement revoke TestRat only bm:story/${a}`);
  for (const t of ['bm.bvmet', 'bm.pqmet', 'bm.mzmet', 'bm.leomet', 'bm.bjmet', 'bm.tumet', 'bm.pmmet', 'bm.dwmet', 'bm.pimet']) await run(`tag TestRat add ${t}`);
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
  await bond('Spoiled Rotten', 'pair_spoiled', ['bv_ball', 'pq_pearls'], ['wolf,tag=bm.bvpet', 'wolf,tag=bm.pqpet'], 'luck');
  A.bars.length = 0; await run('effect clear TestRat minecraft:saturation');
  await run('execute as @e[type=minecraft:wolf,tag=bm.bvpet] run scoreboard players set @s bm.p8spoiled 29');
  ok('...every 30 seconds Queen Pearl\'s cake: a bite to eat, and she says so', await wait(4000, async () => A.bars.some(b => /Cake for you/.test(b))) && /saturation|speed/.test(await fx()),
     A.bars.slice(-1).join('') + ' | ' + (await fx()).slice(0, 120));
  await reset();
  await bond('The Hero\'s Journey', 'pair_journey', ['capshun_pencil', 'leo_crest'], ['wolf,tag=bm.mzpet', 'wolf,tag=bm.leopet'], 'strength');
  await reset();
  await bond('Shark and Sailor', 'pair_sharksailor', ['tul_coin', 'bn_whistle'], ['wolf,tag=bm.tupet', 'wolf,tag=bm.bjpet'], 'conduit_power');
  await reset();
  await bond('The Market Guild', 'trio_guild', ['pearl_card', 'dw_horn', 'pi_cloche'], ['cat,tag=bm.pmpet', 'wolf,tag=bm.dwpet', 'wolf,tag=bm.pipet'], 'hero_of_the_village');
  await run('scoreboard players set TestRat bm.p219 59');
  ok('...every minute your cut: an emerald', await wait(4000, async () => /minecraft:emerald/.test(await run('data get entity TestRat Inventory'))));
  await reset();
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

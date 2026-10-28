// 2.98: THE GEM AND THE GUTTER GENTRY's bonds, as a regular (non-op) player - followers called with their own items (real uses):
//   the Gutter Gentry, Reformed (Batty, Eggbert and the Count: its hidden achievement, Strength, Speed and Luck);
//   Batty and Bender, "Fetch!" (Jump Boost); the Count and Mr. Capshun, "The Villain's Redemption" (Strength);
//   the Creative Forms - Kettle, "First Sketch" (Jump Boost); Batty, "Prism Wings" (Slow Falling); Emma, "Dream Petals"
//   (Regeneration) - and (2.96a) Kettle in his creative look (every part in the rainbow; his own colours once the Gem is gone); Bender, "Fetch the Rainbow" (Speed); and Henry and the Gem, "Shiny Thing" (Luck).
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
  const X = 17800, Y = 100, Z = 17600;
  const HOSTS = ['wolf,tag=bm.cgpet', 'wolf,tag=bm.ytpet', 'wolf,tag=bm.ebpet', 'wolf,tag=bm.knpet', 'wolf,tag=bm.bvpet', 'wolf,tag=bm.mzpet', 'wolf,tag=bm.ktpet', 'cat,tag=bm.emmapet', 'wolf,tag=bm.hypet'];
  const CDS = ['bm.cgcd', 'bm.ytcd', 'bm.ebcd', 'bm.kncd', 'bm.bvcd', 'bm.mzcd', 'bm.ktcd', 'bm.emcd', 'bm.hycd'];
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
  for (const a of ['trio_gentry', 'pair_gb_bender', 'pair_ct_capshun', 'pair_cf_kettle', 'pair_cf_batty', 'pair_cf_emma', 'pair_cf_bender', 'pair_hy_gem']) await run(`advancement revoke TestRat only bm:story/${a}`);
  for (const t of ['bm.cgmet', 'bm.ytmet', 'bm.ebmet', 'bm.knmet', 'bm.bvmet', 'bm.mzmet', 'bm.ktmet', 'bm.emmet', 'bm.hymet']) await run(`tag TestRat add ${t}`);
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
  await bond('The Gutter Gentry, Reformed', 'trio_gentry', ['gentry_batty', 'gentry_eggbert', 'gentry_count'], ['wolf,tag=bm.ytpet', 'wolf,tag=bm.ebpet', 'wolf,tag=bm.knpet'], 'luck');
  await reset();
  await bond('Fetch!', 'pair_gb_bender', ['gentry_batty', 'bv_ball'], ['wolf,tag=bm.ytpet', 'wolf,tag=bm.bvpet'], 'jump_boost');
  await reset();
  await bond("The Villain's Redemption", 'pair_ct_capshun', ['gentry_count', 'capshun_pencil'], ['wolf,tag=bm.knpet', 'wolf,tag=bm.mzpet'], 'strength');
  await reset();
  await bond('Creative Form: First Sketch', 'pair_cf_kettle', ['creativity_gem', 'kettle_plane'], ['wolf,tag=bm.cgpet', 'wolf,tag=bm.ktpet'], 'jump_boost');
  // (2.96a) the form is a look: every part of Kettle washed in the rainbow while he's beside the Gem - and his own again once they part
  const painted = async () => { const m = (await run(`${O}execute as @e[type=minecraft:wolf,tag=bm.ktpet,limit=1] at @s if entity @e[type=minecraft:item_display,distance=..3.5,tag=bm.cft]`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  ok('...Kettle in his creative form: his parts painted in the rainbow', await wait(4000, async () => (await painted()) >= 3), `parts ${await painted()}`);
  await run(`${O}tp @e[type=minecraft:wolf,tag=bm.cgpet] ${X} ${Y - 40} ${Z}`); await run(`${O}kill @e[type=minecraft:wolf,tag=bm.cgpet]`);    // (the Gem gone)
  ok('...the Gem gone: Kettle his own colours again', await wait(9000, async () => (await painted()) === 0), `parts ${await painted()}`);
  await reset();
  await bond('Creative Form: Prism Wings', 'pair_cf_batty', ['creativity_gem', 'gentry_batty'], ['wolf,tag=bm.cgpet', 'wolf,tag=bm.ytpet'], 'slow_falling');
  await reset();
  await bond('Creative Form: Dream Petals', 'pair_cf_emma', ['creativity_gem', 'emma_ribbon'], ['wolf,tag=bm.cgpet', 'cat,tag=bm.emmapet'], 'regeneration');
  await reset();
  await bond('Fetch the Rainbow', 'pair_cf_bender', ['creativity_gem', 'bv_ball'], ['wolf,tag=bm.cgpet', 'wolf,tag=bm.bvpet'], 'speed');
  await reset();
  await bond('Shiny Thing', 'pair_hy_gem', ['henry_tag', 'creativity_gem'], ['wolf,tag=bm.hypet', 'wolf,tag=bm.cgpet'], 'luck');
  await reset();
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

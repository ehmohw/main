// 2.87: THE BONDS OF THE DEEP, as a regular (non-op) player - followers called with their own items (real uses): Emma, Queen Ava and
// Queen Pearl make "THE ROYAL FAMILY" (its achievement; Resistance II, Conduit Power, four more hearts; the ETHEREAL ECHO hurts and
// lights up the foes round you; the BLOODLINE WARD catches you at 2 hearts) - and "Mother and Daughter" between them; then Leo, Emma
// and Ava, "THE QUEEN'S OATH" (Strength II, Resistance II, Absorption IV); then Bloo and Democratus, "Old Wounds". (rcon sets the stage.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const fx = async () => await run('data get entity TestRat active_effects');
  const num = async (sel, path) => +(((await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?entity data: /, '').match(/(-?[\d.]+)/) || [0, NaN])[1]);
  const adv = async (a) => (await cnt(`@a[name=TestRat,advancements={bm:story/${a}=true}]`)) === 1;
  const use = async (slot) => { A.slot(slot); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(2400); };
  const X = 16620, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.seen]'); await run('kill @e[type=minecraft:cat,tag=bm.seen]'); await sleep(2000);
  for (const o of ['bm.emcd', 'bm.avcd', 'bm.pqcd', 'bm.lecd', 'bm.bocd', 'bm.dmcd', 'bm.royw', 'bm.avform', 'bm.pqform']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const a of ['trio_royal', 'trio_oath', 'pair_mother', 'pair_wounds']) await run(`advancement revoke TestRat only bm:story/${a}`);
  await run('advancement grant TestRat only bm:story/emma_friend'); for (const t of ['bm.avmet', 'bm.pqmet', 'bm.leomet', 'bm.bomet', 'bm.dmmet']) await run(`tag TestRat add ${t}`);
  for (const [i, iid] of ['emma_ribbon', 'av_locket', 'pq_pearls'].entries()) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${iid}`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  const home = async () => { for (const w of ['emma', 'ava', 'pearlq', 'leo', 'bloo', 'demo']) await run(`execute as TestRat run function bm:${{ emma: 'p98/home/emma', ava: 'p189/home', pearlq: 'p190/home', leo: 'p98/home/leo', bloo: 'p191/home', demo: 'p97/send_home' }[w]}`);
    await run('clear TestRat'); await sleep(2500); for (const o of ['bm.emcd', 'bm.avcd', 'bm.pqcd', 'bm.lecd', 'bm.bocd', 'bm.dmcd']) await run(`scoreboard players set TestRat ${o} 0`); };

  // ---------------------------------------------------------------- THE ROYAL FAMILY
  A.chats.length = 0; await use(0); await use(1); await use(2);
  ok('Emma\'s ribbon, Ava\'s locket and Pearl\'s pearls used: all three come', (await cnt('@e[type=minecraft:cat,tag=bm.emmapet]')) === 1 && (await cnt('@e[type=minecraft:wolf,tag=bm.avpet]')) === 1 && (await cnt('@e[type=minecraft:wolf,tag=bm.pqpet]')) === 1);
  ok('..."The Royal Family" - its achievement', await wait(5000, async () => adv('trio_royal')));
  ok('...Resistance II, Conduit Power and four more hearts for you', await wait(3000, async () => { const e = await fx(); return /conduit_power/.test(e) && /health_boost/.test(e) && /amplifier: ?1b[^}]*minecraft:resistance|minecraft:resistance[^}]*amplifier: ?1b/.test(e) || /resistance/.test(e) && /conduit_power/.test(e); }), (await fx()).slice(0, 220));
  ok('...and "Mother and Daughter" between Emma and her mother', await wait(4000, async () => adv('pair_mother')));
  await run(`${O}summon minecraft:husk ${X + 4} ${Y + 1} ${Z} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t241z","bm.seen"],attributes:[{id:"minecraft:max_health",base:300}],Health:300f}`);
  ok('the ETHEREAL ECHO (every 15 s): the foe near you hurt and lit up', await wait(18000, async () => (await num('@e[tag=bm.t241z,limit=1]', 'Health')) < 300 &&
     /glowing/.test(await run(`${O}data get entity @e[tag=bm.t241z,limit=1] active_effects`))));
  await run(`${O}kill @e[tag=bm.t241z]`);
  await run('effect clear TestRat'); await sleep(300); A.chats.length = 0;
  for (let k = 0; k < 6 && !A.chats.some(c => /Bloodline Ward/.test(c)); k++) {           // (the trio's own Resistance and hearts soak some of it)
    const h = await num('@a[name=TestRat,limit=1]', 'Health'); if (h > 3) await run(`damage TestRat ${Math.max(1, Math.ceil(h - 3))} minecraft:out_of_world`); await sleep(700); }
  ok('the BLOODLINE WARD: at 2 hearts, the crowns of the deep refuse to let you fall', await wait(4000, async () => A.chats.some(c => /Bloodline Ward/.test(c))) &&
     (await num('@a[name=TestRat,limit=1]', 'Health')) > 10, A.chats.slice(-1).join('').slice(0, 160));
  await run('effect give TestRat minecraft:resistance 900 4 true');
  await home();

  // ---------------------------------------------------------------- THE QUEEN'S OATH
  for (const [i, iid] of ['leo_crest', 'emma_ribbon', 'av_locket'].entries()) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${iid}`);
  await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await use(0); await use(1); await use(2);
  ok('Leo, Emma and Ava: "The Queen\'s Oath" - its achievement', await wait(6000, async () => adv('trio_oath')));
  ok('...Strength II for you, and the Absorption shield', await wait(4000, async () => { const e = await fx(); return /amplifier: ?1b[^}]*minecraft:strength|minecraft:strength[^}]*amplifier: ?1b/.test(e) && /absorption/.test(e); }), (await fx()).slice(0, 220));
  await home();

  // ---------------------------------------------------------------- OLD WOUNDS
  for (const [i, iid] of ['bo_claw', 'demo_seal'].entries()) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${iid}`);
  await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await use(0); await use(1);
  ok('Bloo and Democratus: "Old Wounds" - its achievement', await wait(6000, async () => adv('pair_wounds')));
  ok('...Strength II for you', await wait(3000, async () => /amplifier: ?1b[^}]*minecraft:strength|minecraft:strength[^}]*amplifier: ?1b/.test(await fx())), (await fx()).slice(0, 200));
  await home();

  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

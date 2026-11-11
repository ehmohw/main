// 3.1r: HEARTH AND EMBER, AND THE HEARTH GUARD - a pair and a trio that share a name ('hearth'), each with its own synergy attack
// (phase208: the trio's charge used to take the pair's - the pair's blow said "Trio Synergy! The Hearth Guard"). As a regular
// (non-op) player, followers called with their own items: the Arachno-Lantern and Ashur make "Hearth and Ember" and, charged in a
// fight, set off THEIR synergy ("Synergy! Hearth and Ember"); the Lantern home, Emma and Leo called: "The Hearth Guard" trio,
// its own ("Trio Synergy! The Hearth Guard - Shield Wall"). (rcon sets the stage: a floor, the items, the charge wound forward.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const adv = async (a) => (await cnt(`@a[name=TestRat,advancements={bm:story/${a}=true}]`)) === 1;
  const use = async (slot) => { A.slot(slot); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(2400); };
  const X = 17000, Y = 100, Z = 16300;
  const zom = async (dx, dz, tag, hp = 600) => run(`${O}summon minecraft:zombie ${X + dx} ${Y + 1} ${Z + dz} {Tags:["${tag}","bm.t405z","bm.seen"],PersistenceRequired:1b,Silent:1b,NoAI:1b,` +
                                          `attributes:[{id:"minecraft:max_health",base:${hp}d}],Health:${hp}f}`);
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} minecraft:sandstone`); await run(`${O}fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.seen]'); await run('kill @e[type=minecraft:cat,tag=bm.seen]'); await sleep(2000);
  for (const o of ['bm.lncd', 'bm.ascd', 'bm.emcd', 'bm.lecd']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const a of ['pair_hearth', 'trio_hearth']) await run(`advancement revoke TestRat only bm:story/${a}`);
  for (const t of ['bm.lnmet', 'bm.asmet', 'bm.leomet']) await run(`tag TestRat add ${t}`);
  for (const [i, iid] of ['ln_gourd', 'ashur_cinder', 'emma_ribbon', 'leo_crest'].entries()) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${iid}`);
  await run('scoreboard players set TestRat bm.syn2 0'); await run('scoreboard players set TestRat bm.syn3 0');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);

  // ---------------------------------------------------------------- the pair: the Lantern and Ashur
  A.chats.length = 0; A.bars.length = 0;
  await use(0); await use(1);
  ok('the Lantern\'s gourd and Ashur\'s cinder used: both come', await wait(4000, async () => (await cnt('@e[tag=bm.lnpet]')) >= 1 && (await cnt('@e[tag=bm.aspet]')) >= 1),
     `${await cnt('@e[tag=bm.lnpet]')} ${await cnt('@e[tag=bm.aspet]')} | ${A.bars.slice(-2).join(' | ')}`);
  ok('...side by side: "Hearth and Ember" - its hidden achievement', await wait(6000, async () => adv('pair_hearth')), A.chats.slice(-2).join(' | ').slice(0, 160));
  await run('scoreboard players set TestRat bm.syn2 19'); A.bars.length = 0;
  await zom(4, 4, 'bm.t405a');
  ok('a monster near, the pair charged: "Synergy! Hearth and Ember" - the pair\'s own, not the trio\'s', await wait(6000, async () => A.bars.some(b => /Synergy!.*Hearth and Ember/.test(b))) &&
     !A.bars.some(b => /Trio Synergy!|Hearth Guard/.test(b)), A.bars.slice(-2).join(' | '));
  await run(`${O}kill @e[tag=bm.t405z]`);

  // ---------------------------------------------------------------- the trio: Ashur, Emma and Leo
  await run('execute as TestRat run scoreboard players operation #me bm.pid = @s bm.pid');
  await run('execute as TestRat run function bm:p98/home/lantern');
  await wait(6000, async () => (await cnt('@e[tag=bm.lnpet]')) === 0);
  await use(2); await use(3);
  ok('the Lantern home; Emma and Leo called', (await cnt('@e[tag=bm.lnpet]')) === 0 && await wait(4000, async () => (await cnt('@e[tag=bm.emmapet]')) >= 1 && (await cnt('@e[tag=bm.leopet]')) >= 1));
  ok('...all three: "The Hearth Guard" - its hidden achievement', await wait(6000, async () => adv('trio_hearth')));
  await run('scoreboard players set TestRat bm.syn3 34'); A.bars.length = 0;
  await zom(-4, 4, 'bm.t405b', 1000);
  ok('...a monster near, the trio charged: "Trio Synergy! The Hearth Guard"', await wait(6000, async () => A.bars.some(b => /Trio Synergy!.*The Hearth Guard/.test(b))), A.bars.slice(-2).join(' | '));
  await run(`${O}kill @e[tag=bm.t405z]`);
  for (const w of ['ashur', 'emma', 'leo']) await run(`execute as TestRat run function bm:p98/home/${w}`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  A.end(); R.end();
  console.log(`${res.filter(x => x).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

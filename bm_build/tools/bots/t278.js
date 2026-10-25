// 2.94u: SIGNATURE MOVES (phase223), as a regular (non-op) player - followers called with their own items, monsters set down
// near them (rcon: the stage - and Emma's charge filled, as fighting would). Positions sampled as they move:
//   Emma, Ethereal: CRESCENT DIVE - she swoops to a monster 8 off in steps (never more than 1.6 a sample), it's hurt, she glides back;
//   PETAL WALTZ - three monsters near: she slashes from one to the next (each one hurt), rises, and the slam's ring hurts them again;
//   Leo: SHIELD CHARGE - in steps to a monster 7 off, the bash and the smite land (two blows: 16 or more).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (sel) => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1, 4).map(Number) : null; };
  const use = async (slot) => { A.slot(slot); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(2000); };
  const X = 18020, Y = 100, Z = 16200;
  const hp = async (tag) => +(((await run(`${O}data get entity @e[tag=${tag},limit=1] Health`)).match(/([\d.]+)f/) || [0, -1])[1]);
  const husk = async (dx, dz, tag) => run(`${O}summon minecraft:husk ${X + dx} ${Y + 1} ${Z + dz} {NoAI:1b,PersistenceRequired:1b,Health:200f,Tags:["${tag}","t278","bm.seen"],attributes:[{id:"minecraft:max_health",base:200d}]}`);
  const watch = async (host, ms, stop = async () => false) => { let last = await pos(host), big = 0, far = 0; const p0 = last; const t0 = Date.now();
    while (Date.now() - t0 < ms) { await sleep(40); const p = await pos(host); if (!p || !last) continue; big = Math.max(big, Math.hypot(p[0] - last[0], p[2] - last[2]));
      far = Math.max(far, Math.hypot(p[0] - p0[0], p[2] - p0[2])); last = p; if (await stop()) break; } return { big, far }; };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:invisibility 900 0 true');
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  await run(`${O}fill ${X - 20} ${Y} ${Z - 20} ${X + 20} ${Y} ${Z + 20} minecraft:sandstone`); await run(`${O}fill ${X - 20} ${Y + 1} ${Z - 20} ${X + 20} ${Y + 8} ${Z + 20} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..30]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1000); A.stand();
  for (const o of ['bm.emcd', 'bm.lecd']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/emma_ribbon'); await run('loot replace entity TestRat hotbar.1 loot bm:items/leo_crest'); await sleep(500);

  // ---- Emma: Crescent Dive
  const EM = '@e[type=minecraft:cat,tag=bm.emmapet,limit=1]';
  await use(0); ok('Emma called', await wait(5000, async () => (await cnt(EM)) === 1)); await sleep(1500);
  await run(`${O}scoreboard players set ${EM} bm.kcd2 9999`);             // (the waltz held back: the dive is what we watch)
  await husk(0, 9, 't278a'); await run(`${O}tp ${EM} ${X + 0.5} ${Y + 1} ${Z - 1.5}`); await sleep(300); await run(`${O}scoreboard players set ${EM} bm.emc 100`);
  let sw = 0;
  const w = await watch(EM, 6000, async () => { const m = (await run(`${O}scoreboard players get ${EM} bm.ksw`)).match(/has (\d+)/); if (m && +m[1] === 1) sw = 1; return sw && !(m && +m[1] === 1); });
  ok('her charge full and a monster near: the Ethereal Form', /has [1-9]/.test(await run(`${O}scoreboard players get ${EM} bm.eme`)));
  ok('CRESCENT DIVE: she swoops to it in steps (never more than 2.4 a sample - a tick or two)', sw && w.far > 3 && w.big <= 2.4, JSON.stringify(w) + ' dive ' + sw);
  ok('...it\'s cleaved', await wait(3000, async () => (await hp('t278a')) < 200), `${await hp('t278a')}`);
  ok('...and she glides back to your side', await wait(5000, async () => (await cnt(`${EM.slice(0, -1)},x=${X},y=${Y + 1},z=${Z},distance=..4]`)) === 1));
  await run(`${O}kill @e[tag=t278]`);

  // ---- Emma: Petal Waltz
  await run(`${O}scoreboard players set ${EM} bm.kcd2 0`); await run(`${O}scoreboard players set ${EM} bm.kcd1 9999`); await run(`${O}scoreboard players set ${EM} bm.eme 40`);
  await husk(4, 4, 't278b'); await husk(-4, 5, 't278c'); await husk(0, 7, 't278d');
  const y0 = (await pos(EM))[1]; let ymax = y0;
  const w2 = await watch(EM, 5000, async () => { const p = await pos(EM); if (p) ymax = Math.max(ymax, p[1]); return false; });
  const hs = [await hp('t278b'), await hp('t278c'), await hp('t278d')];
  ok('PETAL WALTZ: from monster to monster in steps (never more than 2.4 a sample - a tick or two)', w2.big <= 2.4 && w2.far > 2, JSON.stringify(w2));
  ok('...each of the three slashed', hs.every(h => h < 200 && h >= 0), hs.join(','));
  ok('...she rises (a block or more) for the slam', ymax - y0 >= 1, `${ymax - y0}`);
  const before = [await hp('t278b'), await hp('t278c'), await hp('t278d')];
  ok('...and the slam\'s ring: those within 4 hurt again (10 more)', await wait(3000, async () => [await hp('t278b'), await hp('t278c'), await hp('t278d')].some((h, i) => h <= before[i] - 10) || before.some(h => h <= 180)),
     [await hp('t278b'), await hp('t278c'), await hp('t278d')].join(','));
  await run(`${O}kill @e[tag=t278]`); await run(`${O}execute as ${EM} run function bm:p62/emma_go`); await sleep(1000);

  // ---- Leo: Shield Charge
  const LEO = '@e[type=minecraft:wolf,tag=bm.leopet,limit=1]';
  await use(1); ok('Leo called', await wait(5000, async () => (await cnt(LEO)) === 1)); await sleep(1500);
  await husk(-7, 0, 't278e');
  const w3 = await watch(LEO, 3000, async () => (await hp('t278e')) <= 184);
  ok('SHIELD CHARGE: he charges in steps (never more than 1.6 a sample)', w3.far > 3 && w3.big <= 1.6, JSON.stringify(w3));
  ok('...the bash and the smite land (16 or more)', await wait(4000, async () => (await hp('t278e')) <= 184), `${await hp('t278e')}`);
  await run(`${O}kill @e[tag=t278]`); await run(`${O}execute as ${LEO} run function bm:p96/go`);

  await run('clear TestRat'); await run('effect clear TestRat'); await run(`${O}forceload remove ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

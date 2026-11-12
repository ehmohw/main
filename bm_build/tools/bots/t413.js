// 3.1y: THE LEADER'S CHOICE GOES ROUND THE CREW - three regular (non-op) players, TestRat, TestRat2, TestRat3, in one party.
// (rcon sets the stage only: Tokens, the party's bookkeeping, a platform; the rooms and the vault won as their own finish would; the
// leader's 75-second clock run down - nobody answering.) TestRat plans a heist through the Ledger's buttons, the crew press "I'm in"
// if asked; won: the leader is asked. Nobody chooses: the choice passes to the next raider in turn - then to the third, never back
// and forth between two (3.1w: it went to whoever was first in the player list, so two away raiders passed it between them) - then
// round to the first again. The one asked presses "Back to the Overworld": everyone home.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const dim = async (n) => (await run(`data get entity ${n} Dimension`)).replace(/.*data: /, '');
  const tagged = async (n, t) => /passed/i.test(await run(`execute if entity @a[name=${n},tag=${t}]`));
  const O = 'execute in minecraft:overworld run ';
  const HX = 13100, HY = 121, HZ = 13020;
  const NAMES = ['TestRat', 'TestRat2', 'TestRat3'];
  const A = await bot('TestRat'); await sleep(1500); const B = await bot('TestRat2'); await sleep(1500); const C3 = await bot('TestRat3'); await sleep(2500);
  const C = { TestRat: A, TestRat2: B, TestRat3: C3 };
  for (const f of ['heist_hard_never', 'plan_anywhere']) await run(`function bm:admin/${f}`);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run(`${O}forceload add ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
  await run(`${O}fill ${HX - 5} ${HY - 1} ${HZ - 4} ${HX + 5} ${HY - 1} ${HZ + 4} minecraft:stone`);
  await run(`${O}fill ${HX - 5} ${HY} ${HZ - 4} ${HX + 5} ${HY + 3} ${HZ + 4} minecraft:air`);
  for (const [k, n] of NAMES.entries()) {
    await run(`${O}tp ${n} ${HX + 0.5 + 2 * k} ${HY} ${HZ + 0.5} 0 0`); await run(`gamemode survival ${n}`); await run(`clear ${n}`); await run(`effect clear ${n}`);
    for (const t of ['bm.gvp', 'bm.gvask', 'bm.gvnext', 'bm.gvoffer', 'bm.gvwaitd', 'bm.gvin', 'bm.gvskip']) await run(`tag ${n} remove ${t}`);
    await run(`execute as ${n} unless score @s bm.pid matches 1.. run function bm:p21/pid`);
    for (const o of ['bm.crew', 'bm.crewoff', 'bm.crewoff2', 'bm.crewoff3', 'bm.fcon', 'bm.fcon2', 'bm.gvhr']) await run(`scoreboard players set ${n} ${o} 0`);
  }
  await run(`loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger`); await run('scoreboard players set TestRat bm.gvu 5');   // (the Ledger first - then the Tokens, not over them)
  for (const n of NAMES) for (let i = 0; i < 4; i++) await run(`loot give ${n} loot bm:items/token`);
  // (a party of three - the party system's own bookkeeping)
  for (const n of NAMES) await run(`scoreboard players operation ${n} bm.pty = TestRat bm.pid`);
  await sleep(1500); for (const n of NAMES) C[n].stand(); A.slot(0);
  B.chats.length = 0; B.cmd('gamemode creative'); C3.chats.length = 0; C3.cmd('gamemode creative'); await sleep(600);
  ok('TestRat2 and TestRat3 are regular players', /unknown|incomplete/i.test(B.chats.join(' ')) && /unknown|incomplete/i.test(C3.chats.join(' ')));

  // ---- the heist, planned through the Ledger; the crew opt in if asked
  const lbls = X => X.buttons().map(b => b.label).join(' | ').slice(0, 300);
  const opened = await A.useWait(); console.log(`   (ledger opened ${opened}: ${lbls(A)})`);
  await A.press(/Plan a Heist/); await sleep(800); console.log(`   (after Plan a Heist: ${lbls(A)} | bar ${A.bars.slice(-1).join('')} | chat ${A.chats.slice(-2).join(' / ').slice(0, 200)})`);
  await A.press(/Tier I\b(?!I)/); await sleep(300); console.log(`   (after Tier I: ${lbls(A)})`);
  for (const X of [B, C3]) X.dialogN.length = 0;
  await A.press(/^3\b|3 tries/i);
  await sleep(4000);
  console.log(`   (after 3 tries - A: ${lbls(A)} | ${A.chats.slice(-3).join(' / ').slice(0, 300)})`);
  for (const [nm, X] of [['B', B], ['C', C3]]) console.log(`   (${nm} sees: ${lbls(X)} | ${X.chats.slice(-2).join(' / ').slice(0, 200)})`);
  for (const X of [B, C3]) if (X.buttons().some(b => /I'm in|Join|Count me in/i.test(b.label))) await X.press(/I'm in|Join|Count me in/i);
  const inV = await wait(60000, async () => { for (const n of NAMES) if (!(await tagged(n, 'bm.gvp')) || !/gutter/.test(await dim(n))) return false; return true; }, 500);
  if (!ok('all three led down into the vault', inV, (await Promise.all(NAMES.map(dim))).join(' '))) return done();
  await sleep(2500);
  const gi = await sc('TestRat', 'bm.gvi'), s = gi - 1;
  // (the stage: the job won - the vault's own payout)
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${gi}},limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi`);
  await run(`execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${gi}},limit=1] at @s run function bm:p70/payout`);
  ok('won: the leader (TestRat) is asked', await wait(10000, async () => tagged('TestRat', 'bm.gvask')));
  const asker = async () => { for (const n of NAMES) if (await tagged(n, 'bm.gvask')) return n; return null; };
  const runOut = async () => { const was = await asker(); await run(`scoreboard players set #dt${s} bm.gvdt 1`);
    await wait(10000, async () => { const now = await asker(); return now && now !== was; }, 300); await sleep(500); return asker(); };
  const first = await runOut();
  ok('nobody chooses: the choice passes on to another raider', first && first !== 'TestRat', `${first}`);
  ok('...TestRat is told "Time\'s up"', A.chats.some(c => /Time's up/.test(c)));
  const dump = async (w) => { const o = []; for (const n of NAMES) o.push(`${n}: pid ${await sc(n, 'bm.pid')} gvnx ${await sc(n, 'bm.gvnx')} ask ${await tagged(n, 'bm.gvask')} gvp ${await tagged(n, 'bm.gvp')} gvi ${await sc(n, 'bm.gvi')}`);
    console.log(`   [${w}] ${o.join(' ; ')} ; #dt${s} ${(await run(`scoreboard players get #dt${s} bm.gvdt`)).replace(/.*has /, '')} #ld ${(await run(`scoreboard players get #ld${s} bm.gvld`)).replace(/.*has /, '')}`); };
  await dump('after pass 1');
  const second = await runOut();
  await dump('after pass 2');
  ok('...and again: to the third raider - not back to TestRat', second && second !== 'TestRat' && second !== first, `${first} -> ${second}`);
  const third = await runOut();
  ok('...and again: round to TestRat', third === 'TestRat', `${first} -> ${second} -> ${third}`);
  // (the one asked chooses: "Back to the Overworld", as their screen shows it)
  const X = C[third]; await run(`scoreboard players set ${third} bm.gvhc 0`);
  if (!X.buttons().some(b => /Back to the Overworld/.test(b.label))) { X.slot(0); await sleep(200); await X.useWait(); }
  const pr = await X.press(/Back to the Overworld/); await sleep(3000);
  ok('the one asked presses "Back to the Overworld": everyone home', !!pr && await wait(8000, async () => { for (const n of NAMES) if (!/overworld/.test(await dim(n))) return false; return true; }, 400),
     (await Promise.all(NAMES.map(dim))).join(' '));
  return done();

  async function done() {
    for (let s2 = 0; s2 < 8; s2++) await run(`function bm:p70/s${s2}/clean`);
    for (const n of NAMES) { await run(`execute as @a[name=${n},tag=bm.gvp] at @s run function bm:p70/home`); await run(`clear ${n}`); await run(`scoreboard players reset ${n} bm.pty`); }
    for (const f of ['heist_hard_any', 'plan_safe']) await run(`function bm:admin/${f}`);
    await run(`${O}forceload remove ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
    const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
    A.end(); B.end(); C3.end(); R.end(); process.exit(n === res.length ? 0 : 1);
  }
})().catch(e => { console.error(e); process.exit(1); });

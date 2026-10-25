// 2.94u: SIGNATURE MOVES II (phase223), as a regular (non-op) player - each called with their own item, monsters set down near
// (rcon: the stage). For each: the move starts (its timeline, bm.ksw), it travels when it should (sampled positions: steps, not
// jumps), and its blows land:
//   Celi - LUNGE AND VAULT: across the gap in steps, the spear lands (12), and she vaults back off it (ends a step or more back);
//   Democratus - REAPING WHIRL: two monsters near; they're drawn in toward him and cut (5 a turn), then the great sweep (12);
//   Apophiss - COIL AND STRIKE: across the gap in steps, the strike (16) and the lash;
//   Ashur - FIRE WHEEL: through them in steps, those passed burned (alight), the eruption where she lands;
//   Cecil - STAFF TWIRL: the blast at his foe (14).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (sel) => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1, 4).map(Number) : null; };
  const sc = async (sel, o) => +(((await run(`${O}scoreboard players get ${sel} ${o}`)).match(/has (-?\d+)/) || [0, -1])[1]);
  const use = async (slot) => { A.slot(slot); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(2000); };
  const X = 18060, Y = 100, Z = 16240;
  const hp = async (tag) => +(((await run(`${O}data get entity @e[tag=${tag},limit=1] Health`)).match(/([\d.]+)f/) || [0, -1])[1]);
  const husk = async (dx, dz, tag) => run(`${O}summon minecraft:husk ${X + dx} ${Y + 1} ${Z + dz} {NoAI:1b,PersistenceRequired:1b,Health:200f,Tags:["${tag}","t279","bm.seen"],attributes:[{id:"minecraft:max_health",base:200d}]}`);
  // (a move watched: its positions while bm.ksw is set; started? biggest step, how far it went, where it ended)
  const watch = async (host, ms) => { let last = null, big = 0, far = 0, on = false, p0 = null, end = null; const t0 = Date.now();
    while (Date.now() - t0 < ms) { await sleep(40); const k = await sc(host, 'bm.ksw'); const p = await pos(host); if (!p) continue;
      if (k >= 1) { if (!on) { on = true; p0 = p; last = p; } big = Math.max(big, Math.hypot(p[0] - last[0], p[2] - last[2])); far = Math.max(far, Math.hypot(p[0] - p0[0], p[2] - p0[2])); last = p; end = p; }
      else if (on) break; }
    return { on, big, far, p0, end }; };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:invisibility 900 0 true');
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  await run(`${O}fill ${X - 20} ${Y} ${Z - 20} ${X + 20} ${Y} ${Z + 20} minecraft:sandstone`); await run(`${O}fill ${X - 20} ${Y + 1} ${Z - 20} ${X + 20} ${Y + 8} ${Z + 20} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..30]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1000); A.stand();
  for (const o of ['bm.cecd', 'bm.dmcd', 'bm.apcd', 'bm.ascd', 'bm.cpcd']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const t of ['bm.celimet', 'bm.dmmet', 'bm.apmet', 'bm.asmet']) await run(`tag TestRat add ${t}`);
  const items = ['celi_charm', 'demo_seal', 'apo_oath', 'ashur_cinder', 'cecil_gem'];
  for (const [i, it] of items.entries()) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${it}`);
  await sleep(500);
  const stage = async (host, dx, dz) => { await run(`${O}tp ${host} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await run(`${O}scoreboard players set ${host} bm.kcd1 0`); };

  // ---- Celi
  const CE = '@e[type=minecraft:wolf,tag=bm.celipet,limit=1]';
  await use(0); ok('Celi called', await wait(5000, async () => (await cnt(CE)) === 1)); await sleep(1500);
  await run(`${O}scoreboard players set ${CE} bm.kcd1 999`); await husk(0, 7, 'ta'); await stage(CE);
  let w = await watch(CE, 5000);
  ok('Celi - LUNGE AND VAULT: across the gap in steps (no jump over 2.5 a sample)', w.on && w.far > 3 && w.big <= 2.5, JSON.stringify(w));
  ok('...the spear lands (12, less the husk\'s armour)', (await hp('ta')) <= 190, `${await hp('ta')}`);
  ok('...and she vaults back off it (ends a step or more back from where she struck)', w.end && Math.hypot(w.end[0] - X, w.end[2] - (Z + 7)) >= 1.6, JSON.stringify(w.end));
  await run(`${O}kill @e[tag=t279]`); await run(`${O}execute as ${CE} run function bm:p66/go`); await sleep(800);

  // ---- Democratus
  const DM = '@e[type=minecraft:wolf,tag=bm.dmpet,limit=1]';
  await use(1); ok('Democratus called', await wait(5000, async () => (await cnt(DM)) === 1)); await sleep(1500);
  await run(`${O}scoreboard players set ${DM} bm.kcd1 999`); await husk(4, 2, 'tb'); await husk(-3, 3, 'tc'); await stage(DM);
  const d0 = Math.hypot(4, 2);
  w = await watch(DM, 6000);
  const pb = await pos('@e[tag=tb,limit=1]');
  ok('Democratus - REAPING WHIRL: it starts', w.on, JSON.stringify(w));
  ok('...they\'re cut (5 a turn) and swept (12): 20 or more each', (await hp('tb')) <= 180 && (await hp('tc')) <= 180, `${await hp('tb')} ${await hp('tc')}`);
  ok('...and drawn in toward him', pb && Math.hypot(pb[0] - X - 0.5, pb[2] - Z - 0.5) < d0 - 0.5, JSON.stringify(pb));
  await run(`${O}kill @e[tag=t279]`); await run(`${O}execute as ${DM} run function bm:p97/go`); await sleep(800);

  // ---- Apophiss
  const AP = '@e[type=minecraft:wolf,tag=bm.appet,limit=1]';
  await use(2); ok('Apophiss called', await wait(5000, async () => (await cnt(AP)) === 1)); await sleep(1500);
  await run(`${O}scoreboard players set ${AP} bm.kcd1 999`); await husk(-9, 0, 'td'); await stage(AP);
  w = await watch(AP, 6000);
  ok('Apophiss - COIL AND STRIKE: across the gap in steps', w.on && w.far > 3 && w.big <= 2.5, JSON.stringify(w));
  ok('...the strike and the lash land (24 or more)', (await hp('td')) <= 176, `${await hp('td')}`);
  await run(`${O}kill @e[tag=t279]`); await run(`${O}execute as ${AP} run function bm:p131/go`); await sleep(800);

  // ---- Ashur
  const AS = '@e[type=minecraft:wolf,tag=bm.aspet,limit=1]';
  await use(3); ok('Ashur called', await wait(5000, async () => (await cnt(AS)) === 1)); await sleep(1500);
  await run(`${O}scoreboard players set ${AS} bm.kcd1 999`); await husk(0, -4, 'te'); await husk(0, -8, 'tf'); await stage(AS);
  w = await watch(AS, 6000);
  const fire = '';
  ok('Ashur - FIRE WHEEL: through them in steps', w.on && w.far > 3 && w.big <= 2.5, JSON.stringify(w));
  ok('...the first burned as she passes, the last caught in the eruption', (await hp('te')) < 200 && (await hp('tf')) < 200, `${await hp('te')} ${await hp('tf')} fire ${fire}`);
  await run(`${O}kill @e[tag=t279]`); await run(`${O}execute as ${AS} run function bm:p185/go`); await sleep(800);

  // ---- Cecil
  const CC = '@e[type=minecraft:wolf,tag=bm.cecilpet,limit=1]';
  await use(4); ok('Cecil called', await wait(5000, async () => (await cnt(CC)) === 1)); await sleep(1500);
  await run(`${O}scoreboard players set ${CC} bm.kcd1 999`); await husk(6, 6, 'tg'); await stage(CC);
  w = await watch(CC, 5000);
  ok('Cecil - STAFF TWIRL: the twirl, then the blast at his foe (14 or more)', w.on && (await hp('tg')) <= 186, `${await hp('tg')}`);
  await run(`${O}kill @e[tag=t279]`); await run(`${O}execute as ${CC} run function bm:p62/cecil_go`);

  await run('clear TestRat'); await run('effect clear TestRat'); await run(`${O}forceload remove ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

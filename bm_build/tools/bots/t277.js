// 2.94u: THE ATTACK KIT (atk.py, phase222), as a regular (non-op) player - followers called with their own items, a monster set
// down near them (rcon: the stage). Their position sampled every tick-ish while they fight:
//   Bloo's pounce: a dash - carried to it in steps (no jump over 1.3 blocks in one sample), and the blow lands (it's hurt);
//   Bender's tackle: the same;
//   a blow's hit-stop: the follower's hold (bm.khs) set on the blow;
//   KillerWatt (no animation clock to hold): his blows still land, the impact with them.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (sel) => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1, 4).map(Number) : null; };
  const use = async (slot) => { A.slot(slot); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(2000); };
  const X = 17980, Y = 100, Z = 16160;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:invisibility 900 0 true');
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  await run(`${O}fill ${X - 20} ${Y} ${Z - 20} ${X + 20} ${Y} ${Z + 20} minecraft:sandstone`); await run(`${O}fill ${X - 20} ${Y + 1} ${Z - 20} ${X + 20} ${Y + 8} ${Z + 20} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..30]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1000); A.stand();
  for (const o of ['bm.bocd', 'bm.bvcd', 'bm.kxcd']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/bo_claw'); await run('loot replace entity TestRat hotbar.1 loot bm:items/bv_ball');
  await run('loot replace entity TestRat hotbar.2 loot bm:items/kw_spark'); await sleep(500);

  const watch = async (host, label, ms) => {        // (its position each sample while it fights; the biggest single jump)
    let last = await pos(host), big = 0, moved = 0;
    const t0 = Date.now();
    while (Date.now() - t0 < ms) { await sleep(40); const p = await pos(host); if (!p || !last) continue;
      const d = Math.hypot(p[0] - last[0], p[2] - last[2]); if (d > 1.3 && process.env.DBG) console.log('   jump', JSON.stringify(last), JSON.stringify(p), await run(`${O}scoreboard players get ${host} bm.ksg`), await run(`${O}scoreboard players get ${host} bm.kd`)); big = Math.max(big, d); moved += d; last = p; }
    return { big, moved };
  };
  const zombie = async (dx, dz, tag) => { await run(`${O}summon minecraft:husk ${X + dx} ${Y + 1} ${Z + dz} {NoAI:1b,PersistenceRequired:1b,Health:200f,Tags:["${tag}","bm.seen"],attributes:[{id:"minecraft:max_health",base:200d}]}`); };
  const hp = async (tag) => +(((await run(`${O}data get entity @e[tag=${tag},limit=1] Health`)).match(/([\d.]+)f/) || [0, -1])[1]);

  // ---- Bloo's pounce
  await use(0); const BLOO = '@e[type=minecraft:wolf,tag=bm.bopet,limit=1]';
  ok('Bloo called', await wait(5000, async () => (await cnt(BLOO)) === 1));
  await sleep(1500); await run(`${O}scoreboard players set ${BLOO} bm.bkrc 0`);
  await zombie(0, 9, 't277a');
  const w1 = await watch(BLOO, 'bloo', 3500);
  ok('Bloo goes for it: carried there in steps - moved, never more than 1.3 blocks in one sample', w1.moved > 4 && w1.big <= 1.3, JSON.stringify(w1));
  ok('...and his blows land (it\'s hurt)', await wait(4000, async () => (await hp('t277a')) < 200 && (await hp('t277a')) >= 0), `${await hp('t277a')}`);
  ok('...a blow holds his animation a beat (bm.khs set on it)', await wait(6000, async () => /has [12]\b/.test(await run(`${O}scoreboard players get ${BLOO} bm.khs`)), 50));
  await run(`${O}kill @e[tag=t277a]`); await run(`${O}execute as ${BLOO} run function bm:p191/go`); await sleep(1000);

  // ---- Bender's tackle
  await use(1); const BEN = '@e[type=minecraft:wolf,tag=bm.bvpet,limit=1]';
  ok('Bender called', await wait(5000, async () => (await cnt(BEN)) === 1));
  await sleep(1500); await run(`${O}scoreboard players set ${BEN} bm.bvrg 9999`);                     // (his Rage held back: the tackle's what we watch)
  await zombie(-8, 4, 't277b');
  const w2 = await watch(BEN, 'bender', 3500);
  ok('Bender bounds in: in steps, never more than 1.3 a sample', w2.moved > 3 && w2.big <= 1.3, JSON.stringify(w2));
  ok('...his blows land', await wait(4000, async () => (await hp('t277b')) < 200 && (await hp('t277b')) >= 0), `${await hp('t277b')}`);
  await run(`${O}kill @e[tag=t277b]`); await run(`${O}execute as ${BEN} run function bm:p195/go`); await sleep(1000);

  // ---- KillerWatt: no clock to hold, his blows still land
  await use(2); const KW = '@e[type=minecraft:wolf,tag=bm.kxpet,limit=1]';
  ok('KillerWatt called', await wait(5000, async () => (await cnt(KW)) === 1));
  await zombie(3, 3, 't277c');
  ok('...his blows land (the impact with them)', await wait(12000, async () => (await hp('t277c')) < 200 && (await hp('t277c')) >= 0), `${await hp('t277c')}`);
  await run(`${O}kill @e[tag=t277c]`); await run(`${O}execute as ${KW} run function bm:p79/pet/vanish`);

  // ---- clean up
  await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}forceload remove ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

// 2.94u: ALTERNATE SWINGS (atk.ALT) and the Frog's sword, as a regular (non-op) player - followers called with their own items, a
// monster set down beside them (rcon: the stage - their signature moves held back, so it's their ordinary blows we watch):
//   Leo, Democratus, Dennis, Bones, Apophiss: over a run of ordinary blows both swings come up (bm.kalt 0 and 1), and they land;
//   the Frog with Mustache: his sword sits at his front foot (low, by his side), not hanging in the air off his body.
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
  const X = 18140, Y = 100, Z = 16320;
  const hp = async (tag) => +(((await run(`${O}data get entity @e[tag=${tag},limit=1] Health`)).match(/([\d.]+)f/) || [0, -1])[1]);
  const husk = async (dx, dz, tag) => run(`${O}summon minecraft:husk ${X + dx} ${Y + 1} ${Z + dz} {NoAI:1b,PersistenceRequired:1b,Health:200f,Tags:["${tag}","t281","bm.seen"],attributes:[{id:"minecraft:max_health",base:200d}]}`);
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
  const stage = async (host, dx, dz) => { await run(`${O}tp ${host} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await run(`${O}scoreboard players set ${host} bm.kcd1 0`); };

  const K = [['Leo', 'leo_crest', 'bm.leopet', 'p98/home/leo'], ['Democratus', 'demo_seal', 'bm.dmpet', 'p97/send_home'], ['Dennis', 'dw_horn', 'bm.dwpet', 'p163/dw/home'],
             ['Bones', 'bn_whistle', 'bm.bjpet', 'p196/home'], ['Apophiss', 'apo_oath', 'bm.appet', 'p98/home/apo']];
  for (const t of ['bm.dmmet', 'bm.apmet']) await run(`tag TestRat add ${t}`);
  for (const o of ['bm.lecd', 'bm.dmcd', 'bm.apcd']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const o of ['bm.apcd','bm.ascd','bm.avcd','bm.bjcd','bm.bocd','bm.bvcd','bm.cecd','bm.cpcd','bm.dmcd','bm.dncd','bm.dwcd','bm.emcd','bm.fgcd','bm.fycd','bm.kkcd','bm.kxcd','bm.lecd','bm.lncd','bm.mzcd','bm.nbcd','bm.omcd','bm.picd','bm.pqcd','bm.svcd','bm.tucd','bm.wlcd','bm.xccd','bm.xlcd','bm.xmcd','bm.ybcd','bm.zbcd']) await run(`scoreboard players set TestRat ${o} 0`);   // (none of them still recovering from an earlier test)
  const only = process.argv[2] ? new RegExp(process.argv[2], 'i') : null;
  for (const [name, iid, tag, home] of K) {
    if (only && !only.test(name)) continue;
    const H = `@e[type=minecraft:wolf,tag=${tag},limit=1]`;
    await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); await sleep(400);
    A.chats.length = 0; await use(0); if (!ok(`${name} called`, await wait(6000, async () => (await cnt(H)) === 1), A.chats.slice(-2).join(' | ').slice(0, 200))) continue;
    await sleep(1000); await run(`${O}scoreboard players set ${H} bm.kcd1 99999`); await run(`${O}scoreboard players set ${H} bm.kcd2 99999`);
    await run(`${O}scoreboard players reset ${H} bm.kalt`);
    await stage(H); await run(`${O}scoreboard players set ${H} bm.kcd1 99999`); await husk(0, 2, 'tz0');
    const seen = new Set(); const t0 = Date.now();
    while (Date.now() - t0 < 25000 && seen.size < 2) { const v = await sc(H, 'bm.kalt'); if (v === 0 || v === 1) seen.add(v); await sleep(100); }
    ok(`${name}: over a run of blows, both swings come up`, seen.size === 2, [...seen].join(','));
    ok('...and they land', (await hp('tz0')) < 200, `${await hp('tz0')}`);
    await run(`${O}kill @e[tag=t281]`); await run(`${O}execute as TestRat at @s run function bm:${home}`); await sleep(1000);
  }
  // ---- the Frog's sword
  if (!only || only.test('Frog')) {
    const FG = '@e[type=minecraft:wolf,tag=bm.frogpet,limit=1]';
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/frog_signet'); await sleep(400);
    await use(0); ok('the Frog with Mustache called', await wait(6000, async () => (await cnt(FG)) === 1));
    await sleep(2500);
    const tr = (await run(`${O}execute as ${FG} on passengers if entity @s[tag=bm.fp_weap] run data get entity @s transformation.translation`)).match(/\[(-?[\d.]+)f, (-?[\d.]+)f, (-?[\d.]+)f\]/);
    const v = tr ? tr.slice(1, 4).map(Number) : null;
    ok('...his sword sits at his front foot, low by his side (not hanging in the air off his body)', v && v[0] > 0.1 && v[0] < 0.35 && v[1] < -0.45 && v[2] > 0.1, JSON.stringify(v));
    await run(`${O}execute as TestRat at @s run function bm:p138/home/frog`);
  }
  for (const t of ['bm.dmmet', 'bm.apmet']) await run(`tag TestRat remove ${t}`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run(`${O}forceload remove ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

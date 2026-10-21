// 2.83b: WHAT THE DEN SELLS PASSES THE COAT CHECK - as a regular (non-op) player (rcon sets the stage: a platform, coins and
// Tokens in the pack, a plain golden apple and a sword from outside).
//   into a heist through the Ledger (Plan a Heist, Tier I, 3 tries); in the den, Goldtooth's trades (right-click him, pick a
//     trade, take it): a Bond Sigil of Fury and a golden apple.
//   through the den's copper door into the Locker Hall, and the hall's plate back: in the den again (it used to say "only heist
//     tools go back into the vault" and leave you in the hall - stuck, with nowhere to put a sigil).
//   home (Leave the heist): the sigil and the apple come home too.
//   the next heist's door: the Fury sigil and Goldtooth's apple go in; the plain apple and the sword from outside still wait
//     with the Fixer - and come home with you.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const passes = async c => /passed/i.test(await run(c));
  const dim = async () => (await run('data get entity TestRat Dimension')).replace(/.*data: /, '');
  const tags = async () => (await run('tag TestRat list')).replace(/.*: /, '');
  const cnt = async pred => { const m = (await run(`clear TestRat ${pred} 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const fury = '*[minecraft:custom_data~{bm:"sigil_fury"}]';
  const gtApple = 'minecraft:golden_apple[minecraft:custom_data~{bm_gt:1b}]';
  const plainApple = 'minecraft:golden_apple[!minecraft:custom_data]';
  const pos = async () => { const m = (await run('data get entity TestRat Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const sc = async o => +(((await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const press = async (re) => { const b = await A.press(re); await sleep(900); return b; };
  const uuidEnt = async sel => { const m = (await run(`execute in bm:gutter run data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const O = 'execute in minecraft:overworld run ', GU = 'execute in bm:gutter run ';
  const HX = 13440, HY = 121, HZ = 13400;
  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));

  // ---- the stage
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/heist_variants_never'); await run('function bm:admin/heist_boss_std');
  await run(`${O}forceload add ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`); await run(`${O}fill ${HX - 4} ${HY - 1} ${HZ - 4} ${HX + 4} ${HY - 1} ${HZ + 4} minecraft:stone`);
  await run(`${O}fill ${HX - 4} ${HY} ${HZ - 4} ${HX + 4} ${HY + 3} ${HZ + 4} minecraft:air`);
  await run(`${O}tp TestRat ${HX + 0.5} ${HY} ${HZ + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run(`spawnpoint TestRat ${HX} ${HY} ${HZ}`);
  for (const t of ['bm.gvp', 'bm.lgbag', 'bm.lgstart', 'bm.lkadv', 'bm.lgadv', 'bm.gvok', 'bm.gvask', 'bm.gvnext', 'bm.gvwait', 'bm.gvwaitd', 'bm.exon', 'bm.exask']) await run(`tag TestRat remove ${t}`);
  const pid = +((await run('scoreboard players get TestRat bm.pid')).match(/has (\d+)/) || [0, 0])[1];
  for (const k of ['bag', 'cb', 'ret']) await run(`data remove storage bm:gv ${k}.p${pid}`);
  await run(`data remove storage bm:lk r.p${pid}`);
  for (const o of ['bm.crew', 'bm.crewoff', 'bm.fcon']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger');
  for (let i = 0; i < 12; i++) await run('loot give TestRat loot bm:items/token');
  await run('item replace entity TestRat hotbar.5 with minecraft:diamond_sword'); await run('give TestRat minecraft:golden_apple 2');
  await sleep(1200); A.stand();

  // ================================================================== 1. into a heist, through the Ledger
  A.slot(0); await sleep(300); await A.useWait(); await press(/Plan a Heist/); await press(/Tier I\b(?!I)/); await press(/^3\b|3 tries/i);
  const inV = await wait(60000, async () => /gutter/.test(await dim()) && /bm\.gvp/.test(await tags()), 500);
  await sleep(2500); A.stand();
  ok('Through the Ledger: in the heist\'s den; the sword and the plain apples wait with the Fixer', inV && !(await cnt('minecraft:diamond_sword')) && !(await cnt(plainApple)), `${await dim()}`);
  if (!inV) { console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(1); }
  const gi = await sc('bm.gvi');
  const lm = `@e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${gi}},limit=1]`;
  const mp = (await run(`${GU}data get entity ${lm} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
  const at = (x, y, z) => [mp[0] + x - 12, mp[1] + y - 4, mp[2] + z - 12];

  // ---- Goldtooth: a Bond Sigil of Fury and a golden apple, bought at his counter (coins and insignia to pay with)
  const GT = `@e[type=minecraft:villager,tag=bm.gvgt,x=${mp[0]},y=${mp[1]},z=${mp[2]},distance=..24,limit=1]`;
  const idx = async (pred) => { for (let i = 0; i < 60; i++) { const o = await run(`${GU}data get entity ${GT} Offers.Recipes[${i}].sell`); if (/Found no|found no/.test(o) || !/data:/.test(o)) return -1; if (pred(o)) return i; } return -1; };
  const iF = await idx(o => /sigil_fury/.test(o)), iA = await idx(o => /golden_apple/.test(o) && !/enchanted/.test(o));
  ok('Goldtooth sells a Bond Sigil of Fury and golden apples (the apples marked as his)', iF >= 0 && iA >= 0 && /bm_gt/.test(await run(`${GU}data get entity ${GT} Offers.Recipes[${iA}].sell`)), `fury #${iF} apple #${iA}`);
  for (const i of [iF, iA]) for (const k of ['buy', 'buyB']) {
    const b = await run(`${GU}data get entity ${GT} Offers.Recipes[${i}].${k}`); const id = (b.match(/bm: ?"([a-z_]+)"/) || [])[1]; const n = +((b.match(/count: (\d+)/) || [0, 1])[1]);
    if (id) for (let j = 0; j < n; j++) await run(`loot give TestRat loot bm:items/${id}`);
  }
  const [gx, gy, gz] = (await run(`${GU}data get entity ${GT} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
  await run(`${GU}tp TestRat ${gx} ${gy} ${gz - 2} 0 10`); await sleep(1500);
  const buy = async (i) => { A.windows.length = 0; A.interact(await uuidEnt(GT)); await sleep(900); const w = A.windows[A.windows.length - 1]; if (!w) return false;
    A.write('select_trade', { slot: i }); await sleep(300);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(500);
    A.close(w.windowId); await sleep(400); return true; };
  const gEid = await uuidEnt(GT);
  const pay = [await run(`${GU}data get entity ${GT} Offers.Recipes[${iF}].buy`), await run(`${GU}data get entity ${GT} Offers.Recipes[${iF}].buyB`)].join(' / ').replace(/.*?data: /g, '').slice(0, 300);
  const b1 = await buy(iF), b2 = await buy(iA);
  ok('...bought: the sigil and a marked golden apple in the pack', (await cnt(fury)) >= 1 && (await cnt(gtApple)) >= 1,
     `fury ${await cnt(fury)} apple ${await cnt(gtApple)} | eid ${gEid} windows ${b1} ${b2} | pays ${pay} | inv ${(await run('data get entity TestRat Inventory')).slice(0, 400)}`);

  // ================================================================== 2. the Locker Hall and back, with them
  await run(`${GU}tp TestRat ${at(8, 4, 3).map((v, i) => i === 1 ? v : Math.floor(v) + 0.5).join(' ')} 180 10`); await sleep(1500);
  const dEid = await uuidEnt(`@e[type=minecraft:interaction,tag=bm.lkdoor,x=${mp[0]},y=${mp[1]},z=${mp[2]},distance=..24,limit=1]`);
  A.interact(dEid); await sleep(1200);
  const p1 = await pos();
  ok('The den\'s copper door: into the Locker Hall', p1 && p1[0] > -256 && p1[0] < -241, `${p1} door eid ${dEid} lobby ${mp}`);
  A.chats.length = 0;
  await A.walkTo(-248.5, -241.5); await sleep(2500); A.stand();
  const p2 = await pos();
  ok('...the hall\'s plate, a sigil and apple in hand: back in the den (not "only heist tools")', p2 && Math.abs(p2[0] - mp[0]) < 16 && Math.abs(p2[2] - mp[2]) < 16 && /bm\.gvp/.test(await tags()) &&
     !A.chats.some(c => /Only heist tools/.test(c)), `${p2} | ${A.chats.slice(-1).join('').slice(0, 120)}`);
  ok('...still carrying both', (await cnt(fury)) >= 1 && (await cnt(gtApple)) >= 1);

  // ================================================================== 3. home, then the next heist's door
  A.slot(0); await sleep(300); await A.useWait(); await press(/Leave the heist/); await press(/Leave now/);
  await wait(10000, async () => /overworld/.test(await dim()), 300); await sleep(4500); A.stand();
  ok('Leave the heist: home - the sigil and the apple come too, with the sword and the plain apples', /overworld/.test(await dim()) && (await cnt(fury)) >= 1 && (await cnt(gtApple)) >= 1 &&
     (await cnt('minecraft:diamond_sword')) === 1 && (await cnt(plainApple)) === 2, `${await dim()} fury ${await cnt(fury)} gt ${await cnt(gtApple)} plain ${await cnt(plainApple)}`);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run(`${O}tp TestRat ${HX + 0.5} ${HY} ${HZ + 0.5} 0 0`); await sleep(1500); A.stand();
  A.slot(0); await sleep(300); await A.useWait(); await press(/Plan a Heist/); await press(/Tier I\b(?!I)/); await press(/^3\b|3 tries/i);
  const in2 = await wait(60000, async () => /gutter/.test(await dim()) && /bm\.gvp/.test(await tags()), 500); await sleep(2500); A.stand();
  ok('The next heist\'s door: the Fury sigil and Goldtooth\'s apple go in', in2 && (await cnt(fury)) >= 1 && (await cnt(gtApple)) >= 1, `fury ${await cnt(fury)} gt ${await cnt(gtApple)}`);
  ok('...the sword and the plain apples from outside still wait with the Fixer', !(await cnt('minecraft:diamond_sword')) && !(await cnt(plainApple)));
  A.slot(0); await sleep(300); await A.useWait(); await press(/Leave the heist/); await press(/Leave now/);
  await wait(10000, async () => /overworld/.test(await dim()), 300); await sleep(4500); A.stand();
  ok('...and come home with you', /overworld/.test(await dim()) && (await cnt('minecraft:diamond_sword')) === 1 && (await cnt(plainApple)) === 2);

  await run('clear TestRat'); await run(`${O}forceload remove ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

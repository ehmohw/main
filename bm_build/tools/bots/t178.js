// 2.80b: Cecil's dolls wait until you've met their follower - as a regular (non-op) player, through his own trading window.
// A player who has met no one sees every follower's doll still under wraps (out of stock: the trade won't go); holding
// KillerWatt's Spark (meeting him) unwraps his doll, and his doll is bought for real; the others stay wrapped. A second
// player stepping up to the counter while the first is still there doesn't change the list; once the first walks off, the
// counter is the second player's, and it shows their own. rcon only sets the stage (Cecil at a stall, trophies, the Spark).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel) => { const u = await uuidOf(sel); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const has = async (who, iid) => +(((await run(`clear ${who} *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const X = 16300, Y = 100, Z = 16060;
  const KINDS = ['cecil', 'celi', 'leo', 'demo', 'killerwatt', 'apo', 'tul', 'zib', 'pearl', 'donado', 'wil', 'frog', 'fishy', 'emma', 'escort'];
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  for (const k of KINDS) await run(`advancement revoke TestRat only bm:met/${k}`);
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} minecraft:stone`); await run(`${O}fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  const at = async (C, nm, x, y, z, yaw, pitch) => { await run(`${O}tp ${nm} ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => C.pos && Math.abs(C.pos.x - x) < 0.05 && Math.abs(C.pos.z - z) < 0.05, 100); await sleep(300); };
  await at(A, 'TestRat', X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await run(`${O}execute positioned ${X + 0.5} ${Y + 1} ${Z + 3.5} rotated 180 0 run function bm:p45/cecil/spawn`); await sleep(1500);
  const CEC = `@e[type=minecraft:villager,tag=bm.npc_wizard,x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..2,limit=1]`;
  ok('Cecil is at his stall', (await cnt(CEC)) === 1);
  // (his doll trades and where they sit)
  const slots = {};
  const scan = async () => { const out = {};
    for (let i = 0; i < 80; i++) { const s = await nbt(CEC, `Offers.Recipes[${i}].sell.components."minecraft:custom_data"`); if (/Found no elements/i.test(s)) break;
      const m = s.match(/bm: "(doll_[a-z]+)"/); if (m) out[m[1]] = i;
      if (/bm_wrapped/.test(s)) out['#' + i] = i; }
    return out; };
  await sleep(1500);
  const s0 = await scan(); const wrapped0 = Object.keys(s0).filter(k => k[0] === '#').length, open0 = Object.keys(s0).filter(k => k[0] !== '#');
  ok("met no one yet: all thirteen dolls under wraps, none on sale", wrapped0 === 13 && open0.length === 0, `wrapped ${wrapped0}, on sale ${open0.join(',')}`);
  const wrapIdx = +Object.keys(s0).find(k => k[0] === '#').slice(1);
  ok('...a wrapped doll is out of stock (its trade will not go)', /^0$/.test((await nbt(CEC, `Offers.Recipes[${wrapIdx}].maxUses`)).trim()));
  // the wrapped doll can't be bought, even with the price in hand
  const price = +(((await nbt(CEC, `Offers.Recipes[${wrapIdx}].buy.count`)).match(/(\d+)/) || [0, 0])[1]);
  for (let i = 0; i < price * 2; i++) await run('loot give TestRat loot bm:items/trophy');
  const cec = await entOf(A, CEC);
  A.windows.length = 0; if (cec) A.interact(cec.entityId); await sleep(900);
  let w = A.windows[A.windows.length - 1];
  ok("right-clicking Cecil opens his trades", !!w, cec ? '' : 'Cecil not seen by the client');
  if (w) { A.write('select_trade', { slot: wrapIdx }); await sleep(300);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(500);
    A.close(w.windowId); await sleep(400); }
  ok('...picking a wrapped doll buys nothing: no doll, the trophies kept', (+(((await run('clear TestRat *[minecraft:custom_data~{bm_wrapped:1b}] 0')).match(/Found (\d+)/) || [0, 0])[1])) === 0 && (await has('TestRat', 'trophy')) === price * 2,
     `trophies ${await has('TestRat', 'trophy')}`);
  // meet KillerWatt: hold his Spark
  await run('loot give TestRat loot bm:items/kw_spark'); await sleep(2500);
  const s1 = await scan();
  ok("holding KillerWatt's Spark (meeting him) unwraps his doll - and only his", s1.doll_kw >= 0 && Object.keys(s1).filter(k => k[0] !== '#').length === 1,
     Object.keys(s1).filter(k => k[0] !== '#').join(','));
  ok('...in the same place in the list', s1.doll_kw === Object.values(s0).sort((a, b) => a - b)[4], `#${s1.doll_kw}`);
  A.windows.length = 0; A.interact(cec.entityId); await sleep(900); w = A.windows[A.windows.length - 1];
  if (w) { A.write('select_trade', { slot: s1.doll_kw }); await sleep(300);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(500);
    A.close(w.windowId); await sleep(400); }
  ok("...and KillerWatt's doll is bought for real", (await has('TestRat', 'doll_kw')) === 1 && (await has('TestRat', 'trophy')) === price, `kw ${await has('TestRat', 'doll_kw')}, trophies ${await has('TestRat', 'trophy')}`);
  // a second player at the counter
  const B = await bot('TestRat2'); await sleep(2500); B.stand();
  for (const k of KINDS) await run(`advancement revoke TestRat2 only bm:met/${k}`); await run('clear TestRat2'); await run('gamemode survival TestRat2');
  await run('loot give TestRat2 loot bm:items/apo_oath'); await sleep(500);
  await at(B, 'TestRat2', X + 2.5, Y + 1, Z + 0.5, 0, 0); await sleep(2500);
  const s2 = await scan();
  ok('a second player steps up while the first is still there: the list stays the first\'s', s2.doll_kw >= 0 && !(s2.doll_apo >= 0), Object.keys(s2).filter(k => k[0] !== '#').join(','));
  await at(A, 'TestRat', X + 0.5, Y + 1, Z - 10.5, 0, 0); await sleep(2500);
  const s3 = await scan();
  ok('...the first walks off: the counter is the second\'s - Apophiss unwrapped, KillerWatt wrapped again', s3.doll_apo >= 0 && !(s3.doll_kw >= 0), Object.keys(s3).filter(k => k[0] !== '#').join(','));
  await at(B, 'TestRat2', X + 0.5, Y + 1, Z - 10.5, 0, 0); await sleep(2500);
  const s4 = await scan();
  ok('no one at the counter: every doll wrapped again', Object.keys(s4).filter(k => k[0] !== '#').length === 0);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`); await run('clear TestRat'); await run('clear TestRat2');
  for (const k of KINDS) { await run(`advancement revoke TestRat only bm:met/${k}`); await run(`advancement revoke TestRat2 only bm:met/${k}`); }
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); A.end(); B.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

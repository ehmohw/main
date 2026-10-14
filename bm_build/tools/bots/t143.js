// 2.78: the Key of New Beginnings, as a regular (non-op) player who has beaten the Hollow King: bought from the Fence in a
// real trade; used - its dialog says what it resets and what stays - "No" changes nothing, "Yes - start over" clears the
// record (the key used up). What was earned stays earned: the Warpstone still crosses over (and back), the Hollow sleeps for
// a veteran mid-climb, Wilfrey still answers his locket, and climbing to the top again gives no second Warpstone. The key
// won't turn with a record already clear, nor while a dungeon boss is awake nearby. A record reset before 2.78 (no trace
// of how far it went) is rebuilt from the Warpstone carried. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel, dim = 'minecraft:overworld') => { const m = (await run(`execute in ${dim} run execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel) => { const u = await uuidOf(sel); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const has = async (who, iid) => +(((await run(`clear ${who} *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const slotOf = async (iid) => { for (let i = 0; i < 36; i++) if (new RegExp(`"${iid}"`).test(await nbt('TestRat', `Inventory[{Slot:${i}b}].components."minecraft:custom_data".bm`))) return i; return -1; };
  const tagged = async (t) => !/failed|No entity/i.test(await run(`execute if entity @a[name=TestRat,tag=${t}]`));
  const dimOf = async () => (await run('data get entity TestRat Dimension')).replace(/^.*data: /, '').trim();
  const X = 16480, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2500, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const useHeld = async (iid, ms = 1700, sneak = false) => { const s = await slotOf(iid); if (s < 0 || s > 8) return false; A.slot(s); await sleep(300);
    if (sneak) { A.input({ shift: true }); await sleep(250); }
    const n0 = A.dialogN.length; A.use(); await sleep(ms); A.release(); if (sneak) { await sleep(150); A.input({}); } await sleep(500); return A.dialogN.length > n0; };

  // ---------------------------------------------------------------- the stage: a conqueror (the Hollow King beaten), from scratch
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await run('tag TestRat remove bm.got_warp'); await run('tag TestRat remove bm.cqbm'); await run('scoreboard players set TestRat bm.conqb 0');
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set TestRat bm.wpc 0'); await run('scoreboard players set TestRat bm.wlcd 0');
  ok('a conqueror: the best-ever record follows the record (6)', await wait(3000, async () => (await sc('TestRat', 'bm.conqb')) === 6));
  ok('...and the Hollow King\'s Warpstone is given, once', await wait(3000, async () => (await has('TestRat', 'hollow_warpstone')) === 1));

  // ---------------------------------------------------------------- the Fence sells the key: a real trade
  await run(`${O}execute positioned ${X + 0.5} ${Y + 1} ${Z + 3.5} rotated 180 0 run function bm:npc/fence`); await sleep(1200);
  const FEN = `@e[type=minecraft:wandering_trader,tag=bm.npc_fence,x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..2,limit=1]`;
  let idx = -1;
  for (let i = 0; i < 80 && idx < 0; i++) {
    const s = await nbt(FEN, `Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`);
    if (/Found no elements|No elements/i.test(s)) break;
    if (/"renewal_key"/.test(s)) idx = i;
  }
  ok('the Fence sells the Key of New Beginnings', idx >= 0, `trade #${idx}`);
  const price = +(((await nbt(FEN, `Offers.Recipes[${idx}].buy.count`)).match(/(\d+)/) || [0, 0])[1]);
  for (let i = 0; i < price; i++) await run('loot give TestRat loot bm:items/token');
  const fen = await entOf(A, FEN);
  A.windows.length = 0; if (fen) A.interact(fen.entityId); await sleep(900);
  const w = A.windows[A.windows.length - 1];
  if (w && idx >= 0) {
    A.write('select_trade', { slot: idx }); await sleep(300);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(500);
    A.close(w.windowId); await sleep(400);
  }
  ok(`bought: the key in the pack, the ${price} Tokens gone`, (await has('TestRat', 'renewal_key')) === 1 && (await has('TestRat', 'token')) === 0);
  let ks = await slotOf('renewal_key');
  if (ks >= 9) { A.write('window_click', { windowId: 0, stateId: 0, slot: ks, mouseButton: 4, mode: 2, changedSlots: [], cursorItem: undefined }); await sleep(400); }
  if (ks >= 9) { await run('item replace entity TestRat hotbar.4 from entity TestRat inventory.' + (ks - 9)); await run('item replace entity TestRat inventory.' + (ks - 9) + ' with minecraft:air'); }

  // ---------------------------------------------------------------- the key: its dialog; "No" changes nothing
  let shown = await useHeld('renewal_key', 700);
  const bt = A.buttons().map(b => b.label).join(' | ');
  const body = JSON.stringify(A.dialogN[A.dialogN.length - 1] || '');
  ok('use the key: a dialog asks first (Yes - start over / No)', shown && /Yes - start over/.test(bt) && /\bNo\b/.test(bt), bt);
  ok('...it says what stays earned (the Warpstone, Wilfrey, the Serpent\'s Den)', /Warpstone/.test(body) && /Wilfrey/.test(body) && /Serpent/.test(body));
  await A.press(/^No$/); await sleep(800);
  ok('"No": the record stands, the key kept', (await sc('TestRat', 'bm.conq')) === 6 && (await has('TestRat', 'renewal_key')) === 1);

  // ---------------------------------------------------------------- not while a boss is awake nearby
  await run(`${O}summon minecraft:marker ${X + 4} ${Y + 1} ${Z} {Tags:["bm.arena","bm.t143a"]}`); await run(`${O}scoreboard players set @e[type=minecraft:marker,tag=bm.t143a] bm.bs 2`);
  A.bars.length = 0; shown = await useHeld('renewal_key', 700);
  ok('a dungeon boss awake nearby: the key won\'t turn (no dialog; it says why)', !shown && /Finish the fight first/.test(A.bars.join(' ')), A.bars.slice(-1).join('').slice(0, 100));
  await run(`${O}kill @e[type=minecraft:marker,tag=bm.t143a]`); await sleep(500);

  // ---------------------------------------------------------------- "Yes - start over"
  A.titles.length = 0;
  shown = await useHeld('renewal_key', 700);
  await A.press(/Yes - start over/); await sleep(1000);
  ok('"Yes - start over": the record is clear (0) and the key used up', (await sc('TestRat', 'bm.conq')) === 0 && (await has('TestRat', 'renewal_key')) === 0);
  ok('..."A NEW BEGINNING"', A.titles.some(t => /NEW BEGINNING/.test(t)), A.titles.join(' | ').slice(0, 100));
  ok('...the best-ever record remembers the Hollow King (6)', (await sc('TestRat', 'bm.conqb')) === 6);
  await sleep(1500);
  ok('...a veteran mid-climb is no challenger: the Hollow sleeps for them', !(await tagged('bm.hch')));

  // ---------------------------------------------------------------- earned stays earned: the Warpstone crosses over - and back
  A.bars.length = 0;
  await useHeld('hollow_warpstone', 1800);
  ok('the Warpstone still crosses over: the Hollow Throne', await wait(4000, async () => /hollow_throne/.test(await dimOf())), `${await dimOf()} ${A.bars.slice(-1).join('')}`);
  ok('...not "the stone is cold"', !/stone is cold/i.test(A.bars.join(' ')));
  await sleep(1500);
  ok('...and the Hollow lies asleep for them (no challenger in the Throne)', /has 1/.test(await run('scoreboard players get #hsafe bm.p2')));
  await run('scoreboard players set TestRat bm.wpc 0'); await sleep(400);
  await useHeld('hollow_warpstone', 1800);
  ok('...used again, it brings them back where they were', await wait(5000, async () => /overworld/.test(await dimOf())), await dimOf());
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);

  // ---------------------------------------------------------------- Wilfrey still answers his locket
  const pid = await sc('TestRat', 'bm.pid');
  await run(`${O}kill @e[type=minecraft:wolf,tag=bm.wilfrey]`);
  await run('item replace entity TestRat hotbar.6 with minecraft:air'); await run('loot replace entity TestRat hotbar.6 loot bm:items/wilfrey_locket');
  A.bars.length = 0; await useHeld('wilfrey_locket', 1500);
  ok('Wilfrey still answers his locket (not "the locket is cold")', await wait(3000, async () => (await cnt(`@e[type=minecraft:wolf,tag=bm.wilfrey,scores={bm.pid=${pid}}]`)) === 1) &&
     !/locket is cold/i.test(A.bars.join(' ')), A.bars.slice(-1).join('').slice(0, 100));
  await sleep(1200); await useHeld('wilfrey_locket', 1500, true);
  ok('...sneak + use: he rests', await wait(3000, async () => (await cnt(`@e[type=minecraft:wolf,tag=bm.wilfrey,scores={bm.pid=${pid}}]`)) === 0));

  // ---------------------------------------------------------------- an empty record: the key would change nothing
  await run('loot give TestRat loot bm:items/renewal_key'); await sleep(300);
  ks = await slotOf('renewal_key');
  A.bars.length = 0; shown = await useHeld('renewal_key', 700);
  ok('with the record already clear the key won\'t turn (it says so, and stays)', !shown && /already clear/.test(A.bars.join(' ')) && (await has('TestRat', 'renewal_key')) === 1,
     A.bars.slice(-1).join('').slice(0, 100));

  // ---------------------------------------------------------------- the climb again: the fifth conquest wakes the Hollow; the top again, no second Warpstone
  await run('scoreboard players set TestRat bm.conq 5'); await sleep(1500);
  ok('back at the fifth conquest: a challenger again (the Hollow wakes for the King\'s fight)', await tagged('bm.hch'));
  await run('scoreboard players set TestRat bm.conq 6'); await sleep(2500);
  ok('the Hollow King beaten again: still just the one Warpstone', (await has('TestRat', 'hollow_warpstone')) === 1);

  // ---------------------------------------------------------------- reset before 2.78: rebuilt from the Warpstone carried
  await run('scoreboard players set TestRat bm.conq 0'); await run('scoreboard players set TestRat bm.conqb 0'); await run('tag TestRat remove bm.cqbm');
  ok('a record reset before 2.78 (best-ever unknown) - the Warpstone on them: rebuilt to 6', await wait(3000, async () => (await sc('TestRat', 'bm.conqb')) === 6));
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.conqb 0'); await run('tag TestRat remove bm.cqbm'); await run('advancement revoke TestRat only bm:story/boss_hollow');
  await sleep(1800);
  ok('...a newcomer with no trace of the King stays at 0 - and is a challenger', (await sc('TestRat', 'bm.conqb')) === 0 && await tagged('bm.hch'));

  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`); await run('clear TestRat'); await run('effect clear TestRat');
  await run('scoreboard players set TestRat bm.conq 6'); await run('tag TestRat add bm.got_warp');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); R.end(); process.exit(0);
})();

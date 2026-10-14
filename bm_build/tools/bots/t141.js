// 2.77d: the Emma doll Cecil sells, as a regular (non-op) player: bought from Cecil with trophies (a real trade - his
// window opened, the doll's trade picked, the doll shift-clicked out), set down with the doll itself (right-click looking at
// the floor), right-clicked so she twirls, her charm curing poison within 10 blocks, a plain punch leaving her be, and sneak
// + punch picking her up again. rcon only sets the stage.
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
  const X = 16240, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };

  // ---------------------------------------------------------------- Cecil at his stall; three trophies in the bot's pocket
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await run(`${O}execute positioned ${X + 0.5} ${Y + 1} ${Z + 3.5} rotated 180 0 run function bm:p45/cecil/spawn`); await sleep(1500);
  const CEC = `@e[type=minecraft:villager,tag=bm.npc_wizard,x=${X + 0.5},y=${Y + 1},z=${Z + 3.5},distance=..2,limit=1]`;
  ok('Cecil is at his stall', (await cnt(CEC)) === 1);
  let idx = -1;
  for (let i = 0; i < 60 && idx < 0; i++) {
    const s = await nbt(CEC, `Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`);
    if (/Found no elements/i.test(s)) break;
    if (/"emma_doll"/.test(s)) idx = i;
  }
  ok('Cecil sells the Emma Doll', idx >= 0, `trade #${idx}`);
  const price = +(((await nbt(CEC, `Offers.Recipes[${idx}].buy.count`)).match(/(\d+)/) || [0, 0])[1]);   // (his price, as the pack sets it)
  for (let i = 0; i < price; i++) await run('loot give TestRat loot bm:items/trophy');
  ok('the bot carries his price in trophies', price > 0 && (await has('TestRat', 'trophy')) === price, `${price} trophies`);

  // ---------------------------------------------------------------- the trade: his window, the doll's trade, the doll taken out
  const cec = await entOf(A, CEC);
  A.windows.length = 0; if (cec) A.interact(cec.entityId); await sleep(900);
  const w = A.windows[A.windows.length - 1];
  ok('right-clicking Cecil opens his trades', !!w, cec ? '' : 'Cecil not seen by the client');
  if (w && idx >= 0) {
    A.write('select_trade', { slot: idx }); await sleep(300);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(500);
    A.close(w.windowId); await sleep(400);
  }
  const nd = await has('TestRat', 'emma_doll'), nt = await has('TestRat', 'trophy');
  ok('the trophies buy her: the doll in the bot\'s pocket, the trophies gone', nd === 1 && nt === 0, `dolls ${nd}, trophies ${nt}`);
  let hb = -1;                                                    // (where the trade put her)
  for (let i = 0; i < 36 && hb < 0; i++) if (/"emma_doll"/.test(await nbt('TestRat', `Inventory[{Slot:${i}b}].components."minecraft:custom_data".bm`))) hb = i;
  ok('...and it is the doll model (bm:emma3d)', /"bm:emma3d"/.test(await nbt('TestRat', `Inventory[{components:{"minecraft:custom_data":{bm:"emma_doll"}}}].components."minecraft:item_model"`)));
  if (hb < 0) hb = 0;
  if (hb >= 9) {                                                   // (in the pack, not the hotbar: the bot swaps it onto hotbar 0)
    A.write('window_click', { windowId: 0, stateId: 0, slot: hb, mouseButton: 0, mode: 2, changedSlots: [], cursorItem: undefined }); await sleep(400); hb = 0;
  }

  // ---------------------------------------------------------------- set down: right-click with her, looking at the floor
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 62);
  A.slot(hb); await sleep(300); A.use(); await sleep(450); A.release(); await sleep(500);
  const DOLL = `@e[type=minecraft:item_display,tag=bm.emmad,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..1.5,limit=1]`;
  const HIT = `@e[type=minecraft:interaction,tag=bm.emmahit,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..1.5,limit=1]`;
  ok('right-clicking the floor sets her down in front of the bot', (await cnt(DOLL)) === 1 && (await cnt(HIT)) === 1);
  ok('...as the doll model', /"bm:emma3d"/.test(await nbt(DOLL, 'item.components."minecraft:item_model"')));
  ok('...and the doll leaves the bot\'s pocket', (await has('TestRat', 'emma_doll')) === 0);

  // ---------------------------------------------------------------- right-click her: she twirls
  const yawOf = async () => +(((await nbt(DOLL, 'Rotation[0]')).match(/(-?[\d.]+)f/) || [0, NaN])[1]);
  const r0 = await yawOf();
  const hit = await entOf(A, HIT);
  A.slot(8); await sleep(250);
  if (hit) A.interact(hit.entityId); await sleep(700);
  const r1 = await yawOf(); const turned = ((r1 - r0) % 360 + 360) % 360;
  ok('right-clicking her: she twirls (a third of a turn)', Math.abs(turned - 120) < 1, `${r0} -> ${r1}`);

  // ---------------------------------------------------------------- her charm: poison within 10 blocks shaken off
  await run('effect give TestRat minecraft:poison 30 0');
  ok('poisoned beside her...', /poison/.test(await nbt('TestRat', 'active_effects')));
  ok('...and her charm cures it within a couple of seconds', await wait(3000, async () => !/poison/.test(await nbt('TestRat', 'active_effects'))));
  ok('(the resistance stays - only harmful effects go)', /resistance/.test(await nbt('TestRat', 'active_effects')));

  // ---------------------------------------------------------------- a plain punch leaves her; sneak + punch picks her up
  if (hit) A.attack(hit.entityId); await sleep(600);
  ok('a plain punch leaves her standing', (await cnt(DOLL)) === 1 && (await has('TestRat', 'emma_doll')) === 0);
  A.input({ shift: true }); await sleep(300); if (hit) A.attack(hit.entityId); await sleep(600); A.input({}); await sleep(300);
  ok('sneak + punch picks her up again', (await cnt(DOLL)) === 0 && (await cnt(HIT)) === 0 && (await has('TestRat', 'emma_doll')) === 1);

  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); R.end(); process.exit(0);
})();

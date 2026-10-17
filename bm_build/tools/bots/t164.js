// 2.79: the Portrait of Two and the mob roll's manners - as a regular (non-op) player, every step a real packet (rcon sets
// the stage: a floor, a wall, the Fence at his stall, the tokens): the Fence sells the portrait (his window opened, its
// trade picked, the painting taken out); used on the wall like any painting - it hangs the portrait (bm:portrait, 5 x 4);
// punched down - it comes back as the portrait, not a random painting. Then the mob roll: twenty named zombies and twenty
// frozen (NoAI) ones are never made Elites or Champions (a name-tagged pet, Wilfrey's body, a statue); plain ones still are.
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
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const X = 16600, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`); await sleep(300);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..24]`);

  // ---------------------------------------------------------------- the Fence sells it: a real trade
  await run(`${O}execute positioned ${X + 0.5} ${Y + 1} ${Z + 4.5} rotated 180 0 run function bm:npc/fence`); await sleep(1200);
  const FEN = `@e[type=minecraft:wandering_trader,tag=bm.npc_fence,x=${X + 0.5},y=${Y + 1},z=${Z + 4.5},distance=..2,limit=1]`;
  let idx = -1;
  for (let i = 0; i < 40 && idx < 0; i++) { const s = await nbt(FEN, `Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`); if (/Found no elements/i.test(s)) break; if (/"portrait_painting"/.test(s)) idx = i; }
  ok('the Fence sells the Portrait of Two', idx >= 0, `trade #${idx}`);
  const price = +(((await nbt(FEN, `Offers.Recipes[${idx}].buy.count`)).match(/(\d+)/) || [0, 0])[1]);
  const buyId = (await nbt(FEN, `Offers.Recipes[${idx}].buy.components."minecraft:custom_data".bm`)).replace(/"/g, '');
  for (let i = 0; i < price; i++) await run(`loot give TestRat loot bm:items/${buyId}`);
  await at(X + 0.5, Y + 1, Z + 2.5, 0, 0);
  const fen = await entOf(FEN); A.windows.length = 0; if (fen) A.interact(fen.entityId); await sleep(900);
  const w = A.windows[A.windows.length - 1];
  ok('right-clicking the Fence opens his trades', !!w);
  if (w && idx >= 0) {
    A.write('select_trade', { slot: idx }); await sleep(300);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(500);
    A.close(w.windowId); await sleep(400);
  }
  ok(`...bought for ${price} ${buyId}: the portrait in the pack, the price gone`, (await has('portrait_painting')) === 1 && (await has(buyId)) === 0);
  const comp = await nbt('TestRat', 'Inventory[{components:{"minecraft:custom_data":{bm:"portrait_painting"}}}]');
  ok('...a painting that carries its picture (painting/variant bm:portrait)', /minecraft:painting/.test(comp) && /bm:portrait/.test(comp), comp.slice(0, 200));
  // (2.82) ...and the Banker's Card, over the same counter: 8 Tokens
  let bdx = -1;
  for (let i = 0; i < 40 && bdx < 0; i++) { const s = await nbt(FEN, `Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`); if (/Found no elements/i.test(s)) break; if (/"bankers_card"/.test(s)) bdx = i; }
  const bprice = bdx < 0 ? 0 : +(((await nbt(FEN, `Offers.Recipes[${bdx}].buy.count`)).match(/(\d+)/) || [0, 0])[1]);
  const bbuy = bdx < 0 ? '' : (await nbt(FEN, `Offers.Recipes[${bdx}].buy.components."minecraft:custom_data".bm`)).replace(/"/g, '');
  ok('(2.82) the Fence sells the Banker\'s Card for 8 Tokens', bdx >= 0 && bprice === 8 && bbuy === 'token', `trade #${bdx}: ${bprice} ${bbuy}`);
  if (bdx >= 0) {
    await run('clear TestRat *[minecraft:custom_data~{bm:"token"}]'); for (let i = 0; i < bprice; i++) await run('loot give TestRat loot bm:items/token');
    A.windows.length = 0; if (fen) A.interact(fen.entityId); await sleep(900);
    const w2 = A.windows[A.windows.length - 1];
    if (w2) { A.write('select_trade', { slot: bdx }); await sleep(300);
      A.write('window_click', { windowId: w2.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(500); A.close(w2.windowId); await sleep(400); }
  }
  ok('...bought in a real trade: the card in the pack, the Tokens gone', (await has('bankers_card')) === 1 && (await has('token')) === 0);
  await run(`${O}kill ${FEN}`);

  // ---------------------------------------------------------------- hung on the wall with a use
  await run(`${O}fill ${X - 6} ${Y + 1} ${Z - 6} ${X + 6} ${Y + 7} ${Z - 6} minecraft:oak_planks`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"portrait_painting"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/portrait_painting');
  await at(X + 0.5, Y + 1, Z - 3.5, 180, -12);            // (facing the wall: north)
  A.slot(0); await sleep(250); A.useOn(X, Y + 3, Z - 6, 3); await sleep(800);     // (a right-click on the wall's south face, as a client sends it)
  const PT = `@e[type=minecraft:painting,x=${X},y=${Y + 3},z=${Z - 5},distance=..6,limit=1]`;
  ok('used on the wall: a painting hangs there, out of the hand', (await cnt(PT)) === 1 && (await has('portrait_painting')) === 0);
  ok('...the Portrait of Two (bm:portrait)', /bm:portrait/.test(await nbt(PT, 'variant')), await nbt(PT, 'variant'));
  // ---------------------------------------------------------------- punched down: back as the portrait
  const pe = await entOf(PT); if (pe) A.attack(pe.entityId); await sleep(900);
  ok('punched down: it comes off the wall', (await cnt(PT)) === 0);
  await sleep(600);
  let drop = await nbt(`@e[type=minecraft:item,x=${X},y=${Y + 2},z=${Z - 5},distance=..12,nbt={Item:{id:"minecraft:painting"}},limit=1]`, 'Item');
  if (/No entity/.test(drop)) drop = 'picked up: ' + await nbt('TestRat', 'Inventory[{id:"minecraft:painting"}]');      // (it may have dropped at the bot's feet)
  ok('...and drops as the portrait again (not a random painting)', /bm:portrait/.test(drop), drop.slice(0, 220));
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y + 2},z=${Z - 5},distance=..8]`);

  // ---------------------------------------------------------------- the mob roll leaves named and frozen mobs be
  const named = async (tag) => { await run(`${O}execute as @e[type=minecraft:zombie,tag=${tag}] if data entity @s CustomName run tag @s add t164r`);
    const n = await cnt(`@e[type=minecraft:zombie,tag=${tag},tag=t164r]`); await run(`${O}tag @e[tag=t164r] remove t164r`); return n; };
  const mk = async (tag, nbtx) => { for (let i = 0; i < 20; i++) await run(`${O}summon minecraft:zombie ${X - 8 + (i % 5) * 2} ${Y + 1} ${Z + 6 + Math.floor(i / 5)} {PersistenceRequired:1b,Silent:1b,Tags:["${tag}"],attributes:[{id:"minecraft:movement_speed",base:0.0d}]${nbtx}}`); };
  await run(`${O}fill ${X - 9} ${Y + 1} ${Z + 5} ${X + 9} ${Y + 4} ${Z + 10} minecraft:air`);
  await mk('t164n', ',CustomName:{text:"Rex"}'); await sleep(2600);                 // (named, like a name-tagged pet or Wilfrey's body)
  const seenN = await cnt('@e[type=minecraft:zombie,tag=t164n,tag=bm.seen]'), rexN = await cnt('@e[type=minecraft:zombie,tag=t164n,nbt={CustomName:"Rex"}]');
  ok('twenty named zombies: seen by the roll, and every one still "Rex"', seenN === 20 && rexN === 20, `seen ${seenN}, Rex ${rexN}`);
  await run(`${O}kill @e[type=minecraft:zombie,tag=t164n]`);
  await mk('t164f', ',NoAI:1b'); await sleep(2600);                                  // (frozen, unnamed: a statue)
  const seenF = await cnt('@e[type=minecraft:zombie,tag=t164f,tag=bm.seen]'), namedF = await named('t164f');
  ok('twenty frozen (NoAI) zombies: seen, none renamed', seenF === 20 && namedF === 0, `seen ${seenF}, renamed ${namedF}`);
  await run(`${O}kill @e[type=minecraft:zombie,tag=t164f]`);
  // (plain: some are rolled - about 7 in 100; two hundred, so at least a few)
  for (let i = 0; i < 200; i++) await run(`${O}summon minecraft:zombie ${X - 8 + (i % 10) * 1.6} ${Y + 1} ${Z + 6 + Math.floor(i / 10) % 4} {PersistenceRequired:1b,Silent:1b,Tags:["t164p"],attributes:[{id:"minecraft:movement_speed",base:0.0d}]}`);
  await sleep(2600);
  const rolled = await named('t164p');
  ok('two hundred plain zombies: the roll still names some (Elite / Champion / Lucky)', rolled >= 3, `${rolled} rolled`);
  await run(`${O}kill @e[type=minecraft:zombie,tag=t164p]`);

  await run('clear TestRat'); await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

// 2.82b: FINDING YOUR WAY, PROTECTED GROUND, AND SAVINGS - in the rat town, as a regular (non-op) player, every step a real packet
// (rcon sets the stage: t162's market, rebuilt into the current town if it's older; the Market Key and a Banker's Card).
//   THE TOWN DIRECTORY: a board on the Lookout and four more about the town; right-clicked, WHO'S WHERE (every trader and place,
//   never the Captain); "Old Barnaby" pressed - a guide marker at his shop, his name on the action bar; walked to him - "You're
//   there", and the guide gone.
//   PROTECTED GROUND: stood on the shop floors, docks, stairs and the Lookout's rock (not the streets): adventure mode each time;
//   out of the market: survival again.
//   SAVINGS: away from the Teller (the Banker's Card), "Savings account" says only the Teller opens one; at the Teller in the
//   Gilded Gutter: opened. Two days later, 100 Tokens and 30 Medallions in the account: 4 + 4 Tokens, 1 + 1 Medallions paid in.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const passes = async c => /passed/i.test(await run(c));
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const sc = async (o) => +((await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const click = async (sel, ms = 900) => { let e = null; await wait(3000, async () => !!(e = await entOf(sel))); if (!e) return false; A.interact(e.entityId); await sleep(ms); return true; };
  const dlg = () => JSON.stringify(A.dialogN.slice(-1)[0] || '');
  const CX = 24000, CY = 30, CZ = 24000, W = 10, BF = 17;
  const T = (x, y, z) => [CX + x, CY + y, CZ + z];
  const at = async (x, y, z, yaw = 0) => { const [a, b, c] = T(x, y, z); await run(`${O}tp TestRat ${a} ${b} ${c} ${yaw} 0`);
    await wait(2500, async () => A.pos && Math.abs(A.pos.x - a) < 0.1 && Math.abs(A.pos.z - c) < 0.1, 100); await sleep(400); };
  const gm = async () => ((await run('data get entity TestRat playerGameType')).match(/: (\d+)/) || [0, -1])[1];
  const BOX = `x=${CX - 4},y=${CY - 4},z=${CZ - 4},dx=84,dy=40,dz=104`;

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run('loot replace entity TestRat hotbar.8 loot bm:items/market_key');
  for (const o of ['bm.bksv', 'bm.bkday', 'bm.bkint', 'bm.dirt', 'bm.dirs']) await run(`execute as TestRat run scoreboard players reset @s ${o}`);

  // ---- the stage: the market (rebuilt into the current town on the way in if it's an old one)
  await run(`${O}forceload add ${CX - 16} ${CZ - 16} ${CX + 127} ${CZ + 127}`);
  const MK = `@e[type=minecraft:marker,tag=bm.mkt,x=${CX + 38.5},y=${CY + 12},z=${CZ + 46.5},distance=..2,limit=1]`;
  await sleep(2500);
  if (!(await passes(`${O}execute if entity ${MK}`))) {
    for (let t = 0; t < 30; t++) { const pl = await run(`${O}place template bm:black_market ${CX} ${CY} ${CZ}`); if (!/not loaded/.test(pl)) break; await sleep(2000); }
  }
  await at(38.5, BF + 1, 79.5, 180);
  ok('the market is the current town (bm.m282b)', await wait(40000, async () => passes(`${O}execute if entity ${MK.replace(',limit=1', ',tag=bm.m282b,limit=1')}`), 500));
  await run(`${O}tag ${MK} remove bm.dir282`);                       // (the boards put up afresh for this run - as a new town gets them)
  await wait(15000, async () => (await cnt(`@e[type=minecraft:interaction,tag=bm.dirb,${BOX}]`)) === 5, 500);
  await sleep(1500);

  // ---- the Town Directory
  ok('five Town Directory boards about the town (the Lookout, the Plaza, the Wharf, Furnace Row, Night Alley)', (await cnt(`@e[type=minecraft:interaction,tag=bm.dirb,${BOX}]`)) === 5);
  const board = `@e[type=minecraft:interaction,tag=bm.dirb,x=${CX + 31.5},y=${CY + BF + 1},z=${CZ + 79.5},distance=..1.5,limit=1]`;
  await at(33.5, BF + 1, 79.5, 90);
  const n0 = A.dialogN.length; await click(board, 1200);
  const labels = A.buttons().map(b => b.label);
  ok('the Lookout\'s board, right-clicked: WHO\'S WHERE - every trader and place (21), and no Captain', A.dialogN.length > n0 && /WHO'S WHERE/.test(dlg()) && labels.length === 21 &&
     ['Old Barnaby', 'The Fence', 'Chef Fromage', 'Lucky Whiskers', 'Dennis', 'Pistachio', 'Cecil', "Fishy's Cabinet", 'The way out'].every(l => labels.includes(l)) &&
     !labels.some(l => /Cheddarbeard|Captain/.test(l)), labels.join(' | ').slice(0, 300));
  A.bars.length = 0;
  await A.press(/^Old Barnaby$/); await sleep(1200);
  const guide = '@e[type=minecraft:marker,tag=bm.dirm]';
  ok('"Old Barnaby": a guide to his shop - its marker by his counter, his name on the action bar', (await cnt(guide)) === 1 && (await sc('bm.dirt')) === 1 &&
     (await passes(`${O}execute if entity @e[type=minecraft:marker,tag=bm.dirm,x=${CX + 29.5},y=${CY + W},z=${CZ + 20.5},distance=..3]`)) && A.bars.some(b => /Old Barnaby/.test(b)),
     A.bars.slice(-1).join(''));
  ok('...and it follows you about (the action bar still names him, on the way)', await wait(3000, async () => { A.bars.length = 0; await sleep(600); return A.bars.some(b => /Old Barnaby.*(follow the light|close by|just ahead)/.test(b)); }),
     A.bars.slice(-1).join(''));
  A.bars.length = 0;
  await at(31.5, W, 21.5, 90);
  ok('...walked up to him: "You\'re there", and the guide is gone', await wait(4000, async () => A.bars.some(b => /You're there/.test(b))) && (await cnt(guide)) === 0 && (await sc('bm.dirt')) === 0,
     A.bars.slice(-1).join(''));

  // ---- protected ground: adventure on every floor the town has, not just its streets
  const spots = [['the Lookout\'s rock', 30.5, BF + 1, 73.5], ['the dock house planks', 9.5, W, 26.5], ['a shop\'s floor (Barnaby\'s)', 31.5, W, 21.5],
                 ['the Assay Office (Dennis)', 34.5, W, 78.5]];
  let advOk = 0, advLog = [];
  for (const [nm, x, y, z] of spots) {
    await run(`${O}tp TestRat ${CX + 38.5} ${CY + 60} ${CZ - 30}`); await sleep(1500); await run('gamemode survival TestRat'); await sleep(800);
    await at(x, y, z, 0); const got = await wait(4000, async () => (await gm()) === '2', 250);
    if (got) advOk++; advLog.push(`${nm}: ${got ? 'adventure' : 'gamemode ' + (await gm())}`);
  }
  ok('stood on the Lookout\'s rock, the dock house, a shop floor and the Assay Office: adventure mode each time', advOk === spots.length, advLog.join('; '));
  await run(`${O}tp TestRat ${CX + 38.5} ${CY + 60} ${CZ - 60}`);
  ok('...and out of the market: survival again', await wait(4000, async () => (await gm()) === '0', 250));

  // ---- savings: opened at the Teller only; then paid every day
  await run('loot replace entity TestRat hotbar.1 loot bm:items/bankers_card');
  await at(38.5, W, 40.5, 0);
  A.slot(1); await sleep(400); A.bars.length = 0; await A.useWait();
  const opened = /Rat Bank/.test(dlg());
  await A.press(/^Savings account$/); await sleep(800);
  ok('the bank by Banker\'s Card: "Savings account" - opened in person only, at the Teller', opened && (await sc('bm.bksv')) <= 0 && A.bars.some(b => /opened in person/.test(b)),
     A.bars.slice(-1).join(''));
  const teller = `@e[type=minecraft:interaction,tag=bm.ledger,scores={bm.lgid=42},${BOX},limit=1]`;
  await run(`${O}execute as ${teller} at @s run tp TestRat ^ ^ ^1.5 facing entity @s`); await sleep(1500);
  A.chats.length = 0; const n1 = A.dialogN.length; await click(teller, 1500);
  ok('...at the Teller, in the Gilded Gutter: the bank opens', A.dialogN.length > n1 && /Rat Bank/.test(dlg()) && /Savings: none yet/.test(dlg()), dlg().slice(0, 120));
  await A.press(/^Savings account$/); await sleep(1000);
  ok('..."Savings account": opened - the Teller says how it works, and the savings page shows it', (await sc('bm.bksv')) === 1 && A.chats.some(c => /A savings account, then/.test(c)) &&
     /Savings/.test(dlg()) && /1 a day for every 25 kept/.test(dlg()), A.chats.slice(-1).join('').slice(0, 120));
  await run('scoreboard players set TestRat bm.bk_tok 100'); await run('scoreboard players set TestRat bm.bk_med 30');
  await run('execute as TestRat run scoreboard players operation @s bm.bkday = #day bm.bm'); await run('scoreboard players remove TestRat bm.bkday 2');
  A.chats.length = 0;
  ok('two days on: interest paid in - 4 Tokens and 1 Medallion a day (1 in 25), both days', await wait(4000, async () => (await sc('bm.bk_tok')) === 108) &&
     (await sc('bm.bk_med')) === 32 && (await sc('bm.bkint')) === 10 && A.chats.some(c => /savings earned interest/.test(c)) && A.chats.some(c => /\+8 Tokens/.test(c)),
     `tokens ${await sc('bm.bk_tok')}, medallions ${await sc('bm.bk_med')}, total ${await sc('bm.bkint')}; ${A.chats.slice(-3).join(' | ').slice(0, 160)}`);
  await run('scoreboard players set TestRat bm.bk_tok 1000');
  await run('execute as TestRat run scoreboard players operation @s bm.bkday = #day bm.bm'); await run('scoreboard players remove TestRat bm.bkday 1');
  ok('...a big balance is capped: 8 Tokens a day at most', await wait(4000, async () => (await sc('bm.bk_tok')) === 1008), `tokens ${await sc('bm.bk_tok')}`);

  // ---- clean up
  for (const o of ['bm.bksv', 'bm.bkday', 'bm.bkint']) await run(`execute as TestRat run scoreboard players reset @s ${o}`);
  await run('scoreboard players set TestRat bm.bk_tok 0'); await run('scoreboard players set TestRat bm.bk_med 0');
  await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode survival TestRat');
  await run(`${O}forceload remove ${CX - 16} ${CZ - 16} ${CX + 127} ${CZ + 127}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

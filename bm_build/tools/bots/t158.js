// 2.78: the Recruiter deals in the two new names too - as a regular (non-op) player in the Lounge (in with the Ledger, as t145):
// Apophiss and Tullius aren't on his book until you've met them (their Oath, their coin in your pocket); then their Raid
// Contracts are, priced in coins - bought from the book (the button the client got), used as items, and "SIGNED".
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const dim = async () => (await run('data get entity TestRat Dimension')).replace(/.*data: /, '');
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const labels = () => A.buttons().map(b => b.label.replace(/[^\x20-\x7e]/g, '').replace(/\s+/g, ' ').trim());
  const shown = () => JSON.stringify(A.dialogN[A.dialogN.length - 1] || {});
  const uuidStr = async (sel) => { const m = (await run(`execute in bm:gutter run data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const O = 'execute in minecraft:overworld run ';
  const HX = 13000, HY = 121, HZ = 13000;
  const KINDS = ['cecil', 'emma', 'celi', 'zib', 'killerwatt', 'leo', 'demo', 'escort', 'apo', 'tul', 'frog', 'donado', 'fishy', 'dennis', 'pistachio', 'omega', 'ashur', 'chef', 'neighbor', 'ava', 'pearlq', 'bloo', 'stalker', 'lantern', 'bender', 'bones', 'capshun', 'sky', 'pxemma', 'pxleo', 'pxcecil', 'kettle', 'rufus', 'henry', 'nia', 'gem', 'batty', 'eggbert', 'count', 'dragon', 'eraser', 'cursor', 'inkblot', 'speech', 'lightbringer', 'dryad', 'sovereign', 'vexis', 'mireling', 'keeper'];
  const A = await bot('TestRat'); await sleep(2500);
  // ---- the stage: a newcomer to the vault who has met no one
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run(`${O}forceload add ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
  await run(`${O}fill ${HX - 4} ${HY - 1} ${HZ - 4} ${HX + 4} ${HY - 1} ${HZ + 4} minecraft:stone`);
  await run(`${O}fill ${HX - 4} ${HY} ${HZ - 4} ${HX + 4} ${HY + 3} ${HZ + 4} minecraft:air`);
  await run(`${O}tp TestRat ${HX + 0.5} ${HY} ${HZ + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  for (const t of ['bm.gvp', 'bm.gvask', 'bm.gvnext', 'bm.gvoffer', 'bm.gvwaitd', 'bm.lgch', 'bm.lkch']) await run(`tag TestRat remove ${t}`);
  for (const k of KINDS) await run(`advancement revoke TestRat only bm:met/${k}`);
  await run('scoreboard players set TestRat bm.fcon 0'); await run('scoreboard players set TestRat bm.crew 0'); await run('scoreboard players set TestRat bm.gvhr 0'); await run('scoreboard players set TestRat bm.gbc 3000');
  await run('loot give TestRat loot bm:items/fixers_ledger');
  await sleep(1500); A.stand(); await sleep(500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player (no operator commands)', /unknown|incomplete|permission/i.test(A.chats.join(' ')), A.chats.slice(-1).join('').slice(0, 120));

  // ---- into the Lounge the way a player goes: the Ledger, the Office, "The Fixer's Lounge", stand still
  A.slot(0); await sleep(300); await A.useWait();
  A.click(/Fixer's Lounge/); await wait(8000, async () => /gutter/.test(await dim())); await sleep(2500); A.stand();
  ok('Into the Fixer\'s Lounge with the Ledger', /gutter/.test(await dim()));
  const hit = '@e[type=minecraft:interaction,tag=bm.rechit,x=-321,y=60,z=-257,dx=26,dy=20,dz=26,limit=1]';
  ok('The Recruiter has a counter to click (his old trades replaced by his book)', await wait(3000, async () => /passed/.test(await run(`execute in bm:gutter if entity ${hit}`))));
  const trades = await run('execute in bm:gutter run data get entity @e[type=minecraft:villager,tag=bm.gvrec,x=-321,y=60,z=-257,dx=26,dy=20,dz=26,limit=1] Offers.Recipes');
  ok('...and his villager sells nothing any more', /\[\]|Found no elements/.test(trades), trades.replace(/.*data: /, '').slice(0, 80));
  await run(`execute in bm:gutter at ${hit} rotated 0 0 positioned ^ ^ ^-1.6 run tp TestRat ~ ~ ~ 0 0`); await sleep(1500);
  const eu = await uuidStr(hit); const ent = Object.values(A.ents).find(e => e.objectUUID === eu);
  const open = async () => { const n0 = A.dialogN.length; A.interact(ent.entityId); await wait(2500, async () => A.dialogN.length > n0, 100); await sleep(200); };
  ok('(the bot sees his counter)', !!ent);

  // ---- Apophiss and Tullius: met (their summoning items in your pocket), their contracts on his book; bought, used, SIGNED
  for (const [who, iid, met, con] of [['Apophiss', 'apo_oath', 'apo', 'fcontract_apo'], ['Tullius', 'tul_coin', 'tul', 'fcontract_tul']]) {
    await open();
    ok(`[${who}] before you've met them: not on his book`, !labels().some(l => new RegExp('^' + who + ' ').test(l)), labels().join(' | '));
    await run(`loot replace entity TestRat hotbar.4 loot bm:items/${iid}`);
    ok(`[${who}] holding their item: you've met them (bm:met/${met})`, await wait(3000, async () => /passed/.test(await run(`execute if entity @a[name=TestRat,advancements={bm:met/${met}=true}]`))));
    await open();
    console.log('   [book] ' + labels().join(' | '));
    const row = labels().find(l => new RegExp('^' + who + ' ').test(l));
    ok(`[${who}] his book now has their contract, priced in coins`, !!row && /\d+ coins/.test(row), row);
    const price = +((row || '').match(/(\d+) coins/) || [0, 0])[1];
    const bank0 = await sc('TestRat', 'bm.gbc');
    const pr = await A.press(new RegExp('^' + who + ' '));
    ok(`[${who}] pressed: paid, and Raid Contract: ${who} in hand`, (await has(con)) === 1 && (await sc('TestRat', 'bm.gbc')) === bank0 - price, `${bank0} -> ${await sc('TestRat', 'bm.gbc')} (price ${price})`);
    ok(`[${who}] ...the book: "IN YOUR PACK"`, !!pr && pr.next && labels().some(l => new RegExp('^' + who + ' IN YOUR PACK').test(l)), labels().join(' | '));
    const cs = +(((await run(`data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"${con}"}}}].Slot`)).match(/(\d+)b?\s*$/) || [0, -1])[1]);
    if (cs !== 5) await run(`item replace entity TestRat hotbar.5 from entity TestRat container.${cs}`), await run(`item replace entity TestRat container.${cs} with minecraft:air`);
    const f0 = await sc('TestRat', 'bm.fcon');
    A.chats.length = 0; A.slot(5); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(900);
    ok(`[${who}] use the contract: signed for the vault`, (await sc('TestRat', 'bm.fcon')) > f0 && (await has(con)) === 0, A.chats.slice(-1).join('').slice(0, 120));
    await open();
    ok(`[${who}] ...the book: "SIGNED"`, labels().some(l => new RegExp('^' + who + ' SIGNED').test(l)), labels().join(' | '));
    await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}]`);
  }

  // ---- the stage put back
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.fcon 0'); await run('scoreboard players set TestRat bm.crew 0'); await run('scoreboard players set TestRat bm.gbc 0');
  await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.lgexit,limit=1] at @s run tp TestRat ~ ~ ~'); await sleep(2000);
  await run(`${O}forceload remove ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); R.end(); process.exit(0);
})();

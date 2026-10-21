// 2.84a: VESPER, THE DREAD BROKER, and DREAD TOKENS - as a regular (non-op) player. (The test server keeps hard mode off -
// #hardoff 1 - so rcon turns it on for the stage, and off again at the end.)
//   Vesper: in the red-and-white stall on the plaza of t162's market only while hard mode is on; his Ledger (the book on his counter).
//   trading: 10 Trophies -> 2 Dread Tokens at his window (5 a token, exact - not the market's discount).
//   the Rat Bank: Dread Tokens kept like a currency; the Exchange swaps 5 banked Trophies for one; the savings page pays 2%.
//   the Ledger: Ward I for the followers (paid from the pockets, then the bank) - and on a follower of the player's, the armour
//     shows; Swift Return I cuts a faint's rest to 80 s; tuning the sword in hand twice (Attack Damage) and unbinding it all
//     for every token back; reforging Hero of Time's Tunic into the Fierce Deity's.
//   his goods: the Auctioneer's Writ owes a Dark Auction tonight; the Tome of Eternity makes the off hand unbreakable; the
//     Dread Compass points at a Dread zombie; the Bottomless Bucket pours and fills itself again; the Echo of the Hollow King
//     steps a Hollow King conqueror's record back to 5.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const passes = async c => /passed/i.test(await run(c));
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const has = async id => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const hand = async (slot = 'SelectedItem') => run(`data get entity TestRat ${slot}`);
  const O = 'execute in minecraft:overworld run ';
  const uuidEnt = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(400); A.stand(); };
  const press = async (re) => { const b = await A.press(re); await sleep(700); return b; };
  const hold = async (ms) => { A.use(); await sleep(ms); A.release(); await sleep(600); };       // (a consumable: held down for its time)
  // (t162's market: template (x, y, z) is the world's (CX + x, CY + y, CZ + z))
  const CX = 24000, CY = 30, CZ = 24000, W = 10;
  const VX = CX + 53.5, VY = CY + W, VZ = CZ + 51.5;                  // Vesper's spot; his Ledger on the counter, a block south-west of him
  const VES = `@e[type=minecraft:villager,tag=bm.vesper,x=${VX},y=${VY},z=${VZ},distance=..3,limit=1]`;
  const LED = `@e[type=minecraft:interaction,tag=bm.vledger,x=${VX - 1},y=${VY + 1},z=${VZ + 1},distance=..2,limit=1]`;
  const saved = { owed: await sc('#owed', 'bm.auc'), conq: await sc('TestRat', 'bm.conq') };

  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run(`${O}forceload add ${CX + 16} ${CZ + 8} ${CX + 72} ${CZ + 64}`);
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  // (a member of the market - its key in the pack, or the rat bouncer tosses a survival player out - and the Banker's Card)
  await run('loot replace entity TestRat hotbar.8 loot bm:items/market_key'); await run('loot replace entity TestRat hotbar.7 loot bm:items/bankers_card');
  for (const o of ['bm.fward', 'bm.fvig', 'bm.fret', 'bm.bk_dread', 'bm.bk_tro']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('scoreboard players set TestRat bm.conq 6');           // (2.84d: his trades are only for those who beat the Hollow King)
  await at(VX, VY, VZ + 2.5, 180, 10);

  // ================================================================== 1. Vesper comes with hard mode
  await run('scoreboard players set #hard bm.cfg 1');
  ok('Hard mode on: Vesper stands in the stall', await wait(25000, async () => passes(`${O}execute if entity ${VES}`), 500));
  ok('...and his Ledger lies on the counter in front of him', await wait(5000, async () => passes(`${O}execute if entity ${LED}`)));
  ok('...named Vesper, the Dread Broker', /Vesper/.test(await run(`${O}data get entity ${VES} CustomName`)));

  // ================================================================== 2. his window: 10 Trophies -> 2 Dread Tokens
  for (let i = 0; i < 10; i++) await run('loot give TestRat loot bm:items/trophy');
  await sleep(500);
  const vEid = await uuidEnt(VES);
  A.windows.length = 0; A.interact(vEid); await sleep(1200);
  const w = A.windows[A.windows.length - 1];
  ok('Right-clicking Vesper opens his trades', !!w);
  if (w) {
    A.write('select_trade', { slot: 0 }); await sleep(400);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(800);
    A.close(w.windowId); await sleep(500);
  }
  ok('...his first trade: 5 Trophies a Dread Token - 10 make exactly 2', (await has('dread_token')) === 2 && (await has('trophy')) === 0,
     `${await has('dread_token')} tokens, ${await has('trophy')} trophies left`);

  // ================================================================== 3. the Rat Bank keeps them
  await run('scoreboard players set TestRat bm.bk_tro 5');
  A.slot(7); await sleep(300); await A.useWait(2500);
  ok('The Banker\'s Card opens the Rat Bank: it lists Dread Tokens', A.buttons().some(b => /Dread Tokens/.test(b.label)), A.buttons().map(b => b.label).join(' | ').slice(0, 300));
  await press(/^Exchange/);
  await press(/5 Trophies.*1 Dread Token/);
  ok('...its Exchange: 5 banked Trophies become a banked Dread Token', (await sc('TestRat', 'bm.bk_dread')) === 1 && (await sc('TestRat', 'bm.bk_tro')) === 0,
     `${await sc('TestRat', 'bm.bk_dread')} dread, ${await sc('TestRat', 'bm.bk_tro')} trophies`);
  await press(/Your account/); await press(/Savings account/);
  ok('...and the savings page pays 2% on them (1 a day for every 50), 2 a day at most', /every 50 kept \(up to 2 a day\)/.test(JSON.stringify(A.dialogN[A.dialogN.length - 1] || '')),
     JSON.stringify(A.dialogN[A.dialogN.length - 1] || '').match(/.{0,60}Dread.{0,80}/) + '');
  A.cmd('trigger bm.act set 2'); await sleep(400);

  // ================================================================== 4. the Ledger
  const lEid = await uuidEnt(LED);
  A.dialogN.length = 0; A.interact(lEid); await sleep(1200);
  ok('Right-clicking the book on his counter opens Vesper\'s Ledger (3 Dread Tokens: 2 in hand, 1 banked)',
     A.buttons().some(b => /Followers' Wards/.test(b.label)) && /\b3\b/.test(JSON.stringify(A.dialogN[A.dialogN.length - 1] || '')),
     `eid ${lEid} at ${(await run('data get entity TestRat Pos')).replace(/.*data: /, '')} | ${A.buttons().map(b => b.label).join(' | ').slice(0, 160)}`);
  await press(/Followers' Wards/);
  await press(/Ward \+1/);
  ok('Ward I for 3 tokens - both in hand, then the banked one', (await sc('TestRat', 'bm.fward')) === 1 && (await has('dread_token')) === 0 && (await sc('TestRat', 'bm.bk_dread')) === 0,
     `ward ${await sc('TestRat', 'bm.fward')}, ${await has('dread_token')} in hand, ${await sc('TestRat', 'bm.bk_dread')} banked`);
  // (a follower of the player's: a stand-in host with the player's id - the second loop finds it like any wolf follower)
  const pid = await sc('TestRat', 'bm.pid');
  await run(`${O}summon minecraft:wolf ${VX + 3} ${VY} ${VZ + 4} {Tags:["bm.cecilpet","bm.t224"],NoAI:1b,Silent:1b,PersistenceRequired:1b}`);
  await run(`${O}scoreboard players set @e[type=minecraft:wolf,tag=bm.t224,limit=1] bm.pid ${pid}`);
  ok('...a follower of the player\'s takes the ward (+3 armour)', await wait(4000, async () => (+((await run(`${O}attribute @e[type=minecraft:wolf,tag=bm.t224,limit=1] minecraft:armor get`)).match(/(-?[\d.]+)(?!.*\d)/) || [0, 0])[1]) >= 3),
     await run(`${O}attribute @e[type=minecraft:wolf,tag=bm.t224,limit=1] minecraft:armor get`));
  await run(`${O}kill @e[type=minecraft:wolf,tag=bm.t224]`);
  await run('scoreboard players set TestRat bm.bk_dread 20');
  await press(/Swift Return \+1/);
  await run('scoreboard players set TestRat bm.cpcd 120');
  ok('Swift Return I: a faint rests 80 seconds, not 120', (await sc('TestRat', 'bm.fret')) === 1 && await wait(2500, async () => (await sc('TestRat', 'bm.cpcd')) <= 80),
     `ret ${await sc('TestRat', 'bm.fret')}, cd ${await sc('TestRat', 'bm.cpcd')}`);
  await run('scoreboard players set TestRat bm.cpcd 0');
  await press(/The Ledger/);

  // ---- tuning the sword in hand
  await run('item replace entity TestRat hotbar.0 with minecraft:diamond_sword'); A.slot(0); await sleep(400);
  await press(/^Tuning/);
  ok('Tuning, with a sword in hand: the weapon page', A.buttons().some(b => /Attack Damage/.test(b.label)), A.buttons().map(b => b.label).join(' | ').slice(0, 200));
  await press(/Attack Damage/); await press(/Attack Damage/);
  const tuned = await hand();
  ok('...Attack Damage twice: two tunings on the sword, 2 tokens paid', /bm:tune_dmg_1/.test(tuned) && /bm:tune_dmg_2/.test(tuned) && /bm_tune: \{[^}]*n: 2/.test(tuned) && (await sc('TestRat', 'bm.bk_dread')) === 15,
     `${(tuned.match(/bm_tune: \{[^}]*\}/) || [''])[0]} bank ${await sc('TestRat', 'bm.bk_dread')}`);
  await press(/Unbind all/);
  const unb = await hand();
  ok('...unbound: the tunings gone, the sword still a sword, and the 2 tokens back in hand', /diamond_sword/.test(unb) && !/bm:tune_/.test(unb) && !/bm_tune/.test(unb) && (await has('dread_token')) === 2,
     `${unb.slice(0, 160)} / ${await has('dread_token')} tokens`);
  await press(/The Ledger/);

  // ---- reforging Hero of Time's Tunic
  await run('loot replace entity TestRat hotbar.0 loot bm:items/hero_chestplate'); await sleep(300);
  await press(/^Reforging/);
  await press(/Reforge what I hold/);
  ok('Reforging the Hero of Time\'s Tunic: the Fierce Deity\'s in hand, 4 tokens paid (2 in hand first)', /deity_chestplate/.test(await hand()) && (await has('dread_token')) === 0 && (await sc('TestRat', 'bm.bk_dread')) === 13,
     `${((await hand()).match(/bm: "([a-z_]+)"/) || [])[1]} / ${await has('dread_token')} in hand, ${await sc('TestRat', 'bm.bk_dread')} banked`);
  ok('...and it still counts toward the Hero of Time set (bm_up)', /bm_up: "hero"/.test(await hand()));
  A.cmd('trigger bm.act set 2'); await sleep(400);

  // ================================================================== 5. his goods (on a stone pad out of town)
  const X = 13480, Y = 121, Z = 13400;
  await run(`${O}forceload add ${X - 32} ${Z - 16} ${X + 32} ${Z + 16}`);
  await run(`${O}fill ${X - 4} ${Y - 1} ${Z - 4} ${X + 30} ${Y - 1} ${Z + 6} minecraft:stone`);
  await run(`${O}fill ${X - 4} ${Y} ${Z - 4} ${X + 30} ${Y + 4} ${Z + 6} minecraft:air`);
  await at(X + 0.5, Y, Z + 0.5, 0, 0); await run('gamemode survival TestRat');
  // ---- the Auctioneer's Writ
  if ((await sc('#state', 'bm.auc')) !== 0) { await run('function bm:p30/abort'); await sleep(500); }     // (the stage: no auction sitting)
  await run('scoreboard players set #owed bm.auc 0'); await run('scoreboard players set #saled bm.auc -1');
  const st = await sc('#state', 'bm.auc');
  await run('loot replace entity TestRat hotbar.1 loot bm:items/auction_writ'); A.slot(1); await sleep(400);
  A.bars.length = 0; A.chats.length = 0; await hold(1700);
  // (owed tonight - or, past dusk already, its doors open at once: the scheduler takes the debt the same second)
  const owed = await sc('#owed', 'bm.auc'), st2 = await sc('#state', 'bm.auc');
  ok(st === 0 ? 'The Auctioneer\'s Writ: a Dark Auction is owed tonight (writ used up)' : 'The Auctioneer\'s Writ (an auction already sitting: refused and returned)',
     st === 0 ? (owed === 1 || st2 >= 1) && (await has('auction_writ')) === 0 && A.chats.some(c => /writ has been served/i.test(c)) : (await has('auction_writ')) === 1,
     `state ${st}->${st2}, owed ${owed} | ${A.bars.concat(A.chats).slice(-2).join(' / ').slice(0, 160)}`);
  // ---- the Tome of Eternity
  await run('item replace entity TestRat weapon.offhand with minecraft:iron_pickaxe');
  await run('loot replace entity TestRat hotbar.2 loot bm:items/tome_eternity'); A.slot(2); await sleep(400);
  await hold(2400);
  ok('The Tome of Eternity: the pickaxe in the off hand is unbreakable now', /unbreakable/.test(await hand('equipment.offhand')) && (await has('tome_eternity')) === 0, (await hand('equipment.offhand')).slice(0, 160));
  // ---- the Dread Compass
  await run(`${O}summon minecraft:zombie ${X + 24.5} ${Y} ${Z + 0.5} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["bm.seen","bm.t224"]}`);
  await run(`${O}execute as @e[type=minecraft:zombie,tag=bm.t224] run function bm:p176/mk/zombie`);
  await run('loot replace entity TestRat hotbar.3 loot bm:items/dread_compass'); A.bars.length = 0; A.slot(3);
  ok('The Dread Compass, held: the needle points east at the Dread zombie', await wait(3000, async () => A.bars.some(b => /shivers\s*east/.test(b))), A.bars.slice(-1).join(''));
  await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t224]`); await run(`${O}kill @e[type=minecraft:item,x=${X + 24},y=${Y},z=${Z},distance=..4]`);
  // ---- the Bottomless Bucket (poured onto the square in front of the stall)
  await run('loot replace entity TestRat hotbar.4 loot bm:items/bottomless_bucket'); A.slot(4); await sleep(400);
  const bx = X, by = Y - 1, bz = Z + 2;
  await run(`${O}setblock ${bx} ${by + 1} ${bz} minecraft:air`);
  await at(X + 0.5, Y, Z + 0.5, 0, 45);                // (a bucket pours where you look: down at the floor two blocks ahead)
  A.use(); await sleep(250); A.release(); await sleep(700);
  ok('The Bottomless Bucket pours - and is full again in hand', (await passes(`${O}execute if block ${bx} ${by + 1} ${bz} minecraft:water`)) && /bottomless_bucket/.test(await hand()),
     `${((await hand()).match(/id: "([a-z_:]+)"/) || [])[1]}`);
  await run(`${O}setblock ${bx} ${by + 1} ${bz} minecraft:air`);
  // ---- the Echo of the Hollow King
  await run('scoreboard players set TestRat bm.conq 6');
  await run('loot replace entity TestRat hotbar.5 loot bm:items/hollow_echo'); A.slot(5); await sleep(400);
  await hold(2000);
  ok('The Echo of the Hollow King: a conqueror\'s record steps back to 5 (the King waits again)', (await sc('TestRat', 'bm.conq')) === 5 && (await has('hollow_echo')) === 0, `${await sc('TestRat', 'bm.conq')}`);

  // ================================================================== 6. (2.84d) the record stepped back: his wares veiled, his Ledger shut
  await at(VX, VY, VZ + 2.5, 180, 10);
  const veiled = async () => passes(`${O}execute if data entity ${VES} Offers.Recipes[{maxUses:0,sell:{id:"minecraft:paper"}}]`);
  ok('Back at the stall with conquest 5: every one of Vesper\'s trades is veiled', await wait(4000, veiled) &&
     !(await passes(`${O}execute if data entity ${VES} Offers.Recipes[1]`)), (await run(`${O}data get entity ${VES} Offers.Recipes[0].sell.id`)).slice(-60));
  A.chats.length = 0; A.interact(await uuidEnt(LED)); await sleep(1200);
  ok('...and his Ledger says no: it is for those who felled the Hollow King', /felled the Hollow King/.test(A.chats.join(' ')), A.chats.join(' | ').slice(-160));
  await run('scoreboard players set TestRat bm.conq 6');
  ok('...the King beaten again (conquest 6): the trades are back', await wait(4000, async () => !(await veiled()) &&
     await passes(`${O}execute if data entity ${VES} Offers.Recipes[{sell:{components:{"minecraft:custom_data":{bm:"dread_token"}}}}]`)));

  // ================================================================== 7. hard mode off: he goes
  await run('scoreboard players set #hard bm.cfg 0');
  ok('Hard mode off: Vesper and his Ledger are gone', await wait(25000, async () => !(await passes(`${O}execute if entity ${VES.replace(',distance=..3', ',distance=..4')}`)) &&
     !(await passes(`${O}execute if entity ${LED}`)), 500));

  // ---- put things back
  await run(`scoreboard players set #owed bm.auc ${isNaN(saved.owed) ? 0 : saved.owed}`); await run(`scoreboard players set TestRat bm.conq ${isNaN(saved.conq) ? 6 : saved.conq}`);
  for (const o of ['bm.fward', 'bm.fvig', 'bm.fret', 'bm.bk_dread']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('clear TestRat'); await run('gamemode creative TestRat');
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

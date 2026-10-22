// 2.85a: A DREAD NIGHT - as a regular player who has beaten the Hollow King (rcon sets the stage: hard mode, the record, the hour).
//   Vesper's window: the Golden Cross for a Dread Token, the Dread Bell for 3 Dread Essence.
//   the bell rung by day: tonight is a Dread Night. Nightfall: it starts - a monster already out flees, a fresh one never rises,
//     Emma won't come out, and the player is hunted.
//   a Stalker rises 30+ blocks off; it can't be hurt; its blow takes a third of a full Eldritch-armoured player's health.
//   the Golden Cross (sneak + use on the floor, and on a wall): a Stalker set inside its ground is thrown back out; punched, both
//     crosses come back.
//   (2.88) the night's own monsters are left to walk it - one out before nightfall stays, a fresh one rises.
//   standing still 8 s: a Stalker shut in a glass box 25 blocks off steps out of the dark behind you ("Don't stand still", "Behind you").
//   outrun (rcon puts it 70 blocks off): it loses you. Dawn: the Stalkers come apart; 3 Essence + 1 for the one outrun.
//   the Dread Totem forged from 16 Essence and 4 Dread Tokens tossed down; carried by day, a fresh monster never rises within 32
//     and one already out joins its side (it won't turn on you); dropped, you're back on your own.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const has = async id => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const num = async c => { const m = (await run(c)).match(/(-?[\d.]+)[dfb]?$/); return m ? +m[1] : NaN; };
  const passes = async c => /passed/.test(await run(c));
  const O = 'execute in minecraft:overworld run ';
  const X = 13480, Y = 121, Z = 13400;
  const CX = 24000, CY = 30, CZ = 24000, W = 10;
  const VX = CX + 57.5, VY = CY + W, VZ = CZ + 58.5;
  const VES = `@e[type=minecraft:villager,tag=bm.vesper,x=${VX},y=${VY},z=${VZ},distance=..3,limit=1]`;
  const STK = '@e[type=minecraft:zombie,tag=bm.stalker,limit=1]';
  const uuidEnt = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(400); A.stand(); };
  const trade = async (sel, iid) => {
    let idx = -1;
    for (let i = 0; i < 40 && idx < 0; i++) if (new RegExp(`"${iid}"`).test(await run(`${O}data get entity ${sel} Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`))) idx = i;
    const eid = await uuidEnt(sel); A.windows.length = 0; A.interact(eid); await sleep(1200);
    const w = A.windows[A.windows.length - 1];
    if (w && idx >= 0) {
      A.write('select_trade', { slot: idx }); await sleep(400);
      A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(800);
      A.close(w.windowId); await sleep(500);
    }
    return idx;
  };
  const dist = async (sel, x, y, z) => { const p = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    return p ? Math.hypot(+p[1] - x, +p[2] - y, +p[3] - z) : NaN; };
  const saved = { conq: await sc('TestRat', 'bm.conq'), hard: await sc('#hard', 'bm.cfg'), dkn: await sc('#dkn', 'bm.cfg'), bmoff: await sc('#bmoff', 'bm.cfg') };

  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  await run('scoreboard players set TestRat bm.conq 6'); await run('scoreboard players set #hard bm.cfg 1');
  await run('scoreboard players set #bmoff bm.cfg 1');                   // (staged: not a Blood Moon day - the bell won't ring on one)
  await run('time set 6000');

  // ================================================================== 1. Vesper: the Golden Cross and the Dread Bell
  await run(`${O}forceload add ${CX + 16} ${CZ + 8} ${CX + 72} ${CZ + 64}`);
  await run('loot replace entity TestRat hotbar.8 loot bm:items/market_key'); await run('loot replace entity TestRat hotbar.7 loot bm:items/bankers_card');
  await at(VX - 2, VY, VZ, -90, 10);
  ok('(staged) hard mode, a King-slayer: Vesper in his shop', await wait(25000, async () => passes(`${O}execute if entity ${VES}`), 500));
  await run('loot give TestRat loot bm:items/dread_token');
  for (let i = 0; i < 3; i++) await run('loot give TestRat loot bm:items/dread_essence');
  await sleep(2500);                                                    // (his window opens for King-slayers within the second)
  const ci = await trade(VES, 'golden_cross');
  const bi = await trade(VES, 'dread_bell');
  ok('Vesper sells a Golden Cross for a Dread Token, and a Dread Bell for 3 Dread Essence', (await has('golden_cross')) === 1 && (await has('dread_bell')) === 1 &&
     (await has('dread_essence')) === 0 && (await has('dread_token')) === 0, `trades ${ci}, ${bi}`);
  await run(`${O}forceload remove ${CX + 16} ${CZ + 8} ${CX + 72} ${CZ + 64}`);

  // ================================================================== 2. the pad: a wide floor in the sky
  await run(`${O}forceload add ${X - 80} ${Z - 80} ${X + 80} ${Z + 80}`);
  await run(`${O}fill ${X - 40} ${Y - 1} ${Z - 40} ${X + 40} ${Y - 1} ${Z + 40} minecraft:stone`);
  for (const [y0, y1] of [[Y, Y + 2], [Y + 3, Y + 5]]) await run(`${O}fill ${X - 40} ${y0} ${Z - 40} ${X + 40} ${y1} ${Z + 40} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..60]`);
  await at(X + 0.5, Y, Z + 0.5, 0, 0);
  // ---- the bell, rung by day
  const bs = await (async () => { for (let s = 0; s < 9; s++) if (/dread_bell/.test(await run(`data get entity TestRat Inventory[{Slot:${s}b}].components."minecraft:custom_data".bm`))) return s; return -1; })();
  A.slot(bs); await sleep(300); A.chats.length = 0; A.use(); await sleep(2400); A.release(); await sleep(800);
  ok('The Dread Bell rung by day: tonight is a Dread Night', (await sc('#dnday', 'bm.bm')) === (await sc('#day', 'bm.bm')) && (await has('dread_bell')) === 0 &&
     /Dread Night/.test(A.chats.join(' ')), A.chats.join(' | ').slice(-160));
  // a monster out before it falls; then nightfall
  await run(`${O}summon minecraft:husk ${X + 6.5} ${Y} ${Z + 0.5} {Tags:["bm.seen","t228a"],PersistenceRequired:1b}`);
  A.chats.length = 0; await run('time set 13100');
  ok('Nightfall: the Dread Night begins - and the player is hunted', await wait(4000, async () => (await sc('#dnight', 'bm.bm')) === 1) &&
     await wait(2000, async () => passes('execute if entity @a[name=TestRat,tag=bm.dnh]')), A.chats.join(' | ').slice(-120));
  await run('scoreboard players set TestRat bm.dnst -1000');          // (staged: no Stalker steps out of the dark behind a player standing about for the test)
  // (2.88: the night's monsters walk it as on any night - it no longer clears them; the Stalkers are its own)
  await sleep(2000);
  ok('...the monster already out stays out (2.88)', await passes(`${O}execute if entity @e[tag=t228a]`));
  await run(`${O}summon minecraft:husk ${X + 6.5} ${Y} ${Z + 0.5} {Tags:["t228a"]}`);           // (no bm.seen: as the night would spawn it)
  await sleep(3000);
  ok('...and a fresh one rises as on any night (2.88)', (await num(`${O}execute if entity @e[type=minecraft:husk,tag=t228a,x=${X},y=${Y},z=${Z},distance=..12]`)) === 2);
  await run(`${O}kill @e[tag=t228a]`);
  await run('loot replace entity TestRat hotbar.3 loot bm:items/emma_ribbon'); A.slot(3); await sleep(300); A.bars.length = 0;
  A.use(); await sleep(300); A.release(); await sleep(1200);
  ok('Emma won\'t come out on a Dread Night', A.bars.some(b => /Emma won't come out/.test(b)) &&
     !(await passes(`${O}execute if entity @e[type=minecraft:cat,tag=bm.emmapet,x=${X},y=${Y},z=${Z},distance=..10]`)), A.bars.slice(-2).join(' | '));
  await run('clear TestRat *[minecraft:custom_data~{bm:"emma_ribbon"}]');

  // ================================================================== 3. a Stalker
  await run('scoreboard players set TestRat bm.dnsp 1');
  let d0 = NaN;
  ok('A Stalker rises - at least 30 blocks away', await wait(5000, async () => { if (!(await passes(`${O}execute if entity ${STK}`))) return false;
    d0 = await dist(STK, A.pos.x, A.pos.y, A.pos.z); return true; }) && d0 >= 29, `${d0.toFixed(1)} blocks`);
  const parts = await run(`${O}execute if entity @e[type=minecraft:item_display,tag=bm.stkpart]`);
  ok('...bound to its quarry, its whole rig with it (2.88: ten jointed parts)', (await sc(STK, 'bm.pid')) === (await sc('TestRat', 'bm.pid')) && /count: 10\b/i.test(parts),
     `${await sc(STK, 'bm.pid')} vs ${await sc('TestRat', 'bm.pid')}; ${parts}`);
  // (it waits in a glass box until it's wanted)
  const box = async (on) => run(`${O}fill ${X + 29} ${Y} ${Z + 24} ${X + 31} ${Y + 3} ${Z + 26} minecraft:${on ? 'glass hollow' : 'air'}`);
  await box(true); await run(`${O}tp ${STK} ${X + 30.5} ${Y} ${Z + 25.5}`);
  // armour on, full health; the Stalker set at arm's length; struck with a netherite sword, it shrugs
  for (const [s, p] of [['head', 'helmet'], ['chest', 'chestplate'], ['legs', 'leggings'], ['feet', 'boots']]) await run(`loot replace entity TestRat armor.${s} loot bm:items/eld_${p}`);
  await run('item replace entity TestRat hotbar.0 with minecraft:netherite_sword'); A.slot(0); await sleep(600);   // (worn armour's health counts from the next tick)
  await run('effect give TestRat minecraft:instant_health 1 10 true'); await sleep(1500);
  await run('scoreboard objectives add t228dt minecraft.custom:minecraft.damage_taken'); await run('scoreboard players set TestRat t228dt 0');
  const hp0 = await num('data get entity TestRat Health');
  await box(false); await run(`${O}tp ${STK} ${X + 0.5} ${Y} ${Z + 3.2} 180 0`); await sleep(150);
  const sEid = await uuidEnt(STK);
  for (let i = 0; i < 2; i++) { A.attack(sEid); await sleep(500); }
  ok('Struck with a netherite sword, the Stalker shrugs it off', await passes(`${O}execute if entity ${STK}`) && (await num(`${O}data get entity ${STK} Health`)) >= 1000);
  let taken = 0;
  await wait(5000, async () => { taken = (await sc('TestRat', 't228dt')) / 10; return taken > 1; }, 100);
  const hp1 = hp0 - taken;
  await run(`${O}tp ${STK} ${X + 30.5} ${Y} ${Z + 25.5}`);
  const mhp = await num('attribute TestRat minecraft:max_health get');
  const third = mhp / 3 + 0.5;
  ok('...its blow takes a third of a full, Eldritch-armoured player (through the armour)', mhp >= 35 && hp0 >= mhp - 1 && Math.abs(taken - third) <= 0.6,
     `${hp0} -> ${hp1} of ${mhp} (a third: ${third.toFixed(1)})`);
  await run('effect give TestRat minecraft:instant_health 1 10 true');

  // ================================================================== 4. the Golden Cross
  await at(X + 0.5, Y, Z + 0.5, 0, 70);
  const cs = await (async () => { for (let s = 0; s < 9; s++) if (/golden_cross/.test(await run(`data get entity TestRat Inventory[{Slot:${s}b}].components."minecraft:custom_data".bm`))) return s; return -1; })();
  A.slot(cs); await sleep(300); A.input({ shift: true }); await sleep(300); A.use(); await sleep(250); A.release(); await sleep(500); A.input({}); await sleep(300);
  ok('The Golden Cross, sneak + use on the floor: set up', await passes(`${O}execute if entity @e[type=minecraft:marker,tag=bm.gcm,x=${X},y=${Y},z=${Z},distance=..4]`) &&
     (await has('golden_cross')) === 0);
  const g = (await run(`${O}data get entity @e[type=minecraft:marker,tag=bm.gcm,x=${X},y=${Y},z=${Z},distance=..4,limit=1] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
  ok('...standing on the floor, not sunk into the block under it (2.88)', Math.abs(g[1] - Y) < 0.05, `at y ${g[1]} (the floor's top is ${Y})`);
  await box(false); await run(`${O}tp ${STK} ${g[0] + 4} ${Y} ${g[2]}`); await sleep(3000);
  const dc = await dist(STK, g[0], g[1], g[2]);
  ok('...a Stalker set four blocks from it is thrown back out of its ground', dc >= 11, `${dc.toFixed(1)} blocks from the cross after 3 s`);
  const hpc = await num('data get entity TestRat Health');
  ok('...and the player beside the cross is untouched', hpc >= hp0 - 1, `${hpc}`);
  // a second one, on a wall
  await box(true); await run(`${O}tp ${STK} ${X + 30.5} ${Y} ${Z + 25.5}`);
  await run(`${O}fill ${X + 3} ${Y} ${Z - 1} ${X + 3} ${Y + 2} ${Z + 1} minecraft:stone`);
  await run('loot give TestRat loot bm:items/golden_cross'); await sleep(300);
  await at(X + 0.5, Y, Z + 0.5, -90, 0);
  const cs2 = await (async () => { for (let s = 0; s < 9; s++) if (/golden_cross/.test(await run(`data get entity TestRat Inventory[{Slot:${s}b}].components."minecraft:custom_data".bm`))) return s; return -1; })();
  A.slot(cs2); await sleep(300); A.input({ shift: true }); await sleep(300); A.use(); await sleep(250); A.release(); await sleep(500); A.input({}); await sleep(300);
  ok('...and one on a wall: hung on it, facing out', /golden_cross_wall/.test(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.gcd,x=${X + 2.5},y=${Y + 1},z=${Z + 0.5},distance=..1.2,limit=1] item`)));
  const gw = (await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.gcd,x=${X + 2.5},y=${Y + 1},z=${Z + 0.5},distance=..1.6,limit=1] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
  ok('...in the open cell in front of the wall, not inside it (2.88)', Math.abs(gw[0] - (X + 2.5)) < 0.05 && Math.abs(gw[1] - (Y + 1)) < 0.05, `at ${gw.join(', ')}`);
  for (const sel of [`@e[type=minecraft:interaction,tag=bm.gci,x=${X + 2.5},y=${Y + 1},z=${Z + 0.5},distance=..1.5,limit=1]`,
                     `@e[type=minecraft:interaction,tag=bm.gci,x=${X},y=${Y},z=${Z},distance=..4,limit=1]`]) { A.attack(await uuidEnt(sel)); await sleep(700); }
  ok('...punched, both come back to the pack', (await has('golden_cross')) === 2 && !(await passes(`${O}execute if entity @e[type=minecraft:marker,tag=bm.gcm,x=${X},y=${Y},z=${Z},distance=..6]`)));
  await run(`${O}fill ${X + 3} ${Y} ${Z - 1} ${X + 3} ${Y + 2} ${Z + 1} minecraft:air`);

  // ================================================================== 5. standing still
  await box(true); await run(`${O}tp ${STK} ${X + 30.5} ${Y} ${Z + 25.5}`);
  await at(X + 30.5, Y, Z + 0.5, 0, 0); await run('scoreboard players set TestRat bm.dnst 0'); A.bars.length = 0;
  const blinked = await wait(13000, async () => (await dist(STK, A.pos.x, A.pos.y, A.pos.z)) <= 4.5, 300);
  ok('Standing still 8 s: the Stalker shut in a glass box 25 blocks off steps out behind you', blinked &&
     A.bars.some(b => /stand still/.test(b)) && A.bars.some(b => /Behind you/.test(b)), A.bars.slice(-3).join(' | '));
  await box(false);
  // ---- outrun
  await run(`${O}tp ${STK} ${X - 72.5} ${Y} ${Z + 0.5}`); A.bars.length = 0;
  ok('Outrun (70 blocks off): it loses you', await wait(3000, async () => !(await passes(`${O}execute if entity @e[type=minecraft:zombie,tag=bm.stalker]`))) &&
     (await sc('TestRat', 'bm.dnesc')) === 1, A.bars.slice(-1).join(''));

  // ================================================================== 6. dawn
  await at(X + 0.5, Y, Z + 0.5, 0, 0);
  await run('scoreboard players set TestRat bm.dnsp 1');
  await wait(4000, async () => passes(`${O}execute if entity ${STK}`));
  await run('scoreboard players set TestRat bm.dnt 400');                      // (staged: out in it most of the night)
  const e0 = await has('dread_essence'); A.chats.length = 0;
  await run('time set 23100');
  ok('Dawn: the night ends and the Stalkers come apart', await wait(4000, async () => (await sc('#dnight', 'bm.bm')) === 0) &&
     !(await passes(`${O}execute if entity @e[type=minecraft:zombie,tag=bm.stalker]`)) && !(await passes(`${O}execute if entity @e[tag=bm.stkpart]`)));
  ok('...survived: 3 Dread Essence, and 1 for the Stalker outrun', await wait(2000, async () => (await has('dread_essence')) === e0 + 4), `${e0} -> ${await has('dread_essence')}`);

  // ================================================================== 7. the Dread Totem
  await run('time set 1000'); await at(X + 0.5, Y, Z + 0.5, 0, 60);
  await run('clear TestRat'); await sleep(300);
  for (let i = 0; i < 16; i++) await run('loot give TestRat loot bm:items/dread_essence');
  for (let i = 0; i < 4; i++) await run('loot give TestRat loot bm:items/dread_token');
  await sleep(300);
  for (const s of [0, 1]) { A.slot(s); await sleep(200); A.drop(true); await sleep(250); }
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 4.5} 0 0`);
  await wait(4000, async () => passes(`${O}execute if entity @e[type=minecraft:marker,tag=bm.fg_dtotem,x=${X},y=${Y},z=${Z},distance=..8]`));
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`);
  ok('16 Dread Essence and 4 Dread Tokens tossed down forge a Dread Totem (picked up)', await wait(12000, async () => (await has('dread_totem')) === 1));
  await sleep(1500);
  await run(`${O}summon minecraft:husk ${X + 8.5} ${Y} ${Z + 0.5}`);
  ok('Carried by day: a fresh monster never rises near you', await wait(3000, async () => !(await passes(`${O}execute if entity @e[type=minecraft:husk,x=${X},y=${Y},z=${Z},distance=..14]`))));
  await run(`${O}summon minecraft:husk ${X + 6.5} ${Y} ${Z + 0.5} {Tags:["bm.seen","t228b"],PersistenceRequired:1b}`);
  ok('...one already out joins its side - it won\'t turn on you', await wait(3000, async () => passes(`${O}execute if entity @e[tag=t228b,team=bm.dtot]`) &&
     passes('execute if entity @a[name=TestRat,team=bm.dtot]')));
  const ts = await (async () => { for (let s = 0; s < 9; s++) if (/dread_totem/.test(await run(`data get entity TestRat Inventory[{Slot:${s}b}].components."minecraft:custom_data".bm`))) return s; return -1; })();
  A.slot(ts); await sleep(200); A.drop(true); await sleep(300); await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 6.5} 0 0`);
  ok('...dropped: you\'re back on your own', await wait(3000, async () => passes('execute if entity @a[name=TestRat,team=]')));

  // ---- put things back
  await run('scoreboard objectives remove t228dt');
  await run(`${O}kill @e[tag=t228b]`); await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..60]`);
  await run(`${O}kill @e[type=minecraft:zombie,tag=bm.stalker]`); await run(`${O}kill @e[tag=bm.stkpart]`);
  await run(`${O}fill ${X - 40} ${Y - 1} ${Z - 40} ${X + 40} ${Y - 1} ${Z + 40} minecraft:air`);
  await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:stone`);
  await run(`scoreboard players set TestRat bm.conq ${isNaN(saved.conq) ? 6 : saved.conq}`); await run(`scoreboard players set #hard bm.cfg ${isNaN(saved.hard) ? 0 : saved.hard}`);
  await run(`scoreboard players set #dkn bm.cfg ${isNaN(saved.dkn) ? 0 : saved.dkn}`); await run('scoreboard players set #dnday bm.bm -1');
  await run(`scoreboard players set #bmoff bm.cfg ${isNaN(saved.bmoff) ? 0 : saved.bmoff}`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 5 true'); await run('gamemode creative TestRat');
  await run('time set 6000');
  await run(`${O}forceload remove ${X - 80} ${Z - 80} ${X + 80} ${Z + 80}`);
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

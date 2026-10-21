// 2.84d: the Omni Token, the golden dolls, the Eldritch Panoply, and hard mode for King-beaters only - as a regular player.
//   the forge: a Dread Token, 16 Ember Scales and 16 Void Shards tossed down (Q) together fuse into an Omni Token.
//   the Ember Rat (rcon sets him on the pad): Cecil's golden doll for sale (met), the Frog's still wrapped (not met - rcon
//     takes that away for the stage); the Golden Cecil Doll bought through his window; set down (sneak + use): Fire
//     Resistance near it; punched: back in the pack.
//   the Void Rat: the Eldritch Panoply on his list; the Gnawing Pick bought for 2 Omni Tokens.
//   the Panoply worn: Night Vision, darkness cleared; struck (rcon: a zombie's blow), the zombie is lashed back.
//   the Maw: a kill feeds two hearts of Absorption.
//   (Vesper's veil for anyone who hasn't beaten the Hollow King, and his Ledger's refusal: t224's last steps.)
//   Dread rolls: a conquest-0 player never sees one in 400 rolls; a King-beater does.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const has = async id => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const num = async c => { const m = (await run(c)).match(/(-?[\d.]+)(?!.*\d)/); return m ? +m[1] : NaN; };
  const passes = async c => /passed/.test(await run(c));
  const effects = async () => run('data get entity TestRat active_effects');
  const O = 'execute in minecraft:overworld run ';
  const X = 13480, Y = 121, Z = 13400;
  const uuidEnt = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
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
  const saved = { conq: await sc('TestRat', 'bm.conq'), hard: await sc('#hard', 'bm.cfg') };

  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:stone`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 4} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..14]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 60`); await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  await run('scoreboard players set TestRat bm.conq 6');
  await sleep(1200); A.stand();

  // ================================================================== 1. the Omni Token forge
  await run('loot replace entity TestRat hotbar.0 loot bm:items/dread_token');
  for (const id of ['ember_scale', 'void_shard']) for (let i = 0; i < 16; i++) await run(`loot give TestRat loot bm:items/${id}`);   // (hotbar.1 and hotbar.2)
  ok('(staged: 16 Ember Scales in hotbar 1, 16 Void Shards in hotbar 2)', /count: 16/.test(await run('data get entity TestRat Inventory[{Slot:1b}].count')) || /: 16$/.test(await run('data get entity TestRat Inventory[{Slot:1b}].count')));
  for (const s of [1, 2, 0]) { A.slot(s); await sleep(200); A.drop(true); await sleep(250); }
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 4.5} 0 0`);           // (then a step back, off the pile - as anyone would, or it's picked up again)
  ok('A Dread Token, 16 Ember Scales and 16 Void Shards tossed down: the forge wakes', await wait(4000, async () => passes(`${O}execute if entity @e[type=minecraft:marker,tag=bm.fg_omni,x=${X},y=${Y},z=${Z},distance=..8]`)));
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`);           // (the forge holds its things now - back to wait by it)
  ok('...and an Omni Token comes out of it (picked up)', await wait(12000, async () => (await has('omni_token')) === 1));

  // ================================================================== 2. the Ember Rat's golden dolls
  await run('advancement grant TestRat only bm:met/cecil'); await run('advancement revoke TestRat only bm:met/frog');
  await run('execute as TestRat at @s run function bm:p22/rat/spawn_ember'); await sleep(500);
  const EMB = '@e[type=minecraft:wandering_trader,tag=bm.frat_ember,limit=1]';
  await run(`${O}tp ${EMB} ${X + 0.5} ${Y} ${Z + 3.5} 180 0`); await sleep(2500);
  const sellOf = async (iid) => { for (let i = 0; i < 40; i++) { const r = await run(`${O}data get entity ${EMB} Offers.Recipes[${i}].sell`); if (/Found no|found no/.test(r)) return null; if (r.includes(`"${iid}"`) || (iid === 'wrapped' && r.includes('bm_wrapped'))) return r; } return null; };
  const cec = await run(`${O}data get entity ${EMB} Offers.Recipes[{sell:{components:{"minecraft:custom_data":{bm:"gdoll_cecil"}}}}].maxUses`);
  ok('The Ember Rat: the Golden Cecil Doll for sale (Cecil met)', /2147483647/.test(cec), cec.slice(-60));
  ok('...the Frog\'s golden doll still under wraps (not met)', !(await passes(`${O}execute if data entity ${EMB} Offers.Recipes[{sell:{components:{"minecraft:custom_data":{bm:"gdoll_frog"}}}}]`)) &&
     await passes(`${O}execute if data entity ${EMB} Offers.Recipes[{maxUses:0,sell:{components:{"minecraft:custom_data":{bm_wrapped:1b}}}}]`));
  const ti = await trade(EMB, 'gdoll_cecil');
  ok('...the Golden Cecil Doll bought through his window (1 Omni Token)', (await has('gdoll_cecil')) === 1 && (await has('omni_token')) === 0, `trade ${ti}`);
  await run(`${O}kill @e[tag=bm.frat_ember]`); await run(`${O}kill @e[tag=bm.field_sprite,x=${X},y=${Y},z=${Z},distance=..60]`);
  const cs = (await run('clear TestRat *[minecraft:custom_data~{bm:"gdoll_cecil"}] 0'));
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.1 loot bm:items/gdoll_cecil'); A.slot(1);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 60`); await sleep(1000); A.stand();
  A.input({ shift: true }); await sleep(400); A.use(); await sleep(300); A.release(); await sleep(700); A.input({}); await sleep(300);
  const gi = 1;                                                           // (Cecil: the second golden doll - emma's first)
  const placed = async () => passes(`${O}execute if entity @e[type=minecraft:marker,tag=bm.gd${gi}m,x=${X},y=${Y},z=${Z},distance=..5]`);
  ok('The Golden Cecil Doll, sneak + use on the floor: set down', await placed() && (await has('gdoll_cecil')) === 0, cs);
  ok('...near it: Fire Resistance', await wait(3000, async () => /fire_resistance/.test(await effects())));
  A.attack(await uuidEnt(`@e[type=minecraft:interaction,tag=bm.gd${gi},x=${X},y=${Y},z=${Z},distance=..5,limit=1]`)); await sleep(900);
  ok('...punched: back in the pack', !(await placed()) && (await has('gdoll_cecil')) === 1);

  // ================================================================== 3. the Void Rat's Eldritch Panoply
  await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat at @s run function bm:p22/rat/spawn_void'); await sleep(500);
  const VOID = '@e[type=minecraft:wandering_trader,tag=bm.frat_void,limit=1]';
  await run(`${O}tp ${VOID} ${X + 0.5} ${Y} ${Z + 3.5} 180 0`); await sleep(1500);
  const sells = async id => passes(`${O}execute if data entity ${VOID} Offers.Recipes[{sell:{components:{"minecraft:custom_data":{bm:"${id}"}}}}]`);
  ok('The Void Rat: the Eldritch Panoply on his list', await sells('eld_chestplate') && await sells('eld_maw') && await sells('eld_pick') && await sells('eld_shovel'));
  await run('loot give TestRat loot bm:items/omni_token'); await run('loot give TestRat loot bm:items/omni_token'); await sleep(400);
  const vi = await trade(VOID, 'eld_pick');
  ok('...the Gnawing Pick bought for 2 Omni Tokens', (await has('eld_pick')) === 1 && (await has('omni_token')) === 0, `trade ${vi}`);
  await run(`${O}kill @e[tag=bm.frat_void]`); await run(`${O}kill @e[tag=bm.field_sprite,x=${X},y=${Y},z=${Z},distance=..60]`);
  A.slot(0); await sleep(300);
  await run('item replace entity TestRat hotbar.0 with minecraft:air'); await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/eld_pick'); await sleep(1500);
  ok('...held: Haste', await wait(3000, async () => /haste/.test(await effects())));

  // ================================================================== 4. the Panoply worn, and the Maw
  await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:darkness 30 0');
  for (const [s, p] of [['head', 'helmet'], ['chest', 'chestplate'], ['legs', 'leggings'], ['feet', 'boots']])
    await run(`loot replace entity TestRat armor.${s} loot bm:items/eld_${p}`);
  ok('The Eldritch Panoply worn: Night Vision, and the darkness lifts', await wait(3000, async () => { const e = await effects(); return /night_vision/.test(e) && !/darkness/.test(e); }));
  await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 2.5} {NoAI:1b,Silent:1b,PersistenceRequired:1b,Tags:["bm.seen","bm.t227"],attributes:[{id:"minecraft:max_health",base:100}],Health:100f}`);
  const zo = '@e[type=minecraft:zombie,tag=bm.t227,limit=1]';
  await sleep(500); await run(`${O}damage TestRat 2 minecraft:mob_attack by ${zo}`);
  ok('...struck by a zombie: it is lashed back (3, and Wither)', await wait(2000, async () => (await num(`${O}data get entity ${zo} Health`)) <= 97.5) &&
     /wither/.test(await run(`${O}data get entity ${zo} active_effects`)), `${await num(`${O}data get entity ${zo} Health`)}`);
  await run(`${O}data merge entity ${zo} {Health:1f}`); await run('effect clear TestRat minecraft:absorption');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/eld_maw'); A.slot(0); await sleep(500);
  A.attack(await uuidEnt(zo)); await sleep(800);
  ok('The Maw of the Outer Dark: a kill feeds two hearts of Absorption', await wait(3000, async () => !(await passes(`${O}execute if entity ${zo}`)) && /absorption/.test(await effects())),
     `zombie ${await passes(`${O}execute if entity ${zo}`) ? 'alive' : 'dead'}; ${(await effects()).slice(-120)}`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..14]`);

  // ================================================================== 5. Dread rolls: only around a King-beater
  await run('scoreboard players set #hard bm.cfg 1');
  await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 4.5} {NoAI:1b,Silent:1b,PersistenceRequired:1b,Tags:["bm.seen","bm.t227r"]}`);
  const roll = async (n) => { let d = 0; for (let i = 0; i < n; i++) {
    await run(`${O}execute as @e[type=minecraft:zombie,tag=bm.t227r,limit=1] at @s run function bm:p176/roll/zombie`);
    if (await passes(`${O}execute if entity @e[type=minecraft:zombie,tag=bm.t227r,tag=bm.dread]`)) { d++; await run(`${O}tag @e[type=minecraft:zombie,tag=bm.t227r] remove bm.dread`); } }
    return d; };
  await run('scoreboard players set TestRat bm.conq 0');
  const d0 = await roll(400);
  await run('scoreboard players set TestRat bm.conq 6');
  const d6 = await roll(400);
  ok('Dread rolls: none in 400 around a player who hasn\'t beaten the King; some around one who has', d0 === 0 && d6 > 0, `${d0} vs ${d6}`);
  await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t227r]`); await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t227]`);

  // ---- put things back
  await run(`scoreboard players set TestRat bm.conq ${isNaN(saved.conq) ? 6 : saved.conq}`); await run(`scoreboard players set #hard bm.cfg ${isNaN(saved.hard) ? 0 : saved.hard}`);
  await run('advancement grant TestRat only bm:met/frog');
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..14]`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 5 true'); await run('gamemode creative TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

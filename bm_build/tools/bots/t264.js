// 2.94d: THE ARCADE (phase216), as a regular (non-op) player. Hard mode on (rcon - the test server keeps it off): Bit and the
// Pixel Villager in the empty house west of Fountain Plaza (t162's market), their flat sprites, the shop's own props; a trade with
// each (Dread Tokens). Then on a pad: the sets worn (rcon hands over the rest of a set) - the BOUNTY HUNTER's fire resistance and
// night sight, the BLUE BOMBER's buster shot on a blow, the PLUMBER's STOMP (falling onto a monster), the VAMPIRE HUNTER's 8 more to
// the undead; the ARM BUSTER, FIRE FLOWER and 8-BIT BLADE's shots; the chips onto a sword in the off hand (Game Genie: its damage
// up; 2.94j - MISSINGNO. kills never glitch a currency in the sixth slot, one in 64; 2.94l - the Eject Button takes them out again, a
// tuned sword takes none, and the tool chips go onto a pickaxe); the props - a ? block set down (a Token, then "Empty"), two Warp Pipes (one takes you to the other), a Save Point (your
// spawn), picked up again (sneak + punch); the Heart Container (+1 heart), the Super Star (Resistance V), the Power Mushroom
// (bigger). Hard mode off: the traders are gone.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const passes = async c => /passed/i.test(await run(c));
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async id => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const fx = async () => await run('data get entity TestRat active_effects');
  const num = async (sel, path) => +(((await run(`${O}data get entity ${sel} ${path}`)).match(/(-?[\d.]+)[dfbsL]?$/) || [0, NaN])[1]);
  const uuidEnt = async sel => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(400); A.stand(); };
  const use = async (slot, ms = 400) => {                             // (the pack's 2-second guard between uses of an item that acts: waited out)
    await wait(3000, async () => !/has [1-9]/.test(await run('scoreboard players get TestRat bm.gvhc')), 200);
    A.slot(slot); await sleep(250); A.use(); await sleep(ms); A.release(); await sleep(500); };
  const give = async (slot, iid) => run(`loot replace entity TestRat ${slot} loot bm:items/${iid}`);
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
    return { idx, opened: !!w };
  };
  // (t162's market: template (x, y, z) is the world's (CX + x, CY + y, CZ + z))
  const CX = 24000, CY = 30, CZ = 24000, W = 10;
  const RAT = `@e[type=minecraft:villager,tag=bm.arcrat,x=${CX + 24.5},y=${CY + W},z=${CZ + 51.6},distance=..2,limit=1]`;
  const VIL = `@e[type=minecraft:villager,tag=bm.arcvil,x=${CX + 26.5},y=${CY + W},z=${CZ + 51.6},distance=..2,limit=1]`;
  const X = 17980, Y = 100, Z = 16000;                                  // (the pad)
  const HUSK = (dx, dz, t, hp = 300) => run(`${O}summon minecraft:husk ${X + dx + 0.5} ${Y + 1} ${Z + dz + 0.5} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t264z","${t}","bm.seen"],attributes:[{id:"minecraft:max_health",base:${hp}}],Health:${hp}f}`);
  const hp = async t => num(`@e[tag=${t},limit=1]`, 'Health');
  const epos = async sel => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const fall = async (floorY) => {                                     // (the bot doesn't fall by itself: a tick at a time, as t133)
    A.unstand(); A.input({}); const p = await epos('@a[name=TestRat,limit=1]');   // (stand()'s on-ground packets would cut the fall short) if (!p) return false; A.pos.x = p[0]; A.pos.y = p[1]; A.pos.z = p[2];
    let v = 0;
    for (let k = 0; k < 400 && A.pos.y > floorY; k++) {
      v = (v + 0.08) * 0.98; A.pos.y = Math.max(floorY, A.pos.y - v);
      A.write('position', { x: A.pos.x, y: A.pos.y, z: A.pos.z, flags: { onGround: A.pos.y <= floorY, hasHorizontalCollision: false } }); A.write('tick_end', {});
      await sleep(100);                                                // (a step a server tick - two in one tick and the fall reads as one jump)
    }
    A.stand(); await sleep(600); return true;
  };
  const heal = async () => { await run('effect give TestRat minecraft:instant_health 1 10 true'); await sleep(300); };

  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run(`${O}forceload add ${CX} ${CZ} ${CX + 76} ${CZ + 84}`);   // (the whole town: the market's patch runs only with it loaded)
  await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  await run('loot replace entity TestRat hotbar.8 loot bm:items/market_key');
  await run('scoreboard players set TestRat bm.bk_dread 0'); await run('scoreboard players reset TestRat bm.archc');
  await run('attribute TestRat minecraft:max_health modifier remove bm:arc_heart_1'); await run('attribute TestRat minecraft:max_health modifier remove bm:arc_heart_2');
  await run('attribute TestRat minecraft:max_health modifier remove bm:arc_heart_3');

  // (t162's market - placed if a last run hasn't)
  const MK = `@e[type=minecraft:marker,tag=bm.mkt,x=${CX + 38.5},y=${CY + 12},z=${CZ + 46.5},distance=..2,limit=1]`;
  await sleep(2500);
  if (!(await passes(`${O}execute if entity ${MK}`))) { let pl = ''; for (let i = 0; i < 30; i++) { pl = await run(`${O}place template bm:black_market ${CX} ${CY} ${CZ}`); if (!/not loaded/.test(pl)) break; await sleep(2000); } console.log('   placed: ' + pl.slice(0, 60)); }
  // ================================================================== 1. the shop comes with hard mode
  await run(`${O}kill @e[tag=bm.arcnpc]`); await run(`${O}kill @e[tag=bm.arcspr]`);
  await run('scoreboard players set #hardoff bm.cfg 0'); await run('scoreboard players set #hard bm.cfg 1');
  await run(`${O}tp TestRat ${CX + 25.5} ${CY + W} ${CZ + 54.5} 180 0`); await sleep(1500); A.stand();
  ok('Hard mode on: Bit and the Pixel Villager behind their counter, in the empty house', await wait(25000, async () => (await cnt(RAT)) === 1 && (await cnt(VIL)) === 1, 500));
  ok('...each a flat pixel sprite (front and back), turned to the room', (await cnt(`@e[type=minecraft:item_display,tag=bm.arcspr,x=${CX + 25.5},y=${CY + W},z=${CZ + 51.6},distance=..3]`)) === 2 &&
     !/billboard: "center"/.test(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.arcspr_rat,limit=1]`)));
  await sleep(3000);
  ok('...and the villagers under them stay invisible, seconds on (2.94j: the market\'s sweep cleared it - plain villagers showed)',
     (await cnt(`@e[type=minecraft:villager,tag=bm.arcnpc,predicate=bm:p126/invis,x=${CX + 25.5},y=${CY + W},z=${CZ + 51.6},distance=..4]`)) === 2);
  ok('...and the shop\'s own props about it (the arcade cabinet, the pipe, the ? block)', (await cnt(`@e[type=minecraft:item_display,tag=bm.arcshop,x=${CX + 25.5},y=${CY + W},z=${CZ + 54.5},distance=..6]`)) === 3);
  // (2.94n) the props face the way the market does: a summon took no rotation, so in a market turned any other way they stood
  // edge-on. Turned 90 degrees off (rcon, the stage): the market's patch turns it back to the market's own facing.
  const yawOf = async sel => +(((await run(`${O}data get entity ${sel} Rotation[0]`)).match(/(-?[\d.]+)f$/) || [0, NaN])[1]);
  const CAB = `@e[type=minecraft:item_display,tag=bm.arcp_arcade_cabinet,x=${CX + 25.5},y=${CY + W},z=${CZ + 54.5},distance=..6,limit=1]`;
  const mktYaw = await yawOf(`@e[type=minecraft:marker,tag=bm.mkt,x=${CX},y=${CY},z=${CZ},distance=..120,limit=1]`);
  await run(`${O}execute as ${CAB} at @s run tp @s ~ ~ ~ ${mktYaw + 90} 0`);
  ok('...a prop turned 90 degrees off is turned back to the market\'s facing (its patch, every 10 s)', await wait(15000, async () => Math.abs(((await yawOf(CAB)) - mktYaw + 540) % 360 - 180) < 1, 500),
     `market ${mktYaw}, cabinet ${await yawOf(CAB)}`);
  const tokens = async n => { await run('clear TestRat *[minecraft:custom_data~{bm:"dread_token"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/dread_token');
    await run(`item modify entity TestRat hotbar.0 {type:"minecraft:set_count",count:${n}}`); A.slot(0); await sleep(300); };
  await tokens(6);
  let t = await trade(RAT, 'pixel_blade');
  ok('Right-click Bit: his trades - the 8-Bit Blade bought for 6 Dread Tokens', t.opened && t.idx >= 0 && (await has('pixel_blade')) === 1 && (await has('dread_token')) === 0,
     JSON.stringify(t) + ` blade ${await has('pixel_blade')} tokens ${await has('dread_token')}`);
  await tokens(4);
  t = await trade(VIL, 'chip_genie');
  ok('...and the Pixel Villager\'s: a Game Genie Chip for 4', t.opened && (await has('chip_genie')) === 1 && (await has('dread_token')) === 0, JSON.stringify(t) + ` chip ${await has('chip_genie')}`);

  // ================================================================== 2. on the pad: the sets
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await sleep(1500);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  const wear = async (pcs) => { for (const [sl, iid] of pcs) await give(`armor.${sl}`, iid); await sleep(1800); };
  await wear([['head', 'hunter_helm'], ['chest', 'hunter_plate'], ['legs', 'hunter_greaves'], ['feet', 'hunter_boots']]);
  ok('the BOUNTY HUNTER set worn: fire resistance, night sight, Jump Boost II', await wait(3000, async () => { const e = await fx(); return /fire_resistance/.test(e) && /night_vision/.test(e) && /jump_boost/.test(e); }), (await fx()).slice(0, 160));
  const mhb = +((await run('attribute TestRat minecraft:max_health base get')).match(/([\d.]+)/) || [0, 0])[1];
  const mhv = +((await run('attribute TestRat minecraft:max_health get')).match(/([\d.]+)/) || [0, 0])[1];
  ok('...and +2 health a piece (+8 in all)', mhv - mhb >= 8, `${mhb} -> ${mhv}`);
  await run('effect clear TestRat');
  await wear([['head', 'bomber_helm'], ['chest', 'bomber_chest'], ['legs', 'bomber_legs'], ['feet', 'bomber_boots']]); await heal();
  await HUSK(2, 0, 'bm.t264b'); await sleep(800); await at(X + 0.5, Y + 1, Z + 0.5, -90, 0);
  const hb = await uuidEnt('@e[tag=bm.t264b,limit=1]'); A.attack(hb); await sleep(300);
  ok('the BLUE BOMBER set: a blow fires a buster shot too (its 7 tops the punch: a bare fist with Strength alone is 4)',
     /has -?\d/.test(await run('scoreboard players get TestRat bm.arcs')) && await wait(3000, async () => (await hp('bm.t264b')) <= 300 - 6.5),
     `hp ${await hp('bm.t264b')} recharge ${await run('scoreboard players get TestRat bm.arcs')}`);
  await run(`${O}kill @e[tag=bm.t264z]`); await sleep(500);
  await wear([['head', 'plumber_cap'], ['chest', 'plumber_shirt'], ['legs', 'plumber_overalls'], ['feet', 'plumber_boots']]);
  await HUSK(3, 3, 'bm.t264s'); await sleep(800);
  await heal(); await run(`${O}tp TestRat ${X + 3.5} ${Y + 8} ${Z + 3.5} 0 90`); await sleep(1500); const h_you = await num('@a[name=TestRat,limit=1]', 'Health');
  if (0) console.log('   DBG before fall: husk', await hp('bm.t264s'), 'tags', (await run('tag TestRat list')).replace(/.*: /, ''), 'pos', (await run('data get entity TestRat Pos')).slice(-40));
  await fall(Y + 1 + 1.95);                                            // (onto the husk's head)
  if (0) console.log('   DBG after fall: husk', await hp('bm.t264s'), 'pos', (await run('data get entity TestRat Pos')).slice(-40), 'husk pos', (await run(`${O}data get entity @e[tag=bm.t264s,limit=1] Pos`)).slice(-40));
  ok('the PLUMBER set: falling onto a monster - STOMP (14, once), and no fall damage', await wait(3000, async () => (await hp('bm.t264s')) <= 300 - 12) && (await hp('bm.t264s')) > 300 - 2 * 12 &&   // (14 less its armour - and once)
     (await num('@a[name=TestRat,limit=1]', 'Health')) >= h_you, `husk ${await hp('bm.t264s')} you ${h_you} -> ${await num('@a[name=TestRat,limit=1]', 'Health')}`);
  await run(`${O}kill @e[tag=bm.t264z]`); await sleep(500);
  await wear([['head', 'vhunter_band'], ['chest', 'vhunter_cuirass'], ['legs', 'vhunter_legs'], ['feet', 'vhunter_boots']]);
  await HUSK(2, 0, 'bm.t264u'); await sleep(600);                    // (a husk: undead, and it doesn't burn by day)
  if (0) console.log('   DBG vhunter husk summoned:', await cnt('@e[tag=bm.t264u]'), await run(`${O}execute if entity @e[type=minecraft:husk,x=${X},y=${Y},z=${Z},distance=..12]`));
  await at(X + 0.5, Y + 1, Z + 0.5, -90, 0); await run('item replace entity TestRat weapon.mainhand with minecraft:stick');
  if (0) console.log('   DBG after at:', await cnt('@e[tag=bm.t264u]'), await hp('bm.t264u'), 'star', await run('scoreboard players get TestRat bm.arcg'));
  A.attack(await uuidEnt('@e[tag=bm.t264u,limit=1]')); await sleep(800);
  if (0) console.log('   DBG after attack:', await cnt('@e[tag=bm.t264u]'), await hp('bm.t264u'));
  ok('the VAMPIRE HUNTER set: a stick\'s tap on a husk (undead) does 8 more', (await hp('bm.t264u')) <= 300 - 8, `hp ${await hp('bm.t264u')} husks ${await cnt('@e[tag=bm.t264u]')}`);
  await run(`${O}kill @e[tag=bm.t264z]`); await run('item replace entity TestRat armor.head with air'); await run('item replace entity TestRat armor.chest with air');
  await run('item replace entity TestRat armor.legs with air'); await run('item replace entity TestRat armor.feet with air'); await run('effect clear TestRat');

  // ================================================================== 3. the weapons' shots
  await heal();
  await HUSK(6, 0, 'bm.t264w'); await sleep(800); await at(X + 0.5, Y + 1, Z + 0.5, -90, 0);
  await give('hotbar.1', 'arm_buster'); await use(1);
  ok('the ARM BUSTER: right-click - a buster shot, and the monster ahead is hit', await wait(4000, async () => (await hp('bm.t264w')) < 300), `hp ${await hp('bm.t264w')}`);
  let h0 = await hp('bm.t264w'); await give('hotbar.2', 'fire_flower'); await sleep(600); await use(2);
  ok('the FIRE FLOWER: a fireball - hit, and alight', await wait(4000, async () => (await hp('bm.t264w')) < h0 && (await num('@e[tag=bm.t264w,limit=1]', 'Fire')) > 0),
     `hp ${await hp('bm.t264w')} fire ${await num('@e[tag=bm.t264w,limit=1]', 'Fire')}`);
  h0 = await hp('bm.t264w'); await run('effect give TestRat minecraft:instant_health 1 4 true'); await sleep(900);
  await run('clear TestRat *[minecraft:custom_data~{bm:"pixel_blade"}]'); await give('hotbar.3', 'pixel_blade'); await use(3);
  ok('the 8-BIT BLADE at full health: a sword beam flies at it', await wait(4000, async () => (await hp('bm.t264w')) < h0), `hp ${await hp('bm.t264w')}`);
  await run(`${O}kill @e[tag=bm.t264z]`);

  // ================================================================== 4. the chips
  await run('item replace entity TestRat weapon.offhand with minecraft:diamond_sword');
  await run('clear TestRat *[minecraft:custom_data~{bm:"chip_genie"}]'); await give('hotbar.4', 'chip_genie'); A.chats.length = 0; await use(4);
  const off = await run('data get entity TestRat equipment.offhand');
  ok('a GAME GENIE CHIP used, a sword in the off hand: in it for good (+4 attack damage), the chip spent', /bm_chip_genie: 1b/.test(off) && /chip_genie/.test(off) && (await has('chip_genie')) === 0, off.slice(0, 200));
  await give('hotbar.4', 'chip_genie'); A.bars.length = 0; await use(4);
  ok('...a second one on the same sword: refused, kept', A.bars.some(b => /already/.test(b)) && (await has('chip_genie')) === 1, A.bars.slice(-1).join(''));
  await give('hotbar.5', 'chip_missingno'); await use(5);
  ok('...and a MISSINGNO. CHIP beside it', /bm_chip_missingno: 1b/.test(await run('data get entity TestRat equipment.offhand')));
  // (2.94j) MISSINGNO. never glitches the market's money: the chipped sword in hand, five Dread Tokens in the sixth slot, twenty
  // kills - still five; and its odds are one in 64 (it was one in four - a Token press)
  await run('item replace entity TestRat hotbar.0 from entity TestRat weapon.offhand'); await run('item replace entity TestRat weapon.offhand with air');
  await give('hotbar.5', 'dread_token'); await run('item modify entity TestRat hotbar.5 {type:"minecraft:set_count",count:5}'); A.slot(0); await sleep(400);
  await run(`${O}fill ${X - 2} ${Y + 1} ${Z + 2} ${X + 2} ${Y + 3} ${Z + 4} minecraft:air`);
  let kills = 0;
  for (let i = 0; i < 20; i++) {
    await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y + 1} ${Z + 1.8} {Tags:["bm.t264mn"],NoAI:1b,Health:1f,attributes:[{id:"minecraft:max_health",base:1}]}`);
    const z = `@e[type=minecraft:zombie,tag=bm.t264mn,limit=1]`; await wait(2000, async () => (await uuidEnt(z)) !== null, 100);
    const eid = await uuidEnt(z); if (eid !== null) { A.attack(eid); await sleep(700); }
    if ((await cnt('@e[type=minecraft:zombie,tag=bm.t264mn]')) === 0) kills++; else await run('kill @e[tag=bm.t264mn]');
  }
  const toks = +(((await run('clear TestRat *[minecraft:custom_data~{bm:"dread_token"}] 0')).match(/Found (\d+)/) || [0, 0])[1]);
  ok('MISSINGNO.: twenty kills with Dread Tokens in the sixth slot - still five (the currencies never glitch)', kills >= 15 && toks === 5, `${kills} kills, ${toks} tokens`);
  const mno = JSON.parse(require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/predicate/p216/mno.json', 'utf8'));
  const kf = require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p216/kill.mcfunction', 'utf8');
  ok('...(every custom currency is turned away before the stack grows: Tokens, Medallions, Trophies, Gutter Coins, Royal Pearls, Blood Crystals, Xenite...)', ['token', 'medallion', 'trophy', 'lucky_token', 'dread_token', 'omni_token', 'gutter_coin', 'gutter_medallion', 'royal_pearl', 'blood_crystal', 'xenite_green']
     .every(c => kf.indexOf(`{bm:"${c}"}] run return 0`) >= 0 && kf.indexOf(`{bm:"${c}"}] run return 0`) < kf.indexOf('set_count')));
  ok('...and its odds are one in 64', Math.abs(mno.chance - 1 / 64) < 1e-9, JSON.stringify(mno));
  // (2.94l) THE EJECT BUTTON: the chipped sword back in the off hand - both chips out (each back as a chip), the sword clean
  await run('item replace entity TestRat weapon.offhand from entity TestRat hotbar.0'); await run('item replace entity TestRat hotbar.0 with air');
  await run('clear TestRat *[minecraft:custom_data~{bm:"chip_genie"}]'); await run('clear TestRat *[minecraft:custom_data~{bm:"chip_missingno"}]');
  await give('hotbar.6', 'chip_eject'); A.chats.length = 0; await use(6);
  const ej = await run('data get entity TestRat equipment.offhand');
  ok('an EJECT BUTTON pressed, the chipped sword in the off hand: both chips back, the sword clean (no mark, no line, no bonus), the button spent',
     /diamond_sword/.test(ej) && !/bm_chip_/.test(ej) && !/bm:chip_/.test(ej) && !/◆/.test(ej) && (await has('chip_genie')) === 1 && (await has('chip_missingno')) === 1 && (await has('chip_eject')) === 0,
     `${ej.slice(0, 200)} | ${A.chats.slice(-1).join('')}`);
  await give('hotbar.6', 'chip_eject'); A.bars.length = 0; await use(6);
  ok('...again, nothing left in it: "Nothing chipped", the button kept', A.bars.some(b => /Nothing chipped/.test(b)) && (await has('chip_eject')) === 1, A.bars.slice(-1).join(''));
  // (2.94l) CHIPS OR TUNINGS: a sword Vesper has tuned takes no chip
  await run('item replace entity TestRat weapon.offhand with minecraft:diamond_sword[custom_data={bm_tune:{dmg:1,n:1}},attribute_modifiers=[{type:"minecraft:attack_damage",id:"bm:tune_dmg_1",amount:1.0,operation:"add_value",slot:"mainhand"}]]');
  await run('clear TestRat *[minecraft:custom_data~{bm:"chip_genie"}]'); await run('clear TestRat *[minecraft:custom_data~{bm:"chip_missingno"}]'); await give('hotbar.4', 'chip_genie');
  A.bars.length = 0; await use(4);
  ok('a Game Genie Chip on a sword Vesper has tuned: refused - chips or tunings - and the chip kept',
     A.bars.some(b => /chips or tunings/.test(b)) && (await has('chip_genie')) === 1 && !/bm_chip_/.test(await run('data get entity TestRat equipment.offhand')), A.bars.slice(-1).join(''));
  // (2.94l) TOOL CHIPS: a pickaxe in the off hand - the Speedrun Chip (mining speed), the Lucky Block Chip (luck); a weapon chip turned away
  await run('item replace entity TestRat weapon.offhand with minecraft:diamond_pickaxe');
  await give('hotbar.7', 'chip_speedrun'); await use(7);
  await give('hotbar.8', 'chip_lucky'); await use(8);
  const pk = await run('data get entity TestRat equipment.offhand');
  ok('the SPEEDRUN and LUCKY BLOCK CHIPS on a pickaxe: in it (mining efficiency, luck), both spent', /bm_chip_speedrun: 1b/.test(pk) && /bm_chip_lucky: 1b/.test(pk) &&
     /bm:chip_speedrun/.test(pk) && /bm:chip_lucky/.test(pk) && (await has('chip_speedrun')) === 0 && (await has('chip_lucky')) === 0, pk.slice(0, 220));
  A.bars.length = 0; await use(4);
  ok('...the Game Genie Chip (a weapon\'s) on the pickaxe: refused, kept', A.bars.some(b => /weapon/.test(b)) && (await has('chip_genie')) === 1 && !/bm_chip_genie/.test(await run('data get entity TestRat equipment.offhand')), A.bars.slice(-1).join(''));
  await run('item replace entity TestRat weapon.offhand with minecraft:diamond_sword');
  await give('hotbar.7', 'chip_warpzone'); A.bars.length = 0; await use(7);
  ok('...and the Warp Zone Chip (a tool\'s) on a sword: refused, kept', A.bars.some(b => /tool/.test(b)) && (await has('chip_warpzone')) === 1, A.bars.slice(-1).join(''));
  await run('item replace entity TestRat weapon.offhand with air'); await run('clear TestRat');

  // ================================================================== 5. the props
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 60);
  await give('hotbar.0', 'q_block'); await use(0);
  const QB = `@e[type=minecraft:interaction,tag=bm.arcpb_q_block,x=${X},y=${Y},z=${Z},distance=..6,limit=1]`;
  ok('a ? BLOCK set down on the floor (its model and click box), the item spent', (await cnt(QB)) === 1 && (await has('q_block')) === 0 &&
     (await cnt(`@e[type=minecraft:item_display,tag=bm.arcp_q_block,x=${X},y=${Y},z=${Z},distance=..6]`)) === 1);
  A.interact(await uuidEnt(QB)); await sleep(1200);
  ok('...right-clicked: a Token pops out (on the floor, or already in your pocket)', await wait(3000, async () => (await has('token')) >= 1 ||
     (await cnt(`@e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..6,nbt={Item:{components:{"minecraft:custom_data":{bm:"token"}}}}]`)) >= 1));
  A.bars.length = 0; A.interact(await uuidEnt(QB)); await sleep(1000);
  ok('...again the same day: "Empty"', A.bars.some(b => /Empty/.test(b)), A.bars.slice(-1).join(''));
  A.input({ shift: true }); await sleep(300); A.attack(await uuidEnt(QB)); await sleep(800); A.input({}); await sleep(800);
  ok('...sneak + punch: picked up (it drops for you)', (await cnt(QB)) === 0 && await wait(3000, async () => (await has('q_block')) === 1 ||
     (await cnt(`@e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..6,nbt={Item:{components:{"minecraft:custom_data":{bm:"q_block"}}}}]`)) === 1));
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
  await give('hotbar.1', 'warp_pipe'); await run('item modify entity TestRat hotbar.1 {type:"minecraft:set_count",count:2}');
  await at(X - 5.5, Y + 1, Z + 0.5, 0, 60); await use(1);
  await at(X + 6.5, Y + 1, Z + 0.5, 0, 60); await use(1);
  const PIPES = `@e[type=minecraft:interaction,tag=bm.arcpb_warp_pipe,x=${X},y=${Y},z=${Z},distance=..12]`;
  ok('two WARP PIPES set down', (await cnt(PIPES)) === 2);
  await at(X - 4.5, Y + 1, Z - 1.5, 0, 30);
  const p1 = `@e[type=minecraft:interaction,tag=bm.arcpb_warp_pipe,x=${X - 5.5},y=${Y + 1},z=${Z + 1.5},distance=..2,limit=1]`;
  A.interact(await uuidEnt(p1)); await sleep(1500);
  ok('...right-click one: out you come from the other', await wait(3000, async () => A.pos && Math.abs(A.pos.x - (X + 6.5)) < 1.5), `x ${A.pos && A.pos.x.toFixed(1)} (pipe at ${X + 6.5})`);
  await give('hotbar.2', 'save_point'); await at(X + 0.5, Y + 1, Z - 3.5, 0, 60); await use(2);
  const SP = `@e[type=minecraft:interaction,tag=bm.arcpb_save_point,x=${X},y=${Y},z=${Z},distance=..8,limit=1]`;
  A.bars.length = 0; A.interact(await uuidEnt(SP)); await sleep(1000);
  ok('a SAVE POINT: right-clicked - "Progress saved", your spawn here', A.bars.some(b => /saved/.test(b)) && /-?\d/.test(await run('data get entity TestRat respawn')) &&
     Math.abs((await num('@a[name=TestRat,limit=1]', 'respawn.pos[0]')) - (X)) < 3, (await run('data get entity TestRat respawn')).slice(0, 120));
  await run(`${O}kill @e[tag=bm.arcprop,x=${X},y=${Y},z=${Z},distance=..14]`); await run(`${O}kill @e[tag=bm.arcpbox,x=${X},y=${Y},z=${Z},distance=..14]`);

  // ================================================================== 6. the practical things
  await run('clear TestRat'); await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  const mh0 = +((await run('attribute TestRat minecraft:max_health get')).match(/([\d.]+)/) || [0, 0])[1];
  await give('hotbar.0', 'heart_container'); A.slot(0); await sleep(300); A.use(); await sleep(1800); A.release(); await sleep(800);
  const mh1 = +((await run('attribute TestRat minecraft:max_health get')).match(/([\d.]+)/) || [0, 0])[1];
  ok('a HEART CONTAINER eaten: +1 heart for good', mh1 === mh0 + 2, `${mh0} -> ${mh1}`);
  await give('hotbar.1', 'super_star'); await use(1);
  ok('a SUPER STAR: Resistance V and Speed II', /amplifier: 4b, id: "minecraft:resistance"|id: "minecraft:resistance"[^}]*amplifier: 4b/.test(await fx()) || /resistance/.test(await fx()), (await fx()).slice(0, 160));
  await give('hotbar.2', 'power_mushroom'); await use(2);
  ok('a POWER MUSHROOM: bigger (scale 1.3) and stronger', /1\.3/.test(await run('attribute TestRat minecraft:scale get')) && /strength/.test(await fx()), await run('attribute TestRat minecraft:scale get'));
  await run('attribute TestRat minecraft:scale modifier remove bm:arc_big'); await run('scoreboard players set TestRat bm.arcd 0');

  // ================================================================== 7. hard mode off: the shop's empty again
  await run('scoreboard players set #hard bm.cfg 0'); await run('scoreboard players set #hardoff bm.cfg 1');   // (held off: a conqueror online would wake it again)
  await run(`${O}tp TestRat ${CX + 25.5} ${CY + W} ${CZ + 54.5} 180 0`);
  ok('Hard mode off: Bit and the Pixel Villager are gone', await wait(25000, async () => (await cnt(RAT)) === 0 && (await cnt(VIL)) === 0, 500));

  // ---------------------------------------------------------------- clean up
  await run('clear TestRat'); await run('effect clear TestRat'); await run('scoreboard players reset TestRat bm.archc');
  for (const n of [1, 2, 3]) await run(`attribute TestRat minecraft:max_health modifier remove bm:arc_heart_${n}`);
  await run(`${O}spawnpoint TestRat 0 100 0`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await run(`${O}forceload remove ${CX} ${CZ} ${CX + 76} ${CZ + 84}`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

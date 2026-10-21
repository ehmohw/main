// 2.86: ASHUR, THE FIRE FOLLOWER - the owner's checklist, as a regular (non-op) player, every step a real packet (rcon sets the
// stage: sand, the items, her in the wild): met in the hot country - asked for something to burn, won with coal (her Cinder,
// the advancement, she comes); her menu (Sit / follow, Send her home, Ashur's ways, Wardrobe; her Heat); sat from the menu and
// stood by a right-click; she fights - a fireball (burning, Heat rising), the Flamethrower on two, the Eruption (you warded);
// Blue Flame worn and kept across a send-home and a call, put back; her aura; her Raid Contract signed; the wheel lists her;
// the Cinder in a frame (she climbs out, punched out she goes); a display case (her figurine); Cecil's doll bought in a real
// trade, set down, twirled, picked up; knocked out - she faints, two minutes on the Cinder.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const num = async (sel, path) => +(((await nbt(sel, path)).match(/(-?[\d.]+)/) || [0, NaN])[1]);
  const score = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const tags = async () => (await run('tag TestRat list'));
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const hold = async (slot, ms = 1600) => { A.slot(slot); await sleep(250); A.use(); await sleep(ms); A.release(); await sleep(400); };
  const sneakMenu = async (slot) => { const n0 = A.dialogN.length; await use(slot, true); await wait(3000, async () => A.dialogN.length > n0); return A.dialogN.length > n0; };
  const dd = (d) => d && (d.data || d);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };

  const X = 16660, Y = 100, Z = 16000;
  const PET = '@e[type=minecraft:wolf,tag=bm.aspet,tag=!bm.ffpet,limit=1]';
  const BODY = '@e[type=minecraft:item_display,tag=bm.asp_pet,tag=bm.asp_body,tag=!bm.asfade,limit=1]';
  const model = async (sel = BODY) => (await nbt(sel, 'item.components."minecraft:item_model"')).replace(/"/g, '');
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.aspet]'); await run('kill @e[type=minecraft:interaction,tag=bm.asenc]'); await run('kill @e[type=minecraft:item_display,tag=bm.asencp]');
  for (const o of ['bm.ascd', 'bm.cosas', 'bm.wuashur']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const t of ['bm.auown_ashur', 'bm.au_ashur']) await run(`tag TestRat remove ${t}`);
  await run('advancement revoke TestRat only bm:met/ashur'); await run('advancement revoke TestRat only bm:story/ashur_friend');
  const BIT = +require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p185/sign.mcfunction', 'utf8').match(/scoreboard players add @s bm\.fcon (\d+)/)[1];
  const fc = await score('bm.fcon'); if (fc > 0 && Math.floor(fc / BIT) % 2 === 1) await run(`scoreboard players set TestRat bm.fcon ${fc - BIT}`);   // (unsigned, for the contract step)
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);

  // ---------------------------------------------------------------- finding her: the encounter, won with coal
  await run(`${O}execute positioned ${X + 0.5} ${Y + 1} ${Z + 4.5} rotated 0 0 run function bm:p185/enc/spawn`); await sleep(1500);   // (admin/ashur_meet finds the ground under the sky - below this floating floor)
  const ENC = '@e[type=minecraft:interaction,tag=bm.asenc,limit=1]';
  ok('(staged) Ashur met out in the hot country: her rig (ten parts) and a click box', (await cnt(ENC)) === 1 && (await cnt('@e[type=minecraft:item_display,tag=bm.asencp]')) === 10);
  const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
  await at(ex + 0.5, Y + 1, ez - 2, 0, 20);
  let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250); A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(900);
  ok('right-clicked empty-handed: she asks for something to burn', A.bars.some(b => /something to burn/.test(b)), A.bars.slice(-1).join(''));
  await run('item replace entity TestRat hotbar.8 with minecraft:coal 2'); await sleep(300);
  await sleep(700); A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
  ok('right-clicked holding coal: she joins - one coal eaten, her Cinder given, the advancement', (await has('ashur_cinder')) === 1 &&
     /Count: 1|1 coal/i.test(await run('clear TestRat minecraft:coal 0')) || /Found 1/.test(await run('clear TestRat minecraft:coal 0')), A.chats.slice(-2).join(' | ').slice(0, 200));
  ok('...the encounter gone, and she comes along (her rig, her own)', (await cnt(ENC)) === 0 && await wait(3000, async () => (await cnt(PET)) === 1) &&
     (await score('bm.pid', PET)) === (await score('bm.pid')));
  ok('..."Feed the Fire", and she\'s met', (await cnt('@a[name=TestRat,advancements={bm:story/ashur_friend=true,bm:met/ashur=true}]')) === 1);
  await run('clear TestRat minecraft:coal');
  if (process.env.DBG) { A.chats.length = 0; for (let i = 0; i < 12; i++) { await sleep(500); console.log('dbg', i, await cnt(PET), await score('bm.fmis', PET), await score('bm.pid', PET)); } console.log(A.chats.join('\n')); }
  const slot0 = await (async () => { for (let i = 0; i < 9; i++) if (/ashur_cinder/.test(await run(`data get entity TestRat Inventory[{Slot:${i}b}]`))) return i; return -1; })();
  if (slot0 !== 0) { await run('clear TestRat *[minecraft:custom_data~{bm:"ashur_cinder"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/ashur_cinder'); }
  const kit = [null, 'cos_ashur_1', 'cos_aura_ashur', 'fcontract_ashur'];
  for (let i = 1; i < kit.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${kit[i]}`);
  await sleep(800);

  // ---------------------------------------------------------------- UI: her menu
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  A.bars.length = 0; await use(0); await sleep(1500);
  ok('the Cinder used while she\'s out: she\'s called over ("Coming!")', A.bars.some(b => /Coming!/.test(b)) && (await cnt(PET)) === 1, A.bars.slice(-1).join(''));
  ok('...her rig: ten parts, 40 health', (await cnt('@e[type=minecraft:item_display,tag=bm.asp_pet,tag=!bm.asfade]')) === 10 &&
     (await num(PET, 'attributes[{id:"minecraft:max_health"}].base')) === 40);
  ok('sneak + use: her menu', await sneakMenu(0));
  const labels = A.buttons().map(b => b.label);
  ok('...Sit / follow, Send her home, Ashur\'s ways, Wardrobe', ['Sit / follow', 'Send her home', "Ashur's ways", 'Wardrobe'].every(l => labels.some(x => x.includes(l))), labels.join(' | '));
  const bodyTxt = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]).body || []);
  ok('...her Heat shown', /Heat/.test(bodyTxt) && /of 10/.test(bodyTxt), bodyTxt.slice(0, 160));
  let pr = await A.press(/Ashur's ways/);
  const pw = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]).body || []);
  ok('her menu -> Ashur\'s ways: Heat, Flamethrower, Eruption, Hearthwarmth', pr && pr.next && ['Heat', 'Flamethrower', 'Eruption', 'Hearthwarmth'].every(w => pw.includes(w)), pw.slice(0, 160));
  await sleep(2200);                                         // (the item-use debounce from opening her menu)

  // ---------------------------------------------------------------- sitting: menu and right-click
  await sneakMenu(0); A.bars.length = 0; await A.press(/Sit \/ follow/); await sleep(1500);
  ok('Sit / follow: she sits', /1b/.test(await nbt(PET, 'Sitting')) && A.bars.some(b => /I'll sit/.test(b)), A.bars.slice(-1).join(''));
  await wait(3000, async () => (await score('bm.azs', PET)) === 4);
  ok('...her seated cycle plays (state 4)', (await score('bm.azs', PET)) === 4);
  const seen = new Set(); for (let k = 0; k < 14; k++) { seen.add(await nbt('@e[type=minecraft:item_display,tag=bm.asp_pet,tag=bm.asp_legr,limit=1]', 'transformation')); await sleep(250); }
  ok('...and moves while she sits (sit_a -> sit_b)', seen.size >= 2, `${seen.size} distinct`);
  const hitSel = '@e[type=minecraft:interaction,tag=bm.ashit,limit=1]';
  await wait(3000, async () => (await cnt(hitSel)) === 1);
  const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');
  await at(wx + 0.5, Y + 1, wz - 1.5, 0, 30);
  A.slot(8); await sleep(300); let hb = await entOf(hitSel);
  A.bars.length = 0; if (hb) A.interact(hb.entityId); await sleep(1000);
  ok('right-clicked: she stands', !!hb && /0b/.test(await nbt(PET, 'Sitting')) && A.bars.some(b => /burn/.test(b)), A.bars.slice(-1).join(''));

  // ---------------------------------------------------------------- she fights: Heat, the flamethrower, the Eruption
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0); await sleep(800);
  const zom = (dx, dz, t) => run(`${O}summon minecraft:husk ${X + dx} ${Y + 1} ${Z + dz} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t234z","${t}","bm.seen"],attributes:[{id:"minecraft:max_health",base:300}],Health:300f}`);
  await run(`scoreboard players set ${PET} bm.azgc 900`); await run(`scoreboard players set ${PET} bm.azbc 900`);
  await zom(9, 0, 'bm.t234a');
  ok('a foe 8 blocks off: a fireball - it burns and is hurt', await wait(6000, async () => (await num('@e[tag=bm.t234a,limit=1]', 'Health')) < 300) &&
     (await num('@e[tag=bm.t234a,limit=1]', 'Fire')) > 0);
  ok('...her Heat rises', await wait(3000, async () => (await score('bm.azh', PET)) >= 1), `heat ${await score('bm.azh', PET)}`);
  await zom(4, 2, 'bm.t234b'); await run(`${O}execute at ${PET} run tp @e[tag=bm.t234a] ~2 ~ ~1`); await run(`${O}execute at ${PET} run tp @e[tag=bm.t234b] ~-1 ~ ~2`); await run(`scoreboard players set ${PET} bm.azbc 0`);
  let blast = false; await wait(9000, async () => (blast = blast || (await score('bm.azs', PET)) === 9) && false, 100);
  ok('two foes near: the Flamethrower (her blast pose, its cooldown)', blast || (await score('bm.azbc', PET)) > 0, `bc ${await score('bm.azbc', PET)}`);
  await run(`scoreboard players set ${PET} bm.azgc 0`); await run(`${O}execute at ${PET} run tp @e[tag=bm.t234b] ~2 ~ ~`);
  A.chats.length = 0; A.bars.length = 0;
  ok('a foe close, the charge ready: the ERUPTION', await wait(8000, async () => A.bars.some(b => /ERUPTION/.test(b))), A.bars.slice(-1).join(''));
  ok('...and you warded against fire', /fire_resistance/.test(await run('data get entity TestRat active_effects')));
  await run(`${O}kill @e[tag=bm.t234z]`); await sleep(500);

  // ---------------------------------------------------------------- cosmetics: Blue Flame, kept across a recall; her aura
  await hold(1); await sleep(800);
  ok('Blue Flame used while she\'s out: picked (bm.cosas 1) and worn (as_body_c1)', (await score('bm.cosas')) === 1 && /as_body_c1$/.test(await model()), await model());
  await sneakMenu(0); A.bars.length = 0; await A.click(/Send her home/); await sleep(1500);
  ok('Send her home: she goes', (await cnt(PET)) === 0 && A.bars.some(b => /burning/.test(b)), A.bars.slice(-1).join(''));
  await sneakMenu(0);
  ok('...her menu now says Call for Ashur', A.buttons().some(b => /Call for Ashur/.test(b.label)) && !A.buttons().some(b => /Send her home/.test(b.label)));
  await A.click(/Call for Ashur/); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('...called from the menu: back, still in Blue Flame', (await cnt(PET)) === 1 && /as_body_c1$/.test(await model()), await model());
  await sneakMenu(0); const w1 = await A.press(/Wardrobe/);
  ok('her menu -> Wardrobe: her dresses', w1 && w1.next && ['Her own magma', 'Blue Flame', 'Verdant Ember', 'Obsidian Rose'].every(l => A.buttons().some(b => b.label.includes(l))),
     A.buttons().map(b => b.label).join(' | '));
  await A.press(/Her own magma/); await sleep(1000);
  ok('"Her own magma": back to her own (as_body)', /^bm:as_body$/.test(await model()) && (await score('bm.cosas')) === 0, await model());
  await sleep(2200); A.chats.length = 0; await hold(2); await sleep(600);
  ok('Ashfall Crown (her rare aura) used: hers for good, and on', /bm\.auown_ashur/.test(await tags()) && /bm\.au_ashur\b/.test(await tags()), await tags());

  // ---------------------------------------------------------------- her Raid Contract
  await sleep(2200);
  const fc0 = await score('bm.fcon');
  A.chats.length = 0; await hold(3); await sleep(600);
  ok('her Raid Contract used: signed, the contract gone', Math.floor((await score('bm.fcon')) / BIT) % 2 === 1 && (await score('bm.fcon')) > fc0 && (await has('fcontract_ashur')) === 0 && A.chats.some(c => /Signed!/.test(c)),
     A.chats.slice(-1).join('').slice(0, 160));
  const rec = require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p137/rc/main.mcfunction', 'utf8');
  ok('...and the Recruiter sells it', /fcontract_ashur/.test(rec));

  // ---------------------------------------------------------------- the partner wheel knows her
  const wheel = require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p179/w/open.mcfunction', 'utf8');
  ok('the Partner Wheel lists her', /Ashur/.test(wheel) || require('child_process').execSync('grep -rl "p185/try_summon" /home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p179 | head -1').toString().length > 0);

  // ---------------------------------------------------------------- frame gimmick
  await sneakMenu(0); await A.click(/Send her home/); await sleep(1200);
  await run(`${O}fill ${X - 6} ${Y + 1} ${Z + 5} ${X + 6} ${Y + 3} ${Z + 5} minecraft:stone`);
  await run(`${O}summon minecraft:item_frame ${X} ${Y + 2} ${Z + 4} {Facing:2b,Tags:["bm.t234f"]}`); await sleep(400);
  await at(X + 0.5, Y + 1, Z + 2.5, 0, -10);
  const frSel = '@e[type=minecraft:item_frame,tag=bm.t234f,limit=1]';
  let fr = null; await wait(4000, async () => (fr = await entOf(frSel)) != null, 250);
  A.slot(0); await sleep(300); A.bars.length = 0; if (fr) A.interact(fr.entityId); await sleep(2800);
  const FPET = `@e[type=minecraft:wolf,tag=bm.aspet,tag=bm.ffpet,x=${X},y=${Y + 2},z=${Z + 4},distance=..10]`;
  ok('the Cinder in a frame: Ashur climbs out (and makes herself at home)', (await cnt(FPET)) === 1 && A.bars.some(b => /Ashur climbs out of the frame.*herself/.test(b)), A.bars.slice(-1).join(''));
  if (fr) A.attack(fr.entityId); await sleep(600);
  ok('the Cinder punched out of the frame: she goes with it', await wait(3000, async () => (await cnt(FPET)) === 0));
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y + 2},z=${Z + 4},distance=..4]`); await run(`${O}kill ${frSel}`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"ashur_cinder"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/ashur_cinder');

  // ---------------------------------------------------------------- display case: her figurine
  await at(X - 4.5, Y + 1, Z - 4.5, 0, 70);
  await run('loot replace entity TestRat hotbar.5 loot bm:items/display_case_oak'); await use(5);
  const caseSel = `@e[type=minecraft:interaction,tag=bm.dchit,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..1.5,limit=1]`;
  ok('a display case set down', (await cnt(caseSel)) === 1);
  const FIG = `@e[type=minecraft:item_display,tag=bm.dcfg,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..2]`;
  let box = await entOf(caseSel); A.slot(0); await sleep(300); if (box) A.interact(box.entityId); await sleep(800);
  const nfig = await cnt(FIG);
  ok('the Cinder right-clicked into it: a little Ashur (her parts, flames hidden), shrunk to fit', nfig >= 8 && nfig <= 10, `parts ${nfig}`);
  const ys = []; for (let k = 0; k < 10; k++) ys.push(await num(`${FIG.slice(0, -1)},limit=1,sort=random]`, 'transformation.translation[1]'));
  ok('...standing on the cushion, inside the glass', Math.min(...ys) >= -0.01 && Math.max(...ys) < 0.62, `translation y ${Math.min(...ys).toFixed(2)}..${Math.max(...ys).toFixed(2)}`);
  A.slot(8); await sleep(250); box = await entOf(caseSel); if (box) A.interact(box.entityId); await sleep(700);
  ok('...empty-handed: the Cinder back out, the figurine gone', (await has('ashur_cinder')) === 1 && (await cnt(FIG)) === 0);
  await run('clear TestRat *[minecraft:custom_data~{bm:"ashur_cinder"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/ashur_cinder');
  A.input({ shift: true }); await sleep(250); box = await entOf(caseSel); if (box) A.attack(box.entityId); await sleep(700); A.input({}); await sleep(300);
  await run(`${O}kill @e[type=minecraft:item,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..3]`);

  // ---------------------------------------------------------------- Cecil's doll of her: a real trade
  await run(`${O}execute positioned ${X + 5.5} ${Y + 1} ${Z - 3.5} rotated 180 0 run function bm:p45/cecil/spawn`); await sleep(1500);
  const CEC = `@e[type=minecraft:villager,tag=bm.npc_wizard,x=${X + 5.5},y=${Y + 1},z=${Z - 3.5},distance=..2,limit=1]`;
  await at(X + 5.5, Y + 1, Z - 0.5, 180, 0); await sleep(2500);
  let idx = -1;
  for (let i = 0; i < 80 && idx < 0; i++) { if (/Found no elements/i.test(await nbt(CEC, `Offers.Recipes[${i}].maxUses`))) break; const s = await nbt(CEC, `Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`); if (/"doll_ashur"/.test(s)) idx = i; }
  ok('Cecil sells the Ashur doll', idx >= 0, `trade #${idx}`);
  const price = +(((await nbt(CEC, `Offers.Recipes[${idx}].buy.count`)).match(/(\d+)/) || [0, 0])[1]);
  const buyId = (await nbt(CEC, `Offers.Recipes[${idx}].buy.components."minecraft:custom_data".bm`)).replace(/"/g, '');
  for (let i = 0; i < price; i++) await run(`loot give TestRat loot bm:items/${buyId}`);
  const cec = await entOf(CEC); A.windows.length = 0; if (cec) A.interact(cec.entityId); await sleep(900);
  const w = A.windows[A.windows.length - 1];
  if (w && idx >= 0) {
    A.write('select_trade', { slot: idx }); await sleep(300);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(500);
    A.close(w.windowId); await sleep(400);
  }
  ok(`...bought in his window`, (await has('doll_ashur')) === 1, `dolls ${await has('doll_ashur')}`);
  await run(`${O}kill ${CEC}`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"doll_ashur"}]'); await run('loot replace entity TestRat hotbar.6 loot bm:items/doll_ashur');
  await at(X + 2.5, Y + 1, Z - 4.5, 180, 45); A.slot(6); await sleep(200); A.use(); await sleep(350); A.release(); await sleep(600);
  const DD = `@e[type=minecraft:item_display,tag=bm.doll_ashurd,x=${X + 2.5},y=${Y + 1},z=${Z - 6.5},distance=..0.4,limit=1]`;
  const DH = `@e[type=minecraft:interaction,tag=bm.doll_ashurhit,x=${X + 2.5},y=${Y + 1},z=${Z - 6.5},distance=..0.4,limit=1]`;
  ok('the doll set down on a block: her own model', (await cnt(DD)) === 1 && /doll_ashur/.test(await nbt(DD, 'item.components')));
  const y0 = await num(DD, 'Rotation[0]'); let dh = await entOf(DH); if (dh) A.interact(dh.entityId); await sleep(700);
  ok('...right-clicked: it twirls', Math.abs(((await num(DD, 'Rotation[0]') - y0 + 540) % 360) - 180) > 30);
  A.input({ shift: true }); await sleep(250); dh = await entOf(DH); if (dh) A.attack(dh.entityId); await sleep(700); A.input({}); await sleep(300);
  ok('...sneak + punch: back in the pack', (await has('doll_ashur')) === 1 && (await cnt(DD)) === 0);

  // ---------------------------------------------------------------- knocked out: she faints
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  A.chats.length = 0; await run(`${O}damage ${PET} 200 minecraft:mob_attack`);
  ok('struck down: she faints, her rig fades away', await wait(4000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.asp_pet]')) === 0));
  ok('..."Ashur faints!" - two minutes on the Cinder (as every follower, 2.82t)', A.chats.some(c => /Ashur faints!/.test(c)) && (await score('bm.ascd')) > 100, A.chats.slice(-1).join('').slice(0, 160));
  A.bars.length = 0; await use(0); await sleep(800);
  ok('...the Cinder used: "still rekindling", no Ashur', (await cnt(PET)) === 0 && A.bars.some(b => /rekindling/.test(b)), A.bars.slice(-1).join(''));

  // ---------------------------------------------------------------- clean up
  await run('scoreboard players set TestRat bm.ascd 0'); await run('clear TestRat');
  for (const t of ['bm.auown_ashur', 'bm.au_ashur']) await run(`tag TestRat remove ${t}`);
  await run(`${O}kill @e[type=minecraft:wolf,tag=bm.aspet]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

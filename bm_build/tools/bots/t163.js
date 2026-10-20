// 2.79: FISHY, THE FOLLOWER - the owner's checklist, as a regular (non-op) player, every step a real packet (rcon sets the
// stage: a floor, a wall, the items): his Pocket Bowl used - he comes (his rig, a poor fighter: 30 health, a 1-point claw);
// sneak + use - his menu (Sit / follow, Send him home, The Cabinet, Fishy's powers, Wardrobe); sat down from the menu and by a
// right-click on him (his seated cycle plays), up again; the Cabinet and his powers from his menu; his wardrobe - a top hat
// used while he's out (his rig wears it), kept across a send-home and a call, put back; his aura (locked, used, on, off);
// his Raid Contract signed (he's met); the bowl in an item frame - he climbs out, punched out - he goes; a display case -
// his figurine (nine parts), out again; Cecil's doll of him bought in a real trade, set down, twirled, picked up; knocked
// out - he faints, five minutes before the bowl calls him again. Then, as an admin, every wing filled - the Golden Bowl:
// gilded limbs, 130 health, and the Grand Exhibition on the first foe.
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
  const X = 16580, Y = 100, Z = 16000;
  const PET = '@e[type=minecraft:wolf,tag=bm.fypet,tag=!bm.ffpet,limit=1]';
  const BODY = '@e[type=minecraft:item_display,tag=bm.fyp_pet,tag=bm.fyp_body,tag=!bm.fyfade,limit=1]';
  const model = async (sel = BODY) => (await nbt(sel, 'item.components."minecraft:item_model"')).replace(/"/g, '');
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.fypet]'); await run('function bm:admin/cabinet_reset');
  for (const o of ['bm.fycd', 'bm.cosfy', 'bm.wufishy']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const t of ['bm.auown_fishy', 'bm.au_fishy']) await run(`tag TestRat remove ${t}`);
  await run('advancement revoke TestRat only bm:met/fishy');
  const fc = await score('bm.fcon'); if (fc > 0 && Math.floor(fc / 1024) % 2 === 1) await run(`scoreboard players set TestRat bm.fcon ${fc - 1024}`);
  await run('tag TestRat add bm.fyfc');          // (his free contract counted as given - the kit carries one; t162 checks the free one)
  await sleep(1200);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  const kit = ['fy_bowl', 'cos_fishy_2', 'cos_aura_fishy', 'fcontract_fishy'];
  for (let i = 0; i < kit.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${kit[i]}`);
  await sleep(1500);
  ok('the Pocket Bowl in his pocket: Fishy is met (his Raid Contract can be signed)', await wait(3000, async () => (await cnt('@a[name=TestRat,advancements={bm:met/fishy=true}]')) === 1));

  // ---------------------------------------------------------------- UI: called, his menu
  A.chats.length = 0; A.bars.length = 0; await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('the bowl used: Fishy comes - his rig (nine parts), a tame wolf under it, his own', (await cnt(PET)) === 1 && (await cnt('@e[type=minecraft:item_display,tag=bm.fyp_pet,tag=!bm.fyfade]')) === 9 &&
     (await score('bm.pid', PET)) === (await score('bm.pid')));
  ok('..."Fishy, curator, at your service!"', A.bars.some(b => /curator, at your service/.test(b)), A.bars.slice(-1).join(''));
  ok('...a poor fighter for now: 30 health, a 1-point claw, armour 4', (await num(PET, 'attributes[{id:"minecraft:max_health"}].base')) === 30 &&
     (await num(PET, 'attributes[{id:"minecraft:attack_damage"}].base')) === 1 && (await num(PET, 'attributes[{id:"minecraft:armor"}].base')) === 4);
  ok('...still in his bowl: the bowl stays in the hand', (await has('fy_bowl')) === 1);
  ok('sneak + use: his menu', await sneakMenu(0));
  const labels = A.buttons().map(b => b.label);
  ok('...Sit / follow, Send him home, The Cabinet, Fishy\'s powers, Wardrobe', ['Sit / follow', 'Send him home', 'The Cabinet', "Fishy's powers", 'Wardrobe'].every(l => labels.some(x => x.includes(l))),
     labels.join(' | '));

  // ---------------------------------------------------------------- sitting: from the menu, by a right-click on him
  A.bars.length = 0; A.click(/Sit \/ follow/); await sleep(1500);
  ok('Sit / follow: he sits ("I shall rest my legs here")', /1b/.test(await nbt(PET, 'Sitting')) && A.bars.some(b => /rest my legs/.test(b)), A.bars.slice(-1).join(''));
  await wait(3000, async () => (await score('bm.fys', PET)) === 4);
  ok('...his seated cycle plays (state 4)', (await score('bm.fys', PET)) === 4, `${await score('bm.fys', PET)}`);
  const seen = new Set(); for (let k = 0; k < 12; k++) { seen.add(await nbt('@e[type=minecraft:item_display,tag=bm.fyp_pet,tag=bm.fyp_fish,limit=1]', 'transformation')); await sleep(250); }
  ok('...and moves while he sits (sit -> sit_b and back)', seen.size >= 2, `${seen.size} distinct`);
  const hitSel = '@e[type=minecraft:interaction,tag=bm.fyhit,limit=1]';
  await wait(3000, async () => (await cnt(hitSel)) === 1);
  const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');                  // (walk up to him)
  await at(wx + 0.5, Y + 1, wz - 1.5, 0, 30);
  A.slot(8); await sleep(300); let hb = await entOf(hitSel);
  A.bars.length = 0; if (hb) A.interact(hb.entityId); await sleep(1000);
  ok('right-clicked empty-handed: he stands ("Onward!")', !!hb && /0b/.test(await nbt(PET, 'Sitting')) && A.bars.some(b => /Onward/.test(b)), hb ? A.bars.slice(-1).join('') : 'no click box seen');
  hb = await entOf(hitSel); if (hb) A.interact(hb.entityId); await sleep(1000);
  ok('...right-clicked again: he sits', /1b/.test(await nbt(PET, 'Sitting')));
  hb = await entOf(hitSel); if (hb) A.interact(hb.entityId); await sleep(800);

  // ---------------------------------------------------------------- the Cabinet and his powers, from his menu
  await sneakMenu(0); let pr = await A.press(/The Cabinet/);
  ok('his menu -> The Cabinet: the Cabinet\'s menu', pr && pr.next && /CABINET OF CURIOSITIES/.test(JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]).title)));
  await sneakMenu(0); pr = await A.press(/Fishy's powers/);
  const pw = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]).body || []);
  ok('his menu -> Fishy\'s powers: every one already his, at 20% (nothing shown yet) - the Grand Exhibition too; the Golden Bowl not yet',
     pr && pr.next && (pw.match(/20%/g) || []).length >= 7 && /Grand Exhibition/.test(pw) && /Golden Bowl/.test(pw) && /not yet/.test(pw), pw.slice(0, 160));

  // ---------------------------------------------------------------- cosmetics: a top hat, kept across a recall, put back
  await hold(1); await sleep(800);
  ok('Crimson Opera used while he\'s out: picked (bm.cosfy 2) and worn (fy_body_c2)', (await score('bm.cosfy')) === 2 && /fy_body_c2$/.test(await model()), await model());
  ok('...his hat and fish too', /_c2$/.test(await model('@e[type=minecraft:item_display,tag=bm.fyp_pet,tag=bm.fyp_fish,limit=1]')));
  await sneakMenu(0); A.bars.length = 0; await A.click(/Send him home/); await sleep(1500);
  ok('Send him home: he goes ("Back to the Cabinet")', (await cnt(PET)) === 0 && A.bars.some(b => /Back to the Cabinet/.test(b)), A.bars.slice(-1).join(''));
  await sneakMenu(0);
  ok('...his menu now says Call for Fishy', A.buttons().some(b => /Call for Fishy/.test(b.label)) && !A.buttons().some(b => /Send him home/.test(b.label)));
  await A.click(/Call for Fishy/); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('...called from the menu: back, still in Crimson Opera', (await cnt(PET)) === 1 && /fy_body_c2$/.test(await model()), await model());
  await sneakMenu(0); const w1 = await A.press(/Wardrobe/);
  ok('his menu -> Wardrobe: his top hats', w1 && w1.next && ['His old black topper', 'Midnight Silk', 'Crimson Opera', 'Emerald Ascot', 'Gilded Topper'].every(l => A.buttons().some(b => b.label.includes(l))),
     A.buttons().map(b => b.label).join(' | '));
  ok('...Crimson Opera: wearing; Midnight Silk: locked', A.buttons().some(b => /Crimson Opera.*wearing/.test(b.label)) && A.buttons().some(b => /Midnight Silk.*locked/.test(b.label)));
  ok('...the aura row: Bubble Halo - locked', A.buttons().some(b => /Bubble Halo.*locked/.test(b.label)));
  A.chats.length = 0; await A.press(/Bubble Halo/); await sleep(600);
  ok('...pressed while locked: where to find it', A.chats.some(c => /Bubble Halo.*locked/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
  await A.press(/His old black topper/); await sleep(1000);
  ok('"His old black topper": back to his own (fy_body)', /^bm:fy_body$/.test(await model()) && (await score('bm.cosfy')) === 0, await model());

  // ---------------------------------------------------------------- the rare cosmetic: his aura
  A.chats.length = 0; await hold(2); await sleep(600);
  ok('Bubble Halo used: his for good, and on', /bm\.auown_fishy/.test(await tags()) && /bm\.au_fishy\b/.test(await tags()), await tags());
  ok('...everyone hears of it; the item used up', A.chats.some(c => /awakened Bubble Halo/.test(c)) && (await has('cos_aura_fishy')) === 0, A.chats.slice(-1).join(''));
  await sneakMenu(0); await A.press(/Wardrobe/);
  ok('...the wardrobe says on', A.buttons().some(b => /Bubble Halo.*on/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  await A.press(/Bubble Halo/); await sleep(600);
  ok('...switched off there (still his)', !/bm\.au_fishy\b/.test(await tags()) && /bm\.auown_fishy/.test(await tags()), await tags());

  // ---------------------------------------------------------------- his Raid Contract (he's met)
  await sleep(2200);                                         // (the item-use debounce from opening his menu: 1-2 s)
  A.chats.length = 0; await hold(3); await sleep(600);
  ok('his Raid Contract used: signed (the contract bit), the contract gone', Math.floor((await score('bm.fcon')) / 1024) % 2 === 1 && (await has('fcontract_fishy')) === 0 &&
     A.chats.some(c => /Signed!/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
  const rec = require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p137/rc/main.mcfunction', 'utf8');
  ok('...and the Recruiter sells it (his book)', /fcontract_fishy/.test(rec));

  // ---------------------------------------------------------------- frame gimmick: the bowl hung in a frame
  await sneakMenu(0); await A.click(/Send him home/); await sleep(1200);
  await run(`${O}fill ${X - 6} ${Y + 1} ${Z + 5} ${X + 6} ${Y + 3} ${Z + 5} minecraft:stone`);
  await run(`${O}summon minecraft:item_frame ${X} ${Y + 2} ${Z + 4} {Facing:2b,Tags:["bm.t163f"]}`); await sleep(400);
  await at(X + 0.5, Y + 1, Z + 2.5, 0, -10);
  const frSel = `@e[type=minecraft:item_frame,tag=bm.t163f,limit=1]`;
  let fr = null; await wait(4000, async () => (fr = await entOf(frSel)) != null, 250);
  A.slot(0); await sleep(300); A.bars.length = 0; if (fr) A.interact(fr.entityId); await sleep(2800);
  const FPET = `@e[type=minecraft:wolf,tag=bm.fypet,tag=bm.ffpet,x=${X},y=${Y + 2},z=${Z + 4},distance=..10]`;
  ok('the bowl in a frame: Fishy climbs out (and says so)', (await cnt(FPET)) === 1 && A.bars.some(b => /Fishy climbs out of the frame/.test(b)), A.bars.slice(-1).join(''));
  ok('...in his rig, nobody\'s', (await cnt(`@e[type=minecraft:item_display,tag=bm.fyp_body,x=${X},y=${Y + 2},z=${Z + 4},distance=..10]`)) === 1 &&
     (await cnt(`${FPET.slice(0, -1)},scores={bm.pid=${await score('bm.pid')}}]`)) === 0);
  await sleep(6000);
  ok('...still by the frame six seconds on', (await cnt(FPET)) === 1);
  if (fr) A.attack(fr.entityId); await sleep(600);
  ok('the bowl punched out of the frame: he goes with it', await wait(3000, async () => (await cnt(FPET)) === 0 &&
     (await cnt(`@e[type=minecraft:item_display,tag=bm.fyp_body,x=${X},y=${Y + 2},z=${Z + 4},distance=..10]`)) === 0));
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y + 2},z=${Z + 4},distance=..4]`); await run(`${O}kill ${frSel}`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/fy_bowl');

  // ---------------------------------------------------------------- display case: his figurine
  await at(X - 4.5, Y + 1, Z - 4.5, 0, 70);
  await run('loot replace entity TestRat hotbar.5 loot bm:items/display_case_oak'); await use(5);
  const caseSel = `@e[type=minecraft:interaction,tag=bm.dchit,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..1.5,limit=1]`;
  ok('a display case set down', (await cnt(caseSel)) === 1);
  const FIG = `@e[type=minecraft:item_display,tag=bm.dcfg,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..2]`;
  let box = await entOf(caseSel); A.slot(0); await sleep(300); if (box) A.interact(box.entityId); await sleep(800);
  const fs = await num(`${FIG.slice(0, -1)},limit=1]`, 'transformation.scale[0]');
  ok('the bowl right-clicked into it: a little Fishy (nine parts), shrunk to fit', (await cnt(FIG)) === 9 && fs > 0.05 && fs < 0.45, `parts ${await cnt(FIG)} scale ${fs}`);
  const ys = []; for (let k = 0; k < 9; k++) ys.push(await num(`${FIG.slice(0, -1)},limit=1,sort=random]`, 'transformation.translation[1]'));
  ok('...standing on the cushion, inside the glass', Math.min(...ys) >= -0.01 && Math.max(...ys) < 0.62, `translation y ${Math.min(...ys).toFixed(2)}..${Math.max(...ys).toFixed(2)}`);
  A.slot(8); await sleep(250); box = await entOf(caseSel); if (box) A.interact(box.entityId); await sleep(700);
  ok('...empty-handed: the bowl back out, the figurine gone', (await has('fy_bowl')) === 1 && (await cnt(FIG)) === 0);
  await run('clear TestRat *[minecraft:custom_data~{bm:"fy_bowl"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/fy_bowl');   // (it came back to the empty hand)
  A.input({ shift: true }); await sleep(250); box = await entOf(caseSel); if (box) A.attack(box.entityId); await sleep(700); A.input({}); await sleep(300);
  await run(`${O}kill @e[type=minecraft:item,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..3]`);

  // ---------------------------------------------------------------- Cecil's doll of him: a real trade
  await run(`${O}execute positioned ${X + 5.5} ${Y + 1} ${Z - 3.5} rotated 180 0 run function bm:p45/cecil/spawn`); await sleep(1500);
  const CEC = `@e[type=minecraft:villager,tag=bm.npc_wizard,x=${X + 5.5},y=${Y + 1},z=${Z - 3.5},distance=..2,limit=1]`;
  await at(X + 5.5, Y + 1, Z - 0.5, 180, 0); await sleep(2500);   // (2.80b: step up to his counter - a doll shows once its follower is met, to whoever is there)
  let idx = -1;
  for (let i = 0; i < 80 && idx < 0; i++) { if (/Found no elements/i.test(await nbt(CEC, `Offers.Recipes[${i}].maxUses`))) break; const s = await nbt(CEC, `Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`); if (/"doll_fishy"/.test(s)) idx = i; }
  ok('Cecil sells the Fishy doll', idx >= 0, `trade #${idx}`);
  const price = +(((await nbt(CEC, `Offers.Recipes[${idx}].buy.count`)).match(/(\d+)/) || [0, 0])[1]);
  const buyId = (await nbt(CEC, `Offers.Recipes[${idx}].buy.components."minecraft:custom_data".bm`)).replace(/"/g, '');
  for (let i = 0; i < price; i++) await run(`loot give TestRat loot bm:items/${buyId}`);
  await at(X + 5.5, Y + 1, Z - 0.5, 180, 0);
  const cec = await entOf(CEC); A.windows.length = 0; if (cec) A.interact(cec.entityId); await sleep(900);
  const w = A.windows[A.windows.length - 1];
  if (w && idx >= 0) {
    A.write('select_trade', { slot: idx }); await sleep(300);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(500);
    A.close(w.windowId); await sleep(400);
  }
  ok(`...bought in his window for ${price} ${buyId}`, (await has('doll_fishy')) === 1 && (await has(buyId)) === 0, `dolls ${await has('doll_fishy')}`);
  await run(`${O}kill ${CEC}`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"doll_fishy"}]'); await run('loot replace entity TestRat hotbar.6 loot bm:items/doll_fishy');
  await at(X + 2.5, Y + 1, Z - 4.5, 180, 45); A.slot(6); await sleep(200); A.use(); await sleep(350); A.release(); await sleep(600);
  const DD = `@e[type=minecraft:item_display,tag=bm.doll_fishyd,x=${X + 2.5},y=${Y + 1},z=${Z - 6.5},distance=..0.4,limit=1]`;
  const DH = `@e[type=minecraft:interaction,tag=bm.doll_fishyhit,x=${X + 2.5},y=${Y + 1},z=${Z - 6.5},distance=..0.4,limit=1]`;
  ok('the doll set down on a block by a use: his own model', (await cnt(DD)) === 1 && (await has('doll_fishy')) === 0 && /doll_fishy/.test(await nbt(DD, 'item.components')),
     `${await cnt(DD)} ${await cnt(DH)}`);
  const y0 = await num(DD, 'Rotation[0]'); let dh = await entOf(DH); if (dh) A.interact(dh.entityId); await sleep(700);
  const y1 = await num(DD, 'Rotation[0]');
  ok('...right-clicked: it twirls', Math.abs(((y1 - y0 + 540) % 360) - 180) > 30, `${y0} -> ${y1}`);
  A.input({ shift: true }); await sleep(250); dh = await entOf(DH); if (dh) A.attack(dh.entityId); await sleep(700); A.input({}); await sleep(300);
  ok('...sneak + punch: back in the pack', (await has('doll_fishy')) === 1 && (await cnt(DD)) === 0);

  // ---------------------------------------------------------------- knocked out: he faints
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  A.chats.length = 0; await run(`${O}damage ${PET} 200 minecraft:mob_attack`);
  ok('struck down: he faints, his rig fades away', await wait(4000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.fyp_pet]')) === 0));
  ok('..."Fishy faints!" - two minutes on the bowl (2.82t)', A.chats.some(c => /Fishy faints!/.test(c)) && (await score('bm.fycd')) > 100, A.chats.slice(-1).join('').slice(0, 160));
  A.bars.length = 0; await use(0); await sleep(800);
  ok('...the bowl used: "still catching his breath", no Fishy', (await cnt(PET)) === 0 && A.bars.some(b => /catching his breath/.test(b)), A.bars.slice(-1).join(''));
  await run('scoreboard players set TestRat bm.fycd 0');

  // ---------------------------------------------------------------- as an admin: every wing filled - the Golden Bowl
  A.bars.length = 0; A.chats.length = 0; await sleep(600); await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1200);
  ok('called again once he\'s rested', (await cnt(PET)) === 1);
  await run('op TestRat'); await sleep(400); A.cmd('function bm:admin/cabinet_fill'); await sleep(2500); await run('deop TestRat'); await sleep(400);
  ok('(admin) every wing filled: the Golden Bowl (#cap)', (await score('#cap', 'bm.cab')) === 1 || /has 1/.test(await run('scoreboard players get #cap bm.cab')));
  await wait(3000, async () => /fy_body_g$/.test(await model()));
  ok('...his limbs gilded where he stands (fy_body_g)', /fy_body_g$/.test(await model()), await model());
  ok('...130 health, armour 10', (await num(PET, 'attributes[{id:"minecraft:max_health"}].base')) === 130 && (await num(PET, 'attributes[{id:"minecraft:armor"}].base')) === 10,
     `${await num(PET, 'attributes[{id:"minecraft:max_health"}].base')} / ${await num(PET, 'attributes[{id:"minecraft:armor"}].base')}`);
  const px = await num(PET, 'Pos[0]'), pz = await num(PET, 'Pos[2]');
  await run(`${O}kill @e[type=#bm:hostile,x=${X},y=${Y},z=${Z},distance=..40]`); await run(`scoreboard players set ${PET} bm.fyu 0`); await sleep(500);
  await run(`${O}summon minecraft:zombie ${px + 4} ${Y + 1} ${pz} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t163z","bm.seen"],attributes:[{id:"minecraft:max_health",base:200}],Health:200f}`);
  let reps = 0;
  const ult = await wait(6000, async () => { reps = Math.max(reps, await cnt('@e[tag=bm.fyrep]')); return (await score('bm.fyu', PET)) > 0; }, 150);
  const t0 = Date.now(); while (Date.now() - t0 < 3000) { reps = Math.max(reps, await cnt('@e[tag=bm.fyrep]')); await sleep(60); }
  ok('a foe near: the Grand Exhibition (his ult, on its cooldown)', ult, `fyu ${await score('bm.fyu', PET)}`);
  ok('...the replicas join the fray', reps > 0, `replicas ${reps}`);
  await sleep(4000);
  ok('...and are gone after it', (await cnt('@e[tag=bm.fyrep]')) === 0);
  ok('...the foe hurt', (await num('@e[tag=bm.t163z,limit=1]', 'Health')) < 200 || (await cnt('@e[tag=bm.t163z]')) === 0);

  // ---------------------------------------------------------------- clean up
  await run(`${O}kill @e[tag=bm.t163z]`); await run('function bm:admin/cabinet_reset'); await sleep(800);
  await sneakMenu(0); await A.click(/Send him home/); await sleep(1200);
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.fycd 0');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

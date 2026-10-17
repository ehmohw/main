// 2.82: KING OMEGA, THE FOLLOWER - the owner's checklist, as a regular (non-op) player, every step a real packet (rcon sets the
// stage: a floor, the items): Omega's Monocle used - he comes (his rig, twelve parts; 80 health, armour 12); sneak + use - his
// menu (Sit / follow, Send him home, King Omega's ways, Wardrobe); sat down from the menu and by a right-click on him (his seated
// cycle plays), up again; his ways from his menu; his Soul Court - a foe slain by the player near him gives him a soul, and his
// menu counts it; his wardrobe - Blood Moon used while he's out (his rig wears it), kept across a send-home and a call, put back;
// his aura, the Court of Souls (locked, used, on, off); his Raid Contract signed (he's met); a display case - his figurine
// (twelve parts), out again; Cecil's doll of him bought in a real trade, set down, twirled, picked up; knocked out - he faints,
// five minutes before the Monocle calls him again. (His frame: t146; every follower's figurine fit: t138; dolls: t156.)
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
  const X = 16700, Y = 100, Z = 16000;
  const PET = '@e[type=minecraft:wolf,tag=bm.ompet,tag=!bm.ffpet,limit=1]';
  const BODY = '@e[type=minecraft:item_display,tag=bm.omp_pet,tag=bm.omp_body,tag=!bm.omfade,limit=1]';
  const model = async (sel = BODY) => (await nbt(sel, 'item.components."minecraft:item_model"')).replace(/"/g, '');
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} minecraft:stone`); await run(`${O}fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 10} ${Z + 12} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.ompet]');
  for (const o of ['bm.omcd', 'bm.cosom', 'bm.wuomega']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const t of ['bm.auown_omega', 'bm.au_omega']) await run(`tag TestRat remove ${t}`);
  await run('advancement revoke TestRat only bm:met/omega');
  const fc0 = await score('bm.fcon');
  await sleep(1200);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  const kit = ['om_monocle', 'cos_omega_2', 'cos_aura_omega', 'fcontract_omega'];
  for (let i = 0; i < kit.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${kit[i]}`);
  await sleep(1500);
  ok('the Monocle in his pocket: Omega is met (his Raid Contract can be signed)', await wait(3000, async () => (await cnt('@a[name=TestRat,advancements={bm:met/omega=true}]')) === 1));

  // ---------------------------------------------------------------- UI: called, his menu
  A.chats.length = 0; A.bars.length = 0; await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(2000);
  ok('the Monocle used: King Omega comes - his rig (twelve parts), a tame wolf under it, his own', (await cnt(PET)) === 1 &&
     (await cnt('@e[type=minecraft:item_display,tag=bm.omp_pet,tag=!bm.omfade]')) === 12 && (await score('bm.pid', PET)) === (await score('bm.pid')),
     `${await cnt('@e[type=minecraft:item_display,tag=bm.omp_pet,tag=!bm.omfade]')} parts`);
  ok('..."King Omega, at your service"', A.bars.some(b => /King Omega, at your service/.test(b)), A.bars.slice(-1).join(''));
  ok('...80 health, armour 12', (await num(PET, 'attributes[{id:"minecraft:max_health"}].base')) === 80 && (await num(PET, 'attributes[{id:"minecraft:armor"}].base')) === 12);
  ok('...the Monocle stays in the hand', (await has('om_monocle')) === 1);
  ok('sneak + use: his menu', await sneakMenu(0));
  const labels = A.buttons().map(b => b.label);
  ok('...Sit / follow, Send him home, King Omega\'s ways, Wardrobe', ['Sit / follow', 'Send him home', "King Omega's ways", 'Wardrobe'].every(l => labels.some(x => x.includes(l))),
     labels.join(' | '));

  // ---------------------------------------------------------------- sitting: from the menu, by a right-click on him
  A.bars.length = 0; A.click(/Sit \/ follow/); await sleep(1500);
  ok('Sit / follow: he sits ("I shall rest a moment")', /1b/.test(await nbt(PET, 'Sitting')) && A.bars.some(b => /rest a moment/.test(b)), A.bars.slice(-1).join(''));
  await wait(3000, async () => (await score('bm.oqs', PET)) === 4);
  ok('...his seated cycle plays (state 4)', (await score('bm.oqs', PET)) === 4, `${await score('bm.oqs', PET)}`);
  const seen = new Set(); for (let k = 0; k < 14; k++) { seen.add(await nbt('@e[type=minecraft:item_display,tag=bm.omp_pet,tag=bm.omp_head,limit=1]', 'transformation')); await sleep(250); }
  ok('...and moves while he sits (sit -> sit_b and back)', seen.size >= 2, `${seen.size} distinct`);
  const hitSel = '@e[type=minecraft:interaction,tag=bm.omhit,limit=1]';
  await wait(3000, async () => (await cnt(hitSel)) === 1);
  const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');                  // (walk up to him)
  await at(wx + 0.5, Y + 1, wz - 2.2, 0, 20);
  A.slot(8); await sleep(300); let hb = await entOf(hitSel);
  A.bars.length = 0; if (hb) A.interact(hb.entityId); await sleep(1000);
  ok('right-clicked empty-handed: he stands ("Onward!")', !!hb && /0b/.test(await nbt(PET, 'Sitting')) && A.bars.some(b => /Onward/.test(b)), hb ? A.bars.slice(-1).join('') : 'no click box seen');
  hb = await entOf(hitSel); if (hb) A.interact(hb.entityId); await sleep(1000);
  ok('...right-clicked again: he sits', /1b/.test(await nbt(PET, 'Sitting')));
  hb = await entOf(hitSel); if (hb) A.interact(hb.entityId); await sleep(800);

  // ---------------------------------------------------------------- his ways, from his menu
  await sneakMenu(0); const pr = await A.press(/King Omega's ways/);
  const pw = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]) || {});
  ok('his menu -> King Omega\'s ways: claw and flame, the Soul Court, Raise the Fallen, the Serpent Squad, the Pardon, Soul Flame, Royal Subjects',
     pr && pr.next && ['Soul Court', 'Raise the Fallen', 'Soul Serpent Squad', "King's Pardon", 'Soul Flame', 'Royal Subjects'].every(w => pw.includes(w)), pw.slice(0, 160));

  // ---------------------------------------------------------------- his Soul Court: a foe slain near him
  await run(`scoreboard players set ${PET} bm.oqso 0`);
  const px = await num(PET, 'Pos[0]'), pz = await num(PET, 'Pos[2]');
  await run(`${O}summon minecraft:zombie ${px + 3} ${Y + 1} ${pz} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t199z","bm.seen"],Health:1f,active_effects:[{id:"minecraft:fire_resistance",duration:2400,show_particles:0b}]}`);   // (no burning up in the sun first)
  await at(px + 3.5, Y + 1, pz - 1.5, 0, 20); await sleep(600);
  let zb = null; await wait(3000, async () => !!(zb = await entOf('@e[tag=bm.t199z,limit=1]'))); if (zb) A.attack(zb.entityId);
  ok('a zombie slain beside him (his claw or the player\'s blow): one soul for his court (not two)', await wait(4000, async () => (await score('bm.oqso', PET)) >= 1) && (await sleep(1500), (await score('bm.oqso', PET)) === 1), `souls ${await score('bm.oqso', PET)}, zombie left: ${/count: 1/i.test(await run(`${O}execute if entity @e[tag=bm.t199z]`))}, hit sent: ${!!zb}`);
  await run(`${O}kill @e[tag=bm.t199z]`);
  await sneakMenu(0);
  const mb = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]) || {});
  ok('...and his menu counts it ("His Soul Court: 1 of 12")', /His Soul Court/.test(mb) && /"1"/.test(mb) && /of 12 souls/.test(mb), mb.slice(0, 200));

  // ---------------------------------------------------------------- cosmetics: Blood Moon, kept across a recall, put back
  await at(px + 0.5, Y + 1, pz - 3.5, 0, 0); await sleep(2200);          // (the item-use cooldown, bm.gvhc, from the menu just opened)
  await hold(1); await sleep(800);
  const m2 = await model();
  ok('Blood Moon used while he\'s out: picked (bm.cosom 2) and worn (his body _c2)', (await score('bm.cosom')) === 2 && /_c2$/.test(m2), `${m2}, cosom ${await score('bm.cosom')}, wardrobe ${await score('bm.wuomega')}, item left ${await has('cos_omega_2')}`);
  await sneakMenu(0); A.bars.length = 0; await A.click(/Send him home/); await sleep(1500);
  ok('Send him home: he goes ("Back to the palace, then")', (await cnt(PET)) === 0 && A.bars.some(b => /Back to the palace/.test(b)), A.bars.slice(-1).join(''));
  await sneakMenu(0);
  ok('...his menu now says Call for Omega', A.buttons().some(b => /Call for Omega/.test(b.label)) && !A.buttons().some(b => /Send him home/.test(b.label)));
  await A.click(/Call for Omega/); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(2000);
  ok('...called from the menu: back, still in Blood Moon', (await cnt(PET)) === 1 && /_c2$/.test(await model()), await model());
  await sneakMenu(0); const w1 = await A.press(/Wardrobe/);
  ok('his menu -> Wardrobe: his looks', w1 && w1.next && ['His own grey ghost', 'Spectral Blue', 'Blood Moon', 'Verdant Wraith', 'Gilded King'].every(l => A.buttons().some(b => b.label.includes(l))),
     A.buttons().map(b => b.label).join(' | '));
  ok('...Blood Moon: wearing; Spectral Blue: locked', A.buttons().some(b => /Blood Moon.*wearing/.test(b.label)) && A.buttons().some(b => /Spectral Blue.*locked/.test(b.label)));
  ok('...the aura row: Court of Souls - locked', A.buttons().some(b => /Court of Souls.*locked/.test(b.label)));
  await A.press(/His own grey ghost/); await sleep(1000);
  ok('"His own grey ghost": back to his own', !/_c\d$/.test(await model()) && (await score('bm.cosom')) === 0, await model());

  // ---------------------------------------------------------------- the rare cosmetic: his aura
  A.chats.length = 0; await hold(2); await sleep(600);
  ok('the Court of Souls used: his for good, and on', /bm\.auown_omega/.test(await tags()) && /bm\.au_omega\b/.test(await tags()), await tags());
  ok('...everyone hears of it; the item used up', A.chats.some(c => /Court of Souls/.test(c)) && (await has('cos_aura_omega')) === 0, A.chats.slice(-1).join(''));
  await sneakMenu(0); await A.press(/Wardrobe/);
  ok('...the wardrobe says on', A.buttons().some(b => /Court of Souls.*on/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  await A.press(/Court of Souls/); await sleep(600);
  ok('...switched off there (still his)', !/bm\.au_omega\b/.test(await tags()) && /bm\.auown_omega/.test(await tags()), await tags());

  // ---------------------------------------------------------------- his Raid Contract (he's met)
  await sleep(2200);
  A.chats.length = 0; await hold(3); await sleep(600);
  ok('his Raid Contract used: signed (a new contract bit), the contract gone', (await score('bm.fcon')) > fc0 && (await has('fcontract_omega')) === 0 &&
     A.chats.some(c => /Signed!/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
  const rec = require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p137/rc/main.mcfunction', 'utf8');
  ok('...and the Recruiter sells it (his book)', /fcontract_omega/.test(rec));
  await sneakMenu(0); await A.click(/Send him home/); await sleep(1200);

  // ---------------------------------------------------------------- display case: his figurine
  await at(X - 4.5, Y + 1, Z - 4.5, 0, 70);
  await run('loot replace entity TestRat hotbar.5 loot bm:items/display_case_oak'); await use(5);
  const caseSel = `@e[type=minecraft:interaction,tag=bm.dchit,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..1.5,limit=1]`;
  ok('a display case set down', (await cnt(caseSel)) === 1);
  const FIG = `@e[type=minecraft:item_display,tag=bm.dcfg,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..2]`;
  let box = await entOf(caseSel); A.slot(0); await sleep(300); if (box) A.interact(box.entityId); await sleep(800);
  const fs = await num(`${FIG.slice(0, -1)},limit=1]`, 'transformation.scale[0]');
  ok('the Monocle right-clicked into it: a little King Omega (twelve parts), shrunk to fit', (await cnt(FIG)) === 12 && fs > 0.02 && fs < 0.45, `parts ${await cnt(FIG)} scale ${fs}`);
  A.slot(8); await sleep(250); box = await entOf(caseSel); if (box) A.interact(box.entityId); await sleep(700);
  ok('...empty-handed: the Monocle back out, the figurine gone', (await has('om_monocle')) === 1 && (await cnt(FIG)) === 0);
  await run('clear TestRat *[minecraft:custom_data~{bm:"om_monocle"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/om_monocle');
  A.input({ shift: true }); await sleep(250); box = await entOf(caseSel); if (box) A.attack(box.entityId); await sleep(700); A.input({}); await sleep(300);
  await run(`${O}kill @e[type=minecraft:item,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..3]`);

  // ---------------------------------------------------------------- Cecil's doll of him: a real trade
  await run(`${O}execute positioned ${X + 5.5} ${Y + 1} ${Z - 3.5} rotated 180 0 run function bm:p45/cecil/spawn`); await sleep(1500);
  const CEC = `@e[type=minecraft:villager,tag=bm.npc_wizard,x=${X + 5.5},y=${Y + 1},z=${Z - 3.5},distance=..2,limit=1]`;
  await at(X + 5.5, Y + 1, Z - 0.5, 180, 0); await sleep(2500);
  let idx = -1;
  for (let i = 0; i < 80 && idx < 0; i++) { if (/Found no elements/i.test(await nbt(CEC, `Offers.Recipes[${i}].maxUses`))) break; const s = await nbt(CEC, `Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`); if (/"doll_omega"/.test(s)) idx = i; }
  ok('Cecil sells the Omega doll (he\'s met)', idx >= 0, `trade #${idx}`);
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
  ok(`...bought in his window for ${price} ${buyId}`, (await has('doll_omega')) === 1 && (await has(buyId)) === 0, `dolls ${await has('doll_omega')}`);
  await run(`${O}kill ${CEC}`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"doll_omega"}]'); await run('loot replace entity TestRat hotbar.6 loot bm:items/doll_omega');
  await at(X + 2.5, Y + 1, Z - 4.5, 180, 45); A.slot(6); await sleep(200); A.use(); await sleep(350); A.release(); await sleep(600);
  const DD = `@e[type=minecraft:item_display,tag=bm.doll_omegad,x=${X + 2.5},y=${Y + 1},z=${Z - 6.5},distance=..0.4,limit=1]`;
  const DH = `@e[type=minecraft:interaction,tag=bm.doll_omegahit,x=${X + 2.5},y=${Y + 1},z=${Z - 6.5},distance=..0.4,limit=1]`;
  ok('the doll set down on a block by a use: his own model', (await cnt(DD)) === 1 && (await has('doll_omega')) === 0 && /doll_omega/.test(await nbt(DD, 'item.components')),
     `${await cnt(DD)} ${await cnt(DH)}`);
  const y0 = await num(DD, 'Rotation[0]'); let dh = await entOf(DH); if (dh) A.interact(dh.entityId); await sleep(700);
  const y1 = await num(DD, 'Rotation[0]');
  ok('...right-clicked: it twirls', Math.abs(((y1 - y0 + 540) % 360) - 180) > 30, `${y0} -> ${y1}`);
  A.input({ shift: true }); await sleep(250); dh = await entOf(DH); if (dh) A.attack(dh.entityId); await sleep(700); A.input({}); await sleep(300);
  ok('...sneak + punch: back in the pack', (await has('doll_omega')) === 1 && (await cnt(DD)) === 0);

  // ---------------------------------------------------------------- knocked out: he faints
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(2000);
  A.chats.length = 0; await run(`${O}damage ${PET} 500 minecraft:mob_attack`);
  ok('struck down: he faints, his rig fades away', await wait(5000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.omp_pet]')) === 0));
  ok('..."Omega faints!" - five minutes on the Monocle', A.chats.some(c => /Omega faints!/.test(c)) && (await score('bm.omcd')) > 280, A.chats.slice(-1).join('').slice(0, 160));
  A.bars.length = 0; await sleep(2200); await use(0); await sleep(800);
  ok('...the Monocle used: "still gathering himself", no Omega', (await cnt(PET)) === 0 && A.bars.some(b => /gathering himself/.test(b)), A.bars.slice(-1).join(''));

  // ---------------------------------------------------------------- clean up
  await run('scoreboard players set TestRat bm.omcd 0');
  await run(`${O}kill @e[tag=bm.t199z]`); await run('kill @e[type=minecraft:wolf,tag=bm.ompet]');
  await run('clear TestRat');
  if (fc0 !== await score('bm.fcon')) await run(`scoreboard players set TestRat bm.fcon ${fc0}`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

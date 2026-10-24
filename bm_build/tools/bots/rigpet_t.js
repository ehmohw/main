// 2.87: the shared as-a-player checklist for a rigpet follower (phase189-191: Queen Ava, Queen Pearl, Bloo) - the owner's list,
// every step a real packet from a regular (non-op) player; rcon only sets the stage. A follower's test gives its config:
//   W, NAME, ab, q, prefix, item, parts, hp, X, Z, called (/re/ - the called-over line), home (/re/), sit (/re/), stand (/re/),
//   ways ([words in her ways]), form ({button: /re/, suffix}), story (/re/), encounter(ctx), abilities(ctx), fainted (/re/)
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs');
const DP = '/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function';

module.exports = async function run(C) {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
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
  const fx = async () => await nbt('@a[name=TestRat,limit=1]', 'active_effects');
  const { W, ab, q, prefix, X, Z } = C; const Y = 100;
  const PET = `@e[type=minecraft:wolf,tag=bm.${ab}pet,tag=!bm.ffpet,limit=1]`;
  const BODY = `@e[type=minecraft:item_display,tag=bm.${ab}p_pet,tag=bm.${ab}p_body,tag=!bm.${ab}fade,limit=1]`;
  const LP = C.lookPart || 'body';                // (2.94: the part a look recolours - the Sky Buddies' nightcap)
  const LOOK = `@e[type=minecraft:item_display,tag=bm.${ab}p_pet,tag=bm.${ab}p_${LP},tag=!bm.${ab}fade,limit=1]`;
  const model = async (sel = LOOK) => (await nbt(sel, 'item.components."minecraft:item_model"')).replace(/"/g, '');
  const ENC = `@e[type=minecraft:interaction,tag=bm.${ab}enc,limit=1]`;
  const zom = (dx, dz, t, hp = 300) => run(`${O}summon minecraft:husk ${X + dx} ${Y + 1} ${Z + dz} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.trpz","${t}","bm.seen"],attributes:[{id:"minecraft:max_health",base:${hp}}],Health:${hp}f}`);
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  const ctx = { A, R, run, ok, wait, O, cnt, nbt, num, score, tags, has, entOf, use, hold, sneakMenu, dd, at, fx, PET, BODY, model, ENC, zom, X, Y, Z, C, sleep };
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await sleep(2500);                // (a chunk's entities load a moment after it does: a host left from an earlier run must be there to be cleared)
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run(`kill @e[type=minecraft:wolf,tag=bm.${ab}pet]`); await run(`kill @e[type=minecraft:interaction,tag=bm.${ab}enc]`); await run(`kill @e[type=minecraft:item_display,tag=bm.${ab}encp]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.seen]'); await run('kill @e[type=minecraft:cat,tag=bm.seen]'); await sleep(1500);
  for (const o of [`bm.${ab}cd`, `bm.cos${ab}`, `bm.wu${W}`]) await run(`scoreboard players set TestRat ${o} 0`);
  if (C.form) await run(`scoreboard players set TestRat ${C.form.score} 0`);
  for (const t of [`bm.auown_${W}`, `bm.au_${W}`, `bm.${ab}met`]) await run(`tag TestRat remove ${t}`);
  await run(`advancement revoke TestRat only bm:met/${W}`); await run(`advancement revoke TestRat only bm:story/${W}_friend`);
  const BIT = +fs.readFileSync(`${DP}/${C.pfx}/sign.mcfunction`, 'utf8').match(/scoreboard players add @s bm\.fcon (\d+)/)[1];
  const fc = await score('bm.fcon'); if (fc > 0 && Math.floor(fc / BIT) % 2 === 1) await run(`scoreboard players set TestRat bm.fcon ${fc - BIT}`);
  await run('scoreboard players set #hard bm.cfg 1');
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);

  // ---------------------------------------------------------------- finding her/him (the follower's own steps; ends recruited, the item given)
  await C.encounter(ctx);
  ok(`...the encounter gone, and ${C.NAME} comes along (the rig, the player's own)`, (await cnt(ENC)) === 0 && await wait(4000, async () => (await cnt(PET)) === 1) &&
     (await score('bm.pid', PET)) === (await score('bm.pid')));
  ok('...the advancement, and met', (await cnt(`@a[name=TestRat,advancements={bm:story/${W}_friend=true,bm:met/${W}=true}]`)) === 1);
  await run(`${O}time set 6000`); await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${C.item}`);
  const kit = [null, `cos_${W}_1`, `cos_aura_${W}`, `fcontract_${W}`];
  for (let i = 1; i < kit.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${kit[i]}`);
  await run('execute as TestRat run function bm:p98/home/emma'); await run('scoreboard players set TestRat bm.emcd 0'); await sleep(800);

  // ---------------------------------------------------------------- UI: the menu
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  A.bars.length = 0; await use(0); await sleep(1500);
  ok('the item used while out: called over', A.bars.some(b => C.called.test(b)) && (await cnt(PET)) === 1, A.bars.slice(-1).join(''));
  { const np = await cnt(`@e[type=minecraft:item_display,tag=bm.${ab}p_pet,tag=!bm.${ab}fade]`), hp = await num(PET, 'attributes[{id:"minecraft:max_health"}].base');
    ok(`...the rig: ${C.parts} parts, ${C.hp} health`, np === C.parts && hp === C.hp, `parts ${np} hp ${hp}`); }
  ok('sneak + use: the menu', await sneakMenu(0));
  const labels = A.buttons().map(b => b.label);
  const pron = C.pron || 'her';
  const poss = C.NAME + (/s$/.test(C.NAME) ? "'" : "'s");
  const want = ['Sit / follow', `Send ${pron} home`, `${poss} ways`, 'Wardrobe'];
  ok(`...${want.join(', ')}${C.form ? ', the form' : ''}${C.story ? ', the story' : ''}`, want.every(l => labels.some(x => x.includes(l))) && (!C.form || labels.some(x => C.form.button.test(x))) && (!C.story || labels.some(x => C.story.test(x))), labels.join(' | '));
  let pr = await A.press(new RegExp(`${poss} ways`));
  const pw = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]).body || []);
  ok(`the menu -> ${poss} ways: ${C.ways.join(', ')}`, pr && pr.next && C.ways.every(w => pw.includes(w)), pw.slice(0, 160));
  await A.press(/« Back/); await sleep(600);
  if (C.story) {
    pr = await A.press(C.story);
    const ps = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]).body || []);
    ok('the menu -> the story: its pages', pr && pr.next && /I\.|II\./.test(ps) && ps.length > 400, ps.slice(0, 120));
  }
  await sleep(2200);

  // ---------------------------------------------------------------- sitting: menu and right-click
  await sneakMenu(0); A.bars.length = 0; await A.press(/Sit \/ follow/); await sleep(1500);
  ok('Sit / follow: sits', /1b/.test(await nbt(PET, 'Sitting')) && A.bars.some(b => C.sit.test(b)), A.bars.slice(-1).join(''));
  await wait(3000, async () => (await score(`bm.${q}s`, PET)) === 4);
  ok('...the seated cycle plays (state 4)', (await score(`bm.${q}s`, PET)) === 4);
  // (2.94: a sprite moves by its frame - the head's custom_model_data - not its transformation)
  const seen = new Set(); for (let k = 0; k < 14; k++) { seen.add(await nbt(`@e[type=minecraft:item_display,tag=bm.${ab}p_pet,tag=bm.${ab}p_head,limit=1]`, C.sprite ? 'item.components."minecraft:custom_model_data"' : 'transformation')); await sleep(C.sprite ? 600 : 250); }
  ok('...and moves while seated (sit_a -> sit_b)', seen.size >= 2, `${seen.size} distinct`);
  if (C.sitPart) {             // (2.94: a part that shows only seated - Ava's gown pooled on the floor)
    const sp = await nbt(`@e[type=minecraft:item_display,tag=bm.${ab}p_pet,tag=bm.${ab}p_${C.sitPart},limit=1]`, 'transformation.scale[0]');
    ok(`...seated, her ${C.sitPart} shows`, +((sp.match(/([\d.]+)/) || [0, 0])[1]) > 0, sp);
  }
  const hitSel = `@e[type=minecraft:interaction,tag=bm.${ab}hit,limit=1]`;
  await wait(3000, async () => (await cnt(hitSel)) === 1);
  const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');
  await at(wx + 0.5, Y + 1, wz - 1.8, 0, 30);
  A.slot(8); await sleep(300); let hb = await entOf(hitSel);
  A.bars.length = 0; if (hb) A.interact(hb.entityId); await sleep(1000);
  ok('right-clicked: stands', !!hb && /0b/.test(await nbt(PET, 'Sitting')) && A.bars.some(b => C.stand.test(b)), A.bars.slice(-1).join(''));

  // ---------------------------------------------------------------- the follower's own abilities
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0); await run(`${O}tp ${PET} ${X + 1.5} ${Y + 1} ${Z + 0.5}`); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await sleep(1500);
  await C.abilities(ctx);
  await run(`${O}kill @e[tag=bm.trpz]`); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  if (C.form) await run(`scoreboard players set TestRat ${C.form.score} 0`);
  await sleep(500);

  // ---------------------------------------------------------------- cosmetics: the first look, kept across a send-home; the aura
  await sneakMenu(0); await A.press(/Send .* home/); await sleep(1200); await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  await hold(1); await sleep(800);
  ok(`the first look used while out: picked (bm.cos${ab} 1) and worn (${prefix}${LP}_c1)`, (await score(`bm.cos${ab}`)) === 1 && new RegExp(`${prefix}${LP}_c1$`).test(await model()), await model());
  await sneakMenu(0); A.bars.length = 0; await A.click(/Send .* home/); await sleep(1500);
  ok('Send home: goes', (await cnt(PET)) === 0 && A.bars.some(b => C.home.test(b)), A.bars.slice(-1).join(''));
  await sneakMenu(0);
  ok(`...the menu now says Call for ${C.NAME}`, A.buttons().some(b => new RegExp(`Call for ${C.NAME}`).test(b.label)) && !A.buttons().some(b => /Send .* home/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  await A.click(new RegExp(`Call for ${C.NAME}`)); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('...called from the menu: back, still in the look', (await cnt(PET)) === 1 && new RegExp(`${prefix}${LP}_c1$`).test(await model()), await model());
  if (C.form) {
    await sneakMenu(0); await A.press(C.form.button); await sleep(1200);
    ok(`...the other form: the look on it too (${prefix}${LP}${C.form.suffix}_c1)`, new RegExp(`${prefix}${LP}${C.form.suffix}_c1$`).test(await model()), await model());
    await sneakMenu(0); await A.press(C.form.button); await sleep(1200);
    ok('...and back', new RegExp(`${prefix}${LP}_c1$`).test(await model()), await model());
  }
  await sneakMenu(0); const w1 = await A.press(/Wardrobe/);
  ok('the menu -> Wardrobe: the looks', w1 && w1.next && [C.plain, ...C.looks].every(l => A.buttons().some(b => b.label.includes(l))), A.buttons().map(b => b.label).join(' | '));
  await A.press(new RegExp(C.plain)); await sleep(1000);
  ok(`"${C.plain}": back to the own look (${prefix}${LP})`, new RegExp(`^bm:${prefix}${LP}$`).test(await model()) && (await score(`bm.cos${ab}`)) === 0, await model());
  await sleep(2200); A.chats.length = 0; await hold(2); await sleep(600);
  ok('the rare aura used: owned for good, and on', new RegExp(`bm\\.auown_${W}`).test(await tags()) && new RegExp(`bm\\.au_${W}\\b`).test(await tags()), await tags());

  // ---------------------------------------------------------------- the Raid Contract
  await sleep(2200);
  const fc0 = await score('bm.fcon');
  A.chats.length = 0; await hold(3); await sleep(600);
  ok('the Raid Contract used: signed, the contract gone', Math.floor((await score('bm.fcon')) / BIT) % 2 === 1 && (await score('bm.fcon')) > fc0 && (await has(`fcontract_${W}`)) === 0 && A.chats.some(c => /Signed!/.test(c)),
     A.chats.slice(-1).join('').slice(0, 160));
  ok('...and the Recruiter sells it', new RegExp(`fcontract_${W}`).test(fs.readFileSync(`${DP}/p137/rc/main.mcfunction`, 'utf8')));
  ok('the Partner Wheel lists her/him', require('child_process').execSync(`grep -rl "${C.pfx}/try_summon" ${DP}/p179 | head -1`).toString().length > 0);

  // ---------------------------------------------------------------- frame gimmick
  await sneakMenu(0); await A.click(/Send .* home/); await sleep(1200);
  await run(`${O}fill ${X - 6} ${Y + 1} ${Z + 5} ${X + 6} ${Y + 3} ${Z + 5} minecraft:stone`);
  await run(`${O}summon minecraft:item_frame ${X} ${Y + 2} ${Z + 4} {Facing:2b,Tags:["bm.trpf"]}`); await sleep(400);
  await at(X + 0.5, Y + 1, Z + 2.5, 0, -10);
  const frSel = '@e[type=minecraft:item_frame,tag=bm.trpf,limit=1]';
  let fr = null; await wait(4000, async () => (fr = await entOf(frSel)) != null, 250);
  A.slot(0); await sleep(300); A.bars.length = 0; if (fr) A.interact(fr.entityId); await sleep(2800);
  const FPET = `@e[type=minecraft:wolf,tag=bm.${ab}pet,tag=bm.ffpet,x=${X},y=${Y + 2},z=${Z + 4},distance=..10]`;
  ok('the item in a frame: out of the frame', (await cnt(FPET)) === 1 && A.bars.some(b => /climbs? out of the frame/.test(b)), A.bars.slice(-1).join(''));
  if (fr) A.attack(fr.entityId); await sleep(600);
  ok('the item punched out of the frame: gone with it', await wait(3000, async () => (await cnt(FPET)) === 0));
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y + 2},z=${Z + 4},distance=..4]`); await run(`${O}kill ${frSel}`);
  await run(`clear TestRat *[minecraft:custom_data~{bm:"${C.item}"}]`); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${C.item}`);

  // ---------------------------------------------------------------- display case: the figurine
  await at(X - 4.5, Y + 1, Z - 4.5, 0, 70);
  await run('loot replace entity TestRat hotbar.5 loot bm:items/display_case_oak'); await use(5);
  const caseSel = `@e[type=minecraft:interaction,tag=bm.dchit,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..1.5,limit=1]`;
  ok('a display case set down', (await cnt(caseSel)) === 1);
  const FIG = `@e[type=minecraft:item_display,tag=bm.dcfg,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..2]`;
  let box = await entOf(caseSel); A.slot(0); await sleep(300); if (box) A.interact(box.entityId); await sleep(800);
  const nfig = await cnt(FIG);
  ok('the item right-clicked into it: a little figure (the parts), shrunk to fit', nfig === (C.figParts || C.parts),   // (2.94: a part hidden at rest - Ava's pooled gown - isn't in the figure)
     `parts ${nfig}`);
  const ys = []; for (let k = 0; k < 12; k++) ys.push(await num(`${FIG.slice(0, -1)},limit=1,sort=random]`, 'transformation.translation[1]'));
  // (2.94: a sprite's quad stands on its middle - its origin is higher than a rig part's)
  ok('...standing on the cushion, inside the glass', Math.min(...ys) >= -0.01 && Math.max(...ys) < (C.sprite ? 0.7 : 0.62), `translation y ${Math.min(...ys).toFixed(2)}..${Math.max(...ys).toFixed(2)}`);
  A.slot(8); await sleep(250); box = await entOf(caseSel); if (box) A.interact(box.entityId); await sleep(700);
  ok('...empty-handed: the item back out, the figurine gone', (await has(C.item)) === 1 && (await cnt(FIG)) === 0);
  await run(`clear TestRat *[minecraft:custom_data~{bm:"${C.item}"}]`); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${C.item}`);
  A.input({ shift: true }); await sleep(250); box = await entOf(caseSel); if (box) A.attack(box.entityId); await sleep(700); A.input({}); await sleep(300);
  await run(`${O}kill @e[type=minecraft:item,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..3]`);

  // ---------------------------------------------------------------- Cecil's doll: a real trade
  await run(`${O}execute positioned ${X + 5.5} ${Y + 1} ${Z - 3.5} rotated 180 0 run function bm:p45/cecil/spawn`); await sleep(1500);
  const CEC = `@e[type=minecraft:villager,tag=bm.npc_wizard,x=${X + 5.5},y=${Y + 1},z=${Z - 3.5},distance=..2,limit=1]`;
  await at(X + 5.5, Y + 1, Z - 0.5, 180, 0); await sleep(2500);
  const DOLL = `doll_${W}`;
  let idx = -1;
  for (let i = 0; i < 90 && idx < 0; i++) { if (/Found no elements/i.test(await nbt(CEC, `Offers.Recipes[${i}].maxUses`))) break; const s = await nbt(CEC, `Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`); if (new RegExp(`"${DOLL}"`).test(s)) idx = i; }
  ok(`Cecil sells the ${C.NAME} doll`, idx >= 0, `trade #${idx}`);
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
  ok('...bought in his window', (await has(DOLL)) === 1, `dolls ${await has(DOLL)}`);
  await run(`${O}kill ${CEC}`);
  await run(`clear TestRat *[minecraft:custom_data~{bm:"${DOLL}"}]`); await run(`loot replace entity TestRat hotbar.6 loot bm:items/${DOLL}`);
  await at(X + 2.5, Y + 1, Z - 4.5, 180, 45); A.slot(6); await sleep(200); A.use(); await sleep(350); A.release(); await sleep(600);
  const DD = `@e[type=minecraft:item_display,tag=bm.${DOLL}d,x=${X + 2.5},y=${Y + 1},z=${Z - 6.5},distance=..0.4,limit=1]`;
  const DH = `@e[type=minecraft:interaction,tag=bm.${DOLL}hit,x=${X + 2.5},y=${Y + 1},z=${Z - 6.5},distance=..0.4,limit=1]`;
  ok('the doll set down on a block: its own model', (await cnt(DD)) === 1 && new RegExp(DOLL).test(await nbt(DD, 'item.components')));
  const y0 = await num(DD, 'Rotation[0]'); let dh = await entOf(DH); if (dh) A.interact(dh.entityId); await sleep(700);
  ok('...right-clicked: it twirls', Math.abs(((await num(DD, 'Rotation[0]') - y0 + 540) % 360) - 180) > 30);
  A.input({ shift: true }); await sleep(250); dh = await entOf(DH); if (dh) A.attack(dh.entityId); await sleep(700); A.input({}); await sleep(300);
  ok('...sneak + punch: back in the pack', (await has(DOLL)) === 1 && (await cnt(DD)) === 0);

  // ---------------------------------------------------------------- knocked out: faints
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  A.chats.length = 0; await run(`${O}effect clear ${PET}`); await run(`${O}damage ${PET} 400 minecraft:out_of_world`);
  ok('struck down: faints, the rig fades away', await wait(5000, async () => (await cnt(`@e[type=minecraft:item_display,tag=bm.${ab}p_pet]`)) === 0));
  ok(`..."${C.NAME} ${C.pron === 'them' ? 'faint' : 'faints'}!" - two minutes on the item`, A.chats.some(c => new RegExp(`${C.NAME} faints?!`).test(c)) && (await score(`bm.${ab}cd`)) > 100, A.chats.slice(-1).join('').slice(0, 160));
  A.bars.length = 0; await use(0); await sleep(800);
  ok('...the item used: "still recovering", nobody comes', (await cnt(PET)) === 0 && A.bars.some(b => /still recovering/.test(b)), A.bars.slice(-1).join(''));

  // ---------------------------------------------------------------- clean up
  await run(`scoreboard players set TestRat bm.${ab}cd 0`); await run('clear TestRat');
  for (const t of [`bm.auown_${W}`, `bm.au_${W}`]) await run(`tag TestRat remove ${t}`);
  await run(`${O}kill @e[type=minecraft:wolf,tag=bm.${ab}pet]`); await run(`${O}kill @e[tag=bm.trpz]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
};

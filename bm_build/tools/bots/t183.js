// 2.80d: DENNIS AND PISTACHIO, THE FOLLOWERS - the owner's checklist for each (node t183.js [dennis|pistachio]; both by
// default), as a regular (non-op) player, every step a real packet (rcon sets the stage: a floor, a wall, the items, a foe):
// his item used - he comes (his rig, his health and armour); sneak + use - his menu (Sit / follow, Send him home, his ways,
// Wardrobe); sat from the menu and by a right-click on him (his seated cycle plays), up again; his ways; a look from his
// wardrobe used while he's out (worn), kept across a send-home and a call, put back; his aura (locked, used, on, off); his
// Raid Contract signed, and the Recruiter sells it; his item in a frame - he steps out, punched out - he goes; a display case -
// his figurine, out again; Cecil's doll of him bought in a real trade, set down, twirled, picked up. Then his fighting: a foe
// near - his great blow (and what it does for you), his ranged blow, then up close his crowd blow and his melee; Pistachio's
// Phantom Escape when you're low. His passive: Dennis - Fortune V on the ores you mine (a plain pickaxe); Pistachio - Looting V
// on the zombies you kill (a plain sword); neither without him. Last, knocked out: he faints, five minutes on his item.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
const WHO = process.argv[2] ? [process.argv[2]] : ['dennis', 'pistachio'];
const CFG = {
  dennis: { k: 'dw', item: 'dw_horn', name: 'Dennis', parts: 9, cos: 'bm.cosdw', look: 'cos_dennis_2', lookName: 'Biker Red', lockedName: 'Road Brown', plainName: 'His old black leather',
            aura: 'Gold Rush Glimmer', contract: 'fcontract_dennis', bit: 2048, ar: 13, doll: 'doll_dennis', hp: 48, armour: 8,
            hello: /Dennis here/, sitDown: /These boots weren't made/, standUp: /let's be off/, home: /Back to the market/, ways: "Dennis's ways", waysTitle: "DENNIS'S WAYS",
            powers: ['Wrench Whack', 'Gold Rush', 'Midas Slam', 'The Mother Lode', 'Fortune V'], ult: /THE MOTHER LODE/, crowd: /MIDAS SLAM/, ultFx: 'absorption' },
  pistachio: { k: 'pi', item: 'pi_cloche', name: 'Pistachio', parts: 8, cos: 'bm.cospi', look: 'cos_pistachio_2', lookName: 'Claret Tails', lockedName: 'Midnight Tails', plainName: 'His charcoal tails',
               aura: 'Ectoplasmic Mist', contract: 'fcontract_pistachio', bit: 4096, ar: 14, doll: 'doll_pistachio', hp: 34, armour: 4,
               hello: /Pistachio, at your service/, sitDown: /I shall take a seat/, standUp: /Onward, sir/, home: /return to the Palace/, ways: "Pistachio's ways", waysTitle: "PISTACHIO'S WAYS",
               powers: ['Spectral Slap', 'The Next Course', 'The Wail', 'The Last Course', 'Phantom Escape', 'Looting V'], ult: /The Last Course/, crowd: /BOOOOO/, ultFx: 'regeneration' } };
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
  const plain = async (iid) => +(((await run(`clear TestRat minecraft:${iid} 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const ground = async (iid, x, y, z) => ((await run(`${O}execute as @e[type=minecraft:item,x=${x},y=${y},z=${z},distance=..10] if items entity @s contents minecraft:${iid} run data get entity @s Item.count`))
    .match(/data: \d+/g) || []).reduce((a, m) => a + +m.slice(6), 0);       // (dropped and not yet picked up: the bot stands still)
  const hasFx = async (sel, id) => (await run(`${O}data get entity ${sel} active_effects`)).includes(`"minecraft:${id}"`);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const hold = async (slot, ms = 1600) => { A.slot(slot); await sleep(250); A.use(); await sleep(ms); A.release(); await sleep(400); };
  const sneakMenu = async (slot) => { await sleep(1000); const n0 = A.dialogN.length; await use(slot, true); await wait(3000, async () => A.dialogN.length > n0); return A.dialogN.length > n0; };
  const press = async (re) => { await sleep(1000); return A.press(re); };
  const click = async (re) => { await sleep(1000); return A.click(re); };
  const dd = (d) => d && (d.data || d);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));

  for (const who of WHO) {
    const c = CFG[who], k = c.k, N = `[${c.name}] `;
    const X = 16620 + (who === 'pistachio' ? 60 : 0), Y = 100, Z = 16000;
    const PET = `@e[type=minecraft:wolf,tag=bm.${k}pet,tag=!bm.ffpet,limit=1]`;
    const BODY = `@e[type=minecraft:item_display,tag=bm.${k}p_pet,tag=bm.${k}p_body,tag=!bm.${k}fade,limit=1]`;
    const model = async (sel = BODY) => (await nbt(sel, 'item.components."minecraft:item_model"')).replace(/"/g, '');
    await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
    await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
    await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
    await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
    // (3.0a: a faint at the end of the last run left "back after a faint" waiting (bm.arw<i>, phase173 - the AR order: Dennis 13,
    //  Pistachio 14) if the bot logged out before loop/second saw his rest over; he then walked back in by himself the moment his
    //  item was in your pocket, and "his hello" was a recall's. And the arena's entities load a moment after the forceload: a kill
    //  sent at once misses a follower left standing there)
    await run(`tag TestRat remove bm.arw${c.ar}`); await sleep(1500);
    await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
    await run('kill @e[type=minecraft:wolf,tag=bm.dwpet]'); await run('kill @e[type=minecraft:wolf,tag=bm.pipet]');
    for (const o of [`bm.${k}cd`, c.cos, 'bm.pisv']) await run(`scoreboard players set TestRat ${o} 0`);
    for (const t of [`bm.auown_${who}`, `bm.au_${who}`]) await run(`tag TestRat remove ${t}`);
    await run(`tag TestRat add bm.${k}met`); await run(`advancement revoke TestRat only bm:met/${who}`);
    const fc = await score('bm.fcon'); if (fc > 0 && Math.floor(fc / c.bit) % 2 === 1) await run(`scoreboard players set TestRat bm.fcon ${fc - c.bit}`);
    await sleep(1200);
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
    const kit = [c.item, c.look, `cos_aura_${who}`, c.contract];
    for (let i = 0; i < kit.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${kit[i]}`);
    await sleep(1500);
    ok(N + 'his item in your pocket: met (his Raid Contract can be signed, Cecil can sell his doll)', await wait(3000, async () => (await cnt(`@a[name=TestRat,advancements={bm:met/${who}=true}]`)) === 1));

    // ---------------------------------------------------------------- UI: called, his menu
    A.chats.length = 0; A.bars.length = 0; await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
    ok(N + `used: he comes - his rig (${c.parts} parts), a tame wolf under it, his own`, (await cnt(PET)) === 1 && (await cnt(`@e[type=minecraft:item_display,tag=bm.${k}p_pet,tag=!bm.${k}fade]`)) === c.parts &&
       (await score('bm.pid', PET)) === (await score('bm.pid')), `${await cnt(`@e[type=minecraft:item_display,tag=bm.${k}p_pet,tag=!bm.${k}fade]`)} parts`);
    ok(N + '...his hello', A.bars.some(b => c.hello.test(b)), A.bars.slice(-1).join(''));
    ok(N + `...${c.hp} health, armour ${c.armour}`, (await num(PET, 'attributes[{id:"minecraft:max_health"}].base')) === c.hp && (await num(PET, 'attributes[{id:"minecraft:armor"}].base')) === c.armour);
    ok(N + 'sneak + use: his menu', await sneakMenu(0));
    const labels = A.buttons().map(b => b.label);
    ok(N + `...Sit / follow, Send him home, ${c.ways}, Wardrobe`, ['Sit / follow', 'Send him home', c.ways, 'Wardrobe'].every(l => labels.some(x => x.includes(l))), labels.join(' | '));

    // ---------------------------------------------------------------- sitting: from the menu, by a right-click on him
    A.bars.length = 0; await click(/Sit \/ follow/); await sleep(1500);
    ok(N + 'Sit / follow: he sits', /1b/.test(await nbt(PET, 'Sitting')) && A.bars.some(b => c.sitDown.test(b)), A.bars.slice(-1).join(''));
    await wait(3000, async () => (await score(`bm.${k}s`, PET)) === 4);
    ok(N + '...his seated cycle plays (state 4)', (await score(`bm.${k}s`, PET)) === 4, `${await score(`bm.${k}s`, PET)}`);
    const seen = new Set(); for (let i = 0; i < 12; i++) { seen.add(await nbt(`@e[type=minecraft:item_display,tag=bm.${k}p_pet,tag=bm.${k}p_head,limit=1]`, 'transformation')); await sleep(250); }
    ok(N + '...and moves while he sits (sit -> sit_b and back)', seen.size >= 2, `${seen.size} distinct`);
    const hitSel = `@e[type=minecraft:interaction,tag=bm.${k}hit,limit=1]`;
    await wait(3000, async () => (await cnt(hitSel)) === 1);
    const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');
    await at(wx + 0.5, Y + 1, wz - 1.5, 0, 30);
    A.slot(8); await sleep(300); let hb = await entOf(hitSel);
    A.bars.length = 0; if (hb) A.interact(hb.entityId); await sleep(1000);
    ok(N + 'right-clicked empty-handed: he stands', !!hb && /0b/.test(await nbt(PET, 'Sitting')) && A.bars.some(b => c.standUp.test(b)), hb ? A.bars.slice(-1).join('') : 'no click box seen');
    await sleep(600); hb = await entOf(hitSel); if (hb) A.interact(hb.entityId); await sleep(1000);
    if (!/1b/.test(await nbt(PET, 'Sitting'))) { await sleep(600); hb = await entOf(hitSel); if (hb) A.interact(hb.entityId); await sleep(1000); }   // (a click lost in the debounce)
    ok(N + '...right-clicked again: he sits', /1b/.test(await nbt(PET, 'Sitting')));
    await sleep(600); hb = await entOf(hitSel); if (hb) A.interact(hb.entityId); await sleep(800);

    // ---------------------------------------------------------------- his ways
    await sneakMenu(0); let pr = await press(new RegExp(c.ways.replace(/'/g, '.')));
    const pw = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]) || {});
    ok(N + `his menu -> ${c.ways}: every blow, and what he does for you`, pr && pr.next && pw.includes(c.waysTitle) && c.powers.every(p => pw.includes(p)), pw.slice(0, 160));
    pr = await press(/Back/);
    ok(N + '..."« Back": his menu again', pr && pr.next && A.buttons().some(b => b.label.includes('Wardrobe')));

    // ---------------------------------------------------------------- cosmetics: a look, kept across a recall, put back
    await sleep(2200); await hold(1); await sleep(800);
    ok(N + `${c.lookName} used while he's out: picked (${c.cos} 2) and worn (_c2)`, (await score(c.cos)) === 2 && /_c2$/.test(await model()), await model());
    await sneakMenu(0); A.bars.length = 0; await click(/Send him home/); await sleep(1500);
    ok(N + 'Send him home: he goes', (await cnt(PET)) === 0 && A.bars.some(b => c.home.test(b)), A.bars.slice(-1).join(''));
    await sneakMenu(0);
    ok(N + `...his menu now says Call for ${c.name}`, A.buttons().some(b => b.label.includes(`Call for ${c.name}`)) && !A.buttons().some(b => /Send him home/.test(b.label)));
    await click(new RegExp(`Call for ${c.name}`)); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
    ok(N + `...called from the menu: back, still in ${c.lookName}`, (await cnt(PET)) === 1 && /_c2$/.test(await model()), await model());
    await sneakMenu(0); const w1 = await press(/Wardrobe/);
    ok(N + 'his menu -> Wardrobe: his looks', w1 && w1.next && [c.plainName, c.lockedName, c.lookName].every(l => A.buttons().some(b => b.label.includes(l))),
       A.buttons().map(b => b.label).join(' | '));
    ok(N + `...${c.lookName}: wearing; ${c.lockedName}: locked`, A.buttons().some(b => new RegExp(c.lookName + '.*wearing').test(b.label)) && A.buttons().some(b => new RegExp(c.lockedName + '.*locked').test(b.label)));
    ok(N + `...the aura row: ${c.aura} - locked`, A.buttons().some(b => new RegExp(c.aura + '.*locked').test(b.label)));
    await press(new RegExp(c.plainName)); await sleep(1000);
    ok(N + `"${c.plainName}": back to his own`, !/_c\d$/.test(await model()) && (await score(c.cos)) === 0, await model());

    // ---------------------------------------------------------------- the rare cosmetic: his aura
    await sleep(2200); A.chats.length = 0; await hold(2); await sleep(600);
    ok(N + `${c.aura} used: his for good, and on`, (await tags()).includes(`bm.auown_${who}`) && new RegExp(`bm\\.au_${who}\\b`).test(await tags()), await tags());
    ok(N + '...everyone hears of it; the item used up', A.chats.some(c2 => new RegExp('awakened ' + c.aura).test(c2)) && (await has(`cos_aura_${who}`)) === 0, A.chats.slice(-1).join(''));
    await sneakMenu(0); await press(/Wardrobe/);
    ok(N + '...the wardrobe says on', A.buttons().some(b => new RegExp(c.aura + '.*on').test(b.label)), A.buttons().map(b => b.label).join(' | '));
    await press(new RegExp(c.aura)); await sleep(600);
    ok(N + '...switched off there (still his)', !new RegExp(`bm\\.au_${who}\\b`).test(await tags()) && (await tags()).includes(`bm.auown_${who}`));

    // ---------------------------------------------------------------- his Raid Contract
    await sleep(2200); A.chats.length = 0; await hold(3); await sleep(600);
    ok(N + 'his Raid Contract used: signed (the contract bit), the contract gone', Math.floor((await score('bm.fcon')) / c.bit) % 2 === 1 && (await has(c.contract)) === 0 &&
       A.chats.some(c2 => /Signed!/.test(c2)), A.chats.slice(-1).join('').slice(0, 160));
    const rec = require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p137/rc/main.mcfunction', 'utf8');
    ok(N + '...and the Recruiter in the den sells it', rec.includes(`bm:"${c.contract}"`));

    // ---------------------------------------------------------------- frame gimmick
    await sneakMenu(0); await click(/Send him home/); await sleep(1200);
    await run(`${O}fill ${X - 6} ${Y + 1} ${Z + 5} ${X + 6} ${Y + 3} ${Z + 5} minecraft:stone`);
    await run(`${O}summon minecraft:item_frame ${X} ${Y + 2} ${Z + 4} {Facing:2b,Tags:["bm.t183f"]}`); await sleep(400);
    await at(X + 0.5, Y + 1, Z + 2.5, 0, -10);
    const frSel = '@e[type=minecraft:item_frame,tag=bm.t183f,limit=1]';
    let fr = null; await wait(4000, async () => (fr = await entOf(frSel)) != null, 250);
    A.slot(0); await sleep(300); A.bars.length = 0; if (fr) A.interact(fr.entityId); await sleep(2800);
    const FPET = `@e[type=minecraft:wolf,tag=bm.${k}pet,tag=bm.ffpet,x=${X},y=${Y + 2},z=${Z + 4},distance=..10]`;
    ok(N + 'his item in a frame: he steps out (and says so)', (await cnt(FPET)) === 1 && A.bars.some(b => new RegExp(c.name + ' climbs out of the frame').test(b)), A.bars.slice(-1).join(''));
    ok(N + '...in his rig, nobody\'s', (await cnt(`@e[type=minecraft:item_display,tag=bm.${k}p_body,x=${X},y=${Y + 2},z=${Z + 4},distance=..10]`)) === 1 &&
       (await cnt(`${FPET.slice(0, -1)},scores={bm.pid=${await score('bm.pid')}}]`)) === 0);
    await sleep(6000);
    ok(N + '...still by the frame six seconds on', (await cnt(FPET)) === 1);
    if (fr) A.attack(fr.entityId); await sleep(600);
    ok(N + 'punched out of the frame: he goes with it', await wait(3000, async () => (await cnt(FPET)) === 0 &&
       (await cnt(`@e[type=minecraft:item_display,tag=bm.${k}p_body,x=${X},y=${Y + 2},z=${Z + 4},distance=..10]`)) === 0));
    await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y + 2},z=${Z + 4},distance=..4]`); await run(`${O}kill ${frSel}`);
    await run(`${O}fill ${X - 6} ${Y + 1} ${Z + 5} ${X + 6} ${Y + 3} ${Z + 5} minecraft:air`);   // (3.0a: the frame's wall down again - the fight's foe stood behind it, and Dennis's throws (2.94, real projectiles) broke on it)
    await run(`clear TestRat *[minecraft:custom_data~{bm:"${c.item}"}]`); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${c.item}`);

    // ---------------------------------------------------------------- display case: his figurine
    await at(X - 4.5, Y + 1, Z - 4.5, 0, 70);
    await run('loot replace entity TestRat hotbar.5 loot bm:items/display_case_oak'); await use(5);
    const caseSel = `@e[type=minecraft:interaction,tag=bm.dchit,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..1.5,limit=1]`;
    ok(N + 'a display case set down', (await cnt(caseSel)) === 1);
    const FIG = `@e[type=minecraft:item_display,tag=bm.dcfg,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..2]`;
    let box = await entOf(caseSel); A.slot(0); await sleep(300); if (box) A.interact(box.entityId); await sleep(800);
    const fs = await num(`${FIG.slice(0, -1)},limit=1]`, 'transformation.scale[0]');
    ok(N + `his item right-clicked into it: a little ${c.name} (${c.parts} parts), shrunk to fit`, (await cnt(FIG)) === c.parts && fs > 0.05 && fs < 0.45, `parts ${await cnt(FIG)} scale ${fs}`);
    const ys = []; for (let i = 0; i < c.parts * 2; i++) ys.push(await num(`${FIG.slice(0, -1)},limit=1,sort=random]`, 'transformation.translation[1]'));
    ok(N + '...standing on the cushion, inside the glass', Math.min(...ys) >= -0.01 && Math.max(...ys) < 0.62, `translation y ${Math.min(...ys).toFixed(2)}..${Math.max(...ys).toFixed(2)}`);
    A.slot(8); await sleep(250); box = await entOf(caseSel); if (box) A.interact(box.entityId); await sleep(700);
    ok(N + '...empty-handed: his item back out, the figurine gone', (await has(c.item)) >= 1 && (await cnt(FIG)) === 0);
    await run(`clear TestRat *[minecraft:custom_data~{bm:"${c.item}"}]`); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${c.item}`);
    A.input({ shift: true }); await sleep(250); box = await entOf(caseSel); if (box) A.attack(box.entityId); await sleep(700); A.input({}); await sleep(300);
    await run(`${O}kill @e[type=minecraft:item,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..3]`);

    // ---------------------------------------------------------------- Cecil's doll of him: a real trade
    await run(`${O}execute positioned ${X + 5.5} ${Y + 1} ${Z - 3.5} rotated 180 0 run function bm:p45/cecil/spawn`); await sleep(1500);
    const CEC = `@e[type=minecraft:villager,tag=bm.npc_wizard,x=${X + 5.5},y=${Y + 1},z=${Z - 3.5},distance=..2,limit=1]`;
    await at(X + 5.5, Y + 1, Z - 0.5, 180, 0); await sleep(2500);
    let idx = -1;
    for (let i = 0; i < 80 && idx < 0; i++) { if (/Found no elements/i.test(await nbt(CEC, `Offers.Recipes[${i}].maxUses`))) break; const s = await nbt(CEC, `Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`); if (new RegExp(`"${c.doll}"`).test(s)) idx = i; }
    ok(N + `Cecil sells the ${c.name} doll`, idx >= 0, `trade #${idx}`);
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
    ok(N + `...bought in his window for ${price} ${buyId}`, (await has(c.doll)) === 1 && (await has(buyId)) === 0, `dolls ${await has(c.doll)}`);
    await run(`${O}kill ${CEC}`);
    await run(`clear TestRat *[minecraft:custom_data~{bm:"${c.doll}"}]`); await run(`loot replace entity TestRat hotbar.6 loot bm:items/${c.doll}`);
    await at(X + 2.5, Y + 1, Z - 4.5, 180, 45); A.slot(6); await sleep(200); A.use(); await sleep(350); A.release(); await sleep(600);
    const DD = `@e[type=minecraft:item_display,tag=bm.${c.doll}d,x=${X + 2.5},y=${Y + 1},z=${Z - 6.5},distance=..0.4,limit=1]`;
    const DH = `@e[type=minecraft:interaction,tag=bm.${c.doll}hit,x=${X + 2.5},y=${Y + 1},z=${Z - 6.5},distance=..0.4,limit=1]`;
    ok(N + 'the doll set down on a block by a use: his own model', (await cnt(DD)) === 1 && (await has(c.doll)) === 0 && new RegExp(c.doll).test(await nbt(DD, 'item.components')),
       `${await cnt(DD)} ${await cnt(DH)}`);
    const y0 = await num(DD, 'Rotation[0]'); let dh = await entOf(DH); if (dh) A.interact(dh.entityId); await sleep(700);
    const y1 = await num(DD, 'Rotation[0]');
    ok(N + '...right-clicked: it twirls', Math.abs(((y1 - y0 + 540) % 360) - 180) > 30, `${y0} -> ${y1}`);
    A.input({ shift: true }); await sleep(250); dh = await entOf(DH); if (dh) A.attack(dh.entityId); await sleep(700); A.input({}); await sleep(300);
    ok(N + '...sneak + punch: back in the pack', (await has(c.doll)) === 1 && (await cnt(DD)) === 0);

    // ---------------------------------------------------------------- his fighting
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
    await sleep(2200); await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(2500);
    for (const o of ['mc', 'rc', 'cc', 'uc']) await run(`scoreboard players set ${PET} bm.${k}${o} 0`);
    await run('effect clear TestRat minecraft:absorption'); await run('effect clear TestRat minecraft:regeneration');
    const px = await num(PET, 'Pos[0]'), pz = await num(PET, 'Pos[2]');
    const FOE = '@e[type=minecraft:zombie,tag=bm.t183z,limit=1]';
    await run(`${O}summon minecraft:zombie ${px} ${Y + 1} ${pz + 5} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["bm.t183z","bm.seen"],attributes:[{id:"minecraft:max_health",base:400}],Health:400f,equipment:{head:{id:"minecraft:stone_button",count:1}}}`);
    A.bars.length = 0;
    const ult = await wait(6000, async () => (await score(`bm.${k}uc`, PET)) > 0, 150);
    ok(N + 'a foe five blocks off: his great blow first', ult, `uc ${await score(`bm.${k}uc`, PET)}`);
    await wait(3000, async () => A.bars.some(b => c.ult.test(b)));
    ok(N + '...its words to you, and what it does for you (' + c.ultFx + ')', A.bars.some(b => c.ult.test(b)) && (await hasFx('TestRat', c.ultFx)), A.bars.slice(-1).join(''));
    // (what the ranged blow leaves on them lasts 3-4 s: watched for together with the blow itself)
    const mark = who === 'dennis' ? async () => hasFx(FOE, 'slowness') : async () => (await hasFx(FOE, 'glowing')) && (await hasFx('TestRat', 'speed'));
    let marked = false;
    // (3.0a: he walks in on a foe - by the end of his great blow he can be in reach of it, where his melee comes first and his
    //  ranged blow never does: the foe is kept 6 blocks off him (inside the arena) until the ranged blow lands)
    const keepOff = async () => { const ax = await num(PET, 'Pos[0]'), az = await num(PET, 'Pos[2]'), fx = await num(FOE, 'Pos[0]'), fz = await num(FOE, 'Pos[2]');
      if (Math.hypot(fx - ax, fz - az) < 4.5) await run(`${O}tp ${FOE} ${ax.toFixed(2)} ${Y + 1} ${(az + 6 <= Z + 9 ? az + 6 : az - 6).toFixed(2)}`); };
    const rng = await wait(8000, async () => { if (await mark()) marked = true; if ((await score(`bm.${k}rc`, PET)) > 0 && marked) return true; if (!(await score(`bm.${k}rc`, PET) > 0)) await keepOff(); return false; }, 150);
    ok(N + '...then his ranged blow', (await score(`bm.${k}rc`, PET)) > 0, `rc ${await score(`bm.${k}rc`, PET)}`);
    ok(N + '...the foe hurt by them', (await num(FOE, 'Health')) < 400 - 10, `${await num(FOE, 'Health')}`);
    ok(N + (who === 'dennis' ? '...Gold Rush slows it' : '...the spirit makes it glow; you, light of foot (Speed)'), rng);
    const qx = await num(PET, 'Pos[0]'), qz = await num(PET, 'Pos[2]');
    A.bars.length = 0; for (const o of ['mc', 'cc']) await run(`scoreboard players set ${PET} bm.${k}${o} 0`);   // (he may have closed in already)
    await run(`${O}tp ${FOE} ${qx} ${Y + 1} ${qz + 1.6}`);
    const crowd = await wait(6000, async () => (await score(`bm.${k}cc`, PET)) > 0, 150);
    ok(N + 'the foe up close: his crowd blow', crowd && await wait(2000, async () => A.bars.some(b => c.crowd.test(b))), A.bars.slice(-1).join(''));
    // (3.0a: after his crowd blow he can wander back to you, out of reach of it - then his ranged blow comes, not his melee: the
    //  foe is kept at his side until the melee lands)
    const keepNear = async () => { const ax = await num(PET, 'Pos[0]'), az = await num(PET, 'Pos[2]'), fx = await num(FOE, 'Pos[0]'), fz = await num(FOE, 'Pos[2]');
      if (Math.hypot(fx - ax, fz - az) > 2.2) await run(`${O}tp ${FOE} ${ax.toFixed(2)} ${Y + 1} ${(az + 1.6).toFixed(2)}`); };
    const melee = await wait(6000, async () => { if ((await score(`bm.${k}mc`, PET)) > 0) return true; await keepNear(); return false; }, 150);
    ok(N + '...and his melee', melee, `mc ${await score(`bm.${k}mc`, PET)}`);
    await run(`${O}kill @e[tag=bm.t183z]`);
    if (who === 'pistachio') {
      await run('effect clear TestRat'); await sleep(300);         // (no Ward, no regeneration: down to 2 hearts)
      await run(`${O}damage TestRat 16 minecraft:generic`); A.bars.length = 0;
      const esc = await wait(3000, async () => hasFx('TestRat', 'invisibility'));
      ok(N + 'you at 2 hearts: Phantom Escape - unseen, unharmed a moment', esc && A.bars.some(b => /Phantom Escape/.test(b)) && (await score('bm.pisv')) > 50, A.bars.slice(-1).join(''));
      await run('effect give TestRat minecraft:instant_health 1 3 true'); await run('effect give TestRat minecraft:resistance 900 4 true');
    }

    // ---------------------------------------------------------------- his passive: Fortune V / Looting V
    await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..20]`);
    await sneakMenu(0); await click(/Sit \/ follow/); await sleep(1200);             // (sat: he stays out of it)
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 30);
    if (who === 'dennis') {
      await run('item replace entity TestRat hotbar.7 with minecraft:diamond_pickaxe[minecraft:enchantments={"minecraft:efficiency":5}]');
      await run('effect give TestRat minecraft:haste 600 1 true'); A.slot(7); await sleep(400);
      const dig = async (x, y, z) => { await A.mine(x, y, z, 200); await sleep(900); };
      let mined = 0;
      const ores = async (n) => { mined = 0; await run('clear TestRat minecraft:diamond'); await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`); for (let i = 0; i < n; i++) { await run(`${O}setblock ${X + 1} ${Y + 1} ${Z + 1 + (i % 2)} minecraft:diamond_ore`); await sleep(150); await dig(X + 1, Y + 1, Z + 1 + (i % 2));
          if (/passed/.test(await run(`${O}execute if block ${X + 1} ${Y + 1} ${Z + 1 + (i % 2)} minecraft:air`))) mined++; }
        await sleep(1500); const got = (await plain('diamond')) + (await ground('diamond', X, Y + 1, Z)); await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`); return got; };
      await wait(3000, async () => (await score('bm.dwft')) === 1);
      ok(N + 'with you: Fortune V marked on you (bm.dwft)', (await score('bm.dwft')) === 1);
      const got = await ores(6);
      ok(N + '...six diamond ores, a plain pickaxe: far more than six diamonds', got >= 10, `${got} diamonds`);
      await run(`kill ${PET}`); await sleep(2500);
      ok(N + '...sent away: the mark gone', (await score('bm.dwft')) === 0);
      const got0 = await ores(4);
      ok(N + '...without him: one diamond an ore', mined >= 3 && got0 === mined, `${got0} diamonds from ${mined} ores`);
      await run('effect clear TestRat minecraft:haste');
    } else {
      await run('item replace entity TestRat hotbar.7 with minecraft:iron_sword'); A.slot(7); await sleep(400);
      const flesh = async () => (await plain('rotten_flesh')) + (await ground('rotten_flesh', X, Y + 1, Z));
      const zombies = async (n) => { await run('clear TestRat minecraft:rotten_flesh'); await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
        let dead = 0, most = 0, total = 0;
        for (let i = 0; i < n; i++) {
          await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y + 1} ${Z + 2.2} {NoAI:1b,Health:1f,PersistenceRequired:1b,Tags:["bm.t183k","bm.seen"],IsBaby:0b}`); await sleep(500);
          const zs = '@e[type=minecraft:zombie,tag=bm.t183k,limit=1]'; let z = null; await wait(2000, async () => (z = await entOf(zs)) != null, 100);
          if (z) { A.attack(z.entityId); await sleep(1300); } if ((await cnt(zs)) === 0) dead++; else await run(`${O}kill ${zs}`);
          const now = await flesh(); most = Math.max(most, now - total); total = now;      // (what this one zombie dropped)
        }
        await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`); await run('clear TestRat minecraft:rotten_flesh'); return [dead, most, total]; };
      await wait(3000, async () => (await score('bm.pslt')) === 1);
      ok(N + 'with you: Looting V marked on you (bm.pslt)', (await score('bm.pslt')) === 1);
      const [d1, m1, f1] = await zombies(8);
      ok(N + '...eight zombies slain with a plain sword: one drops more than a zombie can (3+ flesh)', d1 === 8 && m1 >= 3, `${d1} slain, most ${m1}, ${f1} flesh in all`);
      await run(`kill ${PET}`); await sleep(2500);
      ok(N + '...sent away: the mark gone', (await score('bm.pslt')) === 0);
      const [d0, m0, f0] = await zombies(8);
      ok(N + '...without him: never more than two from one', d0 === 8 && m0 <= 2, `${d0} slain, most ${m0}, ${f0} flesh in all`);
    }
    await run(`scoreboard players set TestRat bm.${k}cd 0`);
    await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..20]`);

    // ---------------------------------------------------------------- knocked out: he faints
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
    await sleep(2200); await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
    A.chats.length = 0; await run(`${O}damage ${PET} 200 minecraft:mob_attack`);
    ok(N + 'struck down: he faints, his rig fades away', await wait(4000, async () => (await cnt(`@e[type=minecraft:item_display,tag=bm.${k}p_pet]`)) === 0));
    ok(N + `..."${c.name} faints!" - two minutes on his item (2.82t)`, A.chats.some(c2 => new RegExp(c.name + ' faints!').test(c2)) && (await score(`bm.${k}cd`)) > 100, A.chats.slice(-1).join('').slice(0, 160));
    await sleep(2200); A.bars.length = 0; await use(0); await sleep(800);
    ok(N + '...used again: "still getting his breath back", no one comes', (await cnt(PET)) === 0 && A.bars.some(b => /getting his breath back/.test(b)), A.bars.slice(-1).join(''));

    // ---------------------------------------------------------------- clean up
    await run(`scoreboard players set TestRat bm.${k}cd 0`); await run(`tag TestRat remove bm.arw${c.ar}`); await sleep(1200);
    await run(`kill @e[type=minecraft:wolf,tag=bm.${k}pet]`);
    await run('clear TestRat'); await run('effect clear TestRat'); await run(`scoreboard players set TestRat ${c.cos} 0`);
  }
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

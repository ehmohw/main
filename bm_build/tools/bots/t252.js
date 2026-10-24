// 2.92: QUEEN AVA'S HONOURS AND THE KINGDOM'S ARMOURY - as a regular (non-op) player: every click a real packet, every
// follower called with their own item, every honour bought with the button the dialog showed (rcon sets the stage: the castle,
// the pearls and tokens, a follower sent home between scenes, a rank). Vesper's retired Ward handed back in Dread Tokens;
// Queen Ava and Leo at the Tide Font - Ava's Honours open, and her Royal Blessing (Vitality I) for both; Leo's page - (2.94) one Honour,
// three ranks: rank I (8 pearls, his tribute) - all three to II, his armour up; rank III refused without an Elemental Gem, then bought with one; the Tide's
// Haste (Swift Return I); the Ethereal Gem with the royal family - THE HEART COMES HOME (+2 hearts; the dome warded) - and with
// Apophiss - THE SERPENT'S RESTRAINT (a rank of every honour for him); Leo's Aegis (a Knight) and Emma's Crescent (a Champion,
// the castle restored); the Aegis's Tidal Charge (sneak + a real jump); the Crescent's Ethereal Step (use) and Bloom Slam (sneak +
// use - a zombie hurt); a Tidewarden piece and Leo's Trident in the Steward's stock, none of it at Cecil's any more.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const score = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const tagged = async (t) => (await run('tag TestRat list')).includes(t);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const click = async (sel, sneak = false) => { await wait(3000, async () => !!(await entOf(sel))); const e = await entOf(sel); if (!e) return false;
    if (sneak) { A.input({ shift: true }); await sleep(800); } A.interact(e.entityId, sneak); await sleep(900); if (sneak) { A.input({}); await sleep(200); } return true; };
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(400); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(200); } await sleep(300); };
  const give = async (slot, iid, n = 1) => { await run(`loot replace entity TestRat hotbar.${slot} loot bm:items/${iid}`); if (n > 1) await run(`item modify entity TestRat hotbar.${slot} {type:"minecraft:set_count",count:${n}}`); await sleep(300); };
  const said = (re) => A.chats.some(c => re.test(c)) || A.bars.some(c => re.test(c)) || A.titles.some(c => re.test(c));
  const screen = () => A.dialogN.length ? JSON.stringify(A.dialogN[A.dialogN.length - 1]) : '';
  const CD = { emma: 'bm.emcd', ava: 'bm.avcd', pearlq: 'bm.pqcd', bones: 'bm.bjcd', apo: 'bm.apcd', leo: 'bm.lecd' };
  const home = async (w) => { await run('execute as TestRat run scoreboard players operation #me bm.pid = @s bm.pid');   // (whose followers)
    await run(`execute as TestRat run function bm:p98/home/${w}`).catch(() => {}); await sleep(600); await run(`scoreboard players reset TestRat ${CD[w]}`); };
  const X = 26000, Y = 31, Z = 26000;
  const CORE = `@e[type=minecraft:marker,tag=bm.kingdom,x=${X},y=${Y},z=${Z},distance=..60,limit=1]`;
  const BOX = (t) => `@e[type=minecraft:interaction,tag=${t},x=${X},y=${Y},z=${Z},distance=..70,limit=1]`;
  const cx = X + 0.5, cy = Y + 4, cz = Z + 6.5;
  const pet = (tag) => `@e[tag=${tag},tag=!bm.ffpet,x=${X},y=${Y},z=${Z},distance=..60,limit=1]`;

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance 1500 4 true'); await run('effect give TestRat minecraft:saturation 1500 0 true');
  for (const t of ['bm.kh_emma', 'bm.kh_ava', 'bm.kh_pearl', 'bm.kh_bones', 'bm.kh_court', 'bm.kh_apo', 'bm.kh_pardon', 'bm.keth_r', 'bm.keth_a', 'bm.kg_aegis', 'bm.kg_cres'])
    await run(`tag TestRat remove ${t}`);
  for (const o of ['bm.ktrib', 'bm.kreq', 'bm.kaud', 'bm.kfav', 'bm.krank', 'bm.fret', 'bm.fward', 'bm.fvig', 'bm.hn_leo', 'bm.hn_ava', 'bm.hn_apo', 'bm.hn_emma', 'bm.hn_pearlq',
                   'bm.bk_dread', 'bm.agcd', 'bm.crst', 'bm.crcd2'])
    await run(`scoreboard players reset TestRat ${o}`);
  await run('attribute TestRat minecraft:max_health modifier remove bm:heart_home');
  await run('scoreboard players set #hard bm.cfg 1');
  for (const w of ['emma', 'ava', 'pearlq', 'bones', 'apo', 'leo']) await home(w);
  await run(`${O}tp TestRat ${X + 200} 120 ${Z}`); await sleep(1500);
  await run(`${O}forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..90]`);
  for (let z = Z - 46; z <= Z + 46; z += 8) {
    await run(`${O}fill ${X - 46} ${Y - 5} ${z} ${X + 46} ${Y - 1} ${Math.min(z + 7, Z + 46)} minecraft:sand`);
    await run(`${O}fill ${X - 46} ${Y} ${z} ${X + 46} ${Y + 31} ${Math.min(z + 7, Z + 46)} minecraft:water`);
  }
  await run(`${O}execute positioned ${X} ${Y} ${Z} run function bm:admin/kingdom`); await sleep(2500);
  await run(`scoreboard players set ${CORE} bm.kbr -1`);
  ok('the castle, and its insignia hung: three plaques (the gate, the keep\'s door, behind the thrones)',
     (await cnt(CORE)) === 1 && await wait(3000, async () => (await cnt(`@e[type=minecraft:item_display,tag=bm.kinsig,x=${X},y=${Y},z=${Z},distance=..70]`)) === 3));

  // ---- Vesper's Ward, retired: its tokens handed back
  await run('scoreboard players set TestRat bm.fward 2');
  ok("Vesper's retired Ward II: its 7 Dread Tokens handed back", await wait(3000, async () => (await has('dread_token')) === 7) && (await score('bm.fward')) === 0 && said(/retired/));
  await run('clear TestRat');

  // ---- Queen Ava and Leo at the Font: her Honours, and her blessing
  await at(cx, cy, cz + 1, 0, 10);
  await give(0, 'av_locket'); await give(1, 'leo_crest'); await sleep(1000);
  await use(0); await sleep(2500); await use(1); await sleep(2500);
  ok('Queen Ava and Leo called with their own things', (await cnt(pet('bm.avpet'))) === 1 && (await cnt(pet('bm.leopet'))) === 1);
  A.chats.length = 0; A.dialogN.length = 0; await click(BOX('bm.kfont')); await sleep(1200);
  ok("the Font with Ava: QUEEN AVA'S HONOURS open - a page for each of them (her and Leo)", /QUEEN AVA'S HONOURS/.test(screen()) && /Leo/.test(screen()) && /Queen Ava/.test(screen()), screen().slice(0, 300));
  ok('...the ROYAL BLESSING for both: Vitality I, free', said(/ROYAL BLESSING/) && (await score('bm.hn_leo')) === 1001 && (await score('bm.hn_ava')) === 1001,
     `leo ${await score('bm.hn_leo')} ava ${await score('bm.hn_ava')}`);
  ok("...on Leo himself (within a second): his health up a fifth", await wait(3000, async () => /0\.2/.test(await run(`${O}attribute ${pet('bm.leopet')} minecraft:max_health modifier value get bm:royal_vitality`))));
  // Leo's page (2.94: one Honour, three ranks - each raises all three)
  await give(5, 'royal_pearl', 8);
  let b = await A.press(/Leo/);
  ok("Leo's page: the Honour, unranked; Vitality at one (the blessing)", !!(b && b.next) && /Honour/.test(screen()) && /○○○/.test(screen()) && /●○○○○/.test(screen()), screen().slice(0, 300));
  await run('item replace entity TestRat hotbar.8 with minecraft:iron_ingot 16');      // (Leo's tribute for the first rank)
  const pr0 = await has('royal_pearl');
  b = await A.press(/Honour \+1/);
  ok('Honour +1 (8 Royal Pearls and 16 iron, his tribute): Honour I - Vitality, Bulwark and Might II; his armour +6', (await run('clear TestRat minecraft:iron_ingot 0')).includes('No items') && (await score('bm.hn_leo')) === 1222 && (await has('royal_pearl')) === pr0 - 8 &&
     await wait(3000, async () => / 6(\.0)?\b/.test(await run(`${O}attribute ${pet('bm.leopet')} minecraft:armor modifier value get bm:royal_bulwark`))),
     `hn ${await score('bm.hn_leo')} pearls ${await has('royal_pearl')}`);
  // Honour III: wants an Elemental Gem
  await run('scoreboard players set TestRat bm.hn_leo 1444'); await run('clear TestRat *[minecraft:custom_data~{bm:"royal_pearl"}]'); await give(5, 'royal_pearl', 36); await give(6, 'dread_token', 8);
  await run('item replace entity TestRat hotbar.8 with minecraft:heart_of_the_sea 1');  // (his last tribute)
  await A.press(/« Her honours/); await A.press(/Leo/);
  A.bars.length = 0; await A.press(/Honour \+1/);
  ok('Honour III without an Elemental Gem: refused (a piece of the kingdom\'s heart)', (await score('bm.hn_leo')) === 1444 && said(/Elemental Gem/));
  await give(7, 'gem_rock');
  await A.press(/« Her honours/); await A.press(/Leo/); await A.press(/Honour \+1/);
  ok('...with one (any of Water, Rock, Fire): Honour III (28 pearls, 3 Dread Tokens, the gem spent) - all three V, his Might on his host', (await score('bm.hn_leo')) === 1555 && (await has('gem_rock')) === 0 &&
     (await has('royal_pearl')) === 8 && await wait(3000, async () => (await score('bm.kua', pet('bm.leopet'))) === 5), `hn ${await score('bm.hn_leo')} pearls ${await has('royal_pearl')}`);
  // the Tide's Haste
  await give(5, 'royal_pearl', 12); await give(6, 'dread_token', 3);
  await A.press(/« Her honours/);
  await A.press(/Tide's Haste/);
  ok("the Tide's Haste +1 (12 pearls, 3 Dread Tokens): Swift Return I", (await score('bm.fret')) === 1 && said(/Tide's Haste I/));

  // ---- Leo's Aegis: a Knight of the Tide
  await run('scoreboard players set TestRat bm.krank 2');
  A.chats.length = 0; await click(BOX('bm.kfont')); await sleep(800);
  ok("Leo at the Font, you a Knight: Leo's Aegis", (await has('leo_aegis')) === 1 && await tagged('bm.kg_aegis') && said(/hold the line/));
  await home('leo');

  // ---- the Ethereal Gem with the royal family: THE HEART COMES HOME (and Emma's Crescent: the castle restored, a Champion)
  await run('scoreboard players set TestRat bm.krank 3');
  await give(2, 'emma_ribbon'); await give(3, 'pq_pearls'); await give(8, 'ethereal_gem');
  await use(2); await sleep(2500); await use(3); await sleep(2500);
  ok('Emma and Queen Pearl join Ava', (await cnt(pet('bm.emmapet'))) === 1 && (await cnt(pet('bm.pqpet'))) === 1 && (await cnt(pet('bm.avpet'))) === 1);
  A.chats.length = 0; A.titles.length = 0; await click(BOX('bm.kfont')); await sleep(1500);
  ok('THE HEART COMES HOME: the title, +2 hearts for good, the dome warded', said(/Heart Comes Home/) && await tagged('bm.keth_r') && (await has('ethereal_gem')) === 1 &&
     /bm\.keth/.test(await run(`${O}data get entity ${CORE} Tags`)) &&
     await wait(3000, async () => /4\.0/.test(await run('attribute TestRat minecraft:max_health modifier value get bm:heart_home'))));
  ok("...and Emma's Crescent (the castle restored, you a Champion)", (await has('emma_crescent')) === 1 && await tagged('bm.kg_cres') && said(/crescent/i));
  for (const w of ['emma', 'pearlq', 'ava']) await home(w);

  // ---- the Ethereal Gem with Apophiss: THE SERPENT'S RESTRAINT
  await give(4, 'apo_oath'); await use(4); await sleep(3000);
  ok('Apophiss called with his oath', (await cnt(pet('bm.appet'))) === 1);
  A.chats.length = 0; A.titles.length = 0; await click(BOX('bm.kfont')); await sleep(1500);
  ok("THE SERPENT'S RESTRAINT: he doesn't take it - a rank of every honour for him", said(/Serpent's Restraint/) && await tagged('bm.keth_a') && (await has('ethereal_gem')) === 1 &&
     (await score('bm.hn_apo')) === 111, `hn_apo ${await score('bm.hn_apo')} | ${A.chats.slice(-3).join(' / ')} | ${A.titles.join(' / ')}`);
  await home('apo');

  // ---- the Aegis's Tidal Charge (sneak + a real jump)
  const GX = X + 300, GY = 100, GZ = Z;
  await run(`${O}fill ${GX - 2} ${GY - 1} ${GZ - 2} ${GX + 2} ${GY - 1} ${GZ + 14} minecraft:stone`); await run(`${O}fill ${GX - 2} ${GY} ${GZ - 2} ${GX + 2} ${GY + 3} ${GZ + 14} minecraft:air`);
  await run('clear TestRat'); await give(0, 'leo_aegis'); A.slot(0);
  await at(GX + 0.5, GY, GZ + 0.5, 0, 0);
  A.input({ shift: true }); await sleep(300); A.input({ shift: true, jump: true }); await sleep(250); A.input({}); await sleep(200);
  ok("the Aegis's TIDAL CHARGE: sneak + jump - you charge ahead", await wait(3000, async () => A.pos && A.pos.z > GZ + 4) && (await score('bm.agcd')) > 0,
     A.pos ? `z ${(A.pos.z - GZ).toFixed(1)}, cd ${await score('bm.agcd')}` : '');

  // ---- the Crescent: Ethereal Step and Bloom Slam
  await run('clear TestRat'); await give(0, 'emma_crescent');
  await at(GX + 0.5, GY, GZ + 0.5, 0, 0);
  await use(0);
  ok("the Crescent's ETHEREAL STEP (use): a blink ahead", await wait(2000, async () => A.pos && A.pos.z > GZ + 4), A.pos ? `z ${(A.pos.z - GZ).toFixed(1)}` : '');
  await at(GX + 0.5, GY, GZ + 0.5, 0, 0);
  await run(`${O}summon minecraft:zombie ${GX + 0.5} ${GY} ${GZ + 3.5} {Tags:["bm.t252z"],NoAI:1b,PersistenceRequired:1b,Health:40f,attributes:[{id:"minecraft:max_health",base:40d}]}`); await sleep(400);
  await use(0, true); await sleep(500);
  const zh = +((await run(`${O}data get entity @e[tag=bm.t252z,limit=1] Health`)).match(/([\d.]+)f/) || [0, 40])[1];
  ok("...BLOOM SLAM (sneak + use): the zombie hurt (16) and tossed; Absorption for you", zh <= 24.5 && /absorption/.test(await run('data get entity TestRat active_effects')), `zombie ${zh}`);
  await run(`${O}kill @e[tag=bm.t252z]`);

  // ---- the armoury's goods: the Steward's, not Cecil's
  const stew = `@e[type=minecraft:wandering_trader,tag=bm.kstew,x=${X},y=${Y},z=${Z},distance=..70,limit=1]`;
  const offers = [];
  for (let i = 0; i < 40; i++) { if (!/has the following/.test(await run(`${O}data get entity ${stew} Offers.Recipes[${i}].maxUses`))) break;
    const r = await run(`${O}data get entity ${stew} Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`); const m = r.match(/"([a-z_0-9]+)"/); if (m) offers.push(m[1]); }
  ok("the Royal Steward sells the armoury: Leo's Trident, the Bloomheart, every Tidewarden and Pearlguard piece", ['leo_trident', 'bloomheart_gem', 'tidewarden_head', 'tidewarden_chest',
     'pearlguard_head', 'pearlguard_feet'].every(i => offers.includes(i)), offers.join(','));
  const cec = await run('execute as @e[type=minecraft:villager,tag=bm.wizard,limit=1] run data get entity @s Offers');
  ok("...and Cecil sells neither Leo's Trident nor the Bloomheart now", !/leo_trident|bloomheart_gem/.test(cec));

  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  await run(`${O}forceload remove ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  for (const w of ['emma', 'ava', 'pearlq', 'apo', 'leo']) await home(w);
  await run('scoreboard players set #hard bm.cfg 0');
  process.exit(0);
})();

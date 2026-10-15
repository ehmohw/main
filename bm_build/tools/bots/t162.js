// 2.79: FISHY'S CABINET OF CURIOSITIES - as a regular (non-op) player, every step a real packet (rcon sets the stage: the hall
// in the Fixer's Lounge, the things to show, a clean cabinet): Fishy at his desk, right-clicked empty-handed - he joins you (his
// Pocket Bowl); again - the Cabinet's menu; a wing's page, every exhibit veiled with its riddle; set out in the hall; a rare thing
// shown to him - a replica (the cabinet records it, world-wide, with your name), the thing itself kept; shown twice - "already";
// something ordinary - not for the cabinet; the page shows it given by you, the hall's case and plaque too; a lost bowl reissued;
// the same shown to YOUR Fishy out in the world. Then, as an admin, a wing filled: its rosette to who gave to it (set up, taken
// back), his power learned (the powers page), and his claws wither now.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const G = 'execute in bm:gutter run ';
  const cnt = async (sel, dim = G) => { const m = (await run(`${dim}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const has = async (iid) => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const uuidOf = async (sel, dim = G) => { const m = (await run(`${dim}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel, dim = G) => { const u = await uuidOf(sel, dim); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const OX = -320, OY = 64, OZ = -256;
  const dd = (d) => d && (d.data || d);
  const HIT = '@e[type=minecraft:interaction,tag=bm.fynhit,limit=1]';
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run('function bm:admin/cabinet_reset'); await run('tag TestRat remove bm.fymet'); await run('kill @e[type=minecraft:wolf,tag=bm.fypet]');
  await run('scoreboard players set TestRat bm.fycd 0');
  await run('data remove storage bm:cab built'); await sleep(2500);
  ok('the hall: twenty cases, Fishy at his desk', (await cnt('@e[type=minecraft:item_display,tag=bm.cabslot]')) === 20 && (await cnt(HIT)) === 1 &&
     (await cnt('@e[type=minecraft:item_display,tag=bm.fyn]')) === 9);
  // ---- into the hall, at his desk
  const stand = async () => { await run(`${G}tp TestRat ${OX + 37.4} ${OY + 4} ${OZ + 12.5} -90 10`); await sleep(1500); };
  await stand();
  const clickFishy = async () => { const h = await entOf(HIT); if (!h) return false; A.interact(h.entityId); await sleep(900); return true; };
  A.chats.length = 0; A.slot(8); await sleep(200);
  ok('right-clicked empty-handed, the first time: he joins you - his Pocket Bowl', (await clickFishy()) && (await has('fy_bowl')) === 1 && A.chats.some(c => /Pocket Bowl/.test(c)),
     A.chats.slice(-1).join(''));
  await sleep(600); const n0 = A.dialogN.length;
  await clickFishy(); await wait(2000, async () => A.dialogN.length > n0, 100);
  const main = dd(A.dialogN[A.dialogN.length - 1]);
  ok('again: the Cabinet\'s menu', A.dialogN.length > n0 && /CABINET OF CURIOSITIES/.test(JSON.stringify(main && main.title)));
  ok('...six wings, each 0 of 20', ['The Hollow', 'The Gutter', 'The Skies', 'The Deep', 'The Wilds', 'The Court'].every(w => A.buttons().some(b => b.label.startsWith(w) && /0 of 20/.test(b.label))),
     A.buttons().map(b => b.label).join(' | '));
  const pg = await A.press(/^The Hollow/);
  const page = dd(A.dialogN[A.dialogN.length - 1]);
  const items = (page && page.body || []).filter(b => b.type === 'minecraft:item' || b.type === 'item');
  ok('a wing\'s page: twenty exhibits', pg && pg.next && items.length === 20, `${items.length}`);
  ok('...all veiled, each with its riddle', items.every(b => JSON.stringify(b.item).includes('cab_veiled')) && /throne/.test(JSON.stringify(items[0].description)),
     JSON.stringify(items[0] && items[0].description).slice(0, 120));
  await A.press(/Set it out in the hall/); await sleep(800);
  ok('set out in the hall: the Hollow\'s cases veiled', (await sc('#hall', 'bm.cab')) === 1 && /cab_veiled/.test(await run(`${G}data get entity @e[type=minecraft:item_display,tag=bm.cabslot,scores={bm.cabi=1},limit=1] item`)));
  // ---- a rare thing shown: a replica - you keep yours
  await run('loot replace entity TestRat hotbar.1 loot bm:items/trophy_hollow'); A.slot(1); await sleep(400);
  A.chats.length = 0; await clickFishy(); await sleep(1200);
  ok('the Hollow King Trophy shown to him: the cabinet records it, with your name', /TestRat/.test(await run('data get storage bm:cab got.trophy_hollow.by')),
     await run('data get storage bm:cab got.trophy_hollow'));
  ok('...the trophy itself is still yours', (await has('trophy_hollow')) === 1);
  ok('...the Hollow: 1 of 20 - and everyone is told', (await sc('#hollow', 'bm.cab')) === 1 && A.chats.some(c => /showed Fishy.*Hollow King Trophy/.test(c)), A.chats.join(' / ').slice(0, 200));
  ok('...its case in the hall holds the replica, its plaque your name', /trophy_hollow/.test(await run(`${G}data get entity @e[type=minecraft:item_display,tag=bm.cabslot,scores={bm.cabi=1},limit=1] item`)) &&
     /TestRat/.test(await run(`${G}data get entity @e[type=minecraft:text_display,tag=bm.cablbl,scores={bm.cabi=1},limit=1] text`)));
  A.chats.length = 0; await sleep(500); await clickFishy(); await sleep(800);
  ok('shown again: "already in the Cabinet" - nothing counted twice', (await sc('#hollow', 'bm.cab')) === 1 && A.chats.some(c => /already in the Cabinet/i.test(c)), A.chats.slice(-1).join(''));
  await run('loot replace entity TestRat hotbar.2 loot bm:items/token'); A.slot(2); await sleep(400);
  A.bars.length = 0; await clickFishy(); await sleep(600);
  ok('something ordinary: not for the cabinet', A.bars.some(b => /Cabinet|rare/i.test(b)) && (await sc('#all', 'bm.cab')) === 1, A.bars.slice(-1).join(''));
  A.slot(8); await sleep(300); const n1 = A.dialogN.length; await clickFishy(); await wait(2000, async () => A.dialogN.length > n1, 100);
  await A.press(/^The Hollow/);
  const page2 = dd(A.dialogN[A.dialogN.length - 1]); const it2 = (page2.body || []).filter(b => /item/.test(b.type));
  ok('the page now: the trophy as itself, "given by TestRat"', /trophy/.test(JSON.stringify(it2[0].item)) && /given by/.test(JSON.stringify(it2[0].description)) && /TestRat/.test(JSON.stringify(it2[0].description)),
     JSON.stringify(it2[0].description).slice(0, 160));
  ok('...its title: 1 of 20', /1/.test(JSON.stringify(page2.title)));
  // ---- a lost bowl: he has a spare
  await run('clear TestRat *[minecraft:custom_data~{bm:"fy_bowl"}]'); A.slot(8); await sleep(300); await clickFishy(); await sleep(600);
  ok('the Pocket Bowl lost: empty-handed at his desk, he gives you a spare', (await has('fy_bowl')) === 1);
  // ---- your own Fishy, out in the world: show him the next thing
  const O = 'execute in minecraft:overworld run ', X = 16540, Y = 100, Z = 16000;
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`);
  await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 6} ${Z + 8} minecraft:air`); await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2500);
  const slotOf = async (iid) => { const inv = await run('data get entity TestRat Inventory'); const m = inv.match(new RegExp(`\\{Slot: (\\d+)b[^{}]*?id: "[^"]+"[^]*?bm: "${iid}"`)); return m ? +m[1] : -1; };
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/fy_bowl'); await run('loot replace entity TestRat hotbar.3 loot bm:items/emblem_hollow');
  A.slot(0); await sleep(300); A.use(); await sleep(350); A.release(); await sleep(1500);
  const PET = '@e[type=minecraft:wolf,tag=bm.fypet,limit=1]';
  ok('his Pocket Bowl used: Fishy comes', (await cnt(PET, O)) === 1);
  await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 2.5}`); await sleep(1500);
  const box = await entOf('@e[type=minecraft:interaction,tag=bm.fyhit,limit=1]', O);
  A.slot(3); await sleep(300); if (box) A.interact(box.entityId); await sleep(1200);
  ok('the Crown of Conquest shown to YOUR Fishy: into the cabinet too', box && /TestRat/.test(await run('data get storage bm:cab got.emblem_hollow.by')) && (await sc('#hollow', 'bm.cab')) === 2);
  ok('...and the crown is still yours', (await has('emblem_hollow')) === 1);
  // ---- as an admin: the Hollow filled - its rosette to who gave to it, his power learned
  await run('op TestRat'); await sleep(400); A.cmd('function bm:admin/cabinet_fill_hollow'); await sleep(1500); await run('deop TestRat'); await sleep(300);
  ok('(admin) the Hollow filled: complete, his power learned', (await sc('#hollow', 'bm.cab')) === 20 && (await sc('#f_hollow', 'bm.cab')) === 1);
  ok('...the rosette is yours (you gave to it) - and its challenge', await wait(3000, async () => (await has('cab_rosette_hollow')) === 1) &&
     /passed/.test(await run('execute if entity @a[name=TestRat,advancements={bm:story/cab_hollow=true}]')));
  // the rosette set up (sneak + use on the floor), taken back (sneak + punch)
  await run('clear TestRat *[minecraft:custom_data~{bm:"cab_rosette_hollow"}]'); await run('loot replace entity TestRat hotbar.5 loot bm:items/cab_rosette_hollow'); A.slot(5); await sleep(300);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 50`); await sleep(800);
  A.input({ shift: true }); await sleep(300); A.use(); await sleep(350); A.release(); await sleep(400); A.input({}); await sleep(600);
  const ROS = `@e[type=minecraft:item_display,tag=bm.cabros,x=${X},y=${Y},z=${Z},distance=..4]`;
  ok('the rosette set up on the floor (sneak + use)', (await cnt(ROS, O)) === 1 && (await has('cab_rosette_hollow')) === 0);
  const rb = await entOf(`@e[type=minecraft:interaction,tag=bm.gvdk_cab_rosette_hollow,limit=1]`, O);
  A.input({ shift: true }); await sleep(300); if (rb) A.attack(rb.entityId); await sleep(600); A.input({}); await sleep(300);
  ok('...and taken back (sneak + punch)', (await cnt(ROS, O)) === 0 && (await has('cab_rosette_hollow')) === 1);
  // his powers page, from his menu (sneak + use the bowl)
  A.slot(0); await sleep(250); A.input({ shift: true }); await sleep(250); const n2 = A.dialogN.length; A.use(); await sleep(350); A.release(); A.input({}); await wait(2000, async () => A.dialogN.length > n2, 100);
  const pw = await A.press(/Fishy's powers/);
  const pj = JSON.stringify(A.dialogN[A.dialogN.length - 1]);
  const prow = (nm) => JSON.stringify((dd(A.dialogN[A.dialogN.length - 1]).body || []).find(b => b.contents && b.contents.text === nm) || {});
  ok('his menu -> his powers: Hollow Grip LEARNED, the rest locked', pw && pw.next && /LEARNED/.test(prow('Hollow Grip')) && /locked/.test(prow('Coin Toss')), prow('Hollow Grip').slice(0, 200));
  // his claws wither now
  await run(`${O}summon minecraft:husk ${X + 0.5} ${Y + 1} ${Z + 3.5} {Tags:["bm.t162m","bm.seen"],PersistenceRequired:1b,attributes:[{id:"minecraft:movement_speed",base:0.0d}],Health:60f}`);
  await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 2.0}`);
  const withered = await wait(8000, async () => /minecraft:wither/.test(await run(`${O}data get entity @e[type=minecraft:husk,tag=bm.t162m,limit=1] active_effects`)), 300);
  ok('a husk beside him: his claws strike - and wither it (the Hollow Grip)', withered, await run(`${O}data get entity @e[type=minecraft:husk,tag=bm.t162m,limit=1] Health`));
  await run(`${O}kill @e[type=minecraft:husk,tag=bm.t162m]`); await run('kill @e[type=minecraft:wolf,tag=bm.fypet]');
  await run('function bm:admin/cabinet_reset'); await run('clear TestRat'); await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

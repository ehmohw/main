// 2.93: THE DREADBORNE AND THE SERAPH - as a regular (non-op) player: the three Dread bosses' rewards (rcon stands in for the
// fights) give the Visage, the Greaves and the Treads, then a Dread Heart; the heart, a netherite chestplate and an elytra
// dropped together forge the Dread Carapace (it glides); the set worn - night vision, poison and darkness thrown off, no fall
// damage, +4 health; DREAD RENDING on a sneaking strike at a netherite-plated zombie (through its armour), and its rest; each
// piece made holy beside a Golden Cross (the Seraph's own looks); SERAPHIC JUDGMENT (more to the undead, alight); a mixed set
// strikes neither.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const score = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const effects = async () => await run('data get entity TestRat active_effects');
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
  const X = 27000, Y = 120, Z = 27000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance 1500 4 true'); await run('effect give TestRat minecraft:saturation 1500 0 true');
  await run('tag TestRat remove bm.dheart'); for (const k of ['snow', 'witch', 'shark']) await run(`scoreboard players reset TestRat bm.dbwin_${k}`);
  await run('scoreboard players reset TestRat bm.dscd');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:stone`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 6} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`);
  await at(X + 0.5, Y, Z + 0.5, 0, 30);

  // ---- the three bosses, beaten (rcon stands in for the fights): a piece from each, then the Dread Heart
  const pieces = { snow: 'dread_visage', witch: 'dread_greaves', shark: 'dread_treads' };
  for (const [k, iid] of Object.entries(pieces)) {
    await run(`execute as TestRat at @s run function bm:p197/${k}/reward`); await sleep(400);
    ok(`the ${k} boss beaten: its piece - ${iid}`, (await has(iid)) === 1);
  }
  ok('...all three: their hearts beat as one - a DREAD HEART', await wait(3000, async () => (await has('dread_heart')) === 1) && said(/Dread Heart/));
  // the forge: drop the heart, a netherite chestplate and an elytra together
  await run('clear TestRat'); await give(0, 'dread_heart');
  await run('item replace entity TestRat hotbar.1 with minecraft:netherite_chestplate'); await run('item replace entity TestRat hotbar.2 with minecraft:elytra');
  await at(X + 0.5, Y, Z + 0.5, 0, 60);
  for (const sl of [1, 2, 0]) { A.slot(sl); await sleep(300); A.drop(); await sleep(500); }
  await at(X + 5.5, Y, Z + 0.5, 0, 60);                                        // (step back while it forges)
  ok('THE FORGE: the heart dropped beside a netherite chestplate and an elytra - the Dread Carapace comes up, the three spent',
     await wait(4000, async () => (await cnt(`@e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..6,nbt={Item:{components:{"minecraft:custom_data":{bm:"dread_carapace"}}}}]`)) === 1) &&
     (await cnt(`@e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..6]`)) === 1);
  await at(X + 0.5, Y, Z + 0.5, 0, 60); await wait(6000, async () => (await has('dread_carapace')) === 1);
  ok('...picked up: it glides (plate and wings)', (await has('dread_carapace')) === 1 && /glider/.test(await run('data get entity TestRat Inventory')));

  // ---- worn: the passives
  await run('clear TestRat');
  for (const [sl, iid] of [['head', 'dread_visage'], ['chest', 'dread_carapace'], ['legs', 'dread_greaves'], ['feet', 'dread_treads']])
    await run(`loot replace entity TestRat armor.${sl} loot bm:items/${iid}`);
  await run('effect give TestRat minecraft:poison 20 1'); await run('effect give TestRat minecraft:darkness 20 0');
  ok('the whole set worn: night vision; poison and darkness can\'t hold you', await wait(3000, async () => { const e = await effects(); return /night_vision/.test(e) && !/poison/.test(e) && !/darkness/.test(e); }));
  ok('...the Treads: no fall damage; the Carapace: +4 health', /-1/.test(await run('attribute TestRat minecraft:fall_damage_multiplier modifier value get bm:dread_treads_fall')) &&
     / 4(\.0)?\b/.test(await run('attribute TestRat minecraft:max_health modifier value get bm:dread_carapace_hp')));
  // ---- DREAD RENDING: sneak and strike a plated zombie
  const ZB = `@e[type=minecraft:zombie,tag=bm.t254z,limit=1]`;
  const hpOf = async () => +((await run(`${O}data get entity ${ZB} Health`)).match(/(-?[\d.]+)f/) || [0, -1])[1];
  const zombie = async () => { await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t254z]`);
    await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 2.0} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t254z"],attributes:[{id:"minecraft:max_health",base:300}],Health:300f,` +
              `equipment:{head:{id:"minecraft:netherite_helmet"},chest:{id:"minecraft:netherite_chestplate"},legs:{id:"minecraft:netherite_leggings"},feet:{id:"minecraft:netherite_boots"}}}`);
    await sleep(800); return await entOf(ZB); };
  await at(X + 0.5, Y, Z + 0.5, 0, 20);
  let z = await zombie();
  A.bars.length = 0; A.input({ shift: true }); await sleep(500); A.attack(z.entityId); await sleep(800); A.input({}); await sleep(300);
  let hp = await hpOf();
  ok('DREAD RENDING (sneak + strike, a netherite-plated zombie): 24 through its armour, withering - then 45 s to gather', hp <= 300 - 24 && (await score('bm.dscd')) >= 43 &&
     said(/DREAD RENDING/), `hp ${hp} cd ${await score('bm.dscd')}`);
  z = await zombie(); A.bars.length = 0; A.input({ shift: true }); await sleep(500); A.attack(z.entityId); await sleep(800); A.input({}); await sleep(300);
  ok('...again at once: still gathering', said(/still gathering/));

  // ---- THE SERAPH: each piece beside a Golden Cross
  const invs = []; await at(X + 0.5, Y, Z + 0.5, 0, 90);            // (looking down: dropped at your feet)
  for (const iid of ['dread_visage', 'dread_carapace', 'dread_greaves', 'dread_treads']) {
    await run('clear TestRat'); await give(0, iid); await give(1, 'golden_cross');          // (each made holy, then put away)
    for (const sl of [1, 0]) { A.slot(sl); await sleep(300); A.drop(); await sleep(400); }
    await at(X + 5.5, Y, Z + 0.5, 0, 90); await sleep(7000); await at(X + 0.5, Y, Z + 0.5, 0, 90);
    await wait(14000, async () => (await has(iid)) === 1, 500);
    invs.push(await run('data get entity TestRat Inventory'));
  }
  const inv = invs.join(' ');
  ok("each piece made holy at a Golden Cross: the Seraph's Gaze, Wings, Greaves and Treads (their own looks)", (inv.match(/bm_angel: 1b/g) || []).length === 4 &&
     /angel_dread_visage/.test(inv) && /seraph_wings/.test(inv) && /Seraph's Gaze/.test(inv), `holy ${(inv.match(/bm_angel: 1b/g) || []).length} gaze ${/angel_dread_visage/.test(inv)} wings ${/seraph_wings/.test(inv)} name ${/Seraph's Gaze/.test(inv)}`);
  await run('clear TestRat');
  for (const [sl, iid] of [['head', 'dread_visage'], ['chest', 'dread_carapace'], ['legs', 'dread_greaves'], ['feet', 'dread_treads']]) {
    await run(`loot replace entity TestRat armor.${sl} loot bm:items/${iid}`); await run(`item modify entity TestRat armor.${sl} bm:p182/up_${iid}`);
  }
  await run('scoreboard players reset TestRat bm.dscd');
  z = await zombie();
  A.bars.length = 0; A.input({ shift: true }); await sleep(500); A.attack(z.entityId); await sleep(800); A.input({}); await sleep(300);
  hp = await hpOf();
  const fire = +((await run(`${O}data get entity ${ZB} Fire`)).match(/(-?\d+)s/) || [0, 0])[1];
  ok('SERAPHIC JUDGMENT (the holy set): 24 through armour and 10 more to the undead, set alight', hp <= 300 - 34 && fire > 0 && said(/SERAPHIC JUDGMENT/), `hp ${hp} fire ${fire}`);
  // a mixed set is neither
  await run('loot replace entity TestRat armor.head loot bm:items/dread_visage'); await run('scoreboard players reset TestRat bm.dscd');
  z = await zombie(); A.bars.length = 0;
  A.input({ shift: true }); await sleep(500); A.attack(z.entityId); await sleep(800); A.input({}); await sleep(300);
  ok('...one dread piece among the holy: neither set - no strike', !(said(/SERAPHIC JUDGMENT/) || said(/DREAD RENDING/)) && (await score('bm.dscd')) <= 0);

  await run(`${O}kill @e[type=minecraft:zombie,tag=bm.t254z]`); await run('clear TestRat');
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..20]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

// 2.91: THE UNDERWATER KINGDOM - as a regular (non-op) player, every click a real packet, every royal called with their own item
// (rcon sets the stage: a deep sea, the castle built on its floor, the items, a follower sent home between scenes, a breach's
// clock run down). In through the Tide Door (and out again); the "Underwater Kingdom" title; the Tide Font with nobody (who's
// missing); Emma called - her homecoming (the Tidecaller Shell, pearls) and a royal audience; the Shell used; the Royal Treasury's
// tribute (and not twice a day); the Request Stand (today's ask shown, fulfilled, favour); the Steward's stock and its daily
// special turning over; Queen Ava and Queen Pearl called - their homecomings, the Full Court: the Crown of the Deep, the castle
// restored (the fires out), the Tide Festival; Bones's homecoming; Apophiss brought in - the carved stone opens, his penance on
// the plinth (Tide-Breaker), and with Queen Ava there her pardon; a dome breach - three cracks sealed by hand, one left to
// burst (the sea gets in), the leak mended at the Dome Heart (2 pearls); the dome shattered - raised again with a Heart of the Sea.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const score = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const hasV = async (id) => +(((await run(`clear TestRat minecraft:${id} 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const block = async (x, y, z, b) => /passed/i.test(await run(`${O}execute if block ${x} ${y} ${z} ${b}`));
  const tagged = async (t) => (await run('tag TestRat list')).includes(t);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const click = async (sel, sneak = false) => { await wait(3000, async () => !!(await entOf(sel))); const e = await entOf(sel); if (!e) return false;
    if (sneak) { A.input({ shift: true }); await sleep(800); } A.interact(e.entityId, sneak); await sleep(900); if (sneak) { A.input({}); await sleep(200); } return true; };
  const use = async (slot) => { A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(300); };
  const said = (re) => A.chats.some(c => re.test(c)) || A.bars.some(c => re.test(c));
  const X = 24000, Y = 31, Z = 24000;                // the sea floor's top: the dome's floor (the seed's level)
  const CORE = `@e[type=minecraft:marker,tag=bm.kingdom,x=${X},y=${Y},z=${Z},distance=..60,limit=1]`;
  const BOX = (t) => `@e[type=minecraft:interaction,tag=${t},x=${X},y=${Y},z=${Z},distance=..70,limit=1]`;
  const cx = X + 0.5, cy = Y + 4, cz = Z + 6.5;      // the core marker (the throne room's middle)

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance 1200 4 true'); await run('effect give TestRat minecraft:saturation 1200 0 true');
  for (const t of ['bm.kh_emma', 'bm.kh_ava', 'bm.kh_pearl', 'bm.kh_bones', 'bm.kh_court', 'bm.kh_apo', 'bm.kh_pardon']) await run(`tag TestRat remove ${t}`);
  for (const o of ['bm.ktrib', 'bm.kreq', 'bm.kaud', 'bm.kfav', 'bm.krank', 'bm.kin']) await run(`scoreboard players reset TestRat ${o}`);
  // (the send-home functions act on the caller's own followers: #me is who's asking)
  await run('execute as TestRat run scoreboard players operation #me bm.pid = @s bm.pid');
  for (const w of ['emma', 'ava', 'pearlq', 'bones', 'apo']) await run(`execute as TestRat run function bm:p98/home/${w}`).catch(() => {});
  await run(`${O}tp TestRat ${X + 200} 120 ${Z}`); await sleep(1500);          // (start well clear of any castle left by an earlier run)
  // ---- the stage: a deep sea, 30 down, and the castle on its floor
  await run(`${O}forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`); await sleep(2500);   // (its entities load a moment after: an earlier run's castle core must be there to be cleared)
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..90]`);
  for (let z = Z - 46; z <= Z + 46; z += 8) {
    await run(`${O}fill ${X - 46} ${Y - 5} ${z} ${X + 46} ${Y - 1} ${Math.min(z + 7, Z + 46)} minecraft:sand`);
    await run(`${O}fill ${X - 46} ${Y} ${z} ${X + 46} ${Y + 31} ${Math.min(z + 7, Z + 46)} minecraft:water`);
  }
  await run(`${O}execute positioned ${X} ${Y} ${Z} run function bm:admin/kingdom`);
  await sleep(1500);
  await run(`scoreboard players set ${CORE} bm.kbcd 0`); await run('scoreboard players reset TestRat bm.kbask');
  ok('the castle is built on the sea floor: its core, five click-boxes (Font, Treasury, Request Stand, Dome Heart, plinth), the Steward',
     (await cnt(CORE)) === 1 && (await cnt(`@e[type=minecraft:interaction,tag=bm.kbox,x=${X},y=${Y},z=${Z},distance=..70]`)) === 5 &&
     (await cnt(`@e[type=minecraft:wandering_trader,tag=bm.kstew,x=${X},y=${Y},z=${Z},distance=..70]`)) === 1,
     `${await cnt(CORE)} core, ${await cnt(`@e[type=minecraft:interaction,tag=bm.kbox,x=${X},y=${Y},z=${Z},distance=..70]`)} boxes`);
  ok('...the dome is air inside (the yard), glass at its crown, the sea outside it', await block(X, Y + 20, Z, 'minecraft:air') &&
     await block(X, Y + 27, Z, 'minecraft:glass') && await block(X + 40, Y + 5, Z, 'minecraft:water'));

  // ---- the Tide Door: swim into it from outside; walk into it from inside
  A.titles.length = 0;
  await at(X + 0.5, Y + 1, Z - 34.5, 0, 0);
  const inside = await wait(3000, async () => A.pos && A.pos.z > Z - 31);
  ok('swum into the Tide Door from the sea: you\'re inside the dome', inside, A.pos ? `z ${A.pos.z.toFixed(1)}` : '');
  ok('..."The Underwater Kingdom" (the title)', await wait(3000, async () => A.titles.some(t => /Underwater Kingdom/.test(t))), A.titles.join(' | '));
  await at(X + 0.5, Y + 1, Z - 30.5, 180, 0);
  ok('walked into it from inside: out in the sea', await wait(3000, async () => A.pos && A.pos.z < Z - 35), A.pos ? `z ${A.pos.z.toFixed(1)}` : '');

  // ---- the Tide Font with nobody
  await at(cx, cy, cz + 1, 0, 10);
  A.chats.length = 0; await click(BOX('bm.kfont'));
  ok('the Tide Font, alone: it lies still, and says who to bring (each one missing)', said(/lies still/) && A.chats.filter(c => /not with you/.test(c)).length === 4,
     A.chats.slice(-5).join(' / '));

  // ---- Emma comes home
  await run('loot replace entity TestRat hotbar.0 loot bm:items/emma_ribbon'); await sleep(1500);
  await use(0); await wait(5000, async () => (await cnt('@e[type=minecraft:cat,tag=bm.emmapet]')) >= 1); await sleep(1500);
  ok('Emma called with her ribbon', (await cnt('@e[type=minecraft:cat,tag=bm.emmapet]')) >= 1);
  A.chats.length = 0; await click(BOX('bm.kfont')); await sleep(500);
  ok('the Font with Emma: her HOMECOMING (her words), the Tidecaller Shell, 4 pearls + a royal audience\'s 1', await tagged('bm.kh_emma') &&
     said(/HOMECOMING/) && said(/smaller than I remember/) && (await has('tidecaller_shell')) === 1 && (await has('royal_pearl')) === 5, `pearls ${await has('royal_pearl')}`);
  A.chats.length = 0; await click(BOX('bm.kfont')); await sleep(300);
  ok('...again: no second homecoming or audience today (the Font still names who\'s missing)', (await has('royal_pearl')) === 5 && (await has('tidecaller_shell')) === 1 &&
     said(/royal family together/));
  // the Tidecaller Shell
  await run('clear TestRat minecraft:emma_ribbon'); await run(`item replace entity TestRat hotbar.1 with minecraft:air`);
  for (let s = 0; s < 9; s++) { if (/tidecaller/.test(await run(`data get entity TestRat Inventory[{Slot:${s}b}]`))) { await use(s); break; } }
  await sleep(500);
  ok('the Tidecaller Shell used: Water Breathing, Dolphin\'s Grace, Conduit Power', /water_breathing/.test(await run('data get entity TestRat active_effects')) &&
     /conduit_power/.test(await run('data get entity TestRat active_effects')) && /dolphins_grace/.test(await run('data get entity TestRat active_effects')));

  // ---- the Royal Treasury
  await at(cx - 3, cy, cz, 90, 20);
  const p0 = await has('royal_pearl');
  A.chats.length = 0; await click(BOX('bm.ktrib'));
  ok('the Royal Treasury: today\'s tribute (2 + 1 for Emma beside you) and a gift', (await has('royal_pearl')) === p0 + 3 && said(/tribute/), `+${(await has('royal_pearl')) - p0}`);
  A.bars.length = 0; await click(BOX('bm.ktrib'));
  ok('...not twice in a day', (await has('royal_pearl')) === p0 + 3 && said(/paid you today/));

  // ---- the Request Stand
  const day = +(((await run('scoreboard players get #day bm.bm')).match(/has (-?\d+)/)) || [0, 0])[1];
  const REQ = [['kelp', 32, 2], ['prismarine_shard', 16, 2], ['cod', 16, 2], ['ink_sac', 8, 2], ['glass', 32, 3], ['sea_pickle', 8, 2], ['nautilus_shell', 1, 4],
               ['gold_ingot', 8, 3], ['stone_bricks', 64, 3], ['magenta_dye', 8, 2], ['tropical_fish', 4, 3], ['light_blue_dye', 8, 2]];
  const [rid, rn, rpay] = REQ[((day % 12) + 12) % 12];
  await at(cx + 3, cy, cz - 1, -90, 15);
  // (the pack's own items made of the same stuff - the Tidecaller Shell is a nautilus shell - are not what the steward asked for)
  await run(`give TestRat minecraft:${rid}[minecraft:custom_data={bm:"t250_lookalike"}] ${rn}`); await sleep(300);
  A.chats.length = 0; await click(BOX('bm.kboard'));
  ok(`the Request Stand: today's ask (${rn} ${rid.replace(/_/g, ' ')}) and your favour - the pack's look-alikes not taken`,
     said(new RegExp(`${rn} ${rid.replace(/_/g, ' ')}`)) && said(/favour/) && (await has('t250_lookalike')) === rn, A.chats.slice(-1).join(''));
  await run('clear TestRat *[minecraft:custom_data~{bm:"t250_lookalike"}]');
  await run(`give TestRat minecraft:${rid} ${rn}`); await sleep(300);
  const p1 = await has('royal_pearl');
  A.chats.length = 0; await click(BOX('bm.kboard'));
  ok(`...brought: taken, +${rpay} pearls, +1 favour`, (await hasV(rid)) === 0 && (await has('royal_pearl')) === p1 + rpay && (await score('bm.kfav')) === 1);

  // ---- the Steward's stock, and the daily special
  const STEW = '@e[type=minecraft:wandering_trader,tag=bm.kstew,limit=1]';
  const nOffers = async () => +(((await run(`${O}execute store result score #t250 bm.rng run data get entity ${STEW} Offers.Recipes`)).match(/(\d+)/) || [0, 0])[1]) &&
    +(((await run('scoreboard players get #t250 bm.rng')).match(/has (-?\d+)/)) || [0, 0])[1];
  const special = async () => (await nbt(STEW, 'Offers.Recipes[-1].sell.id')).replace(/"/g, '');
  const n1 = await nOffers(), s1 = await special();
  // (2.92: the armoury's goods - Leo's trident, the Bloomheart, the two armour sets - come before the daily special)
  ok('the Royal Steward\'s stock: 12 kingdom trades (2.94: the Sealed Royal Chart is Vesper\'s now) + the armoury, Royal Pearls for the kingdom\'s goods (a Heartstone among them)', n1 > 12 &&
     /royal_pearl/.test(await nbt(STEW, 'Offers.Recipes[0].buy')) && /heartstone/.test(await nbt(STEW, 'Offers.Recipes[8].sell')), `${n1} trades`);
  await run('scoreboard players add #bmday bm.bm 1'); await sleep(2500);
  const s2 = await special();
  ok('...a new day: the last trade (the daily special) turns over', (await nOffers()) === n1 && s2 !== s1 && !!s2, `${s1} -> ${s2}`);
  await run('scoreboard players remove #bmday bm.bm 1'); await sleep(1500);

  // ---- the royal family: Queen Ava and Queen Pearl join Emma - the Full Court
  await run('loot replace entity TestRat hotbar.2 loot bm:items/av_locket'); await run('loot replace entity TestRat hotbar.3 loot bm:items/pq_pearls'); await sleep(1500);
  await at(cx, cy, cz + 1, 0, 10);
  await use(2); await sleep(2500); await use(3); await sleep(2500);
  ok('Queen Ava and Queen Pearl called with their own things (Emma still with you)', (await cnt('@e[tag=bm.avpet,tag=!bm.ffpet]')) === 1 &&
     (await cnt('@e[tag=bm.pqpet,tag=!bm.ffpet]')) === 1 && (await cnt('@e[type=minecraft:cat,tag=bm.emmapet]')) >= 1);
  const fires0 = await cnt(`@e[type=minecraft:marker,tag=bm.kfire,x=${X},y=${Y},z=${Z},distance=..70]`);
  A.chats.length = 0; A.titles.length = 0; await click(BOX('bm.kfont')); await sleep(1500);
  ok('the Font: Queen Ava\'s and Queen Pearl\'s homecomings (the Sea-Glass Locket, the Regent\'s Seal)', await tagged('bm.kh_ava') && await tagged('bm.kh_pearl') &&
     (await has('sea_glass_locket')) === 1 && (await has('regent_seal')) === 1);
  ok('...THE FULL COURT: the Crown of the Deep', await tagged('bm.kh_court') && said(/THE FULL COURT/) && (await has('crown_of_the_deep')) === 1);
  ok('...the castle RESTORED: its fires out (markers gone, no campfires left burning)', fires0 > 0 && (await score('bm.kgst', CORE)) === 1 &&
     (await cnt(`@e[type=minecraft:marker,tag=bm.kfire,x=${X},y=${Y},z=${Z},distance=..70]`)) === 0 && A.titles.some(t => /Restored/.test(t)), `${fires0} fires before`);
  ok('...the Tide Festival (once today)', A.titles.some(t => /Tide Festival/.test(t)) && (await score('bm.kfest', CORE)) === day);
  await run('effect give TestRat minecraft:speed 1 0'); await sleep(1200);
  ok('the Regent\'s Seal carried: Hero of the Village; the Locket: Water Breathing', /hero_of_the_village/.test(await run('data get entity TestRat active_effects')) &&
     /water_breathing/.test(await run('data get entity TestRat active_effects')));

  // ---- Bones (Pearl sent home to make room)
  await run('execute as TestRat run function bm:p98/home/pearlq'); await sleep(1500);
  await run('loot replace entity TestRat hotbar.4 loot bm:items/bn_whistle'); await sleep(1500);
  await use(4); await wait(4000, async () => (await cnt('@e[tag=bm.bjpet,tag=!bm.ffpet]')) === 1); await sleep(1000);
  A.chats.length = 0; await click(BOX('bm.kfont'));
  ok('Bones called with his whistle: his homecoming at the Font (the Shark-Tooth Charm)', await tagged('bm.kh_bones') && (await has('shark_tooth_charm')) === 1);

  // ---- Apophiss: the carved stone opens; the penance; Queen Ava's pardon
  await run('execute as TestRat run function bm:p98/home/emma'); await run('execute as TestRat run function bm:p98/home/bones'); await sleep(1500);
  ok('the carved stone behind the thrones is shut', await block(X, cy, Z + 16, 'minecraft:chiseled_stone_bricks'));
  await run('scoreboard players reset TestRat bm.apcd'); await run('scoreboard players reset TestRat bm.gvhc');
  await run('loot replace entity TestRat hotbar.5 loot bm:items/apo_oath'); await sleep(1500);
  await at(cx, cy, cz - 2, 180, 0);
  A.bars.length = 0; A.chats.length = 0;           // (the stone can open the very second he arrives: listen from the summons on)
  await use(5); await wait(6000, async () => (await cnt('@e[tag=bm.appet,tag=!bm.ffpet]')) === 1);
  if ((await cnt('@e[tag=bm.appet,tag=!bm.ffpet]')) !== 1) console.log('  (Apophiss: ' + A.bars.slice(-2).join(' / ') + ')');
  const opened = await wait(6000, async () => await block(X, cy, Z + 16, 'minecraft:air')) && (await wait(2000, async () => said(/grinds open/)));
  if (!opened) console.log('  (apophiss: ' + (await run('execute as @e[tag=bm.appet] run data get entity @s Pos')) + ' | core ' +
                           (await run(`data get entity ${CORE} Pos`)) + ' | ' + (await run(`data get entity ${CORE} Tags`)) + ')');
  ok('Apophiss brought into the throne room: the stone grinds open on the Serpent\'s Alcove', opened);
  await at(cx, cy, Z + 17.5, 0, 15);
  A.chats.length = 0; await click(BOX('bm.kplinth')); await sleep(800);
  ok('the plinth, Apophiss beside you: his penance - Tide-Breaker', await tagged('bm.kh_apo') && said(/never lift against the sea/) && (await has('tide_breaker')) === 1);
  ok('...Queen Ava there too: her pardon (2 Heartstones, 16 pearls)', await tagged('bm.kh_pardon') && said(/I forgive you/) && (await has('heartstone')) >= 2);

  // ---- a dome breach: three cracks sealed, one left to burst; the leak mended at the Dome Heart
  for (const w of ['apo', 'ava']) await run(`execute as TestRat run function bm:p98/home/${w}`);
  await at(X + 0.5, cy + 0.5, Z - 2.0, 180, -20);
  A.chats.length = 0; await click(BOX('bm.kheart')); await sleep(600);
  ok('the Dome Heart, right-click: it offers to call the Tide Raiders - no breach yet', said(/call the Tide Raiders/) && (await score('bm.kbr', CORE)) <= 0);
  A.titles.length = 0; await click(BOX('bm.kheart')); await sleep(800);
  ok('...right-click again: DOME BREACH (and the dome rests 10 minutes after)', A.titles.some(t => /DOME BREACH/.test(t)) && (await score('bm.kbcd', CORE)) > 500);
  const cracks = `@e[type=minecraft:interaction,tag=bm.kcrackbox,x=${X},y=${Y},z=${Z},distance=..70]`;
  ok('DOME BREACH: four cracks, Tide Raiders through them', (await cnt(cracks)) === 4 && (await cnt(`@e[type=minecraft:drowned,tag=bm.kraider]`)) >= 4);
  await run('kill @e[type=minecraft:drowned,tag=bm.kraider]');
  const spots = [];
  for (let k = 0; k < 4; k++) {
    const p = (await nbt(`@e[type=minecraft:interaction,tag=bm.kcrackbox,x=${X},y=${Y},z=${Z},distance=..70,sort=arbitrary,limit=1,tag=!bm.t200seen]`, 'Pos'))
      .match(/(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d/);
    if (!p) break; spots.push([+p[1], +p[2], +p[3]]);
    await run(`tag @e[type=minecraft:interaction,tag=bm.kcrackbox,x=${p[1]},y=${p[2]},z=${p[3]},distance=..0.5] add bm.t200seen`);
  }
  let sealed = 0;
  for (const [x, y, z] of spots.slice(0, 3)) {
    const dx = X + 0.5 - x, dz = Z + 0.5 - z, d = Math.hypot(dx, dz);
    await at(x + dx / d * 1.6, y, z + dz / d * 1.6, Math.atan2(-dx, dz) * 180 / Math.PI + 180, 10);
    const pe = await has('royal_pearl');
    await click(`@e[type=minecraft:interaction,tag=bm.kcrackbox,x=${x},y=${y},z=${z},distance=..0.6,limit=1]`);
    if ((await cnt(`@e[type=minecraft:interaction,tag=bm.kcrackbox,x=${x},y=${y},z=${z},distance=..0.6]`)) === 0 && (await has('royal_pearl')) === pe + 1) sealed++;
  }
  ok('three cracks sealed by hand (a pearl each)', sealed === 3, `${sealed}/3`);
  const [bx, by, bz] = spots[3];
  // (the sea outside the glass is wet already: count only the cells that were dry before the burst)
  const cells = []; for (let dx = -1; dx <= 1; dx++) for (let dz = -1; dz <= 1; dz++) for (let dy = 0; dy <= 2; dy++) cells.push([Math.floor(bx) + dx, Math.floor(by) + dy, Math.floor(bz) + dz]);
  const dry = []; for (const c of cells) if (!(await block(...c, 'minecraft:water'))) dry.push(c);
  const wetNow = async () => { let n = 0; for (const c of dry) if (await block(...c, 'minecraft:water')) n++; return n; };
  await run(`scoreboard players set ${CORE} bm.kbr 2`); await sleep(3500);
  const wet = await wetNow();
  ok('...the fourth left: it bursts - the sea gets in through the glass there', (await score('bm.kburst', CORE)) === 1 && wet > 0, `${wet} water`);
  await at(X + 0.5, cy + 0.5, Z - 2.0, 180, -20);
  await run('give TestRat minecraft:air'); const pm = await has('royal_pearl');
  A.titles.length = 0; A.chats.length = 0; A.bars.length = 0; await click(BOX('bm.kheart'), true); await sleep(1500);
  const wet2 = await wetNow();
  ok('the Dome Heart, sneak + right-click: the leak mended (2 pearls) - glass back, the water drained', wet2 === 0 && (await has('royal_pearl')) === pm - 2 &&
     A.titles.some(t => /dome is whole/.test(t)), `${wet2} water left, pearls ${pm} -> ${await has('royal_pearl')}`);
  A.bars.length = 0; await click(BOX('bm.kheart')); await sleep(300); await click(BOX('bm.kheart')); await sleep(600);
  ok('...and no new breach while the Tide Raiders regroup (the cooldown on the bar)', (await score('bm.kbr', CORE)) <= 0 && A.bars.some(t => /regrouping/.test(t)), A.bars.join(' | '));

  // ---- the dome shattered; raised with a Heart of the Sea
  await run(`execute as ${CORE} at @s run function bm:p199/dome/shatter`); await sleep(1500);
  ok('the dome SHATTERED: its glass gone to sea, the castle flooded', await block(X, Y + 27, Z, 'minecraft:water') && await block(X, Y + 20, Z, 'minecraft:water'));
  await run('item replace entity TestRat hotbar.6 with minecraft:heart_of_the_sea'); A.slot(6); await sleep(400);
  await at(X + 0.5, cy + 0.5, Z - 2.0, 180, -20);
  A.titles.length = 0; await click(BOX('bm.kheart')); await sleep(2000);
  ok('...the Dome Heart with a Heart of the Sea in hand: the dome rises again - glass, dry, the Heart spent', await block(X, Y + 27, Z, 'minecraft:glass') &&
     await block(X, Y + 20, Z, 'minecraft:air') && (await hasV('heart_of_the_sea')) === 0 && (await score('bm.kdome', CORE)) === 0);

  // ---- tidy up
  await run('clear TestRat'); await run('effect clear TestRat');
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..90]`);
  for (let z = Z - 46; z <= Z + 46; z += 8) await run(`${O}fill ${X - 46} ${Y - 5} ${z} ${X + 46} ${Y + 31} ${Math.min(z + 7, Z + 46)} minecraft:air`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

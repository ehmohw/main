// 2.82: THE OMEGA PALACE - his tomb, his coming, his fight, his peace, his court - as a regular (non-op) player, every step a real
// packet (rcon sets the stage: a palace placed by the admin function, the six Conquest Emblems and Apophiss's Oath in the pocket,
// the King worn down for the last blow). Each Emblem seated on its own pedestal by a right-click; six seated without Apophiss:
// the tomb waits ("Apophiss must be here"); his Oath used - he comes - and the King crawls up out of the floor ("Who dares
// disturb-- ...YOU."), and the fight begins. A blow far past his six-percent yield (a sword that would kill him outright): his
// ward takes it - he lives, kneels and yields; the brothers talk; the Monocle is given; and the King takes his throne: right-
// clicked there, his court (the Peerage - Squire already, the Ghost Garrison, the Chronicle). 2.88: nothing spawns in the palace;
// he holds court three blocks out from the throne, clear of its seat and its purple back. 2.89: gifts offered from his court tell
// the old stories - the war of brothers (his brother's land dying), the boy who cursed the island dark.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const pos = async (sel) => { const m = (await nbt(sel, 'Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const score = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const dd = (d) => d && (d.data || d);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const X = 18000, Y = 150, Z = 16000;
  const EMB = ['brood', 'frost', 'tide', 'hex', 'keep', 'hollow'];
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run('effect give TestRat minecraft:regeneration 900 4 true'); await run('effect give TestRat minecraft:saturation 900 0 true');
  await run('kill @e[type=minecraft:wolf,tag=bm.appet]'); await run('kill @e[type=minecraft:wolf,tag=bm.ompet]');
  for (const o of ['bm.omwin', 'bm.omfav', 'bm.apcd']) await run(`execute as TestRat run scoreboard players reset @s ${o}`);
  await run('advancement revoke TestRat only bm:story/om_peace');
  const f0 = await run('scoreboard players get #omfree bm.omwin');
  const hard0 = await run('scoreboard players get #hard bm.cfg'); await run('scoreboard players set #hard bm.cfg 0');   // (2.87: he's a hard-mode exclusive)
  await run('execute as TestRat run scoreboard players reset @s bm.omrd');
  await run('scoreboard players set #omfree bm.omwin 0');

  // ---- the stage: a palace, here
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 96} ${Z + 112}`);
  await at(X + 0.5, Y + 30, Z - 20.5, 0, 0); await sleep(4000);
  await run(`${O}kill @e[type=!minecraft:player,x=${X - 16},y=${Y - 30},z=${Z - 16},dx=112,dy=110,dz=128]`);   // (a clean stage: no palace left from a run before)
  await sleep(500);
  await run(`${O}execute positioned ${X} ${Y} ${Z} run function bm:admin/omega_palace`);
  const TOMB = '@e[type=minecraft:marker,tag=bm.omtomb,limit=1,sort=nearest]';
  ok('the Omega Palace placed: its tomb, six pedestals', await wait(15000, async () => (await cnt(`@e[type=minecraft:interaction,tag=bm.omsock,x=${X},y=${Y},z=${Z},distance=..120]`)) === 6, 500),
     `${await cnt(`@e[type=minecraft:interaction,tag=bm.omsock,x=${X},y=${Y},z=${Z},distance=..120]`)} pedestals`);
  const tp = await pos(`@e[type=minecraft:marker,tag=bm.omtomb,x=${X},y=${Y},z=${Z},distance=..120,limit=1]`);
  ok('...and the tomb asleep', !!tp && (await score('bm.omst', `@e[type=minecraft:marker,tag=bm.omtomb,x=${X},y=${Y},z=${Z},distance=..120,limit=1]`)) === 0);
  // (2.88) nothing spawns in the palace: a monster just come into being in its walls (the stage: one summoned, as a spawn would) is
  // turned away within the second, a bat too; one that was already about (seen) is left alone
  await at(tp[0], tp[1], tp[2] - 6.5, 0, 0); await sleep(1000);
  await run(`${O}summon minecraft:zombie ${tp[0] + 4} ${tp[1]} ${tp[2] - 3} {Tags:["bm.t200z"],NoAI:1b}`);
  await run(`${O}summon minecraft:bat ${tp[0] - 4} ${tp[1] + 3} ${tp[2] - 3} {Tags:["bm.t200z"],NoAI:1b}`);
  await run(`${O}summon minecraft:zombie ${tp[0] - 4} ${tp[1]} ${tp[2] - 3} {Tags:["bm.t200w","bm.seen"],NoAI:1b,PersistenceRequired:1b}`);
  ok('no mobs spawn in the Omega Palace: a new-spawned zombie and a bat inside are turned away', await wait(3500, async () => (await cnt('@e[tag=bm.t200z]')) === 0),
     `${await cnt('@e[tag=bm.t200z]')} left`);
  ok('...a monster that was already about is left alone', (await cnt('@e[tag=bm.t200w]')) === 1);
  await run(`${O}kill @e[tag=bm.t200w]`);

  // ---- the six Emblems, each on its own pedestal
  for (let i = 0; i < EMB.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/emblem_${EMB[i]}`);
  await at(tp[0], tp[1], tp[2] - 0.5, 0, 0); await sleep(1500);
  let seated = 0, wrong = false;
  for (let i = 0; i < EMB.length; i++) {
    const sel = `@e[type=minecraft:interaction,tag=bm.omsock,tag=bm.omsk_${EMB[i]},x=${tp[0]},y=${tp[1]},z=${tp[2]},distance=..12,limit=1]`;
    const sp = await pos(sel); if (!sp) continue;
    const dx = sp[0] - tp[0], dz = sp[2] - tp[2], L = Math.hypot(dx, dz) || 1;
    const sx = sp[0] - dx / L * 1.8, sz = sp[2] - dz / L * 1.8;                     // (step up to it, from the tomb's side)
    const yaw = Math.atan2(-(sp[0] - sx), sp[2] - sz) * 180 / Math.PI;
    await at(sx, tp[1], sz, yaw, 20);
    if (i === 0) {                                                               // (the wrong Emblem first: it won't take it)
      A.slot(1); await sleep(250); A.bars.length = 0; const e0 = await entOf(sel); if (e0) A.interact(e0.entityId); await sleep(700);
      wrong = A.bars.some(b => /carved for the Conquest Emblem of/.test(b)) && (await has('emblem_frost')) === 1;
    }
    A.slot(i); await sleep(250); const e = await entOf(sel); if (e) A.interact(e.entityId); await sleep(800);
    if (/bm\.omfull/.test(await nbt(sel, 'Tags')) && (await has(`emblem_${EMB[i]}`)) === 0) seated++;
  }
  ok('a pedestal refuses the wrong Emblem ("carved for the Conquest Emblem of...")', wrong);
  ok('all six Emblems seated on their own pedestals, out of the hand', seated === 6, `${seated} seated`);
  A.bars.length = 0;
  ok('...not in hard mode: the dead do not stir ("Hard mode only")', await wait(9000, async () => A.bars.some(b => /Hard mode only/.test(b))) && (await cnt('@e[type=minecraft:husk,tag=bm.omboss]')) === 0,
     A.bars.slice(-1).join(''));
  await run('scoreboard players set #hard bm.cfg 1'); A.bars.length = 0;
  ok('...without Apophiss, the tomb waits ("Apophiss must be here")', await wait(9000, async () => A.bars.some(b => /Apophiss must be here/.test(b))), A.bars.slice(-1).join(''));

  // ---- Apophiss comes - and so does he
  await run('loot replace entity TestRat hotbar.7 loot bm:items/apo_oath');
  await at(tp[0], tp[1], tp[2] - 4.5, 0, 0);
  A.chats.length = 0; A.slot(7); await sleep(250); A.use(); await sleep(400); A.release();
  ok('Apophiss\'s Oath used: he comes, beside the tomb', await wait(5000, async () => (await cnt(`@e[type=minecraft:wolf,tag=bm.appet,x=${tp[0]},y=${tp[1]},z=${tp[2]},distance=..24]`)) === 1));
  ok('...and the tomb wakes: the King crawls up out of the floor', await wait(5000, async () => (await cnt(`@e[type=minecraft:husk,tag=bm.omboss,x=${tp[0]},y=${tp[1]},z=${tp[2]},distance=..24]`)) === 1));
  const BOSS = `@e[type=minecraft:husk,tag=bm.omboss,x=${tp[0]},y=${tp[1]},z=${tp[2]},distance=..40,limit=1]`;
  ok('..."Who dares disturb-- ...YOU."', await wait(15000, async () => A.chats.some(c => /Who dares disturb/.test(c))), A.chats.slice(-1).join('').slice(0, 120));
  ok('...the fight begins: he moves, he can be hurt, his bar shows', await wait(20000, async () => (await cnt(BOSS.replace(',limit=1', ',nbt=!{NoAI:1b},nbt=!{Invulnerable:1b},limit=1'))) === 1));

  // ---- the last blow: far past his yield - his ward takes it, and he yields
  // (the stage: the fight worn down - his Grief and his Ghost Guard already past - to a hundred health, eleven percent)
  await run(`scoreboard players set ${BOSS} bm.omph 2`); await run(`scoreboard players set ${BOSS} bm.omr 1`);
  await run(`${O}data merge entity ${BOSS} {Health:100f}`); await sleep(500);
  await run('item replace entity TestRat hotbar.8 with minecraft:netherite_sword[minecraft:enchantments={"minecraft:sharpness":120}]');
  const bp = await pos(BOSS);
  await at(bp[0], bp[1], bp[2] - 2.2, 0, 0); A.slot(8); await sleep(400);
  A.chats.length = 0; const be = await entOf(BOSS); if (be) A.attack(be.entityId); await sleep(1500);
  ok('a blow that would kill him outright: his ward takes it - he lives', (await cnt(BOSS)) === 1, `${await cnt(BOSS)}`);
  ok('...he kneels and yields ("Enough... enough. I yield")', await wait(6000, async () => A.chats.some(c => /I yield/.test(c))), A.chats.slice(-1).join('').slice(0, 120));
  ok('...the brothers talk, and the Monocle is given ("Take this, my friends")', await wait(25000, async () => (await has('om_monocle')) === 1), A.chats.slice(-1).join('').slice(0, 120));
  ok('...the peace is his for good (the advancement; 60 favour)', (await cnt('@a[name=TestRat,advancements={bm:story/om_peace=true}]')) === 1 && (await score('bm.omfav')) >= 60,
     `favour ${await score('bm.omfav')}`);

  // ---- his court
  const NHIT = `@e[type=minecraft:interaction,tag=bm.omnhit,x=${tp[0]},y=${tp[1]},z=${tp[2]},distance=..24,limit=1]`;
  ok('he takes his throne (the King at court)', await wait(15000, async () => (await cnt(NHIT)) === 1));
  const np = await pos(NHIT);
  // (2.88) he holds court three blocks out from his throne and a little up - clear of its seat and its purple back
  const thp = await pos(`@e[type=minecraft:marker,tag=bm.omthrone,x=${tp[0]},y=${tp[1]},z=${tp[2]},distance=..24,limit=1]`);
  const kp = await pos(`@e[type=minecraft:marker,tag=bm.omnpc,x=${tp[0]},y=${tp[1]},z=${tp[2]},distance=..24,limit=1]`);
  ok('...three blocks out from his throne, a little up (clear of the seat and the purple back)', !!thp && !!kp && Math.abs(kp[2] - (thp[2] - 3)) < 0.05 &&
     Math.abs(kp[1] - (thp[1] + 0.9)) < 0.05 && Math.abs(kp[0] - thp[0]) < 0.05, `throne ${thp} king ${kp}`);
  await at(np[0], np[1], np[2] - 2.5, 0, 10); A.slot(6); await sleep(400);
  const n0 = A.dialogN.length; const ne = await entOf(NHIT); if (ne) A.interact(ne.entityId);
  await wait(3000, async () => A.dialogN.length > n0);
  const labels = A.buttons().map(b => b.label);
  ok('right-clicked on his throne: his court (the Peerage, the Ghost Garrison, the Chronicle)', ['The Peerage', 'The Ghost Garrison', 'The Chronicle'].every(l => labels.some(x => x.includes(l))),
     labels.join(' | '));
  const pr = await A.press(/The Peerage/);
  const pb = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]) || {});
  ok('...the Peerage: Squire already (60 favour from the fight)', pr && /Squire/.test(pb), pb.slice(0, 200));

  // ---- (2.89) the old stories: gifts held out and offered - the war of brothers (his land dying), the boy who cursed the island dark
  const gift = async (item, title, re) => {
    await A.press(/« Back/); await sleep(600);
    if (!A.buttons().some(b => /Offer a gift/.test(b.label))) { const n1 = A.dialogN.length; const ne2 = await entOf(NHIT); if (ne2) A.interact(ne2.entityId); await wait(3000, async () => A.dialogN.length > n1); }
    await run(`item replace entity TestRat hotbar.6 with ${item}`); A.slot(6); await sleep(500);
    const n2 = A.dialogN.length; await A.click(/Offer a gift/);
    await wait(4000, async () => A.dialogN.length > n2);
    const body = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]) || {});
    return ok(`a gift (${item.split(':')[1]}) offered from his court: "${title}"`, body.includes(title) && re.test(body) &&
              !/passed|count/i.test(await run(`execute if items entity TestRat hotbar.6 ${item}`)), body.slice(0, 220));
  };
  await gift('minecraft:iron_sword', 'VI. The War of Brothers', /land across the water was dying/);
  await gift('minecraft:honey_bottle', 'IX. The Butler and the Boy', /cursed the whole island dark/);

  // ---- (2.87) a rematch, from his court: he goes back down, wakes, and fights; peace again - another Monocle
  await A.press(/« Back/); await sleep(600);
  if (!A.buttons().some(b => /Re-challenge the King/.test(b.label))) { const n1 = A.dialogN.length; const ne2 = await entOf(NHIT); if (ne2) A.interact(ne2.entityId); await wait(3000, async () => A.dialogN.length > n1); }
  ok('his court: "Re-challenge the King"', A.buttons().some(b => /Re-challenge the King/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  A.chats.length = 0; await A.click(/Re-challenge the King/); await sleep(1500);
  ok('...pressed: "A rematch! Splendid." - the tomb wakes, the King rises again', A.chats.some(c => /A rematch! Splendid/.test(c)) &&
     await wait(15000, async () => (await cnt(BOSS)) === 1), A.chats.slice(-1).join('').slice(0, 120));
  ok('...and fights', await wait(25000, async () => (await cnt(BOSS.replace(',limit=1', ',nbt=!{NoAI:1b},nbt=!{Invulnerable:1b},limit=1'))) === 1));
  await run(`scoreboard players set ${BOSS} bm.omph 2`); await run(`scoreboard players set ${BOSS} bm.omr 1`);
  await run(`${O}data merge entity ${BOSS} {Health:100f}`); await sleep(500);
  const bp2 = await pos(BOSS); await at(bp2[0], bp2[1], bp2[2] - 2.2, 0, 0); A.slot(8); await sleep(400);
  A.chats.length = 0; const be2 = await entOf(BOSS); if (be2) A.attack(be2.entityId); await sleep(1500);
  ok('...worn down, he yields again - and the rematch wins another Monocle (two now)', await wait(30000, async () => (await has('om_monocle')) >= 2), `monocles ${await has('om_monocle')}`);
  await wait(15000, async () => (await cnt(NHIT)) === 1);
  const np3 = await pos(NHIT); if (np3) await at(np3[0], np3[1], np3[2] - 2.5, 0, 10);
  { const n2 = A.dialogN.length; const ne3 = await entOf(NHIT); if (ne3) A.interact(ne3.entityId); await wait(3000, async () => A.dialogN.length > n2); }
  A.bars.length = 0; A.chats.length = 0; await A.click(/Re-challenge the King/); await sleep(1200);
  ok('...a second rematch the same day: "Once a day, friend"', [...A.bars, ...A.chats].some(c => /Once a day/.test(c)) && (await cnt(BOSS)) === 0, [...A.bars, ...A.chats].slice(-1).join(''));

  // ---- clean up
  await run(`${O}kill @e[type=!minecraft:player,x=${X - 16},y=${Y - 30},z=${Z - 16},dx=112,dy=110,dz=128]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.appet]'); await run('clear TestRat'); await run('effect clear TestRat');
  if (!/has 1/.test(f0)) await run('scoreboard players set #omfree bm.omwin 0');
  await run(`scoreboard players set #hard bm.cfg ${(hard0.match(/has (-?\d+)/) || [0, 0])[1]}`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 96} ${Z + 112}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

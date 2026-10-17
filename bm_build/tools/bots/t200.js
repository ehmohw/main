// 2.82: THE OMEGA PALACE - his tomb, his coming, his fight, his peace, his court - as a regular (non-op) player, every step a real
// packet (rcon sets the stage: a palace placed by the admin function, the six Conquest Emblems and Apophiss's Oath in the pocket,
// the King worn down for the last blow). Each Emblem seated on its own pedestal by a right-click; six seated without Apophiss:
// the tomb waits ("Apophiss must be here"); his Oath used - he comes - and the King crawls up out of the floor ("Who dares
// disturb-- ...YOU."), and the fight begins. A blow far past his six-percent yield (a sword that would kill him outright): his
// ward takes it - he lives, kneels and yields; the brothers talk; the Monocle is given; and the King takes his throne: right-
// clicked there, his court (the Peerage - Squire already, the Ghost Garrison, the Chronicle).
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
  await run('scoreboard players set #omfree bm.omwin 0');

  // ---- the stage: a palace, here
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 96} ${Z + 112}`);
  await at(X + 0.5, Y + 30, Z - 20.5, 0, 0); await sleep(4000);
  await run(`${O}execute positioned ${X} ${Y} ${Z} run function bm:admin/omega_palace`);
  const TOMB = '@e[type=minecraft:marker,tag=bm.omtomb,limit=1,sort=nearest]';
  ok('the Omega Palace placed: its tomb, six pedestals', await wait(15000, async () => (await cnt(`@e[type=minecraft:interaction,tag=bm.omsock,x=${X},y=${Y},z=${Z},distance=..120]`)) === 6, 500),
     `${await cnt(`@e[type=minecraft:interaction,tag=bm.omsock,x=${X},y=${Y},z=${Z},distance=..120]`)} pedestals`);
  const tp = await pos(`@e[type=minecraft:marker,tag=bm.omtomb,x=${X},y=${Y},z=${Z},distance=..120,limit=1]`);
  ok('...and the tomb asleep', !!tp && (await score('bm.omst', `@e[type=minecraft:marker,tag=bm.omtomb,x=${X},y=${Y},z=${Z},distance=..120,limit=1]`)) === 0);

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
  ok('...without Apophiss, the tomb waits ("Apophiss must be here")', await wait(9000, async () => A.bars.some(b => /Apophiss must be here/.test(b))), A.bars.slice(-1).join(''));

  // ---- Apophiss comes - and so does he
  await run('loot replace entity TestRat hotbar.7 loot bm:items/apo_oath');
  await at(tp[0], tp[1], tp[2] - 4.5, 0, 0);
  A.chats.length = 0; A.slot(7); await sleep(250); A.use(); await sleep(400); A.release();
  ok('Apophiss\'s Oath used: he comes, beside the tomb', await wait(5000, async () => (await cnt(`@e[type=minecraft:wolf,tag=bm.appet,x=${tp[0]},y=${tp[1]},z=${tp[2]},distance=..24]`)) === 1));
  ok('...and the tomb wakes: the King crawls up out of the floor', await wait(5000, async () => (await cnt(`@e[type=minecraft:husk,tag=bm.omboss,x=${tp[0]},y=${tp[1]},z=${tp[2]},distance=..24]`)) === 1));
  const BOSS = `@e[type=minecraft:husk,tag=bm.omboss,x=${tp[0]},y=${tp[1]},z=${tp[2]},distance=..40,limit=1]`;
  ok('..."Who dares disturb-- ...YOU."', await wait(15000, async () => A.chats.some(c => /Who dares disturb/.test(c))), A.chats.slice(-1).join('').slice(0, 120));
  ok('...the fight begins: he moves, he can be hurt, his bar shows', await wait(20000, async () => /0b/.test(await nbt(BOSS, 'NoAI')) && /0b/.test(await nbt(BOSS, 'Invulnerable'))));

  // ---- the last blow: far past his yield - his ward takes it, and he yields
  await run(`${O}data merge entity ${BOSS} {Health:100f}`);
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
  await at(np[0], np[1], np[2] - 2.5, 0, 10); A.slot(6); await sleep(400);
  const n0 = A.dialogN.length; const ne = await entOf(NHIT); if (ne) A.interact(ne.entityId);
  await wait(3000, async () => A.dialogN.length > n0);
  const labels = A.buttons().map(b => b.label);
  ok('right-clicked on his throne: his court (the Peerage, the Ghost Garrison, the Chronicle)', ['The Peerage', 'The Ghost Garrison', 'The Chronicle'].every(l => labels.some(x => x.includes(l))),
     labels.join(' | '));
  const pr = await A.press(/The Peerage/);
  const pb = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]) || {});
  ok('...the Peerage: Squire already (60 favour from the fight)', pr && /Squire/.test(pb), pb.slice(0, 200));

  // ---- clean up
  await run(`${O}kill @e[type=minecraft:husk,tag=bm.omboss,x=${X},y=${Y},z=${Z},distance=..120]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.appet]'); await run('clear TestRat'); await run('effect clear TestRat');
  if (!/has 1/.test(f0)) await run('scoreboard players set #omfree bm.omwin 0');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 96} ${Z + 112}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

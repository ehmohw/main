// 2.85d (second batch): FIRE, BREEZES, ILLUSIONERS, AND THE ESCORT ON THE WHEEL - as a regular player TestRat (rcon sets the
// stage: floors, fires, markers, mobs, the items in hand).
//   the Fire Extinguisher, used as a real item: every fire within 15 out, one at 20 left; used again at once: the 5 s cooldown
//   holds (nothing goes out); after 5 s it works again.
//   (the Gilded Gutter putting fires out by itself is checked in t231, which plays a real heist.)
//   a breeze in a room with a drop (a Sky Isles marker): becomes a Vault Hexer (witch) within a second; one in a plain fight
//   room stays a breeze. An illusioner anywhere: gone.
//   the Partner Wheel: a Skiff Escort (crimson) put on from the off hand; the wheel's menu launches it (pressed), sends it home
//   (pressed), and gives the beacon back (pressed).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const has = async id => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const cnt = async (dim, sel) => { const m = (await run(`execute in ${dim} if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const block = async (dim, x, y, z, b) => /passed/.test(await run(`execute in ${dim} if block ${x} ${y} ${z} ${b}`));
  const slotOf = async id => { for (let i = 0; i < 9; i++) if (new RegExp(`"${id}"`).test(await run(`data get entity TestRat Inventory[{Slot:${i}b}].components."minecraft:custom_data".bm`))) return i; return -1; };
  const use = async id => { A.slot(await slotOf(id)); await sleep(300); A.use(); await sleep(350); A.release(); await sleep(900); };
  const OW = 'minecraft:overworld', GU = 'bm:gutter';

  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(700);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat resistance 600 4 true'); await run('effect give TestRat fire_resistance 600 0 true');

  // ================================================================== the Fire Extinguisher
  const [X, Y, Z] = [14000, 120, 14000];
  await run(`execute in ${OW} run forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  await run(`execute in ${OW} run fill ${X - 22} ${Y - 1} ${Z - 22} ${X + 22} ${Y - 1} ${Z + 22} minecraft:netherrack`);
  await run(`execute in ${OW} run fill ${X - 22} ${Y} ${Z - 22} ${X + 22} ${Y + 6} ${Z + 22} minecraft:air`);
  await run(`execute in ${OW} run tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); await sleep(2500); A.stand();
  const FIRES = [[5, 0], [-9, 4], [12, -12], [-14, 14], [0, -15]];
  const light = async () => { for (const [dx, dz] of FIRES) await run(`execute in ${OW} run setblock ${X + dx} ${Y} ${Z + dz} minecraft:fire`);
    await run(`execute in ${OW} run setblock ${X + 20} ${Y} ${Z} minecraft:fire`); };
  const burning = async () => { let n = 0; for (const [dx, dz] of FIRES) if (await block(OW, X + dx, Y, Z + dz, 'minecraft:fire')) n++; return n; };
  await run('loot give TestRat loot bm:items/fire_extinguisher'); await light();
  ok('Five fires lit within 15 blocks of TestRat (one more at 20)', (await burning()) === 5 && await block(OW, X + 20, Y, Z, 'minecraft:fire'));
  A.bars.length = 0; await use('fire_extinguisher');
  ok('The Fire Extinguisher used: every fire within 15 goes out, the one at 20 burns on', (await burning()) === 0 && await block(OW, X + 20, Y, Z, 'minecraft:fire'),
     A.bars.slice(-1).join(''));
  ok('...it\'s still in hand (it never runs dry)', (await has('fire_extinguisher')) === 1);
  await light(); await use('fire_extinguisher');
  ok('...used again at once: the 5-second cooldown holds - the fires burn on', (await burning()) === 5);
  await sleep(5000); await use('fire_extinguisher');
  ok('...after 5 seconds it works again', (await burning()) === 0);
  await run(`execute in ${OW} run fill ${X - 22} ${Y} ${Z - 22} ${X + 22} ${Y + 1} ${Z + 22} minecraft:air`);

  // ================================================================== the Partner Wheel and the Skiff Escort
  await run('clear TestRat'); await run('loot give TestRat loot bm:items/partner_wheel');
  await run('item replace entity TestRat weapon.offhand with minecraft:paper'); await run('loot replace entity TestRat weapon.offhand loot bm:items/skiff_escort_crimson');
  const pid = (await run('scoreboard players get TestRat bm.pid')).match(/has (\d+)/);
  A.chats.length = 0; await use('partner_wheel');
  ok('A Skiff Escort held in the off hand, the wheel used: it goes on the wheel', (await has('skiff_escort_crimson')) === 0 && A.chats.some(c => /Partner Wheel/.test(c)),
     A.chats.slice(-1).join(''));
  const esc = async () => cnt(OW, `@e[type=minecraft:bat,tag=bm.eskhost,x=${X},y=${Y},z=${Z},distance=..12]`);
  await use('partner_wheel'); await sleep(500);
  ok('The wheel\'s menu offers to launch it', A.buttons().some(b => /Launch your/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  await A.press(/Launch your/); await sleep(1500);
  ok('...Launch pressed: the escort flies at TestRat\'s shoulder', await wait(3000, async () => (await esc()) === 1),
     `${A.bars.slice(-2).join(' | ')} ${A.chats.slice(-1).join('')} cd ${await run('scoreboard players get TestRat bm.eskcd')} esc ${await run('scoreboard players get TestRat bm.pwesc')}`);
  await sleep(1200); await use('partner_wheel'); await sleep(500);
  await A.press(/Send your Skiff Escort home/); await sleep(1500);
  ok('...Send home pressed: it flies home', await wait(3000, async () => (await esc()) === 0));
  await sleep(1200); await use('partner_wheel'); await sleep(500);
  await A.press(/Take the escort back/); await sleep(2000);
  ok('...Take it back pressed: the crimson beacon is TestRat\'s again', await wait(4000, async () => (await has('skiff_escort_crimson')) === 1));

  // ================================================================== the Gilded Gutter: fire goes out; breezes and illusioners
  const [GX, GY, GZ] = [5000, 100, 5000];
  await run(`execute in ${GU} run forceload add ${GX - 40} ${GZ - 40} ${GX + 40} ${GZ + 40}`);
  await run(`execute in ${GU} run fill ${GX - 24} ${GY - 1} ${GZ - 6} ${GX + 24} ${GY - 1} ${GZ + 6} minecraft:netherrack`);
  await run(`execute in ${GU} run fill ${GX - 24} ${GY} ${GZ - 6} ${GX + 24} ${GY + 6} ${GZ + 6} minecraft:air`);
    // (two rooms 30 apart: a Sky Isles marker to the east, a plain fight room to the west)
  await run(`execute in ${GU} run summon minecraft:marker ${GX + 15.5} ${GY} ${GZ + 0.5} {Tags:["bm.gvr","bm.gvr_isles","bm.t233"]}`);
  await run(`execute in ${GU} run summon minecraft:marker ${GX - 14.5} ${GY} ${GZ + 0.5} {Tags:["bm.gvr","bm.gvr_guards","bm.t233"]}`);
  await run(`execute in ${GU} run summon minecraft:breeze ${GX + 13.5} ${GY} ${GZ + 0.5} {Tags:["bm.gvg","bm.t233"],NoAI:1b,PersistenceRequired:1b}`);
  await run(`execute in ${GU} run summon minecraft:breeze ${GX - 12.5} ${GY} ${GZ + 0.5} {Tags:["bm.gvg","bm.t233","bm.t233w"],NoAI:1b,PersistenceRequired:1b}`);
  const hexer = `@e[type=minecraft:witch,tag=bm.gvg,x=${GX + 13.5},y=${GY},z=${GZ + 0.5},distance=..3]`;
  ok('A breeze in a room with a drop (the Sky Isles) becomes a Vault Hexer', await wait(2500, async () => (await cnt(GU, hexer)) === 1)
     && (await cnt(GU, `@e[type=minecraft:breeze,x=${GX + 13.5},y=${GY},z=${GZ + 0.5},distance=..3]`)) === 0);
  await sleep(1500);
  ok('...one in a plain fight room stays a breeze', (await cnt(GU, '@e[type=minecraft:breeze,tag=bm.t233w]')) === 1);
  await run(`execute in ${GU} run summon minecraft:illusioner ${GX - 3.5} ${GY} ${GZ + 3.5} {Tags:["bm.t233i"],NoAI:1b,PersistenceRequired:1b}`);
  ok('An illusioner: gone within a second or two', await wait(3000, async () => (await cnt(GU, '@e[type=minecraft:illusioner,tag=bm.t233i]')) === 0));

  // ---- put things back
  await run(`execute in ${GU} run kill @e[tag=bm.t233]`); await run(`execute in ${GU} as @e[type=minecraft:witch,tag=bm.gvg,x=${GX},y=${GY},z=${GZ},distance=..40] run tp @s ~ -300 ~`);
  await run(`execute in ${GU} run kill @e[type=minecraft:witch,x=${GX},y=${GY - 400},z=${GZ},distance=..40]`);
  await run(`execute in ${GU} run fill ${GX - 24} ${GY - 1} ${GZ - 6} ${GX + 24} ${GY - 1} ${GZ + 6} minecraft:air`);
  await run(`execute in ${GU} run forceload remove ${GX - 40} ${GZ - 40} ${GX + 40} ${GZ + 40}`);
  await run(`execute in ${OW} run tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); await sleep(1500);
  await run(`execute in ${OW} run forceload remove ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  if (pid) await run(`scoreboard players reset TestRat bm.pwesc`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode creative TestRat');
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

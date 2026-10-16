// 2.80e: no glowing outline on a custom-modelled mob's invisible host - as a regular (non-op) player. A custom-modelled mob is an
// invisible vanilla mob carrying display entities, and the glowing outline ignores invisibility: it showed as a husk or a rabbit
// around the model. rcon sets the stage: a floor, the items, a zombie, a Vorn trooper, a Mimic.
//   The Xeno Visor, put on with a right-click: the zombie glows; the Vorn trooper's invisible husk does not.
//   The Cipher Monocle, swapped on with a right-click: a Mimic's chest model glows; its invisible rabbit does not.
//   A glow from outside the pack on the trooper (a spectral arrow, say) is put out within a second.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const X = 16900, Y = 100, Z = 16000;
  const at = `x=${X},y=${Y},z=${Z},distance=..20`;
  const glows = async sel => /passed/.test(await run(`${O}execute if entity ${sel} if data entity ${sel} active_effects[{id:"minecraft:glowing"}]`));
  const flag = async sel => /: 1b/.test(await run(`${O}data get entity ${sel} Glowing`));
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 6} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,${at}]`); await run('time set 1000');
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(800);
  // the stage: a zombie and a Vorn trooper, held still
  await run(`${O}summon minecraft:zombie ${X + 4.5} ${Y + 1} ${Z + 4.5} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["bm.t185"]}`);
  await run(`${O}execute positioned ${X - 3.5} ${Y + 1} ${Z + 4.5} run function bm:p32/spawn/trooper`); await sleep(300);
  await run(`${O}execute as @e[type=minecraft:husk,tag=bm.vtroop,${at}] run data merge entity @s {NoAI:1b}`);
  const ZOM = `@e[type=minecraft:zombie,tag=bm.t185,${at},limit=1]`, VORN = `@e[type=minecraft:husk,tag=bm.vtroop,${at},limit=1]`;
  ok('the stage: a zombie, and a Vorn trooper whose husk is invisible under its model',
     /passed/.test(await run(`${O}execute if entity ${ZOM}`)) && /invisibility/.test(await run(`${O}data get entity ${VORN} active_effects`)));

  // ---- the Xeno Visor
  await run('loot replace entity TestRat hotbar.0 loot bm:items/xeno_visor'); A.slot(0); await sleep(300); A.use(); await sleep(300); A.release(); await sleep(400);
  ok('right-click: the Xeno Visor is worn', /xeno_visor/.test(await run('data get entity TestRat equipment.head.components."minecraft:custom_data".bm')));
  ok('...the zombie glows', await wait(3500, () => glows(ZOM)));
  ok('...the Vorn trooper\'s invisible husk does not', !(await glows(VORN)) && !(await flag(VORN)));

  // ---- the Cipher Monocle and a Mimic
  await run(`${O}execute positioned ${X + 0.5} ${Y + 1} ${Z - 4.5} run function bm:p39/mimic/spawn_chest`); await sleep(300);
  await run(`${O}execute as @e[type=minecraft:rabbit,tag=bm.mimic,${at}] run data merge entity @s {NoAI:1b}`);
  const MIM = `@e[type=minecraft:rabbit,tag=bm.mimic,${at},limit=1]`;
  await run('loot replace entity TestRat hotbar.1 loot bm:items/cipher_monocle'); A.slot(1); await sleep(300); A.use(); await sleep(300); A.release(); await sleep(400);
  ok('right-click: the Cipher Monocle swaps onto the head', /cipher_monocle/.test(await run('data get entity TestRat equipment.head.components."minecraft:custom_data".bm')));
  const chest = await wait(3500, async () => /: 1b/.test(await run(`${O}execute as ${MIM} on passengers run data get entity @s Glowing`)));
  ok('...a Mimic\'s chest model is outlined', chest);
  ok('...its invisible rabbit is not', !(await flag(MIM)) && !(await glows(MIM)));

  // ---- a glow from outside the pack
  await run(`${O}effect give ${VORN} minecraft:glowing 10 0`);
  ok('a glow from outside (a spectral arrow, say) on the trooper is put out within a second or so', await wait(2500, async () => !(await glows(VORN))));

  await run(`${O}kill @e[type=!minecraft:player,${at}]`); await run('clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

// 2.82e: RED XENITE FROM A DREADNOUGHT'S GUARDS - 1 in 10, not every kill - as a regular (non-op) player TestRat, every kill a real
// hit (rcon sets the stage: a deck, the Dreadnought's alarm raising its guards, the guards held still at 1 health in reach).
//   THE GUARDS: the alarm's guards carry their own loot table (bm:p32/guardian). TestRat kills 60 of them: their shards and
//   Tokens drop as before, but Red Xenite only about one kill in ten (at most 15 of 60; every kill used to drop 1-2).
//   THE INVASION'S VORN: 10 troopers off an Invasion Night still drop Red Xenite every time.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (id) => { const o = await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/g) || [0])[0]); };
  const ground = async (id) => { let n = 0; const o = await run(`${O}execute as @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..24] if items entity @s contents *[minecraft:custom_data~{bm:"${id}"}] run data get entity @s Item.count`);
    for (const m of o.matchAll(/data: (\d+)/g)) n += +m[1]; return n; };
  const got = async (id) => (await cnt(id)) + (await ground(id));
  const sweep = async () => { await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..24]`); await run('clear TestRat *[minecraft:custom_data~{bm:"xenite_red"}]'); };
  const X = 29000, Y = 100, Z = 29000;
  const HERE = `x=${X},y=${Y},z=${Z},distance=..24`;

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  await run(`${O}fill ${X - 10} ${Y - 1} ${Z - 10} ${X + 10} ${Y - 1} ${Z + 10} minecraft:iron_block`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y + 6} ${Z + 10} minecraft:air`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run('time set midnight');
  await run('item replace entity TestRat hotbar.0 with minecraft:netherite_sword[minecraft:enchantments={"minecraft:sharpness":5}]'); A.slot(0);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();

  // the husk's entity type number, from a probe in view (Vorn wear display entities: hitting one of those is a kick)
  const seen = new Set(Object.keys(A.ents));
  await run(`${O}summon minecraft:husk ${X + 0.5} ${Y + 4} ${Z + 6.5} {NoAI:1b,Silent:1b,Tags:["bm.t208probe"]}`); await sleep(700);
  const pk = Object.keys(A.ents).find(k => !seen.has(k) && Math.abs(A.ents[k].z - Z - 6.5) < 0.1 && Math.abs(A.ents[k].y - Y - 4) < 0.1);
  const HUSK = pk ? A.ents[pk].type : null; ok('(the husk\'s type number, from a probe)', HUSK !== null); await run(`${O}tp @e[tag=bm.t208probe] ~ -400 ~`); await run(`${O}kill @e[tag=bm.t208probe]`);

  // hold every husk here still at 1 health, in front of TestRat, then hit each one
  // (the bot only knows where an entity spawned: everything is raised within reach, never moved)
  const done = new Set();
  const killAll = async (sel) => {
    await sleep(500); await run(`${O}execute as @e[${sel},${HERE}] run data merge entity @s {NoAI:1b,Health:1f}`);
    let n = 0;
    for (const e of Object.values(A.ents)) if (e.type === HUSK && !done.has(e.entityId) && Math.hypot(e.x - X - 0.5, e.z - Z - 2.5) < 1.6 && Math.abs(e.y - Y) < 0.5) {
      done.add(e.entityId); A.attack(e.entityId); n++; await sleep(650); }
    await sleep(1200); return n;
  };

  // ---- the Dreadnought's guards
  await run(`${O}kill @e[type=minecraft:husk,${HERE}]`);
  await run(`${O}summon minecraft:marker ${X + 0.5} ${Y} ${Z + 2.5} {Tags:["bm.vguard","bm.t208"]}`);
  await run(`${O}summon minecraft:marker ${X + 1.5} ${Y} ${Z + 2.5} {Tags:["bm.vguard_boss","bm.t208"]}`);
  await run(`${O}summon minecraft:marker ${X + 0.5} ${Y} ${Z + 3.5} {Tags:["bm.t208core","bm.t208"]}`);
  await run(`${O}execute as @e[tag=bm.t208core] at @s run function bm:p32/dread/alarm`); await sleep(300);
  const lt = await run(`${O}data get entity @e[type=minecraft:husk,tag=bm.vguardian,${HERE},limit=1] DeathLootTable`);
  ok('the alarm\'s guards carry their own loot table (bm:p32/guardian)', /p32\/guardian/.test(lt) &&
     !/Test passed/.test(await run(`${O}execute if entity @e[type=minecraft:husk,tag=bm.vguardian,${HERE},nbt=!{DeathLootTable:"bm:p32/guardian"}]`)), lt.slice(-60));
  let killed = 0;
  for (let r = 0; r < 20; r++) {
    if (r) { await run(`${O}execute as @e[tag=bm.t208core] at @s run function bm:p32/dread/alarm`); await sleep(200); }
    killed += await killAll('type=minecraft:husk,tag=bm.vguardian');
  }
  const left = /Test passed/.test(await run(`${O}execute if entity @e[type=minecraft:husk,tag=bm.vguardian,${HERE}]`));
  const red = await got('xenite_red'), green = await got('xenite_green') + await got('xenite_violet') + await got('xenite_cyan');
  ok('TestRat kills 60 guards; their other shards drop as before', killed === 60 && !left && green >= 60, `${killed} hit, ${left ? 'some left' : 'none left'}, ${green} green/violet/cyan`);
  ok('...but Red Xenite only about one kill in ten (at most 15 of 60 - every kill used to drop 1-2)', red <= 15, `${red} red from ${killed} guards`);
  await run('clear TestRat'); await sweep(); A.slot(0);
  await run('item replace entity TestRat hotbar.0 with minecraft:netherite_sword[minecraft:enchantments={"minecraft:sharpness":5}]');

  // ---- the invasion's Vorn
  for (let i = 0; i < 10; i++) await run(`${O}execute positioned ${X + 0.5} ${Y} ${Z + 2.5} run function bm:p32/spawn/trooper`);
  await sleep(300);
  const k2 = await killAll('type=minecraft:husk,tag=bm.vtroop,tag=!bm.vguardian');
  const red2 = await got('xenite_red');
  ok('10 invasion troopers still drop Red Xenite every time', k2 === 10 && red2 >= 10, `${red2} red from ${k2}`);

  // ---- clean up
  await run(`${O}kill @e[tag=bm.t208]`); await run(`${O}tp @e[type=minecraft:husk,${HERE}] ~ -400 ~`); await run(`${O}kill @e[type=item,${HERE}]`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('time set day');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

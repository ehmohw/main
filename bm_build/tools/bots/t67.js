const { bot, rcon, sleep } = require('./lib');
const X = 13800, Y = 100, Z = 13800; const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const hp = async (sel) => { const m = (await run(`data get entity ${sel} Health`)).match(/([\d.]+)f/); return m ? +m[1] : null; };
  const has = async (it) => /passed/.test(await run(`execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"${it}"}]`));
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(3500);
  await run(`fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} stone`); await run(`fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..30]`); await run('clear TestRat'); await run('gamemode survival TestRat');
  await run('effect give TestRat resistance 600 4 true'); await run('kill @e[type=wolf,tag=bm.vhound]'); await run('kill @e[type=marker,tag=bm.vhmark]');
  const husk = async (dz, tag = 'bm.t67', hpv = 100) => run(`summon husk ${X + 0.5} ${Y + 1} ${Z + dz + 0.5} {Tags:["${tag}"],PersistenceRequired:1b,NoAI:1b,Health:${hpv}f,attributes:[{id:"minecraft:max_health",base:${hpv}}]}`);
  // the Gilded set: no fall damage
  for (const p of ['helmet', 'chestplate', 'leggings', 'boots']) await run(`loot replace entity TestRat armor.${p === 'helmet' ? 'head' : p === 'chestplate' ? 'chest' : p === 'leggings' ? 'legs' : 'feet'} loot bm:items/gilded_${p}`);
  await sleep(600);
  const fdm = async () => +((await run('attribute TestRat minecraft:fall_damage_multiplier get')).match(/is ([\d.]+)/) || [0, -1])[1];
  ok('The full Gilded set: no fall damage (fall damage x0)', (await fdm()) === 0, 'x' + await fdm());
  await run('item replace entity TestRat armor.feet with air'); await sleep(500);
  ok('...and the bonus goes with a missing piece', (await fdm()) === 1, 'x' + await fdm());
  await run('effect give TestRat resistance 600 4 true');
  // the shiv's ambush; the hammer's shockwave
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(500);
  await husk(2); await sleep(4000);
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/heisters_shiv'); await sleep(300);
  const hid = () => Object.values(A.ents).filter(e => Math.hypot(e.x - X - 0.5, e.z - Z - 2.5) < 1 && e.type === Object.values(A.ents).find(f => Math.hypot(f.x - X - 0.5, f.z - Z - 2.5) < 0.2)?.type).map(e => e.entityId);
  let ids = [1]; await run('damage @e[tag=bm.t67,limit=1] 5 minecraft:player_attack by TestRat'); await sleep(1200);
  const hs = await hp('@e[tag=bm.t67,limit=1]');
  ok("Heister's Shiv: a stab on a monster not after you - then the hidden second stab", hs !== null && hs <= 100 - 5 - 6 + 0.5, 'husk ' + hs + ' ids ' + ids.length);
  await run('kill @e[tag=bm.t67]'); await husk(2); await husk(4, 'bm.t67b'); await husk(2.2, 'bm.t67c'); await sleep(4000);
  await run(`tp @e[tag=bm.t67c] ${X + 1.6} ${Y + 1} ${Z + 2.5}`);
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/vault_breaker'); await sleep(2000);
  await run(`kill @e[type=item,x=${X},y=${Y},z=${Z},distance=..12]`); await sleep(2000);
  await run('damage @e[tag=bm.t67,limit=1] 12 minecraft:player_attack by TestRat'); await sleep(800);
  ok('Vault Breaker: the blow sends a shockwave through the monsters around', (await hp('@e[tag=bm.t67c,limit=1]')) < 100, 'neighbour ' + await hp('@e[tag=bm.t67c,limit=1]'));
  await run('kill @e[tag=bm.t67]'); await run('kill @e[tag=bm.t67b]'); await run('kill @e[tag=bm.t67c]');
  // the scepter
  await husk(3); await husk(-3, 'bm.t67b'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/treasurers_scepter'); await sleep(300);
  await run('execute as TestRat at @s run function bm:p71/scepter'); await sleep(300);
  ok("The Treasurer's Scepter: COIN STORM hits every monster within 6", (await hp('@e[tag=bm.t67,limit=1]')) <= 88.5 && (await hp('@e[tag=bm.t67b,limit=1]')) <= 88.5);
  await run('kill @e[tag=bm.t67]'); await run('kill @e[tag=bm.t67b]');
  // banner: set down, its aura
  await run('effect clear TestRat'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/raid_banner_3');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 50`); await sleep(400);
  A.input({ shift: true }); await sleep(300); await run('execute as TestRat at @s run function bm:p71/banner/place3'); A.input({}); await sleep(1600);
  const eff = await run('data get entity TestRat active_effects');
  ok('Raid Banner III: set down, it heals, quickens and strengthens its owner nearby', (await cnt('@e[type=item_display,tag=bm.gvban]')) === 1 && /regeneration/.test(eff) && /speed/.test(eff) && /strength/.test(eff), eff.slice(0, 120));
  await run('kill @e[tag=bm.gvban]'); await run('kill @e[tag=bm.gvbanhit]');
  // trophy placed and picked up
  await run('clear TestRat'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/trophy_dial');
  await run(`tp TestRat ${X + 3.5} ${Y + 1} ${Z + 0.5} 0 50`); await sleep(300);
  A.input({ shift: true }); await sleep(300); await run('execute as TestRat at @s run function bm:p71/deco/place_trophy_dial'); await sleep(300);
  const placed = await cnt('@e[type=interaction,tag=bm.gvdk_trophy_dial]'); await sleep(4000); A.input({ shift: true }); await sleep(300);
  const tid = Object.values(A.ents).filter(e => Math.hypot(e.x - X - 3.5, e.z - Z - 1.5) < 1.2).map(e => e.entityId);
  const uu = (await run('data get entity TestRat UUID')).match(/\[I; ([-\d, ]+)\]/)[1];
  await run(`data modify entity @e[type=interaction,tag=bm.gvdk_trophy_dial,limit=1] attack set value {player:[I;${uu}],timestamp:1L}`); await sleep(800); A.input({}); await sleep(200);
  ok('A puzzle trophy: set down, and sneak-punched back up', placed === 1 && (await cnt('@e[type=interaction,tag=bm.gvdk_trophy_dial]')) === 0 && await has('trophy_dial'), `placed ${placed}`);
  // clockwork: four fragments make a key
  await run('clear TestRat'); await run('give TestRat minecraft:stone 1'); for (let i = 0; i < 4; i++) await run('loot give TestRat loot bm:items/clockwork_fragment');
  await run('execute as TestRat at @s run function bm:p71/assemble'); await sleep(200);
  ok('Four Clockwork Key Fragments make a Clockwork Key', await has('clockwork_key') && !(await has('clockwork_fragment')));
  // bond sigils (Mending): two holders in the same party regenerate near each other (since 2.6x it's your party, not the heist the sigil came from)
  const B = await bot('TestRat2'); await sleep(4500); await run(`tp TestRat2 ${X + 2.5} ${Y + 1} ${Z + 0.5}`); await run('effect clear TestRat'); await run('effect clear TestRat2');
  for (const who of ['TestRat', 'TestRat2']) { await run(`clear ${who}`); await run(`loot give ${who} loot bm:items/bond_sigil`); await run(`scoreboard players operation ${who} bm.pty = TestRat bm.pid`); }
  await sleep(3200);
  ok('Bond Sigils of Mending in one party: their holders regenerate near each other', /regeneration/.test(await run('data get entity TestRat2 active_effects')) && /regeneration/.test(await run('data get entity TestRat active_effects')));
  await run('scoreboard players reset TestRat2 bm.pty'); await run('effect clear TestRat'); await run('effect clear TestRat2'); await sleep(2600);
  ok('...but not with someone from another party', !/regeneration/.test(await run('data get entity TestRat active_effects')));
  for (const who of ['TestRat', 'TestRat2']) await run(`scoreboard players reset ${who} bm.pty`);
  B.end && B.end();
  // the hound sniffs out a loot chest
  await run('clear TestRat'); await run(`setblock ${X + 6} ${Y + 1} ${Z - 5} minecraft:chest{LootTable:"minecraft:chests/simple_dungeon"}`);
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/vault_hound_whistle'); await run('execute as TestRat at @s run function bm:p71/hound/use'); await sleep(2500);
  ok('The Vault Hound comes at the whistle and sniffs out an unopened loot chest', (await cnt('@e[type=wolf,tag=bm.vhound]')) === 1 && (await cnt('@e[type=marker,tag=bm.vhmark]')) === 1);
  await run('kill @e[type=wolf,tag=bm.vhound]'); await run('kill @e[type=marker,tag=bm.vhmark]'); await run(`setblock ${X + 6} ${Y + 1} ${Z - 5} air`);
  // the gambler's coin; the ledger
  await run('clear TestRat'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/gamblers_coin');
  for (let i = 0; i < 6; i++) { await run('scoreboard players reset TestRat bm.gvsc'); await run('execute as TestRat at @s run function bm:p71/flip'); }
  ok("Gambler's Coin: heads gives Luck II", /luck/.test(await run('data get entity TestRat active_effects')));
  // Cecil's topper
  await run('clear TestRat'); await run('kill @e[type=wolf,tag=bm.cecilpet]'); await run('scoreboard players reset TestRat bm.cpcd'); await run('scoreboard players reset TestRat bm.cpgild'); await run('scoreboard players reset TestRat bm.cpel');
  await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(1500);
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/gilded_staff_topper'); await run('execute as TestRat at @s run function bm:p71/topper'); await sleep(300);
  ok('Gilded Staff Topper: Cecil\'s staff is gilded', /cec2_arm_gild/.test(await run('data get entity @e[type=item_display,tag=bm.cp_arm,limit=1] item.components')));
  await run('kill @e[type=wolf,tag=bm.cecilpet]'); await run('scoreboard players reset TestRat bm.cpcd'); await run('scoreboard players reset TestRat bm.cpgild');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

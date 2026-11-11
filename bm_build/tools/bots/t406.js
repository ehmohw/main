// 3.1s: TWO NAMES PUT RIGHT, as a regular (non-op) player. The Golden Doodle's golden doll was "Golden Golden Doodle Doll" - now
// "Solid-Gold Golden Doodle Doll", and a copy made before (item version 47, the old name) is re-synced to it in your inventory;
// the Rat Bank's Trophies page: "Deposit all Trophies" says "Every Trophy you carry" (it said "Trophie"). (rcon sets the stage:
// the old copy, the Banker's Card, a Trophy in the account.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run('clear TestRat'); await run('gamemode survival TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');

  // ---------------------------------------------------------------- the doll: an old copy, re-synced
  await run('loot replace entity TestRat hotbar.1 loot bm:items/gdoll_gdoodle');
  await run('item modify entity TestRat hotbar.1 {function:"minecraft:set_components",components:{"minecraft:item_name":"Golden Golden Doodle Doll"}}');
  await run('item modify entity TestRat hotbar.1 {function:"minecraft:set_custom_data",tag:{bmv:47}}');
  const nm = async () => (await run('data get entity TestRat Inventory[{Slot:1b}].components."minecraft:item_name"'));
  ok('the stage: an old copy (item version 47) named "Golden Golden Doodle Doll"', /Golden Golden Doodle Doll/.test(await nm()));
  ok('...re-synced in your inventory: "Solid-Gold Golden Doodle Doll"', await wait(8000, async () => /Solid-Gold Golden Doodle Doll/.test(await nm())), (await nm()).slice(-120));
  ok('...and stamped with this version', /bmv: 48/.test(await run('data get entity TestRat Inventory[{Slot:1b}].components."minecraft:custom_data"')));

  // ---------------------------------------------------------------- the bank: Trophies
  for (const o of ['bm.bk_tok', 'bm.bkac', 'bm.bkag']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/bankers_card'); await run('loot replace entity TestRat hotbar.2 loot bm:items/trophy'); await sleep(300);
  A.slot(0); await sleep(250); let d = await A.useWait(2500); if (!d) { A.use(); await sleep(400); A.release(); await sleep(800); }
  await A.press(/^Currencies/); await sleep(400);
  const b = A.buttons().find(x => /Trophies/.test(x.label));
  ok('the Banker\'s Card: the bank\'s Currencies page has Trophies', !!b, A.buttons().map(x => x.label).join(' | ').slice(0, 300));
  if (b) { await A.press(/Trophies/); await sleep(400); }
  const dep = A.buttons().find(x => /Deposit all/.test(x.label));
  ok('the Trophies page: "Deposit all Trophies" - "Every Trophy you carry, into your account"', !!dep && /Every Trophy you carry/.test(dep.tooltip) && !/Trophie\b/.test(dep.tooltip),
     dep ? `${dep.label} :: ${dep.tooltip}` : A.buttons().map(x => x.label).join(' | ').slice(0, 300));
  await run('clear TestRat');
  A.end(); R.end();
  console.log(`${res.filter(x => x).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

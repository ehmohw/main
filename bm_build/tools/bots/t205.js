// 2.82b: THE CROWNS NO LONGER MAKE YOU BIGGER - as a regular (non-op) player TestRat (rcon sets the stage: the crowns in hand).
//   An old True Crown (2.82, with its +25% size) in the pack: re-synced to the new one; used, worn - TestRat stays his own size
//   (scale 1), and keeps the crown's other powers (+12 health). Apophiss's Crown and the Unbound Crown, worn: scale 1 too.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const attr = async a => +((await run(`attribute TestRat minecraft:${a} get`)).match(/is (-?[\d.]+)/) || [0, NaN])[1];
  const wearing = async id => /Found|1/.test(await run(`execute if items entity TestRat armor.head *[minecraft:custom_data~{bm:"${id}"}]`));
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('execute in minecraft:overworld run tp TestRat 13000.5 121 13000.5'); await run('gamemode survival TestRat'); await run('clear TestRat');
  await run('effect give TestRat minecraft:resistance 900 4 true'); await sleep(800);
  // ---- the stage: a True Crown from 2.82 - its old version stamp, and its old size modifier
  await run('loot replace entity TestRat hotbar.0 loot bm:items/apo_true_crown');
  await run('item modify entity TestRat hotbar.0 {function:"minecraft:set_custom_data",tag:"{bmv:38}"}');
  await run('item modify entity TestRat hotbar.0 {function:"minecraft:set_attributes",modifiers:[{attribute:"minecraft:scale",id:"bm:old_crown_scale",amount:0.25,operation:"add_value",slot:"head"}]}');
  const resynced = await wait(8000, async () => /\{.*bmv: ?39/.test(await run('data get entity TestRat Inventory[{Slot:0b}].components."minecraft:custom_data"')), 500);
  ok('an old True Crown in the pack is re-synced to this version', resynced);
  A.slot(0); await sleep(300); A.use(); await sleep(300); A.release(); await sleep(1200);
  ok('...used: worn, and TestRat stays his own size (scale 1) - with the crown\'s +12 health still', (await wearing('apo_true_crown')) && (await attr('scale')) === 1 && (await attr('max_health')) >= 32,
     `scale ${await attr('scale')}, health ${await attr('max_health')}`);
  for (const id of ['apophiss_crown', 'apo_unbound_crown']) {
    await run('clear TestRat'); await sleep(300);
    await run(`loot replace entity TestRat hotbar.0 loot bm:items/${id}`); A.slot(0); await sleep(300);
    A.use(); await sleep(300); A.release(); await sleep(1200);
    if (!(await wearing(id))) { await run(`item replace entity TestRat armor.head from entity TestRat hotbar.0`); await sleep(600); }
    ok(`${id === 'apophiss_crown' ? "Apophiss's Crown" : 'the Unbound Crown'}, worn: scale 1`, (await wearing(id)) && (await attr('scale')) === 1, `scale ${await attr('scale')}`);
  }
  await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

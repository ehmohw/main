// 2.80g: the coat check sees the crafting grid and the cursor - as a regular (non-op) player. The Ledger's Lounge trip makes
// you hold still for 3 seconds, and nothing stops you opening your inventory meanwhile: a sword parked in the 2x2 crafting
// grid (or held on the cursor) wasn't in the Inventory the Fixer checked, and dropped back into your pack inside the vault
// once you closed the screen. rcon sets the stage: a platform, the Ledger and Tokens, and what the player parked there.
//   In: the sword in the crafting grid and the ingot on the cursor are checked with the rest - closing the inventory inside
//   brings nothing in - and the Lounge's door hands them back at home.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const passes = async c => /passed/i.test(await run(c));
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const dim = async () => (await run('data get entity TestRat Dimension')).replace(/.*data: /, '');
  const anywhere = async id => passes(`execute if items entity TestRat container.* minecraft:${id}`) || passes(`execute if items entity TestRat player.crafting.* minecraft:${id}`) ||
                                passes(`execute if items entity TestRat player.cursor minecraft:${id}`);
  const O = 'execute in minecraft:overworld run ';
  const HX = 13300, HY = 121, HZ = 13100;
  const A = await bot('TestRat'); await sleep(2500);
  await run(`${O}forceload add ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
  await run(`${O}fill ${HX - 4} ${HY - 1} ${HZ - 4} ${HX + 4} ${HY - 1} ${HZ + 4} minecraft:stone`);
  await run(`${O}fill ${HX - 4} ${HY} ${HZ - 4} ${HX + 4} ${HY + 3} ${HZ + 4} minecraft:air`);
  await run(`${O}tp TestRat ${HX + 0.5} ${HY} ${HZ + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`spawnpoint TestRat ${HX} ${HY} ${HZ}`);
  for (const t of ['bm.gvp', 'bm.gvask', 'bm.gvnext', 'bm.gvoffer', 'bm.lgch', 'bm.lkch', 'bm.lgbag', 'bm.lgstart']) await run(`tag TestRat remove ${t}`);
  const pid = await sc('TestRat', 'bm.pid');
  await run(`data remove storage bm:gv bag.p${pid}`); await run(`data remove storage bm:gv cb.p${pid}`);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger');
  for (let k = 0; k < 2; k++) await run('loot give TestRat loot bm:items/token');
  await sleep(1500); A.stand(); await sleep(500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player (no operator commands)', /unknown|incomplete|permission/i.test(A.chats.join(' ')));

  // ---- in, with a sword in the crafting grid and an ingot on the cursor (parked there during the 3-second hold)
  A.slot(0); await sleep(300); await A.useWait(); A.chats.length = 0;
  A.click(/Fixer's Lounge/); await sleep(400);
  await run('item replace entity TestRat player.crafting.0 with minecraft:diamond_sword');
  await run('item replace entity TestRat player.cursor with minecraft:iron_ingot 3');
  await wait(7000, async () => /gutter/.test(await dim())); await sleep(1200); A.stand();
  ok('The Ledger\'s "Fixer\'s Lounge" (hold still): in the lounge', /gutter/.test(await dim()), await dim());
  if (process.env.DBG) { console.log('INV', (await run('data get entity TestRat Inventory')).slice(-300)); console.log('CRAFT', await run('execute if items entity TestRat player.crafting.* minecraft:diamond_sword'), await run('execute if items entity TestRat player.cursor *'));
    console.log('BAG', (await run(`data get storage bm:gv bag.p${pid}`)).slice(0, 600)); }
  A.close(0); await sleep(800);              // (the player closes their inventory, inside)
  if (process.env.DBG) console.log('INV2', (await run('data get entity TestRat Inventory')).slice(-300));
  ok('...closing the inventory inside brings no sword in (the crafting grid was checked too)', !(await anywhere('diamond_sword')));
  ok('...nor the ingots held on the cursor', !(await anywhere('iron_ingot')));
  ok('...the Ledger and Tokens came in as always', await passes('execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"fixers_ledger"}]') &&
     await passes('execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"token"}]'));

  // ---- out through the Fixer's Door: home, and the sword and ingots come back with the rest
  const ex = (await run('execute in bm:gutter run data get entity @e[type=minecraft:marker,tag=bm.lgexit,limit=1] Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  if (ex) await A.walkTo(+ex[1], +ex[3]);
  await wait(8000, async () => /overworld/.test(await dim())); await sleep(2500);
  ok('out through the Lounge\'s door: home', /overworld/.test(await dim()), await dim());
  ok('...the sword and the ingots are handed back with your gear', await wait(4000, async () => (await anywhere('diamond_sword')) && (await anywhere('iron_ingot'))));

  await run('clear TestRat'); await run(`data remove storage bm:gv bag.p${pid}`); await run(`data remove storage bm:gv cb.p${pid}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

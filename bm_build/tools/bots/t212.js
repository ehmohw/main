// 2.82i: THE PRIME COOLER - as a regular (non-op) player TestRat, every step a real packet (rcon sets the stage: a field, the
// cooler in hand, and the goods put into it while it's open - the bot can't drag items in a container window).
//   Chef Fromage sells it (8 Tokens). Right-clicked: TestRat sits in its crate, and the inventory key opens "Prime Cooler".
//   Prime cuts put in stay in; plain beef (and anything else) is handed straight back out to TestRat, with a word. Sneaking out:
//   the cooler is back in hand holding only the Prime cuts; anything slipped in at the last moment comes back out too. Opened
//   again, the cuts are all there.
const fs = require('fs');
const { bot, rcon, sleep } = require('./lib_resp');
const OUT = (process.env.BM_OUT || __dirname + '/../../out_p2') + '/BlackMarket_DP/data/bm/function/';
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const passes = async c => /passed/i.test(await run(c));
  const X = 29000, Y = 100, Z = 29000;
  const CR = '@e[type=minecraft:dark_oak_chest_boat,tag=bm.c_cool,limit=1]';
  const have = async (item) => { const o = await run(`clear TestRat ${item} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/) || [0, 0])[1]); };
  const near = async (id) => { const o = await run(`${O}execute as @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..6] if items entity @s contents ${id}`); return +((o.match(/count: (\d+)/i) || [0, 0])[1]); };
  const riding = () => passes(`${O}execute as TestRat on vehicle if entity @s[tag=bm.c_cool]`);
  const held = async () => run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"prime_cooler"}}}].components."minecraft:container"');   // (anywhere in the pack: a handed-back steak may have taken its slot)

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));

  // ---- the chef's offer
  const chef = fs.readdirSync(OUT + 'npc').filter(f => /chef/.test(f)).map(f => fs.readFileSync(OUT + 'npc/' + f, 'utf8')).join('\n');
  const i = chef.indexOf('bm:"prime_cooler"'); const of = i < 0 ? '' : chef.slice(chef.lastIndexOf('{buy:', i), i);
  ok('Chef Fromage sells the Prime Cooler for 8 Tokens', /count:8,[^]*bm:"token"/.test(of), of.slice(0, 90));

  // ---- the stage
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:grass_block`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 6} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
  await run('loot replace entity TestRat hotbar.0 loot bm:items/prime_cooler'); A.slot(0); await sleep(300);

  // ---- right-click: into the crate; the inventory key opens it
  A.bars.length = 0; A.use(); await sleep(300); A.release(); await sleep(800);
  ok('right-clicked: TestRat sits in the cooler\'s crate (the cooler out of hand while it\'s open)', (await riding()) && !(await have('*[minecraft:custom_data~{bm:"prime_cooler"}]')));
  A.ride(0, 0, {}); A.windows.length = 0;
  A.write('entity_action', { entityId: A.eid, actionId: 'open_inventory', jumpBoost: 0 }); await sleep(800);
  const w = A.windows.slice(-1)[0]; const wt = w ? JSON.stringify(w.windowTitle || w.title || w) : '';
  ok('...the inventory key opens it: "Prime Cooler"', /Prime Cooler/.test(wt), wt.slice(0, 120));

  // ---- goods in (the stage): two Prime cuts, plain beef, a cooked steak
  await run(`${O}loot replace entity ${CR} container.0 loot bm:items/prime_beef`);
  await run(`${O}data modify entity ${CR} Items[{Slot:0b}].count set value 5`);
  await run(`${O}item replace entity ${CR} container.1 with minecraft:beef 3`);
  await run(`${O}loot replace entity ${CR} container.2 loot bm:items/prime_chicken`);
  await run(`${O}item replace entity ${CR} container.3 with minecraft:cooked_beef 2`);
  const kicked = await wait(3000, async () => !(await passes(`${O}execute if items entity ${CR} container.1 *`)) && !(await passes(`${O}execute if items entity ${CR} container.3 *`)));
  ok('plain beef and a steak put in: handed straight back out', kicked);
  ok('...the Prime cuts stay in', (await passes(`${O}execute if items entity ${CR} container.0 *[minecraft:custom_data~{bm:"prime_beef"}]`)) &&
                                 (await passes(`${O}execute if items entity ${CR} container.2 *[minecraft:custom_data~{bm:"prime_chicken"}]`)));
  await sleep(800);
  const beef = (await have('minecraft:beef')) + (await near('minecraft:beef')), steak = (await have('minecraft:cooked_beef')) + (await near('minecraft:cooked_beef'));
  ok('...and TestRat gets the beef and the steak back (none lost), with a word', beef === 3 && steak === 2 && A.bars.some(b => /Only Prime cuts/.test(b)),
     `beef ${beef}, steak ${steak}, ${A.bars.slice(-1)}`);

  // ---- sneak out: the cooler back in hand, the cuts inside
  if (w) A.close(w.windowId); await sleep(200);
  A.ride(0, 0, { shift: true }); await sleep(600); A.ride(0, 0, {}); await sleep(300); A.unride(); A.stand();
  await wait(3000, async () => /prime_beef/.test(await held()), 300);
  const c1 = await held();
  ok('sneaking out: the cooler is back in hand, holding the Prime cuts and nothing else',
     !(await riding()) && /prime_beef/.test(c1) && /prime_chicken/.test(c1) && !/id: ?"minecraft:(beef|cooked_beef)"/.test(c1), `riding ${await riding()} ${c1.slice(0, 200)}`);

  // ---- slipped in at the last moment: out it comes as the cooler closes
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`); await run('clear TestRat minecraft:beef'); await run('clear TestRat minecraft:cooked_beef');
  const sl = +(((await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"prime_cooler"}}}].Slot')).match(/(\d+)b/) || [0, 0])[1]);
  if (sl > 8) { await run(`item replace entity TestRat hotbar.8 from entity TestRat container.${sl}`); await run(`item replace entity TestRat container.${sl} with minecraft:air`); }
  A.slot(Math.min(sl, 8)); await sleep(300);                                            // (TestRat picks the cooler from wherever it went)
  A.use(); await sleep(300); A.release(); await sleep(800);
  ok('opened again: the cuts are all there (5 Prime Beef, the Prime Chicken)', (await riding()) &&
     (await passes(`${O}execute if items entity ${CR} container.0 *[minecraft:custom_data~{bm:"prime_beef"}]`)) &&
     /(^|\D)5$/.test((await run(`${O}data get entity ${CR} Items[{Slot:0b}].count`)).trim()) &&
     (await passes(`${O}execute if items entity ${CR} container.2 *[minecraft:custom_data~{bm:"prime_chicken"}]`)),
     `slot ${sl}, beef ${(await run(`${O}data get entity ${CR} Items[{Slot:0b}].count`)).trim().slice(-3)}`);
  await run(`${O}execute as ${CR} run item replace entity @s container.5 with minecraft:porkchop 4`); await run('ride TestRat dismount');
  A.unride(); A.stand();
  await wait(3000, async () => /prime_beef/.test(await held()), 300); await sleep(800);
  const c2 = await held(); const pork = (await have('minecraft:porkchop')) + (await near('minecraft:porkchop'));
  ok('a raw porkchop slipped in as it closes: back out to TestRat, the cooler keeps only the cuts', /prime_beef/.test(c2) && !/id: ?"minecraft:porkchop"/.test(c2) && pork === 4,
     `pork ${pork} ${c2.slice(0, 160)}`);

  // ---- clean up
  await run(`${O}execute as @e[type=minecraft:dark_oak_chest_boat,tag=bm.c_cool] run tp @s ~ -400 ~`); await run(`${O}kill @e[type=minecraft:dark_oak_chest_boat,tag=bm.c_cool]`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

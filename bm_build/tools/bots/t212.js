// 2.82i/j: THE PRIME COOLER - as a regular (non-op) player TestRat, every step a real packet (rcon sets the stage: a field, the
// cooler in hand, meat dropped on the ground, and the goods put into it while it's open - the bot can't drag items in a
// container window).
//   Chef Fromage sells it (8 Tokens). Carried, it gathers Prime cuts lying nearby into itself - and leaves plain meat on the
//   ground (2.82j). Right-clicked, it unfolds into a barrel in front of TestRat (2.82j - it was a chest boat TestRat sat in),
//   named "Prime Cooler"; a right-click on the barrel opens it. Prime cuts put in stay in; plain beef (and anything else) is
//   handed straight back out to TestRat, with a word. Sneaking: the barrel packs back into the cooler, which holds only the
//   Prime cuts. Unfolded again, the cuts are all there; a raw porkchop slipped in, and TestRat walking off: the barrel packs
//   itself up and the porkchop comes back out too. And where nothing may be set down (the Black Market), it won't unfold.
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
  const BX = `${X} ${Y} ${Z + 2}`;                                                       // (TestRat stands at the middle facing south: the barrel's spot)
  const COOL = '*[minecraft:custom_data~{bm:"prime_cooler"}]';
  const have = async (item) => { const o = await run(`clear TestRat ${item} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/) || [0, 0])[1]); };
  const near = async (id) => { const o = await run(`${O}execute as @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12] if items entity @s contents ${id}`); return +((o.match(/count: (\d+)/i) || [0, 0])[1]); };
  const barrel = () => passes(`${O}execute if block ${BX} minecraft:barrel`);
  const held = async () => run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"prime_cooler"}}}].components."minecraft:container"');   // (anywhere in the pack: a handed-back steak may have taken its slot)
  const pick = async () => {                                                            // (TestRat takes the cooler in hand, wherever it went)
    const sl = +(((await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"prime_cooler"}}}].Slot')).match(/(\d+)b/) || [0, 0])[1]);
    if (sl > 8) { await run(`item replace entity TestRat hotbar.8 from entity TestRat container.${sl}`); await run(`item replace entity TestRat container.${sl} with minecraft:air`); }
    A.slot(Math.min(sl, 8)); await sleep(300); };
  const unfold = async () => { A.bars.length = 0; A.use(); await sleep(300); A.release(); await sleep(800); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));

  // ---- the chef's offer
  const chef = fs.readdirSync(OUT + 'npc').filter(f => /chef/.test(f)).map(f => fs.readFileSync(OUT + 'npc/' + f, 'utf8')).join('\n');
  const i = chef.indexOf('bm:"prime_cooler"'); const of = i < 0 ? '' : chef.slice(chef.lastIndexOf('{buy:', i), i);
  ok('Chef Fromage sells the Prime Cooler for 8 Tokens', /count:8,[^]*bm:"token"/.test(of), of.slice(0, 90));

  // ---- the stage
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 12} ${Y - 1} ${Z - 12} ${X + 12} ${Y - 1} ${Z + 12} minecraft:grass_block`);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y + 6} ${Z + 12} minecraft:air`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..16]`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1500); A.stand();
  await run('loot replace entity TestRat hotbar.0 loot bm:items/prime_cooler'); A.slot(0); await sleep(300);

  // ---- carried: Prime cuts lying 4 blocks off fly into it; plain meat beside them stays put
  await run(`${O}loot spawn ${X - 3.5} ${Y} ${Z + 0.5} loot bm:items/prime_mutton`);
  await run(`${O}loot spawn ${X - 3.5} ${Y} ${Z + 0.5} loot bm:items/prime_mutton`);
  await run(`${O}summon minecraft:item ${X - 3.5} ${Y} ${Z + 1.5} {Item:{id:"minecraft:mutton",count:2}}`);
  await wait(4000, async () => /prime_mutton/.test(await held()), 300); await sleep(600);
  const c0 = await held();
  ok('carried: the cooler gathers the Prime Mutton lying nearby into itself (both, as one stack)',
     /prime_mutton/.test(c0) && /count: ?2/.test(c0) && (await near('*[minecraft:custom_data~{bm:"prime_mutton"}]')) === 0, c0.slice(0, 120));
  ok('...and leaves the plain mutton on the ground', (await near('minecraft:mutton')) === 2 && (await have('minecraft:mutton')) === 0);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..16]`);

  // ---- right-click: a barrel in front of TestRat, no boat; a right-click on it opens "Prime Cooler"
  await unfold();
  ok('right-clicked: the cooler unfolds into a barrel in front of TestRat (out of hand while it\'s open) - no boat, nobody riding',
     (await barrel()) && !(await have(COOL)) && !(await passes(`${O}execute as TestRat on vehicle`)) &&
     !(await passes(`${O}execute if entity @e[type=minecraft:dark_oak_chest_boat,x=${X},y=${Y},z=${Z},distance=..8]`)));
  ok('...holding what the cooler held (the gathered Prime Mutton)', await passes(`${O}execute if items block ${BX} container.* *[minecraft:custom_data~{bm:"prime_mutton"}]`));
  A.windows.length = 0; A.useOn(X, Y, Z + 2, 1); await sleep(800);
  const w = A.windows.slice(-1)[0]; const wt = w ? JSON.stringify(w.windowTitle || w.title || w) : '';
  ok('...a right-click on the barrel opens it: "Prime Cooler"', /Prime Cooler/.test(wt), wt.slice(0, 120));

  // ---- goods in (the stage): two Prime cuts, plain beef, a cooked steak
  await run(`${O}item replace block ${BX} container.0 with minecraft:air`);
  await run(`${O}loot replace block ${BX} container.0 loot bm:items/prime_beef`);
  await run(`${O}data modify block ${BX} Items[{Slot:0b}].count set value 5`);
  await run(`${O}item replace block ${BX} container.1 with minecraft:beef 3`);
  await run(`${O}loot replace block ${BX} container.2 loot bm:items/prime_chicken`);
  await run(`${O}item replace block ${BX} container.3 with minecraft:cooked_beef 2`);
  const kicked = await wait(3000, async () => !(await passes(`${O}execute if items block ${BX} container.1 *`)) && !(await passes(`${O}execute if items block ${BX} container.3 *`)));
  ok('plain beef and a steak put in: handed straight back out', kicked);
  ok('...the Prime cuts stay in', (await passes(`${O}execute if items block ${BX} container.0 *[minecraft:custom_data~{bm:"prime_beef"}]`)) &&
                                 (await passes(`${O}execute if items block ${BX} container.2 *[minecraft:custom_data~{bm:"prime_chicken"}]`)));
  await sleep(800);
  const beef = (await have('minecraft:beef')) + (await near('minecraft:beef')), steak = (await have('minecraft:cooked_beef')) + (await near('minecraft:cooked_beef'));
  ok('...and TestRat gets the beef and the steak back (none lost), with a word', beef === 3 && steak === 2 && A.bars.some(b => /Only Prime cuts/.test(b)),
     `beef ${beef}, steak ${steak}, ${A.bars.slice(-1)}`);

  // ---- sneak: the barrel packs back up into the cooler, the cuts inside
  if (w) A.close(w.windowId); await sleep(300);
  A.input({ shift: true }); await sleep(700); A.input({}); await sleep(300);
  await wait(3000, async () => /prime_beef/.test(await held()), 300);
  const c1 = await held();
  ok('sneaking: the barrel packs up - the cooler back with TestRat, holding the Prime cuts and nothing else',
     !(await barrel()) && /prime_beef/.test(c1) && /prime_chicken/.test(c1) && !/id: ?"minecraft:(beef|cooked_beef)"/.test(c1), `barrel ${await barrel()} ${c1.slice(0, 120)}`);

  // ---- unfolded again; a porkchop slipped in, and TestRat walks off: it packs itself up, the porkchop handed back
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..16]`); await run('clear TestRat minecraft:beef'); await run('clear TestRat minecraft:cooked_beef');
  await pick(); await unfold();
  ok('unfolded again: the cuts are all there (5 Prime Beef, the Prime Chicken)', (await barrel()) &&
     /(^|\D)5$/.test((await run(`${O}data get block ${BX} Items[{Slot:0b}].count`)).trim()) &&
     (await passes(`${O}execute if items block ${BX} container.2 *[minecraft:custom_data~{bm:"prime_chicken"}]`)));
  await run(`${O}item replace block ${BX} container.5 with minecraft:porkchop 4`);
  await A.walkTo(X + 0.5, Z - 8.5);
  await wait(4000, async () => !(await barrel()), 300); await sleep(1200);
  const c2 = await held(); const pork = (await have('minecraft:porkchop')) + (await near('minecraft:porkchop'));
  ok('walking off with a raw porkchop slipped in: the barrel packs itself up, the porkchop back out to TestRat, the cooler keeps only the cuts',
     !(await barrel()) && /prime_beef/.test(c2) && !/id: ?"minecraft:porkchop"/.test(c2) && pork === 4, `barrel ${await barrel()} pork ${pork} ${c2.slice(0, 100)}`);

  // ---- where nothing may be set down: it won't unfold (the stage: TestRat beside a Black Market marker)
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1000); A.stand();
  await run(`${O}summon minecraft:marker ${X} ${Y} ${Z - 4} {Tags:["bm.mkt","t212mkt"]}`);
  await pick(); await unfold();
  ok('beside the Black Market: it won\'t unfold, and stays in hand', !(await barrel()) && (await have(COOL)) === 1 && A.bars.some(b => /won.t unfold/.test(b)), A.bars.slice(-1).join(''));
  await run(`${O}kill @e[type=minecraft:marker,tag=t212mkt]`);

  // ---- clean up
  await run(`${O}execute as @e[type=minecraft:marker,tag=bm.bxm,x=${X},y=${Y},z=${Z},distance=..16] at @s run function bm:p33/box/close`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..16]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

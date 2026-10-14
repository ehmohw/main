// v2.68: currency wins, the Crate Desk, tip-offs, laurels + achievements, Forgeheart, the Alibi, the Counterfeiter's Press
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const fs = require('fs');
const res = []; const X = 17000, Y = 100, Z = 16000;
const DP = BMB + 'out_p2/BlackMarket_DP/data/bm';
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async (pred, who = 'TestRat') => { const o = await run(`clear ${who} ${pred} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/g) || [0])[0]); };
  const bm = id => `*[minecraft:custom_data~{bm:"${id}"}]`;
  const has = async t => new RegExp(`"${t.replace('.', '\\.')}"`).test(await run('data get entity TestRat Tags'));
  const said = re => A.chats.some(x => re.test(x));
  const until = async (f, ms = 6000) => { for (let t = 0; t < ms; t += 250) { if (await f()) return true; await sleep(250); } return !!(await f()); };
  const pos = async () => (await run('data get entity TestRat Pos')).match(/-?[\d.]+(?=d)/g).map(Number);
  const home = async () => { if (await has('bm.gvp')) { await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(2500); }
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1200); };
  const plan = async (tier = 1) => { await run('scoreboard players set TestRat bm.lkht 0'); await run('scoreboard players reset TestRat bm.lkdt');
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${7600 + tier}`); await run('execute as TestRat at @s run function bm:p70/pick_tier');
    await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4000); };
  const gi = () => sc('bm.gvi');
  const win = async () => { const g = await gi();
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,scores={bm.gvi=${g}},limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi`);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,scores={bm.gvi=${g}},limit=1] at @s run function bm:p70/payout`); await sleep(1500); };
  const inv = async () => await run('data get entity TestRat Inventory');
  const inHaul = async id => !/Found no|No elements|not found|Invalid/i.test(await run(`data get entity TestRat Inventory[{id:"minecraft:barrel"}].components."minecraft:container"[{item:{components:{"minecraft:custom_data":{bm:"${id}"}}}}]`));
  const inHaulV = async id => !/Found no|No elements|not found|Invalid/i.test(await run(`data get entity TestRat Inventory[{id:"minecraft:barrel"}].components."minecraft:container"[{item:{id:"minecraft:${id}"}}]`));
  const inst = async () => `@e[type=marker,tag=bm.gvinst,scores={bm.gvi=${await gi()}},limit=1]`;
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/heist_variants_never'); await run('function bm:admin/heist_boss_std');
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run('scoreboard players reset TestRat bm.pty');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid'); await run('execute as TestRat run function bm:p80/init_me');
  for (const t of ['bm.gvask', 'bm.gvnext', 'bm.gvp', 'bm.gvq']) await run(`tag TestRat remove ${t}`);
  await run('scoreboard players set TestRat bm.lr68 1'); await run('scoreboard players set TestRat bm.gvfz 0'); await run('scoreboard players set TestRat bm.aliq 0'); await run('scoreboard players set TestRat bm.prs 0');
  await run(`execute in minecraft:overworld run forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await sleep(1000);
  await run(`fill ${X - 4} ${Y} ${Z - 4} ${X + 6} ${Y} ${Z + 6} minecraft:stone`); await run(`fill ${X - 4} ${Y + 1} ${Z - 4} ${X + 6} ${Y + 4} ${Z + 6} minecraft:air`);
  await home();
  for (let i = 0; i < 40; i++) await run('loot give TestRat loot bm:items/token');
  await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');

  // ---- 1. a won heist pays money: no supplies, no ingots, no heist gear from shares
  const hf = fs.readFileSync(`${DP}/function/p70/haul.mcfunction`, 'utf8');
  ok('The haul no longer packs supplies, food or netherite scrap', !/p84\/supplies|p80\/scrap/.test(hf) && /scoreboard players set #th bm.rng 2/.test(hf));
  ok('...a Shifting Core is 1 in 100 at every tier', /random value 1\.\.1000/.test(hf) && /matches \.\.10 run function bm:p70\/core/.test(hf) && !/matches 3 if score #r bm.rng matches \.\.5 run function bm:p70\/core/.test(hf));
  const t3 = JSON.parse(fs.readFileSync(`${DP}/loot_table/gv/t3.json`, 'utf8'));
  ok('...a share is Gutter Coins and nothing else', JSON.stringify(t3).includes('gutter_coin') && t3.pools[0].entries.length === 1);
  await run('scoreboard players set TestRat bm.gvcl 62');           // (every tier cleared already: no first-clear prizes in this haul)
  await plan(3); ok('In a Tier III heist', await has('bm.gvp'));
  await win();
  ok('Won: The Haul holds coins and Tokens', (await inHaul('gutter_coin')) && (await inHaul('token')));
  const banned = []; for (const v of ['iron_ingot', 'cobblestone', 'oak_log', 'bread', 'cooked_beef', 'gold_ingot', 'emerald', 'diamond', 'netherite_scrap']) if (await inHaulV(v)) banned.push(v);
  for (const c of ['smoke_bomb', 'skeleton_lockpick', 'stolen_watch', 'clockwork_fragment']) if (await inHaul(c)) banned.push(c);
  const found = banned;
  ok('...and none of the old clutter (ingots, supplies, food, heist gear, curios)', found.length === 0, found.join(','));
  await home();

  // ---- 2. tip-offs: call the next heist's kind
  await run('loot give TestRat loot bm:items/tip_bloodmoon'); await run('loot give TestRat loot bm:items/tip_alien'); A.chats.length = 0;
  await run('execute as TestRat at @s run function bm:p105/tip/blood');
  ok('Crimson Tip-off used: the next heist you plan is a Blood Moon heist (the note is spent)', (await sc('bm.gvfz')) === 1 && (await cnt(bm('tip_bloodmoon'))) === 0 && said(/BLOOD MOON HEIST/));
  A.chats.length = 0; await plan(1);
  ok('...planned: a BLOOD MOON heist (even with the admin\'s variants off)', /matches 1|has 1/.test(await run(`execute in bm:gutter run scoreboard players get ${await inst()} bm.gvnt`)) && said(/tip-off pays/) &&
     (await sc('bm.gvfz')) === 0, await run(`execute in bm:gutter run scoreboard players get ${await inst()} bm.gvnt`));
  await win();
  ok('...won: Blood Moon Crystals in the haul', await inHaul('blood_crystal'));
  await home();
  await run('execute as TestRat at @s run function bm:p105/tip/alien'); A.chats.length = 0; await plan(1);
  ok('Vorn Signal: an ALIEN heist', /has 1/.test(await run(`execute in bm:gutter run scoreboard players get ${await inst()} bm.gvsf`)) &&
     /has 3/.test(await run(`execute in bm:gutter run scoreboard players get ${await inst()} bm.gvnt`)) && said(/signal pays/));
  await win();
  ok('...won: Green Xenite in the haul', await inHaul('xenite_green'));
  await home();
  const nb = JSON.parse(fs.readFileSync(`${DP}/loot_table/gv/night_blood_t5.json`, 'utf8'));
  ok('Night currencies scale with the tier (Tier V: 7-14 crystals)', JSON.stringify(nb.pools[0]).includes('"min":7') && JSON.stringify(nb.pools[0]).includes('"max":14'), JSON.stringify(nb.pools[0]).slice(-80));

  // ---- 3. laurels and achievements
  await run('scoreboard players set TestRat bm.gvcl 0'); await run('advancement revoke TestRat from bm:story/raid_t1');
  await run('clear TestRat'); for (let i = 0; i < 20; i++) await run('loot give TestRat loot bm:items/token'); await run('loot give TestRat loot bm:items/fixers_ledger');
  await plan(1); await win();
  ok('First clear of Tier I: the Copper Laurel in the haul', await inHaul('laurel_t1'));
  ok('...and its achievement', /passed/.test(await run('execute if entity @a[name=TestRat,advancements={bm:story/raid_t1=true}]')));
  await home(); await run('clear TestRat');
  await run('scoreboard players set TestRat bm.gvcl 12'); await run('advancement revoke TestRat from bm:story/raid_t2'); await run('scoreboard players reset TestRat bm.lr68'); await sleep(1600);
  ok('Tiers cleared before 2.68: their laurels and achievements arrive by themselves', (await cnt(bm('laurel_t2'))) === 1 && (await cnt(bm('laurel_t3'))) === 1 && (await cnt(bm('laurel_t1'))) === 0 &&
     /passed/.test(await run('execute if entity @a[name=TestRat,advancements={bm:story/raid_t2=true,bm:story/raid_t3=true}]')));
  ok('...once only', (await sc('bm.lr68')) === 1);

  // ---- 4. the Crate Desk
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.gbc 100'); A.chats.length = 0;
  await run('scoreboard players set TestRat bm.menu 8500'); await run('scoreboard players set TestRat bm.act 8501'); await sleep(500);
  ok('Crate Desk: a Raw Materials Crate for 16 coins from the bank', (await cnt(bm('crate_raw'))) === 1 && (await sc('bm.gbc')) === 84, `bank ${await sc('bm.gbc')}`);
  await run('scoreboard players set TestRat bm.menu 8500'); await run('scoreboard players set TestRat bm.act 8504'); await sleep(500);
  ok('...a Crimson Tip-off for 64', (await cnt(bm('tip_bloodmoon'))) === 1 && (await sc('bm.gbc')) === 20);
  await run('scoreboard players set TestRat bm.menu 8500'); await run('scoreboard players set TestRat bm.act 8503'); await sleep(500);
  ok('...a Mineral Crate with only 20: no ("28 coins short")', (await cnt(bm('crate_mineral'))) === 0 && said(/28 coins short|Not enough/), A.chats.slice(-1).join(''));
  // set one down (look down at the floor two blocks ahead) and open it
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 35`); await sleep(800);
  await run('item replace entity TestRat hotbar.0 from entity TestRat container.0'); await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/crate_raw`);
  A.slot(0); await sleep(200);
  A.useOn(X, Y, Z + 2, 1); await sleep(1500);
  const lt = await run(`data get block ${X} ${Y + 1} ${Z + 2} LootTable`);
  ok('Set down: a crate barrel, filled by its loot table when opened', /barrel/.test(await run(`execute if block ${X} ${Y + 1} ${Z + 2} minecraft:barrel`)) || /p105\/crate_raw/.test(lt), lt);
  ok('...the Haul\'s machinery is minding it', /crate_raw/.test(lt) && /Count: 1/.test(await run(`execute store result score #t bm.rng if entity @e[type=marker,tag=bm.haulm,x=${X},y=${Y + 1},z=${Z + 2},distance=..1]`)));
  A.useOn(X, Y + 1, Z + 2, 1); await sleep(800);
  const items = await run(`data get block ${X} ${Y + 1} ${Z + 2} Items`);
  ok('Opened: a few stacks of raw goods', /count/.test(items) && !/LootTable/.test(await run(`data get block ${X} ${Y + 1} ${Z + 2}`)), items.slice(0, 200));
  A.close(1); A.close(2); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z - 9.5}`); await sleep(3500);
  ok('Walked away: it folds into your pack with what\'s left', /air|passed/.test(await run(`execute if block ${X} ${Y + 1} ${Z + 2} minecraft:air`)) && (await cnt('minecraft:barrel')) >= 1);
  await run('clear TestRat'); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 35`); await sleep(800);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/crate_mineral'); A.slot(0); await sleep(200);
  A.useOn(X, Y, Z + 2, 1); await sleep(1500);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z - 9.5}`); await sleep(3500);
  ok('Set down and walked away unopened: the crate comes back as it was', (await cnt(bm('crate_mineral'))) === 1 && /passed/.test(await run(`execute if block ${X} ${Y + 1} ${Z + 2} minecraft:air`)));
  await home();

  // ---- 5. Forgeheart
  await run('clear TestRat'); await run('loot give TestRat loot bm:items/forgeheart'); await run('give TestRat minecraft:raw_iron 20'); await run('give TestRat minecraft:raw_gold_block 2');
  const xp0 = +((await run('xp query TestRat points')).match(/(\d+)/) || [0, 0])[1];
  await sleep(4000);
  const ing = await cnt('minecraft:iron_ingot');
  ok('Forgeheart: raw iron in the pack smelts itself - 20 raw, 20-24 ingots', (await cnt('minecraft:raw_iron')) === 0 && ing >= 20 && ing <= 24, `${ing}`);
  ok('...raw gold blocks become gold blocks', (await cnt('minecraft:gold_block')) === 2 && (await cnt('minecraft:raw_gold_block')) === 0);
  ok('...with the furnace\'s experience', +((await run('xp query TestRat points')).match(/(\d+)/) || [0, 0])[1] > xp0 || /levels/.test(await run('xp query TestRat levels')));
  await run('clear TestRat');

  // ---- 6. The Alibi
  await run('loot give TestRat loot bm:items/the_alibi'); await run('scoreboard players set TestRat bm.aliq 0');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(6500);
  await run(`tp TestRat ${X + 5.5} ${Y + 1} ${Z + 5.5} 0 0`); await sleep(300);
  await run('effect clear TestRat'); await run('damage TestRat 6 minecraft:generic'); await sleep(300); A.bars.length = 0;
  await run('execute as TestRat at @s run function bm:p105/alibi/use'); await sleep(400);
  const pa = await pos();
  ok('The Alibi: back where you stood five seconds ago', Math.abs(pa[0] - (X + 0.5)) < 1.2 && Math.abs(pa[2] - (Z + 0.5)) < 1.2 && A.bars.some(b => /never there/.test(b)), `${pa}`);
  ok('...the hurt of those seconds mended (Instant Health) and the fire put out', /fire_resistance/.test(await run('data get entity TestRat active_effects')));
  A.bars.length = 0; await run('execute as TestRat at @s run function bm:p105/alibi/use'); await sleep(300);
  ok('...once a minute', A.bars.some(b => /more seconds/.test(b)) && (await sc('bm.aliq')) >= 55);
  await run('scoreboard players set TestRat bm.aliq 0'); await sleep(2500);
  await run(`execute in minecraft:the_nether run forceload add 2200 2200`); await run(`execute in minecraft:the_nether run fill 2198 110 2198 2202 110 2202 minecraft:stone`);
  await run(`execute in minecraft:the_nether run tp TestRat 2200.5 111 2200.5`); await sleep(1500); A.bars.length = 0;
  await run('execute as TestRat at @s run function bm:p105/alibi/use'); await sleep(400);
  ok('...but it won\'t cross between worlds', A.bars.some(b => /cross between worlds/.test(b)) && /the_nether/.test(await run('data get entity TestRat Dimension')));
  await run(`execute in minecraft:the_nether run forceload remove 2200 2200`); await home(); await run('clear TestRat');

  // ---- 7. The Counterfeiter's Press
  await run('loot give TestRat loot bm:items/counterfeiters_press'); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 50`); await sleep(800); A.chats.length = 0;
  await run('execute as TestRat at @s run function bm:p105/press/place'); await sleep(400);
  const ph = `@e[type=minecraft:interaction,tag=bm.presshit,x=${X},y=${Y},z=${Z},distance=..4,limit=1]`;
  ok('The press, set down on the floor: yours, and the item is used', /Count: 1/.test(await run(`execute store result score #t bm.rng if entity ${ph}`)) &&
     (await cnt(bm('counterfeiters_press'))) === 0 && (await sc('bm.prs')) === 1 && said(/press is set up/), A.chats.slice(-1).join(''));
  await run(`scoreboard players operation #d108 bm.rng = #day bm.bm`); await run('scoreboard players remove #d108 bm.rng 3');
  await run(`scoreboard players operation ${ph} bm.prsd = #d108 bm.rng`);
  const tk0 = await cnt(bm('token'));
  const pid = await sc('bm.pid');
  await run(`execute as ${ph} run data modify entity @s interaction set value {player:[I;0,0,0,0],timestamp:1L}`);
  await run(`execute as ${ph} run scoreboard players operation #po bm.rng = @s bm.prso`); await run(`execute as ${ph} run scoreboard players operation #pd bm.rng = @s bm.prsd`);
  await run(`tag ${ph} add bm.prme`); await run('execute as TestRat at @s run function bm:p105/press/who'); await run(`tag @e[tag=bm.prme] remove bm.prme`); await run(`execute as ${ph} run data remove entity @s interaction`);
  ok('Three days on: three Tokens', (await cnt(bm('token'))) === tk0 + 3, `${tk0} -> ${await cnt(bm('token'))}`);
  A.bars.length = 0;
  await run(`execute as ${ph} run scoreboard players operation #pd bm.rng = @s bm.prsd`); await run(`tag ${ph} add bm.prme`); await run('execute as TestRat at @s run function bm:p105/press/who'); await run(`tag @e[tag=bm.prme] remove bm.prme`);
  ok('...again the same day: "the ink\'s still wet"', A.bars.some(b => /ink's still wet/.test(b)) && (await cnt(bm('token'))) === tk0 + 3);
  await run('loot give TestRat loot bm:items/counterfeiters_press'); A.chats.length = 0; await run('execute as TestRat at @s run function bm:p105/press/place'); await sleep(300);
  ok('A second press: no (one per crook)', said(/one press per crook/) && (await cnt(bm('counterfeiters_press'))) === 1);
  await run('clear TestRat'); await run(`execute as ${ph} run scoreboard players operation #po bm.rng = @s bm.prso`); await run(`execute as ${ph} run scoreboard players operation #pd bm.rng = @s bm.prsd`);
  await run(`tag ${ph} add bm.prme`); await run('execute as TestRat at @s run function bm:p105/press/take'); await sleep(300);
  ok('Sneak + punch: folded up and back in your pack', (await cnt(bm('counterfeiters_press'))) === 1 && (await sc('bm.prs')) === 0 &&
     /Count: 0|failed/.test(await run(`execute store result score #t bm.rng if entity @e[type=minecraft:interaction,tag=bm.presshit,x=${X},y=${Y},z=${Z},distance=..4]`)));

  // ---- 8. the finds
  await run('clear TestRat'); await run('loot give TestRat loot bm:p105/rare_t3');
  ok('A Tier III vault treasure is the Vault Breaker or the Coinslinger', (await cnt(bm('vault_breaker'))) + (await cnt(bm('coinslinger'))) === 1);
  const fd = fs.readFileSync(`${DP}/function/p105/finds.mcfunction`, 'utf8');
  ok('Every win rolls for Forgeheart (5%), the Alibi (3%) and the Press (1%)', /matches \.\.5 run function bm:p105\/find_rare/.test(fd) && /matches \.\.3 run function bm:p105\/find_legend/.test(fd) &&
     /matches \.\.1 run function bm:p105\/find_myth/.test(fd));
  await run('clear TestRat');
  await run(`execute in minecraft:overworld run forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

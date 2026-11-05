// 3.1: COLLECTOR ACCOUNTS (phase278), the owner's basic pass, as a regular (non-op) player - rcon only sets the stage. The Fence sells
// the Stone Collector and the Wood Box; the Stone Collector used: its account's front page (Natural, Polished, Bricks, Chiseled,
// Deposit everything, Auto-collect: off); Auto-collect on - dropped cobblestone and granite in his main rows go in, the stone in his
// hotbar stays; Natural › Cobblestone ×10 › Take a stack, Deposit all of these; the Wood Box's Deposit everything (oak logs) and its Logs
// page; on the Rat Pack (off hand + the Pack): its Collectors row opens the account, with « Collectors and Take it off the Pack; and the
// move-over - an old Spirit Jar holding rotten flesh and a custom item: the flesh into the account, the custom item handed back, the jar's
// container gone; an old jar on the Pack's 3.0 list: its bones moved over, the jar the Pack's one.
const { bot, rcon, sleep } = require('./lib_resp');
(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:Count: |has |data: |Found )(-?\d+)/) || [0, -1])[1]);
  const has = async (sel) => Math.max(0, await num(`clear TestRat ${sel} 0`));
  const X = 21040, Y = 180, Z = 16040;
  await run(`forceload add ${X - 16} ${Z - 16} ${X + 32} ${Z + 32}`);
  await run(`fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 20} ${Y - 1} ${Z + 20} minecraft:smooth_stone`); await run(`fill ${X - 8} ${Y} ${Z - 8} ${X + 20} ${Y + 4} ${Z + 20} minecraft:air`);
  await run(`kill @e[type=minecraft:item,x=${X - 10},y=${Y - 2},z=${Z - 10},dx=32,dy=8,dz=32]`);
  const A = await bot('TestRat'); await sleep(2500);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1200); A.stand(); await sleep(300);
  { const _p = A.press.bind(A); A.press = async (re, ms) => { await sleep(500); return _p(re, ms); }; }
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat resistance 600 4 true');
  const pid = await num('scoreboard players get TestRat bm.pid');
  await run(`data remove storage bm:cb p${pid}`); for (const k of ['stone', 'wood', 'ore', 'mob']) { await run(`scoreboard players reset TestRat bm.cba_${k}`); await run(`scoreboard players set TestRat bm.rcb_${k} 0`); }
  const bal = (k, n) => num(`data get storage bm:cb p${pid}.k${k}.i${n}`);
  const useSlot = async (s) => { A.slot(s); await sleep(250); const n0 = A.dialogN.length; A.use(); await sleep(350); A.release(); await wait(2500, async () => A.dialogN.length > n0, 100); };

  // ---- the Fence sells both
  await run(`execute positioned ${X + 6.5} ${Y} ${Z - 4.5} run function bm:npc/fence`); await sleep(2500);
  const fence = `@e[type=minecraft:wandering_trader,tag=bm.npc_fence,x=${X + 6},y=${Y},z=${Z - 5},distance=..3,limit=1]`;
  const sells = async (iid) => /passed/i.test(await run(`execute if data entity ${fence} Offers.Recipes[{sell:{components:{"minecraft:custom_data":{bm:"${iid}"}}}}]`));
  ok('the Fence sells the Stone Collector and the Wood Box', (await sells('stone_collector')) && (await sells('wood_box')));
  await run(`kill ${fence}`);

  // ---- the Stone Collector: its account
  await run('loot replace entity TestRat hotbar.0 loot bm:items/stone_collector');
  await useSlot(0);
  ok('used: its account - Natural, Polished, Bricks, Chiseled, Deposit everything, Auto-collect: off',
     ['Natural', 'Polished', 'Bricks', 'Chiseled', 'Deposit everything'].every(n => A.buttons().some(b => b.label.includes(n))) && A.buttons().some(b => /Auto-collect: off/.test(b.label)),
     A.buttons().map(b => b.label).join(' | '));
  await A.press(/Auto-collect/);
  ok('...Auto-collect: on', A.buttons().some(b => /Auto-collect: on/.test(b.label)));
  await run('item replace entity TestRat inventory.0 with minecraft:granite 20'); await run('item replace entity TestRat hotbar.2 with minecraft:stone 5');
  await run(`summon minecraft:item ${X + 2.5} ${Y + 0.5} ${Z + 2.5} {Item:{id:"minecraft:cobblestone",count:10},PickupDelay:0s}`);
  ok('...carried: dropped cobblestone and the granite in his main rows go in; the stone in his hotbar stays', await wait(4000, async () => (await bal('stone', 'cobblestone')) === 10 && (await bal('stone', 'granite')) === 20) &&
     (await has('minecraft:stone')) === 5 && (await has('minecraft:granite')) === 0, `${await bal('stone', 'cobblestone')} / ${await bal('stone', 'granite')}`);
  await useSlot(0); await A.press(/Natural/);
  ok('Natural ›: Cobblestone ×10 and Granite ×20', A.buttons().some(b => /cobblestone.*×10/i.test(b.label)) && A.buttons().some(b => /granite.*×20/i.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  await A.press(/cobblestone/i);
  ok('...its page: Take a stack, Take all, Deposit all of these', ['Take a stack', 'Take all', 'Deposit all of these'].every(n => A.buttons().some(b => b.label.includes(n))));
  await run('scoreboard players set TestRat bm.cba_stone 2');
  await A.press(/Take a stack/); await sleep(600);
  ok('...Take a stack: 10 cobblestone in his inventory, none left in it', (await has('minecraft:cobblestone')) === 10 && (await bal('stone', 'cobblestone')) === 0);
  await A.press(/Deposit all of these/); await sleep(500);
  ok('...Deposit all of these: back in the account', (await has('minecraft:cobblestone')) === 0 && (await bal('stone', 'cobblestone')) === 10);

  // ---- the Wood Box
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/wood_box'); await run('give TestRat minecraft:oak_log 7');
  await useSlot(0);
  ok('the Wood Box: Logs, Stripped logs, Planks', ['Logs', 'Stripped logs', 'Planks'].every(n => A.buttons().some(b => b.label.includes(n))));
  await A.press(/Deposit everything/); await sleep(500);
  ok('...Deposit everything: the oak logs into the account', (await has('minecraft:oak_log')) === 0 && (await bal('wood', 'oak_log')) === 7);
  await A.press(/Logs/);
  ok('...Logs ›: Oak Log ×7', A.buttons().some(b => /oak_log.*×7/i.test(b.label)), A.buttons().map(b => b.label).join(' | '));

  // ---- on the Rat Pack: its Collectors row opens the account
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/partner_wheel');
  await run('loot replace entity TestRat weapon.offhand loot bm:items/stone_collector'); await sleep(300);
  A.chats.length = 0; await useSlot(0); await sleep(500);
  ok('the Stone Collector goes on the Rat Pack (off hand + the Pack)', (await num('scoreboard players get TestRat bm.rcb_stone')) === 1 && (await has('*[minecraft:custom_data~{bm:"stone_collector"}]')) === 0);
  await useSlot(0); await A.press(/Collectors/);
  ok('Collectors: its row', A.buttons().some(b => /Stone Collector/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  await A.press(/Stone Collector/);
  ok('...pressed: its account, with « Collectors and Take it off the Pack', A.buttons().some(b => /Natural/.test(b.label)) && A.buttons().some(b => /« Collectors/.test(b.label)) &&
     A.buttons().some(b => /Take it off the Pack/.test(b.label)));
  const bk = await A.press(/« Collectors/);
  ok('...« Collectors: the Collectors page', bk && bk.next && A.buttons().some(b => /Stone Collector/.test(b.label)));

  // ---- moving over: an old Spirit Jar with rotten flesh and a custom item; an old jar on the Pack's 3.0 list
  await run('clear TestRat');
  await run('item replace entity TestRat hotbar.3 with minecraft:totem_of_undying[minecraft:custom_data={bm:"spirit_jar",bmv:45},minecraft:container=[{slot:0,item:{id:"minecraft:rotten_flesh",count:12}},' +
            '{slot:1,item:{id:"minecraft:totem_of_undying",count:1,components:{"minecraft:custom_data":{bm:"emma_ribbon"}}}}]]');
  A.chats.length = 0;
  ok('an old Spirit Jar in his pocket: the flesh into its account, the custom item handed back, its container gone',
     await wait(4000, async () => (await bal('mob', 'rotten_flesh')) === 12) && await wait(3000, async () => (await has('*[minecraft:custom_data~{bm:"emma_ribbon"}]')) === 1) &&
     !/container/.test(await run('data get entity TestRat Inventory[{Slot:3b}].components')), A.chats.slice(-1).join(''));
  ok('...and he is told', A.chats.some(c => /items are in its account now/.test(c)), A.chats.slice(-2).join(' | '));
  await run(`data modify storage bm:pw p${pid}.rb_sj set value [{it:{id:"minecraft:totem_of_undying",count:1,components:{"minecraft:custom_data":{bm:"spirit_jar",bmv:45},"minecraft:container":[{slot:0,item:{id:"minecraft:bone",count:5}}]}}}]`);
  await run('scoreboard players set TestRat bm.rcb_mob 0'); await run('scoreboard players set TestRat bm.cbmig 0');
  ok('an old jar on the Pack\'s 3.0 list: its bones moved over, the jar the Pack\'s one', await wait(4000, async () => (await bal('mob', 'bone')) === 5) &&
     (await num('scoreboard players get TestRat bm.rcb_mob')) === 1 && !/passed/i.test(await run(`execute if data storage bm:pw p${pid}.rb_sj`)));

  await run('clear TestRat'); for (const k of ['stone', 'mob']) await run(`scoreboard players set TestRat bm.rcb_${k} 0`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

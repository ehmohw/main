// 3.1: THE RAT PACK (phase277 - the Partner Wheel renamed and made the pack's carry-all), the owner's BASIC pass, as a regular (non-op)
// player: rcon only sets the stage (items handed over, the Fence summoned, the heist plan bought). Its name (and an old Partner Wheel
// re-issued as a Rat Pack); the Fence selling it (3 Medallions); the front page and each section's page (Partners, Pocket, Keyring,
// Charms, Maps, Mounts, Bags, Collectors, Settings); one of each put on from the off hand (F, then the Pack used) and taken back
// once: a Pocket tool used from its button (the Particle Toggler - its own menu), the Fixer's Ledger, a key (counted as carried at
// the market gate), a charm (its switch: active / resting), a map, a mount call (used: "blow it in the Nether", kept); auto-pack
// pulling a key out of his inventory with its chat line; two Backpacks with different loads (the Bags list's fill and first
// stacks, each one's look inside, each unfolded into a barrel holding its own load and folded back), a Vacuum Satchel's switch
// (on: a dropped item flies into it on the Pack), a Spirit Jar's Deposit and Withdraw all; then a heist: the Pack stays at the coat
// check, a Heist Ledger handed over on the way in, dropped - back in his pocket, and gone when he leaves.
const { bot, rcon, sleep } = require('./lib_resp');
(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 150) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:Count: |has |data: |Found )(-?\d+)/) || [0, -1])[1]);
  const sc = (o) => num(`scoreboard players get TestRat ${o}`);
  const has = async (iid) => Math.max(0, await num(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`));
  const X = 21040, Y = 180, Z = 16040;
  await run(`forceload add ${X - 16} ${Z - 16} ${X + 32} ${Z + 32}`);
  await run(`fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 20} ${Y - 1} ${Z + 20} minecraft:smooth_stone`);
  await run(`fill ${X - 8} ${Y} ${Z - 8} ${X + 20} ${Y + 4} ${Z + 20} minecraft:air`);
  await run(`kill @e[type=minecraft:item,x=${X - 10},y=${Y - 2},z=${Z - 10},dx=32,dy=8,dz=32]`);
  const A = await bot('TestRat'); await sleep(2500);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(1200); A.stand(); await sleep(300);
  { const _p = A.press.bind(A); A.press = async (re, ms) => { await sleep(500); return _p(re, ms); }; }
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat resistance 600 4 true'); await run('effect give TestRat saturation 600 0 true');
  await run('clear TestRat');
  const pid = await sc('bm.pid');
  // (a clean Pack: nothing on it from an earlier run)
  await run(`data remove storage bm:pw p${pid}.rq_particle_toggler`); await run(`data remove storage bm:pw p${pid}.rq_fixers_ledger`);
  for (const o of ['particle_toggler', 'fixers_ledger', 'rat_king_key', 'vkey_brood', 'vkey_frost', 'charm_ember', 'sealed_explorer_map', 'ember_call']) {
    await run(`scoreboard players set TestRat bm.rq_${o} 0`); await run(`data remove storage bm:pw p${pid}.rq_${o}`); }
  for (const k of ['bp', 'vs', 'sj', 'om', 'pc']) { await run(`scoreboard players set TestRat bm.rb_${k} 0`); await run(`data remove storage bm:pw p${pid}.rb_${k}`); }
  await run('scoreboard players reset TestRat bm.rqap_keys'); await run('scoreboard players reset TestRat bm.rqo_charm_ember');

  // ---- the name; an old wheel re-issued
  await run('loot replace entity TestRat hotbar.0 loot bm:items/partner_wheel'); A.slot(0); await sleep(300);
  ok('the Pack is called The Rat Pack', /The Rat Pack/.test(await run('data get entity TestRat Inventory[{Slot:0b}].components."minecraft:item_name"')));
  await run('item replace entity TestRat hotbar.8 with minecraft:totem_of_undying[minecraft:custom_data={bm:"partner_wheel",bmv:45},minecraft:item_name="Partner Wheel"]');
  A.chats.length = 0;
  ok('...an old Partner Wheel in his pocket becomes a Rat Pack (and he is told)', await wait(3000, async () => /The Rat Pack/.test(await run('data get entity TestRat Inventory[{Slot:8b}].components."minecraft:item_name"'))) &&
     A.chats.some(c => /Rat Pack now/.test(c)));
  await run('item replace entity TestRat hotbar.8 with minecraft:air');

  // ---- the Fence sells it
  await run(`execute positioned ${X + 6.5} ${Y} ${Z - 4.5} run function bm:npc/fence`); await sleep(2500);
  const fence = `@e[type=minecraft:wandering_trader,tag=bm.npc_fence,x=${X + 6},y=${Y},z=${Z - 5},distance=..3,limit=1]`;
  // (its list price, 3 Medallions, is sold at the market's scale - economy.py - as it was at Cecil's: 2)
  ok('the Fence sells the Rat Pack, for Medallions (Cecil\'s price)', /passed/i.test(await run(`execute if data entity ${fence} Offers.Recipes[{sell:{components:{"minecraft:custom_data":{bm:"partner_wheel"}}},buy:{components:{"minecraft:custom_data":{bm:"medallion"}}}}]`)),
     await run(`data get entity ${fence} Offers.Recipes[{sell:{components:{"minecraft:custom_data":{bm:"partner_wheel"}}}}].buy`));
  await run(`kill @e[type=minecraft:wandering_trader,tag=bm.npc_fence,x=${X + 6},y=${Y},z=${Z - 5},distance=..3]`);

  // ---- the front page and every section
  const openP = async () => { A.slot(0); await sleep(200); await run('scoreboard players set TestRat bm.gvhc 0'); return A.useWait(2500); };
  ok('using the Pack: its front page - THE RAT PACK, every section', await openP() && ['Partners', 'Pocket', 'Keyring', 'Charms', 'Maps', 'Mounts', 'Bags', 'Collectors', 'Settings', 'Guide']
     .every(n => A.buttons().some(b => b.label.includes(n))), A.buttons().map(b => b.label).join(' | '));
  for (const [sec, want] of [['Partners', /Gallery/], ['Pocket', /Nothing on this page/], ['Keyring', /Nothing on this page/], ['Charms', /Nothing on this page/],
    ['Maps', /Nothing on this page/], ['Mounts', /Nothing on this page/], ['Bags', /Nothing on this page/], ['Collectors', /Nothing on this page/], ['Settings', /Auto-pack|Keys:/]]) {
    await openP(); const p = await A.press(new RegExp(sec));
    const d = A.dialogs[A.dialogs.length - 1] || '';
    ok(`...${sec} › opens its page (with « Rat Pack)`, p && p.next && want.test(d) && A.buttons().some(b => /« Rat Pack/.test(b.label)));
  }
  await A.press(/« Rat Pack/);
  ok('...« Rat Pack: back on the front page', A.buttons().some(b => /Collectors/.test(b.label)));

  // ---- one of each, on from the off hand
  // (the thing to put on is handed to him in his off hand - auto-pack never takes from there - and he uses the Pack)
  const putOn = async (loot, what) => { await run(`loot replace entity TestRat weapon.offhand loot bm:items/${loot}`); await sleep(300);
    A.chats.length = 0; A.slot(0); await sleep(250); A.use(); await sleep(350); A.release(); await sleep(700);
    return ok(`${what} goes on the Pack (off his hands, he is told)`, (await has(loot)) === 0 && A.chats.some(c => /goes on your Rat Pack/.test(c)), A.chats.slice(-1).join('')); };
  await putOn('particle_toggler', 'the Particle Toggler'); await putOn('fixers_ledger', 'the Fixer\'s Ledger'); await putOn('rat_king_key', 'the Rat King\'s Key');
  await putOn('charm_ember', 'an Ember Charm'); await putOn('sealed_explorer_map', 'a Sealed Explorer\'s Map'); await putOn('ember_call', 'an Ember Rat\'s Call');
  await sleep(1200);
  // Pocket: the toggler used from its row - as using it (its own menu); the Pack still in his hand after
  await openP(); await A.press(/Pocket/);
  ok('Pocket: the Particle Toggler and the Ledger listed', A.buttons().some(b => /Particle Toggler/.test(b.label)) && A.buttons().some(b => /Fixer's Ledger/.test(b.label)));
  const tp = await A.press(/Particle Toggler/);
  ok('...the Toggler pressed: its own menu opens (as using it), it stays on the Pack, the Pack back in his hand', tp && tp.next && !A.buttons().some(b => /« Rat Pack/.test(b.label)) &&
     (await sc('bm.rq_particle_toggler')) === 1 && /partner_wheel/.test(await run('data get entity TestRat SelectedItem')), A.buttons().map(b => b.label).join(' | ').slice(0, 160));
  ok('the Ledger on the Pack counts as carried (bm.rqt_fixers_ledger, the Office\'s "has a Ledger")', /returned 1/.test(await run('execute as TestRat run function bm:p80/can')));
  // Keyring: counts as carried at the market's gate; taken back once
  ok('Keyring: the Rat King\'s Key counts as carried at the market gate (the den\'s)', /returned 1/.test(await run('execute as TestRat run function bm:p28/gate/has_den_in')));
  await openP(); await A.press(/Keyring/);
  await A.press(/Rat King's Key/); await sleep(900);
  ok('...pressed: the key is back in his pocket, off the Pack', (await has('rat_king_key')) === 1 && (await sc('bm.rq_rat_king_key')) === 0);
  A.cmd('trigger bm.act set ' + (8700 + 17 + 3)); await sleep(700);
  ok('...and only once (still one key)', (await has('rat_king_key')) === 1);
  // Charms: active, then resting; taken back
  ok('Charms: the Ember Charm active while carried (bm.rqt_charm_ember)', /passed/i.test(await run('execute if entity @a[name=TestRat,tag=bm.rqt_charm_ember]')));
  await openP(); await A.press(/Charms/);
  ok('...listed with ● (active)', A.buttons().some(b => /●.*Ember Charm/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  await A.press(/Ember Charm/);
  ok('...pressed: ○ resting, its effect off', A.buttons().some(b => /○.*Ember Charm/.test(b.label)) && !/passed/i.test(await run('execute if entity @a[name=TestRat,tag=bm.rqt_charm_ember]')));
  await A.press(/Press to:/);
  ok('...the page switched to "Take back"', A.buttons().some(b => /Press to: Take back/.test(b.label)));
  await A.press(/Ember Charm/); await sleep(900);
  ok('...pressed: the charm back in his pocket', (await has('charm_ember')) === 1 && (await sc('bm.rq_charm_ember')) === 0);
  // Maps: listed, taken back
  await openP(); await A.press(/Maps/);
  ok('Maps: the Sealed Explorer\'s Map listed', A.buttons().some(b => /Explorer's Map/.test(b.label)));
  await A.press(/Press to:/); await A.press(/Explorer's Map/); await sleep(900);
  ok('...taken back', (await has('sealed_explorer_map')) === 1 && (await sc('bm.rq_sealed_explorer_map')) === 0);
  // Mounts: used (as blowing it - not in the Nether: it stays), taken back
  await openP(); await A.press(/Mounts/); A.bars.length = 0;
  await A.press(/Ember Rat's Call/); await sleep(800);
  ok('Mounts: the call used from its row - as blowing it ("Blow it in the Nether"), still on the Pack', A.bars.some(b => /Nether/.test(b)) && (await sc('bm.rq_ember_call')) === 1, A.bars.slice(-1).join(''));
  await openP(); await A.press(/Mounts/); await A.press(/Press to:/); await A.press(/Ember Rat's Call/); await sleep(900);
  ok('...taken back', (await has('ember_call')) === 1);
  // the Toggler and the Ledger taken back (Pocket, Take back)
  await openP(); await A.press(/Pocket/); await A.press(/Press to:/); await A.press(/Particle Toggler/); await sleep(900);
  ok('Pocket: the Toggler taken back once', (await has('particle_toggler')) === 1 && (await sc('bm.rq_particle_toggler')) === 0);

  // ---- auto-pack: a key in his inventory goes on by itself, chat says so
  await openP(); await A.press(/Settings/);
  ok('Settings: "Keys: on" (auto-pack, on by default)', A.buttons().some(b => /^Keys: on/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
  A.chats.length = 0; await run('loot give TestRat loot bm:items/vkey_brood');
  ok('...a Nest Key given to him: pulled onto the Pack within a second or two, with its chat line', await wait(3500, async () => (await has('vkey_brood')) === 0 && (await sc('bm.rq_vkey_brood')) === 1) &&
     A.chats.some(c => /Nest Key is on your Rat Pack now \(Keyring page\)/.test(c)), A.chats.slice(-2).join(' | '));
  await openP(); await A.press(/Settings/); await A.press(/^Keys:/);
  ok('...switched off: "Keys: off"', A.buttons().some(b => /^Keys: off/.test(b.label)));
  await sleep(1500);
  await run('loot give TestRat loot bm:items/vkey_frost'); await sleep(2200);
  ok('...and a Rime Key given now stays in his pocket', (await has('vkey_frost')) === 1);
  await A.press(/^Keys:/);

  // ---- bags: two Backpacks, each its own load
  const load = (slot, items) => run(`item modify entity TestRat ${slot} {type:"minecraft:set_components",components:{"minecraft:container":[${items.map(([id, n], i) => `{slot:${i},item:{id:"minecraft:${id}",count:${n}}}`).join(',')}]}}`);
  await run('loot replace entity TestRat hotbar.1 loot bm:items/backpack'); await load('hotbar.1', [['iron_ingot', 32], ['coal', 12], ['apple', 3]]);
  A.slot(1); await sleep(250); A.swap(); await sleep(400); A.slot(0); await sleep(250); A.use(); await sleep(350); A.release(); await sleep(700);
  await run('loot replace entity TestRat hotbar.1 loot bm:items/backpack'); await load('hotbar.1', [['diamond', 5]]);
  A.slot(1); await sleep(250); A.swap(); await sleep(400); A.slot(0); await sleep(250); A.use(); await sleep(350); A.release(); await sleep(700);
  ok('two Backpacks on the Pack (bm.rb_bp 2), neither in his hands', (await sc('bm.rb_bp')) === 2 && (await has('backpack')) === 0);
  await openP(); await A.press(/Bags/);
  const rows = A.buttons().filter(b => /Backpack/.test(b.label)).map(b => b.label);
  ok('Bags: "Backpack 1  3/27  Iron Ingot ×32, Coal ×12…" and "Backpack 2  1/27  Diamond ×5"', rows.length === 2 && /Backpack 1\s+3\/27.*iron_ingot.*×32.*coal.*×12/.test(rows[0]) && /Backpack 2\s+1\/27.*diamond.*×5/.test(rows[1]), rows.join(' | '));
  const barrel = () => run(`execute positioned ${X + 0.5} ${Y} ${Z + 0.5} as @e[type=minecraft:marker,tag=bm.bxm,distance=..4,limit=1] at @s run data get block ~ ~ ~ Items`);
  for (const [n, want, other] of [[1, /iron_ingot/, /diamond/], [2, /diamond/, /iron_ingot/]]) {
    await openP(); await A.press(/Bags/); await A.press(new RegExp(`Backpack ${n}\\b`));
    const d = A.dialogs[A.dialogs.length - 1] || '';
    ok(`Backpack ${n}: a look inside - its stacks as item icons with their counts, Unfold, Take it back`, want.test(d) && !other.test(d) && /minecraft:item/.test(d) &&
       A.buttons().some(b => /Unfold/.test(b.label)) && A.buttons().some(b => /Take it back/.test(b.label)));
    await A.press(/Unfold/); await sleep(900);
    const it = await barrel();
    ok(`...Unfold: a barrel in front of him holding Backpack ${n}'s own load`, want.test(it) && !other.test(it), it.slice(0, 120));
    await A.walkTo(X + 0.5, Z - 7.5); await sleep(1800);
    ok(`...walked away: it folds back onto the Pack (no barrel, its load kept)`, !/iron_ingot|diamond/.test(await barrel()) &&
       want.test(await run(`data get storage bm:pw p${pid}.rb_bp[${n - 1}].it.components."minecraft:container"`)) && !/out/.test(await run(`data get storage bm:pw p${pid}.rb_bp[${n - 1}]`)));
    await A.walkTo(X + 0.5, Z + 0.5); await sleep(400);
  }
  await openP(); await A.press(/Bags/); await A.press(/Backpack 2\b/); await A.press(/Take it back/); await sleep(1000);
  ok('Backpack 2 taken back: in his pocket with its diamonds, one left on the Pack', (await has('backpack')) === 1 && (await sc('bm.rb_bp')) === 1 &&
     /diamond/.test(await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"backpack"}}}].components."minecraft:container"')));
  // a Vacuum Satchel: its own switch, on - it collects from the Pack
  await run('loot replace entity TestRat hotbar.1 loot bm:items/vacuum_satchel');
  A.slot(1); await sleep(250); A.swap(); await sleep(400); A.slot(0); await sleep(250); A.use(); await sleep(350); A.release(); await sleep(700);
  await openP(); await A.press(/Bags/); await A.press(/Vacuum Satchel 1/);
  ok('a Vacuum Satchel on the Pack: its page says "Vacuum: off"', A.buttons().some(b => /^Vacuum: off/.test(b.label)));
  await A.press(/^Vacuum:/);
  ok('...pressed: "Vacuum: on"', A.buttons().some(b => /^Vacuum: on/.test(b.label)));
  await run(`summon minecraft:item ${X + 2.5} ${Y + 0.5} ${Z + 3.5} {Item:{id:"minecraft:emerald",count:7},PickupDelay:0s}`);
  ok('...an Emerald dropped near him flies into the satchel on the Pack', await wait(3000, async () => /emerald/.test(await run(`data get storage bm:pw p${pid}.rb_vs[0].it.components."minecraft:container"`))) &&
     (await has('emerald')) === 0 && (await num('clear TestRat minecraft:emerald 0')) <= 0);
  // a Spirit Jar: Deposit, Withdraw all
  await run('loot replace entity TestRat hotbar.1 loot bm:items/spirit_jar');
  A.slot(1); await sleep(250); A.swap(); await sleep(400); A.slot(0); await sleep(250); A.use(); await sleep(350); A.release(); await sleep(700);
  await run('give TestRat minecraft:rotten_flesh 10');
  await openP(); await A.press(/Collectors/); await A.press(/Spirit Jar 1/);
  ok('a Spirit Jar on the Pack: Auto-collect, Deposit, Withdraw a stack, Withdraw all', ['Auto-collect', 'Deposit', 'Withdraw a stack', 'Withdraw all'].every(n => A.buttons().some(b => b.label.includes(n))));
  await A.press(/Deposit/); await sleep(500);
  ok('...Deposit: his Rotten Flesh goes into it', (await num('clear TestRat minecraft:rotten_flesh 0')) <= 0 &&
     /rotten_flesh/.test(await run(`data get storage bm:pw p${pid}.rb_sj[0].it.components."minecraft:container"`)));
  await A.press(/Withdraw all/); await sleep(1200);
  ok('...Withdraw all: back in his pocket, the jar empty', (await num('clear TestRat minecraft:rotten_flesh 0')) === 10 &&
     !/rotten_flesh/.test(await run(`data get storage bm:pw p${pid}.rb_sj[0].it.components."minecraft:container"`)));

  // ---- the heist: the Pack at the coat check, a Heist Ledger in, dropped - back, gone on leaving
  const HL = '*[minecraft:custom_data~{bm:"fixers_ledger",bm_hl:1b}]';
  const hl = async () => Math.max(0, await num(`clear TestRat ${HL} 0`));
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/plan_anywhere'); await run('function bm:admin/heist_variants_never'); await run('function bm:admin/rooms_only_levers'); await run('function bm:admin/variant_a');
  await run('clear TestRat'); await run('tag TestRat remove bm.gvzap'); await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players set TestRat bm.gvhc 0');
  await run('execute in minecraft:overworld run fill 12996 119 12996 13004 119 13004 stone'); await run('execute in minecraft:overworld run fill 12996 120 12996 13004 123 13004 air');
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5 0 0'); await sleep(2500);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/partner_wheel');
  for (let i = 0; i < 8; i++) await run('loot give TestRat loot bm:items/token');
  await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players set TestRat bm.gval 1');
  await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7601'); await run('execute as TestRat at @s run function bm:p70/pick_tier');
  await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives');
  ok('into the heist', await wait(12000, async () => /bm\.gvp/.test(await run('data get entity TestRat Tags'))));
  await sleep(1500);
  ok('...the Rat Pack stayed at the coat check', (await has('partner_wheel')) === 0);
  ok('...a Heist Ledger handed to him on the way in', (await hl()) === 1);
  const slot = +(((await run(`data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm_hl:1b}}}].Slot`)).match(/: (\d+)b/) || [0, -1])[1]);
  if (slot >= 0 && slot < 9) { A.slot(slot); await sleep(300); A.drop(true); }
  else await run(`execute at TestRat run summon minecraft:item ~ ~0.3 ~ {Item:{id:"minecraft:stone",count:1},PickupDelay:40s,Tags:["t402"]}`);
  await sleep(300);
  ok('...dropped: no Heist Ledger left lying about, and one back in his pocket', await wait(3000, async () => (await hl()) === 1 &&
     !/Found|passed/.test(await run(`execute at TestRat if entity @e[type=minecraft:item,distance=..8,nbt={Item:{components:{"minecraft:custom_data":{bm_hl:1b}}}}]`))), `slot ${slot}`);
  await run('execute as TestRat at @s run function bm:p70/leave');
  ok('left the heist: the Heist Ledger gone, his Rat Pack back', await wait(9000, async () => (await hl()) === 0 && (await has('partner_wheel')) === 1), `${await hl()} ledgers`);
  await sleep(1500);
  ok('...and it stays gone', (await hl()) === 0);

  // ---- tidy: the stage put back
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/rooms_any');
  await run('clear TestRat');
  for (const k of ['bp', 'vs', 'sj']) { await run(`scoreboard players set TestRat bm.rb_${k} 0`); await run(`data remove storage bm:pw p${pid}.rb_${k}`); }
  await run('scoreboard players set TestRat bm.rq_vkey_brood 0'); await run(`data remove storage bm:pw p${pid}.rq_vkey_brood`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

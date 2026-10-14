const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const fs = require('fs');
const X = 16000, Y = 100, Z = 16000; const res = [];
(async () => {
  const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500); const Bt = await bot('TestRat2'); await sleep(3000);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const uuid = async (p = 'TestRat') => (await run(`data get entity ${p} UUID`)).replace(/^.*data: /, '').trim();
  const click = async (sel, p = 'TestRat') => { await sleep(600); return run(`data modify entity ${sel} interaction set value {player:${await uuid(p)},timestamp:1L}`); };
  const has = async (slot, pred, p = 'TestRat') => /passed/.test(await run(`execute if items entity ${p} ${slot} ${pred}`));
  const pos = async (p) => (await run(`data get entity ${p} Pos`)).match(/\[([-\d.]+)d, ([-\d.]+)d, ([-\d.]+)d\]/).slice(1).map(Number);
  for (const p of ['TestRat', 'TestRat2']) { await run(`execute in minecraft:overworld run tp ${p} ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await run(`clear ${p}`); await run(`gamemode survival ${p}`);
    await run(`effect give ${p} resistance 900 4 true`); await run(`execute as ${p} unless score @s bm.pid matches 1.. run function bm:p21/pid`); }
  await sleep(3500);
  await run(`fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} stone`); await run(`fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..30]`);

  // ---------------------------------------------------------------- a bottled cow in a floor case, a bottled chicken in a wall case
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 70`); await sleep(300);
  await run('loot give TestRat loot bm:items/display_case_oak'); await run('loot give TestRat loot bm:items/display_case_gilded');
  await run('execute as TestRat at @s run function bm:p72/dc/place_oak'); await sleep(200);
  const fl = `@e[type=interaction,tag=bm.dchit,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..1.2,limit=1]`;
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/smuggler_jar');
  await run('item replace entity TestRat weapon.mainhand with minecraft:totem_of_undying[minecraft:custom_data={bm:"smuggler_jar",bmv:33,jar:{eid:"minecraft:cow",name:"Bessie",data:{Health:9f,CustomName:"Bessie"}}}]');
  await click(fl); await sleep(400);
  const cow = '@e[type=cow,tag=bm.dcmob,limit=1]';
  ok('A bottled cow goes in a floor case: she appears on the cushion', (await cnt('@e[type=cow,tag=bm.dcmob]')) === 1 && /Bessie/.test(await run(`data get entity ${cow} CustomName`)));
  const scl = await run(`attribute ${cow} minecraft:scale get`);
  ok('...shrunk to fit', /0\.4/.test(scl), scl);
  ok('...no AI, can\'t be hurt', /1b/.test(await run(`data get entity ${cow} NoAI`)) && /1b/.test(await run(`data get entity ${cow} Invulnerable`)));
  ok('...sat on a seat (can\'t be pushed out)', /passed/.test(await run(`execute as ${cow} on vehicle if entity @s[type=block_display,tag=bm.dcseat]`)));
  ok('...and the jar itself is hidden', /0\.0f, 0\.0f, 0\.0f/.test(await run(`data get entity @e[type=item_display,tag=bm.dcitem,limit=1,sort=nearest,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5}] transformation.scale`)));
  await run(`tag @e[type=item_display,tag=bm.dcitem,limit=1,sort=nearest,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5}] add bm.dcsel`); await run(`tag ${fl} add bm.dcme`);
  await run('execute as TestRat at @s run function bm:p72/dc/spin_toggle'); await run('tag @e remove bm.dcsel'); await run('tag @e remove bm.dcme');
  const y0 = await run(`data get entity ${cow} Rotation[0]`); await sleep(600); const y1 = await run(`data get entity ${cow} Rotation[0]`);
  ok('Sneak + right-click: she turns', y0 !== y1, `${y0.slice(-10)} -> ${y1.slice(-10)}`);
  await run('item replace entity TestRat weapon.mainhand with minecraft:air'); await click(fl); await sleep(400);
  ok('Take the jar back out: the cow is back in it, unharmed', (await cnt('@e[type=cow,tag=bm.dcmob]')) === 0 && (await cnt('@e[type=block_display,tag=bm.dcseat]')) === 0 &&
     /Bessie/.test(await run('data get entity TestRat SelectedItem.components."minecraft:custom_data".jar')));
  ok('...and no cow was dropped (no leather, no beef)', (await cnt(`@e[type=item,x=${X},y=${Y},z=${Z},distance=..10]`)) === 0);
  await run(`setblock ${X + 3} ${Y + 2} ${Z + 4} stone`); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 4.5} -90 5`); await sleep(300);
  await run('execute as TestRat at @s run function bm:p72/dc/place_gilded'); await sleep(200);
  const wl = `@e[type=interaction,tag=bm.dchit,x=${X + 2.75},y=${Y + 2.1},z=${Z + 4.5},distance=..0.4,limit=1]`;
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/smuggler_jar');
  await run('item replace entity TestRat weapon.mainhand with minecraft:totem_of_undying[minecraft:custom_data={bm:"smuggler_jar",bmv:33,jar:{eid:"minecraft:chicken",name:"Chicken",data:{}}}]');
  await click(wl); await sleep(400);
  const chs = await run('attribute @e[type=chicken,tag=bm.dcmob,limit=1] minecraft:scale get');
  ok('A bottled chicken in a wall case: it fits the shallow case', (await cnt('@e[type=chicken,tag=bm.dcmob]')) === 1 && /0\.7/.test(chs), chs);
  await run(`tag ${wl} add bm.dcme`); await run('execute as TestRat at @s run function bm:p72/dc/pick'); await run('tag @e remove bm.dcme'); await sleep(500);
  ok('Pick the case up: the chicken goes back in its jar (the jar drops out)', (await cnt('@e[type=chicken,tag=bm.dcmob]')) === 0 &&
     /chicken/.test(await run(`data get entity @e[type=item,limit=1,sort=nearest,x=${X + 2.5},y=${Y + 2},z=${Z + 4.5}] Item.components."minecraft:custom_data".jar`)));
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..30]`); await run('clear TestRat');

  // ---------------------------------------------------------------- Cecil: a click box the size of him
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await run('kill @e[type=wolf,tag=bm.cecilpet]'); await run('scoreboard players reset TestRat bm.cpcd');
  await run('scoreboard players reset TestRat bm.cpel'); await run('loot replace entity TestRat inventory.20 loot bm:items/cecil_gem');   // (kept out of the hand: swapping the hand item would send him home)
  await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(1500);
  const cw = '@e[type=wolf,tag=bm.cecilpet,limit=1]', ch = '@e[type=interaction,tag=bm.cphit,limit=1]';
  ok('Cecil has a click box over his whole body (riding his host)', /passed/.test(await run(`execute as ${ch} on vehicle if entity @s[tag=bm.cecilpet]`)));
  await click(ch); await sleep(300);
  ok('Right-click him: he sits', /1b/.test(await run(`data get entity ${cw} Sitting`)));
  await click(ch); await sleep(300);
  ok('...again: he follows', /0b/.test(await run(`data get entity ${cw} Sitting`)));
  await click(ch); await sleep(300);
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/gem_fire'); await click(ch); await sleep(300);
  ok('A Fire Gem through the same click: he turns to fire (gem used up)', (await sc(cw, 'bm.cpel')) === 3 || (await sc('TestRat', 'bm.cpel')) >= 1,
     `cpel ${await sc(cw, 'bm.cpel')} / owner ${await sc('TestRat', 'bm.cpel')}`);
  ok('...and stands up to take it', /0b/.test(await run(`data get entity ${cw} Sitting`)));
  await run('item replace entity TestRat weapon.mainhand with minecraft:beef 5'); await click(ch); await sleep(300);
  ok('Fire Cecil + raw beef: the whole stack comes out cooked', await has('weapon.mainhand', 'minecraft:cooked_beef[count=5]'), await run('data get entity TestRat SelectedItem'));
  await run('item replace entity TestRat weapon.mainhand with minecraft:cod 2'); await click(ch); await sleep(300);
  ok('...raw cod too', await has('weapon.mainhand', 'minecraft:cooked_cod[count=2]'));
  await run('item replace entity TestRat weapon.mainhand with minecraft:air'); await A.input({ shift: true }); await sleep(300); await click(ch); await sleep(300); A.input({}); await sleep(200);
  ok('Sneak + empty hand through the click box: the gem comes back', await has('container.*', '*[custom_data~{bm:"gem_fire"}]') && (await sc('TestRat', 'bm.cpel')) === 0);
  await run('execute as TestRat at @s run function bm:p46/pet/dismiss'); await run('kill @e[type=wolf,tag=bm.cecilpet]'); await sleep(2600);
  ok('...and his click box goes when he does', (await cnt('@e[type=interaction,tag=bm.cphit]')) === 0);

  // ---------------------------------------------------------------- Emma: her own blue by default
  await run('kill @e[type=cat,tag=bm.emmapet]'); await run('execute as TestRat at @s run function bm:p57/summon_here'); await sleep(800);
  ok('Emma, newly called: her own blue dress (Healing)', /"bm:em_body"/.test(await run('data get entity @e[type=item_display,tag=bm.ep_body,limit=1] item.components')),
     await run('data get entity @e[type=item_display,tag=bm.ep_body,limit=1] item.components'));
  await run('execute as @e[type=cat,tag=bm.emmapet] at @s run function bm:p62/emma_go'); await sleep(500);

  // ---------------------------------------------------------------- followers go home
  await run('clear TestRat'); await run('loot give TestRat loot bm:items/celi_charm'); await run('scoreboard players reset TestRat bm.cecd'); await run('kill @e[type=wolf,tag=bm.celipet]');
  await run('execute as TestRat at @s run function bm:p66/summon_here'); await sleep(1500);
  ok('Celi called (charm in hand)', (await cnt('@e[type=wolf,tag=bm.celipet]')) === 1);
  await sleep(4000);
  ok('...she stays while you carry the charm', (await cnt('@e[type=wolf,tag=bm.celipet]')) === 1);
  await run('clear TestRat'); await sleep(4500);
  ok('Put the charm away (in a chest): she heads home', (await cnt('@e[type=wolf,tag=bm.celipet]')) === 0 && A.chats.some(c => /put the .*Charm away/.test(c)), A.chats.slice(-1)[0]);
  await run('loot give TestRat loot bm:items/celi_charm'); await run('execute as TestRat at @s run function bm:p66/summon_here'); await sleep(1000);
  // a copy left behind (frozen in some far chunk) while you called her again elsewhere: when it wakes, it dismisses itself
  await run('execute as @e[type=wolf,tag=bm.celipet] run tag @s add bm.t73old'); await run('scoreboard players add TestRat bm.fgl 1'); await sleep(2500);
  ok('A stale copy (you called her again since) dismisses itself - never a double', (await cnt('@e[type=wolf,tag=bm.t73old]')) === 0);
  await run('execute as TestRat at @s run function bm:p66/use'); await sleep(1500);
  ok('...and the charm calls a fresh one', (await cnt('@e[type=wolf,tag=bm.celipet]')) === 1);
  await run(`tp TestRat ${X + 3000.5} ${Y + 1} ${Z + 0.5}`); await sleep(1500); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(1500);
  ok('A long teleport: she follows you or goes home - one Celi at most', (await cnt('@e[type=wolf,tag=bm.celipet]')) <= 1);
  await run('kill @e[type=wolf,tag=bm.celipet]'); await run('kill @e[type=item_display,tag=bm.cep]');

  // ---------------------------------------------------------------- the Fixer's Calling Card
  const p2 = await sc('TestRat2', 'bm.pid');
  await run('clear TestRat'); await run('loot give TestRat loot bm:items/fixers_card');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await run(`execute in minecraft:overworld run tp TestRat2 ${X + 600.5} ${Y + 1} ${Z + 0.5}`); await sleep(3000);
  await run(`fill ${X + 597} ${Y} ${Z - 3} ${X + 603} ${Y} ${Z + 3} stone`);
  await run('execute as TestRat at @s run function bm:p73/tp/use'); await sleep(300);
  const acts = await run('data get storage bm:tp acts');
  ok('The Calling Card lists the other players (go to / bring)', /TestRat2/.test(acts) && /Go to/.test(acts) && /Bring/.test(acts), acts.slice(0, 200));
  A.cmd(`trigger bm.act set ${8000000 + p2}`); await sleep(800);
  ok('"Go to": they get a request with [Accept] / [Deny]', Bt.chats.some(c => /wants to teleport to you/.test(c)) && (await sc('TestRat2', 'bm.tpt')) > 0, Bt.chats.slice(-1)[0]);
  Bt.cmd('trigger bm.act set 7711'); await sleep(1500);
  let a = await pos('TestRat'), b = await pos('TestRat2');
  ok('...they accept: you\'re teleported to them (600 blocks)', Math.hypot(a[0] - b[0], a[2] - b[2]) < 3, `${a} / ${b}`);
  await run(`execute in minecraft:the_nether run tp TestRat2 0.5 120 0.5`); await run('execute in minecraft:the_nether run fill -2 119 -2 2 119 2 obsidian'); await sleep(3000);
  await run('execute as TestRat at @s run function bm:p73/tp/use'); await sleep(300); A.cmd(`trigger bm.act set ${9000000 + p2}`); await sleep(800);
  ok('"Bring": across dimensions too', Bt.chats.some(c => /asks you to teleport to them/.test(c)));
  Bt.cmd('trigger bm.act set 7711'); await sleep(2000);
  a = await pos('TestRat'); b = await pos('TestRat2');
  ok('...accepted: they arrive (from the Nether)', /passed/.test(await run('execute as TestRat2 at @s if dimension minecraft:overworld')) && Math.hypot(a[0] - b[0], a[2] - b[2]) < 3, `${a} / ${b}`);
  await run('execute as TestRat at @s run function bm:p73/tp/use'); await sleep(300); A.cmd(`trigger bm.act set ${8000000 + p2}`); await sleep(800);
  Bt.cmd('trigger bm.act set 7712'); await sleep(800);
  ok('...or they decline', A.chats.some(c => /declined/.test(c)));
  A.cmd(`trigger bm.act set ${8000000 + p2}`); await sleep(600);
  ok('A stale button (menu closed) does nothing', (await sc('TestRat2', 'bm.tpt')) === 0);

  // ---------------------------------------------------------------- the crypt: an old one, rebuilt with wide tunnels (turned once)
  const G1 = [X + 200, 160, Z + 200], G2 = [X + 400, 160, Z + 200];
  for (const g of [G1, G2]) await run(`forceload add ${g[0] - 80} ${g[2] - 20} ${g[0] + 20} ${g[2] + 80}`);
  await run(`tp TestRat ${G1[0] - 30} 220 ${G1[2] + 15}`); await sleep(4000);
  for (const g of [G1, G2]) console.log(await run(`place template bm:graveyard ${g.join(' ')} clockwise_90`));
  await sleep(1500);
  const mk = (g) => `@e[type=marker,tag=bm.crypt_ctrl,x=${g[0] - 32},y=${g[1]},z=${g[2] + 15},distance=..40,limit=1]`;
  console.log(await run(`data get entity ${mk(G1)} Rotation`));
  const rev = JSON.parse(fs.readFileSync('crypt_rev.json', 'utf8'))['1'];
  for (const c of rev) await run(`execute as ${mk(G1)} at @s rotated as @s run ${c}`);
  const air = JSON.parse(fs.readFileSync('crypt_air.json', 'utf8'));
  const mism = async (g) => { let n = 0; for (const [tx, ty, tz, a] of air) { const r = /passed/.test(await run(`execute if block ${g[0] - tz} ${g[1] + ty} ${g[2] + tx} minecraft:air`)); if (r !== a) n++; } return n; };
  const before = await mism(G1);
  ok('(an old, narrow crypt to start from)', before > 100, `${before} cells differ from a new crypt`);
  await run(`tag ${mk(G1)} remove bm.cr62`); await run(`scoreboard players set ${mk(G1)} bm.state 0`);
  await run(`execute as ${mk(G1)} at @s rotated as @s function bm:p73/crypt_fix`.replace('rotated as @s function', 'rotated as @s run function')); await sleep(500);
  const after = await mism(G1);
  ok('An old crypt (built turned) is rebuilt: its tunnels match a new crypt exactly (3 wide)', after === 0, `${after} cells still differ`);
  ok('...and a new crypt is already wide (3 open blocks across a corridor)', (await mism(G2)) === 0);
  ok('...and its signs glow', /1b/.test(await run(`execute as ${mk(G1)} at @s rotated as @s positioned ^ ^2.5 ^-12 run data get block ~ ~ ~ front_text.has_glowing_text`)));
  for (const g of [G1, G2]) await run(`forceload remove ${g[0] - 80} ${g[2] - 20} ${g[0] + 20} ${g[2] + 80}`);

  // ---------------------------------------------------------------- one Dockmaster; Pearlman's model; crash-site altars; the Fence
  await run('tp TestRat 9500 110 9530'); await sleep(7000);
  await run('execute at @e[type=villager,tag=bm.npc_dock,limit=1,sort=nearest,x=9500,y=101,z=9500] run summon minecraft:villager ~ ~ ~ {NoAI:1b,Tags:["bm.npc","bm.npc_dock"]}');
  await sleep(2500);
  ok('A second Dockmaster in a market is removed (one stays)', (await cnt('@e[type=villager,tag=bm.npc_dock,x=9500,y=101,z=9500,distance=..100]')) === 1);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(2500);
  await run(`execute positioned ${X + 3.5} ${Y + 1} ${Z + 3.5} run function bm:p60/pm/spawn`); await sleep(300);
  await run('execute as @e[type=villager,tag=bm.pearl] run tp @s ~ -400 ~'); await run('kill @e[type=villager,tag=bm.pearl]'); await sleep(2000);
  ok('Pearlman gone (however he goes): his model goes too', (await cnt('@e[type=item_display,tag=bm.pearld]')) === 0);
  await run(`summon minecraft:marker ${X + 2.5} ${Y + 1} ${Z + 2.5} {Tags:["bm.npc_spawn","bm.npc.xaltar"]}`); await sleep(1500);
  A.input({ shift: true }); await sleep(300);
  await run(`data modify entity @e[type=interaction,tag=bm.xalt_hit,limit=1] attack set value {player:${await uuid()},timestamp:1L}`); await sleep(500); A.input({});
  ok('A crash site\'s built-in Xenite Altar: sneak + punch picks it up', (await cnt('@e[type=interaction,tag=bm.xalt_hit]')) === 0 &&
     /xenite_altar/.test(await run(`data get entity @e[type=item,limit=1,sort=nearest,x=${X + 2.5},y=${Y + 1},z=${Z + 2.5}] Item.components."minecraft:custom_data"`)));
  const fence = fs.readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/npc/fence.mcfunction', 'utf8');
  ok('The Fence no longer buys emeralds', !/minecraft:emerald",count:24/.test(fence));
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..30]`); await run('clear TestRat'); await run('clear TestRat2');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

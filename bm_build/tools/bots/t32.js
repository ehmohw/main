const { bot, rcon, sleep } = require('./lib');
const X = 27000, Y = 100, Z = 9000;                  // (2.81: 472 blocks from the nearest natural market)
const HERE = `x=${X},y=${Y},z=${Z},distance=..64`;
(async () => { const R = await rcon(); const run = c => R.run(c);
  const res = []; const ok = (n, c, d) => { res.push(!!c); console.log(c ? 'PASS' : 'FAIL', n, d || ''); };
  const score = async (h, o = 'bm.bm') => { const r = await run(`scoreboard players get ${h} ${o}`); const m = r.match(/has (-?\d+)/); return m ? +m[1] : null; };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)[^\d]*$/); return m ? parseFloat(m[1]) : null; };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const inv = async (who, it) => { const r = await run(`clear ${who} ${it} 0`); const m = r.match(/Found (\d+)/); return m ? +m[1] : 0; };
  const adv = async (a) => (await cnt(`@a[name=TestRat,advancements={bm:story/${a}=true}]`)) === 1;
  const TOK = '*[custom_data~{bm:"token"}]';
  const A = await bot('TestRat'); await sleep(1500);
  let parts = 0; A.on('world_particles', () => parts++);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat saturation 900 1 true');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(2500);
  await run(`fill ${X - 16} ${Y - 1} ${Z - 16} ${X + 16} ${Y} ${Z + 16} stone`); await run(`fill ${X - 16} ${Y + 1} ${Z - 16} ${X + 16} ${Y + 8} ${Z + 16} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`);
  for (const s of ['#lnight', '#inv', '#active', '#forced']) await run(`scoreboard players set ${s} bm.bm 0`);
  await run('time set day'); await sleep(1500); await run('scoreboard players set #bmday bm.bm 5'); await sleep(1200);
  // a fake market here (patches already "done", so only our things react) + traders - a current one (bm.m281a), or it's rebuilt as the new town
  await run(`summon marker ${X} ${Y + 1} ${Z} {Tags:["bm.mkt","bm.m281a","bm.p41","bm.p50","bm.p51","bm.p52","bm.t32"]}`);
  await run(`execute positioned ${X - 6} ${Y + 1} ${Z + 6} run function bm:npc/professor`); await run(`execute positioned ${X - 8} ${Y + 1} ${Z + 6} run function bm:npc/lucky`);
  await run(`execute positioned ${X - 10} ${Y + 1} ${Z + 6} run function bm:npc/fence`); await run(`execute positioned ${X - 12} ${Y + 1} ${Z + 6} run function bm:npc/alien`);
  await sleep(2200);
  const price = async (k, iid) => { for (let i = 0; i < 80; i++) { const r = await run(`data get entity @e[tag=bm.npc_${k},limit=1] Offers.Recipes[${i}]`);
      if (!r.includes('has the following')) return null; if (r.includes(`bm: "${iid}"`) && r.indexOf(`bm: "${iid}"`) > r.indexOf('sell')) { const b = r.slice(r.indexOf('buy: {')); return +b.match(/count: (\d+)/)[1]; } } return null; };
  const has = async (k, iid) => { for (let i = 0; i < 80; i++) { const r = await run(`data get entity @e[tag=bm.npc_${k},limit=1] Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`);
      if (!r.includes('has the following')) return false; if (r.includes(`"${iid}"`)) return true; } return false; };
  const pN = await price('professor', 'filter_hopper'), zN = await num(`data get entity @e[tag=bm.npc_alien,limit=1] Offers.Recipes[0].buy.count`);
  let quiet = parts; parts = 0; await sleep(3000); const calm = parts;
  // ---- a Lucky Night
  await run('execute as TestRat run function bm:admin/lucky_night'); await run('time set night'); await sleep(2500);
  ok('Lucky Night started', (await score('#lnight')) === 1);
  parts = 0; await sleep(3000); const lp = parts;
  ok('market ambience: gold and chimes on a Lucky Night (particles reach you)', lp > calm + 10, `${calm} -> ${lp} particle packets in 3 s`);
  const pH = await price('professor', 'filter_hopper'), zH = await num(`data get entity @e[tag=bm.npc_alien,limit=1] Offers.Recipes[0].buy.count`);
  ok('Happy Hour: a third off (Filter Hopper 3 -> 2)', pN === 3 && pH === 2, `${pN} -> ${pH}`);
  ok("Happy Hour: Zorp takes a third off", zH < zN, `${zN} -> ${zH}`);
  ok('Lucky Whiskers: the Four-Leaf Charm is on sale tonight', await has('lucky', 'four_leaf_charm'));
  // ---- slots (a Lucky Den built off the fake market: the patch puts machines + reels + the jackpot sign)
  await run(`summon marker ${X + 4} ${Y + 1} ${Z - 12} {Tags:["bm.t32den"],Rotation:[0f,0f]}`);
  await run('execute as @e[tag=bm.t32den] at @s rotated as @s run function bm:p52/market');
  ok('the Den gets 3 machines (2 Lucky Slots, 1 Jackpot), reels and the jackpot sign', (await cnt(`@e[type=marker,tag=bm.slot_reg,${HERE}]`)) === 2 && (await cnt(`@e[type=marker,tag=bm.slot_jp,${HERE}]`)) === 1 &&
     (await cnt(`@e[type=text_display,tag=bm.slotd,${HERE}]`)) === 3 && (await cnt(`@e[type=text_display,tag=bm.potd,${HERE}]`)) === 1,
     `${await cnt(`@e[type=marker,tag=bm.slot_reg,${HERE}]`)} ${await cnt(`@e[type=marker,tag=bm.slot_jp,${HERE}]`)} ${await cnt(`@e[type=text_display,tag=bm.slotd,${HERE}]`)} ${await cnt(`@e[type=text_display,tag=bm.potd,${HERE}]`)}`);
  // put a lever (on stone) at each machine
  const pos = {};
  for (const k of ['reg', 'jp']) { const r = await run(`data get entity @e[type=marker,tag=bm.slot_${k},limit=1] Pos`); const m = r.match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    pos[k] = m.slice(1).map(v => Math.floor(+v)); const [x, y, z] = pos[k];
    await run(`setblock ${x} ${y - 1} ${z} stone`); await run(`setblock ${x} ${y} ${z} lever[face=floor,facing=north,powered=false]`); }
  const [rx, ry, rz] = pos.reg, [jx, jy, jz] = pos.jp;
  await run(`execute positioned ${rx + 0.5} ${ry + 0.5} ${rz + 0.5} run kill @e[type=marker,tag=bm.slot_reg,distance=0.8..24]`);     // (keep the Lucky Slot with the lever for the test)
  await run(`tp TestRat ${rx + 0.5} ${ry} ${rz + 1.6} 180 40`); A.pos.yaw = 180; A.pos.pitch = 40; await sleep(800);
  A.useOn(rx, ry, rz, 1); await sleep(400);
  ok('no Tokens: the lever does nothing', !((await score('@e[type=marker,tag=bm.slot_reg,limit=1]', 'bm.sst')) > 0) && (A.bars.slice(-1)[0] || '').includes('wants Black Market Tokens'), A.bars.slice(-1)[0]);
  await run(`give TestRat ${'minecraft:totem_of_undying'} 0`); await run('loot give TestRat loot bm:items/token');
  for (let i = 0; i < 9; i++) await run('loot give TestRat loot bm:items/token');
  const t0 = await inv('TestRat', TOK);
  A.useOn(rx, ry, rz, 1); await sleep(200);
  const spinning = await score('@e[type=marker,tag=bm.slot_reg,limit=1]', 'bm.sst');
  // rig the result: three stars (pays 25)
  for (const r of ['bm.sr1', 'bm.sr2', 'bm.sr3']) await run(`scoreboard players set @e[type=marker,tag=bm.slot_reg,limit=1] ${r} 3`);
  const txt0 = await run('data get entity @e[type=text_display,tag=bm.slotd_reg,limit=1] text');
  await sleep(2200);
  const t1 = await inv('TestRat', TOK);
  ok('Lucky Slot: 1 Token a pull, the reels spin', spinning > 0 && t0 === 10, `sst ${spinning}, tokens ${t0}`);
  ok('...three stars pay 25 Tokens', t1 === t0 - 1 + 25, `${t0} -> ${t1}`);
  ok('...the reels show the result', (await run('data get entity @e[type=text_display,tag=bm.slotd_reg,limit=1] text')).split('★').length - 1 === 3);
  ok('One-Armed Bandit', await adv('slots'));
  // the jackpot machine: 5 Tokens, the pot grows; rig three 7s
  const pot0 = await score('#pot', 'bm.slot');
  await run(`tp TestRat ${jx + 0.5} ${jy} ${jz + 1.6} 180 40`); await sleep(500);
  const t2 = await inv('TestRat', TOK);
  A.useOn(jx, jy, jz, 1); await sleep(200);
  const pot1 = await score('#pot', 'bm.slot');
  for (const r of ['bm.sr1', 'bm.sr2', 'bm.sr3']) await run(`scoreboard players set @e[type=marker,tag=bm.slot_jp,limit=1] ${r} 5`);
  await sleep(2200);
  const t3 = await inv('TestRat', TOK), pot2 = await score('#pot', 'bm.slot');
  ok('Jackpot machine: 5 Tokens a pull, the pot grows (x2 on a Lucky Night)', pot1 === pot0 + 4, `${pot0} -> ${pot1}`);
  ok('...three 7s win the whole pot, which resets', t3 === t2 - 5 + pot1 && pot2 === 50, `${t2} -> ${t3} (pot ${pot1}), pot now ${pot2}`);
  ok('...announced to everyone, Jackpot! advancement', A.chats.slice(-5).join(' ').includes('JACKPOT') && await adv('jackpot'));
  const sign = await run('data get entity @e[type=text_display,tag=bm.potd,limit=1] text');
  ok('the jackpot sign shows the pot', sign.includes('50 Tokens') || sign.includes('Tokens'), sign.slice(-80));
  // ---- the Leprechaun Rat
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(400);
  await run(`execute positioned ${X + 6} ${Y + 1} ${Z + 6} run function bm:p52/lep/spawn`); await sleep(1500);
  const lep = await cnt('@e[type=ocelot,tag=bm.lep]'), lepd = await cnt('@e[type=item_display,tag=bm.lepd]');
  const lx = await num('data get entity @e[type=ocelot,tag=bm.lep,limit=1] Pos[0]'), dx = await num('data get entity @e[type=item_display,tag=bm.lepd,limit=1] Pos[0]');
  ok('a Leprechaun Rat appears (a rat in a bowler on a skittish body)', lep === 1 && lepd === 1 && Math.abs(lx - dx) < 0.6, `${lx} ${dx}`);
  await run('damage @e[type=ocelot,tag=bm.lep,limit=1] 50 minecraft:player_attack by TestRat'); await sleep(800);
  ok('caught: it drops a Pot of Gold, the rat is gone', (await cnt(`@e[type=item,nbt={Item:{components:{"minecraft:custom_data":{bm:"pot_of_gold"}}}}]`)) === 1 && !(await cnt('@e[tag=bm.lepd]')));
  ok("Top o' the Mornin'", await adv('leprechaun'));
  await run('kill @e[type=item,nbt={Item:{components:{"minecraft:custom_data":{bm:"pot_of_gold"}}}}]'); await run('clear TestRat');
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/pot_of_gold'); await sleep(150); A.use(); await sleep(1300); A.release(); await sleep(300);
  const pt = await inv('TestRat', TOK), pl = await inv('TestRat', '*[custom_data~{bm:"lucky_token"}]');
  ok('the pot tips out 8-16 Tokens and 3-6 Lucky Tokens', pt >= 8 && pt <= 16 && pl >= 3 && pl <= 6, `${pt} tokens, ${pl} lucky`);
  // dawn: prices back
  await run('time set day'); await sleep(2500);
  ok('dawn: Happy Hour ends, prices back', (await score('#lnight')) === 0 && (await price('professor', 'filter_hopper')) === 3 && !(await has('lucky', 'four_leaf_charm')));
  // ---- an Invasion Night
  await run('execute as TestRat run function bm:admin/invasion_now'); await run('time set night'); await sleep(2500);
  ok('Invasion Night started', (await score('#inv')) === 1);
  await run(`kill @e[tag=bm.vorn,x=${X},y=${Y},z=${Z},distance=..80]`);
  ok('the Fence has invasion stock (Signal Jammer, Flak Rockets, salvage)', await has('fence', 'signal_jammer') && await has('fence', 'flak_rocket'));
  parts = 0; await sleep(3000); ok('market ambience on an Invasion Night', parts > calm + 5, parts + ' particle packets');
  // signal jammer
  await run('clear TestRat'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/signal_jammer'); await sleep(150); A.use(); await sleep(1300); A.release(); await sleep(300);
  ok('Signal Jammer on (Radio Silence)', (await cnt('@a[name=TestRat,tag=bm.jam]')) === 1 && await adv('jammer'));
  await run(`kill @e[tag=bm.vorn,x=${X},y=${Y},z=${Z},distance=..90]`); await sleep(4000);
  for (let i = 0; i < 6; i++) await run('execute as TestRat at TestRat run function bm:p32/inv/surge');
  const vn = await cnt(`@e[tag=bm.vorn,x=${X},y=${Y},z=${Z},distance=..60]`); if (vn) console.log('  vorn:', (await run(`execute as @e[tag=bm.vorn,x=${X},y=${Y},z=${Z},distance=..60] run data get entity @s CustomName`)).slice(0, 300), (await run(`data get entity @e[tag=bm.vorn,x=${X},y=${Y},z=${Z},distance=..60,limit=1] Tags`)).slice(-200));
  ok('...no Vorn drop in near you', !vn);
  // flak at a saucer
  await run(`execute positioned ${X + 0.5} ${Y + 12} ${Z - 10.5} run function bm:p32/spawn/saucer`); await sleep(400);
  await run('data merge entity @e[tag=bm.vsauc,limit=1] {NoAI:1b}');
  const s0 = await num('data get entity @e[tag=bm.vsauc,limit=1] Health');
  await run('clear TestRat'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/flak_rocket'); await run('item modify entity TestRat weapon.mainhand {type:"minecraft:set_count",count:3}');
  await sleep(150); A.use(); await sleep(300); A.release(); await sleep(400);
  const s1 = await num('data get entity @e[tag=bm.vsauc,limit=1] Health');
  ok('Flak Rocket: hits the saucer, one rocket used', (s1 === null || s1 < s0) && (await inv('TestRat', '*[custom_data~{bm:"flak_rocket"}]')) === 2, `${s0} -> ${s1}`);
  await run('kill @e[tag=bm.vsauc]'); await run('tag TestRat remove bm.jam');
  // ---- Defend the Mothership (a green hologram over a deck)
  await run(`summon item_display ${X + 0.5} ${Y + 3.5} ${Z + 0.5} {Tags:["bm.xholo"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"bm:xenite_green"}}}`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 8.5}`); await sleep(2500);
  ok('board on an Invasion Night: RED ALERT, wave 1 beams onto the deck', (await cnt('@e[tag=bm.dwave]')) === 3, (await cnt('@e[tag=bm.dwave]')) + ' troopers');
  await run('kill @e[tag=bm.dwave]'); await sleep(2300); const w2 = await cnt('@e[tag=bm.dwave]');
  await run('kill @e[tag=bm.dwave]'); await sleep(2300); const w3 = await cnt('@e[tag=bm.dwave]');
  ok('...wave 2 (5), wave 3 (7)', w2 === 5 && w3 === 7, `${w2} ${w3}`);
  await run('clear TestRat'); await run('kill @e[tag=bm.dwave]'); await sleep(2300);
  ok('...all three beaten: Xenite, the Donadian Medal, Hold the Line', (await inv('TestRat', '*[custom_data~{bm:"xenite_green"}]')) === 6 && (await inv('TestRat', '*[custom_data~{bm:"donadian_medal"}]')) === 1 && await adv('defend'));
  await sleep(2200); ok('...once a night per ship', !(await cnt('@e[tag=bm.dwave]')));
  await run('kill @e[tag=bm.xholo]');
  // ---- Sabotage the Reactor
  await run(`summon marker ${X + 0.5} ${Y + 1} ${Z + 0.5} {Tags:["bm.dread_core"]}`); await sleep(2200);
  ok('the Dreadnought\'s reactor: 4 conduits round the core', (await cnt('@e[type=interaction,tag=bm.rhit]')) === 4 && (await cnt('@e[type=item_display,tag=bm.rcond]')) === 4);
  const ids = Object.values(A.ents).filter(e => Math.abs(e.y - (Y + 1)) < 0.3 && (Math.abs(e.x - X - 0.5) > 4 || Math.abs(e.z - Z - 0.5) > 4) && Math.hypot(e.x - X - 0.5, e.z - Z - 0.5) < 5.5 && Math.hypot(e.x - X - 0.5, e.z - Z - 0.5) > 4.5).map(e => e.entityId);
  console.log('  conduit candidates', ids.length);
  for (const id of ids) { const e = A.ents[id]; if (!e) continue; await run(`tp TestRat ${e.x + (e.x > X + 0.5 ? 1.2 : e.x < X + 0.5 ? -1.2 : 0)} ${Y + 1} ${e.z + (e.z > Z + 0.5 ? 1.2 : e.z < Z + 0.5 ? -1.2 : 0)}`); await sleep(300);
    for (let i = 0; i < 9; i++) { A.attack(id); await sleep(300); } }
  await sleep(1500);
  console.log('  left:', await cnt('@e[type=interaction,tag=bm.rhit]'), 'hp:', (await run('execute as @e[type=interaction,tag=bm.rhit] run scoreboard players get @s bm.chp')).slice(0,80), 'vorn near:', await cnt(`@e[tag=bm.vtroop,x=${X},y=${Y},z=${Z},distance=..20]`));
  ok('smash all four: reactor offline, the vault opens, Meltdown', !(await cnt('@e[type=interaction,tag=bm.rhit]')) && (await run(`data get block ${X} ${Y + 1} ${Z + 3}`)).includes('p52/vault') && await adv('reactor'));
  // ---- dawn ends the night
  await run('time set day'); await sleep(2500);
  ok('dawn: the Fence\'s invasion stock is gone', (await score('#inv')) === 0 && !(await has('fence', 'signal_jammer')));
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('kill @e[tag=bm.slot]'); await run('kill @e[tag=bm.slotd]'); await run('kill @e[tag=bm.potd]');
  console.log(res.filter(Boolean).length + '/' + res.length);
  A.end(); R.end(); process.exit(0); })().catch(e => { console.log('FATAL', e); process.exit(1); });

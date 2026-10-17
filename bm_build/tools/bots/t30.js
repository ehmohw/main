const { bot, rcon, sleep } = require('./lib_resp');
const X = 5600, Y = 100, Z = 5600;
(async () => { const R = await rcon(); const run = c => R.run(c);
  const res = []; const ok = (n, c, d) => { res.push(!!c); console.log(c ? 'PASS' : 'FAIL', n, d || ''); };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)[^\d]*$/); return m ? parseFloat(m[1]) : null; };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const adv = async (who, a) => (await cnt(`@a[name=${who},advancements={bm:story/${a}=true}]`)) === 1;
  const inv = async (who, it) => { const r = await run(`clear ${who} ${it} 0`); const m = r.match(/Found (\d+)/); return m ? +m[1] : 0; };
  const A = await bot('TestRat'); const V = await bot('Victim'); await sleep(1500);
  await run('advancement revoke TestRat from bm:story/root'); await run('advancement revoke TestRat only bm:recipes/tinkering'); await run('recipe take TestRat *');
  await run('time set noon'); await run('scoreboard players set #forced bm.bm 0'); await run('gamerule keep_inventory false');
  for (const p of ['TestRat', 'Victim']) { await run(`gamemode survival ${p}`); await run(`clear ${p}`); await run(`tp ${p} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); }
  await sleep(2500);
  await run(`fill ${X - 12} ${Y - 1} ${Z - 12} ${X + 12} ${Y} ${Z + 12} stone`); await run(`fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 8} ${Z + 12} air`);
  await run(`fill ${X - 12} ${Y + 5} ${Z - 12} ${X + 12} ${Y + 5} ${Z + 12} sea_lantern`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..30]`);
  // ---- the newcomers' book
  // (the real thing: a lectern, and the market's own book function aimed at it - the old bmtest helper pack is gone)
  await run(`setblock ${X} ${Y + 1} ${Z} minecraft:lectern`); await run(`execute positioned ${X + 4.5} ${Y - 5} ${Z - 33.5} rotated 0 0 run function bm:p50/book`); await sleep(300);
  const B = `${X} ${Y + 1} ${Z} Book.components."minecraft:written_book_content".pages`;
  let pages = 0; for (let i = 0; i < 101; i++) { if (!(await run(`execute if data block ${B}[${i}]`)).includes('passed')) break; pages = i + 1; }
  ok('newcomers\' book: accepted by the game, every page (the short who-sells-what book, 2.63)', pages >= 5 && pages <= 100, pages + ' pages');
  let all = ''; for (let i = 0; i < pages; i++) all += await run(`data get block ${B}[${i}]`);
  ok('...lists Cecil, the tinkering machines, Zorp, and no prices (only the exchange rates)', /Cecil the Wizard/.test(all) && /tinkering machines/.test(all) && /Zorp/.test(all) &&
     !/Token[s]?\s*x?\d|\d+ Tokens/.test(all.replace(/5 Tokens = 1 Medallion/, '').replace(/pays 2 Tokens each/, '')));
  await run(`setblock ${X} ${Y + 1} ${Z} air`);
  // ---- advancements + recipes (first token)
  await run('loot give TestRat loot bm:items/token'); await sleep(500);
  ok('first token: the Black Market tab opens', await adv('TestRat', 'root'));
  ok('...and the tinkering recipes unlock', (await cnt('@a[name=TestRat,advancements={bm:recipes/tinkering=true}]')) === 1);
  await run(`summon zombie ${X + 3} ${Y + 1} ${Z} {NoAI:1b,Tags:["bm.boss_brood"],PersistenceRequired:1b}`);
  await run(`damage @e[tag=bm.boss_brood,limit=1] 500 minecraft:player_attack by TestRat`); await sleep(300);
  ok('slay the Broodmother: advancement', await adv('TestRat', 'boss_brood'));
  await run(`summon ravager ${X + 3} ${Y + 1} ${Z} {NoAI:1b,Tags:["bm.monstrosity"],PersistenceRequired:1b}`);
  await run(`damage @e[tag=bm.monstrosity,limit=1] 900 minecraft:player_attack by TestRat`); await sleep(300);
  ok('slay the Monstrosity: advancement', await adv('TestRat', 'monstrosity'));
  await run('scoreboard players set #forced bm.bm 1'); await run('time set midnight'); await sleep(2200);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..60]`);
  await run('scoreboard players set #forced bm.bm 0'); await run('time set day'); await sleep(2200);
  ok('live to see dawn after a Blood Moon: advancement', await adv('TestRat', 'blood_moon'));
  // ---- crafting: a crafter makes a real Tinker's Wrench
  await run(`setblock ${X - 4} ${Y + 1} ${Z - 1} air`); await run(`setblock ${X - 4} ${Y + 1} ${Z} air`); await sleep(200); await run(`setblock ${X - 4} ${Y + 1} ${Z} crafter[orientation=east_up]`);
  for (const s of [2, 4, 6]) await run(`item replace block ${X - 4} ${Y + 1} ${Z} container.${s} with iron_ingot`);
  await run(`setblock ${X - 4} ${Y + 1} ${Z - 1} redstone_block`); await sleep(1500); console.log('  crafter out:', (await run(`data get entity @e[type=item,x=${X - 3},y=${Y + 1},z=${Z},distance=..4,limit=1] Item.components."minecraft:custom_data"`)).slice(-60));
  ok("recipe: a crafter makes a working Tinker's Wrench", (await inv('TestRat', '*[custom_data~{bm:"tinker_wrench"}]')) === 1 || (await cnt(`@e[type=item,x=${X - 3},y=${Y + 1},z=${Z},distance=..3,nbt={Item:{components:{"minecraft:custom_data":{bm:"tinker_wrench"}}}}]`)) === 1);
  await run(`setblock ${X - 4} ${Y + 1} ${Z - 1} air`); await run(`setblock ${X - 4} ${Y + 1} ${Z} air`); await run(`kill @e[type=item,x=${X},y=${Y},z=${Z},distance=..20]`);
  // ---- settings
  const n0 = A.dialogN.length; await run('execute as TestRat run function bm:admin/settings'); await sleep(600);      // (2.80: a dialog, not chat)
  ok('admin/settings menu opens', A.dialogN.length > n0 && /SERVER SETTINGS/.test(JSON.stringify(A.dialogN[A.dialogN.length - 1])), A.buttons().map(b => b.label).join(' | ').slice(0, 120));
  await run('execute as TestRat run function bm:admin/set/bmper_10'); await run('time set midnight'); await sleep(1500); await run('scoreboard players set #bmday bm.bm 9'); await sleep(2200);
  const cyc10 = await num('scoreboard players get #active bm.bm');
  // (a Blood Moon that has risen lasts till dawn - so the change shows the next night)
  await run('execute as TestRat run function bm:admin/set/bmper_30'); await run('time set day'); await sleep(2200);
  await run('time set midnight'); await sleep(1500); await run('scoreboard players set #bmday bm.bm 9'); await sleep(2200);
  const cyc30 = await num('scoreboard players get #active bm.bm');
  ok('Blood Moon every 10 days: day 9 night has one; at 30 days the next day-9 night does not', cyc10 === 1 && cyc30 === 0, `${cyc10} ${cyc30} day ${await num('scoreboard players get #day bm.bm')}`);
  await run('execute as TestRat run function bm:admin/set/bmoff_1'); await run('time set midnight'); await sleep(1500); await run('scoreboard players set #bmday bm.bm 29'); await sleep(2200);
  ok('"Never": no natural Blood Moon on cycle day 29', (await num('scoreboard players get #active bm.bm')) === 0);
  await run('execute as TestRat run function bm:admin/set/bmper_30'); await sleep(2200);
  ok('...and back on (30 days): day 29 night has one again', (await num('scoreboard players get #active bm.bm')) === 1, ['#day','#cyc','#bday','#tod'].map(async h => h).length + ' ' + (await run('scoreboard players get #day bm.bm')).slice(-14) + ' ' + (await run('scoreboard players get #tod bm.bm')).slice(-16) + ' ' + (await run('scoreboard players get #bmoff bm.cfg')).slice(-14));
  await run('time set day'); await sleep(2000);
  await run('execute as TestRat run function bm:admin/set/breaker_0'); await run(`setblock ${X + 5} ${Y + 1} ${Z + 5} oak_log`);
  await run(`execute positioned ${X + 5} ${Y + 1} ${Z + 5} run function bm:p49/block_breaker/hit`); const kept = (await run(`execute if block ${X + 5} ${Y + 1} ${Z + 5} oak_log`)).includes('passed');
  await run('execute as TestRat run function bm:admin/set/breaker_1'); await run(`execute positioned ${X + 5} ${Y + 1} ${Z + 5} run function bm:p49/block_breaker/hit`);
  ok('Block Breaker switch: off keeps the log, on breaks it', kept && (await run(`execute if block ${X + 5} ${Y + 1} ${Z + 5} air`)).includes('passed'));
  await run('execute as TestRat run function bm:admin/set/bombs_0'); await run('give TestRat tnt 1'); await run('scoreboard players reset TestRat bm.skb');
  await run('execute as TestRat at TestRat run function bm:p35/skiff/bomb'); await sleep(200);
  ok('skiff bombs switch: off, no TNT is dropped', !(await cnt('@e[type=tnt]')) && (await inv('TestRat', 'minecraft:tnt')) === 1, A.bars.slice(-1)[0]);
  await run('execute as TestRat run function bm:admin/set/bombs_1'); await run('clear TestRat tnt');
  await run('execute as TestRat run function bm:admin/set/pvp_0'); await sleep(1300);
  const tagged = await cnt('@a[tag=bm.nopvp]');
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/tidal_tear'); await run('scoreboard players reset TestRat bm.mcd5');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await run(`tp Victim ${X + 0.5} ${Y + 1} ${Z + 3.5}`); await run('effect give Victim instant_health 1 5 true'); await sleep(600);
  const v0 = await num('data get entity Victim Health'); await run('execute as TestRat at TestRat run function bm:p45/tidal_tear/use'); await sleep(1500);
  const v1 = await num('data get entity Victim Health');
  await run('execute as TestRat run function bm:admin/set/pvp_1'); await sleep(1300);
  ok('magic PvP switch: off, the Tidal Tear spares other players', tagged === 2 && v1 >= v0 && !(await cnt('@a[tag=bm.nopvp]')), `tagged ${tagged}; victim ${v0}->${v1}`);
  // ---- the Grave Charm
  await run('clear TestRat'); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z - 4.5}`); await sleep(500);
  await run('loot give TestRat loot bm:items/grave_charm'); await run('give TestRat diamond 7'); await run('give TestRat iron_sword 1');
  await sleep(300); await run('kill TestRat'); await sleep(1500);
  const graves = await cnt('@e[type=marker,tag=bm.grave]'), loose = await cnt(`@e[type=item,x=${X + 0.5},y=${Y + 1},z=${Z - 4.5},distance=..6]`);
  const gitems = await run('data get entity @e[type=marker,tag=bm.grave,limit=1] data.items');
  ok('died carrying the charm: a grave holds everything, nothing scattered', graves === 1 && loose === 0 && /diamond/.test(gitems) && /iron_sword/.test(gitems) && /grave_charm/.test(gitems), `graves ${graves}, loose ${loose}`);
  ok('...and you are told where it is', A.chats.slice(-4).join(' ').includes('rest in a grave'));
  // a stranger can't open it
  const hit = Object.values(V.ents).find(e => Math.abs(e.x - (X + 0.5)) < 0.6 && Math.abs(e.z - (Z - 4.5)) < 0.6 && e.type !== undefined && Math.abs(e.y - (Y + 1)) < 0.6 && e.objectData !== undefined);
  await run(`tp Victim ${X + 0.5} ${Y + 1} ${Z - 2.5} 180 20`); await sleep(2000);
  const iid = async (cl) => { const ids = Object.values({ ...A.ents, ...V.ents }).filter(e => Math.abs(e.x - (X + 0.5)) < 0.6 && Math.abs(e.z - (Z - 4.5)) < 0.6).map(e => e.entityId); return ids; };
  const vi = await iid(V); console.log('  stranger clicks', vi); for (const id of vi) V.interact(id); await sleep(800);
  ok("a stranger can't open it", (await cnt('@e[type=marker,tag=bm.grave]')) === 1 && V.bars.slice(-1)[0] && V.bars.slice(-1)[0].includes("isn't yours"), V.bars.slice(-1)[0]);
  // the owner can
  await sleep(1500); console.log('  owner health', (await run('data get entity TestRat Health')).slice(-8)); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z - 2.5} 180 20`); await sleep(2500);
  const ai = vi; console.log('  owner clicks', ai); for (const id of ai) A.interact(id);
  for (let k = 0; k < 20 && (await inv('TestRat', 'minecraft:diamond')) !== 7; k++) await sleep(200);     // (the grave hands it all back - give it a moment)
  await sleep(400);
  ok('the owner right-clicks: everything comes back, the grave is gone', (await inv('TestRat', 'minecraft:diamond')) === 7 && (await inv('TestRat', 'minecraft:iron_sword')) === 1 &&
     (await inv('TestRat', '*[custom_data~{bm:"grave_charm"}]')) === 1 && !(await cnt('@e[tag=bm.grave]')) && !(await cnt('@e[tag=bm.gravehit]')) && !(await cnt('@e[tag=bm.gravev]')),
     `diamonds ${await inv('TestRat', 'minecraft:diamond')} sword ${await inv('TestRat', 'minecraft:iron_sword')} charm ${await inv('TestRat', '*[custom_data~{bm:"grave_charm"}]')} graves ${await cnt('@e[tag=bm.grave]')}/${await cnt('@e[tag=bm.gravehit]')}/${await cnt('@e[tag=bm.gravev]')}`);
  ok('...Six Feet Under', await adv('TestRat', 'grave'));
  // without the charm, death is vanilla
  await run('clear TestRat'); await run('give TestRat diamond 3'); await run(`tp TestRat ${X + 4.5} ${Y + 1} ${Z + 4.5}`); await sleep(400); await run('kill TestRat');
  for (let k = 0; k < 20 && !(await cnt(`@e[type=item,x=${X + 4.5},y=${Y + 1},z=${Z + 4.5},distance=..5]`)); k++) await sleep(200);   // (a busy tick can hold the drop back - give it a moment)
  ok('no charm: no grave, items drop as usual', !(await cnt('@e[type=marker,tag=bm.grave]')) && (await cnt(`@e[type=item,x=${X + 4.5},y=${Y + 1},z=${Z + 4.5},distance=..5]`)) >= 1);
  // ---- help
  const n1 = A.chats.length; await run('execute as TestRat run function bm:admin/help'); await sleep(300);
  const help = A.chats.slice(n1).join(' | ');
  ok('admin/help lists the commands, settings included', help.includes('admin/settings') && help.includes('place_market') && help.includes('invasion_now'), (A.chats.length - n1) + ' lines');
  await run(`kill @e[type=item,x=${X},y=${Y},z=${Z},distance=..30]`);
  console.log(res.filter(Boolean).length + '/' + res.length);
  A.end(); V.end(); R.end(); process.exit(0); })().catch(e => { console.log('FATAL', e); process.exit(1); });

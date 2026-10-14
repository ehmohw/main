const { bot, rcon, sleep } = require('./lib');
const X = 5300, Y = 100, Z = 5300, H = 13;     // the skiff hovers H above the floor
(async () => { const R = await rcon(); const run = c => R.run(c);
  const res = []; const ok = (n, c, d) => { res.push(!!c); console.log(c ? 'PASS' : 'FAIL', n, d || ''); };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)[^\d]*$/); return m ? parseFloat(m[1]) : null; };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const inv = async (who, it) => { const r = await run(`clear ${who} ${it} 0`); const m = r.match(/Found (\d+)/); return m ? +m[1] : 0; };
  const look = async (yw, pt) => { await run(`rotate TestRat ${yw} ${pt}`); A.pos.yaw = yw; A.pos.pitch = pt; await sleep(200); };
  const y = async (sel) => num(`data get entity ${sel} Pos[1]`);
  const A = await bot('TestRat'); const V = await bot('Victim'); await sleep(1500);
  await run('time set noon'); await run('scoreboard players set #forced bm.bm 0'); await run('weather clear');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await run(`tp Victim ${X + 0.5} ${Y + 1} ${Z + 1.5}`); await sleep(2500);
  await run(`fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} stone`); await run(`fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 24} ${Z + 12} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..50]`);
  for (const p of ['TestRat', 'Victim']) { await run(`gamemode survival ${p}`); await run(`clear ${p}`); await run(`effect clear ${p}`); await run(`tag ${p} remove bm.skbeam`); await run(`scoreboard players reset ${p} bm.skbt`); }
  await run('scoreboard players reset TestRat bm.skl'); await run('scoreboard players reset TestRat bm.skb');
  // ---- call the skiff
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/skiff_key'); await sleep(300);
  A.use(); await sleep(300); A.release(); await sleep(1200);
  ok('skiff called, pilot aboard', (await cnt('@e[type=happy_ghast,tag=bm.skiff]')) === 1 && (await cnt('@a[name=TestRat,predicate=bm:p29/has_vehicle]')) === 1);
  await run(`tp @e[type=happy_ghast,tag=bm.skiff] ${X + 0.5} ${Y + H} ${Z + 0.5} 0 0`); await sleep(1500);
  ok('pilot still aboard after the skiff moved', (await cnt('@a[name=TestRat,predicate=bm:p29/has_vehicle]')) === 1, 'pilot y ' + await y('TestRat'));
  const tr = await run('data get entity @e[tag=bm.skdisp,limit=1] transformation');
  ok('hull rides with the pilot: 4.5 scale, seat translation', /scale: \[4\.5f, 4\.5f, 4\.5f\]/.test(tr) && /translation: \[0\.0f, 0\.22f, 0\.0f\]/.test(tr), tr.replace(/.*translation/, 'translation').slice(0, 60));
  const gy = await y('@e[type=happy_ghast,tag=bm.skiff,limit=1]'), py = await y('TestRat'), hy = await y('@e[tag=bm.skdisp,limit=1]');
  ok('seat geometry as rendered (pilot +0.2, hull +0.8 over the ghast)', Math.abs(py - gy - 0.2) < 0.02 && Math.abs(hy - gy - 0.8) < 0.02, `ghast ${gy} pilot ${py} hull ${hy}`);
  // ---- beam without power
  await look(0, -80); A.use(); await sleep(300); A.release(); await sleep(400);
  ok('2.44: the beam needs no power - it switches on with no Violet Xenite', (await cnt('@a[tag=bm.skbeam]')) === 1, A.bars.slice(-1)[0]);
  await look(0, -80); A.use(); await sleep(300); A.release(); await sleep(400);
  // ---- targets below
  await run(`tp Victim ${X + 0.5} ${Y + 1} ${Z + 0.5}`);
  await run(`summon husk ${X + 1.5} ${Y + 1} ${Z - 0.5} {Tags:["t28z"],PersistenceRequired:1b,attributes:[{id:"minecraft:follow_range",base:0d}]}`);
  await run(`summon husk ${X - 0.5} ${Y + 1} ${Z + 1.5} {Tags:["t28b"],PersistenceRequired:1b,Health:200f,attributes:[{id:"minecraft:max_health",base:200d},{id:"minecraft:follow_range",base:0d}]}`);
  await run('attribute @e[tag=t28b,limit=1] minecraft:max_health base set 200'); console.log('  boss hp', (await run('attribute @e[tag=t28b,limit=1] minecraft:max_health get')).slice(-8));
  await run(`summon pig ${X - 1.5} ${Y + 1} ${Z - 0.5} {Tags:["t28p"]}`);
  await run(`summon item ${X + 0.5} ${Y + 1} ${Z - 1.5} {Item:{id:"minecraft:diamond",count:3},Tags:["t28i"]}`);
  await run(`summon experience_orb ${X - 0.5} ${Y + 1} ${Z - 1.5} {Value:7}`);
  const z0 = await y('@e[tag=t28z,limit=1]'), v0 = await y('Victim');
  await run('give TestRat minecraft:tnt 2');
  await run('loot give TestRat loot bm:items/xenite_violet'); await run('loot give TestRat loot bm:items/xenite_violet');
  const xp0 = await num('xp query TestRat points');
  // ---- beam on
  await look(0, -80); A.use(); await sleep(300); A.release(); await sleep(500);
  const sh1 = await inv('TestRat', '*[custom_data~{bm:"xenite_violet"}]');
  ok('look up + right-click: beam on, no shard drawn', (await cnt('@a[name=TestRat,tag=bm.skbeam]')) === 1 && sh1 === 2, sh1 + ' shards left');
  await sleep(6000);
  const gy2 = await y('@e[type=happy_ghast,tag=bm.skiff,limit=1]');
  const z1 = await y('@e[tag=t28z,limit=1]'), v1 = await y('Victim'), p1 = await y('@e[tag=t28p,limit=1]'), b1 = await y('@e[tag=t28b,limit=1]');
  ok('zombie lifted up under the hull', z1 > z0 + 6 && z1 < gy2, `${z0} -> ${z1} (skiff ${gy2})`);
  const ve = await run('data get entity Victim active_effects'); ok('other player gets the lift (levitation/hover; their own client moves them)', /levitation|slow_falling/.test(ve), ve.slice(-90));
  ok('pig lifted', p1 > Y + 7, '' + p1);
  ok('bosses (over 100 max health) are not lifted', b1 < Y + 2, '' + b1 + ' ' + (await run('data get entity @e[tag=t28b,limit=1] active_effects')).slice(-120) + ' veh:' + (await run('data get entity @e[tag=t28b,limit=1] RootVehicle')).slice(-80));
  ok('items rise into your pack', (await inv('TestRat', 'minecraft:diamond')) === 3 && !(await cnt('@e[tag=t28i]')));
  ok('xp orbs rise into you', !(await cnt(`@e[type=experience_orb,x=${X},y=${Y},z=${Z},distance=..20]`)));
  await sleep(2000);
  const zh = await y('@e[tag=t28z,limit=1]');
  ok('held beneath the saucer (not pulled into it)', zh > gy2 - 6 && zh < gy2 - 1.5, `zombie ${zh}, skiff ${gy2}`);
  // ---- other abilities while the beam runs
  await run(`summon husk ${X + 0.5} ${Y + H + 1} ${Z + 7.5} {Tags:["t28l"],NoAI:1b,NoGravity:1b,PersistenceRequired:1b}`);
  await look(0, 0); await sleep(1200);
  const l0 = await num('data get entity @e[tag=t28l,limit=1] Health'); A.use(); await sleep(300); A.release(); await sleep(400);
  ok('laser still fires while the beam runs', (await num('data get entity @e[tag=t28l,limit=1] Health')) < l0 || !(await cnt('@e[tag=t28l]')), `${l0} -> ${await num('data get entity @e[tag=t28l,limit=1] Health')}`);
  await run('kill @e[tag=t28l]');
  await look(0, 80); A.use(); await sleep(300); A.release(); await sleep(200);
  ok('look down: TNT bomb still drops', (await cnt('@e[type=tnt,tag=bm.skbomb]')) === 1 && (await inv('TestRat', 'minecraft:tnt')) === 1);
  await run('kill @e[type=tnt]');
  ok('beam still on after the laser and the bomb', (await cnt('@a[name=TestRat,tag=bm.skbeam]')) === 1);
  // ---- no power drawn: still running after 14 s, shards untouched; switch off by hand and the held ones drop
  await sleep(4000);
  ok('still running, shards untouched', (await inv('TestRat', '*[custom_data~{bm:"xenite_violet"}]')) === 2 && (await cnt('@a[name=TestRat,tag=bm.skbeam]')) === 1);
  await look(0, -80); A.use(); await sleep(300); A.release(); await sleep(400);
  ok('look up again: beam off', !(await cnt('@a[tag=bm.skbeam]')), A.bars.slice(-1)[0]);
  await sleep(2500);
  { const py2 = await y('@e[tag=t28p,limit=1]'); ok('released creatures drop (the pig)', py2 !== null && py2 < Y + 3, '' + py2); }
  // ---- toggle off by hand
  // ---- creative players are left alone
  await run('gamemode creative Victim'); await run(`tp Victim ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(300);
  await look(0, -80); A.use(); await sleep(300); A.release(); await sleep(3000);
  ok('creative players are not lifted', (await y('Victim')) < Y + 2, '' + await y('Victim'));
  // ---- land
  await look(0, 0); A.input({ shift: true }); await sleep(600); A.input({}); await sleep(1200);
  ok('sneak lands: off the skiff, beam off', (await cnt('@a[name=TestRat,predicate=bm:p29/has_vehicle]')) === 0 && !(await cnt('@a[tag=bm.skbeam]')));
  const tr2 = await run('data get entity @e[tag=bm.skdisp,limit=1] transformation.translation');
  ok('parked hull goes back to its parked height', /0\.775f/.test(tr2) || !(await cnt('@e[tag=bm.skdisp]')), tr2.slice(-30));
  ok('nothing was broken: one skiff, one hull', (await cnt('@e[type=happy_ghast,tag=bm.skiff]')) <= 1 && (await cnt('@e[tag=bm.skdisp]')) <= 1);
  await run('gamemode survival Victim'); await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..50]`);
  console.log(res.filter(Boolean).length + '/' + res.length);
  A.end(); V.end(); R.end(); process.exit(0); })().catch(e => { console.log('FATAL', e); process.exit(1); });

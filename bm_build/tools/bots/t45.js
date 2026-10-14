// v2.45: Pearlman, the gems (finder, display, kin), the fusion, the Ethereal shrine and status
const { bot, rcon, sleep } = require('./lib');
const X = 10200, Y = 100, Z = 10200;
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)[fdbsL]?\s*$/); return m ? +m[1] : null; };
  const inv = async (q) => { const r = await run(`clear TestRat ${q} 0`); const m = r.match(/Found (\d+)/); return m ? +m[1] : 0; };
  const look = async (yaw, pitch) => { await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} ${yaw} ${pitch}`); await sleep(400); };
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run(`forceload add ${X - 40} ${Z - 40} ${X + 40} ${Z + 40}`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2500);
  await run(`fill ${X - 40} ${Y} ${Z - 12} ${X + 40} ${Y} ${Z + 12} stone`); await run(`fill ${X - 40} ${Y + 1} ${Z - 12} ${X + 40} ${Y + 8} ${Z + 12} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..50]`); await run('time set noon'); await run('weather clear');
  await run('kill @e[tag=bm.pearl]'); await run('kill @e[tag=bm.pearld]'); await run('kill @e[tag=bm.eshr]'); await run('kill @e[tag=bm.gdeco]'); await run('kill @e[tag=bm.gplaced]');
  // ---- Pearlman
  await run(`execute as TestRat at @s run function bm:admin/pearlman`); await sleep(500);
  ok('Pearlman arrives: a hidden villager and his penguin model', (await cnt('@e[type=villager,tag=bm.pearl]')) === 1 && (await cnt('@e[type=item_display,tag=bm.pearld]')) === 1);
  const gems = []; for (let i = 0; i < 4; i++) { const m = (await run(`data get entity @e[type=villager,tag=bm.pearl,limit=1] Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`)).match(/"gem_(\w+)"/); if (m) gems.push(m[1]); }
  const cur = await run('data get entity @e[type=villager,tag=bm.pearl,limit=1] Offers.Recipes[0].buy.components."minecraft:custom_data".bm');
  ok('...three different gems for sale, for Medallions', gems.length === 3 && new Set(gems).size === 3 && /medallion/.test(cur), gems.join(','));
  await run('scoreboard players set @e[tag=bm.pearl] bm.pmt 2'); await sleep(2600);
  ok('...and waddles off when his time is up', (await cnt('@e[tag=bm.pearl]')) === 0 && (await cnt('@e[tag=bm.pearld]')) === 0);
  // ---- a gem finds its biome
  await run('execute as TestRat run function bm:admin/elemental_gems'); await sleep(300);
  ok('All nine gems', (await inv('*[custom_data~{bm:"gem_fire"}]')) === 1 && (await inv('*[custom_data~{bm:"gem_ice"}]')) === 1);
  await run('item replace entity TestRat hotbar.0 with air'); await run('item replace entity TestRat hotbar.0 from entity TestRat hotbar.1'); // water
  for (let i = 0; i < 9; i++) await run(`item replace entity TestRat hotbar.${i} with air`);
  await run('give TestRat minecraft:stone 1'); await run('clear TestRat');
  await run('execute as TestRat run function bm:admin/elemental_gems'); await sleep(300);
  A.slot(1); await sleep(300);
  const held = await run('data get entity TestRat SelectedItem.components."minecraft:custom_data".bm');
  A.use(); await sleep(250); A.release(); await sleep(1500);
  const bar = A.bars.slice(-3).join(' | ');
  ok('Use: the gem glints toward its biome (direction + distance)', /glints|standing in it|stays dark/.test(bar), held.slice(-14) + ' :: ' + bar.slice(-160));
  await run('scoreboard players set TestRat bm.gmcd 0'); await run('execute as TestRat at @s run function bm:p60/gem/find_ice'); await sleep(400);
  const bar2 = A.bars.slice(-1)[0] || '';
  ok('...a far-off one: a compass direction and a distance', /glints (north|south|east|west)/.test(bar2) || /stays dark/.test(bar2), bar2.slice(-120));
  const chat = A.chats.slice(-4).join(' | ');
  ok('...no locate spam in chat', !/nearest|blocks away/.test(chat), chat.slice(-120));
  // ---- on display, kin, fusion (placed by command at nine spots round the player)
  const spots = [[1, 1], [1, -1], [2, 1], [2, -1], [0, 1], [0, -1], [2, 0], [3, 0], [3, 1]];
  const keys = ['fire', 'water', 'poison', 'earth', 'electric', 'rock', 'air', 'grass', 'ice'];
  A.slot(0); await sleep(200);
  // one by hand: look at the floor 2 ahead, sneak + use
  await look(0, 60); A.input({ shift: true }); await sleep(300); A.use(); await sleep(250); A.release(); await sleep(300); A.input({}); await sleep(400);
  const nd = await cnt('@e[type=item_display,tag=bm.gdeco]');
  ok('Sneak + use: set a gem on display (and it leaves your hand)', nd === 1 && (await inv('*[custom_data~{bm:"gem_' + 'fire"}]')) + (await inv('*[custom_data~{bm:"gem_water"}]')) === 1, `displays ${nd}`);
  const placedKey = (await run('data get entity @e[type=item_display,tag=bm.gdeco,limit=1] item.components."minecraft:item_model"')).match(/gem_(\w+)/)?.[1];
  for (let i = 0; i < 9; i++) { const k = keys[i]; if (k === placedKey) continue;
    await run(`execute positioned ${X + 0.5 + spots[i][1]} ${Y + 1} ${Z + 0.5 + spots[i][0] + 1} run function bm:p60/spawn/${k}`); await sleep(150);
    if (i === 6) { await sleep(200); ok('...it hums with its kin; eight is not enough', (await cnt('@e[type=marker,tag=bm.gfm]')) === 0); } }
  await sleep(300);
  ok('All nine on display together: they rise and circle (fusion starts)', (await cnt('@e[type=marker,tag=bm.gfm]')) === 1 && (await cnt('@e[type=item_display,tag=bm.gfuse]')) === 9);
  await sleep(3500);
  ok('...and become the Ethereal Gem', (await cnt(`@e[type=item,x=${X},y=${Y},z=${Z},distance=..10,nbt={Item:{components:{"minecraft:custom_data":{bm:"ethereal_gem"}}}}]`)) === 1 && (await cnt('@e[tag=bm.gdeco]')) === 0 && (await cnt('@e[tag=bm.gdeco_hit]')) === 0);
  ok('...secret achievement: Nine Made One', (await cnt('@a[name=TestRat,advancements={bm:story/ethereal_gem=true}]')) === 1);
  // ---- the shrine
  await run('kill @e[type=item]'); await run('clear TestRat'); await run('execute as TestRat run function bm:admin/ethereal_gem'); A.slot(0); await sleep(300);
  await look(0, 60); A.use(); await sleep(250); A.release(); await sleep(1600);
  ok('Use the Ethereal Gem: it is set down as a shrine', (await cnt('@e[type=item_display,tag=bm.eshr]')) === 1 && (await inv('*[custom_data~{bm:"ethereal_gem"}]')) === 0);
  await sleep(1200);
  const tg = await run('tag TestRat list'); const gr = await num('attribute TestRat minecraft:gravity get');
  ok('...within 30 blocks: Ethereal (light as air)', /bm\.eth/.test(tg) && gr < 0.05, `gravity ${gr}`);
  ok('...+3 attack, +4 armour, regeneration', (await num('attribute TestRat minecraft:attack_damage get')) >= 4 && (await num('attribute TestRat minecraft:armor get')) >= 4 && /regeneration/.test(await run('data get entity TestRat active_effects')));
  await run(`summon husk ${X + 0.5} ${Y + 1} ${Z - 1.6} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["bm.t45"],active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0b}]}`); await sleep(500);
  await run('attribute @e[tag=bm.t45,limit=1] minecraft:max_health base set 200'); await run('data modify entity @e[tag=bm.t45,limit=1] Health set value 200f'); await sleep(800);
  const zid = Object.values(A.ents).filter(e => Math.abs(e.x - X - 0.5) < 0.3 && Math.abs(e.z - Z + 1.1) < 0.6).pop()?.entityId;
  A.attack(zid); await sleep(1100);
  const zh = await num('data get entity @e[tag=bm.t45,limit=1] Health'); const ze = await run('data get entity @e[tag=bm.t45,limit=1]');
  ok('...a blow unleashes an element (more than the fist alone)', zh < 194, `${zh} ${/Fire:\d|TicksFrozen|poison|wither|slowness|levitation/.exec(ze)?.[0] || ''}`);
  await run(`tp TestRat ${X + 36.5} ${Y + 1} ${Z + 0.5}`); await sleep(2200);
  ok('Walk 35 blocks away: the lightness fades', !/bm\.eth/.test(await run('tag TestRat list')) && Math.abs((await num('attribute TestRat minecraft:gravity get')) - 0.08) < 0.001);
  // sneak + punch takes it back
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 30`); await sleep(1500);
  const sp = (await run('data get entity @e[type=interaction,tag=bm.eshr_hit,limit=1] Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
  const sid = Object.values(A.ents).filter(e => Math.abs(e.x - sp[0]) < 0.2 && Math.abs(e.z - sp[2]) < 0.2).map(e => e.entityId);
  A.input({ shift: true }); await sleep(300); for (const i of sid) A.attack(i); await sleep(600); A.input({}); await sleep(600);
  ok('Sneak + punch the shrine: you take it back', (await cnt('@e[type=item_display,tag=bm.eshr]')) === 0, `tried ${sid.length}`);
  await run('kill @e[tag=bm.t45]'); await run('kill @e[type=item]');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

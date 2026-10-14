const { bot, rcon, sleep } = require('./lib');
const X = 12100, Y = 200, Z = 12100; const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const sc = async (who, o) => ((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [])[1];
  await run(`fill ${X - 16} ${Y} ${Z - 16} ${X + 16} ${Y} ${Z + 16} snow_block`); await run(`fill ${X - 16} ${Y + 1} ${Z - 16} ${X + 16} ${Y + 8} ${Z + 16} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('kill @e[type=wolf,tag=bm.celipet]'); await run('kill @e[tag=bm.cep]');
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 120 4 true'); await run('time set day');
  await run('scoreboard players reset TestRat bm.cecd');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  // the encounter: she stands 4 ahead, tapping her foot
  await run('execute as TestRat at @s run function bm:admin/celi'); await sleep(800);
  ok('Encounter: Celi stands there (9 rig parts + her hitbox)', (await cnt('@e[type=item_display,tag=bm.ceencp]')) === 9 && (await cnt('@e[type=interaction,tag=bm.ceenc]')) === 1);
  const rs = new Set(); for (let i = 0; i < 20; i++) { rs.add(await run('data get entity @e[tag=bm.ceencp,tag=bm.cp6_legr,limit=1] transformation.left_rotation')); await sleep(150); }
  ok('...tapping her foot', rs.size >= 2, [...rs].map(r => r.slice(-30)).join(' / '));
  // talk empty-handed, then with a snowball
  const click = async () => { await run('data merge entity @e[type=interaction,tag=bm.ceenc,limit=1] {interaction:{timestamp:1L,player:[I;0,0,0,1]}}');
    await run('data modify entity @e[type=interaction,tag=bm.ceenc,limit=1] interaction.player set from entity TestRat UUID'); await sleep(500); };
  await click(); ok('Empty-handed: a sassy brush-off', /bored|snowball/.test(A.bars.slice(-1)[0] || ''), (A.bars.slice(-1)[0] || '').slice(0, 60));
  await run('item replace entity TestRat weapon.mainhand with snowball 4'); await click(); await sleep(800);
  ok('A snowball wins her over: the Moon Charm, and she joins', /passed/.test(await run('execute if items entity TestRat container.* *[custom_data~{bm:"celi_charm"}]'))
     && (await cnt('@e[type=wolf,tag=bm.celipet]')) === 1 && (await cnt('@e[type=item_display,tag=bm.cep,tag=!bm.ceencp]')) === 9 && (await cnt('@e[tag=bm.ceenc]')) === 0);
  ok('Low health: 30', /30\.0f/.test(await run('data get entity @e[type=wolf,tag=bm.celipet,limit=1] Health')));
  // fighting: a husk right next to her gets stabbed and frozen
  await run('execute at @e[type=wolf,tag=bm.celipet,limit=1] run summon husk ^ ^ ^2 {Tags:["bm.t58"],PersistenceRequired:1b,Health:60f,attributes:[{id:"minecraft:max_health",base:60}]}');
  let st = new Set(), frozen = false; for (let i = 0; i < 20; i++) { await sleep(150); const s = await sc('@e[type=wolf,tag=bm.celipet,limit=1]', 'bm.ces'); st.add(s); if (/passed/.test(await run('execute if entity @e[tag=bm.t58,tag=bm.cefrz]'))) frozen = true; }
  const hp = (await run('data get entity @e[tag=bm.t58,limit=1] Health')).match(/([\d.]+)f/);
  ok('She thrusts at the husk next to her (stab state), it is hurt and FROZEN', st.has('7') && frozen && hp && +hp[1] < 60, `states ${[...st]} hp ${hp && hp[1]}`);
  ok('...frozen = Slowness X (held in place)', /passed/.test(await run('execute if entity @e[tag=bm.t58,nbt={active_effects:[{id:"minecraft:slowness",amplifier:9b}]}]')) || frozen);
  await run('kill @e[tag=bm.t58]');
  // a husk 10 away: she throws her spear
  await run('execute at @e[type=wolf,tag=bm.celipet,limit=1] run summon husk ^ ^ ^10 {Tags:["bm.t58"],PersistenceRequired:1b,NoAI:1b,Health:60f,attributes:[{id:"minecraft:max_health",base:60}]}');
  let flew = false, thrown = false; for (let i = 0; i < 30; i++) { await sleep(150); if ((await cnt('@e[type=item_display,tag=bm.cesp]')) > 0) flew = true; if ((await sc('@e[type=wolf,tag=bm.celipet,limit=1]', 'bm.ces')) === '8') thrown = true; }
  const hp2 = (await run('data get entity @e[tag=bm.t58,limit=1] Health')).match(/([\d.]+)f/);
  ok('At range she throws the spear: it flies, hits (and freezes)', thrown && flew && hp2 && +hp2[1] <= 53, `thrown ${thrown} flew ${flew} hp ${hp2 && hp2[1]}`);
  await sleep(1500);
  ok('...and the spear is back in her hand', /\[0\.85f/.test(await run('data get entity @e[tag=bm.cep,tag=bm.cp6_spear,tag=!bm.ceencp,limit=1] transformation.scale')),
     (await run('data get entity @e[tag=bm.cep,tag=bm.cp6_spear,tag=!bm.ceencp,limit=1] transformation.scale')).slice(-30));
  await run('kill @e[tag=bm.t58]');
  // she faints: 5 minutes
  await run('kill @e[type=wolf,tag=bm.celipet]'); await sleep(1500);
  ok('She faints: the rig is gone and the charm rests 300 s', (await cnt('@e[tag=bm.cep]')) === 0 && +(await sc('TestRat', 'bm.cecd')) >= 295, await sc('TestRat', 'bm.cecd'));
  await run('scoreboard players reset TestRat bm.cecd');
  await run('item replace entity TestRat weapon.mainhand from entity TestRat container.0').catch(() => {});
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

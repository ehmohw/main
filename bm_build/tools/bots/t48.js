// v2.48: the Hollow Gate - set up, five Emblem sockets, opens, only 5-conquest players pass, way home, take back, pack up;
// the retired Shard re-forms as a gate; no Warpstone before the Hollow King falls
const { bot, rcon, sleep } = require('./lib');
const X = 10800, Y = 200, Z = 10800;
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const inv = async (q) => { const r = await run(`clear TestRat ${q} 0`); const m = r.match(/Found (\d+)/); return m ? +m[1] : 0; };
  const inHollow = async () => /passed/.test(await run('execute as TestRat at @s if dimension bm:hollow_throne'));
  const em = d => `*[custom_data~{bm:"emblem_${d}"}]`;
  const click = async (d) => { await run(`data merge entity @e[type=interaction,tag=bm.hgs_${d},limit=1] {interaction:{timestamp:1L,player:[I;0,0,0,1]}}`); await run(`data modify entity @e[type=interaction,tag=bm.hgs_${d},limit=1] interaction.player set from entity TestRat UUID`); await sleep(500); };
  const punch = async (d) => { A.input({ shift: true }); await sleep(250); await run(`data merge entity @e[type=interaction,tag=bm.hgs_${d},limit=1] {attack:{timestamp:1L,player:[I;0,0,0,1]}}`); await run(`data modify entity @e[type=interaction,tag=bm.hgs_${d},limit=1] attack.player set from entity TestRat UUID`); await sleep(500); A.input({}); await sleep(200); };
  const hold = async (q) => { await run('item replace entity TestRat weapon.mainhand with air'); await run(`execute as TestRat run loot replace entity @s weapon.mainhand loot bm:items/${q}`); await sleep(150); };
  await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2000);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat'); await run(`forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} stone`); await run(`fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..30]`); await run('scoreboard players set TestRat bm.conq 0'); await run('tag TestRat remove bm.got_warp');
  // ---- set it up
  await run('execute as TestRat run function bm:admin/hollow_gate'); A.slot(0); await sleep(300);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 50`); await sleep(400);
  A.use(); await sleep(250); A.release(); await sleep(600);
  ok('Use the Hollow Gate on the ground: it stands (frame + five sockets), and leaves your hand',
     (await cnt('@e[type=marker,tag=bm.hgate]')) === 1 && (await cnt('@e[type=item_display,tag=bm.hgd]')) === 1 && (await cnt('@e[type=interaction,tag=bm.hgs]')) === 5 && (await inv('*[custom_data~{bm:"hollow_gate"}]')) === 0);
  const rot = await run('data get entity @e[type=marker,tag=bm.hgate,limit=1] Rotation[0]');
  ok('...squared up to face you', /180\.0f|-180\.0f/.test(rot), rot.slice(-12));
  // ---- sockets
  await hold('emblem_frost'); await click('brood');
  ok('The wrong Emblem will not go in', (await cnt('@e[type=interaction,tag=bm.hgfull]')) === 0 && (await inv(em('frost'))) === 1, (A.bars.slice(-1)[0] || '').slice(-80));
  for (const d of ['brood', 'frost', 'tide', 'hex']) { await hold(`emblem_${d}`); await click(d); }
  ok('Four Emblems set: they glow in their sockets; the gate stays shut', (await cnt('@e[type=interaction,tag=bm.hgfull]')) === 4 && (await cnt('@e[type=item_display,tag=bm.hge]')) === 4 && (await cnt('@e[tag=bm.hgon]')) === 0 && (await inv(em('hex'))) === 0);
  await hold('emblem_keep'); await click('keep');
  ok('The fifth: THE HOLLOW GATE OPENS (portal surface)', (await cnt('@e[type=marker,tag=bm.hgon]')) === 1 && (await cnt('@e[type=item_display,tag=bm.hgp]')) === 1);
  // ---- passing through
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z - 1.5} 180 0`); await sleep(300);
  const mz = +((await run('data get entity @e[type=marker,tag=bm.hgate,limit=1] Pos[2]')).match(/(-?[\d.]+)d$/) || [])[1];
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${mz} 180 0`); await sleep(900);
  const pz = +((await run('data get entity TestRat Pos[2]')).match(/(-?[\d.]+)d$/) || [])[1];
  ok('Walk in without all five conquests: thrown back out, still in the Overworld', !(await inHollow()) && Math.abs(pz - mz) > 1.2, `gate z ${mz}, you ${pz}`);
  await run('scoreboard players set TestRat bm.conq 5'); await sleep(1700);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${mz} 180 0`); await sleep(1000);
  ok('With all five conquests: through the gate into the Hollow Throne', await inHollow());
  await sleep(1500);
  ok('...and no Warpstone yet (only the Hollow King gives that)', (await inv('*[custom_data~{bm:"hollow_warpstone"}]')) === 0);
  await run('execute as TestRat at @s run function bm:p2/hollow/leave'); await sleep(2500);
  const back = await run('data get entity TestRat Pos');
  ok('Home through the rift: back just in front of the gate (and not straight back in)', !(await inHollow()) && /2\d\d\.\d+d/.test(back), back.slice(-50));
  // ---- take back, pack up
  await punch('tide');
  ok('Sneak + punch a socket: its Emblem comes back, and the gate shuts', (await inv(em('tide'))) === 1 && (await cnt('@e[tag=bm.hgon]')) === 0 && (await cnt('@e[type=item_display,tag=bm.hgp]')) === 0);
  await punch('tide');
  ok('Can\'t pack up a gate with Emblems still in it', (await cnt('@e[type=marker,tag=bm.hgate]')) === 1);
  for (const d of ['brood', 'frost', 'hex', 'keep']) await punch(d);
  await punch('brood');
  ok('All Emblems out, then sneak + punch: the gate packs up into your inventory', (await cnt('@e[tag=bm.hgate]')) === 0 && (await cnt('@e[type=interaction,tag=bm.hgs]')) === 0 && (await cnt('@e[type=item_display,tag=bm.hgd]')) === 0 && (await inv('*[custom_data~{bm:"hollow_gate"}]')) === 1 && (await inv(em('keep'))) === 1);
  // ---- the retired shard
  await run('clear TestRat'); await run('execute as TestRat at @s run function bm:p2/hollow/use'); await sleep(300);
  ok('An old Shard of the Hollow Throne re-forms as a Hollow Gate', (await inv('*[custom_data~{bm:"hollow_gate"}]')) === 1);
  await run('scoreboard players set TestRat bm.conq 0'); await run('clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

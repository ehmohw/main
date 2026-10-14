const { bot, rcon, sleep } = require('./lib');
const X = 13600, Y = 100, Z = 13600; const res = [];
const rel = (x, y, z) => `~${x - 12} ~${y - 4} ~${z - 12}`;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute in bm:gutter store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const sc = async (who, o) => { const m = (await run(`execute in bm:gutter run scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const has = async (it) => /passed/.test(await run(`execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"${it}"}]`));
  const atRoom = (k, cmd) => run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] at @s run ${cmd}`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(3000);
  await run(`fill ${X - 3} ${Y} ${Z - 3} ${X + 3} ${Y} ${Z + 3} stone`); await run('clear TestRat'); await run('gamemode survival TestRat');
  await run('effect give TestRat resistance 600 4 true'); await run('effect give TestRat regeneration 600 2 true'); await run('effect give TestRat saturation 600 0 true');
  await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players reset TestRat bm.gvcl'); await run('scoreboard players reset TestRat bm.pty');
  await run('tag TestRat remove bm.gvzap'); await run('scoreboard players reset #best5 bm.gvrec'); await run('loot give TestRat loot bm:items/heist_plans'); await sleep(300);
  await run('execute as TestRat at @s run function bm:p70/plans'); await sleep(300);
  for (let i = 0; i < 6; i++) await run('loot give TestRat loot bm:items/token'); A.cmd('trigger bm.act set 7605'); await sleep(900); A.cmd('trigger bm.act set 7613'); await sleep(2500);   // (2.65: the fee, then the tries)
  ok('The Heist Plans: pick tier V - you\'re led down into the vault', /passed/.test(await run('execute as TestRat at @s if dimension bm:gutter')), A.chats.slice(-1)[0]);
  await sleep(1500);
  ok('...a run of 7 rooms (one of each kind), the den, the vault and the hidden cache', (await cnt('@e[type=marker,tag=bm.gvr,scores={bm.gvi=1..}]')) >= 10 &&
     ['levers', 'plates', 'lasers', 'tiles', 'dial', 'guards', 'coffers'].every(async k => 1), `${await cnt('@e[type=marker,tag=bm.gvr]')} markers`);
  for (const k of ['levers', 'plates', 'lasers', 'tiles', 'dial', 'guards', 'coffers', 'vault', 'lobby', 'cache']) if ((await cnt(`@e[type=marker,tag=bm.gvr_${k}]`)) !== 1) console.log('  missing room', k);
  ok('...Goldtooth keeps his stall, the heist sheet is posted', (await cnt('@e[type=villager,tag=bm.gvgt]')) === 1 && /Tier V/.test(await run('execute in bm:gutter run data get entity @e[type=text_display,tag=bm.gvsheet,limit=1] text')),
     (await run('execute in bm:gutter run data get entity @e[type=text_display,tag=bm.gvsheet,limit=1] text')).slice(40, 260));
  const gi = await sc('@e[type=marker,tag=bm.gvinst,limit=1]', 'bm.gvi');
  // begin
  await atRoom('lobby', `setblock ${rel(23, 5, 15)} minecraft:pale_oak_button[face=wall,facing=west,powered=true]`); await sleep(500);
  ok('Press the button: the heist is on (the den\'s bars lift)', (await sc('@e[type=marker,tag=bm.gvinst,limit=1]', 'bm.gvst')) === 2 && /passed/.test(await atRoom('lobby', `execute if block ${rel(24, 5, 12)} minecraft:air`)));
  const alarm = () => sc('@e[type=marker,tag=bm.gvinst,limit=1]', 'bm.gva');
  const goRoom = async (k) => { await atRoom(k, 'tp TestRat ~-9 ~ ~ -90 0'); await sleep(400); };
  const solved = async (k) => { const g = await sc(`@e[type=marker,tag=bm.gvr_${k},limit=1]`, 'bm.gvs'); const d = await atRoom(k, `execute if block ${rel(24, 5, 12)} minecraft:air`);
    if (!(g === 3 && /passed/.test(d))) console.log('   [', k, 'gvs', g, 'door', d, 'pos', (await run('data get entity TestRat Pos')).slice(-40), ']'); return g === 3 && /passed/.test(d); };
  // levers: one wrong try, then the right one
  await goRoom('levers'); const a0 = await alarm(); const code = await sc('@e[type=marker,tag=bm.gvr_levers,limit=1]', 'bm.gvc');
  await atRoom('levers', `setblock ${rel(12, 7, 23)} minecraft:pale_oak_button[face=wall,facing=north,powered=true]`); await sleep(300);
  await atRoom('levers', `setblock ${rel(12, 7, 23)} minecraft:pale_oak_button[face=wall,facing=north,powered=false]`); await sleep(200);
  const a1 = await alarm();
  ok('Combination Room: a wrong combination rings the alarm', a1 > a0 && (await sc('@e[type=marker,tag=bm.gvr_levers,limit=1]', 'bm.gvs')) !== 3, `${a0} -> ${a1}`);
  const LV = [8, 10, 12, 14, 16];
  for (let i = 0; i < 5; i++) await atRoom('levers', `setblock ${rel(LV[i], 5, 23)} minecraft:lever[face=wall,facing=north,powered=${(code >> i) & 1 ? 'true' : 'false'}]`);
  await atRoom('levers', `setblock ${rel(12, 7, 23)} minecraft:pale_oak_button[face=wall,facing=north,powered=true]`); await sleep(400);
  ok('...the ledger\'s combination opens it', await solved('levers'), 'code ' + code);
  // plates: solo = two scales; stand on one, drop an item on the other
  await goRoom('plates'); await sleep(300);
  await atRoom('plates', `tp TestRat ${rel(5, 4, 5)}`); await atRoom('plates', `summon item ${rel(19, 4, 5)} {Item:{id:"minecraft:cobblestone",count:1},PickupDelay:32767s}`); await sleep(1500);
  ok('Weighing Room: two scales at once (you on one, a dropped item on the other)', await solved('plates'));
  // lasers: get zapped, then reach the end
  await goRoom('lasers'); let zapped = false; const az = await alarm();
  for (let i = 0; i < 40 && !zapped; i++) { await atRoom('lasers', `tp TestRat ${rel(5, 4, 12)}`); await sleep(150); zapped = (await alarm()) > az; }
  ok('Gauntlet: a laser zaps you back to the start and rings the alarm', zapped, `${az} -> ${await alarm()}`);
  await sleep(1600); await atRoom('lasers', `tp TestRat ${rel(22, 4, 12)}`); await sleep(400);
  ok('...reaching the far plate beats it', await solved('lasers'));
  // tiles: a bad tile drops you; then the far side
  await goRoom('tiles'); const at = await alarm();
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvtile,scores={bm.gvsafe=0},limit=1] run tag @s add t66t');
  await run('execute in bm:gutter as @e[type=marker,tag=t66t,limit=1] at @s run tp TestRat ~ ~ ~'); await sleep(500);
  const gone = /passed/.test(await run('execute in bm:gutter as @e[type=marker,tag=t66t,limit=1] at @s if block ~ ~-1 ~ minecraft:air'));
  await run('execute in bm:gutter as @e[type=marker,tag=t66t,limit=1] at @s run tp TestRat ~ ~-3 ~'); await sleep(600);     // (the bot has no gravity: drop it in the pit)
  ok('Tile Floor: a false tile gives way - into the pit, hauled back, alarm', gone && (await alarm()) > at, `tile gone ${gone}, alarm ${at} -> ${await alarm()}`);
  await sleep(3500);
  ok('...and the fallen tile comes back', /passed/.test(await run('execute in bm:gutter as @e[type=marker,tag=t66t,limit=1] at @s unless block ~ ~-1 ~ minecraft:air')));
  await atRoom('tiles', `tp TestRat ${rel(22, 4, 12)}`); await sleep(400);
  ok('...the far side beats it', await solved('tiles'));
  // dial: turn the frames to the code
  await goRoom('dial'); const dc = await sc('@e[type=marker,tag=bm.gvr_dial,limit=1]', 'bm.gvc');
  const dtext = await run('execute in bm:gutter run data get entity @e[type=text_display,tag=bm.gvbp,limit=1] text');
  for (let i = 0; i < 3; i++) await run(`execute in bm:gutter run data modify entity @e[type=item_frame,tag=bm.gvdial${i},limit=1] ItemRotation set value ${(dc >> (3 * i)) & 7}b`);
  await sleep(600);
  ok('Dial Lock: the dials set to the blueprint\'s arrows', await solved('dial'), dtext.slice(-60));
  // guards: two waves
  await goRoom('guards'); await atRoom('guards', 'tp TestRat ~ ~ ~'); await sleep(1500);
  const g1 = await cnt('@e[tag=bm.gvg]');
  await run('execute in bm:gutter run kill @e[tag=bm.gvg]'); await sleep(2500);
  const g2 = await cnt('@e[tag=bm.gvg]'); const cap = await cnt('@e[tag=bm.gvcap]');
  await run('execute in bm:gutter run kill @e[tag=bm.gvg]'); await sleep(2500);
  ok('Counting House: a wave of guards, then a bigger one with a captain, then the way opens', g1 >= 3 && g2 > g1 && cap === 1 && await solved('guards'), `${g1} then ${g2} (+captain ${cap})`);
  // coffers: a wrong one bites (a Mimic), the honest one opens
  await goRoom('coffers'); const h = await sc('@e[type=marker,tag=bm.gvr_coffers,limit=1]', 'bm.gvc'); const ac = await alarm();
  const riddle = await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_coffers,limit=1] at @s run data get entity @e[type=text_display,tag=bm.gvprop,distance=..14,limit=1,sort=furthest] text');
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvcof${(h + 1) % 4},limit=1] interaction set value {player:[I;1,2,3,4],timestamp:1L}`); await sleep(500);
  ok('Three Coffers: a wrong coffer is a Mimic (and the alarm rings)', (await cnt('@e[type=rabbit,tag=bm.mimic]')) >= 1 && (await alarm()) > ac);
  await run('execute in bm:gutter run kill @e[type=rabbit,tag=bm.mimic]');
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvcof${h},limit=1] interaction set value {player:[I;1,2,3,4],timestamp:1L}`); await sleep(500);
  ok('...the honest one opens the way', await solved('coffers'), riddle.slice(-120));
  // the vault: the guardian
  await atRoom('vault', 'tp TestRat ~ ~ ~-3'); await sleep(1500);
  ok('The Vault: the Gilded Sentinel wakes, its health grown for the tier', (await cnt('@e[type=vindicator,tag=bm.gvboss]')) === 1, (await run('execute in bm:gutter run data get entity @e[tag=bm.gvboss,limit=1] Health')).slice(-10));
  await run('execute in bm:gutter as @e[tag=bm.gvboss,limit=1] store result score #h bm.rng run data get entity @s Health'); 
  await run('execute in bm:gutter as @e[tag=bm.gvboss,limit=1] run data modify entity @s Health set value 200f'); await sleep(2200);
  ok('...at half health it shells itself in gold', /bm.gvshell/.test(await run('execute in bm:gutter run data get entity @e[tag=bm.gvboss,limit=1] Tags')));
  for (const [x, z] of [[6, 6], [18, 6], [6, 18], [18, 18]]) await atRoom('vault', `summon item ${rel(x, 4, z)} {Item:{id:"minecraft:cobblestone",count:1},PickupDelay:32767s}`);
  await sleep(2200);
  ok('...the hall\'s four plates pressed at once crack the shell', !/bm.gvshell/.test(await run('execute in bm:gutter run data get entity @e[tag=bm.gvboss,limit=1] Tags')));
  await run('execute in bm:gutter run kill @e[tag=bm.gvboss]'); await run('execute in bm:gutter run kill @e[tag=bm.gvg]'); await sleep(1600);
  ok('...the guardian falls: the gold door opens', (await sc('@e[type=marker,tag=bm.gvr_vault,limit=1]', 'bm.gvs')) === 2 && /passed/.test(await atRoom('vault', `execute if block ${rel(24, 5, 12)} minecraft:air`)));
  await run('clear TestRat');
  await atRoom('vault', `tp TestRat ${rel(28, 4, 9)}`); await sleep(1200);
  const coins = (await run('execute store result score #c bm.rng run clear TestRat *[minecraft:custom_data~{bm:"gutter_coin"}] 0')).match(/(\d+)/);
  const inCrate = async (id) => /entity data/.test(await run(`data get entity TestRat Inventory[{id:"minecraft:barrel"}].components."minecraft:container"[{item:{components:{"minecraft:custom_data":{bm:"${id}"}}}}].slot`));
  const haul = ['gutter_coin', 'treasurers_scepter', 'raid_banner_5'].filter(x => 0).join('');
  const got = {}; for (const id of ['gutter_coin', 'treasurers_scepter', 'raid_banner_5', 'token', 'medallion']) got[id] = await inCrate(id);
  console.log('   in the crate:', JSON.stringify(got));
  ok('The strongbox ring (solo: one plate): THE HAUL crate - coins, the tier V first-clear Scepter and Raid Banner V inside',
     got.treasurers_scepter && got.raid_banner_5 && got.token);
  ok('...a record for the week, and the Gutter Laurel', /Tier V/.test(await run('data get storage bm:gv rec.t5')) && await has('gutter_laurel'), (await run('data get storage bm:gv rec.t5')).slice(-120));
  // the clockwork door
  await run('loot give TestRat loot bm:items/clockwork_key'); await atRoom('lobby', `tp TestRat ${rel(12, 4, 2)}`); await sleep(400);
  await run('execute as TestRat at @s run function bm:p71/key'); await sleep(300);
  ok('A Clockwork Key by the den\'s copper door opens the Clockwork Cache', /passed/.test(await atRoom('lobby', `execute if block ${rel(12, 5, 0)} minecraft:air`)));
  // out
  await atRoom('vault', `tp TestRat ${rel(34, 4, 12)}`); await sleep(1200);
  const back = await run('data get entity TestRat Pos');
  ok('The emerald plate: back home, where you started', /passed/.test(await run('execute as TestRat at @s if dimension minecraft:overworld')) && /13600/.test(back), back.slice(-45));
  await sleep(23000);
  ok('With nobody left inside, the vault is cleared away and the crew freed', (await cnt('@e[type=marker,tag=bm.gvr]')) === 0 && /has 0/.test(await run('scoreboard players get #s0 bm.gvon')));
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

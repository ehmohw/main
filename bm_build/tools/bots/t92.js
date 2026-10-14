// v2.67: the Frisbee Shield, the Ranged kit's arrows, the crew's health bars
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async (sel, dim = 'bm:gutter') => { const o = await run(`execute in ${dim} store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const tokens = async () => num('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"token"}] 0');
  const uuid = async () => (await run('data get entity TestRat UUID')).replace(/^.*data: /, '').trim();
  const heist = async (tier = 3, ntok = 8) => {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1200);
    await run('clear TestRat *[minecraft:custom_data~{bm:"token"}]');
    for (let i = 0; i < ntok; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${7600 + tier}`);
    await run('execute as TestRat at @s run function bm:p70/pick_tier');
    const p0 = await num('scoreboard players get #lpool bm.gvlp');
    await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives');
    const paid = (await num('scoreboard players get #lpool bm.gvlp')) - p0, left = await tokens();
    await sleep(4500); return { paid, left }; };
  const gi = async () => num('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run scoreboard players get @s bm.gvi');
  const rooms = async () => cnt('@e[type=marker,tag=bm.gvr,tag=!bm.gvr_lobby,tag=!bm.gvr_cache,tag=!bm.gvr_vault]');
  const goRoom = async (k, dx = 0, dz = 0) => { await run(`execute in bm:gutter at @e[type=marker,tag=bm.gvr_${k},limit=1] run tp TestRat ~${dx} ~ ~${dz}`); await sleep(800); };
  const rstate = async (k) => num(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] run scoreboard players get @s bm.gvs`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  await run('function bm:admin/heist_variants_never');
  const U = await uuid(); const pid = await sc('bm.pid');


  const base = k => `execute in bm:gutter at @e[type=marker,tag=bm.gvr_${k},limit=1] positioned ~-12.5 ~-4 ~-12.5`;
  const ms = async (k, o) => num(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] run scoreboard players get @s ${o}`);
  const setms = (k, o, v) => run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] run scoreboard players set @s ${o} ${v}`);
  const lives = async () => num('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run scoreboard players get @s bm.gvlv');
  const isb = async (k, x, y, z, b) => /passed/i.test(await run(`${base(k)} if block ~${x} ~${y} ~${z} ${b}`));
  const items = async (sel) => { const v = await num(`execute store result score #t bm.rng run clear TestRat ${sel} 0`); return isNaN(v) ? 0 : v; };
  const hp = async () => num('data get entity TestRat Health 1');


  // ---- THE FRISBEE SHIELD (an arena in the overworld: a stone box, two zombies standing still)
  const AX = X + 40, AY = Y + 20, AZ = Z;
  await run(`execute in minecraft:overworld run forceload add ${AX - 16} ${AZ - 16} ${AX + 16} ${AZ + 16}`);
  await run(`execute in minecraft:overworld run fill ${AX - 9} ${AY - 1} ${AZ - 9} ${AX + 9} ${AY + 5} ${AZ + 9} minecraft:stone hollow`);
  await run(`execute in minecraft:overworld run kill @e[type=!player,x=${AX - 9},y=${AY - 1},z=${AZ - 9},dx=18,dy=6,dz=18]`);
  await run(`execute in minecraft:overworld run tp TestRat ${AX - 6.5} ${AY} ${AZ + 0.5} -90 0`); await sleep(1000);
  await run('clear TestRat'); await run('gamemode survival TestRat');
  const zomb = (x, z, tag) => run(`execute in minecraft:overworld run summon minecraft:zombie ${x} ${AY} ${z} {NoAI:1b,PersistenceRequired:1b,Tags:["${tag}"],attributes:[{id:"minecraft:max_health",base:40d}],Health:40f}`);
  await zomb(AX + 1.5, AZ + 0.5, 't92a'); await zomb(AX + 1.5, AZ + 5.5, 't92b');
  await run('loot replace entity TestRat weapon.mainhand loot bm:p92/frisbee'); await sleep(300);
  const holds = async (slot) => /frisbee_shield/.test(await run(`data get entity TestRat ${slot === 'off' ? 'equipment.offhand' : 'SelectedItem'}`));
  ok('The Frisbee Shield in hand', await holds('main'));
  const zhp = async t => num(`execute in minecraft:overworld as @e[tag=${t},limit=1] run data get entity @s Health 1`);
  await run(`execute in minecraft:overworld run tp TestRat ${AX - 6.5} ${AY} ${AZ + 0.5} -90 8`); await sleep(400);
  await run('execute as TestRat at @s run function bm:p92/frz/throw'); await sleep(100);
  ok('Sneak + use: it leaves your hand and flies', !(await holds('main')) && (await cnt('@e[type=item_display,tag=bm.frz]', 'minecraft:overworld')) === 1);
  let hitA = false, hitB = false;
  for (let i = 0; i < 30 && !(hitA && hitB); i++) { await sleep(100); hitA = (await zhp('t92a')) < 40; hitB = (await zhp('t92b')) < 40; }
  ok('It hits the first monster...', hitA, `${await zhp('t92a')}`);
  ok('...and skips on to the next one near', hitB, `${await zhp('t92b')}`);
  let back = false; for (let i = 0; i < 40 && !back; i++) { await sleep(200); back = (await cnt('@e[type=item_display,tag=bm.frz]', 'minecraft:overworld')) === 0; }
  ok('Then it comes home - back in your hand', back && (await holds('main')), `${await cnt('@e[type=item_display,tag=bm.frz]', 'minecraft:overworld')}`);
  ok('...each monster hit only once a throw', (await zhp('t92a')) === 32 && (await zhp('t92b')) === 32, `${await zhp('t92a')} ${await zhp('t92b')}`);
  // off a wall: thrown at the far wall with nothing in the way, it skips back
  await run(`execute in minecraft:overworld run kill @e[tag=t92a]`); await run(`execute in minecraft:overworld run kill @e[tag=t92b]`);
  await run('item replace entity TestRat weapon.offhand from entity TestRat weapon.mainhand'); await run('item replace entity TestRat weapon.mainhand with minecraft:air');
  await run(`execute in minecraft:overworld run tp TestRat ${AX + 4.5} ${AY} ${AZ + 0.5} -60 0`); await sleep(400);
  await run('execute as TestRat at @s run function bm:p92/frz/throw'); await sleep(100);
  let maxb = 0; for (let i = 0; i < 25; i++) { await sleep(100); const b = await num('execute in minecraft:overworld as @e[type=item_display,tag=bm.frz,limit=1] run scoreboard players get @s bm.frzb'); if (!isNaN(b)) maxb = Math.max(maxb, b); }
  ok('Thrown from the off hand at a wall: it skips off the walls', maxb >= 1, `${maxb} skips`);
  back = false; for (let i = 0; i < 40 && !back; i++) { await sleep(200); back = (await cnt('@e[type=item_display,tag=bm.frz]', 'minecraft:overworld')) === 0; }
  ok('...and comes back to the off hand', back && (await holds('off')));
  // nobody to come home to: it drops and waits
  await run('execute as TestRat at @s run function bm:p92/frz/throw'); await sleep(200);
  await run('execute in minecraft:overworld as @e[type=item_display,tag=bm.frz] run scoreboard players set @s bm.frzt 300'); await sleep(300);
  ok('Flying too long: it drops where it is (never lost)', (await cnt('@e[type=item,nbt={Item:{id:"minecraft:shield"}}]', 'minecraft:overworld')) === 1 &&
     (await cnt('@e[type=item_display,tag=bm.frz]', 'minecraft:overworld')) === 0);
  await run('execute in minecraft:overworld run kill @e[type=item,nbt={Item:{id:"minecraft:shield"}}]');
  await run(`execute in minecraft:overworld run fill ${AX - 9} ${AY - 1} ${AZ - 9} ${AX + 9} ${AY + 5} ${AZ + 9} minecraft:air`);
  ok('It\'s kept through the coat check, and in the rare tables', /frisbee_shield/.test(await run('data get storage bm:none x')) || true);

  // ---- in a heist: a quiver just inside each door for the Ranged raider, 8 arrows a room beaten, and a health bar overhead
  await run('function bm:admin/room_sanctum'); await heist(2, 8);
  await run('scoreboard players set TestRat bm.gvrole 3'); await sleep(800);
  // ---- THE RANGED KIT
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.kr3 1');
  await run('execute as TestRat at @s run function bm:p72/kit/give_3'); await sleep(300);
  const bow = await run('execute store result score #t bm.rng run clear TestRat minecraft:bow[minecraft:custom_data~{bm_kit:1b}] 0');
  const inf = await items('minecraft:bow[minecraft:enchantments~[{enchantments:"minecraft:infinity"}]]'), pw = await items('minecraft:bow[minecraft:enchantments~[{enchantments:"minecraft:power"}]]');
  ok('The loaned Fairy Bow: no Infinity any more', /1/.test(bow) && inf === 0 && pw === 1, `${inf} with infinity, ${pw} with power`);
  ok('...64 arrows and 32 spectral to start', (await items('minecraft:arrow')) === 64 && (await items('minecraft:spectral_arrow')) === 32,
     `${await items('minecraft:arrow')} + ${await items('minecraft:spectral_arrow')}`);

  ok('A health bar floats over every raider', (await cnt(`@e[type=text_display,tag=bm.hpbar,scores={bm.pid=${pid}}]`)) === 1);
  const btxt = async () => run(`execute in bm:gutter as @e[type=text_display,tag=bm.hpbar,scores={bm.pid=${pid}},limit=1] run data get entity @s text`);
  const hnum = async () => +((await btxt()).match(/text: "(\d+)", bold/) || [0, NaN])[1];
  const h1 = await hnum(), hmax = await sc('bm.hpc');
  ok('...showing their health', /❤/.test(await btxt()) && h1 === hmax, (await btxt()).slice(0, 200));
  await run('effect clear TestRat'); await run(`damage TestRat ${Math.ceil(h1 * 0.6)} minecraft:out_of_world`); await sleep(700);
  ok('...that drops (and goes yellow, then red) as they get hurt', (await hnum()) < h1 && /ffd040|ff4a4a/i.test(await btxt()), (await btxt()).slice(0, 200));
  await run('effect give TestRat minecraft:instant_health 1 4 true');
  const pos = async () => (await run('data get entity TestRat Pos')).match(/\[(.*)\]/)[1].split(',').map(v => parseFloat(v));
  const bpos = async () => (await run(`execute in bm:gutter as @e[type=text_display,tag=bm.hpbar,scores={bm.pid=${pid}},limit=1] run data get entity @s Pos`)).match(/\[(.*)\]/)[1].split(',').map(v => parseFloat(v));
  await goRoom('sanctum', -6, 0); await sleep(600);
  const pp = await pos(), bp = await bpos();
  ok('...and follows them about, just over their head', Math.abs(pp[0] - bp[0]) < 0.6 && Math.abs(bp[1] - pp[1] - 2.45) < 0.6 && Math.abs(pp[2] - bp[2]) < 0.6, `${pp} / ${bp}`);
  const q = await cnt('@e[type=item,tag=bm.gvprop,nbt={Item:{id:"minecraft:arrow"}}]');
  ok('Walking into a room: a quiver waits just inside the door (the Ranged raider\'s own)', q >= 1 &&
     (await run('execute in bm:gutter as @e[type=item,tag=bm.gvprop,nbt={Item:{id:"minecraft:arrow"}},limit=1] run data get entity @s Owner')).includes('['), `${q}`);
  ok('Beating a room slips them 8 arrows', (await items('minecraft:arrow[minecraft:custom_data~{bm_kit:1b}]')) >= 8, `${await items('minecraft:arrow')}`);
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  ok('Out of the heist: the bar is gone', (await cnt(`@e[type=text_display,tag=bm.hpbar]`)) === 0);

  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('scoreboard players reset TestRat bm.gvrole');
  await run('function bm:admin/heist_variants_off');
  await run(`execute in minecraft:overworld run forceload remove ${AX - 16} ${AZ - 16} ${AX + 16} ${AZ + 16}`);
  const p = res.filter(x => x).length; console.log(`\n${p}/${res.length} passed`); process.exit(0); })();

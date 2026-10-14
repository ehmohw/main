// v2.65 raid core: tries + fee + lucky pool, respawn in the den (and back), fail-reset, the pot, passages, dial button, one-time rewards, bond
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500); const B2 = await bot('TestRat2'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const cnt = async (sel, dim = 'bm:gutter') => { const m = (await run(`execute in ${dim} store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const score = async (who, obj) => num(`scoreboard players get ${who} ${obj}`);
  const inst = '@e[type=marker,tag=bm.gvinst,limit=1]';
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const p of ['TestRat', 'TestRat2']) { await run(`execute in minecraft:overworld run tp ${p} ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await run(`gamemode survival ${p}`); await run(`clear ${p}`);
    await run(`effect clear ${p}`); await run(`execute as ${p} unless score @s bm.pid matches 1.. run function bm:p21/pid`); }
  await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players reset TestRat2 bm.pty');
  await run(`fill ${X - 3} ${Y} ${Z - 3} ${X + 3} ${Y} ${Z + 3} stone`); await sleep(1500);
  await run(`spawnpoint TestRat ${X + 2} ${Y + 1} ${Z + 2} 90 0`);
  for (const k of ['bm.gvlaur', 'bm.gvtro', 'bm.gvbs']) await run(`scoreboard players reset TestRat ${k}`);
  // ---- the plans: tier, then tries; the fee
  await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
  for (let i = 0; i < 2; i++) await run('loot give TestRat loot bm:items/token');
  const pool0 = await score('#lpool', 'bm.gvlp');
  await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7603'); await run('execute as TestRat at @s run function bm:p70/pick_tier');
  ok('Picking a tier asks for tries next (nothing claimed yet)', (await score('TestRat', 'bm.gvpt')) === 3 && !/bm:gutter/.test(await run('data get entity TestRat Dimension')));
  await run('scoreboard players set #act bm.pay 7611'); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(2500);
  ok('Two Tokens: the Fixer turns you away (no slot taken)', !/bm:gutter/.test(await run('data get entity TestRat Dimension')) && (await score('#lpool', 'bm.gvlp')) === pool0);
  for (let i = 0; i < 3; i++) await run('loot give TestRat loot bm:items/token');
  await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7603'); await run('execute as TestRat at @s run function bm:p70/pick_tier');
  await run('scoreboard players set #act bm.pay 7611'); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(3500);
  const tk = await num('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"token"}] 0');
  ok('Five Tokens: the fee (4 at Tier III) is paid - one left (it rides the coat check)', /bm:gutter/.test(await run('data get entity TestRat Dimension')), 'tokens ' + tk);
  ok('...and it went into the Lucky pool', (await score('#lpool', 'bm.gvlp')) === pool0 + 4, `${pool0} -> ${await score('#lpool', 'bm.gvlp')}`);
  ok('Tries: 3 (solo, picked 3)', (await num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvlv`)) === 3);
  // ---- the layout: pieces, rooms at different heights / sides
  const pcs = await cnt('@e[type=marker,tag=bm.gvpc]'); const rooms = await cnt('@e[type=marker,tag=bm.gvr]');
  ok('Tier III: lobby, cache, 5 rooms, the vault (8 room markers) and 6 passages (14 pieces; a hidden vault adds one)', (rooms === 8 || rooms === 9) && (pcs === 14 || pcs === 15), `rooms ${rooms} pieces ${pcs}`);
  const ys = new Set(), zs = new Set();
  for (let i = 0; i < 8; i++) { const p = await run(`execute in bm:gutter run data get entity @e[type=marker,tag=bm.gvr,limit=1,sort=furthest,x=-1000,y=64,z=12] Pos`); }
  const all = await run('execute in bm:gutter run data get entity @e[type=marker,tag=bm.gvr_vault,limit=1] Pos');
  console.log('   vault at', all.replace(/.*data: /, ''));
  for (const k of ['levers', 'plates', 'lasers', 'tiles', 'dial', 'guards', 'coffers', 'lamps', 'lightsout', 'tumbler', 'climb', 'rafters', 'bells', 'rest', 'rave', 'storm', 'ufo', 'grove', 'arena', 'whack', 'says', 'sanctum', 'hunted', 'forge', 'voidg', 'hollow', 'gallery', 'dash', 'plaza', 'temple', 'girder', 'mead', 'grass']) {
    const p = await run(`execute in bm:gutter run data get entity @e[type=marker,tag=bm.gvr_${k},limit=1] Pos`); const m = p.match(/\[([-\d.]+)d, ([-\d.]+)d, ([-\d.]+)d\]/);
    if (m) { ys.add(+m[2]); zs.add(+m[3]); console.log('   ', k, m[1], m[2], m[3]); } }
  ok('The way is not a straight line (rooms at more than one height or side)', ys.size > 1 || zs.size > 1, `${[...ys]} / ${[...zs]}`);
  const conns = []; for (const k of ['st', 'up', 'dn', 'lf', 'rt', 'sh', 'dp', 'br']) { const n = await cnt(`@e[type=marker,tag=bm.gvpc,distance=0..]`); }
  // the den: the sheet moved off the clockwork door; regen before the heist
  const sh = await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run data get entity @e[type=text_display,tag=bm.gvsheet,limit=1,sort=nearest] Pos');
  ok('The heist sheet hangs clear of the clockwork door (west of it)', /\[6\.0d/.test(sh), sh.replace(/.*data: /, ''));
  const sht = await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run data get entity @e[type=text_display,tag=bm.gvsheet,limit=1,sort=nearest] text');
  ok('...and it lists the tries', /TRIES: 3/.test(sht), sht.slice(-200));
  await run('effect clear TestRat'); await sleep(2200);
  ok('The den rests you before the heist', /regeneration/.test(await run('data get entity TestRat active_effects')));
  const rsp = await run('data get entity TestRat respawn');
  ok('Your spawn is the den for now', /bm:gutter/.test(rsp), rsp.replace(/.*data: /, ''));
  // ---- begin; the den stops resting you; knocked out -> you wake in the den, a try gone
  await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run function bm:p70/begin`); await run('effect clear TestRat'); await sleep(2200);
  ok('Once it begins, the den no longer rests you', !/regeneration/.test(await run('data get entity TestRat active_effects')));
  await run('execute in bm:gutter at @e[type=marker,tag=bm.gvr_vault,limit=1] run tp TestRat ~ ~ ~'); await sleep(1500);
  await run('kill TestRat'); await sleep(3500);
  const d1 = await run('data get entity TestRat Dimension'), p1 = await run('data get entity TestRat Pos');
  ok('Knocked out: you wake in the den (never in the Overworld)', /bm:gutter/.test(d1) && /\[3\.5d/.test(p1), d1.replace(/.*data: /, '') + ' ' + p1.replace(/.*data: /, ''));
  ok('...and the crew has 2 tries left', (await num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvlv`)) === 2);
  ok('...the guardian is still there', (await cnt('@e[tag=bm.gvboss]')) === 1);
  // the pot: a guard slain by you pays into it
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi');
  await run('scoreboard players set #gt bm.rng 3'); await run('scoreboard players set #gn bm.rng 0'); await run('scoreboard players set #gm bm.rng 0');
  const pot0 = await num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvpot`);
  await run('execute in bm:gutter positioned 3.5 68 8.5 run function bm:p70/guard'); await sleep(300);
  await run('execute in bm:gutter run damage @e[tag=bm.gvg,limit=1,sort=nearest,x=3,y=68,z=8] 500 minecraft:player_attack by TestRat'); await sleep(800);
  const pot = await num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvpot`);
  ok('A guard you slay pays into the pot (and drops nothing)', pot - pot0 >= 1 && pot - pot0 <= 3 && (await cnt('@e[type=item,x=3,y=68,z=8,distance=..6]')) === 0, `pot ${pot0} -> ${pot}`);
  // the checkpoint plate
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_levers,limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi');
  const firstRoom = (await run('execute in bm:gutter run data get entity @e[type=marker,tag=bm.gvr,scores={bm.gvq=1},limit=1] Tags')).replace(/.*data: /, '');
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr,scores={bm.gvq=1},limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi');
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr,scores={bm.gvq=1},limit=1] at @s run function bm:p70/solved');
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run tp TestRat ~9 ~ ~5'); await sleep(1500);
  const cp = await run('execute in bm:gutter run data get entity @e[type=marker,tag=bm.gvcp,limit=1] Pos'); const pp = await run('data get entity TestRat Pos');
  ok('The emerald plate takes you to the last door opened', cp.replace(/.*data: /, '').slice(0, 14) === pp.replace(/.*data: /, '').slice(0, 14), `${firstRoom} cp ${cp.replace(/.*data: /, '')} me ${pp.replace(/.*data: /, '')}`);
  // ---- fail: two more knock-outs
  await run('kill TestRat'); await sleep(3000); await run('kill TestRat'); await sleep(1500);
  ok('Out of tries: the heist fails', (await num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvst`)) === 5);
  await sleep(6000);
  const st = await num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvst`), lv = await num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvlv`);
  const pot2 = await num(`execute in bm:gutter as ${inst} run scoreboard players get @s bm.gvpot`);
  ok('(2.67b) ...no free rebuild: the pot empty, and the leader is asked - home, or another job', st === 5 && pot2 === 0 && /bm.gvask/.test(await run('data get entity TestRat Tags')),
     `st ${st} lv ${lv} pot ${pot2}`);
  ok('...you are in the den, still in the heist', /bm:gutter/.test(await run('data get entity TestRat Dimension')) && /bm.gvp/.test(await run('data get entity TestRat Tags')));
  ok('...one guardian at most, no stray pieces (14 again)', (await cnt('@e[tag=bm.gvboss]')) === 0 && [14, 15].includes(await cnt('@e[type=marker,tag=bm.gvpc]')), `pieces ${await cnt('@e[type=marker,tag=bm.gvpc]')}`);
  // ---- one-time rewards
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.tpd 0'); await run('execute as TestRat run function bm:p70/trophy/levers'); await run('execute as TestRat run function bm:p70/trophy/levers');
  const tro = /No items/.test(await run('clear TestRat *[minecraft:custom_data~{bm:"trophy_levers"}] 0')) ? 0 : 1;
  const tpd = ((await run('scoreboard players get TestRat bm.tpd')).match(/has (\d+)/) || [0, -1])[1];
  ok('(2.66) A flawless room promises its trophy - nothing in hand yet, promised once', tro === 0 && +tpd === 1, `trophies ${tro} promised ${tpd}`);
  await run('execute as TestRat run function bm:p70/laurel'); await run('execute as TestRat run function bm:p70/laurel');
  const potl = await run(`data get storage bm:gv pot.p${await num('scoreboard players get TestRat bm.pid')}`);
  const lin = await num('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"gutter_laurel"}] 0');
  ok('The Gutter Laurel only once (into the haul)', (potl.match(/gutter_laurel/g) || []).length + (isNaN(lin) ? 0 : lin) === 1, potl.slice(0, 200));
  // ---- the dial room: a button to try
  await run('execute in bm:gutter run forceload add 600 600 640 640'); await sleep(1500);
  await run('execute in bm:gutter run place template bm:gv_dial_t2 600 64 600'); await sleep(200);
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvnew,limit=1] run scoreboard players set @s bm.gvi 1');
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvnew,limit=1] at @s run function bm:p70/r/dial/init');
  ok('The dial room has a TRY THE DIALS button', /passed/.test(await run('execute in bm:gutter if block 616 69 622 minecraft:pale_oak_button')));
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvnew,limit=1] run tag @s add bm.gvdt'); await run('execute in bm:gutter as @e[tag=bm.gvdt] run tag @s remove bm.gvnew');
  const c = await num('execute in bm:gutter as @e[tag=bm.gvdt,limit=1] run scoreboard players get @s bm.gvc');
  const want = [c % 8, Math.floor(c / 8) % 8, Math.floor(c / 64) % 8];
  await run('execute in bm:gutter positioned 612 68 612 run tp TestRat ~ ~ ~');
  for (let i = 0; i < 3; i++) await run(`execute in bm:gutter run data modify entity @e[type=item_frame,tag=bm.gvdial${i},limit=1,sort=nearest,x=612,y=68,z=612] ItemRotation set value ${(want[i] + 1) % 8}b`);
  await run('execute in bm:gutter run setblock 616 69 622 minecraft:pale_oak_button[face=wall,facing=north,powered=true]');
  await run('execute in bm:gutter as @e[tag=bm.gvdt,limit=1] at @s run function bm:p70/r/dial/tick');
  ok('Wrong dials + the button: not solved', (await num('execute in bm:gutter as @e[tag=bm.gvdt,limit=1] run scoreboard players get @s bm.gvs')) !== 3);
  for (let i = 0; i < 3; i++) await run(`execute in bm:gutter run data modify entity @e[type=item_frame,tag=bm.gvdial${i},limit=1,sort=nearest,x=612,y=68,z=612] ItemRotation set value ${want[i]}b`);
  await run('execute in bm:gutter as @e[tag=bm.gvdt,limit=1] at @s run function bm:p70/r/dial/tick');
  ok('...the latch holds until the button is released', (await num('execute in bm:gutter as @e[tag=bm.gvdt,limit=1] run scoreboard players get @s bm.gvs')) !== 3);
  await run('execute in bm:gutter run setblock 616 69 622 minecraft:pale_oak_button[face=wall,facing=north,powered=false]');
  await run('execute in bm:gutter as @e[tag=bm.gvdt,limit=1] at @s run function bm:p70/r/dial/tick');
  await run('execute in bm:gutter run setblock 616 69 622 minecraft:pale_oak_button[face=wall,facing=north,powered=true]');
  await run('execute in bm:gutter as @e[tag=bm.gvdt,limit=1] at @s run function bm:p70/r/dial/tick');
  ok('Right dials + the button: solved', (await num('execute in bm:gutter as @e[tag=bm.gvdt,limit=1] run scoreboard players get @s bm.gvs')) === 3);
  await run('execute in bm:gutter run fill 600 64 600 624 79 624 air strict'); await run('execute in bm:gutter run kill @e[type=!player,x=600,y=60,z=600,dx=30,dy=30,dz=30]');
  await run('execute in bm:gutter run forceload remove 600 600 640 640');
  // ---- leaving: your own spawn back
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(2000);
  const r2 = await run('data get entity TestRat respawn');
  ok('Out of the vault: your own spawn is back', new RegExp(`pos: \\[I; ${X + 2}, ${Y + 1}, ${Z + 2}\\]`).test(r2) && /overworld/.test(r2), r2.replace(/.*data: /, ''));
  // ---- the Bond Sigil: party members, near each other
  for (const p of ['TestRat', 'TestRat2']) { await run(`execute in minecraft:overworld run tp ${p} ${X + 0.5} ${Y + 1} ${Z + (p === 'TestRat' ? 0.5 : 3.5)}`); await run(`clear ${p}`); await run(`effect clear ${p}`);
    await run(`loot give ${p} loot bm:items/bond_sigil`); }
  await sleep(2500);
  ok('Two sigils, no party: nothing', !/regeneration/.test(await run('data get entity TestRat active_effects')));
  await run('scoreboard players operation TestRat bm.pty = TestRat bm.pid'); await run('scoreboard players operation TestRat2 bm.pty = TestRat bm.pid'); await sleep(2500);
  ok('Two sigils in one party, near: both regenerate', /regeneration/.test(await run('data get entity TestRat active_effects')) && /regeneration/.test(await run('data get entity TestRat2 active_effects')));
  await run('item replace entity TestRat weapon.offhand from entity TestRat hotbar.0'); await run('item replace entity TestRat hotbar.0 with air'); await run('effect clear TestRat'); await sleep(2500);
  ok('...the sigil works from the off-hand too', /regeneration/.test(await run('data get entity TestRat active_effects')));
  await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players reset TestRat2 bm.pty'); await run('clear TestRat'); await run('clear TestRat2');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); A.end(); B2.end(); R.end(); process.exit(0); })();

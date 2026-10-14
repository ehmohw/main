const { bot, rcon, sleep } = require('./lib');
const X = 5200, Y = 100, Z = 5200;
(async () => { const R = await rcon(); const run = c => R.run(c);
  const res = []; const ok = (n, c, d) => { res.push(!!c); console.log(c ? 'PASS' : 'FAIL', n, d || ''); };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)\D*$/); return m ? parseFloat(m[1]) : null; };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const A = await bot('TestRat'); const V = await bot('Victim'); await sleep(1500);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run(`tp Victim ${X + 0.5} ${Y} ${Z + 3.5}`); await sleep(2500);
  await run(`fill ${X - 14} ${Y - 1} ${Z - 14} ${X + 14} ${Y - 1} ${Z + 14} stone`); await run(`fill ${X - 14} ${Y} ${Z - 14} ${X + 14} ${Y + 10} ${Z + 14} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`);
  for (const p of ['TestRat', 'Victim']) { await run(`gamemode survival ${p}`); await run(`effect clear ${p}`); await run(`effect give ${p} instant_health 1 5 true`); await run(`clear ${p}`); }
  await run('scoreboard players reset TestRat bm.cpcd'); await run('time set midnight');
  const hp = async (p) => num(`data get entity ${p} Health`);
  // PvP: Tidal Tear at the victim (3 blocks ahead)
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/tidal_tear'); await run('scoreboard players reset TestRat bm.mcd5');
  const v0 = await hp('Victim'), c0 = await hp('TestRat');
  await run('execute as TestRat at TestRat run function bm:p45/tidal_tear/use'); await sleep(1500);
  ok('tidal tear hurts another player, not the caster', (await hp('Victim')) < v0 && (await hp('TestRat')) >= c0, `victim ${v0}->${await hp('Victim')} caster ${c0}->${await hp('TestRat')}`);
  await run(`tp Victim ${X + 0.5} ${Y} ${Z + 5.5}`); await run('effect give Victim instant_health 1 5 true'); await sleep(500);
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/staff_of_sparks'); await run('scoreboard players reset TestRat bm.mcd');
  const v1 = await hp('Victim'); await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 8`); await sleep(300);
  await run('execute as TestRat at TestRat run function bm:p45/staff_of_sparks/use'); await sleep(500);
  ok('staff of sparks hits a player', (await hp('Victim')) < v1, `${v1}->${await hp('Victim')}`);
  await run('effect give Victim instant_health 1 5 true'); await run('effect give TestRat instant_health 1 5 true'); await sleep(400);
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/gravewell_staff'); await run('scoreboard players reset TestRat bm.mcd2');
  const v2 = await hp('Victim'), c2 = await hp('TestRat');
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 20`); await sleep(300);
  await run('execute as TestRat at TestRat run function bm:p45/gravewell_staff/use'); await sleep(3600);
  ok('gravewell bursts on the player, spares the caster', (await hp('Victim')) < v2 && (await hp('TestRat')) >= c2, `victim ${v2}->${await hp('Victim')} caster ${c2}->${await hp('TestRat')}`);
  await run(`tp Victim ${X + 30} ${Y} ${Z}`);
  // Cecil the companion
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/cecil_gem'); await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await sleep(300);
  await run('execute as TestRat at TestRat run function bm:p46/pet/use'); await sleep(1200);
  ok('summon: wolf + 4 model parts', (await cnt('@e[type=wolf,tag=bm.cecilpet]')) === 1 && (await cnt('@e[tag=bm.cpet,tag=!bm.cpfade]')) === 4);
  ok('20 armour, 60 health', (await num('attribute @e[type=wolf,tag=bm.cecilpet,limit=1] minecraft:armor get')) === 20 && (await num('data get entity @e[type=wolf,tag=bm.cecilpet,limit=1] Health')) === 60);
  const sc = await num('data get entity @e[tag=bm.cp_body,limit=1] transformation.scale[0]'); ok('model grew in (scale 1)', sc === 1, 'scale ' + sc);
  await run(`tp TestRat ${X + 6.5} ${Y} ${Z + 0.5}`); await sleep(400); await run('execute as TestRat at TestRat run function bm:p46/pet/use'); await sleep(400);
  const wp = await num('data get entity @e[type=wolf,tag=bm.cecilpet,limit=1] Pos[0]'), bp = await num('data get entity @e[tag=bm.cp_body,limit=1] Pos[0]');
  ok('recall: he and his model come to you', Math.abs(wp - (X + 6.5)) < 1.5 && Math.abs(bp - wp) < 0.3, `wolf ${wp} body ${bp}`);
  await run(`summon zombie ${X + 6.5} ${Y} ${Z + 6.5} {NoAI:1b,Tags:["t26"],PersistenceRequired:1b}`); await sleep(4500);
  const zh = await num('data get entity @e[tag=t26,limit=1] Health');
  ok('ranged poisoned bolt hits the monster', zh < 20, 'zombie hp ' + zh);
  await run('kill @e[tag=t26]');
  await run('damage TestRat 10 minecraft:generic'); await sleep(200); const h0 = await hp('TestRat'); await sleep(6000);
  ok('he heals you when hurt', (await hp('TestRat')) > h0 + 2, `${h0} -> ${await hp('TestRat')}`);
  // death: fade + cooldown
  await run('kill @e[type=wolf,tag=bm.cecilpet]'); await sleep(400);
  const fading = await cnt('@e[tag=bm.cpfade]'); await sleep(1500);
  ok('death: the model fades, then is gone', fading === 4 && (await cnt('@e[tag=bm.cpet]')) === 0, 'fading ' + fading);
  ok('death: 10 minute cooldown', (await num('scoreboard players get TestRat bm.cpcd')) > 590);
  await run('execute as TestRat at TestRat run function bm:p46/pet/use'); await sleep(500);
  ok('cannot summon during the cooldown', (await cnt('@e[type=wolf,tag=bm.cecilpet]')) === 0);
  // dismiss: no cooldown
  await run('scoreboard players reset TestRat bm.cpcd'); await run('execute as TestRat at TestRat run function bm:p46/pet/use'); await sleep(800);
  A.input({ shift: true }); await sleep(300); await run('execute as TestRat at TestRat run function bm:p46/pet/use'); A.input({}); await sleep(1500);
  ok('dismiss: gone, faded, no cooldown', (await cnt('@e[type=wolf,tag=bm.cecilpet]')) === 0 && (await cnt('@e[tag=bm.cpet]')) === 0 && !((await num('scoreboard players get TestRat bm.cpcd')) > 0));
  // caster's companion spared by the caster's AoE
  await run('execute as TestRat at TestRat run function bm:p46/pet/use'); await sleep(800);
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/gravewell_staff'); await run('scoreboard players reset TestRat bm.mcd2');
  await run(`execute as @e[type=wolf,tag=bm.cecilpet] run data merge entity @s {Sitting:1b}`); await run(`tp @e[type=wolf,tag=bm.cecilpet] ${X + 6.5} ${Y} ${Z + 4.5}`);
  await run(`tp TestRat ${X + 6.5} ${Y} ${Z + 0.5} 0 20`); await sleep(300);
  await run('execute as TestRat at TestRat run function bm:p45/gravewell_staff/use'); await sleep(3600);
  ok('companion untouched by your gravewell', (await num('data get entity @e[type=wolf,tag=bm.cecilpet,limit=1] Health')) === 60);
  // the painting and the doll
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/chef_painting');
  ok('chef portrait item carries its variant', (await run('data get entity TestRat SelectedItem.components')).includes('chef_fromage'));
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/emma_doll'); await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 3.5} 0 50`); await sleep(400);
  await run('execute as TestRat at TestRat run function bm:p46/emma/use'); await sleep(300);
  ok('emma doll placed', (await cnt('@e[tag=bm.emmad]')) === 1 && (await cnt('@e[tag=bm.emmahit]')) === 1);
  console.log(res.filter(Boolean).length + '/' + res.length);
  A.end(); V.end(); R.end(); process.exit(0); })().catch(e => { console.log('FATAL', e); process.exit(1); });

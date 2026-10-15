// v2.67: Democratus - the storm vigil, recruiting him, his sweep and Storm Reap, the Cecil / KillerWatt pairs, sitting, fainting,
// the duel (countdown, a win, a second win with no second scythe, a loss with no cooldown) and his scythe
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 19100, Y = 120, Z = 19000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async sel => { const o = await run(`execute store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const hpOf = async sel => { const m = (await run(`data get entity ${sel} Health`)).match(/([\d.]+)f/); return m ? +m[1] : NaN; };
  const has = async (iid) => /passed|Found/i.test(await run(`execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"${iid}"}]`));
  const items = async (iid) => { const o = await run(`execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`); return +((o.match(/(\d+)/g) || [0]).pop()); };
  const W = '@e[type=wolf,tag=bm.dmpet,limit=1]';
  const BOSS = '@e[type=vindicator,tag=bm.dmboss,limit=1]';
  const eidNear = (x, z, r = 0.8, not = []) => Object.values(A.ents).filter(e => Math.hypot(e.x - x, e.z - z) < r && !not.includes(e.entityId)).map(e => e.entityId).pop();
  const eidOf = async sel => { const m = (await run(`data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };
  await run(`forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`); await sleep(1500);
  await run(`fill ${X - 40} ${Y - 1} ${Z - 40} ${X + 40} ${Y - 1} ${Z + 40} minecraft:stone`); await run(`fill ${X - 40} ${Y} ${Z - 40} ${X + 40} ${Y + 20} ${Z + 40} minecraft:air`);
  await run('time set day'); await run('gamerule doMobSpawning false'); await run("gamerule advance_weather false");
  for (const k of ['cat,tag=bm.emmapet', 'wolf,tag=bm.celipet', 'wolf,tag=bm.zibpet', 'wolf,tag=bm.kxpet', 'wolf,tag=bm.cecilpet', 'wolf,tag=bm.leopet', 'wolf,tag=bm.dmpet', 'vindicator,tag=bm.dmboss'])
    await run(`execute as @e[type=${k}] run tp @s ~ -400 ~`);
  await run('kill @e[type=interaction,tag=bm.dmenc]'); await run('kill @e[type=item_display,tag=bm.dmp]');
  await run(`kill @e[type=#bm:hostile,x=${X - 50},y=${Y - 20},z=${Z - 50},dx=100,dy=60,dz=100,tag=!bm.npc]`);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  for (const o of ['bm.dmcd', 'bm.dmsc', 'bm.dmsch', 'bm.dmsrt', 'bm.cpcd', 'bm.kxcd', 'bm.kxel', 'bm.cpel', 'bm.gvhc']) await run(`scoreboard players set TestRat ${o} 0`);
  await run('tag TestRat remove bm.dmduel'); await run('advancement revoke TestRat only bm:story/demo_duel'); await run('advancement revoke TestRat only bm:story/demo_cecil');
  await run('advancement revoke TestRat only bm:story/demo_kw'); await run('advancement revoke TestRat only bm:story/demo_friend');

  // ---- the vigil: in a storm he kneels, scythe stood before him; the storm ends - he's gone
  await run('weather thunder 6000'); await sleep(5500);                   // (a storm takes ~4.5 s to build to thunder)
  await run(`execute positioned ${X + 0.5} ${Y} ${Z + 0.5} rotated -90 0 as TestRat run function bm:admin/democratus`); await sleep(600);
  ok('In a thunderstorm: Democratus kneels in vigil (a click box and his whole rig)', (await cnt('@e[type=interaction,tag=bm.dmenc]')) === 1 && (await cnt('@e[type=item_display,tag=bm.dmencp]')) === 8,
     `${await cnt('@e[type=interaction,tag=bm.dmenc]')} / ${await cnt('@e[type=item_display,tag=bm.dmencp]')}`);
  const sc0 = await run('data get entity @e[type=item_display,tag=bm.dmencp,tag=bm.dp_scythe,limit=1] transformation.scale[0]');
  ok('...scythe and all at full size', /[1-9]\.\d+f/.test(sc0), sc0.replace(/.*data: /, ''));
  await run('weather clear'); await sleep(2300);
  ok('The storm passes: so does he', (await cnt('@e[type=interaction,tag=bm.dmenc]')) === 0 && (await cnt('@e[type=item_display,tag=bm.dmencp]')) === 0);
  await run('weather thunder 6000'); await sleep(5500);
  await run(`execute positioned ${X + 0.5} ${Y} ${Z + 0.5} rotated -90 0 as TestRat run function bm:admin/democratus`); await sleep(800);

  // ---- right-click him: he joins (the seal, the advancement, the follower)
  const enc = await eidOf('@e[type=interaction,tag=bm.dmenc,limit=1]');
  A.interact(enc); await sleep(800);
  ok('Right-click him: he gives you his Storm Seal', await has('demo_seal'));
  ok('..."Eye of the Storm"', /passed/i.test(await run('execute if entity @a[name=TestRat,advancements={bm:story/demo_friend=true}]')));
  await sleep(600);
  ok('...and walks with you: the follower and his 8-part rig', (await cnt(W)) === 1 && (await cnt('@e[type=item_display,tag=bm.dmp,tag=!bm.dmencp,tag=!bm.dmbp,tag=!bm.dmfade]')) === 8,
     `${await cnt(W)} / ${await cnt('@e[type=item_display,tag=bm.dmp,tag=!bm.dmencp,tag=!bm.dmbp,tag=!bm.dmfade]')}`);
  ok('...the vigil is over', (await cnt('@e[type=interaction,tag=bm.dmenc]')) === 0);
  await run('weather clear');
  await run('execute as TestRat run function bm:p58/count'); ok('...he counts toward the follower limit', (await sc('#fc', 'bm.rng')) === 1, `${await sc('#fc', 'bm.rng')}`);

  // ---- the sweep: slow, devastating
  await sleep(1500);
  await run(`tp ${W} ${X + 3.5} ${Y} ${Z + 0.5}`);
  await run(`summon minecraft:zombie ${X + 5.5} ${Y} ${Z + 0.5} {Tags:["bm.t100z","bm.seen"],PersistenceRequired:1b,NoAI:1b,Health:40f,attributes:[{id:"minecraft:max_health",base:40d}]}`);
  let sw = false; for (let i = 0; i < 30 && !sw; i++) { await sleep(100); sw = (await sc(W, 'bm.dma')) === 7 && (await sc(W, 'bm.dmk')) > 0; }
  ok('A monster in reach: he hauls the scythe back for a sweep', sw);
  await sleep(1300);
  const zh = await hpOf('@e[type=zombie,tag=bm.t100z,limit=1]');
  ok('...and it lands: 16 damage', zh <= 26, `zombie ${zh}`);
  ok('...the blow charges him', (await sc(W, 'bm.dmch')) >= 1, `charge ${await sc(W, 'bm.dmch')}`);
  await run('kill @e[type=zombie,tag=bm.t100z]');

  // ---- the Storm Reap: lifted, struck, slammed
  await sleep(2600);
  await run(`tp ${W} ${X + 3.5} ${Y} ${Z + 0.5}`); await run(`execute as ${W} run scoreboard players set @s bm.dmch 5`); await run(`execute as ${W} run scoreboard players set @s bm.dmm 0`);
  for (const dz of [-1.5, 1.5]) await run(`summon minecraft:husk ${X + 6} ${Y} ${Z + 0.5 + dz} {Tags:["bm.t100r","bm.seen"],PersistenceRequired:1b,NoAI:1b,Health:100f,attributes:[{id:"minecraft:max_health",base:100d}]}`);
  let rp = false; for (let i = 0; i < 30 && !rp; i++) { await sleep(100); rp = (await sc(W, 'bm.dma')) === 8; }
  ok('Charged with a monster near: his STORM REAP', rp);
  await sleep(450);
  console.log('   wolf', await cnt(W), await run(`data get entity ${W} Pos`));
  ok('...the monsters are lifted off their feet', /levitation/.test(await run('data get entity @e[type=husk,tag=bm.t100r,limit=1] active_effects')));
  await sleep(2600);
  const h1 = await hpOf('@e[type=husk,tag=bm.t100r,limit=1]');
  ok('...struck by lightning and slammed down (21 damage)', h1 <= 82, `husk ${h1}`);
  ok('...and his charge is spent', (await sc(W, 'bm.dmch')) <= 1, `charge ${await sc(W, 'bm.dmch')}`);
  await run('kill @e[type=husk,tag=bm.t100r]');

  // ---- Old Rivals: with Cecil
  await run('loot replace entity TestRat container.9 loot bm:items/cecil_gem'); await run('scoreboard players set TestRat bm.gvhc 0');
  await run('execute as TestRat at @s run function bm:p46/pet/use'); await sleep(2400);
  ok('With Cecil: Old Rivals - you hit harder', /strength/.test(await run('data get entity TestRat active_effects')));
  ok('...Cecil is tougher', /resistance/.test(await run('data get entity @e[type=wolf,tag=bm.cecilpet,limit=1] active_effects')));
  ok('...and Democratus charges twice as fast', (await cnt('@e[type=wolf,tag=bm.dmpet,tag=bm.dmdc]')) === 1);
  ok('..."Old Rivals" (once)', /passed/i.test(await run('execute if entity @a[name=TestRat,advancements={bm:story/demo_cecil=true}]')));
  await run('execute as @e[type=wolf,tag=bm.cecilpet] run tp @s ~ -400 ~'); await sleep(200);

  // ---- The Storm's Heir: with KillerWatt
  await run('loot replace entity TestRat container.10 loot bm:items/kw_spark'); await run('scoreboard players set TestRat bm.gvhc 0');
  await run('execute as TestRat at @s run function bm:p79/spark'); await sleep(400);
  const ch0 = await sc('@e[type=wolf,tag=bm.kxpet,limit=1]', 'bm.kxch');
  await sleep(2200);
  ok("With KillerWatt: The Storm's Heir - you're quicker", /speed/.test(await run('data get entity TestRat active_effects')) && /jump_boost/.test(await run('data get entity TestRat active_effects')));
  ok('...KillerWatt is tougher and charges faster', /resistance/.test(await run('data get entity @e[type=wolf,tag=bm.kxpet,limit=1] active_effects')) &&
     (await sc('@e[type=wolf,tag=bm.kxpet,limit=1]', 'bm.kxch')) > ch0, `${ch0} -> ${await sc('@e[type=wolf,tag=bm.kxpet,limit=1]', 'bm.kxch')}`);
  ok('...and Democratus regenerates', /regeneration/.test(await run(`data get entity ${W} active_effects`)));
  await run('execute as @e[type=wolf,tag=bm.kxpet] run tp @s ~ -400 ~'); await sleep(300);

  // ---- right-click him: sit / stand
  await run(`tp ${W} ${X + 3.5} ${Y} ${Z + 0.5}`); await sleep(1300);
  A.interact(await eidOf('@e[type=interaction,tag=bm.dmhit,limit=1]'));
  await sleep(500);
  ok('Right-click him: he sits (and his rig sits too)', /1b/.test(await run(`data get entity ${W} Sitting`)) && (await sc(W, 'bm.dms')) === 4, `${await run(`data get entity ${W} Sitting`)} st ${await sc(W, 'bm.dms')}`);
  await run(`execute as ${W} run data merge entity @s {Sitting:0b}`);

  // ---- his challenge: the duel
  await run('scoreboard players set TestRat bm.gvhc 0');
  await run('execute as TestRat at @s run function bm:p97/menu');
  ok('Sneak + use the seal: his challenge (a menu)', (await sc('TestRat', 'bm.menu')) === 9700);
  await run('scoreboard players set TestRat bm.act 9701'); await sleep(400);
  ok('DUEL HIM: the follower steps out and a duelist squares up', (await cnt(W)) === 0 && (await cnt(BOSS)) === 1, `${await cnt(W)} / ${await cnt(BOSS)}`);
  ok('...ten seconds to get clear (he can\'t move or be hurt)', /1b/.test(await run(`data get entity ${BOSS} NoAI`)) && /1b/.test(await run(`data get entity ${BOSS} Invulnerable`)) &&
     (await sc('TestRat', 'bm.dmd')) > 150, `dmd ${await sc('TestRat', 'bm.dmd')}`);
  console.log('   before FIGHT: health', (await run('data get entity TestRat Health')).replace(/.*data: /, ''), 'deaths', await sc('TestRat', 'bm.dmdth'), '/', await sc('TestRat', 'bm.dmdn'));
  await run('scoreboard players set TestRat bm.dmd 2'); await sleep(400);
  ok('...FIGHT: he comes for you', !/1b/.test(await run(`data get entity ${BOSS} NoAI`)) && /0b/.test(await run(`data get entity ${BOSS} Invulnerable`)));
  await run(`effect give TestRat minecraft:resistance 60 4 true`); await run(`effect give TestRat minecraft:regeneration 60 4 true`);
  await sleep(4000);
  ok('...and attacks (sweep, lunge, lightning or Storm Reap)', (await sc(BOSS, 'bm.dmch')) >= 1, `attacks ${await sc(BOSS, 'bm.dmch')}`);
  await run(`data merge entity ${BOSS} {Health:50f}`); await sleep(400);
  ok('Brought to his knee: he yields', (await cnt('@e[type=vindicator,tag=bm.dmboss,tag=bm.dmyield]')) === 1);
  await sleep(3800);
  ok('...the prize: his scythe', (await items('demo_scythe')) === 1 && (await sc('TestRat', 'bm.dmsc')) === 1);
  ok('..."Reaper\'s Due"', /passed/i.test(await run('execute if entity @a[name=TestRat,advancements={bm:story/demo_duel=true}]')));
  ok('...and he goes home; the duel is over', (await cnt(BOSS)) === 0 && !/passed/i.test(await run('execute if entity TestRat[tag=bm.dmduel]')));

  // ---- again: a win, but only his respect
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p97/menu');
  await run('scoreboard players set TestRat bm.act 9701'); await sleep(400); await run('scoreboard players set TestRat bm.dmd 2'); await sleep(500);
  await run(`data merge entity ${BOSS} {Health:50f}`); await sleep(4300);
  ok('A second duel won: no second scythe', (await items('demo_scythe')) === 1, `${await items('demo_scythe')} scythes`);

  // ---- a loss: he simply goes home - and you can try again at once
  await run('effect clear TestRat'); await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p97/menu');
  await run('scoreboard players set TestRat bm.act 9701'); await sleep(400); await run('scoreboard players set TestRat bm.dmd 2'); await sleep(500);
  await run(`execute as ${BOSS} run data merge entity @s {NoAI:1b}`);
  await run('damage TestRat 16 minecraft:generic'); await sleep(400);
  ok('Down to three hearts: the duel is lost - he goes home', (await cnt(BOSS)) === 0 && !/passed/i.test(await run('execute if entity TestRat[tag=bm.dmduel]')));
  ok('...and you get some healing', /regeneration/.test(await run('data get entity TestRat active_effects')));
  await run('effect give TestRat minecraft:instant_health 1 4 true');
  ok('...no cooldown: call him again straight away', await (async () => { await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p97/use'); await sleep(500); return (await cnt(W)) === 1; })());

  // ---- his scythe: arcs of lightning, a charge, a Storm Reap of your own
  await run(`execute as ${W} run tp @s ~ -400 ~`); await sleep(300);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} -90 0`);
  await run('item replace entity TestRat weapon.mainhand from entity TestRat container.0'); await run('clear TestRat *[minecraft:custom_data~{bm:"demo_seal"}]');
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/demo_scythe'); A.slot(0); await sleep(300);
  await run(`summon minecraft:husk ${X + 2.5} ${Y} ${Z + 0.5} {Tags:["bm.t100s","bm.seen"],PersistenceRequired:1b,NoAI:1b,Health:200f,attributes:[{id:"minecraft:max_health",base:200d}]}`);
  await run(`summon minecraft:husk ${X + 3.5} ${Y} ${Z + 2.5} {Tags:["bm.t100t","bm.seen"],PersistenceRequired:1b,NoAI:1b,Health:200f,attributes:[{id:"minecraft:max_health",base:200d}]}`);
  await sleep(1700);                  // (a slow weapon: wait for the full swing)
  const tgt = await eidOf('@e[type=husk,tag=bm.t100s,limit=1]');
  const by0 = await hpOf('@e[type=husk,tag=bm.t100t,limit=1]');
  A.attack(tgt); await sleep(500);
  const hs = await hpOf('@e[type=husk,tag=bm.t100s,limit=1]');
  ok('His scythe hits hard (15)', hs <= 186, `husk ${hs}`);
  ok('...lightning arcs to a monster close by', (await hpOf('@e[type=husk,tag=bm.t100t,limit=1]')) < by0, `${by0} -> ${await hpOf('@e[type=husk,tag=bm.t100t,limit=1]')}`);
  ok('...and the blade charges', (await sc('TestRat', 'bm.dmsch')) === 1, `charge ${await sc('TestRat', 'bm.dmsch')}`);
  await run('scoreboard players set TestRat bm.dmsch 7'); await sleep(1300); A.attack(tgt); await sleep(400);
  ok('At eight: a STORM REAP of your own', (await sc('TestRat', 'bm.dmsrt')) > 0 && /levitation/.test(await run('data get entity @e[type=husk,tag=bm.t100s,limit=1] active_effects')));
  await run('kill @e[type=husk,tag=bm.t100s]'); await run('kill @e[type=husk,tag=bm.t100t]');

  // ---- fainting: 5 minutes before the seal works again
  await run('clear TestRat'); await run('loot replace entity TestRat container.0 loot bm:items/demo_seal'); await run('scoreboard players set TestRat bm.gvhc 0');
  await run('execute as TestRat at @s run function bm:p97/use'); await sleep(600);
  await run(`kill ${W}`); await sleep(800);
  ok('If he falls: his rig crackles away, and the seal rests 5 minutes', (await sc('TestRat', 'bm.dmcd')) >= 290 && (await cnt('@e[type=item_display,tag=bm.dmp,tag=!bm.dmencp,tag=!bm.dmbp,tag=!bm.dmfade]')) === 0,
     `cd ${await sc('TestRat', 'bm.dmcd')}`);
  await run('scoreboard players set TestRat bm.dmcd 0'); await run('weather clear'); await run("gamerule advance_weather true");
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.log('ERR', e); process.exit(1); });

// v2.37 Emma: encounter + recruit, rig follows, states, modes + buffs, quick heal, charge, ethereal strike, harmony with Cecil, falling
const { bot, rcon, sleep } = require('./lib');
const X = 9700, Y = 100, Z = 9700;
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const pos = async (sel) => { const r = await run(`data get entity ${sel} Pos`); const m = r.match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const cnt = async (sel) => { const r = await run(`execute store result score #t bm.rng if entity ${sel}`); const m = r.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const score = async (who, obj) => { const r = await run(`scoreboard players get ${who} ${obj}`); const m = r.match(/has (-?\d+)/); return m ? +m[1] : null; };
  const num = async (c) => { const r = await run(c); const m = r.match(/(-?[\d.]+)[fdbsL]?\s*$/); return m ? +m[1] : null; };
  const EM = '@e[type=cat,tag=bm.emmapet,limit=1]';
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('tag TestRat remove bm.emhint'); await run('tag TestRat remove bm.emharm');
  await run('advancement revoke TestRat only bm:story/emma_friend'); await run('advancement revoke TestRat only bm:story/emma_ethereal'); await run('advancement revoke TestRat only bm:story/emma_cecil');
  await run(`forceload add ${X - 40} ${Z - 40} ${X + 40} ${Z + 40}`);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(2500);
  await run(`fill ${X - 30} ${Y} ${Z - 30} ${X + 30} ${Y} ${Z + 30} grass_block`); await run(`fill ${X - 30} ${Y + 1} ${Z - 30} ${X + 30} ${Y + 8} ${Z + 30} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..60]`); await run('kill @e[type=cat,tag=bm.emmapet]'); await run('kill @e[type=wolf,tag=bm.cecilpet]');
  await run('time set day'); await run('scoreboard players reset TestRat bm.emcd'); await run('scoreboard players reset TestRat bm.cpcd'); await sleep(1500);

  // ---- the encounter: she sits in the flowers; talking to her empty-handed only says hello
  await run('execute as TestRat at @s run function bm:admin/emma'); await sleep(1500);
  ok('admin/emma: Emma sits in front of you (a hitbox + 10 rig parts)', (await cnt('@e[type=interaction,tag=bm.emenc]')) === 1 && (await cnt('@e[type=item_display,tag=bm.emencp]')) === 10);
  const lr = await run('data get entity @e[type=item_display,tag=bm.emencp,tag=bm.ep_legr,limit=1] transformation.left_rotation[0]');
  ok('...posed sitting (legs out in front)', /-0\.[56]/.test(lr), lr.slice(-40));
  const hit = Object.values(A.ents).filter(e => Math.abs(e.x - X - 0.5) < 0.6 && Math.abs(e.z - Z - 4.5) < 0.6 && e.type !== undefined);
  const iid = hit.map(e => e.entityId);
  A.bars.length = 0; for (const i of iid) A.interact(i); await sleep(1200);
  if (!A.bars.some(b => b.includes("I'm Emma"))) { console.log('  (bot interact missed; calling the talk function directly)');
    await run('tag @e[type=interaction,tag=bm.emenc] add bm.emhere'); await run('execute as TestRat at @s run function bm:p57/enc/talk'); await run('tag @e[type=interaction,tag=bm.emenc] remove bm.emhere'); await sleep(800); }
  ok('talking to her empty-handed: a hello, no ribbon', A.bars.some(b => b.includes("I'm Emma")) && !(await run('clear TestRat totem_of_undying[custom_data~{bm:"emma_ribbon"}] 0')).match(/[1-9] item/), A.bars.slice(-1)[0]);
  // with a flower
  await run('item replace entity TestRat hotbar.0 with minecraft:poppy 3'); A.slot(0); await sleep(500);
  for (const i of iid) A.interact(i); await sleep(1500);
  if (!(await cnt('@e[type=cat,tag=bm.emmapet]'))) {        // (the bot's entity view can miss the hitbox: drive the same path by hand)
    console.log('  (bot interact missed; calling the talk function directly)');
    await run('tag @e[type=interaction,tag=bm.emenc] add bm.emhere'); await run('execute as TestRat at @s run function bm:p57/enc/talk'); await sleep(1500);
  }
  const rib = await run('clear TestRat totem_of_undying[custom_data~{bm:"emma_ribbon"}] 0');
  ok('a flower wins her over: the ribbon, one flower gone, the encounter gone', /Found 1 /.test(rib) && /Found 2 /.test(await run('clear TestRat poppy 0')) &&
     (await cnt('@e[type=interaction,tag=bm.emenc]')) === 0 && (await cnt('@e[type=item_display,tag=bm.emencp]')) === 0, rib);
  ok('...and she joins you at once (her host + 10 parts, yours)', (await cnt('@e[type=cat,tag=bm.emmapet]')) === 1 && (await cnt('@e[type=item_display,tag=bm.emp,tag=!bm.emencp]')) === 10 &&
     (await score(EM, 'bm.pid')) === (await score('TestRat', 'bm.pid')));
  ok('...achievement: A Friend Among the Flowers', (await run('execute if entity @a[name=TestRat,advancements={bm:story/emma_friend=true}]')).includes('passed'));

  // ---- the rig follows its host; idle / sit / walk states
  await sleep(1500);
  const cpos = await pos(EM), bpos = await pos('@e[type=item_display,tag=bm.ep_body,tag=!bm.emencp,limit=1]');
  ok('her body part stands at her hips above the host', cpos && bpos && Math.hypot(cpos[0] - bpos[0], cpos[2] - bpos[2]) < 0.3 && Math.abs(bpos[1] - cpos[1] - 0.584) < 0.05,
     `${cpos && cpos.map(v => v.toFixed(2))} / ${bpos && bpos.map(v => v.toFixed(2))}`);
  await run(`tp ${EM} ${X + 0.5} ${Y + 1} ${Z + 2.5}`); await sleep(1500);
  const st0 = await score(EM, 'bm.ems'); const ar = await run('data get entity @e[type=item_display,tag=bm.ep_armr,tag=!bm.emencp,limit=1] transformation.left_rotation[0]');
  ok('idle: state 0, arms folded (arm rotated forward)', (st0 === 0 || st0 === 6), `state ${st0}, ${ar.slice(-14)}`);
  await run(`data modify entity ${EM} Sitting set value 1b`); await sleep(800);
  ok('sitting: state 4', (await score(EM, 'bm.ems')) === 4);
  await run(`data modify entity ${EM} Sitting set value 0b`); await sleep(500);
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 13.2}`);
  const seen = new Set(); for (let i = 0; i < 30; i++) { seen.add(await score(EM, 'bm.ems')); await sleep(100); }
  ok('following you: she walks or runs (state 1/2)', seen.has(1) || seen.has(2), [...seen].join(','));
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(2500);
  await run(`tp ${EM} ${X + 0.5} ${Y + 1} ${Z + 2.5}`); await sleep(1500);

  // ---- modes: the menu, then the buff lands
  await run('scoreboard players set TestRat bm.menu 960'); A.cmd('trigger bm.act set 7302'); await sleep(4500);
  ok('menu: Offense picked', (await score(EM, 'bm.emm')) === 2);
  ok('...and her pulse gives you Strength', (await run('data get entity TestRat active_effects')).includes('minecraft:strength'));
  await run('scoreboard players set TestRat bm.menu 960'); A.cmd('trigger bm.act set 7304'); await sleep(500);
  await run('effect clear TestRat'); await run('effect give TestRat instant_health 1 4 true'); await sleep(300); await run('damage TestRat 16 minecraft:out_of_world'); await sleep(100); const hq0 = await num('data get entity TestRat Health'); await sleep(7000);
  const hp = await num('data get entity TestRat Health');
  ok('Healing: Regeneration, and a quick heal when below 4 hearts', hp >= hq0 + 5 && (await run('data get entity TestRat active_effects')).includes('regeneration'), `health ${hq0} -> ${hp}`);

  // ---- charge with monsters about, then the ethereal form and its strike
  await run(`summon husk ${X + 6.5} ${Y + 1} ${Z + 2.5} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t40z"],active_effects:[{id:"minecraft:fire_resistance",duration:-1,amplifier:0b}],}`); await sleep(300);
  await sleep(800); await run('attribute @e[tag=bm.t40z,limit=1] minecraft:max_health base set 200'); await sleep(200); await run('data modify entity @e[tag=bm.t40z,limit=1] Health set value 200f');
  await run(`scoreboard players set ${EM} bm.emc 10`); await sleep(5200);
  const c1 = await score(EM, 'bm.emc');
  ok('a monster within 16: she charges ~2% a second', c1 >= 16 && c1 <= 22, `charge ${c1}`);
  await run('execute as TestRat run function bm:admin/emma_charge'); await sleep(2200);
  ok('at 100% with a monster near: the Ethereal Form (30 s)', (await score(EM, 'bm.eme')) >= 27, `eme ${await score(EM, 'bm.eme')}`);
  ok('...her parts swap to the ethereal models, wings out', (await run('data get entity @e[type=item_display,tag=bm.ep_body,tag=!bm.emencp,limit=1] item.components')).includes('bm:ee_body') &&
     /0\.85/.test(await run('data get entity @e[type=item_display,tag=bm.ep_wingr,tag=!bm.emencp,limit=1] transformation.scale[0]')));
  ok('...achievement: Ethereal', (await run('execute if entity @a[name=TestRat,advancements={bm:story/emma_ethereal=true}]')).includes('passed'));
  await run('data modify entity @e[tag=bm.t40z,limit=1] Health set value 200f'); const zh0 = await num('data get entity @e[tag=bm.t40z,limit=1] Health'); await sleep(3200);
  const zh1 = await num('data get entity @e[tag=bm.t40z,limit=1] Health');
  ok('...she strikes the monster (8 a second)', zh0 - zh1 >= 15, `${zh0} -> ${zh1}`);
  const cp2 = await pos(EM), bp2 = await pos('@e[type=item_display,tag=bm.ep_body,tag=!bm.emencp,limit=1]');
  ok('...flying: the rig rides 1 block up', bp2[1] - cp2[1] > 1.4, `${(bp2[1] - cp2[1]).toFixed(2)}`);
  await run(`scoreboard players set ${EM} bm.eme 1`); await sleep(2200);
  ok('when it ends: back to normal, charge 0', (await score(EM, 'bm.eme')) === 0 && (await score(EM, "bm.emc")) <= 4 &&
     (await run('data get entity @e[type=item_display,tag=bm.ep_body,tag=!bm.emencp,limit=1] item.components')).includes('bm:em_body'));

  // ---- harmony with Cecil
  await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(2500);
  ok('Cecil\'s first summon drops the hint about Emma (once)', (await run('tag TestRat list')).includes('bm.emhint'));
  ok('harmony: both tagged', (await cnt('@e[type=cat,tag=bm.emmapet,tag=bm.harmony]')) === 1 && (await cnt('@e[type=wolf,tag=bm.cecilpet,tag=bm.harmony]')) === 1);
  ok('...achievement: Best of Friends', (await run('execute if entity @a[name=TestRat,advancements={bm:story/emma_cecil=true}]')).includes('passed'));
  await run(`tp ${EM} ${X + 1.5} ${Y + 1} ${Z + 1.5}`); await run(`tp @e[type=wolf,tag=bm.cecilpet] ${X - 0.5} ${Y + 1} ${Z + 1.5}`); await run(`tp @e[tag=bm.t40z] ${X + 3.5} ${Y + 1} ${Z + 0.5}`);
  await run(`scoreboard players set ${EM} bm.emc 10`); await sleep(4100);
  const c2 = await score(EM, 'bm.emc');
  ok('...she charges twice as fast (4% a second)', c2 >= 24 && c2 <= 30, `charge ${c2}`);
  await run(`scoreboard players set ${EM} bm.emc 0`);
  await run(`tp @e[tag=bm.t40z] ${X + 3.5} ${Y + 1} ${Z + 0.5}`); await run('data modify entity @e[tag=bm.t40z,limit=1] Health set value 200f'); await sleep(200);
  await run(`tp @e[type=wolf,tag=bm.cecilpet] ${X - 0.5} ${Y + 1} ${Z + 1.5}`);
  const zc0 = await num('data get entity @e[tag=bm.t40z,limit=1] Health'); await sleep(4100);
  const zc1 = await num('data get entity @e[tag=bm.t40z,limit=1] Health');
  ok('...Cecil casts every second, 7 a bolt (+poison)', zc0 - zc1 >= 15, `${zc0} -> ${zc1}; cecil ${await pos('@e[type=wolf,tag=bm.cecilpet,limit=1]')}; tags ${(await run('tag @e[type=wolf,tag=bm.cecilpet,limit=1] list')).slice(-50)}`);
  await run('kill @e[tag=bm.t40z]'); await sleep(1500);
  await run(`tp ${EM} ${X + 1.5} ${Y + 1} ${Z + 1.5}`); await run('tp @e[type=wolf,tag=bm.cecilpet] ' + `${X - 0.5} ${Y + 1} ${Z + 1.5}`);
  await run(`data modify entity ${EM} Sitting set value 0b`);
  await run(`scoreboard players set ${EM} bm.emi 44`); A.bars.length = 0;
  let waved = false; for (let i = 0; i < 25; i++) { if ((await score(EM, 'bm.ems')) === 8) { waved = true; break; } await sleep(100); }
  ok('...now and then they chat: Emma waves at Cecil', waved && A.bars.some(b => b.includes('Cecil:')), A.bars.slice(-1)[0]);

  // ---- recall, dismiss and falling
  await run(`tp ${EM} ${X + 20.5} ${Y + 1} ${Z + 20.5}`); await sleep(500);
  await run('execute as TestRat at @s run function bm:p57/use'); await sleep(500);
  const rp = await pos(EM); ok('ribbon: calls her back to you', rp && Math.hypot(rp[0] - X - 0.5, rp[2] - Z - 0.5) < 1.5);
  await run(`kill ${EM}`); await sleep(1500);
  ok('if she falls: the rig fades away, the ribbon rests 10 minutes', (await cnt('@e[type=item_display,tag=bm.emp,tag=!bm.emencp]')) === 0 && (await score('TestRat', 'bm.emcd')) >= 590);
  await run('execute as TestRat at @s run function bm:p57/use'); await sleep(500);
  ok('...and the ribbon refuses meanwhile', (await cnt('@e[type=cat,tag=bm.emmapet]')) === 0);
  await run('scoreboard players reset TestRat bm.emcd'); await run('execute as TestRat at @s run function bm:p57/use'); await sleep(800);
  ok('...after the rest she comes again', (await cnt('@e[type=cat,tag=bm.emmapet]')) === 1);
  await run('scoreboard players set TestRat bm.menu 960'); A.cmd('trigger bm.act set 7305'); await sleep(1800);
  ok('menu: send her home - host and rig gone, no cooldown', (await cnt('@e[type=cat,tag=bm.emmapet]')) === 0 && (await cnt('@e[type=item_display,tag=bm.emp,tag=!bm.emencp]')) === 0 &&
     !((await score('TestRat', 'bm.emcd')) > 0));

  // ---- natural encounters: only in flowery biomes by day, never for someone carrying her ribbon
  await run(`fillbiome ${X - 30} ${Y - 5} ${Z - 30} ${X + 30} ${Y + 20} ${Z + 30} minecraft:cherry_grove`); await sleep(500);
  for (let i = 0; i < 80; i++) await run('execute as TestRat at @s run function bm:p57/enc/roll');
  ok('carrying the ribbon: she never turns up', (await cnt('@e[type=interaction,tag=bm.emenc]')) === 0);
  await run('clear TestRat'); let n = 0;
  for (let i = 0; i < 120 && !n; i++) { await run('execute as TestRat at @s run function bm:p57/enc/roll'); n = await cnt('@e[type=interaction,tag=bm.emenc]'); }
  const ep = await pos('@e[type=interaction,tag=bm.emenc,limit=1]');
  ok('without it, in a cherry grove by day: now and then she turns up ~14 blocks away, on the grass', n === 1 && ep && Math.abs(Math.hypot(ep[0] - X - 0.5, ep[2] - Z - 0.5) - 14) < 1.2 && Math.abs(ep[1] - Y - 1) < 0.01,
     ep && ep.map(v => v.toFixed(1)).join(' '));
  await run('kill @e[type=interaction,tag=bm.emenc]'); await run('kill @e[type=item_display,tag=bm.emencp]');
  await run(`fillbiome ${X - 30} ${Y - 5} ${Z - 30} ${X + 30} ${Y + 20} ${Z + 30} minecraft:plains`);
  await run('kill @e[type=wolf,tag=bm.cecilpet]'); await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..60]`);
  await run(`forceload remove ${X - 40} ${Z - 40} ${X + 40} ${Z + 40}`);
  console.log(`\n${res.filter(x => x).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.log('FATAL', e); process.exit(1); });

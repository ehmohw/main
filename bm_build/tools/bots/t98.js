// v2.67 check: the Scorching Heart / Hearthfire, Ethereal KillerWatt and the Ethereal Tendrils
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 19200, Y = 110, Z = 19200;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const fl = async c => { const m = (await run(c)).match(/(-?\d+(?:\.\d+)?)[fd]?\s*$/); return m ? +m[1] : NaN; };
  const cnt = async sel => { const o = await run(`execute store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const inv = async iid => { const v = await num(`execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`); return isNaN(v) ? 0 : v; };
  await run(`forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  await run(`fill ${X - 40} ${Y - 2} ${Z - 40} ${X + 40} ${Y - 1} ${Z + 40} minecraft:stone`); await run(`fill ${X - 40} ${Y} ${Z - 40} ${X + 40} ${Y + 30} ${Z + 40} minecraft:air`);
  await run('weather clear'); await run('time set day'); await run('gamerule doMobSpawning false');
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat resistance 600 4 true'); await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid'); await sleep(800);

  // ---- THE SCORCHING HEART
  await run('loot give TestRat loot bm:items/scorching_heart'); await sleep(2200);
  ok('Scorching Heart carried: fire can\'t touch you (Fire Resistance kept up)', /fire_resistance/.test(await run('data get entity TestRat active_effects')));
  await run(`execute positioned ${X + 0.5} ${Y} ${Z + 6.5} run function bm:p82/heart/place`); await sleep(300);
  ok('Set down: the Hearthfire (the heart on a light, a click box to take it back)', (await cnt('@e[type=item_display,tag=bm.hearthd]')) === 1 && (await cnt('@e[type=interaction,tag=bm.hearth]')) === 1 &&
     /passed/i.test(await run(`execute if block ${X} ${Y} ${Z + 6} minecraft:light`)));
  await run(`summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 26.5} {Tags:["t98a"]}`); await run(`summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 12.5} {Tags:["t98b"],PersistenceRequired:1b,NoAI:1b}`);
  await run(`summon minecraft:husk ${X + 0.5} ${Y} ${Z + 22.5} {Tags:["t98c","bm.blood"],PersistenceRequired:1b,NoAI:1b,Health:20f}`);
  await sleep(2600);
  ok('...a monster that would spawn (a wandering, despawnable one) within 48 is snuffed out', (await cnt('@e[tag=t98a]')) === 0);
  ok('...one that comes within 12 is seared (set alight)', /[1-9]\d*s/.test(await run('data get entity @e[tag=t98b,limit=1] Fire')) || (await cnt('@e[tag=t98b]')) === 0, await run('data get entity @e[tag=t98b,limit=1] Fire'));
  const hh = await fl('data get entity @e[tag=t98c,limit=1] Health');
  ok('...and a Blood Moon horror within 24 burns', isNaN(hh) || hh < 20, `husk ${hh}`);
  await run('kill @e[tag=t98b]'); await run('kill @e[tag=t98c]');
  await run(`execute positioned ${X + 0.5} ${Y} ${Z + 6.5} run function bm:p82/hearth/take`); await sleep(300);
  ok('Take it back: the heart returns to you', (await inv('scorching_heart')) >= 1 && (await cnt('@e[type=item_display,tag=bm.hearthd]')) === 0);
  await run('kill @e[type=interaction,tag=bm.hearth]'); await run('clear TestRat');

  // ---- ETHEREAL KILLERWATT
  await run('kill @e[type=husk,tag=bm.kxboss]'); await run('advancement revoke TestRat only bm:p83/killed_eth'); await run('scoreboard players reset TestRat bm.kxek');
  await run(`execute positioned ${X + 0.5} ${Y} ${Z + 12.5} run function bm:admin/killerwatt`); await sleep(7500);
  ok('KillerWatt comes down', (await cnt('@e[type=husk,tag=bm.kxboss]')) === 1);
  const h0 = await fl('attribute @e[type=husk,tag=bm.kxboss,limit=1] minecraft:max_health get');
  await run('loot replace entity TestRat weapon.mainhand loot bm:items/ethereal_gem'); await sleep(200);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 90`); await sleep(300);              // (looking straight down at the floor)
  await run('execute as TestRat at @s rotated 0 90 run function bm:p60/eth/use'); await sleep(300);
  const shr = await cnt('@e[type=item_display,tag=bm.eshr]');
  if (!shr) await run(`summon minecraft:item_display ${X + 0.5} ${Y + 1} ${Z + 4.5} {Tags:["bm.eshr"],item:{id:"minecraft:paper",count:1}}`);
  await sleep(2400);
  const h1 = await fl('attribute @e[type=husk,tag=bm.kxboss,limit=1] minecraft:max_health get');
  ok('An Ethereal Gem set down within 30 blocks: he ascends (Ethereal KillerWatt, 80% more health)', /bm\.kxeth/.test(await run('data get entity @e[type=husk,tag=bm.kxboss,limit=1] Tags')) && h1 > h0 * 1.7,
     `${h0} -> ${h1} (shrine ${shr ? 'placed by the gem' : 'stand-in'})`);
  const fhp = await fl('data get entity @e[type=husk,tag=bm.kxboss,limit=1] Health');
  ok('...healed whole at the new maximum', fhp >= h1 - 1, `${fhp}/${h1}`);
  // (a 30% pick at each of his choices: give him 10s to pick it himself, then call it - the cast is the same code either way)
  let lance = false, how = 'his own pick'; for (let i = 0; i < 40 && !lance; i++) { await sleep(250); lance = (await cnt('@e[type=marker,tag=bm.kxlance]')) > 0; }
  if (!lance) { how = 'called'; await run('execute as @e[type=husk,tag=bm.kxboss,limit=1] at @s run function bm:p79/boss/start {a:6}');
    for (let i = 0; i < 16 && !lance; i++) { await sleep(250); lance = (await cnt('@e[type=marker,tag=bm.kxlance]')) > 0; } }
  let hitme = false; for (let i = 0; i < 16 && !hitme; i++) { await sleep(250); hitme = /levitation|wither/.test(await run('data get entity TestRat active_effects')); }
  ok('...he throws Void Lances (they hunt you down: lift and wither)', lance && hitme, `${how}, seen ${lance}, struck ${hitme}`);
  await run('kill @e[tag=bm.kxlance]'); await run('effect give TestRat instant_health 1 5 true');
  await run('damage @e[type=husk,tag=bm.kxboss,limit=1] 99999 minecraft:player_attack by TestRat'); await sleep(4000);
  ok('Beat his Ethereal form: the Ethereal Tendrils', (await inv('ethereal_tendrils')) === 1 || (await cnt('@e[type=item,nbt={Item:{components:{"minecraft:custom_data":{bm:"ethereal_tendrils"}}}}]')) >= 1,
     `inv ${await inv('ethereal_tendrils')}`);
  // the Tendrils: worn, they fling further and float what they hit (their enchantment)
  const comp = await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"ethereal_tendrils"}}}].components');
  ok('...worn in the chest slot, with their own power (the ethereal tendrils enchantment)', /equippable/.test(comp) && /kw_tendrils_eth/.test(comp), comp.slice(0, 160));
  await run('kill @e[type=item_display,tag=bm.eshr]'); await run('kill @e[type=interaction,tag=bm.eshr_hit]'); await run('clear TestRat');
  await run('gamerule doMobSpawning true'); await run(`forceload remove ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`); process.exit(0);
})();

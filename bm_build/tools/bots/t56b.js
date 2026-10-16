const { bot, rcon, sleep } = require('./lib');
const X = 11900, Y = 200, Z = 11900; const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const cbuf = async (sel) => { const m = (await run(`scoreboard players get ${sel} bm.cbuf`)).match(/has (-?\d+)/); return m ? +m[1] : 0; };   // (2.80: a roaming boss carries a health buffer for its staged death)
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  await run(`fill ${X - 14} ${Y} ${Z - 14} ${X + 14} ${Y} ${Z + 14} stone`); await run(`fill ${X - 14} ${Y + 1} ${Z - 14} ${X + 14} ${Y + 9} ${Z + 14} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('clear TestRat'); await run('gamemode survival TestRat'); await run('weather clear'); await run('time set night');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await run('effect give TestRat resistance 60 4 true'); await run('effect clear TestRat levitation'); await sleep(1000);
  await run(`execute positioned ${X} ${Y + 1} ${Z + 9} run function bm:p54/vwk/summon`); await sleep(300);
  await run('execute as @e[type=enderman,tag=bm.vwk] at @s rotated ~ 0 run function bm:p54/vwk/voidlings'); await sleep(300);
  await run('effect give @e[type=enderman,tag=bm.vwk] slowness 60 255 true');
  const hp0 = ((+((await run('data get entity @e[type=enderman,tag=bm.vwk,limit=1] Health')).match(/([\d.]+)f/)?.[1])) - (await cbuf('@e[type=enderman,tag=bm.vwk,limit=1]')));   // (2.80: its arrival holds its health high a while)
  for (let i = 0; i < 16; i++) { await sleep(500); console.log(i, (await run("data get entity @e[type=enderman,tag=bm.vwk,limit=1] Health")).slice(-7), await cnt("@e[type=endermite,tag=bm.vwkmin]"), (await run("data get entity @e[type=endermite,tag=bm.vwkmin,limit=1] Health")).slice(-6), (await run("data get entity @e[type=endermite,tag=bm.vwkmin,limit=1] Pos")).slice(-40), (await run("scoreboard players get @e[type=enderman,tag=bm.vwk,limit=1] bm.r53t")).slice(-12)); }
  await sleep(2500);
  const lev = /passed/.test(await run('execute if entity @a[name=TestRat,nbt={active_effects:[{id:"minecraft:levitation"}]}]'));
  const hp = ((+((await run('data get entity @e[type=enderman,tag=bm.vwk,limit=1] Health')).match(/([\d.]+)f/)?.[1])) - (await cbuf('@e[type=enderman,tag=bm.vwk,limit=1]')));
  ok('Stars home in on the player (levitation from a hit)', lev || (await run('data get entity TestRat Health')).match(/([\d.]+)f/)[1] < 20, 'hp ' + (await run('data get entity TestRat Health')).slice(-6));
  ok('...and never hurt the Voidwalker or its Voidlings', +hp === +hp0 && (await cnt('@e[type=endermite,tag=bm.vwkmin]')) === 3, `boss ${hp0} -> ${hp}, voidlings ${await cnt('@e[type=endermite,tag=bm.vwkmin]')}`);
  ok('No stars left over', (await cnt('@e[type=marker,tag=bm.vwstar]')) === 0);
  await run('kill @e[tag=bm.vwk]'); await run('kill @e[tag=bm.vwkmin]'); await run('time set day');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

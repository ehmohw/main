const { rcon, sleep } = require('./lib_resp');
(async () => { const R = await rcon(); const O='execute in minecraft:overworld run '; const r=c=>R.run(O+c);
  await r('forceload add 16604 15984 16636 16016'); await sleep(1500);
  await r('fill 16610 100 15985 16630 100 16015 minecraft:stone'); await r('fill 16610 101 15985 16630 108 16015 minecraft:air');
  for (const d of [2.5, 3.2, 4, 6, 9, 11]) {
    await r('kill @e[type=!minecraft:player,x=16620,y=100,z=16000,distance=..30]');
    await r(`summon minecraft:zombie 16620.5 101 ${16000+d} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["bm.t183z"],attributes:[{id:"minecraft:max_health",base:400}],Health:400f,equipment:{head:{id:"minecraft:stone_button",count:1}}}`);
    await r('summon minecraft:wolf 16620.5 101 16000 {NoAI:1b,Tags:["bm.dwpet","bm.pjt0"],Silent:1b}'); await r('scoreboard players set @e[tag=bm.pjt0] bm.pid 9999'); await sleep(300);
    await r('execute as @e[tag=bm.pjt0] at @s facing entity @e[tag=bm.t183z,limit=1] eyes positioned ^ ^1.1 ^0.6 run function bm:p212/dw/throw0');
    await sleep(1500);
    console.log(d, (await r('data get entity @e[tag=bm.t183z,limit=1] Health')).slice(-8), (await r('data get entity @e[tag=bm.t183z,limit=1] Fire')).slice(-6));
  }
  await r('kill @e[type=!minecraft:player,x=16620,y=100,z=16000,distance=..30]');
  R.end(); process.exit(0); })();

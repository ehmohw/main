const { rcon, sleep } = require('./lib_resp');
(async () => { const R = await rcon(); const O='execute in minecraft:overworld run '; const r=c=>R.run(O+c);
  await r('forceload add 16604 15984 16636 16016'); await sleep(1500);
  await r('fill 16610 100 15990 16630 100 16010 minecraft:stone'); await r('fill 16610 101 15990 16630 108 16010 minecraft:air');
  await r('kill @e[type=!minecraft:player,x=16620,y=100,z=16000,distance=..24]');
  await r('summon minecraft:zombie 16620.5 101 16007.9 {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["bm.t183z","bm.seen"],attributes:[{id:"minecraft:max_health",base:400}],Health:400f}');
  await r('summon minecraft:armor_stand 16620.5 101 16004.7 {Tags:["bm.pjt0"],NoGravity:1b}'); await sleep(300);
  console.log(await r('execute as @e[tag=bm.pjt0] at @s facing entity @e[tag=bm.t183z,limit=1] eyes positioned ^ ^1.1 ^0.6 run function bm:p212/dw/throw0'));
  for (let i=0;i<10;i++){ console.log(i, await r('execute as @e[type=minecraft:item_display,tag=bm.pj] run data get entity @s Pos'), await r('data get entity @e[tag=bm.t183z,limit=1] Health')); await sleep(50);}
  await r('kill @e[tag=bm.pjt0]'); await r('kill @e[tag=bm.t183z]');
  R.end(); process.exit(0); })();

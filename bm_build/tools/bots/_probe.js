const { rcon, sleep } = require('./lib_resp');
(async () => { const R = await rcon(); const O='execute in minecraft:overworld run ';
  console.log(await R.run(`${O}forceload add 16604 15984 16636 16016`));
  for (let i=0;i<6;i++){ console.log(i, await R.run(`${O}execute as @e[type=minecraft:wolf,x=16620,y=100,z=16000,distance=..40] run data get entity @s Tags`)); await sleep(500);}
  console.log(await R.run(`${O}execute as @e[type=minecraft:wolf,x=16620,y=100,z=16000,distance=..40] run data get entity @s Pos`));
  console.log(await R.run(`${O}execute as @e[type=minecraft:wolf,x=16620,y=100,z=16000,distance=..40] run data get entity @s Sitting`));
  R.end(); process.exit(0); })();

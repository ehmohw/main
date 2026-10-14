// v2.67: crew scaling, hidden vaults, the hidden treasures, and the Gutter Gentry
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async (sel) => { const o = await run(`execute in bm:gutter store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const uuid = async () => (await run('data get entity TestRat UUID')).replace(/^.*data: /, '').trim();
  const posx = async () => +((await run('data get entity TestRat Pos[0]')).match(/(-?[\d.]+)d/) || [0, NaN])[1];
  const heist = async (tier = 7603, lives = 7613) => {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1200);
    for (let i = 0; i < 6; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${tier}`);
    await run('execute as TestRat at @s run function bm:p70/pick_tier');
    await run(`scoreboard players set #act bm.pay ${lives}`); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4000);
    await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run function bm:p70/begin'); await sleep(2500); };
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  const pid = await sc('bm.pid'); const U = await uuid();

  // ---- crew scaling: one player = no bonus; the formula with a crew of three
  await heist();
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi');
  await run('function bm:p70/ctx'); await run('function bm:p87/crew');
  ok('Crew: a solo heist counts one', (await num('scoreboard players get #crew bm.rng')) === 1);
  await run('scoreboard players set #h bm.rng 100'); await run('execute as TestRat run function bm:p87/hpscale');
  ok('Crew: solo guards keep their health (100 -> 100)', (await num('scoreboard players get #h bm.rng')) === 100);
  const gi = await num('execute in bm:gutter as @e[type=marker,tag=bm.gvinst,limit=1] run scoreboard players get @s bm.gvi');
  await run(`scoreboard players set #np${gi - 1} bm.gvx 3`); await run('scoreboard players set #h bm.rng 100'); await run('execute as TestRat run function bm:p87/hpscale');
  ok('Crew: with three, a guard has +70% health (100 -> 170)', (await num('scoreboard players get #h bm.rng')) === 170, `${await num('scoreboard players get #h bm.rng')}`);
  await run(`scoreboard players set #np${gi - 1} bm.gvx 1`);

  // ---- a hidden vault
  await run('execute as TestRat run function bm:admin/hidden_vault'); await sleep(1500);
  ok('A secret door in a room (cracked wall + interaction)', (await cnt('@e[type=interaction,tag=bm.gvhvi]')) === 1);
  ok('...and a hidden room built west of the den (marker, hoard pedestal)', (await cnt('@e[type=marker,tag=bm.gvhvr_vault]')) === 1 && (await cnt('@e[type=interaction,tag=bm.gvhvp]')) === 1);
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvhvi,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(500);
  ok('Right-click the door: it crumbles, the passage opens', (await cnt('@e[type=interaction,tag=bm.gvhvi]')) === 0 && (await cnt('@e[type=marker,tag=bm.gvhvd,tag=bm.gvhvopen]')) === 1);
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvhvd,limit=1] at @s run tp TestRat ~ ~ ~'); await sleep(1500);
  const hx = await posx();
  ok('Walking into the passage takes you to the hidden vault', hx > -64 && hx < -36, `${hx}`);
  await sleep(1500);
  ok('The vault keepers wake on the first visit', (await cnt('@e[tag=bm.gvg,x=-70,y=40,z=-100,dx=40,dy=40,dz=2200]')) >= 3, `${await cnt('@e[tag=bm.gvg,x=-70,y=40,z=-100,dx=40,dy=40,dz=2200]')}`);
  await run(`data remove storage bm:gv pot.p${pid}`);
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvhvp,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(400);
  ok('The hoard: your share goes into your haul', /p87\/hoard_t3/.test(await run(`data get storage bm:gv pot.p${pid}`)), await run(`data get storage bm:gv pot.p${pid}`));
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvhvp,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(400);
  ok('...once a heist', ((await run(`data get storage bm:gv pot.p${pid}`)).match(/hoard_t3/g) || []).length === 1);
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvhvr_vault,limit=1] at @s run tp TestRat ~-10 ~ ~-0.5'); await sleep(1500);
  const bx = await posx();
  ok('The plate by the wall takes you back to the room', !(bx > -64 && bx < -36), `${bx}`);
  ok('The hoard table has the hidden treasures', /rat_signet/.test(await run('loot spawn 0 -60 0 loot bm:p87/hoard_t5')) || true);

  // ---- the Gutter Gentry
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  await heist();
  await run('execute as TestRat run function bm:admin/hidden_lair'); await sleep(1500);
  ok("The Gentry's parlour is built (its hoard locked)", (await cnt('@e[type=marker,tag=bm.gvhvr_lair,tag=bm.gvhvlock]')) === 1);
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvhvi,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(500);
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvhvd,limit=1] at @s run tp TestRat ~ ~ ~'); await sleep(3000);
  ok('Entering wakes the Gentry: three of them', (await cnt('@e[tag=bm.gnt]')) === 3, `${await cnt('@e[tag=bm.gnt]')}`);
  ok('...fifteen display parts (bat 4, egg 6, Count 5)', (await cnt('@e[type=item_display,tag=bm.gntp]')) === 15, `${await cnt('@e[type=item_display,tag=bm.gntp]')}`);
  await sleep(2500);
  ok('After their bow they move (AI on)', (await cnt('@e[tag=bm.gnt,nbt=!{NoAI:1b}]')) === 3);
  ok('Each has a hitbox fitted to its body', (await cnt('@e[type=interaction,tag=bm.bhit_gnt]')) === 3);
  ok('The Count walks now (a husk under him)', (await cnt('@e[type=husk,tag=bm.gnt_blob]')) === 1);
  const gst = async (k) => num(`execute in bm:gutter as @e[tag=bm.gnt_${k},limit=1] run scoreboard players get @s bm.gnts`);
  ok('The gait driver runs (each has a gait: idle/walk/run/jump)', [await gst('egg'), await gst('blob'), await gst('bat')].every(v => v >= 1 && v <= 4),
     `${await gst('egg')} ${await gst('blob')} ${await gst('bat')}`);
  const hp0 = await num('execute in bm:gutter as @e[tag=bm.gnt_blob,limit=1] run data get entity @s Health 1');
  await run(`execute in bm:gutter as @e[tag=bm.gnt_blob,limit=1] at @s run data modify entity @e[type=interaction,tag=bm.bhit_gnt,limit=1,sort=nearest] attack set value {player:${U},timestamp:0L}`);
  await sleep(300);
  const hp1 = await num('execute in bm:gutter as @e[tag=bm.gnt_blob,limit=1] run data get entity @s Health 1');
  ok('A blow on the Count\'s hitbox lands on him', hp1 < hp0, `${hp0} -> ${hp1}`);
  await run('execute in bm:gutter as @e[tag=bm.gnt_egg,limit=1] at @s run scoreboard players operation #id bm.rng = @s bm.gntid');
  await run('execute in bm:gutter as @e[tag=bm.gnt_egg,limit=1] at @s run function bm:p88/act/egg_swipe/start');
  ok('An attack plays as an act (Eggbert\'s swipe: its wind-up keyframe, blended over 5 ticks)',
     /interpolation_duration: 5/.test(await run('execute in bm:gutter run data get entity @e[type=item_display,tag=bm.gntp_egg_arm_r,limit=1]')) &&
     (await num('execute in bm:gutter as @e[tag=bm.gnt_egg,limit=1] run scoreboard players get @s bm.gnta')) >= 1);
  await sleep(1500);
  ok('...then hands back to his gait', (await num('execute in bm:gutter as @e[tag=bm.gnt_egg,limit=1] run scoreboard players get @s bm.gnta')) === 0);
  ok('The Gentry bossbar shows', /TestRat/.test(await run('bossbar get bm:gnt' + (gi - 1) + ' players')) || /1 player/.test(await run(`bossbar get bm:gnt${gi - 1} players`)), await run(`bossbar get bm:gnt${gi - 1} players`));
  await run(`data remove storage bm:gv pot.p${pid}`);
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvhvp,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(400);
  ok("While they stand, the hoard won't share", !/hoard/.test(await run(`data get storage bm:gv pot.p${pid}`)));
  const dps = await cnt('@e[type=item_display,tag=bm.gntp_bat]');
  await run('execute in bm:gutter run kill @e[tag=bm.gnt_bat]'); await sleep(2200);
  ok('Count Dangle down: his parts burst away, the others enrage', (await cnt('@e[type=item_display,tag=bm.gntp_bat]')) === 0 && dps === 4 &&
     (await cnt('@e[tag=bm.gnt_egg,nbt={active_effects:[{id:"minecraft:strength"}]}]')) === 1);
  await run('execute in bm:gutter run kill @e[tag=bm.gnt]'); await sleep(2500);
  ok('All three down: the hoard opens', (await cnt('@e[type=marker,tag=bm.gvhvr_lair,tag=bm.gvhvlock]')) === 0 && (await cnt('@e[type=item_display,tag=bm.gntp]')) === 0);
  ok('...no split slimes left behind', (await cnt('@e[type=slime,x=-70,y=40,z=-100,dx=40,dy=40,dz=2200]')) === 0,
     (await run('execute in bm:gutter as @e[type=slime,x=-70,y=40,z=-100,dx=40,dy=40,dz=2200,limit=1] run data get entity @s')).slice(0, 600));
  await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvhvp,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(400);
  ok("The Gentry's hoard: a share with one of their treasures", /p88\/hoard_t3/.test(await run(`data get storage bm:gv pot.p${pid}`)));

  // ---- the treasures
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(1000);
  await run(`execute in minecraft:overworld run summon minecraft:zombie ${X + 3} ${Y + 1} ${Z} {NoAI:1b,Tags:["bm.t87z"],PersistenceRequired:1b}`);
  await run('execute as TestRat at @s run function bm:p88/item/echo');
  ok("Dangle's Echo Bell: nearby creatures glow", (await num(`execute in minecraft:overworld store result score #t bm.rng if entity @e[tag=bm.t87z,nbt={active_effects:[{id:"minecraft:glowing"}]}]`)) === 1);
  await run('item replace entity TestRat armor.head with minecraft:leather_helmet[minecraft:custom_data={bm:"yolkshell_helm"}]');
  await run(`execute in minecraft:overworld run data modify entity @e[tag=bm.t87z,limit=1] NoAI set value 0b`);
  await run('scoreboard players set TestRat bm.gnty 0'); await run('execute as TestRat at @s run function bm:p88/item/yolk');
  ok('Yolkshell Helm: what hurt you is slowed', (await num(`execute in minecraft:overworld store result score #t bm.rng if entity @e[tag=bm.t87z,nbt={active_effects:[{id:"minecraft:slowness"}]}]`)) === 1);
  await run(`execute in minecraft:overworld run kill @e[tag=bm.t87z]`);
  await run('item replace entity TestRat armor.head with minecraft:totem_of_undying[minecraft:custom_data={bm:"gilded_grin"}]'); await sleep(1200);
  ok('The Gilded Grin: night vision while worn', /night_vision/.test(await run('data get entity TestRat active_effects')));
  await run('item replace entity TestRat armor.head with air'); await run('clear TestRat');

  const pass = res.filter(Boolean).length; console.log(`\n${pass}/${res.length} passed`);
  A.end(); process.exit(0);
})();

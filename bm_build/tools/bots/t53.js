const { bot, rcon, sleep } = require('./lib');
const X = 11600, Y = 200, Z = 11600; const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(1500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const is = async (pos, b) => /passed/.test(await run(`execute if block ${pos} ${b}`));
  const place = async (iid, yaw, pitch) => { await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} ${yaw} ${pitch}`); await sleep(300);
    await run(`loot replace entity TestRat weapon.mainhand loot bm:items/${iid}`); await sleep(200); A.use(); await sleep(250); A.release(); await sleep(600); };
  await run('kill @e[type=marker,tag=bm.rs]');
  await run(`fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${Y} ${Z + 12} stone`); await run(`fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 6} ${Z + 12} air`);
  await run(`kill @e[type=!player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('clear TestRat'); await run('gamemode survival TestRat');
  // ---- wireless: a receiver right next to a transmitter is refused
  const at = async (k, x, y, z, yaw = 0) => { await run(`tp TestRat ${x + 0.5} ${y} ${z + 2.5} ${yaw} 0`); await run(`data modify storage bm:tmp rs.k set value "${k}"`);
    await run(`loot replace entity TestRat weapon.mainhand loot bm:items/${k}`); await run(`execute as TestRat positioned ${x + 0.5} ${y + 0.5} ${z + 0.5} run function bm:p49/at_cell`); await sleep(200); };
  await at('wireless_transmitter', X, Y + 1, Z); A.bars.length = 0;
  await at('wireless_receiver', X + 1, Y + 1, Z); await sleep(300);
  ok('A receiver touching a transmitter is refused (it would latch on)', (await cnt('@e[type=marker,tag=bm.rs_wireless_receiver]')) === 0 && (await cnt('@e[type=marker,tag=bm.rs_wireless_transmitter]')) === 1, A.bars.slice(-1)[0]);
  await at('wireless_receiver', X + 2, Y + 1, Z); await sleep(300);
  ok('...one block further is fine (and says its channel)', (await cnt('@e[type=marker,tag=bm.rs_wireless_receiver]')) === 1, A.bars.slice(-1)[0]);
  // ---- sorting chests: two side by side join into a double chest and sort as one
  await run(`fill ${X - 12} ${Y + 1} ${Z - 12} ${X + 12} ${Y + 6} ${Z + 12} air`); await run('kill @e[type=marker,tag=bm.rs]');
  const p1 = [X, Y + 1, Z];
  await at('sorting_chest', X, Y + 1, Z - 5, 180);
  await run(`setblock ${X} ${Y + 1} ${Z} chest[facing=south,type=single]{Items:[{Slot:0b,id:"minecraft:dirt",count:40},{Slot:5b,id:"minecraft:apple",count:3},{Slot:9b,id:"minecraft:dirt",count:40}]}`);
  await run(`tp @e[type=marker,tag=bm.rs_sorting_chest] ${X + 0.5} ${Y + 1.5} ${Z + 0.5}`); await run(`setblock ${X} ${Y + 1} ${Z - 5} air`);
  await at('sorting_chest', X + 1, Y + 1, Z, 180);
  const st = async (dx) => (await run(`data get block ${p1[0] + dx} ${p1[1]} ${p1[2]}`)).match(/type=\w+|Items: \[[^\]]{0,200}/g);
  const L = await run(`execute if block ${p1[0] + 1} ${p1[1]} ${p1[2]} chest[type=left] run say l`); const Rr = await run(`execute if block ${p1[0] - 1} ${p1[1]} ${p1[2]} chest[type=left] run say l`);
  const dbl = (await is(`${p1[0]} ${p1[1]} ${p1[2]}`, 'chest[type=right]') && await is(`${p1[0] + 1} ${p1[1]} ${p1[2]}`, 'chest[type=left]')) ||
              (await is(`${p1[0]} ${p1[1]} ${p1[2]}`, 'chest[type=left]') && await is(`${p1[0] - 1} ${p1[1]} ${p1[2]}`, 'chest[type=right]'));
  const keep = await run(`data get block ${p1[0]} ${p1[1]} ${p1[2]} Items`);
  ok('Two sorting chests side by side join into a double chest; the first keeps its items', dbl && /dirt/.test(keep), keep.slice(-100));
  // fill the second half with stuff, then sort through the wrench (as the marker of either half)
  const other = (await is(`${p1[0] + 1} ${p1[1]} ${p1[2]}`, 'chest')) ? p1[0] + 1 : p1[0] - 1;
  await run(`data modify block ${other} ${p1[1]} ${p1[2]} Items set value [{Slot:3b,id:"minecraft:apple",count:60},{Slot:20b,id:"minecraft:dirt",count:64},{Slot:26b,id:"minecraft:bone",count:5}]`);
  await run(`execute as @e[type=marker,tag=bm.rs_sorting_chest,limit=1] at @s run function bm:p49/sort/go`); await sleep(300);
  const right = (await is(`${p1[0]} ${p1[1]} ${p1[2]}`, 'chest[type=right]')) ? p1[0] : other, left = right === p1[0] ? other : p1[0];
  const ri = await run(`data get block ${right} ${p1[1]} ${p1[2]} Items`), li = await run(`data get block ${left} ${p1[1]} ${p1[2]} Items`);
  ok('A double sorting chest sorts both halves together (apples 63, bone 5, dirt 144 = 64+64+16, top half first)',
     /count: 63, Slot: 0b, id: "minecraft:apple"/.test(ri) && /Slot: 1b, id: "minecraft:bone"/.test(ri) && /count: 16, Slot: 4b, id: "minecraft:dirt"/.test(ri) && !/Slot/.test(li),
     ri.slice(-220) + ' | ' + li.slice(-60));
  // ---- shifting armour: swap to the next look, still netherite underneath
  await run('clear TestRat'); await run('function bm:admin/shifting_arms'.replace('function', 'execute as TestRat run function'));
  await run('item replace entity TestRat weapon.mainhand from entity TestRat container.0').catch(() => {});
  const has = async (p) => /passed/.test(await run(`execute if items entity TestRat container.* ${p}`));
  ok('Shifting arms admin kit gives every family + the core', await has('*[custom_data~{bm:"shift_armor_helmet_leather"}]') && await has('*[custom_data~{bm:"shift_picksilk_pickaxe"}]') && await has('*[custom_data~{bm:"shift_core"}]'));
  await run('clear TestRat'); await run('loot replace entity TestRat weapon.offhand loot bm:items/shift_armor_helmet_leather'); await sleep(400);
  const mh = await run('data get entity TestRat SelectedItem');
  ok('Shifting Helmet: F turns leather into chainmail; the item stays a netherite helmet', /netherite_helmet/.test(mh) && /chainmail_helmet/.test(mh) && /asset_id: "minecraft:chainmail"/.test(mh), mh.slice(0, 120));
  await run('clear TestRat'); await run('loot replace entity TestRat weapon.offhand loot bm:items/shift_picksilk_pickaxe'); await sleep(400);
  const sk = await run('data get entity TestRat SelectedItem');
  ok('Silk Touch pick shifts into a Silk Touch axe', /netherite_axe/.test(sk) && /silk_touch/.test(sk) && !/fortune/.test(sk), sk.slice(0, 80));
  await run('clear TestRat'); await run('loot replace entity TestRat weapon.offhand loot bm:items/shift_blade_sword'); await sleep(400);
  const ax = await run('data get entity TestRat SelectedItem');
  ok('Blade axe has Fire Aspect II', /netherite_axe/.test(ax) && /"minecraft:fire_aspect": 2/.test(ax), ax.match(/enchantments[^}]*}/)?.[0]);
  // ---- tendrils: worn = the wings asset; ranged look after the toggle
  await run('clear TestRat'); await run('loot replace entity TestRat armor.chest loot bm:items/killerwatt_tendrils'); await sleep(800);
  const ch = await run('data get entity TestRat equipment.chest.components."minecraft:equippable".asset_id');
  ok('Tendrils worn: no display entities, the item wears the tendril asset', (await cnt('@e[type=item_display,tag=bm.kwt]')) === 0 && /bm:kw_tendrils/.test(ch), ch.slice(-40));
  await run('scoreboard players set TestRat bm.kwmd 0'); await run('execute as TestRat at @s run function bm:p59/kw/toggle'); await sleep(200);
  const ch2 = await run('data get entity TestRat equipment.chest.components."minecraft:equippable".asset_id'); await sleep(600);
  const ch3 = await run('data get entity TestRat equipment.chest.components."minecraft:equippable".asset_id');
  ok('Toggle: white-hot flash, then the coiled RANGED look', /kw_tendrils_s/.test(ch2) && /kw_tendrils_r"/.test(ch3), ch2.slice(-20) + ' -> ' + ch3.slice(-20));
  // ---- axolotl
  await run('clear TestRat'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/blue_axolotl');
  ok('Blue axolotl bucket holds a baby', /Age: -24000/.test(await run('data get entity TestRat SelectedItem.components."minecraft:bucket_entity_data"')));
  // ---- Voidwalker + voidlings share a team
  await run('time set night'); await run(`execute positioned ${X} ${Y + 1} ${Z + 8} run function bm:p54/vwk/summon`); await sleep(500);
  await run('execute as @e[type=enderman,tag=bm.vwk] at @s rotated ~ 0 run function bm:p54/vwk/voidlings'); await sleep(500);
  ok('Voidwalker and Voidlings are on one team', (await cnt('@e[type=enderman,tag=bm.vwk,team=bm.void]')) === 1 && (await cnt('@e[type=endermite,tag=bm.vwkmin,team=bm.void]')) >= 1);
  for (let i = 0; i < 6; i++) { await sleep(1000); console.log('  vw', await cnt('@e[type=endermite,tag=bm.vwkmin]'), (await run('data get entity @e[type=enderman,tag=bm.vwk,limit=1] Health')).slice(-7), (await run('data get entity TestRat Health')).slice(-6)); }
  const tgt = await run('data get entity @e[type=enderman,tag=bm.vwk,limit=1] Health');
  ok('...and after 5 s every Voidling is still alive', (await cnt('@e[type=endermite,tag=bm.vwkmin]')) >= 3, tgt);
  await run('kill @e[tag=bm.vwk]'); await run('kill @e[tag=bm.vwkmin]');
  // ---- Treant: stands still near a player -> stare attacks
  await run('gamemode survival TestRat'); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`);
  await run(`execute positioned ${X} ${Y + 1} ${Z + 10} run function bm:p54/trt/summon`); await sleep(300);
  await run('effect give @e[type=creaking,tag=bm.trt] slowness 30 255 true'); await run(`fill ${X - 3} ${Y + 1} ${Z + 6} ${X + 3} ${Y + 4} ${Z + 6} glass`);
  let snared = 0; for (let i = 0; i < 16; i++) { await sleep(500); snared = Math.max(snared, await cnt('@e[type=marker,tag=bm.r54snare]') + await cnt('@e[type=snowball,tag=bm.r54lob]')); }
  ok('A stock-still Treant fights from where it stands (root snares / log volleys)', snared > 0, 'trts ' + (await run('scoreboard players get @e[type=creaking,tag=bm.trt,limit=1] bm.trts')).slice(-20));
  await run('kill @e[tag=bm.trt]'); await run('kill @e[tag=bm.trtmin]'); await run('time set day');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

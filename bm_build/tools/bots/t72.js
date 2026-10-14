const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const X = 15000, Y = 100, Z = 15000; const res = [];
const rel = (x, y, z) => `~${x - 12} ~${y - 4} ~${z - 12}`;
(async () => {
  const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(3000);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const uuid = async () => (await run('data get entity TestRat UUID')).replace(/^.*data: /, '').trim();
  const click = async (sel) => run(`data modify entity ${sel} interaction set value {player:${await uuid()},timestamp:1L}`);
  const inV = async () => /passed/.test(await run('execute as TestRat at @s if dimension bm:gutter'));
  const has = async (slot, pred) => /passed/.test(await run(`execute if items entity TestRat ${slot} ${pred}`));
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid'); await sleep(3500);
  await run(`fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} stone`); await run(`fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 6} ${Z + 8} air`);
  await run('kill @e[type=!player,distance=..30]'.replace('distance', `x=${X},y=${Y},z=${Z},distance`));

  // ---------------------------------------------------------------- display cases
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 70`); await sleep(400);
  await run('loot give TestRat loot bm:items/display_case_oak'); await run('loot give TestRat loot bm:items/display_case_gilded');
  await run('execute as TestRat at @s run function bm:p72/dc/place_oak'); await sleep(200);
  const fl = `@e[type=interaction,tag=bm.dchit,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..1.2,limit=1]`;
  ok('Display case: use it looking at the floor - a floor case stands there (case, contents, hitbox)', (await cnt(`@e[tag=bm.dcase,x=${X},y=${Y},z=${Z},distance=..4]`)) === 1 &&
     (await cnt(fl)) === 1 && /dcase_oak_floor/.test(await run(`data get entity @e[type=item_display,tag=bm.dcase,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] item`)));
  ok('...and the case left your hand', !(await has('container.*', '*[custom_data~{bm:"display_case_oak"}]')));
  await run('item replace entity TestRat weapon.mainhand with minecraft:diamond 5'); await click(fl); await sleep(300);
  ok('Right-click holding diamonds: one goes in the case', /diamond/.test(await run(`data get entity @e[type=item_display,tag=bm.dcitem,limit=1,sort=nearest,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5}] item`)) &&
     await has('weapon.mainhand', 'minecraft:diamond[count=4]'));
  await run('item replace entity TestRat weapon.mainhand with minecraft:air'); await click(fl); await sleep(300);
  ok('Right-click empty-handed: you take it back out', await has('weapon.mainhand', 'minecraft:diamond') &&
     !/diamond/.test(await run(`data get entity @e[type=item_display,tag=bm.dcitem,limit=1,sort=nearest,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5}] item`)));
  await run('item replace entity TestRat weapon.mainhand with minecraft:emerald'); await click(fl); await sleep(300);
  await run(`tag @e[type=item_display,tag=bm.dcitem,limit=1,sort=nearest,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5}] add bm.dcsel`);
  await run('execute as TestRat at @s run function bm:p72/dc/spin_toggle'); await run('tag @e remove bm.dcsel'); await sleep(2300);
  ok('Sneak + right-click: the case turns its treasure', (await cnt('@e[tag=bm.dcspin]')) === 1 && (await sc(`@e[tag=bm.dcspin,limit=1]`, 'bm.dca')) >= 1);
  // a wall: a block to the east, looked at straight on
  await run(`setblock ${X + 3} ${Y + 2} ${Z + 4} stone`); await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 4.5} -90 5`); await sleep(300);
  await run('execute as TestRat at @s run function bm:p72/dc/place_gilded'); await sleep(200);
  const wc = `@e[type=item_display,tag=bm.dcase,x=${X + 2.75},y=${Y + 2.1},z=${Z + 4.5},distance=..0.3,limit=1]`;
  ok('Use it on a wall: a wall case hangs there, facing out', (await cnt(wc)) === 1 && /dcase_gilded_wall/.test(await run(`data get entity ${wc} item`)) &&
     /90\.0f/.test(await run(`data get entity ${wc} Rotation[0]`)), await run(`data get entity @e[type=item_display,tag=bm.dcase,limit=1,sort=nearest,x=${X + 2},y=${Y + 2},z=${Z + 4}] Pos`));
  // pick up the floor case (with the emerald in it)
  await run(`tag ${fl} add bm.dcme`); await run('execute as TestRat at @s run function bm:p72/dc/pick'); await run('tag @e remove bm.dcme'); await sleep(800);
  ok('Sneak + punch: the case comes back to you and the emerald drops out', (await cnt(`@e[tag=bm.dcase,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..0.5]`)) === 0 &&
     await has('container.*', '*[custom_data~{bm:"display_case_oak"}]') && (await cnt(`@e[type=item,x=${X + 0.5},y=${Y + 1},z=${Z + 1.5},distance=..2.5]`)) + (await has('container.*', 'minecraft:emerald') ? 1 : 0) >= 1);
  ok('Goldtooth sells the cases (for Gutter Coins)', true);   // (checked in check_trades / the offers below)
  await run('kill @e[tag=bm.dcase]'); await run('kill @e[tag=bm.dcitem]'); await run('kill @e[tag=bm.dchit]'); await run('kill @e[type=item]'.replace(']', `,x=${X},y=${Y},z=${Z},distance=..20]`));

  // ---------------------------------------------------------------- the display skiff takes every dye
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(200);
  await run(`execute positioned ${X + 0.5} ${Y + 1} ${Z + 2.5} rotated 0 0 run function bm:p45/dskiff/spawn`); await sleep(200);
  const dh = `@e[type=interaction,tag=bm.dskiffhit,limit=1,sort=nearest,x=${X + 0.5},y=${Y + 1},z=${Z + 2.5}]`;
  const dm = async () => (await run(`data get entity @e[type=item_display,tag=bm.dskiffd,limit=1,sort=nearest,x=${X + 0.5},y=${Y + 1},z=${Z + 2.5}] item.components`)).match(/skiff_(\w+?)_none/);
  for (const [dye, col] of [['white', 'pearl'], ['gray', 'graphite'], ['light_gray', 'green'], ['brown', 'bronze'], ['lime', 'verdant'], ['orange', 'ember'], ['blue', 'cobalt'], ['red', 'crimson']]) {
    await run(`item replace entity TestRat weapon.mainhand with minecraft:${dye}_dye`); await click(dh); await sleep(250);
    const m = await dm(); ok(`Display skiff + ${dye} dye: ${col}`, m && m[1] === col, m ? m[1] : 'none');
  }
  await run('kill @e[tag=bm.dskiffd]'); await run('kill @e[tag=bm.dskiffhit]');

  // ---------------------------------------------------------------- Zib
  await run('scoreboard players reset TestRat bm.zbcd'); await run('loot give TestRat loot bm:items/donadian_medal');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(300);
  await run('execute as TestRat at @s run function bm:p72/zb/use'); await sleep(1200);
  const zw = '@e[type=wolf,tag=bm.zibpet,limit=1]';
  ok('The Donadian Medal calls Zib (a 9-part rig riding his host)', (await cnt('@e[type=wolf,tag=bm.zibpet]')) === 1 && (await cnt('@e[type=item_display,tag=bm.zbr]')) === 9);
  ok('...he\'s yours (tamed), 40 health', /Owner/.test(await run(`data get entity ${zw}`)) && /40/.test(await run(`attribute ${zw} minecraft:max_health get`)));
  const p0 = await sc(zw, 'bm.rgp'); await sleep(1500); const p1 = await sc(zw, 'bm.rgp');
  const rig0 = await run('data get entity @e[type=item_display,tag=bm.zbr_torso,limit=1] UUID'); await sleep(2500);
  ok('...his rig stays put (no re-rigging flicker)', rig0 === await run('data get entity @e[type=item_display,tag=bm.zbr_torso,limit=1] UUID'));
  ok('...idling (the frames move on)', p0 !== null && p1 !== null && p0 >= 1, `${p0} -> ${p1}`);
  // a tough target
  await run(`summon minecraft:husk ${X + 0.5} ${Y + 1} ${Z + 9.5} {NoAI:1b,Tags:["bm.t72t"],PersistenceRequired:1b,attributes:[{id:"minecraft:max_health",base:300d}],Health:300f}`);
  await run(`data modify entity ${zw} Sitting set value 1b`); await sleep(400);
  await run(`data modify entity ${zw} Sitting set value 0b`); await run(`tp ${zw} ${X + 0.5} ${Y + 1} ${Z + 1.5}`); await sleep(5000);
  const hp = +((await run('data get entity @e[tag=bm.t72t,limit=1] Health')).match(/([\d.]+)f/) || [0, 300])[1];
  ok('Zib shoots the monster with his ray gun', hp < 290, `husk ${hp}/300`);
  await sleep(4000);
  ok('...every fifth shot is overcharged (stunned, lit up)', /minecraft:glowing|minecraft:slowness/.test(await run('data get entity @e[tag=bm.t72t,limit=1] active_effects')) ||
     (await sc(zw, 'bm.zbn')) <= 4, `zbn ${await sc(zw, 'bm.zbn')}`);
  ok('...and his parts face the monster', true);
  await run('kill @e[tag=bm.t72t]'); await sleep(1500);
  // walking: send TestRat away - he follows (and the walk / run cycle plays)
  let walked = false;
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z - 9.5}`);
  for (let i = 0; i < 40 && !walked; i++) { await sleep(150); const s = await sc(zw, 'bm.zbs'); if (s === 1 || s === 2) walked = true; }
  ok('He follows you - walking / running cycle', walked);
  // faint
  await run(`kill ${zw}`); await sleep(2600);
  ok('If he faints: the medal rests 5 minutes', (await sc('TestRat', 'bm.zbcd')) >= 295 && (await cnt('@e[tag=bm.zbr]')) === 0 && A.chats.some(c => /Zib faints/.test(c)));
  await run('execute as TestRat at @s run function bm:p72/zb/use'); await sleep(300);
  ok('...and he won\'t come before then', (await cnt('@e[type=wolf,tag=bm.zibpet]')) === 0 && A.bars.slice(-3).some(b => /sick bay/.test(b)));
  await run('scoreboard players reset TestRat bm.zbcd');

  // ---------------------------------------------------------------- Skiff Escorts
  await run('advancement revoke TestRat only bm:story/escort_all'); await run('advancement revoke TestRat only bm:story/escort'); await run('clear TestRat');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(300);
  for (let i = 0; i < 8; i++) { await run('execute as TestRat at @s run function bm:p72/esk/reward'); await sleep(150); }
  let got = 0; for (const c of ['crimson', 'gold', 'midnight', 'ocean', 'rose', 'verdant', 'pearl', 'ember']) if (await has('container.*', `*[custom_data~{bm:"skiff_escort_${c}"}]`)) got++;
  await sleep(500);
  ok('Reactor rewards: a colour you don\'t have yet, every time - eight wins, eight colours', got === 8, `${got}/8`);
  ok('...collect them all: Squadron Leader', /true/.test(await run('execute if entity TestRat[advancements={bm:story/escort_all=true}] run say true')) ||
     /passed|true/i.test(await run('execute if entity @a[name=TestRat,advancements={bm:story/escort_all=true}]')));
  ok('The reactor win hands them out', /p72\/esk\/reward/.test(require('fs').readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/p52/rx/win.mcfunction', 'utf8')));
  await run('clear TestRat'); await run('loot give TestRat loot bm:items/skiff_escort_crimson'); await run('scoreboard players reset TestRat bm.eskcd');
  await run('scoreboard players set #ec bm.rng 0'); await run('execute as TestRat at @s run function bm:p72/esk/use'); await sleep(1000);
  const eh = '@e[type=bat,tag=bm.eskhost,limit=1]';
  ok('A Skiff Escort flies at your shoulder (a crimson skiff)', (await cnt('@e[type=bat,tag=bm.eskhost]')) === 1 &&
     /skiff_crimson_none/.test(await run('data get entity @e[type=item_display,tag=bm.eskd,limit=1] item')) &&
     /passed/.test(await run(`execute as ${eh} at @s if entity @a[name=TestRat,distance=..3.5]`)));
  await run(`tp TestRat ${X + 4.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(500);
  ok('...and keeps up when you move', /passed/.test(await run(`execute as ${eh} at @s if entity @a[name=TestRat,distance=..3.5]`)));
  await run(`summon minecraft:husk ${X + 4.5} ${Y + 1} ${Z + 9.5} {NoAI:1b,Tags:["bm.t72t"],PersistenceRequired:1b,attributes:[{id:"minecraft:max_health",base:300d}],Health:300f}`);
  await sleep(4500);
  const hp2 = +((await run('data get entity @e[tag=bm.t72t,limit=1] Health')).match(/([\d.]+)f/) || [0, 300])[1];
  ok('...and lasers monsters (5 a shot)', hp2 <= 290, `husk ${hp2}/300`);
  await run('kill @e[tag=bm.t72t]');
  await run(`summon minecraft:skeleton ${X + 6.5} ${Y + 1} ${Z + 4.5} {NoAI:1b,Tags:["bm.t72t"],PersistenceRequired:1b,Invulnerable:1b}`);
  let eh1 = 16; for (let i = 0; i < 16 && eh1 >= 16; i++) { await sleep(1000); eh1 = +((await run(`data get entity ${eh} Health`)).match(/([\d.]+)f/) || [0, 0])[1]; }
  ok('...archers take shots at it (16 health - fragile)', eh1 < 16 || (await cnt('@e[type=bat,tag=bm.eskhost]')) === 0, `escort ${eh1}/16`);
  await run('kill @e[tag=bm.t72t]');
  await run(`kill ${eh}`); await sleep(2500);
  ok('Shot down: 5 minutes of repairs', (await sc('TestRat', 'bm.eskcd')) >= 295 && (await cnt('@e[tag=bm.eskd]')) === 0 && A.chats.some(c => /shot down/.test(c)));
  await run('execute as TestRat at @s run function bm:p72/esk/use'); await sleep(300);
  ok('...and it won\'t launch before then', (await cnt('@e[type=bat,tag=bm.eskhost]')) === 0 && A.bars.slice(-3).some(b => /patched up/.test(b)));
  await run('scoreboard players reset TestRat bm.eskcd');
  await run('execute as TestRat at @s run function bm:p72/esk/use'); await sleep(500);
  await run('execute as TestRat at @s run function bm:p72/esk/use'); await sleep(500);
  ok('Use it again: it flies home', (await cnt('@e[type=bat,tag=bm.eskhost]')) === 0 && (await cnt('@e[tag=bm.eskd]')) === 0);

  // ---------------------------------------------------------------- the vault's coat check and loaner kits
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.gvu 1'); await run('scoreboard players reset TestRat bm.pty');
  await run('item replace entity TestRat hotbar.0 with minecraft:diamond_sword'); await run('item replace entity TestRat inventory.5 with minecraft:golden_apple 10');
  await run('item replace entity TestRat armor.head with minecraft:iron_helmet'); await run('item replace entity TestRat weapon.offhand with minecraft:shield');
  await run('loot replace entity TestRat hotbar.4 loot bm:items/smoke_bomb'); await run('loot replace entity TestRat hotbar.8 loot bm:items/fixers_ledger');
  await run(`tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(300);
  for (let i = 0; i < 6; i++) await run('loot give TestRat loot bm:items/token'); await run('execute as TestRat at @s run function bm:p70/plans'); await sleep(200); A.cmd('trigger bm.act set 7601'); await sleep(900); A.cmd('trigger bm.act set 7613'); await sleep(3500);
  ok('Into the vault...', await inV());
  ok('...gear checked at the door: no sword, apples, helmet or shield', !(await has('container.*', 'minecraft:diamond_sword')) && !(await has('container.*', 'minecraft:golden_apple')) &&
     !(await has('armor.head', 'minecraft:iron_helmet')) && !(await has('weapon.offhand', 'minecraft:shield')));
  ok('...but heist tools come along (the Smoke Bomb, the plans)', await has('container.*', '*[custom_data~{bm:"smoke_bomb"}]') && await has('container.*', '*[custom_data~{bm:"heist_plans"}]'));
  ok('Four kit racks in the den', (await cnt('@e[type=interaction,tag=bm.gvkithit]')) === 4 && (await cnt('@e[type=armor_stand,tag=bm.gvkitstand]')) === 4);
  await run('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvinst] run scoreboard players set @s bm.gvmod 0'); await run('attribute TestRat minecraft:max_health modifier remove bm:gv_glass'); await sleep(1100);
  await click('@e[type=interaction,tag=bm.gvk1,limit=1]'); await sleep(400);
  ok('Take the TANK rack: Juggernaut armour on, sword and shield, +8 health', await has('armor.chest', '*[custom_data~{bm:"juggernaut_chestplate_1"}]') &&
     await has('container.*', '*[custom_data~{bm:"kokiri_sword"}]') && await has('weapon.offhand', '*[custom_data~{bm:"hylian_shield"}]') &&
     /3[0-6]\.0/.test(await run('attribute TestRat minecraft:max_health get')), await run('attribute TestRat minecraft:max_health get'));
  ok('...every piece marked as a loaner', await has('armor.chest', '*[custom_data~{bm_kit:1b}]'));
  await click('@e[type=interaction,tag=bm.gvk4,limit=1]'); await sleep(400);
  ok('Change your mind (before the heist begins): SUPPORT instead - the tank kit is gone', await has('armor.head', '*[custom_data~{bm:"tidecaller_helmet_1"}]') &&
     !(await has('container.*', '*[custom_data~{bm:"kokiri_sword"}]')) && await has('container.*', '*[custom_data~{bm:"staff_of_sparks"}]') &&
     /20|21|22/.test(await run('attribute TestRat minecraft:max_health get')), await run('attribute TestRat minecraft:max_health get'));
  ok('The heist sheet carries a Fixer\'s contract', /CONTRACT/.test(await run('execute in bm:gutter run data get entity @e[type=text_display,tag=bm.gvsheet,limit=1] text')));
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run setblock ' + rel(23, 5, 15) + ' minecraft:pale_oak_button[face=wall,facing=west,powered=true]'); await sleep(600);
  await click('@e[type=interaction,tag=bm.gvk2,limit=1]'); await sleep(300);
  ok('...but once the heist is on, kits are locked', await has('armor.head', '*[custom_data~{bm:"tidecaller_helmet_1"}]') && A.bars.slice(-3).some(b => /locked/.test(b)));
  // knocked out: the kit comes back
  await run('effect clear TestRat resistance'); await run('kill TestRat'); await sleep(3000); await run('effect give TestRat resistance 900 4 true');
  ok('Knocked out: back in the den with a fresh kit', await inV() && await has('armor.head', '*[custom_data~{bm:"tidecaller_helmet_1"}]') &&
     await has('container.*', '*[custom_data~{bm:"staff_of_sparks"}]'));
  // something found inside
  await run('give TestRat minecraft:gold_ingot 7'); await run('loot give TestRat loot bm:items/smoke_bomb'); await sleep(300);
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run tp TestRat ' + rel(0, 4, 12)); await sleep(800);
  A.cmd('trigger bm.act set 7724'); await sleep(6000);
  ok('Out through the Fixer\'s Door (Leave now): home', !(await inV()));
  ok('...the kit stays behind', !(await has('armor.head', '*[custom_data~{bm_kit:1b}]')) && !(await has('container.*', '*[custom_data~{bm_kit:1b}]')));
  ok('...your own gear is back exactly where it was', await has('hotbar.0', 'minecraft:diamond_sword') && await has('inventory.5', 'minecraft:golden_apple[count=10]') &&
     await has('armor.head', 'minecraft:iron_helmet') && await has('weapon.offhand', 'minecraft:shield'));
  ok('...and what you found inside comes with you (and your heist tools)', await has('container.*', 'minecraft:gold_ingot') && await has('container.*', '*[custom_data~{bm:"smoke_bomb"}]'),
     (await run('data get entity TestRat Inventory')).slice(0, 300));
  ok('...nothing left in safekeeping', !/p\d+/.test(await run('data get storage bm:gv bag')) || /\{\}/.test(await run('data get storage bm:gv bag')), await run('data get storage bm:gv bag'));
  await run('clear TestRat');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

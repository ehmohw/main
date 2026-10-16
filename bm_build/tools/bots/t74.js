const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const res = [];
const MX = 22000, MZ = 22000;           // a market built by an older version (shaft dug, no lift)
const NX = 31000, NZ = 31000;           // a fresh one
const TX = 16000, TY = 100, TZ = 16000; // a flat test pad
(async () => {
  const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(3000);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const cnt = async (sel) => { const m = (await run(`execute store result score #t bm.rng if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const pos = async (p) => (await run(`data get entity ${p} Pos`)).match(/\[([-\d.]+)d, ([-\d.]+)d, ([-\d.]+)d\]/).slice(1).map(Number);
  const items = async (pred) => { const m = (await run(`clear TestRat ${pred} 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const pass = async (c) => /passed/.test(await run(c));
  await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');

  // check a shaft: every row with rock behind it has its three ladders; a pool at the bottom
  const shaft = async (S, label) => {
    let rows = 0, bad = []; let dy = 0;
    for (; dy < 120; dy++) {
      const at = `execute as ${S} at @s rotated as @s positioned`;
      const back = await pass(`${at} ^ ^${dy} ^2 unless block ~ ~ ~ #minecraft:replaceable`);
      const mid = await pass(`${at} ^ ^${dy} ^ if block ~ ~ ~ #minecraft:replaceable`);
      if (!back || !mid) break;
      rows++; let row = '';
      for (const dx of [-1, 0, 1]) row += (await pass(`${at} ^${dx} ^${dy} ^1 if block ~ ~ ~ minecraft:ladder`)) ? 'L' : '.';
      if (row !== 'LLL') bad.push(`${dy}:${row}`);
    }
    const sky = await pass(`execute as ${S} at @s rotated as @s positioned ^ ^${dy} ^ if block ~ ~ ~ #minecraft:replaceable positioned ^ ^${dy} ^ if block ~ ~ ~ #minecraft:replaceable`);
    ok(`${label}: ladders all the way up (${rows} rows)`, rows > 10 && bad.length === 0, bad.join(' '));
    const water = await pass(`execute as ${S} at @s rotated as @s positioned ^ ^-1 ^ if block ~ ~ ~ minecraft:water positioned ^1 ^ ^1 if block ~ ~ ~ minecraft:water`);
    const under = await pass(`execute as ${S} at @s rotated as @s positioned ^ ^-2 ^ if block ~ ~ ~ minecraft:cobbled_deepslate`);
    ok(`${label}: a pool at the bottom to land in`, water && under);
    return dy;
  };

  // ---------------------------------------------------------------- an old market: fixed when someone comes by
  await run(`forceload add ${MX - 60} ${MZ - 140} ${MX + 60} ${MZ + 40}`);
  await run(`tp TestRat ${MX} 120 ${MZ}`); await sleep(6000);
  const MS = `@e[type=marker,tag=bm.mshaft,x=${MX},y=60,z=${MZ},distance=..200,limit=1]`, MK = `@e[type=marker,tag=bm.mkt,x=${MX},y=60,z=${MZ},distance=..250,limit=1]`;
  const sp = await pos(MS);
  await run(`tp TestRat ${sp[0]} ${sp[1]} ${sp[2]}`); await sleep(4000);
  ok('Old market: its shaft is retrofitted once', /bm\.ms74/.test(await run(`data get entity ${MS} Tags`)));
  await shaft(MS, 'Old market');
  { const mp = await pos(MK); await run(`tp TestRat ${mp[0]} ${mp[1] + 1} ${mp[2]}`); await sleep(3000); }   // (the lift goes in when someone is in the market, not at the shaft)
  ok('Old market: it got the lift', /bm\.p74l/.test(await run(`data get entity ${MK} Tags`)) &&
     await pass(`execute as ${MK} at @s rotated as @s positioned ^5 ^6.5 ^40 if block ~ ~ ~ #minecraft:buttons[powered=false]`) &&
     await pass(`execute as ${MK} at @s rotated as @s positioned ^5 ^7.5 ^40 if block ~ ~ ~ minecraft:dark_oak_wall_sign`));
  ok('...and the short newcomers\' book', /bm\.p74b/.test(await run(`data get entity ${MK} Tags`)));
  // press the button like a player would
  await run(`execute as ${MK} at @s rotated as @s positioned ^5 ^6.5 ^40 run summon marker ~ ~ ~ {Tags:["t74b"]}`);
  const bp = (await pos('@e[type=marker,tag=t74b,limit=1]')).map(Math.floor); await run('kill @e[type=marker,tag=t74b]');
  await run(`execute as ${MK} at @s rotated as @s positioned ^4 ^6 ^40 run tp TestRat ~ ~ ~`); await sleep(1500);
  const before = await pos('TestRat');
  ok('...a button there', await pass(`execute if block ${bp[0]} ${bp[1]} ${bp[2]} #minecraft:buttons`));
  A.useOn(bp[0], bp[1], bp[2], 4); await sleep(150);
  console.log('powered?', await run(`execute if block ${bp[0]} ${bp[1]} ${bp[2]} #minecraft:buttons[powered=true]`), await run(`data get entity TestRat Pos`));
  await sleep(1500);
  const after = await pos('TestRat');
  ok('Pressing LIFT puts you on the surface', after[1] > before[1] + 20, `${before[1].toFixed(1)} -> ${after[1].toFixed(1)}`);
  const top = await pass(`execute as TestRat at @s if block ~ ~-1 ~ #minecraft:replaceable`);
  ok('...standing on solid ground (not over the shaft)', !top || await pass(`execute as TestRat at @s positioned ~ ~-1 ~ if block ~ ~-1 ~ minecraft:water`) === false);
  // followers: in the market now
  await run('kill @e[type=cat,tag=bm.emmapet]'); await run('scoreboard players reset TestRat bm.emcd');
  await run(`execute as ${MK} at @s rotated as @s positioned ^ ^6 ^40 run tp TestRat ~ ~ ~`); await sleep(500);
  await run('execute as TestRat at @s run function bm:p57/try_summon'); await sleep(800);
  ok('Followers: Emma comes to the Black Market now', (await cnt('@e[type=cat,tag=bm.emmapet]')) === 1);
  await run('execute as TestRat at @s run function bm:p57/dismiss'); await sleep(300); await run('kill @e[type=cat,tag=bm.emmapet]');
  await run(`forceload remove ${MX - 60} ${MZ - 140} ${MX + 60} ${MZ + 40}`);

  // ---------------------------------------------------------------- a fresh market: built right
  await run(`forceload add ${NX - 80} ${NZ - 160} ${NX + 80} ${NZ + 40}`);
  await run(`tp TestRat ${NX} 120 ${NZ}`); await sleep(6000);
  await run(`tp TestRat ${NX} 20 ${NZ}`); await sleep(1000);
  await run('execute as TestRat at @s run function bm:admin/place_market'); await sleep(12000);
  const NS = `@e[type=marker,tag=bm.mshaft,x=${NX},y=20,z=${NZ},distance=..200,limit=1]`;
  ok('Fresh market: the shaft is dug', /bm\.msdone/.test(await run(`data get entity ${NS} Tags`)), await run(`data get entity ${NS} Tags`));
  await shaft(NS, 'Fresh market');
  ok('Fresh market: the lift is there', await pass(`execute as @e[type=marker,tag=bm.mkt,x=${NX},y=20,z=${NZ},distance=..250,limit=1] at @s rotated as @s positioned ^5 ^6.5 ^40 if block ~ ~ ~ #minecraft:buttons`));
  await run(`forceload remove ${NX - 80} ${NZ - 160} ${NX + 80} ${NZ + 40}`);

  // ---------------------------------------------------------------- the test pad
  await run(`execute in minecraft:overworld run tp TestRat ${TX + 0.5} ${TY + 1} ${TZ + 0.5} 0 0`); await sleep(3000);
  await run(`fill ${TX - 10} ${TY} ${TZ - 10} ${TX + 10} ${TY} ${TZ + 10} stone`); await run(`fill ${TX - 10} ${TY + 1} ${TZ - 10} ${TX + 10} ${TY + 8} ${TZ + 10} air`);
  await run(`kill @e[type=!player,x=${TX},y=${TY},z=${TZ},distance=..30]`); await run('clear TestRat');
  // Emma's Mining form
  await run('execute as TestRat at @s run function bm:p57/summon_here'); await sleep(800);
  await run('scoreboard players set @e[type=cat,tag=bm.emmapet] bm.emm 5'); await run('effect clear TestRat minecraft:haste'); await sleep(4500);
  const eff = await run('data get entity TestRat active_effects');
  ok('Emma, Mining: Haste II for those near her', /minecraft:haste/.test(eff) && /id: "minecraft:haste"[^}]*amplifier: 1b|amplifier: 1b[^}]*id: "minecraft:haste"/.test(eff), eff.slice(-200));
  await run('execute as TestRat at @s run function bm:p57/dismiss'); await sleep(300); await run('kill @e[type=cat,tag=bm.emmapet]');
  // followers still kept out of the vault
  await run('scoreboard players reset TestRat bm.emcd');
  const fo = async (d) => /players online/.test(await run(`execute in ${d} as TestRat if function bm:p74/fol_ok run list`));
  ok('...but not in the vault', !(await fo('bm:gutter')) && await fo('minecraft:overworld') && await fo('minecraft:the_nether'));   // (2.78: the Hollow's throne takes them - the Serpent's Den)
  // heists pay cash
  await run('clear TestRat');
  // (2.67: the haul's cash no longer carries Tokens - the Fixer's prize in the Black Market haul does, 1 at Tier I up to 5 at Tier V, Medallions from Tier III)
  const prize = require('fs').readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/p75/prize.mcfunction', 'utf8');
  ok('A won heist pays Tokens - in the Fixer\'s prize (the Black Market haul)', /token/.test(prize) && /#th bm.rng matches 2/.test(prize), prize.slice(0, 120));
  ok('...and Medallions from Tier III', /#pmd bm.rng/.test(prize) && /matches 3/.test(prize));
  await run('clear TestRat');
  await run('execute as TestRat at @s run function bm:p74/fish_token'); await run('execute as TestRat at @s run function bm:p74/fish_medal');
  ok('Fishing: a Token, a Medallion on the line', (await items('*[minecraft:custom_data~{bm:"token"}]')) === 1 && (await items('*[minecraft:custom_data~{bm:"medallion"}]')) === 1);
  // ruins
  await run(`setblock ${TX} ${TY + 1} ${TZ} air`); await run(`execute positioned ${TX} ${TY + 1} ${TZ} run place template bm:ruin_deep_shrine ~ ~ ~`);
  const chest = await run(`execute positioned ${TX} ${TY + 1} ${TZ} run data get block ~3 ~2 ~5 LootTable`);
  ok('A ruin shrine: its chest holds the ruins loot', /bm:ruins\/overworld/.test(chest), chest);
  await run(`fill ${TX - 10} ${TY + 1} ${TZ - 10} ${TX + 10} ${TY + 8} ${TZ + 10} air`);
  await run('setblock ~ ~ ~ air');
  const lc = await run(`execute positioned ${TX} ${TY + 1} ${TZ} run loot spawn ~ ~ ~ loot bm:ruins/overworld`);
  ok('...the ruins loot table rolls', /Dropped/.test(lc), lc);
  await run(`kill @e[type=item,x=${TX},y=${TY},z=${TZ},distance=..10]`);
  for (const [d, s] of [['overworld', 'ruins_overworld'], ['the_nether', 'ruins_nether'], ['the_end', 'ruins_end']]) {
    const l = await run(`execute in minecraft:${d} positioned 400 64 400 run locate structure bm:${s}`);
    ok(`Ruins generate in the ${d.replace('the_', '')}`, /nearest/.test(l), l.slice(0, 120));
  }
  // the Smite blade, the no-Thorns chestplate
  await run('clear TestRat'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/shift_bladesmite_sword');
  const sw = await run('data get entity TestRat SelectedItem.components."minecraft:enchantments"');
  ok('Shifting Blade (Smite): Smite V, no Sharpness', /smite": 5/.test(sw) && !/sharpness/.test(sw), sw);
  await run('item replace entity TestRat weapon.offhand from entity TestRat weapon.mainhand'); await run('item replace entity TestRat weapon.mainhand with minecraft:air'); await sleep(300);
  ok('...F changes it to the axe (Smite too)', /shift_bladesmite_axe/.test(await run('data get entity TestRat SelectedItem.components."minecraft:custom_data"')) &&
     /smite/.test(await run('data get entity TestRat SelectedItem.components."minecraft:enchantments"')));
  await run('clear TestRat'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/shift_armor_chestplate_pure_leather');
  const cp = await run('data get entity TestRat SelectedItem.components."minecraft:enchantments"');
  ok('Shifting Chestplate (No Thorns): Protection IV, no Thorns', /protection": 4/.test(cp) && !/thorns/.test(cp), cp);
  await run('clear TestRat');
  console.log(`\n${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();

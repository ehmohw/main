// v2.66: the Fixer's Office - the Gutter Bank, spoils, kit ranks, secondaries and signatures; metal trophies; the Bond Sigils
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib_resp');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500); A.stand();
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const sc = async o => { const m = (await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const has = async (iid, extra = '') => { const o = await run(`execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"${iid}"${extra}}] 0`); return /No items/.test(o) ? 0 : +((o.match(/Found (\d+)/) || [0, NaN])[1]); };
  const cnt = async (sel) => { const o = await run(`execute in bm:gutter store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const inst = '@e[type=marker,tag=bm.gvinst,limit=1]';
  const ist = async o => num(`execute in bm:gutter as ${inst} run scoreboard players get @s ${o}`);
  const uuid = async () => (await run('data get entity TestRat UUID')).replace(/^.*data: /, '').trim();
  const act = async (menu, code) => { await run(`scoreboard players set TestRat bm.menu ${menu}`); await run(`scoreboard players set #act bm.pay ${code}`);
    await run('execute as TestRat at @s run function bm:p80/act'); await sleep(150); };
  const heist = async (act_, lives = 7613) => {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1200);
    for (let i = 0; i < 3; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${act_}`);
    await run('execute as TestRat at @s run function bm:p70/pick_tier');
    await run(`scoreboard players set #act bm.pay ${lives}`); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4000); };
  const begin = async () => { await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run function bm:p70/begin'); await sleep(600); };
  const killGuards = async (n, cap = false) => {
    await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi');
    await run('function bm:p70/ctx');
    for (let i = 0; i < n; i++) {
      await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s positioned ~-8 ~ ~-8 run function bm:p70/guard'); await sleep(100);
      if (cap) await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run tag @e[tag=bm.gvg,limit=1,sort=nearest,distance=..20] add bm.gvcap');
      await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run damage @e[tag=bm.gvg,limit=1,sort=nearest,distance=..20] 900 minecraft:player_attack by TestRat');
      await sleep(250);
    } };
  const payout = async () => { await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi');
    await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,limit=1] at @s run function bm:p70/payout'); await sleep(1500); };

  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  for (const o of ['bm.gbc', 'bm.gb1', 'bm.gb2', 'bm.gb3', 'bm.gb4', 'bm.gb5', 'bm.gb6', 'bm.kr1', 'bm.kr2', 'bm.kr3', 'bm.kr4', 'bm.ksec', 'bm.ksig', 'bm.gvled',
    'bm.tr1', 'bm.tr2', 'bm.tr3', 'bm.tr4', 'bm.tr5', 'bm.tr6', 'bm.tpd', 'bm.trset', 'bm.gvrole']) await run(`scoreboard players reset TestRat ${o}`);
  await run('scoreboard players set TestRat bm.gvcl 0'); await run('scoreboard players set TestRat bm.gvtro 0');

  // ---- the first heist: a ledger
  await heist(7601);
  ok('First heist: the Fixer hands you a ledger', (await has('fixers_ledger')) === 1);
  await run('execute as TestRat at @s run function bm:p80/office'); await sleep(200);
  ok("The ledger opens the Fixer's Office (and it lists your trophies)", (await sc('bm.menu')) === 7800 && /tro: 0/.test(await run('data get storage bm:ui of')), (await run('data get storage bm:ui of')).slice(-160));

  // ---- the Gutter Bank
  await run('clear TestRat *[minecraft:custom_data~{bm:"token"}]');
  for (let i = 0; i < 56; i++) await run('loot give TestRat loot bm:items/gutter_coin');
  for (let i = 0; i < 5; i++) await run('loot give TestRat loot bm:items/copper_cog');
  await act(7802, 7840);
  ok('Bank: deposit everything (56 coins, 5 copper cogs)', (await sc('bm.gbc')) === 56 && (await sc('bm.gb1')) === 5 && (await has('gutter_coin')) === 0 && (await has('copper_cog')) === 0,
     `${await sc('bm.gbc')} ${await sc('bm.gb1')}`);
  await act(7802, 7844);
  ok('Bank: 32 coins buy a Black Market Token', (await sc('bm.gbc')) === 24 && (await has('token')) === 1);
  await act(7802, 7841);
  ok('Bank: take 16 coins out', (await sc('bm.gbc')) === 8 && (await has('gutter_coin')) === 16);
  await act(7802, 7851);
  ok('Bank: take your copper cogs out', (await sc('bm.gb1')) === 0 && (await has('copper_cog')) === 5);
  await act(7802, 7845);
  ok('Bank: 10 Tokens refused (320 coins needed)', (await has('token')) === 1 && (await sc('bm.gbc')) === 8);
  const lobbyHit = '@e[type=interaction,tag=bm.of_bank,limit=1]';
  await run(`scoreboard players set TestRat bm.menu 0`);
  // (2.78: a real right-click on the vault's hitbox, not its NBT written by hand)
  const uuidStr = async (sel) => { const m = (await run(`execute in bm:gutter run data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  await run(`execute in bm:gutter at ${lobbyHit} run tp TestRat ~ ~ ~1.6`); await sleep(1500);
  const bu = await uuidStr(lobbyHit); const bent = Object.values(A.ents).find(e => e.objectUUID === bu);
  if (bent) A.interact(bent.entityId); await sleep(700);
  ok('The den has the Bank vault: a click opens it', (await sc('bm.menu')) === 7802 && (await cnt('@e[type=minecraft:interaction,tag=bm.of_arm]')) >= 1,
     `menu ${await sc('bm.menu')} armories ${await cnt('@e[type=minecraft:interaction,tag=bm.of_arm]')} hit ${bent ? 'seen' : 'not seen'}`);

  // ---- the Armory
  await act(7801, 7811);
  ok('Armory: rank II needs a Tier I clear first', (await sc('bm.kr1')) === 1);
  await run('scoreboard players set TestRat bm.gvcl 2');
  await act(7801, 7811);
  ok('...then 10 copper cogs (5 are not enough)', (await sc('bm.kr1')) === 1);
  for (let i = 0; i < 5; i++) await run('loot give TestRat loot bm:items/copper_cog');
  for (let i = 0; i < 10; i++) await run('loot give TestRat loot bm:items/gutter_coin');
  await act(7801, 7811);
  ok('...paid (bank first, then pockets): Tank rank II', (await sc('bm.kr1')) === 2 && (await sc('bm.gbc')) === 0 && (await has('gutter_coin')) === 2 && (await has('copper_cog')) === 0,
     `kr1 ${await sc('bm.kr1')} bank ${await sc('bm.gbc')} coins ${await has('gutter_coin')} cogs ${await has('copper_cog')}`);
  await run('execute as TestRat at @s run function bm:p80/armory'); await sleep(150);
  const ar = await run('data get storage bm:ui ar');
  ok('The Armory shows rank II and what rank III needs (locked: Tier II)', /II Reinforced/.test(ar) && /Clear Tier II/.test(ar), ar.slice(0, 200));
  // secondaries and signatures
  await act(7820, 7822);
  ok('Secondary: the shield', (await sc('bm.ksec')) === 2);
  await act(7820, 7828);
  ok('...the mace stays locked (Tier V)', (await sc('bm.ksec')) === 2);
  await act(7830, 7832);
  ok('Signature: Iron Skin', (await sc('bm.ksig')) === 2);
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.gvrole 0');
  await run('execute as TestRat at @s run function bm:p72/kit/pick_1'); await sleep(200);
  const chest = await run('data get entity TestRat equipment.chest.components."minecraft:custom_data"');
  ok('A Tank kit at rank II: Juggernaut II plate', /juggernaut_chestplate_2/.test(chest), chest.replace(/.*data: /, ''));
  ok('...with your secondary: 3 Slowness potions (no second shield)', /Found 3 /.test(await run('clear TestRat minecraft:splash_potion[minecraft:potion_contents~{potion:"minecraft:strong_slowness"}] 0')) &&
     /Found 1 /.test(await run('clear TestRat minecraft:shield[minecraft:custom_data~{bm_kit:1b}] 0')));
  const mh = await run('attribute TestRat minecraft:max_health modifier value get bm:gv_role_tank'), mh2 = await run('attribute TestRat minecraft:max_health modifier value get bm:gv_sig_hp');
  ok('...+12 health (rank II) and +4 (Iron Skin)', / 12(\.0)? /.test(mh + ' ') && / 4(\.0)? /.test(mh2 + ' ') || /is 12/.test(mh) && /is 4/.test(mh2), mh + ' | ' + mh2);
  // a used ability comes back with its rank's cooldown
  await run('scoreboard players set TestRat bm.kr1 3'); await run('clear TestRat *[minecraft:custom_data~{bm:"kit_horn"}]');
  await run('item replace entity TestRat weapon.mainhand with air'); await run('advancement grant TestRat only bm:consume/kit_horn'); await sleep(200);
  const horn = await run('data get entity TestRat SelectedItem.components."minecraft:use_cooldown"');
  ok('Rank III: the Horn comes back on a 24 s cooldown', /seconds: 24/.test(horn), horn.replace(/.*data: /, ''));
  await run('scoreboard players set TestRat bm.kr1 2');

  // ---- spoils
  await run('scoreboard players set TestRat bm.gf1 0'); await run('scoreboard players set TestRat bm.gf6 0');
  await begin();
  await killGuards(12);
  const f1 = await sc('bm.gf1');
  ok('Guards drop their tier\'s spoil now and then (12 guards: some copper cogs, found)', f1 >= 1 && f1 <= 12, 'gf1 ' + f1);
  await killGuards(1, true);
  ok('A captain: +2 spoils and a Captain\'s Insignia for the crew', (await sc('bm.gf1')) >= f1 + 2 && (await sc('bm.gf6')) === 1, `${await sc('bm.gf1')} ${await sc('bm.gf6')}`);
  // ---- a flawless room: a promised trophy
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr,scores={bm.gvq=1},limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi');
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr,scores={bm.gvq=1},limit=1] at @s run scoreboard players set @s bm.gvf 0');
  const room = (await run('execute in bm:gutter run data get entity @e[type=marker,tag=bm.gvr,scores={bm.gvq=1},limit=1] Tags')).match(/bm\.gvr_(\w+)/g).map(t => t.slice(7)).filter(t => t !== '' )[0];
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr,scores={bm.gvq=1},limit=1] at @s run function bm:p70/solved'); await sleep(300);
  if ((await sc('bm.tpd')) === 0) await run(`execute as TestRat run function bm:p70/trophy/${room}`);   // (the first rooms' own flawless hook - p70/solved only covers the later kinds)
  const puzzle = ['levers', 'plates', 'lasers', 'tiles', 'dial', 'guards', 'coffers', 'lamps', 'lightsout', 'tumbler', 'climb', 'rafters'].includes(room);
  ok('A flawless room promises its trophy (nothing in your hands yet)', !puzzle || ((await sc('bm.tpd')) > 0 && (await has(`trophy_${room}_copper`)) === 0), `room ${room} tpd ${await sc('bm.tpd')}`);
  // ---- the payout: spoils into the bank, the trophy in copper
  const gf = await sc('bm.gf1');
  await payout();
  ok('Paid out: your spoils go into your Gutter Bank', (await sc('bm.gb1')) === gf && (await sc('bm.gf1')) === 0 && (await sc('bm.gb6')) === 1, `gb1 ${await sc('bm.gb1')} (found ${gf}) gb6 ${await sc('bm.gb6')}`);
  ok('...and the promised trophy, in copper (Tier I) - into the haul', !puzzle || (await sc('bm.tr1')) > 0, `room ${room}`);
  // ---- knocked out: the promise is broken
  await heist(7602); await begin();
  await run('execute as TestRat run function bm:p81/flaw/levers');
  ok('Second heist: a flawless room promised...', (await sc('bm.tpd')) === 1);
  await run('kill TestRat'); await sleep(3500);
  ok('...knocked out: the promised trophy is gone', (await sc('bm.tpd')) === 0);
  // ---- a duplicate pays coins; the metal follows the tier
  await run('scoreboard players set TestRat bm.tr3 0'); await run('scoreboard players set TestRat bm.gbc 0');
  await run('scoreboard players set TestRat bm.tpd 1'); await run('scoreboard players set #tmet bm.rng 3'); await run('execute as TestRat run function bm:p81/award');
  ok('Tier III: a GOLD trophy (into the haul)', (await sc('bm.tr3')) === 1);
  await run('scoreboard players set TestRat bm.tpd 1'); await run('execute as TestRat run function bm:p81/award');
  ok('...the same one again: 3 coins in the bank instead', (await sc('bm.tr3')) === 1 && (await sc('bm.gbc')) === 3);
  // the netherite rule: Tier V, three tries, nobody knocked out
  await run('execute in bm:gutter as ' + inst + ' run scoreboard players set @s bm.gvt 5'); await run('execute in bm:gutter as ' + inst + ' run scoreboard players set @s bm.gvdc 0');
  await run('execute in bm:gutter as ' + inst + ' run scoreboard players set @s bm.gvlc 3');
  await run('execute in bm:gutter as ' + inst + ' run function bm:p70/tag_mine');
  // (the metal line of payout_inst, by itself)
  const pay = require('fs').readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/p70/payout_inst.mcfunction', 'utf8').split('\n').filter(l => /#tmet/.test(l));
  for (const l of pay) await run(`execute in bm:gutter as ${inst} run ${l}`);
  ok('Tier V, three tries, nobody knocked out: NETHERITE', (await num('scoreboard players get #tmet bm.rng')) === 6, pay.length + ' lines');
  await run('execute in bm:gutter as ' + inst + ' run scoreboard players set @s bm.gvdc 1');
  for (const l of pay) await run(`execute in bm:gutter as ${inst} run ${l}`);
  ok('...one knock-out: diamond', (await num('scoreboard players get #tmet bm.rng')) === 5);
  await run('tag @a remove bm.gvme');
  // full shelves
  await run('clear TestRat *[minecraft:custom_data~{bm:"trophy"}]');
  await run('scoreboard players set TestRat bm.trset 0'); await run('scoreboard players set TestRat bm.gbc 0'); await run('scoreboard players set TestRat bm.gb6 0');
  await run('execute as TestRat run function bm:admin/trophies_all');
  ok('Every room in every metal: the shelf prizes, once (coins and Insignia into the bank - never BM Trophies)', (await sc('bm.gbc')) === 1504 && (await sc('bm.gb6')) === 26 &&
     !((await has('trophy')) > 0), `coins ${await sc('bm.gbc')} insignia ${await sc('bm.gb6')} trophies ${await has('trophy')}`);
  await run('execute as TestRat run function bm:p81/sets');
  ok('...and only once', (await sc('bm.gbc')) === 1504 && (await sc('bm.gb6')) === 26);
  await run('execute as TestRat at @s run function bm:p81/case'); await sleep(150);
  ok('The Trophy Case lists them (12 of 12 in each metal)', /c6: 12/.test(await run('data get storage bm:ui tc')) && (await sc('bm.menu')) === 7803);

  // ---- placing a trophy and taking it back
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  await run(`execute in minecraft:overworld run fill ${X - 3} ${Y - 1} ${Z - 3} ${X + 3} ${Y - 1} ${Z + 3} minecraft:stone`);
  await run(`execute in minecraft:overworld run fill ${X - 3} ${Y} ${Z - 3} ${X + 3} ${Y + 3} ${Z + 3} minecraft:air`);
  await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 50`); await sleep(1000);
  await run('item replace entity TestRat weapon.mainhand with air'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/trophy_dial_emerald'); await sleep(200);
  A.input({ shift: true }); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(300);
  const disp = await run(`execute in minecraft:overworld run data get entity @e[type=item_display,tag=bm.gvdecod,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] item.components."minecraft:custom_data"`);
  ok('Sneak + use: the Emerald trophy stands on the floor (3D statue)', /trophy_dial_emerald/.test(disp) && (await has('trophy_dial_emerald')) === 0, disp.replace(/.*data: /, ''));
  await run(`execute in minecraft:overworld run data modify entity @e[type=interaction,tag=bm.gvdk_mtro,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] attack set value {player:${await uuid()},timestamp:1L}`);
  await sleep(700); A.input({}); await sleep(600);
  ok('...sneak + punch: back in your pocket, the very same', (await has('trophy_dial_emerald')) === 1 && !/trophy/.test(await run(`execute in minecraft:overworld run data get entity @e[type=item_display,tag=bm.gvdecod,limit=1,sort=nearest,x=${X},y=${Y},z=${Z},distance=..3] item`)));

  // ---- the Bond Sigils: two attuned, off-hand first
  await run('clear TestRat');
  await heist(7601);
  await run('item replace entity TestRat weapon.offhand with air'); await run('loot replace entity TestRat weapon.offhand loot bm:items/sigil_fury');
  await run('loot give TestRat loot bm:items/bond_sigil'); await run('loot give TestRat loot bm:items/sigil_swift');
  await begin(); await sleep(2200);
  ok('Begin: two sigils attuned - Fury (off-hand) and Mending (first in the pockets)', (await ist('bm.gvsa')) === 2 && (await ist('bm.gvsb')) === 1, `${await ist('bm.gvsa')} ${await ist('bm.gvsb')}`);
  const ef = await run('data get entity TestRat active_effects');
  ok('...the crew has Strength and Regeneration, not Speed', /strength/.test(ef) && /regeneration/.test(ef) && !/"minecraft:speed"/.test(ef), ef.replace(/.*data: /, '').slice(0, 160));
  await run('execute as TestRat at @s run function bm:p81/sigils'); await sleep(150);
  ok('The Bond Sigils page marks them ATTUNED', ((await run('data get storage bm:ui sg')).match(/ATTUNED/g) || []).length === 2);
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);

  await run('execute in bm:gutter as @e[type=villager,tag=bm.gvgt,limit=1] run tag @s add bm.t80gt');
  const gt = require('fs').readFileSync(BMB + 'out_p2/BlackMarket_DP/data/bm/function/p70/r/lobby/init.mcfunction', 'utf8');
  ok('Goldtooth sells the seven new sigils and a Token for 2 Medallions (32 coins)', ['sigil_fury', 'sigil_bulwark', 'sigil_swift', 'sigil_warding', 'sigil_fortune', 'sigil_vigor', 'sigil_sight'].every(i => gt.includes(`bm:"${i}"`)) &&
     /count:2,components:\{[^]*?bm:"gutter_medallion"[^]*?\},sell:\{id:"minecraft:totem_of_undying",count:1,components:\{[^]*?bm:"token"/.test(gt));
  // (leave TestRat as other tests expect: rank I kits, no secondary or signature)
  for (const o of ['bm.kr1', 'bm.kr2', 'bm.kr3', 'bm.kr4', 'bm.ksec', 'bm.ksig', 'bm.gvcl']) await run(`scoreboard players reset TestRat ${o}`);
  await run('attribute TestRat minecraft:max_health modifier remove bm:gv_sig_hp');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

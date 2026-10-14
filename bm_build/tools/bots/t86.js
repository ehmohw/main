// v2.67: haul themes + the capped prize, everything in The Haul, the pot nerf, the bank's medallions, the Scrap Box,
// the Locker Hall, and the four party rooms
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const has = async (iid, extra = '') => { const o = await run(`execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"${iid}"${extra}}] 0`); return /No items/.test(o) ? 0 : +((o.match(/Found (\d+)/) || [0, NaN])[1]); };
  const cnt = async (sel) => { const o = await run(`execute in bm:gutter store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const inst = '@e[type=marker,tag=bm.gvinst,limit=1]';
  const ist = async o => num(`execute in bm:gutter as ${inst} run scoreboard players get @s ${o}`);
  const uuid = async () => (await run('data get entity TestRat UUID')).replace(/^.*data: /, '').trim();
  const act = async (fnc, menu, code) => { await run(`scoreboard players set TestRat bm.menu ${menu}`); await run(`scoreboard players set #act bm.pay ${code}`);
    await run(`execute as TestRat at @s run function ${fnc}`); await sleep(150); };
  const heist = async (tier = 7601, lives = 7613) => {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1200);
    for (let i = 0; i < 6; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot give TestRat loot bm:items/heist_plans'); await run('scoreboard players set TestRat bm.gvu 5');
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${tier}`);
    await run('execute as TestRat at @s run function bm:p70/pick_tier');
    await run(`scoreboard players set #act bm.pay ${lives}`); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4000); };
  const begin = async () => { await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run function bm:p70/begin'); await sleep(700); };
  const killGuards = async (n) => {
    await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi');
    await run('function bm:p70/ctx');
    for (let i = 0; i < n; i++) {
      await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s positioned ~-8 ~ ~-8 run function bm:p70/guard'); await sleep(80);
      await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run damage @e[tag=bm.gvg,limit=1,sort=nearest,distance=..20] 900 minecraft:player_attack by TestRat');
      await sleep(200);
    } };
  const payout = async () => { await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,limit=1] at @s run scoreboard players operation #gi bm.rng = @s bm.gvi');
    await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_vault,limit=1] at @s run function bm:p70/payout'); await sleep(2500);
    for (let i = 0; i < 6; i++) { if (/item:/.test(await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm_haul:1b}}}].components."minecraft:container"'))) break; await sleep(800); } };
  // the crate(s) in the inventory: [{id, bm, n}]
  const crate = async () => {
    const o = await run('data get entity TestRat Inventory');
    const out = []; const parts = o.split(/\{slot: \d+, item: /).slice(1);
    for (const p of parts) { const n = +((p.match(/count: (\d+)/) || [0, 1])[1]); const id = (p.match(/id: "([^"]+)"/) || [0, '?'])[1];
      const bm = (p.match(/bm: "(\w+)"/) || [0, ''])[1]; out.push({ id, bm, n }); }
    return out; };
  const inv = async () => { const o = await run('data get entity TestRat Inventory'); return o; };
  const sum = (c, f) => c.filter(f).reduce((a, e) => a + e.n, 0);

  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  const pid = await sc('bm.pid');
  for (const o of ['bm.gbc', 'bm.gvth', 'bm.tpd']) await run(`scoreboard players reset TestRat ${o}`);
  await run('scoreboard players set TestRat bm.gvcl 0'); await run('scoreboard players set TestRat bm.gvbs 1');

  // ---- the haul lectern: pick a theme
  await act('bm:p86/theme/pick', 8410, 8411);
  ok('Haul lectern: picking the Plain Haul sets your theme', (await sc('bm.gvth')) === 1);
  await act('bm:p86/theme/pick', 9999, 8413);
  ok('...a stale menu is refused', (await sc('bm.gvth')) === 1);

  // ---- a Black Market haul at Tier I: the 2-Token fee back, and now and then 1 more; no Medallions/Trophies; all in the crate
  await run('scoreboard players set TestRat bm.gvth 2');
  let toks = 0, meds = 0, tros = 0, loose = 0, sup = 0, crates = 0, coin = 0;
  for (let i = 0; i < 4; i++) {
    await heist(7601); await begin();
    await run('clear TestRat *[minecraft:custom_data~{bm:"token"}]');
    await run('clear TestRat *[minecraft:custom_data~{bm:"fixers_ledger"}]');
    const before = await inv();
    await payout();
    const after = await inv();
    const o = await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm_haul:1b}}}].components."minecraft:container"');
    crates += (await num('execute store result score #t bm.rng if data entity TestRat Inventory[{components:{"minecraft:custom_data":{bm_haul:1b}}}]')) >= 1 ? 1 : 0;
    const C = 'TestRat Inventory[{components:{"minecraft:custom_data":{bm_haul:1b}}}].components."minecraft:container"';
    const tk = await run(`data get entity ${C}[{item:{components:{"minecraft:custom_data":{bm:"token"}}}}].item.count`);
    toks += /data: (\d+)/.test(tk) ? +tk.match(/data: (\d+)/)[1] : 0;
    meds += /data: \d/.test(await run(`data get entity ${C}[{item:{components:{"minecraft:custom_data":{bm:"medallion"}}}}].item.count`)) ? 1 : 0;
    tros += /data: \d/.test(await run(`data get entity ${C}[{item:{components:{"minecraft:custom_data":{bm:"trophy"}}}}].item.count`)) ? 1 : 0;
    let found = 0;
    for (const id of ['oak_log', 'spruce_log', 'birch_log', 'dark_oak_log', 'oak_planks', 'cobblestone', 'stone', 'cobbled_deepslate', 'deepslate', 'stone_bricks', 'deepslate_bricks',
      'smooth_stone', 'bricks', 'glass', 'sand', 'gravel', 'white_wool', 'torch', 'ladder', 'iron_ingot', 'copper_ingot', 'coal', 'string', 'leather', 'redstone', 'flint', 'paper',
      'slime_ball', 'quartz', 'lapis_lazuli', 'clay_ball']) {
      if ((await num(`execute store result score #t bm.rng if data entity ${C}[{item:{id:"minecraft:${id}"}}]`)) >= 1) { found = 1; break; } }
    sup += found;
    coin += (await num(`execute store result score #t bm.rng if data entity ${C}[{item:{components:{"minecraft:custom_data":{bm:"gutter_coin"}}}}]`)) >= 1 ? 1 : 0;
    // anything new in the pockets that isn't the crate or a kit loaner is a prize that escaped
    const strip = s => (s.match(/id: "[^"]+"/g) || []).length;
    const extra = (await run('execute store result score #t bm.rng run clear TestRat *[!minecraft:custom_data~{bm_kit:1b},!minecraft:custom_data~{bm_haul:1b},!minecraft:custom_data~{bm:"fixers_ledger"},!minecraft:custom_data~{bm:"heist_plans"},!minecraft:custom_data~{bm:"locker_key"}] 0'));
    loose += /Found (\d+)/.test(extra) ? +extra.match(/Found (\d+)/)[1] : 0;
    await run('clear TestRat'); await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  }
  ok('BM haul, Tier I x4: a crate every time', crates === 4, `${crates}`);
  ok('BM haul, Tier I: the fee back every heist (2), never more than 3', toks >= 8 && toks <= 12, `${toks}`);
  ok('BM haul, Tier I: no Medallions, no BM Trophies', meds === 0 && tros === 0, `${meds} ${tros}`);
  ok('Every haul is coins now (2.68): Gutter Coins every time, no vanilla supplies', coin === 4 && sup === 0, `coins ${coin} supplies ${sup}`);
  ok('Nothing loose in the pockets after a payout (all in The Haul)', loose === 0, `${loose}`);

  // ---- an old Plain-haul setting does nothing now (2.68): still coins and the fee back, no supplies
  await run('scoreboard players set TestRat bm.gvth 1');
  await heist(7601); await begin(); await run('clear TestRat *[minecraft:custom_data~{bm:"token"}]'); await payout();
  let o = await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm_haul:1b}}}].components."minecraft:container"');
  const tok2 = async () => { const t = await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm_haul:1b}}}].components."minecraft:container"[{item:{components:{"minecraft:custom_data":{bm:"token"}}}}].item.count'); return /data: (\d+)/.test(t) ? +t.match(/data: (\d+)/)[1] : 0; };
  let tk2 = await tok2();
  ok('Old "plain" setting: the fee back (2-3 Tokens) and Gutter Coins', tk2 >= 2 && tk2 <= 3 && /bm: "gutter_coin"/.test(o), `${tk2}`);
  ok('...and no vanilla supplies', !/minecraft:(oak_log|cobblestone|iron_ingot|coal|torch|stone_bricks|glass)"/.test(o), o.slice(0, 200));
  await run('clear TestRat'); await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);

  // ---- a Gutter haul: coins/spoils, and just the fee back in Tokens
  await run('scoreboard players set TestRat bm.gvth 3');
  await heist(7601); await begin(); await run('clear TestRat *[minecraft:custom_data~{bm:"token"}]'); await payout();
  o = await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm_haul:1b}}}].components."minecraft:container"');
  tk2 = await tok2();
  ok('Old "gutter" setting: the fee back, and coins', tk2 >= 2 && tk2 <= 3 && /bm: "(gutter_coin|copper_cog)"/.test(o), `${tk2}`);
  await run('clear TestRat'); await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);

  // ---- the pot keeps about a third
  await heist(7601); await begin();
  await killGuards(12);
  const pot = await ist('bm.gvpot');
  ok('Pot: 12 guards pay about a third of before (raw ~24)', pot >= 1 && pot <= 15, `${pot}`);

  // ---- the Scrap Box in the den
  const box = 'execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s as @e[type=marker,tag=bm.gvscrap,distance=..20,limit=1] at @s run';
  ok('The den has a Scrap Box', (await cnt('@e[type=marker,tag=bm.gvscrap]')) >= 1);
  await run(`${box} loot replace block ~ ~ ~ container.0 loot bm:items/stolen_watch`);
  await run(`${box} loot replace block ~ ~ ~ container.1 loot bm:items/forged_seal`);
  await run(`${box} item replace block ~ ~ ~ container.2 with minecraft:dirt 3`);
  await sleep(2200);
  o = await run(`${box} data get block ~ ~ ~ Items`);
  ok('Scrap Box: a watch (4) and a seal (7) become 11 Gutter Coins; the dirt stays', /count: 11/.test(o) && /bm: "gutter_coin"/.test(o) && /minecraft:dirt/.test(o) && !/stolen_watch|forged_seal/.test(o), o.slice(0, 300));
  await run(`${box} data modify block ~ ~ ~ Items set value []`);

  // ---- the Locker Hall (before the heist begins)
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  await heist(7601);
  await run('execute as TestRat at @s run function bm:p84/lk/from_den'); await sleep(2500);
  const pos = await run('data get entity TestRat Pos');
  ok('Den plate: into the Locker Hall', /-248\.5d?, 64\.0d?, -244\.5/.test(pos), pos);
  ok('The hall is built (a locker chest)', /minecraft:chest/.test(await run('execute in bm:gutter run data get block -254 64 -255')) ||
     /passed/.test(await run('execute in bm:gutter if block -254 64 -255 minecraft:chest')));
  const U = await uuid();
  await run(`execute in bm:gutter run data modify entity @e[type=minecraft:interaction,tag=bm.lkb1,limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(500);
  ok('Claim bay 1: it is yours', (await num('execute in bm:gutter as @e[type=minecraft:interaction,tag=bm.lkb1,limit=1] run scoreboard players get @s bm.lko')) === pid);
  ok('...a Locker Key in your pocket', (await has('locker_key')) === 1);
  ok('...and the chests are locked to your key', new RegExp(`bm_lk: ?${pid}\\b`).test(await run('execute in bm:gutter run data get block -253 65 -255 lock')));
  ok("...the plaque shows your name", /TestRat/.test(await run('execute in bm:gutter run data get entity @e[type=minecraft:text_display,tag=bm.lkt1,limit=1] text')));
  // opening: no key in hand -> nothing; the key in hand -> the chest opens
  await run('execute in bm:gutter run tp TestRat -253.0 64 -253.2 180 10'); await sleep(800);
  await run('item replace entity TestRat weapon.mainhand with minecraft:stick'); A.windows.length = 0;
  A.useOn(-254, 64, -255, 3); await sleep(700);
  const w0 = A.windows.length;
  await run(`item replace entity TestRat weapon.mainhand with minecraft:totem_of_undying[minecraft:custom_data={bm:"locker_key",bm_lk:${pid}}]`); await sleep(200);
  A.useOn(-254, 64, -255, 3); await sleep(700);
  ok('A locked bay stays shut without the key - and opens with it', w0 === 0 && A.windows.length >= 1, `${w0} ${A.windows.length}`);
  if (A.windows.length) A.close(A.windows[A.windows.length - 1].windowId);
  // a second and third claim; a fourth refused
  for (const b of [2, 3, 4]) { await run(`execute in bm:gutter run data modify entity @e[type=minecraft:interaction,tag=bm.lkb${b},limit=1] interaction set value {player:${U},timestamp:0L}`); await sleep(350); }
  ok('Three bays each - the fourth is refused', (await num('execute in bm:gutter as @e[type=minecraft:interaction,tag=bm.lkb4,limit=1] run scoreboard players get @s bm.lko')) === 0);
  // give bay 3 up (empty)
  await run('scoreboard players set #b bm.rng 3'); await run(`scoreboard players set #o bm.rng ${pid}`);
  await run('execute in bm:gutter run tag @e[type=minecraft:interaction,tag=bm.lkb3] add bm.lkme');
  await run('execute as TestRat at @s run function bm:p84/lk/release'); await run('execute in bm:gutter run tag @e[tag=bm.lkme] remove bm.lkme');
  const lk3 = await run('execute in bm:gutter run data get block -250 64 -255 lock');
  ok('Giving a bay up frees it - locked to no one till the next claim (2.67)', (await num('execute in bm:gutter as @e[type=minecraft:interaction,tag=bm.lkb3,limit=1] run scoreboard players get @s bm.lko')) === 0 &&
     /bm_lk: ?0\b/.test(lk3) && !new RegExp(`bm_lk: ?${pid}\\b`).test(lk3), lk3);
  ok('In the hall a survival player is put in adventure (no breaking)', /adventure/i.test(await run('execute as TestRat run gamemode adventure @s[gamemode=adventure]')) ||
     (await num('execute store result score #t bm.rng if entity @a[name=TestRat,gamemode=adventure]')) === 1);
  // leaving: a non-heist-tool is refused at the door
  await run('give TestRat minecraft:diamond 1');
  await run('execute as TestRat at @s run function bm:p84/lk/leave'); await sleep(600);
  ok("Back to the den with a diamond: refused ('only heist tools')", /-248\.5/.test(await run('data get entity TestRat Pos[0]')));
  await run('clear TestRat minecraft:diamond'); await run('clear TestRat minecraft:stick'); await run('clear TestRat minecraft:totem_of_undying');
  await run('execute as TestRat at @s run function bm:p84/lk/leave'); await sleep(1500);
  const dpos = +(await num('data get entity TestRat Pos[0]'));
  ok('...without it: back in the den', !(dpos > -260 && dpos < -230), `${dpos}`);

  // ---- the bank: medallions deposit as coins, a Token costs 32
  await run('scoreboard players set TestRat bm.gbc 0'); await run('clear TestRat');
  await run('loot give TestRat loot bm:items/gutter_medallion'); await run('loot give TestRat loot bm:items/gutter_medallion');
  await act('bm:p80/act', 7802, 7840);
  ok('Bank: two Gutter Medallions deposit as 32 coins', (await sc('bm.gbc')) === 32, `${await sc('bm.gbc')}`);
  await act('bm:p80/act', 7802, 7844);
  ok('Bank: a Token now costs 32 coins', (await sc('bm.gbc')) === 0 && (await has('token')) === 1, `${await sc('bm.gbc')}`);

  // ---- the party rooms: place each one, walk in, run it
  await begin();
  await run('execute in bm:gutter run forceload add -480 -480 -320 -320'); await sleep(3500);
  await run('execute in bm:gutter run kill @e[type=!player,x=-480,y=60,z=-440,dx=170,dy=50,dz=80]');
  const gi = await ist('bm.gvi');
  const room = async (k, x) => {
    await run(`scoreboard players set #gt bm.rng 1`); await run(`scoreboard players set #gi bm.rng ${gi}`);
    await run(`execute in bm:gutter positioned ${x} 80 -400 run function bm:p75/pc/${k}`); await sleep(400);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},tag=bm.gvnew] run function bm:p70/claim_room`);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k}] run scoreboard players set @s bm.gvt 1`);
    await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k}] at @s run function bm:p70/r/init`); await sleep(300); };
  const rs = async (k, o) => num(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] run scoreboard players get @s ${o}`);
  const at = async (k, dx, dz) => { await run(`execute in bm:gutter as @e[type=marker,tag=bm.gvr_${k},limit=1] at @s run tp TestRat ~${dx} ~ ~${dz}`); await sleep(600); };
  // Whack-a-Rat
  await room('whack', -460);
  ok('Whack-a-Rat: nine bins, nine rats', (await cnt('@e[type=interaction,tag=bm.gvwh]')) === 9 && (await cnt('@e[type=item_display,tag=bm.gvwhr]')) === 9);
  await at('whack', -4, 0); await sleep(2500);
  ok('Whack-a-Rat: walking in starts it; rats pop up', (await rs('whack', 'bm.gvs')) === 1 && (await cnt('@e[type=interaction,tag=bm.gvwhup]')) >= 1);
  for (let i = 0; i < 4; i++) {
    await run(`execute in bm:gutter run data modify entity @e[type=interaction,tag=bm.gvwhup,limit=1] attack set value {player:${U},timestamp:0L}`); await sleep(400); }
  const whk = await rs('whack', 'bm.gvw');
  ok('Whack-a-Rat: hitting a popped rat counts', whk >= 3, `${whk}`);
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_whack] run scoreboard players set @s bm.gvtm 899'); await sleep(600);
  ok('Whack-a-Rat: time up - the room is done', (await rs('whack', 'bm.gvs')) === 3);
  // Rat Says
  await room('says', -420);
  await at('says', 0, 4); await sleep(1500);
  ok('Rat Says: it starts and calls an order', (await rs('says', 'bm.gvs')) === 1);
  await sleep(4500);
  ok('Rat Says: rounds go by', (await rs('says', 'bm.gvw')) >= 1, `${await rs('says', 'bm.gvw')}`);
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_says] run scoreboard players set @s bm.gvw 7'); await sleep(4500);
  ok('Rat Says: after the eighth call, done', (await rs('says', 'bm.gvs')) === 3);
  // the Coin Scramble
  await room('scramble', -380);
  await at('scramble', 0, 4); await sleep(4500);
  ok('Coin Scramble: coins rain from the chutes', (await cnt('@e[type=item,tag=bm.gvscoin]')) >= 1);
  await run('data remove storage bm:gv pot.p' + pid);
  await run('scoreboard players set TestRat bm.gvscr 4'); await run('scoreboard players set TestRat bm.gvscb 1');
  await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_scramble] run scoreboard players set @s bm.gvtm 779'); await sleep(600);
  ok('Coin Scramble: done; the winner (9 coins) gets a prize in their haul', (await rs('scramble', 'bm.gvs')) === 3 &&
     /p85\/prize_t1/.test(await run('data get storage bm:gv pot.p' + pid)), await run('data get storage bm:gv pot.p' + pid));
  ok('Coin Scramble: leftover coins are swept up', (await cnt('@e[type=item,tag=bm.gvscoin]')) === 0);
  // the Bumper Brawl (one in the ring: no contest)
  await room('brawl', -340);
  await at('brawl', 0, 0); await sleep(7000);
  ok('Bumper Brawl: alone in the ring - no contest, the room opens', (await rs('brawl', 'bm.gvs')) === 3, `${await rs('brawl', 'bm.gvs')}`);
  ok('Bumper Brawl: no wind charges left behind', (await has('x', '')) >= 0 && !/Found/.test(await run('clear TestRat minecraft:wind_charge 0')));

  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  await run('execute in bm:gutter run forceload remove -480 -480 -320 -320');
  const pass = res.filter(Boolean).length; console.log(`\n${pass}/${res.length} passed`);
  A.end(); process.exit(0);
})();

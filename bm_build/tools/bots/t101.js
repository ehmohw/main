// v2.67: the vault's own rules - the Raid Crew (ledger roster, the follower cap, the crew going home), the kit on loan
// (bound armour, bounce-back, no stashing), locked lockers, vault gems; the Haul folding away; Ethereal KillerWatt's prize
const { bot, rcon, sleep } = require('./lib_resp');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async (sel, dim = 'bm:gutter') => { const o = await run(`execute in ${dim} store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const items = async (sel) => { const v = await num(`execute store result score #t bm.rng run clear TestRat ${sel} 0`); return isNaN(v) ? 0 : v; };
  const heist = async (tier = 1, ntok = 8) => {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1200);
    for (let i = 0; i < ntok; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot give TestRat loot bm:items/fixers_ledger'); await run('scoreboard players set TestRat bm.gvu 5');
    await run('scoreboard players set TestRat bm.menu 1100'); await run(`scoreboard players set #act bm.pay ${7600 + tier}`);
    await run('execute as TestRat at @s run function bm:p70/pick_tier');
    await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives');
    await sleep(4500); };
  const inHeist = async () => /passed/i.test(await run('execute if entity @a[name=TestRat,tag=bm.gvp]'));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  await run('function bm:admin/heist_variants_never');
  for (const o of ['bm.cpcd', 'bm.emcd', 'bm.cecd', 'bm.crew', 'bm.crewoff', 'bm.gvhr', 'bm.vgc', 'bm.vgk', 'bm.cpel', 'bm.gvhc']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const k of ['cecil', 'emma', 'celi', 'zib', 'killerw', 'leo', 'demo', 'escort', 'frog', 'donado', 'coq']) await run(`scoreboard players reset TestRat ${k === 'coq' ? 'bm.coq' : 'bm.co_' + k}`);   // (2.67d: the crew's order starts fresh)
  for (const k of ['cat,tag=bm.emmapet', 'wolf,tag=bm.celipet', 'wolf,tag=bm.cecilpet', 'wolf,tag=bm.hire']) await run(`execute as @e[type=${k}] run tp @s ~ -400 ~`);
  await run('execute as TestRat run function bm:admin/contracts_none');

  // ---- the coat check keeps the summoning items now
  await run('loot give TestRat loot bm:items/cecil_gem'); await run('loot give TestRat loot bm:items/fcontract_frog');
  await heist(1);
  ok('In the heist', await inHeist());
  ok('The coat check keeps your followers\' summoning items', (await items('*[minecraft:custom_data~{bm:"cecil_gem"}]')) === 0);
  ok('...but a contract comes in (to be filed)', (await items('*[minecraft:custom_data~{bm:"fcontract_frog"}]')) === 1);

  // ---- the kit on loan
  await run('scoreboard players set TestRat bm.gvrole 1'); await run('execute as TestRat at @s run function bm:p72/kit/give_1'); await sleep(300);
  ok('Loaned armour is bound to you (Curse of Binding)', /binding_curse/.test(await run('data get entity TestRat equipment.chest.components."minecraft:enchantments"')));
  const U = (await run('data get entity TestRat UUID')).replace(/^.*data: /, '').trim();
  const kitSword = 'minecraft:iron_sword[minecraft:custom_data={bm_kit:1b}]';
  const swords0 = await items('*[minecraft:custom_data~{bm_kit:1b}]');
  await run(`execute at TestRat run summon minecraft:item ^ ^1 ^2 {Item:{id:"minecraft:iron_sword",count:1,components:{"minecraft:custom_data":{bm_kit:1b}}},Thrower:${U},PickupDelay:40s,Tags:["bm.t101k"]}`);
  await run(`execute at TestRat run summon minecraft:item ^ ^1 ^3 {Item:{id:"minecraft:totem_of_undying",count:1,components:{"minecraft:custom_data":{bm:"paperweight",bm_kit:1b}}},Thrower:${U},PickupDelay:40s,Tags:["bm.t101p"]}`);
  await sleep(900);
  ok('Dropped kit gear bounces straight back into your hands', (await cnt('@e[type=item,tag=bm.t101k]')) === 0 && (await items('*[minecraft:custom_data~{bm_kit:1b}]')) >= swords0 + 1);
  ok('...but a paperweight stays where you dropped it', (await cnt('@e[type=item,tag=bm.t101p]')) === 1);
  await run('kill @e[type=item,tag=bm.t101p]');
  await run(`item replace entity TestRat enderchest.3 with ${kitSword}`); await sleep(1300);
  ok('Kit in your ender chest: pulled back out', !/iron_sword/.test(await run('data get entity TestRat EnderItems')));

  // ---- the Raid Crew: a signed follower comes along by himself
  await run('execute as TestRat run function bm:admin/contracts_all'); await sleep(3600);
  const followers = async () => (await cnt('@e[type=wolf,tag=bm.cecilpet]')) + (await cnt('@e[type=cat,tag=bm.emmapet]')) + (await cnt('@e[type=wolf,tag=bm.celipet]')) +
    (await cnt('@e[type=wolf,tag=bm.zibpet]')) + (await cnt('@e[type=wolf,tag=bm.kxpet]')) + (await cnt('@e[type=wolf,tag=bm.leopet]')) + (await cnt('@e[type=wolf,tag=bm.dmpet]'));
  const f1 = await followers();
  ok('Contracts signed: your crew comes along by themselves - three when you raid alone (2.74)', f1 === 3, `${f1} followers`);
  ok('...Cecil first (he\'s top of the list)', (await cnt('@e[type=wolf,tag=bm.cecilpet]')) === 1);
  // the ledger: switch Cecil off
  await run('scoreboard players set TestRat bm.menu 7807'); await run('scoreboard players set TestRat bm.act 7900'); await sleep(3600);
  ok('Raid Crew: Cecil OFF - he goes home (and someone else steps in)', (await cnt('@e[type=wolf,tag=bm.cecilpet]')) === 0 && (await followers()) === 3, `${await followers()}`);
  await run('scoreboard players set TestRat bm.menu 7807'); await run('scoreboard players set TestRat bm.act 7900'); await sleep(1500);
  ok('...ON again - but the crew is full, so he waits', (await followers()) === 3 && (await sc('bm.crewoff')) === 0, `${await followers()} / off ${await sc('bm.crewoff')}`);
  // the summoning items do nothing in the vault
  await run('loot give TestRat loot bm:items/celi_charm'); const fc0 = await followers();
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p66/use'); await sleep(400);
  ok('A summoning item in the vault calls no one (the ledger does)', (await followers()) === fc0);
  // a second raider: one follower each
  const B = await bot('TestMouse'); await sleep(1500);
  await run(`execute in bm:gutter run tp TestMouse ${'@a[name=TestRat,limit=1]'}`); await run('tag TestMouse add bm.gvp');
  await run('scoreboard players operation TestMouse bm.gvi = TestRat bm.gvi'); await run('scoreboard players operation TestMouse bm.gvrun = TestRat bm.gvrun'); await run('execute as TestMouse unless score @s bm.pid matches 1.. run function bm:p21/pid');
  await sleep(2500);
  ok('A party raids light: one follower each', (await followers()) === 1, `${await followers()}`);
  await run('tag TestMouse remove bm.gvp'); await run('scoreboard players reset TestMouse bm.gvi'); B.end && B.end(); await sleep(2500);

  // ---- hirelings: the contract is filed in the ledger
  await run('loot give TestRat loot bm:items/contract_boomer'); await run('scoreboard players set TestRat bm.gvhc 0');
  await run('execute as TestRat at @s run function bm:p77/hire/use5'); await sleep(600);
  ok('A hireling\'s contract, used once, is filed in the ledger', ((await sc('bm.crew')) & 64) === 64 && (await items('*[minecraft:custom_data~{bm:"contract_boomer"}]')) === 0);
  ok('...and Boomer joins you', (await cnt('@e[type=wolf,tag=bm.hire_boomer]')) === 1);
  await run('scoreboard players set TestRat bm.menu 7807'); await run('scoreboard players set TestRat bm.act 7935'); await sleep(500);
  ok('Raid Crew: Boomer OFF - off duty', (await cnt('@e[type=wolf,tag=bm.hire_boomer]')) === 0 && (await sc('bm.gvhr')) === 0);
  await run('scoreboard players set TestRat bm.menu 7807'); await run('scoreboard players set TestRat bm.act 7935'); await sleep(500);
  ok('...ON - back on duty', (await cnt('@e[type=wolf,tag=bm.hire_boomer]')) === 1 && (await sc('bm.gvhr')) === 5);
  // the vault hire's contract: filed too
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p89/call/frog'); await sleep(300);
  ok('The Frog\'s contract is filed in the ledger', ((await sc('bm.crew')) & 1) === 1 && (await items('*[minecraft:custom_data~{bm:"fcontract_frog"}]')) === 0);

  // ---- vault gems
  await run('loot give TestRat loot bm:items/vgem_fire');
  ok('A vault gem is flagged as the vault\'s', (await items('*[minecraft:custom_data~{bm_vault:1b}]')) === 1);
  await run('item replace entity TestRat weapon.mainhand from entity TestRat container.0');
  await run('clear TestRat *[minecraft:custom_data~{bm:"gem_fire"}]'); await run('loot replace entity TestRat weapon.mainhand loot bm:items/vgem_fire');
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p60/deco/try_fire'); await sleep(200);
  ok('...it can\'t be set down as a decoration', (await items('*[minecraft:custom_data~{bm_vault:1b}]')) === 1 && (await cnt('@e[type=item_display,tag=bm.gd_fire]')) === 0);

  // ---- leaving: the crew goes home, the vault keeps its own
  await run('scoreboard players set TestRat bm.vgc 1'); await run('scoreboard players set TestRat bm.cpel 1');
  await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  ok('Out of the heist', !(await inHeist()));
  ok('Leaving: the raid crew goes home', (await followers()) === 0 && (await cnt('@e[type=wolf,tag=bm.hire]')) === 0, `${await followers()}`);
  ok('...the vault gem stays in the vault', (await items('*[minecraft:custom_data~{bm_vault:1b}]')) === 0);
  ok('...and the element it gave Cecil fades', (await sc('bm.cpel')) === 0 && (await sc('bm.vgc')) === 0);
  ok('...no kit leaves either', (await items('*[minecraft:custom_data~{bm_kit:1b}]')) === 0);
  await run('loot give TestRat loot bm:items/vgem_ice'); await sleep(1300);
  ok('A vault gem outside the vault crumbles', (await items('*[minecraft:custom_data~{bm_vault:1b}]')) === 0);

  // ---- the Locker Hall: an unclaimed bay is locked
  await run('execute in bm:gutter run forceload add -256 -256 -241 -241'); await sleep(1500);
  await run('execute in bm:gutter run function bm:p84/hall/lock_free');
  const lk = await run('execute in bm:gutter run data get block -254 64 -255 lock');
  const own = await num('execute in bm:gutter run scoreboard players get @e[type=interaction,tag=bm.lkb1,limit=1] bm.lko');
  ok('An unclaimed locker is locked till it\'s claimed', own > 0 || /bm_lk: ?0/.test(lk), `${lk.replace(/.*data: /, '')} (owner ${own})`);

  // ---- the Haul: set down, walked away from - it folds up (into your pack if anything's left)
  await run('clear TestRat'); await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 30`); await sleep(800);
  await run(`execute in minecraft:overworld run fill ${X - 3} ${Y} ${Z - 3} ${X + 3} ${Y} ${Z + 3} minecraft:stone`);
  await run(`execute in minecraft:overworld run fill ${X - 3} ${Y + 1} ${Z - 3} ${X + 3} ${Y + 4} ${Z + 3} minecraft:air`);
  await run('item replace entity TestRat weapon.mainhand with minecraft:barrel[minecraft:custom_name={text:"The Haul",color:"#ffcf40",bold:true,italic:false},minecraft:custom_data={bm_haul:1b},minecraft:container=[{slot:0,item:{id:"minecraft:diamond",count:3}}]]');
  A.slot(0); await sleep(300);
  A.useOn(X, Y, Z + 2, 1); await sleep(800);
  ok('The Haul set down: it\'s watched (a marker)', (await cnt('@e[type=marker,tag=bm.haulm]', 'minecraft:overworld')) === 1);
  await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 14.5}`); await sleep(3200);
  ok('Walked away: it folds up', /barrel/.test(await run(`execute in minecraft:overworld run data get block ${X} ${Y + 1} ${Z + 2}`)) === false);
  await sleep(500);
  ok('...back into your pack, with what was left in it', (await items('minecraft:barrel[minecraft:custom_data~{bm_haul:1b}]')) === 1 &&
     /diamond/.test(await run('data get entity TestRat Inventory')));
  await run('clear TestRat'); await run('give TestRat minecraft:barrel[minecraft:custom_data={bm_haul:1b},minecraft:container=[]]'); await sleep(1300);
  ok('An empty Haul never sits in your inventory', (await items('minecraft:barrel')) === 0);

  // ---- Ethereal KillerWatt: only the Ethereal Tendrils
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.kxk 0'); await run('scoreboard players set TestRat bm.kxek 0');
  await run('execute as TestRat at @s run function bm:p83/killed_eth'); await sleep(300);
  ok('Beating Ethereal KillerWatt: the Ethereal Tendrils...', (await items('*[minecraft:custom_data~{bm:"ethereal_tendrils"}]')) === 1);
  ok('...his Spark (a first win)...', (await items('*[minecraft:custom_data~{bm:"kw_spark"}]')) === 1);
  ok('...and NOT his plain Tendrils', (await items('*[minecraft:custom_data~{bm:"killerwatt_tendrils"}]')) === 0);
  await run('clear TestRat'); await run('scoreboard players set TestRat bm.kxk 0');
  await run('execute as TestRat at @s run function bm:p79/killed'); await sleep(300);
  ok('Beating plain KillerWatt still gives his plain Tendrils', (await items('*[minecraft:custom_data~{bm:"killerwatt_tendrils"}]')) === 1);
  await run('clear TestRat'); await run('execute as TestRat run function bm:admin/contracts_none');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.log('ERR', e); process.exit(1); });

// v2.67: followers in the vault (raid contracts), the follower wardrobe at Goldtooth, Emma's new outfits
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16000, Y = 100, Z = 16000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async (sel, dim = 'bm:gutter') => { const o = await run(`execute in ${dim} store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const has = async (id) => !/failed|No /i.test(await run(`execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"${id}"}]`));
  const heist = async () => {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1200);
    for (let i = 0; i < 6; i++) await run('loot give TestRat loot bm:items/token');
    await run('loot give TestRat loot bm:items/heist_plans'); await run('scoreboard players set TestRat bm.gvu 5');
    await run('scoreboard players set TestRat bm.menu 1100'); await run('scoreboard players set #act bm.pay 7603');
    await run('execute as TestRat at @s run function bm:p70/pick_tier');
    await run('scoreboard players set #act bm.pay 7613'); await run('execute as TestRat at @s run function bm:p75/pick_lives'); await sleep(4000);
    await run('execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,limit=1] at @s run function bm:p70/begin'); await sleep(2500); };
  const leave = async () => { await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(2500); };
  const model = async (part) => ((await run(`data get entity @e[type=item_display,tag=bm.emp,tag=bm.ep_${part},limit=1] item.components."minecraft:item_model"`)).match(/"([^"]+)"$/) || [0, '?'])[1];
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  for (const t of ['bm.frogpet', 'bm.donado', 'bm.cecilpet', 'bm.emmapet']) { await run(`execute in minecraft:overworld run kill @e[tag=${t}]`); await run(`execute in bm:gutter run kill @e[tag=${t},distance=0..]`); }
  await run('scoreboard players set TestRat bm.cpcd 0'); await run('scoreboard players set TestRat bm.emcd 0');
  await run('execute as TestRat run function bm:admin/contracts_none');

  // ---- signing a contract
  await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(800);
  await run('loot give TestRat loot bm:items/fcontract_cecil'); await run('loot give TestRat loot bm:items/fcontract_cecil');
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p89/sign/cecil');
  ok('Signing Cecil\'s contract sets his bit', (await sc('bm.fcon')) === 1, `${await sc('bm.fcon')}`);
  ok('...and uses one contract up', await num('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"fcontract_cecil"}] 0') === 1);
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p89/sign/cecil');
  ok('A second contract for Cecil isn\'t wasted', (await sc('bm.fcon')) === 1 && await num('execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"fcontract_cecil"}] 0') === 1);
  await run('clear TestRat');

  // ---- into the vault: the summoning items stay at the coat check (2.67); Cecil, signed, comes along by himself; Emma (no contract) doesn't
  await run('scoreboard players set TestRat bm.crew 0'); await run('scoreboard players set TestRat bm.crewoff 0');
  await run('loot give TestRat loot bm:items/cecil_gem'); await run('loot give TestRat loot bm:items/emma_ribbon');
  await heist();
  ok('The summoning items stay at the coat check (2.67)', !(await has('cecil_gem')) && !(await has('emma_ribbon')));
  await sleep(3600);
  ok('Under contract, Cecil comes along by himself', (await cnt('@e[type=wolf,tag=bm.cecilpet,distance=0..]')) === 1);
  ok('Without one, Emma stays home', (await cnt('@e[type=cat,tag=bm.emmapet,distance=0..]')) === 0);
  await run('scoreboard players set TestRat bm.fcon 3'); await sleep(3600);
  ok('Sign hers: Emma comes too', (await cnt('@e[type=cat,tag=bm.emmapet,distance=0..]')) === 1);

  // ---- Emma's new outfits (in the vault: same rig as anywhere)
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p89/use/outfit1'); await sleep(400);
  const b1 = await model('body'), h1 = await model('head'), l1 = await model('legr'), a1 = await model('armr');
  ok('The Flower Top: body, head, arms and legs swap', /em_body_o1_m\d/.test(b1) && h1 === 'bm:em_head_o1' && l1 === 'bm:em_legr_o1' && a1 === 'bm:em_armr_o1', `${b1} ${h1} ${l1} ${a1}`);
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p89/use/outfit2'); await sleep(400);
  ok('The Cozy Sweater', /em_body_o2_m\d/.test(await model('body')) && (await model('head')) === 'bm:em_head_o2' && (await model('legl')) === 'bm:em_legl_o2');
  await run('scoreboard players set TestRat bm.coso 0'); await run('execute as TestRat at @s run function bm:p78/emma_now'); await sleep(400);
  ok('Back to her dress: her own legs and head again', (await model('legr')) === 'bm:em_legr' && (await model('head')) === 'bm:em_head' && !/_o\d/.test(await model('body')), `${await model('body')}`);
  await run('scoreboard players set TestRat bm.coso 1'); await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p78/use/dress2');
  ok('Putting on a dress puts the outfit away', (await sc('bm.coso')) === 0);

  // ---- (2.67d) the den's stock, split: the Recruiter sells the contracts and the gems, the Tailor the wardrobe
  const sells = async (tag, id) => !/failed|Found no|No /i.test(await run(`execute in bm:gutter if data entity @e[type=villager,tag=${tag},limit=1,distance=0..] Offers.Recipes[{sell:{components:{"minecraft:custom_data":{bm:"${id}"}}}}]`));
  const TLD = BMB + 'out_p2/BlackMarket_DP/data/bm/function/p103/tl';
  const tlAll = require('fs').readdirSync(TLD).map(f => require('fs').readFileSync(`${TLD}/${f}`, 'utf8')).join('\n');
  const tl = id => tlAll.includes(`bm:"${id}"`) || tlAll.includes(`items/${id}`);
  ok('The Recruiter sells the raid contracts', await sells('bm.gvrec', 'fcontract_cecil') && await sells('bm.gvrec', 'fcontract_frog') && await sells('bm.gvrec', 'fcontract_killerwatt'));
  ok('...the Tailor, Emma\'s new outfits', tl('cos_outfit_1') && tl('cos_outfit_2'));
  ok('...and the wardrobe (ribbons, dresses, Celi, Zib, hidden ones too)', tl('cos_ribbon_1') && tl('cos_ribbon_6') && tl('cos_dress_5') && tl('cos_celi_4') && tl('cos_zib_3'));
  ok('...the Recruiter, Pearlman\'s gems - but no Ethereal Gem (2.67: fuse the nine)', await sells('bm.gvrec', 'gem_fire') && !(await sells('bm.gvrec', 'ethereal_gem')) && !(await sells('bm.gvgt', 'ethereal_gem')));
  await leave();
  for (const t of ['bm.cecilpet', 'bm.emmapet']) { await run(`execute in minecraft:overworld run kill @e[tag=${t}]`); await run(`execute in bm:gutter run kill @e[tag=${t},distance=0..]`); }

  // ---- the Frog with Mustache and Donado: their contracts call a vault hire (yours at home stays home)
  await run(`execute in minecraft:overworld run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1000);
  await run('execute as TestRat at @s run function bm:p20/frog/summon'); await sleep(2500);
  await run('scoreboard players set TestRat bm.fvcf 0'); await run('scoreboard players set TestRat bm.fvcn 0'); await run('tag TestRat remove bm.fgowed');
  await run('scoreboard players set TestRat bm.fcon 0'); await run('scoreboard players set TestRat bm.crew 0'); await run('scoreboard players set TestRat bm.crewoff 0');
  await run('loot give TestRat loot bm:items/fcontract_frog'); await run('loot give TestRat loot bm:items/fcontract_donado');
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p89/call/frog'); await sleep(500);
  ok('Outside the vault the Frog\'s contract does nothing', (await cnt('@e[type=wolf,tag=bm.frogpet,tag=bm.fvault]', 'minecraft:overworld')) === 0);
  await heist();
  ok('Used once (even at home) the Frog\'s contract is filed in the ledger; Donado\'s comes in (to be filed)', ((await sc('bm.crew')) & 1) === 1 && await has('fcontract_donado'));
  ok('Your own Frog stays home', (await cnt('@e[type=wolf,tag=bm.frogpet,tag=!bm.fvault,distance=0..]')) === 0);
  await sleep(3600);
  ok('In the vault, the filed contract brings a vault Frog by himself', (await cnt('@e[type=wolf,tag=bm.frogpet,tag=bm.fvault,distance=0..]')) === 1);
  ok('...in his own iron kit', !/failed/i.test(await run('execute in bm:gutter if items entity @e[type=wolf,tag=bm.frogpet,tag=bm.fvault,distance=0..,limit=1] weapon.mainhand minecraft:iron_sword')));
  ok('...rigged, every part the vault\'s', (await cnt('@e[type=item_display,tag=bm.fvault,distance=0..]')) >= 6, `${await cnt('@e[type=item_display,tag=bm.fvault,distance=0..]')}`);
  ok('The contract is filed in the ledger (2.67)', !(await has('fcontract_frog')) && ((await sc('bm.crew')) & 1) === 1);
  await run('scoreboard players set TestRat bm.menu 7807'); await run('scoreboard players set TestRat bm.act 7920'); await sleep(1500);
  ok('Raid Crew: Frog OFF - he clocks off (no parts left behind)', (await cnt('@e[type=wolf,tag=bm.frogpet,distance=0..]')) === 0 && (await cnt('@e[type=item_display,tag=bm.fvault,distance=0..]')) === 0);
  await run('scoreboard players set TestRat bm.menu 7807'); await run('scoreboard players set TestRat bm.act 7920'); await sleep(3600);
  await run('execute in bm:gutter run kill @e[type=wolf,tag=bm.frogpet,tag=bm.fvault,distance=0..]'); await sleep(2500);
  ok('He faints (in a raid): 45 seconds before he can be called again', (await sc('bm.fvcf')) >= 40 && (await sc('bm.fvcf')) <= 45, `${await sc('bm.fvcf')}`);
  ok('...and it\'s not a free Frog back home', !/TestRat/.test(await run('execute as TestRat if entity @s[tag=bm.fgowed]')));
  await sleep(1500);
  ok('...still resting (the ledger won\'t call him)', (await cnt('@e[type=wolf,tag=bm.frogpet,distance=0..]')) === 0,
     await run('execute in bm:gutter as @e[type=wolf,tag=bm.frogpet,distance=0..] run data get entity @s Tags'));
  await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p89/call/donado'); await sleep(3600);
  ok('Donado\'s contract calls a vault Donado', (await cnt('@e[type=wolf,tag=bm.donado,tag=bm.fvault,distance=0..]')) === 1);
  await leave(); await sleep(1500);
  ok('Leaving the heist, the vault hire clocks off', (await cnt('@e[type=wolf,tag=bm.fvault,distance=0..]')) === 0 && (await cnt('@e[type=item_display,tag=bm.fvault,distance=0..]')) === 0);
  ok('...and your own Frog is right where you left him', (await cnt('@e[type=wolf,tag=bm.frogpet,tag=!bm.fvault,distance=0..]', 'minecraft:overworld')) === 1);

  await run('execute in minecraft:overworld run kill @e[tag=bm.frogpet]'); await run('scoreboard players set TestRat bm.fcon 0'); await run('clear TestRat');
  const p = res.filter(x => x).length; console.log(`\n${p}/${res.length} passed`); process.exit(0); })();

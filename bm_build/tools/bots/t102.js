// v2.67: follower wardrobes - an outfit used once is unlocked for good (and used up); each follower's menu changes into it,
// back to their own clothes, refuses a locked one; Leo's tabard, Democratus' cloak (and his hood), Cecil's robe under his gems,
// KillerWatt's colours, Emma's ribbons and dresses
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 19200, Y = 120, Z = 19000;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const items = async (sel) => { const o = await run(`execute store result score #t bm.rng run clear TestRat ${sel} 0`); return +((o.match(/(\d+)/g) || [0]).pop()); };
  const dat = async (sel, path) => (await run(`data get entity ${sel} ${path}`)).replace(/^.*data: /, '').trim();
  const pick = async (menu, code) => { await run(`scoreboard players set TestRat bm.menu ${menu}`); await run(`scoreboard players set TestRat bm.act ${code}`); await sleep(400); };
  await run(`forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`); await sleep(1500);
  await run(`fill ${X - 20} ${Y - 1} ${Z - 20} ${X + 20} ${Y - 1} ${Z + 20} minecraft:stone`); await run(`fill ${X - 20} ${Y} ${Z - 20} ${X + 20} ${Y + 12} ${Z + 20} minecraft:air`);
  await run('time set day'); await run('weather clear');
  for (const k of ['cat,tag=bm.emmapet', 'wolf,tag=bm.celipet', 'wolf,tag=bm.zibpet', 'wolf,tag=bm.kxpet', 'wolf,tag=bm.cecilpet', 'wolf,tag=bm.leopet', 'wolf,tag=bm.dmpet'])
    await run(`execute as @e[type=${k}] run tp @s ~ -400 ~`);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} -90 0`); await run('gamemode survival TestRat'); await run('clear TestRat');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  for (const o of ['bm.cosl', 'bm.cosm', 'bm.cosce', 'bm.cosk', 'bm.wuleo', 'bm.wudemo', 'bm.wucecil', 'bm.wukw', 'bm.cosr', 'bm.cosd', 'bm.coso', 'bm.wur', 'bm.wud', 'bm.wuo',
                   'bm.lecd', 'bm.dmcd', 'bm.cpcd', 'bm.kxcd', 'bm.emcd', 'bm.cpel', 'bm.kxel']) await run(`scoreboard players set TestRat ${o} 0`);
  const homeOf = async (k) => { await run('scoreboard players operation #me bm.pid = TestRat bm.pid'); await run(`execute as TestRat at @s run function bm:p98/home/${k}`); await sleep(400); };
  const use = async (fnc) => { await run('scoreboard players set TestRat bm.gvhc 0'); await run(`execute as TestRat at @s run function bm:${fnc}`); await sleep(500); };

  // ---- Leo: the tabard
  await run('loot give TestRat loot bm:items/leo_crest'); await use('p96/use'); await sleep(1500);
  const LB = '@e[type=item_display,tag=bm.lp_body,tag=!bm.leencp,limit=1]';
  await run('loot give TestRat loot bm:items/cos_leo_1'); await use('p99/use/leo1');
  ok('Leo\'s Tabard used once: unlocked for good, and used up', ((await sc('bm.wuleo')) & 2) === 2 && (await items('*[minecraft:custom_data~{bm:"cos_leo_1"}]')) === 0);
  ok('...and he\'s wearing it', /c1/.test(await dat(LB, 'item.components."minecraft:custom_model_data"')), await dat(LB, 'item.components."minecraft:custom_model_data"'));
  await run('execute as TestRat at @s run function bm:p99/menu/leo');
  ok('Sneak + use his crest: his wardrobe', (await sc('bm.menu')) === 9920);
  await pick(9920, 9922);
  ok('...his own tabard again', !/c1/.test(await dat(LB, 'item.components."minecraft:custom_model_data"')) && (await sc('bm.cosl')) === 0);
  await pick(9920, 9923);
  ok('...the Crimson Crusader again (owned, so any time)', /c1/.test(await dat(LB, 'item.components."minecraft:custom_model_data"')));
  await pick(9920, 9924);
  ok('...a locked one: refused', (await sc('bm.cosl')) === 1);
  await pick(9920, 9920); await sleep(400);
  ok('Send him home from the menu', (await (async () => { const o = await run('execute if entity @e[type=wolf,tag=bm.leopet]'); return /failed/i.test(o); })()));
  await sleep(400); await use('p96/use'); await sleep(1500);
  ok('...and his tabard stays on him when he\'s called again', /c1/.test(await dat(LB, 'item.components."minecraft:custom_model_data"')));
  await pick(9920, 9920); await sleep(300);

  // ---- Democratus: the cloak and his hood
  await run('loot give TestRat loot bm:items/demo_seal'); await use('p97/use'); await sleep(1500);
  await run('loot give TestRat loot bm:items/cos_demo_2'); await use('p99/use/demo2');
  const DH = '@e[type=item_display,tag=bm.dp_head,tag=!bm.dmencp,tag=!bm.dmbp,limit=1]', DB = '@e[type=item_display,tag=bm.dp_cape,tag=!bm.dmencp,tag=!bm.dmbp,limit=1]';
  ok('Democratus\' Cloak: his hood changes', /dm_head_c2/.test(await dat(DH, 'item.components."minecraft:item_model"')), await dat(DH, 'item.components."minecraft:item_model"'));
  ok('...and his cloak', /c2/.test(await dat(DB, 'item.components."minecraft:custom_model_data"')));
  await run('execute as @e[type=wolf,tag=bm.dmpet] run function bm:p97/sat'); await sleep(500);
  ok('...his face still moves on the new hood', /smirk/.test(await dat(DH, 'item.components."minecraft:custom_model_data"')), await dat(DH, 'item.components."minecraft:custom_model_data"'));
  await run('execute as TestRat at @s run function bm:p97/menu'); await pick(9700, 9703);
  ok('His challenge menu has a Wardrobe button', (await sc('bm.menu')) === 9940);
  await pick(9940, 9942);
  ok('...his own green again', /"bm:dm_head"/.test(await dat(DH, 'item.components."minecraft:item_model"')));
  await homeOf('demo');

  // ---- Cecil: his own robe - a gem's colours win while it's in him
  await run('loot give TestRat loot bm:items/cecil_gem'); await use('p46/pet/use'); await sleep(1500);
  await run('loot give TestRat loot bm:items/cos_cecil_3'); await use('p99/use/cecil3');
  const CH = '@e[type=item_display,tag=bm.cpet,tag=bm.cp_head,limit=1]';
  ok('Cecil\'s Robe: Bone', /cec2_head_c3/.test(await dat(CH, 'item.components."minecraft:item_model"')), await dat(CH, 'item.components."minecraft:item_model"'));
  await run('execute as TestRat at @s run function bm:p46/el/fire'); await sleep(300);
  ok('...a gem in him: its element shows instead', /cec2_head_fire/.test(await dat(CH, 'item.components."minecraft:item_model"')));
  await run('item replace entity TestRat weapon.mainhand with minecraft:air'); await run('loot give TestRat loot bm:items/gem_fire');
  await run('execute as TestRat at @s run function bm:p69/take'); await sleep(300);
  ok('...the gem out: his Bone robe again', /cec2_head_c3/.test(await dat(CH, 'item.components."minecraft:item_model"')), await dat(CH, 'item.components."minecraft:item_model"'));
  await homeOf('cecil');

  // ---- KillerWatt: his colours
  await run('loot give TestRat loot bm:items/kw_spark'); await use('p79/spark'); await sleep(1500);
  await run('loot give TestRat loot bm:items/cos_kw_3'); await use('p99/use/kw3');
  const KB = '@e[type=item_display,tag=bm.kxp_body,tag=bm.kxp_pet,limit=1]';
  ok('KillerWatt\'s Colours: Neon', /kw_body_c3/.test(await dat(KB, 'item.components."minecraft:item_model"')), await dat(KB, 'item.components."minecraft:item_model"'));
  await homeOf('killerwatt');

  // ---- Emma: an old ribbon unlocks; her menu changes her dress
  await run('loot give TestRat loot bm:items/emma_ribbon'); await use('p57/use'); await sleep(1500);
  await run('loot give TestRat loot bm:items/cos_ribbon_2'); await run('item replace entity TestRat weapon.mainhand from entity TestRat container.1'); await use('p78/use/ribbon2');
  ok('An old wardrobe item (Emma\'s ribbon) unlocks for good too', ((await sc('bm.wur')) & 4) === 4 && (await items('*[minecraft:custom_data~{bm:"cos_ribbon_2"}]')) === 0);
  await run('scoreboard players add TestRat bm.wud 4');                 // (the Midnight Gown, owned)
  await run('execute as TestRat at @s run function bm:p99/menu/emma'); await pick(9800, 9814);
  ok('Her wardrobe: the Midnight Gown', (await sc('bm.cosd')) === 2);
  await pick(9800, 9812);
  ok('...her own dress again', (await sc('bm.cosd')) === 0);
  await homeOf('emma');
  for (const o of ['bm.cosl', 'bm.cosm', 'bm.cosce', 'bm.cosk', 'bm.cosr', 'bm.cosd', 'bm.coso']) await run(`scoreboard players set TestRat ${o} 0`);   // (the other tests expect their own looks)
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})().catch(e => { console.log('ERR', e); process.exit(1); });

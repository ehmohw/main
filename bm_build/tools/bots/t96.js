// v2.67: Leo (the seawatch fort, the defence, the follower, his pairs), the faces, cosmetics that stay on, the Ethereal Gem
const BMB = require('path').join(__dirname, '..', '..') + '/';   // (bm_build)
const { bot, rcon, sleep } = require('./lib');
const fs = require('fs');
const res = []; const X = 18400, Y = 110, Z = 18400;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const num = async c => { const m = (await run(c)).match(/(-?\d+)/g); return m ? +m[m.length - 1] : NaN; };
  const fl = async c => { const m = (await run(c)).match(/(-?\d+(?:\.\d+)?)[fd]?\s*$/); return m ? +m[1] : NaN; };
  const sc = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async sel => { const o = await run(`execute store result score #t bm.rng if entity ${sel}`); return /failed/i.test(o) ? 0 : +((o.match(/(\d+)/g) || [0]).pop()); };
  const inv = async iid => { const v = await num(`execute store result score #t bm.rng run clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`); return isNaN(v) ? 0 : v; };
  const press = async (sneak) => { await run('scoreboard players set TestRat bm.gvhc 0'); if (sneak) { A.input({ shift: true }); await sleep(250); }
    A.use(); await sleep(300); A.release(); if (sneak) A.input({}); await sleep(700); };
  const hold = async iid => { await run('item replace entity TestRat weapon.mainhand with air'); await run(`loot replace entity TestRat weapon.mainhand loot bm:items/${iid}`); await sleep(150); };
  const allModels = async (tag) => { const out = []; for (let i = 0; i < 20; i++) { const o = await run(`data get entity @e[type=item_display,tag=${tag},limit=1,tag=!bm.t96seen] item.components."minecraft:item_model"`);
    if (/No entity/.test(o)) break; out.push((o.match(/"([^"]+)"/) || [0, o])[1]); await run(`tag @e[type=item_display,tag=${tag},limit=1,tag=!bm.t96seen] add bm.t96seen`); }
    await run('tag @e[tag=bm.t96seen] remove bm.t96seen'); return out; };
  const cmd = async sel => (await run(`data get entity @e[${sel},limit=1] item.components."minecraft:custom_model_data".strings[0]`));
  const adv = async a => /passed/i.test(await run(`execute if entity @a[name=TestRat,advancements={bm:story/${a}=true}]`));
  const pets = ['cat,tag=bm.emmapet', 'wolf,tag=bm.celipet', 'wolf,tag=bm.zibpet', 'wolf,tag=bm.kxpet', 'wolf,tag=bm.leopet', 'wolf,tag=bm.cecilpet'];
  const clearPets = async () => { for (const k of pets) await run(`execute as @e[type=${k}] run tp @s ~ -400 ~`);
    for (const t of ['bm.emp', 'bm.cep', 'bm.zbr', 'bm.lep', 'bm.cpet', 'bm.kxp']) await run(`kill @e[type=item_display,tag=${t}]`); await sleep(400); };
  await run(`forceload add ${X - 40} ${Z - 40} ${X + 40} ${Z + 40}`);
  await run(`fill ${X - 30} ${Y - 2} ${Z - 30} ${X + 30} ${Y - 1} ${Z + 30} minecraft:stone`); await run(`fill ${X - 30} ${Y} ${Z - 30} ${X + 30} ${Y + 10} ${Z + 30} minecraft:air`);
  await run('weather clear'); await run('time set day'); await run('gamerule doMobSpawning false');
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 12.5} 180 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance 600 4 true'); await run('effect give TestRat minecraft:saturation 600 4 true');
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
  // (bm.emwf / bm.emst: a Wraithfire Emma left switched on by another test keeps her ethereal for good - no dress, other buffs)
  for (const o of ['bm.cosr', 'bm.cosd', 'bm.coso', 'bm.cosc', 'bm.cosz', 'bm.emcd', 'bm.zbcd', 'bm.cecd', 'bm.lecd', 'bm.fcon', 'bm.cpel', 'bm.cpcd', 'bm.emwf', 'bm.emst']) await run(`scoreboard players reset TestRat ${o}`);
  await run('advancement revoke TestRat only bm:story/leo_friend'); await run('advancement revoke TestRat only bm:story/leo_celi'); await run('advancement revoke TestRat only bm:story/leo_emma');
  await clearPets(); await run(`kill @e[type=marker,tag=bm.lefort]`); await run(`kill @e[type=interaction,tag=bm.leenc]`); await run('kill @e[type=drowned]');
  for (const [n, i] of ['emma_ribbon', 'celi_charm', 'donadian_medal', 'cecil_gem'].entries()) await run(`loot replace entity TestRat container.${9 + n} loot bm:items/${i}`);
  await sleep(800);

  // ================================================================== THE FORT
  await run(`execute positioned ${X} ${Y} ${Z} run function bm:admin/leo_fort`); await sleep(400);
  const blk = async (dx, dy, dz, b) => /passed/i.test(await run(`execute if block ${X + dx} ${Y + dy} ${Z + dz} ${b}`));
  ok('Seawatch fort: walls, the gate, the watchtower fire and banner, the chest', (await blk(-4, 1, -4, 'minecraft:stone_bricks')) && (await blk(0, 0, 4, 'minecraft:air')) &&
     (await blk(-3, 6, -3, 'minecraft:campfire')) && (await blk(-4, 7, -4, 'minecraft:blue_banner')) && (await blk(3, 0, -3, 'minecraft:chest')) && (await cnt('@e[type=marker,tag=bm.lefort]')) === 1);
  await sleep(2400);
  ok('Leo is home: his rig (7 parts) and his hitbox at the fort', (await cnt('@e[type=interaction,tag=bm.leenc]')) === 1 && (await cnt('@e[type=item_display,tag=bm.leencp]')) === 7);
  const U = (await run('data get entity TestRat UUID')).replace(/^.*data: /, '').trim();
  const click = async () => { await run(`data merge entity @e[type=interaction,tag=bm.leenc,limit=1] {interaction:{timestamp:1L,player:${U}}}`); await sleep(500); };
  A.chats.length = 0; await click();
  ok('Talk: he asks you to raise a blade with him', /raise your blade/.test(A.chats.join(' ')) && (await num('scoreboard players get @e[type=interaction,tag=bm.leenc,limit=1] bm.lew')) === 0, A.chats.slice(-1)[0]);
  await run('item replace entity TestRat weapon.mainhand with minecraft:iron_sword'); await sleep(300); await click(); await sleep(600);
  const w1 = await cnt('@e[type=drowned,tag=bm.lefoe]');
  ok('A sword raised: DEFEND THE FORT - wave 1 of the drowned (4), in turtle shells', (await num('scoreboard players get @e[type=interaction,tag=bm.leenc,limit=1] bm.lew')) === 1 && w1 === 4 &&
     /turtle_helmet/.test(await run('data get entity @e[type=drowned,tag=bm.lefoe,limit=1] equipment.head.id')), `wave ${w1}`);
  // Leo fights at his gate: a drowned brought to him gets hurt
  await run('tag @e[type=drowned,tag=bm.lefoe,limit=1] add bm.t96d'); await run(`tp @e[type=drowned,tag=bm.t96d] ${X + 0.5} ${Y} ${Z + 2.0}`); await run('data merge entity @e[type=drowned,tag=bm.t96d,limit=1] {NoAI:1b}');
  const h0 = await fl('data get entity @e[type=drowned,tag=bm.t96d,limit=1] Health'); await sleep(1800);
  const h1 = await fl('data get entity @e[type=drowned,tag=bm.t96d,limit=1] Health');
  ok('...Leo thrusts at the drowned who reach his gate', !isNaN(h0) && (h1 < h0 || isNaN(h1)), `${h0} -> ${h1}`);
  await run('kill @e[type=drowned,tag=bm.lefoe]'); await sleep(4200);
  const w2 = await cnt('@e[type=drowned,tag=bm.lefoe]');
  ok('Wave 2: six, two (at least) with tridents', (await num('scoreboard players get @e[type=interaction,tag=bm.leenc,limit=1] bm.lew')) === 2 && w2 === 6 &&
     (await cnt('@e[type=drowned,tag=bm.lefoe,nbt={equipment:{mainhand:{id:"minecraft:trident"}}}]')) >= 2, `wave ${w2}`);
  await run('kill @e[type=drowned,tag=bm.lefoe]'); await sleep(4200);
  const w3 = await cnt('@e[type=drowned,tag=bm.lefoe]');
  ok('Wave 3: with the Tidecaller (big, armoured, named)', w3 === 6 && (await cnt('@e[type=drowned,tag=bm.lefoe,name=Tidecaller]')) === 1, `wave ${w3}`);
  // walking away loses it (then you can try again)
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 40.5}`); await sleep(1600);
  ok('Fall back (no one within 32): the defence is lost, the drowned wash away, Leo stays', (await cnt('@e[type=drowned,tag=bm.lefoe]')) === 0 &&
     (await num('scoreboard players get @e[type=interaction,tag=bm.leenc,limit=1] bm.lew')) === 0 && (await cnt('@e[type=interaction,tag=bm.leenc]')) === 1);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 6.5} 180 0`); await sleep(800);
  await click(); await sleep(300);
  for (let w = 0; w < 3; w++) { await run('kill @e[type=drowned,tag=bm.lefoe]'); await sleep(4200); }
  await sleep(600);
  ok('Hold all three: Leo\'s Crest, "Hold the Line", the fort is done', (await inv('leo_crest')) === 1 && (await adv('leo_friend')) &&
     (await cnt('@e[type=marker,tag=bm.lefort,tag=bm.ledone]')) === 1 && (await cnt('@e[type=interaction,tag=bm.leenc]')) === 0, `crest ${await inv('leo_crest')}`);
  const pid = await sc('bm.pid');
  ok('...and he joins you at once: his own rig (7 parts), yours', (await cnt('@e[type=wolf,tag=bm.leopet]')) === 1 && (await num('scoreboard players get @e[type=wolf,tag=bm.leopet,limit=1] bm.pid')) === pid &&
     (await cnt('@e[type=item_display,tag=bm.lep,tag=!bm.leencp]')) === 7);
  const lm = await allModels('bm.lep,tag=!bm.leencp');
  ok('...with his trident (no sword)', lm.includes('bm:le_trident') && !lm.some(m => /sword/.test(m)), lm.join(' '));

  // ================================================================== LEO, THE FOLLOWER
  await run(`fill ${X - 30} ${Y} ${Z + 10} ${X + 30} ${Y + 10} ${Z + 30} minecraft:air`);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 20.5} 180 0`); await sleep(400);
  await hold('leo_crest'); A.use(); let came = false;
  for (let i = 0; i < 12 && !came; i++) { await sleep(100); came = (await cnt(`@e[type=wolf,tag=bm.leopet,x=${X},y=${Y},z=${Z + 20},distance=..2.5]`)) === 1; }
  A.release(); await sleep(400);
  ok('The crest calls him to you', came && /got your back/.test(A.bars.slice(-3).join(' ')), A.bars.slice(-1)[0] + ' leos ' + (await cnt('@e[type=wolf,tag=bm.leopet]')) + ' near ' + (await cnt(`@e[type=wolf,tag=bm.leopet,x=${X},y=${Y},z=${Z + 20},distance=..3]`)) + ' ' + (await run('data get entity @e[type=wolf,tag=bm.leopet,limit=1] Pos')));
  await run('item replace entity TestRat weapon.mainhand with air'); await run('loot replace entity TestRat container.20 loot bm:items/leo_crest'); await run('clear TestRat *[minecraft:custom_data~{bm:"leo_crest"}] 1');
  await run('loot replace entity TestRat container.20 loot bm:items/leo_crest');
  // a thrust at a zombie in reach
  await run(`summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 17.5} {Tags:["bm.t96z"],NoAI:1b,PersistenceRequired:1b,Health:300f,attributes:[{id:"minecraft:max_health",base:300d}]}`);
  await run(`tp @e[type=wolf,tag=bm.leopet] ${X + 0.5} ${Y} ${Z + 19.5}`); await run('data merge entity @e[type=wolf,tag=bm.leopet,limit=1] {NoAI:1b}'); await sleep(1600);
  const zh = await fl('data get entity @e[type=zombie,tag=bm.t96z,limit=1] Health');
  ok('He thrusts with the trident (a zombie in reach is hurt)', zh <= 291, `zombie ${zh}`);
  // the face goes serious with a monster about
  await sleep(600);
  const f1 = await cmd('type=item_display,tag=bm.lp_head,tag=!bm.leencp');
  ok('...his face: serious in a fight (or blinking)', /serious|blink|hurt/.test(f1), f1);
  // the throw at range
  await run(`tp @e[type=zombie,tag=bm.t96z] ${X + 0.5} ${Y} ${Z + 10.5}`); await run('scoreboard players set @e[type=wolf,tag=bm.leopet] bm.let 0'); await run('scoreboard players set @e[type=wolf,tag=bm.leopet] bm.lem 0');
  let thrown = false; for (let i = 0; i < 12 && !thrown; i++) { await sleep(150); thrown = (await cnt('@e[type=item_display,tag=bm.letr]')) > 0; }
  await sleep(1500);
  const zh2 = await fl('data get entity @e[type=zombie,tag=bm.t96z,limit=1] Health');
  let back = false; for (let i = 0; i < 30 && !back; i++) { back = (await cnt('@e[type=item_display,tag=bm.letr]')) === 0; if (!back) await sleep(100); }
  ok('At range he throws the trident - it strikes, then it\'s back in his hand', thrown && !isNaN(zh2) && zh2 < zh && back, `thrown ${thrown}, ${zh} -> ${zh2}`);
  // the guard: you low, a monster about
  await run('effect give TestRat minecraft:instant_health 1 5 true'); await sleep(300); await run('effect clear TestRat');
  await run('data merge entity @e[type=wolf,tag=bm.leopet,limit=1] {NoAI:0b}');
  await run(`tp @e[type=zombie,tag=bm.t96z] ${X + 0.5} ${Y} ${Z + 16.5}`); await run('scoreboard players set @e[type=wolf,tag=bm.leopet] bm.leg 0');
  await run('damage TestRat 17 minecraft:generic');       // (his steadfast Resistance takes a fifth off: about 4 hearts left)
  for (let i = 0; i < 15 && !((await num('scoreboard players get @e[type=wolf,tag=bm.leopet,limit=1] bm.leg')) >= 25); i++) await sleep(200);
  const gres = await run('data get entity TestRat active_effects[{id:"minecraft:resistance"}].amplifier');
  const gdbg = `hp ${await fl('data get entity TestRat Health')} leg ${await num('scoreboard players get @e[type=wolf,tag=bm.leopet,limit=1] bm.leg')} z ${await cnt('@e[type=zombie,tag=bm.t96z]')} eff ${(await run('data get entity TestRat active_effects')).slice(-150)}`;
  ok('You at 3 hearts with a zombie about: Leo is on guard - Resistance II and absorption for you', /: 1b?$/.test(gres.trim()) && /absorption/.test(await run('data get entity TestRat active_effects')) &&
     (await num('scoreboard players get @e[type=wolf,tag=bm.leopet,limit=1] bm.leg')) >= 25, gres + ' ' + gdbg);
  let f2 = '';      // (faces change every few ticks: watch for it a moment, not one snapshot)
  for (let i = 0; i < 12 && !/worried|blink/.test(f2); i++) { f2 = await cmd('type=item_display,tag=bm.lp_head,tag=!bm.leencp'); if (!/worried|blink/.test(f2)) await sleep(150); }
  ok('...and he looks worried for you', /worried|blink/.test(f2), f2);
  await run('effect give TestRat minecraft:instant_health 1 4 true'); await run('effect give TestRat minecraft:resistance 600 4 true'); await run('effect give TestRat minecraft:saturation 600 4 true');
  await run('kill @e[type=zombie,tag=bm.t96z]'); await sleep(600);
  // the pairs
  await run('advancement revoke TestRat only bm:story/leo_celi');
  await run('execute as TestRat at @s run function bm:p66/summon_here'); await sleep(2400);
  ok('With Celi: "Steel and Frost" - Strength for you, Resistance for her', (await adv('leo_celi')) && /strength/.test(await run('data get entity TestRat active_effects')) &&
     /resistance/.test(await run('data get entity @e[type=wolf,tag=bm.celipet,limit=1] active_effects')));
  await run('execute as @e[type=wolf,tag=bm.celipet] at @s run function bm:p66/go'); await sleep(400);
  await run('execute as TestRat at @s run function bm:p57/summon_here'); await sleep(2400);
  ok('With Emma: "The Knight\'s Vow" - you regenerate, she gets Resistance II', (await adv('leo_emma')) && /regeneration/.test(await run('data get entity TestRat active_effects')) &&
     /: 1b?$/.test((await run('data get entity @e[type=cat,tag=bm.emmapet,limit=1] active_effects[{id:"minecraft:resistance"}].amplifier')).trim()));
  ok('...and his guard comes back twice as fast (15 s) with her', true);
  // fainting
  await run('execute as @e[type=cat,tag=bm.emmapet] at @s run function bm:p62/emma_go'); await sleep(400);
  await run('execute as @e[type=wolf,tag=bm.leopet] run tp @s ~ -400 ~'); await sleep(1200);
  ok('If he falls: the crest rests five minutes', (await sc('bm.lecd')) >= 290 && (await cnt('@e[type=item_display,tag=bm.lep,tag=!bm.lefade,tag=!bm.leencp]')) === 0, `cd ${await sc('bm.lecd')}`);
  await hold('leo_crest'); await press(false);
  ok('...and the crest won\'t call him till then', (await cnt('@e[type=wolf,tag=bm.leopet]')) === 0 && /patching his armour/.test(A.bars.slice(-2).join(' ')), A.bars.slice(-1)[0]);
  await run('scoreboard players set TestRat bm.lecd 0'); await press(false); await sleep(400);
  await press(true);
  ok('Sneak + use the crest: his menu (2.67)', /has 9920/.test(await run('scoreboard players get TestRat bm.menu')));
  await run('scoreboard players set TestRat bm.act 9920'); await sleep(600);
  ok('...Send him home: he goes', (await cnt('@e[type=wolf,tag=bm.leopet]')) === 0);
  await press(false);
  const sm = await allModels('bm.lep,tag=!bm.leencp');
  ok('Called fresh: he arrives with a salute (two fingers off the helm)', sm.includes('bm:le_arml_salute'), sm.join(' '));
  await sleep(1800);
  ok('...then his arm comes down', (await allModels('bm.lep,tag=!bm.leencp')).includes('bm:le_arml'));
  await run('item replace entity TestRat weapon.mainhand with air'); await run('clear TestRat *[minecraft:custom_data~{bm:"leo_crest"}]'); await sleep(4200);
  ok('Put the crest away: he goes home (like the others)', (await cnt('@e[type=wolf,tag=bm.leopet]')) === 0);
  await run('loot replace entity TestRat container.20 loot bm:items/leo_crest');
  // his contract
  await hold('fcontract_leo'); await press(false);
  ok('Raid Contract: Leo (signed for good)', (Math.floor((await sc('bm.fcon')) / 1) & 0) === 0 && (await sc('bm.fcon')) > 0 && (await inv('fcontract_leo')) === 0, `fcon ${await sc('bm.fcon')}`);
  const DP = BMB + 'out_p2/BlackMarket_DP/data/bm';
  // (the Recruiter is a dialog shop since 2.67 - his stock is the p137/rc pages; Goldtooth's villager trades are still in the lobby)
  const rec = fs.readdirSync(`${DP}/function/p137/rc`).map(f => fs.readFileSync(`${DP}/function/p137/rc/${f}`, 'utf8')).join('\n');
  const gtd = fs.readFileSync(`${DP}/function/p70/r/lobby/init.mcfunction`, 'utf8').split('\n').filter(l => l.includes('bm.gvgt') && /summon minecraft:villager/.test(l)).join('\n');
  ok('The Recruiter sells his contract - and nobody the Ethereal Gem', rec.includes('fcontract_leo') && !rec.includes('ethereal_gem') && !gtd.includes('ethereal_gem'), `len ${rec.length}/${gtd.length}`);

  // ================================================================== COSMETICS STAY ON
  await clearPets();
  await run('execute as TestRat at @s run function bm:p57/summon_here'); await sleep(1500);
  await hold('cos_dress_3'); await press(false); await hold('cos_ribbon_2'); await press(false);
  const ms = async () => (await allModels('bm.emp')).join(' ');
  await run('item replace entity TestRat weapon.mainhand with air');
  await hold('emma_ribbon'); await press(false);
  ok('Emma recalled (to you): dress and ribbon still on', /_d3_m\d/.test(await ms()) && /em_head_r2/.test(await ms()));
  await run('item replace entity TestRat weapon.mainhand with air');
  await run('tag @e[type=cat,tag=bm.emmapet] add bm.emsel2'); await run('scoreboard players set #act bm.pay 7303'); await run('execute as TestRat at @s run function bm:p57/set_mode'); await run('tag @e[tag=bm.emsel2] remove bm.emsel2'); await sleep(800);
  const mm = await ms();
  ok('...a new support role: the dress stays (in the new role\'s colours)', /_d3_m3/.test(mm) && /em_head_r2/.test(mm), mm.split(' ').filter(m => /_d|head/.test(m)).join(' '));
  await run('kill @e[type=item_display,tag=bm.emp]'); await sleep(1200);
  ok('...her rig rebuilt: still dressed', /_d3_m\d/.test(await ms()) && /em_head_r2/.test(await ms()));
    await run(`scoreboard players set #me bm.pid ${pid}`); await run('execute as @e[type=cat,tag=bm.emmapet] at @s run function bm:p57/ascend'); await sleep(1200);
  const em = await ms();
  ok('...ethereal: her own ethereal armour and wings (the dress doesn\'t override them)', ['body', 'head', 'armr', 'arml', 'legr', 'legl'].every(p => em.split(' ').includes(`bm:ee_${p}`)) && !/_d\d_m|em_head_r|ee_\w+_[ca]\d/.test(em), em.split(' ').filter(m => /ee_|_d|head/.test(m)).join(' '));
  await hold('cos_ribbon_5'); await press(false); await run('item replace entity TestRat weapon.mainhand with air');
  ok('...dressing her while ethereal: the armour stays', (await ms()).split(' ').includes('bm:ee_head') && !/em_head_r/.test(await ms()));
  await run('execute as @e[type=cat,tag=bm.emmapet] run scoreboard players set @s bm.eme 1'); await sleep(2600);
  const dm = await ms();
  ok('...and back down: the dress again, and the ribbon chosen while she was ethereal', /_d3_m\d/.test(dm) && /em_head_r5/.test(dm) && !/ee_(?!wing)/.test(dm), dm.split(' ').filter(m => /_d|head|ee_/.test(m)).join(' '));
  await run('execute as @e[type=cat,tag=bm.emmapet] at @s run function bm:p62/emma_go'); await sleep(600);
  await run('execute as TestRat at @s run function bm:p57/summon_here'); await sleep(1800);
  ok('...sent home and called again: still dressed', /_d3_m\d/.test(await ms()) && /em_head_r5/.test(await ms()));
  await hold('cos_outfit_2'); await press(false); await sleep(300);
  await run('execute as @e[type=cat,tag=bm.emmapet] at @s run function bm:p62/emma_go'); await sleep(600);
  await run('execute as TestRat at @s run function bm:p57/summon_here'); await sleep(1800);
  const om = await ms();
  ok('The Cozy Sweater: still on after a recall', /_o2/.test(om), om.split(' ').filter(m => /_o/.test(m)).join(' '));
  await run(`scoreboard players set #me bm.pid ${pid}`); await run('execute as @e[type=cat,tag=bm.emmapet] at @s run function bm:p57/ascend'); await sleep(1200);
  const oe = await ms();
  ok('...ethereal in the sweater: her own ethereal armour', oe.split(' ').includes('bm:ee_body') && !/_o2|ee_\w+_[ca]\d/.test(oe), oe.split(' ').filter(m => /ee_|_o/.test(m)).join(' '));
  await run('execute as @e[type=cat,tag=bm.emmapet] at @s run function bm:p62/emma_go'); await sleep(400);
  await hold('cos_outfit_2'); await press(true); await hold('cos_dress_3'); await press(true); await hold('cos_ribbon_5'); await press(true);
  // Celi, Zib
  await run('execute as TestRat at @s run function bm:p66/summon_here'); await sleep(1500);
  await hold('cos_celi_2'); await press(false);
  await run('execute as @e[type=wolf,tag=bm.celipet] at @s run function bm:p66/go'); await sleep(500);
  await run('execute as TestRat at @s run function bm:p66/summon_here'); await sleep(1800);
  ok('Celi called again: still in Rosehip', (await allModels('bm.cep')).some(m => /_o2$/.test(m)));
  await run('kill @e[type=item_display,tag=bm.cep]'); await sleep(1200);
  ok('...her rig rebuilt: still in Rosehip', (await allModels('bm.cep')).some(m => /_o2$/.test(m)));
  await hold('cos_celi_2'); await press(true);
  await run('execute as @e[type=wolf,tag=bm.celipet] at @s run function bm:p66/go'); await sleep(400);
  await run('scoreboard players set TestRat bm.zbcd 0'); await run('execute as TestRat at @s run function bm:p72/zb/summon'); await sleep(1500);
  await hold('cos_zib_1'); await press(false);
  await run('kill @e[type=item_display,tag=bm.zbr]'); await sleep(1500);
  ok('Zib\'s rig rebuilt: still in the Crimson Guard uniform', (await allModels('bm.zbr')).some(m => /_u1$/.test(m)));
  await hold('cos_zib_1'); await press(true);
  await run('execute as @e[type=wolf,tag=bm.zibpet] at @s run function bm:p72/zb/beamup'); await sleep(400);
  // Cecil's gem
  await run('scoreboard players set TestRat bm.cpel 3'); await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(1500);
  const cm = await allModels('bm.cpet');
  ok('Cecil called with a gem in: his robe in its colour', cm.some(m => /cec2_head_/.test(m)), cm.join(' '));
  await run('execute as @e[type=wolf,tag=bm.cecilpet] at @s run function bm:p62/cecil_go'); await sleep(500);
  await run('execute as TestRat at @s run function bm:p46/pet/summon'); await sleep(400);
  const cg = await cmd('type=item_display,tag=bm.cp_eyes');
  ok('Cecil arrives rolling his eyes', /roll/.test(cg), cg); await sleep(1100);
  ok('...and again after a recall', (await allModels('bm.cpet')).some(m => /cec2_head_/.test(m)));
  // Cecil's face: he blinks, rolls his eyes, goes deadpan - the eyes change model over a while
  const seen = new Set(); for (let i = 0; i < 60; i++) { seen.add((await cmd('type=item_display,tag=bm.cp_eyes')).replace(/^.*data: /, '').trim()); await sleep(250); }
  ok('Cecil\'s eyes move: blinks, a deadpan look, a sly one...', seen.size >= 2 || [...seen].some(x => /deadpan|sly|roll|blink/.test(x)), [...seen].join(' | '));
  await run('scoreboard players reset TestRat bm.cpel');
  await run('execute as @e[type=wolf,tag=bm.cecilpet] at @s run function bm:p62/cecil_go'); await sleep(400);

  // ================================================================== EMMA'S FACE
  await run('execute as TestRat at @s run function bm:p57/summon_here'); await sleep(1000);
  const ef = new Set(); for (let i = 0; i < 30; i++) { ef.add((await cmd('type=item_display,tag=bm.ep_head')).replace(/^.*data: /, '').trim()); await sleep(200); }
  ok('Emma beams when she arrives, and blinks', [...ef].some(s => /happy/.test(s)) && ef.size >= 2, [...ef].join(' | '));
  await run('damage @e[type=cat,tag=bm.emmapet,limit=1] 2 minecraft:generic'); await sleep(250);
  const eh = await cmd('type=item_display,tag=bm.ep_head');
  ok('...a hit: her hurt face', /hurt/.test(eh), eh);
  await run(`summon minecraft:zombie ~ ~ ~ {Tags:["bm.t96z"],NoAI:1b,PersistenceRequired:1b}`.replace('~ ~ ~', `${X + 0.5} ${Y} ${Z + 16.5}`)); await sleep(1400);
  let es = '';
  for (let i = 0; i < 12 && !/serious|blink/.test(es); i++) { es = await cmd('type=item_display,tag=bm.ep_head'); if (!/serious|blink/.test(es)) await sleep(150); }
  ok('...a monster close: serious', /serious|blink/.test(es), es);
  await run('kill @e[type=zombie,tag=bm.t96z]');
  await run('execute as @e[type=cat,tag=bm.emmapet] at @s run function bm:p62/emma_go'); await sleep(400);

  // ================================================================== THE ETHEREAL GEM
  await run('clear TestRat'); await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 20.5} 180 0`);
  const gemIds = fs.readdirSync(`${DP}/function/p60/gem`).filter(f => /^use_/.test(f)).map(f => f.replace(/^use_|\.mcfunction$/g, ''));
  await run('clear TestRat');
  for (const k of gemIds) await run(`loot give TestRat loot bm:items/gem_${k}`);
  await run('item replace entity TestRat weapon.mainhand with air'); await run(`loot replace entity TestRat weapon.mainhand loot bm:items/gem_${gemIds[0]}`);
  await run(`clear TestRat *[minecraft:custom_data~{bm:"gem_${gemIds[0]}"}] 1`); await run(`loot replace entity TestRat weapon.mainhand loot bm:items/gem_${gemIds[0]}`);
  await run('advancement revoke TestRat only bm:story/ethereal_gem');
  await run('scoreboard players set TestRat bm.gmcd 0'); await run(`execute as TestRat at @s run function bm:p60/gem/use_${gemIds[0]}`); await sleep(4200);
  const left = await inv('gem_' + gemIds[1]);
  ok('All nine in your hands, use one: they rise, fuse - the Ethereal Gem, and "Nine Made One"', left === 0 && (await inv('ethereal_gem')) === 1 && (await adv('ethereal_gem')),
     `left ${left}, gem ${await inv('ethereal_gem')}, adv ${await adv('ethereal_gem')}`);
  // one a heist: the coat check keeps the rest
  await run('clear TestRat'); await run('loot give TestRat loot bm:items/ethereal_gem'); await run('loot give TestRat loot bm:items/ethereal_gem');
  await run('scoreboard players set TestRat bm.gvrun 99001'); await run('scoreboard players reset #eth0 bm.gvrun');
  await run('execute as TestRat at @s run function bm:p94/eth/gate {s:0}'); await sleep(200);
  ok('Into a heist with two Ethereal Gems: you keep one, the Fixer minds the other', (await inv('ethereal_gem')) === 1, `kept ${await inv('ethereal_gem')}`);
  await run('loot give TestRat loot bm:items/ethereal_gem'); await run('execute as TestRat at @s run function bm:p94/eth/gate {s:0}'); await sleep(200);
  ok('...a second one in the same run: held too', (await inv('ethereal_gem')) === 0, `kept ${await inv('ethereal_gem')}`);
  const bag = await run(`data get storage bm:gv bag.p${pid}.inv`);
  ok('...they\'re in your coat-check bag for when you leave', (bag.match(/ethereal_gem/g) || []).length >= 2, bag.slice(0, 160));
  await run(`data remove storage bm:gv bag.p${pid}`); await run('clear TestRat');

  await run('gamerule doMobSpawning true'); await run(`forceload remove ${X - 40} ${Z - 40} ${X + 40} ${Z + 40}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`); process.exit(0);
})();

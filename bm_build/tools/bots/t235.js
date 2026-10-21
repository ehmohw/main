// 2.86: THE CHEF, THE HIDDEN FOLLOWER - the owner's checklist, as a regular (non-op) player, every step a real packet (rcon
// sets the stage: a floor, the items, a Chef Fromage villager): the five Prime meats eaten (real items) - by Chef Fromage, his
// old master turns up; asked for a Prime cut, won with one (the Golden Ladle, the advancement, he comes); his menu (Sit /
// follow, Send him home, The Chef's ways, Wardrobe; Well Fed 0 of 5); sat from the menu and stood by a right-click; PRIME
// PRESENCE - a cow killed by him drops Prime Beef; FED all five of Chef Fromage's feasts by right-clicks (Well Fed 5, the Master
// Chef: 80 health) - a foe off: a pie in its face; Midnight Brigade worn and kept across a send-home and a call, put back; his
// aura; his Raid Contract; the wheel lists him; the Ladle in a frame; a display case (his figurine); Cecil's doll bought in a
// real trade; knocked out - he faints, two minutes on the Ladle.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const num = async (sel, path) => +(((await nbt(sel, path)).match(/(-?[\d.]+)/) || [0, NaN])[1]);
  const score = async (o, who = 'TestRat') => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const tags = async () => (await run('tag TestRat list'));
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const hold = async (slot, ms = 1600) => { A.slot(slot); await sleep(250); A.use(); await sleep(ms); A.release(); await sleep(400); };
  const sneakMenu = async (slot) => { const n0 = A.dialogN.length; await use(slot, true); await wait(3000, async () => A.dialogN.length > n0); return A.dialogN.length > n0; };
  const dd = (d) => d && (d.data || d);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };

  const X = 16740, Y = 100, Z = 16000;
  const PET = '@e[type=minecraft:wolf,tag=bm.kkpet,tag=!bm.ffpet,limit=1]';
  const BODY = '@e[type=minecraft:item_display,tag=bm.kkp_pet,tag=bm.kkp_body,tag=!bm.kkfade,limit=1]';
  const model = async (sel = BODY) => (await nbt(sel, 'item.components."minecraft:item_model"')).replace(/"/g, '');
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.kkpet]'); await run('kill @e[type=minecraft:interaction,tag=bm.kkenc]'); await run('kill @e[type=minecraft:item_display,tag=bm.kkencp]');
  for (const o of ['bm.kkcd', 'bm.coskk', 'bm.wuchef', 'bm.kqg', 'bm.kqgl']) await run(`scoreboard players set TestRat ${o} 0`);
  for (const t of ['bm.auown_chef', 'bm.au_chef', 'bm.kkmet']) await run(`tag TestRat remove ${t}`);
  await run('advancement revoke TestRat only bm:met/chef'); await run('advancement revoke TestRat only bm:story/chef_friend'); await run('advancement revoke TestRat only bm:p186/ate_prime'); await run('advancement revoke TestRat only bm:story/chef_master');
  const BIT = +require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p186/sign.mcfunction', 'utf8').match(/scoreboard players add @s bm\.fcon (\d+)/)[1];
  const fc = await score('bm.fcon'); if (fc > 0 && Math.floor(fc / BIT) % 2 === 1) await run(`scoreboard players set TestRat bm.fcon ${fc - BIT}`);   // (unsigned, for the contract step)
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);

  // ---------------------------------------------------------------- finding him: the five Prime meats eaten, then Chef Fromage
  await run('effect give TestRat minecraft:hunger 30 30 true'); await sleep(2500); await run('effect clear TestRat minecraft:hunger');
  await run('effect give TestRat minecraft:resistance 900 4 true');
  const PR = ['prime_beef', 'prime_pork', 'prime_mutton', 'prime_chicken', 'prime_rabbit'];
  for (let i = 0; i < 5; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${PR[i]}`);
  const starve = async () => { for (let k = 0; k < 20; k++) { await run('effect give TestRat minecraft:hunger 2 250 true'); await sleep(1000);
    if (+((await run('data get entity TestRat foodLevel')).match(/(-?\d+)$/) || [0, 20])[1] <= 12) break; } await run('effect clear TestRat minecraft:hunger'); };
  for (let i = 0; i < 5; i++) { await starve(); await hold(i, 3800); }
  ok('the five Prime meats eaten (as food, one each)', (await cnt('@a[name=TestRat,advancements={bm:p186/ate_prime=true}]')) === 1);
  await run(`${O}summon minecraft:villager ${X + 0.5} ${Y + 1} ${Z + 5.5} {Tags:["bm.npc_chef","bm.t235v"],NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b}`);
  A.chats.length = 0;
  const ENC = '@e[type=minecraft:interaction,tag=bm.kkenc,limit=1]';
  ok('near Chef Fromage: his old master turns up in the kitchen (his rig and a click box)', await wait(5000, async () => (await cnt(ENC)) === 1) &&
     (await cnt('@e[type=minecraft:item_display,tag=bm.kkencp]')) === 9 && A.chats.some(c => /delicious smell/.test(c)), A.chats.slice(-1).join(''));
  const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
  await at(ex + 0.5, Y + 1, ez - 2, 0, 20);
  let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8);
  await sleep(250); A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(900);
  ok('right-clicked empty-handed: he asks to taste a Prime cut', A.bars.some(b => /Prime cut/.test(b)), A.bars.slice(-1).join(''));
  await run('loot replace entity TestRat hotbar.8 loot bm:items/prime_beef'); await sleep(700);
  A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
  ok('right-clicked holding Prime Beef: he joins - the cut eaten, the Golden Ladle given', (await has('chef_ladle')) === 1 && (await has('prime_beef')) === 0,
     A.chats.slice(-2).join(' | ').slice(0, 200));
  ok('...the encounter gone, and he comes along (his rig, his own)', (await cnt(ENC)) === 0 && await wait(3000, async () => (await cnt(PET)) === 1) &&
     (await score('bm.pid', PET)) === (await score('bm.pid')));
  ok('..."The Chef Recommends", and he\'s met', (await cnt('@a[name=TestRat,advancements={bm:story/chef_friend=true,bm:met/chef=true}]')) === 1);
  await run(`${O}kill @e[tag=bm.t235v]`); await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/chef_ladle');
  const kit = [null, 'cos_chef_1', 'cos_aura_chef', 'fcontract_chef'];
  for (let i = 1; i < kit.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${kit[i]}`);
  await sleep(800);

  // ---------------------------------------------------------------- UI: his menu
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  A.bars.length = 0; await use(0); await sleep(1500);
  ok('the Ladle used while he\'s out: he\'s called over ("Coming, coming!")', A.bars.some(b => /Coming, coming/.test(b)) && (await cnt(PET)) === 1, A.bars.slice(-1).join(''));
  ok('...his rig: nine parts, 40 health', (await cnt('@e[type=minecraft:item_display,tag=bm.kkp_pet,tag=!bm.kkfade]')) === 9 &&
     (await num(PET, 'attributes[{id:"minecraft:max_health"}].base')) === 40);
  ok('sneak + use: his menu', await sneakMenu(0));
  const labels = A.buttons().map(b => b.label);
  ok('...Sit / follow, Send him home, The Chef\'s ways, Wardrobe', ['Sit / follow', 'Send him home', "The Chef's ways", 'Wardrobe'].every(l => labels.some(x => x.includes(l))), labels.join(' | '));
  const bodyTxt = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]).body || []);
  ok('...Well Fed shown: 0 of 5', /Well Fed/.test(bodyTxt) && /"0"/.test(bodyTxt) && /of 5/.test(bodyTxt), bodyTxt.slice(0, 200));
  let pr = await A.press(/The Chef's ways/);
  const pw = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]).body || []);
  ok('his menu -> The Chef\'s ways: Prime Presence, Feed him, The Master Chef', pr && pr.next && ['Prime Presence', 'Feed him', 'The Master Chef'].every(w => pw.includes(w)), pw.slice(0, 160));
  await sleep(2200);                                         // (the item-use debounce from opening her menu)

  // ---------------------------------------------------------------- sitting: menu and right-click
  await sneakMenu(0); A.bars.length = 0; await A.press(/Sit \/ follow/); await sleep(1500);
  ok('Sit / follow: he sits', /1b/.test(await nbt(PET, 'Sitting')) && A.bars.some(b => /rest his feet/.test(b)), A.bars.slice(-1).join(''));
  await wait(3000, async () => (await score('bm.kqs', PET)) === 4);
  ok('...his seated cycle plays (state 4)', (await score('bm.kqs', PET)) === 4);
  const seen = new Set(); for (let k = 0; k < 14; k++) { seen.add(await nbt('@e[type=minecraft:item_display,tag=bm.kkp_pet,tag=bm.kkp_legr,limit=1]', 'transformation')); await sleep(250); }
  ok('...and moves while he sits (sit_a -> sit_b)', seen.size >= 2, `${seen.size} distinct`);
  const hitSel = '@e[type=minecraft:interaction,tag=bm.kkhit,limit=1]';
  await wait(3000, async () => (await cnt(hitSel)) === 1);
  const wx = await num(PET, 'Pos[0]'), wz = await num(PET, 'Pos[2]');
  await at(wx + 0.5, Y + 1, wz - 1.5, 0, 30);
  A.slot(8); await sleep(300); let hb = await entOf(hitSel);
  A.bars.length = 0; if (hb) A.interact(hb.entityId); await sleep(1000);
  ok('right-clicked: he stands', !!hb && /0b/.test(await nbt(PET, 'Sitting')) && A.bars.some(b => /Allons-y/.test(b)), A.bars.slice(-1).join(''));

  // ---------------------------------------------------------------- PRIME PRESENCE: a cow killed by him drops Prime Beef
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0); await sleep(800);
  await run(`${O}execute at ${PET} run summon minecraft:cow ~2 ~ ~ {Tags:["bm.t235c"],NoAI:1b,PersistenceRequired:1b}`);
  ok('a cow near him: primed (his Prime table)', await wait(4000, async () => /p186\/prime\/cow/.test(await nbt('@e[tag=bm.t235c,limit=1]', 'DeathLootTable'))));
  await run(`${O}execute as @e[tag=bm.t235c] at @s run damage @s 100 minecraft:player_attack by TestRat`); await sleep(800);
  const pb = await cnt(`@e[type=minecraft:item,x=${X},y=${Y + 1},z=${Z},distance=..12,nbt={Item:{components:{"minecraft:custom_data":{bm:"prime_beef"}}}}]`);
  const rb = await cnt(`@e[type=minecraft:item,x=${X},y=${Y + 1},z=${Z},distance=..12,nbt={Item:{id:"minecraft:beef"}}]`);
  ok('...killed: it drops Prime Beef, no plain beef', pb >= 1 && rb === 0, `prime ${pb} plain ${rb}`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y + 1},z=${Z},distance=..14]`);
  await run(`${O}summon minecraft:cow ${X + 9} ${Y + 1} ${Z + 9} {Tags:["bm.t235d"],NoAI:1b,PersistenceRequired:1b}`); await run(`${O}tp ${PET} ${X - 9} ${Y + 1} ${Z - 9}`);
  await run(`${O}data modify entity ${PET} Sitting set value 1b`); await sleep(2500);
  ok('...a cow 25 blocks from him stays plain', !/p186/.test(await nbt('@e[tag=bm.t235d,limit=1]', 'DeathLootTable')));
  await run(`${O}kill @e[tag=bm.t235d]`); await run(`${O}data modify entity ${PET} Sitting set value 0b`); await run(`${O}tp ${PET} ${X + 1.5} ${Y + 1} ${Z + 0.5}`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y + 1},z=${Z},distance=..20]`); await sleep(800);

  // ---------------------------------------------------------------- FEED HIM: Chef Fromage's five feasts, right-clicked onto him
  const FE = ['feast_health_1', 'feast_strength_2', 'feast_resistance_1', 'feast_haste_1', 'feast_speed_2'];
  let fedOk = true;
  for (let i = 0; i < FE.length; i++) {
    await run(`loot replace entity TestRat hotbar.7 loot bm:items/${FE[i]}`); A.slot(7); await sleep(400);
    const px = await num(PET, 'Pos[0]'), pz = await num(PET, 'Pos[2]');
    await at(px + 0.5, Y + 1, pz - 1.6, 0, 30);
    await wait(3000, async () => (await cnt(hitSel)) === 1); hb = await entOf(hitSel); A.slot(7); await sleep(300);
    A.chats.length = 0; if (hb) A.interact(hb.entityId); await sleep(1200);
    fedOk = fedOk && (await score('bm.kqgl')) === i + 1 && (await has(FE[i])) === 0;
    if (i === 0) ok('a feast right-clicked onto him: he eats it - Well Fed 1 of 5', fedOk, A.chats.slice(-1).join('').slice(0, 160));
    await sleep(600);
  }
  ok('...all five kinds: Well Fed 5 of 5', fedOk && (await score('bm.kqgl')) === 5, `${await score('bm.kqgl')}`);
  ok('...the Master Chef: 80 health, the advancement', /bm\.kkmaster/.test(await run(`${O}tag ${PET} list`)) && (await num(PET, 'attributes[{id:"minecraft:max_health"}].base')) === 80 &&
     (await cnt('@a[name=TestRat,advancements={bm:story/chef_master=true}]')) === 1);
  await run('loot replace entity TestRat hotbar.7 loot bm:items/feast_health_2'); await sleep(400);
  hb = await entOf(hitSel); A.slot(7); await sleep(300); A.bars.length = 0; if (hb) A.interact(hb.entityId); await sleep(1000);
  ok('...a kind he knows: eaten, but no new kind ("Bring me something new")', (await score('bm.kqgl')) === 5 && A.bars.some(b => /something new/.test(b)), A.bars.slice(-1).join(''));
  await sneakMenu(0); const bt2 = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]).body || []);
  ok('...his menu: Well Fed 5 of 5 - the Master Chef!', /"5"/.test(bt2) && /Master Chef/.test(bt2), bt2.slice(0, 200));
  await sleep(2200);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  const zom = (dx, dz, t) => run(`${O}summon minecraft:husk ${X + dx} ${Y + 1} ${Z + dz} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t235z","${t}","bm.seen"],attributes:[{id:"minecraft:max_health",base:300}],Health:300f}`);
  await run(`scoreboard players set ${PET} bm.kqgc 900`); await run(`scoreboard players set ${PET} bm.kqbc 900`);
  await zom(9, 0, 'bm.t235a');
  ok('the Master Chef, a foe 8 blocks off: a pie in its face (hurt, slowed)', await wait(6000, async () => (await num('@e[tag=bm.t235a,limit=1]', 'Health')) < 300) &&
     /slowness/.test(await nbt('@e[tag=bm.t235a,limit=1]', 'active_effects')));
  await run(`scoreboard players set ${PET} bm.kqgc 0`); A.bars.length = 0;
  ok('...the charge ready: the MEATBALL BARRAGE', await wait(8000, async () => A.bars.some(b => /MEATBALL BARRAGE/.test(b))), A.bars.slice(-1).join(''));
  await run(`${O}kill @e[tag=bm.t235z]`); await sleep(500);

  // ---------------------------------------------------------------- cosmetics: Blue Flame, kept across a recall; her aura
  await hold(1); await sleep(800);
  ok('Midnight Brigade used while he\'s out: picked (bm.coskk 1) and worn (cf_body_c1)', (await score('bm.coskk')) === 1 && /cf_body_c1$/.test(await model()), await model());
  await sneakMenu(0); A.bars.length = 0; await A.click(/Send him home/); await sleep(1500);
  ok('Send him home: he goes', (await cnt(PET)) === 0 && A.bars.some(b => /return to my stove/.test(b)), A.bars.slice(-1).join(''));
  await sneakMenu(0);
  ok('...his menu now says Call for The Chef', A.buttons().some(b => /Call for The Chef/.test(b.label)) && !A.buttons().some(b => /Send him home/.test(b.label)));
  await A.click(/Call for The Chef/); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('...called from the menu: back, still in Midnight Brigade', (await cnt(PET)) === 1 && /cf_body_c1$/.test(await model()), await model());
  await sneakMenu(0); const w1 = await A.press(/Wardrobe/);
  ok('his menu -> Wardrobe: his whites', w1 && w1.next && ['His spotless whites', 'Midnight Brigade', 'Bistro Blue', 'Sommelier Wine'].every(l => A.buttons().some(b => b.label.includes(l))),
     A.buttons().map(b => b.label).join(' | '));
  await A.press(/His spotless whites/); await sleep(1000);
  ok('"His spotless whites": back to his own (cf_body)', /^bm:cf_body$/.test(await model()) && (await score('bm.coskk')) === 0, await model());
  A.chats.length = 0; await hold(2); await sleep(600);
  ok('Kitchen Steam (his rare aura) used: his for good, and on', /bm\.auown_chef/.test(await tags()) && /bm\.au_chef\b/.test(await tags()), await tags());

  // ---------------------------------------------------------------- his Raid Contract
  await sleep(2200);
  const fc0 = await score('bm.fcon');
  A.chats.length = 0; await hold(3); await sleep(600);
  ok('his Raid Contract used: signed, the contract gone', Math.floor((await score('bm.fcon')) / BIT) % 2 === 1 && (await score('bm.fcon')) > fc0 && (await has('fcontract_chef')) === 0 && A.chats.some(c => /Signed!/.test(c)),
     A.chats.slice(-1).join('').slice(0, 160));
  const rec = require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p137/rc/main.mcfunction', 'utf8');
  ok('...and the Recruiter sells it', /fcontract_chef/.test(rec));

  // ---------------------------------------------------------------- the partner wheel knows him
  const wheel = require('fs').readFileSync('/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p179/w/open.mcfunction', 'utf8');
  ok('the Partner Wheel lists him', /The Chef|the Chef/.test(wheel) || require('child_process').execSync('grep -rl "p186/try_summon" /home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p179 | head -1').toString().length > 0);

  // ---------------------------------------------------------------- frame gimmick
  await sneakMenu(0); await A.click(/Send him home/); await sleep(1200);
  await run(`${O}fill ${X - 6} ${Y + 1} ${Z + 5} ${X + 6} ${Y + 3} ${Z + 5} minecraft:stone`);
  await run(`${O}summon minecraft:item_frame ${X} ${Y + 2} ${Z + 4} {Facing:2b,Tags:["bm.t235f"]}`); await sleep(400);
  await at(X + 0.5, Y + 1, Z + 2.5, 0, -10);
  const frSel = '@e[type=minecraft:item_frame,tag=bm.t235f,limit=1]';
  let fr = null; await wait(4000, async () => (fr = await entOf(frSel)) != null, 250);
  A.slot(0); await sleep(300); A.bars.length = 0; if (fr) A.interact(fr.entityId); await sleep(2800);
  const FPET = `@e[type=minecraft:wolf,tag=bm.kkpet,tag=bm.ffpet,x=${X},y=${Y + 2},z=${Z + 4},distance=..10]`;
  ok('the Ladle in a frame: the Chef climbs out (and makes himself at home)', (await cnt(FPET)) === 1 && A.bars.some(b => /The Chef climbs out of the frame.*himself/.test(b)), A.bars.slice(-1).join(''));
  if (fr) A.attack(fr.entityId); await sleep(600);
  ok('the Ladle punched out of the frame: he goes with it', await wait(3000, async () => (await cnt(FPET)) === 0));
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y + 2},z=${Z + 4},distance=..4]`); await run(`${O}kill ${frSel}`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"chef_ladle"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/chef_ladle');

  // ---------------------------------------------------------------- display case: her figurine
  await at(X - 4.5, Y + 1, Z - 4.5, 0, 70);
  await run('loot replace entity TestRat hotbar.5 loot bm:items/display_case_oak'); await use(5);
  const caseSel = `@e[type=minecraft:interaction,tag=bm.dchit,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..1.5,limit=1]`;
  ok('a display case set down', (await cnt(caseSel)) === 1);
  const FIG = `@e[type=minecraft:item_display,tag=bm.dcfg,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..2]`;
  let box = await entOf(caseSel); A.slot(0); await sleep(300); if (box) A.interact(box.entityId); await sleep(800);
  const nfig = await cnt(FIG);
  ok('the Ladle right-clicked into it: a little Chef (his parts), shrunk to fit', nfig === 9, `parts ${nfig}`);
  const ys = []; for (let k = 0; k < 10; k++) ys.push(await num(`${FIG.slice(0, -1)},limit=1,sort=random]`, 'transformation.translation[1]'));
  ok('...standing on the cushion, inside the glass', Math.min(...ys) >= -0.01 && Math.max(...ys) < 0.62, `translation y ${Math.min(...ys).toFixed(2)}..${Math.max(...ys).toFixed(2)}`);
  A.slot(8); await sleep(250); box = await entOf(caseSel); if (box) A.interact(box.entityId); await sleep(700);
  ok('...empty-handed: the Ladle back out, the figurine gone', (await has('chef_ladle')) === 1 && (await cnt(FIG)) === 0);
  await run('clear TestRat *[minecraft:custom_data~{bm:"chef_ladle"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/chef_ladle');
  A.input({ shift: true }); await sleep(250); box = await entOf(caseSel); if (box) A.attack(box.entityId); await sleep(700); A.input({}); await sleep(300);
  await run(`${O}kill @e[type=minecraft:item,x=${X - 4.5},y=${Y + 1},z=${Z - 3.5},distance=..3]`);

  // ---------------------------------------------------------------- Cecil's doll of her: a real trade
  await run(`${O}execute positioned ${X + 5.5} ${Y + 1} ${Z - 3.5} rotated 180 0 run function bm:p45/cecil/spawn`); await sleep(1500);
  const CEC = `@e[type=minecraft:villager,tag=bm.npc_wizard,x=${X + 5.5},y=${Y + 1},z=${Z - 3.5},distance=..2,limit=1]`;
  await at(X + 5.5, Y + 1, Z - 0.5, 180, 0); await sleep(2500);
  let idx = -1;
  for (let i = 0; i < 80 && idx < 0; i++) { if (/Found no elements/i.test(await nbt(CEC, `Offers.Recipes[${i}].maxUses`))) break; const s = await nbt(CEC, `Offers.Recipes[${i}].sell.components."minecraft:custom_data".bm`); if (/"doll_chef"/.test(s)) idx = i; }
  ok('Cecil sells the Chef doll', idx >= 0, `trade #${idx}`);
  const price = +(((await nbt(CEC, `Offers.Recipes[${idx}].buy.count`)).match(/(\d+)/) || [0, 0])[1]);
  const buyId = (await nbt(CEC, `Offers.Recipes[${idx}].buy.components."minecraft:custom_data".bm`)).replace(/"/g, '');
  for (let i = 0; i < price; i++) await run(`loot give TestRat loot bm:items/${buyId}`);
  const cec = await entOf(CEC); A.windows.length = 0; if (cec) A.interact(cec.entityId); await sleep(900);
  const w = A.windows[A.windows.length - 1];
  if (w && idx >= 0) {
    A.write('select_trade', { slot: idx }); await sleep(300);
    A.write('window_click', { windowId: w.windowId, stateId: 0, slot: 2, mouseButton: 0, mode: 1, changedSlots: [], cursorItem: undefined }); await sleep(500);
    A.close(w.windowId); await sleep(400);
  }
  ok(`...bought in his window`, (await has('doll_chef')) === 1, `dolls ${await has('doll_chef')}`);
  await run(`${O}kill ${CEC}`);
  await run('clear TestRat *[minecraft:custom_data~{bm:"doll_chef"}]'); await run('loot replace entity TestRat hotbar.6 loot bm:items/doll_chef');
  await at(X + 2.5, Y + 1, Z - 4.5, 180, 45); A.slot(6); await sleep(200); A.use(); await sleep(350); A.release(); await sleep(600);
  const DD = `@e[type=minecraft:item_display,tag=bm.doll_chefd,x=${X + 2.5},y=${Y + 1},z=${Z - 6.5},distance=..0.4,limit=1]`;
  const DH = `@e[type=minecraft:interaction,tag=bm.doll_chefhit,x=${X + 2.5},y=${Y + 1},z=${Z - 6.5},distance=..0.4,limit=1]`;
  ok('the doll set down on a block: her own model', (await cnt(DD)) === 1 && /doll_chef/.test(await nbt(DD, 'item.components')));
  const y0 = await num(DD, 'Rotation[0]'); let dh = await entOf(DH); if (dh) A.interact(dh.entityId); await sleep(700);
  ok('...right-clicked: it twirls', Math.abs(((await num(DD, 'Rotation[0]') - y0 + 540) % 360) - 180) > 30);
  A.input({ shift: true }); await sleep(250); dh = await entOf(DH); if (dh) A.attack(dh.entityId); await sleep(700); A.input({}); await sleep(300);
  ok('...sneak + punch: back in the pack', (await has('doll_chef')) === 1 && (await cnt(DD)) === 0);

  // ---------------------------------------------------------------- knocked out: she faints
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  A.chats.length = 0; await run(`${O}damage ${PET} 200 minecraft:mob_attack`);
  ok('struck down: he faints, his rig fades away', await wait(4000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.kkp_pet]')) === 0));
  ok('..."The Chef faints!" - two minutes on the Ladle', A.chats.some(c => /The Chef faints!/.test(c)) && (await score('bm.kkcd')) > 100, A.chats.slice(-1).join('').slice(0, 160));
  A.bars.length = 0; await use(0); await sleep(800);
  ok('...the Ladle used: "still catching his breath", no Chef', (await cnt(PET)) === 0 && A.bars.some(b => /catching his breath/.test(b)), A.bars.slice(-1).join(''));

  // ---------------------------------------------------------------- clean up
  await run('scoreboard players set TestRat bm.kkcd 0'); await run('clear TestRat'); await run('scoreboard players reset TestRat bm.kqgl'); await run('scoreboard players reset TestRat bm.kqg');
  for (const t of ['bm.auown_chef', 'bm.au_chef', 'bm.kkmet']) await run(`tag TestRat remove ${t}`);
  await run(`${O}kill @e[type=minecraft:wolf,tag=bm.kkpet]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

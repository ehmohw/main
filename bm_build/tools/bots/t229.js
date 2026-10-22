// 2.85b: ANGELIC FORGING - as a regular player (rcon sets the stage: the hour, the other three pieces, the trip to the Hollow).
//   the forge: the Deathmask tossed down beside a Golden Cross - light gathers, and it comes up angelic (bm_angel, its white-gold
//     model, gold trim), the cross spent; its enchantments kept. The True Crown the same way.
//   the purified set worn (the other three made angelic by rcon): by day it wakes (+15% damage), at high noon more (+30%), by
//     night not at all; one corrupt piece and it's the old Regalia (night wakes it).
//   the angelic crown: Strength II by day, not by night.
//   a re-sync (an old item version) keeps it angelic.
//   tossed onto Apophiss's seal in the Hollow: corrupted back (bm_angel 0b, the netherite look).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +(((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, NaN])[1]);
  const has = async id => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${id}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const passes = async c => /passed/i.test(await run(c));
  const O = 'execute in minecraft:overworld run ';
  const X = 13480, Y = 121, Z = 13400;
  const slotOf = async id => { for (let s = 0; s < 9; s++) if (new RegExp(`"${id}"`).test(await run(`data get entity TestRat Inventory[{Slot:${s}b}].components."minecraft:custom_data".bm`))) return s; return -1; };
  const power = async () => { const m = (await run('attribute TestRat minecraft:attack_damage modifier value get bm:rg_power')).match(/is (-?[\d.]+)/); return m ? +m[1] : 0; };
  const toss = async (ids) => { for (const id of ids) { const s = await slotOf(id); A.slot(s); await sleep(200); A.drop(true); await sleep(250); } };
  const fetch = async (dim, id) => run(`execute in ${dim} positioned as TestRat as @e[type=minecraft:item,distance=..32] if items entity @s contents *[minecraft:custom_data~{bm:"${id}"}] at @s run tp TestRat ~ ~ ~`);
  const saved = { bmoff: await sc('#bmoff', 'bm.cfg') };

  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:stone`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 4} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..14]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 60`); await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat');
  await run('scoreboard players set #bmoff bm.cfg 1'); await run('time set 6000');
  await sleep(1200); A.stand();

  // ================================================================== 1. the forge
  await run('loot give TestRat loot bm:items/conq_helmet'); await run('loot give TestRat loot bm:items/golden_cross'); await sleep(400);
  A.bars.length = 0; await toss(['conq_helmet', 'golden_cross']);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 4.5} 0 0`);
  ok('The Deathmask tossed down beside a Golden Cross: light gathers', await wait(3000, async () => A.bars.some(b => /Light gathers/.test(b))), A.bars.slice(-1).join(''));
  const angelOnGround = async () => passes(`${O}execute as @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..8] if items entity @s contents *[minecraft:custom_data~{bm:"conq_helmet",bm_angel:1b}]`);
  ok('...and it comes up angelic, the cross spent', await wait(8000, angelOnGround) &&
     !(await passes(`${O}execute as @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..8] if items entity @s contents *[minecraft:custom_data~{bm:"golden_cross"}]`)));
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`);
  await wait(4000, async () => (await has('conq_helmet')) === 1);
  const hs = await slotOf('conq_helmet');
  const hd = await run(`data get entity TestRat Inventory[{Slot:${hs}b}].components`);
  ok('...picked up: the angelic model, gold trim, its name - and its Protection kept', /angel_conq_helmet/.test(hd) && /minecraft:gold/.test(hd) &&
     /Angelic/.test(hd) && /protection/.test(hd), hd.replace(/.*data: /, '').slice(0, 160));
  // the True Crown
  await run('loot give TestRat loot bm:items/apo_true_crown'); await run('loot give TestRat loot bm:items/golden_cross'); await sleep(400);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 60`); await sleep(400);
  await toss(['apo_true_crown', 'golden_cross']); await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 4.5} 0 0`);
  await wait(9000, async () => passes(`${O}execute as @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..8] if items entity @s contents *[minecraft:custom_data~{bm:"apo_true_crown",bm_angel:1b}]`));
  await fetch('minecraft:overworld', 'apo_true_crown');
  const gotC = await wait(4000, async () => (await has('apo_true_crown')) === 1);
  const cm = await run(`data get entity TestRat Inventory[{Slot:${await slotOf('apo_true_crown')}b}].components."minecraft:item_model"`);
  ok('Apophiss\'s True Crown the same way: angelic', gotC && /angel_apo_true_crown/.test(cm), `${gotC} ${await slotOf('apo_true_crown')} ${cm}`);
  // 2.88: the Wings of the Damned
  await run('loot give TestRat loot bm:items/hollow_wings'); await run('loot give TestRat loot bm:items/golden_cross'); await sleep(400);
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 60`); await sleep(400);
  await toss(['hollow_wings', 'golden_cross']); await run(`tp TestRat ${X + 0.5} ${Y} ${Z - 4.5} 0 0`);
  await wait(9000, async () => passes(`${O}execute as @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..8] if items entity @s contents *[minecraft:custom_data~{bm:"hollow_wings",bm_angel:1b}]`));
  await fetch('minecraft:overworld', 'hollow_wings');
  const gotW = await wait(4000, async () => (await has('hollow_wings')) === 1);
  const wc = await run(`data get entity TestRat Inventory[{Slot:${await slotOf('hollow_wings')}b}].components`);
  ok('The Wings of the Damned the same way: angelic - the holy wings on your back (still an elytra: they glide)', gotW && /angel_hollow_wings/.test(wc) &&
     /bm:angelic_wings/.test(wc) && !/"!minecraft:glider"/.test(wc), wc.slice(0, 240));
  await run('clear TestRat *[minecraft:custom_data~{bm:"hollow_wings"}]');
  // 2.88: holy, not angelic - its weapons burn and shine: the Holy Blade's Sun Rend sets the foe alight instead of withering it
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/conq_blade'); await run('item modify entity TestRat hotbar.0 bm:p182/up_conq_blade');
  await run(`tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); A.slot(0); await sleep(400);
  const bn = await run('data get entity TestRat Inventory[{Slot:0b}].components."minecraft:item_name"');
  ok('...named Holy, not Angelic', /Holy/.test(bn) && !/Angelic/.test(bn), bn.slice(0, 160));
  await run(`${O}summon minecraft:husk ${X + 0.5} ${Y} ${Z + 3} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.hrend","bm.seen"],attributes:[{id:"minecraft:max_health",base:200}],Health:200f}`);
  await sleep(600); A.use(); await sleep(250); A.release && A.release(); await sleep(700);
  const hf = +(((await run(`${O}data get entity @e[tag=bm.hrend,limit=1] Fire`)).match(/(-?\d+)s?$/) || [0, -1])[1]);
  const hw = /wither/.test(await run(`${O}data get entity @e[tag=bm.hrend,limit=1] active_effects`));
  const hh = +(((await run(`${O}data get entity @e[tag=bm.hrend,limit=1] Health`)).match(/([\d.]+)f/) || [0, 200])[1]);
  ok('...its Sun Rend: the foe torn and set alight - burning, not withering', hh < 200 && hf > 0 && !hw, `health ${hh}, Fire ${hf}, wither ${hw}`);
  await run(`${O}kill @e[tag=bm.hrend]`); await run('clear TestRat');

  // ================================================================== 2. the purified set: woken by day
  await run(`item replace entity TestRat armor.head from entity TestRat hotbar.${hs}`); await run(`item replace entity TestRat hotbar.${hs} with minecraft:air`);
  for (const [s, p] of [['chest', 'chestplate'], ['legs', 'leggings'], ['feet', 'boots']]) {
    await run(`loot replace entity TestRat armor.${s} loot bm:items/conq_${p}`); await run(`item modify entity TestRat armor.${s} bm:p182/up_conq_${p}`);
  }
  await run('time set 2000');
  ok('The purified Regalia worn, by day: angelic, and the sun wakes it (+15% damage)', await wait(4000, async () => passes('execute if entity @a[name=TestRat,tag=bm.angel]')) &&
     await wait(3000, async () => Math.abs((await power()) - 0.15) < 0.01), `${await power()}`);
  await run('time set 6000');
  ok('...at high noon: +30%', await wait(3000, async () => Math.abs((await power()) - 0.3) < 0.01), `${await power()}`);
  await run('time set 14500');
  ok('...by night: asleep', await wait(3000, async () => (await power()) === 0), `${await power()}`);
  await run('item modify entity TestRat armor.feet bm:p182/down_conq_boots');
  ok('One corrupt piece: the old Regalia - night wakes it again', await wait(4000, async () => !(await passes('execute if entity @a[name=TestRat,tag=bm.angel]'))) &&
     await wait(3000, async () => (await power()) >= 0.15), `${await power()}`);          // (+15% a plain night, +30% under a bright moon)
  // ---- the crown by day
  await run('time set 2000'); await run('effect clear TestRat');
  await run('item replace entity TestRat armor.head with minecraft:air');
  const cs = await slotOf('apo_true_crown'); await run(`item replace entity TestRat armor.head from entity TestRat hotbar.${cs}`); await run(`item replace entity TestRat hotbar.${cs} with minecraft:air`);
  const str = async () => { const m = (await run('data get entity TestRat active_effects[{id:"minecraft:strength"}].amplifier')).match(/(-?\d+)b?$/); return m ? +m[1] : -1; };
  ok('The angelic crown, by day: Strength II', await wait(3000, async () => (await str()) === 1), `${await str()}`);
  await run('time set 14500'); await run('effect clear TestRat minecraft:strength');
  await sleep(2500);
  ok('...by night: not', (await str()) < 1, `${await str()}`);
  await run('time set 6000');

  // ================================================================== 3. a re-sync keeps it angelic
  await run('item modify entity TestRat armor.chest {function:"minecraft:set_custom_data",tag:{bmv:40}}');
  ok('A re-sync (an old item version) keeps it angelic', await wait(5000, async () => /bmv: 41/.test(await run('data get entity TestRat equipment.chest.components."minecraft:custom_data"'))) &&
     /bm_angel: 1b/.test(await run('data get entity TestRat equipment.chest.components."minecraft:custom_data"')) &&
     /angel_conq_chestplate/.test(await run('data get entity TestRat equipment.chest.components."minecraft:item_model"')),
     (await run('data get entity TestRat equipment.chest.components."minecraft:custom_data"')).slice(-80));

  // ================================================================== 4. Apophiss's seal: corrupted back
  await run('item replace entity TestRat hotbar.0 from entity TestRat armor.chest'); await run('item replace entity TestRat armor.chest with minecraft:air');
  await run('execute in bm:hollow_throne run tp TestRat 1086.5 103 1083.5 90 50'); await sleep(2500); A.stand();
  ok('(the seal in the Hollow\'s throne room)', await wait(6000, async () => passes('execute in bm:hollow_throne if entity @e[type=minecraft:marker,tag=bm.apseal]')));
  A.slot(0); await sleep(200); A.drop(true); await sleep(300);
  const onSeal = async (q) => passes(`execute in bm:hollow_throne positioned 1084.5 103 1083.5 as @e[type=minecraft:item,distance=..4] if items entity @s contents *[minecraft:custom_data~{bm:"conq_chestplate",bm_angel:${q}}]`);
  ok('Tossed onto Apophiss\'s seal: black fire takes it back', await wait(4000, async () => onSeal('0b')) && !(await onSeal('1b')));
  await fetch('bm:hollow_throne', 'conq_chestplate'); await wait(4000, async () => (await has('conq_chestplate')) === 1);
  const nm = await run(`data get entity TestRat Inventory[{Slot:${await slotOf('conq_chestplate')}b}]`);
  ok('...the netherite look again', /netherite_chestplate/.test(nm) && !/angel_/.test(nm) && !/bm:angelic/.test(nm) && /quartz/.test(nm), nm.slice(-160));

  // ---- put things back
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5}`); await sleep(1000);
  await run(`scoreboard players set #bmoff bm.cfg ${isNaN(saved.bmoff) ? 0 : saved.bmoff}`);
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..14]`);
  await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode creative TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

// 2.80d: the ground forges - as a regular (non-op) player: every ingredient tossed with Q (ctrl+Q for a stack), the result
// walked over and picked up, the forged relic used and turned with F and with a catalyst. rcon sets the stage: a floor,
// the ingredients, the time of day, a husk to hit, a Lucky Night.
//   The Huntmaster's Relic: the Horseman's Head, the Crook, the Talon and the Branch tossed together -> it forges (the
//     pieces float, locked) -> the Huntmaster's Head in the head's class; F: the Crook, the Talon...; the Talon's
//     Thunderclap at its home strength in clear weather (12, not 8); a catalyst (scute, look up) turns it - still forged.
//   The Riftbound Relic: the Gauntlet + the Scepter.
//   The Starheart: a Fallen Star + a Heartstone by day: it waits (says so); at night under the sky: forged; eaten: +1 heart.
//   A forge that loses a piece (taken mid-burn) goes cold, and the rest can be picked up again.
//   The Talisman of the Three Nights: 8 Blood Crystals + 8 Lucky Tokens + a Red Xenite by night; carried on a Lucky Night:
//     Luck II.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const score = async (o) => +((await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => /Found [1-9]/.test(await run(`clear TestRat *[custom_data~{bm:"${iid}"}] 0`));
  const held = async () => await run('data get entity TestRat SelectedItem.components."minecraft:custom_data".bm');
  const X = 16700, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run('effect give TestRat minecraft:saturation 900 0 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:stone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`);
  await run('weather clear'); await run('time set 1000'); await sleep(1200);
  const stand = async (dz = 0) => { await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5 + dz} 0 25`); await sleep(700); };
  const kit = async (iids) => { await run('clear TestRat'); for (let i = 0; i < iids.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${iids[i]}`); };
  const toss = async (n, stack = false) => { for (let i = 0; i < n; i++) { A.slot(i); await sleep(200); A.drop(stack); await sleep(250); } };
  const forged = async (iid, ms = 9000) => await wait(ms, async () => (await cnt(`@e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12,nbt={Item:{components:{"minecraft:custom_data":{bm:"${iid}"}}}}]`)) >= 1);
  const pickUp = async () => { const p = (await run(`${O}data get entity @e[type=minecraft:item,tag=bm.fgout,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    if (p) { await sleep(1500); await A.walkTo(+p[1], +p[3]); await sleep(1500); } };

  // ---- the Huntmaster's Relic
  await stand(); await kit(['horseman_head', 'pharaoh_crook', 'storm_talon', 'heartwood_branch']);
  A.chats.length = 0; await toss(4);
  const locked = await wait(4000, async () => (await cnt(`@e[type=minecraft:item,tag=bm.fg,x=${X},y=${Y},z=${Z},distance=..10]`)) === 4);
  ok('the four relics tossed together: the forge wakes - all four lifted and locked', locked);
  ok('...nobody can take one while it burns (pickup delay held)', /32767s/.test(await run(`${O}data get entity @e[type=minecraft:item,tag=bm.fg,limit=1,x=${X},y=${Y},z=${Z},distance=..10] PickupDelay`)));
  ok('...and it forges the Huntmaster\'s Head (the head\'s own class: Offense)', await forged('hunt_head_1'));
  ok('...the pieces are gone', (await cnt(`@e[type=minecraft:item,tag=bm.fg,x=${X},y=${Y},z=${Z},distance=..10]`)) === 0);
  ok('..."FORGED" said to the player', A.chats.some(c => /FORGED.*Huntmaster/.test(c)), A.chats.slice(-2).join(' | '));
  await pickUp();
  ok('walked over: the Huntmaster\'s Head picked up', await has('hunt_head_1'));
  await run('clear TestRat *[custom_data~{bm:"hunt_head_1"}]'); await run('loot replace entity TestRat hotbar.0 loot bm:items/hunt_head_1');
  A.slot(0); await sleep(300); A.swap(); await sleep(400);
  ok('swap-hands (F): the next relic - the Huntmaster\'s Crook (same class)', /hunt_crook_1/.test(await held()), await held());
  A.swap(); await sleep(400);
  ok('...F again: the Talon', /hunt_talon_1/.test(await held()), await held());
  // the Thunderclap at home strength in clear weather: 8 x 1.5 = 12 to a monster within 5 blocks
  await run(`${O}summon minecraft:husk ${X + 0.5} ${Y + 1} ${Z + 3.5} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["bm.t180"],attributes:[{id:"minecraft:max_health",base:100d}],Health:100f}`);
  await sleep(400); await run('scoreboard players set TestRat bm.rcd 0');
  A.use(); await sleep(300); A.release(); await sleep(800);
  const hh = +((await run(`${O}data get entity @e[tag=bm.t180,limit=1] Health`)).match(/([\d.]+)f/) || [0, 0])[1];
  ok('the Huntmaster\'s Talon\'s Thunderclap in clear weather: home strength (12, not 8)', hh > 0 && Math.abs(100 - hh - 12) < 0.6, `health ${hh}`);
  await run(`${O}kill @e[tag=bm.t180]`);
  await run('item replace entity TestRat weapon.offhand with minecraft:armadillo_scute'); await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 -80`); await sleep(600);
  await run('scoreboard players set TestRat bm.rcd 0'); A.use(); await sleep(300); A.release(); await sleep(600);
  ok('a catalyst (scute in the off hand, look up): Defense - and still the Huntmaster\'s', /hunt_talon_2/.test(await held()), await held());

  // ---- the Riftbound Relic
  await stand(); await kit(['molten_gauntlet', 'void_scepter']); A.chats.length = 0; await toss(2);
  ok('the Gauntlet and the Scepter: the Riftbound Gauntlet', await forged('rift_gauntlet_1'));
  await pickUp(); await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/rift_gauntlet_1'); A.slot(0); await sleep(300); A.swap(); await sleep(400);
  ok('...F: the Riftbound Scepter', /rift_scepter_1/.test(await held()), await held());

  // ---- the Starheart: by day it waits; at night under the sky it forges
  await stand(); await kit(['fallen_star', 'heartstone']); A.bars.length = 0; await toss(2); await sleep(2500);
  ok('a Fallen Star by a Heartstone, by day: nothing forged...', (await cnt(`@e[type=minecraft:item,tag=bm.fg,x=${X},y=${Y},z=${Z},distance=..10]`)) === 0);
  ok('...and it says why', A.bars.some(b => /open night sky/.test(b)), A.bars.slice(-1).join(''));
  await run('time set 14000');
  ok('...at night: the Starheart', await forged('starheart'));
  await pickUp();
  ok('...picked up', await has('starheart'));
  const mh0 = +((await run('attribute TestRat minecraft:max_health get')).match(/([\d.]+)/) || [0, 0])[1];
  await run('scoreboard players set TestRat bm.shrt 0'); await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/starheart');
  A.slot(0); await sleep(300); A.use(); await sleep(2200); A.release(); await sleep(600);
  const mh1 = +((await run('attribute TestRat minecraft:max_health get')).match(/([\d.]+)/) || [0, 0])[1];
  ok('eaten: +1 max heart (+2 health), one Starheart', mh1 - mh0 >= 1.9 && (await score('bm.shrt')) === 1, `${mh0} -> ${mh1}, ${await score('bm.shrt')}`);

  // ---- a forge that loses a piece goes cold
  await stand(); await kit(['fallen_star', 'heartstone']); A.chats.length = 0; A.bars.length = 0; await toss(2);
  await wait(4000, async () => (await cnt(`@e[type=minecraft:item,tag=bm.fg,x=${X},y=${Y},z=${Z},distance=..10]`)) === 2);
  await run(`${O}kill @e[type=minecraft:item,tag=bm.fg,x=${X},y=${Y},z=${Z},distance=..10,nbt={Item:{components:{"minecraft:custom_data":{bm:"heartstone"}}}}]`); await sleep(800);
  ok('a piece lost mid-burn: the forge goes cold (no Starheart), and says so', !(await forged('starheart', 4000)) && A.bars.some(b => /went missing/.test(b)), A.bars.slice(-1).join(''));
  ok('...the star falls back down, free to pick up', /PickupDelay: ([0-9]|10)s/.test(await run(`${O}data get entity @e[type=minecraft:item,limit=1,x=${X},y=${Y},z=${Z},distance=..10,nbt={Item:{components:{"minecraft:custom_data":{bm:"fallen_star"}}}}]`)));
  await run(`${O}kill @e[type=minecraft:item,x=${X},y=${Y},z=${Z},distance=..12]`);

  // ---- the Talisman of the Three Nights
  await stand(); await run('clear TestRat');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/blood_crystal'); await run('item modify entity TestRat hotbar.0 {type:"minecraft:set_count",count:8}');
  await run('loot replace entity TestRat hotbar.1 loot bm:items/lucky_token'); await run('item modify entity TestRat hotbar.1 {type:"minecraft:set_count",count:8}');
  await run('loot replace entity TestRat hotbar.2 loot bm:items/xenite_red');
  A.chats.length = 0; await toss(3, true);
  ok('8 Blood Crystals, 8 Lucky Tokens and a Red Xenite, by night: the Talisman of the Three Nights', await forged('three_nights_talisman'));
  await pickUp();
  ok('...picked up', await has('three_nights_talisman'));
  const tod = async () => +((await run('scoreboard players get #tod bm.bm')).match(/has (-?\d+)/) || [0, 0])[1];
  const goto = async t => { await run(`time add ${((t - await tod()) % 24000 + 24000) % 24000 || 24000}`); await sleep(1500); };
  await goto(1000); if (/has 1 /.test(await run('scoreboard players get #bday bm.bm'))) await goto(1000);     // (not on a Blood Moon day)
  await run('function bm:admin/lucky_night'); await goto(13100); await wait(6000, async () => /has 1 /.test(await run('scoreboard players get #lnight bm.bm'))); await sleep(2200);
  ok('...carried on a Lucky Night: Luck II and Speed', /luck/.test(await run('data get entity TestRat active_effects')) && /speed/.test(await run('data get entity TestRat active_effects')));
  await goto(23999); await wait(6000, async () => /has 0 /.test(await run('scoreboard players get #lnight bm.bm')));

  await run('clear TestRat'); await run('time set 1000'); await run('scoreboard players set TestRat bm.shrt 0');
  await run('attribute TestRat minecraft:max_health modifier remove bm:starheart');
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..20]`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

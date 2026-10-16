// 2.80b: the special nights, as a regular (non-op) player - rcon only sets the stage (the night chosen, the clock moved on,
// a Leprechaun or a Vorn put down where the bot can reach it).
//   the Blood Moon: it rises (title, word, bar); you can't sleep through it; no Invasion on a Blood Moon day; dawn ends it.
//   a Lucky Night: it starts (title, word, bar); a Leprechaun Rat caught drops a Pot of Gold, tipped out for Tokens; dawn ends it.
//   an Invasion Night: it starts (title, word, bar); the Vorn land near you; at dawn they all lift away - troopers, saucers
//     and the bioengineered beasts.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 300) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const cnt = async sel => { const s = await run(`execute if entity ${sel}`); const m = s.match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const bar = async id => /currently visible/.test(await run(`bossbar get ${id} visible`));
  const has = async iid => { const m = (await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/); return m ? +m[1] : 0; };
  const said = re => A.chats.some(c => re.test(c));
  const O = 'execute in minecraft:overworld run ';
  const X = 13700, Y = 121, Z = 13200;
  // (the clock moved on to a time of day, never back: the pack's day count follows the world's time)
  const goto = async tod => { const t = await sc('#tod', 'bm.bm'); await run(`time add ${((tod - t) % 24000 + 24000) % 24000 || 24000}`); await sleep(1500); };
  const near = `x=${X - 64},y=-64,z=${Z - 64},dx=128,dy=400,dz=128`;      // (the Vorn land on the ground, wherever it is below)
  // (a fresh morning that isn't a Blood Moon day - the special nights never fall on one)
  const morning = async () => { await goto(1000); if ((await sc('#bday', 'bm.bm')) === 1) await goto(1000); };
  const A = await bot('TestRat'); await sleep(2500);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  // ---- the stage: an open platform under the sky, nights cleared, not a Blood Moon day
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y - 1} ${Z - 8} ${X + 8} ${Y - 1} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y + 30} ${Z + 8} minecraft:air`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y} ${Z + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:saturation 900 0 true');
  await run('gamerule doDaylightCycle false'); await run('weather clear');
  for (const [k, v] of [['#forced', 0], ['#lucky', 0], ['#ivn', 0]]) await run(`scoreboard players set ${k} bm.bm ${v}`);
  await morning();
  await sleep(1500); A.stand();

  // ================================================================== 1. the Blood Moon
  A.chats.length = 0; A.titles.length = 0;
  await run('function bm:admin/blood_moon');
  await wait(6000, async () => said(/Blood Moon has risen/));
  ok('The Blood Moon rises: its title, its word, its bar', A.titles.some(t => /Blood Moon Rises/.test(t)) && said(/Blood Moon has risen/) && await bar('bm:bloodmoon'),
     `${A.titles.slice(-2).join(' / ')} | bar ${await bar('bm:bloodmoon')}`);
  A.chats.length = 0; await run('execute as TestRat run function bm:admin/invasion_now'); await sleep(400);   // (an admin's word goes to the admin: here, the bot)
  ok('...no Invasion Night on a Blood Moon day', said(/Not on a Blood Moon day/) && (await sc('#ivn', 'bm.bm')) !== 1);
  // a bed: no sleeping through it
  await run(`${O}setblock ${X + 2} ${Y} ${Z + 1} minecraft:red_bed[facing=south,part=head]`); await run(`${O}setblock ${X + 2} ${Y} ${Z} minecraft:red_bed[facing=south,part=foot]`);
  await run(`${O}kill @e[tag=bm.surge_mob,${near}]`);     // (or vanilla refuses: "monsters nearby")
  A.bars.length = 0; A.useOn(X + 2, Y, Z, 1); await sleep(1500);
  ok('...a bed won\'t let you sleep it away ("You can\'t sleep during a Blood Moon!")', !/sleeping_pos/.test(await run('data get entity TestRat')) && A.bars.some(b => /can't sleep/.test(b)),
     A.bars.slice(-1).join(''));
  await run(`${O}fill ${X + 2} ${Y} ${Z} ${X + 2} ${Y} ${Z + 1} minecraft:air`);
  A.chats.length = 0; A.titles.length = 0; await goto(23100);
  await wait(4000, async () => said(/Blood Moon has passed/));
  ok('Dawn: the Blood Moon sets (its title, its word) and its bar goes', said(/Blood Moon has passed/) && A.titles.some(t => /Blood Moon Sets/.test(t)) && !(await bar('bm:bloodmoon')));

  // ================================================================== 2. a Lucky Night
  await morning(); A.chats.length = 0; A.titles.length = 0;
  await run('function bm:admin/lucky_night'); await goto(13100);
  await wait(4000, async () => said(/A Lucky Night!/));
  ok('A Lucky Night: its title, its word, its bar', A.titles.some(t => /A Lucky Night/.test(t)) && said(/A Lucky Night!/) && await bar('bm:luckynight'), A.titles.slice(-2).join(' / '));
  // a Leprechaun Rat, held still where the bot can reach it (it bolts otherwise)
  await run('item replace entity TestRat hotbar.0 with minecraft:diamond_sword'); A.slot(0);
  await run(`${O}execute positioned ${X + 2.5} ${Y} ${Z + 0.5} run function bm:p52/lep/spawn`); await sleep(300);
  await run(`${O}data merge entity @e[type=minecraft:ocelot,tag=bm.lep,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] {NoAI:1b}`); await sleep(800);
  ok('...a Leprechaun Rat turns up', (await cnt(`@e[type=minecraft:ocelot,tag=bm.lep,${near}]`)) >= 1);
  for (let i = 0; i < 6 && (await cnt(`@e[type=minecraft:ocelot,tag=bm.lep,${near}]`)); i++) {
    const uuid = (await run(`${O}data get entity @e[type=minecraft:ocelot,tag=bm.lep,limit=1,sort=nearest,x=${X},y=${Y},z=${Z}] UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/);
    let eid = null;
    if (uuid) { const h = uuid.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
      const e = Object.values(A.ents).find(e => e.objectUUID === u); eid = e ? e.entityId : null; }
    if (eid != null) A.attack(eid); await sleep(800);
  }
  ok('...caught: it falls', !(await cnt(`@e[type=minecraft:ocelot,tag=bm.lep,${near}]`)));
  await A.walkTo(X + 2.5, Z + 0.5); await sleep(1200); await A.walkTo(X + 0.5, Z + 0.5); await sleep(600); A.stand();
  ok('...and drops a Pot of Gold, picked up', (await has('pot_of_gold')) === 1);
  const tk0 = await has('token');
  const ps = (await run('data get entity TestRat Inventory[{components:{"minecraft:custom_data":{bm:"pot_of_gold"}}}].Slot')).match(/(\d+)b?\s*$/);
  if (ps && +ps[1] <= 8) { A.slot(+ps[1]); await sleep(300); A.use(); await sleep(1300); A.release(); await sleep(800); }   // (drunk down: held for the whole sip)
  ok('Tip out the Pot of Gold: Tokens (8 to 16)', (await has('pot_of_gold')) === 0 && (await has('token')) - tk0 >= 8, `${tk0} -> ${await has('token')}`);
  A.chats.length = 0; await goto(23100);
  await wait(4000, async () => said(/Lucky Night is over/));
  ok('Dawn: the Lucky Night is over, its bar goes', said(/Lucky Night is over/) && !(await bar('bm:luckynight')));

  // ================================================================== 3. an Invasion Night
  await morning(); A.chats.length = 0; A.titles.length = 0;
  await run('function bm:admin/invasion_now'); await goto(13100);
  await wait(4000, async () => said(/Vorn have landed/));
  ok('An Invasion Night: its title, its word, its bar', A.titles.some(t => /INVASION NIGHT/.test(t)) && said(/Vorn have landed/) && await bar('bm:invasion'), A.titles.slice(-2).join(' / '));
  const landed = await wait(40000, async () => (await cnt(`@e[tag=bm.vorn,${near}]`)) >= 1, 1000);
  ok('...the Vorn land near you (under the open sky)', landed, `${await cnt(`@e[tag=bm.vorn,${near}]`)} near`);
  // (one of each, set down to be sure: a trooper, a saucer, a beast)
  for (const k of ['trooper', 'saucer', 'bigslime']) await run(`${O}execute positioned ${X + 6} ${Y} ${Z + 6} run function bm:p32/spawn/${k}`);
  await sleep(1500);
  const before = await cnt(`@e[tag=bm.vorn,${near}]`);
  A.chats.length = 0; await goto(23100);
  await wait(5000, async () => said(/Vorn ships lift away/)); await sleep(1500);
  ok('Dawn: "The Vorn ships lift away" - and the bar goes', said(/Vorn ships lift away/) && !(await bar('bm:invasion')));
  ok('...every Vorn with them - troopers, saucers and the beasts', (await cnt(`@e[tag=bm.vorn,${near}]`)) === 0, `${before} -> ${await cnt(`@e[tag=bm.vorn,${near}]`)}`);

  // ---- the clock back to day, the platform tidied
  await goto(1000); await run('gamerule doDaylightCycle true');
  await run(`${O}kill @e[tag=bm.vorn,${near}]`); await run(`${O}kill @e[type=minecraft:item,${near}]`);
  await run('clear TestRat'); await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

// 2.98b: AN OLDER WORLD'S PARTNERS, BACK IN THEIR OWN PLACES (phase179's repair, phase180's) as a regular (non-op) player.
// The Partner Wheel saved each partner by its number - and followers slotted into the middle of the list renumbered everyone
// after them: a world from 2.94-2.95 read its 8-Bit Leo, 8-Bit Emma and Sky Buddies as Rufus, Henry and Nia. The bot puts four
// partners on its wheel (their items in the off hand, the wheel used); rcon then moves them to where a 2.94 world kept them and
// forgets the repair was done; the bot logs in again, and: they're back where they belong, by the item each slot holds - its
// wheel offers Call 8-Bit Leo, 8-Bit Emma, the Sky Buddies and Emma, not Rufus, Henry or Nia; Take the item back gives the Sky
// Buddies' mobile. A set-down golden doll under an old number: re-tagged by the doll it shows; punched, it's that doll.
const { bot, rcon, sleep } = require('./lib_resp');
(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const O = 'execute in minecraft:overworld run ';
  const X = 16600, Y = 100, Z = 16000;

  let A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('time set 1000');
  await run(`${O}forceload add ${X - 8} ${Z - 8} ${X + 8} ${Z + 8}`);
  await run(`${O}fill ${X - 6} ${Y} ${Z - 6} ${X + 6} ${Y} ${Z + 6} minecraft:stone`); await run(`${O}fill ${X - 6} ${Y + 1} ${Z - 6} ${X + 6} ${Y + 5} ${Z + 6} minecraft:air`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 30`); await sleep(1500);
  // (an empty wheel to start)
  const pid = await sc('TestRat', 'bm.pid');
  for (let i = 0; i < 48; i++) await run(`scoreboard players set TestRat bm.pw${i} 0`);
  await run(`data remove storage bm:pw p${pid}`);

  // ---- four partners on the wheel, as a player: the item in the off hand, the wheel used
  await run('loot replace entity TestRat hotbar.0 loot bm:items/partner_wheel'); A.slot(0); await sleep(400);
  const ON = [['emma_ribbon', 0, 'Emma'], ['cart_leo', 45, '8-Bit Leo'], ['cart_emma', 46, '8-Bit Emma'], ['sky_mobile', 47, 'The Sky Buddies']];
  for (const [iid, i, nm] of ON) {
    await run(`loot replace entity TestRat weapon.offhand loot bm:items/${iid}`); await sleep(300); await A.useWait(1500);
    ok(`${nm}'s item in the off hand + the wheel used: on, in slot ${i}`, (await sc('TestRat', `bm.pw${i}`)) === 1 && (await has(iid)) === 0);
  }

  // ---- the stage: where a 2.94-2.95 world kept them (29, 30, 31) - and the repair not yet run
  for (const [from, to] of [[45, 29], [46, 30], [47, 31]]) {
    await run(`scoreboard players set TestRat bm.pw${from} 0`); await run(`scoreboard players set TestRat bm.pw${to} 1`);
    await run(`data modify storage bm:pw p${pid}.k${to} set from storage bm:pw p${pid}.k${from}`); await run(`data remove storage bm:pw p${pid}.k${from}`);
  }
  await run('scoreboard players reset TestRat bm.pwfix');
  A.end(); await sleep(1500);

  // ---- logging back in: the repair
  A = await bot('TestRat'); await sleep(3500); A.stand(); A.slot(0); await sleep(500);
  ok('back in: told the partners are in their own places again', await wait(4000, async () => A.chats.some(c => /back in their own places/.test(c))), A.chats.slice(-2).join(' | '));
  ok('...8-Bit Leo, 8-Bit Emma and the Sky Buddies in their own slots (45, 46, 47), Emma still in hers (0)',
     (await sc('TestRat', 'bm.pw45')) === 1 && (await sc('TestRat', 'bm.pw46')) === 1 && (await sc('TestRat', 'bm.pw47')) === 1 && (await sc('TestRat', 'bm.pw0')) === 1);
  ok('...and Rufus, Henry and Nia not on it (29, 30, 31 empty)', (await sc('TestRat', 'bm.pw29')) === 0 && (await sc('TestRat', 'bm.pw30')) === 0 && (await sc('TestRat', 'bm.pw31')) === 0);
  await A.useWait(1500);
  const labels = A.buttons().map(b => b.label);
  ok('the wheel offers Call Emma, 8-Bit Leo, 8-Bit Emma and the Sky Buddies', ['Emma', '8-Bit Leo', '8-Bit Emma', 'The Sky Buddies'].every(n => labels.some(l => new RegExp(`(Call|Send) ${n}\\b`).test(l))),
     labels.join(' | ').slice(0, 300));
  ok('...and nobody else (no Rufus, Henry or Nia)', !labels.some(l => /Rufus|Henry|Nia\b/.test(l)));
  const bs = A.buttons(); const k = bs.findIndex(b => /Sky Buddies/.test(b.label)); const out = bs.slice(k).find(b => /Take the item back/.test(b.label));
  if (out) A.cmd(out.command.replace(/^\//, '')); await sleep(1200);
  ok('Take the item back (the Sky Buddies): their mobile, in your hands', (await has('sky_mobile')) === 1 && (await sc('TestRat', 'bm.pw47')) === 0);
  await sleep(1500);
  ok('...and the repair runs once (not again on its own)', (await sc('TestRat', 'bm.pwfix')) >= 1 && (await sc('TestRat', 'bm.pw47')) === 0);

  // ---- a golden doll set down under an old number
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.1 loot bm:items/gdoll_sky'); A.slot(1); await sleep(400);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z - 1.5} 0 50`); await sleep(800);
  A.input({ shift: true }); await sleep(300); A.use(); await sleep(400); A.release(); await sleep(300); A.input({}); await sleep(800);
  const dsel = `@e[type=minecraft:item_display,x=${X},y=${Y},z=${Z},distance=..6,nbt={item:{components:{"minecraft:item_model":"bm:gdoll_sky"}}},limit=1]`;
  const tagsOf = async (sel) => (await run(`${O}data get entity ${sel} Tags`));
  const t0 = await tagsOf(dsel); const j = +((t0.match(/bm\.gd(\d+)d/) || [0, -1])[1]);
  ok('the Sky Buddies\' golden doll set down (sneak + use)', j >= 0, t0.slice(0, 160));
  await run(`${O}execute as ${dsel} at @s run tag @s remove bm.gd${j}d`); await run(`${O}execute as ${dsel} at @s run tag @s add bm.gd${j - 1}d`);
  await run(`${O}execute as ${dsel} at @s run tag @e[type=minecraft:interaction,distance=..0.6] remove bm.gd${j}`); await run(`${O}execute as ${dsel} at @s run tag @e[type=minecraft:interaction,distance=..0.6] add bm.gd${j - 1}`);
  await run(`${O}execute as ${dsel} at @s run tag @e[type=minecraft:marker,distance=..0.6] remove bm.gd${j}m`); await run(`${O}execute as ${dsel} at @s run tag @e[type=minecraft:marker,distance=..0.6] add bm.gd${j - 1}m`);
  await run(`${O}execute as ${dsel} run tag @s remove bm.gdok`);
  ok('...under an old number (re-tagged as the doll before it): re-tagged by the doll it shows', await wait(3000, async () => new RegExp(`bm\\.gd${j}d`).test(await tagsOf(dsel)) && !new RegExp(`bm\\.gd${j - 1}d`).test(await tagsOf(dsel))));
  const isel = `@e[type=minecraft:interaction,x=${X},y=${Y},z=${Z},distance=..6,limit=1]`;
  ok('...its click box and marker too', new RegExp(`bm\\.gd${j}"`).test(await tagsOf(isel)) && /passed/.test(await run(`${O}execute if entity @e[type=minecraft:marker,tag=bm.gd${j}m,x=${X},y=${Y},z=${Z},distance=..6]`)));
  const ip = ((await run(`${O}data get entity ${isel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/) || []).slice(1).map(Number);
  const ie = Object.values(A.ents).filter(e => ip.length && Math.abs(e.x - ip[0]) < 0.3 && Math.abs(e.z - ip[2]) < 0.3 && Math.abs(e.y - ip[1]) < 0.3)
    .sort((a, b) => b.entityId - a.entityId)[0];
  await run('clear TestRat');
  if (ie) A.attack(ie.entityId); await sleep(1200);
  ok('...punched: it\'s the Sky Buddies\' doll you get back', (await has('gdoll_sky')) === 1);

  await run('clear TestRat');
  for (let i = 0; i < 48; i++) await run(`scoreboard players set TestRat bm.pw${i} 0`);   // (an empty wheel left behind, for the next test)
  await run(`data remove storage bm:pw p${pid}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();

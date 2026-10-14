// v2.67d: the Ledger's Locker Hall trip - from safe ground in the Overworld, the Nether or the End (not the Hollow or the gutter;
// not mid-fall, mounted or in water; not hurt in the last 10 seconds; not in a boss dungeon), after holding still for 3 seconds.
const { bot, rcon, sleep } = require('./lib');
const res = []; const X = 16600, Y = 100, Z = 16400;
(async () => { const R = await rcon(); const run = c => R.run(c); const A = await bot('TestRat'); await sleep(2500);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); };
  const sc = async o => { const m = (await run(`scoreboard players get TestRat ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : 0; };
  const dim = async () => (await run('data get entity TestRat Dimension')).replace(/.*data: /, '').trim();
  const pos = async () => (await run('data get entity TestRat Pos')).match(/-?[\d.]+(?=d)/g).map(Number);
  const inHall = async () => { await run('execute as TestRat at @s store result score #t106 bm.rng run function bm:p84/lk/inside'); return /has 1 /.test(await run('scoreboard players get #t106 bm.rng')); };
  const ground = on => A.write('flying', { flags: { onGround: on, hasHorizontalCollision: false } });
  const said = re => A.chats.some(c => re.test(c));
  const trip = async () => { A.chats.length = 0; A.bars.length = 0; await run('scoreboard players set TestRat bm.menu 7800'); await run('scoreboard players set TestRat bm.act 7805'); await sleep(500); };
  const plat = async (d, x, y, z) => { await run(`execute in ${d} run forceload add ${x} ${z}`);
    await run(`execute in ${d} run fill ${x - 2} ${y} ${z - 2} ${x + 2} ${y} ${z + 2} minecraft:stone`); await run(`execute in ${d} run fill ${x - 2} ${y + 1} ${z - 2} ${x + 2} ${y + 3} ${z + 2} minecraft:air`); };
  const go = async (d, x, y, z) => { await run(`execute in ${d} run tp TestRat ${x + 0.5} ${y + 1} ${z + 0.5} 0 0`); await sleep(1500); ground(true); await sleep(200); };
  const home = async () => { await go('minecraft:overworld', X, Y, Z); };
  const until = async (f, ms = 6000) => { for (let t = 0; t < ms; t += 250) { if (await f()) return true; await sleep(250); } return !!(await f()); };

  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  for (const t of ['bm.gvp', 'bm.lkch', 'bm.adv', 'bm.exon', 'bm.exask']) await run(`tag TestRat remove ${t}`);
  await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid'); await run('execute as TestRat run function bm:p80/init_me');
  await run('scoreboard players set TestRat bm.lkht 0'); await run('scoreboard players reset TestRat bm.lkdt'); await run('scoreboard players set TestRat bm.gvhc 0');
  await run('loot give TestRat loot bm:items/fixers_ledger');
  await plat('minecraft:overworld', X, Y, Z); await home();

  // ---- the Office still opens anywhere (here: the Nether)
  await plat('minecraft:the_nether', 2000, 110, 2000); await go('minecraft:the_nether', 2000, 110, 2000);
  await run('scoreboard players set TestRat bm.menu 0'); await run('scoreboard players set TestRat bm.gvhc 0'); await run('execute as TestRat at @s run function bm:p80/ledger');
  ok('The Ledger\'s Office still opens in the Nether', (await sc('bm.menu')) === 7800, `menu ${await sc('bm.menu')}`);
  // ---- the trip works from safe ground in the Nether and the End too - and brings you back there
  for (const [d, x, y, z, nm] of [['minecraft:the_nether', 2000, 110, 2000, 'the Nether'], ['minecraft:the_end', 1500, 100, 1500, 'the End']]) {
    await plat(d, x, y, z); await go(d, x, y, z); const q0 = await pos(); await trip();
    ok(`From the ground in ${nm}: the hold starts`, said(/Hold still for 3 seconds/), A.chats.slice(-1).join(''));
    ok('...and three seconds later, the Locker Hall', await until(inHall, 4500), await dim());
    if (nm === 'the Nether') { await trip(); ok('From inside the Locker Hall: no ("in the gutter already")', said(/in the gutter already/) && !/"bm\.lkch"/.test(await run('data get entity TestRat Tags'))); }
    await run('execute as TestRat at @s run function bm:p84/lk/back'); await sleep(1500); const q1 = await pos();
    ok(`...and back to the same spot in ${nm}`, (await dim()).includes(d.split(':')[1]) && Math.abs(q1[0] - q0[0]) < 0.3 && Math.abs(q1[1] - q0[1]) < 0.3 && Math.abs(q1[2] - q0[2]) < 0.3, `${q0} -> ${q1}`);
  }
  await plat('bm:hollow_throne', 3000, 150, 3000); await go('bm:hollow_throne', 3000, 150, 3000); await trip();
  ok('Not from the Hollow (and it says why)', /hollow_throne/.test(await dim()) && said(/boss dungeon or the Hollow/) && !(await inHall()), A.chats.slice(-1).join(''));
  await run('tag TestRat remove bm.adv'); await home(); await run('gamemode survival TestRat');

  // ---- not a safe spot to come back to
  await run(`tp TestRat ${X + 0.5} ${Y + 25} ${Z + 0.5}`); await sleep(600); ground(false); await sleep(200); await trip();
  ok('Not mid-fall or mid-flight ("find your feet")', said(/Find your feet/) && !(await inHall()), A.chats.slice(-1).join(''));
  await home(); await run(`setblock ${X + 1} ${Y + 1} ${Z} minecraft:water`); await run(`tp TestRat ${X + 1.5} ${Y + 1} ${Z + 0.5}`); await sleep(600); ground(true); await sleep(200); await trip();
  ok('Not standing in water', said(/out of the water/) && !(await inHall()), A.chats.slice(-1).join(''));
  await run(`setblock ${X + 1} ${Y + 1} ${Z} minecraft:air`); await home();
  await run(`summon minecraft:oak_boat ${X - 1.5} ${Y + 1} ${Z + 0.5} {Tags:["bm.t106"]}`); await run('ride TestRat mount @e[type=minecraft:oak_boat,tag=bm.t106,limit=1]'); await sleep(500); await trip();
  ok('Not mounted (here: in a boat)', said(/off your mount/) && !(await inHall()), A.chats.slice(-1).join(''));
  await run('ride TestRat dismount'); await run('kill @e[tag=bm.t106]'); await home();
  await run('tag TestRat add bm.adv'); await trip(); await run('tag TestRat remove bm.adv'); await run('gamemode survival TestRat');
  ok('Not from inside a boss dungeon', said(/inside a boss dungeon/) && !(await inHall()), A.chats.slice(-1).join(''));
  ok('...the boss-dungeon check loads (structure tag + predicate)', /failed/.test(await run(`execute positioned ${X} ${Y + 1} ${Z} if predicate bm:p103/boss_dungeon`)),
     await run(`execute positioned ${X} ${Y + 1} ${Z} if predicate bm:p103/boss_dungeon`));
  // a real boss dungeon, if one has generated near enough to find
  const loc = await run('locate structure bm:p2_brood');
  const lm = loc.match(/at \[(-?\d+), (~|-?\d+), (-?\d+)\]/);
  if (lm) { const lx = +lm[1], lz = +lm[3];
    await run(`forceload add ${lx} ${lz}`); await run(`tp TestRat ${lx + 0.5} 200 ${lz + 0.5}`); await sleep(4000);
    let fy = null; for (let y = 190; y >= -50 && fy === null; y -= 2) if (/passed/.test(await run(`execute positioned ${lx} ${y} ${lz} if predicate bm:p103/boss_dungeon`))) fy = y;
    if (fy !== null) { await run(`tp TestRat ${lx + 0.5} ${fy} ${lz + 0.5}`); await sleep(500); ground(true); await sleep(200); await trip();
      ok('...and inside a real one (the Brood\'s), it says so', said(/inside a boss dungeon/) && !(await inHall()), `at ${lx} ${fy} ${lz}: ` + A.chats.slice(-1).join('')); }
    else console.log('SKIP  (no Brood piece found under the located start)');
    await run('tag TestRat remove bm.adv'); await run('gamemode survival TestRat'); await run(`forceload remove ${lx} ${lz}`); await home();
  } else console.log('SKIP  (no Brood dungeon located: ' + loc.slice(0, 80) + ')');

  // ---- hurt in the last 10 seconds
  await home(); await run('damage TestRat 2 minecraft:generic'); await sleep(400); await trip();
  ok('Not right after getting hurt ("wait N more seconds")', said(/hurt just now - wait/) && !(await inHall()) && (await sc('bm.lkht')) >= 8, `${A.chats.slice(-1).join('')} ht ${await sc('bm.lkht')}`);
  ok('...the 10 seconds run out', await until(async () => (await sc('bm.lkht')) === 0, 12000), `ht ${await sc('bm.lkht')}`);
  await run('effect give TestRat minecraft:instant_health 1 1 true'); await sleep(300);

  // ---- the hold: 3 seconds still, then in; back where you stood
  await home(); const p0 = await pos(); await trip();
  ok('From solid Overworld ground: "hold still for 3 seconds"', said(/Hold still for 3 seconds/) && /"bm\.lkch"/.test(await run('data get entity TestRat Tags')) &&
     A.bars.some(b => /Opening the Locker Hall/.test(b)) && !(await inHall()), A.chats.slice(-1).join(''));
  await sleep(1300); ok('...not yet after one second', !(await inHall()) && /overworld/.test(await dim()));
  ok('...a countdown on the action bar', A.bars.some(b => /Opening the Locker Hall\.\.\. 2/.test(b)), A.bars.slice(-3).join(' | '));
  ok('...and after three: the Locker Hall', await until(inHall, 3000), await dim());
  ok('...the hold is over (no tag, no timer)', !/"bm\.lkch"/.test(await run('data get entity TestRat Tags')));
  await run('execute as TestRat at @s run function bm:p84/lk/back'); await sleep(1500);
  const p1 = await pos();
  ok('Out again: back exactly where you stood', /overworld/.test(await dim()) && Math.abs(p1[0] - p0[0]) < 0.3 && Math.abs(p1[1] - p0[1]) < 0.3 && Math.abs(p1[2] - p0[2]) < 0.3,
     `${p0} -> ${p1}`);

  // ---- moving cancels; turning doesn't
  await home(); await trip(); await sleep(800); await run(`tp TestRat ${X + 2.5} ${Y + 1} ${Z + 0.5}`); await sleep(400);
  ok('Moving cancels it (and says so)', said(/You moved/) && !/"bm\.lkch"/.test(await run('data get entity TestRat Tags')), A.chats.slice(-1).join(''));
  await sleep(2800); ok('...no Locker Hall', !(await inHall()) && /overworld/.test(await dim()));
  await plat('minecraft:the_nether', X, Y, Z); await home(); await trip(); await sleep(600); await run(`execute in minecraft:the_nether run tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(600);
  ok('Changing dimension cancels it too', said(/You moved/) && !/"bm\.lkch"/.test(await run('data get entity TestRat Tags')), A.chats.slice(-1).join(''));
  await home(); await trip(); await sleep(600); await run('execute as TestRat at @s run tp @s ~ ~ ~ 135 20'); await sleep(200); await run('execute as TestRat at @s run tp @s ~ ~ ~ -60 -10');
  ok('Looking around doesn\'t: still in', await until(inHall, 4000) && !said(/You moved/), A.chats.slice(-1).join(''));
  await run('execute as TestRat at @s run function bm:p84/lk/back'); await sleep(1500);

  // ---- getting hurt cancels, and starts the 10 seconds
  await home(); await trip(); await sleep(800); await run('damage TestRat 1 minecraft:generic'); await sleep(500);
  ok('Getting hurt cancels it (and says so)', said(/You were hurt, so the Locker Hall stays shut/) && !/"bm\.lkch"/.test(await run('data get entity TestRat Tags')), A.chats.slice(-1).join(''));
  await sleep(2600); ok('...no Locker Hall', !(await inHall()));
  await trip(); ok('...and trying again at once: "wait N more seconds"', said(/hurt just now - wait/) && !(await inHall()));

  // ---- a raider in a heist still gets the den's copper door
  await run('scoreboard players set TestRat bm.lkht 0'); A.chats.length = 0;
  await run('tag TestRat add bm.gvp'); await run('execute as TestRat run function bm:p84/lk/from_ledger'); await run('tag TestRat remove bm.gvp'); await sleep(300);
  ok('In a heist, the Ledger still points at the den\'s copper door', said(/copper door in the den/) && !/"bm\.lkch"/.test(await run('data get entity TestRat Tags')), A.chats.slice(-1).join(''));

  for (const d of [['minecraft:the_nether', X, Z], ['minecraft:the_nether', 2000, 2000], ['minecraft:the_end', 1500, 1500], ['bm:hollow_throne', 3000, 3000], ['minecraft:overworld', X, Z]]) await run(`execute in ${d[0]} run forceload remove ${d[1]} ${d[2]}`);
  await run('clear TestRat'); await run('effect give TestRat minecraft:instant_health 1 1 true');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`); process.exit(0);
})();

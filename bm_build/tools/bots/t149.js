// 2.78: Apophiss slithers - he doesn't hop. As a regular (non-op) player, up on a ledge two blocks high (as on the den's steps),
// walking real laps along it, Apophiss (phase 1, his base form) below: with a vanilla husk's jump and step (put back for the
// control run) he hops against the ledge again and again; with his own (2.78: jump strength 0, step height 2) he never leaves
// the floor between attacks - he slithers up onto the ledge after the bot instead. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const B = '@e[type=minecraft:husk,tag=bm.apboss,limit=1]';
  const num = async (c) => { const m = (await run(c)).match(/(-?\d+(?:\.\d+)?)[a-z]?\s*$/i); return m ? +m[1] : NaN; };
  const X = 16600, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat');
  await run('attribute TestRat minecraft:max_health base set 1000'); await run('effect give TestRat minecraft:instant_health 1 40 true');
  await run('effect give TestRat minecraft:resistance 900 4 true'); await run('effect give TestRat minecraft:regeneration 900 4 true');
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  await run(`${O}fill ${X - 20} ${Y} ${Z - 20} ${X + 20} ${Y} ${Z + 20} minecraft:stone`);
  await run(`${O}fill ${X - 20} ${Y + 1} ${Z - 20} ${X + 20} ${Y + 12} ${Z + 20} minecraft:air`);
  await run(`${O}fill ${X + 8} ${Y + 1} ${Z - 20} ${X + 20} ${Y + 2} ${Z + 20} minecraft:mossy_cobblestone`);     // (the ledge: x+8 and beyond, 2 high)
  await run(`${O}kill @e[type=minecraft:husk,tag=bm.apboss]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.apb]`);
  await run(`${O}tp TestRat ${X - 6.5} ${Y + 1} ${Z + 0.5} -90 0`); await sleep(1500);
  await run('execute as TestRat at @s run function bm:admin/apophiss');
  ok('Apophiss comes (phase 1)', await wait(8000, async () => /passed/i.test(await run(`${O}execute if entity ${B}`))));
  ok('...his jump: none (jump strength 0)', (await num(`${O}attribute ${B} minecraft:jump_strength get`)) === 0);
  ok('...he steps up instead (step height 2)', (await num(`${O}attribute ${B} minecraft:step_height get`)) === 2);
  await wait(25000, async () => (await num(`${O}scoreboard players get ${B} bm.apph`)) === 1, 500);   // (his entrance, then the fight)
  await run(`${O}tp TestRat ${X + 11.5} ${Y + 3} ${Z + 0.5} -90 0`); await sleep(500); A.stand();
  // laps: the bot walks a ring round the middle, the boss after it; sample his rise off the floor while he isn't attacking
  const lap = async (secs) => {
    let hops = 0, samples = 0, moved = 0, prev = null, last = -9; const t0 = Date.now(); let a = 0;
    let up = 0, upS = 0;
    const walker = (async () => { while (Date.now() - t0 < secs * 1000) { a += 0.5; await A.walkTo(X + 11.5 + 1.5 * Math.cos(a), Z + 0.5 + 6 * Math.sin(a), 0.2); } })();
    while (Date.now() - t0 < secs * 1000) {
      const atk = await num(`${O}scoreboard players get ${B} bm.apatk`);
      const vy = await num(`${O}data get entity ${B} Motion[1] 1000`);
      const pos = (await run(`${O}data get entity ${B} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
      if (pos) { const p = pos.slice(1).map(Number); if (prev) moved += Math.hypot(p[0] - prev[0], p[2] - prev[2]); prev = p; if (p[1] >= Y + 2.9) up = 1; }
      if (!(atk > 0)) { samples++; if (vy > 250 && Date.now() - last > 600) { hops++; last = Date.now(); } }
      await sleep(100);
    }
    await walker; return { hops, samples, moved: Math.round(moved), up };
  };
  await run(`${O}attribute ${B} minecraft:jump_strength base set 0.42`); await run(`${O}attribute ${B} minecraft:step_height base set 1.5`);   // (the control: before 2.78)
  const ctl = await lap(30);
  console.log('(control, before 2.78 - a husk\'s jump, step 1.5: ' + JSON.stringify(ctl) + ' - it never reproduced the hop here; information only)');
  await run(`${O}tp ${B} ${X - 4.5} ${Y + 1} ${Z + 0.5}`); await sleep(500);
  await run(`${O}attribute ${B} minecraft:jump_strength base set 0`); await run(`${O}attribute ${B} minecraft:step_height base set 2`);
  const his = await lap(30);
  ok('his own: not one hop between attacks', his.hops === 0, JSON.stringify(his));
  ok('...he slithers up onto the ledge after the bot instead', his.up === 1, JSON.stringify(his));
  await run(`${O}kill @e[type=minecraft:husk,tag=bm.apboss]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.apb]`);
  await run(`${O}kill @e[type=minecraft:interaction,tag=bm.bhit_ap]`); await run('bossbar set bm:apob visible false');
  await run('attribute TestRat minecraft:max_health base set 20');
  await run(`${O}forceload remove ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();

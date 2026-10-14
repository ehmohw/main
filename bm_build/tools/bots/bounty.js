// Bounty Board play-test: a market marker in the arena gets the board from the p35 patch; a bot signs it during a
// (forced) Blood Moon / Invasion / Lucky Night, kills tagged monsters with its fists and collects the reward.
const { bot, rcon, sleep } = require('./lib');
const X = 5000, Y = 100, Z = 5000;
(async () => {
  const R = await rcon(); const run = (c) => R.run(c);
  const A = await bot('TestRat'); await sleep(800);
  const results = []; const ok = (n, p, d) => { results.push(p); console.log((p ? 'PASS ' : 'FAIL ') + n + '  -- ' + d); };
  const items = async (pred) => { const s = await run(`clear TestRat ${pred} 0`); const m = s.match(/Found (\d+)/); return m ? +m[1] : 0; };
  await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance infinite 4 true');
  await run('scoreboard players set TestRat bm.bnt 0'); await run('scoreboard players reset TestRat bm.bntn');
  // a market marker facing south (yaw 0) at the arena; the patch places the lectern and the board relative to it
  await run('kill @e[type=minecraft:marker,tag=bm.mkt]'); await run('kill @e[tag=bm.bboard]'); await run('kill @e[tag=bm.bbhit]');
  await run(`summon minecraft:marker ${X + 0.5} ${Y - 6} ${Z - 30.5} {Tags:["bm.mkt","t_mkt"],Rotation:[0f,0f]}`);
  const board = await run(`execute as @e[type=minecraft:marker,tag=t_mkt] at @s rotated as @s run function bm:p35/patch`);
  await sleep(300);
  const bp = await run('data get entity @e[type=minecraft:interaction,tag=bm.bbhit,limit=1] Pos');
  const m = bp.match(/\[(.*)\]/); const [bx, by, bz] = m ? m[1].split(',').map(parseFloat) : [0, 0, 0];
  ok('board placed by the market patch', !!m, `board at ${[bx, by, bz].map(v => v.toFixed(1))}`);
  await run(`fill ${Math.floor(bx) - 3} ${Math.floor(by) - 1} ${Math.floor(bz) - 3} ${Math.floor(bx) + 3} ${Math.floor(by) - 1} ${Math.floor(bz) + 3} minecraft:stone`);
  await run(`tp TestRat ${bx} ${by} ${bz - 2} 0 10`); await sleep(1200);
  let hit;
  for (let tries = 0; tries < 8 && !hit; tries++) {
    const floor = Math.max(0, ...Object.keys(A.ents).map(Number));
    await run('kill @e[tag=bm.bbhit]'); await run(`execute as @e[type=minecraft:marker,tag=t_mkt] at @s rotated as @s run function bm:p35/patch`);   // a fresh spawn packet
    for (let i = 0; i < 8 && !hit; i++) { await sleep(250); hit = Object.values(A.ents).filter(e => e.entityId > floor && e.type === 70 && Math.abs(e.x - bx) < 0.6 && Math.abs(e.z - bz) < 0.6)[0]; }
  }
  if (!hit) { console.log('board click box never seen'); process.exit(1); }
  const textOf = async () => (await run('data get entity @e[type=minecraft:text_display,tag=bm.bboard,limit=1] text')).slice(40, 160);

  // no special night: the board says so and refuses
  await run('time set 1000'); await sleep(2500);
  A.bars = []; A.interact(hit.entityId); await sleep(500);
  ok('no bounty on an ordinary night', (await run('scoreboard players get TestRat bm.bnt')).includes('has 0'), `board: ${await textOf()} / "${A.bars.slice(-1)[0]}"`);

  const calm = async () => { await run('scoreboard players set #forced bm.bm 0'); await run('function bm:admin/invasion_stop'); await run('scoreboard players set #lucky bm.bm 0');
                             await run('time set 1000'); await sleep(2500); };
  const start = { 1: async () => { await run('scoreboard players set #forced bm.bm 1'); await run('time set 15000'); },
                  3: async () => { await run('time set 14000'); await run('function bm:admin/invasion_now'); await run('time set 15000'); },
                  2: async () => { await run('time set 14000'); await run('function bm:admin/lucky_night'); await run('time set 15000'); } };
  for (const [st, flag, tag, n, prize, label] of [[1, '#active', 'bm.blood', 8, 'blood_crystal', 'Blood Moon'], [3, '#inv', 'bm.vorn', 8, 'xenite_green', 'Invasion'],
                                                   [2, '#lnight', 'bm.lucky', 6, 'lucky_token', 'Lucky Night']]) {
    await calm(); await start[st](); await sleep(3500);
    console.log('   ', label, 'flag', await run(`scoreboard players get ${flag} bm.bm`), '#bstate', await run('scoreboard players get #bstate bm.rng'));
    const txt = await textOf();
    A.bars = []; A.interact(hit.entityId); await sleep(500);
    const signed = (await run('scoreboard players get TestRat bm.bnt')).includes(`has ${st}`);
    A.interact(hit.entityId); await sleep(300); const again = A.bars.slice(-1)[0] || '';
    const before = await items(`*[minecraft:custom_data~{bm:"${prize}"}]`);
    for (let i = 0; i < n; i++) {
      await run(`summon minecraft:zombie ${bx} ${by} ${bz - 1} {Tags:["${tag}","bm.seen","t_bnt"],NoAI:1b,Health:0.5f,PersistenceRequired:1b,Silent:1b}`); await sleep(250);
      await run('damage @e[tag=t_bnt,limit=1,sort=nearest] 20 minecraft:player_attack by TestRat'); await sleep(250);
    }
    await sleep(500);
    const after = await items(`*[minecraft:custom_data~{bm:"${prize}"}]`);
    ok(`${label} bounty: sign, ${n} kills, reward`, signed && after > before, `board "${txt.replace(/\\n/g, ' ').slice(0, 70)}..."; signed ${signed}; second sign: "${again}"; ${prize} ${before} -> ${after}`);
    await run('kill @e[tag=t_bnt]');
  }
  // dawn: the board resets
  await calm(); await run('kill @e[type=!minecraft:player,x=5000,y=100,z=5000,distance=..120,tag=bm.tiered]');
  ok('board resets at dawn', (await textOf()).includes('No bounties'), await textOf());
  await run('kill @e[tag=t_mkt]'); await run('kill @e[tag=bm.bboard]'); await run('kill @e[tag=bm.bbhit]'); await run('kill @e[tag=bm.newcomer]');
  console.log(`\n${results.filter(x => x).length}/${results.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });

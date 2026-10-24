// 2.94j: BONES UNDERWATER, as a regular (non-op) player - he used to bob at the surface and turn circles there (the wolf under
// him can't path through water). His whistle used (a real use) beside a deep pool; the bot down at the bottom, 9 deep (rcon sets
// the stage: the pool, the bot under the water, Bones on its surface 8 blocks off): he swims down to it - within 3 blocks, well
// under the surface - and faces it as he comes, no spinning. Then ridden (his menu -> Ride): looking down, forward held - he
// dives (his rider's look, pitch too), not stuck on the surface.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const num = async (sel, path) => +(((await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?entity data: /, '').match(/(-?[\d.]+)/) || [0, NaN])[1]);
  const X = 18400, Y = 60, Z = 16000, TOP = Y + 12;            // (the pool: Y+1 .. TOP, water)
  const PET = '@e[type=minecraft:wolf,tag=bm.bjpet,limit=1]';
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true');
  await run('effect give TestRat minecraft:water_breathing 600 0 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await sleep(2500);
  await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${TOP + 4} ${Z + 12} minecraft:stone`);
  await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${TOP} ${Z + 10} minecraft:water`);
  await run(`${O}fill ${X - 12} ${TOP + 1} ${Z - 12} ${X + 12} ${TOP + 4} ${Z + 12} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y + 6},z=${Z},distance=..24]`); await run(`kill ${PET.slice(0, -9)}]`); await sleep(1500);
  await run('scoreboard players set TestRat bm.bjcd 0'); await run('tag TestRat add bm.bjmet');
  await run(`${O}tp TestRat ${X + 11.5} ${TOP + 1} ${Z + 0.5} -90 0`); await sleep(1500); A.stand();
  await run('loot replace entity TestRat hotbar.0 loot bm:items/bn_whistle'); await sleep(400);
  await use(0);
  ok('his whistle used: Bones comes', await wait(5000, async () => (await cnt(PET)) === 1));
  await sleep(2500);

  // ---- following, underwater
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 3} ${Z + 0.5} -90 0`); await run(`${O}tp ${PET} ${X - 7.5} ${TOP} ${Z + 0.5}`); await sleep(300);
  const yaws = [];
  const close = await wait(9000, async () => { yaws.push(await num(PET, 'Rotation[0]'));
    const dx = (await num(PET, 'Pos[0]')) - X - 0.5, dy = (await num(PET, 'Pos[1]')) - Y - 3, dz = (await num(PET, 'Pos[2]')) - Z - 0.5;
    return Math.hypot(dx, dy, dz) < 3; }, 300);
  ok('the bot 9 deep, Bones on the surface 8 off: he swims down to it (within 3)', close, `him ${await run(`${O}data get entity ${PET} Pos`)}`);
  ok('...well under the surface', (await num(PET, 'Pos[1]')) < TOP - 4, `y ${await num(PET, 'Pos[1]')}`);
  await sleep(2000);
  const ys = []; for (let i = 0; i < 8; i++) { ys.push(await num(PET, 'Rotation[0]')); await sleep(250); }
  const spread = Math.max(...ys.map(a => Math.abs((((a - ys[0]) % 360) + 540) % 360 - 180)));
  ok('...and stays by it, facing it - not turning circles', spread < 40 && (await num(PET, 'Pos[1]')) < TOP - 4, `yaw spread ${spread.toFixed(0)} (${ys.map(a => a.toFixed(0)).join(',')}) y ${await num(PET, 'Pos[1]')}`);

  // ---- ridden: a dive
  await run(`${O}tp TestRat ${X + 0.5} ${TOP} ${Z + 0.5} 0 0`); await run(`${O}tp ${PET} ${X + 0.5} ${TOP} ${Z + 1.5} 0 0`); await sleep(1500);
  const n0 = A.dialogN.length; await use(0, true); await wait(3000, async () => A.dialogN.length > n0);
  const pr = await A.press(/^Ride/);
  const riding = async () => /bjpet/.test(await run('execute as TestRat on vehicle run tag @s list'));
  ok('his menu -> Ride: on his back', !!pr && await wait(3000, riding));
  A.ride(0, 0, {}); await sleep(600);
  const y0 = await num(PET, 'Pos[1]');
  A.ride(0, 60, { forward: true }); await sleep(1500); A.ride(0, 60, {}); await sleep(300);
  const y1 = await num(PET, 'Pos[1]');
  ok('...looking down, forward held: he dives (not stuck on the surface)', y0 - y1 > 2.5, `y ${y0.toFixed(1)} -> ${y1.toFixed(1)}`);
  A.input({ shift: true }); await sleep(600); A.input({}); await sleep(400);

  // ---- clean up
  await run(`kill ${PET.slice(0, -9)}]`); await run('clear TestRat'); await run(`${O}fill ${X - 12} ${Y} ${Z - 12} ${X + 12} ${TOP + 4} ${Z + 12} minecraft:air`);
  const n = res.filter(Boolean).length; console.log(`${n}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

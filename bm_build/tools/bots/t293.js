// 2.96: ADVENTURE ACROSS THE GUTTER, as a regular (non-op) player - the heists' dimension (its den, the lobbies before BEGIN, a
// crewmate left waiting) is adventure for everyone, not only a heist's crew: a survival player who comes into the Gutter (rcon: the
// stage - a stone floor somewhere in it, and the trip there) is put in adventure within a second, and can't dig the stone (a real
// dig); back in the Overworld, survival again - and digging works there.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const mode = async () => (await run('data get entity TestRat playerGameType')).match(/(-?\d+)$/)?.[1];
  const block = async (dim, x, y, z) => /passed/i.test(await run(`execute in ${dim} if block ${x} ${y} ${z} minecraft:stone`));
  const GX = -315, GY = 67, GZ = -244,   // (the den: off a heist, the one place in the Gutter a player can stand - p70/belong sends anyone else home)
        OX = 18400, OY = 100, OZ = 16400;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('tag TestRat remove bm.gvp'); await run('tag TestRat remove bm.gvadv'); await run('clear TestRat');
  await run('item replace entity TestRat hotbar.0 with minecraft:diamond_pickaxe'); A.slot(0);
  await run(`execute in bm:gutter run clone ${GX + 1} ${GY + 1} ${GZ} ${GX + 1} ${GY + 1} ${GZ} ${GX + 1} 250 ${GZ}`);   // (what was there, kept)
  await run(`execute in bm:gutter run setblock ${GX + 1} ${GY + 1} ${GZ} minecraft:stone`);
  await run(`execute in bm:gutter run tp TestRat ${GX - 0.5} ${GY + 1} ${GZ + 0.5} -90 30`); await sleep(500);
  ok('in the Gutter (the den, not on any heist): adventure within a second or two', await wait(3000, async () => (await mode()) === '2'), `mode ${await mode()}`);
  await A.mine(GX + 1, GY + 1, GZ, 1500);
  ok('...and the stone can\'t be dug', await block('bm:gutter', GX + 1, GY + 1, GZ));
  await run(`execute in minecraft:overworld run forceload add ${OX - 8} ${OZ - 8} ${OX + 8} ${OZ + 8}`);
  await run(`execute in minecraft:overworld run fill ${OX - 4} ${OY} ${OZ - 4} ${OX + 4} ${OY} ${OZ + 4} minecraft:stone`);
  await run(`execute in minecraft:overworld run fill ${OX - 4} ${OY + 1} ${OZ - 4} ${OX + 4} ${OY + 4} ${OZ + 4} minecraft:air`);
  await run(`execute in minecraft:overworld run setblock ${OX + 1} ${OY + 1} ${OZ} minecraft:stone`);
  await run(`execute in minecraft:overworld run tp TestRat ${OX + 0.5} ${OY + 1} ${OZ + 0.5} -90 30`); await sleep(500);
  ok('back in the Overworld: survival again', await wait(3000, async () => (await mode()) === '0'), `mode ${await mode()}`);
  await A.mine(OX + 1, OY + 1, OZ, 1500);
  ok('...and digging works there', await wait(2000, async () => !(await block('minecraft:overworld', OX + 1, OY + 1, OZ))));
  await run('clear TestRat');
  await run(`execute in bm:gutter run clone ${GX + 1} 250 ${GZ} ${GX + 1} 250 ${GZ} ${GX + 1} ${GY + 1} ${GZ}`);
  await run(`execute in bm:gutter run setblock ${GX + 1} 250 ${GZ} minecraft:air`);
  await run(`execute in minecraft:overworld run forceload remove ${OX - 8} ${OZ - 8} ${OX + 8} ${OZ + 8}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

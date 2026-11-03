// 3.0g: PROTECTED GROUND, FOR EVERYONE (guard.py), in t162's market (placed if a last run hasn't). As a regular (non-op) player,
// then as an operator (the owner's report: "spammed on my hotbar that blocks can't be broken. Yet I can break blocks in every
// protected area. Could it be because I'm OP?"). rcon sets the stage - and plays the thing that keeps turning a player back
// to Survival (another place's way out, a server plugin, an op's own /gamemode survival); the bot stands and digs with real
// dig packets.
//   - on a shop's floor: Adventure, and "Protected ground" said once, not again;
//   - flipped back to Survival again and again while it digs the floor: the block stays (the lock: no breaking speed, and
//     Adventure asked for again), "Protected ground" still said only once; then Adventure, the lock gone;
//   - an operator in Survival there: the same - Adventure, and the floor won't break; in Creative (by design): never locked,
//     the block breaks;
//   - out of the market: Survival, no lock left.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const gm = async () => ((await run('data get entity TestRat playerGameType')).match(/: (\d+)/) || [0, -1])[1];
  const locked = async () => /-1/.test(await run('attribute TestRat minecraft:block_break_speed modifier value get bm:guard_nobreak'));
  const CX = 24000, CY = 30, CZ = 24000, W = 10;
  const SX = CX + 31, SY = CY + W, SZ = CZ + 21;                 // (a shop's floor: Barnaby's - t201)
  const FLOOR = [SX, SY - 1, SZ];
  const solid = async () => !/passed/.test(await run(`${O}execute if block ${FLOOR.join(' ')} minecraft:air`));
  const prot = () => A.bars.filter(b => /Protected ground/.test(b)).length;
  let opped = false;

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  try {
    A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
    ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
    await run('gamemode survival TestRat'); await run('effect clear TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await run(`${O}forceload add ${CX} ${CZ} ${CX + 76} ${CZ + 96}`);
    const MK = `@e[type=minecraft:marker,tag=bm.mkt,x=${CX + 38.5},y=${CY + 12},z=${CZ + 46.5},distance=..2,limit=1]`;
    await sleep(2500);
    if (!(await cnt(MK))) { let pl = ''; for (let i = 0; i < 30; i++) { pl = await run(`${O}place template bm:black_market ${CX} ${CY} ${CZ}`); if (!/not loaded/.test(pl)) break; await sleep(2000); } console.log('   placed: ' + pl.slice(0, 60)); }
    await run('loot replace entity TestRat hotbar.8 loot bm:items/market_key');
    await run('item replace entity TestRat hotbar.0 with minecraft:netherite_pickaxe[minecraft:enchantments={"minecraft:efficiency":5}]'); A.slot(0);
    const enter = async () => {
      await run(`${O}tp TestRat ${CX + 38.5} ${CY + 60} ${CZ - 60}`); await sleep(2500);        // (out of it first)
      await run('scoreboard players reset TestRat bm.gdmsg');
      A.bars.length = 0; await run(`${O}tp TestRat ${SX + 0.5} ${SY} ${SZ + 0.5} 0 60`); await sleep(1200); A.stand();
      return wait(4000, async () => (await gm()) === '2', 250);
    };
    const flipDig = async () => {            // (dig the floor with real packets while something keeps turning TestRat back to Survival)
      let sawLock = false, dig = null;
      const t0 = Date.now();
      while (Date.now() - t0 < 3400) {
        await run('gamemode survival TestRat'); await sleep(120); if (!sawLock && await locked()) sawLock = true;
        if (!dig && Date.now() - t0 > 400) dig = A.mine(FLOOR[0], FLOOR[1], FLOOR[2], 2600);      // (it digs once the flipping has begun)
      }
      await dig; await sleep(300);
      return sawLock;
    };

    // ---- a regular player on a shop's floor
    ok('on a shop\'s floor: Adventure mode', await enter());
    await sleep(8000);
    ok('..."Protected ground" said once in ten seconds, not again and again', prot() === 1, `${prot()} times`);
    const lk = await flipDig();
    ok('turned back to Survival again and again while digging the floor: the floor is still there', await solid());
    ok('...locked meanwhile (no breaking speed: bm:guard_nobreak)', lk);
    ok('..."Protected ground" still said only once (no spam)', prot() === 1, `${prot()} times`);
    ok('...left alone: Adventure again, the lock gone', await wait(2000, async () => (await gm()) === '2' && !(await locked()), 200));

    // ---- an operator
    await run('op TestRat'); opped = true; await sleep(500);
    ok('an operator, on the shop\'s floor: Adventure mode', await enter());
    await run('gamemode survival TestRat');           // (as an op would do for themselves)
    ok('...an operator who sets himself to Survival there: Adventure again within a moment', await wait(2000, async () => (await gm()) === '2', 100));
    await A.mine(FLOOR[0], FLOOR[1], FLOOR[2], 2500); await sleep(300);
    ok('...and the floor won\'t break for him', await solid());
    await flipDig();
    ok('...nor while something keeps turning him back to Survival', await solid());
    const STASH = [CX + 38, CY + 59, CZ - 60];
    await run(`${O}clone ${FLOOR.join(' ')} ${FLOOR.join(' ')} ${STASH.join(' ')}`);           // (the floor's block kept aside, to put back)
    await run('gamemode creative TestRat'); await sleep(800);
    ok('...in Creative (by design): never locked', await wait(1500, async () => !(await locked()), 200) && (await gm()) === '1');
    const before = await solid();
    await A.mine(FLOOR[0], FLOOR[1], FLOOR[2], 300); await sleep(500);
    ok('...and he can break the floor', before && !(await solid()));
    await run(`${O}clone ${STASH.join(' ')} ${STASH.join(' ')} ${FLOOR.join(' ')}`); await run(`${O}setblock ${STASH.join(' ')} minecraft:air`);
  } finally {
    if (opped) await run('deop TestRat');
    await run('gamemode survival TestRat');
  }
  await run(`${O}tp TestRat ${CX + 38.5} ${CY + 60} ${CZ - 60}`); await sleep(3000);
  ok('out of the market: Survival, no lock left', await wait(4000, async () => (await gm()) === '0' && !(await locked()), 250));

  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

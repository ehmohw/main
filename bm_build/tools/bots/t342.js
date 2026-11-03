// 3.0g: THE ARACHNO-LANTERN WAITS OUT ITS BLOOD MOON (phase82, phase125's dormant clock, gen_dp's far sweep) as a regular (non-op)
// player. rcon sets the stage - a Blood Moon (called by #forced, as an effigy does), a flat open field far out with its chunks held,
// a monster at its centre, TestRat 150 blocks off - and the monster rises as the Lantern the way a natural spawn does (the Blood Moon
// roll's own p82/spawn, run as that monster). The bot is the one player online, far away.
//   rise     the monster rolled into the Lantern: the giant stands on the field (not in the void), its rig whole, and the monster it
//            rose from is gone
//   wait     TestRat 150 blocks off for 3 minutes and more: the Lantern is still there the whole time (sampled every 5 s - the far
//            sweep at 160, the two lonely minutes, its dormant clock at 96 all used to take it), still on the field, still whole
//   dawn     the Blood Moon ends: it gutters out (gone within seconds, no part left)
//   gourd    one grown from a Smouldering Gourd (bm.called) is still sent off when left 160+ blocks alone
//   node t342.js [gourd]       (no argument: all four, in order)
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const O = 'execute in minecraft:overworld run ';
const X = 18900, Y = 100, Z = 16500, FAR = 150;

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (sel) => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const at = async (x, y, z) => { await run(`${O}tp TestRat ${x} ${y} ${z}`); await wait(4000, async () => A.pos && Math.abs(A.pos.x - x) < 0.2 && Math.abs(A.pos.z - z) < 0.2, 100); await sleep(400); };
  const LAN = `@e[type=minecraft:giant,tag=bm.salboss,x=${X},y=${Y},z=${Z},distance=..64]`;
  const parts = () => cnt(`@e[type=minecraft:item_display,tag=bm.salp,x=${X},y=${Y},z=${Z},distance=..64]`);
  const field = async (cx, cz, r) => { await run(`${O}forceload add ${cx - r - 16} ${cz - r - 16} ${cx + r + 16} ${cz + r + 16}`); await sleep(1500);
    await run(`${O}fill ${cx - r} ${Y} ${cz - r} ${cx + r} ${Y + 30} ${cz + r} minecraft:air`); await run(`${O}fill ${cx - r} ${Y - 1} ${cz - r} ${cx + r} ${Y - 1} ${cz + r} minecraft:grass_block`); };
  const moon = async () => { await run('scoreboard players set #forced bm.bm 1'); await run('time set 14000');
    return wait(5000, async () => (await sc('#active', 'bm.bm')) === 1); };
  const dawn = async () => { await run('scoreboard players set #forced bm.bm 0'); await run('time set 1000'); return wait(5000, async () => (await sc('#active', 'bm.bm')) === 0); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat');
  await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('gamerule spawn_mobs false');      // (no other Blood Moon monster - nor a second Lantern's roll - while it waits)
  await run(`${O}kill @e[type=minecraft:giant,tag=bm.salboss]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.salp]`);
  await field(X, Z, 20); await field(X + FAR, Z, 3);
  await at(X + FAR + 0.5, Y, Z + 0.5);

  if (!ONLY) {
    ok('the stage: a Blood Moon (#active)', await moon());
    // ---- RISE: a monster at the field's centre rolls into the Lantern, as a natural spawn does
    await run(`${O}summon minecraft:zombie ${X + 0.5} ${Y} ${Z + 0.5} {Tags:["bm.t342src"]}`);
    await run(`${O}execute as @e[type=minecraft:zombie,tag=bm.t342src] at @s run function bm:p82/spawn`);
    ok('a monster\'s spawn rolled into the Arachno-Lantern: it stands on the field', await wait(3000, async () => (await cnt(LAN)) === 1));
    const p0 = await pos(`${LAN.slice(0, -1)},limit=1]`);
    ok('...on the ground, not in the void', p0 && p0[1] > Y - 3 && p0[1] < Y + 6, String(p0));
    ok('...its rig whole (the dormant pumpkin)', await wait(3000, async () => (await parts()) >= 10), `${await parts()} parts`);
    ok('...and the monster it rose from is gone', await wait(3000, async () => (await cnt('@e[type=minecraft:zombie,tag=bm.t342src]')) === 0));

    // ---- WAIT: TestRat 150 blocks off for more than three minutes
    const t0 = Date.now(); let gone = null, low = null, whole = true, n = 0;
    while (Date.now() - t0 < 195000) {
      await sleep(5000); n++;
      if ((await cnt(LAN)) !== 1) { gone = Math.round((Date.now() - t0) / 1000); break; }
      const p = await pos(`${LAN.slice(0, -1)},limit=1]`); if (!p || p[1] < Y - 3) { low = p; break; }
      if ((await parts()) < 10) whole = false;
      if ((await sc('#active', 'bm.bm')) !== 1) await moon();
    }
    ok(`TestRat ${FAR} blocks off for 3 min 15 s: the Lantern is still there (sampled ${n} times)`, gone === null, gone === null ? '' : `gone after ~${gone} s`);
    ok('...still on its field', low === null, String(low));
    ok('...still whole', whole);
    // ---- DAWN: the Blood Moon ends - it gutters out
    ok('the Blood Moon ends', await dawn());
    ok('...and the Lantern gutters out with it - no part left', await wait(5000, async () => (await cnt(LAN)) === 0 && (await parts()) === 0), `${await cnt(LAN)} hosts, ${await parts()} parts`);
  }

  // ---- GOURD: one grown from a Smouldering Gourd is still sent off when left alone, far away
  if (!ONLY || ONLY === 'gourd') {
    await run(`${O}execute positioned ${X + 0.5} ${Y} ${Z + 0.5} run function bm:p82/summon`);
    await run(`${O}tag ${LAN} add bm.called`);
    ok('a gourd\'s Lantern (bm.called), TestRat 150 off: it stays a moment', await wait(2000, async () => (await cnt(LAN)) === 1));
    await field(X + 200, Z, 3); await at(X + 200.5, Y, Z + 0.5);
    ok('...TestRat 200 off: it is sent off (the far sweep)', await wait(5000, async () => (await cnt(LAN)) === 0));
    await run(`${O}kill @e[type=minecraft:item_display,tag=bm.salp]`);
  }

  await run('gamerule spawn_mobs true'); await run('scoreboard players set #forced bm.bm 0'); await run('time set 1000');
  await run(`${O}kill @e[type=minecraft:giant,tag=bm.salboss]`); await run('effect clear TestRat');
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

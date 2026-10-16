// 2.80g: no room the crew can't finish - a straggler out of reach is flushed out. A fighting room is done when no guard is left
// in it, so one the crew couldn't reach (a vex in a wall, a shulker on the ceiling, a flyer up in the rafters) kept the door shut
// for good. As a regular (non-op) player: walked into a Counting House, its guards wake; rcon sets the stage - every guard but
// one cleared away, and that one walled up in a sealed pocket up in the ceiling's corner, where nobody can reach it (and
// nothing can hurt it, a stray follower included, until it's out).
//   Standing in the room, out of its reach: within 40-odd seconds it's flushed out onto the room's floor and glows;
//   killed, the room opens.
const { bot, rcon, sleep } = require('./lib_resp');
const H = require('./h110');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 500) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const h = H.mk(run);
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  await h.heist('guards', 'a', 1); await h.begin(); await sleep(1500);
  const qs = await h.qs('guards'); const q = qs[0];
  ok('a heist of Counting Houses, under way', qs.length >= 1, `rooms ${qs}`);
  // ---- walk in: the first wave wakes
  await h.go('guards', q, 6, 12); await sleep(300);
  const m = await h.mpos('guards', q);
  await A.walkTo(m[0] + 0.5, m[2] + 0.5); await sleep(2500);
  ok('walked in: the guards wake', await wait(5000, async () => (await h.sc('guards', q, 'bm.gvs')) >= 1), `state ${await h.sc('guards', q, 'bm.gvs')}`);
  // ---- the stage: all but one cleared; that one walled up in a sealed pocket in the ceiling's corner
  await h.at('guards', q, 'kill @e[tag=bm.gvg,distance=..18,sort=furthest,limit=40]');
  await h.at('guards', q, `summon minecraft:zombie ${H.rel(2, 9, 2)} {Tags:["bm.gvg","bm.t188"],PersistenceRequired:1b,Silent:1b,Invulnerable:1b}`);
  await h.at('guards', q, `fill ${H.rel(1, 8, 1)} ${H.rel(3, 11, 3)} minecraft:bedrock hollow`);
  await sleep(500);
  const G = '@e[tag=bm.t188,limit=1]';
  const gpos = async () => { const r = (await run(`execute in bm:gutter run data get entity ${G} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return r ? [+r[1], +r[2], +r[3]] : null; };
  const p0 = await gpos();
  ok('the stage: one guard left, sealed in the ceiling corner out of reach', p0 && p0[1] - m[1] >= 4, JSON.stringify(p0));
  // ---- stand in the room and wait: it's flushed out onto the floor, glowing
  A.bars.length = 0;
  const out = await wait(60000, async () => { const p = await gpos(); return p && Math.abs(p[1] - m[1]) < 1.5 && Math.hypot(p[0] - m[0], p[2] - m[2]) < 2; }, 1000);
  ok('...standing in the room, out of its reach: it\'s flushed out onto the middle of the floor', out, JSON.stringify(await gpos()));
  ok('...it glows, and the crew is told', /glowing/.test(await run(`execute in bm:gutter run data get entity ${G} active_effects`)) && A.bars.some(b => /straggler/.test(b)),
     A.bars.slice(-1).join(''));
  // ---- killed: the room goes on (the second wave, then the captain's)
  await run('execute in bm:gutter as @e[tag=bm.t188] run data merge entity @s {Invulnerable:0b}'); await run(`execute in bm:gutter run kill ${G}`);
  ok('...killed: the room moves on to its next wave', await wait(5000, async () => (await h.sc('guards', q, 'bm.gvs')) >= 2), `state ${await h.sc('guards', q, 'bm.gvs')}`);
  await h.at('guards', q, `fill ${H.rel(1, 8, 1)} ${H.rel(3, 11, 3)} minecraft:air replace minecraft:bedrock`);

  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/rooms_any'); await run('function bm:admin/variant_random'); await run('function bm:admin/plan_safe');
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

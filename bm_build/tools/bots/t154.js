// 2.78: the Wings of the Damned, worn by a regular (non-op) player and flown with the real keys. On the ground: crouch half a
// second (the sneak key held, tick by tick, as a client sends it), then jump: the server throws the bot skyward - a Levitation
// burst (the rocket boots' kind) - and takes it off again a few ticks later. A jump with no crouch first: nothing. In the air,
// gliding (start_fall_flying, as a client sends on its mid-air jump): no sneak - no push; the sneak key held - the wings drive the
// bot on (the server sends it motion, tick after tick).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
const varint = (b, o = 0) => { let v = 0, s = 0, x; do { x = b[o++]; v |= (x & 0x7f) << s; s += 7; } while (x & 0x80); return [v, o]; };
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const O = 'execute in minecraft:overworld run ';
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  // what the server tells the bot about itself: its effects, its motion
  const lev = [], vel = [];
  A.on('entity_effect', (p) => { const [e, o] = varint(p.data); if (e !== A.eid) return; const [id, o2] = varint(p.data, o); const [amp] = varint(p.data, o2); lev.push({ id, amp, t: Date.now() }); });
  A.on('remove_entity_effect', (p) => { const [e, o] = varint(p.data || Buffer.alloc(1)); if (e === A.eid) lev.push({ gone: true, t: Date.now() }); });
  A.on('entity_velocity', (p) => { const [e] = varint(p.data); if (e === A.eid) vel.push(Date.now()); });
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance 600 4 true');
  await run(`${O}fill 15300 100 15300 15306 100 15306 minecraft:stone`); await run(`${O}fill 15300 101 15300 15306 104 15306 minecraft:air`);
  await run(`${O}tp TestRat 15303.5 101 15303.5 0 0`); await sleep(1500);
  await run('loot replace entity TestRat armor.chest loot bm:items/hollow_wings'); await sleep(300);
  ok('(the Wings of the Damned worn)', /Found 1/.test(await run('clear TestRat minecraft:elytra[minecraft:custom_data~{bm:"hollow_wings"}] 0')) ||
     /elytra/.test(await run('data get entity TestRat equipment.chest.id')), await run('data get entity TestRat equipment.chest.id'));
  // a client tick: where it stands, what it presses
  A.unstand();
  const tick = async (inputs, onGround = true, n = 1) => { for (let i = 0; i < n; i++) { A.write('player_input', { inputs }); A.ground(onGround); await sleep(50); } };
  // 1. a jump with no crouch first: nothing
  await tick({}, true, 10); lev.length = 0;
  await tick({ jump: true }, true, 2); await tick({}, false, 3); await tick({}, true, 10);
  ok('a plain jump: no launch', !lev.some(e => e.amp === 34), JSON.stringify(lev));
  // 2. crouch half a second, then jump: thrown skyward, and the burst taken off after a few ticks
  lev.length = 0;
  await tick({ shift: true }, true, 14);
  await tick({ shift: true, jump: true }, true, 1); await tick({ jump: true }, false, 2); await tick({}, false, 14);
  const up = lev.find(e => e.id === 24 && e.amp === 34), gone = lev.find(e => e.gone && up && e.t > up.t);
  ok('crouch, then jump: the wings throw the bot skyward (a Levitation burst)', !!up, JSON.stringify(lev));
  ok('...cut off after a few ticks (a burst, not a float)', !!gone && gone.t - up.t < 1200, gone && up ? `${gone.t - up.t} ms` : JSON.stringify(lev));
  await tick({}, true, 10);
  // 3. gliding: no sneak, no push; sneak held, the wings drive on
  await run(`${O}tp TestRat 15303.5 180 15303.5 0 10`); await sleep(800);
  await tick({}, false, 4); A.write('entity_action', { entityId: A.eid, actionId: 6, jumpBoost: 0 }); await tick({}, false, 3);
  ok('(gliding, as a client starts it)', /1b|true/.test(await run('execute if entity TestRat[predicate=bm:p2/ht_gliding]')) || /passed/i.test(await run('execute if entity @a[name=TestRat,predicate=bm:p2/ht_gliding]')),
     await run('execute if entity @a[name=TestRat,predicate=bm:p2/ht_gliding]'));
  vel.length = 0; await tick({}, false, 20); const calm = vel.length;
  vel.length = 0; await tick({ shift: true }, false, 20); const push = vel.length;
  ok('gliding, no sneak: the wings leave the bot be', calm <= 2, `${calm} pushes`);
  ok('gliding, sneak held: the wings drive it on (a push tick after tick)', push >= 12, `${push} pushes in 20 ticks`);
  await run(`${O}tp TestRat 15303.5 101 15303.5`); A.stand(); await sleep(600);
  await run('clear TestRat'); await run('effect clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

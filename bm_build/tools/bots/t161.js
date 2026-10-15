// 2.78c: ridden in his Ethereal or Wraithfire Form, Apophiss flies - as a regular (non-op) player, every step a real packet: the
// Oath calls him, a saddle on him (a right-click), the Ethereal Gem given (a right-click), the Oath beside him to climb on;
// then riding as a client rides (looks and keys every tick): look up and walk - he climbs; look level - he holds his height;
// look down - he dives; jump - a hard wingbeat up. Off, the gem taken back (sneak + right-click), on again: look up and walk -
// he only slithers along the ground. And his click box comes with him, however far he flew. rcon only sets the stage.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const epos = async sel => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const use = async (slot) => { A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(300); };
  const pet = '@e[type=minecraft:wolf,tag=bm.appet,limit=1]';
  const riding = async () => /passed/i.test(await run('execute as TestRat on vehicle if entity @s[type=minecraft:wolf,tag=bm.appet]'));
  const X = 16520, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  for (const t of ['bm.appet', 'bm.emmapet', 'bm.leopet', 'bm.cecilpet', 'bm.kxpet', 'bm.wilfrey']) await run(`kill @e[tag=${t}]`);
  for (const o of ['bm.apcd', 'bm.apel', 'bm.cosap', 'bm.apsd']) await run(`scoreboard players set TestRat ${o} 0`);
  await run(`${O}forceload add ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  await run(`${O}fill ${X - 24} ${Y} ${Z - 24} ${X + 24} ${Y} ${Z + 24} minecraft:stone`);
  for (let y = Y + 1; y < Y + 40; y += 8) await run(`${O}fill ${X - 24} ${y} ${Z - 24} ${X + 24} ${y + 7} ${Z + 24} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..40]`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z - 10.5} 0 0`); await sleep(2000);
  await run('loot replace entity TestRat hotbar.0 loot bm:items/apo_oath');
  await use(0);
  ok('the Oath calls him', await wait(5000, async () => (await cnt(pet)) === 1));
  await sleep(2000);
  const clickHim = async (slot, sneak = false) => {
    await run(`${O}tp ${pet} ${X + 0.5} ${Y + 1} ${Z - 7.5}`); await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z - 10.5} 0 0`); await sleep(1000);
    const box = await entOf('@e[type=minecraft:interaction,tag=bm.aphit,limit=1]'); if (!box) return false;
    A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(250); }
    A.interact(box.entityId, sneak); await sleep(900); if (sneak) { A.input({}); await sleep(200); } return true;
  };
  await run('item replace entity TestRat hotbar.1 with minecraft:saddle'); await clickHim(1);
  ok('a saddle on him (a right-click)', (await sc('TestRat', 'bm.apsd')) === 1);
  await run('loot replace entity TestRat hotbar.2 loot bm:items/ethereal_gem'); await sleep(1300); await clickHim(2);
  ok('the Ethereal Gem given (a right-click): his Ethereal Form', (await sc('TestRat', 'bm.apel')) === 10);
  const mount = async () => {
    await run(`${O}tp ${pet} ${X + 0.5} ${Y + 1} ${Z - 8.7}`); await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z - 10.5} 0 0`); await sleep(900);
    await use(0); await sleep(600); return riding();
  };
  ok('the Oath beside him: you climb on', await mount());
  // (riding as a client: look up and walk)
  const y0 = (await epos(pet))[1];
  A.ride(0, -45, { forward: true }); await sleep(3000);
  const y1 = (await epos(pet))[1];
  ok('look up and walk: he climbs into the air', y1 - y0 > 3, `y ${y0.toFixed(1)} -> ${y1.toFixed(1)}`);
  A.ride(0, 0, { forward: true }); await sleep(600); const y2 = (await epos(pet))[1]; await sleep(1500); const y3 = (await epos(pet))[1];
  ok('look level: he glides, holding his height', Math.abs(y3 - y2) < 0.6 && y3 > Y + 3, `y ${y2.toFixed(1)} -> ${y3.toFixed(1)}`);
  A.ride(0, 0, { jump: true }); await sleep(500); A.ride(0, 0, {}); const y4 = (await epos(pet))[1];
  ok('jump: a hard wingbeat up', y4 - y3 > 0.8, `y ${y3.toFixed(1)} -> ${y4.toFixed(1)}`);
  A.ride(0, 60, { forward: true }); await sleep(1500); const y5 = (await epos(pet))[1];
  ok('look down: he dives', y4 - y5 > 2, `y ${y4.toFixed(1)} -> ${y5.toFixed(1)}`);
  await wait(6000, async () => (await epos(pet))[1] < Y + 1.6, 250);
  A.ride(0, 0, { shift: true }); await sleep(800); A.unride(); A.input({}); await sleep(300); A.stand(); await sleep(500);
  ok('sneak: you climb off', !(await riding()));
  ok('...and he has his weight back (no floating once you are off)', !/1b/.test(await run(`${O}data get entity ${pet} NoGravity`)), await run(`${O}data get entity ${pet} NoGravity`));
  // (the gem taken back: no more flying)
  // (2.78c: his click box comes with him after a long flight - it used to be left behind, and another made)
  A.bars.length = 0; const c0 = await clickHim(5);
  ok('far from where he took off, one click box - with him - and a right-click on it answers', c0 && (await cnt('@e[type=minecraft:interaction,tag=bm.aphit]')) === 1 && A.bars.some(b => /Apophiss/.test(b)),
     A.bars.slice(-1).join(''));
  await sleep(1200); A.bars.length = 0; await clickHim(5, true);
  ok('sneak + right-click empty-handed: the gem back - his own scales', (await sc('TestRat', 'bm.apel')) === 0);
  ok('on again', await mount());
  const g0 = (await epos(pet))[1];
  A.ride(0, -45, { forward: true }); await sleep(2500);
  const g1 = (await epos(pet))[1];
  ok('look up and walk: without a form he only slithers along the ground', g1 - g0 < 1.2, `y ${g0.toFixed(1)} -> ${g1.toFixed(1)}`);
  A.ride(0, 0, { shift: true }); await sleep(800); A.unride(); A.input({}); A.stand(); await sleep(300);
  await run('kill @e[tag=bm.appet]'); await run('clear TestRat');
  await run(`${O}forceload remove ${X - 48} ${Z - 48} ${X + 48} ${Z + 48}`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

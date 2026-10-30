// 3.0d: COMPANION SIZE (compsize.py) - the very large followers shrunk to stand beside you, as a regular (non-op) player: APOPHISS
// (the Serpent's Oath) and KING OMEGA (his Monocle). rcon only sets the stage (a floor, the item in hand, a still monster to fight).
// For each: called at full size (his coil's scale, his host's); his menu's "Companion size" pressed - every part's scale and his host's
// hitbox shrink to a fifth (proportions kept: the coil and the head alike), his parts still at his host; he still follows (walked away
// from: he comes) and still fights (a monster near is hurt); pressed again - full size; on again, sent home and called - still small
// (kept on you); Apophiss small won't be ridden. (The Ophanim's companion size is t326's.)
//   node t333.js [apo|omega]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const vec = (t) => (t.match(/-?[\d.]+(?:E-?\d+)?/g) || []).map(Number);
  const X = 17900, Y = 100, Z = 16080;
  let A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const sneakMenu = async (slot) => { const n0 = A.dialogN.length; await use(slot, true); await wait(3000, async () => A.dialogN.length > n0); return A.dialogN.length > n0; };
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`); await sleep(2500);
  await run(`${O}fill ${X - 16} ${Y} ${Z - 16} ${X + 16} ${Y} ${Z + 16} minecraft:stone`); await run(`${O}fill ${X - 16} ${Y + 1} ${Z - 16} ${X + 16} ${Y + 12} ${Z + 16} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..30]`); await run(`${O}time set noon`);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);

  const KIN = [
    { key: 'apo', name: 'Apophiss', item: 'apo_oath', pet: 'bm.appet', part: 'bm.app', cd: 'bm.apcd', obj: 'bm.apcs', home: /Send him home/ },
    { key: 'omega', name: 'King Omega', item: 'om_monocle', pet: 'bm.ompet', part: 'bm.omp', cd: 'bm.omcd', obj: 'bm.omcs', home: /Send him home/ },
  ];
  for (const K of KIN) {
    if (!on(K.key)) continue;
    const PET = `@e[type=minecraft:wolf,tag=${K.pet},limit=1]`;
    const P = (p) => `@e[type=minecraft:item_display,tag=${K.part}_${p},tag=${K.part}_pet,limit=1]`;
    const sc = async (p) => vec(await nbt(P(p), 'transformation.scale'))[0];
    const hostSc = async () => +(((await run(`${O}attribute ${PET} minecraft:scale base get`)).match(/is (-?[\d.]+)/) || [0, NaN])[1]);
    await run(`kill @e[type=minecraft:wolf,tag=${K.pet}]`); await run(`scoreboard players set TestRat ${K.cd} 0`); await run(`scoreboard players set TestRat ${K.obj} 0`);
    await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${K.item}`); await sleep(2300);
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
    await use(0);
    ok(`${K.name}: called with his own item`, await wait(5000, async () => (await cnt(PET)) === 1));
    await wait(4000, async () => (await sc('coil')) > 2.5 && (await sc('head')) > 2.5, 250);
    const c0 = await sc('coil'), h0 = await sc('head'), s0 = await hostSc();
    ok(`...at his full size (coil ${c0}, head ${h0}, host ${s0})`, c0 > 2.5 && h0 > 2.5 && s0 > 2.5);
    await sleep(2300);
    ok('...his menu: a "Companion size" row', await sneakMenu(0) && A.buttons().some(b => /Companion size/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
    A.bars.length = 0; await A.press(/Companion size/); await sleep(300);
    ok('...pressed: every part shrinks to a fifth, proportions kept (coil and head alike)', await wait(4000, async () => Math.abs((await sc('coil')) - c0 * 0.2) < 0.02 && Math.abs((await sc('head')) - h0 * 0.2) < 0.02, 200),
       `coil ${await sc('coil')} head ${await sc('head')}`);
    ok('...his host\'s hitbox to match (scale 0.8)', Math.abs((await hostSc()) - 0.8) < 0.01, String(await hostSc()));
    ok('...kept on you (bm.*cs 1), and he says so', (+((await run(`scoreboard players get TestRat ${K.obj}`)).match(/has (-?\d+)/) || [0, 0])[1]) === 1 && A.bars.length > 0, A.bars.slice(-1).join(''));
    const hp = vec(await nbt(PET, 'Pos')), cp = vec(await nbt(P('coil'), 'Pos'));
    ok('...his parts at his host', Math.hypot(hp[0] - cp[0], hp[2] - cp[2]) < 1.0, `${hp.map(v => v.toFixed(1))} / ${cp.map(v => v.toFixed(1))}`);
    // still follows
    await at(X + 10.5, Y + 1, Z + 0.5, 90, 0);
    ok('...walked away from: he follows (within 5)', await wait(15000, async () => { const p = vec(await nbt(PET, 'Pos')); return Math.hypot(p[0] - (X + 10.5), p[2] - (Z + 0.5)) < 5; }, 300));
    // still fights
    await run(`${O}summon minecraft:husk ${X + 10.5} ${Y + 1} ${Z + 3.5} {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["cstest","bm.seen"],Health:200f,attributes:[{id:"minecraft:max_health",base:200d}]}`);
    const mh = async () => +(((await nbt('@e[type=minecraft:husk,tag=cstest,limit=1]', 'Health')).match(/([\d.]+)/) || [0, 200])[1]);
    ok('...and still fights: a monster near him is hurt', await wait(12000, async () => (await mh()) < 200, 300), String(await mh()));
    await run(`${O}kill @e[type=minecraft:husk,tag=cstest]`); await sleep(1500);
    if (K.key === 'apo') {
      await run('scoreboard players set TestRat bm.apsd 1'); await sleep(2300);
      await sneakMenu(0); A.bars.length = 0; await A.press(/Ride him/); await sleep(800);
      ok('...small, he won\'t be ridden ("At this size?")', A.bars.some(b => /At this size/.test(b)) && !/minecraft:player/.test(await nbt(PET, 'Passengers')), A.bars.slice(-1).join(''));
      await run('scoreboard players set TestRat bm.apsd 0'); await sleep(2300);
    }
    await sneakMenu(0); await A.press(/Companion size/); await sleep(300);
    ok('...pressed again: his full size back (coil, head, host)', await wait(4000, async () => Math.abs((await sc('coil')) - c0) < 0.02 && Math.abs((await sc('head')) - h0) < 0.02, 200) && Math.abs((await hostSc()) - s0) < 0.01);
    // kept across a send-home and a call
    await sleep(2300); await sneakMenu(0); await A.press(/Companion size/); await sleep(1500);
    await sneakMenu(0); await A.click(K.home); await sleep(1500);
    ok('...on again, sent home: gone', (await cnt(PET)) === 0);
    await run(`scoreboard players set TestRat ${K.cd} 0`); await sleep(2300); await use(0);
    ok('...called again: still at companion size (kept)', await wait(5000, async () => (await cnt(PET)) === 1) && await wait(5000, async () => Math.abs((await sc('coil')) - c0 * 0.2) < 0.02, 250) && Math.abs((await hostSc()) - 0.8) < 0.01,
       `coil ${await sc('coil')}`);
    await sleep(2300); await sneakMenu(0); await A.press(/Companion size/); await sleep(800);
    await sneakMenu(0); await A.click(K.home); await sleep(1200);
    await run(`scoreboard players reset TestRat ${K.obj}`); await run(`scoreboard players set TestRat ${K.cd} 0`);
    ok('...and no part of him left behind', (await cnt(`@e[type=minecraft:item_display,tag=${K.part}_pet]`)) === 0);
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  }
  await run('clear TestRat');
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})();

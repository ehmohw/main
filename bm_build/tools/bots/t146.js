// 2.78: every follower in a frame - as a regular (non-op) player, every step a real packet: Zib's Donadian Medal,
// KillerWatt's Spark and Pearlman's card each hung in an item frame with a right-click: the follower climbs out (and says
// so), stays by the frame (nobody's - not the player's), still there ten seconds on; the item punched out of the frame:
// the follower goes with it. rcon only sets the stage (a wall, the frames, the three items).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (C, sel) => { const u = await uuidOf(sel); return Object.values(C.ents).find(e => e.objectUUID === u); };
  const X = 16420, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 8} ${Y} ${Z - 8} ${X + 8} ${Y} ${Z + 8} minecraft:stone`); await run(`${O}fill ${X - 8} ${Y + 1} ${Z - 8} ${X + 8} ${Y + 8} ${Z + 8} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run(`${O}fill ${X - 6} ${Y + 1} ${Z + 5} ${X + 6} ${Y + 3} ${Z + 5} minecraft:stone`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 2.5} 0 -10`);
  await wait(2000, async () => A.pos && Math.abs(A.pos.z - (Z + 2.5)) < 0.05, 100); await sleep(400);

  const KINDS = [['Zib', 'donadian_medal', 'wolf', 'bm.zibpet', -4], ['KillerWatt', 'kw_spark', 'wolf', 'bm.kxpet', 0], ['Pearlman', 'pearl_card', 'cat', 'bm.pmpet', 4]];
  for (const [name, iid, host, tag, dx] of KINDS) {
    await run(`${O}summon minecraft:item_frame ${X + dx} ${Y + 2} ${Z + 4} {Facing:2b,Tags:["bm.t146f"]}`); await sleep(400);
    await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); await sleep(300);
    await run(`${O}tp TestRat ${X + dx + 0.5} ${Y + 1} ${Z + 2.5} 0 -10`); await sleep(800);
    const frSel = `@e[type=minecraft:item_frame,tag=bm.t146f,x=${X + dx},y=${Y + 2},z=${Z + 4},distance=..2,limit=1]`;
    let fr = null; await wait(4000, async () => (fr = await entOf(A, frSel)) != null, 250);
    ok(`${name}: a frame on the wall`, fr != null);
    if (!fr) continue;
    A.slot(0); await sleep(300); A.bars.length = 0;
    if (fr) A.interact(fr.entityId); await sleep(2800);
    const pet = `@e[type=minecraft:${host},tag=${tag},tag=bm.ffpet,x=${X + dx},y=${Y + 2},z=${Z + 4},distance=..10]`;
    ok(`${name}'s item in a frame: ${name} climbs out`, (await cnt(pet)) === 1, `out ${await cnt(pet)}`);
    ok('...and says so', A.bars.some(b => new RegExp(`${name} climbs out of the frame`).test(b)), A.bars.slice(-1).join(''));
    ok('...nobody\'s - not the player\'s', (await cnt(`${pet.slice(0, -1)},scores={bm.pid=${+((await run('scoreboard players get TestRat bm.pid')).match(/has (-?\d+)/) || [0, -9])[1]}}]`)) === 0);
    await sleep(10000);
    ok('...still there by the frame ten seconds on', (await cnt(pet)) === 1);
    A.attack(fr.entityId); await sleep(500);
    ok('the item punched out of the frame: out it drops', await wait(1500, async () => (await cnt(`@e[type=minecraft:item,x=${X + dx},y=${Y + 2},z=${Z + 4},distance=..3]`)) >= 1));
    ok(`...and ${name} goes with it`, await wait(3000, async () => (await cnt(pet)) === 0));
    await run(`${O}kill @e[type=minecraft:item,x=${X + dx},y=${Y + 2},z=${Z + 4},distance=..4]`);
  }
  await run(`${O}kill @e[type=minecraft:item_frame,tag=bm.t146f]`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();

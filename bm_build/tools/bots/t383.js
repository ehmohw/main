// 3.0j: YOUR SETTINGS - music, chatter and screen shake are yours alone (phase260), as two regular players. A music line of the pack's
// (the market's own swing, played to TestRat as its player does) is heard; Your settings (the Handbook, sneak + right-click) ->
// Music: off - the track is stopped for him, the same line is not heard, and TestRat2 (music on) still hears it; Music: on - heard
// again. Follower chatter: off for TestRat only (bm.hush on him, not on TestRat2). Screen shake: off - a shake set on him sends
// no camera turns; on - it does.
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs'), path = require('path');
const FN = path.join(__dirname, '../../out_p2/BlackMarket_DP/data/bm/function');
(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 100) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const A = await bot('TestRat'); await sleep(1500); const B = await bot('TestRat2'); await sleep(2500); A.stand(); B.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  let rot = 0; A.on('player_rotation', () => rot++); A.on('position', () => {});
  for (const n of ['TestRat', 'TestRat2']) { await run(`tag ${n} remove bm.nomus`); await run(`tag ${n} remove bm.hush`); await run(`tag ${n} remove bm.noshk`); }
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/bm_handbook'); A.slot(0); await sleep(300);
  const SND = 'bm:music.market_theme';
  // (a stand-in for the market's music player: its own line, run as each player)
  const all = []; const walk = (d) => { for (const f of fs.readdirSync(d)) { const q = path.join(d, f); if (fs.statSync(q).isDirectory()) walk(q); else all.push(q); } };
  walk(path.join(FN, 'p250'));
  const line = all.map(f => fs.readFileSync(f, 'utf8')).join('\n').split('\n').find(l => l.includes(`playsound ${SND} `) && !l.startsWith('$'));
  const cmd = line.replace(/^execute if score #mkw bm.rng matches \d+ run /, '');
  ok('the market music line answers to the mute', /tag=!bm\.nomus/.test(cmd), cmd.slice(0, 120));
  const play = async (who) => run(`execute as ${who} at @s run ${cmd}`);
  const heard = (C, t0) => C.sounds.some(s => s.name === SND && s.t >= t0);
  let t0 = Date.now(); await play('TestRat'); await play('TestRat2'); await sleep(600);
  ok('music on: both hear it', heard(A, t0) && heard(B, t0));
  const ps = async () => { await run('scoreboard players set TestRat bm.gvhc 0'); const n0 = A.dialogN.length; A.input({ shift: true }); await sleep(200); A.use(); await sleep(350); A.release(); A.input({});
    await wait(2500, async () => A.dialogN.length > n0); };
  await ps();
  ok('Your settings: its page, Music: on', A.buttons().some(b => /^Music: on/.test(b.label)));
  const s0 = A.stops.length; await A.press(/^Music:/);
  ok('...Music: off - the page says so, the track stopped for him', A.buttons().some(b => /^Music: off/.test(b.label)) && A.stops.slice(s0).some(s => JSON.stringify(s).includes('music.market_theme')));
  t0 = Date.now(); await play('TestRat'); await play('TestRat2'); await sleep(600);
  ok('...the same line: TestRat hears nothing, TestRat2 still does', !heard(A, t0) && heard(B, t0));
  await A.press(/^Music:/); t0 = Date.now(); await play('TestRat'); await sleep(600);
  ok('...Music: on - heard again', heard(A, t0));
  await A.press(/^Follower chatter/);
  const h1 = /passed/i.test(await run('execute if entity @a[name=TestRat,tag=bm.hush]')), h2 = /passed/i.test(await run('execute if entity @a[name=TestRat2,tag=bm.hush]'));
  ok('Follower chatter: off for TestRat alone', h1 && !h2 && A.buttons().some(b => /chatter: off/.test(b.label)));
  await A.press(/^Follower chatter/);
  await A.press(/^Screen shake/);
  rot = 0; await run('scoreboard players set TestRat bm.shka 1'); await run('scoreboard players set TestRat bm.shk 10'); await sleep(800);
  ok('Screen shake: off - a shake sends no camera turns', rot === 0 && A.buttons().some(b => /shake: off/.test(b.label)), `turns ${rot}`);
  await A.press(/^Screen shake/);
  rot = 0; await run('scoreboard players set TestRat bm.shka 1'); await run('scoreboard players set TestRat bm.shk 10'); await sleep(800);
  ok('Screen shake: on - it does', rot > 0, `turns ${rot}`);
  await run('clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); B.end(); R.end(); process.exit(0);
})();

// 2.78: every boss makes an entrance. (2.80: the six roaming bosses now arrive in their own staged sequences - t168 - so this
// covers Captain Tullius, who keeps this entrance.) As a regular (non-op) player standing by (rcon only raises each boss, as the admin
// command would): the Headless Horseman, the Sand Pharaoh, the Storm Roc, the Elder Treant, the Magma Colossus, the Voidwalker
// and Captain Tullius each arrive with a title card on the player's screen (their name, their epithet), a ring of their own
// colours that sweeps in and is gone two seconds later, and - for the Horseman, the Voidwalker and Tullius - the light dips.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const BOSSES = [['tullius', 'CAPTAIN TULLIUS', 'the drowned captain', true, null]];
  const X = 16600, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect give TestRat minecraft:resistance 600 4 true');
  await run(`${O}forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  await run(`${O}fill ${X - 20} ${Y} ${Z - 20} ${X + 20} ${Y} ${Z + 20} minecraft:grass_block`); await run(`${O}fill ${X - 20} ${Y + 1} ${Z - 20} ${X + 20} ${Y + 20} ${Z + 20} minecraft:air`);
  // (each boss's own effect, so the dip can be told apart: what the player's effects say a tick after)
  for (const [b, name, epi, dark] of BOSSES) {
    await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..40]`); await run('effect clear TestRat minecraft:darkness');
    await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(800); A.stand();
    A.titles.length = 0;
    await run(`execute as TestRat at @s run function bm:admin/${b}`);
    ok(`[${b}] the title card: "${name}" - "${epi}"`, await wait(2500, async () => A.titles.some(t => t.includes(name)) && A.titles.some(t => t.includes(epi))), A.titles.join(' | ').slice(0, 120));
    ok(`[${b}] ...a ring of its colours sweeping in`, (await cnt(`@e[type=minecraft:marker,tag=bm.cine_${b === 'storm_roc' ? 'roc' : b}]`)) === 1);
    const dk = /darkness/.test(await run('data get entity TestRat active_effects'));
    ok(`[${b}] ...${dark ? 'the light dips' : 'no darkness (not one of the dark ones)'}`, dk === dark);
    ok(`[${b}] ...and the ring is gone two seconds on`, await wait(4000, async () => (await cnt(`@e[type=minecraft:marker,tag=bm.cine]`)) === 0));
  }
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..60]`);
  for (const bb of ['bm:hhb', 'bm:sph', 'bm:roc', 'bm:trt', 'bm:mcol', 'bm:vwk', 'bm:tub']) await run(`bossbar set ${bb} visible false`).catch(() => {});
  await run('effect clear TestRat'); await run(`${O}forceload remove ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

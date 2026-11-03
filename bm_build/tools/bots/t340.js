// 3.0g: THE UNDERCROWN'S COMBAT ROOMS (p2/logic waves, p2/undercfg.WAVE_MIX, phase237's p237/wkit) as a regular (non-op) player -
// trial 4, the Frostbound Thralls. rcon sets the stage (the Undercrown placed, its progress at trial 3, TestRat stood in the room,
// mobs killed off or moved, a wave's age) and checks; the bot is the player in the room the waves come for.
//   mix      each wave by count, not 12/12/18 Dread: wave 1 is 8 (5 Dread, 3 armoured), wave 2 9 (5 + 4), wave 3 10 (6 + 4); the
//            armoured in diamond or netherite (bm.uarm), never a Dread's dress
//   clear    the last of a wave killed by ANOTHER MOB (a zombie's blow, by rcon): the wave counts as cleared all the same and the
//            next one rises; a wave mob LOST outside the room (moved off, out of reach): the wave clears without it - and the stray
//            is fetched back to a spawn point when the next one rises; stepping out of the room for 2 s doesn't call the waves off;
//            a wave 90 s old with one left: it glows; 150 s old: it's taken, the wave done - the last wave done: the trial solved
//   node t340.js        (both run in order - the clear checks ride on the mix's waves)
const { bot, rcon, sleep } = require('./lib_resp');
const OX = 2560, OZ = -2560;                                  // (p2/undercfg.ORIGIN)
const N = 'execute in minecraft:the_nether run ';
const WM = 'tag=bm.wm_under4';

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`${N}scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const cnt = async (sel) => { const m = (await run(`${N}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const cntIf = async (cmd) => { const m = (await run(`${N}${cmd}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (sel) => { const m = (await run(`${N}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const at = async (x, y, z) => { await run(`${N}tp TestRat ${x} ${y} ${z}`); await wait(3000, async () => A.pos && Math.abs(A.pos.x - x) < 0.2 && Math.abs(A.pos.z - z) < 0.2, 100); await sleep(400); };
  const DG = '@e[type=minecraft:marker,tag=bm.dg,tag=bm.d_under,limit=1]';
  const CT = '@e[type=minecraft:marker,tag=bm.pz,tag=bm.pz4,tag=bm.d_under,limit=1]';

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('tag TestRat add bm.lkpass');      // (phase251's pass: this test sets its stage by teleport)
  await run('gamemode survival TestRat'); await run('scoreboard players set #hard bm.cfg 1'); await run('clear TestRat');
  await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');
  await run('effect give TestRat minecraft:regeneration infinite 2 true');

  // ---- the stage: the Undercrown, its progress at trial 3 (trial 4 armed), TestRat in the Thralls' room
  await run(`${N}tp TestRat ${OX - 40} 100 ${OZ - 40}`); await run(`${N}setblock ${OX - 40} 98 ${OZ - 40} minecraft:obsidian`);
  const UVER = +require('fs').readFileSync(require('path').join(__dirname, '..', '..', 'phase237.py'), 'utf8').match(/^UVER = (\d+)/m)[1];
  if ((await sc('#uver', 'bm.p2')) !== UVER) await run('function bm:admin/under/place');
  ok('the stage: the Undercrown placed', await wait(900000, async () => (await sc('#uver', 'bm.p2')) === UVER, 2000));
  await run(`${N}forceload add ${OX} ${OZ} ${OX + 223} ${OZ + 223}`); await sleep(4000);
  ok('...its markers loaded (the dungeon, trial 4)', await wait(90000, async () => (await cnt(DG)) === 1 && (await cnt(CT)) === 1, 1000));
  const hub = await pos(DG); if (hub) { await at(hub[0], hub[1] + 1, hub[2]); await sleep(3000); }     // (an idle reset, if it's due, before the stage)
  await run(`${N}kill @e[${WM}]`);
  await run(`${N}scoreboard players set ${DG} bm.pz 3`);
  await run(`${N}execute as ${CT} at @s run function bm:p2/under/pz4_reset`); await sleep(500);
  const c = await pos(CT);
  ok('...trial 4 armed (no wave yet)', (await sc(CT, 'bm.wv')) <= 0 && (await sc(CT, 'bm.done')) === 0);
  const here = () => at(c[0], c[1] + 0.05, c[2] + 3);
  await here();

  // ---- MIX: each wave by count
  const wave = async (k, el, pl) => {
    ok(`wave ${k} rises: ${el + pl} of them`, await wait(8000, async () => (await sc(CT, 'bm.wv')) === k && (await cnt(`@e[${WM},tag=!bm.t340old]`)) >= el + pl, 250),
       `wv ${await sc(CT, 'bm.wv')}, ${await cnt(`@e[${WM},tag=!bm.t340old]`)} mobs`);
    await sleep(500);
    const n = await cnt(`@e[${WM},tag=!bm.t340old]`), dr = await cnt(`@e[${WM},tag=!bm.t340old,tag=bm.dread]`), ar = await cnt(`@e[${WM},tag=!bm.t340old,tag=bm.uarm]`);
    ok(`...exactly ${el + pl}: ${el} Dread, ${pl} armoured`, n === el + pl && dr === el && ar === pl, `${n} mobs: ${dr} Dread, ${ar} armoured`);
    const dia = await cntIf(`execute as @e[${WM},tag=bm.uarm] if items entity @s armor.chest minecraft:diamond_chestplate`);
    const net = await cntIf(`execute as @e[${WM},tag=bm.uarm] if items entity @s armor.chest minecraft:netherite_chestplate`);
    const dreadDress = await cntIf(`execute as @e[${WM},tag=bm.uarm] if items entity @s armor.head *[minecraft:item_model="bm:dread_helm"]`);
    ok('...the armoured in diamond or netherite (none in a Dread\'s dress)', dia + net === ar && dreadDress === 0, `${dia} diamond, ${net} netherite, ${dreadDress} dread-dressed`);
  };
  const killBy = async (sel) => {      // (the last of a wave: killed by a mob's blow, not a player's)
    const p = await pos(sel); if (!p) return false;
    await run(`${N}summon minecraft:zombie ${p[0]} ${p[1]} ${p[2] + 1} {NoAI:1b,Silent:1b,PersistenceRequired:1b,Tags:["bm.t340k","bm.seen","bm.dgmob"]}`);
    await run(`${N}damage ${sel} 99999 minecraft:mob_attack by @e[type=minecraft:zombie,tag=bm.t340k,limit=1]`);
    await sleep(300); await run(`${N}kill @e[type=minecraft:zombie,tag=bm.t340k]`); return true;
  };

  await wave(1, 5, 3);
  // ---- CLEAR: the last one killed by another mob
  await run(`${N}kill @e[${WM},sort=random,limit=7]`);
  ok('one left of wave 1: the wave holds', (await cnt(`@e[${WM}]`)) === 1 && await wait(4000, async () => (await sc(CT, 'bm.wv')) === 1) && (await sc(CT, 'bm.wt')) === 0);
  A.bars.length = 0;
  ok('...killed by a zombie\'s blow (no player\'s): gone', await killBy(`@e[${WM},limit=1]`) && (await cnt(`@e[${WM}]`)) === 0);
  ok('...the wave counts as cleared ("Wave cleared")', await wait(3000, async () => A.bars.some(b => /Wave cleared/.test(b))), A.bars.slice(-2).join(' / '));
  await wave(2, 5, 4);

  // ---- stepping out of the room for 2 s: the waves aren't called off
  if (hub) { await at(hub[0], hub[1] + 1, hub[2]); await sleep(2000); }
  await here();
  ok('stepping out of the room for 2 s and back: still wave 2, its mobs still there', (await sc(CT, 'bm.wv')) === 2 && (await cnt(`@e[${WM}]`)) >= 9);

  // ---- LOST: one carried out of the room (out of reach), the rest killed - the wave clears without it
  await run(`${N}tag @e[${WM},tag=bm.dread,limit=1] add bm.t340old`);
  await run(`${N}execute as @e[${WM},tag=bm.t340old] run data merge entity @s {NoAI:1b,Invulnerable:1b}`);
  await run(`${N}tp @e[${WM},tag=bm.t340old] ${c[0]} ${c[1] + 30} ${c[2]}`);
  await run(`${N}kill @e[${WM},tag=!bm.t340old,sort=random,limit=7]`);
  await killBy(`@e[${WM},tag=!bm.t340old,limit=1]`);
  ok('one carried out of the room, the rest dead: the wave clears without it', await wait(6000, async () => (await sc(CT, 'bm.wv')) === 3), `wv ${await sc(CT, 'bm.wv')}`);
  const lost = await pos(`@e[${WM},tag=bm.t340old,limit=1]`);
  ok('...and the stray is fetched back down into the room as the next rises', lost && Math.abs(lost[1] - c[1]) < 4 && Math.hypot(lost[0] - c[0], lost[2] - c[2]) < 24, String(lost));
  await run(`${N}execute as @e[${WM},tag=bm.t340old] run data merge entity @s {NoAI:0b,Invulnerable:0b}`);
  await wave(3, 6, 4);

  // ---- LATE: a wave 90 s old with one left glows; 150 s old, it's taken and the wave is done (the trial solved)
  await run(`${N}kill @e[${WM},tag=bm.t340old]`);
  await run(`${N}tag @e[${WM},tag=bm.dread,limit=1] add bm.t340st`);
  await run(`${N}execute as @e[${WM},tag=bm.t340st] run data merge entity @s {Invulnerable:1b}`);     // (one that can't be got at)
  await run(`${N}kill @e[${WM},tag=!bm.t340st]`); A.bars.length = 0;
  await run(`${N}scoreboard players set ${CT} bm.wage 1795`);
  ok('a wave 90 s old with one left: it glows', await wait(3000, async () => /glowing/.test(await run(`${N}data get entity @e[${WM},tag=bm.t340st,limit=1] active_effects`))));
  ok('..."The last of the wave are lit up"', await wait(2000, async () => A.bars.some(b => /lit up/.test(b))), A.bars.slice(-2).join(' / '));
  ok('...and still wave 3 (it holds the room)', (await sc(CT, 'bm.wv')) === 3 && (await cnt(`@e[${WM}]`)) === 1);
  await run(`${N}scoreboard players set ${CT} bm.wage 2995`);
  ok('150 s old: it is taken', await wait(3000, async () => (await cnt(`@e[${WM}]`)) === 0));
  ok('...the last wave done: trial 4 solved', await wait(6000, async () => (await sc(CT, 'bm.done')) === 1 && (await sc(DG, 'bm.pz')) === 4),
     `done ${await sc(CT, 'bm.done')}, progress ${await sc(DG, 'bm.pz')}`);

  await run(`${N}kill @e[${WM}]`); await run(`${N}kill @e[type=minecraft:zombie,tag=bm.t340k]`);
  await run('tag TestRat remove bm.lkpass'); await run('effect clear TestRat');
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

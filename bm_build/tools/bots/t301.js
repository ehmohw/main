// 2.96c: TOGETHER (phase234), as a regular (non-op) player - every follower called with its own item, used as an item.
// RIDING BENDER: Bender and Mr. Capshun out together, calm - Capshun hops up and rides (a real passenger of Bender's, in his
// 'ride' state, his rig seated on Bender's back); Bender carries him when you walk off; a monster and Bender's Rage - Capshun hops
// off first; calm again, he climbs back on. Kettle and the rat mercenary ride him too. DOG PILE: Bender and Henry - Henry's charged
// move: up onto Bender's back, riding him into the fight (Bender holding his own charged moves meanwhile), then off onto the
// monster for the finish; all their wits back after. THE NIGHT CUDDLE: Bender, Henry and Nia at night, calm, you by - in time all
// three lie down together (Bender asleep, the cats curled up either side of his chest, all three facing his way); you walk off -
// they wake and are up.
// (rcon sets the stage only: the arena, the time, the monsters, the followers' cooldowns, and sending one home between steps.)
const { bot, rcon, sleep } = require('./lib_resp');

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const num = async (sel, path) => +(((await nbt(sel, path)).match(/(-?[\d.]+)/) || [0, NaN])[1]);
  const score = async (o, who) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  // (an item used inside two seconds of the last is ignored - bm.gvhc)
  const use = async (slot) => { await sleep(2200); A.slot(slot); await sleep(250); A.use(); await sleep(400); A.release(); await sleep(300); };
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const X = 17600, Y = 100, Z = 16000;
  const P = (ab) => `@e[type=minecraft:wolf,tag=bm.${ab}pet,tag=!bm.ffpet,limit=1]`;
  const BV = P('bv'), MZ = P('mz'), KT = P('kt'), RU = P('ru'), HY = P('hy'), NI = P('ni');
  const riding = async (sel) => (await cnt(`${sel.replace('limit=1]', 'tag=bm.rdr,limit=1]')}`)) === 1 &&
    /count: 1/i.test(await run(`${O}execute as ${sel} on vehicle if entity @s[tag=bm.bvpet]`));
  const husk = (dx, dz, t, hp = 300) => run(`${O}summon minecraft:husk ${X + dx} ${Y + 1} ${Z + dz} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t301z","${t}","bm.seen"],attributes:[{id:"minecraft:max_health",base:${hp}}],Health:${hp}f}`);
  const home = async (pfx) => run(`${O}execute as TestRat at @s run function bm:${pfx}/home`);
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`); await run('weather clear'); await run(`${O}time set noon`); await sleep(2500);
  await run(`${O}fill ${X - 24} ${Y} ${Z - 24} ${X + 24} ${Y} ${Z + 24} minecraft:grass_block`); await run(`${O}fill ${X - 24} ${Y + 1} ${Z - 24} ${X + 24} ${Y + 8} ${Z + 24} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..40]`);
  // (their rigs too - a rig left without its host counts as a faint a moment later, and puts it on its cooldown)
  for (const ab of ['bv', 'mz', 'kt', 'ru', 'hy', 'ni']) { await run(`kill @e[type=minecraft:wolf,tag=bm.${ab}pet]`); await run(`kill @e[type=minecraft:item_display,tag=bm.${ab}p]`); }
  await sleep(1500); for (const ab of ['bv', 'mz', 'kt', 'ru', 'hy', 'ni']) await run(`scoreboard players set TestRat bm.${ab}cd 0`);
  // (every follower an earlier test left with you sent home - three at most may be out)
  const HOME = '/home/user/main/bm_build/out_p2/BlackMarket_DP/data/bm/function/p98/home';
  for (const f of require('fs').readdirSync(HOME)) await run(`${O}execute as TestRat at @s run function bm:p98/home/${f.replace('.mcfunction', '')}`);
  for (const t of ['bv', 'mz', 'kt', 'ru', 'hy', 'ni']) await run(`tag TestRat add bm.${t}met`);
  await run('advancement revoke TestRat only bm:story/cuddle_pile');
  await run('gamerule spawn_mobs false');            // (the night step: nothing of the world's own coming for them while they sleep)
  const items = ['bv_ball', 'capshun_pencil', 'kettle_plane', 'merc_contract', 'henry_tag', 'nia_bell'];
  for (let i = 0; i < items.length; i++) await run(`loot replace entity TestRat hotbar.${i} loot bm:items/${items[i]}`);
  await at(X + 0.5, Y + 1, Z + 0.5);
  A.bars.length = 0; await use(0); await use(1);
  ok('Bender and Mr. Capshun called with their items', await wait(4000, async () => (await cnt(BV)) === 1 && (await cnt(MZ)) === 1), A.bars.join(' | ').slice(0, 200));
  await run(`scoreboard players set ${MZ} bm.rdc 0`);

  // ---------------------------------------------------------------- RIDING BENDER
  ok('calm, the two of them together: Capshun hops up onto Bender\'s back - a real passenger of his', await wait(25000, async () => riding(MZ)));
  await sleep(600);
  ok('...riding (his state 16 - the ride pose)', (await score('bm.zqs', MZ)) === 16, String(await score('bm.zqs', MZ)));
  { const by = await num(BV, 'Pos[1]'), cy = await num(`@e[type=minecraft:item_display,tag=bm.mzp_pet,tag=bm.mzp_body,limit=1]`, 'Pos[1]');
    ok('...his rig seated on Bender\'s back (his body\'s joint over Bender\'s)', cy - by > 0.5 && cy - by < 1.6, (cy - by).toFixed(3)); }
  const bx0 = await num(BV, 'Pos[0]');
  await at(X + 12.5, Y + 1, Z + 0.5, 90);
  ok('you walk off: Bender follows, carrying him', await wait(12000, async () => (await num(BV, 'Pos[0]')) - bx0 > 5 && await riding(MZ)), `bender x ${(await num(BV, 'Pos[0]')).toFixed(1)}`);
  // his Rage: the rider hops off first
  for (const o of ['bm.dqgc', 'bm.dqbc', 'bm.dqrc', 'bm.dqmc']) await run(`scoreboard players set ${BV} ${o} 900`);
  await run(`scoreboard players set ${BV} bm.bvrg 0`);
  await run(`${O}execute at ${BV} run summon minecraft:husk ~4 ~ ~ {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t301z","bm.t301r","bm.seen"],attributes:[{id:"minecraft:max_health",base:300}],Health:300f}`);
  ok('a monster: Bender\'s Rage - and Capshun hops off before it', await wait(5000, async () => (await score('bm.bvrp', BV)) >= 1 && !(await riding(MZ)) && (await cnt(`${MZ.replace('limit=1]', 'tag=!bm.rdr,limit=1]')}`)) === 1));
  ok('...off him, his wits back (no AI of his own only while he rides)', await wait(3000, async () => (await nbt(MZ, 'NoAI')) !== '1b'));
  await run(`${O}kill @e[tag=bm.t301z]`);
  await wait(8000, async () => (await score('bm.bvrp', BV)) <= 0);
  await run(`scoreboard players set ${MZ} bm.rdc 0`);
  ok('calm again: he climbs back on', await wait(25000, async () => riding(MZ)));
  // Kettle and the rat ride him too
  await home('p198'); await sleep(1000);
  ok('Capshun sent home: off Bender, and gone (Bender left standing)', (await cnt(MZ)) === 0 && (await cnt(BV)) === 1 && await wait(2000, async () => (await cnt(`${BV.replace('limit=1]', 'tag=!bm.bvseat,limit=1]')}`)) === 1));
  await at(X + 12.5, Y + 1, Z + 3.5, 90); await use(2);
  await wait(3000, async () => (await cnt(KT)) === 1); await run(`scoreboard players set ${KT} bm.rdc 0`);
  ok('Kettle called: she rides Bender too', await wait(25000, async () => riding(KT)));
  await sleep(500); ok('...in her ride pose (state 16)', (await score('bm.kqs', KT)) === 16);
  await home('p227'); await sleep(800); await use(3);
  await wait(3000, async () => (await cnt(RU)) === 1); await run(`scoreboard players set ${RU} bm.rdc 0`);
  ok('the rat mercenary called: he rides Bender too', await wait(25000, async () => riding(RU)),
     `${await cnt(RU)} out; x ${await score('bm.rgx', RU)} rdc ${await score('bm.rdc', RU)} state ${await score('bm.rgs', RU)}; bender seat ${await cnt(BV.replace('limit=1]', 'tag=bm.bvseat,limit=1]'))}`);
  await sleep(500); ok('...in his ride pose (state 16)', (await score('bm.rgs', RU)) === 16);
  await home('p228'); await sleep(800);

  // ---------------------------------------------------------------- DOG PILE
  await at(X + 0.5, Y + 1, Z + 0.5); await run(`${O}tp ${BV} ${X + 2} ${Y + 1} ${Z + 2}`);
  A.bars.length = 0; await use(4);
  ok('Henry called with his tag', await wait(3000, async () => (await cnt(HY)) === 1), A.bars.join(' | ').slice(0, 200));
  for (const o of ['gc', 'bc', 'rc', 'mc', 'k', 'k2', 'sc']) await run(`scoreboard players set ${HY} bm.hq${o} 900`);
  for (const o of ['bm.dqgc', 'bm.bvrg']) await run(`scoreboard players set ${BV} ${o} 900`);
  await run(`${O}tp ${HY} ${X + 2} ${Y + 1} ${Z + 3}`); await sleep(500);
  await run(`${O}execute at ${BV} run summon minecraft:husk ~5 ~ ~ {NoAI:1b,PersistenceRequired:1b,Tags:["bm.t301z","bm.t301d","bm.seen"],attributes:[{id:"minecraft:max_health",base:300}],Health:300f}`);
  await run(`scoreboard players set ${HY} bm.hqgc 0`);
  let phases = [];
  ok('a monster, Henry\'s charged move ready, Bender beside him: the Dog Pile - he springs onto Bender\'s back',
     await wait(8000, async () => { phases.push(await score('bm.hqdp', HY)); return riding(HY); }, 100), phases.join(','));
  ok('...Bender knows (bm.bvduo): his own charged moves held', (await cnt(`${BV.replace('limit=1]', 'tag=bm.bvduo,limit=1]')}`)) === 1);
  await run(`scoreboard players set ${BV} bm.bvrg 0`); await run(`scoreboard players set ${BV} bm.dqgc 0`);
  let raged = false;
  for (let i = 0; i < 8; i++) { if ((await score('bm.bvrp', BV)) >= 1 || (await score('bm.dqa', BV)) === 12 && (await score('bm.dqx', BV)) >= 1) raged = true; await sleep(250); }
  ok('...while Henry rides into the fight, no Rage, no Good Boy!', !raged);
  ok('...and the monster takes it - swipes from up there, and the finish', await wait(10000, async () => (await num('@e[tag=bm.t301d,limit=1]', 'Health')) < 290),
     String(await num('@e[tag=bm.t301d,limit=1]', 'Health')));
  ok('...the finish: off his back, onto it - and the double act over (Henry\'s wits back, Bender\'s moves his own again)',
     await wait(12000, async () => (await score('bm.hqdp', HY)) === 0 && !(await riding(HY)) && (await nbt(HY, 'NoAI')) !== '1b' &&
       (await cnt(`${BV.replace('limit=1]', 'tag=bm.bvduo,limit=1]')}`)) === 0));
  await run(`${O}kill @e[tag=bm.t301z]`); await sleep(1500);

  // ---------------------------------------------------------------- THE NIGHT CUDDLE
  await use(5); await wait(3000, async () => (await cnt(NI)) === 1);
  await run(`${O}time set midnight`); await run(`${O}kill @e[type=#bm:hostile,x=${X},y=${Y},z=${Z},distance=..48]`); await wait(8000, async () => (await score('bm.bvrp', BV)) <= 0 && (await score('bm.dqx', BV)) <= 0);
  await at(X + 0.5, Y + 1, Z + 0.5); A.chats.length = 0;
  for (const s of [BV, HY, NI]) await run(`${O}tp ${s} ${X + 2.5} ${Y + 1} ${Z + 2.5}`);
  for (const o of ['gc', 'bc', 'rc', 'mc', 'k', 'k2', 'sc']) { await run(`scoreboard players set ${HY} bm.hq${o} 900`); await run(`scoreboard players set ${NI} bm.nq${o} 900`); }
  await run(`scoreboard players set ${BV} bm.cdlw 0`);
  ok('night, the three of them calm, you by: in time they lie down together', await wait(150000, async () => (await cnt('@e[type=minecraft:wolf,tag=bm.cdl]')) === 3, 1000));
  await sleep(1500);
  ok('...Bender asleep (state 17), and the cats curled up (17)', (await score('bm.dqs', BV)) === 17 && (await score('bm.hqs', HY)) === 17 && (await score('bm.nqs', NI)) === 17,
     [await score('bm.dqs', BV), await score('bm.hqs', HY), await score('bm.nqs', NI)].join(' '));
  { const bx = await num(BV, 'Pos[0]'), bz = await num(BV, 'Pos[2]'), by = await num(BV, 'Rotation[0]');
    const d = async (s) => Math.hypot((await num(s, 'Pos[0]')) - bx, (await num(s, 'Pos[2]')) - bz);
    const turn = async (s) => { const a = ((await num(s, 'Rotation[0]')) - by) % 360; return Math.min(Math.abs(a), 360 - Math.abs(a)); };
    const dh = await d(HY), dn = await d(NI), th = await turn(HY), tn = await turn(NI);
    ok('...the cats one either side of him, pressed close (within 0.7)', dh < 0.7 && dn < 0.7, `${dh.toFixed(2)} ${dn.toFixed(2)}`);
    ok('...all three facing the same way', th < 2 && tn < 2, `${th.toFixed(1)} ${tn.toFixed(1)}`); }
  ok('...and you\'re told so (and the advancement)', A.chats.some(c => /asleep in moments/.test(c)) &&
     (await cnt('@a[name=TestRat,advancements={bm:story/cuddle_pile=true}]')) === 1, A.chats.slice(-1).join('').slice(0, 120));
  await sleep(3000);
  ok('...they stay put, asleep, while you stay', (await cnt('@e[type=minecraft:wolf,tag=bm.cdl]')) === 3);
  await at(X + 20.5, Y + 1, Z + 0.5);
  ok('you walk off: they wake - up, their wits back', await wait(5000, async () => (await cnt('@e[type=minecraft:wolf,tag=bm.cdl]')) === 0 &&
     (await nbt(BV, 'NoAI')) !== '1b' && (await nbt(HY, 'NoAI')) !== '1b' && (await nbt(NI, 'NoAI')) !== '1b'),
     [await cnt('@e[type=minecraft:wolf,tag=bm.cdl]'), await nbt(BV, 'NoAI'), await nbt(HY, 'NoAI'), await nbt(NI, 'NoAI')].join(' '));
  ok('...and they come after you', await wait(12000, async () => Math.abs((await num(BV, 'Pos[0]')) - (X + 20.5)) < 8));

  // ---------------------------------------------------------------- tidy
  for (const pfx of ['p195', 'p229', 'p230']) await home(pfx);
  await run(`${O}time set noon`); await run(`${O}kill @e[tag=bm.t301z]`); await run('gamerule spawn_mobs true');
  await run(`${O}forceload remove ${X - 32} ${Z - 32} ${X + 32} ${Z + 32}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

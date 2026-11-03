// 3.0g: FRIENDLY STATUE KNIGHTS (phase245's home knights; phase82's Hearthfire, phase127's Wraithfire Heart, phase60's Ethereal
// Gem) as a regular (non-op) player. rcon sets the stage (a field, a husk to compare with, a shrine of the Gem) and reads tags and
// fire; the bot plays: it sets a Dread Sentinel's statue up, wakes it with its dialog's buttons, sets the Scorching Heart down, strikes
// while Ethereal, right-clicks and sneak + right-clicks the KNIGHT itself, duels it carrying a Wraithfire Heart.
//   hearth   a guard beside a Hearthfire: never alight - while a husk the same Hearthfire reaches burns
//   eth      Ethereal (the Gem's shrine near), a blow on the guard: it is never marked for an element (bm.etv) - a blow on the husk is
//   click    the guard carries a click box (bm.kcb); its owner right-clicks the knight: its dialog, "Rest" - stone on its plinth again;
//            woken again, sneak + right-clicked: the statue back in the pack, the plinth gone, nothing of the knight left
//   parts    woken again and its host killed outright (/kill - no fall): within seconds no rig part, no click box left - its plinth
//            stone again (the statue shown); and an orphaned part (no knight, no statue) swept within 4 s
//   wraith   duelling it with a Wraithfire Heart in the pack, stood beside it: it is never seared alight - the husk beside you is
//   node t344.js [hearth|eth|click|parts|wraith]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const X = 18800, Y = 100, Z = 16400;
const O = 'execute in minecraft:overworld run ';

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`${O}scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (sel) => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const fire = async (sel) => +(((await run(`${O}data get entity ${sel} Fire`)).match(/(-?\d+)s?$/) || [0, -1])[1]);
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(4000, async () => A.pos && Math.abs(A.pos.x - x) < 0.2 && Math.abs(A.pos.z - z) < 0.2, 100); await sleep(400); };
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const near = (r = 14) => `x=${X},y=${Y},z=${Z},distance=..${r}`;
  const ST = `@e[type=minecraft:interaction,tag=bm.knst_dread,${near(4)},limit=1]`;
  const GUARD = `@e[type=minecraft:husk,tag=bm.khome,tag=bm.kguard,${near(20)},limit=1]`;
  const DUEL = `@e[type=minecraft:husk,tag=bm.khome,tag=bm.kduel,${near(30)},limit=1]`;
  const BOX = `@e[type=minecraft:interaction,tag=bm.kcb,${near(20)},limit=1]`;
  const PARTS = `@e[type=minecraft:item_display,tag=bm.kr,${near(30)}]`;
  const HUSK = '@e[type=minecraft:husk,tag=bm.t344h,limit=1]';
  const husk = async (x, z) => { await run(`${O}kill @e[type=minecraft:husk,tag=bm.t344h]`);
    await run(`${O}summon minecraft:husk ${x} ${Y} ${z} {NoAI:1b,Silent:1b,PersistenceRequired:1b,Tags:["bm.t344h","bm.seen"],attributes:[{id:"minecraft:max_health",base:200.0d}],Health:200f}`); };
  const place = async () => {      // (the statue set up at the field's centre, sneak + used on the block)
    await at(X + 0.5, Y, Z - 0.5, 0, 60); await run('clear TestRat');
    await run('loot replace entity TestRat hotbar.0 loot bm:items/knight_statue_dread'); A.slot(0); await sleep(400);
    A.input({ shift: true }); await sleep(200); A.use(); await sleep(400); A.release(); await sleep(300); A.input({}); await sleep(800);
    return (await cnt(ST)) === 1;
  };
  const dialog = async (sel, sneak = false) => { const e = await entOf(sel); if (!e) return false; const n0 = A.dialogN.length;
    A.interact(e.entityId, sneak); return wait(3000, async () => A.dialogN.length > n0, 100); };
  const wake = async (btn) => { await at(X + 0.5, Y, Z - 2.5, 0, 10); if (!(await dialog(ST))) return false; await A.press(btn); await sleep(2500); return true; };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('scoreboard players set #hard bm.cfg 1'); await run(`${O}time set 18000`); await run('difficulty normal');
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`); await sleep(2500);
  await run(`${O}fill ${X - 16} ${Y} ${Z - 16} ${X + 16} ${Y + 8} ${Z + 16} minecraft:air`); await run(`${O}fill ${X - 16} ${Y - 1} ${Z - 16} ${X + 16} ${Y - 1} ${Z + 16} minecraft:stone`);
  await run(`${O}kill @e[type=minecraft:interaction,tag=bm.knst,${near(24)}]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.knsd,${near(24)}]`);
  await run(`${O}kill @e[type=minecraft:interaction,tag=bm.hearth,${near(24)}]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.hearthd,${near(24)}]`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:fire_resistance infinite 0 true');

  ok('a Dread Sentinel\'s statue set up at home', await place());
  ok('..."Stand guard": it wakes as a guard', await wake(/Stand guard/) && await wait(4000, async () => (await cnt(GUARD)) === 1));

  if (on('hearth')) {
    // (the Scorching Heart set down 6 south of the plinth - the guard by it, a husk 12 off the plinth, 6 the other side of the hearth)
    await at(X + 0.5, Y, Z - 7.5, 180, 70); await run('loot replace entity TestRat hotbar.1 loot bm:items/scorching_heart'); A.slot(1); await sleep(400);
    A.input({ shift: true }); await sleep(200); A.use(); await sleep(400); A.release(); await sleep(300); A.input({}); await sleep(800);
    ok('a Hearthfire set down by the guard (sneak + use)', (await cnt(`@e[type=minecraft:interaction,tag=bm.hearth,${near(10)}]`)) === 1);
    await husk(X + 0.5, Z - 11.5);
    let lit = 0;
    const seen = await wait(6000, async () => { if ((await fire(GUARD)) > 0) lit++; return (await fire(HUSK)) > 0; }, 200);
    ok('...a husk it reaches is set alight', seen, String(await fire(HUSK)));
    await sleep(2000); if ((await fire(GUARD)) > 0) lit++;
    ok('...the guard by it never is', lit === 0, `${lit} samples alight`);
    await run(`${O}kill @e[type=minecraft:husk,tag=bm.t344h]`);
    await run(`${O}execute as @e[type=minecraft:interaction,tag=bm.hearth,${near(14)}] at @s run kill @e[type=minecraft:item_display,tag=bm.hearthd,distance=..0.6]`);
    await run(`${O}kill @e[type=minecraft:interaction,tag=bm.hearth,${near(14)}]`);
  }

  if (on('eth')) {
    await run(`${O}execute positioned ${X - 8.5} ${Y} ${Z - 8.5} run function bm:p60/spawn/ethereal`);
    await at(X + 0.5, Y, Z - 1.6, 0, 10);
    ok('the Ethereal Gem\'s shrine near: TestRat is Ethereal (bm.eth)', await wait(3000, async () => /bm\.eth\b/.test(await run('tag TestRat list'))));
    await run('item replace entity TestRat weapon.mainhand with minecraft:stick'); A.slot(0); await sleep(1300);
    const watchMark = async (sel) => { const e = await entOf(sel); if (!e) return null; A.attack(e.entityId); let m = false;
      await wait(1500, async () => { if (/bm\.etv/.test(await run(`${O}tag ${sel} list`))) m = true; return m; }, 50); return m; };
    const gp = await pos(GUARD); if (gp) await at(gp[0], gp[1], gp[2] - 1.6, 0, 10);
    await run('scoreboard players set TestRat bm.etcd 0');
    ok('...an Ethereal blow on the guard: it is never marked for an element', (await watchMark(GUARD)) === false);
    await husk(X + 0.5, Z - 13.5); await at(X + 0.5, Y, Z - 15.1, 0, 10); await sleep(1300);
    await run('scoreboard players set TestRat bm.etcd 0');
    ok('...an Ethereal blow on a husk: marked (bm.etv) - the element strikes', (await watchMark(HUSK)) === true);
    await run(`${O}kill @e[type=minecraft:husk,tag=bm.t344h]`); await run(`${O}kill @e[tag=bm.eshr,${near(30)}]`); await run(`${O}kill @e[tag=bm.eshr_hit,${near(30)}]`);
    await run('clear TestRat'); await sleep(1500);
  }

  if (on('click')) {
    ok('the guard carries a click box (bm.kcb) where it stands', await wait(3000, async () => { const b = await pos(BOX), g = await pos(GUARD);
      return b && g && Math.hypot(b[0] - g[0], b[2] - g[2]) < 0.3; }));
    const gp = await pos(GUARD); await at(gp[0], gp[1], gp[2] - 2.2, 0, 10);
    ok('...right-clicking the KNIGHT: its dialog ("Rest")', await dialog(BOX) && A.buttons().some(b => /Rest/.test(b.label)), JSON.stringify(A.buttons().map(b => b.label)));
    await A.press(/Rest/);
    ok('..."Rest": stone on its plinth again (no host, no box, bm.kgm 0)', await wait(10000, async () => (await cnt(GUARD)) === 0 && (await cnt(BOX)) === 0) && (await sc(ST, 'bm.kgm')) === 0);
    ok('woken again', await wake(/Stand guard/) && await wait(4000, async () => (await cnt(GUARD)) === 1 && (await cnt(BOX)) === 1));
    const g2 = await pos(GUARD); await at(g2[0], g2[1], g2[2] - 2.2, 0, 10);
    const b = await entOf(BOX); A.input({ shift: true }); await sleep(300); if (b) A.interact(b.entityId, true); await sleep(900); A.input({}); await sleep(600);
    ok('...sneak + right-clicking the knight: its statue back in your pack', (await has('knight_statue_dread')) === 1);
    ok('...its plinth gone, and nothing of it left (no host, no box, no part)', await wait(4000, async () => (await cnt(ST)) === 0 && (await cnt(GUARD)) === 0 &&
       (await cnt(BOX)) === 0 && (await cnt(PARTS)) === 0), `plinth ${await cnt(ST)} host ${await cnt(GUARD)} box ${await cnt(BOX)} parts ${await cnt(PARTS)}`);
    ok('set up again, "Stand guard" again', await place() && await wake(/Stand guard/) && await wait(4000, async () => (await cnt(GUARD)) === 1));
  }

  if (on('parts')) {
    if ((await cnt(GUARD)) === 0) { await place(); await wake(/Stand guard/); }
    ok('a guard on watch: its rig whole', await wait(4000, async () => (await cnt(PARTS)) >= 13));
    await run(`${O}kill ${GUARD}`);
    ok('its host killed outright (/kill): no rig part, no click box left within seconds', await wait(8000, async () => (await cnt(PARTS)) === 0 && (await cnt(BOX)) === 0),
       `parts ${await cnt(PARTS)} box ${await cnt(BOX)}`);
    ok('...and its plinth stone again, the statue shown (bm.kgm 0)', await wait(8000, async () => (await sc(ST, 'bm.kgm')) === 0 &&
       /scale: \[1\.0f/.test(await run(`${O}data get entity @e[type=minecraft:item_display,tag=bm.knsd_dread,${near(4)},limit=1] transformation`))));
    await run(`${O}summon minecraft:item_display ${X + 4.5} ${Y} ${Z + 4.5} {Tags:["bm.kr","bm.kr_head"],item:{id:"minecraft:stone",count:1}}`);
    await run(`${O}scoreboard players set @e[type=minecraft:item_display,tag=bm.kr,${near(20)}] bm.kid 999999`);
    ok('a stray rig part (no knight, no statue of its kid): swept within 4 s', await wait(6000, async () => (await cnt(PARTS)) === 0));
  }

  if (on('wraith')) {
    if ((await cnt(GUARD)) === 1) { await at(X + 0.5, Y, Z - 2.5, 0, 10); if (await dialog(ST)) await A.press(/Rest/); await wait(10000, async () => (await cnt(GUARD)) === 0); }
    if ((await cnt(ST)) === 0) await place();
    await run('clear TestRat'); await run('loot replace entity TestRat inventory.0 loot bm:items/wraithfire_heart');
    ok('"Duel me", a Wraithfire Heart in the pack: it wakes against you', await wake(/Duel me/) && await wait(4000, async () => (await cnt(DUEL)) === 1));
    const dp = await pos(DUEL); await husk(dp[0] - 1.5, dp[2] - 2.5); await at(dp[0], dp[1], dp[2] - 1.6, 0, 10);
    let lit = 0;
    const seen = await wait(6000, async () => { const p = await pos(DUEL); if (p) await run(`${O}tp TestRat ${p[0]} ${p[1]} ${p[2] - 1.6}`); if ((await fire(DUEL)) > 0) lit++; return (await fire(HUSK)) > 0; }, 300);
    ok('...the husk beside you is seared alight', seen, String(await fire(HUSK)));
    for (let i = 0; i < 8; i++) { const p = await pos(DUEL); if (p) await run(`${O}tp TestRat ${p[0]} ${p[1]} ${p[2] - 1.6}`); await sleep(250); if ((await fire(DUEL)) > 0) lit++; }
    ok('...the knight you duel, never', lit === 0, `${lit} samples alight`);
    await run(`${O}kill @e[type=minecraft:husk,tag=bm.t344h]`); await run(`${O}execute as ${DUEL} at @s run function bm:p245/h/stone`); await run('clear TestRat');
  }

  // (leave the field as found: the statue taken back up)
  await run(`${O}execute as @e[type=minecraft:husk,tag=bm.khome,${near(30)}] at @s run function bm:p245/h/stone`); await sleep(1500);
  await run(`${O}kill @e[type=minecraft:interaction,tag=bm.knst,${near(24)}]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.knsd,${near(24)}]`);
  await run(`${O}kill @e[type=minecraft:husk,tag=bm.t344h]`); await run('clear TestRat'); await run('effect clear TestRat');
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

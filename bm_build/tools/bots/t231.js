// 2.85d: SEVEN NEW FIGHTS - as a regular (non-op) player TestRat, every heist planned through the Ledger and begun with the den's
// button (rcon sets the stage: Tokens, the Ledger, heists of one kind of room, where TestRat stands, and the guards' health - the
// fights are won by killing what each wave brings, a blow from TestRat's own sword among them).
//   each room: walked into, it springs - its door barred, its own kind of foe out; wave after wave until it's won, then the
//   exit opens and the door unbars.
//   THE STRONGROOM SIEGE: the Teller on his strongbox; safecrackers at the box drain its bar - cracked, it costs a try and the
//     siege starts over (the door unbarred, then barred again as TestRat is still inside).
//   THE SINKING VAULT: squares of the floor give way during the fight; down in the hay pit: back at the door. Won: the floor mended.
//   THE HOG PENS: vault boars (hoglins), then the Swineherd. THE CROSSFIRE GALLERY: archers up on the balconies.
//   THE HALL OF MIRRORS: guards, then the Mirror Thief (an illusioner). THE SPIDER LARDER: spiders from the ceiling, then the
//   Broodmother. THE FLOODED VAULT: the drowned, then the Drowned Bailiff.
//   the whole crew out of a fight for ten seconds: it starts over (nobody locked out).
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
const ONLY = process.argv[2];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found )(-?\d+)/) || [0, -1])[1]);
  const G = 'execute in bm:gutter run ';
  const passes = async c => /passed/i.test(await run(c));
  const cnt = async sel => { const m = (await run(`${G}execute if entity ${sel}`)).match(/Count: (\d+)/); return m ? +m[1] : 0; };
  const uuidEnt = async sel => { const m = (await run(`${G}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
    const e = Object.values(A.ents).find(e => e.objectUUID === u); return e ? e.entityId : null; };

  const A = await bot('TestRat'); await sleep(2500); A.stand();
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(700);
  ok('TestRat is a regular player', /unknown|incomplete|permission/i.test(A.chats.join(' ')));
  for (const f of ['plan_anywhere', 'heist_variants_never', 'prime_never', 'fork_never', 'traps_never', 'curse_never']) await run(`function bm:admin/${f}`);
  await run('execute in minecraft:overworld run fill 12996 119 12996 13004 119 13004 stone');
  const gvi = () => num('scoreboard players get TestRat bm.gvi');

  const KINDS = ONLY ? [ONLY] : ['siege', 'sink', 'pens', 'crossfire', 'mirror', 'larder', 'flood'];
  const FOE = { pens: 'minecraft:hoglin', crossfire: 'minecraft:skeleton', larder: 'minecraft:spider', flood: 'minecraft:drowned', siege: 'minecraft:vindicator',
                sink: 'minecraft:vindicator', mirror: 'minecraft:vindicator' };
  const BOSS = { pens: 'minecraft:piglin_brute', mirror: 'minecraft:evoker', larder: 'minecraft:spider', flood: 'minecraft:drowned', crossfire: 'minecraft:skeleton' };
  for (const K of KINDS) {
    // ---- the stage: no heist running; Tokens, the Ledger; heists of this one kind of room
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run(`function bm:admin/fight_${K}`);
    await run('clear TestRat'); await run('gamemode survival TestRat'); await run('effect give TestRat resistance 900 4 true'); await run('effect give TestRat saturation 900 0 true');
    await run('tag TestRat remove bm.gvp'); await run('scoreboard players reset TestRat bm.gvi'); await run('scoreboard players set TestRat bm.gvhc 0');
    await run('execute as TestRat unless score @s bm.pid matches 1.. run function bm:p21/pid');
    await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
    for (let k = 0; k < 16; k++) await run('loot give TestRat loot bm:items/token');
    await run('scoreboard players set TestRat bm.gvu 5'); await run('scoreboard players set TestRat bm.gval 0');
    await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger');
    await sleep(2000);
    // ---- the Ledger: Plan a Heist, Tier III, 7 tries (the buttons as sent)
    A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(900);
    A.cmd('trigger bm.act set 7603'); await sleep(1500); A.cmd('trigger bm.act set 7613');
    const inH = await wait(40000, async () => passes('execute if entity @a[name=TestRat,tag=bm.gvp]'), 500); await sleep(2500);
    const GI = await gvi();
    const LB = `@e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${GI}},limit=1]`;
    const inst = `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI}},limit=1]`;
    const lp = (await run(`${G}data get entity ${LB} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    if (!inH || !lp) { ok(`${K}: a heist planned through the Ledger`, false, `in ${inH} gvi ${GI}`); continue; }
    const [bx, by, bz] = [Math.floor(+lp[1]) + 11, Math.floor(+lp[2]) + 1, Math.floor(+lp[3]) + 3];
    await run(`execute in bm:gutter as ${LB} at @s run tp TestRat ~10 ~ ~3 -90 0`); await sleep(1500);
    A.useOn(bx, by, bz, 4); await sleep(2500);
    if ((await num(`${G}scoreboard players get ${inst} bm.gvst`)) < 2) A.useOn(bx, by, bz, 4);
    const begun = await wait(8000, async () => (await num(`${G}scoreboard players get ${inst} bm.gvst`)) >= 2);
    const room = `@e[type=minecraft:marker,tag=bm.gvr_${K},scores={bm.gvi=${GI}},sort=nearest,limit=1]`;
    const rp = (await run(`${G}execute at ${LB} run data get entity ${room} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    ok(`${K}: planned through the Ledger, begun at the den's button - the first room is ${K}`, begun && !!rp, `gvi ${GI} begun ${begun}`);
    if (!rp) continue;
    const [rx, ry, rz] = rp.slice(1).map(Number);
    const room1 = `@e[type=minecraft:marker,tag=bm.gvr_${K},x=${rx},y=${ry},z=${rz},distance=..1,limit=1]`;
    const at = `execute in bm:gutter positioned ${rx} ${ry} ${rz} run `;
    const gv = `@e[tag=bm.gvg,scores={bm.gvi=${GI}},x=${rx},y=${ry},z=${rz},distance=..22]`;
    const sc = o => num(`${G}scoreboard players get ${room1} ${o}`);
    const barred = () => passes(`${at}execute if block ~-12 ~ ~ minecraft:iron_bars`);

    // ---- in: it springs
    A.chats.length = 0; A.bars.length = 0;
    await run(`${at}tp TestRat ~-8.5 ~ ~0.5 -90 0`); await sleep(500); A.stand();
    const sprung = await wait(5000, async () => (await sc('bm.gvs')) === 1);
    await sleep(1500);
    ok(`${K}: walked in, it springs - the door barred, its foes out (${FOE[K]})`, sprung && (await barred()) && (await cnt(`@e[type=${FOE[K]},scores={bm.gvi=${GI}},x=${rx},y=${ry},z=${rz},distance=..22]`)) >= 1,
       `gvs ${await sc('bm.gvs')} barred ${await barred()} foes ${await cnt(gv)}`);

    // ---- each room's own trick
    if (K === 'siege') {
      ok('siege: the Teller on his strongbox, its bar above', (await cnt(`@e[type=minecraft:villager,tag=bm.gvteller,x=${rx},y=${ry},z=${rz},distance=..20]`)) === 1 &&
         /STRONGBOX/.test(await run(`${G}data get entity @e[type=minecraft:text_display,tag=bm.gvsbox,x=${rx},y=${ry},z=${rz},distance=..20,limit=1] text`)));
      const lv0 = await num(`${G}scoreboard players get ${inst} bm.gvlv`);
      // (the stage: the guards gone, the safecrackers stood at the box)
      await run(`${G}kill @e[tag=bm.gvg,tag=!bm.gvsc,scores={bm.gvi=${GI}}]`);
      await run(`${at}execute as @e[tag=bm.gvsc,distance=..22] run data merge entity @s {NoAI:1b}`);
      await run(`${at}tp @e[tag=bm.gvsc,distance=..22] ~ ~1 ~-8.5`);
      const hp0 = await sc('bm.gvc');
      await sleep(3500);
      const hp1 = await sc('bm.gvc');
      ok('siege: safecrackers at the strongbox wear its bar down', hp1 < hp0 && hp1 >= 0, `${hp0} -> ${hp1}`);
      await run(`${G}scoreboard players set ${room1} bm.gvc 1`);
      const cracked = await wait(5000, async () => (await num(`${G}scoreboard players get ${inst} bm.gvlv`)) === lv0 - 1);
      ok('siege: cracked - it costs a try, and the siege starts over around TestRat', cracked && A.chats.concat(A.bars).some(c => /CRACKED|cost a try|try/i.test(c)) &&
         await wait(4000, async () => (await sc('bm.gvs')) === 1), `tries ${lv0} -> ${await num(`${G}scoreboard players get ${inst} bm.gvlv`)} gvs ${await sc('bm.gvs')}`);
    }
    if (K === 'sink') {
      const dropped = await wait(9000, async () => (await cnt(`@e[type=minecraft:marker,tag=bm.gvskb,x=${rx},y=${ry},z=${rz},distance=..22]`)) >= 1);
      ok('sink: a square of the floor gives way during the fight', dropped);
      A.bars.length = 0;
      await run(`${at}tp TestRat ~-8.5 ~-3 ~-9.5`); await sleep(1500);
      const back = await passes(`${at}execute positioned ~-12 ~ ~-2 if entity @a[name=TestRat,dx=2,dy=3,dz=4]`);
      ok('sink: down in the hay pit - back at the door', back && A.bars.some(b => /hay/i.test(b)), `${A.bars.slice(-1).join('')} | ${await run('data get entity TestRat Pos')} room ${rx} ${ry} ${rz}`);
      await run(`${at}tp TestRat ~-8.5 ~ ~0.5 -90 0`);
    }
    if (K === 'crossfire') {
      ok('crossfire: archers up on the balconies', (await cnt(`@e[type=minecraft:skeleton,scores={bm.gvi=${GI}},x=${rx - 12},y=${ry + 4.5},z=${rz - 12},dx=24,dy=3,dz=24]`)) >= 2);
    }

    // ---- (2.85d) a fire lit beside TestRat in the heist goes out by itself - raiders in adventure mode can't punch it out
    if (K === KINDS[0]) {
      await run(`${G}execute at TestRat run setblock ~2 ~-1 ~ minecraft:netherrack`); await run(`${G}execute at TestRat run setblock ~2 ~ ~ minecraft:fire`);
      const lit = await passes(`${G}execute at TestRat if block ~2 ~ ~ minecraft:fire`);
      ok(`${K}: a fire lit beside TestRat in the heist goes out by itself`, lit && await wait(3000, async () => !(await passes(`${G}execute at TestRat if block ~2 ~ ~ minecraft:fire`))), `lit ${lit}`);
    }

    // ---- a blow of TestRat's own: one foe brought low and struck with a real swing
    await run('item replace entity TestRat hotbar.0 with minecraft:netherite_sword'); A.slot(0); await sleep(300);
    const tgt = `@e[tag=bm.gvg,scores={bm.gvi=${GI}},x=${rx},y=${ry},z=${rz},distance=..22,sort=random,limit=1]`;
    await run(`${G}tag ${tgt} add bm.t231`);
    await run(`${G}execute as @e[tag=bm.t231] run data merge entity @s {Health:1f,NoAI:1b}`);
    await run(`${G}execute at @e[tag=bm.t231,limit=1] run tp TestRat ^ ^ ^-1.6 facing entity @e[tag=bm.t231,limit=1]`); await sleep(700);
    const te = await uuidEnt('@e[tag=bm.t231,limit=1]');
    if (te) { A.attack(te); await sleep(600); A.attack(te); }
    ok(`${K}: TestRat strikes one down with a real swing`, await wait(3000, async () => (await cnt('@e[tag=bm.t231]')) === 0), `eid ${te}`);
    await run(`${at}tp TestRat ~-8.5 ~ ~0.5 -90 0`);

    // ---- the waves (the stage: each wave's foes killed by rcon once out) until it's won
    let waves = new Set([await sc('bm.gvw')]), boss = false;
    const t0 = Date.now();
    while ((await sc('bm.gvs')) === 1 && Date.now() - t0 < 90000) {
      await sleep(1200);
      waves.add(await sc('bm.gvw'));
      if (BOSS[K] && (await cnt(`@e[type=${BOSS[K]},tag=bm.gvcap,scores={bm.gvi=${GI}},x=${rx},y=${ry},z=${rz},distance=..22]`)) >= 1) boss = true;
      if (K === 'crossfire' && (await cnt(`@e[type=minecraft:skeleton,scores={bm.gvi=${GI}},x=${rx},y=${ry},z=${rz},distance=..22]`)) >= 1) boss = true;
      await run(`${G}execute as ${gv} at @s run tp @s ~ -300 ~`); await run(`${G}kill @e[tag=bm.gvg,scores={bm.gvi=${GI}},y=-400,dy=200]`);
      await run(`${G}kill ${gv}`);
    }
    const won = (await sc('bm.gvs')) >= 2;
    await sleep(1500);
    const exitOpen = !(await passes(`${at}execute if block ~12 ~ ~ minecraft:iron_bars`));
    ok(`${K}: wave after wave (${[...waves].sort().join(',')})${BOSS[K] ? ' and its boss' : ''} - won: the exit opens`, won && waves.size >= 2 && exitOpen && (!BOSS[K] || boss),
       `gvs ${await sc('bm.gvs')} exit ${exitOpen} boss ${boss}`);
    if (K === 'sink') ok('sink: won - the floor mended', (await cnt(`@e[type=minecraft:marker,tag=bm.gvskb,x=${rx},y=${ry},z=${rz},distance=..22]`)) === 0);
    if (K === 'larder') {
      // ---- everyone out for ten seconds: a fresh fight starts over (another larder down the line)
      const r2 = `@e[type=minecraft:marker,tag=bm.gvr_larder,scores={bm.gvi=${GI},bm.gvs=0},sort=nearest,limit=1]`;
      const p2 = (await run(`${G}execute at ${room1} run data get entity ${r2} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
      if (p2) {
        const at2 = `execute in bm:gutter positioned ${p2[1]} ${p2[2]} ${p2[3]} run `;
        const s2q = () => num(`${G}execute positioned ${p2[1]} ${p2[2]} ${p2[3]} run scoreboard players get @e[type=minecraft:marker,tag=bm.gvr_larder,distance=..1,limit=1] bm.gvs`);
        await run(`${at2}tp TestRat ~-8.5 ~ ~0.5 -90 0`);
        const s2 = (await wait(8000, async () => (await s2q()) === 1)) ? 1 : await s2q();
        await run(`${at2}tp TestRat ~-30 ~ ~0.5`); await sleep(12000);         // (out of reach: the room doesn't tick - the gap is counted on return)
        await run(`${at2}tp TestRat ~-17.5 ~ ~0.5 -90 0`);                      // (back in the corridor, short of the fight)
        const reset = (await wait(8000, async () => (await s2q()) === 0, 500)) ? 0 : await s2q();
        const unbarred = !(await passes(`${at2}execute if block ~-12 ~ ~ minecraft:iron_bars`));
        ok('larder: the crew out of a fight for ten seconds - it starts over, the door unbarred', s2 === 1 && reset === 0 && unbarred, `sprung ${s2} after ${reset} unbarred ${unbarred} at ${p2.slice(1).join(' ')}`);
      }
    }
  }

  // ---- put things back
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('function bm:admin/rooms_any');
  await run('tag TestRat remove bm.gvp'); await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  await run('clear TestRat'); await run('effect clear TestRat'); await run('gamemode creative TestRat');
  const n = res.filter(Boolean).length; console.log(`\n${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

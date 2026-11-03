// 3.0g: THE DREAD MIRE AND THE STATUE KNIGHTS, HARDER (hitcap.py on mirekit/phase246 and phase245) as a regular (non-op) player. rcon sets
// the stage (the night, a field, a Mire set down in front of TestRat, the Sovereign's Edge and Strength C in hand, armour on) and reads
// health; the bot plays: it walks up to the Mire (it rises for it), strikes it with the final boss's sword, sets a Dread Sentinel's
// statue up at home, right-clicks it and presses "Duel me", strikes the knight and stands in its reach.
//   mire     risen, the Mire is under the cap (bm.hcap, 20): a Strength C blow of the Edge takes at most 20, the next the same
//   knight   duelled at home, the Dread Sentinel is under the cap (20; 420 health over its floor, armour 16): a Strength C blow takes
//            at most 20; in Protection IV netherite with no Resistance its slam still lands heavy (one hit of 7+: Dread, past armour
//            and its enchantments - the old mace blow came through at under 2); the duel walked away from, the statue taken back
//   node t343.js [mire|knight]
const { bot, rcon, sleep } = require('./lib_resp');
const ONLY = process.argv[2];
const on = (s) => !ONLY || ONLY === s;
const X = 18700, Y = 100, Z = 16300;
const O = 'execute in minecraft:overworld run ';
const CAP = 20, FLOOR = 100;

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`${O}scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const pos = async (sel) => { const m = (await run(`${O}data get entity ${sel} Pos`)).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
  const hpOf = async (sel) => +(((await run(`${O}data get entity ${sel} Health`)).match(/(-?[\d.]+)f?$/) || [0, NaN])[1]);
  const hp = () => hpOf('@a[name=TestRat,limit=1]');
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const at = async (x, y, z, yaw = 0, pitch = 0) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`);
    await wait(4000, async () => A.pos && Math.abs(A.pos.x - x) < 0.2 && Math.abs(A.pos.z - z) < 0.2, 100); await sleep(400); };
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const edge = async () => { await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/sov_edge'); A.slot(0);
    await run('effect give TestRat minecraft:strength 120 100 true'); await sleep(1400); };
  const strike = async (sel) => { const e = await entOf(sel); if (!e) return null; const h0 = await hpOf(sel); A.attack(e.entityId); await sleep(250); return h0 - (await hpOf(sel)); };

  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  const dfell = await sc('#dfell', 'bm.cfg');
  await run('scoreboard players set #dfell bm.cfg 0'); await run('scoreboard players set #hard bm.cfg 1'); await run(`${O}time set 18000`); await run('difficulty normal');
  await run(`${O}forceload add ${X - 24} ${Z - 24} ${X + 24} ${Z + 24}`); await sleep(2500);
  await run(`${O}fill ${X - 14} ${Y} ${Z - 14} ${X + 14} ${Y + 10} ${Z + 14} minecraft:air`); await run(`${O}fill ${X - 14} ${Y - 1} ${Z - 14} ${X + 14} ${Y - 1} ${Z + 14} minecraft:stone`);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run('effect give TestRat minecraft:resistance infinite 4 true'); await run('effect give TestRat minecraft:instant_health 1 4 true');

  if (on('mire')) {
    const MIRE = `@e[type=minecraft:husk,tag=bm.mire,x=${X},y=${Y},z=${Z},distance=..12,limit=1]`;
    await run(`${O}execute as @e[type=minecraft:husk,tag=bm.mire,x=${X},y=${Y},z=${Z},distance=..20] at @s run function bm:p246/melt`);
    await at(X + 0.5, Y, Z - 8.5, 0, 0);
    await run(`${O}execute positioned ${X + 0.5} ${Y} ${Z + 0.5} run function bm:p246/spawn`);
    ok('a Dread Mire set down (dormant): under the hit cap (bm.hcap, 20)', await wait(3000, async () => (await cnt(MIRE)) === 1) &&
       /bm\.hcap/.test(await run(`${O}tag ${MIRE} list`)) && (await sc(MIRE, 'bm.hcc')) === CAP * 10);
    await A.walkTo(X + 0.5, Z - 3.5);
    ok('...walked up to: it rises', await wait(8000, async () => (await sc(MIRE, 'bm.ms')) >= 2 && !/1b/.test(await run(`${O}data get entity ${MIRE} Invulnerable`))), `ms ${await sc(MIRE, 'bm.ms')}`);
    ok('...armour 16, toughness 10', /16\.0/.test(await run(`${O}attribute ${MIRE} minecraft:armor base get`)) && /10\.0/.test(await run(`${O}attribute ${MIRE} minecraft:armor_toughness base get`)));
    await edge();
    const mp = await pos(MIRE); await at(mp[0], mp[1], mp[2] - 2.4, 0, 10);
    const d1 = await strike(MIRE);
    ok(`a Strength C blow of the Sovereign's Edge takes at most ${CAP} off it`, d1 > 0 && d1 <= CAP + 0.5, `took ${d1}`);
    await sleep(900);
    const d2 = await strike(MIRE);
    ok('...and the next the same', d2 > 0 && d2 <= CAP + 0.5, `took ${d2}`);
    ok('...still standing, well above its floor', (await hpOf(MIRE)) > FLOOR + 300, String(await hpOf(MIRE)));
    await run('effect clear TestRat minecraft:strength'); await run('clear TestRat');
    await run(`${O}execute as ${MIRE} at @s run function bm:p246/melt`);
  }

  if (on('knight')) {
    const K = `@e[type=minecraft:husk,tag=bm.kduel,x=${X},y=${Y},z=${Z},distance=..30,limit=1]`;
    const ST = `@e[type=minecraft:interaction,tag=bm.knst_dread,x=${X},y=${Y},z=${Z},distance=..12,limit=1]`;
    await run(`${O}kill @e[type=minecraft:interaction,tag=bm.knst,x=${X},y=${Y},z=${Z},distance=..20]`); await run(`${O}kill @e[type=minecraft:item_display,tag=bm.knsd,x=${X},y=${Y},z=${Z},distance=..20]`);
    await at(X + 0.5, Y, Z + 0.5, 0, 60);
    await run('loot replace entity TestRat hotbar.0 loot bm:items/knight_statue_dread'); A.slot(0); await sleep(400);
    A.input({ shift: true }); await sleep(200); A.use(); await sleep(400); A.release(); await sleep(300); A.input({}); await sleep(800);
    ok('a Dread Sentinel\'s statue set up at home (sneak + use)', (await cnt(ST)) === 1);
    await at(X + 0.5, Y, Z - 2.5, 0, 10);
    const st = await entOf(ST); const n0 = A.dialogN.length; if (st) A.interact(st.entityId, false);
    ok('...right-clicked: its dialog', await wait(3000, async () => A.dialogN.length > n0, 100) && A.buttons().some(b => /Duel me/.test(b.label)), JSON.stringify(A.buttons().map(b => b.label)));
    await A.press(/Duel me/);
    ok('..."Duel me": it wakes against you, under the hit cap (20)', await wait(5000, async () => (await cnt(K)) === 1) && /bm\.hcap/.test(await run(`${O}tag ${K} list`)) && (await sc(K, 'bm.hcc')) === CAP * 10);
    ok('...420 over its floor, armour 16, toughness 10', (await hpOf(K)) >= 519.5 && /16\.0/.test(await run(`${O}attribute ${K} minecraft:armor base get`)) &&
       /10\.0/.test(await run(`${O}attribute ${K} minecraft:armor_toughness base get`)), `health ${await hpOf(K)}`);
    await wait(5000, async () => (await sc(K, 'bm.ks')) >= 1);
    await edge();
    const kp = await pos(K); await at(kp[0], kp[1], kp[2] - 1.8, 0, 10);
    const d1 = await strike(K);
    ok(`a Strength C blow of the Edge takes at most ${CAP} off it`, d1 > 0 && d1 <= CAP + 0.5, `took ${d1}`);
    await run('effect clear TestRat minecraft:strength'); await run('clear TestRat');
    for (const [s, p] of [['head', 'helmet'], ['chest', 'chestplate'], ['legs', 'leggings'], ['feet', 'boots']])
      await run(`item replace entity TestRat armor.${s} with minecraft:netherite_${p}[enchantments={"minecraft:protection":4}]`);
    await run('effect clear TestRat minecraft:resistance'); await run('attribute TestRat minecraft:max_health base set 200'); await run('effect give TestRat minecraft:instant_health 1 20 true');
    await run('effect give TestRat minecraft:regeneration infinite 1 true');
    let last = await hp(), big = 0; const t0 = Date.now();
    while (Date.now() - t0 < 25000 && big < 7) {
      const p = await pos(K); if (p) await run(`${O}tp TestRat ${p[0]} ${p[1]} ${p[2] - 1.6}`);
      await sleep(100); const h = await hp(); if (h < last) big = Math.max(big, last - h); last = h;
      if (h < 60) { await run('effect give TestRat minecraft:instant_health 1 20 true'); await sleep(100); last = await hp(); }
    }
    ok('in Protection IV netherite, no Resistance: its slam still lands heavy (one hit of 7+ - Dread)', big >= 7, `heaviest ${big.toFixed(2)}`);
    await run('attribute TestRat minecraft:max_health base set 20'); await run('effect give TestRat minecraft:instant_health 1 4 true'); await run('clear TestRat');
    await run('effect give TestRat minecraft:resistance infinite 4 true');
    await at(X + 0.5, Y, Z - 13.5);
    await run(`${O}execute as ${K} at @s run function bm:p245/h/stone`);      // (the duel let go: stone on its plinth)
    ok('the duel over: stone on its plinth, no host, no part left loose', await wait(6000, async () => (await cnt(K)) === 0 &&
       (await cnt(`@e[type=minecraft:item_display,tag=bm.kr,x=${X},y=${Y},z=${Z},distance=..30]`)) === 0));
    await at(X + 0.5, Y, Z - 2.5, 0, 10);
    const st2 = await entOf(ST); A.input({ shift: true }); await sleep(300); if (st2) A.attack(st2.entityId); await sleep(600); A.input({}); await sleep(600);
    ok('...sneak + punched: its statue back in your pack', (await has('knight_statue_dread')) === 1);
    await run('clear TestRat');
  }

  await run(`scoreboard players set #dfell bm.cfg ${dfell < 0 ? 0 : dfell}`); await run('attribute TestRat minecraft:max_health base set 20'); await run('effect clear TestRat');
  const p = res.filter(Boolean).length; console.log(`\n${p}/${res.length} passed`);
  A.end(); R.end(); process.exit(p === res.length ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });

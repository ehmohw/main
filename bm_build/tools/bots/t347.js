// 3.0g: THE GUARDIAN STAYS IN ITS HALL, THE MIRROR MAGE WAKES, NO SOUL VIALS IN THE GUTTER, HEIST BARRELS VANISH - as a regular
// player (rcon sets the stage).
//  mage     Tier IV, the second guardian forced (the Abyssal Ravager, the Mirror Mage on its back): TestRat walks into the vault;
//           the mage thrown off while the guardian rises (as a teleport under the floor can) is not left frozen: once the entrance
//           is over it has its AI and can be hurt.
//  hall     the guardian pushed into the sealed treasury, into a wall, under the floor: each time it is back in the hall within a second.
//  vial     the 1-in-700 Soul Vial's kill granted as the game grants it, in the gutter: no vial; outside: the vial (the path still works).
//  barrels  a Crate Desk crate and The Haul set down in the overworld and broken with a bare fist (TestRat mining them): what was
//           inside spills, the barrel never drops; and no plain barrel can drop from a block in the gutter.
const { bot, rcon, sleep } = require('./lib_resp');
const { mk, rel } = require('./h110');
const res = [];
const want = (k) => !process.argv[2] || process.argv[2].split(',').includes(k);
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 150) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const H = mk(run); const { num, cnt, heist, begin } = H;
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  ok('TestRat is a regular player (no operator commands)', await new Promise(r => { const n0 = A.chats.length; A.cmd('gamemode creative');
    setTimeout(() => r(A.chats.slice(n0).some(c => /unknown or incomplete|Unknown command/i.test(c))), 1200); }));
  await run('function bm:admin/prime_never'); await run('function bm:admin/fork_never'); await run('function bm:admin/traps_never'); await run('function bm:admin/curse_never');
  const G = 'execute in bm:gutter run ';

  if (want('mage') || want('hall')) {
    await run('function bm:admin/heist_boss_alt'); await run('function bm:admin/heist_hall_0'); await run('function bm:admin/heist_hard_never');
    await heist('levers', 'a', 4); await begin();
    const GI = await num('scoreboard players get TestRat bm.gvi');
    const V = `@e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${GI}},limit=1]`;
    const B = `@e[tag=bm.gvboss,scores={bm.gvi=${GI}},limit=1]`;
    const MAGE = '@e[type=minecraft:pillager,tag=bm.b93rider,limit=1]';
    const atV = (cmd) => run(`execute in bm:gutter as ${V} at @s run ${cmd}`);
    const vpos = (await run(`${G}data get entity ${V} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/).slice(1).map(Number);
    const bpos = async () => { const m = (await run(`${G}data get entity ${B} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/); return m ? m.slice(1).map(Number) : null; };
    const inHall = async () => { const p = await bpos(); return p && Math.abs(p[0] - vpos[0]) <= 11.3 && Math.abs(p[2] - vpos[2]) <= 11.3 && p[1] > vpos[1] - 1.6; };
    await atV(`tp TestRat ${rel(6, 4, 12)} -90 0`);
    ok('Into the Tier IV vault: the Abyssal Ravager rises, the Mirror Mage on its back', await wait(4000, async () => (await cnt(MAGE)) === 1 && /b93_ravager/.test(await run(`${G}data get entity ${B} Tags`))));
    if (want('mage')) {
      ok('...both frozen while it rises', /1b/.test(await run(`${G}data get entity ${MAGE} NoAI`)));
      await run(`${G}ride ${MAGE} dismount`);                                    // (thrown off on the way up)
      ok('...the mage thrown off its back mid-entrance', !/Found|passed/.test(await run(`${G}execute as ${MAGE} on vehicle if entity @s`)));
      ok('Once the entrance is over the mage has its AI again, and can be hurt', await wait(7000, async () => /: 0b/.test(await run(`${G}data get entity ${MAGE} NoAI`)) &&
         /: 0b/.test(await run(`${G}data get entity ${MAGE} Invulnerable`))), (await run(`${G}data get entity ${MAGE} NoAI`)).slice(-30));
      const h0 = await num(`${G}data get entity ${MAGE} Health`);
      await run('effect clear TestRat'); await run(`${G}tp TestRat ${MAGE}`); await sleep(400);
      let mage = null;
      { const m = (await run(`${G}data get entity ${MAGE} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/);
        if (m) { const h = m.slice(1).map(v => ((+v) >>> 0).toString(16).padStart(8, '0')).join(''); const u = `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`;
                 const e = Object.values(A.ents).find(e => e.objectUUID === u); mage = e ? e.entityId : null; } }
      if (mage) { A.attack(mage); await sleep(600); }
      ok('...TestRat\'s blow lands on it', mage && (await num(`${G}data get entity ${MAGE} Health`)) < h0, `${h0} -> ${await num(`${G}data get entity ${MAGE} Health`)} (eid ${mage})`);
      await run('effect give TestRat resistance 900 4 true');
    }
    if (want('hall')) {
      await wait(6000, async () => !/bm\.cfrz/.test(await run(`${G}data get entity ${B} Tags`)));
      ok('The guardian stands its ground a little better (+0.4 knockback resistance)', /0\.4/.test(await run(`${G}attribute ${B} minecraft:knockback_resistance get`)));
      for (const [what, x, y, z] of [['into the sealed treasury', 30, 4, 12], ['into the wall', 24, 5, 3], ['out of the entry doorway', -3, 4, 12], ['under the floor', 12, 1, 12]]) {
        await atV(`tp ${B} ${rel(x, y, z)}`);
        ok(`The guardian pushed ${what}: back in the hall within a second`, await wait(1500, inHall), `${await bpos()} (hall at ${vpos})`);
      }
    }
    await run(`${G}kill @e[type=minecraft:pillager,tag=bm.b93rider]`);
    await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
    await run('function bm:admin/heist_boss_any'); await run('function bm:admin/heist_hall_any'); await run('function bm:admin/heist_hard_any');
  }

  if (want('vial')) {
    await heist('levers', 'a', 1); await begin(); await sleep(500);
    const vials = async () => Math.max(0, await num('clear TestRat *[minecraft:custom_data~{bm:"soul_vial_zombie"}] 0'));
    await run('clear TestRat *[minecraft:custom_data~{bm:"soul_vial_zombie"}]');
    await run('advancement revoke TestRat only bm:p44/vial_zombie'); await run('advancement grant TestRat only bm:p44/vial_zombie'); await sleep(600);
    ok('A heist zombie\'s lucky kill, in the gutter: no Soul Vial', (await vials()) === 0);
    await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(2000);
    await run('advancement revoke TestRat only bm:p44/vial_zombie'); await run('advancement grant TestRat only bm:p44/vial_zombie'); await sleep(600);
    ok('...the same kill out in the world: the vial (the path still works)', (await vials()) === 1);
    await run('clear TestRat *[minecraft:custom_data~{bm:"soul_vial_zombie"}]');
  }

  if (want('barrels')) {
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    await run('execute in minecraft:overworld run fill 12996 119 12996 13004 119 13004 stone'); await run('execute in minecraft:overworld run fill 12996 120 12996 13004 124 13004 air');
    await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5 0 30'); await run('gamemode survival TestRat'); await run('clear TestRat'); await sleep(2000);
    const barrelsNear = () => num('execute in minecraft:overworld store result score #t bm.rng if entity @e[type=minecraft:item,x=13000,y=120,z=13002,distance=..4,nbt={Item:{id:"minecraft:barrel"}}]');
    const itemsNear = () => num('execute in minecraft:overworld store result score #t bm.rng if entity @e[type=minecraft:item,x=13000,y=120,z=13002,distance=..4]');
    const kinds = [['a Crate Desk crate (Raw Materials)', 'loot replace entity TestRat hotbar.0 loot bm:items/crate_raw'],
                   ['The Haul', 'item replace entity TestRat hotbar.0 with minecraft:barrel[minecraft:custom_name={text:"The Haul",color:"#ffcf40",bold:true},minecraft:custom_data={bm_haul:1b},minecraft:container=[{slot:0,item:{id:"minecraft:diamond",count:3}}]]']];
    for (const [nm, give] of kinds) {
      await run('execute in minecraft:overworld run kill @e[type=minecraft:item,x=13000,y=120,z=13002,distance=..6]');
      await run(give); A.slot(0); await sleep(300);
      A.useOn(13000, 119, 13002, 1); await sleep(800);                          // (set down on the floor in front of him)
      const placed = /passed/i.test(await run('execute in minecraft:overworld if block 13000 120 13002 minecraft:barrel'));
      ok(`${nm}: set down by TestRat`, placed && (await num('execute in minecraft:overworld store result score #t bm.rng if entity @e[type=minecraft:marker,tag=bm.haulm,x=13000,y=120,z=13002,distance=..1]')) === 1);
      A.slot(8); await sleep(200);
      await A.mine(13000, 120, 13002, 4200, 1); await sleep(700);             // (a bare fist: barrel 2.5 hardness, ~3.75 s)
      ok(`...broken with a bare fist: gone`, /failed|Test failed/i.test(await run('execute in minecraft:overworld if block 13000 120 13002 minecraft:barrel')) ||
         !/passed/i.test(await run('execute in minecraft:overworld if block 13000 120 13002 minecraft:barrel')));
      ok(`...no barrel dropped (what was inside spilled)`, (await barrelsNear()) <= 0 && (await itemsNear()) >= 1, `barrels ${await barrelsNear()}, items ${await itemsNear()}`);
      await run('clear TestRat minecraft:barrel');
    }
    await heist('levers', 'a', 1);
    await run('execute at TestRat run summon minecraft:item ~ ~0.5 ~ {Item:{id:"minecraft:barrel",count:1},PickupDelay:10s}');
    await sleep(600);
    ok('A plain barrel dropped from a block in the gutter is gone before it can be picked up', (await num('clear TestRat minecraft:barrel 0')) <= 0 &&
       (await cnt('@e[type=minecraft:item,distance=0..,nbt={Item:{id:"minecraft:barrel"}}]')) === 0);
    await run('execute as TestRat at @s run function bm:p70/leave'); await sleep(1500);
  }

  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run('execute in minecraft:overworld run tp TestRat 13000.5 120 13000.5');
  await run('function bm:admin/prime_chance'); await run('function bm:admin/fork_chance'); await run('function bm:admin/traps_chance'); await run('function bm:admin/curse_chance'); await run('function bm:admin/rooms_any');
  console.log(`${res.filter(Boolean).length}/${res.length} passed`); A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

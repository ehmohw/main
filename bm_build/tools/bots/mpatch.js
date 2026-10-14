// A market placed deep underground (as an old market would be): the 2.20 patch - shaft to the surface, dock rat, docks sign, water dried.
const { rcon, sleep } = require('./lib');
(async () => {
  const R = await rcon(); const run = (c) => R.run(c);
  let pass = 0, fail = 0; const ok = (n, p, d) => { p ? pass++ : fail++; console.log((p ? 'PASS ' : 'FAIL ') + n + '  -- ' + d); };
  for (const [rot, n] of [['none', 0], ['clockwise_90', 1]]) {
    const CX = 31000 + n * 400, CZ = 30000, y = 15;
    for (const [a, b, c, d] of [[-112, -112, -1, -1], [0, -112, 111, -1], [-112, 0, -1, 111], [0, 0, 111, 111]]) await run(`forceload add ${CX + a} ${CZ + b} ${CX + c} ${CZ + d}`);
    let pl = ''; for (let t = 0; t < 40; t++) { await sleep(2500); pl = await run(`place template bm:black_market ${CX} ${y} ${CZ} ${rot}`); if (!pl.includes('not loaded')) break; }
    const MX = [38.5, -46.5][n], MZ = [46.5, 38.5][n];
    const mk = `@e[type=minecraft:marker,tag=bm.mkt,x=${CX + MX},y=${y + 12},z=${CZ + MZ},distance=..2,limit=1]`;
    console.log(rot, pl.slice(0, 50), (await run(`data get entity ${mk} Rotation[0]`)).slice(-8));
    // an "old" market: the waterlogged ceiling bars and chains the 2.20 patch must dry
    const at = (p) => `execute as ${mk} at @s rotated as @s positioned ${p}`;
    // make something wet: every iron bar / chain within the market gets waterlogged (like a flooded old market)
    const wetN = await run(`${at('^ ^ ^')} run fill ~-45 ~-12 ~-50 ~45 ~20 ~50 minecraft:iron_bars[waterlogged=true] replace minecraft:iron_bars`);
    await run(`${at('^ ^ ^')} run fill ~-45 ~-12 ~-50 ~45 ~20 ~50 minecraft:iron_chain[waterlogged=true,axis=y] replace minecraft:iron_chain[axis=y]`);
    await run(`execute as ${mk} at @s rotated as @s run function bm:p28/install`);
    await run(`execute as ${mk} at @s rotated as @s run function bm:p41/patch`); await sleep(2500);
    const wetLeft = await run(`${at('^ ^ ^')} if blocks ~-1 ~-1 ~-1 ~1 ~1 ~1 ~-1 ~-1 ~-1 all`);   // (no "count waterlogged" command; sample below)
    let wet = 0; const s = await run(`${at('^ ^ ^')} run fill ~-45 ~-12 ~-50 ~45 ~20 ~50 minecraft:iron_bars[waterlogged=true] replace minecraft:iron_bars[waterlogged=true]`);
    const m = s.match(/filled (\d+)/i); wet = m ? +m[1] : 0;
    ok(`${rot}: waterlogged bars dried`, wet === 0, `bars made wet: ${wetN.slice(0, 40)}; still wet after the patch: ${wet} (${s.slice(0, 50)})`);
    await run(`${at('^ ^ ^')} run fill ~-45 ~-12 ~-50 ~45 ~20 ~50 minecraft:iron_bars[waterlogged=false] replace minecraft:iron_bars[waterlogged=true]`);
    // the dock rat
    const rat = await run(`${at('^-28 ^-2 ^-20')} if entity @e[type=minecraft:item_display,tag=bm.rat_sprite,distance=..2]`);
    const vil = await run(`${at('^-28 ^-2 ^-20')} run data get entity @e[type=minecraft:villager,tag=bm.npc_dock,distance=..2,limit=1] CustomName`);
    ok(`${rot}: the Dockmaster is a rat`, rat.includes('passed'), `${rat} / ${vil.slice(-80)}`);
    // the shaft: ladders from the tunnel's end up to the surface
    const sm = await run(`${at('^ ^6 ^53')} run data get entity @e[type=minecraft:marker,tag=bm.mshaft,distance=..2,limit=1] Tags`);
    await sleep(2500);
    let ladders = 0, top = 0;
    for (let dy = 0; dy < 70; dy++) { const r = await run(`${at('^ ^' + (6 + dy) + ' ^54')} if block ~ ~ ~ minecraft:ladder`); if (r.includes('passed')) { ladders++; top = dy; } }
    const sky = await run(`${at('^ ^' + (6 + top + 2) + ' ^53')} if predicate bm:sees_sky`);
    ok(`${rot}: a ladder shaft to the surface`, ladders > 10 && sky.includes('passed'), `marker ${sm.slice(-50)}; ladders ${ladders}, top +${top}, open sky above ${sky.includes('passed')}`);
    for (const [a, b, c, d] of [[-112, -112, -1, -1], [0, -112, 111, -1], [-112, 0, -1, 111], [0, 0, 111, 111]]) await run(`forceload remove ${CX + a} ${CZ + b} ${CX + c} ${CZ + d}`);
  }
  console.log(`${pass} passed, ${fail} failed`);
  R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });

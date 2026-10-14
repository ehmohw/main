// Place the market at all four turns; check every lectern (blocks and ledger displays) faces the same way relative to the market.
const { rcon, sleep } = require('./lib');
const cfg = require('./lect_cfg.json');
const DIRS = ['north', 'east', 'south', 'west'];
const cw = (d, n) => DIRS[(DIRS.indexOf(d) + n) % 4];
(async () => {
  const R = await rcon(); const run = (c) => R.run(c);
  let pass = 0, fail = 0;
  const rots = [['none', 0], ['clockwise_90', 1], ['180', 2], ['counterclockwise_90', 3]];
  const CX = 30000, CZ = 30000;
  for (const [a, b, c, d] of [[-112, -112, -1, -1], [0, -112, 111, -1], [-112, 0, -1, 111], [0, 0, 111, 111]]) await run(`forceload add ${CX + a} ${CZ + b} ${CX + c} ${CZ + d}`);
  await sleep(3000);
  for (const [rot, n] of rots) {
    const bx = CX, bz = CZ, y = 60;
    const MX = [38.5, -45.5, -38.5, 45.5][n], MZ = [45.5, 38.5, -45.5, -38.5][n];
    let pl = '';
    for (let t = 0; t < 20; t++) { await sleep(2000); pl = await run(`place template bm:black_market ${bx} ${y} ${bz} ${rot}`); if (!pl.includes('not loaded')) break; }
    await sleep(2500);
    const mk = `@e[type=minecraft:marker,tag=bm.mkt,x=${CX + MX},y=72,z=${CZ + MZ},distance=..2,limit=1]`;
    const yaw = (await run(`data get entity ${mk} Rotation[0]`)).replace(/.*: /, '');
    await run(`execute as ${mk} at @s rotated as @s run function bm:p28/install`);
    await run(`execute as ${mk} at @s rotated as @s run function bm:p35/patch`);
    await sleep(800);
    const at = (p) => `execute as ${mk} at @s rotated as @s positioned ${p}`;
    const facing = async (p) => { for (const d of DIRS) if ((await run(`${at(p)} if block ~ ~ ~ minecraft:lectern[facing=${d}]`)).includes('passed')) return d; return 'none'; };
    const chk = (name, got, want) => { const ok = got === want; ok ? pass++ : fail++; console.log(`  ${ok ? 'ok  ' : 'BAD '} ${rot.padEnd(20)} ${name.padEnd(22)} ${got} (want ${want})`); };
    console.log(`${rot}: ${pl.slice(0, 60)}; marker yaw ${yaw}`);
    chk('newcomer lectern', await facing(cfg.newcomer), cw('east', n));
    chk('stacks lectern', await facing(cfg.stacks), cw('south', n));
    for (const [k, [p, ly]] of Object.entries(Object.assign({}, cfg.ledgers, cfg.gates))) {
      const r = await run(`${at(p)} run data get entity @e[type=minecraft:block_display,tag=bm.lg_book,distance=..1.2,limit=1] Rotation[0]`);
      const got = parseFloat(r.replace(/.*: /, '')); const want = ((parseFloat(yaw) + ly) % 360 + 540) % 360 - 180;
      const g = ((got % 360) + 540) % 360 - 180;
      const okk = Math.abs(g - want) < 1 || Math.abs(Math.abs(g - want) - 360) < 1;
      okk ? pass++ : fail++; console.log(`  ${okk ? 'ok  ' : 'BAD '} ${rot.padEnd(20)} ledger ${k.padEnd(15)} yaw ${isNaN(got) ? r.slice(0, 50) : g} (want ${want})`);
    }
  }
  console.log(`\n${pass} ok, ${fail} bad`);
  R.end(); process.exit(0);
})().catch((e) => { console.log('FATAL', e); process.exit(1); });

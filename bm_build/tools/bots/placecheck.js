// Worldgen placement audit: for each structure, find a fresh one far from anything generated, bring the bot near (some build
// themselves when a player comes close), let it generate and settle, save, and record where it is - tools/preview/placecheck.py
// then reads the region files and renders/scores each site.   node placecheck.js [sid ...] [--n 2] [--far 400000]
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs');
const ALL = { overworld: ['graveyard', 'frog_hut', 'crash_site', 'leo_fort', 'sword_shrine', 'db_snow', 'db_witch', 'db_shark', 'om_palace', 'tul_ship',
                         'p2_frost', 'p2_hex', 'p2_keep', 'p2_tide', 'p199_kingdom', 'ruins_overworld'],
              the_nether: ['p200_ember_outpost', 'p200_colossus_forge', 'ruins_nether'], the_end: ['p200_void_outpost', 'p200_observatory', 'ruins_end'] };
(async () => {
  const args = process.argv.slice(2);
  const nIdx = args.indexOf('--n'); const N = nIdx >= 0 ? +args[nIdx + 1] : 2;
  const fIdx = args.indexOf('--far'); const FAR = fIdx >= 0 ? +args[fIdx + 1] : 400000;
  const want = args.filter((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
  const R = await rcon(); const run = c => R.run(c);
  const A = await bot('TestRat'); await sleep(2500); A.stand();
  await run('gamemode creative TestRat'); await run('effect give TestRat minecraft:resistance 99999 4 true');
  const out = fs.existsSync('/tmp/placecheck.json') ? JSON.parse(fs.readFileSync('/tmp/placecheck.json')) : {};
  let k = 0;
  for (const [dim, sids] of Object.entries(ALL)) {
    const D = `execute in minecraft:${dim} run `;
    for (const sid of sids) {
      if (want.length && !want.includes(sid)) continue;
      out[sid] = [];
      for (let s = 0; s < N; s++) {
        k++;
        const ox = FAR + k * 9000 * (s % 2 ? -1 : 1), oz = FAR + k * 7000;
        const r = await run(`${D}execute positioned ${ox} 64 ${oz} run locate structure bm:${sid}`);
        const m = r.match(/\[(-?\d+), (~|-?\d+), (-?\d+)\]/);
        if (!m) { console.log(`${sid}: not found near ${ox} ${oz} (${r.slice(0, 120)})`); continue; }
        const x = +m[1], z = +m[3];
        await run(`${D}forceload add ${x - 80} ${z - 80} ${x + 80} ${z + 80}`);
        await run(`${D}tp TestRat ${x} ${dim === 'the_nether' ? 110 : 200} ${z}`);
        await sleep(9000);                                  // (generate; the seed-built ones build when you're near)
        await run(`${D}tp TestRat ${x} ${dim === 'the_nether' ? 100 : 120} ${z}`); await sleep(6000);
        await run('save-all flush'); await sleep(2500);
        out[sid].push({ dim, x, z });
        console.log(`${sid} #${s + 1}: ${dim} ${x} ${z}`);
        await run(`${D}forceload remove ${x - 80} ${z - 80} ${x + 80} ${z + 80}`);
      }
      fs.writeFileSync('/tmp/placecheck.json', JSON.stringify(out, null, 1));
    }
  }
  await run('gamemode survival TestRat');
  process.exit(0);
})();

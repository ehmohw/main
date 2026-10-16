// After a test or a sweep: are any chunks still force-loaded where the pack never holds any?
// The pack force-loads only in bm:gutter (the den, Lounge and Locker Hall for good; a raid's instance while it runs)
// and bm:hollow_throne (while its builds are placed). The Overworld, the Nether and the End should read empty.
// `node chunkcheck.js` reports; `node chunkcheck.js --clear` also releases what it found in those three.
const { rcon } = require('./lib_resp');
(async () => { const R = await rcon(); let bad = 0;
  for (const d of ['minecraft:overworld', 'minecraft:the_nether', 'minecraft:the_end']) {
    const q = await R.run(`execute in ${d} run forceload query`);
    if (/^No force loaded/.test(q)) { console.log(`${d}: none`); continue; }
    bad++; console.log(`${d}: LEFT LOADED - ${q.slice(0, 300)}`);
    if (process.argv.includes('--clear')) console.log('  ' + await R.run(`execute in ${d} run forceload remove all`));
  }
  for (const d of ['bm:gutter', 'bm:hollow_throne']) console.log(`${d} (the pack's own): ${(await R.run(`execute in ${d} run forceload query`)).replace(/ at:.*/, '')}`);
  R.end(); process.exit(bad && !process.argv.includes('--clear') ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });

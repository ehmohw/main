// node cmd.js "cmd1" "cmd2" ... : runs commands with TestRat online (WAIT n = sleep n ms)
const { bot, rcon, sleep } = require('./lib');
(async () => { const R = await rcon(); const A = await bot('TestRat'); await sleep(1200);
  for (const c of process.argv.slice(2)) { if (c.startsWith('WAIT ')) { await sleep(+c.slice(5)); continue; } console.log('>', c.slice(0, 90)); console.log((await R.run(c)).slice(0, 400)); }
  A.end(); R.end(); process.exit(0); })();

const { rcon } = require('./lib_resp');
(async () => { const R = await rcon();
  for (const c of process.argv.slice(2)) console.log(c, ' => ', await R.run(c));
  R.end(); process.exit(0); })();

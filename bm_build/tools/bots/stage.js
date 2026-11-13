// Shared staging for the bot tests (3.2a).
// sendAllHome(run): every follower of TestRat's sent home as the game does it (p98/home/<kind>, as TestRat, #me bm.pid set) - one
// left out by an earlier test fills the follower limit, and the follower a test calls next quietly sends another home (t100, t103).
const fs = require('fs');
const path = require('path');
const HOME = path.join(__dirname, '..', '..', 'out_p2/BlackMarket_DP/data/bm/function/p98/home');
async function sendAllHome(run, who = 'TestRat') {
  await run(`scoreboard players operation #me bm.pid = ${who} bm.pid`);
  for (const f of fs.readdirSync(HOME)) await run(`execute as ${who} at @s run function bm:p98/home/${f.replace(/\.mcfunction$/, '')}`);
}
module.exports = { sendAllHome };

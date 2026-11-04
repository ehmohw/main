// 3.0j: THE BLACK MARKET HANDBOOK (phase260), as a regular player - given once on joining (bm.hbgot cleared: it arrives within
// two seconds, and only once); right-click: its page counts what you've met / beaten / found; met two followers: "2 of N", the
// Followers page names them and hints at the next unmet ones ("#01 ???" style); one more met and the Elder Treant beaten: the
// counts and pages follow by themselves; Places: the Loom Sanctuary found once the Keeper's met; Currencies renders; sneak +
// right-click: Your settings. The recipe and the Fence's offer are in the built pack.
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs'), path = require('path');
const DP = path.join(__dirname, '../../out_p2/BlackMarket_DP/data/bm');
(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 100) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  { const _press0 = A.press.bind(A); A.press = async (re, ms) => { await sleep(700); return _press0(re, ms); }; }
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  const has = async () => +(((await run('clear TestRat *[minecraft:custom_data~{bm:"bm_handbook"}] 0')).match(/Found (\d+)/) || [0, 0])[1]);
  await run('clear TestRat'); await run('tag TestRat remove bm.hbgot');
  ok('given on joining: one Handbook within two seconds', await wait(3000, async () => (await has()) === 1));
  await sleep(2500); ok('...and only once', (await has()) === 1);
  await run('advancement revoke TestRat from bm:met/emma'); for (const a of (fs.readdirSync(path.join(DP, 'advancement/met')))) await run(`advancement revoke TestRat only bm:met/${a.replace('.json', '')}`);
  await run('advancement revoke TestRat only bm:story/treant');
  await run('advancement grant TestRat only bm:met/emma'); await run('advancement grant TestRat only bm:met/celi');
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/bm_handbook'); A.slot(0); await sleep(300);
  const body = () => JSON.stringify(((d => d && (d.data || d))(A.dialogN[A.dialogN.length - 1]) || {}).body || '');
  const title = () => JSON.stringify(((d => d && (d.data || d))(A.dialogN[A.dialogN.length - 1]) || {}).title || '');
  const openB = async (sneak = false) => { await run('scoreboard players set TestRat bm.gvhc 0'); const n0 = A.dialogN.length;
    if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(350); A.release(); A.input({}); await wait(2500, async () => A.dialogN.length > n0); return A.dialogN.length > n0; };
  const met = (b) => +((b.match(/Followers met: ","[^}]*\},\{"text":"(\d+)/) || b.match(/Followers met: .*?"(\d+)"/) || [0, -1])[1]);
  let o = await openB();
  ok('right-click: the Handbook, "Followers met: 2"', o && /HANDBOOK/.test(title()) && /Followers met/.test(body()) && /"2"|:"2"|text":"2"/.test(body()), body().slice(0, 200));
  let p = await A.press(/^Followers/);
  ok('...Followers: Emma and Celi named, three hints for the next', p && p.next && /Emma/.test(body()) && /Celi/.test(body()) && (body().match(/\?\?\?/g) || []).length === 3, body().slice(0, 300));
  await run('advancement grant TestRat only bm:met/zib'); await run('advancement grant TestRat only bm:story/treant'); await run('advancement grant TestRat only bm:met/keeper');
  await A.press(/« Handbook/);
  ok('...three more met (one the Keeper) and the Treant beaten: "Followers met: 4", "Bosses beaten: 1"', /HANDBOOK/.test(title()) && /text":"4"/.test(body()) && /Bosses beaten/.test(body()), body().slice(0, 300));
  p = await A.press(/^Bosses/);
  ok('...Bosses: ✔ The Elder Treant, ✘ the rest', p && p.next && /✔ The Elder Treant/.test(body()) && /✘ The Storm Roc/.test(body()));
  await A.press(/« Handbook/); p = await A.press(/^Places/);
  ok('...Places: ✔ The Loom Sanctuary (its Keeper met)', p && p.next && /✔ The Loom Sanctuary/.test(body()));
  await A.press(/« Handbook/); p = await A.press(/^Dungeons/);
  ok('...Dungeons & heists: renders (Tier I heist listed)', p && p.next && /Tier I heist/.test(body()));
  await A.press(/« Handbook/); p = await A.press(/^Currencies/);
  ok('...Currencies: Tokens and who takes them', p && p.next && /Tokens/.test(body()) && /taken by/.test(body()), body().slice(0, 200));
  await A.press(/« Handbook/); p = await A.press(/Your settings/);
  ok('...Your settings: its page', p && p.next && /YOUR SETTINGS/.test(title()));
  o = await openB(true);
  ok('sneak + right-click: Your settings straight away', o && /YOUR SETTINGS/.test(title()));
  ok('the recipe (a book and a gold nugget) is in the pack', fs.existsSync(path.join(DP, 'recipe/bm_handbook.json')));
  const fence = fs.readdirSync(path.join(DP, 'function/npc')).some(f => /bm_handbook/.test(fs.readFileSync(path.join(DP, 'function/npc', f), 'utf8')));
  ok('the Fence sells it', fence);
  await run('advancement revoke TestRat only bm:story/treant');
  for (const a of ['emma', 'celi', 'zib', 'keeper']) await run(`advancement revoke TestRat only bm:met/${a}`);
  await run('clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();

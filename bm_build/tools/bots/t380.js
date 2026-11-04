// 3.0j: EVERY FOLLOWER'S MENUS, CRAWLED (phase260), as a regular (non-op) player. The list comes from the built pack (p260/fs/open/<who>,
// and each one's item from p260's Stay here / the wheel's rows), the routes from BUTTON_CODES.md. For each follower: sneak + use their
// item - their menu (or, for those without one, their wardrobe) renders, has "Settings" and no chatter switch; Settings - their
// settings page renders (named, "settings", Chatter, Keep up); Wardrobe › - the wardrobe renders, with "Settings";
// « Back - back to where we came from. Every button on every screen seen is routed in the legend. Then the heist crew page (the
// Fixer's Ledger -> Raid Crew): renders; a met follower without a contract is on "Not signed yet", which opens and goes back.
//   node t380.js [who ...]
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '../..');
const FN = path.join(ROOT, 'out_p2/BlackMarket_DP/data/bm/function');
const ONLY = process.argv.slice(2);
const legend = fs.readFileSync(path.join(ROOT, 'BUTTON_CODES.md'), 'utf8');
const routed = new Set(); for (const l of legend.split('\n')) { const m = l.match(/^\| (\d+)(?: \(link\))? \|.*\| ([^|]*) \|$/); if (m && !/not routed/.test(m[2])) routed.add(+m[1]); }
// every follower's item, from the wheel as built (p179/w/use: which item puts whom in which slot)
const use = fs.readFileSync(path.join(FN, 'p179/w/use.mcfunction'), 'utf8');
const W = [...use.matchAll(/weapon\.offhand \*\[minecraft:custom_data~\{bm:"([a-z0-9_]+)"\}\] run return run function bm:p179\/w\/add(\d+)/g)].map(m => ({ w: m[1], iid: m[1] }));
const PAGES = fs.readdirSync(path.join(FN, 'p260/fs/open')).length;

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 100) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const X = 16760, Y = 100, Z = 16060;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  ok(`${W.length} followers' items on the wheel, ${PAGES} settings pages`, W.length >= 50 && PAGES === W.length);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('time set 1000'); await run('weather clear');
  await run('scoreboard players set #hard bm.cfg 1'); await run('effect give TestRat minecraft:resistance infinite 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:grass_block`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 6} ${Z + 10} minecraft:air`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  const shown = () => A.dialogN[A.dialogN.length - 1] || {};
  const title = () => JSON.stringify(shown().title || '');
  const unrouted = () => A.buttons().filter(b => /bm\.act set \d+/.test(b.command) && !routed.has(+b.command.match(/set (\d+)/)[1])).map(b => b.label);
  const sneakMenu = async () => { await run('scoreboard players set TestRat bm.gvhc 0'); const n0 = A.dialogN.length; A.slot(0); await sleep(200);
    A.input({ shift: true }); await sleep(200); A.use(); await sleep(350); A.release(); A.input({}); await wait(3000, async () => A.dialogN.length > n0); return A.dialogN.length > n0; };

  for (const { w, iid } of W.filter(x => !ONLY.length || ONLY.includes(x.w))) {
    await run('clear TestRat'); await run(`loot replace entity TestRat hotbar.0 loot bm:items/${iid}`); await sleep(300);
    const got = await sneakMenu();
    const b0 = A.buttons().map(b => b.label), u0 = unrouted();
    ok(`${w}: sneak + use ${iid} - a menu with Settings, no chatter switch, every button routed`,
       got && b0.some(l => /Settings/.test(l)) && !b0.some(l => /^Chatter/.test(l)) && !u0.length, `${title().slice(0, 50)} ${u0.join(',')}`);
    const p1 = await A.press(/Settings$/);
    const b1 = A.buttons().map(b => b.label), u1 = unrouted();
    ok(`...Settings: the settings page (Chatter, Keep up; no Stay here), every button routed`,
       p1 && p1.next && /settings/.test(title()) && !b1.some(l => /Stay here|Come with me/.test(l)) && b1.some(l => /^Chatter/.test(l)) && b1.some(l => /^Keep up/.test(l)) && !u1.length,
       `${title().slice(0, 60)} ${u1.join(',')}`);
    const p2 = await A.press(/^Wardrobe/);
    const b2 = A.buttons().map(b => b.label), u2 = unrouted();
    ok('...Wardrobe ›: the wardrobe, with Settings, every button routed', p2 && p2.next && /wardrobe/.test(title()) && b2.some(l => /Settings$/.test(l)) && !u2.length,
       `${title().slice(0, 60)} ${u2.join(',')}`);
    await A.press(/Settings$/); const p3 = await A.press(/« Back/);
    ok('...Settings from the wardrobe, then « Back: the wardrobe again', p3 && p3.next && /wardrobe/.test(title()));
  }

  // ---- the heist crew page
  await run('clear TestRat'); await run('advancement grant TestRat only bm:met/emma'); await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger');
  await run('scoreboard players set TestRat bm.gvhc 0'); A.slot(0); await sleep(300);
  const office = await A.useWait(2500);
  const pc = await A.press(/Raid Crew/);
  const bc = A.buttons().map(b => b.label);
  ok('the Fixer\'s Ledger -> Raid Crew: the crew page, every button routed, no "no contract" row on it', office && pc && pc.next && /RAID CREW/.test(title()) && !unrouted().length && !bc.some(l => /no contract|not hired/.test(l)),
     bc.slice(0, 6).join(' | '));
  const pm = await A.press(/Not signed yet/);
  const bm = A.buttons().map(b => b.label);
  ok('...Not signed yet: its page (Emma, without a contract), every button routed', pm && pm.next && /not signed yet/.test(title()) && bm.some(l => /^Emma/.test(l)) && !unrouted().length, bm.slice(0, 5).join(' | '));
  const pb = await A.press(/« Raid Crew/);
  ok('...« Raid Crew: back on the crew page', pb && pb.next && /RAID CREW/.test(title()) && !/not signed/.test(title()));
  await run('clear TestRat');
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();

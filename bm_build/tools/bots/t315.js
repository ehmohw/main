// 2.98c: THE PARTNER WHEEL, AUDITED - every partner through it, as a regular (non-op) player. The list comes from the built
// pack itself (p179/w/use: which item puts whom in which slot; p179/w/row<i>: whose follower that row looks for; the legend:
// the row's words), so a label that drifts from what its buttons do shows up here. For each partner: their item in the off
// hand + the wheel used: on, in their slot, the item gone, told by their item's name; the wheel's page: "Call <name>" once,
// and no other row with their name; Call: THEIR follower comes (theirs: our pid); the page again: "Send <name> home" in that
// row; its Menu: their own menu (it names them); Send home: they go; Take the item back: THEIR item, the slot empty.
//   node t315.js [name ...]
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs'), path = require('path');
const FN = path.join(__dirname, '../../out_p2/BlackMarket_DP/data/bm/function');
const ONLY = process.argv.slice(2);

// ---- the wheel, as built
const use = fs.readFileSync(path.join(FN, 'p179/w/use.mcfunction'), 'utf8');
const P = [];
for (const m of use.matchAll(/weapon\.offhand \*\[minecraft:custom_data~\{bm:"([a-z0-9_]+)"\}\] run return run function bm:p179\/w\/add(\d+)/g)) {
  const i = +m[2];
  const row = fs.readFileSync(path.join(FN, `p179/w/row${i}.mcfunction`), 'utf8');
  const host = row.match(/execute as (@e\[type=minecraft:[a-z_]+,tag=[^\]]+\]) if score @s bm\.pid = #me bm\.pid/)[1];
  const leg = fs.readFileSync(path.join(__dirname, '../../BUTTON_CODES.md'), 'utf8').split('\n').find(l => l.includes(`p179/w/row${i} |`) && /\| Call /.test(l));
  const name = leg.match(/\| Call (.+?) \/ Send /)[1];
  P.push({ i, iid: m[1], host, name });
}

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const sc = async (who, o) => +((await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/) || [0, -99])[1];
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const O = 'execute in minecraft:overworld run ';
  const X = 16700, Y = 100, Z = 16000;
  const A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  ok(`the wheel as built: ${P.length} partners, each with an item, a row and a name`, P.length >= 48 && P.every(p => p.iid && p.host && p.name));
  ok('...every slot taken once, every item once', new Set(P.map(p => p.i)).size === P.length && new Set(P.map(p => p.iid)).size === P.length);
  await run('gamemode survival TestRat'); await run('clear TestRat'); await run('time set 1000'); await run('weather clear');
  await run('scoreboard players set #hard bm.cfg 1'); await run('effect give TestRat minecraft:resistance infinite 4 true');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  await run(`${O}fill ${X - 14} ${Y} ${Z - 14} ${X + 14} ${Y} ${Z + 14} minecraft:grass_block`); await run(`${O}fill ${X - 14} ${Y + 1} ${Z - 14} ${X + 14} ${Y + 8} ${Z + 14} minecraft:air`);
  await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(1500);
  const pid = await sc('TestRat', 'bm.pid');
  const empty = async () => { for (const p of P) await run(`scoreboard players set TestRat bm.pw${p.i} 0`); await run(`data remove storage bm:pw p${pid}`); };
  await empty();
  await run('loot replace entity TestRat hotbar.0 loot bm:items/partner_wheel'); A.slot(0); await sleep(400);
  const mine = (p) => `${p.host.slice(0, -1)},x=${X},y=${Y},z=${Z},distance=..48]`;
  const ours = async (p) => /passed/.test(await run(`${O}execute as ${mine(p)} if score @s bm.pid = TestRat bm.pid`));
  const rowOf = (p) => { const bs = A.buttons(); const k = bs.findIndex(b => new RegExp(`^(Call|Send) ${p.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}( home)?$`).test(b.label.replace(/^\W+\s*/, '').trim()));
                         return k < 0 ? null : { head: bs[k], menu: bs.slice(k + 1).find(b => /Menu/.test(b.label)), out: bs.slice(k + 1).find(b => /Take the item back/.test(b.label)) }; };
  const open = async () => { A.slot(0); await sleep(200); return A.useWait(1500); };
  const send = async (b) => { const n0 = A.dialogN.length; A.cmd(b.command.replace(/^\//, '')); await wait(2000, async () => A.dialogN.length > n0, 50); };

  for (const p of P.filter(p => !ONLY.length || ONLY.includes(p.name))) {
    await run(`${O}kill ${mine(p)}`); await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/partner_wheel');
    await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`);
    A.chats.length = 0;
    await run(`loot replace entity TestRat weapon.offhand loot bm:items/${p.iid}`); await sleep(300); await open();
    const on = (await sc('TestRat', `bm.pw${p.i}`)) === 1 && (await has(p.iid)) === 0;
    const told = A.chats.some(c => /goes on your Partner Wheel/.test(c));
    await open();
    const r = rowOf(p);
    const others = A.buttons().filter(b => /^(Call|Send) /.test(b.label.replace(/^\W+\s*/, '').trim())).length;
    ok(`${p.name} (slot ${p.i}, ${p.iid}): on the wheel; its page has their row and only theirs`, on && told && r && others === 1, `on ${on}, told ${told}, row ${!!r}, rows ${others}`);
    if (!r) { await empty(); continue; }
    await send(r.head);
    const came = await wait(8000, async () => ours(p));
    await open(); const r2 = rowOf(p);
    ok(`...Call ${p.name}: THEY come, and the row says Send ${p.name} home`, came && r2 && /Send/.test(r2.head.label), `came ${came}, row ${r2 ? r2.head.label : '-'}`);
    if (r2 && r2.menu) {
      const n0 = A.dialogs.length; await send(r2.menu);
      const d = A.dialogs.slice(n0).join(' ');
      const first = p.name.replace(/^(The|the) /, '').split(' ')[0];
      ok(`...their Menu: their own (it names ${p.name})`, d.length > 0 && d.includes(first), d.length ? (d.match(/"text":"([^"]{3,60})"/) || [0, d.slice(0, 80)])[1] : 'no screen');
    }
    await open(); const r3 = rowOf(p);
    if (r3 && /Send/.test(r3.head.label)) await send(r3.head);
    ok(`...Send ${p.name} home: they go`, await wait(8000, async () => !(await ours(p))));
    await open(); const r4 = rowOf(p);
    if (r4 && r4.out) await send(r4.out); await sleep(800);
    ok(`...Take the item back: THEIR item (${p.iid}), the slot empty`, (await has(p.iid)) === 1 && (await sc('TestRat', `bm.pw${p.i}`)) === 0);
    await empty();
  }
  await empty(); await run('clear TestRat');
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  console.log(`${res.filter(x => x).length}/${res.length} passed`);
  A.end(); R.end(); process.exit(0);
})();

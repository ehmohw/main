// URGENT (2.76), two players (both regular, non-op): the end-of-heist "Go to the Lounge" for a crew - pressed from the screens
// each client is shown. Heist 1: the leader takes the whole crew. Heist 2: a member goes on their own; the leader heads home.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const dim = async (n) => (await run(`data get entity ${n} Dimension`)).replace(/.*data: /, '');
  const fnTrue = async (pre, f) => /returned [1-9]/.test(await run(`execute ${pre} run function ${f}`));
  const tagged = async (n, t) => /passed/i.test(await run(`execute if entity @a[name=${n},tag=${t}]`));
  const show = (C, tag) => console.log(`   [${tag}] ` + C.buttons().map(b => `${b.label.replace(/[^\x20-\x7e·]/g, '').trim()} <${b.command.replace('/trigger bm.act set ', '')}>`).join(' | '));
  const O = 'execute in minecraft:overworld run ';
  const HX = 13100, HY = 121, HZ = 13000;
  const A = await bot('TestRat'); await sleep(1500); const B = await bot('TestRat2'); await sleep(2500);
  const NAMES = ['TestRat', 'TestRat2']; const C = { TestRat: A, TestRat2: B };
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run(`${O}forceload add ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
  await run(`${O}fill ${HX - 4} ${HY - 1} ${HZ - 4} ${HX + 4} ${HY - 1} ${HZ + 4} minecraft:stone`);
  await run(`${O}fill ${HX - 4} ${HY} ${HZ - 4} ${HX + 4} ${HY + 3} ${HZ + 4} minecraft:air`);
  for (const [k, n] of NAMES.entries()) {
    await run(`${O}tp ${n} ${HX + 0.5 + 2 * k} ${HY} ${HZ + 0.5} 0 0`); await run(`gamemode survival ${n}`); await run(`clear ${n}`); await run(`effect clear ${n}`);
    for (const t of ['bm.gvp', 'bm.gvask', 'bm.gvnext', 'bm.gvoffer', 'bm.gvwaitd', 'bm.gvin']) await run(`tag ${n} remove ${t}`);
    await run(`execute as ${n} unless score @s bm.pid matches 1.. run function bm:p21/pid`);
    await run(`loot replace entity ${n} hotbar.0 loot bm:items/fixers_ledger`);
  }
  // (a party of two - the party system's own bookkeeping)
  await run('scoreboard players operation TestRat bm.pty = TestRat bm.pid'); await run('scoreboard players operation TestRat2 bm.pty = TestRat bm.pid');
  await sleep(1500); A.stand(); B.stand(); A.slot(0); B.slot(0);
  for (const [n, X] of [['TestRat', HX + 0.5], ['TestRat2', HX + 2.5]]) { /* (regular players) */ }
  C.TestRat2.chats.length = 0; C.TestRat2.cmd('gamemode creative'); await sleep(500);
  ok('TestRat2 is a regular player too', /unknown|incomplete/i.test(B.chats.join(' ')));

  async function holdLedger(n) {     // (select whichever hotbar slot the Ledger came back to - or bring it to the hotbar, as a player would)
    const m = (await run(`data get entity ${n} Inventory[{components:{"minecraft:custom_data":{bm:"fixers_ledger"}}}].Slot`)).match(/(-?\d+)b?\s*$/);
    let slot = m ? +m[1] : -1;
    if (slot < 0) { await run(`loot replace entity ${n} hotbar.0 loot bm:items/fixers_ledger`); slot = 0; }
    if (slot > 8) { await run(`item replace entity ${n} hotbar.8 from entity ${n} container.${slot}`); await run(`item replace entity ${n} container.${slot} with minecraft:air`); slot = 8; }
    C[n].slot(slot); await sleep(300); return slot;
  }
  async function heist(tag) {
    for (const n of NAMES) for (let k = 0; k < 3; k++) await run(`loot give ${n} loot bm:items/token`);
    await holdLedger('TestRat');
    const opened = await A.useWait();
    if (!opened) console.log(`   (${tag}: no Office on the Ledger - chat: ${A.chats.slice(-2).join(' / ').slice(0, 200)} | bar: ${A.bars.slice(-1).join('').slice(0, 120)})`); await A.press(/Plan a Heist/); await A.press(/Tier I\b(?!I)/);
    B.dialogN.length = 0; B.chats.length = 0;
    await A.press(/^3\b|3 tries/i);
    // the member may be asked to opt in: press "I'm in" if a screen asks
    await wait(4000, async () => B.buttons().length > 0, 200);
    if (B.buttons().length) { show(B, `${tag}: TestRat2 is asked`); await B.press(/I'm in|Join|opt in|Count me in/i); }
    const inV = await wait(60000, async () => (await tagged('TestRat', 'bm.gvp')) && (await tagged('TestRat2', 'bm.gvp')) && /gutter/.test(await dim('TestRat2')));
    ok(`${tag}: both of the crew are led down into the vault`, inV, `${await dim('TestRat')} ${await dim('TestRat2')} | B: ${B.chats.slice(-2).join(' / ').slice(0, 200)}`);
    if (!inV) return null;
    await sleep(2500); A.stand(); B.stand();
    const gi = await sc('TestRat', 'bm.gvi');
    const lp = (await run(`execute in bm:gutter run data get entity @e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${gi}},limit=1] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    const [lx, ly, lz] = lp.slice(1).map(v => Math.floor(+v));
    await run(`execute in bm:gutter run tp TestRat ${lx + 9.5} ${ly + 1} ${lz + 3.5} -90 0`); await sleep(1200); A.stand();
    A.useOn(lx + 11, ly + 1, lz + 3, 4); await sleep(2600); A.useOn(lx + 11, ly + 1, lz + 3, 4); await sleep(1500);
    for (const n of NAMES) await run(`effect give ${n} minecraft:resistance 3600 4 true`);
    // (the rooms and the guardian aren't what this test is about: cleared)
    for (let q = 1; q <= 12; q++) {
      const sel = `@e[type=minecraft:marker,tag=bm.gvr,tag=!bm.gvr_vault,tag=!bm.gvr_lobby,tag=!bm.gvr_cache,scores={bm.gvi=${gi},bm.gvq=${q}},limit=1]`;
      if (!/\[/.test(await run(`execute in bm:gutter run data get entity ${sel} Tags`))) continue;
      await run(`execute in bm:gutter as ${sel} at @s run tp @a[tag=bm.gvp,scores={bm.gvi=${gi}}] ~-10 ~ ~ -90 0`); await sleep(1200);
      await run(`execute in bm:gutter as ${sel} at @s run function bm:p70/solved`); await sleep(300);
      await run(`execute in bm:gutter as ${sel} at @s run kill @e[tag=bm.gvg,distance=..30]`);
    }
    const vsel = `@e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${gi}},limit=1]`;
    await run(`execute in bm:gutter as ${vsel} at @s run tp @a[tag=bm.gvp,scores={bm.gvi=${gi}}] ~-6 ~ ~ -90 0`); await sleep(3000);
    for (let k = 0; k < 60 && /passed/i.test(await run('execute in bm:gutter if entity @e[tag=bm.gvboss]')); k++) {
      if (/bm.gvshell/.test(await run('execute in bm:gutter run data get entity @e[tag=bm.gvboss,limit=1] Tags'))) {      // (the Sentinel's gold shell: its four plates)
      for (const [x, z] of [[-6, -6], [6, -6], [-6, 6], [6, 6]]) await run(`execute in bm:gutter as ${vsel} at @s run summon minecraft:item ~${x} ~0.2 ~${z} {Item:{id:"minecraft:heavy_weighted_pressure_plate",count:1},PickupDelay:32767s,Tags:["hz_pw"]}`);
      await sleep(2500); await run('execute in bm:gutter run kill @e[type=minecraft:item,tag=hz_pw]'); }
    await run('execute in bm:gutter as @e[tag=bm.gvboss] run damage @s 40 minecraft:player_attack by TestRat'); await sleep(500); }
    await run(`execute in bm:gutter as ${vsel} at @s run kill @e[tag=bm.gvg,distance=..40]`);
    await wait(10000, async () => { const m = (await run(`execute in bm:gutter run scoreboard players get ${vsel} bm.gvs`)).match(/has (-?\d+)/); return m && +m[1] === 2; });
    A.dialogN.length = 0; B.dialogN.length = 0;
    await run(`execute in bm:gutter as ${vsel} at @s run tp TestRat ~16 ~ ~-3 -90 0`); await run(`execute in bm:gutter as ${vsel} at @s run tp TestRat2 ~16 ~ ~3 -90 0`);
    await sleep(500); A.stand(); B.stand();
    const paid = await wait(10000, async () => /passed/.test(await run('execute if items entity TestRat container.* minecraft:barrel')));
    ok(`${tag}: the strongbox pays out`, paid, paid ? '' : `boss left ${(await run('execute in bm:gutter if entity @e[tag=bm.gvboss]')).slice(0, 40)} | vault state ${(await run(`execute in bm:gutter run scoreboard players get ${vsel} bm.gvs`)).replace(/.*has /, '')}`);
    await wait(8000, async () => A.buttons().some(b => /Go to the Lounge/.test(b.label)) && B.buttons().some(b => /Go to the Lounge/.test(b.label)));
    show(A, `${tag}: leader's screen`); show(B, `${tag}: member's screen`);
    ok(`${tag}: the leader and the member each get a screen with "Go to the Lounge"`, A.buttons().some(b => /Go to the Lounge/.test(b.label)) && B.buttons().some(b => /Go to the Lounge/.test(b.label)));
    return gi;
  }
  const inLounge = async n => /gutter/.test(await dim(n)) && await fnTrue(`as ${n}`, 'bm:p121/inside') && !(await tagged(n, 'bm.gvp'));
  async function walkHome(C_, n) {
    const ex = (await run('execute in bm:gutter run data get entity @e[type=minecraft:marker,tag=bm.lgexit,limit=1] Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
    if (ex) await C_.walkTo(+ex[1], +ex[3]);
    await wait(4000, async () => /overworld/.test(await dim(n)));
    return /overworld/.test(await dim(n));
  }

  // ================================================================== heist 1: the leader takes the crew to the lounge
  const ONLY3 = process.argv[2] === '3';
  if (!ONLY3 && await heist('Heist 1') !== null) {
    A.chats.length = 0; B.chats.length = 0;
    const g = await A.press(/Go to the Lounge/); await sleep(2500);
    ok('Heist 1: the leader presses "Go to the Lounge" - the whole crew is in the lounge, the heist over', !!g && await inLounge('TestRat') && await inLounge('TestRat2'),
       `${await dim('TestRat')} / ${await dim('TestRat2')} | B: ${B.chats.slice(-2).join(' / ').slice(0, 200)}`);
    await sleep(800); A.stand(); B.stand();
    ok('...each walks out through its door - home', await walkHome(A, 'TestRat') && await walkHome(B, 'TestRat2'));
    await sleep(1000); A.stand(); B.stand();
  }
  // ================================================================== heist 2: a member goes on their own; the leader heads home
  if (!ONLY3 && await heist('Heist 2') !== null) {
    A.chats.length = 0;
    const m = await B.press(/Go to the Lounge/); await sleep(2500);
    ok('Heist 2: the member presses "Go to the Lounge" - they\'re in the lounge, the leader still deciding', !!m && await inLounge('TestRat2') && await tagged('TestRat', 'bm.gvp') && /gutter/.test(await dim('TestRat')),
       `${await dim('TestRat2')} | A heard: ${A.chats.slice(-1).join('').slice(0, 160)}`);
    await sleep(500);
    const h = await A.press(/Back to the Overworld/); await sleep(2500);
    ok('...the leader presses "Back to the Overworld" - home; the member stays in the lounge', !!h && /overworld/.test(await dim('TestRat')) && !(await tagged('TestRat', 'bm.gvp')) && await inLounge('TestRat2'),
       `${await dim('TestRat')} / ${await dim('TestRat2')}`);
    await sleep(800); B.stand();
    ok('...and the member\'s door takes them home', await walkHome(B, 'TestRat2'));
  }
  // ================================================================== heist 3: the leader starts a new raid; the member opts out to the lounge
  await sleep(1000); A.stand(); B.stand();
  if (await heist('Heist 3') !== null) {
    B.dialogN.length = 0;
    const nr = await A.press(/Start a new raid/); await sleep(1500);
    await wait(6000, async () => B.buttons().some(b => /Go to the Lounge/.test(b.label)), 200);
    show(B, 'Heist 3: member asked to go again'); show(A, 'Heist 3: leader');
    const out = await B.press(/Go to the Lounge/); await sleep(2500);
    ok('Heist 3: the leader starts a new raid; the member, asked to go again, presses "Go to the Lounge" - in the lounge, out of the crew',
       !!nr && !!out && await inLounge('TestRat2') && /gutter/.test(await dim('TestRat')), `${await dim('TestRat2')} | leader ${await dim('TestRat')}`);
    await sleep(800); B.stand();
    ok('...and the member\'s door takes them home', await walkHome(B, 'TestRat2'));
  }
  await run(`${O}forceload remove ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const n of NAMES) await run(`scoreboard players reset ${n} bm.pty`);
  const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
  A.end(); B.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

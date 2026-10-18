// 2.82m: A CREW OF TWO - THE WHOLE KIT BACK FOR A NEW RAID, NOBODY SHUT OUT OF THE AMBUSH, ADVENTURE MODE ALL THE WAY - as regular
// (non-op) players TestRat (the leader) and TestMouse, every step a real packet (rcon sets the stage: a party, Tokens, the Ledger,
// the kits and their wind-charge secondaries, where each raider stands when the ambush springs).
//   THE KIT: TestRat (Ranged kit) throws wind charges and arrows' worth of the kit away by using them; TestMouse (Support kit)
//   throws a healing potion. The heist ends, TestRat presses Start a new raid and plans it through the Ledger, TestMouse is in:
//   both walk into the new den with the whole kit back - the secondary's 12 wind charges, the support's potions - no more.
//   THE AMBUSH: the Arcane Study springs on TestRat while TestMouse is still outside; the bars drop - and TestMouse, walking up
//   to them, is let through to the fight.
//   ADVENTURE MODE: from the first den to the last, every second, neither raider is ever in survival down there.
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const num = async c => +(((await run(c)).match(/(?:has |Found )(-?\d+)/) || [0, -1])[1]);
  const G = 'execute in bm:gutter run ';
  const passes = async c => /passed/i.test(await run(c));
  const have = async (who, item) => { const o = await run(`clear ${who} ${item} 0`); return /No items/.test(o) ? 0 : +((o.match(/(\d+)/) || [0, 0])[1]); };
  const WC = 'minecraft:wind_charge[minecraft:custom_data~{bm_kit:1b}]';
  const POT = 'minecraft:splash_potion[minecraft:custom_data~{bm_kit:1b}]';
  const NAMES = ['TestRat', 'TestMouse'];

  const A = await bot('TestRat'); await sleep(1500); const M = await bot('TestMouse'); await sleep(2000);
  A.stand(); M.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); M.cmd('gamemode creative'); await sleep(700);
  ok('TestRat is a regular player (and so is TestMouse)', /unknown|incomplete|permission/i.test(A.chats.join(' ')));

  // ---- the stage: no heist running, a party of two led by TestRat, Tokens, the Ledger
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const f of ['plan_anywhere', 'heist_variants_never', 'prime_never', 'fork_never', 'traps_never', 'curse_never', 'rooms_only_ambush']) await run(`function bm:admin/${f}`);
  await run('execute in minecraft:overworld run fill 12996 119 12996 13004 119 13004 stone');
  for (const [i, n] of NAMES.entries()) {
    await run(`clear ${n}`); await run(`gamemode survival ${n}`); await run(`effect give ${n} resistance 900 4 true`); await run(`effect give ${n} saturation 900 0 true`);
    await run(`tag ${n} remove bm.gvp`); await run(`scoreboard players reset ${n} bm.gvi`); await run(`scoreboard players set ${n} bm.gvhc 0`);
    await run(`execute as ${n} unless score @s bm.pid matches 1.. run function bm:p21/pid`);
    await run(`execute in minecraft:overworld run tp ${n} ${13000.5 + i} 120 13000.5`);
    for (let k = 0; k < 16; k++) await run(`loot give ${n} loot bm:items/token`);
    await run(`scoreboard players set ${n} bm.gvu 5`); await run(`scoreboard players set ${n} bm.gval 1`);
    await run(`scoreboard players set ${n} bm.ksec 3`);                       // (the secondary: Wind Charges)
  }
  for (const n of NAMES) await run(`scoreboard players operation ${n} bm.pty = TestRat bm.pid`);
  await run('loot replace entity TestRat hotbar.7 loot bm:items/fixers_ledger');
  await sleep(2000);

  // ---- adventure mode, watched every second from here to the end
  let watching = false; const slips = [];
  const watch = setInterval(async () => {
    if (!watching) return;
    for (const n of NAMES) {
      try { if (await passes(`execute as ${n} if entity @s[tag=bm.gvp,gamemode=survival] if dimension bm:gutter`)) slips.push(`${n} @${Date.now() % 100000}`); } catch (e) {}
    }
  }, 1000);

  const gvi = n => num(`scoreboard players get ${n} bm.gvi`);
  const plan = async (from = -99) => {                          // the Ledger's buttons, as sent: Tier I, then 7 tries
    A.cmd('trigger bm.act set 7601'); await sleep(1500); A.cmd('trigger bm.act set 7613');
    await sleep(1500);
    if (M.buttons().length) await M.press(/I'm in|Join|opt in|Count me in/i);
    return wait(40000, async () => (await passes('execute if entity @a[name=TestRat,tag=bm.gvp]')) && (await gvi('TestRat')) !== from, 500);
  };
  A.slot(7); await sleep(300); await A.useWait(); await sleep(400); A.cmd('trigger bm.act set 7809'); await sleep(800);
  const in1 = await plan(); await sleep(2500);
  const GI1 = await gvi('TestRat');
  ok('a heist planned through the Ledger: both raiders are in its den', in1 && (await gvi('TestMouse')) === GI1, `gvi ${GI1} / ${await gvi('TestMouse')}`);
  watching = true;

  // ---- the kits (the stage): TestRat Ranged, TestMouse Support, both with the wind charges
  await run('scoreboard players set TestRat bm.gvrole 3'); await run('execute as TestRat run function bm:p72/kit/give_3');
  await run('scoreboard players set TestMouse bm.gvrole 4'); await run('execute as TestMouse run function bm:p72/kit/give_4');
  await sleep(500);
  const wc0 = await have('TestRat', WC), wm0 = await have('TestMouse', WC), pm0 = await have('TestMouse', POT);
  ok('the kits carry the secondary\'s wind charges (and the support\'s potions)', wc0 === 12 && wm0 === 12 && pm0 >= 1, `rat ${wc0}, mouse ${wm0}, potions ${pm0}`);
  const toHand = async (who, item, sl) => {
    let src = -1; for (let i = 0; i < 36 && src < 0; i++) if (await passes(`execute if items entity ${who} container.${i} ${item}`)) src = i;
    if (src >= 0 && src !== sl) await run(`item replace entity ${who} hotbar.${sl} from entity ${who} container.${src}`), await run(`item replace entity ${who} container.${src} with minecraft:air`);
  };
  await toHand('TestRat', WC, 8); A.slot(8); await sleep(300);
  for (let k = 0; k < 3; k++) { A.use(); await sleep(200); A.release(); await sleep(700); }
  await toHand('TestMouse', POT, 8); M.slot(8); await sleep(300); M.use(); await sleep(200); M.release(); await sleep(800);
  const wc1 = await have('TestRat', WC), pm1 = await have('TestMouse', POT);
  ok('...TestRat throws three wind charges, TestMouse a potion (real right-clicks)', wc1 === wc0 - 3 && pm1 === pm0 - 1, `wind ${wc0} -> ${wc1}, potions ${pm0} -> ${pm1}`);

  // ---- the ambush: TestRat in the study, TestMouse behind; the trap springs on TestRat
  const room = `@e[type=minecraft:marker,tag=bm.gvr_ambush,scores={bm.gvi=${GI1}},sort=nearest,limit=1]`;
  const LB = `@e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${GI1}},limit=1]`;
  const lp = (await run(`${G}data get entity ${LB} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  const [bx, by, bz] = [Math.floor(+lp[1]) + 11, Math.floor(+lp[2]) + 1, Math.floor(+lp[3]) + 3];
  await run(`execute in bm:gutter as ${LB} at @s run tp TestRat ~10 ~ ~3 -90 0`); await sleep(1500);
  A.useOn(bx, by, bz, 4); await sleep(2500);
  const inst = `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${GI1}},limit=1]`;
  if ((await num(`${G}scoreboard players get ${inst} bm.gvst`)) < 2) { A.useOn(bx, by, bz, 4); }
  const begun = await wait(6000, async () => (await num(`${G}scoreboard players get ${inst} bm.gvst`)) >= 2);
  // (the stage: the room ahead is the study; TestMouse in the doorway behind, a step short of the bars' reach, TestRat just inside)
  await run(`${G}execute as ${room} at @s run tp TestMouse ~-16.1 ~ ~0.5 -90 0`);
  await run(`${G}execute as ${room} at @s run tp TestRat ~2.5 ~ ~0.5 -90 0`);
  const barred = await wait(4000, async () => passes(`${G}execute as ${room} at @s if block ~-12 ~ ~ minecraft:iron_bars`));
  ok('BEGIN pressed; the Arcane Study springs on TestRat and its bars drop behind him', begun && barred, `begun ${begun} barred ${barred}`);
  await sleep(1000);
  const out = await passes(`${G}execute as ${room} at @s positioned ~-16 ~ ~-3 if entity @a[name=TestMouse,dx=3.5,dy=4,dz=5]`);
  M.bars.length = 0;
  // TestMouse walks up to the bars (real movement packets)
  const mp = (await run(`${G}data get entity ${room} Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  await M.walkTo(+mp[1] - 12.8, +mp[3] + 0.5).catch(() => {});
  const through = await wait(4000, async () => passes(`${G}execute as ${room} at @s positioned ~-11.4 ~ ~-12 if entity @a[name=TestMouse,dx=22,dy=6,dz=24]`), 250);
  ok('...TestMouse, left outside, walks up to the bars and is let through to the fight', out && through, `outside first ${out}, through ${through} ${M.bars.slice(-1).join('')}`);

  // ---- the heist ends (the stage: its own "home, or another job?"), TestRat presses Start a new raid, TestMouse is in
  await run(`${G}kill @e[tag=bm.gvg,scores={bm.gvi=${GI1}}]`);
  await run(`execute as ${inst.replace('limit=1', 'limit=1')} run scoreboard players set @s bm.gvst 4`.replace('execute as', 'execute in bm:gutter as'));
  for (const n of NAMES) await run(`execute in bm:gutter as ${LB} at @s run tp ${n} ~8 ~ ~3 -90 0`);
  await sleep(1500);
  await run(`execute as TestRat at @s run function bm:p101/s${GI1 - 1}/ask`); await sleep(1200);
  M.dialogN && (M.dialogN.length = 0);
  const sn = await A.press(/Start a new raid/); await sleep(1500);
  await wait(6000, async () => M.buttons().some(b => /Count me in/.test(b.label)), 200);
  const cm = await M.press(/Count me in/); await sleep(1500);
  ok('the heist-over dialog offers Start a new raid, TestRat presses it, and TestMouse presses Count me in', !!sn && !!cm);
  const in2 = await plan(GI1); await sleep(3000);
  const GI2 = await gvi('TestRat');
  const wc2 = await have('TestRat', WC), wm2 = await have('TestMouse', WC), pm2 = await have('TestMouse', POT);
  ok('Start a new raid: both in the new den, the whole kit back - 12 wind charges each, the support\'s potions - no more',
     in2 && GI2 !== GI1 && (await gvi('TestMouse')) === GI2 && wc2 === 12 && wm2 === 12 && pm2 === pm0,
     `heist ${GI1} -> ${GI2} (mouse ${await gvi('TestMouse')}), wind ${wc1} -> ${wc2} / ${wm0} -> ${wm2}, potions ${pm1} -> ${pm2}`);
  await sleep(2500);
  watching = false;
  ok('from the first den to the last, neither raider was ever in survival down there for a second', slips.length === 0, slips.slice(0, 6).join(', '));

  // ---- clean up
  clearInterval(watch);
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  for (const f of ['prime_chance', 'fork_chance', 'traps_chance', 'curse_chance', 'rooms_any', 'plan_safe']) await run(`function bm:admin/${f}`);
  for (const n of NAMES) { await run(`tag ${n} remove bm.gvp`); await run(`scoreboard players reset ${n} bm.gvi`); await run(`scoreboard players reset ${n} bm.pty`);
    await run(`scoreboard players set ${n} bm.ksec 0`); await run(`clear ${n}`); await run(`effect clear ${n}`); await run(`gamemode survival ${n}`);
    await run(`execute in minecraft:overworld run tp ${n} 13000.5 120 13000.5`); }
  console.log(`\n${res.filter(Boolean).length}/${res.length} passed`);
  A.end(); M.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

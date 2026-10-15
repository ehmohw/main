// URGENT (2.76): the Ledger, played as a regular (non-op) player - every step is a real packet: the item used, the buttons
// read off the dialog the client is shown and pressed by sending exactly the command each carries, standing still, walking.
// (rcon only sets the stage: a platform, a few tokens, clearing rooms the test isn't about - never a menu step.)
const { bot, rcon, sleep } = require('./lib_resp');
const res = [];
(async () => { const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const sc = async (who, o) => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };
  const passes = async c => /passed/i.test(await run(c));
  const fnTrue = async (pre, f) => /returned [1-9]/.test(await run(`execute ${pre} run function ${f}`));     // (26.3: 'execute if function' can't end a command)
  const wait = async (ms, fn, step = 250) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const dim = async () => (await run('data get entity TestRat Dimension')).replace(/.*data: /, '');
  const show = (tag) => console.log(`   [${tag}] ` + A.buttons().map(b => `${b.label.replace(/[^\x20-\x7e·]/g, '').trim()} <${b.command.replace('/trigger bm.act set ', '')}>`).join(' | '));
  const O = 'execute in minecraft:overworld run ';
  const HX = 13000, HY = 121, HZ = 13000;
  const A = await bot('TestRat'); await sleep(2500);
  // ---- the stage
  for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
  await run(`${O}forceload add ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
  await run(`${O}fill ${HX - 4} ${HY - 1} ${HZ - 4} ${HX + 4} ${HY - 1} ${HZ + 4} minecraft:stone`);
  await run(`${O}fill ${HX - 4} ${HY} ${HZ - 4} ${HX + 4} ${HY + 3} ${HZ + 4} minecraft:air`);
  await run(`${O}tp TestRat ${HX + 0.5} ${HY} ${HZ + 0.5} 0 0`); await run('gamemode survival TestRat'); await run('clear TestRat'); await run('effect clear TestRat');
  await run(`spawnpoint TestRat ${HX} ${HY} ${HZ}`);
  for (const t of ['bm.gvp', 'bm.gvask', 'bm.gvnext', 'bm.gvoffer', 'bm.gvwaitd', 'bm.lgch', 'bm.lkch']) await run(`tag TestRat remove ${t}`);
  await run('scoreboard players reset TestRat bm.pty'); await run('scoreboard players set TestRat bm.gvcl 0');
  await sleep(1500); A.stand(); await sleep(500);
  // 0. a regular player: no operator commands
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(600);
  ok('TestRat is a regular player (no operator commands)', /unknown|incomplete|permission/i.test(A.chats.join(' ')) && (await run('data get entity TestRat playerGameType')).endsWith(' 0'), A.chats.slice(-1).join('').slice(0, 120));

  // ================================================================== 1. an old Ledger (as players carry it since 2.74) is re-issued
  // (a Ledger as it was before 2.76 - lying at your feet; you pick it up)
  await run(`${O}summon minecraft:item ${HX + 0.5} ${HY + 0.2} ${HZ + 0.5} {Tags:["t131old"],PickupDelay:20s,Item:{id:"minecraft:totem_of_undying",count:1,components:{"minecraft:item_model":"bm:fixers_ledger","minecraft:max_stack_size":1,"!minecraft:death_protection":{},"minecraft:consumable":{consume_seconds:100000.0f,animation:"none",sound:"minecraft:intentionally_empty",has_consume_particles:false},"minecraft:custom_data":{bm:"fixers_ledger",bmv:33},"minecraft:item_name":{text:"The Fixer's Ledger"},"minecraft:lore":[{text:"A battered book with your name in it.",color:"gray",italic:false},{text:"Use: the Fixer's Office - the Armory",color:"blue",italic:false}]}}}`);
  const old = await run(`${O}data get entity @e[type=minecraft:item,tag=t131old,limit=1] Item.components."minecraft:custom_data"`);
  await wait(4000, async () => /passed/.test(await run('execute if items entity TestRat container.* *[minecraft:custom_data~{bm:"fixers_ledger"}]')));
  await sleep(2000);
  const nowCd = await run('data get entity TestRat Inventory[{id:"minecraft:totem_of_undying"}].components."minecraft:custom_data"');
  const nowLore = await run('data get entity TestRat Inventory[{id:"minecraft:totem_of_undying"}].components."minecraft:lore"');
  ok('An old Ledger you pick up is re-issued as the current one (its lore now says it plans heists)', /bmv: 33/.test(old) && !/bmlv/.test(old) && /bmlv: 276/.test(nowCd) && /plan a heist/i.test(nowLore),
     `${old.replace(/.*data: /, '')} -> ${nowCd.replace(/.*data: /, '')}`);
  const lslot = +(((await run('data get entity TestRat Inventory[{id:"minecraft:totem_of_undying"}].Slot')).match(/(\d+)b?\s*$/) || [0, 0])[1]);
  if (lslot !== 0) { await run(`item replace entity TestRat hotbar.0 from entity TestRat container.${lslot}`); await run(`item replace entity TestRat container.${lslot} with minecraft:air`); }

  // ================================================================== 2. the Office: Plan a Heist on top, the Lounge
  A.slot(0); await sleep(300); await A.useWait();
  show('office');
  const b0 = A.buttons();
  ok('Using the Ledger opens the Office', b0.length > 5, `${b0.length} buttons`);
  ok('...and "Plan a Heist" heads it', b0.length && /Plan a Heist/.test(b0[0].label), b0[0] && b0[0].label);
  ok('...and "The Fixer\'s Lounge" is on it', b0.some(b => /Fixer's Lounge/.test(b.label)));

  // ================================================================== 3. the Lounge button: hold still 3 seconds - in the lounge
  A.chats.length = 0; A.bars.length = 0;
  const lb = A.click(/Fixer's Lounge/); await sleep(800);
  ok('Pressing "The Fixer\'s Lounge" starts the 3-second hold', /Hold still/i.test(A.chats.join(' ')) || /Lounge/i.test(A.bars.join(' ')), `${lb && lb.command} | ${A.chats.slice(-2).join(' / ').slice(0, 160)} | ${A.bars.slice(-1).join('').slice(0, 80)}`);
  await wait(6000, async () => /gutter/.test(await dim()));
  await sleep(600);
  ok('...stand still - and you\'re in the Fixer\'s Lounge', /gutter/.test(await dim()) && await fnTrue('as TestRat', 'bm:p121/inside'), `${await dim()} ${(await run('data get entity TestRat Pos')).replace(/.*data: /, '')} | ${A.chats.slice(-2).join(' / ').slice(0, 200)}`);
  await sleep(1500); A.stand();

  // ================================================================== 4. in the lounge the Ledger still plans heists
  await A.useWait();
  show('office in the lounge');
  ok('In the lounge the Office still has "Plan a Heist"', A.buttons().some(b => /Plan a Heist/.test(b.label)));
  A.chats.length = 0; A.bars.length = 0; const pl = await A.press(/Plan a Heist/);
  show('planner from the lounge');
  ok('...and pressing it opens the heist planner', pl && pl.next && A.buttons().some(b => /Tier/i.test(b.label)), `${A.bars.slice(-1).join('').slice(0, 120)} ${A.chats.slice(-1).join('').slice(0, 120)}`);

  // ================================================================== 5. walk out through the lounge's door - home
  const ex = (await run('execute in bm:gutter run data get entity @e[type=minecraft:marker,tag=bm.lgexit,limit=1] Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  if (ex) await A.walkTo(+ex[1], +ex[3]);
  await wait(4000, async () => /overworld/.test(await dim()));
  const hp = (await run('data get entity TestRat Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  ok('Walking through the lounge\'s door takes you home, where you were', /overworld/.test(await dim()) && hp && Math.abs(+hp[1] - HX - 0.5) < 2 && Math.abs(+hp[3] - HZ - 0.5) < 2, `${await dim()} ${hp && hp.slice(1).join(',')}`);
  await sleep(1000); A.stand();

  // ================================================================== 6. a heist, planned from the Ledger's buttons
  for (let k = 0; k < 3; k++) await run('loot give TestRat loot bm:items/token');
  A.slot(0); await sleep(200); await A.useWait();
  await A.press(/Plan a Heist/); show('planner');
  const tb = await A.press(/Tier I\b(?!I)/); show('tries');
  A.chats.length = 0; const lvb = await A.press(/^3\b|3 tries/i); show('after tries');
  ok('Plan a Heist -> Tier I -> 3 tries (buttons pressed as shown)', !!tb && !!lvb, `${tb && tb.label} / ${lvb && lvb.label} | ${A.chats.slice(-2).join(' / ').slice(0, 200)}`);
  const inV = await wait(60000, async () => /gutter/.test(await dim()) && await passes('execute if entity @a[name=TestRat,tag=bm.gvp]'));
  ok('...the fee is paid and you\'re led down into the vault', inV, `${await dim()} | ${A.chats.slice(-3).join(' / ').slice(0, 260)}`);
  if (!inV) return end();
  await sleep(2500); A.stand();
  const gi = await sc('TestRat', 'bm.gvi');
  const inst = `@e[type=minecraft:marker,tag=bm.gvinst,scores={bm.gvi=${gi}},limit=1]`;
  const iscore = async o => { const m = (await run(`execute in bm:gutter run scoreboard players get ${inst} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : NaN; };

  // ---- the heist's Office: Leave the heist, Skip this puzzle; no planning, no lounge
  await A.useWait(); show('office on a heist');
  const hb = A.buttons();
  ok('On a heist the Ledger opens the heist\'s Office: "Leave the heist" and "Skip this puzzle", no "Plan a Heist"',
     hb.some(b => /Leave the heist/.test(b.label)) && hb.some(b => /Skip this puzzle/.test(b.label)) && !hb.some(b => /Plan a Heist|Fixer's Lounge/.test(b.label)));

  // ---- BEGIN: right-click the den's button
  const lp = (await run(`execute in bm:gutter run data get entity @e[type=minecraft:marker,tag=bm.gvr_lobby,scores={bm.gvi=${gi}},limit=1] Pos`)).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  const [lx, ly, lz] = lp.slice(1).map(v => Math.floor(+v));
  await run(`execute in bm:gutter run tp TestRat ${lx + 9.5} ${ly + 1} ${lz + 3.5} -90 0`); await sleep(1200); A.stand();
  A.chats.length = 0; A.useOn(lx + 11, ly + 1, lz + 3, 4); await sleep(1500);
  const rdy = A.chats.join(' ');
  ok('Right-clicking BEGIN with no kit: the ready check says so ("press BEGIN again")', /Not everyone's ready/.test(rdy) && (await iscore('bm.gvst')) === 1, rdy.slice(-160));
  await sleep(2200); A.useOn(lx + 11, ly + 1, lz + 3, 4); await sleep(1500);
  ok('...pressing BEGIN again starts the heist', (await iscore('bm.gvst')) === 2, `state ${await iscore('bm.gvst')}`);
  await run('effect give TestRat minecraft:resistance 3600 4 true');

  // ---- the rooms: the first puzzle room is skipped with the Ledger's button; the rest are cleared for the test
  const rooms = [];
  for (let q = 1; q <= 12; q++) {
    const t = await run(`execute in bm:gutter run data get entity @e[type=minecraft:marker,tag=bm.gvr,tag=!bm.gvr_vault,tag=!bm.gvr_lobby,tag=!bm.gvr_cache,scores={bm.gvi=${gi},bm.gvq=${q}},limit=1] Tags`);
    if (!/\[/.test(t)) continue; const kind = (t.match(/"bm\.gvr_([a-z]+)"/) || [])[1]; rooms.push({ q, kind });
  }
  console.log('   rooms: ' + rooms.map(r => `${r.q}:${r.kind}`).join(', '));
  let skipped = false;
  for (const r of rooms) {
    const sel = `@e[type=minecraft:marker,tag=bm.gvr,scores={bm.gvi=${gi},bm.gvq=${r.q}},limit=1]`;
    const puzzle = await fnTrue(`in bm:gutter as ${sel}`, 'bm:p122/is_puzzle');
    await run(`execute in bm:gutter as ${sel} at @s run tp TestRat ~-10 ~ ~ -90 0`); await sleep(1500); A.stand();
    if (puzzle && !skipped) {
      const lv0 = await iscore('bm.gvlv');
      await A.useWait();
      await A.press(/Skip this puzzle/); show('skip?');
      // (2.76c) "Keep at it" first: the question closes, nothing else - it used to open the standing screen
      const kb = await A.press(/Keep at it/); await sleep(600);
      const s0 = (await run(`execute in bm:gutter run scoreboard players get ${sel} bm.gvs`)).match(/has (-?\d+)/);
      const pm = ((await run('scoreboard players get TestRat bm.menu')).match(/has (-?\d+)/) || [])[1];
      ok('"Keep at it" just closes the question - no other screen opens (not the standing screen), no try spent, the room still to solve',
         !!kb && !kb.next && pm !== '1' && (await iscore('bm.gvlv')) === lv0 && !(s0 && +s0[1] === 3), `next screen ${kb && kb.next}; menu ${pm}; tries ${await iscore('bm.gvlv')}`);
      await A.useWait(); await A.press(/Skip this puzzle/);
      const yb = await A.press(/Skip it|Yes|skip/i); await sleep(1200);
      const s = (await run(`execute in bm:gutter run scoreboard players get ${sel} bm.gvs`)).match(/has (-?\d+)/);
      ok(`In a puzzle room (${r.kind}) the Ledger's "Skip this puzzle" asks, then opens the way for a try`, yb && s && +s[1] === 3 && (await iscore('bm.gvlv')) === lv0 - 1,
         `${yb && yb.label} | solved ${s && s[1]} | tries ${lv0} -> ${await iscore('bm.gvlv')}`);
      skipped = true; continue;
    }
    await run(`execute in bm:gutter as ${sel} at @s run function bm:p70/solved`); await sleep(400);
    await run(`execute in bm:gutter as ${sel} at @s run kill @e[tag=bm.gvg,distance=..30]`);
  }
  if (!skipped) console.log('   (no puzzle room in this heist - skip not tried)');

  // ---- the vault: the guardian falls (cleared for the test), stand on the strongbox's plate - the Haul
  const vsel = `@e[type=minecraft:marker,tag=bm.gvr_vault,scores={bm.gvi=${gi}},limit=1]`;
  await run(`execute in bm:gutter as ${vsel} at @s run tp TestRat ~-6 ~ ~ -90 0`); await sleep(3000); A.stand();
  for (let k = 0; k < 60 && /Count: [1-9]|passed/i.test(await run('execute in bm:gutter if entity @e[tag=bm.gvboss]')); k++) {
    if (/bm.gvshell/.test(await run('execute in bm:gutter run data get entity @e[tag=bm.gvboss,limit=1] Tags'))) {      // (the Sentinel's gold shell: its four plates)
      for (const [x, z] of [[-6, -6], [6, -6], [-6, 6], [6, 6]]) await run(`execute in bm:gutter as ${vsel} at @s run summon minecraft:item ~${x} ~0.2 ~${z} {Item:{id:"minecraft:heavy_weighted_pressure_plate",count:1},PickupDelay:32767s,Tags:["hz_pw"]}`);
      await sleep(2500); await run('execute in bm:gutter run kill @e[type=minecraft:item,tag=hz_pw]'); }
    await run('execute in bm:gutter as @e[tag=bm.gvboss] run damage @s 40 minecraft:player_attack by TestRat'); await sleep(500); }
  await run(`execute in bm:gutter as ${vsel} at @s run kill @e[tag=bm.gvg,distance=..40]`);
  await wait(10000, async () => { const m = (await run(`execute in bm:gutter run scoreboard players get ${vsel} bm.gvs`)).match(/has (-?\d+)/); return m && +m[1] === 2; });
  await run(`execute in bm:gutter as ${vsel} at @s run tp TestRat ~16 ~ ~-3 -90 0`); await sleep(500); A.stand();
  A.dialogN.length = 0; A.chats.length = 0;
  const paid = await wait(10000, async () => /passed/.test(await run('execute if items entity TestRat container.* minecraft:barrel')));
  ok('The strongbox pays out: the Haul', paid);

  // ================================================================== 7. the heist is over: the results - and "Go to the Lounge"
  await wait(8000, async () => A.buttons().some(b => /Go to the Lounge/.test(b.label)));
  show('the heist is over');
  ok('The end-of-heist screen offers "Go to the Lounge"', A.buttons().some(b => /Go to the Lounge/.test(b.label)), `${A.dialogN.length} dialogs`);
  const tok0 = +(((await run('clear TestRat *[minecraft:custom_data~{bm:"token"}] 0')).match(/Found (\d+)/) || [0, 0])[1]);
  A.chats.length = 0; const gl = A.click(/Go to the Lounge/); await sleep(2500);
  ok('...pressing it: the heist ends and you\'re in the Fixer\'s Lounge', !!gl && /gutter/.test(await dim()) && await fnTrue('as TestRat', 'bm:p121/inside') && !(await passes('execute if entity @a[name=TestRat,tag=bm.gvp]')),
     `${gl && gl.command} | ${await dim()} | ${A.chats.slice(-3).join(' / ').slice(0, 260)}`);
  ok('...with your Haul, and your coat-check things back', /passed/.test(await run('execute if items entity TestRat container.* minecraft:barrel')) &&
     +(((await run('clear TestRat *[minecraft:custom_data~{bm:"token"}] 0')).match(/Found (\d+)/) || [0, 0])[1]) >= tok0, '');
  await sleep(1000); A.stand();
  // the lounge's door: home
  const ex2 = (await run('execute in bm:gutter run data get entity @e[type=minecraft:marker,tag=bm.lgexit,limit=1] Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  if (ex2) await A.walkTo(+ex2[1], +ex2[3]);
  await wait(4000, async () => /overworld/.test(await dim()));
  const hp2 = (await run('data get entity TestRat Pos')).match(/\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]/);
  ok('...and its door takes you home - where you planned the heist', /overworld/.test(await dim()) && hp2 && Math.abs(+hp2[1] - HX - 0.5) < 3 && Math.abs(+hp2[3] - HZ - 0.5) < 3, `${await dim()} ${hp2 && hp2.slice(1).join(',')}`);
  await sleep(1000); A.stand();

  // ================================================================== 8. the Rat Bank: Red Xenite's own buttons
  await sleep(3000);       // (2.78: what you carried out of the Lounge comes back a couple of seconds after your gear - let it land first)
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.1 loot bm:items/bankers_card'); for (let k = 0; k < 5; k++) await run('loot give TestRat loot bm:items/xenite_red');
  await run('scoreboard players set TestRat bm.bk_xr 0'); await run('scoreboard players set TestRat bm.bk_tok 3');
  A.slot(1); await sleep(300); await A.useWait();
  await A.press(/Red Xenite/);                                    // (2.80: the account page, then Red Xenite's own page)
  const bb = A.buttons(); const di = bb.findIndex(b => /Deposit all Red Xenite/.test(b.label));
  console.log('   [bank] ' + bb.map(b => `${b.label} <${b.command.replace('/trigger bm.act set ', '')}>`).join(' | '));
  const n1 = A.dialogN.length; if (di >= 0) A.cmd(bb[di].command.slice(1)); await wait(2000, async () => A.dialogN.length > n1, 50);
  const xr = await sc('TestRat', 'bm.bk_xr'); const tk = +(((await run('clear TestRat *[minecraft:custom_data~{bm:"token"}] 0')).match(/Found (\d+)/) || [0, 0])[1]);
  ok('Rat Bank: "Deposit all Red Xenite" deposits the Red Xenite (and takes out no Token)', di >= 0 && xr === 5 && tk === 0 && (await sc('TestRat', 'bm.bk_tok')) === 3, `account ${xr}, tokens on you ${tk}`);
  const bb2 = A.buttons(); const t1 = bb2.findIndex(b => /^Take 1$/.test(b.label));
  if (t1 >= 0) A.cmd(bb2[t1].command.slice(1)); await sleep(900);
  ok('...and its "Take 1" gives one back', (await sc('TestRat', 'bm.bk_xr')) === 4 && /Found 1\b/.test(await run('clear TestRat *[minecraft:custom_data~{bm:"xenite_red"}] 0')), `account ${await sc('TestRat', 'bm.bk_xr')}`);

  // ================================================================== 9. the Armory: the Tier V signature can be picked
  await run('scoreboard players set TestRat bm.gvcl 62'); await run('scoreboard players set TestRat bm.ksig 0');
  await run('loot replace entity TestRat hotbar.0 loot bm:items/fixers_ledger'); A.slot(0); await sleep(300);
  await A.useWait();
  await A.press(/Armory/);   // (2.78: the Office's names lost their "The") show('armory');
  await A.press(/signature/i); show('signature');
  A.chats.length = 0; const ad = A.click(/Adrenaline/); await sleep(800);
  ok('Armory: the Tier V signature "Adrenaline" can be picked', !!ad && (await sc('TestRat', 'bm.ksig')) === 9, `${ad && ad.command} | ksig ${await sc('TestRat', 'bm.ksig')} | ${A.chats.slice(-1).join('').slice(0, 120)}`);
  await run('scoreboard players set TestRat bm.ksig 0');
  return end();

  async function end() {
    await run(`${O}forceload remove ${HX - 8} ${HZ - 8} ${HX + 8} ${HZ + 8}`);
    for (let s = 0; s < 8; s++) await run(`function bm:p70/s${s}/clean`);
    const pp = res.filter(Boolean).length; console.log(`\n${pp}/${res.length} passed`);
    A.end(); R.end(); process.exit(0);
  }
})().catch(e => { console.error(e); process.exit(1); });

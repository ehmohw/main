// 3.0p: THE LIGHTBRINGER'S CROSS, HER DOLL, AND THE DREAD EMBER - as a regular (non-op) player; rcon only sets the stage.
//   (a) hard mode, noon, open sky: TestRat (never met her) sets a Golden Cross down (sneak + use): a puff of light high above, she
//       glides down - her rig's parts stay where they stand while their translation eases down from ~7 blocks (interpolated, no
//       teleport) - and joins him: the feather in hand, bm:met/lightbringer, she comes along. A second cross: nothing.
//   (b) the feather gone (she goes home without it): her doll (Cecil's) set down by the cross - she comes down again, a new feather
//       ("You lost my feather"). With the feather on the Partner Wheel: only a hint, nobody comes; not hard mode: only a hint.
//   (c) the Dread Sovereign fallen (admin/under/fell, bm.dfin on TestRat), TestRat fresh again: a cross by day still brings her.
//   (d) the Dread Ember kindled (used as an item): #dfell 0; Dread Essence-free - the kill count past its mark and the normal roll
//       at dusk (p181/roll from p181/tick) books tonight; at 13000 the Dread Night falls (DREAD NIGHT, #dnight 1); dawn ends it.
//   (menus, cheap) the Handbook: "Followers met: N of <every bm:met/>", "Places found: 6 of 6" with all six found; its Followers
//       page title's grey part not bold (no inherited bold); the Partner Wheel: "⌂ Send all home", Cecil's "⚙ Menu" tooltip "his ways".
//   `node t395.js lean`: only (a) and the doll's respawn in (b).
const { bot, rcon, sleep } = require('./lib_resp');
const fs = require('fs');
(async () => {
  const res = [];
  const LEAN = process.argv[2] === 'lean';
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const num = async (sel, path) => +(((await nbt(sel, path)).match(/(-?[\d.]+)/) || [0, NaN])[1]);
  const score = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const passes = async (c) => /passed/i.test(await run(c));
  const give = async (iid, slot) => run(`loot replace entity TestRat ${slot} loot bm:items/${iid}`);
  const dd = (d) => d && (d.data || d);
  let A;
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const X = 18200, Y = 100, Z = 16200;
  const SLOT_LB = 41, SLOT_CECIL = 3;                // (phase179.SLOTS: frozen, saved by number)
  const ENC = '@e[type=minecraft:interaction,tag=bm.lhenc,limit=1]';
  const PET = '@e[type=minecraft:wolf,tag=bm.lhpet,tag=!bm.ffpet]';
  const HEAD = '@e[type=minecraft:item_display,tag=bm.lhencp,tag=bm.lhp_head,limit=1]';
  const metLB = async () => passes(`execute if entity @a[name=TestRat,advancements={bm:met/lightbringer=true}]`);
  const clearEnc = async () => { await run('kill @e[type=minecraft:interaction,tag=bm.lhenc]'); await run('kill @e[type=minecraft:item_display,tag=bm.lhencp]'); };
  const fresh = async () => {                          // (TestRat as one who has never met her)
    await run('kill @e[type=minecraft:wolf,tag=bm.lhpet]'); await clearEnc();
    for (const t of ['bm.lhmet', 'bm.lhcross', 'bm.lhseen']) await run(`tag TestRat remove ${t}`);
    await run('advancement revoke TestRat only bm:met/lightbringer'); await run('advancement revoke TestRat only bm:story/lightbringer_friend');
    await run(`scoreboard players set TestRat bm.pw${SLOT_LB} 0`); await run('clear TestRat *[minecraft:custom_data~{bm:"herald_feather"}]');
    await run('scoreboard players set TestRat bm.lhform 0'); await run('scoreboard players set TestRat bm.lhcd 0');
  };
  const sneakUse = async (slot) => { A.slot(slot); await sleep(300); A.input({ shift: true }); await sleep(300); A.use(); await sleep(250); A.release(); await sleep(500); A.input({}); await sleep(300); };
  const plainUse = async (slot) => { A.slot(slot); await sleep(300); A.use(); await sleep(350); A.release(); await sleep(500); };
  const crosses = async () => cnt(`@e[type=minecraft:marker,tag=bm.gcm,x=${X},y=${Y},z=${Z},distance=..12]`);
  // (one descent, watched: the puff, the head's translation easing down while it stays put, the feather)
  const descent = async (label) => {
    const came = await wait(3000, async () => (await cnt(ENC)) === 1);
    ok(`${label}: she is coming - her encounter, its show running (bm.lzsh)`, came && (await score('bm.lzsh', ENC)) > 0);
    await wait(3000, async () => (await num(HEAD, 'transformation.translation[1]')) > 3, 150);
    const y0 = await num(HEAD, 'transformation.translation[1]'), p0 = await num(HEAD, 'Pos[1]');
    await sleep(2500);
    const y1 = await num(HEAD, 'transformation.translation[1]'), p1 = await num(HEAD, 'Pos[1]'), dur = await num(HEAD, 'interpolation_duration');
    ok('...high up first, then gliding down: the translation falls, eased (interpolated), the part itself never moved', y0 > 3 && y1 < y0 && dur >= 10 && Math.abs(p1 - p0) < 0.01,
       `lift ${y0.toFixed(2)} -> ${y1.toFixed(2)}, interpolation ${dur}, Pos y ${p0} -> ${p1}`);
    const joined = await wait(12000, async () => (await has('herald_feather')) === 1);
    ok('...she alights and joins you: her feather in your pack', joined);
    return joined;
  };

  A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));

  // ---------------------------------------------------------------- the stage
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await run('weather clear'); await sleep(2500);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 12} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  const hard0 = await score('bm.cfg', '#hard'), fell0 = await score('bm.cfg', '#dfell'), dfin0 = await passes('execute if entity @a[name=TestRat,tag=bm.dfin]');
  const pwc0 = await score(`bm.pw${SLOT_CECIL}`), dkn0 = await score('bm.cfg', '#dkn');
  await run('scoreboard players set #dfell bm.cfg 0'); await run('tag TestRat remove bm.dfin');
  await run('scoreboard players set TestRat bm.wulightbringer 128');      // (no 1-in-100 shiny roll mid-test)
  await run(`${O}time set noon`); await run('scoreboard players set #hard bm.cfg 1');
  await fresh();
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 45);

  // ---------------------------------------------------------------- (a) the first cross, by day
  await give('golden_cross', 'hotbar.0'); await run('item modify entity TestRat hotbar.0 {type:"minecraft:set_count",count:2}');
  A.chats.length = 0; await sneakUse(0);
  ok('(a) a Golden Cross set down (sneak + use)', (await crosses()) === 1);
  ok('...a soft puff of light high over it: "Something is coming down through it, slowly, on open wings"', await wait(2000, async () => A.chats.some(c => /coming down through it/.test(c))));
  await descent('(a)');
  ok('...her met advancement, and she comes along (her follower out)', (await metLB()) && await wait(4000, async () => (await cnt(PET)) === 1));
  ok('..."She plucks a feather from her wing"', A.chats.some(c => /plucks a feather from her wing/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 200));
  ok('...the descended rig gone (only her follower remains)', (await cnt(ENC)) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.lhencp]')) === 0);
  await at(X - 3.5, Y + 1, Z + 0.5, 0, 45); A.chats.length = 0; await sneakUse(0);
  ok('a second cross by day: set down, and nobody comes', (await crosses()) === 2 && !(await wait(3000, async () => (await cnt(ENC)) > 0)));

  // ---------------------------------------------------------------- (b) her doll by a cross
  await run('clear TestRat *[minecraft:custom_data~{bm:"herald_feather"}]');
  ok('(b) the feather gone: she goes home without it', await wait(8000, async () => (await cnt(PET)) === 0));
  await give('doll_lightbringer', 'hotbar.1'); await run('item modify entity TestRat hotbar.1 {type:"minecraft:set_count",count:4}');
  await at(X + 2.5, Y + 1, Z + 0.5, 0, 45); A.chats.length = 0;
  await plainUse(1);
  ok('...her doll set down beside the first cross', (await cnt(`@e[type=minecraft:item_display,tag=bm.doll_lightbringerd,x=${X},y=${Y},z=${Z},distance=..10]`)) === 1);
  ok('..."The herald is coming down to you again"', await wait(2000, async () => A.chats.some(c => /coming down to you again/.test(c))));
  await descent('(b)');
  ok('..."You lost my feather? It is no matter"', A.chats.some(c => /You lost my feather/.test(c)));
  await sleep(1500);
  if (!LEAN) {                                       // (`node t395.js lean`: only the first cross and one doll respawn)
  // the feather on the Partner Wheel (off hand, the wheel used): a hint, nobody
  await run('clear TestRat *[minecraft:custom_data~{bm:"herald_feather"}]');
  await give('herald_feather', 'weapon.offhand'); await give('partner_wheel', 'hotbar.2'); await sleep(2300);
  await plainUse(2); await sleep(500);
  ok('...the feather put on the Partner Wheel (off hand, the wheel used)', (await score(`bm.pw${SLOT_LB}`)) === 1 && (await has('herald_feather')) === 0);
  await at(X + 4.5, Y + 1, Z + 0.5, 0, 45); A.bars.length = 0; await sleep(2300); await plainUse(1);
  ok('...a doll by the cross with the feather on the wheel: a gentle hint, and nobody comes', A.bars.some(b => /still have the herald's feather/.test(b)) &&
     !(await wait(2500, async () => (await cnt(ENC)) > 0)), A.bars.slice(-1).join(''));
  await run('scoreboard players set #hard bm.cfg 0'); await run(`scoreboard players set TestRat bm.pw${SLOT_LB} 0`);
  await at(X - 1.5, Y + 1, Z + 0.5, 0, 45); A.bars.length = 0; await plainUse(1);
  ok('...not hard mode (the feather nowhere): a hint, nobody', A.bars.some(b => /not sent yet/.test(b)) && !(await wait(2500, async () => (await cnt(ENC)) > 0)), A.bars.slice(-1).join(''));
  await run('scoreboard players set #hard bm.cfg 1');

  // ---------------------------------------------------------------- (c) after the Sovereign, a fresh player
  await run('function bm:admin/under/fell'); await run('tag TestRat add bm.dfin');
  await fresh(); await run(`${O}kill @e[type=minecraft:interaction,tag=bm.dollhit,x=${X},y=${Y},z=${Z},distance=..12]`);
  await run(`${O}kill @e[type=minecraft:item_display,tag=bm.dolld,x=${X},y=${Y},z=${Z},distance=..12]`);
  ok('(c) the Dread Sovereign has fallen (#dfell 1), TestRat marked by it (bm.dfin) and never met her', (await score('bm.cfg', '#dfell')) === 1);
  await give('golden_cross', 'hotbar.0'); await at(X + 0.5, Y + 1, Z - 4.5, 0, 45); A.chats.length = 0; await sneakUse(0);
  await descent('(c) a cross by day');
  ok('...met, all the same (bm:met/lightbringer)', await metLB());

  // ---------------------------------------------------------------- (d) the Dread Ember rekindled
  await run('kill @e[type=minecraft:wolf,tag=bm.lhpet]');
  await give('dread_ember', 'hotbar.3'); A.chats.length = 0;
  A.slot(3); await sleep(300); A.use(); await sleep(2400); A.release(); await sleep(800);
  ok('(d) the Dread Ember used: kindled - #dfell 0, the word to everyone', (await score('bm.cfg', '#dfell')) === 0 && A.chats.some(c => /kindled a Dread Ember/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
  ok('...hard mode still on', (await score('bm.cfg', '#hard')) === 1);
  // the normal roll: enough Dread counted, a day not yet rolled, dusk
  await run('scoreboard players operation #dkn bm.cfg = #dnt bm.cfg'); await run('scoreboard players set #dnr bm.bm -9');
  await run('scoreboard players set #forced bm.bm 0'); A.chats.length = 0;
  await run(`${O}time set 11000`);
  ok('...at dusk the normal roll books tonight (p181/roll: #dnday = today) - "Tonight is a Dread Night"', await wait(4000, async () =>
     (await score('bm.bm', '#dnday')) === (await score('bm.bm', '#day')) && A.chats.some(c => /Tonight is a Dread Night/.test(c))), A.chats.slice(-1).join('').slice(0, 160));
  A.titles && (A.titles.length = 0);
  await run(`${O}time set 13000`);
  ok('...and at nightfall the Dread Night falls (#dnight 1)', await wait(4000, async () => (await score('bm.bm', '#dnight')) === 1));
  await run(`${O}time set 23999`); await sleep(1500); await run(`${O}time add 6001`);
  ok('...dawn ends it', await wait(5000, async () => (await score('bm.bm', '#dnight')) !== 1));
  await run('kill @e[tag=bm.stalker]'); await run('kill @e[tag=bm.stkpart]');

  // ---------------------------------------------------------------- the menus, cheaply
  await run('tag TestRat add bm.hb_mk'); await run('tag TestRat add bm.hb_gg'); await run('tag TestRat add bm.hb_ht'); await run('tag TestRat add bm.hb_uc');
  await run('tag TestRat add bm.hb_ar'); const keeper0 = await passes('execute if entity @a[name=TestRat,advancements={bm:met/keeper=true}]');
  await run('advancement grant TestRat only bm:met/keeper');
  const metN = fs.readdirSync(`${process.env.HOME}/bm_srv/world/datapacks/BlackMarket_DP/data/bm/advancement/met`).filter(f => f.endsWith('.json')).length;
  await give('bm_handbook', 'hotbar.4'); await sleep(2300); let n0 = A.dialogN.length; await plainUse(4);
  await wait(3000, async () => A.dialogN.length > n0);
  const hb = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]).body || []);
  const fm = hb.match(/Followers met: ","color":"white"[^}]*\},\{"text":"(\d+)"[^}]*\},\{"text":" of (\d+)/);
  ok(`the Handbook: "Followers met: N of ${metN}" - every bm:met/ advancement the pack has`, fm && +fm[2] === metN, fm ? `${fm[1]} of ${fm[2]}` : hb.slice(0, 200));
  const pf = hb.match(/Places found: ","color":"white"[^}]*\},\{"text":"(\d+)"[^}]*\},\{"text":" of (\d+)/);
  ok('...all six places found: "Places found: 6 of 6"', pf && pf[1] === '6' && pf[2] === '6', pf ? `${pf[1]} of ${pf[2]}` : '');
  const pr = await A.press(/Followers ›/);
  const t = pr && pr.next && dd(A.dialogN[A.dialogN.length - 1]).title;
  ok('...its Followers page: the title\'s grey part is not bold (no inherited bold)', Array.isArray(t) && t[0].bold === true && t[1] && t[1].bold === false, JSON.stringify(t).slice(0, 200));
  if (!keeper0) await run('advancement revoke TestRat only bm:met/keeper');
  // the wheel: Cecil on it (staged), opened as a player
  await run(`scoreboard players set TestRat bm.pw${SLOT_CECIL} 1`); await run('item replace entity TestRat weapon.offhand with minecraft:air'); await sleep(2300);
  n0 = A.dialogN.length; await plainUse(2); await wait(3000, async () => A.dialogN.length > n0);
  const labels = A.buttons().map(b => b.label);
  ok('the Partner Wheel: "⌂ Send all home" (it fits its button)', labels.some(l => /Send all home/.test(l)), labels.slice(0, 3).join(' | '));
  const wj = JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]));
  ok('...Cecil\'s "⚙ Menu" tooltip: "the wardrobe, his ways" (not "him ways")', /Cecil's own menu - the wardrobe, his ways/.test(wj) && !/him ways/.test(wj));
  A.close && A.close(0);

  }
  // ---------------------------------------------------------------- put back
  await run(`scoreboard players set TestRat bm.pw${SLOT_CECIL} ${pwc0 || 0}`);
  await run(`scoreboard players set #hard bm.cfg ${hard0 === null ? 0 : hard0}`); await run(`scoreboard players set #dfell bm.cfg ${fell0 === null ? 0 : fell0}`);
  if (dkn0 !== null) await run(`scoreboard players set #dkn bm.cfg ${dkn0}`);
  await run(dfin0 ? 'tag TestRat add bm.dfin' : 'tag TestRat remove bm.dfin');
  await run('kill @e[type=minecraft:wolf,tag=bm.lhpet]'); await clearEnc();
  for (const tg of ['bm.gci', 'bm.gcd', 'bm.gcm', 'bm.dollhit', 'bm.dolld']) await run(`${O}kill @e[tag=${tg},x=${X},y=${Y},z=${Z},distance=..16]`);
  await run('clear TestRat'); await run(`${O}time set noon`);
  console.log(`${res.filter(Boolean).length}/${res.length} passed`);
  A.end && A.end(); R.end(); process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });

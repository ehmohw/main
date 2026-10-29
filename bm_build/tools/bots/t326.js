// 3.0: THE LIGHTBRINGER, SHE OR HE (phase236's FORM, lightbringer_art's '_m' twins) - as a regular (non-op) player; rcon only sets
// the stage (hard mode, noon, the herald placed as the open sky would, scores reset between meetings).
//   THE FIRST MEETING IS A COIN TOSS: up to 12 first meetings (bm.lhform reset, never met): the herald who comes down is she or he
//     at random (the encounter's rig wears the form chosen - every part), the choice kept on the player; both turn up.
//   MET AS HIM: a holy helmet, right-clicked - "He plucks a feather from his wing"; he comes along in his own models (lb_*_m).
//   HIS WORDS: called over ("his halo brightening"); the menu (sneak + use): "Send him home", "Form: Herald (he)", "He loves it..."; his
//     ways ("his wings close round you", "he takes his true form"); sat down ("folds his wings").
//   THE FORM BUTTON: she (every part's model back to lb_*; "Send her home", "Form: Herald (she)") and he again.
//   KEPT: sent home and called again; fainted ("He needs 2 minutes") and called again after; logged out and back in - still him.
//   WHOEVER HAD HER BEFORE: met already (bm.lhmet), no form yet - called, she comes (bm.lhform 0).
const { bot, rcon, sleep } = require('./lib_resp');

(async () => {
  const res = [];
  const R = await rcon(); const run = c => R.run(c);
  const ok = (n, p, d = '') => { res.push(!!p); console.log((p ? 'PASS ' : 'FAIL ') + n + (d ? '  -- ' + d : '')); return !!p; };
  const wait = async (ms, fn, step = 200) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(step); } return false; };
  const O = 'execute in minecraft:overworld run ';
  const cnt = async (sel) => { const m = (await run(`${O}execute if entity ${sel}`)).match(/count: (\d+)/i); return m ? +m[1] : 0; };
  const nbt = async (sel, path) => (await run(`${O}data get entity ${sel} ${path}`)).replace(/^.*?has the following entity data: /, '');
  const num = async (sel, path) => +(((await nbt(sel, path)).match(/(-?[\d.]+)/) || [0, NaN])[1]);
  const score = async (o, who = 'TestRat') => { const m = (await run(`scoreboard players get ${who} ${o}`)).match(/has (-?\d+)/); return m ? +m[1] : null; };
  const has = async (iid) => +(((await run(`clear TestRat *[minecraft:custom_data~{bm:"${iid}"}] 0`)).match(/Found (\d+)/) || [0, 0])[1]);
  const uuidOf = async (sel) => { const m = (await run(`${O}data get entity ${sel} UUID`)).match(/\[I; (-?\d+), (-?\d+), (-?\d+), (-?\d+)\]/); if (!m) return null;
    const h = m.slice(1).map(v => (Number(v) >>> 0).toString(16).padStart(8, '0')).join(''); return `${h.slice(0, 8)}-${h.slice(8, 12)}-${h.slice(12, 16)}-${h.slice(16, 20)}-${h.slice(20)}`; };
  let A;
  const entOf = async (sel) => { const u = await uuidOf(sel); return Object.values(A.ents).find(e => e.objectUUID === u); };
  const use = async (slot, sneak = false) => { A.slot(slot); await sleep(250); if (sneak) { A.input({ shift: true }); await sleep(200); } A.use(); await sleep(400); A.release(); if (sneak) { A.input({}); await sleep(150); } };
  const sneakMenu = async (slot) => { const n0 = A.dialogN.length; await use(slot, true); await wait(3000, async () => A.dialogN.length > n0); return A.dialogN.length > n0; };
  const dd = (d) => d && (d.data || d);
  const body = () => JSON.stringify(dd(A.dialogN[A.dialogN.length - 1]).body || []);
  const at = async (x, y, z, yaw, pitch) => { await run(`${O}tp TestRat ${x} ${y} ${z} ${yaw} ${pitch}`); await wait(2000, async () => A.pos && Math.abs(A.pos.x - x) < 0.05 && Math.abs(A.pos.z - z) < 0.05, 100); await sleep(300); };
  const X = 17860, Y = 100, Z = 16040;
  const HOLY = 'minecraft:golden_helmet[custom_data={bm_angel:1b}]';
  const PARTS = ['body', 'skirt', 'head', 'halo', 'hair', 'hairlo', 'armr', 'forer', 'arml', 'forel', 'staff', 'wingr', 'wingl', 'legr', 'legl', 'pool'];
  const PET = '@e[type=minecraft:wolf,tag=bm.lhpet,tag=!bm.ffpet,limit=1]';
  const ENC = '@e[type=minecraft:interaction,tag=bm.lhenc,limit=1]';
  const part = (p, enc = false) => `@e[type=minecraft:item_display,tag=bm.lhp_${p},${enc ? 'tag=bm.lhencp' : 'tag=bm.lhp_pet,tag=!bm.lhfade'},limit=1]`;
  const model = async (sel) => (await nbt(sel, 'item.components."minecraft:item_model"')).replace(/"/g, '');
  // every part's model, as one form: 'm' (all lb_<part>_m), 'f' (all lb_<part>), or 'mixed'
  const formOf = async (enc = false) => {
    const ms = []; for (const p of PARTS) ms.push(await model(part(p, enc)));
    if (ms.every((m, i) => m === `bm:lb_${PARTS[i]}_m`)) return 'm';
    if (ms.every((m, i) => m === `bm:lb_${PARTS[i]}`)) return 'f';
    return 'mixed: ' + ms.join(',');
  };
  const clearEnc = async () => { await run('kill @e[type=minecraft:interaction,tag=bm.lhenc]'); await run('kill @e[type=minecraft:item_display,tag=bm.lhencp]'); await sleep(300); };

  A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  A.chats.length = 0; A.cmd('gamemode creative'); await sleep(500);
  ok('TestRat is a regular player', /unknown|incomplete/i.test(A.chats.join(' ')));
  await run('gamemode survival TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await run('clear TestRat');
  await run(`${O}forceload add ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`); await run('weather clear'); await sleep(2500);
  await run(`${O}fill ${X - 10} ${Y} ${Z - 10} ${X + 10} ${Y} ${Z + 10} minecraft:sandstone`); await run(`${O}fill ${X - 10} ${Y + 1} ${Z - 10} ${X + 10} ${Y + 8} ${Z + 10} minecraft:air`);
  await run(`${O}kill @e[type=!minecraft:player,x=${X},y=${Y},z=${Z},distance=..24]`);
  await run('kill @e[type=minecraft:wolf,tag=bm.lhpet]'); await clearEnc();
  await run('kill @e[type=minecraft:wolf,tag=bm.seen]'); await run('kill @e[type=minecraft:cat,tag=bm.seen]');        // (a full party: nobody comes)
  const hard0 = await score('bm.cfg', '#hard');                                                    // (put back as it was, at the end)
  await run('scoreboard players set TestRat bm.lhcd 0'); await run('scoreboard players set TestRat bm.coslh 0');
  for (const k of ['snow', 'witch', 'shark']) await run(`scoreboard players reset TestRat bm.dbwin_${k}`);      // (the three Dread bosses not beaten: else hard mode hands the Summons back - p237/summons)
  for (const t of ['bm.lhmet', 'bm.dfin', 'bm.usum', 'bm.lhseen']) await run(`tag TestRat remove ${t}`);
  await run(`${O}time set noon`); await run('scoreboard players set #hard bm.cfg 1');
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 10);

  // ---------------------------------------------------------------- the first meeting: a coin toss, kept
  const seen = { f: 0, m: 0 }; let last = null, tries = 0, both = 0, mixed = '', kept = true;
  for (tries = 1; tries <= 24; tries++) {             // (both should turn up within 12; then on, if need be, until the one met is him)
    await clearEnc(); await run('scoreboard players reset TestRat bm.lhform'); await run('tag TestRat remove bm.lhmet');
    await run(`clear TestRat *[minecraft:custom_data~{bm:"herald_feather"}]`);
    await run(`${O}execute as TestRat at @s rotated 0 0 positioned ^ ^ ^5 run function bm:p236l/enc/place`);
    if (!(await wait(4000, async () => (await cnt(ENC)) === 1 && (await cnt('@e[type=minecraft:item_display,tag=bm.lhencp]')) === PARTS.length))) { mixed = 'no herald came'; break; }
    await sleep(300);
    const f = await formOf(true), sc = await score('bm.lhform');
    if (f !== 'f' && f !== 'm') { mixed = f; break; }
    if ((f === 'm') !== (sc === 1) || sc === null) kept = false;
    seen[f]++; last = f;
    if (!both && seen.f && seen.m) both = tries;
    if (both && last === 'm') break;
  }
  ok('a first meeting: the herald comes down whole in one form or the other (every part)', !mixed, mixed.slice(0, 200));
  ok('...the form met kept on the player (bm.lhform 0 she, 1 he)', kept);
  ok(`...a coin toss: she and he both turn up within 12 first meetings (both by meeting ${both}; she ${seen.f}, he ${seen.m})`, both > 0 && both <= 12);
  ok('...and the last one met is him', last === 'm');

  // ---------------------------------------------------------------- met as him: right-clicked, wearing something holy
  await run(`item replace entity TestRat armor.head with ${HOLY}`);
  const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
  await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
  A.slot(8); await sleep(300); A.chats.length = 0;
  { const eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500); }
  ok('right-clicked: his feather - "He plucks a feather from his wing"', (await has('herald_feather')) === 1 && A.chats.some(c => /He plucks a feather from his wing/.test(c)), A.chats.slice(-2).join(' ').slice(0, 200));
  ok('..."call him; sneak + use for his menu"', A.chats.some(c => /to call him; sneak \+ use for his menu/.test(c)), A.chats.slice(-1).join('').slice(0, 200));
  ok('...he comes along in his own models (every part lb_*_m)', await wait(4000, async () => (await cnt(PET)) === 1) && await wait(3000, async () => (await formOf()) === 'm'), await formOf());
  await run('item replace entity TestRat armor.head with minecraft:air');
  await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/herald_feather');
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);

  // ---------------------------------------------------------------- his words
  A.bars.length = 0; await use(0); await sleep(1500);
  ok('the feather used while he\'s out: called over - "his halo brightening"', A.bars.some(b => /glides back to your side, his halo brightening/.test(b)), A.bars.slice(-1).join(''));
  ok('sneak + use: the menu', await sneakMenu(0));
  let labels = A.buttons().map(b => b.label);
  ok('...his menu: "Send him home", "Form: Herald (he)"', labels.includes('Send him home') && labels.includes('Form: Herald (he)'), labels.join(' | '));
  ok('..."He loves it when you wear holy things."', /He loves it when you wear holy things/.test(body()), body().slice(0, 200));
  let pr = await A.press(/The Lightbringer's ways/);
  ok('...his ways: "his wings close round you", "he takes his true form", "beside him, you heal"', pr && pr.next && /his wings close round you/.test(body()) && /he takes his true form/.test(body()) && /beside him, you heal/.test(body()), body().slice(0, 240));
  await A.press(/« Back/); await sleep(600);
  A.bars.length = 0; await A.press(/Sit \/ follow/); await sleep(1500);
  ok('Sit / follow: "he kneels and folds his wings"', A.bars.some(b => /he kneels and folds his wings, the staff across his lap/.test(b)), A.bars.slice(-1).join(''));
  await sneakMenu(0); await A.press(/Sit \/ follow/); await sleep(1200);

  // ---------------------------------------------------------------- the Form button: she, then he again
  await sneakMenu(0); A.bars.length = 0; pr = await A.press(/Form: Herald/); await sleep(1200);
  ok('Form pressed: she - every part back to her own model', await wait(3000, async () => (await formOf()) === 'f') && (await score('bm.lhform')) === 0, await formOf());
  ok('...her word on it, and the menu back in her words ("Send her home", "Form: Herald (she)")', A.bars.some(b => /As I was, then/.test(b)) && pr && pr.next &&
     A.buttons().some(b => b.label === 'Send her home') && A.buttons().some(b => b.label === 'Form: Herald (she)'), A.buttons().map(b => b.label).join(' | '));
  A.bars.length = 0; pr = await A.press(/Form: Herald/); await sleep(1200);
  ok('Form pressed again: he - every part lb_*_m', await wait(3000, async () => (await formOf()) === 'm') && (await score('bm.lhform')) === 1 && A.bars.some(b => /The light wears many faces/.test(b)), await formOf());
  ok('...the head wears his face (lb_head_m) and its moods are his (the item definition picks lb_head_x<face>_m)', (await model(part('head'))) === 'bm:lb_head_m');

  // ---------------------------------------------------------------- kept: sent home and called; fainted and called; logged out and in
  await sneakMenu(0); A.bars.length = 0; await A.click(/Send him home/); await sleep(1500);
  ok('Send him home: he goes ("he bows, and rises into the light")', (await cnt(PET)) === 0 && A.bars.some(b => /he bows, and rises into the light/.test(b)), A.bars.slice(-1).join(''));
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('...called again: still him', (await formOf()) === 'm', await formOf());
  A.chats.length = 0; await run(`${O}effect clear ${PET}`); await run(`${O}damage ${PET} 400 minecraft:out_of_world`);
  ok('struck down: he faints - "He needs 2 minutes before he can come back."', await wait(5000, async () => A.chats.some(c => /He needs 2 minutes before he can come back/.test(c))), A.chats.slice(-1).join('').slice(0, 200));
  await run('scoreboard players set TestRat bm.lhcd 0'); await sleep(1200);
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('...called again after: still him', (await formOf()) === 'm', await formOf());
  await sneakMenu(0); await A.click(/Send him home/); await sleep(1200);
  A.end(); await sleep(3000);
  A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('logged out and back in, called: still him', (await formOf()) === 'm', await formOf());
  await sneakMenu(0); await A.click(/Send him home/); await sleep(1200);

  // ---------------------------------------------------------------- whoever had her before keeps her
  await run('scoreboard players reset TestRat bm.lhform'); await run('tag TestRat add bm.lhmet'); await sleep(300);
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('met her before the male form existed (bm.lhmet, no form yet): called, she comes - and stays she (bm.lhform 0)', (await formOf()) === 'f' && (await score('bm.lhform')) === 0, await formOf());
  await sneakMenu(0); await A.click(/Send her home/); await sleep(1200);

  // ---------------------------------------------------------------- clean up
  await clearEnc(); await run('kill @e[type=minecraft:wolf,tag=bm.lhpet]'); await run('clear TestRat'); await run('effect clear TestRat');      // (its Resistance off again)
  await run('scoreboard players reset TestRat bm.lhform'); await run('scoreboard players set TestRat bm.lhcd 0'); await run(hard0 === null ? 'scoreboard players reset #hard bm.cfg' : `scoreboard players set #hard bm.cfg ${hard0}`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})();

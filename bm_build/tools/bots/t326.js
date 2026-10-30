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
//   (3.0a) THE ELEMENTAL FORMS (phase236.elements): his menu's Element / Give back; Element with nothing given - "Bring me..."; right-
//     clicked holding an Ethereal Gem - he keeps it (one from the hand), every part lb_<part>_m_e; the gem again - nothing taken; the
//     Wraithfire Heart - lb_<part>_m_w; Element steps his own light -> Ethereal -> Wraithfire; Form under it: she in Wraithfire (lb_<part>_w)
//     and he again; his ways tell of it; THE OPHANIM in Wraithfire (three still monsters staged): his parts shrink away in their _m_w
//     models and come back in them, what it struck burns; kept across send home / call and a log-out; Give back - both in your pack.
//   (3.0d) THE OPHANIM, FOR GOOD: the menu's Ophanim form locked below Queen Ava's rank III; at III (staged) pressed - the wheel's four
//     parts at full size where she stands (centred ~3.35 up), her rig unseen, its rings turning, a gentle bob, following her; her
//     charged Ophanim flares it (no second wheel); Companion size: small, hovering (and back); sent home - gone, called - back; off.
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
  await run('scoreboard players set TestRat bm.wulightbringer 128');   // (his shiny look already found: no 1-in-100 shiny roll on the many calls below - it would put every part in its _c7 twin)
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

  // ---------------------------------------------------------------- (3.0a) THE ELEMENTAL FORMS: the gem and the heart handed to him, kept, switched,
  //      layered on the male form (both suffixes), the Ophanim in an element form, kept across recall and log-out, given back
  const formIs = async (sfx) => { const ms = []; for (const p of PARTS) ms.push(await model(part(p))); return ms.every((m, i) => m === `bm:lb_${PARTS[i]}${sfx}`) ? true : ms.join(','); };
  const HIT = '@e[type=minecraft:interaction,tag=bm.lhhit,limit=1]';
  const clickHer = async (slot) => { A.slot(slot); await sleep(300); await run(`${O}tp ${PET} TestRat`); await sleep(400);
    const eb = await entOf(HIT); A.bars.length = 0; A.chats.length = 0; if (eb) A.interact(eb.entityId); await sleep(1500); return !!eb; };
  for (const o of ['bm.lhel', 'bm.lheg', 'bm.lhwh']) await run(`scoreboard players reset TestRat ${o}`);
  await run('loot replace entity TestRat hotbar.1 loot bm:items/ethereal_gem'); await run('loot replace entity TestRat hotbar.2 loot bm:items/wraithfire_heart');
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  await sneakMenu(0); labels = A.buttons().map(b => b.label);
  ok('his menu: "Element: Ethereal / Wraithfire", "Give back the gem & heart"', labels.includes('Element: Ethereal / Wraithfire') && labels.includes('Give back the gem & heart'), labels.join(' | '));
  A.bars.length = 0; pr = await A.press(/^Element/); await sleep(800);
  ok('Element with nothing given him: "Bring me an Ethereal Gem, or a Wraithfire Heart" - and his menu again, his form unchanged', A.bars.some(b => /Bring me an Ethereal Gem/.test(b)) && pr && pr.next && (await formIs('_m')) === true, A.bars.slice(-1).join(''));
  await A.press(/Sit \/ follow/); await sleep(1000);                                                     // (sat: he stays where he's clicked)
  ok('right-clicked holding the Ethereal Gem: a click box to click', await clickHer(1));
  ok('...he keeps it - one gone from your hand (bm.lheg 1)', (await has('ethereal_gem')) === 0 && (await score('bm.lheg')) === 1, `${await has('ethereal_gem')} / ${await score('bm.lheg')}`);
  ok('...and takes its form: every part lb_<part>_m_e (his and the element\'s suffix)', await wait(3000, async () => (await formIs('_m_e')) === true) && (await score('bm.lhel')) === 1, String(await formIs('_m_e')).slice(0, 200));
  ok('..."Starlight, all the way through"; "he can take it whenever you like ... in his menu"', A.bars.some(b => /Starlight, all the way through/.test(b)) &&
     A.chats.some(c => /keeps the Ethereal Gem/.test(c) && /he can take it whenever you like/.test(c) && /in his menu/.test(c)), (A.bars.slice(-1).join('') + ' / ' + A.chats.slice(-1).join('')).slice(0, 240));
  ok('...still sitting (the click gave - it didn\'t stand him up)', /1b/.test(await nbt(PET, 'Sitting')));
  await clickHer(1);
  ok('the Ethereal Gem again (none left in hand - the slot empty): nothing taken, his form kept', (await score('bm.lheg')) === 1 && (await formIs('_m_e')) === true);
  ok('right-clicked holding the Wraithfire Heart: he keeps it too, and burns with it - every part lb_<part>_m_w', await clickHer(2) && (await has('wraithfire_heart')) === 0 &&
     (await score('bm.lhwh')) === 1 && await wait(3000, async () => (await formIs('_m_w')) === true) && A.bars.some(b => /Cold fire, gentle as a candle/.test(b)), String(await formIs('_m_w')).slice(0, 200));
  // Element steps: Wraithfire -> his own light -> Ethereal -> Wraithfire
  await sneakMenu(0);
  for (const [sfx, re, nm] of [['_m', /plain light of dawn/, 'his own light'], ['_m_e', /Starlight/, 'Ethereal'], ['_m_w', /Cold fire/, 'Wraithfire']]) {
    A.bars.length = 0; pr = await A.press(/^Element/); await sleep(1000);
    ok(`Element pressed: ${nm} (every part lb_<part>${sfx}), his word, the menu back`, await wait(3000, async () => (await formIs(sfx)) === true) && A.bars.some(b => re.test(b)) && pr && pr.next &&
       A.buttons().some(b => b.label === 'Send him home'), String(await formIs(sfx)).slice(0, 160));
  }
  // the gender form under the element: she in Wraithfire, then he again
  pr = await A.press(/Form: Herald/); await sleep(1200);
  ok('Form pressed in Wraithfire: she - every part lb_<part>_w (her models, still the element\'s)', await wait(3000, async () => (await formIs('_w')) === true) && (await score('bm.lhel')) === 2, String(await formIs('_w')).slice(0, 160));
  ok('...her menu now: "Send her home", "Form: Herald (she)"', pr && pr.next && A.buttons().some(b => b.label === 'Send her home') && A.buttons().some(b => b.label === 'Form: Herald (she)'));
  pr = await A.press(/Form: Herald/); await sleep(1200);
  ok('Form again: he - lb_<part>_m_w; the head wears his Wraithfire face (lb_head_m_w: its moods pick lb_head_x<face>_m_w)', await wait(3000, async () => (await formIs('_m_w')) === true) && (await model(part('head'))) === 'bm:lb_head_m_w');
  if (/1b/.test(await nbt(PET, 'Sitting'))) { pr = await A.press(/Sit \/ follow/); await sleep(1000); }   // (up: the Ophanim needs him free - the empty-handed click above already stood him up)
  ok('...and his ways tell of it ("Ethereal and Wraithfire": "right-click him with an Ethereal Gem")', await sneakMenu(0) && (await A.press(/The Lightbringer's ways/)) && /right-click him with an Ethereal Gem/.test(body()), body().slice(0, 200));
  await A.press(/« Back/); await sleep(500);
  // THE OPHANIM in Wraithfire: three monsters 8-10 off (still, unharmable - only staged); the wheel opens, his parts shrink away, then come back in the same models
  await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await at(X + 0.5, Y + 1, Z - 1.5, 0, 0);
  for (const pe of ['bm.lzk2', 'bm.lzgc', 'bm.lzrc', 'bm.lzsc', 'bm.lzmc', 'bm.lzk', 'bm.lzx']) await run(`${O}scoreboard players set ${PET} ${pe} 0`);
  await run(`${O}scoreboard players set ${PET} bm.lzrc 400`);                                            // (no smite first: the wheel's turn)
  for (const [dx, dz] of [[8, 3], [-8, 3], [0, 9]]) await run(`${O}summon minecraft:husk ${X + 0.5 + dx} ${Y + 1} ${Z + 0.5 + dz} {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,Tags:["lhtest"]}`);
  const hid = await wait(9000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.oph]')) > 0 && /^\[0\.0f?,/.test((await nbt(part('body'), 'transformation.scale')).replace(/\s/g, '')), 250);
  ok('three monsters near, he in Wraithfire: the Ophanim - the wheel above, his parts shrunk away', hid, `${await nbt(part('body'), 'transformation.scale')} sitting ${await nbt(PET, 'Sitting')} lzx ${await score('bm.lzx', PET)} lzk2 ${await score('bm.lzk2', PET)} husks ${await cnt('@e[type=minecraft:husk,tag=lhtest]')} tags ${await nbt(PET, 'Tags')}`);
  ok('...his parts keep their Wraithfire models while hidden', (await formIs('_m_w')) === true);
  const back = await wait(12000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.oph]')) === 0 && !/^\[0\.0f?,/.test((await nbt(part('body'), 'transformation.scale')).replace(/\s/g, '')), 300);
  ok('...the wheel gone, he is himself again - every part restored, still lb_<part>_m_w', back && (await formIs('_m_w')) === true, `${await nbt(part('body'), 'transformation.scale')} ${String(await formIs('_m_w')).slice(0, 120)}`);
  ok('...and what his light struck burns (Wraithfire: soul fire on the monsters)', +(((await nbt('@e[type=minecraft:husk,tag=lhtest,limit=1]', 'Fire')).match(/(-?\d+)/) || [0, 0])[1]) > 0);
  await run(`${O}kill @e[type=minecraft:husk,tag=lhtest]`);
  // kept: sent home and called; logged out and in - still his Wraithfire
  await sneakMenu(0); await A.click(/Send him home/); await sleep(1200);
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('sent home and called again: still his Wraithfire form (lb_<part>_m_w)', (await formIs('_m_w')) === true, String(await formIs('_m_w')).slice(0, 160));
  await sneakMenu(0); await A.click(/Send him home/); await sleep(1200);
  A.end(); await sleep(3000);
  A = await bot('TestRat'); await sleep(2500); A.stand(); await sleep(300);
  await at(X + 0.5, Y + 1, Z + 0.5, 0, 0);
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('logged out and back in, called: still his Wraithfire form', (await formIs('_m_w')) === true, String(await formIs('_m_w')).slice(0, 160));
  // given back: both in your hands, his own light again
  await sneakMenu(0); A.bars.length = 0; pr = await A.press(/Give back the gem & heart/); await sleep(1200);
  ok('Give back the gem & heart: both back in your pack, his own light again (lb_<part>_m)', (await has('ethereal_gem')) === 1 && (await has('wraithfire_heart')) === 1 &&
     (await score('bm.lheg')) === 0 && (await score('bm.lhwh')) === 0 && await wait(3000, async () => (await formIs('_m')) === true) && A.bars.some(b => /only lent to me/.test(b)), `${await has('ethereal_gem')} ${await has('wraithfire_heart')} ${String(await formIs('_m')).slice(0, 100)}`);
  A.bars.length = 0; await A.press(/^Element/); await sleep(800);
  ok('...and Element has nothing to wear now ("Bring me an Ethereal Gem")', A.bars.some(b => /Bring me an Ethereal Gem/.test(b)) && (await formIs('_m')) === true);
  await A.click(/Send him home/); await sleep(1200);
  await run('clear TestRat *[minecraft:custom_data~{bm:"ethereal_gem"}]'); await run('clear TestRat *[minecraft:custom_data~{bm:"wraithfire_heart"}]');

  // ---------------------------------------------------------------- whoever had her before keeps her
  await run('scoreboard players reset TestRat bm.lhform'); await run('tag TestRat add bm.lhmet'); await sleep(300);
  await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
  ok('met her before the male form existed (bm.lhmet, no form yet): called, she comes - and stays she (bm.lhform 0)', (await formOf()) === 'f' && (await score('bm.lhform')) === 0, await formOf());
  await sneakMenu(0); await A.click(/Send her home/); await sleep(1200);

  // ---------------------------------------------------------------- (3.0d) THE OPHANIM, FOR GOOD - and its companion size
  {
    const hn0 = await score('bm.hn_lightbringer');
    const W = (p) => `@e[type=minecraft:item_display,tag=bm.ophf_${p},limit=1]`;
    const vec = (t) => (t.match(/-?[\d.]+(?:E-?\d+)?/g) || []).map(Number);
    const pos = async (sel) => vec(await nbt(sel, 'Pos'));
    await run('scoreboard players set TestRat bm.lhoph 0'); await run('scoreboard players set TestRat bm.lhcs 0'); await run('scoreboard players set TestRat bm.hn_lightbringer 1444');
    await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
    ok('(3.0d) her menu: an "Ophanim form" row and a "Companion size" row', await sneakMenu(0) && A.buttons().some(b => /Ophanim form/.test(b.label)) && A.buttons().some(b => /Companion size/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
    A.bars.length = 0; await A.press(/Ophanim form/); await sleep(1200);
    ok('...below Queen Ava\'s rank III: locked - "Honoured by Queen Ava to rank III" (no wheel)', A.bars.some(b => /rank III/.test(b)) && (await cnt('@e[type=minecraft:item_display,tag=bm.ophf]')) === 0 && (await score('bm.lhoph')) === 0, A.bars.slice(-1).join(''));
    await run('scoreboard players set TestRat bm.hn_lightbringer 1555');                 // (rank III: Vitality, Bulwark and Might at V - staged)
    await sneakMenu(0); A.bars.length = 0; await A.press(/Ophanim form/); await sleep(1500);
    ok('rank III, pressed: she IS the Ophanim - its four parts out (bm.ophf), kept on you (bm.lhoph 1)', await wait(3000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.ophf]')) === 4) && (await score('bm.lhoph')) === 1);
    ok('...her own rig unseen (view_range 0)', /^0\.0f?$/.test((await nbt(part('body'), 'view_range')).trim()), await nbt(part('body'), 'view_range'));
    const sc0 = vec(await nbt(W('ring_a'), 'transformation.scale'));
    ok('...at its full size (2.2), not a companion\'s', Math.abs(sc0[0] - 2.2) < 0.01, JSON.stringify(sc0));
    const pp = await pos(PET), wp = await pos(W('ring_a'));
    ok('...standing where she is: centred on her, its centre ~3.35 up (its lowest flames just clear of the ground)', Math.hypot(wp[0] - pp[0], wp[2] - pp[2]) < 0.7 && wp[1] - pp[1] > 3.0 && wp[1] - pp[1] < 3.7, `${wp.map(v => v.toFixed(2))} vs ${pp.map(v => v.toFixed(2))}`);
    const r1 = await nbt(W('ring_a'), 'transformation.left_rotation'); const c1 = await nbt(W('ring_c'), 'transformation.left_rotation'); await sleep(1300);
    const r2 = await nbt(W('ring_a'), 'transformation.left_rotation'); const c2 = await nbt(W('ring_c'), 'transformation.left_rotation');
    ok('...its rings turning, each on its own (left_rotation changing)', r1 !== r2 && c1 !== c2, `${r1} -> ${r2}`);
    const y1 = (await pos(W('core')))[1]; await sleep(2500); const y2 = (await pos(W('core')))[1];
    ok('...bobbing gently (its height moves, within a few tenths)', Math.abs(y2 - y1) > 0.005 && Math.abs(y2 - y1) < 0.3, `${y1} -> ${y2}`);
    await run(`${O}tp ${PET} ${X + 4.5} ${Y + 1} ${Z + 3.5}`); await sleep(1200);
    const pp2 = await pos(PET), wp2 = await pos(W('ring_a'));
    ok('...and it follows her (moved with her host)', Math.hypot(wp2[0] - pp2[0], wp2[2] - pp2[2]) < 0.7, `${wp2.map(v => v.toFixed(2))} vs ${pp2.map(v => v.toFixed(2))}`);
    // its charged move, in this form: no second wheel - it flares, at its own size
    for (const pe of ['bm.lzk2', 'bm.lzgc', 'bm.lzrc', 'bm.lzsc', 'bm.lzmc', 'bm.lzk', 'bm.lzx']) await run(`${O}scoreboard players set ${PET} ${pe} 0`);
    await run(`${O}scoreboard players set ${PET} bm.lzrc 400`);
    const px = pp2[0], pz = pp2[2];
    for (const [dx, dz] of [[8, 3], [-8, 3], [0, 9]]) await run(`${O}summon minecraft:husk ${px + dx} ${Y + 1} ${pz + dz} {NoAI:1b,Invulnerable:1b,PersistenceRequired:1b,Silent:1b,Tags:["lhtest"]}`);
    const fl = await wait(9000, async () => (await score('bm.lza', PET)) === 15 && (await score('bm.lzx', PET)) > 0, 200);
    ok('...her Ophanim (three monsters near) in this form: it flares - no second wheel, its size unchanged',
       fl && (await cnt('@e[type=minecraft:item_display,tag=bm.oph]')) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.ophf]')) === 4 && Math.abs(vec(await nbt(W('ring_a'), 'transformation.scale'))[0] - 2.2) < 0.01,
       `fl ${fl} oph ${await cnt('@e[type=minecraft:item_display,tag=bm.oph]')}`);
    await wait(9000, async () => (await score('bm.lzx', PET)) === 0, 300);
    await run(`${O}kill @e[type=minecraft:husk,tag=lhtest]`);
    // companion size
    await sneakMenu(0); await A.press(/Companion size/); await sleep(1500);
    const sc1 = vec(await nbt(W('ring_a'), 'transformation.scale')); const pp3 = await pos(PET), wp3 = await pos(W('ring_a'));
    ok('Companion size pressed: the wheel small (scale ~0.70), hovering just above her place (~1.9)', (await score('bm.lhcs')) === 1 && Math.abs(sc1[0] - 0.704) < 0.01 && wp3[1] - pp3[1] > 1.5 && wp3[1] - pp3[1] < 2.2,
       `${JSON.stringify(sc1)} dy ${(wp3[1] - pp3[1]).toFixed(2)}`);
    await sneakMenu(0); await A.press(/Companion size/); await sleep(1500);
    ok('...pressed again: full size', (await score('bm.lhcs')) === 0 && Math.abs(vec(await nbt(W('ring_a'), 'transformation.scale'))[0] - 2.2) < 0.01);
    // kept: sent home - the wheel goes with her; called - it's back
    await sneakMenu(0); await A.click(/Send (him|her) home/); await sleep(1600);
    ok('sent home: the wheel goes with her (no stray part)', (await cnt('@e[type=minecraft:item_display,tag=bm.ophf]')) === 0);
    await use(0); await wait(4000, async () => (await cnt(PET)) === 1);
    ok('...called again: the Ophanim again (kept)', await wait(4000, async () => (await cnt('@e[type=minecraft:item_display,tag=bm.ophf]')) === 4, 200) && /^0\.0f?$/.test((await nbt(part('body'), 'view_range')).trim()));
    await sneakMenu(0); A.bars.length = 0; await A.press(/Ophanim form/); await sleep(1500);
    ok('Ophanim form pressed again: off - the wheel gone, the herald seen again (view_range 1.6)', (await score('bm.lhoph')) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.ophf]')) === 0 &&
       /^1\.6f?$/.test((await nbt(part('body'), 'view_range')).trim()), await nbt(part('body'), 'view_range'));
    await sneakMenu(0); await A.click(/Send (him|her) home/); await sleep(1200);
    await run(hn0 === null ? 'scoreboard players reset TestRat bm.hn_lightbringer' : `scoreboard players set TestRat bm.hn_lightbringer ${hn0}`);
    await run('scoreboard players reset TestRat bm.lhoph'); await run('scoreboard players reset TestRat bm.lhcs');
  }

  // ---------------------------------------------------------------- clean up
  await clearEnc(); await run('kill @e[type=minecraft:wolf,tag=bm.lhpet]'); await run('clear TestRat'); await run('effect clear TestRat');      // (its Resistance off again)
  for (const o of ['bm.lhform', 'bm.lhel', 'bm.lheg', 'bm.lhwh']) await run(`scoreboard players reset TestRat ${o}`);
  await run('scoreboard players set TestRat bm.lhcd 0'); await run(hard0 === null ? 'scoreboard players reset #hard bm.cfg' : `scoreboard players set #hard bm.cfg ${hard0}`);
  await run(`${O}forceload remove ${X - 16} ${Z - 16} ${X + 16} ${Z + 16}`);
  const n = res.filter(x => x).length; console.log(`${n}/${res.length} passed`);
  A.end(); R.end(); process.exit(n === res.length ? 0 : 1);
})();

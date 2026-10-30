// 2.98: THE GEM OF CREATIVITY, as a regular (non-op) player - the owner's checklist (rigpet_t). It comes to you when the Creative
// Spark forms: Mr. Capshun, Kettle and Emma called with their own items (real uses) - and down out of the sky, once, comes the Gem
// (3.0a: a scene - high above, a slow spiral down, twice round you, up over your head, and it DROPS into your hands; its halo always circling).
// Its ways: CONJURE (a foe within 14: one of its 3D Buddies pops out of a sparkle at it, its own attack), PRISM (a foe close: a flash
// off its facets), INSPIRATION (out of a fight: Haste and Luck for you), MASTERPIECE (three foes: three Buddies at once). It feels in
// text - an emoticon on its face (2.96a: lit on its table facet - :) c: :o :3 o3o ^-^ ;( o.O ...): >:( in a fight. Then the shared list.
// (3.0a) ITS FORMS: right-clicked holding the Ethereal Gem - it keeps it (the item gone from you), the resonance, its parts to their '_e' twins
// (wings shown), every face on the new table, its Prism at 7; the menu's Ethereal Form: on / off both ways; sent home and called - still
// Ethereal; handed a Wraithfire Heart - the Ethereal Gem comes back, '_w'; sneak + right-click empty-handed - the heart back, its own self.
// (Its rig: five parts now - the gem, its face, its halo and two wings, a speck in its own form; the figurine stays three.)
const runT = require('./rigpet_t');
runT({ W: 'gem', NAME: 'The Gem of Creativity', ab: 'cg', q: 'cq', pfx: 'p231', prefix: 'cg_', item: 'creativity_gem', parts: 5, figParts: 3, hp: 40, X: 17400, Z: 17600, pron: 'it',
  called: /floats down to you/, home: /twinkles goodbye/, sit: /settles low and dims/, stand: /lifts and brightens/,
  ways: ['Conjure', 'Prism', 'Inspiration', 'Masterpiece', 'Creative Forms'],
  plain: 'Its own colours', looks: ['Ruby Facets', 'Sapphire Facets', 'Amethyst Facets'], lookPart: 'body',
  encounter: async ({ A, run, ok, wait, O, cnt, has, nbt, X, Y, Z, sleep, use }) => {
    await run('scoreboard players set TestRat bm.cgel 0'); await run('scoreboard players set TestRat bm.cgfo 0');   // (whatever an earlier run left it holding)
    for (const t of ['bm.mzmet', 'bm.ktmet', 'bm.emmet']) await run(`tag TestRat add ${t}`);
    for (const o of ['bm.mzcd', 'bm.ktcd', 'bm.emcd']) await run(`scoreboard players set TestRat ${o} 0`);
    await run('advancement revoke TestRat only bm:story/trio_creative_spark');
    const items = ['capshun_pencil', 'kettle_plane', 'emma_ribbon'];
    for (const [i, iid] of items.entries()) await run(`loot replace entity TestRat hotbar.${i + 5} loot bm:items/${iid}`);
    A.chats.length = 0;
    // (3.0a) THE SCENE: high in the sky, a slow spiral down, twice round you at shoulder height, up over your head - and the Gem DROPS
    const pos = async (sel) => { const m = (await nbt(sel, 'Pos')).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
    const GEM = '@e[type=minecraft:item_display,tag=bm.cgcz_body,limit=1]', DROP = '@e[type=minecraft:item,tag=bm.cgdrop,limit=1]', ME = '@a[name=TestRat,limit=1]', WAITING = '@a[name=TestRat,tag=bm.cgwait]';
    const track = [];                                   // (dy above the player, out from them, angle round them)
    const sample = async () => { const g = await pos(GEM), p = await pos(ME); if (!g || !p) return false;
      track.push({ dy: g[1] - p[1], out: Math.hypot(g[0] - p[0], g[2] - p[2]), ang: Math.atan2(g[2] - p[2], g[0] - p[0]) * 180 / Math.PI }); return true; };
    for (let i = 0; i < 3; i++) { await use(i + 5); if (i < 2) await sleep(2200); }
    const begun = await wait(6000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.cgcin]')) === 1, 50); await sample();   // (its first spot, at once: it is coming down already)
    const here = [await cnt('@e[type=minecraft:wolf,tag=bm.mzpet]'), await cnt('@e[type=minecraft:wolf,tag=bm.ktpet]'), await cnt('@e[type=minecraft:cat,tag=bm.emmapet]')];
    ok('Mr. Capshun, Kettle and Emma called with their own items', here.every(n => n >= 1), here.join(','));
    ok('...together, the Creative Spark: the Gem shines high in the sky, its scene begins', begun &&
       A.chats.some(c => /a swirl of every colour comes down out of the sky/i.test(c)), A.chats.slice(-3).join(' | ').slice(0, 200));
    ok('...nothing given yet - the drop is the reward', (await has('creativity_gem')) === 0 && (await cnt(WAITING)) === 1, `gems ${await has('creativity_gem')} waiting ${await cnt(WAITING)}`);
    for (let i = 0; i < 60 && (await cnt(GEM)) === 1; i++) { if (!(await sample())) break; await sleep(180); }
    const sky = track.slice(0, 3).map(t => t.dy), low = track.filter(t => t.dy < 2.0 && t.dy > 1.2 && Math.abs(t.out - 2) < 0.35);
    ok('...it starts high above (15+ up) and comes slowly down', track.length >= 20 && Math.max(...sky) > 15 && track.findIndex(t => t.dy < 2.0) > 8 &&
       track.slice(0, track.findIndex(t => t.dy < 2.0)).every((t, i, a) => i === 0 || t.dy <= a[i - 1].dy + 0.05),
       track.filter((_t, i) => i % 6 === 0).map(t => t.dy.toFixed(1)).join(' '));
    let turned = 0; for (let i = 1; i < low.length; i++) { let d = low[i].ang - low[i - 1].ang; while (d > 180) d -= 360; while (d < -180) d += 360; turned += d; }
    ok('...then swirls round you at shoulder height, 2 out (positions around a circle over time)', low.length >= 8 && Math.abs(turned) > 300,
       `${low.length} samples, ${Math.round(turned)} deg round`);
    ok('...rises over your head before it drops', track.slice(-4).some(t => t.dy > 2.3 && t.out < 1.2), track.slice(-4).map(t => `${t.dy.toFixed(1)}/${t.out.toFixed(1)}`).join(' '));
    // (the drop: an item over your head, only yours to pick up - and standing there, it falls into your hands)
    let dropAt = null, owner = null;
    await wait(3000, async () => { dropAt = await pos(DROP); return !!dropAt || (await has('creativity_gem')) === 1; }, 50);
    if (dropAt) owner = await nbt(DROP, 'Owner');
    const me = await pos(ME), myU = await nbt(ME, 'UUID');
    ok('...and DROPS as an item just over you - its owner you', !dropAt || (Math.hypot(dropAt[0] - me[0], dropAt[2] - me[2]) < 1.5 && dropAt[1] - me[1] > 0.8 && owner === myU),
       dropAt ? `dy ${(dropAt[1] - me[1]).toFixed(2)} owner ${owner === myU}` : 'caught at once');
    ok('...picked up where you stand: the Gem is yours (the scene gone, nothing left behind)', await wait(5000, async () => (await has('creativity_gem')) === 1 && (await cnt(DROP)) === 0 && (await cnt(WAITING)) === 0 && A.chats.some(c => /drops into your hands/.test(c))) &&   // (picked up in one tick, caught the next: wait for both)
       (await cnt('@e[type=minecraft:marker,tag=bm.cgcin]')) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.cgcz]')) === 0 && (await cnt(WAITING)) === 0 &&
       A.chats.some(c => /drops into your hands/.test(c)), `gems ${await has('creativity_gem')} drop ${JSON.stringify(await pos(DROP))} me ${JSON.stringify(await pos(ME))} waiting ${await cnt(WAITING)} | ` + A.chats.slice(-2).join(' | ').slice(0, 160));
    // (it can't be lost: a drop not caught in 30 s is given to you directly - the wait run on to its end)
    await run('clear TestRat *[minecraft:custom_data~{bm:"creativity_gem"}]'); await run('tag TestRat remove bm.cgmet');
    await run(`${O}execute as TestRat at @s run function bm:p231/arrives`); await sleep(300); await run('scoreboard players set TestRat bm.cgwt 770');
    ok('...not caught in time: given directly, the scene put out', await wait(3000, async () => (await has('creativity_gem')) === 1) &&
       (await cnt('@e[type=minecraft:marker,tag=bm.cgcin]')) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.cgcz]')) === 0 && (await cnt(DROP)) === 0 &&
       (await cnt(WAITING)) === 0);
    for (const w of ['capshun', 'kettle', 'emma']) await run(`${O}execute as TestRat at @s run function bm:p98/home/${w}`);
    for (let i = 5; i < 8; i++) await run(`item replace entity TestRat hotbar.${i} with minecraft:air`);
    await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(500);
    await run('clear TestRat *[minecraft:custom_data~{bm:"creativity_gem"}]'); await run('loot replace entity TestRat hotbar.7 loot bm:items/creativity_gem');
    await use(7); await sleep(1500);
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, fx, PET, zom, X, Y, Z, sleep, at, has, score, entOf, sneakMenu, use }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.cq${o} ${v}`);
    const calm = async () => { for (const o of ['gc', 'rc', 'mc', 'k']) await cd(o, 900); };
    const hp = async (t) => num(`@e[tag=${t},limit=1]`, 'Health');
    const HEAD = '@e[type=minecraft:item_display,tag=bm.cgp_head,tag=bm.cgp_pet,limit=1]';
    const face = async () => await nbt(HEAD, 'item.components."minecraft:custom_model_data".strings[0]');
    await run(`${O}time set noon`); await calm();
    // (3.0a) its halo's glints - the white squares - circle it without stopping: a glint's spot (the halo turned by its right_rotation),
    // sampled over a few seconds, goes on round, the same way, at the same distance from the gem
    const HALO = '@e[type=minecraft:item_display,tag=bm.cgp_halo,tag=bm.cgp_pet,limit=1]';
    const glint = async () => { const m = (await nbt(HALO, 'transformation.right_rotation')).match(/(-?[\d.E-]+)f?, (-?[\d.E-]+)f?, (-?[\d.E-]+)f?, (-?[\d.E-]+)f?/);
      if (!m) return null; const [, y, , w] = m.slice(1).map(Number); const a = 2 * Math.atan2(y, w); return { a: a * 180 / Math.PI, x: 0.45 * Math.cos(a), z: -0.45 * Math.sin(a) }; };
    const gl = []; for (let i = 0; i < 7; i++) { const g = await glint(); if (g) gl.push(g); await sleep(600); }
    const steps = gl.slice(1).map((g, i) => { let d = g.a - gl[i].a; while (d > 180) d -= 360; while (d < -180) d += 360; return d; });
    ok('its halo (the white squares) circles it without stopping - the glint\'s spot goes round, one way', gl.length === 7 &&
       steps.every(d => d * Math.sign(steps[0]) > 10) && Math.abs(steps.reduce((a, b) => a + b, 0)) > 150 && gl.every(g => Math.abs(Math.hypot(g.x, g.z) - 0.45) < 0.01),
       gl.map(g => `(${g.x.toFixed(2)},${g.z.toFixed(2)})`).join(' '));
    ok('no line of text floats over it any more (its face is on the gem)', (await cnt('@e[type=minecraft:text_display,tag=bm.cgemo]')) === 0);
    ok('...an emoticon lit on its face, now and then (out of a fight)', await wait(15000, async () => /m_/.test(await face())), await face());
    await zom(2.0, 0, 'bm.trps'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trps] ~1.4 ~ ~`); await cd('mc', 0);
    ok('PRISM - a foe beside it: a flash off its facets', await wait(5000, async () => (await hp('bm.trps')) < 300));
    ok('...and in a fight its face says so, on its facet (>:( >:o :|)', await wait(4000, async () => /m_(angry|shout|flat)/.test(await face())), await face());
    await run(`${O}kill @e[tag=bm.trpz]`); await calm();
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); await zom(9, 0, 'bm.trpp'); await cd('rc', 0);
    ok('CONJURE - a foe 9 off: one of its Buddies pops out of a sparkle at it', await wait(6000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.cgbdm]')) >= 1));
    ok('...the Buddy strikes', await wait(5000, async () => (await hp('bm.trpp')) < 300));
    ok('...and goes', await wait(8000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.cgbdm]')) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.cgbdp]')) === 0));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true');
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z}`); for (const [dx, dz] of [[4, 0], [4, 2], [4, -2]]) await zom(dx, dz, 'bm.trpm'); await cd('gc', 0);
    ok('MASTERPIECE - three foes: three Buddies at once', await wait(8000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.cgbdm]')) >= 2));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await sleep(4000);
    await at(X + 0.5, Y + 1, Z - 1.5, 0, 10); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 0.5}`); await sleep(800);
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await cd('k', 0);
    ok('INSPIRATION - out of a fight beside you: Haste and Luck', await wait(7000, async () => /haste/.test(await fx()) && /luck/.test(await fx())));
    await run('effect clear TestRat'); await run('effect give TestRat minecraft:resistance 900 4 true'); await calm();

    // ---------------------------------------------------------------- (3.0a) ITS FORMS: the Ethereal Gem, the Wraithfire Heart
    const HIT = '@e[type=minecraft:interaction,tag=bm.cghit,limit=1]';
    const PART = (p) => `@e[type=minecraft:item_display,tag=bm.cgp_pet,tag=bm.cgp_${p},tag=!bm.cgfade,limit=1]`;
    const mdl = async (p) => (await nbt(PART(p), 'item.components."minecraft:item_model"')).replace(/"/g, '');
    const all = async (sfx) => { const m = []; for (const p of ['body', 'head', 'halo', 'wing_r', 'wing_l']) m.push(await mdl(p)); return { ok: m.every((x, i) => x === `bm:cg_${['body', 'head', 'halo', 'wing_r', 'wing_l'][i]}${sfx}`), m: m.join(' ') }; };
    const click = async (slot, sneak = false) => {
      await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 2.3}`); await at(X + 0.5, Y + 1, Z + 0.5, 0, 25); await sleep(400);
      const hb = await entOf(HIT); A.slot(slot); await sleep(300);
      if (sneak) { A.input({ shift: true }); await sleep(250); }
      if (hb) A.interact(hb.entityId, sneak); await sleep(700);
      if (sneak) { A.input({}); await sleep(200); }
      return !!hb; };
    await run('scoreboard players set TestRat bm.cgel 0'); await run('scoreboard players set TestRat bm.cgfo 0');
    for (const i of ['ethereal_gem', 'wraithfire_heart']) await run(`clear TestRat *[minecraft:custom_data~{bm:"${i}"}]`);
    ok('ITS FORMS - in its own form: its own models, the wings a speck', (await all('')).ok, (await all('')).m);
    await run('loot replace entity TestRat hotbar.5 loot bm:items/ethereal_gem'); A.chats.length = 0; A.bars.length = 0;
    ok('...right-clicked holding the Ethereal Gem: it keeps it (yours no more; bm.cgel 10, worn)',
       await click(5) && (await score('bm.cgel')) === 10 && (await score('bm.cgfo')) === 1 && (await has('ethereal_gem')) === 0 && A.chats.some(c => /knows this light/.test(c)),
       `cgel ${await score('bm.cgel')} gems ${await has('ethereal_gem')}`);
    ok('...the two resonate - then its parts are the Ethereal twins (the wings too)', await wait(4000, async () => (await all('_e')).ok), (await all('_e')).m);
    ok('...the wings unfold (shown, full size)', await wait(2500, async () => (await num(PART('wing_r'), 'transformation.scale[0]')) > 0.7 && (await num(PART('wing_l'), 'transformation.scale[0]')) > 0.7),
       String(await num(PART('wing_r'), 'transformation.scale[0]')));
    ok('...ETHEREAL FORM said, and a cheer on its face (\\o/ - its emoticons work in the form)', A.bars.some(b => /ETHEREAL FORM/.test(b)) &&
       await wait(3000, async () => /m_(cheer|stars|heart)/.test(await nbt(PART('head'), 'item.components."minecraft:custom_model_data".strings[0]'))), A.bars.slice(-1).join(''));
    await calm(); await zom(1.6, 2, 'bm.trpe'); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z + 2.3}`); await run(`${O}tp @e[tag=bm.trpe] ${X + 1.9} ${Y + 1} ${Z + 2.3}`); await cd('mc', 0);
    ok('...its PRISM in the form hits harder (7, not 5)', await wait(5000, async () => (await hp('bm.trpe')) < 300) && (await hp('bm.trpe')) <= 294, String(await hp('bm.trpe')));
    await run(`${O}kill @e[tag=bm.trpz]`); await calm(); await sleep(1500);
    ok('the menu, while it holds one: Ethereal Form: on / off, Take back the Ethereal Gem', await sneakMenu(0) &&
       A.buttons().some(b => /Ethereal Form: on \/ off/.test(b.label)) && A.buttons().some(b => /Take back the Ethereal Gem/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
    await A.press(/Ethereal Form: on \/ off/); await sleep(1200);
    ok('...Ethereal Form: off - its own models again (the gem kept)', (await score('bm.cgfo')) === 0 && (await score('bm.cgel')) === 10 && (await all('')).ok, (await all('')).m);
    await sneakMenu(0); await A.press(/Ethereal Form: on \/ off/); await sleep(1200);
    ok('...and on - the Ethereal twins', (await score('bm.cgfo')) === 1 && (await all('_e')).ok, (await all('_e')).m);
    await sneakMenu(0); await A.click(/Send .* home/); await sleep(1200); await use(0); await wait(4000, async () => (await cnt(PET)) === 1); await sleep(1500);
    ok('...sent home and called again: still Ethereal', (await cnt(PET)) === 1 && (await all('_e')).ok, (await all('_e')).m);
    await run('loot replace entity TestRat hotbar.5 loot bm:items/wraithfire_heart'); A.chats.length = 0;
    ok('handed a Wraithfire Heart: it keeps that one, and gives the Ethereal Gem back (one at a time)',
       await click(5) && (await score('bm.cgel')) === 11 && (await has('wraithfire_heart')) === 0 && (await has('ethereal_gem')) === 1, `cgel ${await score('bm.cgel')}`);
    ok('...the Wraithfire twins - smoke and soul fire, wings of flame', await wait(4000, async () => (await all('_w')).ok), (await all('_w')).m);
    await sleep(1500); await run('clear TestRat *[minecraft:custom_data~{bm:"ethereal_gem"}]');
    ok('sneak + right-click it empty-handed: the heart back, its own self again',
       await click(8, true) && (await score('bm.cgel')) === 0 && (await has('wraithfire_heart')) === 1 && await wait(2000, async () => (await all('')).ok), (await all('')).m);
    await sneakMenu(0);
    ok('...and its menu has no form buttons now', !A.buttons().some(b => /Form: on|Take back the/.test(b.label)), A.buttons().map(b => b.label).join(' | '));
    await run('clear TestRat *[minecraft:custom_data~{bm:"wraithfire_heart"}]'); await sleep(800);
  } });

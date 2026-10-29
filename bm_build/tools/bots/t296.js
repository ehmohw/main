// 2.98: THE GEM OF CREATIVITY, as a regular (non-op) player - the owner's checklist (rigpet_t). It comes to you when the Creative
// Spark forms: Mr. Capshun, Kettle and Emma called with their own items (real uses) - and down out of the sky, once, comes the Gem
// (3.0a: a scene - high above, a slow spiral down, twice round you, up over your head, and it DROPS into your hands; its halo always circling).
// Its ways: CONJURE (a foe within 14: one of its 3D Buddies pops out of a sparkle at it, its own attack), PRISM (a foe close: a flash
// off its facets), INSPIRATION (out of a fight: Haste and Luck for you), MASTERPIECE (three foes: three Buddies at once). It feels in
// text - an emoticon on its face (2.96a: lit on its table facet - :) c: :o :3 o3o ^-^ ;( o.O ...): >:( in a fight. Then the shared list.
const runT = require('./rigpet_t');
runT({ W: 'gem', NAME: 'The Gem of Creativity', ab: 'cg', q: 'cq', pfx: 'p231', prefix: 'cg_', item: 'creativity_gem', parts: 3, figParts: 3, hp: 40, X: 17400, Z: 17600, pron: 'it',
  called: /floats down to you/, home: /twinkles goodbye/, sit: /settles low and dims/, stand: /lifts and brightens/,
  ways: ['Conjure', 'Prism', 'Inspiration', 'Masterpiece', 'Creative Forms'],
  plain: 'Its own colours', looks: ['Ruby Facets', 'Sapphire Facets', 'Amethyst Facets'], lookPart: 'body',
  encounter: async ({ A, run, ok, wait, O, cnt, has, X, Y, Z, sleep, use }) => {
    for (const t of ['bm.mzmet', 'bm.ktmet', 'bm.emmet']) await run(`tag TestRat add ${t}`);
    for (const o of ['bm.mzcd', 'bm.ktcd', 'bm.emcd']) await run(`scoreboard players set TestRat ${o} 0`);
    await run('advancement revoke TestRat only bm:story/trio_creative_spark');
    const items = ['capshun_pencil', 'kettle_plane', 'emma_ribbon'];
    for (const [i, iid] of items.entries()) await run(`loot replace entity TestRat hotbar.${i + 5} loot bm:items/${iid}`);
    A.chats.length = 0;
    for (let i = 0; i < 3; i++) { await use(i + 5); await sleep(2200); }
    const here = [await cnt('@e[type=minecraft:wolf,tag=bm.mzpet]'), await cnt('@e[type=minecraft:wolf,tag=bm.ktpet]'), await cnt('@e[type=minecraft:cat,tag=bm.emmapet]')];
    ok('Mr. Capshun, Kettle and Emma called with their own items', here.every(n => n >= 1), here.join(','));
    // (3.0a) THE SCENE: high in the sky, a slow spiral down, twice round you at shoulder height, up over your head - and the Gem DROPS
    const pos = async (sel) => { const m = (await nbt(sel, 'Pos')).match(/\[(-?[\d.]+)d?, (-?[\d.]+)d?, (-?[\d.]+)d?\]/); return m ? m.slice(1).map(Number) : null; };
    const GEM = '@e[type=minecraft:item_display,tag=bm.cgcz_body,limit=1]', DROP = '@e[type=minecraft:item,tag=bm.cgdrop,limit=1]', ME = '@a[name=TestRat,limit=1]';
    ok('...together, the Creative Spark: the Gem shines high in the sky, its scene begins', await wait(6000, async () => (await cnt('@e[type=minecraft:marker,tag=bm.cgcin]')) === 1) &&
       A.chats.some(c => /A swirl of every colour comes down out of the sky/.test(c)), A.chats.slice(-3).join(' | ').slice(0, 200));
    ok('...nothing given yet - the drop is the reward', (await has('creativity_gem')) === 0 && (await cnt(`${ME}[tag=bm.cgwait]`)) === 1);
    const track = [];                                   // (dy above the player, out from them, angle round them)
    for (let i = 0; i < 60 && (await cnt(GEM)) === 1; i++) {
      const g = await pos(GEM), p = await pos(ME); if (!g || !p) break;
      track.push({ dy: g[1] - p[1], out: Math.hypot(g[0] - p[0], g[2] - p[2]), ang: Math.atan2(g[2] - p[2], g[0] - p[0]) * 180 / Math.PI });
      await sleep(180);
    }
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
    ok('...picked up where you stand: the Gem is yours (the scene gone, nothing left behind)', await wait(5000, async () => (await has('creativity_gem')) === 1 && (await cnt(DROP)) === 0) &&
       (await cnt('@e[type=minecraft:marker,tag=bm.cgcin]')) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.cgcz]')) === 0 && (await cnt(`${ME}[tag=bm.cgwait]`)) === 0 &&
       A.chats.some(c => /drops into your hands/.test(c)), A.chats.slice(-2).join(' | ').slice(0, 160));
    // (it can't be lost: a drop not caught in 30 s is given to you directly - the wait run on to its end)
    await run('clear TestRat *[minecraft:custom_data~{bm:"creativity_gem"}]'); await run('tag TestRat remove bm.cgmet');
    await run(`${O}execute as TestRat at @s run function bm:p231/arrives`); await sleep(300); await run('scoreboard players set TestRat bm.cgwt 770');
    ok('...not caught in time: given directly, the scene put out', await wait(3000, async () => (await has('creativity_gem')) === 1) &&
       (await cnt('@e[type=minecraft:marker,tag=bm.cgcin]')) === 0 && (await cnt('@e[type=minecraft:item_display,tag=bm.cgcz]')) === 0 && (await cnt(DROP)) === 0 &&
       (await cnt(`${ME}[tag=bm.cgwait]`)) === 0);
    for (const w of ['capshun', 'kettle', 'emma']) await run(`${O}execute as TestRat at @s run function bm:p98/home/${w}`);
    for (let i = 5; i < 8; i++) await run(`item replace entity TestRat hotbar.${i} with minecraft:air`);
    await run(`${O}tp TestRat ${X + 0.5} ${Y + 1} ${Z + 0.5} 0 0`); await sleep(500);
    await run('clear TestRat *[minecraft:custom_data~{bm:"creativity_gem"}]'); await run('loot replace entity TestRat hotbar.7 loot bm:items/creativity_gem');
    await use(7); await sleep(1500);
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, fx, PET, zom, X, Y, Z, sleep, at }) => {
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
  } });

// 2.87: THE ARACHNO-LANTERN, the hidden mount, as a regular (non-op) player - the owner's checklist (rigpet_t): HARD MODE ONLY -
// the great Lantern falls: a Kindled Gourd in its embers; used, it cracks and the little one unfolds; right-clicked with the gourd,
// it's yours. Its fight (EMBER BITE, TONGUE LASH, STOMP, EMBER RAIN); then RIDING it from its menu - it strides where you look, LEAPS,
// and from the saddle the gourd is THE GLARE; sneak to get off. Then the shared list.
const runT = require('./rigpet_t');
runT({ W: 'lantern', NAME: 'The Arachno-Lantern', ab: 'ln', q: 'lj', pfx: 'p194', prefix: 'ln_', item: 'ln_gourd', parts: 11, hp: 80, X: 16860, Z: 16000, pron: 'it',
  called: /scuttles over/, home: /sinks into the embers/, sit: /settles, glowing low/, stand: /unfolds its legs and stands/,
  ways: ['Riding', 'The Glare', 'Ember Bite', 'Tongue Lash', 'Stomp', 'Ember Rain', 'Hallowfire'],
  plain: 'Its own pumpkin orange', looks: ['Ghost Gourd', 'Soulfire Rind', 'Harvest Moon'],
  encounter: async ({ A, run, ok, wait, O, cnt, at, entOf, num, has, use, X, Y, Z, ENC, sleep }) => {
    // (the stage: the great Lantern has just fallen beside TestRat - its reward runs as each player near)
    await at(X + 0.5, Y + 1, Z + 0.5, 0, 10); A.chats.length = 0;
    await run('execute as TestRat at @s run function bm:p82/reward'); await sleep(600);
    ok('the Scorching Arachno-Lantern falls in hard mode: a Kindled Gourd in its embers', (await has('ln_gourd')) === 1 && A.chats.some(c => /Kindled Gourd!/.test(c)),
       A.chats.slice(-1).join('').slice(0, 160));
    await run('clear TestRat'); await run('loot replace entity TestRat hotbar.0 loot bm:items/ln_gourd');
    A.chats.length = 0; await use(0); await sleep(800);
    ok('the gourd used: it cracks, and the little one unfolds out of it (its rig and a click box)', await wait(5000, async () => (await cnt(ENC)) === 1) &&
       (await cnt('@e[type=minecraft:item_display,tag=bm.lnencp]')) === 11 && A.chats.some(c => /gourd cracks/.test(c)), A.chats.slice(-1).join('').slice(0, 160));
    const ex = await num(ENC, 'Pos[0]'), ez = await num(ENC, 'Pos[2]');
    await at(ex + 0.5, Y + 1, ez - 2.5, 0, 10);
    let eb = null; await wait(5000, async () => (eb = await entOf(ENC)) != null, 250); A.slot(8); await sleep(250);
    A.bars.length = 0; if (eb) A.interact(eb.entityId); await sleep(900);
    ok('right-clicked empty-handed: it looks for the gourd', A.bars.some(b => /looks at your empty hand/.test(b)), A.bars.slice(-1).join(''));
    A.slot(0); await sleep(300);
    A.chats.length = 0; eb = await entOf(ENC); if (eb) A.interact(eb.entityId); await sleep(1500);
    ok('right-clicked holding the gourd: it climbs into its light - and it\'s yours (the gourd kept)', (await has('ln_gourd')) === 1 && A.chats.some(c => /sunbeam/.test(c)),
       A.chats.slice(-2).join(' | ').slice(0, 200));
  },
  abilities: async ({ A, run, ok, wait, O, cnt, nbt, num, score, fx, PET, zom, X, Y, Z, sleep, use, sneakMenu, at }) => {
    const cd = async (o, v) => run(`scoreboard players set ${PET} bm.lj${o} ${v}`);
    for (const o of ['gc', 'bc', 'rc', 'mc']) await cd(o, 900);
    await zom(2.5, 0, 'bm.trpr'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trpr] ~2 ~ ~`); await cd('mc', 0);
    ok('EMBER BITE - the foe hurt, and burning', await wait(5000, async () => (await num('@e[tag=bm.trpr,limit=1]', 'Health')) < 300 && (await num('@e[tag=bm.trpr,limit=1]', 'Fire')) > 0));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('mc', 900);
    await run(`${O}tp ${PET} ${X} ${Y + 1} ${Z} 0 0`); await zom(0, 9, 'bm.trpl'); await cd('rc', 0);
    ok('TONGUE LASH - a foe 9 off: dragged in close', await wait(6000, async () => (await cnt(`@e[tag=bm.trpl,x=${X},y=${Y + 1},z=${Z},distance=..4]`)) === 1));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('rc', 900); await run(`${O}tp ${PET} ${X + 1.5} ${Y + 1} ${Z + 0.5}`);
    await zom(3, 1, 'bm.trps'); await run(`${O}execute at ${PET} run tp @e[tag=bm.trps] ~2 ~ ~1`); await run(`${O}data merge entity @e[tag=bm.trps,limit=1] {NoAI:0b}`); await cd('bc', 0);
    ok('STOMP - a foe close: thrown up, burning', await wait(6000, async () => (await num('@e[tag=bm.trps,limit=1]', 'Pos[1]')) > Y + 1.6 || ((await num('@e[tag=bm.trps,limit=1]', 'Health')) < 300 && (await num('@e[tag=bm.trps,limit=1]', 'Fire')) > 0)));
    await run(`${O}kill @e[tag=bm.trpz]`); await cd('bc', 900);
    await zom(6, 3, 'bm.trpe'); await zom(6, -3, 'bm.trpe'); await cd('gc', 0);
    ok('EMBER RAIN - every foe within 12 burned', await wait(8000, async () => (await cnt('@e[tag=bm.trpe,nbt={Health:300.0f}]')) === 0));
    await sleep(2000); await run(`${O}kill @e[tag=bm.trpz]`); await cd('gc', 900);
    ok('HALLOWFIRE - fire can\'t hurt you beside it', await wait(3000, async () => /fire_resistance/.test(await fx())));
    // ---- RIDING: from its menu; it strides where you look; it leaps; the gourd from the saddle is the Glare; sneak - off
    await at(X + 0.5, Y + 1, Z - 7.5, 0, 0); await run(`${O}tp ${PET} ${X + 0.5} ${Y + 1} ${Z - 6.5} 0 0`); await sleep(500);
    await sneakMenu(0); const pr = await A.press(/^Ride/);
    const riding = async () => /lnpet/.test(await run('execute as TestRat on vehicle run tag @s list'));
    ok('its menu -> Ride: on its back', !!pr && await wait(3000, riding));
    A.ride(0, 0, {}); await sleep(600);
    const z0 = await num(PET, 'Pos[2]');
    A.ride(0, 0, { forward: true }); await sleep(600); A.ride(0, 0, {}); await sleep(400);
    const z1 = await num(PET, 'Pos[2]');
    ok('walk: it strides where you look (south)', z1 - z0 > 2.5, `z ${z0.toFixed(1)} -> ${z1.toFixed(1)}`);
    let top = -1e9; A.ride(0, 0, { jump: true }); for (let k = 0; k < 10; k++) { top = Math.max(top, await num(PET, 'Pos[1]')); await sleep(80); } A.ride(0, 0, {});
    ok('jump: it LEAPS', top > Y + 2.2, `top ${top.toFixed(2)}`);
    await sleep(1500);
    // (the foe set 5 ahead of the rider, at ground level under its gaze - looking a little down)
    const px = await num('TestRat', 'Pos[0]'), pz = await num('TestRat', 'Pos[2]');
    await run(`${O}summon minecraft:husk ${px.toFixed(1)} ${Y + 1} ${(pz + 5).toFixed(1)} {NoAI:1b,PersistenceRequired:1b,Tags:["bm.trpz","bm.trpg","bm.seen"],attributes:[{id:"minecraft:max_health",base:300}],Health:300f}`);
    A.ride(0, 20, {}); await sleep(500); const rid = await riding(); await use(0); await sleep(800);
    ok('the gourd from the saddle: THE GLARE - the foe ahead burned', (await num('@e[tag=bm.trpg,limit=1]', 'Health')) < 300 && (await num('@e[tag=bm.trpg,limit=1]', 'Fire')) > 0,
       `riding ${rid} health ${await num('@e[tag=bm.trpg,limit=1]', 'Health')}`);
    A.ride(0, 0, { shift: true }); await sleep(800); A.ride(0, 0, {}); await sleep(300);
    ok('sneak: off its back', await wait(3000, async () => !(await riding())));
    A.unride(); A.stand(); await sleep(800);
    await run(`${O}kill @e[tag=bm.trpz]`);
  } });
